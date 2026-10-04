<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: PES-CAD-04
feature_set: PES-CAD
dominio: PES
entidade: Pessoa
data_model_ref: data-models/pessoas.md#pessoa
endpoints: []
error_codes: []
depende_de: ["PES-CAD-01"]
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

# Excluir Pessoa
> **Nível 3** - Feature Set: Cadastro de Pessoas — Major Feature Set: Pessoas - `PES-CAD-04`

## Descrição

Permite que o Administrador exclua do cadastro uma pessoa que não participa de nenhum evento; a pessoa deixa de existir no sistema, junto com seus grupos de trabalho, temas e histórico de participação.

A exclusão é acionada pela opção Remover Pessoa, em cada linha da lista de pessoas. O sistema pede confirmação e, confirmada, retira a pessoa e atualiza a lista.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE003 – Manter Pessoa v1.0, de 03/10/2025 (documento legado), funcionalidade "Excluir Pessoa" ⚠️ sem chave na ferramenta de demandas | Criação | — Excluir uma pessoa a partir da pesquisa, deixando de exibi-la no sistema. O bloqueio por vínculo com evento não está no documento: vem do código 💻 |

---

<div class="dev-only">

## Superfície

**Ação em tela** — origem: Pesquisar Pessoas `PES-CAD-01` (`/administracao-pessoas`), ícone de lixeira em cada linha da lista

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Pesquisar Pessoas" de GPE003

---

</div>

## Regras de negócio

1. A pessoa que participa de algum evento não é excluída, qualquer que seja a situação dela nesse evento. 💻 → ver RULES-DICTIONARY: RC-09 — Registro vinculado não pode ser excluído (parâmetro: entidade vinculada = participação em evento)
2. A exclusão da pessoa é definitiva: o registro é apagado, não apenas ocultado. 💻 ⚠️ GPE003 diz que "o registro da pessoa passa a não ser exibido no sistema" 📄, redação que cabe tanto à exclusão definitiva quanto à lógica; no evento, a exclusão é lógica. Confirmar com o PO qual é a intenção.
3. Os grupos de trabalho, os temas e o histórico de participação da pessoa são excluídos junto com ela. 💻
4. A foto da pessoa excluída continua guardada. 💻 ⚠️ Parece resíduo, não intenção.

---

## Cenários

```gherkin
Feature: Excluir pessoa

  Background:
    Given que o usuário está autenticado no GPE
    And está na lista de pessoas

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Excluir pessoa sem vínculo com evento
    Given que a pessoa "Maria Souza" não participa de nenhum evento
    When o usuário aciona "Remover Pessoa" na linha de "Maria Souza"
    And confirma a pergunta "Tem certeza que deseja remover a pessoa? Essa operação não poderá ser desfeita."
    Then o sistema exclui a pessoa, com seus grupos de trabalho, temas e histórico
    And exibe: "Pessoa removido com sucesso"
    And a lista é recarregada sem "Maria Souza"
    # ⚠️ o texto exibido é literalmente "Pessoa removido" — erro de concordância na mensagem 💻

  Scenario: Desistir da exclusão
    When o usuário aciona "Remover Pessoa" na linha de uma pessoa
    And não confirma a pergunta
    Then o sistema mantém a pessoa e a lista como estavam

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há dado a validar
    When o usuário aciona "Remover Pessoa"
    Then o sistema pede apenas a confirmação, sem solicitar nenhum dado

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Pessoa vinculada a evento
    Given que a pessoa "João Lima" é participante de pelo menos um evento
    When o usuário aciona "Remover Pessoa" na linha de "João Lima" e confirma
    Then o sistema mantém a pessoa
    And exibe o aviso "Não é possível remover" com o detalhe "Não é possível remover a pessoa, pois ela já possui vínculo com evento."
    # ← RULES-DICTIONARY: RC-09 — Registro vinculado não pode ser excluído

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Excluir Pessoa" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Administração › Pessoas, e a ação não fica ao alcance dele
    # ⚠️ a tela não confere o perfil; ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Falha ao excluir
    Given que a exclusão falha por motivo diferente do vínculo com evento
    When o usuário confirma a exclusão
    Then o sistema mantém a pessoa
    And exibe: "Erro ao remover pessoa" com o detalhe "Contate o administrador do sistema."
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| — | Pessoa | — | — | — | — | A ação não tem campos: opera sobre a pessoa da linha escolhida e pede só a confirmação |

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| — | — | Nenhum campo é gravado: o registro é apagado |

---

## Dados lidos e gravados

| Entidade | Papel | Por que a feature a toca |
|---|---|---|
| EventoPessoa | lê | Verifica se a pessoa participa de algum evento antes de excluir (regra 1) |
| GrupoTrabalhoPessoa | grava | Apagados junto com a pessoa (regra 3) |
| TemaPessoa | grava | Apagados junto com a pessoa (regra 3) |
| HistoricoPessoa | grava | Apagados junto com a pessoa (regra 3) |

---

## Comportamento de tela

### Onde fica
Na tela Pessoas, em cada linha da lista, o ícone de lixeira com a dica "Remover Pessoa", ao lado do ícone de edição. A confirmação é a caixa de pergunta padrão do navegador, com as opções de confirmar e cancelar. 💻 ⚠️ A tela traz também uma caixa de confirmação própria, com o título "Remover Pessoa" e os botões "Remover" e "Cancelar", que não é usada.

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Sem indicador próprio; a lista mostra o indicador de carregamento ao ser recarregada |
| Erro de validação | Não se aplica — não há campos |
| Erro de servidor | Aviso "Não é possível remover", quando a pessoa tem vínculo com evento; nos demais casos, erro "Erro ao remover pessoa" com o detalhe "Contate o administrador do sistema." |
| Sucesso | Mensagem "Sucesso" com o detalhe "Pessoa removido com sucesso" e recarga da lista a partir da primeira página. 🔍 A recarga pede 100 linhas, e não as 10 da paginação: até a próxima pesquisa, a lista pode mostrar até 100 pessoas numa página só |
| Empty state | Não se aplica — a ação só existe em linha da lista |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Uma pessoa sem vínculo com evento, depois de excluída, não é mais encontrada pela pesquisa de pessoas | Cenário "Excluir pessoa sem vínculo com evento" |
| SC-02 | Nenhuma pessoa vinculada a evento é excluída, e a tentativa informa o motivo | Regra 1 · cenário "Pessoa vinculada a evento" |
| SC-03 | Nenhuma exclusão acontece sem a confirmação do usuário | Cenário "Desistir da exclusão" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Excluir Pessoa | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade Pessoa

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Ação Remover Pessoa e mensagens | sistema_mesa_checkin_frontend | `src/app/admin/administracao/acessibilidade/pessoas/pages/pessoas/components/pessoas-list/pessoas-list.component.ts` (linhas 129–173) e `.html` (linhas 66–71) | — |
| Operação `DELETE /administracao/pessoas/{id}` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/PessoaController.java` (linhas 96–107) | — |
| Verificação de vínculo e exclusão | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/PessoaServiceImpl.java` (linhas 148–159) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

Resposta do servidor quando há vínculo: código `PESSOA_COM_VINCULO_EVENTO` → ver ERROR-DICTIONARY: `PESSOA_COM_VINCULO_EVENTO`

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE003 – Manter Pessoa (funcionalidade "Excluir Pessoa") e do código |

---

*Feature Set: Cadastro de Pessoas · Major Feature Set: Pessoas · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
