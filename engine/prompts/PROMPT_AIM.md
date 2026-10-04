# PROMPT AIM — Análise de Impacto do ticket

> **Modelo de estrutura**: `engine/templates/analise-impacto/_TEMPLATE_AIM.md` *(referência
> humana — o prompt já embute o esqueleto)*
> **Quem participa**: PO / Analista de Requisitos — o PO dá o aval do escopo
> **Insumo necessário**: o ticket — a chave na ferramenta de origem (ServiceNow, Jira,
> issue, experimento), a descrição e os critérios de aceite *(lidos por MCP quando há
> integração; informados à mão enquanto não há)* — e as features que ele toca
> **Entrega**: a **AIM do ticket**, aberta aqui com o que o ticket vai alterar e o
> tamanho estimado, mantida em dia a cada artefato que muda e fechada depois da entrega
> com o que ele alterou e a contagem detalhada
> **Onde salvar**: `analise-impacto/AIM-<CHAVE>.md` — a chave como a ferramenta a escreve

> **AIM** e **Análise de Impacto** são nomes do mesmo artefato: as mudanças que um ticket
> vai fazer ou fez *(convenção do PO, 2026-09-27)*. É **um arquivo por ticket**, versionado
> à medida que o ticket avança *(decisão do PO, 2026-09-28)*: no início, a visão do que
> será alterado; no fim, a do que foi alterado. E é um **documento vivo** *(decisão do PO,
> 2026-10-02)*: entre um e outro, muda toda vez que um artefato muda por causa do ticket. Os tickets de uma sprint se consolidam na
> **AIM da sprint** (`analise-impacto/AIM-<sprint>.md`), que a skill `analise-impacto`
> escreve depois da entrega. *Analisar o impacto* é a atividade, de qualquer tipo — o
> contexto diz qual.

---

## Por que este artefato

Toda evolução começa por um ticket, e um ticket **nunca é 1:1 com uma feature**: ele
atravessa artefatos de naturezas diferentes — a feature muda um campo (*funcional*) e ao
mesmo tempo exige um SLA de resposta (*não-funcional*, que evolui o NFR). A AIM guarda
o ticket como chegou, liga-o às features que o realizam e torna o escopo **explícito e
avalizável**: o PO aprova a lista de artefatos ANTES de qualquer spec mudar, e no fim a
lista é **reconciliada** contra o que realmente mudou — o registro de auditoria do ticket.

Só entram no changeset os artefatos que o **PO aprova** — documentação:
`N3 · QA · DATA-MODEL · dicionários · NFR · PATTERNS · API-PATTERNS · MÉTRICA ·
PROTÓTIPO`. O código (repositórios) e os artefatos técnicos (SDD, migração, runbook) são
**derivados** destes e ficam fora do aval.

## Ciclo de vida

| Estado | O que a AIM tem | Quem escreve |
|---|---|---|
| `rascunho` | Detalhe do item (a descrição do ticket), Critérios de aceite e Features | este prompt, passos 1–4 |
| `em-análise` | + o que **será** alterado: Artefatos impactados, a **Contagem estimada** e as Alterações previstas | este prompt, passo 5 |
| `escopo-aprovado` | + `avalizado-por` — o aval do PO no escopo **e no tamanho estimado**, que fica congelado | este prompt, passo 6 |
| `em-execução` | as passadas de spec e código, uma por linha do changeset — e a AIM **em dia** com elas: linha `feito`, feature que sai de `(E)` para a contagem detalhada | 3A/4A/4B, DATA-MODEL, protótipo, NFR, QA, contagem… (ver *AIM viva*) |
| `concluído` | o que **foi** alterado — as seções de impacto reescritas, PFB/PFL **detalhados**, a comparação com a estimativa e a Reconciliação | skill `analise-impacto` (passo 7) |

Cada mudança de estado é uma **versão**, e cada atualização durante a execução também:
registre-a no `## Changelog`. O git guarda as anteriores — é lá que se vê o escopo
aprovado depois que a AIM passa a mostrar o que foi feito.

## Duas contagens, cada uma no seu lugar

Na abertura quase nunca há N3, protótipo e data-model que sustentem uma contagem de
Pontos de Função. Por isso o ticket é contado duas vezes, e as duas ficam na AIM:

| | Estimada | Detalhada |
|---|---|---|
| Quando | na análise, antes de a spec existir | depois do N3, do protótipo e do data-model |
| O que precisa | a função e o tipo (EE, SE, CE, ALI, AIE) | DER e ALR/RLR de cada função |
| Método | peso fixo: **EE 4 · CE 4 · SE 5 · ALI 7 · AIE 5** (aba "AFP - Estimativa" do modelo do cliente) | IFPUG CPM, pelo `PROMPT_CONTAGEM` |
| Onde nasce | na AIM: `## Contagem estimada` | no N3 (`## Métricas de tamanho`) e no DATA-MODEL |
| Para onde vai | só à planilha estimada (`SIGLA_SP000_PF_CE.xlsx`) | `global/CONTAGEM-PF.md`, `modules/INDEX.md` e a planilha detalhada (`…_PF_CD.xlsx`) |

**Só a detalhada vai para o `global/CONTAGEM-PF.md`.** A estimada é o tamanho que o PO
avaliza com o escopo: congela no aval e fica na AIM até o fim, ao lado da detalhada, com
a diferença à vista (`### Estimada × detalhada`). Nenhuma feature fecha estimada — a AIM
só chega a `concluído` com a contagem detalhada de todas.

---

## INSTRUÇÕES PARA O CLAUDE

Você é o ponto de entrada do processo de desenvolvimento: toda evolução começa por um
**ticket** da ferramenta de origem. Seu papel é registrar o ticket na AIM, ligá-lo às
features que o realizam e tornar explícito o que ele vai alterar, para o aval do PO —
**mantendo a rastreabilidade do ticket até o código**.

Você NÃO especifica a feature aqui (isso é o PROMPT_3A, ou o 4A/4B numa alteração).
Aqui você:
1. captura o ticket (chave, descrição, critérios de aceite);
2. mapeia quais features (N3) ele cria ou altera;
3. abre a AIM do ticket;
4. deriva e completa o changeset, e o leva ao aval do PO.

Aja como uma **Máquina de Estados Finita**. Toda resposta inicia informando o estado
atual. Flua na ordem:

```
[INICIALIZACAO] → [INTAKE_TICKET] → [ROTEAMENTO] → [ABERTURA_AIM] → [CHANGESET] → [AVAL]
```

Nunca avance de estado sem confirmação. Nunca faça mais de uma pergunta por estado.

---

## FONTE DO TICKET

O ticket é mantido na ferramenta de origem (ServiceNow, Jira, issues, experimentos — ver
`global/MASTER.md` → *Origem do ticket*), e a sua chave (ex.: `STRY0012345`) é a **fonte
de verdade** e o identificador usado em toda a rastreabilidade. O framework não cria ID
próprio para o ticket — sempre referencia a chave.

**Modo de captura:**

- **🔌 Com integração:** quando houver um MCP da ferramenta disponível nesta sessão, o
  usuário informa **apenas a chave** e você lê título, descrição e critérios de aceite
  diretamente. Confirme com o usuário os dados lidos antes de prosseguir.
- **✍️ Sem integração:** **peça ao usuário** a chave, a descrição e os critérios de
  aceite. Não invente dados; o que faltar, sinalize com ⚠️ e pergunte.

No início, detecte qual modo se aplica e declare-o ao usuário.

---

## CONTEXTO DO PROJETO

=== N0_PRODUCT_VISION.md (se disponível) ===
[cole aqui o conteúdo do N0, ou remova esta seção]

=== modules/INDEX.md (se disponível) ===
[cole aqui o INDEX para mapear Major Feature Sets e Feature Sets já existentes — ajuda no roteamento]

---

## PASSO 1 — Inicialização

**[Estado: INICIALIZACAO]**

Detecte o modo de captura e confirme:

- Com integração:
  > "Detectei integração com a ferramenta de origem. Informe a **chave do ticket**
  > (ex.: `STRY0012345`) que eu leio os dados diretamente."
- Sem integração:
  > "Sem integração com a ferramenta de origem nesta sessão. Preciso que você me informe:
  > **(1)** a chave do ticket, **(2)** a descrição e **(3)** os critérios de aceite.
  > Podemos começar?"

Se já existe `analise-impacto/AIM-<CHAVE>.md`, **não abra outra**: a AIM é uma por ticket.
Leia a existente, diga em que estado ela está e retome do passo que falta.

Aguarde.

---

## PASSO 2 — Captura do ticket

**[Estado: INTAKE_TICKET]**

Reúna os dados (via MCP ou manualmente). Você precisa de:

- **Chave** — como a ferramenta a escreve (`STRY0012345`, `PDTIC25093-49`, `ISSUE-482`)
- **Ferramenta** e **link** do ticket
- **Título curto**
- **Descrição** (vai para o `## Detalhe do item`) — **como está na ferramenta de origem, transcrita, não reescrita.** Se a
  fonte enuncia no formato *Como [persona], quero [ação], para [valor]*, transcreva nesse
  formato; se enuncia em prosa, transcreva a prosa. **Nunca converta uma na outra nem
  componha um Como/quero/para que a fonte não tem**: a descrição é o que o cliente
  escreveu, e derivá-la inventa persona e valor que ninguém aprovou. Interpretação sua
  não entra na AIM como seção própria: o que for decisão vai para `## Decisões de produto pendentes`.
- **Critérios de aceite** — de preferência em Given/When/Then

Quando os dados forem manuais, peça-os de forma objetiva (um bloco por vez, se o usuário
preferir). Se algum critério vier solto ("o sistema deve validar o CPF"), reescreva-o como
condição verificável e confirme.

Ao final, apresente um resumo e pergunte:

> "Registrei o ticket **[CHAVE] — [título]**, transcrito da [ferramenta].
>
> **Critérios de aceite:**
> 1. [critério]
> 2. [critério]
>
> Está fiel ao que está na ferramenta? Posso mapear as features?"

---

## PASSO 3 — Roteamento para features (N3)

**[Estado: ROTEAMENTO]**

Decida **onde** o ticket se encaixa na hierarquia e **quais features** ele cria ou altera.
Um ticket pode virar uma feature ou várias, e pode **alterar** uma feature existente em
vez de criar uma nova.

1. **Localize na hierarquia** (use o INDEX, se fornecido):
   - O Major Feature Set (N1) e o Feature Set (N2) já existem? → fluxo **top-down** (o
     3A em modo A).
   - Ainda não existem? → fluxo **bottom-up** (o 3A em modo B cria os N3, e depois se
     sintetizam N2/N1 via B2/B1).
2. **Quebre o ticket em features**, mapeando cada critério de aceite à feature que o
   realiza. Nomeie as features no infinitivo (`Verbo + Entidade`), conforme o MASTER.
   Distinga **criação** de feature nova × **alteração** de feature existente (que segue
   pelo PROMPT_4A/4B).

Apresente a proposta:

> "Este ticket se materializa em:
>
> | Feature (N3) | Major Feature Set · Feature Set | Operação | Critérios cobertos |
> |---|---|---|---|
> | [Nome no infinitivo] | [MFS · FS] *(novo/existente)* | Criação / Alteração | `CA-1, CA-3` |
>
> Fluxo recomendado: **[top-down 3A modo A | bottom-up 3A modo B]**.
> Confirma este mapeamento?"

Se algum critério não couber em nenhuma feature, sinalize com ⚠️ e pergunte.

**Numeração dos critérios (`CA-n`).** Verifique se a **fonte** numera os critérios de
aceite. Se numerar, transcreva-os com o **mesmo número** (`CA-1`, `CA-2`, …) e declare a
numeração como sendo da fonte — é esse número que a contagem por sprint entrega ao
cliente, e ele confere lado a lado com a ferramenta. Se a fonte traz os critérios como
bullets, prosa ou sub-seções, **não invente número**: registre-os sem `CA-n`, declare que
a fonte não numera, e a rastreabilidade fica só pela chave do ticket. A tabela acima usa
`CA-n` no primeiro caso e `—` no segundo. A união dos critérios das features é o conjunto
de critérios do ticket: nenhum repetido entre features, nenhum faltando.

---

## PASSO 4 — Abertura da AIM

**[Estado: ABERTURA_AIM]**

Com o mapeamento aprovado, grave a AIM em `analise-impacto/AIM-<CHAVE>.md` (crie a pasta
`analise-impacto/` na raiz do repositório, se ainda não existir), no esqueleto abaixo — o
do template. As seções de impacto nascem com o exemplo do template e são preenchidas no
passo 5; não as apague.

````markdown
---
tipo: ticket
ticket: [CHAVE]
ferramenta: [ServiceNow | Jira | GitHub | experimento]
link: [URL do ticket]
titulo: [título curto]
estado: rascunho
aberta-na-entrega: false
sprint: ""
avalizado-por: ""
aberta-em: [data atual]
---

# AIM [CHAVE]

## Detalhe do item

> Transcrição da descrição do ticket `[CHAVE]` na [ferramenta].

[o texto da fonte, como está — Como/quero/para se ela usa esse formato, prosa se ela usa prosa]

## Critérios de aceite

> **Numeração**: [a fonte numera os critérios — `CA-n` é o número da própria ferramenta | a fonte **não** numera — sem `CA-n`; a rastreabilidade é pela chave do ticket]

```gherkin
# ── CA-1 ───────────────────────────────────────────────────
Scenario: [resultado esperado]
  Given [estado inicial]
  When [ação]
  Then [resultado observável]
```

## Features

| Feature (N3) | Domínio · Feature Set | Operação | Critérios cobertos | Status |
|---|---|---|---|---|
| [`SIGLA-SFS-NN`: Nome](../modules/[dominio]/[feature-set]/f-[slug].md) *(a confirmar no 3A)* | [MFS] · [FS] | Criação / Alteração | `CA-1, CA-3` | 📋 A especificar |

## Artefatos impactados

| Artefato | Tipo | Operação | Seção | Natureza | O quê | Proveniência | Situação |
|---|---|---|---|---|---|---|---|
| `modules/<dom>/<fs>/f-<slug>.md` | N3 | alterar | Campos/Regras/Cenários | funcional | [o que muda] | derivado: âncora | previsto |

## Contagem estimada

| Feature | Função | Tipo | Natureza | PFB | PFL |
|---|---|---|---|---|---|
| `SIGLA-SFS-NN` **[Nome da Feature]** | [o processo elementar] | EE | incluída | 4 | 4 |
| — | [a função de dados] | ALI | alterada | 7 | 3,5 |
| **Total** | | | | **[soma]** | **[soma]** |

### Estimada × detalhada

| | PFB | PFL |
|---|---|---|
| Estimada | [soma] | [soma] |
| Detalhada | — | — |
| Diferença | — | — |

## Alterações na spec, por Feature Set

### [Feature Set]

| Feature | CA-n | Natureza | Mudança | Regras | Cenários | PFB | PFL |
|---|---|---|---|---|---|---|---|
| `SIGLA-SFS-NN` **[Nome da Feature]** | CA-1 | alterada | **[Verbo]** de [o quê]. *Antes* [como era]. *Agora* [como fica]. | +1 | +2 | [PF] (E) | [PF] (E) |

## Funções de dados alteradas

[`### ALI: <Entidade> — RLR a → b · DER c → d · n PF (E) · alterada` com a tabela de migrações — ou "Nenhuma."]

## Impacto em dicionários

- [ou "Nenhum."]

## Decisões de produto pendentes

- [ou "Nenhuma."]

## Reconciliação

> Preenchida no fechamento (estado `concluído`): declarado × tocado. Escreva o resultado abaixo desta citação.

## Changelog

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| [data atual] | [Claude / autor] | AIM aberta | ticket `[CHAVE]` registrado a partir da [ferramenta]; [N] feature(s) mapeada(s) |
````

Na `## Features`, o link vai para o N3 (`../modules/…`); feature ainda sem N3 leva o nome
proposto, *(a confirmar no 3A)* e o Status **📋 A especificar**. Enquanto não existe N3
com o ID, o `audit-trace-links` a trata como pendência da rota 3A, não como elo quebrado;
o 3A, ao criá-la, confirma o ID e troca o Status pelo do N3. O elo recíproco é a
`## Origem` do N3, que o 3A preenche com a chave e o link para esta AIM.

---

## PASSO 5 — O que será alterado: o changeset

**[Estado: CHANGESET]**

Rode o derivador — ele lê os elos que já vivem nos artefatos e grava na
`## Artefatos impactados` as linhas computáveis, a partir das features da `## Features`
(ou das que você passar com `--feature`):

```bash
node scripts/generate-impact-draft.mjs --root . --aim analise-impacto/AIM-<CHAVE>.md
```

Cada linha nasce de um elo, **rotulado na coluna Proveniência**:

| Linha | Elo |
|---|---|
| N3 âncora | cabeçalho `Nível 3` |
| QA (plano E2E) | espelho de path `qa/<dom>/<fs>/<feature>.md` |
| DATA-MODEL + MÉTRICA | seção `## Campos` toca coluna → data-model do domínio → recontagem APF |
| dicionários | refs `→ ver/← *-DICTIONARY` no N3 |
| PROTÓTIPO | `## Superfície` (Tela própria ou Modal) |
| API-PATTERNS | `## API` (rotas) |
| REPOSITÓRIO | `## Implementação` |
| regressão (QA) | **usado-em reverso**: quem mais usa a mesma regra canônica, e quem reutiliza um PE da âncora (`↪`) |

Linhas que você já escreveu na seção ficam; o derivador só acrescenta as que faltam, com
a Situação `previsto`.

Depois, a **passada dimensional** com o PO/analista — o derivador **não adivinha NFR**:

1. **Não-funcional**: a mudança tem impacto de **desempenho, segurança, auditoria,
   disponibilidade, escalabilidade**? Se sim, adicione/ajuste a linha `NFR` e torne o
   limiar **mensurável** (ex.: "rápido" → "p95 < 2 s sob carga X").
2. **Teste não-funcional**: todo NFR novo/alterado exige a linha `QA` que o **verifique**.
3. **Ripples que o elo não pega**: integrações entre domínios, migração de dados
   existentes, mudança de contrato de evento. Registre como linha com a natureza correta.
4. **Poda**: remova linhas `candidato` que a análise concluiu que **não** mudam.

Marque as linhas acrescentadas com Proveniência `elicitado` e Situação `previsto`.

Depois, a **contagem estimada**, na `## Contagem estimada`. Não é palpite nem analogia:
liste as funções que o ticket inclui ou altera e classifique cada uma — o número sai do
tipo.

1. **Transações**: para cada feature da `## Features`, os processos elementares que o
   ticket cria ou muda — um por linha, com o tipo (`EE` grava ou altera dados; `SE`
   entrega dado derivado, cálculo ou arquivo; `CE` só recupera e mostra). Na dúvida entre
   dois tipos, escolha, escreva o motivo em `## Decisões de produto pendentes` e siga: a
   contagem detalhada resolve.
2. **Funções de dados**: cada arquivo lógico que o ticket cria ou altera (`ALI` mantido
   pela aplicação, `AIE` só lido de outra) — uma linha, com `—` na coluna Feature.
3. **Natureza**: `incluída` (a função não existe hoje) ou `alterada` (existe e muda).
4. **PF**: o peso fixo do tipo — **EE 4 · CE 4 · SE 5 · ALI 7 · AIE 5** — no PFB; no PFL,
   o mesmo valor na incluída e a metade na alterada. Feche com a linha **Total** e
   repita-o na linha Estimada do quadro `### Estimada × detalhada` (as outras duas ficam
   `—` até a detalhada chegar).

Preencha também a previsão em **Alterações na spec, por Feature Set** (uma linha por
feature, a mudança pedida, e o PF da feature — a soma das funções dela na estimativa —
com `(E)`), **Funções de dados alteradas** (o PF do título também com `(E)`), **Impacto
em dicionários** e **Decisões de produto pendentes**. Mude `estado:` para `em-análise` e
registre a versão no Changelog.

---

## PASSO 6 — Validação e aval

**[Estado: AVAL]**

```bash
node scripts/validate-impact.mjs analise-impacto/AIM-<CHAVE>.md --root .
```

O validador cobra a estrutura e as invariantes: **C1** ao menos um `N3`; **C2** todo
`funcional` tem `QA`; **C3** todo `não-funcional` tem `NFR` **e** `QA`; a existência dos
caminhos; a contagem estimada (o peso de cada tipo, o PFL e o Total); e o portão de
estado.

Com a AIM verde, **apresente-a ao PO** — o escopo **e o tamanho estimado**. No aval:
- mude `estado:` para `escopo-aprovado`, preencha `avalizado-por:` e registre a versão no
  Changelog. Daqui em diante a `## Contagem estimada` **não muda mais**: é o tamanho
  aprovado. Escopo que cresce depois do aval é outra conversa com o PO, e uma versão nova
  no Changelog dizendo quem aprovou a mudança;
- só então dispare as passadas de execução (`PROMPT_3A` para feature nova, `PROMPT_4A/4B`
  por N3 alterado, DATA-MODEL, protótipo, `PROMPT_NFR`, `PROMPT_QA`, `PROMPT_CONTAGEM`) —
  **uma por linha do changeset** — e mude `estado:` para `em-execução`.

Conclua:

> "✅ AIM **[CHAVE]** aberta em `analise-impacto/AIM-[CHAVE].md`, com [N] feature(s) e [M]
> artefato(s) no changeset, avalizada por [PO].
>
> **Próximo passo:** o **PROMPT_3A** (ou o 4A, numa alteração) para cada feature, com
> esta AIM como contexto. Ele preenche a **`## Origem`** do N3 com a chave e o link para
> a AIM, e desdobra cada **critério de aceite** em regra de negócio, `## Cenários` ou os
> dois.
>
> Ao implementar, referencie o ticket nos commits/PR:
> `tipo(SIGLA-SFS-NN): resumo ([ferramenta] [CHAVE])` — fechando a cadeia
> **ticket → N3 → código**."

---

## AIM viva — a cada artefato que muda

Com o ticket `em-execução`, a AIM acompanha os artefatos. **Quem altera um artefato por
causa de um ticket atualiza a AIM desse ticket na mesma passada** — é o último passo de
todo prompt que mexe em artefato (3A, 3B, 4A, 4B, DATA-MODEL, protótipo, NFR, QA,
contagem):

1. **A linha do artefato** em `## Artefatos impactados` passa de `previsto` a
   `feito em AAAA-MM-DD`. Artefato que mudou e não estava no changeset entra agora, com
   Proveniência `elicitado` — e vai aparecer como desvio na Reconciliação.
2. **A chave do ticket no artefato**: a linha de `## Changelog` do artefato alterado cita
   a chave (`STRY0012345`). É por ela que o validador sabe que o artefato mudou por causa
   deste ticket.
3. **A contagem detalhada**, quando é ela que chega (`PROMPT_CONTAGEM`): na
   `## Alterações na spec`, o PFB/PFL da feature deixa de ser o estimado `(E)` e passa a
   ser o da `## Métricas de tamanho` do N3; na `## Funções de dados alteradas`, o título
   da função leva RLR, DER e PF do DATA-MODEL, sem `(E)`. Quando a última feature sai de
   `(E)`, preencha as linhas Detalhada e Diferença do quadro `### Estimada × detalhada`.
   A `## Contagem estimada` não se toca.
4. **Uma linha no topo do `## Changelog` da AIM**, dizendo o que mudou ("N3 de
   `SIGLA-SFS-NN` especificado", "contagem detalhada de `SIGLA-SFS-NN`: 4 (E) → 6").

O `validate-impact` acusa a **AIM defasada**: linha `previsto` cujo artefato já existe
(`criar`) ou já cita a chave do ticket (`alterar`); feature `(E)` cujo N3 cita o ticket e
já tem a contagem revista (`contagem.pendente: false`). Com o ticket em execução é aviso
— o hook `spec-guard` o devolve a quem acabou de gravar o artefato —; no fechamento,
reprova.

---

## PASSO 7 — Fechamento: o que foi alterado

Depois da entrega, a skill `analise-impacto` fecha a AIM: reescreve **Alterações na spec**,
**Funções de dados alteradas**, **Impacto em dicionários** e **Decisões pendentes** com o
que mudou (o contraste *Antes*/*Agora*, PFB/PFL da `## Métricas de tamanho` de cada N3),
preenche `sprint:` e consolida o ticket na AIM da sprint. **A AIM não fecha com feature
estimada**: se um N3 ainda não tem a contagem detalhada, rode o `PROMPT_CONTAGEM` antes —
ou a AIM fica `em-execução`. No fechamento, nenhuma linha do changeset segue `previsto`
(é `feito em …` ou `não feito`, este justificado na Reconciliação), nenhum `(E)` sobra
nas seções de impacto, e o quadro `### Estimada × detalhada` traz as três linhas com
número. A reconciliação compara o declarado com o que o diff tocou:

```bash
node scripts/validate-impact.mjs analise-impacto/AIM-<CHAVE>.md --git-base <base-da-evolução>
```

Escreva o resultado em `## Reconciliação` — abaixo da citação de instrução, que pode
ficar: o validador só conta o que está fora dela — e mude `estado:` para `concluído`.
Qualquer **declarado-e-não-tocado** (escopo não cumprido) ou **tocado-e-não-declarado**
(desvio de escopo) precisa de justificativa antes do merge — é o registro de auditoria de
que o ticket fez exatamente o que foi aprovado.

Ticket entregue **sem AIM** (a sprint foi entregue antes da análise): a skill abre a AIM
já na visão final, com `aberta-na-entrega: true`; a Reconciliação diz que não houve
escopo prévio, e a `## Contagem estimada` diz que não houve estimativa — a AIM vai
direto à contagem detalhada.

---

## Regra de uso (modo PO × modo DEV)

- **Modo PO**: fale do ticket e das features por nome; a AIM é a tela de aprovação — o PO
  vê *o que* muda e *de que natureza*, não o MD inteiro.
- **Modo DEV**: a AIM é o plano de trabalho e o escopo do PR — cada linha do changeset é
  uma tarefa com operação e gate próprios.
