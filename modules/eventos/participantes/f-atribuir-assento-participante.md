<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: EVT-PAR-08
feature_set: EVT-PAR
dominio: EVT
entidade: EventoPessoa
data_model_ref: data-models/eventos.md#eventopessoa
endpoints: []
error_codes: []
depende_de: ["EVT-PAR-07"]
origem:
  tipo: ""
  chave: ""
estado: rascunho
gates:
  requisitos:   { aprovado: false, por: "", em: "", pr: "" }
  modelo-dados: { aprovado: false, por: "", em: "", pr: "" }
  testes:       { aprovado: false, por: "", em: "", pr: "" }
  codigo:       { aprovado: false, por: "", em: "", pr: "" }
contagem:
  pendente: true
  revisada_em: ""
  revisada_ate: ""
---

# Atribuir Assento ao Participante
> **Nível 3** - Feature Set: Participantes — Major Feature Set: Eventos - `EVT-PAR-08`

## Descrição

Permite que o Administrador atribua a um participante um assento do mapa do evento; o participante passa a ocupar o assento, sai da lista de pessoas disponíveis e fica localizável no mapa pela secretaria de mesa.

No mapa de assentos, o Administrador arrasta a pessoa da lista "Pessoas Disponíveis" até o assento, arrasta-a de um assento para outro, ou clica no assento vazio e escolhe a pessoa na janela "Selecionar Pessoa". A alteração é gravada sozinha 30 segundos depois da última mudança, ou na hora pelo botão "Salvar Alocações (n)".

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE005 – Gerenciar Participante v1.1, de 16/12/2025 (documento legado), funcionalidade "Marcar Assento do Participante" ⚠️ sem chave na ferramenta de demandas | Criação | — Definir o assento de um participante colocando-o sobre um assento do mapa, por arraste, e retirá-lo da lista de pessoas disponíveis. A escolha pela janela "Selecionar Pessoa", a gravação do mapa inteiro — automática ou pelo botão "Salvar Alocações (n)" — e o destino do ocupante anterior vêm do código 💻. Tickets do Jira relacionados pelo título, sem AIM aberta 🔍: `PDTIC25148-16` (Mapa de mesa) e `PDTIC25148-28` (Mapa de mesa - melhorias), concluídos; `PDTIC25148-31` (Mapa de mesa - Permitir arrastar mais de uma cadeira ao mesmo tempo), a fazer — o arraste de várias pessoas de uma vez não existe hoje |

---

<div class="dev-only">

## Superfície

**Ação em tela** — origem: Consultar Mapa de Assentos `EVT-PAR-07` (`/evento-pessoa/:id`, visão Mapa de Assentos, versão do Administrador); gatilhos: soltar sobre o assento o cartão arrastado da lista "Pessoas Disponíveis", soltar sobre o assento o ocupante arrastado de outro assento, ou clicar no assento e escolher a pessoa na janela "Selecionar Pessoa". A gravação é disparada pelo botão "Salvar Alocações (n)" ou sozinha, 30 s depois da última alteração

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Consultar Mapa de Assentos — Perfil Administrador" de GPE005

---

</div>

## Regras de negócio

1. Recebe assento o participante que faz parte do mapa: o que tem presença confirmada ou check-in feito. → ver Consultar Mapa de Assentos `EVT-PAR-07` 💻
2. Um participante ocupa no máximo um assento: atribuir-lhe outro assento o tira do anterior.
3. Atribuir um participante a um assento já ocupado tira o ocupante anterior do assento e o devolve às pessoas disponíveis; os dois não trocam de lugar. 💻 ⚠️ GPE005 diz que a marcação pode ser feita "arrastando o participante para um assento vazio ou ocupado" 📄, sem dizer o que acontece com quem ocupava o assento.
4. A atribuição só passa a valer para quem mais consulta o mapa depois de gravada. O que se grava é sempre o mapa inteiro: a relação completa dos participantes sentados, cada um com o seu assento, substitui todas as atribuições que o evento tinha. 💻 ⚠️ GPE005 não menciona gravação: descreve a marcação como imediata 📄.
5. A gravação acontece sozinha, 30 segundos depois da última alteração feita no mapa, ou de imediato, a pedido do Administrador. 💻 ⚠️ No código, o intervalo de 30 segundos vem acompanhado da anotação "5 segundos" — confirmar com o PO qual é o intervalo desejado.
6. A gravação só acontece quando há pelo menos um participante sentado; o mapa sem ninguém sentado nunca é enviado ao servidor. 💻 ⚠️ É o que impede a gravação da retirada do último participante e da liberação de todos os assentos → ver Remover Assento do Participante `EVT-PAR-09` e Liberar Todos os Assentos `EVT-PAR-11`.
7. A gravação é indivisível: se algum dos assentos enviados não existe entre os assentos do evento, nenhuma atribuição é gravada e o mapa anterior permanece. 💻
8. O servidor não confere se dois participantes receberam o mesmo assento nem se o assento já estava ocupado: a regra de um ocupante por assento depende do que o mapa do Administrador envia. 💻 ⚠️ Com dois Administradores montando o mesmo mapa, prevalece por inteiro a última gravação, e o que o outro tinha gravado se perde. 🔍
9. Ao gravar o mapa, o servidor regrava a participação de cada pessoa sentada com as marcações de Convidado, Confirmado, Check-In e Atendido que o mapa do Administrador tinha naquele momento — e não com as que estavam guardadas. 💻 ⚠️ Suspeita de defeito: uma marcação mudada em outro ponto do sistema e ainda não refletida no mapa do Administrador pode ser desfeita pela gravação; é o caso do atendimento, que o mapa aberto não percebe sozinho. 🔍
10. Na mesma gravação, a participação de cada pessoa sentada perde a data e hora do check-in e todos os dados que vieram do CRM na importação de inscritos. 💻 ⚠️ Suspeita de defeito, lida no código e não confirmada em execução: a participação é regravada só com as quatro marcações, o assento e a pessoa. 🔍
11. Quem tinha assento e ficou fora do mapa gravado volta a não atendido. 💻
12. O sistema não guarda quem montou o mapa nem quando cada assento foi atribuído. 💻

---

## Cenários

```gherkin
Feature: Atribuir assento ao participante

  Background:
    Given que o usuário está autenticado no GPE
    And está no mapa de assentos de um evento, na versão do Administrador

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Atribuir arrastando a pessoa da lista para um assento vazio
    Given que "Maria Souza" está na lista "Pessoas Disponíveis" e o assento "B12" está vazio
    When o usuário arrasta o cartão de "Maria Souza" e o solta sobre o assento "B12"
    Then o assento "B12" passa a mostrar "Maria Souza" e a organização dela, na cor da legenda
    And "Maria Souza" sai da lista "Pessoas Disponíveis"
    And o botão passa de "Salvar Alocações (0)" para "Salvar Alocações (1)"
    And a gravação automática fica marcada para 30 segundos depois

  Scenario: Atribuir escolhendo a pessoa na janela Selecionar Pessoa
    Given que o assento "F8" está vazio
    When o usuário clica no assento "F8"
    And escolhe "João Lima" na janela "Selecionar Pessoa"
    Then a janela se fecha e o assento "F8" passa a mostrar "João Lima"
    And "João Lima" sai da lista "Pessoas Disponíveis"

  Scenario: Mudar o participante de assento
    Given que "Maria Souza" ocupa o assento "B12" e o assento "C3" está vazio
    When o usuário arrasta "Maria Souza" do assento "B12" e a solta sobre o assento "C3"
    Then o assento "C3" passa a mostrar "Maria Souza" e o assento "B12" fica vazio

  Scenario: Gravação automática do mapa
    Given que o usuário atribuiu um assento e não fez outra alteração
    When se passam 30 segundos
    Then o sistema mostra "Salvando composição automaticamente..." e envia o mapa inteiro para gravação
    And exibe: "Salvo" com o detalhe "Composição salva automaticamente"

  Scenario: Várias alterações em sequência geram uma só gravação
    Given que o usuário atribuiu um assento há 20 segundos
    When ele atribui outro assento
    Then a contagem de 30 segundos recomeça, e as duas atribuições são gravadas juntas

  Scenario: Gravar o mapa na hora
    Given que há três participantes sentados no mapa
    When o usuário aciona "Salvar Alocações (3)"
    Then o sistema cancela a gravação automática que estava marcada e envia o mapa inteiro para gravação
    And exibe: "Sucesso" com o detalhe "Composições da mesa salvas com sucesso! 3 pessoas foram alocadas."

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Mapa sem ninguém sentado
    Given que nenhum participante está sentado
    When o usuário olha o painel "Gerenciar Pessoas Alocadas na Mesa"
    Then o botão "Salvar Alocações (0)" está desabilitado
    # 💻 o código prevê o aviso "Não há pessoas alocadas na mesa para salvar.", que o botão desabilitado impede de aparecer

  Scenario: Pessoa da lista que já está sentada
    Given que a pessoa arrastada da lista "Pessoas Disponíveis" já consta como sentada
    When o usuário a solta sobre um assento
    Then o sistema ignora a operação e o mapa fica como estava

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Assento de destino ocupado
    Given que "Pedro Alves" ocupa o assento "A1" e "Maria Souza" está na lista "Pessoas Disponíveis"
    When o usuário solta "Maria Souza" sobre o assento "A1"
    Then o assento "A1" passa a mostrar "Maria Souza"
    And "Pedro Alves" perde o assento e volta para a lista "Pessoas Disponíveis"
    # ⚠️ não há troca de lugares nem pedido de confirmação; GPE005 não diz o que acontece com o ocupante 📄

  Scenario: Assento que não existe no evento
    Given que o mapa enviado para gravação traz um assento que não está entre os assentos do evento
    When o usuário aciona "Salvar Alocações (n)"
    Then o servidor recusa a gravação inteira e o mapa gravado antes permanece
    And o sistema exibe: "Erro" com o detalhe "Erro ao salvar composições da mesa. Verifique o console para mais detalhes."
    # ⚠️ o motivo informado pelo servidor ("Cadeira não encontrada: " e a identificação) não chega ao usuário, e a mensagem o manda a um recurso técnico do navegador 💻

  Scenario: Mudança de outro usuário chega antes da gravação
    Given que o usuário atribuiu um assento e a gravação automática ainda não aconteceu
    When a recepção registra o check-in de um participante
    Then a atualização automática refaz o mapa com o que está gravado no servidor
    And a atribuição ainda não gravada some da tela, sem aviso
    # ⚠️ 🔍 suspeita de defeito, lida no código e não executada: em dia de evento, com check-ins seguidos, o trabalho de até 30 segundos pode ser descartado

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Atribuir Assento ao Participante" na matriz do N2
    When o usuário abre o mapa de assentos
    Then os assentos não aceitam arraste nem clique, os cartões da lista não podem ser arrastados e não há o botão "Salvar Alocações (n)"
    # ⚠️ quem não chega ao mapa nem vê a opção; ver a nota da matriz no N2 sobre o que o servidor confere

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Mapa carregando ou gravando
    Given que o mapa está sendo carregado ou gravado
    When o usuário tenta arrastar, soltar ou clicar em um assento
    Then o sistema ignora a operação até o carregamento ou a gravação terminar

  Scenario: Falha na gravação automática
    Given que a gravação automática falha
    When o sistema tenta gravar o mapa
    Then exibe: "Erro ao Salvar" com o detalhe "Erro ao salvar composição automaticamente. Suas alterações podem não ter sido salvas."
    And as alterações continuam na tela, sem nova tentativa automática até a próxima alteração

  Scenario: Sair do mapa antes da gravação
    Given que o usuário atribuiu um assento há menos de 30 segundos
    When ele passa para a visão "Participantes" ou fecha a tela
    Then a gravação automática que estava marcada é cancelada, sem aviso
    # ⚠️ 🔍 lido no código, não executado: ao voltar ao mapa na mesma sessão a atribuição reaparece, mas só é gravada na próxima alteração ou pelo botão; fechada a tela, perde-se

  Scenario: Clique em assento ocupado da mesa principal
    Given que "Pedro Alves" ocupa o assento "A1", da mesa principal
    When o usuário clica no assento "A1" e fecha a janela "Selecionar Pessoa" sem escolher ninguém
    Then "Pedro Alves" continua no assento "A1" e passa a aparecer também na lista "Pessoas Disponíveis"
    # ⚠️ 🔍 suspeita de defeito, lida no código: nos setores A, B, C e D a janela abre mesmo com o assento ocupado; nos setores E, F, G e H o clique em assento ocupado não faz nada

  Scenario: Administrador no tablet
    Given que o usuário está em um tablet
    When ele atribui um assento
    Then a tela não mostra o painel "Gerenciar Pessoas Alocadas na Mesa", e a atribuição só é gravada pela gravação automática
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| Pessoa (cartão da lista "Pessoas Disponíveis", ocupante de outro assento ou opção da janela "Selecionar Pessoa") | EventoPessoa | entrada do usuário | editável | seleção → EventoPessoa | sim | Participante do mapa; na janela e na lista, só quem ainda não tem assento |
| Assento (posição do mapa onde a pessoa é solta, ou em que se clica) | CadeiraMesa | entrada do usuário | editável | seleção → CadeiraMesa | sim | Assento existente entre os assentos do evento |
| "Digite o nome para filtrar..." (campo da janela "Selecionar Pessoa", sem rótulo) | Pessoa | entrada do usuário | editável | texto | não | Filtra as opções enquanto se digita, por nome, codinome, cargo, razão social, nome fantasia ou legenda, sem diferenciar maiúsculas nem acentos |

*Cada opção da janela "Selecionar Pessoa" mostra o nome da pessoa (o codinome, quando há), o número de participações anteriores entre parênteses, a organização e a etiqueta "Check in realizado" ou "Check in não identificado". 💻 ⚠️ A opção repete a organização em duas linhas — nome fantasia e razão social — e não mostra o cargo nem a legenda.*

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| Assento | O assento em que o participante está no mapa | A cada gravação do mapa, para cada participante sentado |
| Convidado, Confirmado e Check-In | O valor que o mapa do Administrador tinha no momento ⚠️ | A cada gravação do mapa, para cada participante sentado (regra 9) |
| Atendido | Para quem continua sentado, o valor que o mapa do Administrador tinha; para quem perdeu o assento, não ⚠️ | A cada gravação do mapa (regras 9 e 11) |
| Data e hora do check-in | Vazio ⚠️ 🔍 | A cada gravação do mapa, para cada participante sentado (regra 10) |
| Dados vindos do CRM | Vazios ⚠️ 🔍 | A cada gravação do mapa, para cada participante sentado (regra 10) |

---

## Dados lidos e gravados

| Entidade | Papel | Por que a feature a toca |
|---|---|---|
| Evento | lê | A gravação localiza os assentos e as atribuições pelo evento do mapa (regras 4 e 7) |

---

## Comportamento de tela

### Onde fica
No mapa de assentos do Administrador. Os cartões da lista "Pessoas Disponíveis" podem ser arrastados; cada assento aceita que se solte uma pessoa sobre ele, e o ocupante de um assento também pode ser arrastado para outro. Clicar em um assento abre a janela "Selecionar Pessoa", com o campo "Digite o nome para filtrar...", a lista das pessoas disponíveis e o botão "×" para fechar; clicar fora da janela também a fecha. 💻 ⚠️ O campo de filtro da janela e o campo "Buscar pessoa..." da lista lateral são o mesmo: o que se digita em um vale para o outro, e fechar a janela apaga o filtro dos dois.

A gravação fica no painel "Gerenciar Pessoas Alocadas na Mesa", acima do mapa, com o botão "Salvar Alocações (n)", em que n é o número de participantes sentados. O botão fica desabilitado quando não há ninguém sentado e enquanto o mapa carrega ou grava. Durante a gravação automática aparece o texto "Salvando composição automaticamente..." e a tela fica bloqueada, com o indicador "Carregando dados da mesa...". No tablet o painel não é mostrado. 💻

A atribuição aparece no mapa na hora, antes da gravação: nada na tela distingue o assento já gravado do que ainda aguarda gravação. ⚠️

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Durante a gravação, tela esmaecida com "Carregando dados da mesa..."; na gravação automática, também "Salvando composição automaticamente..." no painel. Arraste, clique e botões ficam sem efeito |
| Erro de validação | Não há mensagem: sem ninguém sentado, o botão "Salvar Alocações (0)" fica desabilitado; soltar sobre um assento uma pessoa que já está sentada não faz nada |
| Erro de servidor | Na gravação pelo botão: "Erro" com o detalhe "Erro ao salvar composições da mesa. Verifique o console para mais detalhes." ⚠️. Na gravação automática: "Erro ao Salvar" com o detalhe "Erro ao salvar composição automaticamente. Suas alterações podem não ter sido salvas." |
| Sucesso | Na gravação pelo botão: "Sucesso" com o detalhe "Composições da mesa salvas com sucesso! {n} pessoas foram alocadas.". Na gravação automática: "Salvo" com o detalhe "Composição salva automaticamente" |
| Empty state | Janela "Selecionar Pessoa" sem pessoa disponível ou sem pessoa que case com o filtro: a lista fica vazia, sem texto de aviso |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Depois da gravação, o participante aparece no assento atribuído para qualquer usuário que abra o mapa do evento, e não consta mais entre as pessoas disponíveis do Administrador | Regra 4 · cenários "Atribuir arrastando a pessoa da lista para um assento vazio" e "Gravar o mapa na hora" |
| SC-02 | Nenhuma atribuição deixa um participante em dois assentos nem um assento com dois ocupantes | Regras 2 e 3 · cenários "Mudar o participante de assento" e "Assento de destino ocupado" |
| SC-03 | Com o mapa aberto e pelo menos um participante sentado, toda alteração é gravada sem ação do usuário 30 segundos depois da última mudança | Regras 5 e 6 · cenário "Gravação automática do mapa" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Atribuir Assento ao Participante | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade EventoPessoa

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Arraste, clique no assento e janela "Selecionar Pessoa" | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/components/mesa/components/retangular/retangular.component.ts` (linhas 436–555, 686–744, 978–986, 1019–1031) e `.html` (linhas 24–42, 388–417); o formato invertido repete o código em `../retangular-invertido/retangular-invertido.component.ts` | — |
| Gravação pelo botão e gravação automática | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/components/mesa/components/retangular/retangular.component.ts` (linhas 69, 126–132, 1421–1463, 1497–1556) e `.html` (linhas 81–99) | — |
| Serviço `salvarComposicoesMesa` | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento/services/evento.service.ts` (linhas 68–71) | — |
| Descarte do mapa na atualização automática | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/evento-pessoa.component.ts` (linhas 123–140, 218–235) e `components/mesa/components/retangular/retangular.component.ts` (linhas 82–91, 228–240) | — |
| Operação `POST /administracao/eventos/{eventoId}/composicoes-mesa` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoController.java` (linhas 172–183) | — |
| Substituição do mapa inteiro e regravação da participação | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/EventoServiceImpl.java` (linhas 221–312, 413–422) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

Resposta do servidor quando a gravação falha: HTTP 400 com o texto `Erro ao salvar composições: Erro ao salvar composições da mesa: Cadeira não encontrada: <identificação>`. A tela não lê esse texto.

O atraso da gravação automática é a constante `DEBOUNCE_DELAY = 30000`, com o comentário `// 5 segundos de delay`. O método `salvarComposicaoAutomatica`, que gravaria uma só pessoa, não tem chamador.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE005 – Gerenciar Participante (funcionalidade "Marcar Assento do Participante") e do código |

---

*Feature Set: Participantes · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
