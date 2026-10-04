<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: EVT-PAR-02
feature_set: EVT-PAR
dominio: EVT
entidade: EventoPessoa
data_model_ref: data-models/eventos.md#eventopessoa
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
  pendente: true
  revisada_em: ""
  revisada_ate: ""
---

# Cadastrar Participante
> **Nível 3** - Feature Set: Participantes — Major Feature Set: Eventos - `EVT-PAR-02`

## Descrição

Permite que a recepção do evento cadastre, na hora, uma pessoa que não estava na lista: ela entra no cadastro de pessoas e passa a ser participante do evento, já com o check-in registrado quando assim indicado.

O cadastro é aberto pelo botão Cadastrar Pessoa, no cabeçalho da tela de participantes. Informam-se o nome completo, a instituição ou empresa, o cargo e o e-mail, decide-se se o check-in é automático e aciona-se Enviar.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE005 – Gerenciar Participante v1.1, de 16/12/2025 (documento legado), funcionalidade "Incluir Participante" ⚠️ sem chave na ferramenta de demandas | Criação | — Cadastrar uma pessoa diretamente em um evento, informando os dados básicos; a pessoa é incluída como participante do evento e no cadastro de pessoas. A opção de check-in automático entrou na v1.1 do documento, que cita os tickets `PDTIC25148-32`, `PDTIC25148-20` e `PDTIC25148-28` sem dizer qual deles a originou ❓. No Jira, o cadastro de pessoas no dia do evento é o ticket `PDTIC25148-15` 🔍 |

---

<div class="dev-only">

## Superfície

**Modal** — origem: Pesquisar Participantes `EVT-PAR-01` (`/evento-pessoa/:id`), botão "Cadastrar Pessoa" no cabeçalho da tela

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Incluir Participante" de GPE005 (`GPE005-03.png`)

---

</div>

## Regras de negócio

1. O cadastro inclui a pessoa no cadastro de pessoas e, ao mesmo tempo, como participante do evento aberto.
2. O cadastro cria sempre uma pessoa nova: o sistema não procura, antes, pessoa já cadastrada com o mesmo nome ou o mesmo e-mail. 💻 ⚠️ Quem já está no cadastro de pessoas e é incluído por aqui fica em duplicidade; GPE005 não trata do caso 📄. Confirmar com o PO se a recepção deveria poder escolher uma pessoa já cadastrada.
3. A pessoa cadastrada por aqui fica sem o `Cód. Contato` do CRM. 💻 🔍 Como as cargas e a importação do CRM reconhecem a pessoa por esse código, uma carga posterior que traga a mesma pessoa tende a criar outro cadastro em vez de aproveitar este.
4. Nome completo, instituição ou empresa, cargo e e-mail são obrigatórios. ⚠️ A exigência é conferida antes do envio; o servidor não a repete e aceitaria o cadastro sem esses dados 💻.
5. O formato do e-mail não é conferido. 💻 ⚠️
6. O participante incluído entra no evento como não convidado e não confirmado. 💻
7. Com o check-in automático, o participante já entra com o check-in feito; sem ele, entra sem check-in.
8. O check-in feito pelo cadastro fica sem data e hora. 💻 ⚠️ Suspeita de defeito: o check-in registrado na lista guarda o momento, e é por esse momento que a fila da secretaria de mesa se ordena — quem entra por aqui tende a aparecer à frente de todos, e não na ordem de chegada 🔍.
9. O participante incluído entra sem legenda e sem assento; a legenda só vem com a geração das legendas do evento ou por atribuição manual. 💻
10. O participante cadastrado com check-in automático passa a constar entre as pessoas do mapa de assentos; cadastrado sem check-in, e por não estar confirmado, fica fora do mapa. 💻

---

## Cenários

```gherkin
Feature: Cadastrar participante

  Background:
    Given que o usuário está autenticado no GPE
    And abriu os participantes de um evento

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Cadastrar participante com check-in automático
    When o usuário aciona "Cadastrar Pessoa"
    And preenche "Nome Completo:" com "Marina Duarte", "Instituição/Empresa" com "Acme Ltda", "Cargo" com "Diretora" e "E-mail" com "marina@acme.com.br"
    And mantém "Check-in Automático" marcado
    And aciona "Enviar"
    Then o sistema cria a pessoa "Marina Duarte" e a inclui como participante do evento, com o check-in feito
    And exibe: "Sucesso" com o detalhe "Cadastro de pessoa na recepção realizado com sucesso"
    And a janela é fechada
    # ⚠️ a lista de participantes não é recarregada: a nova pessoa só aparece depois de nova pesquisa 💻
    # ⚠️ a mensagem fica na tela até ser fechada por quem a vê 💻

  Scenario: Cadastrar participante sem check-in automático
    When o usuário preenche os dados da pessoa, desmarca "Check-in Automático" e aciona "Enviar"
    Then o sistema cria a pessoa e a inclui como participante do evento, sem check-in

  Scenario: Desistir do cadastro
    Given que a janela de cadastro está aberta com dados preenchidos
    When o usuário fecha a janela
    Then nada é cadastrado
    And os dados digitados são descartados

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Campo obrigatório vazio
    When o usuário passa por "Nome Completo:", "Instituição/Empresa", "Cargo" ou "E-mail" sem preencher
    Then o sistema exibe abaixo do campo: "Este campo é obrigatório"
    And o botão "Enviar" fica desabilitado
    # ← MESSAGE-DICTIONARY: BASELINE

  Scenario: Nome muito curto
    When o usuário preenche "Nome Completo:" com "Jo"
    Then o sistema exibe abaixo do campo: "Mínimo de 3 caracteres"
    And o botão "Enviar" fica desabilitado
    # ← MESSAGE-DICTIONARY: BASELINE

  Scenario: Texto além do tamanho do campo
    When o usuário digita em "Cargo" até o centésimo caractere
    Then o campo não aceita mais caracteres
    And o contador abaixo do campo mostra "100/100"

  Scenario: E-mail fora do formato
    When o usuário preenche "E-mail" com "marina.acme" e aciona "Enviar"
    Then o sistema aceita o cadastro
    # ⚠️ o formato do e-mail não é conferido 💻

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Pessoa que já existe no cadastro
    Given que "Marina Duarte" já está no cadastro de pessoas
    When o usuário cadastra "Marina Duarte" pela recepção
    Then o sistema cria uma segunda pessoa com o mesmo nome, sem aviso
    And é essa nova pessoa que entra como participante do evento
    # ⚠️ o sistema não procura pessoa já cadastrada; ver a regra 2 💻

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Cadastrar Participante" na matriz do N2
    When o usuário abre os participantes do evento
    Then o botão "Cadastrar Pessoa" não é exibido
    # ⚠️ interface e servidor não coincidem neste ponto; ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Cadastro feito a partir do mapa de assentos
    Given que o usuário está na visão "Mapa de Assentos"
    When cadastra uma pessoa com "Check-in Automático" marcado
    Then, cerca de 1 segundo depois, a pessoa aparece entre as pessoas disponíveis do mapa
    # 💻 sem o check-in automático a pessoa não aparece no mapa, por não estar confirmada nem ter check-in; ver a regra 10

  Scenario: Falha ao cadastrar
    Given que o cadastro falha no servidor
    When o usuário aciona "Enviar"
    Then o sistema exibe: "Erro" com o detalhe "Erro ao cadastrar pessoa na recepção"
    And a janela continua aberta, com os dados digitados
    # ⚠️ o motivo devolvido pelo servidor não é mostrado 💻
    # ⚠️ o botão "Enviar" fica em carregamento até a janela ser fechada e aberta de novo 🔍
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| Nome do evento (título da janela, sem rótulo) | Evento | exibido do cadastro | somente leitura | texto | — | — |
| Local e data do evento (subtítulo da janela, sem rótulo) | Evento | exibido do cadastro | somente leitura | texto | — | O local, um hífen e a data por extenso com a hora — por exemplo, "Connect Towers - 20 de outubro de 2025 às 07:32" |
| "Nome Completo:" | Pessoa | entrada do usuário | editável | texto | sim | De 3 a 255 caracteres |
| "Instituição/Empresa" | Pessoa | entrada do usuário | editável | texto | sim | Até 255 caracteres. Fica guardada como a Razão Social da pessoa 💻 |
| "Cargo" | Pessoa | entrada do usuário | editável | texto | sim | Até 100 caracteres |
| "E-mail" | Pessoa | entrada do usuário | editável | texto | sim | Até 255 caracteres. ⚠️ O formato não é conferido 💻 |
| "Check-in Automático" | EventoPessoa | entrada do usuário | editável | sim·não | não | Vem marcado 💻. Dica: "Ao marcar esta opção, a pessoa cadastrada terá seu check-in realizado automaticamente". ⚠️ GPE005 o dá como obrigatório 📄; por ser uma caixa de marcar, sempre tem valor |

*Os tamanhos coincidem com os de GPE005: 255, 255, 100 e 255. O tamanho mínimo do nome, de 3 caracteres, só está no código 💻.*

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| Origem do cadastro | Recepção 💻 | Ao criar a pessoa |
| Sexo | Não informado 💻 | Ao criar a pessoa |
| Data de Criação | Data e hora do cadastro 💻 | Ao criar a pessoa |
| Convidado | Não 💻 | Ao incluir o participante |
| Confirmado | Não 💻 | Ao incluir o participante |
| Check-In | Sim, com "Check-in Automático" marcado; não, com ele desmarcado | Ao incluir o participante |
| Data e hora do check-in | ⚠️ Fica vazia, mesmo com o check-in automático 💻 | Ao incluir o participante |
| Atendido | ⚠️ Fica sem valor — nem sim, nem não 🔍 | Ao incluir o participante |

---

## Comportamento de tela

### Onde fica
No cabeçalho da tela de participantes do evento, o botão "Cadastrar Pessoa", disponível tanto na lista quanto no mapa de assentos. Ele abre uma janela sobre a tela, que pode ser arrastada, com o nome do evento no título e, abaixo, o local e a data por extenso. ⚠️ GPE005 chama a opção de "Cadastrar Participante", e é esse o texto do botão na imagem "Pesquisar Participantes" do documento 📄; na imagem "Incluir Participante" do mesmo documento, e na tela, o botão é "Cadastrar Pessoa" 💻.

Os campos obrigatórios trazem um asterisco vermelho, e cada campo de texto tem, abaixo, um contador de caracteres digitados sobre o limite — "0/255", por exemplo. O botão "Enviar" fica desabilitado enquanto houver campo obrigatório vazio ou inválido. Fechar a janela descarta o que foi digitado.

Depois do cadastro, a janela se fecha. Se o usuário não é da Secretaria Check-In, a tela consulta de novo, cerca de 1 segundo depois, os participantes usados pelo mapa de assentos. ⚠️ A lista de participantes não é recarregada: a pessoa recém-cadastrada só aparece nela depois de nova pesquisa 💻.

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | O botão "Enviar" mostra o indicador de carregamento enquanto o cadastro é enviado |
| Erro de validação | Texto em vermelho abaixo do campo — "Este campo é obrigatório" ou "Mínimo de 3 caracteres" — depois que o usuário passa pelo campo; o botão "Enviar" permanece desabilitado |
| Erro de servidor | "Erro" com o detalhe "Erro ao cadastrar pessoa na recepção", que fica na tela até ser fechado; a janela continua aberta. ⚠️ A mensagem é emitida com um tipo que a tela não reconhece, e pode aparecer sem a aparência de erro 🔍 |
| Sucesso | "Sucesso" com o detalhe "Cadastro de pessoa na recepção realizado com sucesso", que fica na tela até ser fechado; a janela se fecha e o formulário é limpo |
| Empty state | Não se aplica — a janela abre sempre com os campos vazios e "Check-in Automático" marcado |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Depois do cadastro, a pessoa é encontrada tanto na pesquisa de participantes do evento quanto na pesquisa de pessoas | Regra 1 · cenário "Cadastrar participante com check-in automático" |
| SC-02 | Com "Check-in Automático" marcado, o participante aparece com o check-in feito sem nenhuma outra ação | Regra 7 |
| SC-03 | Nenhum cadastro é enviado pela tela com nome completo, instituição ou empresa, cargo ou e-mail em branco | Regra 4 · cenário "Campo obrigatório vazio" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Cadastrar Participante | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade EventoPessoa

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Janela de cadastro: campos, validações e mensagens | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/components/pessoa-cadastro/pessoas-cadastro.component.ts` (linhas 61–141) e `.html` (linhas 1–150) | — |
| Botão "Cadastrar Pessoa" e o que acontece ao salvar | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/evento-pessoa.component.ts` (linhas 146–161) e `.html` (linhas 62–72 e 132–139) | — |
| Chamada ao servidor | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento/services/evento.service.ts` (linhas 78–81) | — |
| Operação `POST /administracao/eventos/{eventoId}/cadastro-rapido` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoController.java` (linhas 205–215) | — |
| Criação da pessoa e do participante | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/EventoPessoaServiceImpl.java` (linhas 438–462) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

Em caso de falha, o servidor responde com o texto `Erro ao criar pessoa na recepção: ` seguido do motivo; a tela não o usa. Quando o evento informado não existe, o servidor não faz nada e responde como sucesso.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE005 – Gerenciar Participante (funcionalidade "Incluir Participante") e do código |

---

*Feature Set: Participantes · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
