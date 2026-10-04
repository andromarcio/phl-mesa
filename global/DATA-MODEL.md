<!-- docqui: 4.0.2 | prompt: PROMPT_CONTAGEM | atualizado: 2026-10-04 -->
# DATA-MODEL.md
> **Índice e fonte de verdade** para nomenclatura e mapeamento de campos.
> Os modelos detalhados estão fragmentados por domínio em `global/data-models/`
> para otimizar o contexto enviado ao LLM — cole apenas o fragmento do
> domínio que está sendo trabalhado, não o arquivo inteiro.
>
> **Fonte única de definição de banco.** Toda definição física — entidade/tabela,
> Label Dev, campo banco, tipo SQL, FK, índice, restrição de unicidade e enum —
> vive **exclusivamente** aqui (índice) e nos fragmentos `global/data-models/`.
> Qualquer outro artefato (N0–N3, SDD, protótipo, contagem) **referencia**, nunca
> redefine: `→ ver DATA-MODEL.md: Entidade [Nome]`. Os N3 usam só Label PO e
> **nunca** duplicam Label Dev, campo banco, tipo ou FK em suas tabelas.

---

## Convenção de nomenclatura

| Camada | Convenção | Exemplo | Onde aparece |
|---|---|---|---|
| Entidade | PascalCase singular, português | `ModeloEmail` | **data-models/[dominio].md** (cabeçalho), "Modelos por domínio" |
| Label PO | Português, title case, sem jargão | `Nome completo` | N3 (campos), Gherkin, telas |
| Label Dev | camelCase, português, autoexplicativo | `nomeCompleto` | **data-models/[dominio].md** — apenas aqui |
| Campo banco | snake_case, português ⚠️ | `nome_completo` | **data-models/[dominio].md** — apenas aqui |

> ⚠️ Entidades e campos em **português**. Confirme apenas a caixa dos identificadores
> (snake_case vs. UPPER_SNAKE_CASE) antes de implementar; em engenharia reversa,
> transcreva a origem como está — não traduza.

---

## Campos globais (presentes em todas as tabelas)

Estão implícitos — não precisam ser listados nos arquivos de domínio.

> ⚠️ **No GPE só o Identificador é comum a todas as entidades** (engenharia reversa de 2026-09-30 💻). Data de criação e data de alteração existem apenas na pessoa; data de criação, também na legenda do participante e no preset; exclusão lógica, apenas no evento — e como indicador sim·não, não como data. Por isso os fragmentos de domínio listam esses atributos entidade a entidade. A tabela abaixo é a convenção do framework, mantida como referência para uma evolução.

| Label PO | Label Dev | Campo banco | Tipo SQL | Notas |
|---|---|---|---|---|
| Identificador | id | id | [tipo PK] | PK; gerada automaticamente |
| Data de criação | createdAt | created_at | [timestamp] | Gerado automaticamente |
| Data de atualização | updatedAt | updated_at | [timestamp] | Atualizado automaticamente |
| Data de exclusão | deletedAt | deleted_at | [timestamp] | Exclusão lógica (soft delete); null = ativo |

---

## Modelos por domínio

<!--
  Tipo do fragmento: `entidades` (tabelas relacionais — padrão) ou `artefatos`
  (datasets/caches/checkpoints — modelo `data-models/_template-artefatos.md`,
  típico do arquétipo ml-dados). Um domínio pode ter os dois fragmentos.
-->

| Domínio | Arquivo | Tipo | Entidades/Artefatos |
|---|---|---|---|
| Acesso e Usuários | [data-models/acesso-usuarios.md](./data-models/acesso-usuarios.md) | entidades (negocial) | Usuario, PerfilAcesso — ⚠️ mantidas no cadastro corporativo da CNI, não no banco do GPE |
| Pessoas | [data-models/pessoas.md](./data-models/pessoas.md) | entidades (negocial) | Pessoa, GrupoTrabalhoPessoa, TemaPessoa, HistoricoPessoa, Arquivo |
| Eventos | [data-models/eventos.md](./data-models/eventos.md) | entidades (negocial) | Evento, TipoEvento, TipoMesa, CadeiraMesa, EventoPessoa, Legenda, EventoLegenda, EventoLegendaCondicao, EventoPessoaLegenda, PresetLegenda |

> Os três fragmentos são **negociais** (perfil `requisitos`): atributos em Label PO, sem camada física. A estrutura física existe e está no repositório `sistema_mesa_checkin_backend` (`db/migrations` e pacote `domain`) — ver `repos/sistema_mesa_checkin_backend.md`.

---

## Enums do sistema

| Enum | Campo banco | Valores | Usado em |
|---|---|---|---|
| Sexo | — | Masculino, Feminino, Não informado | Pessoa.Sexo |
| Estado (UF) | — | AC, AL, AP, AM, BA, CE, DF, ES, GO, MA, MT, MS, MG, PA, PB, PR, PE, PI, RJ, RN, RS, RO, RR, SC, SP, SE, TO | Pessoa.Estado · Pessoa.Estado da organização |
| Origem do cadastro | — | Cadastro, Carga, Recepção | Pessoa.Origem do cadastro |
| Disposição da mesa | — | Retangular, Retangular Invertido | TipoMesa.Disposição |
| Composição da mesa | — | Principal, Lateral | CadeiraMesa.Composição |
| Campo da condição | — | Grupo de trabalho, Tema, Cargo, Nome fantasia, Papel desempenhado | EventoLegendaCondicao.Campo |
| Operador da condição | — | Igual a, Diferente de, Contém, Em (lista) | EventoLegendaCondicao.Operador |
| Conectivo da condição | — | E, OU | EventoLegendaCondicao.Conectivo |
| Tipo de perfil | — | DN, DR, UA — Departamento Nacional, Departamento Regional e Unidade 🔍 | PerfilAcesso.Tipo |

> A coluna do nome físico fica sem preenchimento: esta instância é de perfil `requisitos` e não mantém a camada física. Tipo de evento (Reunião, Comitê, Seminário) e tipo de mesa **não** são listas fixas: são entidades, com registros mantidos fora das telas.

---

## Campos adicionados recentemente

| Data | Entidade | Label PO | Label Dev | Campo banco | Tipo | N3 de origem |
|---|---|---|---|---|---|---|
| — | — | — | — | — | — | Nenhum campo foi acrescentado depois da engenharia reversa de 2026-09-30 |

---

## Relacionamentos

```
PerfilAcesso 1──N Usuario                  (cada usuário tem um perfil — cadastro corporativo)

Pessoa 1──N GrupoTrabalhoPessoa            (grupos de trabalho da pessoa, com o papel)
Pessoa 1──N TemaPessoa                     (temas a que a pessoa se vincula)
Pessoa 1──N HistoricoPessoa                (participações por ano)
Pessoa N──1 Arquivo                        (foto, quando há)

Evento N──1 TipoEvento
Evento N──1 TipoMesa
Evento N──1 Arquivo                        (imagem do evento, quando há)
Evento 1──N CadeiraMesa                    (assentos do mapa)
Evento 1──N EventoPessoa                   (participantes)
Pessoa 1──N EventoPessoa                   (eventos de que a pessoa participa)
CadeiraMesa 1──1 EventoPessoa              (quem ocupa o assento, quando ocupado)

Evento 1──N EventoLegenda                  (blocos de legenda do evento, em ordem)
Legenda 1──N EventoLegenda                 (eventos em que o bloco está em uso)
EventoLegenda 1──N EventoLegendaCondicao   (condições do bloco, em ordem)
EventoPessoa 1──N EventoPessoaLegenda      (legendas do participante no evento)
Legenda 1──N EventoPessoaLegenda           (participantes que receberam a legenda)
```

---

## Relacionamentos de seleção (comboboxes)

> Fonte de verdade para campos que, na tela, são uma **combobox/seleção cujas
> opções vêm de outra entidade** (chave estrangeira com exibição de label).
> Um campo do N3 com tipo `seleção → [Entidade]` referencia uma linha desta tabela.
> O agente de implementação usa estas colunas para resolver a consulta sozinho:
> grava o **campo-valor**, exibe o **campo-label** e busca as opções no **endpoint origem**.

| Campo (FK) | Entidade origem | Campo-valor | Campo-label | Endpoint origem | Filtro de origem |
|---|---|---|---|---|---|
| — | — | — | — | — | Não mantido nesta instância (perfil `requisitos`): a origem de cada seleção está na coluna **Entidade** de `## Campos` do N3 |

**Significado das colunas:**
- **Campo (FK)** — Label Dev do campo que armazena a referência; termina em `Id`. É uma FK.
- **Entidade origem** — entidade de onde vêm as opções; deve existir em "Modelos por domínio".
- **Campo-valor** — o que é gravado no banco. Quase sempre o `id` da entidade origem.
- **Campo-label** — Label Dev exibido na combobox (ex: `nomeCompleto`, `razaoSocial`).
- **Endpoint origem** — rota de coleção que retorna as opções (paginada, com `?search=` para autocomplete). **Nunca** um endpoint novo dedicado — reusa a coleção da entidade.
- **Filtro de origem** — restrição de negócio sobre quais registros podem aparecer (ex.: "apenas ativos").

> A **estratégia de carga** (lista completa vs. autocomplete por digitação) é decisão
> de cada feature e fica no N3 (coluna Validação do campo), não aqui.

---

## Índices e restrições de unicidade

| Tabela | Campos | Tipo | Justificativa |
|---|---|---|---|
| Legenda | Nome da legenda | UNIQUE | Não há dois blocos de legenda com o mesmo nome |
| PresetLegenda | Nome do preset | UNIQUE | Não há dois presets com o mesmo nome |
| EventoLegenda | Evento + Legenda | UNIQUE | A mesma legenda aparece uma só vez na configuração do evento |
| EventoPessoaLegenda | Participante + Legenda | UNIQUE | O participante não recebe a mesma legenda duas vezes |

> ⚠️ **Unicidades que o sistema não garante** 💻: o `Cód. Contato` (CRM) da pessoa, o CPF da pessoa, o par evento + pessoa da participação e o par evento + assento. As quatro são premissas do negócio sem proteção — ver `REVISAO-CONVERSAO.md`.

---

## Arquivos Lógicos (APF)

> Registro central de ALIs e AIEs do sistema.
> Mantido via atualização dos fragmentos `global/data-models/[dominio].md`.
> A contagem de DER **exclui** os campos globais técnicos (createdAt, updatedAt, deletedAt) e conta o `id` como **1 DER por ALI**, não por tabela — ver `global/SIZING.md`.
> **RLR** (Registro Lógico Referenciado = IFPUG RET) e **DER** (Dado Elementar Referenciado = IFPUG DET) determinam a complexidade — ver `global/SIZING.md`.

### ALIs — Arquivos Lógicos Internos

| ALI | Domínio | Entidades constituintes | RLR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Evento | Eventos | Evento (principal) · CadeiraMesa, EventoPessoa, EventoLegenda, EventoLegendaCondicao, EventoPessoaLegenda (subgrupos) | 6 | 33 | Alta | 15 | 2026-10-04 |
| Legenda | Eventos | Legenda (principal) | 1 | 3 | Baixa | 7 | 2026-10-04 |
| PresetLegenda | Eventos | PresetLegenda (principal) | 1 | 5 | Baixa | 7 | 2026-10-04 |

**Total ALIs: 29 PF** *(só o domínio Eventos, contado em 2026-10-04; os de Pessoas e de Acesso e Usuários ainda não foram dimensionados — a memória de cálculo está em `global/data-models/eventos.md`)*

### AIEs — Arquivos de Interface Externa

| AIE | Sistema externo | Entidades / estruturas usadas | RLR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|

**Total AIEs: nenhum dimensionado** *(as features contadas até aqui não leem arquivo de outra aplicação; os candidatos — o cadastro corporativo de usuários e perfis da CNI e os inscritos do CRM — serão avaliados na contagem das features que os usam)*

---

> ℹ️ **Como manter esta seção**
> 1. Ao criar ou alterar uma entidade num fragmento `data-models/[dominio].md`,
>    atualize a linha do ALI correspondente (RLR, DER, Complexidade, PF).
> 2. Se uma nova entidade formar um ALI novo, adicione a linha aqui
>    **e** anote o ALI no cabeçalho da entidade no fragmento do domínio.
> 3. Entidades de suporte (tabelas de junção, tabelas de auditoria) geralmente
>    não formam ALI próprio — pertencem ao ALI da entidade principal.
