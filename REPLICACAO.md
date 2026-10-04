# Registro de mudanças para replicação

> Ledger das mudanças feitas **primeiro aqui** (`gpe-doc`) que precisam ser **replicadas depois** nas outras instâncias docqui que usam a mesma solução — `portal-compras`, `premio-iel` e `transparencia-web`. Cada entrada diz o que mudou, onde e como aplicar no destino; a **matriz de status** mostra o que já foi replicado e o que ainda falta. Segue o modelo dos ledgers dessas instâncias.

---

## Escopo — o que entra e o que não entra

Entra o que é **maquinário compartilhado entre as instâncias**: o visualizador (`index.html`, `assets/`), os scripts que não vêm do engine (`scripts/gera-mapa-features.mjs`) e convenções do `CLAUDE.md`. O que vem do engine (`engine/`, o restante de `scripts/`, `.claude/`) não entra: chega pelo `sync-instance`.

**Não entra** conteúdo de especificação do produto: os N0–N3 em `modules/`, o `global/` preenchido, `documentos/`, `REVISAO-CONVERSAO.md` e `revisao-conversao/` descrevem o GPE e não têm equivalente nas outras.

---

## Como replicar sem quebrar o destino

As instâncias **divergem** entre si: o visualizador é copiado de uma para outra e cada cópia seguiu o seu caminho. Antes de aplicar uma entrada, procure o trecho equivalente no destino e **estenda em vez de duplicar**; confira no navegador comparando os títulos `##` da fonte de cada `.md` com o texto renderizado — conferir só que a página abriu não pega nenhum dos defeitos abaixo — e prove que a conferência dispara contra o código anterior.

---

## Matriz de status

> Legenda: ⬜ pendente · ✅ replicado · ➖ não se aplica.

| ID | Data | Mudança | Rota | `portal-compras` | `premio-iel` | `transparencia-web` |
|---|---|---|---|:---:|:---:|:---:|
| REP-001 | 2026-10-01 | Visualizador e mapa de features leem o N1 com o título da 3.0.0 (`# Major Feature Set:`) | local entre instâncias | ✅ | ✅ | ✅ |
| REP-002 | 2026-10-01 | Visualizador: o leitor de front-matter casa um comentário por vez e deixa de engolir seções | local entre instâncias | ✅ | ✅ | ✅ |
| REP-003 | 2026-10-01 | Visualizador: a subseção `###` dentro da `## Descrição` do N1 deixa de sumir | local entre instâncias | ➖ | ✅ | ✅ |
| REP-004 | 2026-10-01 | Visualizador: o link de um N1 para outro N1 deixa de ser reescrito para um caminho que não existe | local entre instâncias | ✅ | ✅ | ✅ |
| REP-005 | 2026-10-01 | Visualizador: a seção de regras do N3 aparece também quando a lista vem colada ao título | local entre instâncias | ✅ | ✅ | ✅ |

Os ✅ são de 2026-10-01 e valem para os repositórios `phl-portal-compras-doc`, `premio-iel` e `phl-transparencia-web-doc`, onde as mudanças ficaram **na cópia de trabalho, sem commit**. Os repositórios `portal-compras` e `transparencia-web` do GitHub, que pararam em 2026-09-29 no engine 2.23.0, não foram tocados e têm os mesmos defeitos.

---

## Entradas

> Append-only: uma entrada nunca é reescrita para "corrigir" o que a mudança foi — se algo evoluir depois, abre-se **nova** entrada. O que se atualiza é a **matriz** (⬜ → ✅) quando a replicação é feita.

### REP-001 — Visualizador e mapa leem o N1 da 3.0.0 · 2026-10-01

- **O que mudou aqui**: o `scripts/gera-mapa-features.mjs` e o `extractTitle` do `index.html` passaram a ler o par `(?:Major Feature Set|Domínio):`, e não só `Domínio:`. O título de reserva do template de N1 (`renderN1DomainTemplate`) e a cópia `assets/js/app.js` receberam o mesmo par.
- **Por que existe**: o `gpe-doc` é a primeira instância com os N1 escritos no molde da 3.0.0. Com o título novo, o mapa de features saía com **0 domínios** e o passo do `atualiza-pages` respondia ✓; o menu e o título da página mostravam "Major Feature Set: Eventos". É a quebra que o `CHANGELOG.md` do engine descreve em *Migração da 3.0.0 — quem lê o título do N1*.
- **Arquivos**: `scripts/gera-mapa-features.mjs`, `index.html`, `assets/js/app.js`.
- **Como replicar**: `grep -n "Domínio" scripts/gera-mapa-features.mjs index.html assets/js/app.js` e trocar os **leitores** do título pelo par; os rótulos de tela ("Domínio: Eventos" no breadcrumb) ficam como estão.
- **Prove que dispara antes de dar por feito**: numa cópia de rascunho de `modules/` com um N1 retitulado, o gerador anterior perde o domínio (no `transparencia-web`, 3 domínios e 28 features em vez de 4 e 30) e o corrigido o conta. No navegador, trocando o título em memória, o menu mostra o nome sem o prefixo.

### REP-002 — Visualizador: o front-matter casa um comentário por vez · 2026-10-01

- **O que mudou aqui**: no `parseFrontMatter`, o grupo `(?:\s*<!--[\s\S]*?-->)*` virou `(?:\s*<!--(?:(?!-->)[\s\S])*-->)*`. O mesmo na cópia `assets/js/app.js`.
- **Por que existe**: com o `[\s\S]*?-->` solto, o documento que abre com o carimbo docqui, **não** tem front-matter e traz adiante outro comentário seguido de `---` tinha tudo até ali lido como front-matter. O `modules/INDEX.md` perdia Domínios, Rastreabilidade, Esteira e Pendências; nenhum erro aparecia.
- **Arquivos**: `index.html`, `assets/js/app.js`.
- **Como replicar**: a expressão é a mesma nas quatro instâncias; basta a troca.
- **Prove que dispara antes de dar por feito**: contra o código anterior, perdiam conteúdo o `global/PATTERNS.md` nas três instâncias, o `global/DESIGN-SYSTEM.md` e três documentos da base de conhecimento no `portal-compras`, e um documento da base de conhecimento no `premio-iel`. Depois da troca, nenhum; os documentos com front-matter de verdade continuam lidos como antes.

### REP-003 — Visualizador: a subseção dentro da Descrição do N1 · 2026-10-01

- **O que mudou aqui**: no `renderN1DomainTemplate`, o corte da `## Descrição` passou de `\n##` para `\n##\s`, nas duas expressões (a que lê e a que remove do corpo).
- **Por que existe**: `\n##` também casa o início de `### O que este domínio NÃO faz`, que o molde do N1 põe **dentro** da Descrição. A subseção e a sua tabela sumiam da página.
- **Arquivos**: `index.html`.
- **Como replicar**: a correção nasceu no `portal-compras` (commit `3a288b6` do `phl-portal-compras-doc`, de 2026-09-24, sem entrada no ledger de lá) e foi trazida para cá na cópia do visualizador; por isso a coluna dele é ➖.
- **Prove que dispara antes de dar por feito**: contra o código anterior, 4 de 4 N1 do `transparencia-web` e 5 de 5 do `premio-iel` não mostravam a subseção; depois, todos mostram.

### REP-004 — Visualizador: link de um N1 para outro N1 · 2026-10-01

- **O que mudou aqui**: no `renderN1DomainTemplate`, as duas expressões que reescrevem `…/README.md` para `#modules/<domínio>/…` ganharam `(?!\.\.\/)`: só o link para um Feature Set do próprio domínio é reescrito ali. O link `../outro/README.md` segue adiante e é resolvido pelo pós-processamento do DOM, contra a pasta do documento.
- **Por que existe**: `→ ver [N1 Pessoas](../pessoas/README.md)` virava `#modules/eventos/./pessoas/README.md`, que não existe.
- **Arquivos**: `index.html`.
- **Como replicar**: onde o visualizador já tem o pós-processamento do DOM (o `REP-039` do `portal-compras`), basta o `(?!\.\.\/)`. **No `premio-iel` ele não existe**: só com o `(?!\.\.\/)` o link ficava relativo e tirava o leitor do visualizador. Lá, a seção do N1 passou também pelo `reescreveLinksInternos`, que a instância já tinha para o documento genérico.
- **Prove que dispara antes de dar por feito**: injetando o link em memória num N1, o `href` final tem de ser `#modules/<outro>/README.md` e o clique tem de abrir o N1 de destino; os links reais dos N1 para os seus Feature Sets têm de continuar válidos (28 no `transparencia-web`, 47 no `portal-compras`, 26 no `premio-iel`).

### REP-005 — Visualizador: regras coladas ao título · 2026-10-01

- **O que mudou aqui**: no template do N3, a leitura da seção passou de `## Regras de negócio\s*\n\n(` para `## Regras de negócio\s*\n(`.
- **Por que existe**: com a lista começando na linha logo abaixo do título, sem linha em branco, a leitura não casava — e o corte seguinte tirava a seção do corpo. As regras sumiam da página. Achado ao replicar as entradas acima no `transparencia-web`, onde 5 features estavam assim.
- **Arquivos**: `index.html`.
- **Como replicar**: a expressão é a mesma nas quatro instâncias; basta a troca. Com linha em branco o resultado é idêntico ao de antes.
- **Prove que dispara antes de dar por feito**: no `transparencia-web`, as 5 features voltam a mostrar as regras; nas demais, colando a lista ao título em memória, a primeira regra continua na página.

---

## Convenções deste ledger

- IDs sequenciais `REP-NNN`, próprios deste ledger — o `REP-001` daqui não é o `REP-001` do `portal-compras`; cite sempre com o repositório quando houver dúvida.
- Entradas são **histórico** (append-only); só a **matriz de status** muda ao longo do tempo (⬜ → ✅).
