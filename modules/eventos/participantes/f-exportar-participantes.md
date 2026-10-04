<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: EVT-PAR-14
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

# Exportar Participantes
> **Nível 3** - Feature Set: Participantes — Major Feature Set: Eventos - `EVT-PAR-14`

## Descrição

Permite que a equipe do evento exporte para uma planilha os participantes que atendem à pesquisa em vigor, com os dados da pessoa, seus grupos de trabalho, temas e participações anteriores, a legenda e a situação de confirmação, check-in e atendimento.

A exportação é acionada pelo botão Download, no rodapé da lista de participantes. O sistema baixa o arquivo Participantes.xls com os participantes que a última pesquisa encontrou, de todas as páginas.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE005 – Gerenciar Participante v1.1, de 16/12/2025 (documento legado), funcionalidade "Exportar Participantes" ⚠️ sem chave na ferramenta de demandas | Criação | — Exportar a pesquisa de participantes de um evento, com as 14 colunas da tabela "Exportação da Pesquisa de Participantes" do documento. A funcionalidade entrou na v1.1, que cita os tickets `PDTIC25148-32`, `PDTIC25148-20` e `PDTIC25148-28` sem dizer qual deles a originou ❓ |

---

<div class="dev-only">

## Superfície

**Ação em tela** — origem: Pesquisar Participantes `EVT-PAR-01` (`/evento-pessoa/:id`), botão "Download" no rodapé da lista

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem da planilha exportada em GPE005 (`GPE005-02.png`)

---

</div>

## Regras de negócio

1. A planilha traz os participantes do evento aberto que atendem aos critérios da última pesquisa feita.
2. São exportados todos os participantes que a pesquisa encontra, e não só os da página exibida, até o limite de 100.000. 💻
3. Cada participante ocupa uma linha da planilha, e as linhas vêm em ordem alfabética de nome. 💻
4. A planilha tem 14 colunas, sempre na mesma ordem, de "Cód. Contato" a "Atendido" — as mesmas, e na mesma ordem, da tabela de GPE005.
5. Os grupos de trabalho da pessoa saem todos na mesma célula, cada um seguido do papel entre parênteses e separados por ponto e vírgula; os temas, do mesmo modo, sem o papel. 💻
6. O número de participações é a soma das participações da pessoa em todos os anos do histórico; quem não tem histórico sai com zero. 💻
7. Em "Legendas" sai uma única legenda, a prioritária do participante, apesar do título no plural. 💻 → ver [N1 Eventos](../README.md): Regras transversais de negócio: 9
8. Confirmado, Checkin e Atendido saem como "Sim", "Não" ou "Pendente" — este último quando o participante não tem a informação. 💻
9. A razão social e o nome fantasia saem cada um na sua coluna, com o conteúdo do cadastro da pessoa. 💻 ⚠️ É o contrário do que acontece na coluna Organização da lista, em que os dois chegam trocados — ver Pesquisar Participantes (`EVT-PAR-01`).
10. A planilha não traz a situação de convite nem o assento do participante, embora a lista os mostre.

---

## Cenários

```gherkin
Feature: Exportar participantes

  Background:
    Given que o usuário está autenticado no GPE
    And está na lista de participantes de um evento

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Exportar todos os participantes do evento
    Given que o evento tem 35 participantes e nenhum critério de pesquisa foi informado
    When o usuário aciona "Download"
    Then o sistema exibe o aviso "Exportação em andamento." com o detalhe "A exportação dos participantes está em andamento, por favor aguarde."
    And baixa o arquivo "Participantes.xls"
    And a planilha tem a linha de títulos e 35 linhas, uma por participante, em ordem alfabética de nome

  Scenario: Exportar o resultado de uma pesquisa
    Given que o usuário pesquisou com "Sim" em "Confirmado" e a pesquisa encontrou 12 participantes
    When o usuário aciona "Download"
    Then a planilha traz somente esses 12 participantes

  Scenario: Conferir o conteúdo de uma linha
    Given que "Adriana Blikstein" participa do grupo de trabalho "Descarbonização" como "Membro", tem o tema "Empresa" e 11 participações no histórico
    When o usuário exporta os participantes
    Then a linha de "Adriana Blikstein" traz "Descarbonização (Membro)" em "Grupos de Trabalho", "Empresa" em "Temas" e "11" em "Nro. Participações"

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há dado a validar
    When o usuário aciona "Download"
    Then o sistema gera a planilha sem solicitar nenhum dado

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Não há conflito com dados existentes
    When o usuário exporta os participantes
    Then o sistema apenas lê os dados, sem alterar nada

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Exportar Participantes" na matriz do N2
    When o usuário entra no sistema
    Then a tela de participantes abre direto no mapa de assentos
    And a lista, com o botão "Download", não fica ao alcance dele
    # ⚠️ o botão aparece para todo perfil que vê a lista; ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Critério alterado e ainda não pesquisado
    Given que o usuário pesquisou com "Sim" em "Confirmado"
    And depois escolheu "Não" em "Confirmado", sem acionar "Pesquisar"
    When o usuário aciona "Download"
    Then a planilha traz os participantes da última pesquisa feita, com "Sim" em "Confirmado"

  Scenario: Pesquisa sem resultado
    Given que a última pesquisa não encontrou nenhum participante
    When o usuário aciona "Download"
    Then o sistema baixa a planilha só com a linha de títulos
    # 🔍 o botão continua na tela com a lista vazia; conclusão tirada da leitura do código, sem execução

  Scenario: Participante sem informação de atendimento
    Given que um participante foi cadastrado na recepção e nunca foi atendido
    When o usuário exporta os participantes
    Then a linha dele traz "Pendente" em "Atendido"
    # 🔍 o cadastro na recepção deixa o atendimento sem valor; ver Cadastrar Participante (EVT-PAR-02)

  Scenario: Falha na exportação
    Given que a geração da planilha falha no servidor
    When o usuário aciona "Download"
    Then o sistema exibe: "Erro" com o detalhe "Erro ao exportar participantes."
    And nenhum arquivo é baixado
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| "Cód. Contato" | Pessoa | exibido do cadastro | somente leitura | texto | — | Código da pessoa no CRM; vazio para quem foi cadastrado na recepção ou pela tela de pessoas sem o código |
| "Nome Completo" | Pessoa | exibido do cadastro | somente leitura | texto | — | — |
| "Codinome" | Pessoa | exibido do cadastro | somente leitura | texto | — | — |
| "Cargo" | Pessoa | exibido do cadastro | somente leitura | texto | — | — |
| "Cargo do Cartão" | Pessoa | exibido do cadastro | somente leitura | texto | — | — |
| "Razão Social" | Pessoa | exibido do cadastro | somente leitura | texto | — | — |
| "Nome Fantasia" | Pessoa | exibido do cadastro | somente leitura | texto | — | — |
| "Grupos de Trabalho" | GrupoTrabalhoPessoa | exibido do cadastro | somente leitura | texto | — | Todos os grupos da pessoa, no formato "Grupo (Papel)", separados por ponto e vírgula; sem o papel, sai só o nome do grupo 💻 |
| "Temas" | TemaPessoa | exibido do cadastro | somente leitura | texto | — | Todos os temas da pessoa, separados por ponto e vírgula 💻 |
| "Nro. Participações" | derivado ↓ | calculado | somente leitura | número | — | Zero quando a pessoa não tem histórico 💻 |
| "Legendas" | Legenda | exibido do cadastro | somente leitura | texto | — | Nome da legenda prioritária do participante; vazio quando ele não tem legenda 💻 |
| "Confirmado" | EventoPessoa | exibido do cadastro | somente leitura | texto | — | "Sim", "Não" ou "Pendente" |
| "Checkin" | EventoPessoa | exibido do cadastro | somente leitura | texto | — | "Sim", "Não" ou "Pendente" |
| "Atendido" | EventoPessoa | exibido do cadastro | somente leitura | texto | — | "Sim", "Não" ou "Pendente" |

*A tabela lista as colunas da planilha, na ordem em que saem. A feature não tem campos de entrada: os critérios são os da pesquisa de participantes (`EVT-PAR-01`). Grupos de trabalho, temas, número de participações e atendimento só aparecem aqui — a lista de participantes não os mostra.*

---

## Derivações

| Campo derivado | Fórmula (Label PO) | Campos-fonte (Entidade) |
|---|---|---|
| Nro. Participações | Soma de Participações em todos os anos do histórico da pessoa | Participações (HistoricoPessoa) |

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| — | — | Nenhum campo é gravado: a feature só gera a planilha |

---

## Dados lidos e gravados

| Entidade | Papel | Por que a feature a toca |
|---|---|---|
| EventoPessoaLegenda | lê | Legendas que o participante tem no evento, de onde sai a prioritária (regra 7) e sobre as quais age o critério Legendas da pesquisa |
| EventoLegenda | lê | Ordem dos blocos na configuração do evento, que decide a legenda prioritária quando não há legenda manual (regra 7) |
| CadeiraMesa | lê | A consulta que alimenta a planilha é a mesma da pesquisa e lê o assento do participante, embora a planilha não o traga (regra 10) |

---

## Comportamento de tela

### Onde fica
Na lista de participantes do evento, o botão "Download", com o ícone de arquivo, à direita no rodapé da lista. GPE005 chama a opção pelo mesmo nome 📄. O botão está disponível para todo perfil que vê a lista 💻.

O arquivo baixado chama-se "Participantes.xls", no formato de planilha do Excel 97–2003, com uma única aba, "Participantes", e a primeira linha com os títulos das colunas em destaque 💻. Não há escolha de formato nem de colunas.

A planilha segue os critérios da última pesquisa feita, e não os que estiverem na tela sem pesquisar. Enquanto o arquivo é gerado a tela continua livre, e o botão pode ser acionado de novo 🔍.

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Aviso "Exportação em andamento." com o detalhe "A exportação dos participantes está em andamento, por favor aguarde."; não há indicador de progresso |
| Erro de validação | Não se aplica — não há campos |
| Erro de servidor | "Erro" com o detalhe "Erro ao exportar participantes." |
| Sucesso | O navegador baixa "Participantes.xls"; não há mensagem de conclusão |
| Empty state | Com a pesquisa sem resultado, a planilha sai só com a linha de títulos 🔍 |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | A planilha tem uma linha para cada participante que a pesquisa em vigor encontra, inclusive os das páginas que não estão à vista | Regras 1 e 2 · cenário "Exportar todos os participantes do evento" |
| SC-02 | As 14 colunas saem sempre na mesma ordem, de "Cód. Contato" a "Atendido" | Regra 4 |
| SC-03 | O arquivo baixado abre em programa de planilha com o nome "Participantes.xls" | Cenário "Exportar todos os participantes do evento" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Exportar Participantes | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade EventoPessoa

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Botão "Download", aviso e gravação do arquivo no computador | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/components/evento-pessoas-list/evento-pessoas-list.component.ts` (linhas 454–476) e `.html` (linhas 168–181) | — |
| Chamada ao servidor | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento/services/evento.service.ts` (linhas 93–100) | — |
| Operação `GET /administracao/eventos/participantes/excel` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoController.java` (linhas 237–255) | — |
| Montagem da planilha e dos títulos das colunas | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/EventoPessoaServiceImpl.java` (linhas 477–639) | — |
| Consulta dos participantes, a mesma da pesquisa | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/repository/impl/EventoPessoaRepositoryImpl.java` (linhas 92–284) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

O limite de 100.000 participantes é pedido pela tela. A operação do servidor reaproveita a consulta paginada da pesquisa e, chamada sem esse tamanho, devolveria só os 10 primeiros. O arquivo vem dentro da resposta, em base64, com o nome e o tipo; a tela o grava com o nome recebido. O botão chama-se "Download", o método da tela, `exportCSV`, e a operação, `…/participantes/excel` — o formato real é `.xls`.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE005 – Gerenciar Participante (funcionalidade "Exportar Participantes" e tabela "Exportação da Pesquisa de Participantes") e do código |

---

*Feature Set: Participantes · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
