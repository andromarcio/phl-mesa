#!/usr/bin/env node
// valida-sumario-kpi.mjs — acusa Sumário de AIM que vai cair no modo tabela em vez do
// grid de cartões KPI.
//
// Por quê: `scripts/gera-html-impacto.mjs` converte a tabela `## Sumário` (Indicador |
// Valor) num grid de cartões — MAS só se TODAS as linhas tiverem um valor extraível
// (um número, opcionalmente composto, ou uma palavra curta). Se uma única linha trouxer
// prosa longa na coluna Valor, a tabela INTEIRA cai de volta para o modo tabela simples,
// em silêncio — o markdown renderiza sem erro, só o visual sai diferente de todos os
// outros documentos do lote. Foi o que aconteceu no portal-compras, na análise do
// PDTIC25114-660: linhas como "Das 16 regras atuais, boa parte muda, some ou ganha par
// nova — ver seção 2" não reduzem a um valor de cartão.
//
// O molde da AIM não tem `## Sumário`; quem o traz é a AIM migrada de um relatório
// `ANALISE_IMPACTO_*` (o `migra-aim` preserva a seção) e a AIM que a instância escolher
// abrir com o painel. AIM sem a seção passa batido.
//
// Este validador reaproveita a MESMA função do gerador (`kpiDaTabela`/`valorDe`,
// importadas de `gera-html-impacto.mjs`) — não uma cópia da regra, que arriscaria
// aprovar algo que o gerador reprovaria (ou vice-versa) assim que uma delas mudasse.
//
// Uso:  node scripts/valida-sumario-kpi.mjs [arquivo.md | pasta] ...
//       (sem argumentos: varre analise-impacto/)

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { kpiDaTabela, valorDe } from './gera-html-impacto.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));

const alvos = process.argv.slice(2).length ? process.argv.slice(2) : ['analise-impacto'];
const arquivos = [];
for (const alvo of alvos) {
  if (!fs.existsSync(alvo)) continue;
  const st = fs.statSync(alvo);
  if (st.isFile()) { arquivos.push(alvo); continue; }
  for (const nome of fs.readdirSync(alvo)) {
    if (nome.startsWith('_') || nome === 'INDEX.md') continue;
    if (nome.endsWith('.md')) arquivos.push(path.join(alvo, nome));
  }
}

// Extrai o bloco de tabela (linhas que começam com `|`) do primeiro trecho contíguo
// dentro da seção "## Sumário" — a seção não deve ter mais nada além da tabela, mas a
// extração tolera uma linha em branco solta.
function extraiTabelaDoSumario(linhas) {
  const idx = linhas.findIndex((l) => /^##\s+Sum[áa]rio\s*$/i.test(l.trim()));
  if (idx === -1) return null;
  let fim = linhas.length;
  for (let i = idx + 1; i < linhas.length; i++) {
    if (/^##\s/.test(linhas[i]) || /^---\s*$/.test(linhas[i].trim())) { fim = i; break; }
  }
  const tabela = [];
  let comecou = false;
  for (const l of linhas.slice(idx + 1, fim)) {
    const t = l.trim();
    if (t.startsWith('|')) { tabela.push(t); comecou = true; }
    else if (comecou) break;
  }
  return tabela.length ? tabela.join('\n') : null;
}

function diagnostica(blocoTabela) {
  const linhas = blocoTabela.split('\n');
  const falhas = [];
  for (let i = 2; i < linhas.length; i++) {
    const cols = linhas[i].split('|');
    const rotulo = (cols[1] ?? '').trim();
    const valorBruto = (cols[2] ?? '').trim();
    if (!valorDe(valorBruto)) falhas.push({ rotulo, valorBruto });
  }
  return falhas;
}

let arquivosReprovados = 0;
for (const arq of arquivos) {
  const linhas = fs.readFileSync(arq, 'utf-8').split('\n');
  const bloco = extraiTabelaDoSumario(linhas);
  if (!bloco) continue; // sem "## Sumário" com tabela — nada a checar

  const cab = bloco.split('\n')[0].split('|').map((c) => c.trim()).filter(Boolean);
  if (cab.length !== 2 || !/indicador/i.test(cab[0]) || !/valor/i.test(cab[1])) continue; // não é a tabela Indicador|Valor — nada a checar

  if (kpiDaTabela(bloco)) continue; // ✓ vira grade de KPI

  arquivosReprovados++;
  const falhas = diagnostica(bloco);
  console.log(`✗ ${arq} — Sumário NÃO vai virar grade de KPI; cai no modo tabela simples.`);
  for (const f of falhas) {
    const amostra = f.valorBruto.length > 70 ? f.valorBruto.slice(0, 70) + '…' : f.valorBruto;
    console.log(`    linha "${f.rotulo}" — valor não reduz a um número ou palavra curta: "${amostra}"`);
  }
  console.log('    Mova o detalhamento para a seção correspondente e deixe só um valor curto na coluna Valor.');
}

console.log(arquivosReprovados
  ? `\n${arquivosReprovados} Sumário(s) fora do padrão de KPI. Corrija a coluna Valor (ver ${path.relative(process.cwd(), HERE)}/gera-html-impacto.mjs → kpiDaTabela) e rode de novo.`
  : '✓ Todo Sumário com tabela Indicador|Valor vira grade de KPI.');
process.exit(arquivosReprovados ? 1 : 0);
