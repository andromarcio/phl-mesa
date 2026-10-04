<!-- docqui: 4.0.2 | prompt: PROMPT_CONTAGEM | atualizado: 2026-10-04 -->
---
id: EVT-PAR-04
feature_set: EVT-PAR
dominio: EVT
entidade: EventoPessoaLegenda
data_model_ref: data-models/eventos.md#eventopessoalegenda
endpoints: []
error_codes: []
depende_de: ["EVT-PAR-01"]
origem:
  tipo: ""
  chave: ""
estado: rascunho
gates:
  requisitos:   { aprovado: false, por: "", em: "", pr: "" }
  modelo-dados: { aprovado: false, por: "", em: "", pr: "" }
  testes:       { aprovado: false, por: "", em: "", pr: "" }
  codigo:       { aprovado: false, por: "", em: "", pr: "" }
contagem:
  pendente: false
  revisada_em: "2026-10-04"
  revisada_ate: "PDTIC25148-35"
---

# Consultar Legenda do Participante
> **Nível 3** - Feature Set: Participantes — Major Feature Set: Eventos - `EVT-PAR-04`

## Descrição

Permite que o Administrador consulte, para um participante do evento, a legenda que lhe foi atribuída manualmente e as legendas do catálogo que podem ser atribuídas a ele, com a indicação das que fazem parte da configuração do evento.

A consulta abre na janela Gerenciar Legenda da Pessoa, acionada pelo valor da coluna Assento, na linha do participante. É dessa janela que partem a alteração e a remoção da legenda.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE005 – Gerenciar Participante v1.1, de 16/12/2025 (documento legado), funcionalidade "Consultar Legenda do Participante" ⚠️ sem chave na ferramenta de demandas | Criação | — Consultar a legenda de um participante a partir da pesquisa de participantes. O documento descreve a consulta da legenda atribuída pelo processamento das regras 📄; a janela mostra só a legenda manual 💻 ⚠️ |
| [`PDTIC25148-34`](../../../analise-impacto/AIM-PDTIC25148-34.md) | Alteração | — Sem critério numerado: a lista de legendas vinda do catálogo e a marca "Configurada neste evento" acompanham o modelo de legendas por evento que o ticket descreve 🔍 |
| [`PDTIC25148-35`](../../../analise-impacto/AIM-PDTIC25148-35.md) | Alteração | `CA-01` — a opção "Assento livre" deixa de ser oferecida na lista de legendas da janela |
<!-- trace-verified: PDTIC25148-34 @ f6bae69fe29f -->
<!-- trace-verified: PDTIC25148-35 @ 8882df4a0634 -->

---

<div class="dev-only">

## Superfície

**Modal** — origem: Pesquisar Participantes `EVT-PAR-01` (`/evento-pessoa/:id`), valor da coluna "Assento" em cada linha da lista

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Consultar Legenda do Participante" de GPE005 (`GPE005-04.png`)

---

</div>

## Regras de negócio

1. A legenda consultada é a do participante naquele evento, e não a da pessoa. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 8
2. A legenda apresentada como atual é somente a que foi atribuída manualmente ao participante; a legenda recebida por regra não entra na consulta. 💻 ⚠️ GPE005 diz que a legenda consultada "é atribuída ao participante após o processamento das regras de legenda" 📄. Consequência: o participante cuja legenda veio de regra aparece, nesta consulta, como se não tivesse legenda, embora a lista de participantes e o mapa de assentos o identifiquem por ela. Confirmar com o PO se a consulta deveria trazer a legenda prioritária.
3. As legendas oferecidas para escolha são todas as do catálogo, em ordem alfabética, menos "Assento livre". 💻 ⚠️ GPE005 traz uma relação fixa e numerada, de "1 – Anfitrião" a "16 – Assento livre" 📄, do modelo anterior ao catálogo de legendas.
4. A legenda do catálogo que faz parte da configuração do evento é identificada como tal; as que não fazem parte também são oferecidas. 💻
5. A consulta não altera nenhum dado do participante.

---

## Cenários

```gherkin
Feature: Consultar legenda do participante

  Background:
    Given que o usuário está autenticado no GPE
    And está na lista de participantes de um evento

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Consultar participante com legenda manual
    Given que o participante "Paulo Henrique", no assento "A1", tem a legenda manual "Anfitrião"
    When o usuário aciona "A1" na coluna "Assento" da linha de "Paulo Henrique"
    Then o sistema abre a janela "Gerenciar Legenda da Pessoa" com o nome, o cargo e a organização do participante e "Assento: A1"
    And mostra em "Legenda Atual:" a cor e o nome "Anfitrião", com a marca "Legenda manual"
    And mostra em "Selecione uma Legenda:" as legendas do catálogo, com "Anfitrião" já destacada
    And oferece os botões "Remover Legenda", "Cancelar" e "Salvar"

  Scenario: Consultar participante sem legenda manual
    Given que o participante "Victor Lucas" não tem legenda manual
    When o usuário aciona o valor da coluna "Assento" na linha de "Victor Lucas"
    Then a janela mostra, no lugar da legenda atual: "Esta pessoa não possui legenda configurada."
    And a opção "Remover legenda" aparece destacada ao fim da lista de legendas
    And o botão "Remover Legenda" não é oferecido
    # ⚠️ vale também para o participante que tem legenda recebida por regra; ver a regra 2 💻

  Scenario: Reconhecer as legendas configuradas no evento
    Given que a configuração do evento tem os blocos "Anfitrião" e "Palestrantes"
    When o usuário abre a janela de legenda de um participante
    Then as legendas "Anfitrião" e "Palestrantes" trazem o texto "Configurada neste evento"
    And as demais legendas do catálogo aparecem sem esse texto

  Scenario: Fechar a consulta
    When o usuário aciona "Cancelar" ou fecha a janela
    Then a janela é fechada sem alterar a legenda do participante

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há dado a validar
    When o usuário aciona o valor da coluna "Assento" de um participante
    Then o sistema abre a consulta sem solicitar nenhum dado

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Não há conflito com dados existentes
    When o usuário consulta a legenda de um participante
    Then o sistema apenas lê os dados, sem alterar nada

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Consultar Legenda do Participante" na matriz do N2
    When o usuário vê a lista de participantes
    Then o valor da coluna "Assento" é texto simples e não abre a janela de legenda
    # ⚠️ a tela só retira o atalho da Secretaria Check-In; ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Legenda "Assento livre" não é oferecida
    Given que o catálogo tem a legenda "Assento livre"
    When o usuário abre a janela de legenda de um participante
    Then a lista "Selecione uma Legenda:" não traz "Assento livre"

  Scenario: Participante sem assento
    Given que o participante não tem assento
    When o usuário aciona "Sem assento" na coluna "Assento" da linha dele
    Then a janela abre sem a linha "Assento:"

  Scenario: Falha ao buscar a legenda do participante
    Given que a busca da legenda falha no servidor
    When o usuário aciona o valor da coluna "Assento" de um participante
    Then a janela abre mesmo assim, como se o participante não tivesse legenda manual
    # ⚠️ a falha não é informada a quem usa a tela 💻

  Scenario: Falha ao carregar o catálogo de legendas
    Given que o catálogo de legendas não pôde ser carregado ao abrir a tela de participantes
    When o usuário abre a janela de legenda de um participante
    Then a lista "Selecione uma Legenda:" traz apenas a opção "Remover legenda"
    # ⚠️ a falha não é informada a quem usa a tela 💻
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| Nome do participante (sem rótulo na tela) | Pessoa | exibido do cadastro | somente leitura | texto | — | — |
| Cargo e organização (sem rótulo na tela) | Pessoa | exibido do cadastro | somente leitura | texto | — | O cargo, um hífen e a organização. ⚠️ A organização é o nome fantasia e, na falta dele, a razão social — a mesma troca da lista de participantes 💻 |
| "Assento:" | CadeiraMesa | exibido do cadastro | somente leitura | texto | — | Identificação do assento; a linha só aparece quando o participante tem assento |
| "Legenda Atual:" | EventoPessoaLegenda | exibido do cadastro | somente leitura | texto | — | Amostra da cor e nome da legenda manual, com a marca "Legenda manual". Sem legenda manual, no lugar vem "Esta pessoa não possui legenda configurada." |

*O campo "Selecione uma Legenda:" pertence à feature Alterar Legenda do Participante (`EVT-PAR-05`); aqui a lista é só consultada, e o que ela mostra está em Colunas do resultado.*

---

## Colunas do resultado

| Coluna (Label PO) | Origem | Ordenação |
|---|---|---|
| Amostra de cor (sem título) | Legenda — cor | — |
| Nome da legenda (sem título) | Legenda — nome da legenda | padrão ↑ |
| "Configurada neste evento" | EventoLegenda — aparece quando a legenda é um dos blocos da configuração do evento | — |

*As colunas acima descrevem a lista "Selecione uma Legenda:". A última linha da lista não é uma legenda: é a opção "Remover legenda", usada por Remover Legenda do Participante (`EVT-PAR-06`).*

⚠️ Na imagem "Consultar Legenda do Participante" de GPE005, cada legenda aparece com um número e com a composição da mesa ("PRINCIPAL") 📄; a tela atual não mostra número nem composição 💻.

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| — | — | Nenhum campo é gravado: a feature só consulta |

---

## Dados lidos e gravados

| Entidade | Papel | Por que a feature a toca |
|---|---|---|
| EventoPessoa | lê | É o participante da linha escolhida, de quem se consulta a legenda (regra 1) |
| Legenda | lê | Catálogo de legendas: as opções de "Selecione uma Legenda:" (regra 3) e o nome e a cor da legenda atual |
| EventoLegenda | lê | Blocos da configuração do evento, para marcar as legendas com "Configurada neste evento" (regra 4) |

---

## Comportamento de tela

### Onde fica
Na lista de participantes do evento, o valor da coluna "Assento" — a identificação do assento ou "Sem assento" — é o atalho da consulta, com a dica "Clique para gerenciar legenda da pessoa". Ele abre, sobre a lista, a janela "Gerenciar Legenda da Pessoa". GPE005 chama a opção de "Gerenciar legenda da pessoa" e registra, na descrição da coluna Assento, que é por ela que se consulta e se altera a legenda 📄. ⚠️ O atalho fica na coluna do assento, mas a janela não trata de assento: a atribuição de assento é feita no mapa.

A janela tem três blocos: os dados do participante (nome, cargo e organização e, se houver, "Assento:"); "Legenda Atual:"; e "Selecione uma Legenda:", uma lista com rolagem em que cada legenda traz a amostra da cor, o nome e, quando é o caso, o texto "Configurada neste evento". No rodapé ficam os botões "Remover Legenda" — só quando o participante tem legenda manual —, "Cancelar" e "Salvar".

O catálogo de legendas e a configuração do evento são lidos uma vez, quando a tela de participantes é aberta, e não a cada abertura da janela 💻. Uma legenda criada no catálogo depois disso só aparece ao recarregar a tela.

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Sem indicador: a janela só aparece depois da resposta do servidor |
| Erro de validação | Não se aplica — a consulta não tem campos de entrada |
| Erro de servidor | ⚠️ Nenhuma mensagem: a janela abre como se o participante não tivesse legenda manual 💻 |
| Sucesso | Janela aberta com os dados do participante, a legenda atual e a lista de legendas |
| Empty state | "Esta pessoa não possui legenda configurada.", quando não há legenda manual; lista só com a opção "Remover legenda", quando o catálogo está vazio |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Para o participante com legenda manual, a consulta mostra o nome e a cor dessa legenda e a marca "Legenda manual" | Regra 2 · cenário "Consultar participante com legenda manual" |
| SC-02 | A lista de legendas traz todas as do catálogo, menos "Assento livre", e marca as que estão na configuração do evento | Regras 3 e 4 |
| SC-03 | Abrir e fechar a consulta não muda a legenda de nenhum participante | Regra 5 · cenário "Fechar a consulta" |

---

## Métricas de tamanho

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Consultar Legenda do Participante | principal | CE | 3 | 8 | Média | 4 | 2026-10-04 |
| Consultar Selecione uma Legenda (combo) | acessório | CE | 2 | 4 | Baixa | 3 | 2026-10-04 |

### Memória de cálculo

**Consultar Legenda do Participante** — CE · ALR 3 · DER 8 · Média · 4 PF

```json
{"pe": "Consultar Legenda do Participante",
 "alr": ["Evento", "Pessoa", "Legenda"],
 "der": ["Nome do participante", "Cargo", "Organização", "Assento", "Legenda Atual", "Cor da legenda atual", "Mensagem", "Ação"],
 "nao_contados": "O campo Cargo e organização traz duas informações e conta dois DER; Legenda Atual traz a cor e o nome e conta dois. A lista de legendas é a lista consultada, contada à parte."}
```

Por que cada ALR:
1. `Evento` — lê o participante, o assento dele e a legenda manual que ele tem no evento
2. `Pessoa` — lê o nome, o cargo e a organização
3. `Legenda` — lê o nome e a cor da legenda manual

Classificação: CE — a intenção primária é apresentar, com as formas 5, 7, 8 e 11, sem cálculo nem dado derivado.

**Consultar Selecione uma Legenda (combo)** — CE · ALR 2 · DER 4 · Baixa · 3 PF

```json
{"pe": "Consultar Selecione uma Legenda (combo)",
 "alr": ["Legenda", "Evento"],
 "der": ["Amostra de cor", "Nome da legenda", "Configurada neste evento", "Ação"],
 "nao_contados": "A opção Remover legenda, última linha da lista, é comando de Remover Legenda do Participante. A lista consultada não conta Mensagem."}
```

Por que cada ALR:
1. `Legenda` — lê as legendas do catálogo, menos Assento livre
2. `Evento` — lê os blocos da configuração do evento, para marcar as legendas que fazem parte dela

Classificação: CE — lista consultada, com as formas 4, 5, 7, 8, 11 e 13. É este o processo que os tickets `PDTIC25148-34` e `PDTIC25148-35` alteraram nesta feature.

**Total: 7 PF**

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade EventoPessoaLegenda

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Atalho da coluna "Assento" e janela "Gerenciar Legenda da Pessoa" | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/components/evento-pessoas-list/evento-pessoas-list.component.html` (linhas 151–164 e 193–298) | — |
| Carga do catálogo, da configuração do evento e da legenda do participante | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/components/evento-pessoas-list/evento-pessoas-list.component.ts` (linhas 310–377) | — |
| Reconhecimento de "Assento livre" | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/services/legenda-mesa.helper.ts` (linhas 14 e 66–72) | — |
| Operação `GET /administracao/eventos/participante/{eventoPessoaId}/legenda` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoController.java` (linhas 290–295) | — |
| Leitura da legenda manual do participante | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/LegendaEventoServiceImpl.java` (linhas 441–457) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

O servidor devolve a primeira atribuição manual do participante e responde sem conteúdo quando não há nenhuma; as atribuições automáticas não são lidas por esta operação.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-10-04 | Claude (apf-cpm) | Contagem | Primeira contagem, pelo `PROMPT_CONTAGEM`: 7 PF — Consultar Legenda do Participante (CE Média, 4 PF); Consultar Selecione uma Legenda (combo) (CE Baixa, 3 PF). Confirmada em 2026-10-04 e espelhada em `global/CONTAGEM-PF.md` |
| 2026-10-04 | Claude (analise-impacto) | Origem atualizada | Elo com as AIMs dos tickets `PDTIC25148-34` e `PDTIC25148-35`, abertas na entrega: cada ticket ganha linha própria na Origem, como Alteração — o primeiro sem critério numerado, o segundo com o critério CA-01; regras, campos e cenários inalterados |
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE005 – Gerenciar Participante (funcionalidade "Consultar Legenda do Participante"), do código e do ticket `PDTIC25148-35` do Jira |

---

*Feature Set: Participantes · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
