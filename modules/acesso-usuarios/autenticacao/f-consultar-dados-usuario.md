<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: ACE-AUT-06
feature_set: ACE-AUT
dominio: ACE
entidade: Usuario
data_model_ref: data-models/acesso-usuarios.md#usuario
endpoints: []
error_codes: []
depende_de: ["ACE-AUT-01"]
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

# Consultar Dados do Usuário
> **Nível 3** - Feature Set: Autenticação — Major Feature Set: Acesso e Usuários - `ACE-AUT-06`

## Descrição

Permite que o usuário consulte os dados da conta com que está autenticado — nome, login, perfil e e-mail —, confirmando com qual conta e com qual perfil está operando o sistema.

Os dados aparecem no menu que se abre ao clicar na foto ou no nome do usuário, no cabeçalho de qualquer tela interna. Não há nada a informar; o mesmo menu traz as opções Alterar Foto do Perfil, Alterar Senha e Logout.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE001 – Efetuar Login v1.0, de 03/10/2025 (documento legado), funcionalidade "Consultar dados do Usuário" ⚠️ sem chave na ferramenta de demandas | Criação | — Consultar os dados do usuário pelo menu suspenso que se abre ao clicar no link do usuário. O texto do documento não diz quais dados 📄; nome, login, perfil e e-mail estão na imagem do documento e no código |

---

<div class="dev-only">

## Superfície

**Modal** — origem: cabeçalho de todas as telas internas; o menu suspenso do usuário se abre sobre a tela ao clicar na foto ou no nome

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Consultar dados do Usuário" de GPE001

---

</div>

## Regras de negócio

1. Os dados exibidos são sempre os do próprio usuário autenticado; por aqui não se consultam os dados de outro usuário.
2. Os dados são os que o cadastro corporativo da CNI devolveu no momento da autenticação; não são consultados de novo a cada abertura do menu. 💻
3. Por isso, uma alteração feita no cadastro do usuário enquanto ele está com a sessão aberta — de nome, de e-mail ou de perfil — só aparece para ele depois que sai e entra de novo. 🔍
4. A foto é o único dado buscado à parte: vem do cadastro corporativo cada vez que o cabeçalho é carregado — ao entrar no sistema e ao recarregar a página. 💻
5. A consulta traz só nome, login, perfil e e-mail; os demais dados do usuário, como CPF, telefone, cargo e instituições, ficam na manutenção de usuários. 💻

---

## Cenários

```gherkin
Feature: Consultar dados do usuário

  Background:
    Given que o usuário está autenticado no GPE
    And está em uma tela interna do sistema

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Consultar os próprios dados
    When o usuário clica na sua foto ou no seu nome, no cabeçalho
    Then o sistema abre o menu do usuário com "Nome:", "Login:", "Perfil:" e "Email:", cada um seguido do dado da conta autenticada
    And, abaixo dos dados, as opções "Alterar Foto do Perfil", "Alterar Senha" e "Logout"

  Scenario: Fechar o menu do usuário
    Given que o menu do usuário está aberto
    When o usuário clica de novo na foto ou no nome, ou em qualquer outro ponto da tela
    Then o sistema fecha o menu

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há dado a validar
    When o usuário abre o menu do usuário
    Then o sistema mostra os dados sem solicitar nenhuma informação

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Dado alterado no cadastro com a sessão aberta
    Given que o nome, o e-mail ou o perfil do usuário foi alterado no cadastro depois que ele entrou
    When o usuário abre o menu do usuário
    Then o menu mostra os dados de quando ele entrou
    And os dados novos só aparecem depois que ele sai e entra de novo
    # 🔍 inferido: os dados vêm do que a autenticação devolveu, e nada os atualiza durante a sessão 💻

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Não há restrição por perfil para consultar os próprios dados
    Given que o usuário está autenticado, com qualquer perfil
    When abre uma tela interna
    Then o cabeçalho traz o nome e a foto dele, e o menu do usuário está disponível

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Falha ao buscar a foto
    Given que o cadastro corporativo não devolve a foto do usuário
    When o sistema carrega o cabeçalho
    Then o cabeçalho mostra o nome sem a foto, e o menu abre normalmente com os demais dados
    And o sistema emite uma mensagem de erro com o detalhe enviado pelo cadastro corporativo ou, na falta dele, "Serviço indisponível"
    # 🔍 a mensagem só é vista nas telas que têm área de mensagens ligada ao cabeçalho; a confirmar em execução

  Scenario: Usuário sem foto no cadastro
    Given que o usuário não tem foto de perfil no cadastro corporativo
    When o sistema carrega o cabeçalho
    Then o espaço da foto fica vazio, sem imagem padrão
    # 🔍 inferido do código: não há imagem substituta
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| — | Usuario | — | — | — | — | A consulta não tem campos de entrada: os dados exibidos estão em Colunas do resultado |

---

## Colunas do resultado

| Coluna (Label PO) | Origem | Ordenação |
|---|---|---|
| Foto (sem rótulo) | cadastro — Foto do Usuario, buscada no cadastro corporativo ao carregar o cabeçalho 💻 | — |
| Nome | cadastro — Nome do Usuario, recebido na autenticação | — |
| Login | cadastro — Login do Usuario, recebido na autenticação | — |
| Perfil | entidade relacionada — Nome do PerfilAcesso do usuário, recebido na autenticação | — |
| Email | cadastro — Email do Usuario, recebido na autenticação | — |

*A consulta mostra um registro só, o do usuário autenticado; não há ordenação nem paginação.*

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| — | — | Nenhum campo é gravado: a feature só exibe |

---

## Dados lidos e gravados

| Entidade | Papel | Por que a feature a toca |
|---|---|---|
| PerfilAcesso | lê | O nome do perfil do usuário é um dos dados exibidos (regra 5) |

---

## Comportamento de tela

### Onde fica
No cabeçalho azul de todas as telas internas, à direita do nome do sistema, ficam o nome do usuário e a sua foto, em um círculo. O clique em qualquer dos dois abre, logo abaixo, o menu do usuário; um novo clique, ou o clique em outro ponto da tela, o fecha. GPE001 chama esse conjunto de "link do usuário". 📄

O menu traz primeiro os dados, cada um em uma linha, com o rótulo em negrito: "Nome:", "Login:", "Perfil:" e "Email:". As linhas de dados não são clicáveis. Em seguida vêm as opções "Alterar Foto do Perfil", "Alterar Senha" e "Logout", cada uma com o seu ícone — são as features Alterar Foto de Perfil `ACE-AUT-05`, Alterar Senha `ACE-AUT-04` e Encerrar Sessão `ACE-AUT-02`.

As telas de acesso, de recuperação de senha e de alteração de senha não têm cabeçalho, e portanto não têm o menu do usuário. 💻

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Sem indicador: os dados já estão na sessão e aparecem de imediato; a foto surge quando a busca termina |
| Erro de validação | Não se aplica — não há campos de entrada |
| Erro de servidor | Só na busca da foto: mensagem de erro com o detalhe enviado pelo cadastro corporativo ou, na falta dele, "Serviço indisponível"; os demais dados não dependem do servidor 💻 |
| Sucesso | O menu abre com Nome, Login, Perfil e Email da conta autenticada e, abaixo, as opções "Alterar Foto do Perfil", "Alterar Senha" e "Logout" |
| Empty state | Dado que o cadastro não tem aparece só com o rótulo, sem valor; usuário sem foto fica com o espaço da foto vazio 🔍 |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Em qualquer tela interna, o usuário vê com um clique o nome, o login, o perfil e o e-mail da conta com que entrou | Cenário "Consultar os próprios dados" |
| SC-02 | Os dados exibidos são sempre os do usuário autenticado, nunca os de outro | Regra 1 |
| SC-03 | O nome do usuário autenticado está visível no cabeçalho de toda tela interna, sem abrir o menu | Cenário "Não há restrição por perfil para consultar os próprios dados" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Consultar Dados do Usuário | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade Usuario

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Menu do usuário: foto, nome, dados e opções | sistema_mesa_checkin_frontend | `src/app/shared/layout/topbar/topbar.component.html` (linhas 14–68) | — |
| Busca e exibição da foto ao carregar o cabeçalho | sistema_mesa_checkin_frontend | `src/app/shared/layout/topbar/topbar.component.ts` (linhas 38–40, 66–81 e 96–107) | — |
| Dados do usuário guardados na autenticação e chamada da foto | sistema_mesa_checkin_frontend | `src/app/service/core/auth.service.ts` (linhas 33–39, 90–94 e 104–117) | — |
| Abertura e fechamento do menu | sistema_mesa_checkin_frontend | `src/app/admin/admin.component.ts` (linhas 52–72 e 108–116) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

Nenhuma operação do servidor do GPE é chamada. Nome, login, perfil e e-mail são lidos do objeto `usuario` que a autenticação devolveu e que fica no `localStorage`; só a foto é buscada, no serviço corporativo, no endereço de `urlPesquisaUsuarios` seguido do identificador do usuário e de `/foto`. A mensagem de erro da foto sai por `AlertaService`, pelo `MessageService` da aplicação; o cabeçalho não tem `<p-toast>` próprio.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE001 – Efetuar Login (funcionalidade "Consultar dados do Usuário") e do código |

---

*Feature Set: Autenticação · Major Feature Set: Acesso e Usuários · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
