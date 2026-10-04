<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: PES-CAD-01
feature_set: PES-CAD
dominio: PES
entidade: Pessoa
data_model_ref: data-models/pessoas.md#pessoa
endpoints: []
error_codes: []
depende_de: []
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
  pendente: true
  revisada_em: ""
  revisada_ate: ""
---

# Pesquisar Pessoas
> **Nível 3** - Feature Set: Cadastro de Pessoas — Major Feature Set: Pessoas - `PES-CAD-01`

## Descrição

Permite que o Administrador localize pessoas do cadastro por nome, CRM, razão social ou e-mail; o resultado é a lista das pessoas encontradas, em ordem alfabética de nome, de onde se abre a edição ou a exclusão de cada uma.

Chega-se pelo menu Administração › Pessoas. A tela abre já com a lista de todas as pessoas; para restringir, o usuário preenche um ou mais filtros — Nome, CRM, Razão Social, E-mail — e aciona Pesquisar. Limpar esvazia os filtros e volta à lista completa.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE003 – Manter Pessoa v1.0, de 03/10/2025 (documento legado), funcionalidade "Pesquisar Pessoas" ⚠️ sem chave na ferramenta de demandas | Criação | — Pesquisar as pessoas cadastradas por um ou vários filtros (nome, CRM, razão social e e-mail) e, a partir do resultado, gerir cada pessoa retornada. A ordem do resultado, a paginação e a pesquisa por trecho do nome e do CRM não estão no documento: vêm do código 💻 |

---

<div class="dev-only">

## Superfície

**Tela própria** — rota `/administracao-pessoas`

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Pesquisar Pessoas" de GPE003

---

</div>

## Regras de negócio

1. Os critérios de pesquisa — nome, CRM, razão social e e-mail — são opcionais e se somam: a pessoa entra no resultado quando atende a todos os que foram informados.
2. Sem nenhum critério informado, o resultado traz todas as pessoas do cadastro. 💻
3. Cada critério localiza pelo trecho informado, em qualquer posição do texto, sem diferenciar maiúsculas de minúsculas. 💻 ⚠️ GPE003 fala em busca por parte do texto só para a razão social e o e-mail 📄; no código, o mesmo vale para o nome e para o CRM. Se letra acentuada e letra sem acento contam como iguais, nenhuma fonte responde ❓.
4. O resultado vem sempre em ordem alfabética crescente de nome. 💻
5. A pesquisa alcança todas as pessoas do cadastro, qualquer que seja a origem do cadastro de cada uma. 💻

---

## Cenários

```gherkin
Feature: Pesquisar pessoas

  Background:
    Given que o usuário está autenticado no GPE
    And abriu a tela "Pessoas" pelo menu Administração › Pessoas

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Abrir a tela sem informar filtro
    When a tela "Pessoas" é aberta
    Then o sistema lista todas as pessoas do cadastro, em ordem alfabética de nome
    And mostra 10 pessoas por página

  Scenario: Pesquisar por trecho do nome
    When o usuário preenche "Nome" com "mari"
    And aciona "Pesquisar"
    Then o sistema lista as pessoas cujo nome contém "mari", como "Maria Souza" e "Ana Marinho"
    And a lista volta à primeira página

  Scenario: Combinar filtros
    When o usuário preenche "Nome" com "maria" e "Razão Social" com "exemplo"
    And aciona "Pesquisar"
    Then o sistema lista só as pessoas que atendem aos dois filtros

  Scenario: Limpar os filtros
    Given que há filtros preenchidos
    When o usuário aciona "Limpar"
    Then os filtros "Nome", "CRM", "Razão Social" e "E-mail" ficam vazios
    And o sistema lista de novo todas as pessoas

  Scenario: Percorrer as páginas do resultado
    Given que o resultado tem mais de 10 pessoas
    When o usuário avança para a página seguinte
    Then o sistema mostra as 10 pessoas seguintes
    And o indicador de posição passa a "[11 a 20 de 47]", para um resultado de 47 pessoas

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há dado a validar
    When o usuário aciona "Pesquisar" com qualquer texto nos filtros
    Then o sistema pesquisa pelo que foi digitado, sem conferir formato nem tamanho

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Não há conflito possível
    When o usuário pesquisa
    Then o sistema apenas consulta o cadastro, sem alterar nenhum dado

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Pesquisar Pessoas" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Administração › Pessoas, e a tela não fica ao alcance dele pelo menu
    # ⚠️ a tela não confere o perfil; ver a nota da matriz no N2

  Scenario: Usuário sem acesso informa o endereço da tela
    Given que o perfil do usuário não tem acesso a "Pesquisar Pessoas" na matriz do N2
    When o usuário digita o endereço da tela "Pessoas" no navegador
    Then a tela abre, porque só o menu restringe o acesso
    # ⚠️ 💻 nenhuma tela do sistema confere o perfil; o que o servidor devolve a esse perfil depende do cadastro corporativo ❓

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Nenhuma pessoa atende aos filtros
    When o usuário pesquisa por um texto que nenhuma pessoa tem
    Then o sistema exibe: "Nenhuma pessoa encontrada."
    And deixa de mostrar o cabeçalho das colunas

  Scenario: Acionar o ícone de ordenação de uma coluna
    When o usuário aciona o ícone de ordenação da coluna "Cargo"
    Then o sistema consulta de novo o cadastro
    And a lista continua em ordem alfabética de nome
    # ⚠️ 💻 os ícones de ordenação aparecem em seis colunas e nenhum muda a ordem — suspeita de defeito

  Scenario: Falha ao consultar
    Given que a consulta ao servidor falha
    When o usuário aciona "Pesquisar"
    Then o indicador de carregamento some e a lista fica como estava
    And o sistema não informa a falha ao usuário
    # ⚠️ 💻 a falha só fica registrada no navegador; se ocorrer na abertura da tela, a lista vazia mostra "Nenhuma pessoa encontrada."
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| Nome | Pessoa | entrada do usuário | editável | texto | não | Filtro. Localiza pelo trecho informado, em qualquer posição do nome; sem limite de tamanho e sem validação 💻 |
| CRM | Pessoa | entrada do usuário | editável | texto | não | Filtro. Localiza pelo trecho informado do código da pessoa no CRM; aceita qualquer texto 💻 |
| Razão Social | Pessoa | entrada do usuário | editável | texto | não | Filtro. Localiza pelo trecho informado do nome da organização |
| E-mail | Pessoa | entrada do usuário | editável | texto | não | Filtro. Localiza pelo trecho informado do e-mail; o formato não é conferido |

*Um filtro preenchido só com o texto `null` é tratado como vazio 💻 ⚠️ — efeito colateral da forma como os filtros em branco são enviados ao servidor.*

---

## Colunas do resultado

| Coluna (Label PO) | Origem | Ordenação |
|---|---|---|
| Nome | cadastro | padrão ↑ — fixa; o ícone de ordenação aparece e não tem efeito ⚠️ |
| Email | cadastro | — · o ícone de ordenação aparece e não tem efeito ⚠️ |
| Codinome | cadastro | — · o ícone de ordenação aparece e não tem efeito ⚠️ |
| CRM | cadastro | — · o ícone de ordenação aparece e não tem efeito ⚠️ |
| Razão Social | cadastro | — · o ícone de ordenação aparece e não tem efeito ⚠️ |
| Cargo | cadastro | — · o ícone de ordenação aparece e não tem efeito ⚠️ |
| Data de Criação | cadastro | — · sem ícone de ordenação. Exibida só com a data, no formato dd/mm/aaaa |

*O rótulo do filtro é "E-mail" e o da coluna é "Email": as duas grafias estão assim na tela e no documento legado.*

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| — | — | Nenhum campo é gravado: a feature só consulta |

---

## Comportamento de tela

### Onde fica
No menu Administração › Pessoas. A tela, de título "Pessoas", tem em cima o quadro dos filtros e embaixo a "Lista de Pessoas". Sob os filtros ficam, nesta ordem, os botões "Pesquisar", "Limpar", "Adicionar", "Carga de GT", "Carga de Temas" e "Carga de Histórico": "Adicionar" abre a inclusão de uma pessoa (Cadastrar Pessoa `PES-CAD-02`), e os de carga abrem as janelas de Carregar Grupos de Trabalho `PES-CAD-05`, Carregar Temas `PES-CAD-06` e Carregar Histórico de Participação `PES-CAD-07`. Nenhum desses botões depende do perfil de quem está na tela 💻.

Em cada linha da lista, antes das colunas, ficam o ícone de lápis, que abre a pessoa para alteração (Editar Pessoa `PES-CAD-03`), e o ícone de lixeira (Excluir Pessoa `PES-CAD-04`). O código dá a esses ícones as dicas "Editar Pessoa" e "Remover Pessoa" 💻 ⚠️ 🔍 — pela forma como a tela foi montada, é provável que as dicas não apareçam ao passar o cursor; a confirmar em execução.

A lista mostra 10 pessoas por página, com a paginação sempre visível embaixo e o indicador de posição no formato "[1 a 10 de 47]". Acionar "Pesquisar" ou "Limpar" leva de volta à primeira página.

As colunas "Nome", "Email", "Codinome", "CRM", "Razão Social" e "Cargo" trazem ícone de ordenação; "Data de Criação" não traz. Acionar um desses ícones refaz a consulta, mas a ordem pedida ao servidor é sempre a de nome, crescente 💻 ⚠️ — suspeita de defeito: o ícone promete uma ordenação que não acontece.

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Indicador de carregamento sobre a lista enquanto a consulta está em andamento |
| Erro de validação | Não se aplica — os filtros não têm validação |
| Erro de servidor | Nenhuma mensagem: o indicador de carregamento some e a lista fica como estava ⚠️ 💻. Se a falha acontece na abertura da tela, a lista vazia mostra "Nenhuma pessoa encontrada." |
| Sucesso | Lista preenchida, com a paginação e o indicador de posição |
| Empty state | "Nenhuma pessoa encontrada.", centralizado, sem o cabeçalho das colunas |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Uma pessoa cadastrada é encontrada informando qualquer trecho do seu nome, do seu CRM, da sua razão social ou do seu e-mail | Regra 3 · cenário "Pesquisar por trecho do nome" |
| SC-02 | Com mais de um filtro preenchido, o resultado só traz pessoas que atendem a todos eles | Regra 1 · cenário "Combinar filtros" |
| SC-03 | O resultado está sempre em ordem alfabética de nome | Regra 4 |
| SC-04 | Uma pesquisa sem resultado informa "Nenhuma pessoa encontrada." | Cenário "Nenhuma pessoa atende aos filtros" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Pesquisar Pessoas | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade Pessoa

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Filtros e botões da tela | sistema_mesa_checkin_frontend | `src/app/admin/administracao/acessibilidade/pessoas/pages/pessoas/components/pessoas-filter/pessoas-filter.component.html` (linhas 4–105) e `.ts` (linhas 60–76) | — |
| Lista, paginação e colunas | sistema_mesa_checkin_frontend | `src/app/admin/administracao/acessibilidade/pessoas/pages/pessoas/components/pessoas-list/pessoas-list.component.ts` (linhas 97–120 e 179–231) e `.html` (linhas 8–96) | — |
| Operação `GET /administracao/pessoas` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/PessoaController.java` (linhas 62–71) | — |
| Critérios da pesquisa e paginação | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/PessoaServiceImpl.java` (linhas 49–123) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

A consulta envia sempre a ordem `nomeCompleto` crescente, qualquer que seja a coluna acionada (`pessoas-list.component.ts`, linhas 101–108). O servidor aceita outros critérios que a tela não oferece — codinome, sexo, cargo, CPF, estado, com ou sem foto e um filtro geral.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE003 – Manter Pessoa (funcionalidade "Pesquisar Pessoas") e do código |

---

*Feature Set: Cadastro de Pessoas · Major Feature Set: Pessoas · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
