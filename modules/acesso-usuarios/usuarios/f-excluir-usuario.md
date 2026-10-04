<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: ACE-USU-04
feature_set: ACE-USU
dominio: ACE
entidade: Usuario
data_model_ref: data-models/acesso-usuarios.md#usuario
endpoints: []
error_codes: []
depende_de: ["ACE-USU-01"]
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

# Excluir Usuário
> **Nível 3** - Feature Set: Usuários — Major Feature Set: Acesso e Usuários - `ACE-USU-04`

## Descrição

Permite que o Administrador exclua um usuário do sistema, mediante confirmação; o usuário deixa de ser exibido na lista de usuários.

A exclusão é acionada pela opção Remover Usuário, em cada linha da lista de usuários. O sistema pede confirmação e, confirmada, solicita a exclusão ao cadastro corporativo e retira a linha da lista.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE002 – Manter Usuário v1.0, de 03/10/2025 (documento legado), funcionalidade "Excluir Usuário" ⚠️ sem chave na ferramenta de demandas | Criação | — Excluir um usuário a partir da pesquisa, deixando de exibi-lo no sistema. Se a exclusão é definitiva ou lógica, e se alcança só o acesso a este sistema ou o usuário inteiro no cadastro corporativo, o documento não diz e o código do GPE não mostra ❓. Pelo título, relaciona-se aos tickets do Jira `PDTIC25148-1` (Cadastro de Usuário) e `PDTIC25148-23` (Cadastro de usuários - Ajustes), ambos concluídos 🔍; o conteúdo deles não foi consultado e a AIM não foi aberta |

---

<div class="dev-only">

## Superfície

**Ação em tela** — origem: Pesquisar Usuários `ACE-USU-01` (`/administracao-usuarios`), ícone de lixeira em cada linha da lista

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Pesquisar Usuário" de GPE002

---

</div>

## Regras de negócio

1. Nenhuma exclusão acontece sem a confirmação de quem a pediu. 💻
2. O usuário excluído deixa de ser exibido no sistema. 📄 ❓ GPE002 diz que o usuário "passa a não ser exibido no sistema"; a exclusão é executada pelo cadastro corporativo, e se lá ela é definitiva ou lógica o código do GPE não mostra.
3. A exclusão retira o usuário deste sistema, e não a conta dele no cadastro corporativo da CNI. 🔍 É o que o nome da operação chamada indica — ela trata do usuário no sistema —, não o que o código do GPE comprova.
4. O GPE não impõe condição para excluir: não guarda dado próprio ligado ao usuário que pudesse impedir a exclusão, não impede que o usuário exclua a si mesmo nem que o último Administrador seja excluído. 💻 ❓ Se o cadastro corporativo recusa algum desses casos, o código do GPE não mostra.
5. O usuário pertence ao cadastro corporativo da CNI, que é quem executa a exclusão. → ver [N1 Acesso e Usuários](../README.md): Regras transversais de negócio: 1

---

## Cenários

```gherkin
Feature: Excluir usuário

  Background:
    Given que o usuário está autenticado no GPE
    And está na lista de usuários

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Excluir um usuário
    When o usuário aciona "Remover Usuário" na linha de "Maria Souza"
    And confirma a pergunta "Deseja remover este usuário?" pelo botão "Remover"
    Then o sistema solicita a exclusão ao cadastro corporativo
    And retira "Maria Souza" da lista
    # ⚠️ 🔍 a mensagem de sucesso prevista é "Usuário removido com Sucesso"; a tela "Usuários" não tem onde exibi-la

  Scenario: Desistir da exclusão
    When o usuário aciona "Remover Usuário" na linha de um usuário
    And responde à pergunta pelo botão "Cancelar"
    Then o sistema mantém o usuário e a lista como estavam

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há dado a validar
    When o usuário aciona "Remover Usuário"
    Then o sistema pede apenas a confirmação, sem solicitar nenhum dado

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Exclusão recusada pelo cadastro corporativo
    Given que o cadastro corporativo recusa a exclusão do usuário
    When o usuário confirma a exclusão
    Then o sistema mantém o usuário na lista
    # ❓ o GPE não confere nada antes de pedir a exclusão; que casos o cadastro corporativo recusa, o código do GPE não mostra
    # ⚠️ 🔍 a mensagem prevista é "Erro Interno" com o detalhe devolvido pelo cadastro corporativo; a tela "Usuários" não tem onde exibi-la

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Excluir Usuário" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Administração › Usuários, e a ação não fica ao alcance dele
    # ⚠️ a tela não confere o perfil; ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Excluir o próprio usuário
    Given que a lista traz a linha do próprio usuário autenticado
    When ele aciona "Remover Usuário" nessa linha e confirma
    Then o sistema trata o pedido como qualquer outra exclusão e o envia ao cadastro corporativo
    # ⚠️ 💻 a tela não tem trava para esse caso; ❓ o que o cadastro corporativo responde, o código do GPE não mostra

  Scenario: Falha ao excluir
    Given que o pedido de exclusão falha por indisponibilidade do cadastro corporativo
    When o usuário confirma a exclusão
    Then o sistema mantém o usuário na lista
    # ⚠️ 🔍 a mensagem prevista é um texto genérico conforme a falha, como "Serviço indisponível."; a tela "Usuários" não tem onde exibi-la, e a falha tende a passar sem aviso
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| — | Usuario | — | — | — | — | A ação não tem campos: opera sobre o usuário da linha escolhida e pede só a confirmação |

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| — | — | Nenhum campo é gravado pelo GPE: a exclusão é executada no cadastro corporativo ❓ |

---

## Comportamento de tela

### Onde fica
Na tela Usuários, em cada linha da lista, o ícone de lixeira com a dica "Remover Usuário", ao lado do ícone de edição. A confirmação é uma caixa própria da tela, com o título "Remover Usuário", a pergunta "Deseja remover este usuário?" e os botões "Remover" e "Cancelar" 💻. ⚠️ GPE002 chama a opção de "Excluir" 📄; na tela ela se chama "Remover Usuário" 💻.

Confirmada a exclusão e aceita pelo cadastro corporativo, a linha é retirada da lista que está na tela, sem nova consulta 💻.

⚠️ A tela Usuários não tem quadro de mensagens: nem a mensagem de sucesso nem as de erro desta ação têm onde aparecer 🔍. No sucesso, o único sinal é a linha sair da lista; na falha, nada muda na tela. A conclusão vem da leitura do código, sem execução.

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Sem indicador de carregamento 💻 |
| Erro de validação | Não se aplica — não há campos |
| Erro de servidor | Previsto: erro "Erro Interno" com o detalhe devolvido pelo cadastro corporativo ou, na falta dele, um texto genérico conforme a falha, como "Serviço indisponível.". ⚠️ 🔍 A tela não tem onde exibir a mensagem; a linha continua na lista |
| Sucesso | A linha sai da lista. Previsto: "Usuário removido com Sucesso" ⚠️ 🔍 — a tela não tem onde exibi-lo |
| Empty state | Não se aplica — a ação só existe em linha da lista |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Um usuário excluído não é mais encontrado pela pesquisa de usuários | Regra 2 · cenário "Excluir um usuário" |
| SC-02 | Nenhuma exclusão acontece sem a confirmação do usuário | Regra 1 · cenário "Desistir da exclusão" |
| SC-03 | Quando o cadastro corporativo recusa ou não responde, o usuário continua na lista | Cenários "Exclusão recusada pelo cadastro corporativo" e "Falha ao excluir" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Excluir Usuário | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade Usuario

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Ícone "Remover Usuário" e caixa de confirmação | sistema_mesa_checkin_frontend | `src/app/admin/administracao/acessibilidade/usuarios/pages/usuarios/components/usuarios-list/usuarios-list.component.html` (linhas 1–6 e 55–60) | — |
| Confirmação, pedido de exclusão e retirada da linha | sistema_mesa_checkin_frontend | `src/app/admin/administracao/acessibilidade/usuarios/pages/usuarios/components/usuarios-list/usuarios-list.component.ts` (linhas 131–156) | — |
| Exclusão no serviço corporativo (`DELETE urlAtualizaUsuarioSistema`) | sistema_mesa_checkin_frontend | `src/app/shared/http-crud.service.ts` (linhas 52–55) | — |
| Tratamento do erro devolvido | sistema_mesa_checkin_frontend | `src/app/shared/page-base.ts` (linhas 14–64) | — |
| Endereços dos serviços corporativos (`GET /servicos/corporativo`) — única participação do servidor do GPE | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/corporativo/controller/RecursosController.java` (linhas 24–28) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

O servidor do GPE não implementa usuários: a tela chama direto o serviço corporativo, pelo mesmo endereço da alteração (`urlAtualizaUsuarioSistema`, com o código do usuário), trocando o verbo. A lista não contém `<p-toast>`, e as mensagens saem pelo `AlertaService`, ligado ao `MessageService` da raiz. A lista tem ainda os métodos `mudarSituacao` e `copiar`, sem acionador na tela.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE002 – Manter Usuário (funcionalidade "Excluir Usuário") e do código |

---

*Feature Set: Usuários · Major Feature Set: Acesso e Usuários · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
