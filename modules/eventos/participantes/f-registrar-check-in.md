<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: EVT-PAR-03
feature_set: EVT-PAR
dominio: EVT
entidade: EventoPessoa
data_model_ref: data-models/eventos.md#eventopessoa
endpoints: []
error_codes: []
depende_de: ["EVT-PAR-01"]
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

# Registrar Check-in
> **Nível 3** - Feature Set: Participantes — Major Feature Set: Eventos - `EVT-PAR-03`

## Descrição

Permite que a recepção do evento registre a chegada de um participante, marcando o check-in na lista; ele passa a constar como presente e entra na fila de atendimento da secretaria de mesa. A mesma ação desfaz um check-in marcado por engano.

O check-in é marcado e desmarcado pelo ícone da coluna Check-In, em cada linha da lista de participantes. Um toque basta: o sistema não pede confirmação.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE005 – Gerenciar Participante v1.1, de 16/12/2025 (documento legado), funcionalidade "Realizar Check-in" ⚠️ sem chave na ferramenta de demandas | Criação | — Realizar o check-in de um participante no evento e, acionando a opção de novo, removê-lo; quem fez check-in fica disponível para o atendimento da secretaria de mesa (regra de negócio "Realizar Check-in" do documento). No Jira, o check-in é o ticket `PDTIC25148-14` 🔍 |

---

<div class="dev-only">

## Superfície

**Ação em tela** — origem: Pesquisar Participantes `EVT-PAR-01` (`/evento-pessoa/:id`), ícone da coluna "Check-In" em cada linha da lista

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Pesquisar Participantes" de GPE005 (`GPE005-01.png`)

---

</div>

## Regras de negócio

1. O check-in de um participante tem dois valores, feito e não feito, e a mesma ação alterna entre eles.
2. Qualquer participante do evento pode receber o check-in: não é preciso estar convidado nem confirmado. 💻 → ver [N1 Eventos](../README.md): Regras transversais de negócio: 4. ❓ GPE005 não diz se o check-in de quem não confirmou deveria ser aceito.
3. Ao marcar o check-in, o sistema guarda a data e a hora em que ele foi feito. 💻
4. Ao desmarcar o check-in, a data e a hora são trocadas pelo momento da desmarcação, em vez de apagadas. 💻 ⚠️ Suspeita de defeito: o participante fica sem check-in e com uma data de check-in.
5. Quem registrou o check-in não fica guardado. 💻 ⚠️ O sistema não registra o autor de nenhuma ação.
6. O participante com check-in feito e ainda não atendido entra na lista de pessoas disponíveis da secretaria de mesa, em ordem de chegada; desmarcado o check-in, ele sai dessa lista. 📄 💻
7. Marcar ou desmarcar o check-in não altera a confirmação, o assento, a legenda nem o atendimento do participante. 💻
8. O check-in também é desfeito, sem passar por esta feature, quando a confirmação do participante é alterada. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 7

---

## Cenários

```gherkin
Feature: Registrar check-in

  Background:
    Given que o usuário está autenticado no GPE
    And está na lista de participantes de um evento

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Marcar o check-in
    Given que o participante "João Lima" está sem check-in
    When o usuário aciona o ícone da coluna "Check-In" na linha de "João Lima"
    Then o sistema registra o check-in, com a data e a hora
    And o ícone da linha passa a indicar check-in feito
    And exibe: "Check-in realizado." com o detalhe "Check-in foi realizado com sucesso"

  Scenario: Desmarcar o check-in
    Given que o participante "João Lima" está com check-in feito
    When o usuário aciona o ícone da coluna "Check-In" na linha de "João Lima"
    Then o sistema desfaz o check-in
    And o ícone da linha volta a indicar check-in não feito
    And exibe: "Check-in não realizado." com o detalhe "Check-in foi atualizado para não realizado"
    # ⚠️ a data e a hora do check-in são regravadas com o momento da desmarcação 💻

  Scenario: Check-in de quem não foi convidado nem confirmou
    Given que a participante "Ana Reis" não está convidada nem confirmada
    When o usuário aciona o ícone da coluna "Check-In" na linha de "Ana Reis"
    Then o sistema registra o check-in normalmente

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há dado a validar
    When o usuário aciona o ícone da coluna "Check-In"
    Then o sistema grava a alteração de imediato, sem solicitar dado nem confirmação

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Não há conflito com dados existentes
    Given que o participante tem ou não convite, confirmação, assento e legenda
    When o usuário aciona o ícone da coluna "Check-In"
    Then o sistema registra o check-in sem conferir nenhuma dessas situações

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Registrar Check-in" na matriz do N2
    When o usuário entra no sistema
    Then a tela de participantes abre direto no mapa de assentos
    And a lista, com a coluna "Check-In", não fica ao alcance dele
    # ⚠️ quem chega à lista encontra o ícone ativo: a coluna não confere o perfil; ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Falha ao registrar
    Given que o registro falha no servidor
    When o usuário aciona o ícone da coluna "Check-In"
    Then o sistema exibe: "Erro ao realizar Check-in" com o detalhe "Erro ao realizar Check-in"
    # ⚠️ o ícone já mudou antes da resposta e não volta: a linha fica mostrando o contrário do que está gravado, até nova pesquisa 💻

  Scenario: Check-in já alterado por outro usuário
    Given que outro usuário marcou o check-in de "João Lima" depois de a lista ser carregada
    And a linha de "João Lima" ainda mostra o check-in como não feito
    When o usuário aciona o ícone da coluna "Check-In" na linha de "João Lima"
    Then o check-in continua feito, e a data e a hora passam a ser as desta segunda ação
    # 🔍 a ação envia o contrário do que a linha mostra, e a lista não se atualiza sozinha; conclusão tirada da leitura do código, sem execução
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| — | EventoPessoa | — | — | — | — | A ação não tem campos: opera sobre o participante da linha escolhida e inverte o valor do check-in |

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| Check-In | Sim, ao marcar; não, ao desmarcar | Ao acionar o ícone |
| Data e hora do check-in | Momento da ação 💻 | Ao marcar e ⚠️ também ao desmarcar |

---

## Comportamento de tela

### Onde fica
Na lista de participantes do evento, a coluna "Check-In" traz, em cada linha, uma imagem que mostra a situação — uma para o check-in feito, outra para o não feito — e que funciona como botão: acioná-la inverte a situação. A imagem está ativa para todo perfil que vê a lista 💻. GPE005 chama a opção de "Realizar check-in" 📄; na tela não há esse texto, só a imagem.

⚠️ As dicas da imagem são "Confirmado", com o check-in feito, e "Não confirmado", sem ele — textos de confirmação, e não de check-in, os mesmos da coluna "Confirmado" 💻.

O registro feito pela Secretaria Check-In segue por uma operação do servidor reservada a esse perfil; a regra aplicada é a mesma 💻.

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Sem indicador: a imagem muda no instante em que é acionada, antes da resposta do servidor |
| Erro de validação | Não se aplica — não há campos |
| Erro de servidor | "Erro ao realizar Check-in" com o detalhe "Erro ao realizar Check-in". ⚠️ A imagem não volta à situação anterior |
| Sucesso | "Check-in realizado." com o detalhe "Check-in foi realizado com sucesso", ao marcar; "Check-in não realizado." com o detalhe "Check-in foi atualizado para não realizado", ao desmarcar. A lista não é recarregada |
| Empty state | Não se aplica — a ação só existe em linha da lista |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Depois de marcado o check-in, o participante aparece com Check-In igual a Sim na pesquisa e na planilha exportada, e entra na lista de pessoas disponíveis da secretaria de mesa | Regras 1 e 6 · cenário "Marcar o check-in" |
| SC-02 | Acionar de novo a mesma opção desfaz o check-in, sem pedido de confirmação | Regra 1 · cenário "Desmarcar o check-in" |
| SC-03 | Toda falha no registro é informada a quem acionou a opção | Cenário "Falha ao registrar" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Registrar Check-in | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade EventoPessoa

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Imagem da coluna "Check-In", mensagens e dicas | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/components/evento-pessoas-list/evento-pessoas-list.component.ts` (linhas 126–158 e 236–240) e `.html` (linhas 127–149) | — |
| Escolha da operação conforme o perfil | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento/services/evento.service.ts` (linhas 55–61) | — |
| Operação `PUT /administracao/eventos/participante/checkin` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoController.java` (linhas 160–164) | — |
| Operação `PUT /secretaria/checkin/participante`, usada pela Secretaria Check-In | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/SecretariaCheckinController.java` (linhas 30–34) | — |
| Gravação do check-in e da data e hora | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/EventoPessoaServiceImpl.java` (linhas 410–419) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

A tela tem ainda o par de mensagens "Check-in pendente." e "Check-in foi atualizado para pendente", para um check-in sem valor; nenhuma ação da tela chega a ele. Quando o participante informado não existe, o servidor não faz nada e responde como sucesso — nenhuma tela retira um participante do evento, de modo que a situação não ocorre pelo uso normal.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE005 – Gerenciar Participante (funcionalidade e regra de negócio "Realizar Check-in") e do código |

---

*Feature Set: Participantes · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
