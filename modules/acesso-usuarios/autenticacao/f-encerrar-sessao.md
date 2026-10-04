<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: ACE-AUT-02
feature_set: ACE-AUT
dominio: ACE
entidade: Usuario
data_model_ref: data-models/acesso-usuarios.md#usuario
endpoints: []
error_codes: []
depende_de: ["ACE-AUT-01", "ACE-AUT-06"]
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

# Encerrar Sessão
> **Nível 3** - Feature Set: Autenticação — Major Feature Set: Acesso e Usuários - `ACE-AUT-02`

## Descrição

Permite que o usuário encerre a sua sessão no sistema; ele volta à tela de acesso e, para usar o sistema de novo naquele navegador, precisa autenticar-se outra vez.

A saída é acionada pela opção Logout, no menu que se abre ao clicar na foto ou no nome do usuário, no cabeçalho de qualquer tela interna. Não há dado a informar nem confirmação a dar.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE001 – Efetuar Login v1.0, de 03/10/2025 (documento legado), funcionalidade "Efetuar Logout" ⚠️ sem chave na ferramenta de demandas | Criação | — Encerrar a sessão pela opção "Logout" do menu suspenso do usuário. O encerramento automático, quando o cadastro corporativo recusa a credencial, não está no documento: vem do código 💻 |

---

<div class="dev-only">

## Superfície

**Ação em tela** — origem: Consultar Dados do Usuário `ACE-AUT-06` (menu do usuário, no cabeçalho de todas as telas internas), item "Logout"

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Efetuar Logout" de GPE001

---

</div>

## Regras de negócio

1. Encerrar a sessão apaga do navegador o que a autenticação guardou: a credencial, os dados do usuário e o menu do perfil. 💻
2. O encerramento acontece só no navegador: o cadastro corporativo não é avisado, e a credencial não é cancelada lá. 💻 ⚠️ Se a credencial continua aceita pelo cadastro corporativo até vencer, o código do GPE não permite confirmar ❓.
3. A sessão também se encerra sozinha quando o cadastro corporativo recusa a credencial do usuário em qualquer operação; o GPE não a renova. 💻
4. Encerrada a sessão, nada do sistema deve ficar ao alcance sem nova autenticação. → ver [N1 Acesso e Usuários](../README.md): Regras transversais de negócio: 4 ⚠️ 🔍 Pelo código, o encerramento limpa o que está guardado no navegador, mas não o que a página aberta ainda tem em memória; até a página ser recarregada, a regra não se sustenta.

---

## Cenários

```gherkin
Feature: Encerrar sessão

  Background:
    Given que o usuário está autenticado no GPE
    And está em uma tela interna do sistema

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Sair pelo menu do usuário
    When o usuário abre o menu do usuário, no cabeçalho, e aciona "Logout"
    Then o sistema encerra a sessão, sem pedir confirmação
    And abre a tela de acesso

  Scenario: Voltar ao sistema depois de sair
    Given que o usuário acionou "Logout"
    When recarrega a página ou abre de novo o endereço do sistema
    Then o sistema mostra a tela de acesso e pede usuário e senha

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há dado a validar
    When o usuário aciona "Logout"
    Then o sistema encerra a sessão sem solicitar nenhum dado

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Não há conflito com dados existentes
    When o usuário aciona "Logout"
    Then o sistema encerra a sessão sem consultar nem alterar registro algum
    # 💻 o que estiver preenchido e não salvo na tela aberta se perde, sem aviso

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Não há restrição por perfil para sair
    Given que o usuário está autenticado, com qualquer perfil
    When abre o menu do usuário
    Then a opção "Logout" está disponível

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Credencial recusada durante o uso
    Given que o cadastro corporativo deixou de aceitar a credencial do usuário
    When o usuário executa qualquer operação que consulte o servidor
    Then o sistema encerra a sessão e abre a tela de acesso
    # 💻 a tela de acesso não explica por que a sessão caiu
    # 💻 o código tem pronta a renovação automática da credencial, mas ela está desligada

  Scenario: Voltar pelo navegador logo depois de sair
    Given que o usuário acionou "Logout" e a página não foi recarregada
    When usa o botão de voltar do navegador
    Then o sistema reabre a tela interna anterior, como se a sessão continuasse aberta
    # ⚠️ 🔍 suspeita de defeito: a sessão é apagada do navegador, mas não da memória da página; inferido da leitura do código, a confirmar em execução
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| — | Usuario | — | — | — | — | A ação não tem campos: encerra a sessão do usuário autenticado, sem confirmação |

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| — | — | Nenhum campo é gravado: a sessão guardada no navegador é apagada, e o cadastro corporativo não é alterado |

---

## Comportamento de tela

### Onde fica
No cabeçalho de todas as telas internas, à direita, ficam o nome e a foto do usuário; o clique neles abre o menu do usuário. "Logout" é o último item desse menu, com o ícone de saída, abaixo de "Alterar Foto do Perfil" e de "Alterar Senha". O clique encerra a sessão na hora, sem pergunta de confirmação. 💻

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Não se aplica — o encerramento é imediato e não consulta o servidor 💻 |
| Erro de validação | Não se aplica — não há campos |
| Erro de servidor | Não se aplica — nenhuma operação do servidor é chamada 💻 |
| Sucesso | Sem mensagem: o sistema abre a tela de acesso |
| Empty state | Não se aplica — a ação não lista dados |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Depois de "Logout", a página recarregada ou reaberta mostra a tela de acesso e pede usuário e senha | Regra 1 · cenário "Voltar ao sistema depois de sair" |
| SC-02 | Depois de encerrada a sessão, nenhuma tela interna é exibida sem nova autenticação ⚠️ hoje não atendido enquanto a página não é recarregada | Regra 4 · cenário "Voltar pelo navegador logo depois de sair" |
| SC-03 | A credencial recusada pelo cadastro corporativo leva o usuário à tela de acesso | Regra 3 · cenário "Credencial recusada durante o uso" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Encerrar Sessão | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade Usuario

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Item "Logout" do menu do usuário | sistema_mesa_checkin_frontend | `src/app/shared/layout/topbar/topbar.component.html` (linhas 60–65) e `.ts` (linhas 113–116) | — |
| Limpeza da sessão guardada no navegador | sistema_mesa_checkin_frontend | `src/app/service/core/auth.service.ts` (linhas 126–134) | — |
| Encerramento automático por credencial recusada | sistema_mesa_checkin_frontend | `src/app/service/core/interceptor.service.ts` (linhas 33–49 e 135–151) | — |
| Exigência de sessão nas telas internas | sistema_mesa_checkin_frontend | `src/app/service/core/auth-guard.service.ts` (linhas 11–18) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

Nenhuma operação é chamada no encerramento, nem no servidor do GPE nem no serviço corporativo. `AuthService.logout()` remove do `localStorage` as chaves `access_token`, `token_type`, `expires_in`, `refresh_token`, `usuario` e `menus`, mas não zera as propriedades `usuario`, `access_token` e `menus` em memória — é o valor em memória que `AuthGuard` consulta — nem remove a chave `eventoPrincipalId`. O encerramento automático ocorre nas respostas de status `401` e nas de status `400` com `invalid_grant`.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE001 – Efetuar Login (funcionalidade "Efetuar Logout") e do código |

---

*Feature Set: Autenticação · Major Feature Set: Acesso e Usuários · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
