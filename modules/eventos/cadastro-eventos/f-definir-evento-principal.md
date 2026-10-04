<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: EVT-CAD-06
feature_set: EVT-CAD
dominio: EVT
entidade: Evento
data_model_ref: data-models/eventos.md#evento
endpoints: []
error_codes: []
depende_de: ["EVT-CAD-01"]
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

# Definir Evento Principal
> **Nível 3** - Feature Set: Cadastro de Eventos — Major Feature Set: Eventos - `EVT-CAD-06`

## Descrição

Permite que o Administrador defina um evento como o principal; ele passa a ser o evento em que a Secretaria Check-In e a Secretaria Mesa trabalham, e o evento que era o principal deixa de sê-lo.

A ação é acionada pelo ícone de bandeira Tornar evento principal, na linha de cada evento que ainda não é o principal. Não pede confirmação nem dado algum: a troca vale assim que o ícone é acionado.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE004 – Manter Evento v1.1, de 16/12/2025 (documento legado), funcionalidade "Tornar Evento como Principal" ⚠️ sem chave na ferramenta de demandas | Criação | — Marcar um evento como principal, retirando a marcação dos demais, de modo que só ele fique disponível para o check-in e a recepção dos convidados durante a realização do evento |

---

<div class="dev-only">

## Superfície

**Ação em tela** — origem: Pesquisar Eventos `EVT-CAD-01` (`/eventos`), ícone de bandeira "Tornar evento principal" em cada linha da lista

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Pesquisar Evento" de GPE004

---

</div>

## Regras de negócio

1. Existe no máximo um evento principal: definir um evento como principal retira essa condição de todos os demais. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 1
2. É sobre o evento principal que a Secretaria Check-In e a Secretaria Mesa trabalham. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 2
3. Qualquer evento pode ser definido como principal, inclusive um evento já finalizado. 💻
4. A troca do evento principal vale de imediato. 💻
5. Não há ação para deixar o sistema sem evento principal: a condição só sai de um evento quando passa a outro. 💻
6. A cada troca, a marcação de principal é reescrita em todos os eventos, um a um, inclusive nos excluídos. 💻 ⚠️ A troca não é indivisível: uma falha no meio dela deixa parte dos eventos com a marcação antiga e parte com a nova 🔍.
7. A troca não confere se o evento escolhido existe ou se está excluído: escolhido um evento excluído ou inexistente, a marcação sai de todos os outros e o sistema fica sem evento principal disponível. 💻 ⚠️ Suspeita de defeito.

---

## Cenários

```gherkin
Feature: Definir evento principal

  Background:
    Given que o usuário está autenticado no GPE
    And está na lista de eventos

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Trocar o evento principal
    Given que "Reunião de Diretoria" é o evento principal e "Comitê de Inovação" não é
    When o usuário aciona "Tornar evento principal" na linha de "Comitê de Inovação"
    Then "Comitê de Inovação" passa a ser o evento principal, e "Reunião de Diretoria" deixa de ser
    And o sistema exibe: "Evento atualizado" com o detalhe "O evento principal foi atualizado com sucesso."
    And a lista é recarregada, com "Sim" na coluna "Principal" de "Comitê de Inovação" e o indicador "Este evento é o principal" no lugar da bandeira

  Scenario: Definir o primeiro evento principal
    Given que nenhum evento é o principal
    When o usuário aciona "Tornar evento principal" na linha de "Reunião de Diretoria"
    Then "Reunião de Diretoria" passa a ser o evento principal

  Scenario: Secretarias passam a trabalhar no novo evento principal
    Given que "Comitê de Inovação" acabou de ser definido como evento principal
    When um usuário da Secretaria Check-In ou da Secretaria Mesa entra no sistema
    Then ele é levado aos participantes de "Comitê de Inovação"

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há dado a validar nem confirmação
    When o usuário aciona "Tornar evento principal"
    Then o sistema faz a troca imediatamente, sem solicitar dado e sem pedir confirmação
    # ⚠️ 💻 um único acionamento muda o evento em que as secretarias trabalham

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Evento que já é o principal
    Given que "Reunião de Diretoria" é o evento principal
    When o sistema lista o evento
    Then no lugar da bandeira aparece o indicador "Este evento é o principal", que não tem ação

  Scenario: Evento excluído por outra pessoa com a lista ainda aberta
    Given que "Comitê de Inovação" foi excluído por outro Administrador, mas ainda aparece na lista aberta
    When o usuário aciona "Tornar evento principal" na linha de "Comitê de Inovação"
    Then o sistema exibe: "Evento atualizado" com o detalhe "O evento principal foi atualizado com sucesso."
    And nenhum evento fica disponível como principal para a Secretaria Check-In e a Secretaria Mesa
    # ⚠️ 🔍 inferido do código (regra 7), sem execução

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Definir Evento Principal" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Eventos › Cadastro, e a ação não fica ao alcance dele
    # ⚠️ o ícone "Tornar evento principal" não confere o perfil; quem recusa a troca é o servidor — ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Falha ao definir o evento principal
    Given que a troca falha no servidor
    When o usuário aciona "Tornar evento principal"
    Then a lista permanece como estava, sem nenhum aviso ao usuário
    # ⚠️ 💻 a tela não trata a falha desta ação; o texto de erro que o servidor devolve é o de outra operação ("Erro ao salvar composições: …") e não chega ao usuário

  Scenario: Lista recarregada depois da troca
    Given que a lista mostrava 10 eventos na página
    When a troca do evento principal é concluída
    Then a lista é recarregada na ordem padrão, com 5 eventos na página
    # ⚠️ 💻 a recarga pede só 5 eventos ao servidor — suspeita de defeito 🔍
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| — | Evento | — | — | — | — | A ação não tem campos nem confirmação: opera sobre o evento da linha escolhida |

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| Principal | Sim no evento escolhido; Não em todos os demais | Ao acionar o ícone |

*O sistema não guarda quando o evento principal foi trocado nem quem o trocou 💻.*

---

## Comportamento de tela

### Onde fica
Na tela Eventos, em cada linha da lista, o ícone de bandeira com a dica "Tornar evento principal", o segundo da coluna "Ações". Ele só aparece no evento que não é o principal; no evento principal, o lugar é ocupado por uma bandeira cheia, com a dica "Este evento é o principal", sem ação. A coluna "Principal" mostra "Sim" ou "Não". 💻 ⚠️ O ícone aparece para qualquer perfil que chegue à tela.

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Sem indicador próprio; a lista mostra o indicador de carregamento ao ser recarregada |
| Erro de validação | Não se aplica — não há campos |
| Erro de servidor | ⚠️ Nenhum aviso: a falha não é tratada, e a lista fica como estava 💻 |
| Sucesso | "Evento atualizado" com o detalhe "O evento principal foi atualizado com sucesso." e recarga da lista na página em que estava, na ordem padrão. ⚠️ A recarga traz 5 eventos por página 💻 |
| Empty state | Não se aplica — a ação só existe em linha da lista |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Depois da ação, um único evento está marcado como principal: o escolhido | Regra 1 · cenário "Trocar o evento principal" |
| SC-02 | A coluna "Principal" e o ícone da linha mostram a troca logo depois da ação | Cenário "Trocar o evento principal" |
| SC-03 | Quem entra pela Secretaria Check-In ou pela Secretaria Mesa depois da troca é levado ao novo evento principal | Regra 2 · cenário "Secretarias passam a trabalhar no novo evento principal" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Definir Evento Principal | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade Evento

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Ícone, mensagem de sucesso e recarga da lista | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento/pages/eventos/components/eventos-list/evento-list.component.ts` (linhas 207–219) e `.html` (linhas 90–93) | — |
| Chamada da operação | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento/services/evento.service.ts` (linhas 83–86) | — |
| Operação `POST /administracao/eventos/{eventoId}/principal` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoController.java` (linhas 217–225) | — |
| Regravação da marcação em todos os eventos | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/EventoServiceImpl.java` (linhas 424–431) | — |
| Consulta do evento principal, que ignora o excluído | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/EventoServiceImpl.java` (linhas 433–437) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE004 – Manter Evento (funcionalidade "Tornar Evento como Principal" e regra "Tornar Evento Principal") e do código |

---

*Feature Set: Cadastro de Eventos · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
