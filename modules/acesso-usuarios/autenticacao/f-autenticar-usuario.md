<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: ACE-AUT-01
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

# Autenticar Usuário
> **Nível 3** - Feature Set: Autenticação — Major Feature Set: Acesso e Usuários - `ACE-AUT-01`

## Descrição

Permite que o usuário entre no sistema informando usuário e senha; autenticado no cadastro corporativo da CNI, ele chega à tela inicial do seu perfil, com o menu que esse perfil enxerga.

A tela de acesso é a primeira que o sistema mostra a quem não tem sessão aberta, qualquer que seja o endereço digitado. O usuário informa Usuário e Senha e aciona Entrar; quem esqueceu a senha segue pelo atalho "Esqueceu a senha?".

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE001 – Efetuar Login v1.0, de 03/10/2025 (documento legado), funcionalidade "Efetuar Login" ⚠️ sem chave na ferramenta de demandas | Criação | — Acessar o sistema com usuário e senha e chegar à tela inicial, com as opções de menu do perfil. O destino próprio das secretarias, o desvio para a troca obrigatória de senha, a validação dos campos e a sessão lembrada não estão no texto da funcionalidade: vêm do código 💻. No Jira, a tarefa `PDTIC25148-17` (Definir uma página de login para aplicação, concluída) trata desta tela; os critérios dela não foram consultados e não há AIM aberta |

---

<div class="dev-only">

## Superfície

**Tela própria** — rota `/login`

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Efetuar Login" de GPE001

---

</div>

## Regras de negócio

1. Usuário e senha são conferidos no cadastro corporativo da CNI; o GPE não guarda senha nem decide se ela está certa. 💻 → ver [N1 Acesso e Usuários](../README.md): Regras transversais de negócio: 1
2. A senha informada para entrar tem no mínimo 8 caracteres; com menos que isso, o pedido nem chega ao cadastro corporativo. 💻 → ver [N1 Acesso e Usuários](../README.md): Regras transversais de negócio: 5
3. O menu que o usuário enxerga depois de entrar é o do seu perfil, definido no cadastro corporativo e entregue junto com a autenticação.
4. O ponto de chegada depende do perfil: Secretaria Mesa e Secretaria Check-In chegam aos participantes do evento principal; os demais perfis, à página de boas-vindas. 💻 ⚠️ GPE001 fala de um único destino para todos os perfis 📄.
5. Quem se autentica com senha provisória só entra depois de definir uma senha nova. A senha provisória é a recebida por e-mail na inclusão do usuário 📄 e, ao que tudo indica, também a enviada na recuperação de senha 🔍; quem diz que a senha é provisória é o cadastro corporativo 💻.
6. A sessão aberta fica guardada no navegador e vale até o usuário sair ou até o cadastro corporativo recusar a credencial: fechar e reabrir o navegador não exige nova autenticação. 💻 ⚠️ O código prevê uma opção de lembrar ou não a sessão, que não é oferecida ao usuário nem respeitada — a sessão é sempre lembrada.
7. O GPE não renova a credencial da sessão: por quanto tempo ela vale é decisão do cadastro corporativo. 💻 ❓ O prazo não está no código do GPE.
8. O GPE não limita o número de tentativas de entrada nem suspende o usuário por senha errada; se existe esse controle, é do cadastro corporativo. 💻 ❓

---

## Cenários

```gherkin
Feature: Autenticar usuário

  Background:
    Given que a pessoa não tem sessão aberta no GPE
    And está na tela de acesso

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Entrar com perfil que chega à tela de boas-vindas
    Given que o usuário tem o perfil "Administrador"
    When informa "Usuário" e "Senha" corretos e aciona "Entrar"
    Then o sistema abre a tela inicial, com o texto "Seja bem-vindo ao Gestão de Participantes em Eventos"
    And o menu traz os itens que o cadastro corporativo define para o perfil dele

  Scenario: Entrar como Secretaria Mesa ou Secretaria Check-In
    Given que o usuário tem o perfil "Secretaria Mesa" ou "Secretaria Check-In"
    And existe um evento marcado como principal
    When informa "Usuário" e "Senha" corretos e aciona "Entrar"
    Then o sistema abre os participantes do evento principal, sem passar pela tela de boas-vindas
    # 💻 GPE001 só fala em "tela inicial do sistema"; o destino próprio das secretarias vem do código
    # ⚠️ a comparação é pelo nome exato do perfil: qualquer outro perfil, inclusive Painel e Participante, vai para a tela de boas-vindas

  Scenario: Entrar com senha provisória
    Given que a senha do usuário é provisória
    When informa "Usuário" e a senha provisória e aciona "Entrar"
    Then o sistema abre a tela Alterar senha, no modo de troca obrigatória, sem pedir de novo a senha provisória
    And o usuário só chega ao sistema depois de definir a nova senha
    # a troca em si é a feature Alterar Senha (ACE-AUT-04)
    # 💻 🔍 antes de mudar de tela, o sistema emite a mensagem de erro comum; como a tela muda em seguida, é provável que ela não chegue a ser vista

  Scenario: Seguir para a recuperação de senha
    When a pessoa aciona "Esqueceu a senha?"
    Then o sistema abre a tela Recuperar senha

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Usuário não informado
    When a pessoa deixa "Usuário" vazio e aciona "Entrar"
    Then o sistema exibe abaixo do campo: "Campo obrigatório."
    And nada é enviado ao cadastro corporativo
    # ← MESSAGE-DICTIONARY: BASELINE

  Scenario: Senha não informada
    When a pessoa deixa "Senha" vazia e aciona "Entrar"
    Then o sistema exibe abaixo do campo: "Senha obrigatória"
    And nada é enviado ao cadastro corporativo

  Scenario: Senha com menos de 8 caracteres
    When a pessoa informa em "Senha" um texto de 7 caracteres e aciona "Entrar"
    Then o sistema exibe abaixo do campo: "A sua senha deve ter mais de 8 caracteres."
    And nada é enviado ao cadastro corporativo
    # ⚠️ o texto diz "mais de 8", mas a senha de exatamente 8 caracteres é aceita 💻

  Scenario: Usuário ou senha que o cadastro corporativo não reconhece
    Given que o cadastro corporativo recusa o usuário e a senha informados
    When a pessoa aciona "Entrar"
    Then o sistema mantém a pessoa na tela de acesso
    And exibe a mensagem "Erro" com o detalhe enviado pelo cadastro corporativo
    # ❓ o texto do detalhe é do cadastro corporativo; não está no código do GPE

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Não há conflito com dados existentes
    When a pessoa aciona "Entrar"
    Then o sistema só confere usuário e senha, sem criar nem alterar registro algum

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Abrir tela interna sem sessão aberta
    When a pessoa digita o endereço de uma tela interna do sistema
    Then o sistema mostra a tela de acesso no lugar da tela pedida
    And, depois de entrar, a pessoa é levada ao ponto de chegada do seu perfil, não ao endereço que havia digitado
    # 💻 GPE001 dá como endereço de acesso o da tela de pessoas, que é interna: quem o usa cai na tela de acesso

  Scenario: Não há restrição por perfil para entrar
    Given que a pessoa tem usuário e senha válidos, de qualquer perfil
    When aciona "Entrar"
    Then o sistema a autentica; o que muda conforme o perfil é o menu e o ponto de chegada

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Secretaria entra sem haver evento principal
    Given que o usuário tem o perfil "Secretaria Mesa" ou "Secretaria Check-In"
    And nenhum evento está marcado como principal
    When informa "Usuário" e "Senha" corretos e aciona "Entrar"
    Then a autenticação é concluída, mas o sistema permanece na tela de acesso, sem mensagem
    # ⚠️ 🔍 suspeita de defeito: o código não trata a falta de evento principal nem a falha ao buscá-lo; existe uma tela de aviso para esse caso, que nunca é aberta 💻

  Scenario: Falha sem detalhe na autenticação
    Given que o cadastro corporativo não responde ou responde sem dizer o motivo
    When a pessoa aciona "Entrar"
    Then o sistema exibe a mensagem "Erro" com o detalhe "Serviço indisponível."
    # ← MESSAGE-DICTIONARY: BASELINE

  Scenario: Serviços corporativos fora do ar ao abrir o sistema
    Given que o sistema não consegue obter os endereços dos serviços corporativos
    When a pessoa abre o sistema
    Then a tela de acesso não é exibida, e nenhuma mensagem explica o motivo
    # 💻 ⚠️ a abertura da tela é barrada sem aviso; 🔍 a página tende a ficar em branco

  Scenario: Reabrir o sistema com a sessão guardada
    Given que o usuário entrou antes neste navegador e não saiu
    When abre de novo o endereço do sistema
    Then o sistema abre a tela de boas-vindas, sem pedir usuário e senha
    # 💻 ⚠️ vale para qualquer perfil: Secretaria Mesa e Secretaria Check-In, que ao entrar vão para os participantes do evento principal, aqui caem na tela de boas-vindas
    # 🔍 pelo menu cadastrado para o sistema, esses dois perfis só têm o item Dashboard: da tela de boas-vindas não há caminho de menu até os participantes
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| Usuário | Usuario | entrada do usuário | editável | texto | sim | É o login do usuário; para usuário externo, o endereço de e-mail. Obrigatório. A tela não limita o tamanho nem aplica máscara 💻 |
| Senha | Usuario | entrada do usuário | editável | texto | sim | Obrigatória, com no mínimo 8 caracteres. A digitação fica oculta; o ícone de olho, dentro do campo, mostra o que foi digitado |

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| Sessão do usuário | A credencial, os dados do usuário (nome, login, perfil e e-mail) e o menu do perfil, devolvidos pelo cadastro corporativo 💻 | Ao autenticar; fica guardada no navegador até o usuário sair |

---

## Dados lidos e gravados

| Entidade | Papel | Por que a feature a toca |
|---|---|---|
| PerfilAcesso | lê | O perfil do usuário vem com a autenticação e define o menu e o ponto de chegada (regras 3 e 4) |
| Evento | lê | Para Secretaria Mesa e Secretaria Check-In, localiza o evento principal, cujos participantes são o ponto de chegada (regra 4) |

---

## Comportamento de tela

### Onde fica
Na tela de acesso, que ocupa a tela inteira: à esquerda, o título "Seja bem-vindo(a) ao Portal de Gestão de Participantes em Eventos!", a frase "Faça o login para acessar.", os campos "Usuário" e "Senha", o atalho "Esqueceu a senha?", o botão "Entrar" e as marcas do Sistema Indústria; à direita, uma ilustração. A tecla Enter, em qualquer dos campos, equivale ao botão "Entrar". 💻

É a tela que o sistema mostra a quem não tem sessão aberta, qualquer que seja o endereço digitado. Depois de entrar, o usuário vai para o ponto de chegada do seu perfil — os participantes do evento principal, para Secretaria Mesa e Secretaria Check-In, e a tela de boas-vindas, para os demais —, e não para o endereço que havia digitado. 💻

A tela não oferece a opção de lembrar ou não a sessão: ela é sempre lembrada. ⚠️ Quem já tem sessão aberta e digita o endereço da tela de acesso vê a tela normalmente, sem ser levado ao sistema. 💻

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Sem indicador: enquanto o cadastro corporativo confere usuário e senha, a tela fica como está e o botão "Entrar" continua disponível 💻 |
| Erro de validação | Texto em vermelho abaixo do campo, depois que ele é tocado ou que "Entrar" é acionado: "Campo obrigatório." em Usuário; "Senha obrigatória" ou "A sua senha deve ter mais de 8 caracteres." em Senha |
| Erro de servidor | Mensagem "Erro" com o detalhe enviado pelo cadastro corporativo; sem detalhe, "Serviço indisponível." |
| Sucesso | Sem mensagem: o sistema abre o ponto de chegada do perfil. Com senha provisória, abre a tela Alterar senha |
| Empty state | Não se aplica — a tela não lista dados |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Quem informa usuário e senha corretos chega ao ponto de chegada do seu perfil sem passo intermediário, com o menu desse perfil | Regras 3 e 4 · cenários do caminho feliz |
| SC-02 | Nenhuma tela interna é exibida a quem não tem sessão aberta | Cenário "Abrir tela interna sem sessão aberta" |
| SC-03 | Quem está com senha provisória não chega a nenhuma tela interna antes de definir a nova senha | Regra 5 · cenário "Entrar com senha provisória" |
| SC-04 | Usuário ou senha recusados mantêm a pessoa na tela de acesso, com o motivo informado | Cenário "Usuário ou senha que o cadastro corporativo não reconhece" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Autenticar Usuário | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade Usuario

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Tela de acesso: campos, destino por perfil e desvio para a troca de senha | sistema_mesa_checkin_frontend | `src/app/auth/login/login.component.ts` (linhas 48–100) e `.html` (linhas 1–34) | — |
| Chamada da autenticação e guarda da sessão no navegador | sistema_mesa_checkin_frontend | `src/app/service/core/auth.service.ts` (linhas 33–61 e 104–124) | — |
| Validação de Usuário e de Senha | sistema_mesa_checkin_frontend | `src/app/shared/basic-validators.ts` (linhas 120–131 e 180–188) | — |
| Exigência de sessão nas telas internas e redirecionamento da raiz | sistema_mesa_checkin_frontend | `src/app/service/core/auth-guard.service.ts` (linhas 11–18) e `src/app/app-routing.module.ts` (linhas 6–25) | — |
| Operação `GET /administracao/eventos/evento-principal` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoController.java` (linhas 227–235) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

A autenticação em si não é do servidor do GPE: a tela chama direto o serviço corporativo de autenticação, no endereço recebido em `urlAutenticacaoSistemaV2`. A troca obrigatória de senha é reconhecida pela resposta de status `302` desse serviço (`login.component.ts`, linhas 91–93). Sem evento principal, a operação do servidor responde `200` com corpo vazio, e a tela falha ao ler o identificador (`login.component.ts`, linhas 69–75).

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE001 – Efetuar Login (funcionalidade "Efetuar Login") e do código |

---

*Feature Set: Autenticação · Major Feature Set: Acesso e Usuários · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
