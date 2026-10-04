<!-- docqui: 4.1.0 | prompt: PROMPT_PROTOTYPE_FLOW_FULL | atualizado: 2026-10-04 -->
# Protótipo de Fluxo: Participantes
> Feature Set: Participantes — Major Feature Set: Eventos
> Spec de referência: [../../../modules/eventos/participantes/README.md](../../../modules/eventos/participantes/README.md)

---

## Protótipos de fluxo

| Arquivo / Link | Formato | Status | Última revisão |
|---|---|---|---|
| [flow.html](./flow.html) | HTML gerado | 🎨 Mockup | 2026-10-04 |

---

## Telas cobertas neste fluxo

| Tela | Rota | Protótipo de estado |
|---|---|---|
| Participantes do evento, visão do Administrador — cabeçalho do evento, critérios de pesquisa, Lista de Participantes com check-in, confirmação de presença, atalho da legenda e Download (`flow.html#lista`) | `/evento-pessoa/:id`, visão Participantes | — |
| Participantes do evento, visão da Secretaria Check-In — sem os critérios Temas, Grupos de Trabalho e Cargo, com Confirmado só para leitura e Assento como texto (`flow.html#checkin`) | `/evento-pessoa/:id`, no evento principal | — |
| Cadastrar Pessoa | janela aberta pelo botão do cabeçalho, na lista e no mapa do Administrador e na lista da Secretaria Check-In | — |
| Gerenciar Legenda da Pessoa | janela sobre a lista, aberta pela coluna Assento | — |
| Caixa de confirmação — Remover confirmação, Confirmar participante e Confirmar Remoção | janela sobre a lista e sobre Gerenciar Legenda da Pessoa | — |
| Mapa de Assentos, visão do Administrador — Pessoas Disponíveis, busca na mesa, Gerenciar Pessoas Alocadas na Mesa, mapa Retangular, Legenda das Categorias e Exportações (`flow.html#mapa`) | `/evento-pessoa/:id`, visão Mapa de Assentos | — |
| Selecionar Pessoa | janela aberta pelo clique em assento do mapa do Administrador | — |
| Mapa de Assentos, visão da Secretaria Mesa — fila de quem chegou, atendimento e mapa só para consulta (`flow.html#mapa-secretaria`) | `/evento-pessoa/:id`, aberta direto no mapa do evento principal | — |

*O escopo desta geração é um fluxo por Feature Set; os protótipos de estado por feature (`PROMPT_PROTOTYPE_SCREEN_FULL`) não foram gerados.*

---

## Decisões de design deste fluxo

- As telas foram recuperadas do código-fonte da aplicação, e não desenhadas a partir do design system do kit: rótulos, textos de apoio, botões, colunas, dicas e mensagens vêm do inventário extraído do `sistema_mesa_checkin_frontend` (`arquivos/engenharia-reversa/frontend-inventory.md`, seções 2.3 e 2.4, 4.0, 4.12 a 4.16, 4.23 e 5.1 a 5.4), e o visual, das imagens de GPE005 — a lista, a planilha exportada, a janela Cadastrar Pessoa, a janela de legenda e os dois mapas. A camada [`tema-gpe.css`](../../_biblioteca-ds/tema-gpe.css) reveste as classes `.dsc-*` com esse visual (decisão de 2026-10-04).
- O protótipo mostra o que o sistema faz hoje, inclusive o que os N3 marcam com ⚠️: as dicas "Confirmado" e "Não confirmado" no ícone de check-in, a caixa de confirmação com os botões "Remover" e "Cancelar" também para confirmar presença, a janela de legenda que só reconhece a legenda manual, a lista que não é recarregada depois do cadastro na recepção, a gravação do mapa inteiro, o "Limpar Todas" que não é gravado e a alteração não gravada descartada pela atualização automática. Cada desvio está no painel de notas do protótipo.
- Um único arquivo cobre os três perfis, como o código, que usa a mesma rota com visões diferentes. O seletor "Perfil simulado", no painel de notas, troca o perfil e leva à tela de entrada de cada um: o Administrador entra na lista e alterna com o mapa pelos botões "Participantes" e "Mapa de Assentos"; a Secretaria Mesa entra direto no mapa de consulta, com o menu reduzido a "Evento"; a Secretaria Check-In entra na lista reduzida. O cabeçalho do evento é comum às visões e mostra, conforme o perfil, os botões de alternância, o "Cadastrar Pessoa" ou o indicador de atualização automática. Os endereços `#lista`, `#mapa`, `#mapa-secretaria` e `#checkin` abrem cada visão já com o perfil certo, e são os endereços que os outros fluxos usam para chegar aqui.
- O mapa é o do formato de mesa Retangular, com os 181 assentos dos setores A a H na disposição do código: setores F, G e H empilhados à esquerda, a mesa principal ao centro e o setor E à direita. Atribuir assento funciona com arrastar e soltar de verdade (HTML5), pelo cartão da lista ou pelo ocupante de outro assento, e também pelo clique no assento vazio. O protótipo separa o que está gravado do que está só no mapa aberto, para que a gravação automática de 30 segundos, o botão "Salvar Alocações (n)" e a atualização automática de 3 segundos se comportem como no sistema; o botão "Simular check-in feito na recepção por outro usuário", no painel de notas, provoca a atualização.
- A fila da Secretaria Mesa usa o texto "ATENDIDO", que é o do botão no computador; "ATENDER", que aparece na imagem de GPE005, é o texto do tablet, cuja disposição em carrossel não foi representada. As fotos das pessoas foram substituídas por iniciais; sem foto, aparece o ícone de pessoa, como no sistema.
- O menu horizontal, o menu do usuário, o nome do participante (que abre o cadastro da pessoa em nova aba) e o breadcrumb levam aos fluxos dos outros Feature Sets. O menu "Evento" da Secretaria Check-In foi suposto igual ao da Secretaria Mesa, porque não há captura desse perfil.
- Componentes que o tema ainda não tinha foram criados no `<style>` do arquivo, como candidatos ao `tema-gpe.css`: seleção múltipla (`gpe-ms`), disposição da mesa principal (`gpe-main-table`, `gpe-map-stack`), camada de carregamento do mapa (`gpe-map-wrap`, `gpe-map-overlay`), lista de opções clicáveis (`gpe-option-list`, `gpe-option`) e a etiqueta amarela de check-in não identificado (`gpe-tag-check--pendente`).

---

## Status geral

**Status**: 🎨 Mockup

**Aprovado por**: — *(preencher quando aprovado)*

---

*Links: [N2 da spec](../../../modules/eventos/participantes/README.md) · [Protótipos do domínio](../README.md) · [Manifesto de protótipos](../../INDEX.md)*
