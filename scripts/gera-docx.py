#!/usr/bin/env python3
# gera-docx.py — gera a "Especificação Funcional" (.docx) de um Feature Set (N2 + seus N3),
# de forma PADRONIZADA, preenchendo o template PHL (scripts/templates/…docx).
#
# Uso (a partir da raiz do repositório):
#   python3 scripts/gera-docx.py --all                 # todos os feature sets com N3
#   python3 scripts/gera-docx.py modules/.../faq       # um feature set (pasta do N2)
#
# Saída: documentos/<SIGLA_N2>.docx  (+ documentos/_diagramas/<SIGLA_N2>.png, se renderizado)
#
# ESCOPO: canônico no engine desde 2026-09-30 (trazido do portal-compras); chega às
# instâncias pelo sync-instance, com o template e as fontes de scripts/templates/.
# A geração é SOB DEMANDA — o .docx é entrega, não artefato de build: rode-o local,
# com navegador, ou pelo workflow engine/templates/.github/workflows/gera-docx.yml
# (só `workflow_dispatch`), copiado à mão para .github/workflows/ da instância.
#
# Diagrama da Jornada: renderiza o bloco ```mermaid do N2 via Chromium headless, se
# houver um no PATH/PLAYWRIGHT_BROWSERS_PATH; senão reaproveita o PNG em cache; senão
# cai para uma lista textual dos passos. Assim o script roda com ou sem navegador.
import os, re, sys, html, glob, subprocess, unicodedata, zipfile, hashlib, json

ROOT      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE  = os.path.join(ROOT, "scripts", "templates", "especificacao-funcional.docx")
OUT_DIR   = os.path.join(ROOT, "documentos")
DIAG_DIR  = os.path.join(OUT_DIR, "_diagramas")
MERMAIDJS = os.path.join(ROOT, "assets", "vendor", "mermaid.min.js")
GRID, TEAL = 9628, "00B4C8"
ASPECT_MAX_H_IN = 7.4

def rd(p):
    try: return open(p, encoding="utf-8").read()
    except Exception: return ""

# nome do sistema (nó de topo): o `**Nome**` do global/MASTER.md, a fonte única da
# identidade (decisão de 2026-09-30); com o MASTER ainda em placeholder, o config.js do
# visualizador. Os dois divergem nas instâncias ("Portal de Compras" × "Portal Compras"),
# e o documento entregue leva o nome por extenso, o do MASTER.
_nome_master = re.search(r"^-\s+\*\*Nome\*\*:\s*([^\[\n].*?)\s*$", rd(os.path.join(ROOT, "global", "MASTER.md")), re.M)
_nome_config = re.search(r'name:\s*"([^"]+)"', rd(os.path.join(ROOT,"assets/js/config.js")))
NOME_SISTEMA  = (_nome_master or _nome_config or [None, "Documentação"])[1]
# Sigla do sistema: vem do ambiente (é o que os workflows passam). Sem ela, tenta o
# `**Sigla**` do global/MASTER.md e, não achando, ABORTA — o default antes era a sigla
# de uma instância específica, então rodar noutra marcava o documento com o sistema
# errado, em silêncio. Documento com a sigla errada é pior que documento não gerado.
def _sigla_do_master():
    # 2 a 6 letras: a sigla do transparencia-web é `TW`, e a faixa antiga (3–6) a
    # rejeitava — sem casar, o gerador ABORTA, que é o comportamento certo para
    # sigla ausente e o errado para sigla curta.
    m = re.search(r"^-\s+\*\*Sigla\*\*:\s*`?([A-Z]{2,6})`?\b",
                  rd(os.path.join(ROOT, "global", "MASTER.md")), re.M)
    return m.group(1) if m else None

AUTOR_DOCUMENTO = os.environ.get("AUTOR_DOCUMENTO", "PHL TI")  # coluna Autor do Histórico de Versões
SIGLA_SISTEMA = os.environ.get("SIGLA_SISTEMA") or _sigla_do_master()
if not SIGLA_SISTEMA:
    sys.exit("✗ Sigla do sistema indefinida. Passe SIGLA_SISTEMA=XXXXX ou declare "
             "`- **Sigla**: XXXXX` em global/MASTER.md.")

# ─────────────────────────── parsing de markdown ───────────────────────────
def section(md, title):
    m = re.search(r'^##\s+'+re.escape(title)+r'\s*\n(.*?)(?=\n##\s|\n---\s*\n|\Z)', md, re.S|re.M)
    return m.group(1).strip() if m else ""
def clean_md(s):
    s = re.sub(r'<small>.*?</small>', '', s)
    s = re.sub(r'\[\*\*(.*?)\*\*\]\([^)]*\)', r'\1', s)
    s = re.sub(r'\[(.*?)\]\([^)]*\)', r'\1', s)
    s = s.replace('**','').replace('`','')
    return re.sub(r'\s+', ' ', s).strip()
def md_table(block):
    rows=[]
    for line in block.splitlines():
        line=line.strip()
        if not line.startswith('|'): continue
        cells=[c.strip() for c in line.strip('|').split('|')]
        if all(re.fullmatch(r':?-{2,}:?', c or '-') for c in cells): continue
        rows.append([clean_md(c) for c in cells])
    return rows
def md_tables(block):
    """Cada tabela markdown da seção, em separado — `[(subtítulo, linhas), …]`.

    `md_table()` achata TODAS as linhas `|` da seção numa lista só. Numa seção com
    duas tabelas de larguras diferentes (a matriz de perfis e a de visibilidade por
    natureza da etapa) isso produzia uma única tabela Word: a segunda entrava como
    linhas da primeira, espremida nas colunas dela.
    """
    out, atual, sub = [], [], None
    for line in (block or "").splitlines():
        s = line.strip()
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if not all(re.fullmatch(r":?-{2,}:?", c or "-") for c in cells):
                atual.append([clean_md(c) for c in cells])
            continue
        if atual:
            out.append((sub, atual)); atual, sub = [], None
        m = re.match(r"^#{3,4}\s+(.+?)\s*$", s)
        if m:
            sub = clean_md(m.group(1))
    if atual:
        out.append((sub, atual))
    return [(s, r) for s, r in out if len(r) > 1]

def widths_por_conteudo(linhas, grid=None):
    """Larguras proporcionais ao conteúdo, amortecidas pela raiz.

    A regra anterior dava 4628 (quase metade da grade) à primeira coluna, qualquer
    que fosse o número de colunas: numa tabela de 8, sobravam ~714 por coluna e os
    cabeçalhos quebravam em quatro linhas. A raiz evita o extremo oposto — uma
    célula muito longa não engole a tabela inteira.
    """
    grid = grid or GRID
    n = len(linhas[0])
    tam = [max((len(r[i]) if i < len(r) else 0) for r in linhas) or 1 for i in range(n)]
    peso = [max(t, 4) ** 0.5 for t in tam]
    total = sum(peso)
    w = [max(int(grid * x / total), 700) for x in peso]
    w[-1] += grid - sum(w)          # a última absorve o arredondamento
    return w

def numbered(block):
    return [(m.group(1), clean_md(m.group(2))) for line in block.splitlines()
            if (m:=re.match(r'^\s*(\d+)\.\s+(.*)$', line))]
def notes(block):
    return [clean_md(l) for l in block.splitlines()
            if l.strip().startswith('⚠️') or l.strip().startswith('*')]
# ─────────────── regra citada por remissão: o documento leva a regra original ────────
# Um N3 que cita a regra de outro artefato — "→ ver N1 Registro de Preços: Regras
# transversais de negócio: 3" ou "→ ver PUB-REL-01 Consultar Relatório de Carga: Regras
# de negócio: 2" — costuma trazer só um RESUMO dela: o texto completo mora na origem, e
# quem lê a spec chega lá pelo link. Quem lê o .docx não chega. Por isso a Especificação
# Funcional leva a regra ORIGINAL no lugar do resumo, e a remissão some — nem "ver N1…"
# nem número de regra de outro documento. Regra comum às três instâncias (2026-09-23);
# índice em documentos/README.md, "Regras de exportação".
#
# Um intervalo ("6 a 9") vira as regras citadas, uma após a outra, na mesma linha. O que
# vem DEPOIS da remissão (uma nota ⚠️, por exemplo) é preservado. Alvo que não existe:
# fica o texto do N3 sem a remissão, e o console avisa — o documento não pode sair com
# um "ver N1…" que não leva a lugar nenhum, nem com uma regra inventada.
REF_REGRA = re.compile(
    r'\s*→\s*ver\s+(?:N1\s+(?P<dom>[^:]+?)\s*:\s*Regras transversais de negócio'
    r'|(?P<fid>[A-Z]{3}-[A-Z]{3}-\d{2})\s+[^:]*?:\s*Regras de negócio)'
    r'\s*:\s*(?P<ini>\d+)(?:\s*(?:a|–|-)\s*(?P<fim>\d+))?\.?')

def _chave(txt):
    t = unicodedata.normalize("NFD", txt)
    return re.sub(r'\s+', ' ', "".join(c for c in t if unicodedata.category(c) != "Mn")).strip().lower()

_REGRAS_CITAVEIS = {}   # ("n1", domínio) / ("n3", ID) -> {nº: texto}; lido uma vez por execução

def _regras_do_n1(dominio):
    k = ("n1", _chave(dominio))
    if k not in _REGRAS_CITAVEIS:
        achado = {}
        for f in glob.glob(os.path.join(ROOT, "modules", "*", "README.md")):
            md = rd(f)
            h = re.search(r'^#\s*(?:Major Feature Set|Dom[ií]nio):\s*(.+)$', md, re.M)  # 3.0.0 + legado
            if h and _chave(h.group(1)) == k[1]:
                achado = {int(n): t for n, t in numbered(section(md, "Regras transversais de negócio"))}
                break
        _REGRAS_CITAVEIS[k] = achado
    return _REGRAS_CITAVEIS[k]

def _regras_do_n3(fid):
    k = ("n3", fid)
    if k not in _REGRAS_CITAVEIS:
        achado = {}
        for f in glob.glob(os.path.join(ROOT, "modules", "**", "f-*.md"), recursive=True):
            md = rd(f)
            if re.search(r'^id:\s*' + re.escape(fid) + r'\s*$', md, re.M):
                achado = {int(n): t for n, t in numbered(section(md, "Regras de negócio"))}
                break
        _REGRAS_CITAVEIS[k] = achado
    return _REGRAS_CITAVEIS[k]

def regra_original(texto, origem="", _nivel=0):
    """Texto de uma regra do N3 pronto para o .docx: cada remissão a regra de outro
    artefato é trocada pelo texto da(s) regra(s) citada(s), e o resumo que a precedia
    sai. Sem remissão, devolve o texto como veio."""
    partes, pos = [], 0
    for m in REF_REGRA.finditer(texto):
        resumo = texto[pos:m.start()].strip()
        if m.group('dom'):
            fonte, rotulo = _regras_do_n1(m.group('dom')), f"N1 {m.group('dom').strip()}"
        else:
            fonte, rotulo = _regras_do_n3(m.group('fid')), m.group('fid')
        ini = int(m.group('ini')); fim = int(m.group('fim') or ini)
        citadas = [fonte[n] for n in range(ini, fim + 1) if n in fonte]
        if citadas and len(citadas) == fim - ini + 1:
            original = " ".join(citadas)
            if _nivel < 2:                       # a regra citada pode, ela mesma, citar outra
                original = regra_original(original, rotulo, _nivel + 1)
            partes.append(original)
        else:
            faixa = m.group('ini') + (f"–{m.group('fim')}" if m.group('fim') else "")
            print(f"  ⚠️  {origem}: remissão a {rotulo}, regra {faixa}, não encontrada — "
                  f"fica o texto do N3, sem a remissão")
            partes.append(resumo)
        pos = m.end()
    if not partes:
        return texto
    resto = texto[pos:].strip()
    return " ".join(p for p in partes + [resto] if p)

def gherkin(md):
    m=re.search(r'```gherkin\s*\n(.*?)```', md, re.S)
    return m.group(1).rstrip('\n').split('\n') if m else []
def mermaid(md):
    m=re.search(r'```mermaid\s*\n(.*?)```', md, re.S)
    return m.group(1).strip() if m else ""

# ── ordem das funcionalidades no documento: a do fluxo principal do N2 ──────
# O leitor percorre o documento na ordem em que usa o sistema, não na ordem em que
# os arquivos caem no `ls`. A ordem sai do bloco ```mermaid``` do N2 (o mesmo que
# vira a Jornada do Usuário): cada nó é o **nome** de uma funcionalidade, e a
# posição da primeira aparição manda. Funcionalidade que não aparece no fluxo — a
# que ainda não entrou na jornada, ou a de outro Feature Set — vai para o fim, em
# ordem de arquivo, que é estável. Nó que não casa com N3 nenhum (funcionalidade de
# outro Feature Set, início e fim da jornada) simplesmente não ordena nada.
def _norm_rotulo(t):
    t = unicodedata.normalize("NFD", t or "")
    t = "".join(c for c in t if unicodedata.category(c) != "Mn").lower()
    return re.sub(r"[^a-z0-9]+", " ", t).strip()

def ordem_do_fluxo(n2, arquivos):
    """`arquivos` (N3 do Feature Set) na ordem do fluxo principal do N2."""
    rotulos = re.findall(r'[\[\({]+"?([^"\]\)}|]+?)"?[\]\)}]+', mermaid(n2) or "")
    pos = {}
    for i, r in enumerate(_norm_rotulo(r) for r in rotulos):
        if r and r not in pos: pos[r] = i
    def chave(fn):
        titulo = _norm_rotulo((re.search(r'^#\s+(.+)$', rd(fn), re.M) or [None, ""])[1])
        p = pos.get(titulo)
        if p is None and titulo:
            # nó abreviado ou com complemento ("Enviar Solicitação de Compras (SC)").
            # A folga é curta de propósito: com contenção solta, "Cadastrar Solicitação
            # de Compras Compartilhada" casava o nó "Cadastrar Solicitação de Compras" e
            # ia para a posição da feature que o fluxo de fato cita.
            for r, i in pos.items():
                if (titulo in r or r in titulo) and min(len(titulo), len(r)) >= 0.8 * max(len(titulo), len(r)):
                    p = i; break
        return (0, p, fn) if p is not None else (1, 0, fn)
    return sorted(arquivos, key=chave)

# ─────────────────────────── helpers de WordprocessingML ───────────────────
def x(s): return html.escape(s, quote=False)
HRPR='<w:b/><w:bCs/><w:sz w:val="28"/><w:szCs w:val="28"/><w:u w:val="none"/>'  # 14pt · negrito · sem sublinhado
GKW={'Given':'Dado','When':'Quando','Then':'Então','And':'E','But':'Mas'}
KW_MUTED="6E6E6E"; _hn=[0]

def _run(text, bold=False, italic=False, color=None):
    rpr=""
    if bold: rpr+="<w:b/><w:bCs/>"
    if italic: rpr+="<w:i/><w:iCs/>"
    if color: rpr+=f'<w:color w:val="{color}"/>'
    rpr=f"<w:rPr>{rpr}</w:rPr>" if rpr else ""
    return f'<w:r>{rpr}<w:t xml:space="preserve">{x(text)}</w:t></w:r>'
def P(text, italic=False, size=None, bold=False, align=None):
    rpr=""
    if bold: rpr+="<w:b/><w:bCs/>"
    if italic: rpr+="<w:i/><w:iCs/>"
    if size: rpr+=f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    prpr=f"<w:rPr>{rpr}</w:rPr>" if rpr else ""
    jc=f'<w:jc w:val="{align}"/>' if align else ''
    ppr=f"<w:pPr>{jc}{prpr}</w:pPr>" if (jc or prpr) else ""
    return f'<w:p>{ppr}<w:r>{prpr}<w:t xml:space="preserve">{x(text)}</w:t></w:r></w:p>'
def _head(text, center=False, page_break=False):
    p='<w:keepNext/>'
    if page_break: p+='<w:pageBreakBefore/>'
    if center: p+='<w:jc w:val="center"/>'
    return (f'<w:p><w:pPr><w:pStyle w:val="AxureHeadingBasic"/>{p}<w:rPr>{HRPR}</w:rPr></w:pPr>'
            f'<w:r><w:rPr>{HRPR}</w:rPr><w:t xml:space="preserve">{x(text)}</w:t></w:r></w:p>')
def H(text, page_break=False):
    _hn[0]+=1
    return _head(f"{_hn[0]}. {text}", page_break=page_break)
def H_plain(text, center=False):
    return _head(text, center=center)
def FUNC(text):
    _hn[0]=0
    rpr='<w:rPr><w:b/><w:bCs/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>'
    return (f'<w:p><w:pPr><w:keepNext/><w:pageBreakBefore/>{rpr}</w:pPr>'
            f'<w:r>{rpr}<w:t xml:space="preserve">{x(text)}</w:t></w:r></w:p>')
def cell(text, w, header=False):
    rpr="<w:b/><w:bCs/>" if header else ""
    jc='<w:jc w:val="center"/>' if header else ''
    shd=f'<w:shd w:val="clear" w:color="auto" w:fill="{TEAL}"/>' if header else ''
    sp='<w:spacing w:before="120" w:after="120"/>' if header else '<w:spacing w:before="0" w:after="0"/>'
    prpr=f"<w:rPr>{rpr}</w:rPr>" if rpr else ""
    p=(f'<w:p><w:pPr>{sp}{jc}{prpr}</w:pPr><w:r>{prpr}<w:t xml:space="preserve">{x(text)}</w:t></w:r></w:p>')
    return f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>{shd}<w:vAlign w:val="center"/></w:tcPr>{p}</w:tc>'
def table(headers, rows, widths):
    if abs(sum(widths)-GRID)>=5: raise ValueError(f"grid {sum(widths)} != {GRID}")
    grid="".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    trs=[f'<w:tr><w:trPr><w:tblHeader/></w:trPr>'+"".join(cell(h,w,True) for h,w in zip(headers,widths))+'</w:tr>']
    for r in rows: trs.append('<w:tr>'+"".join(cell(c,w) for c,w in zip(r,widths))+'</w:tr>')
    tblpr=('<w:tblPr><w:tblStyle w:val="Tabelacomgrade"/><w:tblW w:w="0" w:type="auto"/>'
           '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" '
           'w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr>')
    return f'<w:tbl>{tblpr}<w:tblGrid>{grid}</w:tblGrid>{"".join(trs)}</w:tbl>'
def eq_widths(n):
    base=GRID//n; return [base]*(n-1)+[GRID-base*(n-1)]
def cenarios_paras(md):
    TT={'Scenario':'Cenário','Scenario Outline':'Esquema do Cenário','Background':'Contexto','Examples':'Exemplos'}
    out=[]
    for raw in gherkin(md):
        s=raw.strip()
        if not s or s.startswith('#') or s.startswith('Feature:'): continue
        m=re.match(r'^(Scenario Outline|Scenario|Background|Examples):?\s*(.*)$', s)
        if m:
            title=f"{TT[m.group(1)]}: {m.group(2)}" if m.group(2) else TT[m.group(1)]
            out.append(f'<w:p><w:pPr><w:spacing w:before="140" w:after="40"/></w:pPr>{_run(title,bold=True)}</w:p>'); continue
        st=re.match(r'^(Given|When|Then|And|But)\b\s*(.*)$', s)
        if st:
            out.append(f'<w:p><w:pPr><w:spacing w:before="0" w:after="0"/><w:ind w:left="454"/></w:pPr>'
                       f'{_run(GKW[st.group(1)]+" ",bold=True,color=KW_MUTED)}{_run(st.group(2))}</w:p>'); continue
        out.append(f'<w:p><w:pPr><w:spacing w:before="0" w:after="0"/><w:ind w:left="454"/></w:pPr>{_run(s)}</w:p>')
    return out
def img(cx, cy, rid="rId20", docpr=100, name="Figura"):
    A='http://schemas.openxmlformats.org/drawingml/2006/main'; PICNS='http://schemas.openxmlformats.org/drawingml/2006/picture'
    nm=x(name)
    return (f'<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing>'
            f'<wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/>'
            f'<wp:effectExtent l="0" t="0" r="0" b="0"/><wp:docPr id="{docpr}" name="{nm}"/>'
            f'<wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="{A}" noChangeAspect="1"/></wp:cNvGraphicFramePr>'
            f'<a:graphic xmlns:a="{A}"><a:graphicData uri="{PICNS}"><pic:pic xmlns:pic="{PICNS}">'
            f'<pic:nvPicPr><pic:cNvPr id="{docpr}" name="{nm}"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic>'
            f'</wp:inline></w:drawing></w:r></w:p>')
def spacer(): return '<w:p/>'

# ─────────────────────────── render do diagrama (mermaid) ───────────────────
def find_chrome():
    if os.environ.get("GERA_DOCX_NO_BROWSER"):   # CI: reusa o cache de _diagramas, sem navegador
        return None
    for env in ("PLAYWRIGHT_BROWSERS_PATH",):
        base=os.environ.get(env)
        if base:
            for pat in ("**/chrome-linux/headless_shell","**/chrome-linux/chrome","**/chrome-mac*/**/Chromium*","**/chrome"):
                for p in glob.glob(os.path.join(base,pat), recursive=True):
                    if os.access(p, os.X_OK) and os.path.isfile(p): return p
    from shutil import which
    for n in ("chromium","chromium-browser","google-chrome","google-chrome-stable","chrome"):
        p=which(n)
        if p: return p
    return None
def render_jornada(src, out_png, origem=None):
    base = os.path.splitext(out_png)[0]
    if os.path.exists(out_png):                           # cache
        if origem: _confere_fonte(base, origem, _sha_texto(src or ""), "mermaid", out_png)
        return out_png
    chrome=find_chrome()
    if not (chrome and src and os.path.exists(MERMAIDJS)): return None
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    def page(force_w=None):
        css = ".mermaid{width:%dpx}.mermaid svg{width:100%%!important;height:auto!important;display:block}"%force_w if force_w else ""
        grid=("body{background-color:#f4f8fc;background-image:linear-gradient(#d3e2f1 1px,transparent 1px),"
              "linear-gradient(90deg,#d3e2f1 1px,transparent 1px);background-size:26px 26px}.mermaid svg{background:transparent}")
        return (f"<!doctype html><meta charset=utf-8><style>html,body{{margin:0;padding:0}}{grid}{css}</style>"
                f'<div class="mermaid">{src}</div><script src="file://{MERMAIDJS}"></script><script>'
                "try{mermaid.initialize({startOnLoad:false,theme:'default',flowchart:{useMaxWidth:false,htmlLabels:true,curve:'basis'}});}catch(e){}"
                "(function(){try{(mermaid.run?mermaid.run({querySelector:'.mermaid'}):mermaid.init(undefined,'.mermaid'));}catch(e){document.title='ERR';}})();</script>")
    def run(args, cap=False):
        base=[chrome,"--no-sandbox","--disable-gpu","--disable-dev-shm-usage","--force-device-scale-factor=2"]
        return subprocess.run(base+args, capture_output=cap, text=True, timeout=90)
    h1=out_png+".p1.html"; h2=out_png+".p2.html"
    try:
        open(h1,"w").write(page())
        dom=run(["--virtual-time-budget=8000","--dump-dom",f"file://{h1}"], cap=True).stdout
        mm=re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', dom or "")
        if not mm: return None
        W,H=float(mm.group(1)),float(mm.group(2)); TW=1200; TH=round(TW*H/W)+8
        open(h2,"w").write(page(force_w=TW))
        run(["--virtual-time-budget=8000",f"--window-size={TW},{TH}",f"--screenshot={out_png}",f"file://{h2}"])
        if not os.path.exists(out_png): return None
        if origem: _grava_fonte(base, origem, _sha_texto(src or ""), "mermaid")
        return out_png
    except Exception:
        return None
    finally:
        for f in (h1,h2):
            try: os.remove(f)
            except OSError: pass
# Esta cópia leva a jornada E as telas do protótipo (ver captura abaixo); a convenção
# de protótipo desta instância é o HTML composto por Feature Set com manifesto de telas.
# ─────────────────── estados de tela que ficam fora do .docx ─────────────────
# Regra comum às três instâncias (2026-09-03): protótipo que representa o estado
# "loading", "empty" ou "error" NÃO vai para a Especificação Funcional. O documento
# entregue ao cliente mostra a tela que o usuário opera; espera, vazio e falha são
# contrato do protótipo e da regra de negócio escrita, não figura do documento.
# Vale também para as variantes em português (carregando, vazio/vazia, erro) e para o
# estado de um componente da tela (`combos-ano-vazio`). Mesmo texto nas três
# cópias — índice das regras em documentos/README.md, "Regras de exportação".
ESTADOS_FORA_DO_DOCX = ("loading", "empty", "error", "carregando", "vazio", "vazia", "erro")

def estado_fora_do_docx(nome):
    """`nome` é o que identifica a tela: o nome do arquivo do protótipo
    (`empty.html`, `combos-ano-erro.html`) ou o título do botão na barra do fluxo
    ("Erro de servidor"). Casa por palavra inteira, sem acento nem caixa — `erro`
    casa em "Erro de servidor" e em `combos-ano-erro`, mas não em "Erros de
    crítica", que é conteúdo de negócio e continua no documento."""
    t = unicodedata.normalize("NFD", os.path.splitext(os.path.basename(str(nome)))[0])
    t = "".join(c for c in t if unicodedata.category(c) != "Mn").lower()
    palavras = set(re.split(r"[^a-z0-9]+", t))
    return any(e in palavras for e in ESTADOS_FORA_DO_DOCX)

def png_size(path):
    import struct
    with open(path,"rb") as f: f.read(16); w,h=struct.unpack(">II", f.read(8))
    return w,h

# ─────────────────── captura das telas do protótipo (portal-compras) ─────────
# Convenção desta instância: um HTML composto por Feature Set, com as telas trocadas
# por JS. Um manifesto invisível `<script id="docx-telas">` no protótipo lista cada
# tela, a(s) funcionalidade(s) a que pertence e o `setup` (JS que a exibe antes da
# captura). Sem manifesto, captura-se a tela de entrada. Reaproveita o Chromium do
# render da jornada; com GERA_DOCX_NO_BROWSER (CI) usa só o cache já commitado. Telas
# de estado loading/empty/error ficam fora (estado_fora_do_docx), como nos outros dois.
PROTO_DIR = os.path.join(OUT_DIR, "_prototipos")

# ── impressão digital da fonte de cada figura ────────────────────────────────
# As duas figuras do documento saem de cache versionado e reaproveitado sem navegador:
# a TELA do protótipo (`_prototipos/`, fonte = o HTML) e a JORNADA (`_diagramas/`,
# fonte = o bloco ```mermaid``` do N2). Nenhum dos dois caches se invalida sozinho, e
# sem esta conferência a correção fica no repositório e nunca chega ao .docx — em
# silêncio, porque o documento continua sendo gerado e o diff sai vazio, que é o mesmo
# retorno de "já está em dia". Ao produzir a figura grava-se o sha256 da fonte em
# `_fontes.json`, ao lado do cache; ao reaproveitar, compara-se. Por CONTEÚDO, nunca
# por data nem por `git log`: o checkout da CI é raso e não enxerga o histórico.
FIGURAS_VELHAS = []        # [(png, origem, motivo)] — cache que não casa mais com a fonte

def _fontes_path(cache_base):
    return os.path.join(os.path.dirname(cache_base), "_fontes.json")

def _sha_arquivo(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for parte in iter(lambda: f.read(65536), b""): h.update(parte)
    return h.hexdigest()

def _sha_texto(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest()

def _le_fontes(base):
    try:
        with open(_fontes_path(base), encoding="utf-8") as f: return json.load(f)
    except Exception: return {}

def _grava_fonte(base, origem, sha, tipo):
    """`tipo` diz como reconferir depois, sem refazer a figura: `arquivo` = o sha é do
    conteúdo de `origem`; `mermaid` = é do bloco ```mermaid``` extraído de `origem`."""
    d = _le_fontes(base)
    d[os.path.basename(base)] = {"origem": origem, "sha": sha, "tipo": tipo}
    p = _fontes_path(base)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1, sort_keys=True); f.write("\n")

def _confere_fonte(base, origem, sha, tipo, alvo):
    """Anota a figura quando o cache veio de outra versão da fonte — ou de versão
    desconhecida, quando não há impressão digital gravada."""
    reg = _le_fontes(base).get(os.path.basename(base))
    if reg and reg.get("sha") == sha: return
    FIGURAS_VELHAS.append((os.path.relpath(alvo, ROOT), origem,
                           "a fonte mudou depois da figura" if reg else "figura sem impressão digital"))


def prototipo_do_n3(md):
    """Caminho do protótipo referenciado na ## Superfície do N3 ('Fidelidade ao
    protótipo … `prototypes/…html`'), ou None."""
    sup = section(md, "Superfície")
    m = re.search(r'`(prototypes/[^`]+\.html)`', sup) or re.search(r'(prototypes/[^\s)`]+\.html)', sup)
    return m.group(1) if m else None

def prototipo_do_indice(feat_id):
    """Protótipo que o manifesto `prototypes/INDEX.md` liga à feature, quando o N3 ainda
    não aponta nenhum na ## Superfície. O manifesto é a fonte de verdade do vínculo
    protótipo ↔ N3; no GPE os N3 ficaram com `Fidelidade ao protótipo: n/a` por decisão
    de 2026-10-04, e o vínculo vive só lá. Pega a 1ª linha com `` `<ID>` `` e o link
    `](./…html)` dela, sem o `#` da tela. None se não houver."""
    if not feat_id: return None
    for linha in rd(os.path.join(ROOT, "prototypes", "INDEX.md")).splitlines():
        if f"`{feat_id}`" not in linha: continue
        m = re.search(r'\]\(\./([^)#\s]+\.html)', linha)
        if m: return "prototypes/" + m.group(1)
    return None

def telas_do_manifesto(proto_abs):
    """Lê o `<script id="docx-telas">` do protótipo. Retorna a lista de telas
    (cada uma {nome, features, setup}) ou None se não houver manifesto."""
    m = re.search(r'<script[^>]*id="docx-telas"[^>]*>(.*?)</script>', rd(proto_abs), re.S)
    if not m: return None
    try:
        import json
        return json.loads(m.group(1)).get("telas", [])
    except Exception:
        return None

# Altura de página útil em px para a captura a 1280px de largura (largura útil 6,4" →
# uma página ~8,6"). Tela mais alta que isso (com folga) é fatiada em páginas.
PAGINA_ALT_PX = int(1280 * 8.6 / 6.4)   # ~1720

def _screenshot_tela(proto_abs, setup, out_png, altura=None):
    """Captura UM PNG (1280px de largura) da tela com o `setup` aplicado, a Inter e os
    ícones locais injetados, `<base href>` para os caminhos relativos resolverem e o
    andaime (`.req-toggle`/`.ds-req-toggle`) escondido. `altura` fixa a altura da janela em vez
    de medir o conteúdo. Devolve o caminho ou None."""
    chrome = find_chrome()
    if not (chrome and proto_abs and os.path.exists(proto_abs)): return None
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    # Inter vendorizada (scripts/templates/vendor/inter — vem do engine com o gerador): o
    # Chromium headless não usa o proxy do ambiente nem confia na CA dele, então o
    # `@import` remoto do Google Fonts falha e a fonte cai no fallback. Injeta a Inter
    # local e neutraliza o import remoto → captura com a fonte real, offline e determinística.
    inter_css = os.path.join(ROOT, "scripts", "templates", "vendor", "inter", "inter.css")
    font = f'<link rel="stylesheet" href="file://{inter_css}">' if os.path.exists(inter_css) else ""
    # Ícones: os protótipos que não são autocontidos carregam o Font Awesome de CDN, e a
    # captura roda sem rede — os botões só de ícone (editar, remover, visualizar, anexar)
    # saíam EM BRANCO na figura. `scripts/templates/vendor/icones-proto/icones.css` traz
    # glifos locais equivalentes (não é o Font Awesome; ver o cabeçalho daquele arquivo).
    icones_css = os.path.join(ROOT, "scripts", "templates", "vendor", "icones-proto", "icones.css")
    icones = f'<link rel="stylesheet" href="file://{icones_css}">' if os.path.exists(icones_css) else ""
    # Andaime fora da foto: `.req-toggle` nos protótipos autocontidos, `.ds-req-toggle` na
    # família que usa a biblioteca do design system. São o mesmo botão flutuante.
    css = font + icones + "<style>.req-toggle,.ds-req-toggle{display:none!important}</style>"
    js  = ("<script>window.addEventListener('load',function(){try{%s}catch(e){}"
           "(document.fonts&&document.fonts.ready?document.fonts.ready:Promise.resolve()).then(function(){"
           "setTimeout(function(){document.title='H:'+document.documentElement.scrollHeight},250);});});</script>"
           % (setup or ""))
    doc = rd(proto_abs)
    doc = re.sub(r'@import\s+url\((["\']?)https://fonts\.googleapis\.com[^)]*\1\)\s*;?', '', doc)
    # Fora também os `<link>` remotos (Google Fonts, Font Awesome de CDN): a captura não tem
    # rede, então eles só custam o tempo de espera do Chromium até desistir — a passada do
    # SDC-SOL levava ~4 min por isso. E há um efeito pior que a lentidão: numa máquina COM
    # rede eles carregariam, e a mesma tela sairia diferente. Tirando-os, a figura é a mesma
    # em qualquer ambiente, com a Inter e os ícones locais injetados logo abaixo.
    doc = re.sub(r'<link[^>]+href=["\'][^"\']*(?:fonts\.googleapis\.com|fonts\.gstatic\.com|cdnjs\.cloudflare\.com)[^"\']*["\'][^>]*>', '', doc, flags=re.I)
    # `<base href>` logo depois do `<head>`: o HTML temporário é gravado junto do PNG, em
    # documentos/_prototipos/<SIGLA>/, e sem isto os caminhos relativos do protótipo
    # (`../../_biblioteca-ds/components.js`) apontam para o lugar errado e não carregam —
    # o JS da biblioteca some e os modais nem abrem. Precisa vir ANTES dos `<link>`/
    # `<script src>` do próprio protótipo, por isso não pode ir junto do `css`.
    base = '<base href="file://%s/">' % os.path.dirname(os.path.abspath(proto_abs))
    doc = re.sub(r'<head[^>]*>', lambda m: m.group(0) + base, doc, count=1)
    doc = doc.replace("</head>", css+"</head>", 1).replace("</body>", js+"</body>", 1)
    tmp = out_png + ".tmp.html"
    def run(args, cap=False):
        base=[chrome,"--headless=new","--no-sandbox","--disable-gpu","--disable-dev-shm-usage",
              "--hide-scrollbars","--force-device-scale-factor=1"]
        return subprocess.run(base+args, capture_output=cap, text=True, timeout=90)
    try:
        open(tmp,"w",encoding="utf-8").write(doc)
        if altura:
            H = min(max(int(altura), 600), 9000)
        else:
            # `--window-size=1280,…` também na medição: sem ele o Chromium mede numa
            # janela de 780px de largura, a tela responsiva fica mais alta do que sairá
            # na captura (1280px) e a altura a mais vira uma página final em branco no
            # .docx. Na vitrine do SDC-VIT: 5229px medidos contra 4103px capturados —
            # uma fatia inteira de sobra.
            dom = run(["--window-size=1280,1024","--virtual-time-budget=6000","--dump-dom",
                       f"file://{tmp}"], cap=True).stdout
            mm = re.search(r'<title>H:(\d+)', dom or "")
            H = min(max(int(mm.group(1)) if mm else 1200, 600), 9000)
        run(["--virtual-time-budget=6000",f"--window-size=1280,{H}",f"--screenshot={out_png}",f"file://{tmp}"])
        return out_png if os.path.exists(out_png) else None
    except Exception:
        return None
    finally:
        try: os.remove(tmp)
        except OSError: pass

def capturar_tela(proto_abs, setup, cache_base, altura=None):
    """Lista de PNGs da tela, **fatiada em páginas** quando é mais alta que uma página.
    Cache: `<base>-pN.png` (fatiado) ou `<base>.png` (curta), reaproveitado pela CI sem
    navegador. Fatia com Pillow; sem Pillow, devolve a imagem inteira (o `.docx` a escala
    para caber). Assim uma tela longa (vitrine, formulário) sai legível, uma página por
    fatia, em vez de uma tira estreita."""
    cached = sorted(glob.glob(cache_base + "-p*.png"))
    def _confere(alvo):
        _confere_fonte(cache_base, os.path.relpath(proto_abs, ROOT), _sha_arquivo(proto_abs), "arquivo", alvo)
    if cached: _confere(cached[0]); return cached
    if os.path.exists(cache_base + ".png"):
        _confere(cache_base + ".png"); return [cache_base + ".png"]
    full = cache_base + ".full.png"
    if not _screenshot_tela(proto_abs, setup, full, altura): return []
    try:
        from PIL import Image
    except Exception:
        Image = None
    w, h = png_size(full)
    if Image and h > int(PAGINA_ALT_PX * 1.35):
        img = Image.open(full)
        n = (h + PAGINA_ALT_PX - 1) // PAGINA_ALT_PX
        sh = (h + n - 1) // n          # fatias uniformes → sem sobra fina no fim
        out = []
        for i in range(n):
            top = i * sh; bot = min(h, (i + 1) * sh)
            if top >= bot: break
            p = f"{cache_base}-p{i+1}.png"
            img.crop((0, top, w, bot)).save(p); out.append(p)
        img.close()
        try: os.remove(full)
        except OSError: pass
        _grava_fonte(cache_base, os.path.relpath(proto_abs, ROOT), _sha_arquivo(proto_abs), "arquivo")
        return out
    os.replace(full, cache_base + ".png")
    _grava_fonte(cache_base, os.path.relpath(proto_abs, ROOT), _sha_arquivo(proto_abs), "arquivo")
    return [cache_base + ".png"]

def telas_da_feature(fs_dir, sigla_n2, md, feat_id):
    """[(png, legenda)] das telas do protótipo que pertencem à feature `feat_id`. Usa o
    manifesto do protótipo referenciado no N3; sem manifesto, a tela de entrada."""
    proto_rel = prototipo_do_n3(md) or prototipo_do_indice(feat_id)
    if not proto_rel: return []
    proto_abs = os.path.join(ROOT, proto_rel)
    if not os.path.exists(proto_abs): return []
    telas = telas_do_manifesto(proto_abs)
    if telas is None:
        telas = [{"nome":"Tela do protótipo","features":[],"setup":""}]
    figs=[]
    for t in telas:
        feats_t = t.get("features") or []
        if feats_t and feat_id and feat_id not in feats_t: continue
        nome_t = t.get("nome","Tela")
        if estado_fora_do_docx(nome_t): continue
        slug = title_case(nome_t) or "tela"
        cache_base = os.path.join(PROTO_DIR, sigla_n2, f"{feat_id or 'fs'}-{slug}")
        pngs = capturar_tela(proto_abs, t.get("setup",""), cache_base, t.get("viewport"))
        for i, p in enumerate(pngs):
            leg = nome_t if len(pngs) == 1 else f"{nome_t} — parte {i+1}/{len(pngs)}"
            figs.append((p, leg))
    return figs

# ─────────────────────────── montagem do corpo do N2 ────────────────────────
def build_body(fs_dir):
    n2 = rd(os.path.join(fs_dir,"README.md"))
    nome_n2 = (re.search(r'^#\s*Feature Set:\s*(.+)$', n2, re.M) or [None,fs_dir])[1].strip()
    sigla_n2 = (re.search(r'Nível 2[^`]*`([A-Z][A-Z-]+)`', n2) or [None,"N2"])[1]
    sfs = sigla_n2.split('-')[-1]
    nome_base = re.sub(r'\s*\([^)]*\)\s*$','',nome_n2).strip()
    n2_label = f"{nome_base} ({sfs})"
    _hn[0]=0
    body=[]
    images=[]                                  # PNGs na ordem de emissão → rId(20+i)/image(3+i).png
    def add_image(png):
        idx=len(images); images.append(png)
        return f"rId{20+idx}", 100+idx
    body.append(P(SIGLA_SISTEMA, bold=True, size=28, align="right"))
    body.append(P("Especificação Funcional", bold=True, align="right"))
    body.append(P(n2_label, align="right"))
    body.append(spacer())
    # Histórico de Versões (do changelog do N2), sem número, centralizado
    body.append(H_plain("Histórico de Versões", center=True))
    chg = md_table(section(n2,"Changelog"))
    ver=[f"1.{i}" for i in range(len(chg)-2,-1,-1)]
    # Autor fixo: o documento é entregue pela PHL TI. A coluna `Autor` do `## Changelog`
    # do N2 identifica quem editou a especificação (inclusive o agente que a gerou) — é
    # rastreabilidade interna, não a autoria do documento que vai ao cliente.
    hist=[[ver[i] if i<len(ver) else "—", r[0], f"{r[2]} — {r[3]}" if len(r)>=4 else r[-1], AUTOR_DOCUMENTO]
          for i,r in enumerate(chg[1:])] if len(chg)>1 else []
    if hist: body.append(table(["Versão","Data","Descrição","Autor"], hist, [1077,1367,5616,1568]))
    body.append(spacer())
    # 1. Nome (SFS) + descrição — começa em nova página
    body.append(H(n2_label, page_break=True))
    # O parágrafo "**Não faz**: …" da `## Descrição` fica FORA do documento: ele é
    # fronteira entre Feature Sets, escrita para quem navega a especificação inteira, e
    # cita Feature Sets e IDs que o leitor do .docx não tem à mão. O documento entregue
    # descreve o que o Feature Set faz.
    for para in [p for p in section(n2,"Descrição").split("\n") if p.strip()]:
        if re.match(r'\s*\*\*N[ãa]o faz\*\*\s*:', para):
            continue
        body.append(P(clean_md(para)))
    body.append(spacer())
    # 2. Funcionalidades (só o nome)
    body.append(H("Funcionalidades"))
    feats=md_table(section(n2,"Features"))
    if feats and len(feats)>1:
        frows=[[r[0], r[-1]] for r in feats[1:]]
        body.append(table(["Funcionalidade","Descrição"], frows, [3600,6028]))
    body.append(spacer())
    # 3. Jornada do Usuário — imagem (ou passos textuais)
    body.append(H("Jornada do Usuário"))
    src=mermaid(n2)
    png=render_jornada(src, os.path.join(DIAG_DIR, f"{sigla_n2}.png"),
                       os.path.relpath(os.path.join(fs_dir, "README.md"), ROOT)) if src else None
    if png:
        w,h=png_size(png); cy=int(ASPECT_MAX_H_IN*914400); cx=int(cy*w/h)
        maxw=int(6.6*914400)
        if cx>maxw: cx=maxw; cy=int(cx*h/w)
        rid,docpr=add_image(png)
        body.append(img(cx,cy,rid,docpr,"Jornada"))   # nome estável — não alterar (determinismo dos .docx já gerados)
    else:
        for lbl in re.findall(r'[\[\({]+"?([^"\]\)}|]+?)"?[\]\)}]+', src or ""):
            if lbl.strip(): body.append(P("• "+lbl.strip()))
        if not src: body.append(P("Jornada não disponível.", italic=True, size=18))
    body.append(spacer())
    # 4. Permissões
    body.append(H("Permissões"))
    for i, (sub, linhas) in enumerate(md_tables(section(n2,"Permissões por perfil"))):
        if i: body.append(spacer())
        if sub: body.append(P(sub, bold=True))
        body.append(table(linhas[0], linhas[1:], widths_por_conteudo(linhas)))
    body.append(spacer())
    # por feature (N3) — cada um em nova página; numeração reinicia
    for fn in ordem_do_fluxo(n2, sorted(glob.glob(os.path.join(fs_dir,"f-*.md")))):
        md=rd(fn)
        nome=(re.search(r'^#\s+(.+)$', md, re.M) or [None,os.path.basename(fn)])[1].strip()
        body.append(FUNC(f"Funcionalidade: {nome}"))
        body.append(H("Descrição")); body.append(P(clean_md(section(md,"Descrição"))))
        reg=section(md,"Regras de negócio")
        body.append(H("Regras de Negócio"))
        # a remissão a regra de outro artefato vira a regra original — ver regra_original()
        nums=[(n, regra_original(t, f"{os.path.basename(fn)} regra {n}")) for n, t in numbered(reg)]
        body.append(table(["Nº","Descrição"], nums, [700,8928]) if nums else P("—"))
        for nt in notes(reg): body.append(P(nt, italic=True, size=18))
        body.append(H("Cenários")); body.extend(cenarios_paras(md) or [P("—")])
        body.append(H("Telas e Protótipos"))
        feat_id=(re.search(r'^id:\s*([A-Za-z0-9-]+)', md, re.M) or [None,None])[1]
        figs=telas_da_feature(fs_dir, sigla_n2, md, feat_id)
        for png_t,legenda in figs:
            w,h=png_size(png_t); cy=int(8.6*914400); cx=int(cy*w/h); maxw=int(6.4*914400)
            if cx>maxw: cx=maxw; cy=int(cx*h/w)
            rid,docpr=add_image(png_t)
            body.append(img(cx,cy,rid,docpr,legenda))
            body.append(P(legenda, italic=True, size=18, align="center"))
        body.append(P(("Campos da funcionalidade:" if figs
                       else "Sem protótipo de tela para esta funcionalidade. Campos da funcionalidade:"),
                      italic=True, size=18))
        campos=md_table(section(md,"Campos"))
        if campos and len(campos)>1:
            hdr=campos[0]
            widths=[1500,1350,1150,1550,1250,2828] if len(hdr)==6 else eq_widths(len(hdr))
            body.append(table(hdr, campos[1:], widths))
        body.append(H("Campos Automáticos"))
        ca=md_table(section(md,"Campos automáticos"))
        body.append(table(ca[0], ca[1:], [2400,4628,2600]) if ca and len(ca)>1 else P("Não se aplica."))
    return "".join(body), sigla_n2, nome_n2, images

def eq_widths_rest(total, n):
    if n<=0: return []
    base=total//n; return [base]*(n-1)+[total-base*(n-1)]

# ─────────────────────────── escrita do .docx (zip) ─────────────────────────
def build_docx(fs_dir):
    CONTENT, sigla_n2, nome_n2, images = build_body(fs_dir)
    z=zipfile.ZipFile(TEMPLATE)
    doc=z.read('word/document.xml').decode('utf-8')
    prefix=doc[:doc.index('<w:p ')]
    cover=re.search(r'<w:p [^>]*>(?:(?!</w:p>).)*?<w:drawing.*?</w:p>', doc, re.S).group(0)
    sectpr=re.search(r'<w:sectPr\b.*?</w:sectPr>', doc, re.S).group(0)
    newdoc=prefix+cover+CONTENT+sectpr+"</w:body></w:document>"
    hdr=z.read('word/header1.xml').decode('utf-8')
    hdr=hdr.replace('&lt;&lt;SIGLA&gt;&gt;', x(SIGLA_SISTEMA)).replace('&lt;&lt;Nome do Sistema&gt;&gt;', x(NOME_SISTEMA))
    # cada imagem (jornada + telas do protótipo) ganha um rId(20+i) → media/image(3+i).png.
    # A jornada (índice 0) mantém rId20/image3.png — preserva o determinismo dos .docx sem protótipo.
    rels=z.read('word/_rels/document.xml.rels').decode('utf-8')
    add=""
    for idx in range(len(images)):
        rid=f"rId{20+idx}"
        if f'Id="{rid}"' not in rels:
            add+=(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
                  f'Target="media/image{3+idx}.png"/>')
    if add: rels=rels.replace('</Relationships>', add+'</Relationships>')
    os.makedirs(OUT_DIR, exist_ok=True)
    out=os.path.join(OUT_DIR, nome_arquivo(nome_n2))
    with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED) as o:
        for it in z.infolist():
            n=it.filename
            if n=='word/document.xml': o.writestr(it,newdoc)
            elif n=='word/header1.xml': o.writestr(it,hdr)
            elif n=='word/_rels/document.xml.rels': o.writestr(it,rels)
            else: o.writestr(it, z.read(n))
        for idx,png in enumerate(images):
            zi=zipfile.ZipInfo(f'word/media/image{3+idx}.png', date_time=(1980,1,1,0,0,0))  # determinístico (sem churn no CI)
            zi.compress_type=zipfile.ZIP_DEFLATED
            o.writestr(zi, open(png,"rb").read())
    z.close()
    return out, sigla_n2, nome_n2

def feature_sets():
    out=[]
    for r in glob.glob(os.path.join(ROOT,"modules","*","*","README.md")):
        if re.search(r'^#\s*Feature Set:', rd(r), re.M) and glob.glob(os.path.join(os.path.dirname(r),"f-*.md")):
            out.append(os.path.dirname(r))
    return sorted(out)

def title_case(s):
    """"Apuração e Devolutiva" -> "ApuracaoEDevolutiva"; acentos e pontuação saem."""
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return "".join(w[0].upper()+w[1:] for w in re.split(r"[^A-Za-z0-9]+", s) if w)

def nome_arquivo(nome_n2):
    """Nome do .docx: o nome do N2 em TitleCase, sem a sigla.

    A sigla identifica o Feature Set na spec; o documento entregue e citado
    (coluna `Requisito` da planilha de contagem) é o nome. `AVL-APU.docx` obriga
    quem recebe a consultar a tabela de siglas — `ApuracaoDevolutiva.docx` não.
    O diagrama em `_diagramas/` continua nomeado pela SIGLA: é cache interno,
    chaveado pela identidade do Feature Set, que sobrevive a renomear o N2.
    """
    return f"{title_case(nome_n2)}.docx"

def fs_meta(fs_dir):
    n2=rd(os.path.join(fs_dir,"README.md"))
    nome=(re.search(r'^#\s*Feature Set:\s*(.+)$',n2,re.M) or [None,os.path.basename(fs_dir)])[1].strip()
    sigla=(re.search(r'Nível 2[^`]*`([A-Z][A-Z-]+)`',n2) or [None,"N2"])[1]
    # O N1 se chama Major Feature Set desde a 3.0.0; o título legado `# Domínio:` segue valendo.
    dom=(re.search(r'^#\s*(?:Major Feature Set|Domínio):\s*(.+)$', rd(os.path.join(os.path.dirname(fs_dir),"README.md")), re.M) or [None,""])[1].strip()
    return sigla, {"nome":nome,"dominio":dom,"nfeat":len(glob.glob(os.path.join(fs_dir,"f-*.md")))}

def read_pendencias():
    idx=rd(os.path.join(ROOT,"modules","INDEX.md"))
    m=re.search(r'<!-- PENDENCIAS:INICIO -->(.*?)<!-- PENDENCIAS:FIM -->', idx, re.S)
    blk=m.group(1) if m else ""
    def sub(t):
        mm=re.search(r'###\s+'+t+r'[^\n]*\n(.*?)(?=\n###\s|\Z)', blk, re.S)
        return md_table(mm.group(1)) if mm else []
    return sub("Exist"), sub("Conte")

def _htbl(rows, cls=""):
    if not rows or len(rows)<2: return "<p class='vazio'>Nenhum item.</p>"
    th="".join(f"<th>{html.escape(c)}</th>" for c in rows[0])
    tb="".join("<tr>"+"".join(f"<td>{html.escape(c)}</td>" for c in r)+"</tr>" for r in rows[1:])
    return f"<table class='{cls}'><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table>"

def write_docs_index():
    meta=dict(fs_meta(fs) for fs in feature_sets())
    # Percorre os Feature Sets, não os nomes de arquivo: o arquivo passou a se chamar
    # pelo nome do N2, e casar nome de arquivo com sigla perderia domínio e contagem.
    linhas=""; n_docs=0
    for sig, m in sorted(meta.items(), key=lambda kv: (kv[1]["dominio"], kv[1]["nome"])):
        arq=nome_arquivo(m["nome"])
        if not os.path.exists(os.path.join(OUT_DIR, arq)): continue
        n_docs+=1
        linhas+=(f"<tr><td>{html.escape(m['dominio'])}</td>"
                 f"<td><strong>{html.escape(m['nome'])}</strong> <span class='sig'>{sig}</span></td>"
                 f"<td class='c'>{m['nfeat']}</td>"
                 f"<td class='c'><a class='dl' href='{html.escape(arq)}' download>&#8595;&nbsp;.docx</a></td></tr>")
    exi, con = read_pendencias()
    CSS="""
:root{--teal:#00B4C8;--ink:#1a2b3c;--muted:#5b6b7a;--line:#d6e3f0;--bg:#f4f8fc}
*{box-sizing:border-box}body{font-family:'Segoe UI',Arial,sans-serif;color:var(--ink);margin:0;background:var(--bg)}
header{background:#fff;border-bottom:3px solid var(--teal);padding:22px 32px;display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}
header h1{font-size:20px;margin:0;color:var(--ink)}header .sys{color:var(--teal);font-weight:700}
header a.voltar{margin-left:auto;color:var(--teal);text-decoration:none;font-size:13px;font-weight:600}
main{max-width:1100px;margin:0 auto;padding:26px 32px 60px}
h2{font-size:16px;margin:30px 0 12px;color:var(--ink);border-bottom:1px solid var(--line);padding-bottom:6px}
h2 .cnt{color:var(--muted);font-weight:400;font-size:13px}
table{border-collapse:collapse;width:100%;background:#fff;font-size:13px;margin:8px 0 4px;box-shadow:0 1px 2px rgba(0,0,0,.04)}
th,td{border:1px solid var(--line);padding:7px 10px;text-align:left;vertical-align:top}
thead th{background:var(--teal);color:#083039;font-weight:700}
td.c,th.c{text-align:center;white-space:nowrap}
.sig{color:var(--muted);font-size:11px;font-weight:600;background:#eef3f9;border-radius:4px;padding:1px 6px;margin-left:4px}
a.dl{display:inline-block;background:var(--teal);color:#fff;text-decoration:none;padding:5px 12px;border-radius:5px;font-weight:600;font-size:12px}
a.dl:hover{filter:brightness(.93)}
.pend th{background:#eef3f9;color:var(--ink)}
.nota{color:var(--muted);font-size:12px;margin:4px 0 0}
.vazio{color:var(--muted)}
"""
    doc=f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Docs — {html.escape(NOME_SISTEMA)}</title><style>{CSS}</style></head><body>
<header><h1>Central de Documentos</h1><span class="sys">{html.escape(NOME_SISTEMA)}</span>
<a class="voltar" href="../index.html">&larr; Documentação</a></header>
<main>
<p class="nota">Especificações Funcionais (.docx) geradas por <code>scripts/gera-docx.py</code> — uma por Feature Set. Regerar após aprovar/alterar N2/N3.</p>
<h2>Especificações Funcionais <span class="cnt">({n_docs} documento(s))</span></h2>
<table><thead><tr><th>Domínio</th><th>Feature Set</th><th class="c">Features</th><th class="c">Download</th></tr></thead>
<tbody>{linhas}</tbody></table>
<h2>Pendências de especificação <span class="cnt">— o que ainda falta (de <code>modules/INDEX.md</code>)</span></h2>
<h3 style="font-size:14px;color:#5b6b7a">Existência — falta N3</h3>
{_htbl(exi,'pend')}
<h3 style="font-size:14px;color:#5b6b7a">Conteúdo — ⚠️/❓ em aberto</h3>
{_htbl(con,'pend')}
</main></body></html>"""
    os.makedirs(OUT_DIR, exist_ok=True)
    open(os.path.join(OUT_DIR,"index.html"),"w",encoding="utf-8").write(doc)
    return n_docs

def figuras_do_cache():
    """[(png, origem, sha gravado, tipo)] de tudo que os `_fontes.json` registram. Serve
    à conferência sem gerar nada: relê a fonte e recompara, sem navegador e sem escrever
    um byte em documentos/."""
    saida = []
    for fj in sorted(glob.glob(os.path.join(OUT_DIR, "_*", "**", "_fontes.json"), recursive=True)):
        try:
            with open(fj, encoding="utf-8") as f: reg = json.load(f)
        except Exception: continue
        for nome, d in sorted(reg.items()):
            saida.append((os.path.join(os.path.dirname(fj), nome), d.get("origem",""),
                          d.get("sha",""), d.get("tipo","arquivo")))
    return saida

def confere_figuras():
    """Reconfere as impressões digitais sem produzir figura nem documento. Devolve 0 se
    tudo casa, 3 se alguma figura está velha — barato o bastante para rodar a cada push,
    ao contrário da geração do .docx, que é sob demanda."""
    conferidas = 0
    for base, origem, sha, tipo in figuras_do_cache():
        abs_origem = os.path.join(ROOT, origem)
        if not origem or not os.path.exists(abs_origem):
            FIGURAS_VELHAS.append((os.path.relpath(base, ROOT), origem or "(origem não registrada)",
                                   "a fonte não existe mais")); continue
        atual = _sha_texto(mermaid(rd(abs_origem)) or "") if tipo == "mermaid" else _sha_arquivo(abs_origem)
        conferidas += 1
        if atual != sha:
            FIGURAS_VELHAS.append((os.path.relpath(base, ROOT), origem, "a fonte mudou depois da figura"))
    print(f"{conferidas} figura(s) conferida(s) contra a fonte que as gerou.")
    return relata_figuras_velhas(0)

def refaz_figuras_velhas(argv):
    """Apaga **só** as figuras cuja fonte mudou e regera. Existe para não se apagar o
    cache inteiro: tanto o render do mermaid quanto a captura do Chromium têm jitter de
    antialiasing (~0,03% dos pixels), então refazer o que está em dia troca bytes sem
    trocar figura — e a mudança real se perde num commit de ruído. Uma passada de
    `rm -rf` no cache trocou 18 diagramas quando só 4 tinham mudado de verdade."""
    confere_figuras()
    if not FIGURAS_VELHAS:
        print("Nada a refazer."); return 0
    if not find_chrome():
        print("\n✗ Sem Chromium: apagar a figura velha aqui a tiraria do documento em vez"
              "\n  de atualizá-la. Rode numa máquina com navegador (e sem GERA_DOCX_NO_BROWSER).")
        return 2
    apagados = 0
    for alvo, _origem, _motivo in list(FIGURAS_VELHAS):
        base = os.path.join(ROOT, re.sub(r"\.png$", "", alvo))
        for f in [base + ".png"] + sorted(glob.glob(base + "-p*.png")):
            if os.path.exists(f): os.remove(f); apagados += 1
    print(f"\n{apagados} arquivo(s) de figura velha apagado(s) — refazendo.\n")
    FIGURAS_VELHAS.clear()
    resto = [a for a in argv if a != "--refaz-figuras-velhas"]
    return main(resto if [a for a in resto if not a.startswith("-")] or "--all" in resto else resto + ["--all"])

def relata_figuras_velhas(codigo_ok):
    """Imprime as figuras velhas (e escreve no resumo do job, quando há um). Sem elas,
    devolve `codigo_ok`; com elas, 3 se a execução for estrita."""
    if not FIGURAS_VELHAS: return codigo_ok
    print(f"\n⚠️  {len(FIGURAS_VELHAS)} figura(s) do documento saíram de uma versão anterior da fonte."
          f"\n    Refaça só essas, local, com Chromium, e commite documentos/:"
          f"\n      python3 scripts/gera-docx.py --refaz-figuras-velhas")
    for png, origem, por in FIGURAS_VELHAS: print(f"    ✗ {png}  ←  {origem}  ({por})")
    resumo = os.environ.get("GITHUB_STEP_SUMMARY")
    if resumo:
        with open(resumo, "a", encoding="utf-8") as f:
            f.write(f"### ⚠️ {len(FIGURAS_VELHAS)} figura(s) desatualizada(s) no .docx\n\n"
                    "Saíram de uma versão anterior da fonte. A esteira não refaz figura (roda sem "
                    "navegador): refaça local com `python3 scripts/gera-docx.py --refaz-figuras-velhas` "
                    "e commite `documentos/`.\n\n")
            for png, origem, por in FIGURAS_VELHAS: f.write(f"- `{png}` ← `{origem}` ({por})\n")
    # Nome antigo aceito de propósito: quem seguir o REP-033 não fica com um sinalizador
    # de rigor que não faz nada — falha silenciosa é o defeito que este guarda combate.
    estrito = os.environ.get("GERA_DOCX_FIGURAS_ESTRITO") or os.environ.get("GERA_DOCX_TELAS_ESTRITO")
    return 3 if estrito else codigo_ok

def main(argv):
    if '--confere-figuras' in argv: return confere_figuras()
    if '--refaz-figuras-velhas' in argv: return refaz_figuras_velhas(argv)
    args=[a for a in argv if not a.startswith('--')]
    targets = feature_sets() if ('--all' in argv or not args) else [os.path.join(ROOT,a) if not os.path.isabs(a) else a for a in args]
    if not os.path.exists(TEMPLATE):
        print(f"✗ template ausente: {TEMPLATE}"); return 2
    ok=0
    for fs in targets:
        try:
            out, sig, nome = build_docx(fs)
            print(f"  ✓ {sig}  {nome}  → {os.path.relpath(out, ROOT)}"); ok+=1
        except Exception as e:
            print(f"  ✗ {os.path.relpath(fs, ROOT)}: {e}")
    n=write_docs_index()
    print(f"\n{ok}/{len(targets)} documento(s) gerado(s) · documentos/index.html lista {n} · pendências de INDEX.md")
    return relata_figuras_velhas(0 if ok else 1)

if __name__=="__main__":
    sys.exit(main(sys.argv[1:]))
