<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: EVT-CAD-01
feature_set: EVT-CAD
dominio: EVT
entidade: Evento
data_model_ref: data-models/eventos.md#evento
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

# Pesquisar Eventos
> **Nível 3** - Feature Set: Cadastro de Eventos — Major Feature Set: Eventos - `EVT-CAD-01`

## Descrição

Permite que o Administrador pesquise os eventos cadastrados por nome, local, tipo de evento, tipo de mesa ou data, e veja de cada um a data e o horário, o local, o tipo, o formato da mesa, a quantidade de participantes e se é o evento principal.

A pesquisa abre pelo menu Eventos › Cadastro e já traz todos os eventos, do incluído por último para o mais antigo. O Administrador informa um ou mais filtros e aciona Pesquisar; de cada linha do resultado partem as ações sobre o evento, como visualizar, editar e excluir.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE004 – Manter Evento v1.1, de 16/12/2025 (documento legado), funcionalidade "Pesquisar Eventos" ⚠️ sem chave na ferramenta de demandas | Criação | — Pesquisar os eventos cadastrados por um ou mais filtros e, a partir do resultado, chegar à gestão de cada evento. O selo "Finalizado", o texto relativo da data e o tipo de mesa Retangular Invertido não estão no documento: vêm do código 💻. Os ícones de ação aparecem na imagem do documento, sem descrição no texto |

---

<div class="dev-only">

## Superfície

**Tela própria** — rota `/eventos`

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Pesquisar Evento" de GPE004

---

</div>

## Regras de negócio

1. O evento excluído não entra no resultado da pesquisa. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 3
2. Os critérios informados valem em conjunto: o evento precisa atender a todos eles. 💻
3. Sem nenhum critério, a pesquisa traz todos os eventos não excluídos. 💻
4. Nome e Local localizam o evento por qualquer parte do texto, sem diferenciar maiúsculas de minúsculas. A indiferença a maiúsculas vem do código 💻.
5. Tipo de Evento e Tipo de Mesa localizam os eventos que têm exatamente o tipo escolhido.
6. Data Inicial localiza os eventos cuja data é igual ou posterior a ela. 💻
7. Data Final não limita o resultado. 💻 ⚠️ GPE004 a traz ao lado da Data Inicial, como fim do período de realização 📄; no servidor, a Data Final repete a comparação da Data Inicial e, informada sozinha, é desconsiderada. Suspeita de defeito.
8. É finalizado o evento cuja data é anterior à meia-noite de hoje; o evento de hoje não é finalizado, ainda que o horário dele já tenha passado. 💻

---

## Cenários

```gherkin
Feature: Pesquisar eventos

  Background:
    Given que o usuário está autenticado no GPE
    And abriu a tela Eventos pelo menu Eventos › Cadastro

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Abrir a pesquisa
    When a tela Eventos é aberta
    Then o sistema pesquisa sem nenhum filtro e lista todos os eventos não excluídos
    And a lista vem do evento incluído por último para o mais antigo

  Scenario: Pesquisar por parte do nome
    Given que existem os eventos "Reunião de Diretoria" e "Comitê de Inovação"
    When o usuário preenche "Nome:" com "diretoria"
    And aciona "Pesquisar"
    Then o sistema lista "Reunião de Diretoria" e não lista "Comitê de Inovação"

  Scenario: Combinar filtros
    Given que existem dois eventos no local "Sede da CNI", um do tipo "Reunião" e outro do tipo "Seminário"
    When o usuário preenche "Local:" com "sede" e escolhe "Reunião" em "Tipo de Evento:"
    And aciona "Pesquisar"
    Then o sistema lista apenas o evento do tipo "Reunião"

  Scenario: Pesquisar a partir de uma data
    Given que existem eventos em 10/03/2026 e em 20/04/2026
    When o usuário preenche "Data Inicial:" com "01/04/2026"
    And aciona "Pesquisar"
    Then o sistema lista apenas o evento de 20/04/2026

  Scenario: Limpar os filtros
    Given que o usuário pesquisou com filtros preenchidos
    When aciona "Limpar"
    Then os filtros ficam vazios
    And o sistema volta a listar todos os eventos não excluídos

  Scenario: Ordenar por uma coluna
    When o usuário aciona o cabeçalho da coluna "Data e Horário"
    Then o sistema refaz a consulta ordenada pela data do evento
    And um novo acionamento do mesmo cabeçalho inverte a ordem

  Scenario: Reconhecer evento finalizado
    Given que o evento "Reunião de Diretoria" aconteceu ontem
    When o sistema lista o evento
    Then o nome vem acompanhado do selo "Finalizado"
    And a linha inteira aparece esmaecida

  Scenario: Ler quanto falta para o evento
    Given que faltam 9 dias e 12 horas para o evento "Comitê de Inovação"
    When o sistema lista o evento
    Then abaixo da data e do horário aparece "Em 10 dias"
    # 💻 os textos possíveis são "Hoje", "Amanhã", "Ontem", "Em {n} dias" e "Há {n} dias"
    # ⚠️ a conta é feita em blocos de 24 horas a partir do momento da consulta, não por dia do calendário:
    #    o evento de hoje que ainda vai começar aparece como "Amanhã", e "Hoje" só aparece para o evento
    #    que começou há menos de 24 horas — suspeita de defeito 💻

  Scenario: Seguir para os participantes do evento
    When o usuário aciona o ícone "Participantes" na linha de um evento
    Then o sistema abre, em nova aba do navegador, os participantes daquele evento
    # os participantes são do Feature Set Participantes (EVT-PAR); as demais ações da linha estão em "Comportamento de tela"

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Período invertido não é criticado
    When o usuário preenche "Data Inicial:" com "20/04/2026" e "Data Final:" com "10/03/2026"
    And aciona "Pesquisar"
    Then o sistema executa a pesquisa sem criticar o período
    # 💻 nenhum filtro é obrigatório nem tem o conteúdo conferido

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Não há conflito a tratar
    When o usuário pesquisa eventos
    Then o sistema apenas lê os eventos, sem alterar nenhum dado

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Pesquisar Eventos" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Eventos › Cadastro, e a pesquisa não fica ao alcance dele
    # ⚠️ a tela não confere o perfil, e a consulta de eventos está declarada no servidor para mais perfis; ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Nenhum evento encontrado
    Given que nenhum evento atende aos filtros informados
    When o usuário aciona "Pesquisar"
    Then o sistema mostra um ícone de calendário e o texto "Nenhum evento encontrado"
    And oferece o botão "Criar Primeiro Evento", que leva ao cadastro de evento

  Scenario: Data Final não limita o período
    Given que existem eventos em 10/03/2026 e em 20/04/2026
    When o usuário preenche "Data Inicial:" com "01/03/2026" e "Data Final:" com "31/03/2026"
    And aciona "Pesquisar"
    Then o sistema lista os dois eventos
    # ⚠️ suspeita de defeito 💻: o esperado pelo documento é listar só o evento de 10/03/2026 📄

  Scenario: Data Final informada sozinha
    When o usuário preenche apenas "Data Final:" com "31/03/2026"
    And aciona "Pesquisar"
    Then o sistema lista todos os eventos não excluídos, como se nenhum filtro de data tivesse sido informado
    # ⚠️ mesma suspeita de defeito 💻

  Scenario: Falha ao consultar os eventos
    Given que a consulta de eventos falha
    When o usuário aciona "Pesquisar"
    Then a lista permanece como estava, sem nenhum aviso ao usuário
    # ⚠️ 💻 a falha só é registrada internamente pelo navegador

  Scenario: Falha ao carregar os tipos de mesa
    Given que a lista de tipos de mesa não pôde ser carregada
    When a tela Eventos é aberta
    Then o filtro "Tipo de Mesa:" fica sem opções, sem nenhum aviso
    And o filtro "Tipo de Evento:" também é esvaziado
    # ⚠️ 💻 o tratamento da falha dos tipos de mesa apaga a lista de tipos de evento — suspeita de defeito
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| Nome: | Evento | entrada do usuário | editável | texto | não | Qualquer parte do nome do evento. Sem limite de tamanho no filtro 💻 |
| Local: | Evento | entrada do usuário | editável | texto | não | Qualquer parte do local do evento |
| Tipo de Evento: | TipoEvento | entrada do usuário | editável | seleção → TipoEvento | não | Uma opção, que pode ser desmarcada. Tipos existentes: Reunião, Comitê e Seminário |
| Tipo de Mesa: | TipoMesa | entrada do usuário | editável | seleção → TipoMesa | não | Uma opção, que pode ser desmarcada. Tipos existentes: Retangular e Retangular Invertido 💻 ⚠️ GPE004 só lista Retangular 📄 |
| Data Inicial: | Evento | entrada do usuário | editável | data | não | Dia, mês e ano, sem hora, escolhidos em calendário que vai de 1950 a 2050. Não é comparada com a Data Final 💻 |
| Data Final: | Evento | entrada do usuário | editável | data | não | Dia, mês e ano, sem hora. ⚠️ Não limita o resultado (regra 7) |

*Os seis filtros são opcionais e se combinam; Data Inicial e Data Final referem-se ao campo Data e Hora do evento.*

---

## Colunas do resultado

| Coluna (Label PO) | Origem | Ordenação |
|---|---|---|
| Nome | cadastro (Evento). Quando o evento é finalizado (regra 8), o nome vem com o selo "Finalizado" — derivado da Data e Hora 💻 | ordenável |
| Data e Horário | cadastro (Evento), como dia/mês/ano e hora:minuto. Abaixo, um texto relativo — "Hoje", "Amanhã", "Ontem", "Em {n} dias" ou "Há {n} dias" — derivado da Data e Hora e do momento da consulta 💻 | ordenável |
| Local | cadastro (Evento) | ordenável |
| Tipo | entidade relacionada (TipoEvento) — nome do tipo de evento | ordenável |
| Formato da Mesa | entidade relacionada (TipoMesa) — nome do tipo de mesa | ordenável |
| Nº de Participantes | cadastro (Evento) — a quantidade prevista, informada no cadastro; não é a contagem de participantes do evento | ordenável |
| Principal | cadastro (Evento) — "Sim" ou "Não" | ordenável |
| Ações | — ícones de ação da linha (ver Comportamento de tela) | — |

*Ordem padrão: do evento incluído por último para o mais antigo 💻 — não corresponde a nenhuma coluna. Acionar um cabeçalho ordena por aquela coluna, em ordem crescente ou decrescente.*

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| — | — | Nenhum campo é gravado: a pesquisa só lê |

---

## Comportamento de tela

### Onde fica
No menu Eventos › Cadastro. A tela tem, em cima, o título "Eventos", os filtros e os botões "Pesquisar", "Limpar" e "Adicionar"; embaixo, a lista de eventos com o paginador. O botão "Adicionar" leva a Cadastrar Evento `EVT-CAD-02` e só aparece para o perfil Administrador — e para um perfil "Gestor", que não existe no cadastro corporativo ⚠️ 💻 (ver a nota da matriz no N2). A pesquisa é disparada sozinha quando a tela abre.

A lista tem 10 linhas por página, com o paginador sempre visível embaixo. ⚠️ A primeira consulta, e a recarga feita depois de definir o evento principal, pedem só 5 eventos ao servidor 💻 — a página pode vir com 5 linhas numa lista de 10; suspeita de defeito 🔍. A imagem de GPE004 mostra, no paginador, o total de registros e um seletor de linhas por página que a tela atual não tem.

### Ações de cada linha

A coluna "Ações" traz, nesta ordem, os ícones abaixo; o nome entre aspas é a dica que aparece ao passar o cursor. Nenhum deles confere o perfil do usuário ⚠️ 💻.

| Ícone (dica) | Quando aparece | Aonde leva |
|---|---|---|
| "Configuração de Legendas" | sempre | Configuração de legendas do evento — Feature Set Legendas (`EVT-LEG`), a partir de Consultar Configuração de Legendas `EVT-LEG-01` |
| "Tornar evento principal" | quando o evento não é o principal | Definir Evento Principal `EVT-CAD-06` |
| "Este evento é o principal" | quando o evento é o principal | Só indica a condição; não tem ação |
| "Cargas de Convidados e Confirmados" | sempre | Janela das cargas: Carregar Convidados `EVT-CAD-07`, Carregar Confirmados `EVT-CAD-08` e Importar Inscritos do CRM `EVT-CAD-09` |
| "Participantes" | sempre | Participantes do evento, em nova aba do navegador — Feature Set Participantes (`EVT-PAR`), a partir de Pesquisar Participantes `EVT-PAR-01` |
| "Visualizar evento" | sempre | Visualizar Evento `EVT-CAD-04` |
| "Editar evento" | sempre | Editar Evento `EVT-CAD-03` |
| "Excluir evento" | sempre | Excluir Evento `EVT-CAD-05` |

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Indicador de carregamento sobre a lista enquanto a consulta não responde |
| Erro de validação | Não se aplica — nenhum filtro é obrigatório nem tem o conteúdo conferido; período invertido não é criticado 💻 |
| Erro de servidor | ⚠️ Nenhum aviso: a falha na consulta só é registrada internamente, e a lista fica como estava 💻. A falha ao carregar os tipos também não avisa: os filtros de tipo ficam sem opções |
| Sucesso | A lista é preenchida com os eventos encontrados; o evento finalizado aparece esmaecido e com o selo "Finalizado" |
| Empty state | Ícone de calendário, o texto "Nenhum evento encontrado" e o botão "Criar Primeiro Evento", que leva ao cadastro de evento. ⚠️ O botão aparece para qualquer perfil 💻 |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Todo evento não excluído que atende a todos os filtros informados aparece no resultado, e nenhum evento excluído aparece | Regras 1 e 2 · cenário "Combinar filtros" |
| SC-02 | Informada a Data Inicial, nenhum evento anterior a ela aparece no resultado | Regra 6 · cenário "Pesquisar a partir de uma data" |
| SC-03 | O evento de data passada é reconhecido na lista pelo selo "Finalizado", sem que seja preciso abri-lo | Regra 8 · cenário "Reconhecer evento finalizado" |
| SC-04 | De cada linha do resultado o Administrador chega, com um acionamento, a cada ação disponível para o evento | Comportamento de tela — Ações de cada linha |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Pesquisar Eventos | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade Evento

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Filtros e botões da tela Eventos | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento/pages/eventos/components/eventos-filter/eventos-filter.component.ts` (linhas 41–124) e `.html` (linhas 1–76) | — |
| Lista, selo, texto relativo, ações por linha e estado vazio | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento/pages/eventos/components/eventos-list/evento-list.component.ts` (linhas 56–102 e 148–169) e `.html` (linhas 1–121) | — |
| Operação `GET /administracao/eventos` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoController.java` (linhas 74–83) | — |
| Critérios da pesquisa e defeito da Data Final | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/EventoServiceImpl.java` (linhas 82–159; Data Final nas linhas 147–153) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

O servidor aceita ainda critérios que a tela não envia: texto livre sobre nome, local e tipos, faixa de quantidade de participantes e existência de imagem.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE004 – Manter Evento (funcionalidade "Pesquisar Eventos") e do código |

---

*Feature Set: Cadastro de Eventos · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
