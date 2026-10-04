# MASTER.md
> Arquivo de contexto global, independente do módulo ou nível em trabalho.
> No Claude Code é carregado automaticamente a cada sessão via o `CLAUDE.md` da
> instância (ver `global/CLAUDE.md`); no fluxo copy-paste/CLI, cole-o em toda sessão.

---

## Identificação do sistema

- **Sigla**: GPE *3 letras — a convenção abaixo sugere 5; é a sigla que os documentos legados GPE001 a GPE006 já usam. No cadastro corporativo da CNI o mesmo sistema aparece com a sigla `SMC` e o código `652`*
- **Nome**: Portal de Gestão de Participantes em Eventos
- **Descrição**: Apoia a organização de reuniões e eventos com mesa da CNI: mantém as pessoas e os eventos, recebe as listas de convidados e confirmados, registra o check-in na recepção, monta o mapa de assentos e classifica os participantes por legenda.
- **Versão atual**: ❓ a definir
- **Repositório de docs**: gpe-doc (este repositório)

> O sistema tem três nomes em circulação e os três valem: **Portal de Gestão de Participantes em Eventos** (cadastro corporativo e tela de acesso), **Gestão de Participantes em Eventos** (cabeçalho das telas) e **Sistema de Mesa e Check-in** (nome dos repositórios de código e do projeto no Jira, *Solução para montagem e organização de mesas de reunião*). Esta documentação usa o primeiro.

> **Fonte única da identidade do sistema.** O N0 (`global/N0_PRODUCT_VISION.md`) repete a
> sigla no subtítulo, mas a **lê daqui** — não a redefine; o `validate-doc` reprova o N0 cuja
> sigla diverge desta. A descrição de uma frase aqui é o resumo; o `## Propósito` do N0 a desenvolve.
>
> A **sigla do sistema** (5 letras) identifica o produto como um todo e é **distinta** da
> `[SIGLA]` de **domínio** (3 letras, usada nos IDs `[SIGLA]-[SFS]-[NN]`) descrita
> na seção *Identificadores únicos* abaixo.

---

## Arquétipo do produto

<!--
  Declara o TIPO de produto que esta instância documenta. Linha máquina-legível:
  prompts e validadores (validate-doc.mjs) a leem para ligar/desligar exigências.
  Valores aceitos: transacional | ml-dados | cli-biblioteca. Ausente/valor
  desconhecido → transacional (comportamento clássico do framework).
-->

- **Arquétipo**: `transacional`

| Arquétipo | Quando usar | O que muda no framework |
|---|---|---|
| `transacional` | Sistema de negócio com UI + banco relacional (CRM, ERP, portais) | Comportamento clássico — nada muda |
| `ml-dados` | Pipelines de dados/ML: preparação, treino, avaliação, serving | N2: `Telas`/`Permissões por perfil` opcionais · N3: superfície típica `CLI`/`Job/Pipeline` com `## Execução e operação` no lugar de `## Comportamento de tela` · data-model pode usar o fragmento de **artefatos** (dataset/cache/checkpoint) · protótipos e APF opcionais (APF pressupõe transações de negócio) · engenharia reversa pela **Trilha B** do `PROMPT_REVERSE_ENGINEERING` |
| `cli-biblioteca` | Ferramentas de linha de comando, SDKs e bibliotecas | Igual a `ml-dados`, sem a ênfase em artefatos de dados — superfície típica `CLI`/`API` |

> A superfície de **cada feature** continua sendo declarada no `## Superfície` do N3 —
> o arquétipo dá o padrão do produto (e o validador usa a superfície da feature, não o
> arquétipo, para exigir `Comportamento de tela` vs `Execução e operação`). Um produto
> `transacional` pode ter features `Job` (ex.: *gerar cobrança mensal*) e um `ml-dados`
> pode ter uma tela de acompanhamento.

---

## Perfil de escopo

<!--
  Declara ATÉ ONDE na esteira esta instância vai. Linha máquina-legível:
  o PROMPT_MENU e o gates.py a leem para encurtar o fluxo. Valores aceitos:
  completo | requisitos. Ausente/valor desconhecido → completo (esteira inteira).
  As seções e itens técnicos deste arquivo (stack, repositórios, convenções de código,
  campos globais, padrão de API…) ficam entre os marcadores perfil:completo: o
  `init-instance --perfil requisitos` semeia o MASTER SEM eles, e o `completo`, com
  eles (os marcadores somem nos dois casos).
-->

- **Perfil**: `requisitos`

| Perfil | Quando usar | O que muda no framework |
|---|---|---|
| `completo` | Instância que documenta **e** leva ao código (spec → banco → testes → implementação) | Comportamento clássico — esteira inteira `requisitos → modelo-dados → testes → codigo`, todas as opções do menu |
| `requisitos` | Instância **só de requisitos**: para no negocial + data-model, sem passada técnica nem codificação | Menu só com as opções negociais (esconde 1B/2B/3B/4B, R1/R3/R4, Fase 5 e a exportação spec-kit) · esteira encurta para `requisitos → modelo-dados` (para em `modelo-validado`) · a camada de código (`mapa-codigo`, `valida-artefatos-previstos`, CI de código) fica inerte · o MASTER nasce **sem as seções técnicas** (stack, repositórios, convenções de código, campos globais, padrão de API) |

> O corte do perfil `requisitos` é no **3A**: mantém-se todo o lado negocial (N0, N1A, N2A, 3A, CRUD/Wizard, cenários, protótipos, auditoria, APF/NFR) **e o data-model** (`PROMPT_DATA_MODEL_negocio`, gate `modelo-dados`); a especificação técnica (3B) e a implementação ficam de fora. O perfil é ortogonal ao arquétipo: um `transacional` ou um `ml-dados` pode rodar em `completo` ou `requisitos`.

---

## Integrações externas

<!-- Sistemas de que este depende ou com que troca dados, na ótica do negócio: o que vem de cada um e como (integração via API, arquivo, referência digitada). Vale nos dois perfis — é daqui que saem as AIE da contagem (global/ALI-AIE-MAP.md) e as fontes `externo: [Sistema]` dos N3. -->

- **Serviços corporativos da CNI** (autenticação, configurações e cadastro básico) — integração via API. São eles que guardam usuário, senha, perfil, entidade e menu, e que decidem, a cada operação, se o perfil do usuário pode executá-la. O GPE não guarda usuário nem senha: as telas de acesso e de usuários operam sobre esse cadastro. Para usuário interno, o login precisa existir no diretório corporativo 🔍.
- **CRM da CNI (Dynamics 365)** — integração via API, só de leitura. Fornece os inscritos aprovados e confirmados de uma campanha, localizados pelo Código da Campanha do evento.
- **Planilhas extraídas do CRM** — arquivo. Trazem convidados, confirmados, grupos de trabalho, temas e histórico de participação; a pessoa é reconhecida pelo `Cód. Contato`, a chave do CRM.

---

## Identificadores únicos (IDs)

Cada nível da hierarquia de documentação possui um ID único para rastreabilidade
entre ferramentas externas (Jira, Azure DevOps, etc.).

| Nível | Formato | Exemplo |
|---|---|---|
| Ticket de origem (entrada) | chave da **ferramenta de origem** — externa, **não gerada aqui**; é a fonte de verdade do ticket. Tipos suportados: `servicenow` (`STRY…`), `issue` (`ISSUE-…`), `experimento` (`EXP-…`) — ver *Origem do ticket* abaixo | `STRY0012345` · `ISSUE-482` · `EXP-2026-003` |
| Major Feature Set (N1) | `[SIGLA]` — sigla do domínio (sempre 3 letras maiúsculas) definida na criação do domínio | `CRM` |
| Feature Set (N2) | `[SIGLA]-[SFS]` — sigla do domínio + sigla do Feature Set (sempre 3 letras maiúsculas) | `CRM-CLI` |
| Feature (N3) | `[SIGLA]-[SFS]-[NN]` — 2 dígitos sequenciais dentro do Feature Set | `CRM-CLI-01` |

**Regras:**
- O ticket entra pela ferramenta de origem; o framework **referencia** a chave (nunca cria ID próprio para o ticket), abre a AIM do ticket em `analise-impacto/AIM-<CHAVE>.md` e registra a chave na seção `## Origem` do N3
- A sigla do domínio é definida uma única vez na criação do N1 e nunca alterada
- A sigla do Feature Set é definida **no N1** (ao listar os Feature Sets do domínio) e **reutilizada** pelo N2; é única dentro do domínio e nunca reutilizada após exclusão; deriva do nome do Feature Set (ex.: Usuários → `USR`)
- A numeração de Features é sequencial dentro do Feature Set e não reutilizada após exclusão
- O ID fica no cabeçalho de cada artefato, logo abaixo da linha `**Nível X**`

### Origem do ticket (plugável)

<!--
  A ferramenta de onde vêm os tickets varia por organização: ServiceNow num time de
  produto corporativo, issues (GitHub/GitLab/Jira) num time OSS, registro de
  experimentos num time de pesquisa. Declare aqui a origem padrão desta instância;
  o front-matter de cada N3 registra `origem: { tipo, chave }` (o campo legado
  `servicenow:` de instâncias ≤1.5.x continua aceito pelos scripts).
  Os scripts de rastreabilidade reconhecem a chave pelo prefixo (STRY\d+ | ISSUE-\d+ |
  EXP-<id>) ou, em qualquer formato, pelo link da AIM (`AIM-<CHAVE>.md`).
-->

- **Origem padrão desta instância**: issue — Jira `sistemaindustria.atlassian.net`, projeto `PDTIC25148` (Solução para montagem e organização de mesas de reunião)

> As features desta instância nasceram por engenharia reversa (2026-09-30), a partir dos documentos legados GPE001 a GPE006 e do código. A `## Origem` de cada N3 cita o documento legado e, quando há, a chave do Jira **em texto**. Só os tickets com AIM aberta têm link na `## Origem` e linha na tabela de rastreabilidade do `modules/INDEX.md`: `PDTIC25148-34` e `PDTIC25148-35`, abertas na entrega em 2026-10-04.

| Tipo | Formato da chave | AIM em `analise-impacto/` | Exemplo |
|---|---|---|---|
| `servicenow` | `STRY` + dígitos | `AIM-STRY0012345.md` | `STRY0012345` |
| `issue` | `ISSUE-` + número | `AIM-ISSUE-482.md` | `ISSUE-482` |
| `experimento` | `EXP-` + identificador | `AIM-EXP-2026-003.md` | `EXP-2026-003` |

### Rastreabilidade ponta a ponta (ticket → spec → código)

Todo desenvolvimento começa por um ticket na ferramenta de origem e é
rastreável até o código pela cadeia de IDs:

```
Ticket ([tipo] [chave] — ex.: ServiceNow STRYxxxxxxx, issue ISSUE-123, experimento EXP-…)
   └─ AIM (analise-impacto/AIM-<CHAVE>.md)  ← o que o ticket pede, vai mudar e mudou
        └─ N3 Feature (SIGLA-SFS-NN)  ← seção "Origem" guarda a chave e o link da AIM
             └─ Código (commit/PR)    ← referencia a feature e o ticket
```

- **Ticket → N3**: a chave de origem é registrada na seção `## Origem` de
  cada feature, com o link da AIM; o elo recíproco é a `## Features` da AIM
  (`analise-impacto/AIM-<CHAVE>.md`). Cada
  critério de aceite é analisado e vira uma regra de negócio, um `## Cenário`
  (Gherkin) ou ambos — rastreabilidade semântica, não só por ID.
- **Critério de aceite → N3** *(quando a fonte numera)*: a coluna `Critérios
  cobertos` do `## Origem` abre com as referências `CA-n`, no mesmo número que a
  ferramenta de origem usa. É o elo que a **contagem por sprint** exige: cada
  feature impactada sai com a chave do ticket **e** o número do critério. Quando a
  fonte não numera os critérios, a coluna sai `—` e a rastreabilidade fica só pela
  chave — não se inventa número.
---

## Nomenclatura de features

Features são nomeadas sempre no **infinitivo**, seguindo o padrão:

**`Verbo + Entidade + Complemento (quando necessário)`**

| Regra | Exemplo |
|---|---|
| Criação | `Cadastrar Cliente` |
| Edição | `Editar Endereço de Entrega` |
| Exclusão | `Excluir Produto` |
| Listagem sem filtro | `Listar Pedidos` |
| Listagem com filtro | `Pesquisar Pedidos` |
| Ação específica | `Aprovar Solicitação de Crédito` |

**Regras:**
- Sempre infinitivo — nunca substantivo (`Cadastro de Cliente` ❌) nem gerúndio (`Cadastrando Cliente` ❌)
- Listagens que exibem apenas a lista, sem opções de filtro → verbo **Listar**
- Listagens que possuem campos de filtro ou busca → verbo **Pesquisar**
- Complemento é opcional — usar apenas quando necessário para distinguir features de mesma entidade

---

## Nomenclatura de entidades e campos

Entidades e campos são nomeados em **português**. A nomenclatura de campos segue
três camadas com responsabilidades distintas.
**A única fonte de verdade para Label Dev e campo banco é o `global/DATA-MODEL.md`.**
Os N3 usam apenas Label PO — nunca duplicam as camadas técnicas.

| Camada | Convenção | Exemplo | Onde aparece |
|---|---|---|---|
| Entidade | PascalCase singular, português | `ModeloEmail` | DATA-MODEL.md, data-models/[dominio].md (cabeçalho) |
| Label PO | Português, title case, sem jargão | `Nome completo` | N3 (tabela de campos), Gherkin, telas |
| Label Dev | camelCase, português, autoexplicativo | `nomeCompleto` | DATA-MODEL.md, código, API |
| Campo banco | snake_case, português ⚠️ | `nome_completo` | DATA-MODEL.md, migrations, ORM |

> ⚠️ Entidades e campos são nomeados em **português**. Confirme apenas a caixa
> dos identificadores do banco (snake_case vs. UPPER_SNAKE_CASE) antes de gerar
> N1/N3. Em engenharia reversa de bases legadas, transcreva os identificadores
> como estão na origem (podem estar em inglês) — não os traduza.

---

## Decisões transversais

> ⚠️ Itens marcados dependem de decisão do projeto.

1. **Exclusão**: lógica para o evento (o registro fica e deixa de ser exibido); física para a pessoa, a legenda e o preset de legendas. A pessoa só é excluída quando não participa de nenhum evento.
2. **Auditoria**: ⚠️ o sistema hoje **não registra quem fez** nenhuma ação. Guarda data de criação e de alteração da pessoa, data e hora do check-in, data da atribuição de legenda e data de criação do preset — e mais nada. O padrão do framework (ações críticas sempre em log de auditoria) não está atendido; ver `global/NFR.md`.
3. **Autorização**: o perfil vem do serviço corporativo. No servidor, a decisão é tomada por **recurso e tipo de operação** (consultar, incluir, alterar, excluir), não por funcionalidade; na interface, é o perfil que mostra ou esconde botões, colunas e telas. ⚠️ As duas camadas não coincidem em tudo — as diferenças estão anotadas na matriz `## Permissões por perfil` de cada N2. O padrão do framework (acesso por funcionalidade, `global/AUTHZ.md`) é a referência para a evolução, não o retrato do que existe.
4. **Chave da pessoa**: o `Cód. Contato` do CRM identifica a pessoa em todas as cargas e na importação de inscritos. ⚠️ O sistema não impede duas pessoas com o mesmo código.

---

## O que NUNCA fazer

- Duplicar Label Dev ou campo banco nos N3 — essas informações vivem apenas no DATA-MODEL.md

---

## Arquivos globais de referência

| Arquivo | Propósito |
|---|---|
| `CLAUDE.md` (raiz) | Índice de contexto carregado a cada sessão no Claude Code |
| `global/MASTER.md` | Identificação, perfil e convenções globais (este arquivo) |
| `global/DATA-MODEL.md` | Índice de entidades + campos globais + enums |
| `global/SIZING.md` | Convenções de contagem APF e COSMIC |
| `global/RULES-DICTIONARY.md` | Regras de negócio canônicas |
| `global/FIELD-DICTIONARY.md` | Campos canônicos (CPF, CEP, e-mail…) |
| `global/MESSAGE-DICTIONARY.md` | Mensagens de UI genéricas + baseline de validação |
| `global/ERROR-DICTIONARY.md` | Fonte única de códigos de erro |
| `global/API-PATTERNS.md` | Padrões de API |
| `global/AUTHZ.md` | Modelo de autorização — controle de acesso por funcionalidade (Feature = átomo de permissão) |
| `global/DESIGN-SYSTEM.md` | Padrões de UI |
| `global/PATTERNS.md` | Catálogo de padrões de projeto (design patterns) — como o sistema é construído no nível tático; consumido pelo `PROMPT_SDD` |
| `global/VOCABULARY-OVERRIDES.md` | *(opcional)* Ajustes de vocabulário desta instância (verbos/termos — ver FEATURE-DEFINITION) |
| `global/gates-config.yml` | *(opcional)* Papéis dos checkpoints CP1–CP4 desta instância (ver `scripts/gates.py`) |
