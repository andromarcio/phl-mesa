<!-- docqui: 4.0.2 | prompt: PROMPT_CONTAGEM | atualizado: 2026-10-04 -->
---
id: EVT-LEG-11
feature_set: EVT-LEG
dominio: EVT
entidade: Legenda
data_model_ref: data-models/eventos.md#legenda
endpoints: []
error_codes: []
depende_de: []
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

# Pesquisar Blocos de Legenda
> **Nível 3** - Feature Set: Legendas — Major Feature Set: Eventos - `EVT-LEG-11`

## Descrição

Permite que o Administrador pesquise, pelo nome, os blocos de legenda do catálogo comum a todos os eventos, vendo de cada um o nome e a cor que o identifica.

O catálogo abre pelo menu Administração › Catálogo de legendas ou pelo botão Gerenciar catálogo da Configuração de Legendas de um evento. Digita-se parte do nome no campo de busca e a lista se atualiza sozinha; de cada linha partem a edição e a exclusão do bloco, e do cabeçalho, a inclusão de um novo.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| [`PDTIC25148-34`](../../../analise-impacto/AIM-PDTIC25148-34.md) | Criação | `CA-05` — consultar o catálogo de blocos, que não tem número nem ordem: a numeração pertence à configuração de cada evento. Especificada a partir do código-fonte (engenharia reversa de 2026-09-30); a funcionalidade não consta nos documentos legados ⚠️. A busca pelo nome, a paginação e a tela própria do catálogo não estão nos critérios do ticket: vêm do código 💻 |
<!-- trace-verified: PDTIC25148-34 @ f6bae69fe29f -->

---

<div class="dev-only">

## Superfície

**Tela própria** — rota `/catalogo-legendas`, que aceita o parâmetro `eventoId` para lembrar de qual evento o usuário veio

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada, ainda em teste — os documentos legados não trazem imagem dela

⚠️ O endereço `/regras-legenda`, sem o identificador do evento, abre esta mesma tela, e `/catalogo-legendas/{id}` abre a Configuração de Legendas do evento: as duas rotas compartilham a mesma lista de caminhos, o que o próprio código reconhece em comentário.

---

</div>

## Regras de negócio

1. O catálogo é um só, comum a todos os eventos: a pesquisa não depende de evento e traz os mesmos blocos de onde quer que seja aberta. 💻
2. A pesquisa procura pelo nome do bloco, por qualquer trecho dele, sem diferenciar maiúsculas de minúsculas. 💻 ❓ Nenhuma fonte diz se a acentuação é diferenciada: o código não trata disso.
3. Sem termo informado, a pesquisa traz todos os blocos do catálogo. 💻
4. O bloco do catálogo tem só nome e cor: não tem número nem posição. O número de um bloco existe apenas dentro da configuração de cada evento. 💻
5. O catálogo traz todos os blocos, estejam ou não em uso em algum evento; não existe bloco inativo nem oculto. 💻

---

## Cenários

```gherkin
Feature: Pesquisar blocos de legenda

  Background:
    Given que o usuário está autenticado no GPE
    And está na tela "Catálogo de blocos"

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Abrir o catálogo
    Given que o catálogo tem 14 blocos
    When a tela é aberta
    Then o sistema lista os 10 primeiros blocos em ordem alfabética de nome, cada um com o nome e a cor
    And o paginador, abaixo da lista, dá acesso aos 4 restantes

  Scenario: Pesquisar por parte do nome
    Given que o catálogo tem os blocos "Diretores da CNI", "Empresas – diretores" e "Palestrantes"
    When o usuário digita "diretor" no campo de busca
    And para de digitar por 300 milissegundos
    Then o sistema lista "Diretores da CNI" e "Empresas – diretores"
    And a lista volta à primeira página

  Scenario: Limpar a busca
    Given que a lista está restrita por um termo de busca
    When o usuário apaga o termo
    Then o sistema volta a listar todos os blocos do catálogo

  Scenario: Inverter a ordem da lista
    When o usuário aciona o cabeçalho da coluna "Nome"
    Then o sistema lista os blocos em ordem alfabética inversa de nome

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há dado a validar
    When o usuário digita qualquer texto no campo de busca
    Then o sistema aceita o texto e pesquisa com ele, sem restrição de formato ou de tamanho
    # 💻 espaços no início e no fim do termo são desprezados; um termo só com espaços equivale a nenhum termo

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Não há conflito possível
    When o usuário pesquisa
    Then o sistema apenas lê o catálogo, sem alterar nenhum dado

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Pesquisar Blocos de Legenda" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Administração › Catálogo de legendas, e a tela não fica ao alcance dele
    # ⚠️ a tela não confere o perfil; ver a nota da matriz no N2
    # ⚠️ 💻 no servidor, a consulta ao catálogo está declarada para os três perfis: quem chega à tela pelo endereço vê a lista, e só a inclusão, a alteração e a exclusão são recusadas

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Nenhum bloco corresponde à busca
    When o usuário digita um termo que não aparece no nome de nenhum bloco
    Then o sistema mostra, no lugar da lista, "Nenhum bloco encontrado."

  Scenario: Catálogo vazio
    Given que nenhum bloco foi cadastrado
    When a tela é aberta
    Then o sistema mostra "Nenhum bloco encontrado."

  Scenario: Falha ao carregar a lista
    Given que o servidor falha ao pesquisar
    When a tela é aberta ou o usuário pesquisa
    Then a lista fica como estava
    And o sistema exibe o erro "Erro interno do servidor."
    # 🔍 inferido da leitura do código, sem execução: nesta pesquisa o servidor responde à falha com um texto solto, e a tela cai na mensagem genérica
    # ⚠️ a mensagem genérica vem acompanhada do detalhe literal "&nbsp;" 💻
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| Buscar bloco pelo nome | Legenda | entrada do usuário | editável | texto | não | O campo não tem rótulo: o texto é a dica exibida dentro dele. Aceita qualquer texto; procura o trecho digitado no nome do bloco, sem diferenciar maiúsculas de minúsculas; vazio, traz todos os blocos |

---

## Colunas do resultado

| Coluna (Label PO) | Origem | Ordenação |
|---|---|---|
| Nome | cadastro | padrão ↑ / ordenável |
| Cor | cadastro | — |
| Ações | — | — |

A coluna "Cor" mostra uma amostra da cor; o código da cor aparece ao passar o ponteiro sobre a amostra. A coluna "Ações" traz o ícone de lápis, com a dica "Editar bloco", e o de lixeira, com a dica "Excluir bloco".

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| — | — | Nenhum campo é gravado: a pesquisa só lê |

---

## Comportamento de tela

### Onde fica
Na tela "Catálogo de blocos", que tem o subtítulo "Blocos de legenda reutilizáveis nas configurações dos eventos.". Chega-se a ela pelo menu Administração › Catálogo de legendas ou pelo botão "Gerenciar catálogo" da tela Configuração de Legendas de um evento. No cabeçalho ficam os botões "Voltar" e "Novo bloco"; abaixo, o campo de busca, com a dica "Buscar bloco pelo nome"; depois, a lista. 💻

A lista é paginada, com 10 blocos por página e o paginador embaixo, sem opção de mudar a quantidade por página. Abre em ordem alfabética de nome, e só a coluna "Nome" pode ser reordenada. A busca não tem botão: a lista é refeita 300 milissegundos depois da última tecla, voltando à primeira página. 💻

O botão "Voltar" leva à Configuração de Legendas do evento de onde o usuário veio; quando o catálogo foi aberto pelo menu, leva à lista de eventos. "Novo bloco" é Cadastrar Bloco de Legenda `EVT-LEG-12`; o lápis de cada linha é Editar Bloco de Legenda `EVT-LEG-13`; a lixeira é Excluir Bloco de Legenda `EVT-LEG-14`. Não há ação de copiar ou duplicar bloco, nem coluna de número. A lista não informa em quantos eventos cada bloco está em uso — isso só aparece na pergunta da exclusão. 💻

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Indicador de carregamento sobre a lista enquanto a consulta acontece |
| Erro de validação | Não se aplica — a busca aceita qualquer texto |
| Erro de servidor | Mensagem genérica conforme a falha — "Erro interno do servidor." na falha da pesquisa 🔍 —, com o detalhe literal `&nbsp;` ⚠️. Resposta de erro sem conteúdo: "Erro" com o detalhe "Falha de comunicação com o servidor." |
| Sucesso | A lista mostra os blocos encontrados, sem mensagem |
| Empty state | "Nenhum bloco encontrado.", com um ícone de etiquetas, tanto para a busca sem resultado quanto para o catálogo vazio |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Todo bloco cujo nome contém o trecho digitado aparece no resultado, e nenhum outro | Regra 2 · cenário "Pesquisar por parte do nome" |
| SC-02 | Sem termo de busca, a soma das páginas traz todos os blocos do catálogo, em ordem alfabética de nome | Regra 3 · cenário "Abrir o catálogo" |
| SC-03 | O resultado é o mesmo, qualquer que seja o evento de onde o catálogo foi aberto | Regra 1 |

---

## Métricas de tamanho

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Pesquisar Blocos de Legenda | principal | CE | 1 | 4 | Baixa | 3 | 2026-10-04 |

### Memória de cálculo

**Pesquisar Blocos de Legenda** — CE · ALR 1 · DER 4 · Baixa · 3 PF

```json
{"pe": "Pesquisar Blocos de Legenda",
 "alr": ["Legenda"],
 "der": ["Nome", "Cor", "Mensagem", "Ação"],
 "nao_contados": "Buscar bloco pelo nome filtra pelo mesmo atributo da coluna Nome e conta uma vez. A paginação e a coluna Ações não são DER (Guia STI 5.5)."}
```

Por que cada ALR:
1. `Legenda` — lê os blocos do catálogo cujo nome contém o termo buscado

Classificação: CE — a intenção primária é apresentar, com as formas 4, 7, 8, 11 e 13, sem cálculo nem dado derivado.

**Total: 3 PF**

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade Legenda

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Tela do catálogo: busca, lista, paginação e navegação | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/pages/catalogo-legendas/catalogo-legendas.component.ts` (linhas 92–156 e 273–280) e `.html` (linhas 5–88) | — |
| Rotas do catálogo e da configuração | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/legendas-routing.module.ts` (linhas 7–16) | — |
| Serviço do catálogo | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/services/legenda-catalogo.service.ts` (linhas 44–53) | — |
| Operação `GET /administracao/legendas` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/LegendaController.java` (linhas 52–61) | — |
| Filtro pelo nome e ordem padrão | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/LegendaServiceImpl.java` (linhas 51–88) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada e em teste (ticket `PDTIC25148-34`); o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

A operação do servidor aceita também uma busca geral, por nome ou por cor, e um filtro só por cor; a tela não usa nenhum dos dois.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-10-04 | Claude (apf-cpm) | Contagem | Primeira contagem, pelo `PROMPT_CONTAGEM`: 3 PF — Pesquisar Blocos de Legenda (CE Baixa, 3 PF). Confirmada em 2026-10-04 e espelhada em `global/CONTAGEM-PF.md` |
| 2026-10-04 | Claude (analise-impacto) | Origem atualizada | Elo com a AIM do ticket `PDTIC25148-34`, aberta na entrega: o ticket passa a ser a Origem da feature (Criação), com o critério CA-05; regras, campos e cenários inalterados |
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do código e do ticket `PDTIC25148-34` do Jira (critério CA05); a funcionalidade não consta no documento legado GPE006 – Gerenciar Regras de Legendas |

---

*Feature Set: Legendas · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
