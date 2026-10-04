<!-- docqui: 4.0.2 | prompt: analise-impacto | atualizado: 2026-10-04 -->
---
tipo: sprint
sprint: SP005
entrega: ""
estado: rascunho
---

# AIM SP005

## Sumário

| Indicador | Valor |
|---|---|
| Tickets | 2 |
| Features alcançadas | 17 |
| Features incluídas | 9 |
| Features alteradas | 8 |
| Processos elementares | 20 |
| Funções de dados | 3 |
| PFB | 102 |
| PFL | 74,5 |

## Tickets da sprint

| Ticket | AIM | Features | Resumo |
|---|---|---|---|
| `PDTIC25148-34` | [AIM-PDTIC25148-34](AIM-PDTIC25148-34.md) | `EVT-LEG-01` **Consultar Configuração de Legendas** · `EVT-LEG-02` **Adicionar Bloco de Legenda ao Evento** · `EVT-LEG-03` **Configurar Condições de Legenda** · `EVT-LEG-04` **Reordenar Blocos de Legenda** · `EVT-LEG-05` **Remover Bloco de Legenda do Evento** · `EVT-LEG-06` **Simular Aplicação de Legendas** · `EVT-LEG-07` **Gerar Legendas do Evento** · `EVT-LEG-08` **Salvar Preset de Legendas** · `EVT-LEG-09` **Carregar Configuração de Legendas** · `EVT-LEG-10` **Excluir Preset de Legendas** · `EVT-LEG-11` **Pesquisar Blocos de Legenda** · `EVT-LEG-12` **Cadastrar Bloco de Legenda** · `EVT-LEG-13` **Editar Bloco de Legenda** · `EVT-LEG-14` **Excluir Bloco de Legenda** · `EVT-PAR-04` **Consultar Legenda do Participante** · `EVT-PAR-05` **Alterar Legenda do Participante** | Configuração de Legendas por Evento: a tela de regras de legenda foi reformulada, com catálogo de blocos comum a todos os eventos, configuração e ordem por evento, presets e legenda do participante guardada por evento |
| `PDTIC25148-35` | [AIM-PDTIC25148-35](AIM-PDTIC25148-35.md) | `EVT-PAR-01` **Pesquisar Participantes** · `EVT-PAR-04` **Consultar Legenda do Participante** | Melhorias na Listagem de Pessoas Confirmadas: o nome do participante abre o cadastro da pessoa em nova aba, a pesquisa ganhou o critério de pessoas sem foto e "Assento livre" saiu da lista de legendas |

## Premissas

- **Rótulo da sprint.** `SP005` é a sprint que o Jira chama de `SP_SMC_5`. A data da entrega não consta em nenhuma fonte ❓: os dois tickets foram criados em 2026-09-04, estavam em teste em 2026-09-30 e em homologação em 2026-10-04.
- **AIMs abertas na entrega.** Os dois tickets foram entregues antes de terem AIM, então não há estimativa a comparar: o apurável é só a contagem detalhada.
- **Sem baseline anterior.** A primeira contagem do sistema é a de 2026-10-04, feita já com a entrega dentro. Ela dá o tamanho de cada função depois da sprint, que é a base do cálculo da função alterada; o tamanho de antes não consta.
- **O "antes" é o documento legado.** A natureza de cada feature — incluída ou alterada — foi decidida pela existência da funcionalidade em GPE005 – Gerenciar Participante v1.1 e em GPE006 – Gerenciar Regras de Legendas v1.0. É proposta, a confirmar com a equipe de métricas.
- **PFL.** O PFB inteiro na função incluída e a metade na alterada, o fator de impacto de 50% do Guia de Métricas da STI (4.2), que vale para a função desenvolvida ou já mantida pela contratada.
- **Cada função conta uma vez.** A lista de legendas da janela Gerenciar Legenda da Pessoa foi alterada pelos dois tickets — o primeiro trouxe o catálogo e a marca "Configurada neste evento", o segundo tirou "Assento livre" — e entra uma vez só, em `EVT-PAR-04` *Consultar Legenda do Participante*. Por isso a soma das duas AIMs dos tickets, 76 PFB, é maior que as transações desta sprint, 73 PFB.

## Alterações na spec, por Feature Set

### Legendas

| Feature | Ticket | CA-n | Natureza | PFB | PFL |
|---|---|---|---|---|---|
| `EVT-LEG-01` **Consultar Configuração de Legendas** | `PDTIC25148-34` | CA-06, CA-08 | alterada | 4 | 2 |
| `EVT-LEG-02` **Adicionar Bloco de Legenda ao Evento** | `PDTIC25148-34` | CA-01 | alterada | 6 | 3 |
| `EVT-LEG-03` **Configurar Condições de Legenda** | `PDTIC25148-34` | CA-13, CA-14 | alterada | 4 | 2 |
| `EVT-LEG-04` **Reordenar Blocos de Legenda** | `PDTIC25148-34` | CA-07 | incluída | 3 | 3 |
| `EVT-LEG-05` **Remover Bloco de Legenda do Evento** | `PDTIC25148-34` | CA-09 | incluída | 3 | 3 |
| `EVT-LEG-06` **Simular Aplicação de Legendas** | `PDTIC25148-34` | CA-19 | alterada | 5 | 2,5 |
| `EVT-LEG-07` **Gerar Legendas do Evento** | `PDTIC25148-34` | CA-20, CA-21, CA-22, CA-23 | alterada | 4 | 2 |
| `EVT-LEG-08` **Salvar Preset de Legendas** | `PDTIC25148-34` | CA-15 | incluída | 4 | 4 |
| `EVT-LEG-09` **Carregar Configuração de Legendas** | `PDTIC25148-34` | CA-16, CA-18 | incluída | 15 | 15 |
| `EVT-LEG-10` **Excluir Preset de Legendas** | `PDTIC25148-34` | CA-17 | incluída | 3 | 3 |
| `EVT-LEG-11` **Pesquisar Blocos de Legenda** | `PDTIC25148-34` | CA-05 | incluída | 3 | 3 |
| `EVT-LEG-12` **Cadastrar Bloco de Legenda** | `PDTIC25148-34` | CA-02, CA-03, CA-04 | incluída | 3 | 3 |
| `EVT-LEG-13` **Editar Bloco de Legenda** | `PDTIC25148-34` | CA-10 | incluída | 3 | 3 |
| `EVT-LEG-14` **Excluir Bloco de Legenda** | `PDTIC25148-34` | CA-11, CA-12 | incluída | 3 | 3 |

### Participantes

| Feature | Ticket | CA-n | Natureza | PFB | PFL |
|---|---|---|---|---|---|
| `EVT-PAR-01` **Pesquisar Participantes** | `PDTIC25148-35` | CA-02, CA-03 | alterada | 4 | 2 |
| `EVT-PAR-04` **Consultar Legenda do Participante** | `PDTIC25148-34` · `PDTIC25148-35` | CA-01 | alterada | 3 | 1,5 |
| `EVT-PAR-05` **Alterar Legenda do Participante** | `PDTIC25148-34` | — | alterada | 3 | 1,5 |

Em `EVT-PAR-04` o critério `CA-01` é do ticket `PDTIC25148-35`; o `PDTIC25148-34` alcançou a mesma lista sem critério numerado. Em `EVT-PAR-01` e em `EVT-PAR-04` o PFB é menor que o tamanho da feature — 16 PF e 7 PF —, porque a sprint alcançou só um dos processos de cada uma.

### Processos elementares

| Processo elementar | Da feature | Do ticket | Tipo | PFB | Critérios |
|---|---|---|---|---|---|
| Consultar Configuração de Legendas | `EVT-LEG-01` | `PDTIC25148-34` | CE | 4 | `CA-06, CA-08` |
| Adicionar Bloco de Legenda ao Evento | `EVT-LEG-02` | `PDTIC25148-34` | EE | 3 | `CA-01` |
| Consultar Lista de blocos (combo) | `EVT-LEG-02` | `PDTIC25148-34` | CE | 3 | `CA-01` |
| Configurar Condições de Legenda | `EVT-LEG-03` | `PDTIC25148-34` | EE | 4 | `CA-13, CA-14` |
| Reordenar Blocos de Legenda | `EVT-LEG-04` | `PDTIC25148-34` | EE | 3 | `CA-07` |
| Remover Bloco de Legenda do Evento | `EVT-LEG-05` | `PDTIC25148-34` | EE | 3 | `CA-09` |
| Simular Aplicação de Legendas | `EVT-LEG-06` | `PDTIC25148-34` | SE | 5 | `CA-19` |
| Gerar Legendas do Evento | `EVT-LEG-07` | `PDTIC25148-34` | EE | 4 | `CA-20, CA-21, CA-22, CA-23` |
| Salvar Preset de Legendas | `EVT-LEG-08` | `PDTIC25148-34` | EE | 4 | `CA-15` |
| Carregar Configuração de Legendas | `EVT-LEG-09` | `PDTIC25148-34` | EE | 6 | `CA-16, CA-18` |
| Consultar Biblioteca de presets (combo) | `EVT-LEG-09` | `PDTIC25148-34` | SE | 5 | `CA-16` |
| Consultar De outro evento (combo) | `EVT-LEG-09` | `PDTIC25148-34` | SE | 4 | `CA-18` |
| Excluir Preset de Legendas | `EVT-LEG-10` | `PDTIC25148-34` | EE | 3 | `CA-17` |
| Pesquisar Blocos de Legenda | `EVT-LEG-11` | `PDTIC25148-34` | CE | 3 | `CA-05` |
| Cadastrar Bloco de Legenda | `EVT-LEG-12` | `PDTIC25148-34` | EE | 3 | `CA-02, CA-03, CA-04` |
| Editar Bloco de Legenda | `EVT-LEG-13` | `PDTIC25148-34` | EE | 3 | `CA-10` |
| Excluir Bloco de Legenda | `EVT-LEG-14` | `PDTIC25148-34` | EE | 3 | `CA-11, CA-12` |
| Pesquisar Participantes | `EVT-PAR-01` | `PDTIC25148-35` | CE | 4 | `CA-02, CA-03` |
| Consultar Selecione uma Legenda (combo) | `EVT-PAR-04` | `PDTIC25148-35` | CE | 3 | `CA-01` |
| Alterar Legenda do Participante | `EVT-PAR-05` | `PDTIC25148-34` | EE | 3 | — |

## Funções de dados alteradas

| Função de dados | Natureza da função | PFB | PFL |
|---|---|---|---|
| Evento | alterada | 15 | 7,5 |
| Legenda | alterada | 7 | 3,5 |
| PresetLegenda | incluída | 7 | 7 |

As três vêm do ticket `PDTIC25148-34`; o `PDTIC25148-35` não mexeu em dados. Evento é alterado porque a configuração de legendas do evento e a legenda do participante entraram nele como registros lógicos; Legenda, porque o bloco do catálogo perdeu o número e a composição de mesa; PresetLegenda é arquivo novo.

## Apurável da sprint

| | PFB | PFL |
|---|---|---|
| Transações | 73 | 56,5 |
| Funções de dados | 29 | 18 |
| **Total** | **102** | **74,5** |

Dos 102 PFB, 47 são de funções incluídas — 40 de transações e 7 de dados — e 55 de funções alteradas — 33 de transações e 22 de dados.

## Decisões de produto pendentes

- **Aval das AIMs dos tickets.** As AIMs de `PDTIC25148-34` e de `PDTIC25148-35` estão em `em-análise`, sem o aval do PO, e esta AIM fica em `rascunho` enquanto elas não concluírem. **Trava** o fechamento da sprint e o uso destes números como apuração final.
- **Data de entrega.** Não consta em nenhuma fonte ❓. **Trava** o preenchimento de `entrega:` e o fechamento desta AIM.
- **Um arquivo lógico Evento, com seis registros.** A contagem agrupou o participante, a configuração de legendas e a legenda do participante no arquivo lógico do evento, que fica com complexidade Alta. Se a equipe de métricas ler o participante ou a configuração como arquivo lógico próprio, mudam o tamanho das funções de dados e o número de arquivos referenciados de quase todas as transações. **Trava** os 29 PFB de dados e, em cascata, as transações.
- **Natureza das features.** Nove incluídas e oito alteradas é proposta, pela existência da funcionalidade no documento legado. `EVT-LEG-02` *Adicionar Bloco de Legenda ao Evento* e `EVT-LEG-05` *Remover Bloco de Legenda do Evento* admitem as duas leituras. **Trava** o PFL: cada ponto de função que muda de alterada para incluída vale meio ponto a mais.
- **Fator de impacto.** O PFL usa 50%, o da função desenvolvida ou já mantida pela contratada. O Guia de Métricas da STI (4.2) prevê 75% quando a contratada não desenvolveu a função, e 90% quando além disso há redocumentação. Quem desenvolveu as funções alteradas não consta ❓. **Trava** o PFL dos 55 PFB alterados: a 75%, seriam 41,25 em vez de 27,5.
- **"Resetar Regras" deixou de existir.** A funcionalidade está em GPE006 e não está no sistema entregue. Se foi retirada nesta sprint, é função excluída, que o Guia mede a 30% do tamanho — e não há tamanho, porque ela não tem N3. **Trava** a parcela de funções excluídas do apurável, que hoje é zero.
- **Alcance sobre outras features de Participantes.** Seis features que leem a legenda do participante ficaram fora: `EVT-PAR-01` *Pesquisar Participantes*, no que toca à legenda, `EVT-PAR-06` *Remover Legenda do Participante*, `EVT-PAR-07` *Consultar Mapa de Assentos*, `EVT-PAR-12` *Buscar Pessoa na Mesa*, `EVT-PAR-14` *Exportar Participantes* e `EVT-PAR-15` *Exportar Mapa de Assentos*. Confirmar com o time de desenvolvimento quais o ticket `PDTIC25148-34` alterou. **Trava** a completude do apurável: cada uma que entrar soma metade do seu tamanho, e nenhuma das cinco últimas foi contada ainda.
- **Decisões de produto dos tickets.** As divergências entre o que os tickets pedem e o que foi entregue — a composição de mesa do bloco, a exclusão de bloco que apaga legendas manuais, a legenda única por participante, o filtro sem foto restrito aos confirmados — estão nas AIMs dos tickets. **Trava** a contagem só se a decisão mudar o sistema: aí as features atingidas são recontadas.

## Changelog

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-10-04 | Claude (analise-impacto) | AIM da sprint | consolidação dos tickets `PDTIC25148-34` e `PDTIC25148-35` na `SP005`: 17 features, 20 processos elementares e 3 funções de dados, com a contagem detalhada de 2026-10-04 — 102 PFB e 74,5 PFL. Fica em `rascunho`: as AIMs dos tickets ainda não têm o aval do PO e a data de entrega não consta |
