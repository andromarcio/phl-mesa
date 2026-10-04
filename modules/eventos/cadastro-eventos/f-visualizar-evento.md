<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: EVT-CAD-04
feature_set: EVT-CAD
dominio: EVT
entidade: Evento
data_model_ref: data-models/eventos.md#evento
endpoints: []
error_codes: []
depende_de: ["EVT-CAD-01"]
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

# Visualizar Evento
> **Nível 3** - Feature Set: Cadastro de Eventos — Major Feature Set: Eventos - `EVT-CAD-04`

## Descrição

Permite que o Administrador visualize os dados básicos de um evento em modo de leitura, sem poder alterá-los, e baixe a imagem anexada a ele.

A visualização é aberta pelo ícone Visualizar evento, em cada linha da lista de eventos. A tela mostra cada dado como texto e oferece apenas o botão Voltar.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE004 – Manter Evento v1.1, de 16/12/2025 (documento legado), funcionalidade "Visualizar Evento" — "Detalhar Evento" na tela e na tabela de perfis do documento ⚠️ sem chave na ferramenta de demandas | Criação | — Visualizar os dados básicos do evento no modo de apenas leitura, sem que nenhum dado possa ser editado. O campo Código da Campanha não está no documento: vem do ticket do Jira `PDTIC25148-36`, em teste; AIM ainda não aberta 💻 |

---

<div class="dev-only">

## Superfície

**Tela própria** — rota `/eventos/detail/view/:id`

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Detalhar Evento" de GPE004

---

</div>

## Regras de negócio

1. Na visualização, nenhum dado do evento pode ser alterado.
2. A visualização mostra os mesmos dados básicos do cadastro: Nome do Evento, Data e Hora, Local, Tipo de Evento, Tipo de Mesa, Participantes, Código da Campanha e a imagem do evento. O Código da Campanha vem do código 💻; a imagem de GPE004 não o traz 📄.
3. Não fazem parte da visualização a condição de evento principal, os participantes e os assentos do evento. 💻
4. O evento excluído continua podendo ser visualizado por quem tem o endereço dele. 💻 ⚠️ GPE004 diz que, após a exclusão, "o evento passa a não ser exibido no sistema" 📄.

---

## Cenários

```gherkin
Feature: Visualizar evento

  Background:
    Given que o usuário está autenticado no GPE
    And está na lista de eventos

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Visualizar os dados do evento
    When o usuário aciona "Visualizar evento" na linha de "Reunião de Diretoria"
    Then o sistema mostra cada dado do evento como texto, sem campo de entrada
    And a data aparece como dia/mês/ano e hora:minuto, por exemplo "20/10/2026 09:00"
    And o botão "Salvar" não aparece
    # ⚠️ 💻 o título da tela é "Editar Evento", o mesmo da edição; a imagem "Detalhar Evento" de GPE004 mostra o título "Dados do Evento" 📄

  Scenario: Baixar a imagem do evento
    Given que o evento visualizado tem uma imagem
    When o usuário aciona o botão com o nome do arquivo
    Then o navegador baixa a imagem do evento

  Scenario: Evento sem imagem
    Given que o evento visualizado não tem imagem
    When a tela é exibida
    Then no lugar do arquivo aparece o texto "Nenhuma imagem inserida."

  Scenario: Voltar para a lista
    When o usuário aciona "Voltar"
    Then o sistema volta à tela Eventos

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há dado a validar
    When o usuário visualiza um evento
    Then o sistema não solicita nenhum dado

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Não há conflito a tratar
    When o usuário visualiza um evento
    Then o sistema apenas lê o evento, sem alterar nenhum dado

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Visualizar Evento" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Eventos › Cadastro, e a visualização não fica ao alcance dele
    # ⚠️ o ícone "Visualizar evento" e a tela não conferem o perfil, e a consulta de eventos está declarada no servidor para mais perfis: quem digita o endereço da tela vê o evento — ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Evento não encontrado
    Given que o evento não existe no servidor
    When o usuário abre a visualização pelo endereço da tela
    Then a tela abre com os dados em branco e o texto "Nenhuma imagem inserida.", sem nenhum aviso
    # ⚠️ 🔍 a falha na leitura do evento não é tratada pela tela

  Scenario: Evento excluído visualizado pelo endereço
    Given que o evento "Reunião de Diretoria" foi excluído
    When o usuário abre a visualização dele pelo endereço da tela
    Then o sistema mostra os dados do evento normalmente
    # ⚠️ 💻 a leitura de um evento não distingue o excluído (regra 4)

  Scenario: Falha ao baixar a imagem
    Given que a imagem do evento não pôde ser lida no servidor
    When o usuário aciona o botão com o nome do arquivo
    Then nada é baixado, e a tela não mostra nenhum aviso
    # ⚠️ 🔍 a falha no download não é tratada pela tela
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| Nome do Evento | Evento | exibido do cadastro | somente leitura | texto | — | — |
| Data e Hora | Evento | exibido do cadastro | somente leitura | data e hora | — | Exibida como dia/mês/ano e hora:minuto |
| Local | Evento | exibido do cadastro | somente leitura | texto | — | — |
| Tipo de Evento | TipoEvento | exibido do cadastro | somente leitura | seleção → TipoEvento | — | Mostra o nome do tipo de evento |
| Tipo de Mesa | TipoMesa | exibido do cadastro | somente leitura | seleção → TipoMesa | — | Mostra o nome do tipo de mesa |
| Participantes | Evento | exibido do cadastro | somente leitura | número | — | A quantidade prevista, informada no cadastro |
| Código da Campanha | Evento | exibido do cadastro | somente leitura | texto | — | Em branco quando o evento não tem código 💻 |
| Arquivo | Arquivo | exibido do cadastro | somente leitura | arquivo | — | Botão com o nome do arquivo, que baixa a imagem; sem imagem, o texto "Nenhuma imagem inserida." |

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| — | — | Nenhum campo é gravado: a visualização só lê |

---

## Comportamento de tela

### Onde fica
Em tela própria, aberta pelo ícone de olho com a dica "Visualizar evento", em cada linha da lista de eventos. É a mesma tela do cadastro e da edição, em modo de leitura: cada campo vira texto, na mesma ordem, e o rodapé traz só o botão "Voltar", que leva à tela Eventos.

⚠️ O título da tela é "Editar Evento", igual ao da edição 💻; na imagem "Detalhar Evento" de GPE004 o título é "Dados do Evento" 📄. Os asteriscos dos campos obrigatórios e o texto "Campos com * são obrigatórios" continuam aparecendo, embora nada possa ser preenchido.

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Sem indicador: os dados aparecem instantes depois de a tela abrir 💻 |
| Erro de validação | Não se aplica — não há campo de entrada |
| Erro de servidor | ⚠️ Nenhum aviso: se o evento não puder ser lido, a tela fica com os dados em branco 🔍 |
| Sucesso | Os dados do evento são exibidos como texto |
| Empty state | Evento sem imagem: o texto "Nenhuma imagem inserida." no lugar do arquivo |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Os dados exibidos são os que estão gravados no cadastro do evento | Regra 2 · cenário "Visualizar os dados do evento" |
| SC-02 | Nenhum dado do evento pode ser alterado a partir da visualização: não há campo de entrada nem botão de gravação | Regra 1 |
| SC-03 | A imagem do evento, quando existe, pode ser baixada pela visualização | Cenário "Baixar a imagem do evento" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Visualizar Evento | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade Evento

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Modo de leitura da tela do evento, título e download da imagem | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento/pages/evento/create/evento-create.component.ts` (linhas 49–56, 65–80 e 248–263) e `.html` (linhas 7–10, 43, 72, 234–248 e 266–271) | — |
| Rota da visualização | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento/evento-routing.module.ts` (linha 11) | — |
| Operação `GET /administracao/eventos/{id}` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoController.java` (linhas 85–90) | — |
| Operação `GET /administracao/eventos/anexos/{id}` — conteúdo da imagem | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoController.java` (linhas 110–128) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE004 – Manter Evento (funcionalidade "Visualizar Evento", tela "Detalhar Evento") e do código |

---

*Feature Set: Cadastro de Eventos · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
