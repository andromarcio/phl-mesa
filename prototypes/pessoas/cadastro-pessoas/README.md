<!-- docqui: 4.1.0 | prompt: PROMPT_PROTOTYPE_FLOW_FULL | atualizado: 2026-10-04 -->
# Protótipo de Fluxo: Cadastro de Pessoas
> Feature Set: Cadastro de Pessoas — Major Feature Set: Pessoas
> Spec de referência: [../../../modules/pessoas/cadastro-pessoas/README.md](../../../modules/pessoas/cadastro-pessoas/README.md)

---

## Protótipos de fluxo

| Arquivo / Link | Formato | Status | Última revisão |
|---|---|---|---|
| [flow.html](./flow.html) | HTML gerado | 🎨 Mockup | 2026-10-04 |

---

## Telas cobertas neste fluxo

| Tela | Rota | Protótipo de estado |
|---|---|---|
| Pessoas — filtros, lista, Editar Pessoa e Remover Pessoa em cada linha | `/administracao-pessoas` | — |
| Pessoa — inclusão ("Cadastrar Pessoa") e edição, em cinco abas | `/administracao-pessoa` e `/administracao-pessoa/:id` | — |
| Carga de Grupos Temáticos | janela sobre a tela Pessoas | — |
| Carga de Temas | janela sobre a tela Pessoas | — |
| Carga de Histórico | janela sobre a tela Pessoas | — |

*O escopo desta geração é um fluxo por Feature Set; os protótipos de estado por feature (`PROMPT_PROTOTYPE_SCREEN_FULL`) não foram gerados.*

---

## Decisões de design deste fluxo

- As telas foram recuperadas do código-fonte da aplicação, e não desenhadas a partir do design system do kit: rótulos, placeholders, botões, colunas e mensagens vêm do inventário extraído do `sistema_mesa_checkin_frontend` (`arquivos/engenharia-reversa/frontend-inventory.md`, seções 4.4 a 4.8), e o visual, das imagens de GPE003. A camada [`tema-gpe.css`](../../_biblioteca-ds/tema-gpe.css) reveste as classes `.dsc-*` com esse visual (decisão de 2026-10-04).
- O protótipo mostra o que o sistema faz hoje, inclusive o que o N3 marca com ⚠️: a confirmação nativa do navegador na exclusão, a mensagem "Pessoa removido com sucesso", a mensagem de inclusão repetida na edição e a tela que não volta à lista depois de gravar. Cada desvio está no painel de notas do protótipo.
- A Pessoa usa uma só tela para inclusão e edição, como o código: na inclusão aparece o título "Cadastrar Pessoa" e o botão "Criar"; na edição, o cabeçalho com as iniciais e o nome, as datas de criação e de alteração e o botão "Atualizar". A aba ativa verde e o botão principal anil reproduzem o tema Aura que essa tela usa.
- As três cargas compartilham uma janela, trocando título, instrução e mensagens conforme o botão que a abriu.
- O menu horizontal e o menu do usuário levam aos fluxos dos outros Feature Sets.

---

## Status geral

**Status**: 🎨 Mockup

**Aprovado por**: — *(preencher quando aprovado)*

---

*Links: [N2 da spec](../../../modules/pessoas/cadastro-pessoas/README.md) · [Protótipos do domínio](../README.md) · [Manifesto de protótipos](../../INDEX.md)*
