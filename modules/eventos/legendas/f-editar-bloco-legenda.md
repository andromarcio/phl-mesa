<!-- docqui: 4.0.2 | prompt: PROMPT_CONTAGEM | atualizado: 2026-10-04 -->
---
id: EVT-LEG-13
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

# Editar Bloco de Legenda
> **Nível 3** - Feature Set: Legendas — Major Feature Set: Eventos - `EVT-LEG-13`

## Descrição

Permite que o Administrador altere o nome ou a cor de um bloco de legenda do catálogo; a mudança passa a valer em todos os eventos que usam o bloco e nas legendas já atribuídas aos participantes.

No Catálogo de blocos, o ícone de lápis de cada linha abre a janela Editar bloco com o nome e a cor atuais. Altera-se o que for preciso e aciona-se Salvar.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| [`PDTIC25148-34`](../../../analise-impacto/AIM-PDTIC25148-34.md) | Criação | `CA-10` — alterar um bloco do catálogo, com reflexo nos eventos que o utilizam. Especificada a partir do código-fonte (engenharia reversa de 2026-09-30); a funcionalidade não consta nos documentos legados ⚠️. O ticket não diz quais dados do bloco podem ser alterados; no código são o nome e a cor, os únicos que o bloco tem 💻 |
<!-- trace-verified: PDTIC25148-34 @ f6bae69fe29f -->

---

<div class="dev-only">

## Superfície

**Modal** — origem: Pesquisar Blocos de Legenda `EVT-LEG-11` (`/catalogo-legendas`), ícone de lápis em cada linha da lista, que abre a janela "Editar bloco"

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada, ainda em teste — os documentos legados não trazem imagem dela

---

</div>

## Regras de negócio

1. Do bloco podem ser alterados o nome e a cor, que são os únicos dados que ele tem. 💻
2. O nome e a cor continuam obrigatórios depois da alteração. 💻
3. O nome continua único no catálogo, sem diferenciar maiúsculas de minúsculas; o próprio bloco não entra na comparação, de modo que ele pode manter o nome ou mudar só as maiúsculas e minúsculas dele. 💻
4. A cor continua guardada como código no formato `#RRGGBB`. 💻
5. O bloco é um só para todos os eventos: a alteração do nome ou da cor vale de imediato em todas as configurações de evento que usam o bloco e em todas as legendas dele já atribuídas a participantes, automáticas ou manuais, sem que as legendas precisem ser geradas de novo. 💻
6. A alteração não muda a presença do bloco em nenhum evento, nem a ordem, nem as condições dele. 💻
7. A alteração não distingue a situação do evento: alcança também os eventos já realizados e os excluídos. 💻 ⚠️ Depois de alterado o nome ou a cor, o mapa de um evento passado deixa de mostrar a legenda como ela era no dia.
8. O valor anterior não fica guardado: não há histórico da alteração nem como desfazê-la, a não ser editando de novo. 💻
9. O bloco em uso pode ser alterado como qualquer outro: o uso em eventos não impede nem condiciona a alteração. 💻

---

## Cenários

```gherkin
Feature: Editar bloco de legenda

  Background:
    Given que o usuário está autenticado no GPE
    And está na tela "Catálogo de blocos"

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Alterar o nome e a cor de um bloco
    Given que o catálogo tem o bloco "Palestrante"
    When o usuário aciona "Editar bloco" na linha de "Palestrante"
    And altera "Nome da legenda" para "Palestrantes" e escolhe outra cor
    And aciona "Salvar"
    Then o sistema grava o novo nome e a nova cor do bloco
    And exibe: "Bloco atualizado" com o detalhe "O bloco foi atualizado com sucesso."
    And a janela se fecha e a lista é recarregada na mesma página em que estava

  Scenario: Alterar só a cor
    When o usuário aciona "Editar bloco" na linha de um bloco
    And escolhe outra cor, sem mexer no nome
    And aciona "Salvar"
    Then o sistema grava a nova cor e mantém o nome

  Scenario: Salvar sem alterar nada
    When o usuário aciona "Editar bloco" na linha de um bloco
    And aciona "Salvar" sem mudar o nome nem a cor
    Then o sistema aceita e exibe: "Bloco atualizado"

  Scenario: Desistir da alteração
    When o usuário aciona "Editar bloco", muda o nome e aciona "Cancelar"
    Then o bloco continua com o nome e a cor que tinha

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Nome da legenda vazio
    When o usuário apaga o conteúdo de "Nome da legenda"
    And aciona "Salvar"
    Then a janela continua aberta e o sistema exibe abaixo do campo: "Este campo é obrigatório"
    And o bloco não é alterado

  Scenario: Nome da legenda só com espaços
    When o usuário preenche "Nome da legenda" só com espaços
    And aciona "Salvar"
    Then o bloco não é alterado
    And o sistema exibe o erro "Erro Interno" com o detalhe "O nome do bloco de legenda é obrigatório."
    # ⚠️ a tela aceita o nome só com espaços e quem recusa é o servidor 💻

  Scenario: Cor fora do formato
    When a alteração chega ao servidor sem cor ou com cor fora do formato "#RRGGBB"
    Then o servidor recusa com a mensagem "A cor deve estar no formato #RRGGBB."
    # 💻 pela tela isso não acontece: a cor vem sempre da paleta ou do seletor, já no formato

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Nome igual ao de outro bloco
    Given que o catálogo tem os blocos "Palestrantes" e "Anfitrião"
    When o usuário edita "Anfitrião", muda o nome para "palestrantes" e aciona "Salvar"
    Then o bloco não é alterado
    And o sistema exibe o erro "Erro Interno" com o detalhe "Já existe um bloco de legenda com este nome."
    And a janela continua aberta, com o que foi digitado
    # ⚠️ a tela não confere o nome repetido antes de enviar; o resumo é "Erro Interno" embora o motivo seja uma regra de negócio 💻

  Scenario: Mudar só maiúsculas e minúsculas do próprio nome
    Given que o catálogo tem o bloco "diretores da cni"
    When o usuário muda o nome para "Diretores da CNI" e aciona "Salvar"
    Then o sistema aceita a alteração

  Scenario: Bloco excluído por outra pessoa durante a edição
    Given que o bloco foi excluído do catálogo depois de a janela "Editar bloco" ser aberta
    When o usuário aciona "Salvar"
    Then o sistema exibe o erro "Erro Interno" com o detalhe "Bloco de legenda não encontrado."
    # 💻 a janela continua aberta e a lista não é recarregada: a linha do bloco que não existe mais segue na tela

  Scenario: Bloco em uso em eventos
    Given que o bloco "Palestrantes" está na configuração de três eventos e já foi atribuído a participantes
    When o usuário altera o nome ou a cor do bloco
    Then a configuração dos três eventos, a lista de participantes e o mapa de assentos passam a mostrar o novo nome e a nova cor
    # ⚠️ a alteração é feita sem aviso de que o bloco está em uso e sem pedir confirmação 💻

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Editar Bloco de Legenda" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Administração › Catálogo de legendas, e a ação não fica ao alcance dele
    # ⚠️ a tela não confere o perfil; ver a nota da matriz no N2
    # 💻 no servidor, a alteração de bloco está declarada só para o Administrador

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Falha inesperada ao alterar
    Given que o servidor falha ao gravar a alteração
    When o usuário aciona "Salvar"
    Then o bloco não é alterado e a janela continua aberta
    And o sistema exibe o erro "Erro Interno" com o detalhe "Ocorreu um erro inesperado. Contate o suporte."
    # 💻 quando a resposta de erro vem sem conteúdo, o texto é "Erro" com o detalhe "Falha de comunicação com o servidor."
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| Nome da legenda | Legenda | entrada do usuário | editável | texto | sim | Vem preenchido com o nome atual. Até 100 caracteres, limite imposto pela tela; os espaços no início e no fim são descartados; não pode repetir o nome de outro bloco, sem diferenciar maiúsculas de minúsculas |
| Cor | Legenda | entrada do usuário | editável | texto | sim | Vem preenchida com a cor atual. Código de cor no formato `#RRGGBB`, escolhido na paleta de cores sugeridas ou no seletor de cor; é guardado em letras maiúsculas |

O bloco não tem campo somente leitura nem imutável: tudo o que ele guarda pode ser alterado.

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| — | — | Nenhum campo é preenchido pelo sistema: não há data de alteração nem registro de quem alterou 💻 |

---

## Comportamento de tela

### Onde fica
No Catálogo de blocos, na coluna "Ações" de cada linha, o ícone de lápis com a dica "Editar bloco", ao lado do ícone de lixeira. Ele abre a janela "Editar bloco", com o mesmo formulário do cadastro — "Nome da legenda" e "Cor", com o seletor de cor, o código da cor e a paleta de cores sugeridas —, já preenchido com o nome e a cor atuais, e os botões "Cancelar" e "Salvar". 💻

Quando a cor atual do bloco é uma das cores da paleta, ela aparece marcada; quando não é, nenhuma cor da paleta fica marcada e a cor aparece só no seletor e no código. A janela não informa em quantos eventos o bloco está em uso, e a alteração não pede confirmação. Depois de salvar, a lista permanece na página e na ordem em que estava. Quando o servidor recusa a alteração, a janela continua aberta com o que foi digitado. 💻

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | O botão "Salvar" fica desabilitado enquanto a gravação acontece; não há outro indicador |
| Erro de validação | "Este campo é obrigatório", abaixo de "Nome da legenda", quando o campo é deixado vazio. O campo não aceita digitação além de 100 caracteres |
| Erro de servidor | Erro "Erro Interno" com o texto enviado pelo servidor no detalhe: "O nome do bloco de legenda é obrigatório.", "A cor deve estar no formato #RRGGBB.", "Já existe um bloco de legenda com este nome.", "Bloco de legenda não encontrado." ou, em falha inesperada, "Ocorreu um erro inesperado. Contate o suporte.". Resposta de erro sem conteúdo: "Erro" com o detalhe "Falha de comunicação com o servidor.". A janela continua aberta. ⚠️ O resumo é "Erro Interno" mesmo quando o motivo é uma regra de negócio |
| Sucesso | Mensagem "Bloco atualizado" com o detalhe "O bloco foi atualizado com sucesso.", fechamento da janela e recarga da lista na mesma página |
| Empty state | Não se aplica — a ação só existe em linha da lista |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Depois de alterado, o bloco aparece com o novo nome e a nova cor no catálogo, na configuração de todos os eventos que o usam, na lista de participantes e no mapa de assentos, sem nova geração de legendas | Regra 5 · cenário "Bloco em uso em eventos" |
| SC-02 | Nenhuma alteração deixa dois blocos com o mesmo nome no catálogo | Regra 3 · cenário "Nome igual ao de outro bloco" |
| SC-03 | A alteração do nome ou da cor não muda quais participantes têm a legenda, nem a ordem ou as condições do bloco em evento algum | Regra 6 |

---

## Métricas de tamanho

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Editar Bloco de Legenda | principal | EE | 1 | 4 | Baixa | 3 | 2026-10-04 |
| Consultar Bloco de Legenda (implícita) | acessório | — | — | — | — | 0 | 2026-10-04 |

### Memória de cálculo

**Editar Bloco de Legenda** — EE · ALR 1 · DER 4 · Baixa · 3 PF

```json
{"pe": "Editar Bloco de Legenda",
 "alr": ["Legenda"],
 "der": ["Nome da legenda", "Cor", "Mensagem", "Ação"]}
```

Por que cada ALR:
1. `Legenda` — regrava o nome e a cor do bloco e confere que o nome não se repete

Classificação: EE — a intenção primária é manter o arquivo lógico Legenda, com as formas 1, 6, 7 e 12.

**Consultar Bloco de Legenda (implícita)** — 0 PF

```json
{"pe": "Consultar Bloco de Legenda (implícita)", "motivo": "A janela Editar bloco abre com o nome e a cor, que a lista do catálogo já mostrava. Nada novo cruza a fronteira, e a leitura não é processo elementar (SIZING, Regra da consulta implícita)."}
```

**Total: 3 PF**

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade Legenda

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Ícone "Editar bloco", janela "Editar bloco" e mensagens | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/pages/catalogo-legendas/catalogo-legendas.component.ts` (linhas 160–217) e `.html` (linhas 65–66 e 90–103) | — |
| Formulário do bloco, com o preenchimento dos valores atuais | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/components/bloco-form/bloco-form.component.ts` (linhas 38–77) | — |
| Serviço do catálogo | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/services/legenda-catalogo.service.ts` (linhas 36–38) | — |
| Operação `PUT /administracao/legendas/{id}` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/LegendaController.java` (linhas 102–105) | — |
| Conferência de existência, validação, unicidade e gravação | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/LegendaServiceImpl.java` (linhas 112–129 e 177–187) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada e em teste (ticket `PDTIC25148-34`); o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

A edição grava só o registro do bloco: as configurações de evento e as legendas dos participantes não são regravadas — apontam para o bloco do catálogo e, por isso, passam a mostrar o novo nome e a nova cor. Os presets guardam, no retrato, o nome e a cor que o bloco tinha quando foram salvos; a Biblioteca de presets mostra os valores atuais do catálogo, mas o bloco trazido de um preset aparece na configuração com os valores antigos até a tela ser reaberta — ver Carregar Configuração de Legendas `EVT-LEG-09`.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-10-04 | Claude (apf-cpm) | Contagem | Primeira contagem, pelo `PROMPT_CONTAGEM`: 3 PF — Editar Bloco de Legenda (EE Baixa, 3 PF); Consultar Bloco de Legenda (implícita) não conta (0 PF). Confirmada em 2026-10-04 e espelhada em `global/CONTAGEM-PF.md` |
| 2026-10-04 | Claude (analise-impacto) | Origem atualizada | Elo com a AIM do ticket `PDTIC25148-34`, aberta na entrega: o ticket passa a ser a Origem da feature (Criação), com o critério CA-10; regras, campos e cenários inalterados |
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do código e do ticket `PDTIC25148-34` do Jira (critério CA10); a funcionalidade não consta no documento legado GPE006 – Gerenciar Regras de Legendas |

---

*Feature Set: Legendas · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
