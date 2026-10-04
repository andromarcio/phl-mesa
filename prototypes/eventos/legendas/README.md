<!-- docqui: 4.1.0 | prompt: PROMPT_PROTOTYPE_FLOW_FULL | atualizado: 2026-10-04 -->
# Protótipo de Fluxo: Legendas
> Feature Set: Legendas — Major Feature Set: Eventos
> Spec de referência: [../../../modules/eventos/legendas/README.md](../../../modules/eventos/legendas/README.md)

---

## Protótipos de fluxo

| Arquivo / Link | Formato | Status | Última revisão |
|---|---|---|---|
| [flow.html](./flow.html) | HTML gerado | 🎨 Mockup | 2026-10-04 |

---

## Telas cobertas neste fluxo

| Tela | Rota | Protótipo de estado |
|---|---|---|
| Configuração de Legendas — nome do evento, contagem de blocos, indicador "Salvando…"/"Salvo", barra de ações, um cartão por bloco com as condições, as setas de reordenação e a remoção, e o estado sem blocos | `/regras-legenda/:eventoId` | — |
| Remover bloco — confirmação | caixa sobre a Configuração de Legendas | — |
| Executar aplicação de legendas — confirmação | caixa sobre a Configuração de Legendas e sobre a Simulação | — |
| Adicionar bloco — abas Usar bloco existente e Criar novo bloco | janela sobre a Configuração de Legendas | — |
| Simulação de aplicação de legendas | janela sobre a Configuração de Legendas | — |
| Salvar como preset | janela sobre a Configuração de Legendas | — |
| Carregar configuração — abas Biblioteca de presets e De outro evento, com a confirmação Excluir preset | janela sobre a Configuração de Legendas | — |
| Catálogo de blocos — busca pelo nome, lista paginada com cor e ações | `/catalogo-legendas` (com `?eventoId=` quando aberto por Gerenciar catálogo) | — |
| Novo bloco e Editar bloco | janela sobre o Catálogo de blocos | — |
| Excluir bloco — confirmação com o uso em eventos | caixa sobre o Catálogo de blocos | — |

*O escopo desta geração é um fluxo por Feature Set; os protótipos de estado por feature (`PROMPT_PROTOTYPE_SCREEN_FULL`) não foram gerados.*

---

## Decisões de design deste fluxo

- As telas foram recuperadas do código-fonte da aplicação, e não desenhadas a partir do design system do kit: rótulos, dicas, botões, colunas, listas de opções e mensagens vêm do inventário extraído do `sistema_mesa_checkin_frontend` (`arquivos/engenharia-reversa/frontend-inventory.md`, seções 4.0 e 4.17 a 4.22) e dos N3 EVT-LEG-01 a EVT-LEG-14. A camada [`tema-gpe.css`](../../_biblioteca-ds/tema-gpe.css) reveste as classes `.dsc-*` com o visual PrimeNG das demais telas (decisão de 2026-10-04).
- A tela atual não tem captura: as imagens de GPE006 retratam o modelo anterior, com a chave Ativa ou Inativa por legenda, os comandos "Salvar Regras" e "Resetar" e o quadro "Preview da condição", que não existem mais, e o protótipo anexado ao ticket `PDTIC25148-34` não foi trazido. A Configuração de Legendas foi montada pelo inventário e pelos N3, em cartões brancos e botões azuis; a cor e o estilo dos botões da barra de ações e das ações de linha do catálogo não constam do inventário.
- O protótipo mostra o que o sistema faz hoje, inclusive o que os N3 marcam com ⚠️: a gravação automática sem botão de salvar e sem mensagem de sucesso, o plural fixo de "Legendas aplicadas", a janela de preset que fecha antes da resposta, a substituição sem confirmação, a data que não chega à aba "De outro evento" e a pergunta de exclusão de bloco que omite o próprio evento e as legendas manuais. Cada desvio está explicado no painel de notas.
- A exclusão de bloco do catálogo não tem caixa de bloqueio: o N3 EVT-LEG-14 não prevê bloqueio, e o uso em eventos só muda o texto da confirmação, em quatro variantes conforme o uso e o caminho por onde o catálogo foi aberto.
- A simulação e a geração avaliam de fato as condições sobre catorze participantes fictícios, segundo as regras de avaliação do N3 EVT-LEG-07, de modo que mudar uma condição muda o resultado. Uma caixa no painel de notas simula a falha do servidor na próxima gravação ou ação, para mostrar o "Erro Interno" e a volta da configuração ao que está gravado.
- A tela mostra só o nome do evento, sem data nem local, como no código. O formulário do bloco é o mesmo na aba "Criar novo bloco" e na janela do catálogo, com a paleta de dezesseis cores, o seletor de cor e o código em maiúsculas.
- O menu horizontal e o menu do usuário levam aos fluxos dos outros Feature Sets; a configuração volta à lista de eventos pelo caminho no alto da tela, e o catálogo aberto pelo menu volta a ela pelo botão "Voltar".

---

## Status geral

**Status**: 🎨 Mockup

**Aprovado por**: — *(preencher quando aprovado)*

---

*Links: [N2 da spec](../../../modules/eventos/legendas/README.md) · [Protótipos do domínio](../README.md) · [Manifesto de protótipos](../../INDEX.md)*
