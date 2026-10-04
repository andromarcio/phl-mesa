#!/usr/bin/env node
// validate-impact.mjs — valida uma AIM (Análise de Impacto) e suas invariantes.
//
// A AIM é o artefato do ticket (decisão do PO, 2026-09-28): um arquivo por ticket em
// `analise-impacto/AIM-<CHAVE>.md`, versionado à medida que o ticket avança — aberto pelo
// PROMPT_AIM com o ticket, o que ele VAI alterar e o aval do PO; fechado depois da entrega
// pela skill analise-impacto com o que ele ALTEROU. A AIM da sprint
// (`analise-impacto/AIM-<sprint>.md`) consolida os tickets entregues na sprint. Este
// validador é o contrato determinístico das duas: estrutura + cobertura + reconciliação.
// Não julga o conteúdo.
//
// AIM do ticket (`tipo: ticket`):
//   front-matter  `ticket` (a mesma chave do nome do arquivo) e `estado` da esteira:
//                 rascunho → em-análise → escopo-aprovado → em-execução → concluído
//   seções        Detalhe do item · Critérios de aceite · Features · Artefatos
//                 impactados · Alterações na spec, por Feature Set · Reconciliação ·
//                 Changelog (a `## Contagem estimada` tem regra própria, abaixo)
//   de em-análise em diante: a `## Features` com ao menos uma feature, e o changeset sem
//                 linha de exemplo do template e com as invariantes de cobertura:
//     C1  ao menos uma linha N3 (a feature-âncora)
//     C2  linha `funcional`     → linha `QA`   (mudança funcional é testada)
//     C3  linha `não-funcional` → linha `NFR` E linha `QA` (NFR verificável)
//     AIM aberta na entrega (`aberta-na-entrega: true`): C2 e C3 viram aviso — não houve
//     escopo prévio a cobrir.
//     Existência: `alterar` sobre arquivo que não existe é erro; `criar` sobre arquivo que
//     já existe é aviso só até `escopo-aprovado` — depois, a execução o criou.
//   escopo-aprovado|em-execução|concluído → `avalizado-por`
//   concluído     → `sprint`; a visão final em `## Alterações na spec, por Feature Set`
//                   (linha com ID de feature, sem exemplo do template); e a
//                   `## Reconciliação` preenchida — com conteúdo fora da citação de
//                   instrução, que pode ficar.
//
//   Contagem estimada (decisão do PO, 2026-10-02) — o tamanho que o PO avaliza com o
//   escopo, antes de haver N3 que sustente a detalhada. Uma linha por função, com o peso
//   fixo do tipo (aba "AFP - Estimativa" do modelo do cliente):
//     E1  de `em-análise` a `em-execução`, a `## Contagem estimada` com ao menos uma
//         função, sem exemplo do template (na `concluído` sem ela, aviso; AIM aberta na
//         entrega não tem estimativa);
//     E2  cada linha: Tipo EE|SE|CE|ALI|AIE, Natureza incluída|alterada, PFB = o peso
//         (EE 4 · CE 4 · SE 5 · ALI 7 · AIE 5), PFL = PFB na incluída e metade na
//         alterada; a linha Total = a soma;
//     E3  o quadro `### Estimada × detalhada`: Estimada = o Total; com a Detalhada
//         preenchida, Diferença = Detalhada − Estimada. Na `concluído`, o quadro é
//         obrigatório e a Detalhada = a soma da `## Alterações na spec` com a das
//         funções de dados (título `### ALI: … · n PF · alterada`).
//
//   AIM viva (decisão do PO, 2026-10-02) — a AIM muda a cada artefato que muda por causa
//   do ticket. DEFASADA é a que ficou para trás; de `em-execução` em diante:
//     D1  feature com PFB/PFL estimado `(E)` cujo N3 cita o ticket e já tem a contagem
//         revista (PE contado e `contagem.pendente` diferente de `true`);
//     D2  linha do changeset `previsto` cujo artefato já existe (`criar`) ou já cita a
//         chave do ticket (`alterar`); linha `feito` de arquivo que não existe é erro;
//     D3  (sempre aviso) PFB detalhado que o N3 não sustenta: maior que a soma dos PE
//         contados, ou — na feature incluída — diferente dela e da dos `principal`.
//     Em `em-execução`, D1 e D2 são AVISO; na `concluído`, REPROVAM — e ali nenhuma
//     linha fica `previsto` (é `feito em …` ou `não feito`), nenhum `(E)` sobra nas
//     seções de impacto e toda feature traz PFB e PFL em número. A coluna Situação é
//     posterior à AIM única: tabela sem ela só avisa.
//     `--defasagem` imprime só D1 e D2 e sai 1 se houver — é o que o hook spec-guard
//     roda quando um artefato do changeset é gravado.
//
//   Critério por processo elementar (decisões do PO, 2026-10-02 e 2026-10-04) — a tabela
//   de PE da `## Alterações na spec` (`Processo elementar | Da feature | …`) pode trazer a
//   coluna `Critérios`, que a planilha de entrega leva ao Insumo de cada linha:
//     P1  (sempre aviso) critério citado que a `## Critérios de aceite` não tem. Vale
//         QUALQUER critério do card — inclusive o que a `## Features` dá a outra feature,
//         quando ele alcança aquele PE; o que não vale é o que o card não traz.
//
// AIM da sprint (`tipo: sprint`): `sprint` no front-matter; `## Tickets da sprint` e
// `## Alterações na spec, por Feature Set` com linhas; e conferida com as AIMs dos tickets
// da pasta (em `concluído` reprova; em `rascunho`, avisa):
//     S1  os mesmos tickets — cada listado com a sua AIM, de `sprint:` igual; e toda AIM
//         com `sprint:` igual, listada — com a AIM concluída;
//     S2  cada feature e cada função de dados UMA vez; a coluna Ticket só com tickets
//         listados;
//     S3  a visão final de cada ticket dentro da sprint, nos dois sentidos: a feature
//         que ele alterou está na linha que cita a chave dele, e a linha que cita a chave
//         está na visão final dele; cada `### ALI|AIE:` dele, em `## Funções de dados
//         alteradas`; natureza incluída se algum ticket a incluiu, alterada se não
//         (PFB/PFL diferente do ticket único é aviso: os dois espelham o N3);
//     S4  o `## Apurável da sprint` como a soma das linhas — o Total sempre; Transações e
//         Funções de dados, quando a tabela as traz; Estimado (a soma da `## Contagem
//         estimada` dos tickets da sprint) e Diferença (Total − Estimado), também quando
//         a tabela os traz. Sem a seção, na concluída, é aviso.
//
// Formato anterior à AIM única — registro `demandas/<chave>.md`, `impactos/AIM-AAAA-NNN.md`
// do PROMPT_IMPACTO, relatório `ANALISE_IMPACTO_*.md` — reprova, com a instrução de migrar.
//
// Reconciliação (opcional):
//   --touched "a,b,c"    compara os artefatos declarados (caminhos) com esta lista
//   --git-base <ref>     usa `git -C <root> diff --name-only <ref>...HEAD`
//   → declarado e não tocado = escopo não cumprido; tocado e não declarado = desvio.
//
// Uso:
//   node scripts/validate-impact.mjs <analise-impacto/AIM-….md> [--root <inst>] [--touched …|--git-base …] [--defasagem]

import { readFileSync, existsSync, readdirSync, statSync } from 'node:fs';
import { join, dirname, basename, relative } from 'node:path';
import { execFileSync } from 'node:child_process';
import { pesDoN3, contado } from './lib/pe.mjs';
import { frontMatterBloco } from './lib/front-matter.mjs';

const args = process.argv.slice(2);
const opt = (n, d = null) => { const i = args.indexOf(n); return i !== -1 && args[i + 1] ? args[i + 1] : d; };
const FILE = args.find((a, k) => !a.startsWith('--') && a.endsWith('.md') && !['--root', '--touched', '--git-base'].includes(args[k - 1]));
if (!FILE || !existsSync(FILE)) {
  console.error('Uso: node scripts/validate-impact.mjs <analise-impacto/AIM-….md> [--root <inst>] [--touched …|--git-base …] [--defasagem]');
  process.exit(2);
}
const ROOT = opt('--root', dirname(dirname(FILE)) || '.');
const raw = readFileSync(FILE, 'utf8');
const lines = raw.split(/\r?\n/);
const errors = [];
const warns = [];
const norm = (s) => String(s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().trim();

const sai = () => {
  console.log(`validate-impact — ${FILE}`);
  for (const w of warns) console.log(`  ⚠️  ${w}`);
  if (errors.length) {
    for (const e of errors) console.log(`  ✗ ${e}`);
    console.log(`\n${errors.length} erro(s), ${warns.length} aviso(s).`);
    process.exit(1);
  }
};

/* ------------------------- front-matter ------------------------- */
// Carimbo e linhas em branco antes do `---`, como o leitor único (lib/front-matter.mjs);
// o comentário de fim de linha (`campo: valor  # …`) não faz parte do valor.
function frontMatter(ls) {
  const out = {};
  let i = 0;
  while (i < ls.length && (!ls[i].trim() || /^\s*<!--.*-->\s*$/.test(ls[i]))) i++;
  if (ls[i] && ls[i].trim() === '---') {
    for (i++; i < ls.length && ls[i].trim() !== '---'; i++) {
      const m = ls[i].match(/^([a-z][\w-]*):\s*(.*)$/i);
      if (m) out[m[1].toLowerCase()] = m[2].replace(/\s+#.*$/, '').trim().replace(/^(["'])(.*)\1$/, '$2');
    }
  }
  return out;
}
const fm = frontMatter(lines);

/* --------------------- formato anterior --------------------- */
const MIGRE = 'o ticket agora tem uma AIM só, em `analise-impacto/AIM-<CHAVE>.md` — migre (CHANGELOG → 3.0.0, "AIM única")';
if (basename(FILE).startsWith('ANALISE_IMPACTO_')) {
  errors.push(`relatório pós-entrega no formato anterior (\`ANALISE_IMPACTO_*\`): ${MIGRE}.`);
  sai();
}
if (/(^|[\\/])demandas[\\/]/.test(FILE)) {
  errors.push(`registro do ticket no formato anterior (\`demandas/\`): ${MIGRE}.`);
  sai();
}
if (!fm.tipo && (fm['feature-ancora'] || fm['feature-âncora'] || fm.origem)) {
  errors.push(`AIM no formato anterior (PROMPT_IMPACTO, \`feature-ancora\`/\`origem\`, sem \`tipo\`): ${MIGRE}.`);
  sai();
}

const tipo = norm(fm.tipo);
if (!['ticket', 'sprint'].includes(tipo)) {
  errors.push('front-matter sem `tipo: ticket` ou `tipo: sprint`.');
  sai();
}

/* ----------------------------- apoio ----------------------------- */
const ID_RE = /\b[A-Z]{3}-[A-Z]{3}-\d{2}\b/;
const splitRow = (r) => r.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map((c) => c.trim());
const temSecao = (s) => lines.some((l) => l.trim() === `## ${s}`);
const corpoDe = (s, ls = lines) => {
  const i = ls.findIndex((l) => l.trim() === `## ${s}`);
  if (i < 0) return [];
  const out = [];
  for (let k = i + 1; k < ls.length && !/^##\s/.test(ls[k].trim()); k++) out.push(ls[k]);
  return out;
};
// Tabelas de uma seção: [{ cab: [...], linhas: [[...]] }] — sem o separador.
const tabelasDe = (s, ls = lines) => {
  const out = [];
  let atual = null;
  for (const l of corpoDe(s, ls).map((x) => x.trim())) {
    if (!l.startsWith('|')) { atual = null; continue; }
    if (/^\|[\s:|-]+\|?$/.test(l)) continue;
    if (!atual) { atual = { cab: splitRow(l).map(norm), linhas: [] }; out.push(atual); continue; }
    atual.linhas.push(splitRow(l));
  }
  return out;
};
const EXEMPLO = /\[[^\]]*\]|<(?:dom|fs|slug|CHAVE)>|SIGLA-SFS-NN/i; // placeholder do template
const semComentario = (s) => corpoDe(s).join('\n').replace(/<!--[\s\S]*?-->/g, '');
const conteudoForaDaCitacao = (s) => semComentario(s).split('\n')
  .filter((l) => l.trim() && !/^\s*>/.test(l));
const num = (c) => {
  const m = String(c ?? '').replace(/\*/g, '').replace(/−/g, '-').match(/-?\d+(?:[.,]\d+)?/);
  return m ? Number(m[0].replace(',', '.')) : null;
};
const fmt = (x) => (x == null ? '—' : String(Math.round(x * 100) / 100).replace('.', ','));
const igual = (a, b) => a != null && b != null && Math.abs(a - b) <= 0.005;
// Vale a palavra, não a célula: `incluída (proposta)` e `alterada · superfície` são
// incluída e alterada. Comparada inteira, a célula com qualificador divergia da
// palavra esperada, e a mensagem mostrava os dois lados iguais.
const natureza = (c) => {
  const v = norm(c).replace(/[`*]/g, '').trim();
  const w = (v.match(/^(incluida|alterada|nova)\b/) || [])[1] || v;
  return w === 'nova' ? 'incluida' : w;
};
const ESTIMADO = /\(E\)/; // a marca de "ainda estimado" — na célula ou no cabeçalho da coluna

// A contagem estimada de uma AIM: uma linha por função, com o peso fixo do tipo — o da
// aba "AFP - Estimativa" do modelo do cliente. null quando a AIM não tem a tabela.
const PESO_ESTIMADO = { EE: 4, CE: 4, SE: 5, ALI: 7, AIE: 5 };
function estimativaDe(ls) {
  const tabs = tabelasDe('Contagem estimada', ls);
  const t = tabs.find((x) => x.cab.includes('tipo') && x.cab.includes('pfb') && x.cab.includes('pfl'));
  const q = tabs.find((x) => x.linhas.some((c) => /^estimada$/.test(norm(c[0]).replace(/\*/g, ''))));
  if (!t) return null;
  const i = (h) => t.cab.indexOf(h);
  const [iFn, iT, iN, iB, iL] = [Math.max(i('funcao'), 0), i('tipo'), i('natureza'), i('pfb'), i('pfl')];
  const ehTotal = (c) => /^total/.test(norm(c[0]).replace(/\*/g, ''));
  const funcoes = t.linhas.filter((c) => !ehTotal(c)).map((c) => ({
    nome: (c[iFn] || '').replace(/[`*]/g, '').trim(), tipo: (c[iT] || '').replace(/[`*]/g, '').trim().toUpperCase(),
    natureza: iN >= 0 ? natureza(c[iN]) : '', pfb: num(c[iB]), pfl: num(c[iL]), exemplo: EXEMPLO.test(c.join(' ')),
  }));
  const total = t.linhas.find(ehTotal);
  const linhaDoQuadro = (re) => {
    const c = q && q.linhas.find((x) => re.test(norm(x[0]).replace(/\*/g, '')));
    return c ? { pfb: num(c[q.cab.indexOf('pfb')]), pfl: num(c[q.cab.indexOf('pfl')]), exemplo: EXEMPLO.test(c.join(' ')) } : null;
  };
  return {
    funcoes,
    total: total ? { pfb: num(total[iB]), pfl: num(total[iL]), exemplo: EXEMPLO.test(total.join(' ')) } : null,
    quadro: q ? { estimada: linhaDoQuadro(/^estimada$/), detalhada: linhaDoQuadro(/^detalhada$/), diferenca: linhaDoQuadro(/^diferenca$/) } : null,
  };
}

/* =========================== AIM da sprint =========================== */
if (tipo === 'sprint') {
  if (!fm.sprint || EXEMPLO.test(fm.sprint)) errors.push('front-matter sem `sprint:` (o rótulo da sprint).');
  for (const s of ['Tickets da sprint', 'Alterações na spec, por Feature Set']) {
    if (!temSecao(s)) errors.push(`falta a seção \`## ${s}\`.`);
  }
  const tickets = tabelasDe('Tickets da sprint').flatMap((t) => t.linhas).filter((c) => !EXEMPLO.test(c[0] || ''));
  const feats = tabelasDe('Alterações na spec, por Feature Set').flatMap((t) => t.linhas)
    .filter((c) => ID_RE.test(c[0] || '') && !EXEMPLO.test(c.join(' ')));
  if (temSecao('Alterações na spec, por Feature Set') && !feats.length)
    errors.push('`## Alterações na spec, por Feature Set` sem linha de feature — a AIM da sprint consolida as features entregues.');
  const conferidas = confereSprint(tickets);
  sai();
  console.log(`  ✓ AIM da sprint bem-formada — ${tickets.length} ticket(s), ${feats.length} feature(s), conferida com ${conferidas} AIM(s) de ticket${warns.length ? `, ${warns.length} aviso(s)` : ''}.`);
  process.exit(0);
}

// A AIM da sprint consolida as AIMs dos tickets (decisão do PO, 2026-09-28): os mesmos
// tickets — os de `sprint:` igual, cada um com a sua AIM —, cada feature e cada função de
// dados UMA vez, a visão final de cada ticket concluído dentro dela, e o apurável como a
// soma das linhas. Na AIM `concluído`, divergência reprova; em `rascunho`, a consolidação
// está em curso e ela é aviso. Devolve quantas AIMs de ticket da sprint foram conferidas.
function confereSprint(tickets) {
  const fechada = norm(fm.estado) === 'concluido';
  const acusa = (msg) => (fechada ? errors : warns).push(msg);
  const rotulo = String(fm.sprint || '').trim();
  const col = (t, re) => t.cab.findIndex((h) => re.test(h));
  const esc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const listados = [...new Set(tickets.map((c) => ((c[0] || '').match(/`([^`]+)`/) || [])[1])
    .filter(Boolean).map((k) => k.trim().toUpperCase()))];
  // A coluna Ticket: as chaves em crase (um ID de feature citado não é chave) e, sem
  // crase, as dos tickets listados — "⚠️ sem ticket" não traz nenhuma.
  const chavesDe = (cel) => {
    const s = String(cel || '');
    const out = (s.match(/`([^`]+)`/g) || []).map((x) => x.replace(/`/g, '').trim().toUpperCase())
      .filter((k) => k && !/^[A-Z]{3}-[A-Z]{3}-\d{2}$/.test(k));
    for (const k of listados)
      if (!out.includes(k) && new RegExp(`(?<![\\w-])${esc(k)}(?![\\w-])`, 'i').test(s)) out.push(k);
    return out;
  };
  const alteracoesDe = (ls) => tabelasDe('Alterações na spec, por Feature Set', ls).flatMap((t) => {
    const iF = Math.max(col(t, /^feature$/), 0);
    const iT = col(t, /^(ticket|item do jira)$/);
    const iN = col(t, /^natureza$/);
    const iB = col(t, /^pfb$/);
    const iL = col(t, /^pfl$/);
    return t.linhas.map((c) => ({ c, m: (c[iF] || '').match(ID_RE) }))
      .filter(({ c, m }) => m && !EXEMPLO.test(c.join(' ')))
      .map(({ c, m }) => ({
        id: m[0], chaves: iT >= 0 ? chavesDe(c[iT]) : [], natureza: iN >= 0 ? natureza(c[iN]) : '',
        pfb: iB >= 0 ? num(c[iB]) : null, pfl: iL >= 0 ? num(c[iL]) : null,
      }));
  });

  // O que a sprint diz.
  const linhas = alteracoesDe(lines);
  const funcoes = tabelasDe('Funções de dados alteradas').flatMap((t) => {
    const iF = col(t, /^funcao de dados$/);
    if (iF < 0) return [];
    return t.linhas.map((c) => ({ nome: (c[iF] || '').replace(/[`*]/g, '').trim(), pfb: num(c[col(t, /^pfb$/)]), pfl: num(c[col(t, /^pfl$/)]) }))
      .filter((f) => f.nome && !EXEMPLO.test(f.nome));
  });
  const repetidos = (arr) => [...arr.reduce((m, x) => m.set(x, (m.get(x) || 0) + 1), new Map())].filter(([, n]) => n > 1);
  for (const [id, n] of repetidos(linhas.map((l) => l.id)))
    acusa(`\`${id}\` aparece ${n} vezes em \`## Alterações na spec, por Feature Set\` — na AIM da sprint, cada feature entra uma vez (a coluna Ticket junta as chaves).`);
  for (const [nome, n] of repetidos(funcoes.map((f) => norm(f.nome))))
    acusa(`a função de dados \`${nome}\` aparece ${n} vezes em \`## Funções de dados alteradas\` — cada função entra uma vez.`);
  for (const l of linhas) for (const k of l.chaves)
    if (!listados.includes(k)) acusa(`\`${l.id}\` cita o ticket \`${k}\`, que não está em \`## Tickets da sprint\`.`);

  // O que as AIMs dos tickets dizem: os mesmos tickets, nos dois sentidos.
  const dir = dirname(FILE);
  const aims = readdirSync(dir).filter((n) => /^AIM-.+\.md$/.test(n)).map((n) => {
    const ls = readFileSync(join(dir, n), 'utf8').split(/\r?\n/);
    const f = frontMatter(ls);
    return { n, ls, fm: f, k: String(f.ticket || '').trim().toUpperCase() };
  }).filter((a) => norm(a.fm.tipo) === 'ticket' && a.k);
  const daSprint = rotulo ? aims.filter((a) => norm(a.fm.sprint) === norm(rotulo)) : [];
  for (const a of daSprint)
    if (!listados.includes(a.k)) acusa(`o ticket \`${a.k}\` tem \`sprint: ${rotulo}\` (\`${a.n}\`), mas não está em \`## Tickets da sprint\`.`);
  for (const k of listados) {
    const a = aims.find((x) => x.k === k);
    if (!a) acusa(`ticket \`${k}\` sem AIM em \`${dir}/\` — a sprint consolida as AIMs dos tickets.`);
    else if (norm(a.fm.sprint) !== norm(rotulo))
      acusa(`o ticket \`${k}\` está em \`## Tickets da sprint\`, mas a AIM dele ${a.fm.sprint ? `diz \`sprint: ${a.fm.sprint}\`` : 'não diz a sprint'}.`);
  }

  // A visão final de cada ticket concluído, dentro da sprint.
  const porFeature = new Map(); // id → [{ k, natureza, pfb, pfl }]
  for (const a of daSprint) {
    if (norm(a.fm.estado) !== 'concluido') {
      acusa(`a AIM do ticket \`${a.k}\` está em \`${a.fm.estado || '—'}\` — a sprint consolida a visão final dos tickets concluídos.`);
      continue;
    }
    const finais = alteracoesDe(a.ls);
    for (const f of finais) {
      if (!porFeature.has(f.id)) porFeature.set(f.id, []);
      porFeature.get(f.id).push({ ...f, k: a.k });
      const l = linhas.find((x) => x.id === f.id);
      if (!l) acusa(`\`${f.id}\` está na visão final da AIM de \`${a.k}\`, mas não em \`## Alterações na spec, por Feature Set\` da sprint.`);
      else if (!l.chaves.includes(a.k)) acusa(`\`${f.id}\`: a coluna Ticket da sprint não cita \`${a.k}\`, que alterou a feature.`);
    }
    for (const l of linhas.filter((x) => x.chaves.includes(a.k)))
      if (!finais.some((f) => f.id === l.id)) acusa(`\`${l.id}\` cita \`${a.k}\`, mas a visão final da AIM de \`${a.k}\` não tem a feature.`);
    for (const h of a.ls.filter((x) => /^###\s+(ALI|AIE):/i.test(x.trim()))) {
      const nome = h.trim().replace(/^###\s+(ALI|AIE):\s*/i, '').split(/\s+[—–]\s+/)[0].trim();
      if (nome && !EXEMPLO.test(nome) && !funcoes.some((f) => norm(f.nome) === norm(nome)))
        acusa(`a função de dados \`${nome}\` está na AIM de \`${a.k}\`, mas não em \`## Funções de dados alteradas\` da sprint.`);
    }
  }
  // Natureza e PF da linha da sprint × os das AIMs. Incluída por um ticket da sprint, a
  // feature entra nela como incluída, ainda que outro a tenha alterado depois. O PF só
  // se compara com ticket único: com dois, a sprint soma os PE de ambos uma vez só.
  for (const l of linhas) {
    const fs = (porFeature.get(l.id) || []).filter((f) => l.chaves.includes(f.k));
    if (!fs.length) continue;
    if (l.natureza && fs.every((f) => f.natureza)) {
      const espera = fs.some((f) => f.natureza === 'incluida') ? 'incluida' : 'alterada';
      const mostra = (v) => `\`${v === 'incluida' ? 'incluída' : v}\``;
      if (l.natureza !== espera)
        acusa(`\`${l.id}\`: natureza ${mostra(l.natureza)} na sprint, mas ${fs.map((f) => `${mostra(f.natureza)} na AIM de \`${f.k}\``).join(', ')}${fs.length > 1 ? ` — a sprint diz ${mostra(espera)}` : ''}.`);
    }
    const [f] = fs;
    if (fs.length === 1 && l.chaves.length === 1
      && ((f.pfb != null && l.pfb != null && f.pfb !== l.pfb) || (f.pfl != null && l.pfl != null && f.pfl !== l.pfl)))
      warns.push(`\`${l.id}\`: PFB/PFL ${fmt(l.pfb)}/${fmt(l.pfl)} na sprint e ${fmt(f.pfb)}/${fmt(f.pfl)} na AIM de \`${f.k}\` — as duas espelham o N3.`);
  }

  // O apurável é a soma das linhas: o Total, sempre; Transações e Funções de dados, quando
  // a tabela as traz — a do relatório anterior à AIM única, que o migra-aim preserva,
  // quebra as transações por origem ("Features alteradas…", "Features novas…").
  const ap = tabelasDe('Apurável da sprint')[0];
  if (!ap) {
    if (fechada) warns.push('sem `## Apurável da sprint` — a soma das transações e das funções de dados que a equipe de métricas audita.');
  } else if (ap.linhas.some((c) => EXEMPLO.test(c.join(' ')))) {
    acusa('`## Apurável da sprint` ainda com o exemplo do template (`[soma]`).');
  } else if (col(ap, /^pfb$/) < 0 || col(ap, /^pfl$/) < 0) {
    acusa('`## Apurável da sprint` sem as colunas PFB e PFL.');
  } else {
    const iB = col(ap, /^pfb$/);
    const iL = col(ap, /^pfl$/);
    const soma = (arr, campo) => arr.reduce((s, x) => s + (x[campo] || 0), 0);
    const confere = (nome, re, pfb, pfl, exigida) => {
      const c = ap.linhas.find((x) => re.test(norm(String(x[0] || '').replace(/\*/g, ''))));
      if (!c) { if (exigida) acusa(`\`## Apurável da sprint\` sem a linha ${nome}.`); return; }
      const [b, l] = [num(c[iB]), num(c[iL])];
      if (b == null || l == null) { acusa(`\`## Apurável da sprint\`, linha ${nome}: PFB/PFL sem número ("${c[iB] || ''}" / "${c[iL] || ''}").`); return; }
      if (Math.abs(b - pfb) > 0.005 || Math.abs(l - pfl) > 0.005)
        acusa(`\`## Apurável da sprint\`, linha ${nome}: ${fmt(b)} / ${fmt(l)}, mas a soma dá ${fmt(pfb)} / ${fmt(pfl)}.`);
    };
    const tr = [soma(linhas, 'pfb'), soma(linhas, 'pfl')];
    const fd = [soma(funcoes, 'pfb'), soma(funcoes, 'pfl')];
    confere('Transações', /^transac/, ...tr, false);
    confere('Funções de dados', /^funcoes de dados/, ...fd, false);
    confere('Total', /^total/, tr[0] + fd[0], tr[1] + fd[1], true);
    // O Estimado é a soma das estimativas dos tickets da sprint — os que a têm: ticket
    // aberto na entrega não foi estimado. Conferido só quando a tabela traz a linha.
    const ests = daSprint.map((a) => estimativaDe(a.ls)).filter(Boolean).flatMap((e) => e.funcoes.filter((f) => !f.exemplo));
    const es = [soma(ests, 'pfb'), soma(ests, 'pfl')];
    confere('Estimado', /^estimad/, ...es, false);
    confere('Diferença', /^diferenca/, tr[0] + fd[0] - es[0], tr[1] + fd[1] - es[1], false);
  }
  return daSprint.length;
}

/* =========================== AIM do ticket =========================== */
const ESTADOS = ['rascunho', 'em-analise', 'escopo-aprovado', 'em-execucao', 'concluido'];
const est = norm(fm.estado);
if (!fm.estado) errors.push('front-matter sem `estado:` (rascunho|em-análise|escopo-aprovado|em-execução|concluído).');
else if (!ESTADOS.includes(est)) errors.push(`\`estado: ${fm.estado}\` não é um estado válido da esteira da AIM.`);
const depoisDe = (e) => ESTADOS.indexOf(est) >= ESTADOS.indexOf(e);

if (!fm.ticket || EXEMPLO.test(fm.ticket)) errors.push('front-matter sem `ticket:` (a chave na ferramenta de origem).');
else {
  const doNome = basename(FILE, '.md').replace(/^AIM-/, '');
  if (!basename(FILE).startsWith('AIM-') || doNome.toLowerCase() !== fm.ticket.toLowerCase())
    errors.push(`o arquivo deve se chamar \`AIM-${fm.ticket}.md\` (a chave do \`ticket:\`), não \`${basename(FILE)}\`.`);
}
const naEntrega = norm(fm['aberta-na-entrega']) === 'true';

// `## Detalhe do item` é a descrição do ticket (decisão do PO, 2026-09-30); a AIM anterior a
// ela, com `## Descrição do ticket`, segue válida.
for (const s of ['Detalhe do item', 'Critérios de aceite', 'Features', 'Artefatos impactados',
  'Alterações na spec, por Feature Set', 'Reconciliação', 'Changelog']) {
  if (!temSecao(s) && !(s === 'Detalhe do item' && temSecao('Descrição do ticket'))) errors.push(`falta a seção \`## ${s}\`.`);
}

// Features: o elo recíproco da `## Origem` dos N3.
const features = tabelasDe('Features').flatMap((t) => t.linhas).filter((c) => ID_RE.test(c[0] || '') && !/SIGLA-SFS-NN/.test(c[0]));
if (depoisDe('em-analise') && temSecao('Features') && !features.length)
  errors.push('`## Features` sem feature — de `em-análise` em diante, a AIM diz quais N3 realizam o ticket.');

/* ---------------------- changeset ---------------------- */
const TIPOS = new Set(['N3', 'QA', 'DATA-MODEL', 'FIELD-DICT', 'RULES-DICT', 'MESSAGE-DICT', 'ERROR-DICT',
  'NFR', 'PATTERNS', 'API-PATTERNS', 'MÉTRICA', 'METRICA', 'PROTÓTIPO', 'PROTOTIPO', 'REPOSITÓRIO', 'REPOSITORIO']);
const tabCs = tabelasDe('Artefatos impactados')[0] || { cab: [], linhas: [] };
const iSit = tabCs.cab.indexOf('situacao'); // posterior à AIM única: -1 na tabela sem a coluna
const rows = tabCs.linhas.map((c) => ({
  artefato: (c[0] || '').replace(/`/g, ''), tipo: (c[1] || '').toUpperCase(), operacao: norm(c[2]),
  secao: c[3] || '', natureza: norm(c[4]), oque: c[5] || '', prov: c[6] || '', bruta: c.join(' | '),
  situacao: iSit >= 0 ? norm(c[iSit]).replace(/[`*]/g, '') : null,
}));
const ehCaminho = (a) => (/^(modules|global|qa|prototypes|analise-impacto)\//.test(a) || /\.md$/.test(a))
  && !/[()<>[\]]| de /.test(a); // ignora "qa/ de X", "prototypes/ (tela…)"
if (depoisDe('em-analise') && temSecao('Artefatos impactados')) {
  if (!rows.length) errors.push('a seção `## Artefatos impactados` não tem tabela de linhas.');
  if (rows.length && !(tabCs.cab.includes('artefato') && tabCs.cab.includes('tipo') && tabCs.cab.includes('natureza')))
    errors.push('cabeçalho da tabela de artefatos deve ter ao menos: Artefato, Tipo, Natureza.');
  const exemplos = rows.filter((r) => /<(?:dom|fs|slug)>|\[[^\]]*\]/.test(r.bruta));
  for (const r of exemplos) errors.push(`linha de exemplo do template no changeset: \`${r.artefato}\` — troque pelo artefato real ou apague.`);
  for (const r of rows) {
    if (r.tipo && !TIPOS.has(r.tipo)) warns.push(`Tipo desconhecido "${r.tipo}" (${r.artefato}).`);
    if (ehCaminho(r.artefato)) {
      const exists = existsSync(join(ROOT, r.artefato));
      if (r.operacao === 'alterar' && !exists) errors.push(`\`${r.artefato}\` marcado \`alterar\` mas não existe — é \`criar\`?`);
      // Até o aval, `criar` sobre arquivo existente é suspeito — a linha devia ser `alterar`?
      // Da execução em diante, a passada criou o arquivo: em `em-execução` e `concluído` ele
      // existe por construção, e o aviso seria ruído em toda AIM que criou algo.
      if (r.operacao === 'criar' && exists && !depoisDe('em-execucao')) warns.push(`\`${r.artefato}\` marcado \`criar\` mas já existe — é \`alterar\`?`);
    }
  }
  const has = (pred) => rows.some(pred);
  const isFunc = (n) => n.startsWith('funcional');
  const isNF = (n) => n.includes('nao-funcional') || n.startsWith('nao');
  const cobertura = (msg) => (naEntrega ? warns : errors).push(msg + (naEntrega ? ' (AIM aberta na entrega: aviso)' : ''));
  if (!has((r) => r.tipo === 'N3')) errors.push('C1: nenhuma linha `N3` — todo ticket ancora em ao menos uma feature.');
  if (has((r) => isFunc(r.natureza)) && !has((r) => r.tipo === 'QA'))
    cobertura('C2: há mudança `funcional` sem linha `QA` — mudança funcional deve ser testada (gate CP3).');
  if (has((r) => isNF(r.natureza))) {
    if (!has((r) => r.tipo === 'NFR')) cobertura('C3: há mudança `não-funcional` sem linha `NFR`.');
    if (!has((r) => r.tipo === 'QA')) cobertura('C3: há mudança `não-funcional` sem linha `QA` (teste não-funcional que a verifique).');
  }
}

/* --------------------- portões por estado --------------------- */
if (depoisDe('escopo-aprovado') && !fm['avalizado-por'])
  errors.push(`estado \`${fm.estado}\` exige front-matter \`avalizado-por\` (o aval do PO no escopo).`);
if (est === 'concluido') {
  if (!fm.sprint) errors.push('estado `concluído` exige `sprint:` — a sprint em que o ticket foi entregue.');
  const final = tabelasDe('Alterações na spec, por Feature Set').flatMap((t) => t.linhas)
    .filter((c) => ID_RE.test(c[0] || '') && !EXEMPLO.test(c.join(' ')));
  if (!final.length)
    errors.push('estado `concluído` exige a visão final em `## Alterações na spec, por Feature Set` — o que foi alterado, uma linha por feature, sem o exemplo do template.');
  // A instrução do template vem em citação (`> Preenchida no fechamento…`) e pode ficar;
  // o que conta é o conteúdo FORA dela (e fora de comentário).
  if (!conteudoForaDaCitacao('Reconciliação').length)
    errors.push('estado `concluído` exige `## Reconciliação` preenchida (declarado × tocado) — escreva o resultado fora da citação de instrução.');
}

/* --------------------- contagem estimada --------------------- */
const estimativa = estimativaDe(lines);
const funcoesEst = estimativa ? estimativa.funcoes.filter((f) => !f.exemplo) : [];
if (!naEntrega && depoisDe('em-analise') && !funcoesEst.length) {
  const msg = 'E1: sem `## Contagem estimada` — de `em-análise` em diante a AIM traz o tamanho estimado do ticket, uma linha por função (EE 4 · CE 4 · SE 5 · ALI 7 · AIE 5).';
  if (est === 'concluido') warns.push(`${msg} (AIM fechada sem estimativa: não há diferença a mostrar)`);
  else errors.push(msg);
}
if (estimativa) {
  const metade = { incluida: 1, alterada: 0.5 };
  if (depoisDe('em-analise')) {
    for (const f of estimativa.funcoes.filter((x) => x.exemplo))
      errors.push(`E1: linha de exemplo do template na \`## Contagem estimada\`: \`${f.nome}\` — troque pela função real ou apague.`);
    if (estimativa.total && estimativa.total.exemplo) errors.push('E2: a linha Total da `## Contagem estimada` ainda traz o exemplo do template (`[soma]`).');
  }
  for (const f of funcoesEst) {
    const peso = PESO_ESTIMADO[f.tipo];
    if (!peso) { errors.push(`E2: \`${f.nome}\`: Tipo "${f.tipo || '—'}" — a contagem estimada conta EE, SE, CE, ALI ou AIE.`); continue; }
    if (!(f.natureza in metade)) { errors.push(`E2: \`${f.nome}\`: Natureza "${f.natureza || '—'}" — é \`incluída\` ou \`alterada\` (é ela que decide o PFL).`); continue; }
    if (!igual(f.pfb, peso)) errors.push(`E2: \`${f.nome}\` (${f.tipo}): PFB ${fmt(f.pfb)}, mas o peso estimado de ${f.tipo} é ${peso}.`);
    if (!igual(f.pfl, peso * metade[f.natureza]))
      errors.push(`E2: \`${f.nome}\` (${f.tipo}, ${f.natureza === 'incluida' ? 'incluída' : 'alterada'}): PFL ${fmt(f.pfl)}, mas é ${fmt(peso * metade[f.natureza])}.`);
  }
  const somaEst = { pfb: funcoesEst.reduce((s, f) => s + (f.pfb || 0), 0), pfl: funcoesEst.reduce((s, f) => s + (f.pfl || 0), 0) };
  if (funcoesEst.length) {
    const tot = estimativa.total;
    if (!tot) errors.push('E2: a `## Contagem estimada` não tem a linha **Total**.');
    else if (!tot.exemplo && (!igual(tot.pfb, somaEst.pfb) || !igual(tot.pfl, somaEst.pfl)))
      errors.push(`E2: Total da \`## Contagem estimada\`: ${fmt(tot.pfb)} / ${fmt(tot.pfl)}, mas a soma dá ${fmt(somaEst.pfb)} / ${fmt(somaEst.pfl)}.`);
    const q = estimativa.quadro;
    if (q && q.estimada && !q.estimada.exemplo && (!igual(q.estimada.pfb, somaEst.pfb) || !igual(q.estimada.pfl, somaEst.pfl)))
      errors.push(`E3: \`### Estimada × detalhada\`, linha Estimada: ${fmt(q.estimada.pfb)} / ${fmt(q.estimada.pfl)}, mas a estimativa soma ${fmt(somaEst.pfb)} / ${fmt(somaEst.pfl)}.`);
    const det = q && q.detalhada;
    if (det && det.pfb != null && det.pfl != null) {
      const dif = q.diferenca;
      if (!dif || !igual(dif.pfb, det.pfb - somaEst.pfb) || !igual(dif.pfl, det.pfl - somaEst.pfl))
        errors.push(`E3: \`### Estimada × detalhada\`, linha Diferença: ${dif ? `${fmt(dif.pfb)} / ${fmt(dif.pfl)}` : 'ausente'}, mas Detalhada − Estimada dá ${fmt(det.pfb - somaEst.pfb)} / ${fmt(det.pfl - somaEst.pfl)}.`);
    }
  }
}

/* ----------------------- AIM defasada ------------------------ */
// A AIM é um documento vivo: muda a cada artefato que muda por causa do ticket. Daqui
// para baixo, o que ficou para trás — aviso com o ticket em execução, erro no fechamento.
const chave = String(fm.ticket || '').trim();
const citaOTicket = (txt) => !!chave && new RegExp(`(?<![\\w-])${chave.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(?![\\w-])`, 'i').test(txt);
const le = (rel) => { try { const f = join(ROOT, rel); return statSync(f).isFile() ? readFileSync(f, 'utf8') : null; } catch { return null; } };
// O N3 de cada feature, pelo link da `## Features` — a AIM já diz onde ele mora.
const n3De = new Map();
for (const c of features) {
  const id = (c[0].match(ID_RE) || [])[0];
  const alvo = (c[0].match(/\]\(\s*<?([^)>\s]+)>?\s*\)/) || [])[1];
  if (id && alvo) n3De.set(id, relative(ROOT, join(dirname(FILE), alvo)));
}
// A tabela do delta é a que traz Feature, Natureza, PFB e PFL — a seção costuma ter
// outras (os PE por trás do PFB, um resumo por tipo), que citam a feature e não são ela.
const alteracoes = tabelasDe('Alterações na spec, por Feature Set').flatMap((t) => {
  const iF = t.cab.indexOf('feature');
  const iN = t.cab.indexOf('natureza');
  const iB = t.cab.findIndex((h) => /^pfb\b/.test(h));
  const iL = t.cab.findIndex((h) => /^pfl\b/.test(h));
  if ([iF, iN, iB, iL].some((i) => i < 0)) return [];
  return t.linhas.filter((c) => ID_RE.test(c[iF] || '') && !EXEMPLO.test(c.join(' '))).map((c) => ({
    id: c[iF].match(ID_RE)[0], natureza: natureza(c[iN]), pfb: num(c[iB]), pfl: num(c[iL]),
    estimada: [iB, iL].some((i) => ESTIMADO.test(c[i] || '') || /\(e\)/.test(t.cab[i])),
  }));
});
// P1 — o critério do processo elementar é um dos critérios do card.
const CRITERIO_RE = /CA-\d+|CRIT\.\d+\.\d+/g;
const doCard = new Set(corpoDe('Critérios de aceite').join('\n').match(CRITERIO_RE) || []);
for (const t of tabelasDe('Alterações na spec, por Feature Set')) {
  const [iP, iD, iK] = ['processo elementar', 'da feature', 'criterios'].map((h) => t.cab.indexOf(h));
  if (Math.min(iP, iD, iK) < 0) continue;
  for (const c of t.linhas.filter((x) => !EXEMPLO.test(x.join(' ')))) {
    const fora = [...new Set((c[iK] || '').match(CRITERIO_RE) || [])].filter((k) => !doCard.has(k));
    if (fora.length) warns.push(`P1: \`${((c[iD] || '').match(ID_RE) || ['—'])[0]}\` · ${(c[iP] || '').replace(/[\`*]/g, '').trim()}: ${fora.join(', ')} não está na \`## Critérios de aceite\` — o critério do processo elementar é um dos critérios do card.`);
  }
}
const dados = corpoDe('Funções de dados alteradas').map((l) => l.trim().match(/^###\s+(?:ALI|AIE):\s*(.+)$/i)).filter(Boolean)
  .map((m) => m[1]).filter((tit) => !EXEMPLO.test(tit)).map((tit) => {
    const pf = tit.match(/(\d+(?:[.,]\d+)?)\s*PF\b/i);
    return { nome: tit.split(/\s+[—–]\s+/)[0].trim(), pf: pf ? Number(pf[1].replace(',', '.')) : null,
      natureza: (norm(tit).match(/\b(incluida|alterada)\b/) || [])[1] || '', estimada: ESTIMADO.test(tit) };
  });

const defasagens = [];
const emExecucao = depoisDe('em-execucao');
if (emExecucao) {
  // D1 — a feature segue estimada, e o N3 já tem a contagem revista para este ticket.
  for (const a of alteracoes.filter((x) => x.estimada)) {
    const raw = n3De.has(a.id) ? le(n3De.get(a.id)) : null;
    if (!raw || !citaOTicket(raw)) continue;
    const pes = pesDoN3(raw).filter(contado);
    const bloco = frontMatterBloco(raw.split(/\r?\n/), 'contagem');
    if (pes.length && !(bloco && norm(bloco.pendente) === 'true')) {
      a.defasada = true;
      defasagens.push(`D1: \`${a.id}\` segue estimada \`(E)\`, mas o N3 (\`${n3De.get(a.id)}\`) cita \`${chave}\` e já tem a contagem revista (${pes.reduce((s, x) => s + x.pf, 0)} PF contados) — troque o PFB/PFL pelo da \`## Métricas de tamanho\`.`);
    }
  }
  // D2 — a linha segue `previsto`, e o artefato já mudou por causa do ticket.
  for (const r of rows.filter((x) => x.situacao === 'previsto' && ehCaminho(x.artefato))) {
    const raw = le(r.artefato);
    if (raw == null) continue;
    if (r.operacao === 'criar' || citaOTicket(raw)) {
      r.defasada = true;
      defasagens.push(`D2: \`${r.artefato}\` segue \`previsto\`, mas ${r.operacao === 'criar' ? 'o arquivo já existe' : `já cita \`${chave}\``} — marque \`feito em AAAA-MM-DD\` e registre a versão no Changelog.`);
    }
  }
}
if (args.includes('--defasagem')) {
  for (const d of defasagens) console.log(`${basename(FILE)} — ${d}`);
  process.exit(defasagens.length ? 1 : 0);
}
for (const d of defasagens) (est === 'concluido' ? errors : warns).push(`AIM defasada — ${d}`);

if (depoisDe('em-analise') && rows.length) {
  if (iSit < 0) {
    if (emExecucao) warns.push('`## Artefatos impactados` sem a coluna Situação (`previsto` · `feito em AAAA-MM-DD` · `não feito`) — sem ela, a AIM não diz o que já mudou.');
  } else {
    for (const r of rows) {
      if (!/^(previsto$|feito\b|nao feito\b)/.test(r.situacao))
        errors.push(`\`${r.artefato}\`: Situação "${r.situacao || '—'}" — é \`previsto\`, \`feito em AAAA-MM-DD\` ou \`não feito\`.`);
      else if (/^feito\b/.test(r.situacao) && r.operacao !== 'deprecar' && ehCaminho(r.artefato) && !existsSync(join(ROOT, r.artefato)))
        errors.push(`\`${r.artefato}\` marcado \`feito\`, mas o arquivo não existe.`);
    }
  }
}
if (emExecucao) {
  // D3 — o PFB detalhado que o N3 não sustenta. Aviso: o ticket pode ter alterado só
  // parte dos PE da feature, e aí a AIM traz menos que o N3 — o que não pode é trazer mais.
  for (const a of alteracoes.filter((x) => !x.estimada && x.pfb != null && n3De.has(x.id))) {
    const raw = le(n3De.get(a.id));
    const pes = raw ? pesDoN3(raw).filter(contado) : [];
    if (!pes.length) continue;
    const total = pes.reduce((s, x) => s + x.pf, 0);
    const principal = pes.filter((x) => /principal/i.test(x.papel || '')).reduce((s, x) => s + x.pf, 0);
    if (a.natureza === 'incluida' ? ![total, principal].some((v) => igual(a.pfb, v)) : a.pfb > total + 0.005)
      warns.push(`D3: \`${a.id}\`: PFB ${fmt(a.pfb)} na AIM, e o N3 conta ${fmt(total)} PF (${fmt(principal)} nos PE \`principal\`) — a tabela espelha o N3.`);
  }
}
if (est === 'concluido') {
  // Sem a tabela do delta não há como dizer se alguma feature fecha estimada — e calar
  // aqui daria ao "nada a apontar" a mesma cara de "não conferi".
  if (!alteracoes.length && tabelasDe('Alterações na spec, por Feature Set').some((t) => t.linhas.some((c) => ID_RE.test(c[0] || ''))))
    warns.push('a `## Alterações na spec, por Feature Set` não tem a tabela do delta com as colunas Feature, Natureza, PFB e PFL — não foi possível conferir se alguma feature fecha estimada.');
  for (const r of rows.filter((x) => x.situacao === 'previsto' && !x.defasada))
    errors.push(`\`${r.artefato}\` fecha \`previsto\` — no fechamento a linha é \`feito em AAAA-MM-DD\` ou \`não feito\` (justificado na \`## Reconciliação\`).`);
  for (const a of alteracoes) {
    if (a.estimada && !a.defasada)
      errors.push(`\`${a.id}\` fecha com PFB/PFL estimado \`(E)\` — a AIM só conclui com a contagem detalhada: conte no N3 (PROMPT_CONTAGEM) e espelhe aqui, ou mantenha a AIM \`em-execução\`.`);
    else if (!a.estimada && (a.pfb == null || a.pfl == null))
      errors.push(`\`${a.id}\` fecha sem PFB/PFL em número — a contagem detalhada vem da \`## Métricas de tamanho\` do N3 (0 quando a feature não conta, com o motivo).`);
  }
  for (const d of dados.filter((x) => x.estimada))
    errors.push(`a função de dados \`${d.nome}\` fecha com PF estimado \`(E)\` — traga RLR, DER e PF do DATA-MODEL.`);
  if (!alteracoes.some((a) => a.estimada) && !dados.some((d) => d.estimada)
    && ['Alterações na spec, por Feature Set', 'Funções de dados alteradas'].some((s) => ESTIMADO.test(semComentario(s))))
    errors.push('ainda há `(E)` nas seções de impacto (subtotal, nota ou cabeçalho) — no fechamento nenhum número é estimado.');
  // E3 no fechamento: o quadro com as três linhas, e a Detalhada conferida com as seções.
  if (funcoesEst.length) {
    const det = estimativa.quadro && estimativa.quadro.detalhada;
    if (!det || det.pfb == null || det.pfl == null)
      errors.push('E3: estado `concluído` exige o quadro `### Estimada × detalhada` com a linha Detalhada em número — é onde a diferença para a estimativa fica à vista.');
    else if (alteracoes.every((a) => !a.estimada && a.pfb != null && a.pfl != null)) {
      const semPf = dados.filter((d) => d.pf == null || !d.natureza || d.estimada);
      if (semPf.length) warns.push(`E3: a linha Detalhada não foi conferida — função de dados sem \`n PF · incluída|alterada\` no título: ${semPf.map((d) => `\`${d.nome}\``).join(', ')}.`);
      else {
        const b = alteracoes.reduce((s, a) => s + a.pfb, 0) + dados.reduce((s, d) => s + d.pf, 0);
        const l = alteracoes.reduce((s, a) => s + a.pfl, 0) + dados.reduce((s, d) => s + d.pf * (d.natureza === 'incluida' ? 1 : 0.5), 0);
        if (!igual(det.pfb, b) || !igual(det.pfl, l))
          errors.push(`E3: \`### Estimada × detalhada\`, linha Detalhada: ${fmt(det.pfb)} / ${fmt(det.pfl)}, mas as seções de impacto somam ${fmt(b)} / ${fmt(l)} (features + funções de dados).`);
      }
    }
  }
}

/* ----------------------- reconciliação ------------------------ */
const touchedOpt = opt('--touched');
const gitBase = opt('--git-base');
let touched = null;
if (touchedOpt) touched = touchedOpt.split(',').map((s) => s.trim()).filter(Boolean);
else if (gitBase) {
  try {
    touched = execFileSync('git', ['-C', ROOT, 'diff', '--name-only', `${gitBase}...HEAD`], { encoding: 'utf8' })
      .split(/\r?\n/).map((s) => s.trim()).filter(Boolean);
  } catch (e) { warns.push(`reconciliação: git diff falhou (${String(e.message).split('\n')[0]}).`); }
}
if (touched) {
  const declared = rows.filter((r) => /^(modules|global|qa|prototypes)\//.test(r.artefato) && !/[()]| de /.test(r.artefato))
    .map((r) => r.artefato);
  const inSpec = (p) => /^(modules|global|qa|prototypes)\//.test(p);
  const notTouched = declared.filter((d) => !touched.includes(d));
  const notDeclared = touched.filter((t) => inSpec(t) && !declared.includes(t));
  for (const d of notTouched) errors.push(`reconciliação: \`${d}\` foi declarado mas NÃO tocado (escopo não cumprido).`);
  for (const t of notDeclared) errors.push(`reconciliação: \`${t}\` foi tocado mas NÃO declarado (desvio de escopo).`);
}

/* ------------------------------ saída ------------------------------ */
sai();
console.log(`  ✓ AIM bem-formada — ${fm.estado}, ${features.length} feature(s), ${rows.length} linha(s) no changeset${warns.length ? `, ${warns.length} aviso(s)` : ''}.`);
