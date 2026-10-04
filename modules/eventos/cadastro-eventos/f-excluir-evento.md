<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: EVT-CAD-05
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

# Excluir Evento
> **Nível 3** - Feature Set: Cadastro de Eventos — Major Feature Set: Eventos - `EVT-CAD-05`

## Descrição

Permite que o Administrador exclua um evento; o evento deixa de aparecer na pesquisa de eventos, e os seus dados, com os participantes e os assentos, permanecem guardados.

A exclusão é acionada pelo ícone Excluir evento, em cada linha da lista de eventos. O sistema pede confirmação e, confirmada, retira o evento da lista.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE004 – Manter Evento v1.1, de 16/12/2025 (documento legado), funcionalidade "Excluir Evento" ⚠️ sem chave na ferramenta de demandas | Criação | — Excluir um evento a partir da pesquisa, de forma lógica: o registro e os dados relacionados não são apagados, e o evento deixa de ser exibido |

---

<div class="dev-only">

## Superfície

**Ação em tela** — origem: Pesquisar Eventos `EVT-CAD-01` (`/eventos`), ícone de lixeira em cada linha da lista

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Pesquisar Evento" de GPE004

---

</div>

## Regras de negócio

1. A exclusão do evento é lógica: o evento permanece guardado e deixa de ser exibido. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 3
2. Os dados relacionados ao evento excluído — participantes, check-ins e assentos — são mantidos como estavam.
3. Qualquer evento pode ser excluído, tenha ou não participantes, check-ins registrados ou assentos ocupados: não há verificação de vínculos. 💻
4. O evento principal também pode ser excluído, e a exclusão não passa a condição de principal a outro evento: o sistema fica sem evento principal até que outro seja definido. 💻 ⚠️
5. Não existe operação para restaurar o evento excluído. 💻
6. O evento excluído sai da pesquisa de eventos, mas continua acessível a quem tem o endereço dele, para visualizar, editar e ver os participantes. 💻 ⚠️ GPE004 diz que, após a exclusão, "o evento passa a não ser exibido no sistema" 📄.

---

## Cenários

```gherkin
Feature: Excluir evento

  Background:
    Given que o usuário está autenticado no GPE
    And está na lista de eventos

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Excluir evento
    When o usuário aciona "Excluir evento" na linha de "Reunião de Diretoria"
    And confirma a pergunta "Tem certeza que deseja remover o evento? Essa operação não poderá ser desfeita."
    Then o sistema marca o evento como excluído, mantendo os dados dele
    And exibe: "Sucesso" com o detalhe "Evento removido com sucesso"
    And a lista é recarregada a partir da primeira página, sem "Reunião de Diretoria"

  Scenario: Desistir da exclusão
    When o usuário aciona "Excluir evento" na linha de um evento
    And não confirma a pergunta
    Then o sistema mantém o evento e a lista como estavam

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há dado a validar
    When o usuário aciona "Excluir evento"
    Then o sistema pede apenas a confirmação, sem solicitar nenhum dado

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Evento com participantes
    Given que o evento "Comitê de Inovação" tem participantes, check-ins registrados e assentos ocupados
    When o usuário aciona "Excluir evento" na linha de "Comitê de Inovação" e confirma
    Then o sistema exclui o evento do mesmo modo, sem nenhum aviso sobre os vínculos
    And os participantes, os check-ins e os assentos continuam guardados
    # 💻 não há verificação de vínculos

  Scenario: Excluir o evento principal
    Given que o evento "Reunião de Diretoria" é o evento principal
    When o usuário aciona "Excluir evento" na linha de "Reunião de Diretoria" e confirma
    Then o sistema exclui o evento, sem aviso
    And nenhum evento fica disponível como principal para a Secretaria Check-In e a Secretaria Mesa
    # ⚠️ 💻 a exclusão não confere se o evento é o principal (regra 4)

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Excluir Evento" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Eventos › Cadastro, e a ação não fica ao alcance dele
    # ⚠️ o ícone "Excluir evento" não confere o perfil; quem recusa a exclusão é o servidor — ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Falha ao excluir
    Given que a exclusão falha no servidor
    When o usuário confirma a exclusão
    Then o sistema mantém o evento
    And exibe: "Erro ao remover evento" com o detalhe "Contate o administrador do sistema."

  Scenario: Evento já excluído por outra pessoa
    Given que o evento já foi excluído por outro Administrador, mas ainda aparece na lista aberta
    When o usuário aciona "Excluir evento" e confirma
    Then o sistema responde como numa exclusão normal e exibe: "Sucesso" com o detalhe "Evento removido com sucesso"
    # 💻 o servidor não distingue o evento já excluído, nem o inexistente
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| — | Evento | — | — | — | — | A ação não tem campos: opera sobre o evento da linha escolhida e pede só a confirmação |

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| Excluído | Sim | Ao confirmar a exclusão |

*O sistema não guarda quando o evento foi excluído nem quem o excluiu 💻.*

---

## Comportamento de tela

### Onde fica
Na tela Eventos, em cada linha da lista, o ícone de lixeira com a dica "Excluir evento", o último da coluna "Ações". A confirmação é a caixa de pergunta padrão do navegador, com as opções de confirmar e cancelar. 💻 ⚠️ O ícone aparece para qualquer perfil que chegue à tela.

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Sem indicador próprio; a lista mostra o indicador de carregamento ao ser recarregada |
| Erro de validação | Não se aplica — não há campos |
| Erro de servidor | "Erro ao remover evento" com o detalhe "Contate o administrador do sistema."; o evento permanece na lista |
| Sucesso | "Sucesso" com o detalhe "Evento removido com sucesso" e recarga da lista a partir da primeira página, do evento incluído por último para o mais antigo |
| Empty state | Não se aplica — a ação só existe em linha da lista |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Um evento excluído não é mais encontrado pela pesquisa de eventos | Regra 1 · cenário "Excluir evento" |
| SC-02 | Os participantes, os check-ins e os assentos do evento excluído continuam guardados | Regra 2 · cenário "Evento com participantes" |
| SC-03 | Nenhuma exclusão acontece sem a confirmação do usuário | Cenário "Desistir da exclusão" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Excluir Evento | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade Evento

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Ação Excluir evento, confirmação e mensagens | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento/pages/eventos/components/eventos-list/evento-list.component.ts` (linhas 111–145) e `.html` (linhas 102–103) | — |
| Operação `DELETE /administracao/eventos/{id}` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoController.java` (linhas 104–108) | — |
| Exclusão lógica, sem verificação de vínculos | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/EventoServiceImpl.java` (linhas 180–188) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

Só a pesquisa de eventos, a consulta do evento principal e a lista de eventos de origem para cópia de legendas deixam de fora o evento excluído; a leitura de um evento pelo identificador e as operações sobre os participantes dele não o distinguem.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE004 – Manter Evento (funcionalidade e regra "Excluir Evento") e do código |

---

*Feature Set: Cadastro de Eventos · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
