#!/usr/bin/env node
// Gera assets/mapa-data.js — dados da tela "Mapa de features" do visualizador
// (Produto → N1 domínios → N2 feature sets → N3 features). Data-driven: varre
// modules/ e embute a árvore real. Regerar após criar/alterar N1/N2/N3.
//
// Cada feature (N3) também abre a CAMADA DE CÓDIGO — os arquivos reais do back-end e
// do front-end que a implementam, ligados por scripts/lib/mapa-codigo.mjs (varre os
// repos irmãos siesa-backend/siesa-frontend; sem eles, a camada fica vazia e o mapa
// gera igual). É a rastreabilidade spec → código dentro do próprio mapa.
// Uso: node scripts/gera-mapa-features.mjs
import { readFileSync, writeFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { ligarCodigo } from './lib/mapa-codigo.mjs';

const ROOT = new URL('..', import.meta.url).pathname;
const MODULES = join(ROOT, 'modules');

const ORDEM_DOMINIOS = ['demandas', 'esteira', 'agentes', 'sistemas', 'administracao', 'operacao'];

function isDir(p) { try { return statSync(p).isDirectory(); } catch { return false; } }
function read(p) { try { return readFileSync(p, 'utf8'); } catch { return ''; } }

// primeiro parágrafo após um "## Cabeçalho"
function paraApos(texto, cabecalho) {
  const re = new RegExp('##\\s+' + cabecalho + '\\s*\\n+([\\s\\S]*?)(?:\\n\\s*\\n|\\n#|$)');
  const m = texto.match(re);
  return m ? m[1].replace(/\s+/g, ' ').trim() : '';
}
function m1(texto, re) { const m = texto.match(re); return m ? m[1].trim() : ''; }

// A `## Descrição` do N3 tem duas camadas em parágrafos consecutivos: o 1º é o
// contrato de entrega, o 2º diz COMO SE USA. Antes o uso era uma seção própria
// (`## Como se usa`), mas ela caía longe da entrega no documento — o texto virou o
// segundo parágrafo da mesma seção, e é daqui que o card do mapa o lê.
function paragrafoApos(texto, cabecalho, n) {
  const re = new RegExp('##\\s+' + cabecalho + '\\s*\\n+([\\s\\S]*?)(?=\\n\\s*\\n\\s*(?:---|#)|$)');
  const m = texto.match(re);
  if (!m) return '';
  // Só prosa conta como camada: blockquote (ressalvas ⚠️/❓), tabela, lista e
  // cabeçalho podem aparecer na Descrição e não são o texto do uso.
  const ehProsa = (s) => s && !/^[>|#]/.test(s) && !/^([-*+]\s|\d+[.)]\s)/.test(s);
  const paras = m[1].split(/\n\s*\n/)
    .map((s) => s.replace(/\s+/g, ' ').trim())
    .filter(ehProsa);
  return paras[n - 1] || '';
}

// ---- camada 2 da descrição: a definição do OBJETO de negócio -----------------
// O N3 não duplica a definição da entidade — ela vive só no fragmento de
// data-model, no blockquote sob "## <Entidade>", e o N3 aponta para lá pelo
// `data_model_ref` do frontmatter. O mapa BUSCA essa definição na hora de gerar,
// de modo que corrigir o data-model corrige todos os cards que usam a entidade.
const slug = (s) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]/g, '');
const dmCache = new Map();
function definicaoObjeto(ref, entidade) {
  if (!ref) return '';
  const [arq, ancora] = ref.split('#');
  const alvo = slug(ancora || entidade || '');
  if (!arq || !alvo) return '';
  const caminho = join(ROOT, 'global', arq.trim());
  if (!dmCache.has(caminho)) dmCache.set(caminho, read(caminho));
  const linhas = dmCache.get(caminho).split(/\r?\n/);
  for (let i = 0; i < linhas.length; i++) {
    const h = linhas[i].match(/^##\s+(.+?)\s*$/);
    if (!h || slug(h[1]) !== alvo) continue;
    const buf = [];
    for (let j = i + 1; j < linhas.length; j++) {
      const l = linhas[j].trim();
      if (!l) { if (buf.length) break; continue; }
      if (!l.startsWith('>')) break;
      buf.push(l.replace(/^>\s?/, ''));
    }
    return buf.join(' ').replace(/\s+/g, ' ').trim();
  }
  return '';
}

// ---- varredura ----
const dominios = [];
for (const domNome of readdirSync(MODULES)) {
  if (domNome.startsWith('_') || domNome.startsWith('.')) continue;
  const domDir = join(MODULES, domNome);
  if (!isDir(domDir)) continue;
  const domReadme = read(join(domDir, 'README.md'));
  // O N1 se chama Major Feature Set desde a 3.0.0; o título legado `# Domínio:` segue valendo.
  if (!/^# (?:Major Feature Set|Domínio):/m.test(domReadme)) continue;

  const dom = {
    folder: domNome,
    nome: m1(domReadme, /^# (?:Major Feature Set|Domínio):\s*(.+)$/m),
    sigla: m1(domReadme, /Nível 1[^\n]*?`([A-Z]+)`/),
    desc: paraApos(domReadme, 'Descrição'),
    path: `modules/${domNome}/README.md`,
    fss: [],
  };

  for (const fsNome of readdirSync(domDir)) {
    if (fsNome.startsWith('_') || fsNome.startsWith('.')) continue;
    const fsDir = join(domDir, fsNome);
    if (!isDir(fsDir)) continue;
    const fsReadme = read(join(fsDir, 'README.md'));
    if (!/^# Feature Set:/m.test(fsReadme)) continue;

    const fs = {
      nome: m1(fsReadme, /^# Feature Set:\s*(.+)$/m),
      sigla: m1(fsReadme, /Nível 2[^\n]*?`([A-Z-]+)`/),
      desc: paraApos(fsReadme, 'Descrição'),
      path: `modules/${domNome}/${fsNome}/README.md`,
      feats: [],
    };

    for (const arq of readdirSync(fsDir)) {
      if (!arq.startsWith('f-') || !arq.endsWith('.md')) continue;
      const t = read(join(fsDir, arq));
      const id = m1(t, /^id:\s*(.+)$/m);
      if (!id) continue;
      fs.feats.push({
        id,
        nome: m1(t, /^#\s+(.+)$/m),
        // As três camadas da descrição (ver CLAUDE.md): o que ENTREGA (Descrição
        // do N3), o que É o objeto entregue (buscado no data-model) e COMO SE USA
        // a funcionalidade — para o mapa se explicar sem abrir o documento.
        desc: paragrafoApos(t, 'Descrição', 1),
        objeto: definicaoObjeto(m1(t, /^data_model_ref:\s*(.+)$/m), m1(t, /^entidade:\s*(.+)$/m)),
        uso: paragrafoApos(t, 'Descrição', 2),
        estado: m1(t, /^estado:\s*(.+)$/m) || 'rascunho',
        mvp: /^mvp:\s*true/m.test(t),
        path: `modules/${domNome}/${fsNome}/${arq}`,
      });
    }
    fs.feats.sort((a, b) => a.id.localeCompare(b.id));
    dom.fss.push(fs); // mantém também os N2 vazios (lacunas) — visualização de cobertura
  }
  dom.fss.sort((a, b) => a.sigla.localeCompare(b.sigla));
  dominios.push(dom); // mantém também os N1 sem N2 (lacunas)
}
dominios.sort((a, b) => {
  const ia = ORDEM_DOMINIOS.indexOf(a.folder), ib = ORDEM_DOMINIOS.indexOf(b.folder);
  return (ia < 0 ? 99 : ia) - (ib < 0 ? 99 : ib);
});

const totFs = dominios.reduce((s, d) => s + d.fss.length, 0);
const totFeat = dominios.reduce((s, d) => s + d.fss.reduce((n, f) => n + f.feats.length, 0), 0);
const fssVazios = dominios.reduce((s, d) => s + d.fss.filter((f) => f.feats.length === 0).length, 0);
const domsVazios = dominios.filter((d) => d.fss.length === 0).length;

// Cobertura das camadas 2 e 3 — quanto do mapa já se explica sozinho.
const todasFeats = dominios.flatMap((d) => d.fss.flatMap((f) => f.feats));
const featComObjeto = todasFeats.filter((f) => f.objeto).length;
const featComUso = todasFeats.filter((f) => f.uso).length;

// ---- Camada de código: liga cada feature aos ARQUIVOS reais do back/front ------
// (scripts/lib/mapa-codigo.mjs — varre os repos irmãos; sem eles, `codigo` fica
// vazio e o mapa gera igual). É o "expandir com o código" da rastreabilidade:
// o nó da feature ganha os controllers/serviços/entidades/migrações (back) e
// componentes/telas/serviços/specs (front) que a materializam.
const featIds = [];
for (const d of dominios) for (const fs of d.fss) for (const f of fs.feats) featIds.push(f.id);
const codigo = ligarCodigo({ docRoot: ROOT, featIds });
let featComBack = 0, featComFront = 0, arqBack = 0, arqFront = 0;
for (const d of dominios) for (const fs of d.fss) for (const f of fs.feats) {
  const c = codigo.byFeat[f.id] || { back: [], front: [] };
  f.codigo = { back: c.back, front: c.front };
  if (c.back.length) featComBack++;
  if (c.front.length) featComFront++;
  arqBack += c.back.length;
  arqFront += c.front.length;
}

// Nome do produto (nó-raiz do mapa): lido do visualizador (assets/js/config.js →
// DOCS_CONFIG.name); fallback ao "Nome" do global/MASTER.md; senão rótulo genérico.
const nomeMaster = m1(read(join(ROOT, 'global', 'MASTER.md')), /^-\s*\*\*Nome\*\*\s*:\s*(.+)$/m);
const nomeProduto =
  m1(read(join(ROOT, 'assets', 'js', 'config.js')), /name:\s*"([^"]+)"/)
  || (nomeMaster && !nomeMaster.startsWith('[') ? nomeMaster : '')
  || 'Documentação';

const MAPA = {
  produto: { nome: nomeProduto, desc: '', path: 'global/MASTER.md' },
  dominios,
  kpi: {
    dominios: dominios.length, fss: totFs, feats: totFeat, fssVazios, domsVazios,
    codBackend: codigo.backend, codFrontend: codigo.frontend,
    featComBack, featComFront, arqBack, arqFront,
    featComObjeto, featComUso,
  },
  registros: codigo.registros,
};
const json = JSON.stringify(MAPA).replace(/</g, '\\u003c');

console.log('mapa de features: ' + dominios.length + ' domínios · ' + totFs + ' feature sets · ' + totFeat + ' features.');
console.log('  camadas da descrição: ' + totFeat + '/' + totFeat + ' com entrega · '
  + featComObjeto + '/' + totFeat + ' com definição do objeto (data-model) · '
  + featComUso + '/' + totFeat + ' com o parágrafo de uso na Descrição.');
console.log('  camada de código: back=' + (codigo.backend || '—') + ' front=' + (codigo.frontend || '—')
  + ' · ' + featComBack + '/' + totFeat + ' features com back (' + arqBack + ' arq.) · '
  + featComFront + '/' + totFeat + ' com front (' + arqFront + ' arq.)');

// ---- Dados para a tela "Mapa de features" do visualizador (GitHub Pages) ----
// Mesma árvore, agora com o caminho do artefato em cada nó (o visualizador liga
// cada nó ao respectivo .md). Consumido por assets/js/app.js (renderMapa).
const dataJs = '// GERADO por scripts/gera-mapa-features.mjs — não editar à mão.\n'
  + 'window.AVAL_MAPA = ' + json + ';\n';
writeFileSync(join(ROOT, 'assets', 'mapa-data.js'), dataJs);
console.log('assets/mapa-data.js gerado (dados da tela Mapa de features do visualizador).');
