<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: ACE-AUT-03
feature_set: ACE-AUT
dominio: ACE
entidade: Usuario
data_model_ref: data-models/acesso-usuarios.md#usuario
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

# Recuperar Senha
> **Nível 3** - Feature Set: Autenticação — Major Feature Set: Acesso e Usuários - `ACE-AUT-03`

## Descrição

Permite que o usuário que esqueceu a senha recupere o acesso informando apenas o seu login; o cadastro corporativo da CNI envia a ele uma senha temporária, com a qual volta a entrar no sistema.

Chega-se pelo atalho "Esqueceu a senha?", na tela de acesso, sem precisar estar autenticado. O usuário informa o login no campo Usuário e aciona Recuperar senha; o botão Voltar retorna à tela de acesso sem pedir nada.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE001 – Efetuar Login v1.0, de 03/10/2025 (documento legado), funcionalidade "Esqueci Minha Senha" ⚠️ sem chave na ferramenta de demandas | Criação | — Solicitar uma nova senha informando o login. ⚠️ O documento diz que o sistema encaminha um link para o usuário definir a nova senha 📄; a tela, inclusive na imagem do próprio documento, fala em senha temporária enviada 💻 |

---

<div class="dev-only">

## Superfície

**Tela própria** — rota `/recuperar-senha`

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Esqueci Minha Senha" de GPE001

---

</div>

## Regras de negócio

1. A recuperação de senha está ao alcance de quem não está autenticado. 💻 → ver [N1 Acesso e Usuários](../README.md): Regras transversais de negócio: 4
2. O pedido é identificado só pelo login: nenhum outro dado é exigido para comprovar que quem pede é o dono da conta. 💻
3. Quem gera e envia a senha é o cadastro corporativo da CNI; o GPE só encaminha o pedido e não chega a conhecer a senha enviada. 💻 → ver [N1 Acesso e Usuários](../README.md): Regras transversais de negócio: 1
4. O que o usuário recebe é uma senha temporária. 💻 ⚠️ GPE001 diz que o sistema encaminha um link para o usuário definir a nova senha 📄. O envio é feito pelo cadastro corporativo, e o código do GPE não permite confirmar qual dos dois de fato chega ao usuário, nem por qual meio ❓ — presume-se o e-mail do cadastro dele 🔍.
5. A senha temporária é provisória: ao autenticar-se com ela, o usuário é levado a definir uma senha nova antes de entrar. 🔍
6. Por quanto tempo a senha temporária vale, e se a senha anterior continua valendo até ela ser usada, é decisão do cadastro corporativo. ❓

---

## Cenários

```gherkin
Feature: Recuperar senha

  Background:
    Given que a pessoa não tem sessão aberta no GPE
    And está na tela Recuperar senha, aberta pelo atalho "Esqueceu a senha?" da tela de acesso

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Pedir a senha temporária
    When a pessoa informa o seu login em "Usuário" e aciona "Recuperar senha"
    Then o cadastro corporativo envia ao usuário uma senha temporária
    And o sistema volta à tela de acesso
    And exibe: "Senha temporária enviada."
    # ⚠️ GPE001 fala em link para definir a nova senha 📄; o texto da tela e a confirmação falam em senha temporária 💻
    # ⚠️ 🔍 suspeita de defeito: a confirmação é emitida no instante em que a tela muda, por um canal que nem esta tela nem a de acesso acompanham; é provável que não chegue a aparecer — confirmar em execução

  Scenario: Entrar com a senha temporária recebida
    Given que o usuário recebeu a senha temporária
    When se autentica com ela na tela de acesso
    Then o sistema abre a tela Alterar senha, no modo de troca obrigatória
    # 🔍 inferido: a troca obrigatória depende de o cadastro corporativo tratar a senha temporária como provisória
    # a autenticação é a feature Autenticar Usuário (ACE-AUT-01); a troca, Alterar Senha (ACE-AUT-04)

  Scenario: Desistir do pedido
    When a pessoa aciona "Voltar"
    Then o sistema abre a tela de acesso, sem enviar pedido algum

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Sair do campo sem informar o login
    When a pessoa clica em "Usuário" e sai do campo sem preenchê-lo
    Then o sistema exibe abaixo do campo: "Campo obrigatório."
    # ← MESSAGE-DICTIONARY: BASELINE

  Scenario: Acionar a recuperação sem informar o login
    When a pessoa aciona "Recuperar senha" com "Usuário" vazio
    Then o sistema envia o pedido mesmo assim, sem conferir o campo
    # ⚠️ suspeita de defeito: o campo é obrigatório, mas o botão não confere o preenchimento 💻
    # ❓ o que o cadastro corporativo responde a um pedido sem login não está no código do GPE

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Pedido recusado pelo cadastro corporativo
    Given que o cadastro corporativo recusa o pedido para o login informado
    When a pessoa aciona "Recuperar senha"
    Then o sistema permanece na tela Recuperar senha
    And exibe a mensagem "Erro" com o detalhe enviado pelo cadastro corporativo
    # ❓ os motivos de recusa — login que não existe, usuário inativo — e o texto de cada um são do cadastro corporativo; não estão no código do GPE

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Não há restrição de acesso
    When a pessoa informa um login qualquer e aciona "Recuperar senha"
    Then o sistema encaminha o pedido ao cadastro corporativo, sem conferir quem o faz
    # ⚠️ quem conhece o login de outro usuário consegue pedir a recuperação da senha dele 💻

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Falha sem detalhe no envio
    Given que o cadastro corporativo não responde ou responde sem dizer o motivo
    When a pessoa aciona "Recuperar senha"
    Then o sistema permanece na tela Recuperar senha
    And exibe a mensagem "Erro" com o detalhe "Serviço indisponível."
    # ← MESSAGE-DICTIONARY: BASELINE
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| Usuário | Usuario | entrada do usuário | editável | texto | sim | É o login do usuário. A obrigatoriedade só é conferida quando o campo é tocado: o botão "Recuperar senha" não confere o preenchimento ⚠️ 💻. A tela não limita o tamanho nem aplica máscara |

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| Senha temporária | Gerada e enviada pelo cadastro corporativo da CNI; o GPE não a conhece 💻 | Quando o cadastro corporativo aceita o pedido de recuperação |

---

## Comportamento de tela

### Onde fica
Na tela Recuperar senha, aberta pelo atalho "Esqueceu a senha?" da tela de acesso. Ela usa a mesma moldura da tela de acesso — o título "Seja bem-vindo(a) ao Portal de Gestão de Participantes em Eventos!", a frase "Faça o login para acessar." e a ilustração à direita — e, dentro dela, traz o aviso informativo "Digite seu login e uma senha temporária será enviada para redefinir a sua senha", o campo "Usuário" e os botões "Recuperar senha" e "Voltar", este em vermelho.

A tela não confere se há sessão aberta: quem já está autenticado e digita o endereço dela também a vê. 💻

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Sem indicador: enquanto o pedido é processado, a tela fica como está e o botão "Recuperar senha" continua disponível 💻 |
| Erro de validação | "Campo obrigatório." em vermelho abaixo do campo, só depois que ele é tocado; acionar "Recuperar senha" não dispara a validação ⚠️ |
| Erro de servidor | Mensagem "Erro" com o detalhe enviado pelo cadastro corporativo; sem detalhe, "Serviço indisponível.". O usuário permanece na tela |
| Sucesso | O sistema volta à tela de acesso. A confirmação prevista é "Senha temporária enviada." ⚠️ 🔍 provavelmente não chega a aparecer |
| Empty state | Não se aplica — a tela não lista dados |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | O usuário que informa o próprio login recebe do cadastro corporativo o meio de voltar a entrar, sem depender de um administrador | Regras 3 e 4 · cenário "Pedir a senha temporária" |
| SC-02 | Depois do pedido aceito, o usuário está de volta à tela de acesso e sabe que a senha foi enviada ⚠️ a confirmação hoje provavelmente não aparece | Cenário "Pedir a senha temporária" |
| SC-03 | O pedido recusado mantém o usuário na tela, com o motivo informado | Cenário "Pedido recusado pelo cadastro corporativo" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Recuperar Senha | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade Usuario

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Tela Recuperar senha | sistema_mesa_checkin_frontend | `src/app/auth/recuperar-senha/RecuperarSenhaComponent.ts` (linhas 39–56) e `src/app/auth/recuperar-senha/recuperar-senha.component.html` (linhas 1–30) | — |
| Envio do pedido ao serviço corporativo | sistema_mesa_checkin_frontend | `src/app/service/core/auth.service.ts` (linhas 96–102) | — |
| Atalho "Esqueceu a senha?" na tela de acesso | sistema_mesa_checkin_frontend | `src/app/auth/login/login.component.html` (linha 29) | — |
| Rota sem exigência de sessão | sistema_mesa_checkin_frontend | `src/app/auth/auth.routing.ts` (linhas 22–25) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

O pedido não passa pelo servidor do GPE: a tela chama direto o serviço corporativo, no endereço recebido em `urlRecuperacaoSenha`, com o login no lugar de `{login}` e sem corpo. `recuperarSenha()` não chama `validateForm()` nem testa `form.valid`; com o campo vazio, o login vai como o texto `null`. A confirmação usa `AlertaService`, ligado ao `MessageService` da aplicação, enquanto o `<p-toast>` desta tela e o da tela de acesso escutam o `MessageService` do próprio componente.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE001 – Efetuar Login (funcionalidade "Esqueci Minha Senha") e do código |

---

*Feature Set: Autenticação · Major Feature Set: Acesso e Usuários · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
