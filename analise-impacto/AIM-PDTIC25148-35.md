<!-- docqui: 4.0.2 | prompt: PROMPT_AIM | atualizado: 2026-10-04 -->
---
tipo: ticket
ticket: PDTIC25148-35
ferramenta: Jira
link: https://sistemaindustria.atlassian.net/browse/PDTIC25148-35
titulo: Melhorias na Listagem de Pessoas Confirmadas
estado: em-análise
aberta-na-entrega: true
sprint: "SP005"
avalizado-por: ""
aberta-em: 2026-10-04
---

# AIM PDTIC25148-35

## Detalhe do item

> Transcrição da descrição do ticket `PDTIC25148-35` no Jira, a partir da exportação de 2026-10-04 guardada em `arquivos/`.

### História do Usuário

**Eu como** usuário responsável pela gestão do evento

**Quero** visualizar e filtrar as pessoas confirmadas com informações e ações adicionais

**Para** facilitar a consulta e a manutenção dos dados dos participantes do evento.

### Descrição

Realizar melhorias na listagem de **Pessoas Confirmadas** do evento, ajustando as opções disponíveis na definição de critérios, permitindo o acesso ao perfil da pessoa diretamente pela listagem e incluindo um novo filtro para identificação de pessoas sem foto cadastrada.

### Regras de Negócio

#### Definição de Critérios

Ao definir um critério para as pessoas confirmadas, o sistema não deverá mais disponibilizar a opção **Assento Livre**.

As demais opções existentes deverão permanecer inalteradas.

#### Acesso ao Perfil da Pessoa

O nome da pessoa deverá ser apresentado como um link na listagem de Pessoas Confirmadas.

Ao acionar o nome, o sistema deverá:

- direcionar o usuário para o perfil da respectiva pessoa;
- abrir o perfil em uma nova aba do navegador.

#### Filtro de Pessoas sem Foto

A listagem deverá disponibilizar um filtro que permita consultar somente as pessoas que **não possuem foto cadastrada**.

Ao aplicar o filtro, deverão ser exibidas apenas as pessoas confirmadas no evento que estejam sem foto.

## Critérios de aceite

> **Numeração**: a fonte numera os critérios, de `CA01` a `CA03`; aqui eles são `CA-01` a `CA-03` — o mesmo número da ferramenta.

```gherkin
# ── CA-01 ───────────────────────────────────────────────────
Scenario: Remover opção Assento Livre
  Given que estou na listagem de Pessoas Confirmadas
  When acessar a definição de um critério
  Then a opção Assento Livre não deverá ser apresentada

# ── CA-02 ───────────────────────────────────────────────────
Scenario: Acessar perfil da pessoa
  Given que estou visualizando uma pessoa na listagem de Pessoas Confirmadas
  When acionar o nome da pessoa
  Then o sistema deverá abrir o perfil correspondente em uma nova aba do navegador

# ── CA-03 ───────────────────────────────────────────────────
Scenario: Filtrar pessoas sem foto
  Given que estou na listagem de Pessoas Confirmadas
  When aplicar o filtro para pessoas sem foto cadastrada
  Then o sistema deverá apresentar somente as pessoas confirmadas no evento que não possuem foto
```

## Features

| Feature (N3) | Domínio · Feature Set | Operação | Critérios cobertos | Status |
|---|---|---|---|---|
| [`EVT-PAR-01`: Pesquisar Participantes](../modules/eventos/participantes/f-pesquisar-participantes.md) | Eventos · Participantes | Alteração | `CA-02, CA-03` | ✏️ Rascunho |
| [`EVT-PAR-04`: Consultar Legenda do Participante](../modules/eventos/participantes/f-consultar-legenda-participante.md) | Eventos · Participantes | Alteração | `CA-01` | ✏️ Rascunho |
<!-- trace-verified: EVT-PAR-01 @ 8ef556812d7a -->
<!-- trace-verified: EVT-PAR-04 @ f05eedd48922 -->

## Artefatos impactados

| Artefato | Tipo | Operação | Seção | Natureza | O quê | Proveniência | Situação |
|---|---|---|---|---|---|---|---|
| `modules/eventos/participantes/f-pesquisar-participantes.md` | N3 | alterar | Campos/Regras/Cenários | funcional | nome como atalho para o cadastro da pessoa, em nova aba, e critério "Somente pessoas sem foto" | derivado: âncora | feito em 2026-09-30 |
| `modules/eventos/participantes/f-consultar-legenda-participante.md` | N3 | alterar | Campos/Regras/Cenários | funcional | "Assento livre" sai da lista de legendas oferecida na janela | derivado: âncora | feito em 2026-09-30 |
| `modules/eventos/participantes/f-alterar-legenda-participante.md` | N3 | alterar | Regras | funcional | regra 9, consequência da lista: "Assento livre" não é atribuída — a feature fica fora da `## Features` | elicitado | feito em 2026-09-30 |
| `modules/pessoas/cadastro-pessoas/f-editar-pessoa.md` | N3 | alterar | Cenários/Comportamento de tela | funcional | segundo caminho de acesso à tela, pelo nome do participante — a feature fica fora da `## Features` | elicitado | feito em 2026-09-30 |
| `global/CONTAGEM-PF.md` | MÉTRICA | alterar | — | derivado | contagem detalhada das 2 features, pelo `PROMPT_CONTAGEM` | elicitado | feito em 2026-10-04 |

## Contagem estimada

Não houve — AIM aberta na entrega.

## Premissas

- **Linha do tempo.** O ticket foi criado em 2026-09-04, estava *em teste* em 2026-09-30 e em *homologação* em 2026-10-04, na sprint que o Jira chama de `SP_SMC_5` e esta instância, de `SP005`; a data da entrega não consta em nenhuma fonte ❓. A especificação foi escrita em 2026-09-30, por engenharia reversa dos documentos legados e de um código que já continha a entrega. Não havia baseline de Pontos de Função: a primeira contagem é a de 2026-10-04, feita já com a entrega dentro — ela dá o tamanho de cada função depois do ticket, que é a base do cálculo da função alterada.
- **O "antes" é o documento legado.** Os N3 já nasceram descrevendo o comportamento depois do ticket. O contraste *Antes* e *Agora* usa GPE005 – Gerenciar Participante v1.1 (16/12/2025) como retrato do que existia.
- **Natureza.** As duas features têm funcionalidade correspondente em GPE005, então são alteradas — proposta a confirmar com a equipe de métricas.
- **PFB e PFL.** O PFB de cada feature é a soma dos processos elementares que o ticket alterou, como estão na `## Métricas de tamanho` do N3; o PFL é a metade, porque as duas features são alteradas.
- **Regras e Cenários.** O número é o do que existe no N3 por causa deste ticket. Em `EVT-PAR-04` *Consultar Legenda do Participante* a restrição entrou numa regra que já existia, a regra 3, e por isso a coluna de regras sai zero.

## Alterações na spec, por Feature Set

### Participantes

| Feature | CA-n | Natureza | Mudança | Regras | Cenários | PFB | PFL |
|---|---|---|---|---|---|---|---|
| `EVT-PAR-01` **Pesquisar Participantes** | CA-02, CA-03 | alterada | **Inclusão** do atalho para o cadastro da pessoa e do critério de foto. *Antes* o nome do participante era só texto na lista, e a pesquisa não tinha critério de foto. *Agora* o nome abre o cadastro da pessoa em nova aba, com a dica "Abrir o perfil da pessoa em nova aba", e a caixa "Somente pessoas sem foto" restringe o resultado aos participantes cuja pessoa não tem foto. | +1 | +2 | 4 | 2 |
| `EVT-PAR-04` **Consultar Legenda do Participante** | CA-01 | alterada | **Remoção** da opção "Assento livre" da lista de legendas. *Antes* a relação de legendas oferecida para o participante terminava em "16 – Assento livre". *Agora* a lista traz as legendas do catálogo, menos "Assento livre"; as demais opções ficam como estavam. | 0 | +1 | 3 | 1,5 |

| Processo elementar | Da feature | Papel | Tipo | PFB | Natureza | PFL | Critérios |
|---|---|---|---|---|---|---|---|
| Pesquisar Participantes | `EVT-PAR-01` | principal | CE | 4 | alterada | 2 | `CA-02, CA-03` |
| Consultar Selecione uma Legenda (combo) | `EVT-PAR-04` | acessório | CE | 3 | alterada | 1,5 | `CA-01` |

Em `EVT-PAR-01` *Pesquisar Participantes* o ticket alcançou só a pesquisa; as quatro listas de critérios — Legendas, Temas, Grupos de Trabalho e Cargo —, de 3 PF cada, não mudaram. Em `EVT-PAR-04` *Consultar Legenda do Participante* alcançou só a lista de legendas; o processo principal, de 4 PF, não entra. A mesma lista foi alterada também pelo ticket `PDTIC25148-34`: na sprint, ela conta uma vez.

## Funções de dados alteradas

Nenhuma. O critério de foto lê a foto que a pessoa já tinha, e as outras duas mudanças são de tela.

## Impacto em dicionários

- Nenhum. Os textos novos da tela — a caixa "Somente pessoas sem foto" e a dica "Abrir o perfil da pessoa em nova aba" — são rótulo e dica, e estão literais no N3 de `EVT-PAR-01` *Pesquisar Participantes*.

## Decisões de produto pendentes

- **Sem foto, mas só entre os confirmados.** O critério `CA-03` pede "somente as pessoas confirmadas no evento que não possuem foto"; a entrega traz todo participante cuja pessoa não tem foto, confirmado ou não — o recorte do ticket só sai combinando com Confirmado igual a Sim. O ticket também chama de "Pessoas Confirmadas" a lista que a tela chama de Lista de Participantes, e que não se limita aos confirmados. Decidir se o critério de foto deve embutir a confirmação. **Trava** o aceite do critério na homologação e a regra 10 de `EVT-PAR-01` *Pesquisar Participantes*.
- **"Assento livre" barrada só na tela.** O critério `CA-01` foi atendido tirando a opção da lista, e a opção é reconhecida pelo nome do bloco: o servidor continuaria aceitando a atribuição e, renomeado o bloco no catálogo, ele voltaria à lista 🔍. Com o catálogo editável de `PDTIC25148-34`, o nome deixou de ser fixo. Decidir se a restrição deve ser regra do sistema, e não só da tela. **Trava** a aprovação de `EVT-PAR-04` *Consultar Legenda do Participante* e de `EVT-PAR-05` *Alterar Legenda do Participante*.
- **Quem pode abrir o cadastro da pessoa pelo nome.** O critério `CA-02` fala em abrir o "perfil" da pessoa; a entrega abre a tela de edição, `PES-CAD-03` *Editar Pessoa*, para qualquer perfil que veja a lista, inclusive a Secretaria Check-In, e o endereço da tela não confere o perfil. Decidir quem pode chegar à edição por esse caminho, e se ele deveria abrir só para consulta. **Trava** a matriz de permissões do Feature Set Cadastro de Pessoas e a aprovação de `PES-CAD-03`.
- **Duas features tocadas sem critério próprio.** `EVT-PAR-05` *Alterar Legenda do Participante* e `PES-CAD-03` *Editar Pessoa* trazem no N3 uma consequência do ticket — a regra de que "Assento livre" não é atribuída e o segundo caminho de acesso à tela —, mas ficaram fora da `## Features`: o que cada uma grava e como grava não mudou, e os critérios pertencem à lista de legendas e à lista de participantes. Confirmar essa fronteira. **Trava** a contagem: dentro da AIM, cada uma entraria como alterada, a 50% do PFB — `EVT-PAR-05` vale 3 PF e entraria com 1,5; `PES-CAD-03` ainda não foi contada.

## Reconciliação

> Preenchida no fechamento (estado `concluído`): declarado × tocado. Escreva o resultado abaixo desta citação.

AIM aberta na entrega: o ticket foi entregue antes de haver escopo avalizado, então não há declarado × tocado a reconciliar. O changeset registra o que a especificação já tinha absorvido do ticket na engenharia reversa de 2026-09-30 e a contagem detalhada, feita e confirmada em 2026-10-04. Ficaram fora dele, de propósito, quatro tipos de artefato: o plano de testes, porque a instância roda no perfil `requisitos`, cuja esteira para no modelo de dados; o protótipo, porque a instância não tem nenhum e a referência dos N3 é a tela implementada; os repositórios de código, que estão fora do aval; e o `global/NFR.md`, porque o ticket não traz requisito não-funcional.

## Changelog

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-10-04 | Claude (apf-cpm) | Contagem detalhada | PFB e PFL das 2 features, espelhados dos N3: 7 PFB e 3,5 PFL, sem função de dados. Changeset sem linha `previsto`. A sprint passa a `SP005`. Continua em `em-análise`: falta só o aval do PO |
| 2026-10-04 | Claude (analise-impacto) | AIM aberta na entrega | ticket `PDTIC25148-35` registrado a partir da exportação do Jira de 2026-10-04, em homologação; 2 features de Participantes mapeadas, com os 3 critérios distribuídos sem repetição; elo fechado na `## Origem` dos N3 e no `modules/INDEX.md`. Fica em `em-análise`: faltam o aval do PO e a contagem detalhada |
