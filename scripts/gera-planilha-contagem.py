#!/usr/bin/env python3
"""gera-planilha-contagem.py — planilha de entrega da contagem, no modelo do cliente.

Preenche uma CÓPIA do modelo do cliente (`scripts/templates/template_planilha_contagem.xlsx`,
Guia de Métricas da STI), aba **AFP - Detalhada**: um processo elementar — e uma função
de dados — por linha, a partir da linha 10. As fórmulas do modelo (complexidade, PFB,
PFL, totais e o Resumo) ficam intactas e o Excel as recalcula ao abrir. O arquivo sai com
o nome da métrica: `SIGLA_SP028_PF_CD.xlsx` numa sprint, `SIGLA_BASELINE_PF_CD.xlsx` na
aplicação inteira (CD = contagem detalhada). A sigla é a do MASTER, salvo a fixa do
portal-compras (SIPDC → PSC).

Colunas preenchidas: B Tipo Projeto · D Módulo (o N1) · E Requisito (o N2, em TitleCase
com `.docx`, ex.: `AtendimentoSocial.docx`) · F Processos elementares · G Tipo · I/J TD/DER
(Qtd., Descrição) · K/L RLR/ALR (Qtd., Descrição) · T Insumo · U Observação. `Qtd. INM` (H)
fica em branco: é da equipe de métrica. No cabeçalho, a Data da Contagem; no Resumo, a
O.S. (a sprint ou "Baseline"), a Aplicação (o `**Nome**` do MASTER) e o Escopo da
Contagem — o recorte com que a planilha foi gerada (sprint, tickets, prefixos), para que
quem a regenerar use o mesmo.

O **Insumo** (T) diz de onde a linha veio: cada ticket que alcançou a feature, com os
critérios de aceite que ela cobriu — `PDTIC25093-13 (CA-1, CA-3); PDTIC25093-14 (CA-2)`.
Chave e critérios saem das AIMs (`analise-impacto/AIM-*.md`): na AIM do ticket, o
`ticket:` do front-matter É a chave, e a `## Alterações na spec, por Feature Set` traz as
features e a coluna `CA-n`; na AIM da sprint, a chave vem da coluna `Ticket`. Sem `CA-n` na
AIM, valem os "Critérios cobertos" da `## Origem` do N3; sem nenhum dos dois (a fonte não
numera), só a chave. Feature que nenhum ticket alcançou sai com `—`.

O critério é do **processo elementar** quando a AIM o diz: a tabela de processos
elementares da `## Alterações na spec, por Feature Set` (`Processo elementar | Da feature
| …`) pode trazer a coluna `Critérios`, e o que estiver nela vale para aquela linha — é o
que separa o critério da pesquisa do critério da combo que ela hospeda. Aceita a numeração
da fonte: `CA-n` ou `CRIT.0n.0m` (decisão do PO, 2026-10-02). Sem a coluna, ou com `—`
na célula, o PE herda os critérios da feature, como antes.

O **Tipo Projeto** (B) escolhe o fator do PFL. Numa sprint (ou com `--jira`), sai da
natureza do PE na AIM: incluído → "Guia de Métricas da STI - Aplicação/Desenvolvimento";
alterado → "… Projeto de Melhoria - Desenv./Mantido pela Empresa". Na baseline, tudo é
Aplicação/Desenvolvimento.

A fonte é sempre o N3 — `## Métricas de tamanho` para os números e, para as
descrições de DER e ALR, o bloco ```json de cada processo elementar na
`### Memória de cálculo` (`{"pe", "alr", "der", "nao_contados", "motivo"}`). Só o
bloco: a enumeração em prosa misturava campo e comentário (memória antiga →
`migra-enumeracao.py`). Nada é recalculado aqui: a planilha ESPELHA a contagem
gravada na feature (ver a regra "A contagem nasce no N3" no CLAUDE.md). Sem o bloco,
as colunas Descrição saem vazias — o número existe, a enumeração não.

As colunas Descrição levam **só o nome** de cada DER e de cada arquivo lógico — o que o
usuário vê na tela —, sem comentário nem explicação (decisão do PO, 2026-10-02). Na
transação, é o que o bloco já traz, item a item, e o gate F11 do hook barra o item que
não é nome; na função de dados, o `so_o_nome` limpa os campos do data-model e as
entidades: unidade no rótulo (`Unit. (R$)`) e nome de arquivo lógico com parêntese
(`Contrato (Protheus)`) ficam.

A linha de **0 PF** fica na planilha, com o motivo À VISTA na **Observação** (coluna U)
(`Não contado: …`, do `motivo` do bloco): o PO precisa ver que a feature foi impactada e
não foi contada (decisão do PO, 2026-09-28). A Descrição do DER fica vazia, porque não há
DER a descrever — o motivo ia nela até 2026-10-02, quando o PO o levou para a Observação.
O Tipo (G) e as quantidades e descrições de DER e ALR (I a L) também ficam em branco: o
PE não foi mensurado. Sem o motivo, a Observação diz que ele falta. Linha com `—` no PF
(ainda não medida, ou PE reutilizado `↪`) não entra.

Por cima do modelo, a AFP - Detalhada sai com a largura das colunas B, F, J, L e T e o
alinhamento de J, L, T e U nas linhas de conteúdo pedidos pelo PO (2026-10-02) —
`LARGURA_PX` e `ALINHAMENTO`.

**Só entra o que tem contagem detalhada.** Feature que a AIM ainda traz com PFB/PFL
estimado — `(E)` na célula ou no cabeçalho da coluna — fica fora do Insumo e do recorte da
sprint, e o script diz quais são: o número dela no N3 ainda não é o do ticket.

**Contagem estimada** (`--estimada`): preenche a aba **AFP - Estimativa** com as funções
da `## Contagem estimada` das AIMs dos tickets — função e tipo; o peso fixo (EE 4 · CE 4 ·
SE 5 · ALI 7 · AIE 5) é fórmula do modelo — e sai como `SIGLA_SP028_PF_CE.xlsx` (CE =
contagem estimada), com o Tipo de Contagem do Resumo em "Estimativa". A fonte da estimada
é a AIM, e só ela: a estimativa nunca vai ao N3 nem ao `global/CONTAGEM-PF.md`.

Geração **sob demanda**: rode quando for entregar a contagem. A planilha é saída,
não fonte, e não é gerada em CI; o que roda em CI é o teste deste script sobre
`scripts/__fixtures__/planilha-contagem/`. Mudou a contagem? Corrija o N3 e gere de novo.
Só a biblioteca padrão: o arquivo é gravado direto no XML do modelo (o openpyxl, ao
regravar um .xlsx existente, perde a imagem, o gráfico e os comentários do modelo).

Uso:
  python3 scripts/gera-planilha-contagem.py [raiz-da-instância] [-o saida.xlsx | -o pasta]
                                            [--sprint NNN] [--escopo PREFIXO ...]
                                            [--jira [CHAVE ...]] [--estimada]

  --sprint  a planilha da sprint (ex.: 028, SP028): só o que a AIM da sprint e as AIMs
            dos tickets dela cobrem, com os tickets dela — `SIGLA_SP028_PF_CD.xlsx`
  --escopo  limita as TRANSAÇÕES às features cujo ID começa pelo prefixo (ex.:
            TEM-ASO, CEP); as funções de dados saem inteiras
  --jira    com chaves (ex.: STRY0012345, ISSUE-482, PDTIC25093-49): só o que elas
            alcançaram; sem valor: tudo o que alguma AIM cita, inclusive o que foi
            entregue sem ticket
  --estimada  a contagem ESTIMADA: a `## Contagem estimada` das AIMs dos tickets da
            `--sprint` (os de `sprint:` igual) ou das chaves do `--jira`, na aba AFP -
            Estimativa — `SIGLA_SP028_PF_CE.xlsx`
"""
import argparse, html, json, re, sys, unicodedata, zipfile
from datetime import date
from xml.sax.saxutils import escape as xml_escape
from pathlib import Path


# ── leitura de tabelas markdown, sempre guiada pelo CABEÇALHO ────────────────
# Posição de coluna varia entre instâncias; nome de coluna, não. Ler por posição
# devolve o número errado com cara de número certo.
def celulas(linha):
    return [c.strip() for c in linha.strip().strip("|").split("|")]

def eh_separador(linha):
    return re.fullmatch(r"\|[\s\-:|]+\|", linha.strip()) is not None

def tabelas(linhas, ini, parar):
    """Todas as tabelas a partir de `ini` até `parar`; cada uma como (cab, linhas)."""
    out, cab, corpo = [], None, []
    for l in linhas[ini:]:
        if parar(l):
            break
        if not l.strip().startswith("|"):
            if cab is not None:
                out.append((cab, corpo)); cab, corpo = None, []
            continue
        if eh_separador(l):
            continue
        if cab is None:
            cab = celulas(l)
        else:
            corpo.append(celulas(l))
    if cab is not None:
        out.append((cab, corpo))
    return out

def col(cab, *nomes):
    for i, c in enumerate(cab):
        for n in nomes:
            if re.fullmatch(n, c, re.I):
                return i
    return -1

def secao(linhas, titulo):
    for i, l in enumerate(linhas):
        if re.fullmatch(rf"#{{2}}\s+{titulo}\s*", l.strip()):
            return i
    return -1

def corpo_da_secao(linhas, titulo):
    """Linhas de `## titulo` até o próximo `## ` — os `###` dela vêm junto."""
    i = secao(linhas, titulo)
    if i < 0:
        return []
    fim = next((j for j in range(i + 1, len(linhas)) if re.match(r"##\s", linhas[j])), len(linhas))
    return linhas[i + 1:fim]

def chave_pe(s):
    """Nome do PE para casar a tabela com a memória: sem crase, negrito nem caixa."""
    return re.sub(r"\s+", " ", re.sub(r"[`*]", "", s)).strip(" .;").casefold()

# ── extração por feature ────────────────────────────────────────────────────
def id_da_feature(raw):
    l = next((x for x in raw.splitlines() if re.search(r"N[íi]vel 3", x)), "")
    m = re.search(r"`([A-Z]{3}-[A-Z]{3}-\d{2})`", l)
    return m.group(1) if m else None

def title_case(s):
    """"Atendimento Social" -> "AtendimentoSocial"; acentos e pontuação saem."""
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    palavras = [w for w in re.split(r"[^A-Za-z0-9]+", s) if w]
    return "".join(w[0].upper() + w[1:] for w in palavras)

def nome_do_n2(caminho):
    """Nome do Feature Set (N2), do `# Feature Set: X` do README irmão do N3."""
    readme = caminho.parent / "README.md"
    if readme.exists():
        for l in readme.read_text(encoding="utf-8").splitlines()[:12]:
            m = re.match(r"#\s+Feature Set:\s*(.+?)\s*$", l)
            if m:
                return m.group(1)
            if l.startswith("# "):  # instância que não usa o prefixo
                return re.sub(r"^#\s+", "", l).strip()
    return None

def requisito(caminho):
    """Coluna Requisito: o N2 em TitleCase com extensão .docx, sem o código."""
    n2 = nome_do_n2(caminho)
    if not n2:
        return None
    return f"{title_case(n2)}.docx"

def modulo(caminho):
    """Coluna Módulo: o nome do N1 (Major Feature Set), do título do README do domínio.
    O título legado `# Domínio:` segue valendo. Sem N1 com título, ""."""
    readme = caminho.parent.parent / "README.md"
    if readme.exists():
        m = re.search(r"^#\s*(?:Major Feature Set|Dom[íi]nio):\s*(.+?)\s*$",
                      readme.read_text(encoding="utf-8"), re.M)
        if m:
            return m.group(1)
    return ""

def fora_de_parenteses(s, sep):
    """`s` quebrada em `sep` só fora de parênteses e de crases."""
    partes_, nivel, crase, ini = [], 0, False, 0
    for i, ch in enumerate(s):
        crase ^= ch == "`"
        nivel += (ch == "(") - (ch == ")") if not crase else 0
        if nivel == 0 and not crase and s.startswith(sep, i):
            partes_.append(s[ini:i]); ini = i + len(sep)
    return [x for x in partes_ + [s[ini:]] if x.strip()]

# A célula Descrição leva SÓ O NOME (decisão do PO, 2026-10-02): de cada DER, o rótulo do
# campo como o usuário o vê; de cada ALR, o nome do arquivo lógico. O que a memória põe ao
# lado — "(contador, calculado)", "(filtro)", "— lido pela vigência", "(AIE, lê — …)" — é
# comentário para quem confere o N3, e na planilha vira ruído que a métrica tem de limpar.
# PE de lista consultada pelo nome: `Consultar <rótulo> (<componente>)` (SIZING → Regra da lista consultada)
LISTA_CONSULTADA = re.compile(r"\((?:combo|autocomplete|carrossel|bot[õo]es|chips|lookup|dropdown|lista)\)\s*$", re.I)
UNIDADE = re.compile(r"^\((?:R\$|US\$|€|%|KB|MB|GB)\)$")  # "Unit. (R$)": a unidade é do rótulo
# No ALR, o parêntese que é parte do nome registrado do arquivo lógico — "(Protheus)",
# "(CR)", "(UO)" — começa em maiúscula e não traz pontuação; o comentário ("(vigentes)",
# "(AIE, lê — …)", "(lido pela vigência)") não.
def parte_do_nome_alr(dentro):
    return bool(re.match(r"[A-ZÀ-Ú]", dentro)) and not re.match(r"(?:ALI|AIE)\b", dentro) \
        and not re.search(r"[,:;—–]", dentro)

def so_o_nome(item, alr=False):
    """O nome do DER ou do arquivo lógico, sem o comentário que a memória traz ao lado.

    Nome entre crases é o nome (`Ata de Registro de Preços` (lê — …)). No DER, sai todo
    parêntese salvo a unidade; no ALR, todo parêntese que não é parte do nome do arquivo
    lógico — "(Protheus)" fica, "(vigentes)" sai. Os dois DER fixos do template ("+1 capacidade de mensagens …",
    "+1 ação que dispara …") saem como o usuário os conhece: Mensagem e Ação."""
    s = re.sub(r"⚠️?", "", item).strip()   # o ⚠️ é pendência para o PO, não parte do nome
    if re.fullmatch(r"[—–\-\s]*", s):    # "—": nenhum
        return ""
    m = re.match(r"`([^`]+)`", s)
    if m:
        return m.group(1).strip()
    s = re.sub(r"^\+\d+\s*", "", s.replace("`", ""))
    if re.match(r"capacidade de (?:exibir )?mensage", s, re.I):
        return "Mensagem"
    if re.match(r"a[çc][ãa]o que dispara", s, re.I) or re.fullmatch(r"a[çc](?:ão|ões)", s, re.I):
        return "Ação"
    if re.fullmatch(r"mensage(?:m|ns)", s, re.I):
        return "Mensagem"
    s = re.split(r"\s+[—–]\s+", s)[0]
    saida, i = "", 0
    while i < len(s):
        if s[i] == "(":
            dentro, resto = entre_parenteses(s[i:])
            grupo = f"({dentro})"
            if UNIDADE.match(grupo) or (alr and parte_do_nome_alr(dentro)):
                saida += grupo
            s, i = saida + resto, len(saida)
            continue
        saida += s[i]; i += 1
    return re.sub(r"\s+", " ", saida).strip(" .;:,")

def entre_parenteses(s):
    """`(…)` balanceado no começo de `s` → (conteúdo, resto)."""
    s = s.lstrip()
    if not s.startswith("("):
        return "", s
    nivel = 0
    for i, ch in enumerate(s):
        nivel += (ch == "(") - (ch == ")")
        if nivel == 0:
            return s[1:i], s[i + 1:]
    return s[1:], ""

def enumeracao(sec):
    """Os blocos ```json da `### Memória de cálculo` → `{chave do PE: bloco}`.

    `sec` é o corpo de `## Métricas de tamanho`. A enumeração de ALR e DER é DADO, não
    prosa — `{"pe": …, "alr": […], "der": […]}`, mais `nao_contados` (vai à Observação)
    e, na linha de 0 PF, `motivo` —, e é só ela que a planilha lê. A memória em prosa
    dizia campo e comentário na mesma frase, e o `so_o_nome` separava um do outro por
    heurística: a explicação do CPM saía como o primeiro ALR, o parêntese de anotação
    como parte do nome do DER (planilha do portal-compras, 2026-10-02). O formato é
    cobrado ao gravar o N3 (`valida-enumeracao-contagem.mjs`, gate F11); a memória antiga
    se converte com `migra-enumeracao.py`. Bloco com JSON inválido é como bloco ausente.
    """
    blocos, corpo, na_memoria, dentro = {}, [], False, False
    for l in sec:
        s = l.strip()
        if re.match(r"###\s+Mem[óo]ria de c[áa]lculo", s):
            na_memoria = True
        elif na_memoria and not dentro and s == "```json":
            dentro, corpo = True, []
        elif dentro and s == "```":
            dentro = False
            try:
                b = json.loads("\n".join(corpo))
            except ValueError:
                continue
            if isinstance(b, dict) and isinstance(b.get("pe"), str):
                blocos[chave_pe(b["pe"])] = b
        elif dentro:
            corpo.append(l)
    return blocos

def processos(caminho):
    raw = caminho.read_text(encoding="utf-8")
    fid = id_da_feature(raw)
    if not fid:
        return []
    linhas = raw.splitlines()
    i = secao(linhas, "Métricas de tamanho")
    if i < 0:
        return []
    tabs = tabelas(linhas, i + 1, lambda l: re.match(r"#{2,3}\s", l) is not None)
    if not tabs:
        return []
    cab, corpo = tabs[0]
    iPE = col(cab, r"Fun[çc][ãa]o de Transa[çc][ãa]o", r"Processo elementar")
    iTipo, iALR, iDER, iPF = col(cab, r"Tipo"), col(cab, r"ALR"), col(cab, r"DER"), col(cab, r"PF")
    if iPE < 0 or iPF < 0:
        return []
    blocos = enumeracao(corpo_da_secao(linhas, "Métricas de tamanho"))
    req, mod = requisito(caminho), modulo(caminho)
    origem_ca = criterios_da_origem(linhas)
    linhas_out = []
    for c in corpo:
        if iPF >= len(c) or not re.fullmatch(r"\d+", c[iPF]):
            continue  # `—` = ainda não medida
        pega = lambda k: c[k] if 0 <= k < len(c) else ""
        nome = re.sub(r"[`*]", "", pega(iPE)).strip()
        b = blocos.get(chave_pe(nome))
        lista = lambda k: [str(x) for x in ((b or {}).get(k) or [])]
        alr_d, der_d = lista("alr"), lista("der")
        nota = f"Não contados: {b['nao_contados']}" if b and b.get("nao_contados") else ""
        # PF 0: a linha fica, com o motivo À VISTA, e não num comentário que só aparece
        # ao passar o mouse (decisão do PO, 2026-09-28): o PO precisa ver que a feature
        # foi impactada e NÃO foi contada — uma linha só de traços parece item esquecido.
        # O motivo vai para a Observação (coluna U), e a Descrição do DER fica vazia: não
        # há DER a descrever, e o texto ali parecia um campo (decisão do PO, 2026-10-02).
        # Sem o motivo, a Observação diz que ele falta. O Tipo e as quantidades de DER e
        # de ALR também ficam em branco: o PE não foi mensurado, e o "— (não
        # classificável)", o "—" e o "0" do N3 pareciam medida (decisão do PO, 2026-10-02).
        tipo, der_qtd, alr_qtd = pega(iTipo), pega(iDER), pega(iALR)
        if pega(iPF) == "0":
            motivo = re.sub(r"\s+", " ", str((b or {}).get("motivo") or "")).strip()
            nota = f"Não contado: {motivo}" if motivo else "Não contado — a memória de cálculo não diz por quê"
            der_d, alr_d = [], []
            tipo = der_qtd = alr_qtd = ""
        linhas_out.append({
            "requisito": req, "pe": pega(iPE), "tipo": tipo,
            "der_qtd": der_qtd, "der_desc": "\n".join(der_d),
            "alr_qtd": alr_qtd, "alr_desc": "\n".join(alr_d),
            "nota_alt": nota,
            "tem_memoria": b is not None,
            "id": fid,
            "modulo": mod, "origem_ca": origem_ca,
        })
    return linhas_out

# ── rastreabilidade: feature → chave do ticket ──────────────────────────────
# A chave NÃO vive no N3 (lá mora a `## Origem`, que aponta para a AIM do ticket). Quem
# liga feature a ticket, com a natureza (incluída/alterada), é a AIM (decisão do PO,
# 2026-09-28): a do ticket — `analise-impacto/AIM-<CHAVE>.md` — lista na
# `## Alterações na spec, por Feature Set` as features que ele alcançou; a da sprint
# consolida a entrega, inclusive o que foi entregue sem ticket. O `tipo` do
# front-matter separa as duas, e o `ticket:` é a chave — sem adivinhar pelo nome.
PASTA_AIM = "analise-impacto"
SECAO_ALTERACOES = "Alterações na spec, por Feature Set"
SECAO_DADOS = "Funções de dados alteradas"
# Chave de ticket: a mesma lista do STORY_KEY_RE de scripts/lib/trace-index.mjs
# (STRY…, ISSUE-n, PDTIC…-n, EXP-…) mais o formato Jira (PRJ25001-49). Na coluna
# Ticket da AIM da sprint, a chave em crase vale em qualquer formato.
STORY_KEY = r"(?:STRY\d{4,}|ISSUE-\d{1,7}|PDTIC\d+-\d{1,7}|EXP-[A-Za-z0-9][A-Za-z0-9_-]*)"
JIRA_LEGADO = r"(?:[A-Za-z]+\d+-\d+)"
CHAVE_TICKET = rf"(?:{STORY_KEY}|{JIRA_LEGADO})"

def front_matter(texto):
    """{campo: valor} do front-matter (carimbo e linhas em branco antes do `---` valem;
    o comentário de fim de linha não faz parte do valor)."""
    linhas, i, out = texto.splitlines(), 0, {}
    while i < len(linhas) and (not linhas[i].strip() or re.match(r"^\s*<!--.*-->\s*$", linhas[i])):
        i += 1
    if i >= len(linhas) or linhas[i].strip() != "---":
        return out
    for l in linhas[i + 1:]:
        if l.strip() == "---":
            break
        m = re.match(r"^([a-z][\w-]*):\s*(.*)$", l, re.I)
        if m:
            out[m.group(1).lower()] = re.sub(r"\s+#.*$", "", m.group(2)).strip().strip("\"'")
    return out

def chaves_da_celula(cel):
    """Chaves de ticket numa célula: o que estiver em crase, em qualquer formato (célula
    com duas chaves traz as duas); sem crase, só o que tem cara de chave. Um ID de
    feature citado não é chave."""
    return [k for k in (re.findall(r"`([^`\s]+)`", cel)
                        or re.findall(rf"(?<![\w-]){CHAVE_TICKET}(?![\w-])", cel, re.I))
            if not re.fullmatch(r"[A-Z]{3}-[A-Z]{3}-\d{2}", k)]

def normaliza_ca(cel):
    """Os critérios de aceite de uma célula, como a fonte os numera — `CA-1, CA-3`,
    `CA-1 a CA-8` —, sem a descrição que às vezes vem ao lado. Sem `CA-n`, ""
    (a fonte não numera: não se inventa número)."""
    return ", ".join(re.findall(r"CA-\d+(?:\s+(?:a|até)\s+CA-\d+|\s*[–—]\s*CA-\d+)?", cel or ""))

# A coluna `Critérios` da tabela de processos elementares é escrita para ser lida: só
# identificadores, na numeração da fonte. `CA-n` é a numeração própria da instância;
# `CRIT.0n.0m` é a da especificação de negócio anexa ao ticket (filho da `HIST0n`).
RE_CRITERIO = r"(?:CA-\d+|CRIT\.\d+\.\d+)"

def normaliza_criterios(cel):
    """Os critérios de aceite ligados a UM processo elementar — `CRIT.01.02, CRIT.01.19`,
    `CRIT.01.01 a CRIT.01.22`, `CA-1, CA-3` —, sem crase nem o comentário que vier ao
    lado. Célula sem identificador (`—`, prosa) devolve "": não se inventa número."""
    t = re.sub(r"[`*]", "", cel or "")
    achados = re.findall(RE_CRITERIO + r"(?:\s*(?:a|até|–|—)\s*" + RE_CRITERIO + r")?", t)
    return ", ".join(re.sub(r"\s*(?:até|a|–|—)\s*(?=C)", " a ", x) for x in achados)

def nome_pe_da_aim(cel):
    """Nome do PE numa tabela de AIM, sem a anotação em itálico — `X (combo) *(fora do
    total)*` é o PE `X (combo)`."""
    return chave_pe(re.sub(r"(?<!\*)\*[^*\n]+\*(?!\*)", "", cel or ""))

# (feature, PE, ticket, critérios que valeram, critérios da outra AIM) — ver `registra_pe`.
CA_PE_DIVERGENTES = []

def criterios_por_pe(cab, corpo):
    """[(feature, PE, ticket-ou-"", critérios)] de uma tabela de processos elementares que
    traga a coluna `Critérios`. `Do ticket` só existe na AIM da sprint; na do ticket a
    chave é a da própria AIM."""
    iP, iD, iK = col(cab, r"^Processo elementar$"), col(cab, r"^Da feature$"), col(cab, r"^Crit[ée]rios$")
    iT = col(cab, r"^Do ticket$")
    if min(iP, iD, iK) < 0:
        return []
    out = []
    for c in corpo:
        if max(iP, iD, iK) >= len(c):
            continue
        m = re.search(r"[A-Z]{3}-[A-Z]{3}-\d{2}", c[iD])
        if m:
            out.append((m.group(0), nome_pe_da_aim(c[iP]), c[iT].strip() if 0 <= iT < len(c) else "",
                        normaliza_criterios(c[iK])))
    return out

def pes_listados(cab, corpo):
    """[(feature, PE)] de uma tabela de processos elementares (`Processo elementar | Da
    feature | …`), com ou sem a coluna `Critérios`. É o que a sprint ALCANÇOU: quando a
    AIM lista os PEs de uma feature, só eles entram no recorte (ver `PES_FORA`)."""
    iP, iD = col(cab, r"^Processo elementar$"), col(cab, r"^Da feature$")
    if min(iP, iD) < 0:
        return []
    out = []
    for c in corpo:
        if max(iP, iD) >= len(c):
            continue
        m = re.search(r"[A-Z]{3}-[A-Z]{3}-\d{2}", c[iD])
        if m:
            out.append((m.group(0), nome_pe_da_aim(c[iP])))
    return out

# PEs de feature alcançada que a AIM não lista — ficam fora do recorte e são avisados.
PES_FORA = []

def criterios_da_origem(linhas):
    """{chave: critérios} da `## Origem` do N3 — o elo recíproco da AIM, que a planilha
    usa quando a AIM não diz quais critérios a feature cobriu."""
    i = secao(linhas, "Origem")
    out = {}
    if i < 0:
        return out
    for cab, corpo in tabelas(linhas, i + 1, lambda l: l.startswith("## ")):
        iT, iC = col(cab, r"Ticket.*", r"Hist[óo]ria.*"), col(cab, r"Crit[ée]rios.*")
        if iT < 0 or iC < 0:
            continue
        for c in corpo:
            ca = normaliza_ca(c[iC]) if iC < len(c) else ""
            for k in chaves_da_celula(c[iT]) if iT < len(c) else []:
                if ca:
                    out.setdefault(k, ca)
    return out

def rotulo_sprint(s):
    """Os números de um rótulo de sprint: `SP_028`, `SP028`, `028` → (28,); `SP07-08` → (7, 8)."""
    return tuple(int(n) for n in re.findall(r"\d+", s or ""))

def aims(raiz, sprint=None):
    """[(chave | None, Path)] — chave preenchida = AIM do ticket; None = AIM da sprint.

    Com `sprint` (os números do rótulo, ver `rotulo_sprint`), só a AIM daquela sprint e as
    dos tickets que ela cita na coluna Ticket — ou que declaram a mesma `sprint:` no
    front-matter. É o recorte da planilha de uma sprint: a feature que outra sprint também
    alterou entra com os tickets desta, e só deles."""
    lidas = []
    for arq in sorted((raiz / PASTA_AIM).glob("AIM-*.md")):
        fm = front_matter(arq.read_text(encoding="utf-8"))
        tipo = fm.get("tipo", "").lower()
        if tipo == "ticket" and fm.get("ticket") and not fm["ticket"].startswith("["):
            lidas.append((fm["ticket"], arq, fm))
        elif tipo == "sprint":
            lidas.append((None, arq, fm))
    if sprint is None:
        return [(k, arq) for k, arq, _ in lidas]
    da_sprint = [arq for k, arq, fm in lidas if k is None and rotulo_sprint(fm.get("sprint")) == sprint]
    citadas = set()
    for arq in da_sprint:
        for cab, corpo in tabelas(secao_md(arq.read_text(encoding="utf-8"), SECAO_ALTERACOES).splitlines(),
                                  0, lambda l: False):
            iJ = col(cab, r"^Ticket$", r"Item do Jira")
            for c in corpo:
                if 0 <= iJ < len(c):
                    citadas.update(chaves_da_celula(c[iJ]))
    return [(k, arq) for k, arq, fm in lidas
            if (k is None and arq in da_sprint)
            or (k is not None and (k in citadas or rotulo_sprint(fm.get("sprint")) == sprint))]

def secao_md(texto, titulo):
    """O corpo de `## <titulo>` até o próximo `## ` — "" se a seção não existe."""
    m = re.search(rf"^##\s+{re.escape(titulo)}\s*$", texto, re.M)
    if not m:
        return ""
    prox = re.search(r"^##\s", texto[m.end():], re.M)
    return texto[m.end(): m.end() + prox.start()] if prox else texto[m.end():]

def eh_estimada(cab, c):
    """A linha traz PFB/PFL estimado: `(E)` na célula ou no cabeçalho da coluna."""
    return any(re.match(r"PF[BL]\b", h, re.I) and ("(E)" in h or (i < len(c) and "(E)" in c[i]))
               for i, h in enumerate(cab))

def rotulo_feature(cel):
    """`ID — Nome` da célula Feature (`\`ID\` **Nome**`); só o ID, se ela não traz o nome."""
    m = re.search(r"`([A-Z]{3}-[A-Z]{3}-\d{2})`\s*\*\*([^*]+)\*\*", cel)
    return f"{m.group(1)} — {m.group(2).strip()}" if m else re.search(r"[A-Z]{3}-[A-Z]{3}-\d{2}", cel).group(0)

def mapa_tickets(raiz, sprint=None, estimadas=None):
    """{fid: {"jira": [chaves], "natureza": "incluída"|"alterada"|"", "ca": {chave: "CA-1, CA-3"},
              "ca_pe": {PE: {chave: "CRIT.01.02, CRIT.01.19"}}}}

    Feature que a AIM ainda traz ESTIMADA (`(E)`) não entra no mapa: a contagem do ticket
    ainda não chegou ao N3, e a planilha detalhada só leva o que foi contado. Com
    `estimadas` (um dict), elas saem ali — {"ID — Nome": [chaves]} —, para o aviso.

    Duas fontes, porque nenhuma sozinha cobre a sprint:

      • a AIM do ticket — a chave é o `ticket:` do front-matter e a
        `## Alterações na spec, por Feature Set` lista as features alcançadas;
      • a AIM da sprint — a única fonte das features **entregues sem ticket**:
        ler só as AIMs dos tickets deixa a planilha com features a menos, com a
        mesma cara de estar completa.

    Nos dois casos a leitura é pelo CABEÇALHO. A coluna `Natureza` diz se o
    processo elementar foi **incluído** (conta 100% em PFB) ou **alterado**
    (conta 50% em PFL) — é o que separa as duas metades de um projeto de
    melhoria, e sem ela a métrica não fecha o cálculo.

    A coluna `CA-n` diz quais critérios de aceite do ticket a feature cobriu — é o que
    vai ao Insumo, ao lado da chave. Vale a da AIM do ticket; a da sprint só completa
    quando a linha tem UMA chave (com duas, não há como saber de qual ticket é o critério).

    `ca_pe` é o critério do PROCESSO ELEMENTAR, da coluna `Critérios` da tabela de
    processos elementares: quando existe, passa à frente do critério da feature naquela
    linha. Vale a AIM do ticket; a da sprint só completa o que a do ticket não disse.
    """
    mapa = {}
    listados = []   # (feature, PE) das tabelas de processos elementares das AIMs

    def registra_pe(fid, pe, chave, crit):
        if fid in mapa and chave and crit:
            ja = mapa[fid].setdefault("ca_pe", {}).setdefault(pe, {}).setdefault(chave, crit)
            # O mesmo PE do mesmo ticket com critérios diferentes em duas AIMs (a do
            # ticket e a da sprint): vale o primeiro lido, e o desencontro é avisado.
            if ja != crit:
                CA_PE_DIVERGENTES.append((fid, pe, chave, ja, crit))

    def registra(fid, chave, natureza, ca=""):
        d = mapa.setdefault(fid, {"jira": [], "natureza": "", "ca": {}})
        if chave and chave not in d["jira"]:
            d["jira"].append(chave)
        if natureza:
            d["natureza"] = natureza
        if chave and ca:
            d["ca"].setdefault(chave, ca)

    def limpa_nat(x):
        # A célula pode trazer um qualificador — "incluída (proposta)", "alterada · 50%".
        # A natureza é a PALAVRA (incluída/alterada/nova); o qualificador não muda o que a
        # métrica precisa (100% vs 50%). Casa a palavra, não a célula inteira.
        t = re.sub(r"[`*]", "", str(x)).strip().lower()
        for palavra, canon in (("alterada", "alterada"), ("incluída", "incluída"),
                               ("incluida", "incluída"), ("nova", "incluída")):
            if re.search(r"(?<![a-zà-ú])" + palavra + r"(?![a-zà-ú])", t):
                return canon
        return ""

    for chave, arq in aims(raiz, sprint):
        if chave is None:
            continue
        trecho = secao_md(arq.read_text(encoding="utf-8"), SECAO_ALTERACOES)
        nat_por_id, ca_por_id, est_ids, do_pe = {}, {}, {}, []
        for cab, corpo in tabelas(trecho.splitlines(), 0, lambda l: False):
            do_pe += criterios_por_pe(cab, corpo)
            listados += pes_listados(cab, corpo)
            iF, iN = col(cab, r"^Feature$"), col(cab, r"^Natureza$")
            iC = col(cab, r"CA-n", r"Crit[ée]rios.*")
            if iF < 0 or iN < 0:
                continue
            for c in corpo:
                m = re.match(r"`([A-Z]{3}-[A-Z]{3}-\d{2})`", c[iF]) if iF < len(c) else None
                if m and eh_estimada(cab, c):
                    est_ids[m.group(1)] = rotulo_feature(c[iF])
                if m and iN < len(c):
                    nat_por_id[m.group(1)] = limpa_nat(c[iN])
                if m and 0 <= iC < len(c):
                    ca_por_id[m.group(1)] = normaliza_ca(c[iC])
        for fid in re.findall(r"^\| `([A-Z]{3}-[A-Z]{3}-\d{2})` \*\*", trecho, re.M):
            if fid in est_ids:
                if estimadas is not None and chave not in estimadas.setdefault(est_ids[fid], []):
                    estimadas[est_ids[fid]].append(chave)
                continue
            registra(fid, chave, nat_por_id.get(fid, ""), ca_por_id.get(fid, ""))
        for fid, pe, _, crit in do_pe:
            if fid not in est_ids:
                registra_pe(fid, pe, chave, crit)

    # A AIM da sprint fecha a entrega: traz as features sem ticket e confirma a
    # natureza das demais. A chave sai da coluna `Ticket` — quando ela não é uma
    # chave ("⚠️ sem ticket", "—"), a feature entra sem chave, que é a informação
    # verdadeira, e não fica de fora da contagem.
    for chave, arq in aims(raiz, sprint):
        if chave is not None:
            continue
        linhas = secao_md(arq.read_text(encoding="utf-8"), SECAO_ALTERACOES).splitlines()
        do_pe = []
        for cab, corpo in tabelas(linhas, 0, lambda l: False):
            do_pe += criterios_por_pe(cab, corpo)
            listados += pes_listados(cab, corpo)
            iF, iN = col(cab, r"^Feature$"), col(cab, r"^Natureza$")
            iJ = col(cab, r"^Ticket$", r"Item do Jira")
            iC = col(cab, r"CA-n", r"Crit[ée]rios.*")
            if iF < 0 or iN < 0:
                continue
            for c in corpo:
                m = re.match(r"`([A-Z]{3}-[A-Z]{3}-\d{2})`", c[iF]) if iF < len(c) else None
                if not m:
                    continue
                # A coluna É a da chave (ver `chaves_da_celula`).
                chaves = chaves_da_celula(c[iJ]) if 0 <= iJ < len(c) else []
                if eh_estimada(cab, c):
                    if estimadas is not None:
                        ja = estimadas.setdefault(rotulo_feature(c[iF]), [])
                        ja += [k for k in chaves if k not in ja]
                    continue
                ca = normaliza_ca(c[iC]) if len(chaves) == 1 and 0 <= iC < len(c) else ""
                for chave in chaves or [""]:
                    registra(m.group(1), chave, limpa_nat(c[iN]) if iN < len(c) else "", ca)
        # A tabela de PE da sprint cita o ticket pelo número curto (`612`), e vem depois
        # das tabelas de feature — por isso só aqui, com as chaves da feature já no mapa.
        for fid, pe, tk, crit in do_pe:
            achadas = chaves_da_celula(tk) or [k for k in mapa.get(fid, {}).get("jira", [])
                                               if tk and re.search(rf"(?<!\d){re.escape(tk)}$", k)]
            if len(achadas) == 1:
                registra_pe(fid, pe, achadas[0], crit)
    # A sprint conta o PROCESSO ELEMENTAR, não a feature: a AIM que lista os PEs de uma
    # feature diz quais deles a sprint alcançou (ex.: só a pesquisa, e não as combos que
    # ela hospeda). A lista é a união das AIMs lidas no recorte.
    for fid, pe in listados:
        if fid in mapa:
            mapa[fid].setdefault("pes", set()).add(pe)
    return mapa

# A contagem ESTIMADA mora na AIM do ticket (`## Contagem estimada`): uma linha por função,
# com o tipo — o peso fixo é o da aba "AFP - Estimativa" do modelo (decisão do PO,
# 2026-10-02). É a única fonte da planilha estimada: nada dela vem do N3.
SECAO_ESTIMADA = "Contagem estimada"
PESO_ESTIMADO = {"EE": 4, "CE": 4, "SE": 5, "ALI": 7, "AIE": 5}

def estimativas(raiz, sprint=None, chaves=None):
    """[{chave, id, pe, tipo, natureza, modulo, requisito, insumo}] — as funções estimadas
    das AIMs de ticket: as da `sprint` (ver `aims`) e, com `chaves`, só as desses tickets.

    Módulo e Requisito saem da feature: do N3, quando ele já existe (o link da `## Features`),
    ou da coluna "Domínio · Feature Set" da própria AIM. Função de dados não tem feature."""
    out = []
    for chave, arq in aims(raiz, sprint):
        if chave is None or (chaves and chave.upper() not in chaves):
            continue
        texto = arq.read_text(encoding="utf-8")
        feats = {}
        for cab, corpo in tabelas(secao_md(texto, "Features").splitlines(), 0, lambda l: False):
            iF, iD, iC = col(cab, r"Feature.*"), col(cab, r"Dom[íi]nio.*", r"Major Feature Set.*"), col(cab, r"Crit[ée]rios.*")
            for c in corpo:
                m = re.search(r"[A-Z]{3}-[A-Z]{3}-\d{2}", c[iF]) if 0 <= iF < len(c) else None
                if not m:
                    continue
                link = re.search(r"\]\(\s*<?([^)>\s]+)>?\s*\)", c[iF])
                n3 = (arq.parent / link.group(1)).resolve() if link else None
                if n3 and n3.is_file():
                    mod, req = modulo(n3), requisito(n3) or ""
                else:
                    dom, _, fs = (c[iD] if 0 <= iD < len(c) else "").partition("·")
                    mod, req = dom.strip(), (f"{title_case(fs)}.docx" if fs.strip() else "")
                feats[m.group(0)] = (mod, req, normaliza_ca(c[iC]) if 0 <= iC < len(c) else "")
        for cab, corpo in tabelas(secao_md(texto, SECAO_ESTIMADA).splitlines(), 0, lambda l: False):
            iFe, iFn, iT, iN = col(cab, r"Feature"), col(cab, r"Fun[çc][ãa]o"), col(cab, r"Tipo"), col(cab, r"Natureza")
            if min(iFn, iT, iN) < 0:
                continue
            for c in corpo:
                if len(c) <= max(iFn, iT, iN) or re.match(r"\W*total", c[0], re.I) or "[" in c[iFn]:
                    continue   # a linha Total e o exemplo do template não são função
                m = re.search(r"[A-Z]{3}-[A-Z]{3}-\d{2}", c[iFe]) if 0 <= iFe < len(c) else None
                mod, req, ca = feats.get(m.group(0), ("", "", "")) if m else ("", "", "")
                nat = re.sub(r"[`*]", "", c[iN]).strip().lower()
                out.append({"chave": chave, "id": m.group(0) if m else "", "pe": re.sub(r"[`*]", "", c[iFn]).strip(),
                            "tipo": re.sub(r"[`*]", "", c[iT]).strip().upper(),
                            "natureza": "incluída" if nat.startswith("inclu") else "alterada" if nat.startswith("alterada") else "",
                            "modulo": mod, "requisito": req, "insumo": f"{chave} ({ca})" if ca else chave})
    return out

# `secao()` casa `##` com o título inteiro — é o que o caminho das transações
# precisa. Os cabeçalhos do DATA-MODEL são `###` e trazem texto depois do termo
# ("### ALIs — Arquivos Lógicos Internos"), então este caminho usa um casador
# próprio. Ampliar o compartilhado consertaria aqui e mudaria o comportamento lá.
def secoes_amplas(linhas, *termos):
    """Índices de TODOS os cabeçalhos que citam algum dos termos.

    Devolve todos, e não o primeiro, porque o documento costuma ter um cabeçalho
    de seção sem tabela ("## Arquivos Lógicos (APF)") seguido do que tem a tabela
    ("### ALIs — …"). Parar no primeiro devolve zero linha com cara de "não há
    funções de dados".
    """
    return [i for i, l in enumerate(linhas)
            if re.match(r"#{2,3}\s", l.strip())
            and any(re.search(t, l.strip(), re.I) for t in termos)]

# ── funções de dados (ALI / AIE) ────────────────────────────────────────────
# A contagem de dados não vive no N3 — vive no DATA-MODEL (índice, com RLR/DER/PF)
# e nos fragmentos por domínio (com as entidades constituintes, que são o que a
# memória oferece como descrição de RLR). Sem esta aba a planilha entrega só
# metade da contagem: as transações.
NOME_ARQ_LOGICO = (r"^ALI$", r"^AIE$", r"ALI\s*/\s*AIE", r"Arquivo l[óo]gico")

def tipo_da_tabela(cab, titulo):
    """ALI ou AIE pela coluna do nome e, na falta, pelo título da seção. Numa tabela
    mista ("ALI / AIE | Tipo | …") devolve "": lá o tipo vem da coluna Tipo, linha a linha."""
    if col(cab, r"^AIE$") >= 0:
        return "AIE"
    if col(cab, r"^ALI$") >= 0:
        return "ALI"
    ali = re.search(r"\bALIs?\b|Internos?\b", titulo, re.I)
    aie = re.search(r"\bAIEs?\b|Interface Externa", titulo, re.I)
    return "AIE" if aie and not ali else "ALI" if ali and not aie else ""

def registro_ali_aie(raiz):
    """{nome: (tipo, domínio)} do `global/ALI-AIE-MAP.md`, o registro canônico."""
    arq = raiz / "global" / "ALI-AIE-MAP.md"
    if not arq.is_file():
        return {}
    lim = lambda x: re.sub(r"\s+", " ", re.sub(r"[`*]", "", x)).strip(" .;")
    reg = {}
    for cab, corpo in tabelas(arq.read_text(encoding="utf-8").splitlines(), 0, lambda l: False):
        iN, iT, iD = col(cab, r"^Nome$"), col(cab, r"^Tipo$"), col(cab, r"Dom[íi]nio")
        if iN < 0:
            continue
        for c in corpo:
            nome = lim(c[iN]) if iN < len(c) else ""
            if not nome or nome.startswith("["):
                continue
            tipo = lim(c[iT]).upper() if 0 <= iT < len(c) else ""
            dom = lim(c[iD]) if 0 <= iD < len(c) else ""
            reg[nome] = (tipo if tipo in ("ALI", "AIE") else "", "" if dom in ("—", "-") else dom)
    return reg

def _ders_da_lista(texto, n):
    """Os DER de uma enumeração em prosa — "a, b, c e d" —, um por item. A vírgula separa;
    o último "e" também, mas só se a contagem declarada `n` pedir: "Nome, Data e Hora"
    com n = 2 são dois DER, não três. Sem `n`, vale a leitura usual do "e" final."""
    partes = fora_de_parenteses(texto.strip().rstrip("."), ", ")
    if partes and " e " in partes[-1] and (n is None or len(partes) < n):
        ini, _, fim = partes[-1].rpartition(" e ")
        partes[-1:] = [ini, fim]
    out = []
    for x in partes:
        x = re.sub(r"^(?:o|a|os|as)\s+", "", so_o_nome(x.strip()))
        if x:
            out.append(x[0].upper() + x[1:])
    return out

def ders_da_memoria(flin):
    """{arquivo lógico: [DER contados]} da memória de cálculo do fragmento de data-model —
    a lista que sustenta o DER da tabela de arquivos lógicos. A tabela de atributos não
    serve para isso: traz o que o modelo guarda (o marcador de exclusão lógica entra, o
    identificador não), e o DER é o que a contagem reconheceu. Lê dois formatos:
      **ALI: X** … "DER (n): a, b e c."  ou  "DER (n):" seguido de "- Entidade (k): a, b e c"
      **ALI: X** … "- DER Entidade: a, b, c = k"   (template do engine)"""
    out, atual, em_lista = {}, None, False
    for l in flin:
        s = l.strip()
        m = re.match(r"^\*\*(?:ALI|AIE):\s*([^*]+?)\s*\*\*", s)
        if m:
            atual, em_lista = m.group(1).strip(), False
            continue
        if atual is None:
            continue
        if re.match(r"^#{1,6}\s|^\*\*[^*]+\*\*|^</details>", s):
            atual = None
            continue
        m = re.match(r"^-\s*DER\s+(?!total)([^:]+):\s*(.+?)\s*=\s*(\d+)\s*$", s, re.I)
        if m:
            out.setdefault(atual, []).extend(_ders_da_lista(m.group(2), int(m.group(3))))
            continue
        m = re.search(r"\bDER\s*\((\d+)\):\s*(.*)$", s)
        if m:
            resto = re.split(r"\.(?:\s|$)", m.group(2), maxsplit=1)[0]
            if resto.strip():
                out.setdefault(atual, []).extend(_ders_da_lista(resto, int(m.group(1))))
            em_lista = not resto.strip()
            continue
        if em_lista:
            m = re.match(r"^[-*]\s+.+?\((\d+)\):\s*(.+)$", s)
            if m:
                out.setdefault(atual, []).extend(_ders_da_lista(m.group(2), int(m.group(1))))
            elif s:
                em_lista = False
    return out

def funcoes_de_dados(raiz):
    idx = raiz / "global" / "DATA-MODEL.md"
    if not idx.is_file():
        return []
    linhas = idx.read_text(encoding="utf-8").splitlines()
    # O índice do template traz DUAS tabelas — "### ALIs — …" (ALI | Domínio | …) e
    # "### AIEs — …" (AIE | Sistema externo | Entidades / estruturas usadas | …) — e há
    # instância com uma tabela só, mista, com coluna Tipo. Lê todas: parar na primeira
    # entregava a aba sem as AIEs, com a mesma cara de "não há AIE".
    achadas = []
    for i in secoes_amplas(linhas, r"\bAL[IE]s?\b", r"Arquivos L[óo]gicos", r"Interface Externa"):
        for cab, corpo in tabelas(linhas, i + 1, lambda l: re.match(r"#{2,3}\s", l) is not None):
            if col(cab, *NOME_ARQ_LOGICO) >= 0 and col(cab, r"RLR") >= 0:
                achadas.append((cab, corpo, tipo_da_tabela(cab, linhas[i])))
    if not achadas:
        return []

    # entidades constituintes e CAMPOS: o fragmento por domínio é quem os nomeia.
    # Cada entidade abre com "> **ALI: X** · papel" (ou "> **AIE: X** · estrutura
    # externa de …"), que é o elo entidade→arquivo lógico; a tabela logo abaixo lista
    # os campos em Label PO. O título do fragmento dá o domínio de quem o declara.
    const, campos, dom_frag, contados = {}, {}, {}, {}
    cab_campos = re.compile(r"^\|\s*(?:Atributo\s*\(\s*)?Label PO")   # "| Label PO" ou "| Atributo (Label PO)"
    for frag in sorted((raiz / "global" / "data-models").glob("*.md")):
        flin = frag.read_text(encoding="utf-8").splitlines()
        for ali, ders in ders_da_memoria(flin).items():
            contados.setdefault(ali, ders)
        mdom = next((m for m in (re.match(r"#\s+Data Model:\s*(.+?)\s*$", l) for l in flin[:5]) if m), None)
        for k, l in enumerate(flin):
            m = re.match(r"^>\s*\*\*(?:ALI|AIE):\s*([^*]+)\*\*", l)
            if not m:
                continue
            if mdom:
                dom_frag.setdefault(m.group(1).strip(), mdom.group(1))
            ali = m.group(1).strip()
            j = k + 1
            while j < len(flin) and not cab_campos.match(flin[j]):
                if re.match(r"^##\s", flin[j]):
                    break
                j += 1
            if j >= len(flin) or not cab_campos.match(flin[j]):
                continue
            vistos = campos.setdefault(ali, [])
            for linha in flin[j + 2:]:
                if not linha.startswith("|"):
                    break
                campo = re.sub(r"[`*]", "", celulas(linha)[0]).strip()
                if campo and campo not in vistos:
                    vistos.append(campo)

        for j in secoes_amplas(flin, r"Arquivos L[óo]gicos deste dom[íi]nio"):
            for fcab, fcorpo in tabelas(flin, j + 1, lambda l: re.match(r"#{2,3}\s", l) is not None):
                k, kc = col(fcab, r"ALI\s*/\s*AIE"), col(fcab, r"Entidades constituintes")
                if k >= 0 and kc >= 0:
                    for c in fcorpo:
                        if k < len(c) and kc < len(c):
                            nome = re.sub(r"[`*]", "", c[k]).strip()
                            const[nome] = c[kc]
                            if mdom:
                                dom_frag.setdefault(nome, mdom.group(1))
                    break

    reg = registro_ali_aie(raiz)
    lim = lambda x: re.sub(r"\s+", " ", re.sub(r"[`*]", "", x)).strip(" .;")
    saida, vistos = [], set()
    for cab, corpo, tipo_tab in achadas:
        iNome = col(cab, *NOME_ARQ_LOGICO)
        iDom, iRLR, iDER, iPF = col(cab, r"Dom[íi]nio"), col(cab, r"RLR"), col(cab, r"DER"), col(cab, r"PF")
        iTipo = col(cab, r"^Tipo$")
        iEnt = col(cab, r"Entidades constituintes", r"Entidades\s*/\s*estruturas.*")
        for c in corpo:
            nome = lim(c[iNome]) if iNome < len(c) else ""
            if not nome or nome.lower().startswith("total") or nome in vistos:
                continue
            vistos.add(nome)
            pega = lambda k: lim(c[k]) if 0 <= k < len(c) else ""
            reg_tipo, reg_dom = reg.get(nome, ("", ""))
            # O tipo decide o peso (ALI 7/10/15, AIE 5/7/10): vem da coluna Tipo, da
            # tabela ou do registro, nesta ordem. Sem nenhum dos três, ALI — o que o
            # script sempre assumiu.
            tipo = pega(iTipo).upper()
            if tipo not in ("ALI", "AIE"):
                tipo = tipo_tab or reg_tipo or "ALI"
            # A tabela de AIEs não tem coluna Domínio (tem "Sistema externo"): sem
            # ela, o domínio vem do registro e, na falta, do fragmento que declara o
            # arquivo lógico.
            dom = pega(iDom) if iDom >= 0 else (reg_dom or dom_frag.get(nome, ""))
            # A descrição de RLR são as entidades constituintes, UMA POR LINHA. O
            # data-model as escreve em dois níveis — "Principal (principal) · A, B, C
            # (subgrupos)" —, então não basta quebrar no `·`: os subgrupos ficariam
            # todos numa linha só e a coluna deixaria de ser enumeração. Quebra-se
            # também na vírgula. Cuidado: nomes como "Critério/Decisão de Desempate +
            # Inscrição da Decisão" trazem `+` e `/` e NÃO se quebram — só a vírgula
            # separa itens neste formato. Sem o fragmento, vale a coluna do índice.
            # A vírgula de dentro do parêntese não separa: "Solicitação (+ itens, histórico)"
            # é uma entidade. E a célula leva só o nome (ver `so_o_nome`).
            ents = const.get(nome, "") or pega(iEnt)
            ents = [n for grupo in re.split(r"\s+·\s+",
                        re.sub(r"\((principal|subgrupos?|suporte)\)", "", ents))
                    for e in fora_de_parenteses(grupo, ",") if (n := so_o_nome(lim(e), alr=True))]
            saida.append({
                "requisito": dom, "pe": nome, "tipo": tipo,
                # A Descrição do DER é a lista da memória de cálculo, que sustenta o
                # número; sem ela, os atributos do modelo (população diferente — ver o
                # aviso de DER no fim do main).
                "der_qtd": pega(iDER),
                "der_desc": "\n".join(contados.get(nome) or
                                      [n for c_ in campos.get(nome, []) if (n := so_o_nome(c_))]),
                "alr_qtd": pega(iRLR), "alr_desc": "\n".join(ents),
                "tipo_registro": reg_tipo,
                "id": nome,
            })
    return saida

# quais arquivos lógicos cada ticket alterou — `## Funções de dados alteradas` das
# AIMs. Traz também o RLR/DER DEPOIS da alteração: o CPM dimensiona a função alterada
# (CHGA) pelo tamanho que ela tem DEPOIS, e o DATA-MODEL guarda o antes. Entregar
# só o antes dá à métrica o número errado para o cálculo que ela vai fazer.
def natureza_dados(raiz, sprint=None):
    """{arquivo lógico: "incluída"|"alterada"} — da tabela de totais da AIM da sprint.

    A coluna `Natureza` das tabelas por ALI fala das TABELAS ("Tabela incluída"),
    não da função de dados: um ALI alterado pode ganhar uma tabela nova sem
    deixar de ser alterado. A natureza da FUNÇÃO só existe na tabela de totais.
    """
    out = {}
    for chave, arq in aims(raiz, sprint):
        if chave is not None:
            continue
        linhas = arq.read_text(encoding="utf-8").splitlines()
        for cab, corpo in tabelas(linhas, 0, lambda l: False):
            iN = col(cab, r"Natureza da .*fun[çc][ãa]o.*")
            iF = col(cab, r"Fun[çc][ãa]o de dados")
            if iF < 0 or iN < 0:
                continue
            for c in corpo:
                if iF >= len(c) or iN >= len(c):
                    continue
                nome = re.sub(r"[`*]", "", c[iF]).strip()
                v = re.sub(r"[^a-zà-ú]", "", re.sub(r"[`*]", "", c[iN]).strip().lower())
                if nome and not nome.lower().startswith("total") and v in ("alterada", "incluída", "incluida"):
                    out[nome] = "incluída" if v.startswith("inclu") else "alterada"
    return out

def mapa_tickets_dados(raiz, sprint=None, estimadas=None):
    mapa, depois = {}, {}
    for chave, arq in aims(raiz, sprint):
        if chave is None:
            continue
        trecho = secao_md(arq.read_text(encoding="utf-8"), SECAO_DADOS)
        for cabec in re.findall(r"^###\s+(?:ALI|AIE):\s*(.+)$", trecho, re.M):
            nome = cabec.split("—")[0].strip()
            if not nome or nome.startswith("["):
                continue
            if "(E)" in cabec:   # PF ainda estimado: a função de dados fica fora, como a feature
                if estimadas is not None and chave not in estimadas.setdefault(nome, []):
                    estimadas[nome].append(chave)
                continue
            mapa.setdefault(nome, [])
            if chave not in mapa[nome]:
                mapa[nome].append(chave)
            # O antes pode não ter sido apurado (`RLR ❓ → 6`): o depois vale do mesmo jeito.
            mrlr = re.search(r"RLR\s+(\d+|❓|\?)\s*→\s*(\d+)", cabec)
            mder = re.search(r"DER\s+(\d+|❓|\?)\s*→\s*(\d+)", cabec)
            mnat = re.search(r"·\s*(inclu[íi]da|alterada)\s*$", cabec.strip())
            if mrlr or mder:
                depois[nome] = {
                    "rlr": (mrlr.group(1), mrlr.group(2)) if mrlr else None,
                    "der": (mder.group(1), mder.group(2)) if mder else None,
                    "natureza": ("incluída" if mnat.group(1).startswith("inclu") else "alterada") if mnat else "",
                }
    return mapa, depois

# ── planilha: o modelo do cliente ───────────────────────────────────────────
# A planilha sai no MODELO DO CLIENTE (scripts/templates/template_planilha_contagem.xlsx,
# aba "AFP - Detalhada"), e não num layout próprio: é nele que a equipe de métricas
# confere e que o cliente recebe (decisão do PO, 2026-09-30). O arquivo é uma CÓPIA do
# modelo com só as células de entrada preenchidas, gravadas direto no XML da aba: o
# openpyxl, ao regravar um .xlsx existente, descarta a imagem, o gráfico, os comentários
# e os vínculos das outras abas — o modelo sairia mutilado, sem erro nenhum. As fórmulas
# (complexidade, PFB, PFL, totais e o Resumo) ficam como estão; o Excel as recalcula ao
# abrir (`fullCalcOnLoad`).
MODELO = Path(__file__).resolve().parent / "templates" / "template_planilha_contagem.xlsx"
ABA_DETALHADA, ABA_RESUMO, ABA_ESTIMATIVA = "AFP - Detalhada", "Resumo", "AFP - Estimativa"
PRIMEIRA, ULTIMA = 10, 382   # linhas de dados do modelo; a 383 é "Só inserir linhas antes desta"
PRIMEIRA_EST = 11            # na AFP - Estimativa a 10 é "Só inserir linhas depois desta"

# Formatação da AFP - Detalhada por cima do modelo (decisão do PO, 2026-10-02). Largura em
# PIXELS, convertida para a unidade do Excel pela fórmula da norma (ECMA-376, 18.3.1.13),
# com a largura do dígito da fonte padrão do modelo — Arial 10, 7 px a 96 dpi. O
# alinhamento vale só nas linhas de conteúdo; cabeçalho e rodapé ficam como no modelo.
LARGURA_PX = {"B": 400, "F": 400, "J": 170, "L": 170, "T": 200}
LARGURA_DIGITO_PX = 7
ALINHAMENTO = {"J": {"vertical": "top"}, "L": {"vertical": "top"},
               "T": {"horizontal": "left", "vertical": "top"},
               "U": {"horizontal": "left", "vertical": "top"}}


# Tipo Projeto (coluna B) — escolhe o fator do PFL. Numa sprint, pela natureza do PE:
# incluído conta inteiro, alterado conta metade (decisão do PO, 2026-09-30). Na
# baseline, tudo é Aplicação/Desenvolvimento: é o tamanho da aplicação inteira.
TIPO_PROJETO = {
    "incluída": "Guia de Métricas da STI - Aplicação/Desenvolvimento",
    "alterada": "Guia de Métricas da STI - Projeto de Melhoria - Desenv./Mantido pela Empresa",
}
TIPO_PROJETO_BASELINE = TIPO_PROJETO["incluída"]

# Sigla do NOME DO ARQUIVO: a do MASTER, salvo onde a métrica conhece o sistema por outra
# (decisão do PO, 2026-09-30 — fixa aqui, não configurável).
SIGLA_ARQUIVO = {"SIPDC": "PSC"}

def identidade(raiz):
    """(sigla, nome) do `**Sigla**` e do `**Nome**` do global/MASTER.md — None se ausentes."""
    master = raiz / "global" / "MASTER.md"
    txt = master.read_text(encoding="utf-8") if master.exists() else ""
    s = re.search(r"^-\s+\*\*Sigla\*\*:\s*`?([A-Z]{2,6})`?\b", txt, re.M)
    n = re.search(r"^-\s+\*\*Nome\*\*:\s*([^\[\n].*?)\s*$", txt, re.M)
    return (s.group(1) if s else None), (n.group(1) if n else None)

def nome_do_arquivo(sigla, sprint, contagem="CD"):
    """SIGLA_SP028_PF_CD.xlsx numa sprint · SIGLA_BASELINE_PF_CD.xlsx na aplicação inteira.
    PF é fixo; CD = contagem detalhada, CE = contagem estimada."""
    rot = "SP" + "-".join(f"{n:03d}" for n in sprint) if sprint else "BASELINE"
    return f"{SIGLA_ARQUIVO.get(sigla, sigla)}_{rot}_PF_{contagem}.xlsx"

def _col_num(letras):
    n = 0
    for ch in letras:
        n = n * 26 + ord(ch) - 64
    return n

def _celula(ref, estilo, valor):
    if valor is None or valor == "":
        return f'<c r="{ref}"{estilo}/>'
    if isinstance(valor, (int, float)):
        return f'<c r="{ref}"{estilo}><v>{valor}</v></c>'
    return (f'<c r="{ref}"{estilo} t="inlineStr"><is><t xml:space="preserve">'
            f"{xml_escape(str(valor))}</t></is></c>")

def _preenche_linha(xml_linha, num, valores):
    """Troca as células `valores` ({coluna: valor}) de uma <row>, mantendo o estilo."""
    for colu, valor in valores.items():
        ref = f"{colu}{num}"
        m = re.search(rf'<c r="{ref}"(?P<a>[^>]*?)(?:/>|>.*?</c>)', xml_linha, re.S)
        if m:
            s = re.search(r'\ss="\d+"', m.group("a"))
            xml_linha = xml_linha[:m.start()] + _celula(ref, s.group(0) if s else "", valor) + xml_linha[m.end():]
            continue
        # célula que o modelo não tem nesta linha: entra na posição da coluna
        pos = next((mc.start() for mc in re.finditer(r'<c r="([A-Z]+)\d+"', xml_linha)
                    if _col_num(mc.group(1)) > _col_num(colu)), xml_linha.rindex("</row>"))
        xml_linha = xml_linha[:pos] + _celula(ref, "", valor) + xml_linha[pos:]
    return xml_linha

def _preenche_aba(xml, por_linha):
    """por_linha: {número da linha: {coluna: valor}} → o XML da aba com as trocas."""
    existentes = {int(n) for n in re.findall(r'<row r="(\d+)"', xml)}
    faltam = set(por_linha) - existentes
    if faltam:
        sys.exit(f"✗ O modelo não tem as linhas {sorted(faltam)[:5]} — o template mudou?")
    def troca(m):
        num = int(m.group(1))
        return _preenche_linha(m.group(0), num, por_linha[num]) if num in por_linha else m.group(0)
    return re.sub(r'<row r="(\d+)"[^>]*?(?:/>|>.*?</row>)', troca, xml, flags=re.S)

def _abas(z):
    """{nome da aba: caminho da parte no .xlsx}."""
    rels = z.read("xl/_rels/workbook.xml.rels").decode("utf-8")
    alvo = {}
    for rel in re.findall(r"<Relationship\b[^>]*>", rels):
        i, t = re.search(r'\bId="([^"]+)"', rel), re.search(r'\bTarget="([^"]+)"', rel)
        if i and t:
            alvo[i.group(1)] = t.group(1).lstrip("/") if t.group(1).startswith("/") else "xl/" + t.group(1)
    out = {}
    for aba in re.findall(r"<sheet\b[^>]*>", z.read("xl/workbook.xml").decode("utf-8")):
        n, rid = re.search(r'\bname="([^"]+)"', aba), re.search(r'\br:id="([^"]+)"', aba)
        if n and rid and rid.group(1) in alvo:
            out[html.unescape(n.group(1))] = alvo[rid.group(1)]
    return out

def _largura_excel(px, digito=LARGURA_DIGITO_PX):
    """Pixels → atributo `width` de `<col>` (ECMA-376, 18.3.1.13): primeiro o número de
    caracteres que cabem, arredondado a centésimos; depois a largura com o respiro de 5 px."""
    chars = int((px - 5) / digito * 100 + 0.5) / 100
    return int((chars * digito + 5) / digito * 256) / 256

def _ajusta_colunas(xml, larguras):
    """Grava a largura de cada coluna ({letra: px}) no `<cols>` da aba. Um `<col>` que
    cobre várias colunas é partido, para não mudar as vizinhas."""
    bloco = re.search(r"<cols>(.*?)</cols>", xml, re.S)
    cols = [dict(re.findall(r'(\w+)="([^"]*)"', c)) for c in re.findall(r"<col\b[^>]*/>", bloco.group(1))]
    for letra, px in larguras.items():
        n, novos = _col_num(letra), []
        for c in cols:
            ini, fim = int(c["min"]), int(c["max"])
            if not ini <= n <= fim:
                novos.append(c)
                continue
            if ini < n:
                novos.append({**c, "max": str(n - 1)})
            novos.append({**c, "min": str(n), "max": str(n)})
            if n < fim:
                novos.append({**c, "min": str(n + 1)})
        if not any(int(c["min"]) == n for c in novos):
            novos.append({"min": str(n), "max": str(n)})
        for c in novos:
            if int(c["min"]) == n:
                c.pop("bestFit", None)
                c["width"], c["customWidth"] = f"{_largura_excel(px):g}", "1"
        cols = sorted(novos, key=lambda c: int(c["min"]))
    corpo = "".join("<col " + " ".join(f'{k}="{v}"' for k, v in c.items()) + "/>" for c in cols)
    return xml[:bloco.start(1)] + corpo + xml[bloco.end(1):]

def _realinha(xml_aba, styles, linhas_conteudo, alinhamento):
    """Alinha as células das colunas de `alinhamento` nas linhas de conteúdo. Cada estilo
    do modelo usado ali ganha um irmão com o alinhamento pedido — mesma fonte, borda e
    preenchimento —, acrescentado ao fim do `cellXfs`. Devolve (aba, styles)."""
    xfs = re.search(r'<cellXfs count="(\d+)">(.*?)</cellXfs>', styles, re.S)
    lista = re.findall(r"<xf\b[^>]*?(?:/>|>.*?</xf>)", xfs.group(2), re.S)
    novos, cache = [], {}
    def irmao(sid, pedido):
        chave = (sid, tuple(sorted(pedido.items())))
        if chave not in cache:
            xf = lista[sid]
            if xf.endswith("/>"):
                xf = xf[:-2] + "></xf>"
            al = re.search(r"<alignment\b[^>]*/>", xf)
            attrs = dict(re.findall(r'(\w+)="([^"]*)"', al.group(0))) if al else {}
            attrs.update(pedido)
            tag = "<alignment " + " ".join(f'{k}="{v}"' for k, v in attrs.items()) + "/>"
            xf = xf.replace(al.group(0), tag) if al else re.sub(r"^(<xf\b[^>]*>)", r"\1" + tag, xf)
            if "applyAlignment=" in xf:
                xf = re.sub(r'applyAlignment="[^"]*"', 'applyAlignment="1"', xf, count=1)
            else:
                xf = xf.replace("<xf ", '<xf applyAlignment="1" ', 1)
            cache[chave] = len(lista) + len(novos)
            novos.append(xf)
        return cache[chave]
    def troca(m):
        col, lin = m.group(1), int(m.group(2))
        if lin not in linhas_conteudo or col not in alinhamento:
            return m.group(0)
        return f'{m.group(0)[:m.start(3) - m.start(0)]}{irmao(int(m.group(3)), alinhamento[col])}"'
    xml_aba = re.sub(r'<c r="([A-Z]+)(\d+)"[^>]*?\ss="(\d+)"', troca, xml_aba)
    if novos:
        corpo = xfs.group(2) + "".join(novos)
        styles = (styles[:xfs.start()] + f'<cellXfs count="{len(lista) + len(novos)}">' + corpo
                  + "</cellXfs>" + styles[xfs.end():])
    return xml_aba, styles

def escopo_da_contagem(sprint, jira, escopo):
    """O texto do "Escopo da Contagem" (Resumo, A14): o recorte com que a planilha foi gerada.

    A planilha não guardava o próprio recorte, e regenerá-la sem ele mudava o conteúdo: a
    da SP_028 do portal-compras fora gerada só com os cinco tickets com apurável, e a
    regenerada pela sprint inteira trouxe dez processos a mais."""
    partes = ["Sprint " + "-".join(f"{n:03d}" for n in sprint)] if sprint else []
    if jira:
        partes.append(("ticket " if len(jira) == 1 else "tickets ") + ", ".join(jira))
    elif jira is not None:
        partes.append("tudo o que as AIMs citam, inclusive o entregue sem ticket")
    if not partes:
        partes.append("Aplicação inteira (baseline)")
    if escopo:
        partes.append("features com prefixo " + ", ".join(e.upper() for e in escopo))
    return " · ".join(partes)

def escreve(linhas, saida, rotulo_os, nome_sistema, escopo=""):
    """Copia o modelo e preenche a AFP - Detalhada: uma linha por PE e por função de dados.

    Colunas preenchidas: B Tipo Projeto · D Módulo · E Requisito · F Processos elementares ·
    G Tipo · I/J TD/DER (Qtd., Descrição) · K/L RLR/ALR (Qtd., Descrição) · T Insumo ·
    U Observação. H (Qtd. INM) fica para a equipe de métrica. No cabeçalho, a Data da
    Contagem (R4); no Resumo, a O.S. (B4), a Aplicação (F5) e o Escopo da Contagem (A14).
    Por cima do modelo, a largura das colunas de `LARGURA_PX` e o alinhamento de
    `ALINHAMENTO` nas linhas de conteúdo."""
    cabem = ULTIMA - PRIMEIRA + 1
    if len(linhas) > cabem:
        sys.exit(f"✗ {len(linhas)} linhas para {cabem} no modelo (linhas {PRIMEIRA}–{ULTIMA} da aba "
                 f"{ABA_DETALHADA}). Recorte com --sprint, --jira ou --escopo, ou amplie o modelo "
                 f"inserindo linhas, com as fórmulas, antes da {ULTIMA + 1}.")
    num = lambda v: int(v) if isinstance(v, str) and v.isdigit() else v
    detalhada = {r: {"B": d.get("tipo_projeto", ""), "D": d.get("modulo", ""), "E": d.get("requisito") or "",
                     "F": d["pe"], "G": d["tipo"],
                     "I": num(d["der_qtd"]), "J": d["der_desc"], "K": num(d["alr_qtd"]), "L": d["alr_desc"],
                     "T": d.get("insumo") or "—", "U": d.get("nota_alt", "")}
                 for r, d in enumerate(linhas, start=PRIMEIRA)}
    resumo = {4: {"B": rotulo_os}, 5: {"F": nome_sistema or ""}, 14: {"A": escopo}}
    _grava(saida, {ABA_DETALHADA: detalhada, ABA_RESUMO: resumo}, (ABA_DETALHADA, 4, "R"),
           formata=(ABA_DETALHADA, set(range(PRIMEIRA, PRIMEIRA + len(linhas)))))

def escreve_estimada(linhas, saida, rotulo_os, nome_sistema, escopo=""):
    """Copia o modelo e preenche a AFP - Estimativa: uma linha por função estimada.

    Colunas preenchidas: B Tipo Projeto · D Módulo · E Requisito · F Processos elementares ·
    G Tipo · K Insumos. PFB e PFL (I, J) são fórmula do modelo — o peso fixo do tipo. No
    cabeçalho, a Data da Contagem (K4); no Resumo, a O.S. (B4), o Tipo de Contagem (B5,
    "Estimativa" — é ele que aponta o Resumo para esta aba), a Aplicação (F5) e o Escopo da
    Contagem (A14)."""
    cabem = ULTIMA - PRIMEIRA_EST + 1
    if len(linhas) > cabem:
        sys.exit(f"✗ {len(linhas)} linhas para {cabem} no modelo (linhas {PRIMEIRA_EST}–{ULTIMA} da aba "
                 f"{ABA_ESTIMATIVA}). Recorte com --sprint ou --jira, ou amplie o modelo inserindo "
                 f"linhas, com as fórmulas, antes da {ULTIMA + 1}.")
    estimativa = {r: {"B": TIPO_PROJETO.get(d["natureza"], ""), "D": d["modulo"], "E": d["requisito"],
                      "F": d["pe"], "G": d["tipo"], "K": d["insumo"]}
                  for r, d in enumerate(linhas, start=PRIMEIRA_EST)}
    resumo = {4: {"B": rotulo_os}, 5: {"B": "Estimativa", "F": nome_sistema or ""}, 14: {"A": escopo}}
    _grava(saida, {ABA_ESTIMATIVA: estimativa, ABA_RESUMO: resumo}, (ABA_ESTIMATIVA, 4, "K"))

def _grava(saida, por_aba, celula_da_data, formata=None):
    """Copia o modelo trocando as células de `por_aba` ({aba: {linha: {coluna: valor}}});
    `celula_da_data` = (aba, linha, coluna) da Data da Contagem; `formata` = (aba, linhas de
    conteúdo) que recebem a largura de `LARGURA_PX` e o alinhamento de `ALINHAMENTO`."""
    with zipfile.ZipFile(MODELO) as zi, zipfile.ZipFile(saida, "w", zipfile.ZIP_DEFLATED) as zo:
        # Data da Contagem como número de série do Excel — contado a partir da época do
        # PRÓPRIO arquivo: o modelo usa o sistema de 1904 (herança do Excel para Mac), e
        # a conta pela época de 1900 punha a data quatro anos à frente.
        em_1904 = re.search(r'<workbookPr\b[^>]*\bdate1904="(?:1|true)"', zi.read("xl/workbook.xml").decode("utf-8"))
        aba_d, lin_d, col_d = celula_da_data
        por_aba[aba_d].setdefault(lin_d, {})[col_d] = (date.today() - (date(1904, 1, 1) if em_1904 else date(1899, 12, 30))).days
        abas = _abas(zi)
        alvos = {abas[nome]: celulas_da_aba for nome, celulas_da_aba in por_aba.items()}
        # A formatação mexe em duas partes que precisam combinar — a aba (largura, e o
        # estilo de cada célula) e o styles.xml (os estilos novos) —, então sai antes do
        # laço de cópia, que grava as partes na ordem em que estão no modelo.
        prontas = {}
        if formata:
            parte = abas[formata[0]]
            aba = _ajusta_colunas(_preenche_aba(zi.read(parte).decode("utf-8"), alvos[parte]), LARGURA_PX)
            aba, estilos = _realinha(aba, zi.read("xl/styles.xml").decode("utf-8"), formata[1], ALINHAMENTO)
            prontas[parte], prontas["xl/styles.xml"] = aba.encode("utf-8"), estilos.encode("utf-8")
        for item in zi.infolist():
            dado = zi.read(item.filename)
            if item.filename in prontas:
                dado = prontas[item.filename]
            elif item.filename in alvos:
                dado = _preenche_aba(dado.decode("utf-8"), alvos[item.filename]).encode("utf-8")
            elif item.filename == "xl/workbook.xml":
                # cada fórmula guarda o valor da última conta — a do modelo vazio; sem isto
                # o leitor veria os totais zerados até mandar recalcular
                dado = re.sub(r"<calcPr\b(?![^>]*fullCalcOnLoad)", '<calcPr fullCalcOnLoad="1"',
                              dado.decode("utf-8"), count=1).encode("utf-8")
            zo.writestr(item, dado)

def insumo(chaves, ca, origem, ca_pe=None):
    """Coluna T (Insumo): cada ticket com os critérios de aceite da linha —
    `PDTIC25093-13 (CA-1, CA-3); PDTIC25093-14 (CA-2)`. Vale o critério do PROCESSO
    ELEMENTAR (`ca_pe`, da coluna `Critérios` da tabela de PE da AIM); sem ele, o da
    feature, que vem da AIM ou, na falta, da `## Origem` do N3; sem nenhum (a fonte não
    numera), só a chave."""
    ca_pe = ca_pe or {}
    return "; ".join(f"{k} ({c})" if (c := ca_pe.get(k) or ca.get(k) or origem.get(k, "")) else k
                     for k in chaves)

def main():
    ap = argparse.ArgumentParser(description="Planilha de entrega da contagem, no modelo do cliente, espelhada dos N3.")
    ap.add_argument("raiz", nargs="?", default=".", help="raiz da instância (padrão: a pasta atual)")
    ap.add_argument("-o", "--saida", default=None,
                    help="arquivo .xlsx ou pasta (padrão: SIGLA_SP000_PF_CD.xlsx ou "
                         "SIGLA_BASELINE_PF_CD.xlsx na raiz)")
    ap.add_argument("--sprint", default=None, metavar="NNN",
                    help="a planilha da sprint (ex.: 028): só o que a AIM da sprint e as AIMs dos "
                         "tickets dela cobrem, com os tickets dela; sem ela, a aplicação inteira (baseline)")
    ap.add_argument("--escopo", nargs="*", default=None, metavar="PREFIXO",
                    help="limita as transações às features com este prefixo de ID; "
                         "as funções de dados saem inteiras")
    ap.add_argument("--jira", nargs="*", default=None, metavar="CHAVE",
                    help="só o que estes tickets alcançaram nas AIMs (STRY…, ISSUE-n, "
                         "PDTIC…-n, EXP-…, Jira); sem valor, tudo o que alguma AIM cita — "
                         "inclusive o que foi entregue sem ticket")
    ap.add_argument("--estimada", action="store_true",
                    help="a contagem estimada: a `## Contagem estimada` das AIMs dos tickets (da --sprint "
                         "ou do --jira), na aba AFP - Estimativa — SIGLA_SP000_PF_CE.xlsx")
    a = ap.parse_args()

    raiz = Path(a.raiz).resolve()
    if not (raiz / "modules").is_dir():
        sys.exit(f"✗ Não parece uma instância (sem modules/): {raiz}")
    if not MODELO.exists():
        sys.exit(f"✗ Modelo do cliente ausente: {MODELO}")
    sprint = rotulo_sprint(a.sprint) if a.sprint else None
    if a.sprint and not sprint:
        sys.exit(f"✗ --sprint {a.sprint}: sem número de sprint (ex.: 028, SP028).")
    if sprint and not a.estimada and not any(k is None for k, _ in aims(raiz, sprint)):
        rotulos = sorted({front_matter(arq.read_text(encoding="utf-8")).get("sprint", "?")
                          for k, arq in aims(raiz) if k is None})
        sys.exit(f"✗ Nenhuma AIM da sprint {a.sprint} em {PASTA_AIM}/ "
                 f"(AIMs de sprint: {', '.join(rotulos) or 'nenhuma'}).")
    sigla, nome_sistema = identidade(raiz)
    nome_arq = nome_do_arquivo(sigla, sprint, "CE" if a.estimada else "CD") if sigla else None
    if a.saida and a.saida.lower().endswith(".xlsx"):
        saida = Path(a.saida)
    elif not nome_arq:
        sys.exit("✗ Sigla do sistema indefinida: declare `- **Sigla**: XXXXX` em global/MASTER.md "
                 "(é ela que dá nome ao arquivo), ou passe -o arquivo.xlsx.")
    elif a.estimada and not sprint:
        sys.exit("✗ --estimada sem --sprint: a estimada é de uma sprint (SIGLA_SP000_PF_CE.xlsx). "
                 "Para os tickets do --jira fora de uma sprint, dê o nome: -o arquivo.xlsx.")
    else:
        saida = (Path(a.saida) if a.saida else raiz) / nome_arq
    rotulo_os = "SP" + "-".join(f"{n:03d}" for n in sprint) if sprint else "Baseline"
    recorte_txt = escopo_da_contagem(sprint, a.jira, None if a.estimada else a.escopo)

    if a.estimada:
        linhas = estimativas(raiz, sprint, {k.upper() for k in a.jira} if a.jira else None)
        if not linhas:
            lidas = sum(1 for k, _ in aims(raiz, sprint) if k)
            sys.exit(f"✗ Nenhuma função estimada: {lidas} AIM(s) de ticket "
                     f"{'da sprint ' + a.sprint if sprint else 'na instância'}"
                     f"{' (--jira ' + ' '.join(a.jira) + ')' if a.jira else ''}, nenhuma com linhas na "
                     f"`## {SECAO_ESTIMADA}`. A sprint do ticket é o `sprint:` do front-matter da AIM.")
        escreve_estimada(linhas, saida, rotulo_os if sprint else " ".join(sorted({d["chave"] for d in linhas})), nome_sistema, recorte_txt)
        pfb = sum(PESO_ESTIMADO.get(d["tipo"], 0) for d in linhas)
        pfl = sum(PESO_ESTIMADO.get(d["tipo"], 0) * (0.5 if d["natureza"] == "alterada" else 1 if d["natureza"] else 0) for d in linhas)
        print(f"✓ {len(linhas)} função(ões) estimada(s) de {len({d['chave'] for d in linhas})} ticket(s) em {saida} — "
              f"{pfb} PFB · {f'{pfl:g}'.replace('.', ',')} PFL")
        print(f"   Escopo da Contagem (Resumo): {recorte_txt}")
        fora = [d for d in linhas if d["tipo"] not in PESO_ESTIMADO]
        if fora:
            print(f"⚠️  {len(fora)} linha(s) com tipo fora de EE/SE/CE/ALI/AIE — o PF da linha sai 0. Corrija na AIM:")
            for d in fora[:8]:
                print(f"      {d['chave']} — {d['pe']}: \"{d['tipo']}\"")
        sem_nat = [d for d in linhas if not d["natureza"]]
        if sem_nat:
            print(f"⚠️  {len(sem_nat)} linha(s) sem natureza (incluída/alterada) — Tipo Projeto (coluna B) em "
                  f"branco, e o PFL da linha sai 0. Corrija na AIM:")
            for d in sem_nat[:8]:
                print(f"      {d['chave']} — {d['pe']}")
        # Uma função conta uma vez na sprint, venha de quantos tickets vier. A planilha
        # espelha as AIMs — não deduplica —, mas a repetição não pode passar calada.
        vistas = {}
        for d in linhas:
            vistas.setdefault((chave_pe(d["pe"]), d["tipo"]), []).append(d["chave"])
        repetidas = {k: v for k, v in vistas.items() if len(set(v)) > 1}
        if repetidas:
            print(f"⚠️  {len(repetidas)} função(ões) estimada(s) em mais de um ticket — na sprint, cada função "
                  f"conta uma vez; a soma acima a conta em cada um:")
            for (pe, tipo), ks in list(repetidas.items())[:8]:
                print(f"      {pe} ({tipo}) — {', '.join(sorted(set(ks)))}")
        return
    # Com recorte (sprint ou tickets), a natureza de cada PE decide o Tipo Projeto; sem
    # ele, é a baseline: o tamanho da aplicação inteira.
    recorte = sprint is not None or a.jira is not None

    linhas = []
    for p in sorted(raiz.glob("modules/**/f-*.md")):
        linhas += processos(p)
    estimadas = {}   # o que a AIM ainda traz `(E)`: fica fora, e o aviso diz o quê
    impacto = mapa_tickets(raiz, sprint, estimadas)
    for d in linhas:
        info = impacto.get(d["id"])
        d["jira"] = " ".join(info["jira"]) if info else ""
        # A natureza é da FEATURE; o PE herda. Um PE nasce dentro de uma feature
        # incluída ou dentro de uma alterada — não há terceiro caso no delta.
        d["natureza"] = (info or {}).get("natureza", "")
        d["na_sprint"] = info is not None
        # O critério é do PE quando a AIM o diz (coluna `Critérios` da tabela de PE);
        # senão é o da feature, e o PE herda os do ticket que a alcançou.
        do_pe = (info or {}).get("ca_pe", {})
        d["ca_do_pe"] = chave_pe(d["pe"]) in do_pe
        d["insumo"] = insumo(info["jira"], info["ca"], d["origem_ca"], do_pe.get(chave_pe(d["pe"]))) if info else ""
        d["tipo_projeto"] = TIPO_PROJETO.get(d["natureza"], "") if recorte else TIPO_PROJETO_BASELINE
    contadas = len(linhas)
    if a.escopo:
        linhas = [d for d in linhas if any(d["id"].startswith(e.upper()) for e in a.escopo)]
    no_escopo = len(linhas)
    if recorte:
        alvo = {k.upper() for k in a.jira or []}
        # Sem chaves informadas: tudo o que as AIMs lidas cobrem — inclusive o que foi
        # entregue sem item no Jira. Filtrar por `d["jira"]` deixaria essas de fora.
        linhas = [d for d in linhas
                  if (d["na_sprint"] and (not alvo or any(k.upper() in alvo for k in d["jira"].split())))]
        # PE com PF de feature cujos PEs a AIM lista, e que não está na lista: não foi
        # alcançado pela sprint. A linha de 0 PF fica (o PO quer ver o não contado).
        def alcancado(d):
            pes = (impacto.get(d["id"]) or {}).get("pes")
            if not pes or not d["tipo"] or chave_pe(d["pe"]) in pes:
                return True
            PES_FORA.append(d); return False
        linhas = [d for d in linhas if alcancado(d)]
    linhas.sort(key=lambda d: (d["id"], d["pe"]))

    # Planilha vazia pode ter três causas, e cada uma se corrige num lugar diferente:
    # dizer só "nenhum processo contado" mandava procurar o erro no N3 quando o que
    # esvaziou a lista foi o filtro — ou uma AIM que o script não reconheceu.
    if not linhas:
        if not contadas:
            sys.exit("✗ Nenhum processo elementar contado encontrado (coluna PF preenchida no N3).")
        if not no_escopo:
            sys.exit(f"✗ {contadas} processo(s) contado(s), nenhum com o prefixo {' '.join(a.escopo)}.")
        rels = aims(raiz, sprint)
        chaves = sorted({k for info in impacto.values() for k in info["jira"]})
        sys.exit(f"✗ {no_escopo} processo(s) contado(s), nenhum alcançado "
                 f"{'por ' + ' '.join(a.jira) if a.jira else 'por AIM'}. "
                 f"AIMs lidas ({PASTA_AIM}/): {sum(1 for k, _ in rels if k)} "
                 f"de ticket, {sum(1 for k, _ in rels if not k)} de sprint; "
                 f"chaves encontradas: {', '.join(chaves) or 'nenhuma'}."
                 + (f" {len(estimadas)} feature(s) ainda com a contagem estimada `(E)` na AIM "
                    f"({', '.join(sorted(estimadas))}) — a planilha delas é a --estimada." if estimadas else ""))

    # Critério escrito na AIM para um PE que não existe no N3 com aquele nome não chega à
    # planilha — e a linha sai só com a chave, com a mesma cara de "a fonte não numera".
    nomes_no_n3 = {(d["id"], chave_pe(d["pe"])) for d in linhas}
    ids_na_planilha = {d["id"] for d in linhas}
    orfaos = sorted((fid, pe) for fid, info in impacto.items() if fid in ids_na_planilha
                    for pe in info.get("ca_pe", {}) if (fid, pe) not in nomes_no_n3)
    if orfaos:
        print(f"⚠️  {len(orfaos)} processo(s) elementar(es) com `Critérios` na AIM que não casam com "
              f"nenhum PE do N3 — o critério não chegou à planilha. Acerte o nome na tabela de "
              f"processos elementares da AIM:")
        for fid, pe in orfaos[:8]:
            print(f"      {fid} — {pe}")
    if CA_PE_DIVERGENTES:
        print(f"⚠️  {len(CA_PE_DIVERGENTES)} processo(s) elementar(es) com `Critérios` diferentes na AIM do "
              f"ticket e na da sprint — vale a do ticket. Acerte o espelho:")
        for fid, pe, chave, vale, outro in CA_PE_DIVERGENTES[:8]:
            print(f"      {fid} — {pe} ({chave}): {vale} ≠ {outro}")

    dados = funcoes_de_dados(raiz)
    jira_d, depois = mapa_tickets_dados(raiz, sprint, estimadas)
    nat_d = natureza_dados(raiz, sprint)
    for d in dados:
        d["jira"] = " ".join(jira_d.get(d["pe"], []))
        d["natureza"] = nat_d.get(d["pe"], "")
        # Na sprint = alguma AIM a cita: a do ticket (Funções de dados alteradas) ou a
        # da sprint, que é a única fonte da função de dados alterada sem ticket — o
        # mesmo critério das transações.
        d["na_sprint"] = bool(d["jira"] or d["natureza"])
        # No modelo, o domínio da função de dados é o Módulo; ela não tem Requisito (N2).
        d["modulo"], d["requisito"] = d["requisito"], ""
        d["insumo"] = "; ".join(jira_d.get(d["pe"], []))
        d["tipo_projeto"] = TIPO_PROJETO.get(d["natureza"], "") if recorte else TIPO_PROJETO_BASELINE
        alt = depois.get(d["pe"])
        if alt:
            # a célula passa a levar o tamanho DEPOIS; o antes fica na descrição
            nota, sem_antes = [], False
            incluida = (alt.get("natureza") or d["natureza"]) == "incluída"
            for chv, campo in (("rlr", "alr_qtd"), ("der", "der_qtd")):
                if alt[chv]:
                    antes, dps = alt[chv]
                    d[campo] = dps
                    sem_antes |= not antes.isdigit()
                    # função incluída não tem antes: o "0 →" da AIM só diz que ela não existia
                    nota.append(f"{chv.upper()} {dps}" if incluida
                                else f"{chv.upper()} {antes if antes.isdigit() else '?'} → {dps}")
            # A nota NÃO entra na enumeração: aquela coluna é a lista de DER e
            # nada mais — recado no meio dos campos faz o primeiro item parecer um
            # deles. Vai para a Observação (coluna U) da mesma linha.
            quem = d["jira"] or "item sem chave"
            if nota and incluida:
                d["nota_alt"] = f"Incluído por {quem}: " + " · ".join(nota) + "."
            elif nota:
                d["nota_alt"] = (f"Alterado por {quem}: " + " · ".join(nota)
                                 + (". O tamanho antes da alteração não foi apurado" if sem_antes else "")
                                 + ". A quantidade é a DEPOIS da alteração, base do CHGA.")
    if recorte:
        alvo = {k.upper() for k in a.jira or []}
        dados = [d for d in dados
                 if (d["na_sprint"] and (not alvo or any(k.upper() in alvo for k in d["jira"].split())))]

    escreve(linhas + dados, saida, rotulo_os, nome_sistema, recorte_txt)
    n = len(linhas)
    print(f"✓ {n} processo(s) elementar(es) e {len(dados)} função(ões) de dados em {saida}")
    print(f"   Escopo da Contagem (Resumo): {recorte_txt}")
    if PES_FORA:
        print(f"   {len(PES_FORA)} PE(s) de feature alcançada fora do recorte — as AIMs listam os PEs "
              f"que a entrega alcançou, e estes não estão lá:")
        for d in PES_FORA:
            print(f"      {d['id']} — {d['pe']} ({d['tipo']})")
    if estimadas:
        print(f"⚠️  {len(estimadas)} com a contagem ainda ESTIMADA `(E)` na AIM — o ticket não entra nesta "
              f"planilha: a detalhada só leva o que foi contado no N3 e no DATA-MODEL. Conte "
              f"(PROMPT_CONTAGEM), atualize a AIM e gere de novo; a planilha da estimativa é a --estimada:")
        for alvo, ks in sorted(estimadas.items())[:12]:
            print(f"      {alvo} — {', '.join(ks) or 'sem ticket'}")
    if not dados:
        print("⚠️  Nenhuma função de dados — a contagem sai pela metade. "
              "A fonte é global/DATA-MODEL.md (tabelas de ALIs e de AIEs) + global/data-models/*.md.")
    # É o tipo que escolhe a tabela de peso (ALI 7/10/15, AIE 5/7/10). A planilha fica
    # com o do índice — foi com ele que o PF do índice foi calculado —, mas índice e
    # registro discordando é erro de um dos dois, e não cabe à planilha arbitrar.
    tipo_dif = [d for d in dados if d.get("tipo_registro") and d["tipo_registro"] != d["tipo"]]
    if tipo_dif:
        print(f"⚠️  {len(tipo_dif)} arquivo(s) lógico(s) com tipo diferente no DATA-MODEL e no "
              f"ALI-AIE-MAP — o tipo escolhe o peso; corrija a fonte errada:")
        for d in tipo_dif[:8]:
            print(f"      {d['pe']}: {d['tipo']} no DATA-MODEL · {d['tipo_registro']} no ALI-AIE-MAP")
    # A enumeração de campos NÃO é a lista de DER que o baseline contou: o
    # data-model lista atributos físicos da engenharia reversa, e o DER do CPM é
    # elemento reconhecido pelo usuário, sem repetição, considerando todos os PE.
    # Divergir é o esperado — o que não pode é passar despercebido.
    dif = []
    for d in dados:
        if str(d["der_qtd"]).isdigit():
            n = len([x for x in d["der_desc"].split("\n") if x.strip() and not x.startswith("[")])
            if n != int(d["der_qtd"]):
                dif.append((d["pe"], d["der_qtd"], n))
    if dif:
        print(f"ℹ️  {len(dif)} arquivo(s) lógico(s) em que a quantidade de DER do baseline difere "
              f"do número de campos do data-model — esperado, são populações diferentes:")
        for pe, q, n in dif:
            print(f"      {pe}: DER {q} no baseline · {n} campos no data-model")

    # O RLR do baseline e as entidades constituintes descrevem a mesma coisa por
    # dois caminhos: quantos subgrupos reconhecíveis o arquivo lógico tem, e quais
    # são eles. Divergir não prova erro — o CPM permite agrupar várias entidades
    # físicas num único RET —, mas a lista deixa de sustentar o número, e é isso
    # que a auditoria vai perguntar. Sinalizar, não arbitrar.
    rlr_dif = []
    for d in dados:
        if str(d["alr_qtd"]).isdigit() and d["alr_desc"]:
            n_ent = len([x for x in d["alr_desc"].split("\n") if x.strip()])
            if n_ent != int(d["alr_qtd"]):
                rlr_dif.append((d["pe"], d["alr_qtd"], n_ent))
    if rlr_dif:
        print(f"⚠️  {len(rlr_dif)} arquivo(s) lógico(s) em que o RLR não bate com as entidades "
              f"constituintes enumeradas — a lista não sustenta o número. Pode ser agrupamento "
              f"legítimo de entidades num mesmo RET; confirme com a equipe de métricas:")
        for pe, q, n_ent in rlr_dif:
            print(f"      {pe}: RLR {q} · {n_ent} entidade(s) enumerada(s)")

    sem_ent = [d for d in dados if not d["alr_desc"]]
    if sem_ent:
        print(f"⚠️  {len(sem_ent)} função(ões) de dados sem entidades constituintes — coluna "
              f"Descrição de RLR vazia: {', '.join(d['pe'] for d in sem_ent[:6])}")

    # Num recorte (sprint ou tickets) toda linha tem de ter natureza: é ela que escolhe o
    # Tipo Projeto e, com ele, se o processo entra inteiro (incluído) ou pela metade
    # (alterado). Sem ela, a coluna B sai em branco e o fator do PFL, zero. Na baseline
    # não se aplica — tudo é Aplicação/Desenvolvimento.
    sem_nat = [d for d in linhas + dados if recorte and d.get("na_sprint", True) and not d.get("natureza")]
    if sem_nat:
        print(f"⚠️  {len(sem_nat)} linha(s) sem natureza (incluído/alterado) — Tipo Projeto (coluna B) "
              f"em branco, e o PFL da linha sai 0 até alguém escolher. A fonte é a coluna "
              f"`Natureza` das AIMs:")
        for d in sem_nat[:8]:
            print(f"      {d.get('id', d['pe'])} — {d['pe']}")

    sem_n2 = [d for d in linhas if not d["requisito"]]
    if sem_n2:
        print(f"⚠️  {len(sem_n2)} sem N2 resolvido — coluna Requisito vazia. "
              f"O nome sai do `# Feature Set: X` do README ao lado do N3.")
        for d in sem_n2[:6]:
            print(f"      {d['id']} — {d['pe']}")

    sem_mem = [d for d in linhas if not d["tem_memoria"]]
    if sem_mem:
        print(f"⚠️  {len(sem_mem)} sem a enumeração na memória de cálculo — colunas Descrição vazias. "
              f"Ela é um bloco ```json por processo elementar na ### Memória de cálculo do N3; "
              f"memória antiga: python3 scripts/migra-enumeracao.py.")
        for d in sem_mem[:6]:
            print(f"      {d['id']} — {d['pe']}")

    # A lista consultada não exibe mensagem (decisão do PO, 2026-10-02): o PE de combo,
    # autocomplete, carrossel… que conta o DER Mensagem contou um a mais. A planilha
    # espelha a contagem — não tira o DER —, mas diz onde corrigir.
    lista_com_msg = [d for d in linhas if LISTA_CONSULTADA.search(d["pe"]) and "Mensagem" in d["der_desc"].split("\n")]
    if lista_com_msg:
        print(f"⚠️  {len(lista_com_msg)} PE de lista consultada com o DER Mensagem — combo, autocomplete, carrossel "
              f"e botões não exibem mensagem: o DER sobra. Recorte no N3 (`## Métricas de tamanho`):")
        for d in lista_com_msg[:12]:
            print(f"      {d['id']} — {d['pe']}")

    # Memória que não bate com o número não sustenta o número: se a quantidade
    # declarada difere do que a descrição enumera, uma das duas está errada.
    def itens(s):
        return len([x for x in s.split("\n") if x.strip()])
    divergem = []
    for d in linhas:
        if not d["der_desc"] and not d["alr_desc"]:
            continue
        for rot, qtd, desc in (("DER", d["der_qtd"], d["der_desc"]), ("ALR", d["alr_qtd"], d["alr_desc"])):
            if qtd.isdigit() and itens(desc) != int(qtd):
                divergem.append(f"{d['id']} — {d['pe']}: {rot} diz {qtd}, a memória enumera {itens(desc)}")
    if divergem:
        print(f"⚠️  {len(divergem)} divergência(s) entre a quantidade e o que a memória enumera:")
        for x in divergem[:8]:
            print(f"      {x}")
        print("      Corrija no N3 — a planilha espelha a fonte, não a conserta.")

if __name__ == "__main__":
    main()
