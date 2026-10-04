<!-- docqui: 4.0.2 | prompt: PROMPT_AIM | atualizado: 2026-10-04 -->
---
tipo: ticket
ticket: PDTIC25148-34
ferramenta: Jira
link: https://sistemaindustria.atlassian.net/browse/PDTIC25148-34
titulo: Configuração de Legendas por Evento
estado: em-análise
aberta-na-entrega: true
sprint: "SP005"
avalizado-por: ""
aberta-em: 2026-10-04
---

# AIM PDTIC25148-34

## Detalhe do item

> Transcrição da descrição do ticket `PDTIC25148-34` no Jira, a partir da exportação de 2026-10-04 guardada em `arquivos/`.

### História do Usuário

**Eu como** usuário responsável pela configuração do evento

**Quero** configurar e aplicar as legendas das pessoas por meio de blocos e regras reutilizáveis

**Para** definir a identificação dos participantes de cada evento de forma flexível, permitindo reaproveitar configurações entre eventos.

### Descrição

A funcionalidade **Configuração de Legendas**, disponível na rota `/regras-legenda/:eventoId`, deverá ser reformulada para permitir que as legendas sejam configuradas especificamente para cada evento.

Atualmente, a funcionalidade utiliza blocos de legenda pré-definidos e a numeração está relacionada à classificação automática. Com a alteração, os blocos poderão ser criados ou reutilizados entre eventos, enquanto sua ordem e suas regras serão definidas no contexto de cada evento.

A legenda atribuída a uma pessoa também deverá passar a ser vinculada ao evento, seguindo a associação **Evento – Pessoa – Legenda**.

A tela deverá permitir:

- visualizar os blocos configurados para o evento;
- adicionar um bloco existente do Catálogo;
- criar um novo bloco;
- remover blocos do evento;
- alterar a ordem dos blocos;
- configurar as condições de aplicação;
- salvar a configuração como preset;
- carregar configurações de outros eventos ou presets existentes;
- simular a aplicação das regras;
- executar a geração das legendas.

Todo bloco adicionado à configuração do evento deverá estar em vigor. Não haverá conceito de bloco ativo ou inativo. Caso um bloco não deva ser considerado na aplicação das regras, ele deverá ser removido da configuração do evento.

### Blocos de Legenda do Evento

Cada evento deverá possuir sua própria configuração de blocos de legenda.

As ações de adicionar, remover ou reordenar um bloco deverão alterar somente a configuração do evento atual.

Cada bloco deverá possuir um número (**Nº**), correspondente à sua posição na configuração do evento:

- o primeiro bloco deverá possuir Nº 1;
- o segundo, Nº 2;
- e assim sucessivamente.

Ao alterar a ordem dos blocos, o sistema deverá recalcular automaticamente a numeração.

A ordem dos blocos também deverá representar a prioridade de aplicação das regras.

A numeração não será uma característica do bloco cadastrado no Catálogo, existindo exclusivamente no contexto da associação entre o bloco e o evento.

### Catálogo de Blocos

Ao adicionar um bloco ao evento, o usuário deverá poder:

- pesquisar e selecionar um bloco já existente no Catálogo; ou
- criar um novo bloco.

Para criação de um bloco, deverão ser informados:

- Nome;
- Cor da legenda;
- Composição de mesa.

Ao pesquisar por um nome que não corresponda a nenhum bloco existente no Catálogo, o sistema deverá disponibilizar a opção:

**Adicionar bloco ""**

Ao selecionar essa opção, o sistema deverá abrir a criação de um novo bloco com o campo **Nome** previamente preenchido com o termo pesquisado.

Ao salvar um novo bloco, ele deverá ser incluído no Catálogo e ficar disponível para utilização em outros eventos.

O Catálogo representa uma biblioteca compartilhada de blocos e, portanto, os blocos cadastrados **não deverão possuir número ou ordem**.

A numeração deverá existir exclusivamente na associação do bloco com o evento.

#### Gestão do Catálogo

O sistema deverá permitir:

- criar blocos;
- editar blocos existentes;
- excluir blocos.

Não deverá ser disponibilizada funcionalidade para duplicar ou copiar blocos.

A edição de um bloco do Catálogo deverá refletir nas configurações dos eventos que utilizam o respectivo bloco.

Ao excluir um bloco que esteja associado a um ou mais eventos, o sistema deverá informar ao usuário que o bloco está em uso e que sua exclusão também o removerá das configurações desses eventos.

A exclusão somente deverá ser realizada após a confirmação do usuário.

### Condições de Aplicação

Cada bloco poderá possuir uma ou mais condições para determinar quais pessoas receberão a respectiva legenda.

Cada condição deverá ser composta por:

**Campo | Operador | Valor**

Deverão estar disponíveis os seguintes campos:

- Grupo de Trabalho;
- Tema/Grupo Temático;
- Cargo;
- Nome Fantasia;
- Papel Desempenhado.

Deverão estar disponíveis os seguintes operadores:

- Igual a;
- Diferente de;
- Contém;
- Em (lista).

Quando houver mais de uma condição, a partir da segunda deverá ser possível definir o conector lógico:

- **E**;
- **OU**.

Os campos **Campo**, **Operador** e **Valor** deverão permanecer alinhados entre as diferentes condições do bloco.

### Presets

O sistema deverá permitir salvar a configuração atual do evento como um **preset**, informando um nome para identificação.

O preset deverá armazenar o conjunto de blocos e suas respectivas regras, permitindo sua reutilização em outros eventos.

Também deverá ser possível recuperar uma configuração:

- pela biblioteca de presets; ou
- pelas regras configuradas em outro evento.

Ao carregar uma configuração, o usuário deverá escolher uma das seguintes opções:

**Substituir:** remove a configuração atual e aplica integralmente a configuração selecionada.

**Mesclar:** mantém os blocos configurados no evento atual e acrescenta os blocos da configuração selecionada.

O sistema também deverá permitir excluir um preset existente.

A exclusão de um preset deverá remover somente o preset da biblioteca, sem alterar as configurações dos eventos nos quais ele já tenha sido aplicado.

### Associação Evento – Pessoa – Legenda

A legenda atribuída a uma pessoa deverá existir no contexto do evento.

Dessa forma, a associação deverá considerar:

**Evento – Pessoa – Legenda**

A execução das regras deverá gerar novamente as associações das pessoas pertencentes ao evento atual, considerando os blocos configurados, suas respectivas condições e sua ordem de prioridade.

A execução não deverá alterar:

- as legendas de outros eventos;
- o cadastro da pessoa;
- as legendas definidas manualmente.

### Legendas Manuais

As legendas atribuídas manualmente, como **Anfitrião** e **Palestrante**, deverão ser preservadas.

Essas legendas não deverão ser recalculadas pelas regras automáticas e não poderão ser removidas durante a regeneração das legendas do evento.

### Simular

A ação **Simular** deverá permitir visualizar o resultado da configuração antes de efetivamente aplicá-la.

A simulação deverá apresentar quantas e quais pessoas seriam associadas a cada legenda considerando os blocos, a ordem e as condições configuradas.

A simulação não deverá realizar qualquer alteração nos dados do evento.

### Executar

A ação **Executar** deverá aplicar as regras configuradas e regenerar as associações **Evento – Pessoa – Legenda** do evento atual.

Antes da execução, o sistema deverá solicitar confirmação do usuário, informando que:

- as associações de legenda do evento serão recriadas;
- as legendas manuais serão preservadas;
- outros eventos não serão afetados.

Após a confirmação, o sistema deverá executar as regras considerando os blocos configurados, suas condições e sua ordem de prioridade.

### Observações Técnicas

A implementação requer adequação da modelagem para que a legenda atribuída à pessoa seja associada ao respectivo evento, seguindo a estrutura **Evento – Pessoa – Legenda**.

Atualmente, a entidade Legenda mantém informações como número, nome, background e composição, sem os conceitos de bloco reutilizável ou preset.

Deverão ser previstos novos elementos de persistência para:

- Catálogo de Blocos;
- Presets;
- configuração dos blocos por evento;
- associação Evento – Pessoa – Legenda.

A numeração deverá deixar de ser uma característica do bloco e passar a representar exclusivamente sua posição dentro da configuração de cada evento.

Os blocos do Catálogo não deverão possuir estado ativo/inativo no contexto do evento. A permanência do bloco na configuração determinará sua participação na aplicação das regras.

A exclusão de um bloco do Catálogo deverá considerar suas associações existentes com eventos, removendo-as somente após a confirmação do usuário.

## Critérios de aceite

> **Numeração**: a fonte numera os critérios, de `CA01` a `CA23`; aqui eles são `CA-01` a `CA-23` — o mesmo número da ferramenta.

```gherkin
# ── CA-01 ───────────────────────────────────────────────────
Scenario: Adicionar bloco existente
  Given que estou na Configuração de Legendas de um evento
  When solicitar a inclusão de um bloco
  Then o sistema deverá permitir pesquisar e selecionar um bloco existente no Catálogo

# ── CA-02 ───────────────────────────────────────────────────
Scenario: Criar novo bloco
  Given que estou adicionando um bloco
  When optar pela criação de um novo bloco
  Then o sistema deverá permitir informar nome, cor da legenda e composição de mesa

# ── CA-03 ───────────────────────────────────────────────────
Scenario: Criar bloco a partir da busca
  Given que pesquisei um nome que não corresponde a nenhum bloco existente no Catálogo
  When o sistema não localizar o bloco
  Then deverá disponibilizar a opção Adicionar bloco ""
  And ao selecionar a opção, deverá abrir a criação do bloco com o campo Nome previamente preenchido com o termo pesquisado

# ── CA-04 ───────────────────────────────────────────────────
Scenario: Disponibilizar bloco no Catálogo
  Given que criei um novo bloco
  When salvar o cadastro
  Then o bloco deverá ser incluído no Catálogo e ficar disponível para utilização em outros eventos

# ── CA-05 ───────────────────────────────────────────────────
Scenario: Catálogo sem numeração
  Given que estou visualizando o Catálogo de Blocos
  Then os blocos não deverão apresentar número ou ordem

# ── CA-06 ───────────────────────────────────────────────────
Scenario: Numeração por evento
  Given que existem blocos configurados para o evento
  When visualizar a configuração
  Then o Nº de cada bloco deverá corresponder à sua posição na ordem do evento

# ── CA-07 ───────────────────────────────────────────────────
Scenario: Reordenar blocos
  Given que alterei a ordem dos blocos
  When a nova ordem for aplicada
  Then o sistema deverá recalcular automaticamente a numeração dos blocos
  And a nova ordem deverá definir a prioridade de aplicação das regras

# ── CA-08 ───────────────────────────────────────────────────
Scenario: Blocos sem estado ativo/inativo
  Given que um bloco foi adicionado à configuração do evento
  Then o bloco deverá estar em vigor enquanto permanecer associado ao evento
  And não deverá ser disponibilizada opção para ativar ou desativar o bloco
  And caso ele não deva ser considerado, deverá ser removido da configuração do evento

# ── CA-09 ───────────────────────────────────────────────────
Scenario: Remover bloco do evento
  Given que um bloco está configurado para o evento
  When solicitar sua remoção
  Then o sistema deverá remover somente sua associação com o evento atual, sem excluir o bloco do Catálogo ou alterar outros eventos

# ── CA-10 ───────────────────────────────────────────────────
Scenario: Editar bloco do Catálogo
  Given que existe um bloco cadastrado no Catálogo
  When o usuário editar seus dados e salvar as alterações
  Then o cadastro do bloco deverá ser atualizado
  And as alterações deverão refletir nas configurações dos eventos que utilizam o respectivo bloco

# ── CA-11 ───────────────────────────────────────────────────
Scenario: Excluir bloco do Catálogo
  Given que existe um bloco cadastrado no Catálogo
  When o usuário solicitar sua exclusão
  Then o sistema deverá excluir o bloco do Catálogo
  And, caso o bloco esteja associado a um ou mais eventos, o sistema deverá informar que o bloco está em uso e que sua exclusão também o removerá das configurações desses eventos, solicitando confirmação antes de concluir a operação

# ── CA-12 ───────────────────────────────────────────────────
Scenario: Não duplicar blocos
  Given que estou gerenciando os blocos do Catálogo
  Then o sistema não deverá disponibilizar funcionalidade para duplicar ou copiar blocos

# ── CA-13 ───────────────────────────────────────────────────
Scenario: Configurar condições
  Given que estou configurando um bloco
  When adicionar uma condição
  Then o sistema deverá permitir informar Campo, Operador e Valor

# ── CA-14 ───────────────────────────────────────────────────
Scenario: Utilizar múltiplas condições
  Given que um bloco possui mais de uma condição
  When visualizar ou editar suas condições
  Then o sistema deverá manter Campo, Operador e Valor alinhados
  And apresentar o conector E/OU a partir da segunda condição

# ── CA-15 ───────────────────────────────────────────────────
Scenario: Salvar preset
  Given que configurei os blocos e regras de um evento
  When solicitar o salvamento como preset
  Then o sistema deverá permitir informar um nome e salvar a configuração para reutilização

# ── CA-16 ───────────────────────────────────────────────────
Scenario: Carregar preset
  Given que existe um preset disponível
  When carregá-lo em um evento
  Then o sistema deverá permitir escolher entre Substituir ou Mesclar a configuração atual

# ── CA-17 ───────────────────────────────────────────────────
Scenario: Excluir preset
  Given que existe um preset cadastrado
  When o usuário solicitar sua exclusão
  Then o sistema deverá remover o preset da biblioteca
  And manter inalteradas as configurações dos eventos nos quais o preset já tenha sido aplicado

# ── CA-18 ───────────────────────────────────────────────────
Scenario: Recuperar configuração de outro evento
  Given que outro evento possui uma configuração de legendas
  When solicitar sua recuperação
  Then o sistema deverá permitir utilizar seus blocos e regras na configuração do evento atual

# ── CA-19 ───────────────────────────────────────────────────
Scenario: Simular regras
  Given que existem blocos e condições configurados
  When acionar Simular
  Then o sistema deverá apresentar quantas e quais pessoas seriam associadas a cada legenda, sem alterar os dados

# ── CA-20 ───────────────────────────────────────────────────
Scenario: Confirmar execução
  Given que acionei Executar
  When o sistema solicitar confirmação
  Then deverá informar que as associações do evento serão recriadas, que as legendas manuais serão preservadas e que outros eventos não serão afetados

# ── CA-21 ───────────────────────────────────────────────────
Scenario: Regenerar legendas do evento
  Given que confirmei a execução
  When as regras forem processadas
  Then o sistema deverá recriar as associações Evento – Pessoa – Legenda, considerando os blocos configurados, suas condições e a ordem de prioridade

# ── CA-22 ───────────────────────────────────────────────────
Scenario: Preservar legendas manuais
  Given que uma pessoa possui uma legenda atribuída manualmente
  When as regras forem executadas
  Then essa legenda deverá ser preservada

# ── CA-23 ───────────────────────────────────────────────────
Scenario: Isolar configuração por evento
  Given que executei ou alterei a configuração de um evento
  Then as configurações e associações de legenda dos demais eventos não deverão ser alteradas
```

## Features

| Feature (N3) | Domínio · Feature Set | Operação | Critérios cobertos | Status |
|---|---|---|---|---|
| [`EVT-LEG-01`: Consultar Configuração de Legendas](../modules/eventos/legendas/f-consultar-configuracao-legendas.md) | Eventos · Legendas | Alteração | `CA-06, CA-08` | ✏️ Rascunho |
| [`EVT-LEG-02`: Adicionar Bloco de Legenda ao Evento](../modules/eventos/legendas/f-adicionar-bloco-legenda.md) | Eventos · Legendas | Alteração | `CA-01` | ✏️ Rascunho |
| [`EVT-LEG-03`: Configurar Condições de Legenda](../modules/eventos/legendas/f-configurar-condicoes-legenda.md) | Eventos · Legendas | Alteração | `CA-13, CA-14` | ✏️ Rascunho |
| [`EVT-LEG-04`: Reordenar Blocos de Legenda](../modules/eventos/legendas/f-reordenar-blocos-legenda.md) | Eventos · Legendas | Criação | `CA-07` | ✏️ Rascunho |
| [`EVT-LEG-05`: Remover Bloco de Legenda do Evento](../modules/eventos/legendas/f-remover-bloco-legenda.md) | Eventos · Legendas | Criação | `CA-09` | ✏️ Rascunho |
| [`EVT-LEG-06`: Simular Aplicação de Legendas](../modules/eventos/legendas/f-simular-aplicacao-legendas.md) | Eventos · Legendas | Alteração | `CA-19` | ✏️ Rascunho |
| [`EVT-LEG-07`: Gerar Legendas do Evento](../modules/eventos/legendas/f-gerar-legendas-evento.md) | Eventos · Legendas | Alteração | `CA-20, CA-21, CA-22, CA-23` | ✏️ Rascunho |
| [`EVT-LEG-08`: Salvar Preset de Legendas](../modules/eventos/legendas/f-salvar-preset-legendas.md) | Eventos · Legendas | Criação | `CA-15` | ✏️ Rascunho |
| [`EVT-LEG-09`: Carregar Configuração de Legendas](../modules/eventos/legendas/f-carregar-configuracao-legendas.md) | Eventos · Legendas | Criação | `CA-16, CA-18` | ✏️ Rascunho |
| [`EVT-LEG-10`: Excluir Preset de Legendas](../modules/eventos/legendas/f-excluir-preset-legendas.md) | Eventos · Legendas | Criação | `CA-17` | ✏️ Rascunho |
| [`EVT-LEG-11`: Pesquisar Blocos de Legenda](../modules/eventos/legendas/f-pesquisar-blocos-legenda.md) | Eventos · Legendas | Criação | `CA-05` | ✏️ Rascunho |
| [`EVT-LEG-12`: Cadastrar Bloco de Legenda](../modules/eventos/legendas/f-cadastrar-bloco-legenda.md) | Eventos · Legendas | Criação | `CA-02, CA-03, CA-04` | ✏️ Rascunho |
| [`EVT-LEG-13`: Editar Bloco de Legenda](../modules/eventos/legendas/f-editar-bloco-legenda.md) | Eventos · Legendas | Criação | `CA-10` | ✏️ Rascunho |
| [`EVT-LEG-14`: Excluir Bloco de Legenda](../modules/eventos/legendas/f-excluir-bloco-legenda.md) | Eventos · Legendas | Criação | `CA-11, CA-12` | ✏️ Rascunho |
| [`EVT-PAR-04`: Consultar Legenda do Participante](../modules/eventos/participantes/f-consultar-legenda-participante.md) | Eventos · Participantes | Alteração | — | ✏️ Rascunho |
| [`EVT-PAR-05`: Alterar Legenda do Participante](../modules/eventos/participantes/f-alterar-legenda-participante.md) | Eventos · Participantes | Alteração | — | ✏️ Rascunho |
<!-- trace-verified: EVT-LEG-01 @ c8018e9f8042 -->
<!-- trace-verified: EVT-LEG-02 @ e185b8b34ad9 -->
<!-- trace-verified: EVT-LEG-03 @ 55b8f3ef8821 -->
<!-- trace-verified: EVT-LEG-04 @ 09f5bae316c8 -->
<!-- trace-verified: EVT-LEG-05 @ 852e46630f8b -->
<!-- trace-verified: EVT-LEG-06 @ 011c9cba8f9e -->
<!-- trace-verified: EVT-LEG-07 @ 4976f9025e38 -->
<!-- trace-verified: EVT-LEG-08 @ acdb750c668a -->
<!-- trace-verified: EVT-LEG-09 @ 388c9c15f3cd -->
<!-- trace-verified: EVT-LEG-10 @ 59e4201ad826 -->
<!-- trace-verified: EVT-LEG-11 @ b8c2e77097a9 -->
<!-- trace-verified: EVT-LEG-12 @ 6948c2456376 -->
<!-- trace-verified: EVT-LEG-13 @ 10b2a5dddc91 -->
<!-- trace-verified: EVT-LEG-14 @ af2e50e0e48b -->
<!-- trace-verified: EVT-PAR-04 @ f05eedd48922 -->
<!-- trace-verified: EVT-PAR-05 @ 22371e65c29a -->

## Artefatos impactados

| Artefato | Tipo | Operação | Seção | Natureza | O quê | Proveniência | Situação |
|---|---|---|---|---|---|---|---|
| `modules/eventos/legendas/f-consultar-configuracao-legendas.md` | N3 | alterar | Campos/Regras/Cenários | funcional | só os blocos do evento, numerados pela posição; sem chave Ativa/Inativa; gravação a cada alteração | derivado: âncora | feito em 2026-09-30 |
| `modules/eventos/legendas/f-adicionar-bloco-legenda.md` | N3 | alterar | Campos/Regras/Cenários | funcional | bloco entra no evento pela busca no catálogo, em vez de ativar uma legenda fixa | derivado: âncora | feito em 2026-09-30 |
| `modules/eventos/legendas/f-configurar-condicoes-legenda.md` | N3 | alterar | Campos/Regras/Cenários | funcional | condições editadas no cartão do bloco, com conectivo a partir da segunda | derivado: âncora | feito em 2026-09-30 |
| `modules/eventos/legendas/f-reordenar-blocos-legenda.md` | N3 | alterar | Campos/Regras/Cenários | funcional | feature nascida do ticket: mover o bloco e renumerar | derivado: âncora | feito em 2026-09-30 |
| `modules/eventos/legendas/f-remover-bloco-legenda.md` | N3 | alterar | Campos/Regras/Cenários | funcional | feature nascida do ticket: tirar o bloco só do evento atual | derivado: âncora | feito em 2026-09-30 |
| `modules/eventos/legendas/f-simular-aplicacao-legendas.md` | N3 | alterar | Campos/Regras/Cenários | funcional | simulação passa a trazer totais e a relação nominal por legenda | derivado: âncora | feito em 2026-09-30 |
| `modules/eventos/legendas/f-gerar-legendas-evento.md` | N3 | alterar | Campos/Regras/Cenários | funcional | confirmação antes de gerar; legendas manuais preservadas; todo bloco presente vale | derivado: âncora | feito em 2026-09-30 |
| `modules/eventos/legendas/f-salvar-preset-legendas.md` | N3 | alterar | Campos/Regras/Cenários | funcional | feature nascida do ticket: guardar a configuração como preset | derivado: âncora | feito em 2026-09-30 |
| `modules/eventos/legendas/f-carregar-configuracao-legendas.md` | N3 | alterar | Campos/Regras/Cenários | funcional | feature nascida do ticket: trazer preset ou configuração de outro evento | derivado: âncora | feito em 2026-09-30 |
| `modules/eventos/legendas/f-excluir-preset-legendas.md` | N3 | alterar | Campos/Regras/Cenários | funcional | feature nascida do ticket: excluir preset da biblioteca | derivado: âncora | feito em 2026-09-30 |
| `modules/eventos/legendas/f-pesquisar-blocos-legenda.md` | N3 | alterar | Campos/Regras/Cenários | funcional | feature nascida do ticket: catálogo de blocos, sem número nem ordem | derivado: âncora | feito em 2026-09-30 |
| `modules/eventos/legendas/f-cadastrar-bloco-legenda.md` | N3 | alterar | Campos/Regras/Cenários | funcional | feature nascida do ticket: criar bloco no catálogo, inclusive a partir da busca | derivado: âncora | feito em 2026-09-30 |
| `modules/eventos/legendas/f-editar-bloco-legenda.md` | N3 | alterar | Campos/Regras/Cenários | funcional | feature nascida do ticket: alterar nome e cor do bloco, com reflexo nos eventos | derivado: âncora | feito em 2026-09-30 |
| `modules/eventos/legendas/f-excluir-bloco-legenda.md` | N3 | alterar | Campos/Regras/Cenários | funcional | feature nascida do ticket: excluir bloco, com aviso de uso e confirmação | derivado: âncora | feito em 2026-09-30 |
| `modules/eventos/participantes/f-consultar-legenda-participante.md` | N3 | alterar | Campos/Regras/Cenários | funcional | lista de legendas vinda do catálogo, com a marca "Configurada neste evento" | derivado: âncora | feito em 2026-09-30 |
| `modules/eventos/participantes/f-alterar-legenda-participante.md` | N3 | alterar | Campos/Regras/Cenários | funcional | a legenda atribuída é manual, única por participante e preservada na geração | derivado: âncora | feito em 2026-09-30 |
| `global/data-models/eventos.md` | DATA-MODEL | alterar | Legenda · EventoLegenda · EventoLegendaCondicao · EventoPessoaLegenda · PresetLegenda | dados | as cinco entidades de legenda, como o ticket as deixou | derivado: ## Campos → coluna | feito em 2026-09-30 |
| `global/MESSAGE-DICTIONARY.md` | MESSAGE-DICT | alterar | Eventos — legendas | dados | as 16 mensagens das telas de configuração, catálogo e presets | elicitado | feito em 2026-09-30 |
| `global/DATA-MODEL.md` | DATA-MODEL | alterar | Arquivos Lógicos (APF) | dados | os três arquivos lógicos de Eventos dimensionados: Evento, Legenda e PresetLegenda | elicitado | feito em 2026-10-04 |
| `global/CONTAGEM-PF.md` | MÉTRICA | alterar | — | derivado | contagem detalhada das 16 features e das funções de dados, pelo `PROMPT_CONTAGEM` | derivado: delta de dados | feito em 2026-10-04 |

## Contagem estimada

Não houve — AIM aberta na entrega.

## Premissas

- **Linha do tempo.** O ticket foi criado em 2026-09-04, estava *em teste* em 2026-09-30 e em *homologação* em 2026-10-04, na sprint que o Jira chama de `SP_SMC_5` e esta instância, de `SP005`; a data da entrega não consta em nenhuma fonte ❓. A especificação foi escrita em 2026-09-30, por engenharia reversa dos documentos legados e de um código que já continha a entrega. Não havia baseline de Pontos de Função: a primeira contagem é a de 2026-10-04, feita já com a entrega dentro — ela dá o tamanho de cada função depois do ticket, que é a base do cálculo da função alterada.
- **O "antes" é o documento legado.** Os N3 já nasceram descrevendo o comportamento depois do ticket, então não há versão anterior do N3 nem do código para comparar. O contraste *Antes* e *Agora* usa GPE006 – Gerenciar Regras de Legendas v1.0 (03/10/2025) e GPE005 – Gerenciar Participante v1.1 (16/12/2025) como retrato do que existia. ⚠️ Onde o sistema já divergia desses documentos antes do ticket, o contraste atribui ao ticket uma mudança que não é dele.
- **Natureza é proposta.** `alterada` é a feature que tem funcionalidade correspondente no documento legado; `incluída`, a que não tem. A contagem detalhada mediu o tamanho, não a natureza: ela segue como proposta, a confirmar com a equipe de métricas — ver as decisões pendentes.
- **Regras e Cenários.** Nas features incluídas, o número é o total do N3, porque tudo nele veio com o ticket. Nas alteradas sai `—`: o N3 nasceu já com o delta, e não há como separar o que o ticket acrescentou do que já existia.
- **Dados declarados, não verificados.** Os scripts de migração do banco não estão nesta instância; as fontes citam três deles, sem o conteúdo. As alterações de dados são as declaradas nas *Observações Técnicas* do ticket, confrontadas com `global/data-models/eventos.md`.
- **PFB e PFL.** O PFB de cada feature é a soma dos processos elementares que o ticket incluiu ou alterou, como estão na `## Métricas de tamanho` do N3; o PFL é o PFB inteiro na feature incluída e a metade na alterada. Nas funções de dados, o tamanho é o de depois do ticket, do `global/DATA-MODEL.md`; o de antes só consta para a Legenda, pelo que o próprio ticket diz dela.

## Alterações na spec, por Feature Set

### Legendas

| Feature | CA-n | Natureza | Mudança | Regras | Cenários | PFB | PFL |
|---|---|---|---|---|---|---|---|
| `EVT-LEG-01` **Consultar Configuração de Legendas** | CA-06, CA-08 | alterada | **Alteração** do que a consulta lista e de como numera. *Antes* a tela trazia as doze legendas configuráveis, ativas e inativas, cada uma com a chave Ativa/Inativa, sem número, e o que se alterava só valia depois de "Salvar Regras". *Agora* a tela traz só os blocos adicionados ao evento, um cartão por bloco, numerado pela posição na configuração — que é também a prioridade —, não há bloco inativo, e cada alteração é gravada na hora, sem botão de salvar. | — | — | 4 | 2 |
| `EVT-LEG-02` **Adicionar Bloco de Legenda ao Evento** | CA-01 | alterada | **Alteração** de como a legenda entra em vigor no evento. *Antes* a legenda era uma das doze fixas e entrava em vigor quando o usuário a ativava, como primeiro passo de "Incluir Regra de Legenda". *Agora* o usuário abre a janela Adicionar bloco, busca pelo nome no catálogo comum a todos os eventos, marca um ou mais blocos e os adiciona; cada bloco entra no fim da ordem, sem condições. A busca sem resultado oferece o atalho que leva a Cadastrar Bloco de Legenda. | — | — | 6 | 3 |
| `EVT-LEG-03` **Configurar Condições de Legenda** | CA-13, CA-14 | alterada | **Alteração** da edição das condições. *Antes* "Incluir Regra" e "Editar Regra" eram funcionalidades separadas, com Campo, Operador e Valor obrigatórios, o quadro "Preview da condição" e gravação por "Salvar Regras". *Agora* a condição é incluída, alterada e excluída no próprio cartão do bloco e gravada a cada mudança, com as colunas Conectivo, Campo, Operador e Valor alinhadas e o conectivo E ou OU a partir da segunda; o preview não existe, e o valor vazio é aceito. | — | — | 4 | 2 |
| `EVT-LEG-04` **Reordenar Blocos de Legenda** | CA-07 | incluída | **Inclusão** da reordenação dos blocos. *Antes* não havia como mudar a ordem: GPE006 só dizia que as regras se aplicam "na ordem de prioridade das legendas". *Agora* as setas Mover para cima e Mover para baixo trocam o bloco de lugar com o vizinho, os números são recalculados e a nova ordem passa a ser a prioridade. | +9 | +9 | 3 | 3 |
| `EVT-LEG-05` **Remover Bloco de Legenda do Evento** | CA-09 | incluída | **Inclusão** da remoção do bloco da configuração do evento. *Antes* a legenda que não devia valer era inativada pela chave Ativa/Inativa, e continuava na lista. *Agora* o bloco é removido do evento, com as condições que tinha ali, depois de confirmação; continua no catálogo, e os blocos que ficam são renumerados. | +8 | +8 | 3 | 3 |
| `EVT-LEG-06` **Simular Aplicação de Legendas** | CA-19 | alterada | **Alteração** do resultado da simulação. *Antes* "Simular Execução" apresentava só um resumo da quantidade de pessoas selecionadas para cada legenda. *Agora* "Simular" mostra quatro totais — Participantes, Legendas removidas, Legendas aplicadas e Manuais preservadas —, os blocos ignorados e, para cada legenda, a relação nominal dos participantes, e dá acesso direto à geração. | — | — | 5 | 2,5 |
| `EVT-LEG-07` **Gerar Legendas do Evento** | CA-20, CA-21, CA-22, CA-23 | alterada | **Alteração** do que a geração apaga e do que ela exige. *Antes* "Executar Regras" removia todas as legendas existentes do evento antes de aplicar as regras ativas, sem pedir confirmação. *Agora* "Executar" pede confirmação — informando que as associações do evento serão recriadas, que as manuais serão preservadas e que os outros eventos não serão afetados —, apaga só as legendas atribuídas por regra, preserva as manuais e aplica todos os blocos presentes na configuração, pela ordem. | — | — | 4 | 2 |
| `EVT-LEG-08` **Salvar Preset de Legendas** | CA-15 | incluída | **Inclusão** do preset. *Antes* a configuração de um evento não podia ser guardada para reúso. *Agora* "Salvar como preset" guarda na biblioteca, com um nome, os blocos, a ordem e as condições do evento. | +9 | +10 | 4 | 4 |
| `EVT-LEG-09` **Carregar Configuração de Legendas** | CA-16, CA-18 | incluída | **Inclusão** da carga de configuração. *Antes* cada evento era configurado do zero. *Agora* "Carregar configuração" traz a configuração de um preset ou de outro evento, no modo Substituir — troca a configuração atual pela selecionada — ou no modo Mesclar — acrescenta os blocos que faltam. | +11 | +17 | 15 | 15 |
| `EVT-LEG-10` **Excluir Preset de Legendas** | CA-17 | incluída | **Inclusão** da exclusão de preset. *Antes* não havia preset. *Agora* o preset é excluído da biblioteca, depois de confirmação, sem alterar os eventos em que já foi aplicado. | +5 | +8 | 3 | 3 |
| `EVT-LEG-11` **Pesquisar Blocos de Legenda** | CA-05 | incluída | **Inclusão** do catálogo de blocos como tela de consulta. *Antes* as legendas eram uma relação fixa e numerada, sem tela própria. *Agora* o Catálogo de blocos, comum a todos os eventos, é pesquisado pelo nome e mostra o nome e a cor de cada bloco, sem número nem ordem. | +5 | +10 | 3 | 3 |
| `EVT-LEG-12` **Cadastrar Bloco de Legenda** | CA-02, CA-03, CA-04 | incluída | **Inclusão** do cadastro de bloco. *Antes* não se criava legenda: a relação era fixa. *Agora* o bloco é criado no catálogo, com nome e cor, e fica disponível a todos os eventos; pode ser criado de dentro da configuração de um evento, com o nome já preenchido pelo termo buscado, e nesse caso já entra no evento. | +9 | +14 | 3 | 3 |
| `EVT-LEG-13` **Editar Bloco de Legenda** | CA-10 | incluída | **Inclusão** da edição de bloco. *Antes* o nome e a cor das legendas não eram alteráveis pela tela. *Agora* os dois são alterados no catálogo, e a mudança vale em todos os eventos que usam o bloco e nas legendas já atribuídas. | +9 | +13 | 3 | 3 |
| `EVT-LEG-14` **Excluir Bloco de Legenda** | CA-11, CA-12 | incluída | **Inclusão** da exclusão de bloco. *Antes* não se excluía legenda. *Agora* o bloco é excluído do catálogo depois de o sistema informar em que eventos ele está em uso e pedir confirmação; a exclusão o retira da configuração desses eventos e das legendas dos participantes. Não há cópia de bloco. | +12 | +15 | 3 | 3 |

| Processo elementar | Da feature | Papel | Tipo | PFB | Natureza | PFL | Critérios |
|---|---|---|---|---|---|---|---|
| Consultar Configuração de Legendas | `EVT-LEG-01` | principal | CE | 4 | alterada | 2 | `CA-06, CA-08` |
| Adicionar Bloco de Legenda ao Evento | `EVT-LEG-02` | principal | EE | 3 | alterada | 1,5 | `CA-01` |
| Consultar Lista de blocos (combo) | `EVT-LEG-02` | acessório | CE | 3 | alterada | 1,5 | `CA-01` |
| Configurar Condições de Legenda | `EVT-LEG-03` | principal | EE | 4 | alterada | 2 | `CA-13, CA-14` |
| Reordenar Blocos de Legenda | `EVT-LEG-04` | principal | EE | 3 | incluída | 3 | `CA-07` |
| Remover Bloco de Legenda do Evento | `EVT-LEG-05` | principal | EE | 3 | incluída | 3 | `CA-09` |
| Simular Aplicação de Legendas | `EVT-LEG-06` | principal | SE | 5 | alterada | 2,5 | `CA-19` |
| Gerar Legendas do Evento | `EVT-LEG-07` | principal | EE | 4 | alterada | 2 | `CA-20, CA-21, CA-22, CA-23` |
| Salvar Preset de Legendas | `EVT-LEG-08` | principal | EE | 4 | incluída | 4 | `CA-15` |
| Carregar Configuração de Legendas | `EVT-LEG-09` | principal | EE | 6 | incluída | 6 | `CA-16, CA-18` |
| Consultar Biblioteca de presets (combo) | `EVT-LEG-09` | acessório | SE | 5 | incluída | 5 | `CA-16` |
| Consultar De outro evento (combo) | `EVT-LEG-09` | acessório | SE | 4 | incluída | 4 | `CA-18` |
| Excluir Preset de Legendas | `EVT-LEG-10` | principal | EE | 3 | incluída | 3 | `CA-17` |
| Pesquisar Blocos de Legenda | `EVT-LEG-11` | principal | CE | 3 | incluída | 3 | `CA-05` |
| Cadastrar Bloco de Legenda | `EVT-LEG-12` | principal | EE | 3 | incluída | 3 | `CA-02, CA-03, CA-04` |
| Editar Bloco de Legenda | `EVT-LEG-13` | principal | EE | 3 | incluída | 3 | `CA-10` |
| Excluir Bloco de Legenda | `EVT-LEG-14` | principal | EE | 3 | incluída | 3 | `CA-11, CA-12` |

Em `EVT-LEG-13` *Editar Bloco de Legenda* a leitura que abre a janela de edição não conta: a lista do catálogo já mostra o nome e a cor.

### Participantes

| Feature | CA-n | Natureza | Mudança | Regras | Cenários | PFB | PFL |
|---|---|---|---|---|---|---|---|
| `EVT-PAR-04` **Consultar Legenda do Participante** | — | alterada | **Alteração** da lista de legendas oferecida na consulta. *Antes* a janela trazia uma relação fixa e numerada, de "1 – Anfitrião" a "16 – Assento livre", com a composição da mesa. *Agora* a lista vem do catálogo de blocos, em ordem alfabética, sem número nem composição, e marca "Configurada neste evento" nos blocos que fazem parte da configuração do evento. 🔍 Atribuída ao ticket por dedução: a lista e a marca dependem do catálogo e da configuração por evento, que só existem a partir dele. | — | — | 3 | 1,5 |
| `EVT-PAR-05` **Alterar Legenda do Participante** | — | alterada | **Alteração** da natureza da legenda atribuída. *Antes* GPE005 falava só em alterar ou atribuir a legenda do participante, sem distinguir a manual, e a execução das regras removia todas as legendas do evento. *Agora* a legenda escolhida é manual, única por participante, guardada na associação Evento – Pessoa – Legenda, vale só para o evento aberto, prevalece sobre as recebidas por regra e não é desfeita pela geração. | — | — | 3 | 1,5 |

| Processo elementar | Da feature | Papel | Tipo | PFB | Natureza | PFL | Critérios |
|---|---|---|---|---|---|---|---|
| Consultar Selecione uma Legenda (combo) | `EVT-PAR-04` | acessório | CE | 3 | alterada | 1,5 | — |
| Alterar Legenda do Participante | `EVT-PAR-05` | principal | EE | 3 | alterada | 1,5 | — |

Em `EVT-PAR-04` *Consultar Legenda do Participante* o ticket alcançou só a lista de legendas; o processo principal da feature, de 4 PF, não entra no PFB.

## Funções de dados alteradas

### ALI: Evento — RLR ❓ → 6 · DER ❓ → 33 · 15 PF · alterada

| Migração | Entidade · atributo | Natureza | Mudança |
|---|---|---|---|
| ❓ | EventoLegenda · Legenda e Nº | registro lógico incluído 🔍 | **Inclusão** do bloco de legenda do evento. *Antes* GPE006 já descrevia regras de legenda por evento, com cada legenda ativa ou inativa; como isso era guardado não consta em nenhuma fonte ❓. *Agora* cada bloco presente na configuração é um registro do evento, com o Nº que dá a ordem e a prioridade; não há atributo de ativo ou inativo. |
| ❓ | EventoLegendaCondicao · Ordem, Conectivo, Campo, Operador e Valor | registro lógico incluído 🔍 | **Inclusão** da condição como registro do bloco. *Antes* a regra de uma legenda tinha Campo, Operador e Valor, segundo GPE006; a guarda anterior não consta ❓. *Agora* cada condição guarda também a ordem dentro do bloco e o conectivo E ou OU que a liga à anterior. |
| ❓ | EventoPessoaLegenda · Legenda do participante, Manual e Data de atribuição | registro lógico incluído 🔍 | **Inclusão** da associação Evento – Pessoa – Legenda. *Antes* o ticket diz apenas que a legenda da pessoa "deverá passar a ser vinculada ao evento"; onde ela era guardada não consta ❓. *Agora* cada legenda que o participante recebe num evento é um registro, com a marca de manual e a data de atribuição, e o participante pode ter mais de uma legenda recebida por regra. |

O arquivo lógico Evento já existia — o evento, os assentos e os participantes são anteriores ao ticket — e por isso é função alterada, medida pelo tamanho de depois: 6 registros lógicos e 33 DER, complexidade Alta. O tamanho de antes não consta ❓. Dos números de hoje, 3 registros e 10 DER são das três entidades acima; se as regras por evento e a legenda do participante já eram guardadas neste arquivo antes do ticket, veio menos do que isso.

### ALI: Legenda — RLR 1 → 1 · DER 5 → 3 · 7 PF · alterada

| Migração | Entidade · atributo | Natureza | Mudança |
|---|---|---|---|
| ❓ | Legenda · número | atributo removido | **Remoção** do número da legenda. *Antes* a legenda tinha número próprio: o ticket registra que a entidade guardava "número, nome, background e composição", e GPE005 lista as opções de "1 – Anfitrião" a "16 – Assento livre". *Agora* o número não é do bloco: é a posição dele na configuração de cada evento. |
| `V00020` 🔍 | Legenda · composição | atributo removido | **Remoção** da composição de mesa. *Antes* a legenda guardava a composição, que a imagem de GPE005 mostra ao lado do nome. *Agora* o bloco só tem nome e cor. ⚠️ O ticket pede a composição na criação do bloco — ver as decisões pendentes. |

Os 5 DER de antes são os quatro atributos que o ticket cita — número, nome, background e composição — mais o identificador 🔍. A complexidade é Baixa antes e depois.

### ALI: PresetLegenda — RLR 0 → 1 · DER 0 → 5 · 7 PF · incluída

| Migração | Entidade · atributo | Natureza | Mudança |
|---|---|---|---|
| `V00018` 🔍 | PresetLegenda · Nome do preset, Descrição, Evento de origem e Configuração | entidade incluída | **Inclusão** do preset. *Antes* não havia como guardar uma configuração: o ticket registra que a Legenda existia "sem os conceitos de bloco reutilizável ou preset". *Agora* o preset guarda, com nome único, o retrato dos blocos, da ordem e das condições, mais a descrição e o nome do evento de origem. |

## Impacto em dicionários

- **`global/MESSAGE-DICTIONARY.md`** — as 16 mensagens da seção *Eventos — legendas* pertencem às telas que o ticket reformulou ou criou: três da configuração do evento (`EVT_LEG_EVENTO_NAO_INFORMADO`, `EVT_LEG_EVENTO_NAO_ENCONTRADO` e `EVT_LEG_BLOCO_REPETIDO`), seis de preset (`EVT_LEG_PRESET_SALVO`, `EVT_LEG_PRESET_NOME_OBRIGATORIO`, `EVT_LEG_PRESET_NOME_DUPLICADO`, `EVT_LEG_PRESET_ILEGIVEL`, `EVT_LEG_PRESET_REMOVIDO` e `EVT_LEG_PRESET_NAO_ENCONTRADO`) e sete do catálogo de blocos (`EVT_LEG_BLOCO_CRIADO`, `EVT_LEG_BLOCO_ATUALIZADO`, `EVT_LEG_BLOCO_EXCLUIDO`, `EVT_LEG_NOME_OBRIGATORIO`, `EVT_LEG_COR_INVALIDA`, `EVT_LEG_NOME_DUPLICADO` e `EVT_LEG_BLOCO_NAO_ENCONTRADO`). Também são dessas telas as duas mensagens de lista vazia, `EMPTY_BLOCOS` e `EMPTY_CONFIGURACAO`. O dicionário foi levantado do código em 2026-09-30: não há texto anterior para comparar.
- **Regras e campos canônicos** — nenhum: `global/RULES-DICTIONARY.md` e `global/FIELD-DICTIONARY.md` não têm entrada de legenda.

## Decisões de produto pendentes

- **Composição de mesa na criação do bloco.** O critério `CA-02` pede nome, cor da legenda e composição de mesa; a entrega tem só nome e cor, e a composição que a legenda guardava foi retirada. Decidir se o critério é aceito sem a composição ou se ela volta. **Trava** o aceite do critério na homologação e a aprovação de `EVT-LEG-12` *Cadastrar Bloco de Legenda*; se a composição voltar, mudam também `EVT-LEG-13` *Editar Bloco de Legenda*, a entidade Legenda e a contagem.
- **Exclusão de bloco apaga legendas manuais.** O critério `CA-11` diz que excluir um bloco em uso o remove das configurações dos eventos; a entrega apaga também todas as legendas desse bloco atribuídas a participantes, em todos os eventos, inclusive as manuais — que o próprio ticket manda preservar na geração. E o aviso de uso só olha a configuração dos eventos: o bloco que está fora de todas elas, mas foi atribuído manualmente, é excluído como se não estivesse em uso. Decidir se a exclusão deve preservar, impedir ou avisar. **Trava** a aprovação de `EVT-LEG-14` *Excluir Bloco de Legenda*.
- **Uma legenda por participante ou várias.** O critério `CA-21` fala em aplicar os blocos pela "ordem de prioridade"; a entrega atribui uma legenda por bloco atendido e usa a ordem só para escolher qual aparece. Decidir qual é a intenção. **Trava** a aprovação de `EVT-LEG-07` *Gerar Legendas do Evento* e de `EVT-LEG-06` *Simular Aplicação de Legendas*, cujo total "Legendas aplicadas" conta atribuições e não pessoas.
- **Mesclar descarta as condições da origem.** O critério `CA-16` define Mesclar como manter os blocos do evento e acrescentar os da configuração selecionada; a entrega acrescenta só os blocos cuja legenda ainda não está no evento, e para a legenda presente dos dois lados ficam as condições do evento. Substituir, que apaga a configuração atual, não pede confirmação. **Trava** a aprovação de `EVT-LEG-09` *Carregar Configuração de Legendas*.
- **"Resetar Regras" deixou de existir.** GPE006 traz a funcionalidade, a tela entregue não tem o botão e o ticket não a menciona. Decidir se ela foi retirada por este ticket ou se precisa voltar. **Trava** a contagem da sprint — função retirada é função excluída, e as tabelas desta AIM só têm `incluída` e `alterada` — e a pendência "Resetar Regras de Legenda" do `modules/INDEX.md`.
- **Natureza de duas features de configuração.** `EVT-LEG-02` *Adicionar Bloco de Legenda ao Evento* saiu aqui como alterada, porque descende de "Incluir Regra de Legenda"; `EVT-LEG-05` *Remover Bloco de Legenda do Evento* saiu como incluída, embora substitua a chave Ativa/Inativa. As duas leituras são defensáveis. A contagem de 2026-10-04 tratou adicionar, configurar condições, reordenar e remover como quatro processos elementares, porque diferem nos dados ou na lógica, embora as quatro gravem a configuração inteira do evento; a equipe de métricas pode ler de outro modo. **Trava** o PFL das features de configuração, que vale 100% na incluída e 50% na alterada.
- **Arquivos lógicos novos ou alterados.** O ticket declara quatro "novos elementos de persistência" — catálogo, presets, configuração por evento e associação Evento – Pessoa – Legenda —, mas GPE006 já tinha regras por evento e GPE005 já tinha legenda do participante. Sem o modelo anterior, só o preset é seguramente novo e só a Legenda é seguramente alterada. **Encaminhada pela contagem de 2026-10-04**, a confirmar com a equipe de métricas: a configuração por evento e a legenda do participante entraram como registros do arquivo lógico Evento, que já existia e conta como alterado — 15 PF, PFL 7,5 —; a Legenda, como alterada — 7 PF, PFL 3,5 —; e o preset, como incluído — 7 PF. Se a configuração ou o participante forem lidos como arquivos lógicos próprios, mudam esses números e o ALR das transações. **Trava** o PF das funções de dados.
- **Dois critérios que tocam duas features.** O critério `CA-03` ficou em `EVT-LEG-12` *Cadastrar Bloco de Legenda*, que faz a criação, embora o atalho que a abre esteja na janela de `EVT-LEG-02` *Adicionar Bloco de Legenda ao Evento*; o critério `CA-22` ficou em `EVT-LEG-07` *Gerar Legendas do Evento*, que é quem preserva a legenda manual, e não em `EVT-PAR-05` *Alterar Legenda do Participante*, que a atribui. Confirmar essa fronteira no aval. **Trava** só o critério que a planilha da sprint leva a cada feature.
- **Alcance sobre as features de Participantes.** A nova guarda da legenda é lida por seis features que esta AIM não lista: `EVT-PAR-01` *Pesquisar Participantes*, `EVT-PAR-06` *Remover Legenda do Participante*, `EVT-PAR-07` *Consultar Mapa de Assentos*, `EVT-PAR-12` *Buscar Pessoa na Mesa*, `EVT-PAR-14` *Exportar Participantes* e `EVT-PAR-15` *Exportar Mapa de Assentos*. Entraram só `EVT-PAR-04` *Consultar Legenda do Participante* e `EVT-PAR-05` *Alterar Legenda do Participante*, cujos N3 já atribuíam a mudança ao ticket. Confirmar com o time de desenvolvimento quais das seis o ticket alterou. **Trava** a completude da `## Features` e da contagem.

## Reconciliação

> Preenchida no fechamento (estado `concluído`): declarado × tocado. Escreva o resultado abaixo desta citação.

AIM aberta na entrega: o ticket foi entregue antes de haver escopo avalizado, então não há declarado × tocado a reconciliar. O changeset registra o que a especificação já tinha absorvido do ticket na engenharia reversa de 2026-09-30 e a contagem detalhada, feita e confirmada em 2026-10-04. Ficaram fora dele, de propósito, quatro tipos de artefato: o plano de testes, porque a instância roda no perfil `requisitos`, cuja esteira para no modelo de dados; o protótipo, porque a instância não tem nenhum — o ticket traz o anexo `prototipo_regras_legenda_v3 (2).html`, que não foi trazido, e a referência dos N3 é a tela implementada —; os repositórios de código, que estão fora do aval; e o `global/NFR.md`, porque o ticket não traz requisito não-funcional.

## Changelog

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-10-04 | Claude (apf-cpm) | Contagem detalhada | PFB e PFL das 16 features e das três funções de dados, espelhados dos N3 e do `global/DATA-MODEL.md`: 98 PFB e 72,5 PFL — transações 69 e 54,5, dados 29 e 18. Changeset sem linha `previsto`. A sprint passa a `SP005`. Continua em `em-análise`: falta só o aval do PO |
| 2026-10-04 | Claude (analise-impacto) | AIM aberta na entrega | ticket `PDTIC25148-34` registrado a partir da exportação do Jira de 2026-10-04, em homologação; 16 features mapeadas — 14 de Legendas e 2 de Participantes —, com os 23 critérios distribuídos sem repetição; elo fechado na `## Origem` dos N3 e no `modules/INDEX.md`. Fica em `em-análise`: faltam o aval do PO e a contagem detalhada |
