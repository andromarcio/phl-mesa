<!-- docqui: 4.1.0 | prompt: PROMPT_PROTOTYPE_FLOW_FULL | atualizado: 2026-10-04 -->
# Protótipo de Fluxo: Cadastro de Eventos
> Feature Set: Cadastro de Eventos — Major Feature Set: Eventos
> Spec de referência: [../../../modules/eventos/cadastro-eventos/README.md](../../../modules/eventos/cadastro-eventos/README.md)

---

## Protótipos de fluxo

| Arquivo / Link | Formato | Status | Última revisão |
|---|---|---|---|
| [flow.html](./flow.html) | HTML gerado | 🎨 Mockup | 2026-10-04 |

---

## Telas cobertas neste fluxo

| Tela | Rota | Protótipo de estado |
|---|---|---|
| Eventos — filtros, lista e os ícones de ação de cada linha: Configuração de Legendas, Tornar evento principal, Cargas de Convidados e Confirmados, Participantes, Visualizar evento, Editar evento e Excluir evento | `/eventos` | — |
| Evento — inclusão ("Novo Evento") | `/eventos/detail` | — |
| Evento — edição ("Editar Evento") | `/eventos/detail/edit/:id` | — |
| Evento — visualização, na mesma tela, com os dados como texto | `/eventos/detail/view/:id` | — |
| Confirmação da exclusão (caixa nativa do navegador) | janela sobre a tela Eventos | — |
| Cargas de Convidados e Confirmados — Carga de Convidados, Carga de Confirmados e Inscritos do CRM | janela sobre a tela Eventos | — |

*O escopo desta geração é um fluxo por Feature Set; os protótipos de estado por feature (`PROMPT_PROTOTYPE_SCREEN_FULL`) não foram gerados.*

---

## Decisões de design deste fluxo

- As telas foram recuperadas do código-fonte da aplicação, e não desenhadas a partir do design system do kit: rótulos, placeholders, botões, colunas, dicas dos ícones e mensagens vêm do inventário extraído do `sistema_mesa_checkin_frontend` (`arquivos/engenharia-reversa/frontend-inventory.md`, seções 4.0, 4.9 a 4.11, 4.16 e 7.1), e o visual, das imagens de GPE004 — "Pesquisar Evento", "Incluir / Editar Evento", "Detalhar Evento" e "Carregar Convidados / Confirmados". A camada [`tema-gpe.css`](../../_biblioteca-ds/tema-gpe.css) reveste as classes `.dsc-*` com esse visual (decisão de 2026-10-04).
- O protótipo mostra o que o sistema faz hoje, inclusive o que os N3 marcam com ⚠️: a lista que abre com 5 linhas, a Data Final que não limita a pesquisa, o texto relativo contado em blocos de 24 horas, a confirmação nativa do navegador na exclusão, o evento principal trocado sem confirmação, a visualização com o título "Editar Evento", as cargas sem resumo e a planilha de confirmados que não é enviada junto com a de convidados. Cada desvio está explicado no painel de notas do protótipo.
- O paginador segue a tela atual, sem o relatório "[1 a N de T]" e sem o seletor de linhas por página que a imagem de GPE004 mostra: o N3 de Pesquisar Eventos registra que a tela atual não os tem.
- O Evento usa uma só tela para inclusão, edição e visualização, como o código: na inclusão, o título "Novo Evento" e o botão "Salvar" com o sinal de mais; na edição, "Editar Evento" e o ícone de confirmação; na visualização, os campos viram texto e só resta "Voltar". O Código da Campanha fica ao lado de Participantes, na ordem do código, porque as imagens de GPE004 são anteriores ao campo.
- A janela de cargas reúne as duas planilhas e a importação do CRM. A aparência da seção "Inscritos do CRM" é inferida do inventário: a imagem de GPE004 não a mostra.
- As datas dos eventos fictícios são calculadas a partir do dia em que o protótipo é aberto, para que sempre haja eventos futuros, de hoje e finalizados.
- O painel de notas traz dois controles de simulação: o perfil do usuário, para mostrar que só o botão "Adicionar" confere o perfil, e uma falha a aplicar nas próximas ações (servidor, tipo de arquivo, CRM indisponível), para exibir as mensagens de erro dos N3.
- O ícone "Participantes" abre o fluxo de Participantes em nova aba, como o sistema; o ícone "Configuração de Legendas", o menu horizontal e o menu do usuário levam aos fluxos dos outros Feature Sets. O fluxo aceita os endereços `#eventos`, `#evento-novo`, `#evento`, `#evento-visualizar` e `#cargas`.

---

## Status geral

**Status**: 🎨 Mockup

**Aprovado por**: — *(preencher quando aprovado)*

---

*Links: [N2 da spec](../../../modules/eventos/cadastro-eventos/README.md) · [Protótipos do domínio](../README.md) · [Manifesto de protótipos](../../INDEX.md)*
