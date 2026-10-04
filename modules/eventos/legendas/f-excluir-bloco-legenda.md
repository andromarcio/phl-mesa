<!-- docqui: 4.0.2 | prompt: PROMPT_CONTAGEM | atualizado: 2026-10-04 -->
---
id: EVT-LEG-14
feature_set: EVT-LEG
dominio: EVT
entidade: Legenda
data_model_ref: data-models/eventos.md#legenda
endpoints: []
error_codes: []
depende_de: ["EVT-LEG-11"]
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

# Excluir Bloco de Legenda
> **Nível 3** - Feature Set: Legendas — Major Feature Set: Eventos - `EVT-LEG-14`

## Descrição

Permite que o Administrador exclua um bloco de legenda do catálogo; o bloco deixa de existir e sai, junto, da configuração de todos os eventos que o usam e das legendas dos participantes que o tinham recebido.

No Catálogo de blocos, o ícone de lixeira de cada linha consulta onde o bloco está em uso e pede confirmação, avisando quando há eventos afetados. Confirmada a exclusão, o bloco é retirado e a lista é atualizada.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| [`PDTIC25148-34`](../../../analise-impacto/AIM-PDTIC25148-34.md) | Criação | `CA-11, CA-12` — excluir um bloco do catálogo, informando antes que ele está em uso e que a exclusão o retira das configurações dos eventos, e só excluindo depois da confirmação; e não oferecer cópia de bloco no catálogo. Especificada a partir do código-fonte (engenharia reversa de 2026-09-30); a funcionalidade não consta nos documentos legados ⚠️. ⚠️ O ticket fala em retirar o bloco das configurações dos eventos; o código apaga também as legendas dos participantes, inclusive as atribuídas manualmente 💻 |
<!-- trace-verified: PDTIC25148-34 @ f6bae69fe29f -->

---

<div class="dev-only">

## Superfície

**Ação em tela** — origem: Pesquisar Blocos de Legenda `EVT-LEG-11` (`/catalogo-legendas`), ícone de lixeira em cada linha da lista

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada, ainda em teste — os documentos legados não trazem imagem dela

---

</div>

## Regras de negócio

1. A exclusão do bloco é definitiva: o bloco é apagado do catálogo e não há como recuperá-lo. 💻
2. O uso do bloco não impede a exclusão: o bloco em uso em eventos, ou já atribuído a participantes, é excluído como qualquer outro. 💻 ⚠️ É o oposto do que vale para a pessoa, que não pode ser excluída enquanto participa de algum evento.
3. Junto com o bloco é excluída a presença dele na configuração de todos os eventos que o usam, com as condições que ele tinha em cada um. 💻
4. Junto com o bloco são excluídas todas as legendas dele atribuídas a participantes, em todos os eventos. 💻
5. A exclusão alcança também as legendas atribuídas manualmente. 💻 ⚠️ Ponto de atenção forte: a legenda manual, que a geração das legendas preserva — → ver [N1 Eventos](../README.md): Regras transversais de negócio: 10 —, é apagada aqui sem ação nenhuma sobre o participante e sem que a pergunta de confirmação diga que há legendas manuais envolvidas. O ticket `PDTIC25148-34` só fala em retirar o bloco das configurações dos eventos. Confirmar com o PO.
6. Em cada evento afetado, os blocos que ficam são renumerados em sequência — 1, 2, 3 —, sem lacuna e na mesma ordem relativa. 💻
7. O participante que exibia a legenda do bloco excluído passa a exibir a próxima legenda que tiver, pela prioridade, ou nenhuma, sem que as legendas sejam geradas de novo. 💻 → ver [N1 Eventos](../README.md): Regras transversais de negócio: 9
8. A exclusão não distingue a situação do evento: alcança também os eventos já realizados e os excluídos. 💻 ⚠️
9. Os presets não são alterados: o preset que continha o bloco continua existindo e passa a ser mostrado e aplicado sem ele — ver Carregar Configuração de Legendas `EVT-LEG-09`. 💻
10. O uso informado antes da exclusão é a presença do bloco na configuração dos eventos; a atribuição do bloco a participantes não conta como uso. 💻 ⚠️ Um bloco fora de todas as configurações, mas atribuído manualmente a participantes, é tratado como sem uso.
11. A exclusão vale pelo que existir no momento em que é confirmada, e não pelo que a consulta de uso mostrou: o servidor não exige a consulta nem confere se o uso mudou. 💻
12. A exclusão é feita por inteiro ou não é feita: se alguma parte falha, nada é alterado. 💻 🔍 Lido do código, que trata a exclusão como uma operação única; não verificado em execução.

---

## Cenários

```gherkin
Feature: Excluir bloco de legenda

  Background:
    Given que o usuário está autenticado no GPE
    And está na tela "Catálogo de blocos"

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Excluir bloco que não está em uso
    Given que o bloco "Imprensa" não está na configuração de nenhum evento
    When o usuário aciona "Excluir bloco" na linha de "Imprensa"
    And confirma, em "Excluir", a pergunta "Excluir o bloco 'Imprensa'?"
    Then o sistema exclui o bloco do catálogo
    And exibe: "Bloco excluído" com o detalhe "O bloco foi excluído com sucesso."
    And a lista é recarregada a partir da primeira página, sem "Imprensa"

  Scenario: Excluir bloco em uso, com o catálogo aberto pelo menu
    Given que o catálogo foi aberto pelo menu
    And que o bloco "Palestrantes" está na configuração dos eventos "Reunião de Março" e "Seminário de Inovação"
    When o usuário aciona "Excluir bloco" na linha de "Palestrantes"
    Then o sistema pergunta: "O bloco 'Palestrantes' está em uso nos eventos: Reunião de Março, Seminário de Inovação. Excluir também o removerá dessas configurações e das legendas dos participantes. Deseja continuar?"
    When o usuário confirma em "Excluir"
    Then o sistema exclui o bloco do catálogo, da configuração dos dois eventos e das legendas dos participantes
    And os blocos que ficaram em cada evento são renumerados em sequência

  Scenario: Excluir bloco em uso em outros eventos, com o catálogo aberto a partir de um evento
    Given que o catálogo foi aberto por "Gerenciar catálogo" na configuração do evento "Reunião de Março"
    And que o bloco "Palestrantes" está na configuração de "Reunião de Março" e de "Seminário de Inovação"
    When o usuário aciona "Excluir bloco" na linha de "Palestrantes"
    Then o sistema pergunta: "O bloco 'Palestrantes' está em uso em outros eventos: Seminário de Inovação. Excluir também o removerá dessas configurações e das legendas dos participantes. Deseja continuar?"
    # ⚠️ a pergunta não cita o evento de onde o usuário veio, embora o bloco saia da configuração dele também 💻

  Scenario: Excluir bloco em uso só no evento de onde o usuário veio
    Given que o catálogo foi aberto por "Gerenciar catálogo" na configuração do evento "Reunião de Março"
    And que o bloco "Anfitrião" está só na configuração de "Reunião de Março"
    When o usuário aciona "Excluir bloco" na linha de "Anfitrião"
    Then o sistema pergunta: "Excluir o bloco 'Anfitrião'? Ele será removido da configuração deste evento e das legendas dos participantes."

  Scenario: Desistir da exclusão
    When o usuário aciona "Excluir bloco" na linha de um bloco
    And responde "Cancelar" à pergunta
    Then o sistema mantém o bloco, as configurações dos eventos e as legendas dos participantes como estavam

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há dado a validar
    When o usuário aciona "Excluir bloco"
    Then o sistema pede apenas a confirmação, sem solicitar nenhum dado

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Bloco com legendas atribuídas manualmente
    Given que o bloco "Anfitrião" foi atribuído manualmente a participantes de um evento
    When o usuário exclui o bloco e confirma
    Then o sistema apaga essas legendas manuais junto com as automáticas
    And os participantes passam a exibir a próxima legenda que tiverem, ou nenhuma
    # ⚠️ a pergunta fala em "legendas dos participantes", sem distinguir as manuais; é a única operação que desfaz legenda manual sem ação sobre o participante 💻

  Scenario: Bloco fora das configurações, mas atribuído manualmente a participantes
    Given que o bloco "Anfitrião" não está na configuração de nenhum evento
    And que ele foi atribuído manualmente a participantes
    When o usuário aciona "Excluir bloco" na linha de "Anfitrião"
    Then o sistema pergunta apenas: "Excluir o bloco 'Anfitrião'?"
    And, confirmada a exclusão, apaga as legendas manuais desses participantes
    # ⚠️ o aviso de uso não aparece, porque a consulta de uso só olha a configuração dos eventos 💻

  Scenario: Bloco em uso em evento excluído
    Given que o bloco está na configuração de um evento que foi excluído
    When o usuário aciona "Excluir bloco" na linha dele
    Then a pergunta lista o evento excluído, pelo nome, entre os eventos em uso
    # ⚠️ a consulta de uso não deixa de fora os eventos excluídos 💻

  Scenario: Uso alterado entre a pergunta e a confirmação
    Given que a pergunta foi montada quando o bloco estava sem uso
    And que outra pessoa adicionou o bloco a um evento antes da confirmação
    When o usuário confirma em "Excluir"
    Then o sistema exclui o bloco e o retira também desse evento, sem novo aviso

  Scenario: Bloco já excluído por outra pessoa
    Given que o bloco foi excluído por outra pessoa depois de a lista ser carregada
    When o usuário aciona "Excluir bloco" na linha dele e confirma a pergunta "Excluir o bloco '{nome}'?"
    Then o sistema exibe o erro "Erro Interno" com o detalhe "Bloco de legenda não encontrado."
    # 💻 a consulta de uso não confere se o bloco existe: responde que ele está sem uso, e a recusa só vem na exclusão

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Excluir Bloco de Legenda" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Administração › Catálogo de legendas, e a ação não fica ao alcance dele
    # ⚠️ a tela não confere o perfil; ver a nota da matriz no N2
    # 💻 no servidor, a exclusão de bloco está declarada só para o Administrador; a consulta de uso, para os três perfis

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Falha ao consultar o uso
    Given que o servidor falha ao informar onde o bloco está em uso
    When o usuário aciona "Excluir bloco"
    Then o sistema não faz a pergunta de confirmação e não exclui nada
    And exibe o erro "Erro Interno" com o detalhe "Ocorreu um erro inesperado. Contate o suporte."

  Scenario: Falha inesperada ao excluir
    Given que o servidor falha no meio da exclusão
    When o usuário confirma em "Excluir"
    Then nada é alterado: o bloco, as configurações dos eventos e as legendas dos participantes continuam como estavam
    And o sistema exibe o erro "Erro Interno" com o detalhe "Ocorreu um erro inesperado. Contate o suporte."
    # 💻 quando a resposta de erro vem sem conteúdo, o texto é "Erro" com o detalhe "Falha de comunicação com o servidor."

  Scenario: Voltar à configuração do evento depois da exclusão
    Given que o catálogo foi aberto a partir da configuração de um evento que usava o bloco excluído
    When o usuário aciona "Voltar"
    Then a configuração do evento aparece sem o bloco e com os demais renumerados
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| — | Legenda | — | — | — | — | A ação não tem campos: opera sobre o bloco da linha escolhida e pede só a confirmação |

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| Nº | Nova posição, em sequência a partir de 1, de cada bloco que fica na configuração dos eventos afetados | Ao excluir o bloco |

O bloco em si não recebe valor nenhum: o registro é apagado. Não há registro de quem excluiu nem de quando 💻.

---

## Dados lidos e gravados

| Entidade | Papel | Por que a feature a toca |
|---|---|---|
| EventoLegenda | lê e grava | Lê em quais eventos o bloco está configurado, para a pergunta de confirmação (regra 10); apaga o bloco dessas configurações (regra 3) e renumera os que ficam (regra 6) |
| EventoLegendaCondicao | grava | As condições do bloco em cada evento são apagadas junto com ele (regra 3) |
| EventoPessoaLegenda | grava | Apaga todas as legendas do bloco atribuídas a participantes, automáticas e manuais (regras 4 e 5) |
| Evento | lê | Fornece o nome dos eventos listados na pergunta de confirmação |

---

## Comportamento de tela

### Onde fica
No Catálogo de blocos, na coluna "Ações" de cada linha, o ícone de lixeira com a dica "Excluir bloco", ao lado do ícone de lápis. Ao ser acionado, o sistema primeiro consulta em quais eventos o bloco está configurado e só então abre a caixa de confirmação, com o título "Excluir bloco", um ícone de alerta e os botões "Excluir" e "Cancelar". 💻

A pergunta muda conforme o uso encontrado e conforme o caminho por onde o catálogo foi aberto. Quando o bloco está na configuração de outros eventos, a pergunta lista os nomes deles, separados por vírgula: "O bloco '{nome}' está em uso em outros eventos: {lista}. Excluir também o removerá dessas configurações e das legendas dos participantes. Deseja continuar?", se o catálogo foi aberto a partir de um evento, ou a mesma frase com "nos eventos" no lugar de "em outros eventos", se foi aberto pelo menu. Quando o bloco está só no evento de onde o usuário veio: "Excluir o bloco '{nome}'? Ele será removido da configuração deste evento e das legendas dos participantes.". Quando não está em nenhuma configuração: "Excluir o bloco '{nome}'?". 💻

⚠️ O evento de onde o usuário veio nunca entra na lista de nomes, mesmo quando o bloco está nele e em outros. A pergunta não informa quantos participantes perderão a legenda nem que há legendas manuais entre elas. Eventos excluídos aparecem na lista como os demais. 💻

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Sem indicador durante a consulta de uso nem durante a exclusão; a lista mostra o indicador de carregamento ao ser recarregada |
| Erro de validação | Não se aplica — não há campos |
| Erro de servidor | Erro "Erro Interno" com o texto enviado pelo servidor no detalhe: "Bloco de legenda não encontrado." quando o bloco já não existe, "Ocorreu um erro inesperado. Contate o suporte." em falha inesperada. Resposta de erro sem conteúdo: "Erro" com o detalhe "Falha de comunicação com o servidor.". Se a falha é na consulta de uso, a pergunta de confirmação não chega a ser feita |
| Sucesso | Mensagem "Bloco excluído" com o detalhe "O bloco foi excluído com sucesso." e recarga da lista a partir da primeira página |
| Empty state | Não se aplica — a ação só existe em linha da lista. Excluído o último bloco, a lista mostra "Nenhum bloco encontrado." |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Depois da exclusão, o bloco não é encontrado no catálogo, não aparece na configuração de nenhum evento e nenhum participante o exibe como legenda | Regras 1, 3 e 4 · cenário "Excluir bloco em uso, com o catálogo aberto pelo menu" |
| SC-02 | Nenhuma exclusão acontece sem a confirmação do usuário, e a pergunta lista os eventos em cuja configuração o bloco está | Regra 10 · cenários "Desistir da exclusão" e "Excluir bloco em uso, com o catálogo aberto pelo menu" |
| SC-03 | Em todo evento afetado, os blocos que ficam têm numeração contínua a partir de 1, na mesma ordem relativa de antes | Regra 6 |
| SC-04 | Se a exclusão falha, o catálogo, as configurações dos eventos e as legendas dos participantes ficam exatamente como estavam | Regra 12 · cenário "Falha inesperada ao excluir" |

---

## Métricas de tamanho

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Excluir Bloco de Legenda | principal | EE | 2 | 4 | Baixa | 3 | 2026-10-04 |

### Memória de cálculo

**Excluir Bloco de Legenda** — EE · ALR 2 · DER 4 · Baixa · 3 PF

```json
{"pe": "Excluir Bloco de Legenda",
 "alr": ["Legenda", "Evento"],
 "der": ["Bloco", "Eventos em uso", "Mensagem", "Ação"],
 "nao_contados": "Nº dos blocos que ficam é recalculado pelo sistema."}
```

Por que cada ALR:
1. `Legenda` — apaga o bloco do catálogo
2. `Evento` — lê em quais eventos o bloco está configurado e o nome deles, apaga o bloco e as condições dessas configurações, renumera os que ficam e apaga as legendas do bloco atribuídas a participantes

Classificação: EE — a intenção primária é manter os arquivos lógicos Legenda e Evento, com as formas 6, 7, 11 e 12. A consulta de uso só alimenta a pergunta de confirmação: não é acionada sozinha nem deixa o negócio em estado consistente, então é passo deste processo, e não um processo à parte.

**Total: 3 PF**

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade Legenda

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Ícone "Excluir bloco", consulta de uso, montagem da pergunta e mensagens | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/pages/catalogo-legendas/catalogo-legendas.component.ts` (linhas 219–269) e `.html` (linhas 2–3 e 67–68) | — |
| Serviço do catálogo: exclusão e consulta de uso | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/services/legenda-catalogo.service.ts` (linhas 40–42 e 55–58) | — |
| Operações `GET /administracao/legendas/{id}/uso` e `DELETE /administracao/legendas/{id}` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/LegendaController.java` (linhas 107–116) | — |
| Consulta de uso | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/LegendaServiceImpl.java` (linhas 131–142) e `repository/EventoLegendaRepository.java` (linhas 27–33) | — |
| Exclusão em cascata e renumeração | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/LegendaServiceImpl.java` (linhas 144–175) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada e em teste (ticket `PDTIC25148-34`); o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

A cascata é feita pelo serviço, na ordem: legendas dos participantes, blocos dos eventos (as condições saem com eles), bloco do catálogo, renumeração. A operação de exclusão não depende da consulta de uso: chamada diretamente, exclui sem aviso.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-10-04 | Claude (apf-cpm) | Contagem | Primeira contagem, pelo `PROMPT_CONTAGEM`: 3 PF — Excluir Bloco de Legenda (EE Baixa, 3 PF). Confirmada em 2026-10-04 e espelhada em `global/CONTAGEM-PF.md` |
| 2026-10-04 | Claude (analise-impacto) | Origem atualizada | Elo com a AIM do ticket `PDTIC25148-34`, aberta na entrega: o ticket passa a ser a Origem da feature (Criação), com os critérios CA-11 e CA-12; regras, campos e cenários inalterados |
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do código e do ticket `PDTIC25148-34` do Jira (critérios CA11 e CA12); a funcionalidade não consta no documento legado GPE006 – Gerenciar Regras de Legendas |

---

*Feature Set: Legendas · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
