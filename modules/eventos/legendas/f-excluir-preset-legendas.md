<!-- docqui: 4.0.2 | prompt: PROMPT_CONTAGEM | atualizado: 2026-10-04 -->
---
id: EVT-LEG-10
feature_set: EVT-LEG
dominio: EVT
entidade: PresetLegenda
data_model_ref: data-models/eventos.md#presetlegenda
endpoints: []
error_codes: []
depende_de: ["EVT-LEG-08", "EVT-LEG-09"]
origem:
  tipo: "issue"
  chave: "PDTIC25148-34"
estado: rascunho
gates:
  requisitos:   { aprovado: false, por: "", em: "", pr: "" }
  modelo-dados: { aprovado: false, por: "", em: "", pr: "" }
  testes:       { aprovado: false, por: "", em: "", pr: "" }
  codigo:       { aprovado: false, por: "", em: "", pr: "" }
contagem:
  pendente: false
  revisada_em: "2026-10-04"
  revisada_ate: "PDTIC25148-34"
---

# Excluir Preset de Legendas
> **Nível 3** - Feature Set: Legendas — Major Feature Set: Eventos - `EVT-LEG-10`

## Descrição

Permite que o Administrador exclua da biblioteca um preset de legendas que não serve mais; o preset deixa de ser oferecido para aplicação, e os eventos em que ele já foi aplicado continuam com a configuração que têm.

Na janela Carregar configuração, aba Biblioteca de presets, cada preset tem o botão Excluir preset. O sistema pede confirmação e, confirmada, retira o preset e atualiza a lista.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| [`PDTIC25148-34`](../../../analise-impacto/AIM-PDTIC25148-34.md) | Criação | `CA-17` — retirar um preset da biblioteca sem alterar os eventos em que ele já foi aplicado. Especificada a partir do código-fonte (engenharia reversa de 2026-09-30); a funcionalidade não consta nos documentos legados ⚠️. A confirmação antes de excluir não está no ticket: vem do código 💻 |
<!-- trace-verified: PDTIC25148-34 @ f6bae69fe29f -->

---

<div class="dev-only">

## Superfície

**Ação em tela** — origem: Carregar Configuração de Legendas `EVT-LEG-09` (janela "Carregar configuração", aberta sobre `/regras-legenda/:eventoId`), botão "Excluir preset" no cartão de cada preset da aba "Biblioteca de presets"

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada, ainda em teste — os documentos legados não trazem imagem dela

---

</div>

## Regras de negócio

1. A exclusão do preset é definitiva: o preset é apagado da biblioteca e não há como recuperá-lo. 💻
2. Excluir o preset não altera nenhum evento: a configuração montada a partir dele continua como está, porque o evento guarda cópia própria dos blocos e das condições. 💻
3. Excluir o preset não altera o catálogo de blocos nem as legendas dos participantes. 💻
4. Qualquer preset pode ser excluído: nenhuma condição impede a exclusão, nem o fato de ele já ter sido aplicado. 💻
5. O preset excluído deixa de existir para todos os eventos, não só para aquele de onde a exclusão foi acionada. 💻

---

## Cenários

```gherkin
Feature: Excluir preset de legendas

  Background:
    Given que o usuário está autenticado no GPE
    And está na janela "Carregar configuração", na aba "Biblioteca de presets"

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Excluir um preset
    Given que a biblioteca tem o preset "Reuniões da MEI"
    When o usuário aciona "Excluir preset" no cartão de "Reuniões da MEI"
    And confirma, em "Excluir", a pergunta "Excluir o preset 'Reuniões da MEI'? Esta ação não pode ser desfeita."
    Then o sistema exclui o preset
    And exibe: "Preset excluído" com o detalhe "O preset 'Reuniões da MEI' foi removido."
    And a lista de presets é recarregada sem "Reuniões da MEI", com a janela ainda aberta

  Scenario: Desistir da exclusão
    When o usuário aciona "Excluir preset" no cartão de um preset
    And responde "Cancelar" à pergunta de confirmação
    Then o sistema mantém o preset e a lista como estavam

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há dado a validar
    When o usuário aciona "Excluir preset"
    Then o sistema pede apenas a confirmação, sem solicitar nenhum dado

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Preset já aplicado a eventos
    Given que o preset "Reuniões da MEI" foi aplicado ao evento "Reunião de Março"
    When o usuário exclui o preset
    Then o sistema exclui o preset sem avisar que ele já foi aplicado
    And a configuração de legendas de "Reunião de Março" continua igual

  Scenario: Preset já excluído por outra pessoa
    Given que o preset foi excluído por outra pessoa depois de a janela ser aberta
    When o usuário aciona "Excluir preset" no cartão dele e confirma
    Then o sistema exibe o erro "Erro Interno" com o detalhe "Preset não encontrado."
    # ⚠️ a lista não é recarregada depois do erro: o cartão do preset que não existe mais continua na janela até ela ser reaberta 💻

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Excluir Preset de Legendas" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Eventos › Cadastro, por onde se chega à Configuração de Legendas, e a ação não fica ao alcance dele
    # ⚠️ a tela não confere o perfil; ver a nota da matriz no N2
    # 💻 no servidor, a exclusão de preset está declarada só para o Administrador

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Excluir o último preset da biblioteca
    Given que a biblioteca tem um único preset
    When o usuário o exclui
    Then a aba "Biblioteca de presets" passa a mostrar "Nenhum preset salvo ainda."

  Scenario: Falha inesperada ao excluir
    Given que o servidor falha ao excluir o preset
    When o usuário confirma a exclusão
    Then o sistema mantém o preset
    And exibe o erro "Erro Interno" com o detalhe "Ocorreu um erro inesperado. Contate o suporte."
    # ⚠️ 🔍 quando a resposta de erro vem sem conteúdo, nenhuma mensagem aparece: o tratamento de erro da janela não prevê esse caso
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| — | PresetLegenda | — | — | — | — | A ação não tem campos: opera sobre o preset do cartão escolhido e pede só a confirmação |

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| — | — | Nenhum campo é gravado: o registro é apagado |

---

## Comportamento de tela

### Onde fica
Na janela "Carregar configuração", aberta pelo botão de mesmo nome da tela Configuração de Legendas, a aba "Biblioteca de presets" traz um cartão por preset. Em cada cartão, ao lado de "Aplicar ao evento", fica o botão "Excluir preset", em vermelho e com ícone de lixeira. Ele abre uma caixa de confirmação com o título "Excluir preset", a pergunta "Excluir o preset '{nome}'? Esta ação não pode ser desfeita." e os botões "Excluir" e "Cancelar". 💻

A exclusão não fecha a janela nem mexe na configuração do evento que está aberta por trás dela. Não existe outro lugar de onde excluir preset: o caminho passa sempre pela configuração de legendas de algum evento. 💻

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Sem indicador durante a exclusão; "Carregando presets…" enquanto a lista é recarregada |
| Erro de validação | Não se aplica — não há campos |
| Erro de servidor | Erro "Erro Interno" com o texto enviado pelo servidor no detalhe: "Preset não encontrado." quando o preset já não existe, "Ocorreu um erro inesperado. Contate o suporte." em falha inesperada. A lista não é recarregada depois do erro. ⚠️ A resposta de erro sem conteúdo não produz mensagem alguma 🔍 |
| Sucesso | Mensagem "Preset excluído" com o detalhe "O preset '{nome}' foi removido." e recarga da lista de presets, com a janela aberta |
| Empty state | "Nenhum preset salvo ainda.", quando o preset excluído era o último |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | O preset excluído deixa de aparecer na Biblioteca de presets de todos os eventos | Regras 1 e 5 · cenário "Excluir um preset" |
| SC-02 | A configuração de legendas de um evento em que o preset foi aplicado é a mesma antes e depois da exclusão | Regra 2 · cenário "Preset já aplicado a eventos" |
| SC-03 | Nenhuma exclusão acontece sem a confirmação do usuário | Cenário "Desistir da exclusão" |

---

## Métricas de tamanho

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Excluir Preset de Legendas | principal | EE | 1 | 3 | Baixa | 3 | 2026-10-04 |

### Memória de cálculo

**Excluir Preset de Legendas** — EE · ALR 1 · DER 3 · Baixa · 3 PF

```json
{"pe": "Excluir Preset de Legendas",
 "alr": ["PresetLegenda"],
 "der": ["Preset", "Mensagem", "Ação"]}
```

Por que cada ALR:
1. `PresetLegenda` — apaga o preset da biblioteca

Classificação: EE — a intenção primária é manter o arquivo lógico PresetLegenda, com as formas 6 e 12.

**Total: 3 PF**

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade PresetLegenda

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Botão "Excluir preset", confirmação e mensagens | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/components/carregar-configuracao-dialog/carregar-configuracao-dialog.component.ts` (linhas 151–171) e `.html` (linhas 52–54) | — |
| Serviço de presets | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/services/legenda-catalogo.service.ts` (linhas 75–78) | — |
| Operação `DELETE /administracao/legendas/presets/{id}` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/LegendaController.java` (linhas 82–86) | — |
| Conferência de existência e exclusão | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/PresetLegendaServiceImpl.java` (linhas 115–123) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada e em teste (ticket `PDTIC25148-34`); o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-10-04 | Claude (apf-cpm) | Contagem | Primeira contagem, pelo `PROMPT_CONTAGEM`: 3 PF — Excluir Preset de Legendas (EE Baixa, 3 PF). Confirmada em 2026-10-04 e espelhada em `global/CONTAGEM-PF.md` |
| 2026-10-04 | Claude (analise-impacto) | Origem atualizada | Elo com a AIM do ticket `PDTIC25148-34`, aberta na entrega: o ticket passa a ser a Origem da feature (Criação), com o critério CA-17; regras, campos e cenários inalterados |
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do código e do ticket `PDTIC25148-34` do Jira (critério CA17); a funcionalidade não consta no documento legado GPE006 – Gerenciar Regras de Legendas |

---

*Feature Set: Legendas · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
