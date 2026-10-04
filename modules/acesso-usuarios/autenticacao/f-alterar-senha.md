<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: ACE-AUT-04
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

# Alterar Senha
> **Nível 3** - Feature Set: Autenticação — Major Feature Set: Acesso e Usuários - `ACE-AUT-04`

## Descrição

Permite que o usuário altere a senha com que entra no sistema — por obrigação, quando a senha em uso é provisória, ou por vontade própria, a qualquer momento; a nova senha passa a valer de imediato e ele segue autenticado com ela.

Na troca obrigatória, a tela se abre sozinha quando o usuário tenta entrar com a senha provisória, e pede só a nova senha e a sua confirmação. Na voluntária, o usuário já autenticado abre a tela pela opção Alterar Senha do menu do usuário e informa também a senha atual. Nos dois casos, a troca é feita pelo botão Alterar Senha.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE001 – Efetuar Login v1.0, de 03/10/2025 (documento legado), funcionalidade "Alterar senha do primeiro acesso" ⚠️ sem chave na ferramenta de demandas | Criação | — Definir uma nova senha de acesso ao entrar com a senha recebida por e-mail. ⚠️ O documento só descreve a troca do primeiro acesso 📄; a troca voluntária, pela opção "Alterar Senha" do menu do usuário, aparece nas imagens do documento mas não é descrita: vem do código 💻 |

---

<div class="dev-only">

## Superfície

**Tela própria** — rota `/alterar-senha`

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Alterar senha do primeiro acesso" de GPE001, que mostra só a troca do primeiro acesso

---

</div>

## Regras de negócio

1. A nova senha tem no mínimo 8 caracteres. 💻 → ver [N1 Acesso e Usuários](../README.md): Regras transversais de negócio: 5
2. A nova senha é informada duas vezes, e as duas digitações têm de ser iguais. 💻
3. A troca exige a senha em uso: na voluntária, o usuário a informa; na obrigatória, vale a senha provisória com que ele acabou de tentar entrar, sem pedi-la de novo. 💻
4. A troca é feita no cadastro corporativo da CNI, para o login do usuário; o GPE não guarda a senha. 💻 → ver [N1 Acesso e Usuários](../README.md): Regras transversais de negócio: 1
5. A troca obrigatória acontece antes de o usuário entrar: enquanto a senha provisória não for trocada, ele não chega ao sistema.
6. Trocada a senha, o usuário fica autenticado com a senha nova, sem precisar informá-la outra vez. 💻
7. O GPE só confere o tamanho mínimo e a igualdade das duas digitações. Composição da senha, reuso de senha anterior e igualdade com a senha atual não são conferidos por ele; se o cadastro corporativo confere, o código do GPE não mostra. ❓

---

## Cenários

```gherkin
Feature: Alterar senha

  Background:
    Given que o usuário está na tela Alterar senha

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Trocar a senha provisória, na troca obrigatória
    Given que o usuário tentou entrar com a senha provisória e foi trazido a esta tela
    And a tela mostra "Nova Senha" e "Confirme a Nova Senha", sem "Senha Atual"
    When informa a mesma senha, de 8 caracteres ou mais, nos dois campos e aciona "Alterar Senha"
    Then o cadastro corporativo passa a aceitar a nova senha
    And o sistema autentica o usuário com ela e abre a tela de boas-vindas
    # ⚠️ 💻 o destino é a tela de boas-vindas para qualquer perfil; Secretaria Mesa e Secretaria Check-In, que na autenticação comum vão para os participantes do evento principal, aqui não vão

  Scenario: Trocar a senha por vontade própria, na troca voluntária
    Given que o usuário está autenticado e abriu a tela pela opção "Alterar Senha" do menu do usuário
    When informa "Senha Atual", "Nova Senha" e "Confirme a Nova Senha" e aciona "Alterar Senha"
    Then o cadastro corporativo passa a aceitar a nova senha
    And o sistema autentica de novo o usuário com ela e abre a tela de boas-vindas
    # 💻 GPE001 não descreve esta entrada

  Scenario: Desistir da troca
    When o usuário aciona "Voltar"
    Then o sistema abre a tela de acesso, sem alterar a senha
    # ⚠️ 💻 na troca voluntária, "Voltar" também leva à tela de acesso, embora o usuário continue autenticado

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Nova senha não informada
    When o usuário deixa "Nova Senha" vazia e aciona "Alterar Senha"
    Then o sistema exibe abaixo do campo: "Senha obrigatória"
    And a senha não é trocada

  Scenario: Nova senha com menos de 8 caracteres
    When o usuário informa em "Nova Senha" um texto de 7 caracteres e aciona "Alterar Senha"
    Then o sistema exibe abaixo do campo: "A sua senha deve ter mais de 8 caracteres."
    And a senha não é trocada
    # ⚠️ o texto diz "mais de 8", mas a senha de exatamente 8 caracteres é aceita 💻

  Scenario: Confirmação diferente da nova senha
    When o usuário informa valores diferentes em "Nova Senha" e em "Confirme a Nova Senha"
    Then o sistema exibe abaixo da confirmação: "As senhas não conferem."
    And a senha não é trocada

  Scenario: Senha atual não informada, na troca voluntária
    Given que a tela foi aberta pelo menu do usuário
    When o usuário deixa "Senha Atual" vazia e aciona "Alterar Senha"
    Then o sistema exibe abaixo do campo: "Senha obrigatória"
    And a senha não é trocada

  Scenario: Senha atual incorreta, na troca voluntária
    Given que a tela foi aberta pelo menu do usuário
    And o usuário informa em "Senha Atual" uma senha que não é a sua
    When aciona "Alterar Senha"
    Then o cadastro corporativo recusa a troca e a senha continua a mesma
    And o sistema permanece na tela, sem mostrar o motivo
    # ⚠️ suspeita de defeito: o erro é gerado, mas a tela não tem onde exibi-lo 💻 🔍

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Nova senha recusada pelo cadastro corporativo
    Given que o cadastro corporativo recusa a nova senha informada
    When o usuário aciona "Alterar Senha"
    Then a senha continua a mesma
    And o sistema permanece na tela, sem mostrar o motivo
    # ❓ os motivos de recusa — composição da senha, reuso de senha anterior — são do cadastro corporativo; não estão no código do GPE
    # ⚠️ o texto previsto é "Erro" com o detalhe enviado ou "Serviço indisponível.", mas a tela não tem onde exibi-lo 💻 🔍

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Abrir a tela sem sessão e sem troca pendente
    Given que a pessoa não está autenticada nem acabou de tentar entrar com senha provisória
    When digita o endereço da tela Alterar senha
    Then o sistema abre a tela de acesso

  Scenario: Não há restrição por perfil para trocar a senha
    Given que o usuário está autenticado, com qualquer perfil
    When abre o menu do usuário
    Then a opção "Alterar Senha" está disponível

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Aviso de troca obrigatória
    Given que o usuário foi trazido a esta tela por ter tentado entrar com a senha provisória
    When a tela se abre
    Then ela não mostra "Senha Atual"
    And o aviso previsto no topo é "Alteração de senha obrigatória!", com o detalhe "Para continuar altere a sua senha."
    # ⚠️ 🔍 o aviso está definido no código, mas a forma como é montado indica que o texto não aparece como previsto; na imagem de GPE001 ele não aparece — confirmar em execução

  Scenario: Troca voluntária logo depois de uma troca obrigatória
    Given que o usuário fez a troca obrigatória e, sem recarregar a página, abre "Alterar Senha" pelo menu do usuário
    When a tela se abre
    Then ela volta no modo obrigatório, sem "Senha Atual", valendo como senha em uso a provisória que já foi substituída
    # ⚠️ 🔍 suspeita de defeito: o sistema não esquece a troca obrigatória depois de concluída; a nova troca tende a ser recusada, sem mensagem

  Scenario: Falha ao autenticar depois da troca
    Given que a senha foi trocada, mas a autenticação com a nova senha falha
    When o cadastro corporativo responde
    Then o sistema permanece na tela, sem mensagem, com a senha já trocada
    # 💻 🔍 o usuário precisa voltar à tela de acesso e entrar com a nova senha
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| Senha Atual | Usuario | entrada do usuário | editável | texto | sim | Só aparece na troca voluntária; na obrigatória fica oculto, já com a senha provisória usada na tentativa de entrada. Mínimo de 8 caracteres. Digitação oculta |
| Nova Senha | Usuario | entrada do usuário | editável | texto | sim | Mínimo de 8 caracteres. Digitação oculta, sem opção de mostrar o que foi digitado |
| Confirme a Nova Senha | Usuario | entrada do usuário | editável | texto | sim | Mínimo de 8 caracteres e igual a Nova Senha. Digitação oculta |

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| — | — | Nenhum campo é preenchido pelo GPE: a nova senha é registrada no cadastro corporativo da CNI. Se ele guarda a data e o autor da troca, o código do GPE não mostra ❓ |

---

## Comportamento de tela

### Onde fica
Na tela Alterar senha, que usa a mesma moldura da tela de acesso: o título "Seja bem-vindo(a) ao Portal de Gestão de Participantes em Eventos!", a frase "Faça o login para acessar." e a ilustração à direita. Dentro dela ficam os campos e os botões "Alterar Senha" e "Voltar", este em vermelho.

Chega-se a ela por dois caminhos. Na troca obrigatória, é a autenticação que a abre, quando a senha usada é provisória; a tela mostra só "Nova Senha" e "Confirme a Nova Senha". Na troca voluntária, o usuário a abre pela opção "Alterar Senha" do menu do usuário, no cabeçalho de qualquer tela interna; a tela mostra também "Senha Atual". ⚠️ Na voluntária, o usuário autenticado sai das telas internas — sem cabeçalho nem menu — e vê a moldura da tela de acesso, com a frase "Faça o login para acessar."; e o botão "Voltar" o leva à tela de acesso, não à tela de onde veio. 💻

Depois da troca, o sistema abre a tela de boas-vindas, para qualquer perfil. 💻

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Sem indicador: enquanto a troca é processada, a tela fica como está e o botão "Alterar Senha" continua disponível 💻 |
| Erro de validação | Texto em vermelho abaixo de cada campo, depois que ele é tocado ou que "Alterar Senha" é acionado: "Senha obrigatória" ou "A sua senha deve ter mais de 8 caracteres.". Abaixo da confirmação, "As senhas não conferem." aparece assim que os dois valores diferem — inclusive enquanto a nova senha é digitada e a confirmação ainda está vazia 💻 |
| Erro de servidor | ⚠️ Nenhuma mensagem aparece: o texto previsto é "Erro" com o detalhe enviado pelo cadastro corporativo ou, sem detalhe, "Serviço indisponível.", mas a tela não tem a área onde ele seria exibido 💻 🔍 |
| Sucesso | Sem mensagem: o sistema autentica o usuário com a nova senha e abre a tela de boas-vindas |
| Empty state | Não se aplica — a tela não lista dados |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Depois da troca, o usuário está autenticado e entra no sistema com a nova senha | Regra 6 · cenários do caminho feliz |
| SC-02 | Quem tentou entrar com senha provisória só chega às telas internas depois de trocá-la | Regra 5 · cenário "Trocar a senha provisória, na troca obrigatória" |
| SC-03 | Nenhuma troca é feita com nova senha de menos de 8 caracteres ou com confirmação diferente | Regras 1 e 2 · cenários de erro de validação |
| SC-04 | A troca recusada informa o motivo ao usuário ⚠️ hoje não atendido | Cenários "Senha atual incorreta, na troca voluntária" e "Nova senha recusada pelo cadastro corporativo" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Alterar Senha | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade Usuario

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Tela Alterar senha: campos, modo obrigatório e destino depois da troca | sistema_mesa_checkin_frontend | `src/app/auth/alterar-senha/alterar-senha.component.ts` (linhas 28–82) e `.html` (linhas 1–49) | — |
| Condição para abrir a tela | sistema_mesa_checkin_frontend | `src/app/auth/alterar-senha/alterar-senha-guard.ts` (linhas 12–18) | — |
| Desvio da autenticação para a troca obrigatória | sistema_mesa_checkin_frontend | `src/app/auth/login/login.component.ts` (linhas 80–100) | — |
| Envio da troca ao serviço corporativo | sistema_mesa_checkin_frontend | `src/app/service/core/auth.service.ts` (linhas 14 e 76–82) | — |
| Item "Alterar Senha" do menu do usuário | sistema_mesa_checkin_frontend | `src/app/shared/layout/topbar/topbar.component.html` (linhas 54–59) | — |
| Validação de senha e de confirmação | sistema_mesa_checkin_frontend | `src/app/shared/basic-validators.ts` (linhas 120–143) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

A troca não passa pelo servidor do GPE: a tela chama direto o serviço corporativo, no endereço recebido em `urlAlteracaoSenha`, com o login no lugar de `{login}` e o corpo `{senhaAtual, senhaNova, confirmaSenha}`. O modo obrigatório é `auth.alteracaoSenha.senhaAtual` preenchido; `auth.alteracaoSenha` nunca é limpo depois da troca. O template não tem `<p-toast>`, e o componente declara um `MessageService` próprio: o que `handleError` emite não tem onde aparecer. O aviso de troca obrigatória interpola, dentro de `<p-message>`, uma lista de objeto (`alterarSenhaAlerta`), e não o texto dela.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE001 – Efetuar Login (funcionalidade "Alterar senha do primeiro acesso") e do código, que acrescenta a troca voluntária |

---

*Feature Set: Autenticação · Major Feature Set: Acesso e Usuários · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
