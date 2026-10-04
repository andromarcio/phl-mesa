<!-- docqui: 4.1.0 | prompt: PROMPT_PROTOTYPE_FLOW_FULL | atualizado: 2026-10-04 -->
# Protótipos — Manifesto de fidelidade e aprovação
> Fonte de verdade do vínculo **protótipo ↔ N3**, do nível de **fidelidade** e do
> **status de aprovação**. Uma tela com fidelidade **obrigatória** só vira **contrato
> de implementação** quando o protótipo está **aprovado** aqui (com quem e quando).

> ⚠️ **Protótipos recuperados do sistema existente.** Os protótipos desta instância são de fluxo, um por Feature Set (`PROMPT_PROTOTYPE_FLOW_FULL`), e reproduzem as telas como estão no código-fonte da aplicação — o inventário de telas em `arquivos/engenharia-reversa/frontend-inventory.md` e as imagens dos documentos legados GPE001 a GPE006 —, revestidos pela camada [`_biblioteca-ds/tema-gpe.css`](./_biblioteca-ds/tema-gpe.css). A fidelidade registrada aqui é **referência**; os N3 continuam com `Fidelidade ao protótipo: n/a`, por decisão de 2026-10-04 de não alterar as specs para registrar o vínculo. Quando um N3 for revisto pelo `PROMPT_4A`, a linha da `## Superfície` passa a apontar o protótipo.

| Protótipo | Feature (N3) | Fidelidade | Status | Aprovado por | Data |
|---|---|---|---|---|---|
| [pessoas/cadastro-pessoas/flow.html](./pessoas/cadastro-pessoas/flow.html) — tela Pessoas | `PES-CAD-01` | referência | rascunho | — | — |
| [pessoas/cadastro-pessoas/flow.html](./pessoas/cadastro-pessoas/flow.html) — tela Pessoa, inclusão | `PES-CAD-02` | referência | rascunho | — | — |
| [pessoas/cadastro-pessoas/flow.html](./pessoas/cadastro-pessoas/flow.html) — tela Pessoa, edição | `PES-CAD-03` | referência | rascunho | — | — |
| [pessoas/cadastro-pessoas/flow.html](./pessoas/cadastro-pessoas/flow.html) — tela Pessoas, Remover Pessoa | `PES-CAD-04` | referência | rascunho | — | — |
| [pessoas/cadastro-pessoas/flow.html](./pessoas/cadastro-pessoas/flow.html) — janela Carga de Grupos Temáticos | `PES-CAD-05` | referência | rascunho | — | — |
| [pessoas/cadastro-pessoas/flow.html](./pessoas/cadastro-pessoas/flow.html) — janela Carga de Temas | `PES-CAD-06` | referência | rascunho | — | — |
| [pessoas/cadastro-pessoas/flow.html](./pessoas/cadastro-pessoas/flow.html) — janela Carga de Histórico | `PES-CAD-07` | referência | rascunho | — | — |

## Como manter

- A pasta `prototypes/` **espelha `modules/`**: `prototypes/[dominio]/[feature-set]/[feature]/`, com os mesmos nomes de pasta e um `README.md` em cada nível — domínio (índice dos Feature Sets com protótipo), Feature Set (protótipo de fluxo) e feature (protótipos de estado). Modelos em `engine/templates/prototypes/_template/`.
- Ao **gerar** um protótipo, registre a linha com status **rascunho** e a fidelidade lida do N3 (linha `Fidelidade ao protótipo` na `## Superfície`).
- Na **aprovação**, troque o status para **aprovado** e preencha **quem** e **quando**. Só então a tela é **contrato** para a codificação.
- A implementação de telas **obrigatória** exige a **checklist de fidelidade** — `node scripts/fidelity-checklist.mjs <pasta-do-protótipo> <N3.md>` — com **todos os estados cobertos** (✅, ou ⚠️ com desvio aprovado; nenhum ❌).
- **Reforço opcional (CI, onde há runtime):** regressão visual `node scripts/proto-visual-diff.mjs <protótipo> <tela-implementada>` — roda no **repositório de código** (Playwright + app), não aqui. Ver o cabeçalho do script.

## Legenda

- **Fidelidade** — `obrigatória`: a implementação reproduz o protótipo; `referência`: guia a intenção.
- **Status** — `rascunho`: em elaboração; `aprovado`: travado como contrato (registrar quem/quando).
