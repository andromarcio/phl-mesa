<!-- docqui: {{VERSION}} | prompt: PROMPT_AIM | atualizado: {{YYYY-MM-DD}} -->
---
tipo: ticket
ticket: [STRYxxxxxxx | ISSUE-NNN | EXP-… | PDTIC…-NN]
ferramenta: [ServiceNow | Jira | GitHub | experimento]
link: [URL do ticket na ferramenta de origem]
titulo: [título curto do ticket]
estado: rascunho          # rascunho → em-análise → escopo-aprovado → em-execução → concluído
aberta-na-entrega: false  # true quando a AIM nasce depois da entrega (skill analise-impacto)
sprint: ""                # sprint que atende o ticket — no planejamento, se já se sabe; obrigatória no fechamento
avalizado-por: ""         # aval do PO no escopo — obrigatório de escopo-aprovado em diante
aberta-em: [AAAA-MM-DD]
---

<!--
  AIM — ANÁLISE DE IMPACTO DO TICKET. Um arquivo por ticket, em
  `analise-impacto/AIM-<CHAVE>.md` (a chave como a ferramenta a escreve:
  `AIM-STRY0012345.md`, `AIM-PDTIC25093-49.md`). É o único artefato do ticket no
  framework: o que o ticket pede, o que ele vai mudar e, no fim, o que ele mudou.
  A AIM é um DOCUMENTO VIVO, versionado à medida que o ticket avança — o Changelog
  registra cada versão e o git guarda as anteriores:

    rascunho         aberta: Detalhe do item, Critérios e Features (PROMPT_AIM, passos 1–4)
    em-análise       o que SERÁ alterado: Artefatos impactados, a Contagem estimada e as
                     Alterações previstas (passo 5)
    escopo-aprovado  o PO avalizou o escopo e o tamanho estimado (`avalizado-por`) — só
                     então a spec muda (passo 6)
    em-execução      as passadas de spec e código, uma por linha do changeset. A CADA
                     artefato que muda por causa do ticket, a AIM muda junto: a linha do
                     artefato passa a `feito`, e a feature que ganhou a contagem detalhada
                     no N3 troca o `(E)` pelo PF medido
    concluído        o que FOI alterado: as seções de impacto reescritas com o que mudou,
                     PFB/PFL detalhados — nenhuma feature fecha estimada —, a comparação
                     com a estimativa e a Reconciliação com o escopo aprovado (skill
                     analise-impacto, PROMPT_AIM passo 7)

  AIM DEFASADA é a que ficou para trás dos artefatos: a linha segue `previsto` e o
  artefato já mudou; a feature segue `(E)` e o N3 já tem a contagem. O `validate-impact`
  avisa enquanto o ticket está em execução e REPROVA no fechamento.

  Front-matter: fonte única dos metadados — o HTML da AIM o mostra como ficha.
    ticket · ferramenta · link · titulo → o ticket na ferramenta de origem; a chave é a
      FONTE DE VERDADE e o identificador em toda a rastreabilidade (o framework não
      cria ID próprio para o ticket).
    aberta-na-entrega → a AIM nasceu depois da entrega, sem escopo prévio a
      reconciliar: C2 e C3 viram aviso, e a Reconciliação diz isso.
    sprint → a sprint que atende o ticket; é por ela que a AIM da sprint
      (`analise-impacto/AIM-<sprint>.md`) consolida os tickets, e que a planilha
      estimada (`--estimada --sprint`) junta as estimativas.
  Dentro do front-matter, comentário só no fim da linha: linha que começa com `#` seria
  lida como o título do arquivo.
-->

# AIM [CHAVE]

## Detalhe do item

<!--
  O detalhe do item é a descrição do ticket.
  TRANSCRIÇÃO, não formulação. Cole aqui a descrição como ela está na ferramenta de
  origem. Se a fonte enuncia no formato Como/quero/para, transcreva nesse formato; se
  enuncia em prosa, transcreva a prosa. NUNCA converta uma na outra nem componha um
  Como/quero/para que a fonte não tem — derivá-lo inventa persona e valor que ninguém
  aprovou. O que você concluir a partir dela não entra aqui: o que for decisão vai para
  `## Decisões de produto pendentes`.
-->

> Transcrição da descrição do ticket `[CHAVE]` na ferramenta de origem.

[o texto da fonte, como está]

## Critérios de aceite

<!--
  Cada critério é analisado no N3 e vira regra de negócio (se expressa uma invariante),
  um `## Cenários` (Gherkin, se descreve comportamento observável) ou os dois.

  NUMERAÇÃO `CA-n` — a contagem por sprint cita o critério pelo número, para o cliente
  conferir lado a lado com a ferramenta. Só numere quando a FONTE numerar, e com o MESMO
  número dela. Se a fonte traz os critérios como bullets, prosa ou sub-seções, NÃO
  invente número: deixe a lista sem `CA-n` e declare isso abaixo — a rastreabilidade
  fica pela chave do ticket, e a coluna CA-n sai `—`. Número inventado aqui vira número
  errado no relatório do cliente.
-->

> **Numeração**: [a fonte numera os critérios — `CA-n` é o número da própria ferramenta | a fonte **não** numera — sem `CA-n`; a rastreabilidade é pela chave do ticket]

```gherkin
# ── CA-1 ───────────────────────────────────────────────────
Scenario: [resultado esperado em linguagem de negócio]
  Given [estado inicial]
  When [ação do usuário]
  Then [resultado observável]
```

## Features

<!--
  As features (N3) que realizam o ticket. Relação M:N: um ticket pode ser realizado por
  várias features, e uma feature atende a vários tickets. É o elo recíproco da
  `## Origem` de cada N3 — os dois lados precisam dizer o mesmo, e o
  `audit-trace-links` confere. Preencha no roteamento (PROMPT_AIM, passo 3) e mantenha
  o Status em dia (o ícone do `estado` do N3, da legenda do modules/INDEX.md). Feature
  que o ticket cria e que ainda não tem N3: nome proposto, *(a confirmar no 3A)* e o
  Status `📋 A especificar` — o `audit-trace-links` a trata como pendência até o 3A
  criá-la e trocar o Status.

  A união dos `CA-n` das features é o conjunto de critérios do ticket: nenhum repetido
  entre features, nenhum faltando. Critério sobrando é feature que falta; critério
  repetido é fronteira mal traçada entre duas features.

  CARIMBO DE VERIFICAÇÃO (elo suspeito): depois de fechar ou rever o elo, rode
  `node scripts/suspect-links.mjs --stamp --file <este arquivo>` — ele grava aqui um
  comentário `<!- - trace-verified: [ID da feature] @ fingerprint - ->` por feature. Se
  a Descrição ou os Critérios mudarem depois disso, o `suspect-links` acusa o elo como
  suspeito. Não edite os carimbos à mão.
-->

| Feature (N3) | Domínio · Feature Set | Operação | Critérios cobertos | Status |
|---|---|---|---|---|
| [`SIGLA-SFS-NN`: Nome da Feature](../modules/[dominio]/[feature-set]/f-[slug].md) | [Major Feature Set] · [Feature Set] | Criação / Alteração | `CA-1, CA-3` | ✏️ Rascunho |

## Artefatos impactados

> O **changeset**: os artefatos de documentação que o ticket vai criar ou alterar,
> aprovados pelo PO ANTES de qualquer um deles mudar. Linhas `derivado:` nascem dos elos
> (`node scripts/generate-impact-draft.mjs --aim <este arquivo>`); linhas `elicitado`
> vêm da passada do analista (NFR e limiares de teste não-funcional não são deriváveis).
> Só documentação entra aqui — código e artefatos técnicos (SDD, migração, runbook)
> derivam destes e ficam fora do aval.
>
> Invariantes (o `validate-impact` cobra): **C1** ao menos uma linha `N3`; **C2** toda
> linha `funcional` tem uma linha `QA`; **C3** toda linha `não-funcional` tem `NFR`
> **e** `QA`.

| Artefato | Tipo | Operação | Seção | Natureza | O quê | Proveniência | Situação |
|---|---|---|---|---|---|---|---|
| `modules/<dom>/<fs>/f-<slug>.md` | N3 | alterar | Campos/Regras/Cenários | funcional | [o que muda] | derivado: âncora | previsto |
| `qa/<dom>/<fs>/<slug>.md` | QA | criar | — | funcional | plano E2E | derivado: espelho do N3 | previsto |

> Tipos: `N3 · QA · DATA-MODEL · FIELD-DICT · RULES-DICT · MESSAGE-DICT · ERROR-DICT ·
> NFR · PATTERNS · API-PATTERNS · MÉTRICA · PROTÓTIPO · REPOSITÓRIO`.
> Operação: `criar | alterar | deprecar`.
> Situação: `previsto` até o artefato mudar · `feito em AAAA-MM-DD` quando ele mudou por
> causa deste ticket — quem altera o artefato atualiza a linha na mesma passada, e cita a
> chave do ticket no Changelog do artefato · `não feito` no que o fechamento deixou de
> fora, com a justificativa na Reconciliação. Nenhuma linha fecha `previsto`.

## Contagem estimada

<!--
  O TAMANHO ESTIMADO do ticket — o que o PO avaliza junto com o escopo, quando ainda não
  há N3, protótipo nem data-model que sustentem a contagem detalhada. Basta a FUNÇÃO e o
  TIPO: uma linha por processo elementar (EE, SE, CE) e por função de dados (ALI, AIE)
  que o ticket inclui ou altera, com o peso fixo da aba "AFP - Estimativa" do modelo do
  cliente:

      EE 4 · CE 4 · SE 5 · ALI 7 · AIE 5

  PFL = PFB na função incluída; metade na alterada. Função de dados não tem feature: a
  coluna Feature sai `—`. O `validate-impact` confere o peso, o PFL e o Total.

  CONGELADA NO AVAL: de `escopo-aprovado` em diante esta tabela não muda — é o tamanho
  que o PO aprovou. A contagem detalhada NÃO a substitui: nasce no N3 (`## Métricas de
  tamanho`) e no DATA-MODEL, é consolidada em `global/CONTAGEM-PF.md` e entra na AIM
  pela `## Alterações na spec` e pelo quadro `### Estimada × detalhada`. A estimada
  NUNCA vai para o N3, para o consolidado nem para o `modules/INDEX.md`: é só daqui e da
  planilha estimada (`gera-planilha-contagem.py --estimada`, `SIGLA_SP000_PF_CE.xlsx`).

  AIM aberta na entrega (`aberta-na-entrega: true`): não houve estimativa. Escreva
  "Não houve — AIM aberta na entrega." e apague as duas tabelas.
-->

| Feature | Função | Tipo | Natureza | PFB | PFL |
|---|---|---|---|---|---|
| `SIGLA-SFS-NN` **[Nome da Feature]** | [o processo elementar] | EE | incluída | 4 | 4 |
| — | [a função de dados] | ALI | alterada | 7 | 3,5 |
| **Total** | | | | **[soma]** | **[soma]** |

### Estimada × detalhada

<!--
  A diferença à vista. A linha Estimada repete o Total acima. A Detalhada entra quando a
  contagem detalhada do ticket fecha: a soma do PFB/PFL da `## Alterações na spec` com o
  das `## Funções de dados alteradas`. Até lá, `—`. No fechamento as três são número, e o
  `validate-impact` confere a conta.
-->

| | PFB | PFL |
|---|---|---|
| Estimada | [soma] | [soma] |
| Detalhada | — | — |
| Diferença | — | — |

## Alterações na spec, por Feature Set

<!--
  O DELTA FUNCIONAL, por Feature Set, uma linha por feature — as novas também.
  Enquanto a feature não tem a contagem detalhada, é o PREVISTO: a mudança que o ticket
  pede, e o PF da `## Contagem estimada` (a soma das funções da feature) marcado `(E)`.
  O `(E)` é a marca de "ainda estimada": sai da linha quando o N3 da feature ganha a
  `## Métricas de tamanho` revista para este ticket — aí o PFB/PFL é o do N3, e a tabela
  espelha o N3, nunca o antecede. No fechamento nenhuma linha traz `(E)`.

  Coluna Mudança: abra com o verbo da mudança (Inclusão, Alteração, Restrição, Remoção,
  Correção) e traga o contraste: *Antes* … *Agora* … — não descreva o estado atual da
  feature, diga o que mudou e de quê.
  Natureza: `incluída` (a função não existia — PFL = 100% do PFB) ou `alterada` (existia
  e mudou — PFL = 50%). É lida pela planilha de entrega.
-->

### [Feature Set]

| Feature | CA-n | Natureza | Mudança | Regras | Cenários | PFB | PFL |
|---|---|---|---|---|---|---|---|
| `SIGLA-SFS-NN` **[Nome da Feature]** | CA-1 | alterada | **[Verbo]** de [o quê]. *Antes* [como era]. *Agora* [como fica]. | +1 | +2 | [PF] | [PF] |

<!--
  OPCIONAL — OS PROCESSOS ELEMENTARES por trás do PFB, um por linha, com o nome que têm na `## Métricas de tamanho` do N3 (é pelo nome que a planilha de entrega casa a linha). Escreva a tabela quando o critério de aceite precisar chegar à planilha POR PROCESSO ELEMENTAR: a coluna `Critérios` vai ao Insumo daquela linha, à frente do critério da feature — é o que separa o critério da pesquisa do critério da combo que ela hospeda.
  Critérios: vale qualquer critério do card que alcance o PE, inclusive o que a `## Features` dá a outra feature (decisão do PO, 2026-10-04); número que o card não traz, não (o `validate-impact` avisa). Na numeração da fonte (`CA-n` ou `CRIT.0n.0m`), com faixa (`CA-1 a CA-4`). Com `—`, ou sem a tabela, o PE herda os critérios da feature.
  Só depois da contagem detalhada: o PE ainda estimado não tem nome no N3. Sem critério por PE a registrar, apague a tabela.
-->

| Processo elementar | Da feature | Papel | Tipo | PFB | Natureza | PFL | Critérios |
|---|---|---|---|---|---|---|---|
| [Nome do PE, como no N3] | `SIGLA-SFS-NN` | principal | EE | [PF] | alterada | [PF] | `CA-1` |

## Funções de dados alteradas

<!--
  As alterações físicas agrupadas pela função de dados (ALI/AIE) a que cada tabela
  pertence: migração → tabela/coluna → ALI/AIE, com o tamanho antes e depois. O título
  de cada função segue o formato que a planilha de entrega lê:
  `### ALI: <Entidade> — RLR a → b · DER c → d · n PF · alterada` (ou `### AIE: …`;
  `incluída` na função nova). Enquanto o DATA-MODEL não sustenta o número, o PF é o da
  estimativa, marcado `n PF (E)`. Sem alteração de dados, escreva "Nenhuma." e apague o
  exemplo.
-->

### ALI: [Entidade] — RLR [a] → [b] · DER [c] → [d] · [n] PF · alterada

| Migração | Tabela / coluna | Natureza | Mudança |
|---|---|---|---|
| [V000NN] | `[TABELA.COLUNA]` | coluna incluída | **Inclusão** de [o quê]. *Antes* [como era]. |

## Impacto em dicionários

- [mensagens, regras e campos canônicos novos ou alterados — ou "Nenhum."]

## Decisões de produto pendentes

- [onde o ticket contradiz o publicado, ou falta uma escolha — e o que TRAVA se ela não for tomada; ou "Nenhuma."]

## Reconciliação

> Preenchida no fechamento (estado `concluído`): artefatos **declarados** no changeset ×
> artefatos **efetivamente tocados** no diff/PR. Rodar:
> `node scripts/validate-impact.mjs analise-impacto/AIM-<CHAVE>.md --git-base <base>`.
> Declarado-e-não-tocado = escopo não cumprido; tocado-e-não-declarado = desvio — os dois
> precisam de justificativa. AIM aberta na entrega: diga que não houve escopo prévio.
> Escreva o resultado abaixo desta citação — ela é instrução e pode ficar.

## Changelog

<!-- Ordem decrescente por data: a versão mais recente fica no topo. Cada mudança de estado é uma versão — e, com o ticket em execução, cada atualização: artefato que passou a `feito`, feature que saiu de `(E)` para a contagem detalhada. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| [AAAA-MM-DD] | [autor] | AIM aberta | ticket `[CHAVE]` registrado; features mapeadas |
