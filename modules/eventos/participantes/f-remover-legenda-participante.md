<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: EVT-PAR-06
feature_set: EVT-PAR
dominio: EVT
entidade: EventoPessoaLegenda
data_model_ref: data-models/eventos.md#eventopessoalegenda
endpoints: []
error_codes: []
depende_de: ["EVT-PAR-04"]
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

# Remover Legenda do Participante
> **Nível 3** - Feature Set: Participantes — Major Feature Set: Eventos - `EVT-PAR-06`

## Descrição

Permite que o Administrador remova a legenda atribuída manualmente a um participante do evento; ele volta a ser identificado pela legenda que recebeu por regra ou, se não tiver nenhuma, fica sem legenda.

Na janela Gerenciar Legenda da Pessoa, aciona-se Remover Legenda e confirma-se a pergunta. O mesmo resultado se obtém escolhendo a opção Remover legenda, ao fim da lista de legendas, e acionando Salvar.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE005 – Gerenciar Participante v1.1, de 16/12/2025 (documento legado), funcionalidade "Remover Legenda do Participante" ⚠️ sem chave na ferramenta de demandas | Criação | — Remover a legenda de um participante a partir da consulta de legenda. O documento não distingue a legenda manual da recebida por regra 📄; o código remove só a manual 💻 ⚠️ |

---

<div class="dev-only">

## Superfície

**Ação em tela** — origem: Consultar Legenda do Participante `EVT-PAR-04` (janela "Gerenciar Legenda da Pessoa", sobre `/evento-pessoa/:id`), botão "Remover Legenda"

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Consultar Legenda do Participante" de GPE005 (`GPE005-04.png`)

---

</div>

## Regras de negócio

1. A remoção retira somente a legenda manual do participante. 💻 ⚠️ GPE005 fala em "remover a legenda de um determinado participante", sem distinguir a manual da recebida por regra 📄.
2. As legendas que o participante recebeu por regra permanecem; removida a manual, ele volta a ser identificado pela de menor número na configuração do evento. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 9
3. A legenda recebida por regra não pode ser removida de um participante isolado: ela só sai com a mudança da configuração do evento e nova geração das legendas. 💻 ⚠️ Confirmar com o PO se a remoção individual deveria alcançá-la.
4. A legenda manual que nasceu de uma legenda recebida por regra é apagada por inteiro na remoção; a legenda de regra só volta na próxima geração das legendas do evento. 💻 🔍 Decorre de a atribuição por regra ter virado manual, sem cópia — ver Alterar Legenda do Participante (`EVT-PAR-05`), regra 6.
5. A remoção é definitiva: a atribuição é apagada, e não apenas ocultada. 💻
6. A remoção vale só para o evento aberto. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 8
7. Quem removeu a legenda não fica guardado. 💻 ⚠️ O sistema não registra o autor de nenhuma ação.

---

## Cenários

```gherkin
Feature: Remover legenda do participante

  Background:
    Given que o usuário está autenticado no GPE
    And abriu a janela "Gerenciar Legenda da Pessoa" de um participante

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Remover a legenda manual
    Given que a participante "Ana Reis" tem a legenda manual "Anfitrião" e nenhuma legenda recebida por regra
    When o usuário aciona "Remover Legenda"
    And confirma a pergunta "Tem certeza que deseja remover a legenda desta pessoa?"
    Then o sistema remove a legenda manual de "Ana Reis"
    And exibe: "Sucesso" com o detalhe "Legenda removida com sucesso!"
    And fecha a janela e recarrega a página atual da lista de participantes
    And a linha de "Ana Reis" fica sem legenda e com a faixa de cor cinza-clara

  Scenario: Voltar à legenda recebida por regra
    Given que o participante "Paulo Henrique" tem a legenda manual "Anfitrião" e, por regra, a legenda "Empresas – presidentes"
    When o usuário aciona "Remover Legenda" e confirma a pergunta
    Then o sistema remove "Anfitrião"
    And a linha de "Paulo Henrique" passa a mostrar "Empresas – presidentes"

  Scenario: Remover pela opção da lista de legendas
    Given que o participante tem legenda manual
    When o usuário seleciona "Remover legenda" ao fim da lista "Selecione uma Legenda:"
    And aciona "Salvar"
    Then o sistema faz a mesma pergunta de confirmação e, confirmada, remove a legenda manual

  Scenario: Desistir da remoção
    When o usuário aciona "Remover Legenda"
    And não confirma a pergunta
    Then a legenda do participante continua a mesma e a janela permanece aberta

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há dado a validar
    When o usuário aciona "Remover Legenda"
    Then o sistema pede apenas a confirmação, sem solicitar nenhum dado

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Participante sem legenda manual
    Given que o participante não tem legenda manual
    When o usuário abre a janela de legenda
    Then o botão "Remover Legenda" não é oferecido
    # ⚠️ vale também para quem só tem legenda recebida por regra; ver a regra 3 💻

  Scenario: Salvar com "Remover legenda" sem legenda manual
    Given que o participante não tem legenda manual
    And a opção "Remover legenda" está selecionada
    When o usuário aciona "Salvar"
    Then o sistema exibe o aviso "Atenção" com o detalhe "Esta pessoa já não possui legenda."
    And nada é alterado

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Remover Legenda do Participante" na matriz do N2
    When o usuário vê a lista de participantes
    Then o valor da coluna "Assento" é texto simples e a janela de legenda não fica ao alcance dele
    # ⚠️ a tela só retira o atalho da Secretaria Check-In; ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Remover legenda manual que veio de uma legenda de regra
    Given que o participante recebeu "Empresas – diretores" por regra
    And essa mesma legenda foi depois tornada manual
    When o usuário aciona "Remover Legenda" e confirma a pergunta
    Then o participante fica sem a legenda "Empresas – diretores", inclusive como legenda de regra
    # 🔍 a legenda só volta na próxima geração das legendas do evento; ver a regra 4

  Scenario: Falha ao remover
    Given que a remoção falha no servidor
    When o usuário confirma a pergunta
    Then o sistema exibe: "Erro" com o detalhe "Erro ao remover legenda da pessoa."
    And a janela continua aberta e a legenda do participante continua a mesma
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| — | EventoPessoaLegenda | — | — | — | — | A ação não tem campos: opera sobre a legenda manual do participante consultado e pede só a confirmação |

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| — | — | Nenhum campo é gravado: a atribuição manual é apagada |

---

## Dados lidos e gravados

| Entidade | Papel | Por que a feature a toca |
|---|---|---|
| EventoPessoa | lê | Confere que o participante existe antes de remover a legenda |
| EventoLegenda | lê | Ordem dos blocos na configuração do evento: decide a legenda que volta a identificar o participante (regra 2) |
| Legenda | lê | Nome e cor da legenda que volta a identificar o participante na lista (regra 2) |

---

## Comportamento de tela

### Onde fica
Na janela "Gerenciar Legenda da Pessoa", aberta pela coluna "Assento" da lista de participantes (Consultar Legenda do Participante, `EVT-PAR-04`). O botão "Remover Legenda", com o ícone de lixeira, fica à esquerda no rodapé da janela e só aparece quando o participante tem legenda manual. Há um segundo caminho: a opção "Remover legenda", última da lista "Selecione uma Legenda:", seguida de "Salvar".

Os dois caminhos levam à mesma caixa de pergunta, com o texto "Tem certeza que deseja remover a legenda desta pessoa?". A ação pede o título "Confirmar Remoção"; os botões são os da caixa de confirmação da tela, "Remover" e "Cancelar" 🔍 — a caixa é a mesma usada por Alterar Confirmação de Presença (`EVT-PAR-13`), e foi montada com o título "Remover Pessoa". Qual título aparece de fato não foi conferido em execução ❓.

Depois da remoção, a janela se fecha e a lista de participantes é recarregada na mesma página.

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Os botões da janela ficam desabilitados até a resposta do servidor |
| Erro de validação | Não se aplica — não há campos |
| Erro de servidor | "Erro" com o detalhe "Erro ao remover legenda da pessoa."; a janela continua aberta |
| Sucesso | "Sucesso" com o detalhe "Legenda removida com sucesso!"; a janela se fecha e a lista é recarregada |
| Empty state | Sem legenda manual, o botão "Remover Legenda" não aparece; pelo caminho da lista, o aviso "Atenção" com o detalhe "Esta pessoa já não possui legenda." |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Depois da remoção, o participante deixa de ter legenda manual e passa a ser identificado pela legenda de regra de menor número, ou por nenhuma | Regras 1 e 2 · cenário "Voltar à legenda recebida por regra" |
| SC-02 | Nenhuma remoção acontece sem a confirmação do usuário | Cenário "Desistir da remoção" |
| SC-03 | A remoção em um evento não muda a legenda da mesma pessoa em outro evento | Regra 6 |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Remover Legenda do Participante | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade EventoPessoaLegenda

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Botão "Remover Legenda", opção "Remover legenda", confirmação e mensagens | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/components/evento-pessoas-list/evento-pessoas-list.component.ts` (linhas 375–392 e 413–443) e `.html` (linhas 2–7, 251–261 e 269–277) | — |
| Chamada ao servidor, sem legenda informada | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento/services/evento-legenda.service.ts` (linhas 59–61) | — |
| Operação `PUT /administracao/eventos/participante/legenda` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoController.java` (linhas 297–302) | — |
| Remoção das atribuições manuais do participante | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/LegendaEventoServiceImpl.java` (linhas 459–478) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

A remoção usa a mesma operação da alteração, com a legenda vazia. A tela tem ainda o aviso "Atenção" com o detalhe "Esta pessoa não possui legenda para remover."; nenhuma ação da tela chega a ele, porque o botão e o caminho da lista só ficam disponíveis quando há legenda manual.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE005 – Gerenciar Participante (funcionalidade "Remover Legenda do Participante") e do código |

---

*Feature Set: Participantes · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
