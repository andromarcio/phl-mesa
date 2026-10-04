<!-- docqui: 4.0.2 | prompt: PROMPT_CONTAGEM | atualizado: 2026-10-04 -->
---
id: EVT-LEG-09
feature_set: EVT-LEG
dominio: EVT
entidade: EventoLegenda
data_model_ref: data-models/eventos.md#eventolegenda
endpoints: []
error_codes: []
depende_de: ["EVT-LEG-01"]
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

# Carregar Configuração de Legendas
> **Nível 3** - Feature Set: Legendas — Major Feature Set: Eventos - `EVT-LEG-09`

## Descrição

Permite que o Administrador traga para o evento a configuração de legendas guardada em um preset ou montada em outro evento, substituindo a configuração atual ou acrescentando a ela os blocos que faltam; o evento passa a ter os blocos, a ordem e as condições trazidos.

Na tela Configuração de Legendas, o botão Carregar configuração abre uma janela em que se escolhe o modo — substituir ou mesclar — e, na aba Biblioteca de presets ou na aba De outro evento, aciona-se Aplicar ao evento na origem desejada. A configuração resultante é gravada na hora.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| [`PDTIC25148-34`](../../../analise-impacto/AIM-PDTIC25148-34.md) | Criação | `CA-16, CA-18` — carregar um preset, com Substituir ou Mesclar, e recuperar a configuração de outro evento, aplicando-a ao evento atual. Especificada a partir do código-fonte (engenharia reversa de 2026-09-30); a funcionalidade não consta nos documentos legados ⚠️. O descarte dos blocos que saíram do catálogo e a restrição das origens a eventos não excluídos e com blocos não estão no ticket: vêm do código 💻 |
<!-- trace-verified: PDTIC25148-34 @ f6bae69fe29f -->

---

<div class="dev-only">

## Superfície

**Modal** — origem: Consultar Configuração de Legendas `EVT-LEG-01` (`/regras-legenda/:eventoId`), botão "Carregar configuração" da barra de ações

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada, ainda em teste — os documentos legados não trazem imagem dela

---

</div>

## Regras de negócio

1. A configuração pode vir de um preset da biblioteca ou da configuração de outro evento. 💻
2. Só serve de origem o evento que não foi excluído e que tem pelo menos um bloco configurado; o próprio evento não é origem de si mesmo. 💻
3. O que se traz são os blocos, a ordem deles e as condições de cada bloco — conectivo, campo, operador e valor. As legendas já atribuídas aos participantes da origem não são trazidas. 💻
4. Em modo de substituição, a configuração do evento passa a ser exatamente a trazida: os blocos que o evento tinha saem da configuração, junto com as suas condições. 💻
5. Em modo de mescla, os blocos que o evento já tem ficam como estão, na mesma ordem e com as mesmas condições, e entram depois deles só os blocos trazidos cuja legenda ainda não está no evento. Para a legenda que já está no evento, valem as condições do evento; as da origem são desprezadas. 💻 ⚠️ O ticket diz que mesclar "mantém os blocos atuais e acrescenta os da selecionada", sem tratar do bloco que existe dos dois lados; a regra do código decorre de cada legenda aparecer uma única vez na configuração do evento.
6. Do preset só se aproveitam os blocos cuja legenda ainda existe no catálogo; os demais ficam de fora. 💻
7. A configuração resultante é renumerada pela posição — 1, 2, 3 e assim sucessivamente — e gravada no evento como qualquer outra alteração da configuração. 💻 A gravação segue as regras de Consultar Configuração de Legendas `EVT-LEG-01` e de Adicionar Bloco de Legenda ao Evento `EVT-LEG-02`.
8. Carregar a configuração não altera as legendas dos participantes do evento: elas só mudam em Gerar Legendas do Evento `EVT-LEG-07`. 💻 ⚠️ Até a geração, o participante continua com a legenda de um bloco que saiu da configuração.
9. A origem não é alterada: o preset e o outro evento ficam como estavam. 💻
10. O evento de destino recebe uma cópia: o que mudar depois no outro evento, ou a exclusão do preset, não chega a ele. 💻
11. A substituição não tem volta: a configuração anterior não fica guardada. 💻 ⚠️

---

## Cenários

```gherkin
Feature: Carregar configuração de legendas

  Background:
    Given que o usuário está autenticado no GPE
    And está na tela "Configuração de Legendas" de um evento
    And acionou "Carregar configuração"

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Substituir a configuração pela de um preset
    Given que o evento tem os blocos "Anfitrião" e "Imprensa"
    And que o preset "Reuniões da MEI" tem os blocos "Palestrantes" e "Diretores da CNI", com as suas condições
    And que "Substituir configuração atual" está marcado em "Ao aplicar:"
    When o usuário aciona "Aplicar ao evento" no cartão do preset "Reuniões da MEI"
    Then a janela se fecha
    And a configuração do evento passa a ter só "Palestrantes", com o número 1, e "Diretores da CNI", com o número 2, com as condições do preset
    And a configuração é gravada, com o indicador "Salvando…" e, em seguida, "Salvo"
    # ⚠️ a substituição é feita sem pedir confirmação 💻

  Scenario: Mesclar a configuração com a de um preset
    Given que o evento tem os blocos "Anfitrião" e "Palestrantes", cada um com as suas condições
    And que o preset "Reuniões da MEI" tem os blocos "Palestrantes" e "Diretores da CNI"
    When o usuário marca "Mesclar (adicionar blocos ausentes)"
    And aciona "Aplicar ao evento" no cartão do preset
    Then a configuração do evento fica com "Anfitrião", "Palestrantes" e "Diretores da CNI", nessa ordem
    And "Anfitrião" e "Palestrantes" mantêm as condições que tinham no evento
    And "Diretores da CNI" entra com as condições do preset

  Scenario: Substituir a configuração pela de outro evento
    Given que o evento "Reunião de Março" tem três blocos configurados
    When o usuário abre a aba "De outro evento"
    And aciona "Aplicar ao evento" na linha de "Reunião de Março"
    Then a configuração do evento passa a ser uma cópia dos blocos, da ordem e das condições de "Reunião de Março"
    And a configuração de "Reunião de Março" continua como estava

  Scenario: Mesclar a configuração com a de outro evento
    When o usuário marca "Mesclar (adicionar blocos ausentes)"
    And aciona "Aplicar ao evento" na linha de um evento da aba "De outro evento"
    Then os blocos do evento atual ficam como estão
    And entram, ao final, os blocos do outro evento cuja legenda ainda não estava na configuração

  Scenario: Desistir de carregar
    When o usuário aciona "Cancelar" ou fecha a janela
    Then a configuração do evento continua como estava

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há dado a validar
    When o usuário abre a janela
    Then o modo já vem com "Substituir configuração atual" marcado e não há campo de digitação

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Preset com bloco que não existe mais no catálogo
    Given que o preset foi salvo com os blocos "Palestrantes" e "Imprensa"
    And que "Imprensa" foi excluído do catálogo depois disso
    When o usuário aciona "Aplicar ao evento" no cartão do preset
    Then só "Palestrantes" é trazido para o evento
    And o sistema exibe o aviso "Blocos ignorados" com o detalhe "1 bloco(s) do preset não existe(m) mais no catálogo e foram ignorados."
    # 💻 o cartão do preset já mostra só os blocos que continuam no catálogo, e a quantidade de blocos conta só esses

  Scenario: Mesclar quando todos os blocos da origem já estão no evento
    Given que todas as legendas da origem já estão na configuração do evento
    When o usuário aplica a origem em modo "Mesclar (adicionar blocos ausentes)"
    Then nenhum bloco é acrescentado e as condições do evento não mudam
    And a configuração é gravada de novo, igual

  Scenario: Bloco excluído do catálogo com a janela aberta
    Given que um bloco do preset foi excluído do catálogo depois de a janela ser aberta
    When o usuário aciona "Aplicar ao evento" no cartão do preset
    Then o servidor recusa a gravação
    And o sistema exibe o erro "Erro Interno" com o detalhe "Bloco de legenda inexistente: " seguido do identificador do bloco
    And a tela volta a mostrar a configuração que está gravada
    # 🔍 inferido da leitura do código: a relação de blocos do catálogo é lida uma vez, na abertura da janela

  Scenario: Preset excluído por outra pessoa com a janela aberta
    Given que o preset foi excluído depois de a janela ser aberta
    When o usuário aciona "Aplicar ao evento" no cartão dele
    Then a configuração do evento continua como estava
    # ⚠️ 🔍 nenhuma mensagem aparece e a janela continua aberta: a resposta vem sem conteúdo e o tratamento de erro da janela não prevê esse caso — suspeita de defeito

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Carregar Configuração de Legendas" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Eventos › Cadastro, por onde se chega à Configuração de Legendas, e a ação não fica ao alcance dele
    # ⚠️ a tela não confere o perfil; ver a nota da matriz no N2
    # 💻 no servidor, a leitura dos presets e das configurações está declarada para os três perfis; a gravação da configuração do evento, só para o Administrador

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Biblioteca sem presets
    Given que nenhum preset foi salvo
    When o usuário abre a janela
    Then a aba "Biblioteca de presets" mostra "Nenhum preset salvo ainda."

  Scenario: Nenhum outro evento com configuração
    Given que nenhum outro evento não excluído tem bloco configurado
    When o usuário abre a aba "De outro evento"
    Then a aba mostra "Nenhum outro evento com blocos configurados."

  Scenario: Substituir por um preset sem blocos aproveitáveis
    Given que o preset não tem blocos, ou que todos os blocos dele saíram do catálogo
    And que "Substituir configuração atual" está marcado
    When o usuário aciona "Aplicar ao evento" no cartão do preset
    Then a configuração do evento fica vazia e a tela mostra "Nenhum bloco configurado"
    # ⚠️ o evento perde todos os blocos sem confirmação e sem como desfazer 💻

  Scenario: Participantes que já tinham legenda
    Given que as legendas do evento já foram geradas
    When o usuário substitui a configuração
    Then as legendas dos participantes continuam as mesmas até que as legendas sejam geradas de novo

  Scenario: Preset com conteúdo ilegível
    Given que o conteúdo guardado de um preset não pode ser lido
    When o usuário abre a janela ou aciona "Aplicar ao evento" nesse preset
    Then o sistema exibe o erro "Erro Interno" com o detalhe "Não foi possível ler a configuração do preset."
    # 🔍 situação que a tela não produz, porque o conteúdo é sempre gravado pelo próprio sistema; se ocorrer, a biblioteca inteira deixa de ser listada, e não só o preset com problema ⚠️

  Scenario: Falha ao gravar a configuração trazida
    Given que o servidor falha ao gravar a configuração
    When o usuário aciona "Aplicar ao evento"
    Then o sistema exibe o erro "Erro Interno" com o detalhe "Ocorreu um erro inesperado. Contate o suporte."
    And a tela volta a mostrar a configuração que está gravada, descartando a que foi trazida
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| Ao aplicar: | dado de código | entrada do usuário | editável | lista de opções | sim | "Substituir configuração atual", que já vem marcado a cada abertura da janela, ou "Mesclar (adicionar blocos ausentes)". Vale para as duas origens |

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| Nº | Posição do bloco na configuração resultante, a partir de 1 | Ao aplicar, antes da gravação |

---

## Dados lidos e gravados

| Entidade | Papel | Por que a feature a toca |
|---|---|---|
| PresetLegenda | lê | Lista os presets da biblioteca e traz a configuração do preset escolhido (regras 1 e 3) |
| Evento | lê | Lista os eventos que podem servir de origem, com o nome e a quantidade de blocos (regra 2) |
| EventoLegenda | lê e grava | Lê os blocos do evento de origem; grava os blocos da configuração resultante no evento de destino (regras 4, 5 e 7) |
| EventoLegendaCondicao | lê e grava | Lê as condições dos blocos da origem; grava as condições dos blocos no evento de destino (regra 3) |
| Legenda | lê | Diz quais blocos do preset ainda existem no catálogo e dá o nome e a cor mostrados no cartão do preset (regra 6) |

---

## Comportamento de tela

### Onde fica
Na tela Configuração de Legendas do evento, o botão "Carregar configuração" é o primeiro da barra de ações. Ele abre a janela "Carregar configuração" sobre a tela. No alto fica a escolha "Ao aplicar:", com as opções "Substituir configuração atual" e "Mesclar (adicionar blocos ausentes)". Abaixo há duas abas, "Biblioteca de presets", que é a aberta, e "De outro evento". No rodapé, o botão "Cancelar". A cada abertura a janela volta à primeira aba e ao modo de substituição. 💻

A aba "Biblioteca de presets" traz um cartão por preset, com o nome, a quantidade de blocos ("1 bloco" ou "{n} blocos"), a descrição, quando há, uma etiqueta com a cor e o nome de cada bloco e os botões "Aplicar ao evento" e "Excluir preset" — este último é Excluir Preset de Legendas `EVT-LEG-10`. O nome e a cor das etiquetas são os atuais do catálogo, e não os da época em que o preset foi salvo. O evento de origem e a data de criação do preset não aparecem. 💻

A aba "De outro evento" traz uma linha por evento, com o nome, a quantidade de blocos e o botão "Aplicar ao evento". ⚠️ A linha foi desenhada para mostrar também a data do evento antes da quantidade de blocos, mas a data não chega à tela 🔍 — suspeita de defeito. Nenhuma das abas tem busca, paginação ou ordem definida. 💻

É a tela que faz a cópia: lê a origem, monta a configuração resultante e a grava no evento, pelo mesmo caminho das demais alterações da configuração. Ao acionar "Aplicar ao evento", a janela se fecha de imediato e os cartões da configuração passam a mostrar os blocos trazidos, enquanto a gravação acontece. Não há pergunta de confirmação antes de substituir nem resumo do que vai mudar. ⚠️ O bloco trazido de um preset aparece na tela com o nome e a cor que tinha quando o preset foi salvo, até que a tela seja aberta de novo 🔍.

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | "Carregando presets…" e "Carregando eventos…", cada um na sua aba, enquanto as listas chegam. Depois de aplicar, a tela da configuração mostra "Salvando…" |
| Erro de validação | Não se aplica — não há digitação, e o modo tem sempre uma opção marcada |
| Erro de servidor | Erro "Erro Interno" com o texto enviado pelo servidor no detalhe; em falha inesperada, "Ocorreu um erro inesperado. Contate o suporte.". As recusas da gravação são as mesmas de qualquer alteração da configuração do evento — ver Consultar Configuração de Legendas `EVT-LEG-01`. Quando a gravação da configuração falha, a tela descarta o que foi trazido e volta a mostrar a configuração gravada. ⚠️ Dentro da janela, a resposta de erro sem conteúdo não produz mensagem alguma 🔍 |
| Sucesso | Sem mensagem própria: a janela se fecha, os cartões e o contador de blocos da configuração são atualizados e o indicador "Salvo" aparece por alguns instantes. Quando blocos do preset ficam de fora, aviso "Blocos ignorados" com o detalhe "{n} bloco(s) do preset não existe(m) mais no catálogo e foram ignorados." |
| Empty state | "Nenhum preset salvo ainda." na aba "Biblioteca de presets"; "Nenhum outro evento com blocos configurados." na aba "De outro evento" |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Depois de substituir, a configuração do evento tem exatamente os blocos, a ordem e as condições da origem que ainda existem no catálogo | Regras 4 e 6 · cenário "Substituir a configuração pela de um preset" |
| SC-02 | Depois de mesclar, nenhum bloco que o evento já tinha muda de posição ou de condições, e nenhuma legenda aparece duas vezes na configuração | Regra 5 · cenário "Mesclar a configuração com a de um preset" |
| SC-03 | Carregar uma configuração não altera a origem nem as legendas já atribuídas aos participantes do evento de destino | Regras 8 e 9 |
| SC-04 | Todo bloco do preset deixado de fora por não existir mais no catálogo é informado ao usuário, com a quantidade | Regra 6 · cenário "Preset com bloco que não existe mais no catálogo" |

---

## Métricas de tamanho

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Carregar Configuração de Legendas | principal | EE | 3 | 5 | Alta | 6 | 2026-10-04 |
| Consultar Biblioteca de presets (combo) | acessório | SE | 2 | 6 | Média | 5 | 2026-10-04 |
| Consultar De outro evento (combo) | acessório | SE | 1 | 3 | Baixa | 4 | 2026-10-04 |

### Memória de cálculo

**Carregar Configuração de Legendas** — EE · ALR 3 · DER 5 · Alta · 6 PF

```json
{"pe": "Carregar Configuração de Legendas",
 "alr": ["Evento", "PresetLegenda", "Legenda"],
 "der": ["Ao aplicar", "Preset", "Evento de origem", "Mensagem", "Ação"],
 "nao_contados": "Nº é recalculado pelo sistema."}
```

Por que cada ALR:
1. `Evento` — lê a configuração do evento de origem e grava a configuração resultante no evento de destino
2. `PresetLegenda` — lê a configuração guardada no preset escolhido
3. `Legenda` — diz quais blocos do preset ainda existem no catálogo

Classificação: EE — a intenção primária é manter o arquivo lógico Evento, com as formas 4, 5, 6, 7 e 12. Carregar de um preset e carregar de outro evento são fluxos alternativos do mesmo processo, e não dois processos (Guia STI 3.2): os DER e os ALR são a união dos dois caminhos. Preset e Evento de origem são a origem escolhida no cartão ou na linha, como registram as seções Dados lidos e gravados e Comportamento de tela.

**Consultar Biblioteca de presets (combo)** — SE · ALR 2 · DER 6 · Média · 5 PF

```json
{"pe": "Consultar Biblioteca de presets (combo)",
 "alr": ["PresetLegenda", "Legenda"],
 "der": ["Nome do preset", "Quantidade de blocos", "Descrição", "Cor do bloco", "Nome do bloco", "Ação"],
 "nao_contados": "A lista consultada não conta Mensagem. Evento de origem e data de criação do preset não aparecem no cartão."}
```

Por que cada ALR:
1. `PresetLegenda` — lê os presets da biblioteca, com o nome, a descrição e os blocos guardados
2. `Legenda` — lê o nome e a cor atuais de cada bloco e deixa de fora o bloco que saiu do catálogo

Classificação: SE — lista consultada com cálculo (forma 2): a quantidade de blocos de cada preset é contada na hora. Os DER estão descritos no Comportamento de tela do N3, que não tem a seção Colunas do resultado.

**Consultar De outro evento (combo)** — SE · ALR 1 · DER 3 · Baixa · 4 PF

```json
{"pe": "Consultar De outro evento (combo)",
 "alr": ["Evento"],
 "der": ["Nome do evento", "Quantidade de blocos", "Ação"],
 "nao_contados": "A lista consultada não conta Mensagem. A data do evento foi desenhada para a linha, mas não chega à tela."}
```

Por que cada ALR:
1. `Evento` — lê os eventos não excluídos que têm ao menos um bloco, menos o próprio, e conta os blocos de cada um

Classificação: SE — lista consultada com cálculo (forma 2): a quantidade de blocos de cada evento é contada na hora. Os DER estão descritos no Comportamento de tela do N3.

**Total: 15 PF**

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade EventoLegenda — é a que a feature grava; a configuração vem de PresetLegenda ou dos blocos de outro evento

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Janela "Carregar configuração": modo, abas, leitura da origem, substituição e mescla | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/components/carregar-configuracao-dialog/carregar-configuracao-dialog.component.ts` (linhas 83–149 e 173–203) e `.html` (linhas 1–90) | — |
| Aplicação à configuração, renumeração, gravação e aviso de blocos ignorados | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/pages/configuracao-legendas-evento/configuracao-legendas-evento.component.ts` (linhas 111–124, 182–188 e 324–335) | — |
| Operações `GET /administracao/legendas/presets` e `GET /administracao/legendas/presets/{id}` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/LegendaController.java` (linhas 65–75) e `service/impl/PresetLegendaServiceImpl.java` (linhas 52–83 e 163–184) | — |
| Operação `GET /administracao/eventos/legendas/origens` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/LegendaEventoServiceImpl.java` (linhas 144–162) e `repository/EventoLegendaRepository.java` (linhas 35–41) | — |
| Operações `GET` e `PUT /administracao/eventos/{id}/legendas` — leitura da origem e gravação no destino | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoController.java` (linhas 261–270) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada e em teste (ticket `PDTIC25148-34`); o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

O servidor não tem operação de cópia nem de aplicação de preset: a tela lê a origem e grava o destino. A data que falta na aba "De outro evento" é diferença de nome entre o que o servidor envia (`dataEvento`) e o que a tela lê (`data`). A relação de blocos do catálogo usada para descartar os que não existem mais é lida com limite de 1.000 blocos.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-10-04 | Claude (apf-cpm) | Contagem | Primeira contagem, pelo `PROMPT_CONTAGEM`: 15 PF — Carregar Configuração de Legendas (EE Alta, 6 PF); Consultar Biblioteca de presets (combo) (SE Média, 5 PF); Consultar De outro evento (combo) (SE Baixa, 4 PF). Confirmada em 2026-10-04 e espelhada em `global/CONTAGEM-PF.md` |
| 2026-10-04 | Claude (analise-impacto) | Origem atualizada | Elo com a AIM do ticket `PDTIC25148-34`, aberta na entrega: o ticket passa a ser a Origem da feature (Criação), com os critérios CA-16 e CA-18; regras, campos e cenários inalterados |
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do código e do ticket `PDTIC25148-34` do Jira (critérios CA16 e CA18); a funcionalidade não consta no documento legado GPE006 – Gerenciar Regras de Legendas |

---

*Feature Set: Legendas · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
