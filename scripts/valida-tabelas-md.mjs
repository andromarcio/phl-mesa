#!/usr/bin/env node
// valida-tabelas-md.mjs — acusa tabela markdown que o visualizador renderiza errado
// mesmo com o `.md` aparentemente bem-formado.
//
// Uso:  node scripts/valida-tabelas-md.mjs [arquivo.md | pasta] ...
//       (sem argumentos: varre global/, modules/, analise-impacto/, contagem/ e os .md da raiz)
//
// Dois achados, os dois invisíveis na leitura do markdown:
//
//   T1 — TABELA COLADA AO PARÁGRAFO SEGUINTE. Sem linha em branco entre a última linha
//        da tabela e o texto que vem depois, o parser absorve esse texto como MAIS UMA
//        LINHA da tabela, inteiro numa única célula da primeira coluna. Como a primeira
//        coluna do visualizador é `white-space: nowrap` (para o ID não quebrar), a célula
//        não quebra: a coluna estica e empurra as demais para fora da tela. Foi o que
//        aconteceu com o Subtotal do `global/CONTAGEM-PF.md` do portal-compras em
//        2026-09-08 — a coluna `#` foi a 4828px e a tabela a 5816px num contêiner de
//        1143px, deixando visíveis só os números das linhas. Nenhum outro validador pega:
//        o markdown estava correto, com 11 colunas em todas as 235 linhas.
//
//   T2 — LINHA COM NÚMERO DE COLUNAS DIFERENTE DO CABEÇALHO. Quase sempre é um `|`
//        literal dentro de uma célula, sem escape (`\|`). A linha sai deslocada, e o
//        valor que você lê numa coluna é o de outra.
//
// Sai 1 havendo achado, 0 limpo. Ver CLAUDE.md → "Verificar de verdade": esta checagem
// foi provada por injeção antes de entrar (removida a linha em branco numa cópia, ela
// acusa; no estado íntegro, zero) — e o eval 41 repete a prova.

import fs from 'node:fs';
import path from 'node:path';

const PADROES = ['global', 'modules', 'analise-impacto', 'contagem', 'repos', 'qa'];
const alvos = process.argv.slice(2).length ? process.argv.slice(2) : PADROES;

const arquivos = [];
for (const alvo of alvos) {
  if (!fs.existsSync(alvo)) continue;
  const st = fs.statSync(alvo);
  if (st.isFile()) { arquivos.push(alvo); continue; }
  (function walk(dir) {
    for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
      if (e.name.startsWith('.') || e.name === 'node_modules') continue;
      const p = path.join(dir, e.name);
      if (e.isDirectory()) { if (e.name !== 'engine') walk(p); }
      else if (e.name.endsWith('.md') && !p.includes('_template')) arquivos.push(p);
    }
  })(alvo);
}
// sem argumento, inclui também os .md da raiz (CLAUDE.md, README.md…)
if (!process.argv.slice(2).length) {
  for (const e of fs.readdirSync('.', { withFileTypes: true })) {
    if (e.isFile() && e.name.endsWith('.md')) arquivos.push(e.name);
  }
}

// conta as células de uma linha de tabela, ignorando o `|` escapado dentro de célula
const nCelulas = (l) => l.trim().replace(/\\\|/g, ' ').replace(/^\||\|$/g, '').split('|').length;

let t1 = 0, t2 = 0;
for (const arq of [...new Set(arquivos)].sort()) {
  const linhas = fs.readFileSync(arq, 'utf-8').split('\n');
  let fence = null, coment = false, emTabela = false, colunas = 0, linhaCab = 0;
  for (let i = 0; i < linhas.length; i++) {
    const l = linhas[i];
    // A cerca só fecha com o mesmo caractere, em número igual ou maior e sem texto depois
    // (CommonMark): a ```json dentro de um exemplo ````markdown é conteúdo do exemplo.
    const cerca = l.match(/^\s*(`{3,}|~{3,})(.*)$/);
    if (cerca && !fence) { fence = cerca[1]; emTabela = false; continue; }
    if (cerca && cerca[1][0] === fence[0] && cerca[1].length >= fence.length && !cerca[2].trim()) { fence = null; continue; }
    if (fence) continue;                                   // tabela em bloco de código é exemplo
    // comentário HTML de várias linhas: o interior não é renderizado, e a tabela de
    // exemplo que os moldes guardam ali não estica nada (o verifica-texto-corrido faz o mesmo)
    if (coment) { if (l.includes('-->')) coment = false; continue; }
    if (/^\s*<!--/.test(l) && !l.includes('-->')) { coment = true; emTabela = false; continue; }

    const eLinhaTabela = l.startsWith('|') && l.trim().endsWith('|');
    if (eLinhaTabela) {
      if (!emTabela) { emTabela = true; colunas = nCelulas(l); linhaCab = i + 1; continue; }
      if (/^\|[\s:|-]+\|$/.test(l.trim())) continue;       // linha separadora
      const n = nCelulas(l);
      if (n !== colunas) {
        t2++;
        console.log(`✗ ${arq}:${i + 1} — [T2] linha com ${n} coluna(s); o cabeçalho (linha ${linhaCab}) tem ${colunas}. ` +
          `Um "|" literal dentro de célula precisa de escape (\\|).`);
      }
      continue;
    }

    if (emTabela) {
      emTabela = false;
      const t = l.trim();
      if (t && !t.startsWith('<!--')) {                    // comentário HTML não estica a tabela
        t1++;
        console.log(`✗ ${arq}:${i + 1} — [T1] tabela colada ao parágrafo seguinte; falta uma linha em branco. ` +
          `O parser absorve este texto como célula da 1ª coluna e a tabela estoura a tela: ${t.slice(0, 70)}…`);
      }
    }
  }
}

const total = t1 + t2;
console.log(total
  ? `\n${total} achado(s) — ${t1} tabela(s) coladas ao parágrafo seguinte (T1), ${t2} linha(s) com colunas a mais ou a menos (T2).`
  : `✓ ${[...new Set(arquivos)].length} arquivo(s) conferido(s) — nenhuma tabela quebrada.`);
process.exit(total ? 1 : 0);
