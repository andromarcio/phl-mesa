<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: EVT-PAR-13
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

# Alterar Confirmação de Presença
> **Nível 3** - Feature Set: Participantes — Major Feature Set: Eventos - `EVT-PAR-13`

## Descrição

Permite que o Administrador altere a confirmação de presença de um participante, retirando a que veio do CRM ou das cargas, ou repondo-a; retirada a confirmação, o participante deixa de constar como confirmado e o assento que ocupava fica livre.

A alteração é feita pelo ícone da coluna Confirmado, em cada linha da lista de participantes. O sistema pergunta antes de gravar, e só grava com a resposta afirmativa.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE005 – Gerenciar Participante v1.1, de 16/12/2025 (documento legado), funcionalidade "Remover confirmação de presença" ⚠️ sem chave na ferramenta de demandas | Criação | — Remover a confirmação de presença de um participante, originada no CRM, pela opção disponível em cada linha da pesquisa. A funcionalidade entrou na v1.1 do documento, que cita os tickets `PDTIC25148-32`, `PDTIC25148-20` e `PDTIC25148-28` sem dizer qual deles a originou ❓. Repor a confirmação, liberar o assento e desfazer o check-in vêm do código 💻 |

---

<div class="dev-only">

## Superfície

**Ação em tela** — origem: Pesquisar Participantes `EVT-PAR-01` (`/evento-pessoa/:id`), ícone da coluna "Confirmado" em cada linha da lista

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Pesquisar Participantes" de GPE005 (`GPE005-01.png`)

---

</div>

## Regras de negócio

1. A confirmação de presença pode ser alterada nos dois sentidos: retirada de quem está confirmado e reposta a quem não está. 💻 ⚠️ GPE005 só prevê a remoção 📄; o nome da feature, Alterar, segue o código.
2. Retirar a confirmação libera o assento que o participante ocupava. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 6
3. Alterar a confirmação de quem já tinha check-in desfaz o check-in, nos dois sentidos. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 7
4. O check-in desfeito por esta feature perde também a data e a hora. 💻
5. Retirada a confirmação, o participante deixa de constar no mapa de assentos, tanto no assento quanto entre as pessoas disponíveis: o mapa só reúne quem está confirmado ou fez check-in, e a retirada desfaz os dois. 💻
6. A alteração não muda o convite, o atendimento nem a legenda do participante. 💻
7. Qualquer participante pode ser confirmado por aqui, inclusive quem não foi convidado. 💻
8. A alteração vale só no GPE: nada é enviado ao CRM. 💻 ⚠️ Uma nova carga de confirmados ou uma nova importação de inscritos do CRM volta a marcar como confirmado quem teve a confirmação retirada, se a pessoa continuar na relação recebida.
9. Quem alterou a confirmação, e quando, não fica guardado. 💻 ⚠️ O sistema não registra o autor de nenhuma ação.

---

## Cenários

```gherkin
Feature: Alterar confirmação de presença

  Background:
    Given que o usuário está autenticado no GPE
    And está na lista de participantes de um evento

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Retirar a confirmação
    Given que o participante "Carlos Prado" está confirmado, com check-in feito e no assento "B3"
    When o usuário aciona o ícone da coluna "Confirmado" na linha de "Carlos Prado"
    And responde afirmativamente à pergunta "Deseja remover a confirmação do participante Carlos Prado?"
    Then o sistema marca "Carlos Prado" como não confirmado, desfaz o check-in e libera o assento "B3"
    And exibe: "Não confirmação realizada." com o detalhe "A confirmação foi atualizada para não realizada"
    And a linha passa a mostrar o participante sem confirmação, sem check-in e com "Sem assento"

  Scenario: Repor a confirmação
    Given que a participante "Ana Reis" não está confirmada nem tem check-in
    When o usuário aciona o ícone da coluna "Confirmado" na linha de "Ana Reis"
    And responde afirmativamente à pergunta "Deseja confirmar o participante Ana Reis?"
    Then o sistema marca "Ana Reis" como confirmada
    And exibe: "Confirmação realizada." com o detalhe "Confirmação foi realizado com sucesso"
    # ⚠️ o texto exibido é literalmente "Confirmação foi realizado" — erro de concordância na mensagem 💻

  Scenario: Desistir da alteração
    When o usuário aciona o ícone da coluna "Confirmado" na linha de um participante
    And responde negativamente à pergunta
    Then o sistema mantém a confirmação, o check-in e o assento como estavam

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há dado a validar
    When o usuário aciona o ícone da coluna "Confirmado"
    Then o sistema pede apenas a confirmação da pergunta, sem solicitar nenhum dado

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Confirmar participante que já tinha check-in
    Given que a participante "Marina Duarte" foi cadastrada na recepção, com check-in feito e sem confirmação
    When o usuário aciona o ícone da coluna "Confirmado" na linha de "Marina Duarte" e responde afirmativamente
    Then o sistema marca "Marina Duarte" como confirmada e desfaz o check-in dela
    # ⚠️ a linha continua mostrando o check-in como feito até nova pesquisa: a tela só atualiza o check-in quando a confirmação é retirada 💻
    # ⚠️ desfazer o check-in ao confirmar parece defeito; ver a regra 7 do N1

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Alterar Confirmação de Presença" na matriz do N2
    When o usuário vê a lista de participantes
    Then a coluna "Confirmado" mostra só o ícone da situação, com a dica "Sim", "Não" ou "Pendente", sem nenhuma ação

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Participante sem informação de confirmação
    Given que o participante não tem a informação de confirmação
    When o usuário vê a linha dele
    Then a coluna "Confirmado" mostra o ícone de não confirmado, com a dica "Status desconhecido"
    And acionar o ícone leva à pergunta de confirmar o participante

  Scenario: Falha ao alterar
    Given que a gravação falha no servidor
    When o usuário responde afirmativamente à pergunta
    Then o sistema exibe: "Erro ao realizar Confirmação" com o detalhe "Erro ao realizar Confirmação"
    # ⚠️ a linha já mudou antes da resposta e não volta — ao retirar a confirmação, também o check-in e o assento da linha; fica mostrando o que não foi gravado, até nova pesquisa 💻
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| — | EventoPessoa | — | — | — | — | A ação não tem campos: opera sobre o participante da linha escolhida, inverte o valor da confirmação e pede só a resposta à pergunta |

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| Confirmado | O contrário do valor atual: não, ao retirar; sim, ao repor | Ao responder afirmativamente à pergunta |
| Check-In | Não 💻 | Quando o participante tinha check-in feito, em qualquer dos dois sentidos |
| Data e hora do check-in | Apagada 💻 | Quando o participante tinha check-in feito, em qualquer dos dois sentidos |
| Assento | Vazio 💻 | Quando a confirmação é retirada |

---

## Comportamento de tela

### Onde fica
Na lista de participantes do evento, a coluna "Confirmado". Para o Administrador, ela traz em cada linha uma imagem que mostra a situação e funciona como botão, com as dicas "Confirmado", "Não confirmado" e, quando não há informação, "Status desconhecido". Para os demais perfis, a coluna traz só um ícone de leitura, com as dicas "Sim", "Não" e "Pendente" 💻. GPE005 chama a opção de "Confirmação" 📄; a coluna se chama "Confirmado".

Acionar a imagem abre uma caixa de pergunta. Para retirar, a pergunta é "Deseja remover a confirmação do participante {nome}?"; para repor, "Deseja confirmar o participante {nome}?".

⚠️ O texto da caixa não bate com o que a ação pede. A ação pede o título "Remover confirmação" ou "Confirmar participante" e os botões "Sim" e "Não"; a caixa de confirmação da tela, porém, foi montada com o título "Remover Pessoa" e com os botões "Remover" e "Cancelar", os mesmos da remoção de legenda 💻. Pelo modo como esse tipo de caixa costuma funcionar, o título pedido pela ação prevalece e os botões são os da caixa — de modo que, para confirmar um participante, o usuário acionaria "Remover" 🔍. O texto que de fato aparece não foi conferido em execução ❓.

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Sem indicador: a linha muda no instante em que a pergunta é respondida, antes da resposta do servidor |
| Erro de validação | Não se aplica — não há campos |
| Erro de servidor | "Erro ao realizar Confirmação" com o detalhe "Erro ao realizar Confirmação". ⚠️ A linha não volta à situação anterior |
| Sucesso | "Não confirmação realizada." com o detalhe "A confirmação foi atualizada para não realizada", ao retirar; "Confirmação realizada." com o detalhe "Confirmação foi realizado com sucesso", ao repor. A lista não é recarregada |
| Empty state | Não se aplica — a ação só existe em linha da lista |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Depois de retirada a confirmação, o participante aparece como não confirmado e sem assento na pesquisa, e o assento que ele ocupava aparece livre no mapa | Regras 1, 2 e 5 · cenário "Retirar a confirmação" |
| SC-02 | Nenhuma alteração de confirmação é gravada sem a resposta afirmativa à pergunta | Cenário "Desistir da alteração" |
| SC-03 | A confirmação retirada pode ser reposta pela mesma opção | Regra 1 · cenário "Repor a confirmação" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Alterar Confirmação de Presença | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade EventoPessoa

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Imagem da coluna "Confirmado", pergunta e mensagens | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/components/evento-pessoas-list/evento-pessoas-list.component.ts` (linhas 87–88 e 160–240) e `.html` (linhas 2–7 e 94–125) | — |
| Chamada ao servidor | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento/services/evento.service.ts` (linhas 63–66) | — |
| Operação `PUT /administracao/eventos/participante/confirmacao` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoController.java` (linhas 166–170) | — |
| Gravação da confirmação, desfazimento do check-in e liberação do assento | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/EventoPessoaServiceImpl.java` (linhas 421–436) | — |
| Quem entra no mapa de assentos: confirmado ou com check-in | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/repository/impl/EventoPessoaRepositoryImpl.java` (linhas 535–542) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

A tela envia o novo valor da confirmação no atributo que leva o nome do check-in (`statusCheckin`), e o servidor o lê como confirmação. A tela tem ainda o par de mensagens "Confirmação pendente." e "Confirmação foi atualizada para pendente", para uma confirmação sem valor; nenhuma ação da tela chega a ele.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE005 – Gerenciar Participante (funcionalidade "Remover confirmação de presença") e do código |

---

*Feature Set: Participantes · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
