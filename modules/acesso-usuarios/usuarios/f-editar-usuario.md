<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: ACE-USU-03
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

# Editar Usuário
> **Nível 3** - Feature Set: Usuários — Major Feature Set: Acesso e Usuários - `ACE-USU-03`

## Descrição

Permite que o Administrador altere os dados e o perfil de acesso de um usuário já cadastrado, sem mudar o login; as alterações passam a valer no cadastro do usuário e aparecem na lista de usuários.

A edição é aberta pelo ícone de lápis de cada linha da lista de usuários. O formulário vem preenchido, com o login bloqueado; quando o usuário é interno da CNI, só o perfil e as instituições relacionadas podem ser alterados. Conclui-se em "Atualizar Usuário".

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE002 – Manter Usuário v1.0, de 03/10/2025 (documento legado), funcionalidade "Editar Usuário" ⚠️ sem chave na ferramenta de demandas | Criação | — Editar os dados de um usuário a partir da pesquisa, com exceção do login. O documento diz que todos os demais dados podem ser editados 📄; o código bloqueia os dados do usuário interno, que vêm do diretório corporativo 💻 ⚠️. Pelo título, relaciona-se aos tickets do Jira `PDTIC25148-1` (Cadastro de Usuário) e `PDTIC25148-23` (Cadastro de usuários - Ajustes), ambos concluídos 🔍; o conteúdo deles não foi consultado e a AIM não foi aberta |

---

<div class="dev-only">

## Superfície

**Tela própria** — rota `/administracao-usuario/:login`

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Incluir / Editar Usuário" de GPE002

---

</div>

## Regras de negócio

1. O login do usuário não muda na edição. → ver [N1 Acesso e Usuários](../README.md): Regras transversais de negócio: 6
2. Os dados do usuário interno — nome, CPF, telefone, celular, e-mail e cargo — não são alterados pelo GPE: pertencem ao diretório corporativo. 💻 ⚠️ GPE002 diz que, na edição, "todos os dados podem ser editados, com exceção do login" 📄.
3. Do usuário externo, todos os dados podem ser alterados, menos o login — inclusive o e-mail, que deixa então de coincidir com o login. 💻
4. Nome, CPF, e-mail e perfil continuam obrigatórios, e o CPF e o e-mail alterados passam pelas mesmas conferências da inclusão. 💻 ⚠️ GPE002 dá o cargo como obrigatório 📄; o sistema não o exige 💻.
5. O usuário continua com exatamente um perfil. → ver [N1 Acesso e Usuários](../README.md): Regras transversais de negócio: 2
6. O perfil gravado é um dos atribuíveis no sistema: o usuário que tem outro perfil só tem a alteração concluída depois de receber um deles. 💻 → ver [N1 Acesso e Usuários](../README.md): Regras transversais de negócio: 3
7. A edição não altera a situação do usuário. 💻
8. Trocar o perfil por outro de tipo diferente descarta as instituições relacionadas já escolhidas. 💻 Os perfis atribuíveis hoje têm todos o mesmo tipo, de modo que a troca entre eles as mantém.
9. As alterações são gravadas no cadastro corporativo da CNI. → ver [N1 Acesso e Usuários](../README.md): Regras transversais de negócio: 1

---

## Cenários

```gherkin
Feature: Editar usuário

  Background:
    Given que o usuário está autenticado no GPE
    And está na lista de usuários

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Editar os dados de um usuário externo
    Given que "Maria Souza" é usuária externa, cadastrada no sistema
    When o usuário aciona "Editar Usuário" na linha de "Maria Souza"
    Then o sistema abre a tela "Atualizar Usuário" com os dados dela preenchidos e o campo "Login" bloqueado
    When o usuário altera "Celular" e "Cargo" e aciona "Atualizar Usuário"
    Then o sistema grava as alterações
    And volta à tela "Usuários"
    # ⚠️ 🔍 a mensagem de sucesso prevista é "Usuário Atualizado com Sucesso"; a tela "Usuários" não tem onde exibi-la

  Scenario: Trocar o perfil de um usuário interno
    Given que "João Silva" é usuário interno, cadastrado no sistema com o perfil "Secretaria Mesa"
    When o usuário aciona "Editar Usuário" na linha de "João Silva"
    Then o sistema abre a tela "Atualizar Usuário" com "Nome", "CPF", "Telefone", "Celular", "Email" e "Cargo" bloqueados
    And deixa liberados o "Perfil" e as instituições relacionadas
    When o usuário escolhe "Secretaria Check-In" em "Perfil" e aciona "Atualizar Usuário"
    Then o sistema grava o novo perfil
    And volta à tela "Usuários"
    # ⚠️ GPE002 diz que todos os dados podem ser editados, com exceção do login 📄; para o usuário interno, o código só libera o perfil e as instituições 💻

  Scenario: Trocar a instituição relacionada
    Given que a tela "Atualizar Usuário" está aberta e a tabela "Instituições Selecionadas" traz a entidade do usuário
    When o usuário retira a entidade pelo ícone de lixeira, escolhe outra em "Entidade" e aciona "Adicionar Instituição"
    And aciona "Atualizar Usuário"
    Then o sistema grava o usuário com a nova entidade

  Scenario: Desistir da edição
    Given que a tela "Atualizar Usuário" está aberta
    When o usuário aciona "Cancelar"
    Then o sistema volta à tela "Usuários" sem gravar nenhuma alteração

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Campo obrigatório apagado
    Given que a tela "Atualizar Usuário" está aberta para um usuário externo
    When o usuário apaga "Nome", "CPF", "Email" ou "Perfil" e aciona "Atualizar Usuário"
    Then o sistema não grava as alterações
    And exibe o erro "Formulário inválido" com o detalhe "Preencha todos os campos obrigatórios corretamente"
    And exibe abaixo de cada campo vazio: "Campo obrigatório."
    # ← MESSAGE-DICTIONARY: BASELINE

  Scenario: CPF inválido
    Given que a tela "Atualizar Usuário" está aberta para um usuário externo
    When o usuário troca o "CPF" por um número cujos dígitos verificadores não conferem
    Then o sistema exibe abaixo do campo: "CPF inválido"
    # ⚠️ 🔍 quando o erro está no primeiro dígito verificador, o texto exibido tende a ser "Campo obrigatório." em vez de "CPF inválido"

  Scenario: E-mail em formato inválido
    Given que a tela "Atualizar Usuário" está aberta para um usuário externo
    When o usuário troca o "Email" por "maria.souza@empresa"
    Then o sistema exibe abaixo do campo: "Email inválido"

  Scenario: Usuário com perfil que a tela não oferece
    Given que o usuário editado tem um perfil do sistema diferente de Administrador, Secretaria Mesa e Secretaria Check-In
    When o usuário aciona "Atualizar Usuário" sem escolher outro perfil
    Then o sistema não grava as alterações
    And esvazia o campo "Perfil" e exibe abaixo dele: "Campo obrigatório."
    # 💻 nesse caso não há a mensagem "Formulário inválido": só o campo é marcado

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Alteração recusada pelo cadastro corporativo
    Given que o cadastro corporativo recusa a alteração
    When o usuário aciona "Atualizar Usuário"
    Then o sistema mantém a tela "Atualizar Usuário" aberta, sem gravar
    # ❓ que conflitos o cadastro corporativo recusa — CPF ou e-mail já usados por outro usuário, por exemplo — o código do GPE não mostra
    # ⚠️ 🔍 a mensagem prevista é "Erro Interno" com o detalhe devolvido pelo cadastro corporativo; ela sai por um canal que o quadro de mensagens deste formulário não escuta e tende a não aparecer

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Editar Usuário" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Administração › Usuários, e a ação não fica ao alcance dele
    # ⚠️ a tela não confere o perfil; ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Login que existe no cadastro corporativo, mas não no sistema
    Given que a tela de edição é aberta para um login que o cadastro corporativo conhece e que não está cadastrado no sistema
    When o sistema carrega os dados
    Then a tela se apresenta como "Cadastrar Usuário", com o formulário aberto para inclusão
    And exibe o aviso "Usuário não cadastrado no sistema." com o detalhe "O usuário informado não foi encontrado no sistema."
    # 💻 só ocorre quando a tela é aberta pelo endereço, e não pela lista; daí em diante vale Cadastrar Usuário (ACE-USU-02)
    # ⚠️ qualquer falha na consulta do usuário no sistema, inclusive indisponibilidade, cai neste mesmo caminho

  Scenario: Login que o cadastro corporativo não conhece
    Given que a tela de edição é aberta para um login que não existe no cadastro corporativo e não tem formato de e-mail
    When o sistema carrega os dados
    Then o sistema não abre o formulário
    And exibe o aviso: "Para usuários internos, o login deve existir no Active Directory. Para usuários externos, o login deve ser um e-mail válido."

  Scenario: Falha ao carregar o usuário
    Given que a consulta ao cadastro corporativo falha por motivo diferente de login não encontrado
    When o usuário aciona "Editar Usuário"
    Then o sistema não abre o formulário
    And exibe o erro "Erro" com o detalhe enviado pelo cadastro corporativo ou, na falta dele, "Serviço indisponível."
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| Login | Usuario | exibido do cadastro | imutável | texto | sim | Exibido bloqueado; identifica o usuário editado |
| Nome | Usuario | entrada do usuário, sobre o valor já cadastrado; para usuário interno, exibido do cadastro | editável para usuário externo; somente leitura para usuário interno | texto | sim | GPE002 fixa 255 caracteres 📄; a tela não limita o tamanho 💻 ⚠️ |
| CPF | Usuario | entrada do usuário, sobre o valor já cadastrado; para usuário interno, exibido do cadastro | editável para usuário externo; somente leitura para usuário interno | texto | sim | → ver FIELD-DICTIONARY: CPF |
| Telefone | Usuario | entrada do usuário, sobre o valor já cadastrado; para usuário interno, exibido do cadastro | editável para usuário externo; somente leitura para usuário interno | texto | não | DDD de 2 dígitos e número de 8 dígitos, em duas caixas, com as máscaras (99) e 9999-9999; sem outra conferência 💻 |
| Celular | Usuario | entrada do usuário, sobre o valor já cadastrado; para usuário interno, exibido do cadastro | editável para usuário externo; somente leitura para usuário interno | texto | não | DDD de 2 dígitos e número de 9 dígitos, em duas caixas, com as máscaras (99) e 99999-9999; sem outra conferência 💻 |
| Email | Usuario | entrada do usuário, sobre o valor já cadastrado; para usuário interno, exibido do cadastro | editável para usuário externo; somente leitura para usuário interno | texto | sim | → ver FIELD-DICTIONARY: E-mail. GPE002 fixa 256 caracteres 📄; a tela não limita o tamanho 💻 ⚠️ |
| Cargo | Usuario | entrada do usuário, sobre o valor já cadastrado; para usuário interno, exibido do cadastro | editável para usuário externo; somente leitura para usuário interno | texto | não | ⚠️ GPE002 dá o campo como obrigatório, com 256 caracteres 📄; a tela não o exige nem limita o tamanho 💻 |
| Perfil | PerfilAcesso | entrada do usuário, sobre o valor já cadastrado | editável | seleção → PerfilAcesso | sim | Oferece somente Administrador, Secretaria Mesa e Secretaria Check-In 💻; o perfil atual que não seja um deles tem de ser trocado para concluir |
| Entidade | externo: Cadastro corporativo da CNI | entrada do usuário | editável | lista de opções | não | Fica no painel "Instituições Relacionadas", cuja tabela já traz as instituições do usuário. Exigida apenas para acionar "Adicionar Instituição"; a edição se conclui sem instituição 💻 |
| Departamento Regional | externo: Cadastro corporativo da CNI | entrada do usuário | editável | lista de opções | não | Só para perfil do tipo Departamento Regional ou Unidade, o que nenhum dos perfis oferecidos é 💻; não consta em GPE002 |
| Unidade | externo: Cadastro corporativo da CNI | entrada do usuário | editável | lista de opções | não | Só para perfil do tipo Unidade. ⚠️ A lista de unidades nunca é carregada, de modo que o campo não chega a aparecer 💻; não consta em GPE002 |

*Usuário interno é aquele cujo login pertence ao diretório corporativo; para ele, só "Perfil" e as instituições relacionadas são editáveis. A situação do usuário não tem campo nesta tela.*

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| Responsável Atualização | Usuário que fez a alteração | Na gravação — preenchido pelo cadastro corporativo 🔍 |
| Data Atualização | Data da alteração | Na gravação — preenchida pelo cadastro corporativo 🔍 |
| Situação | A que o usuário já tinha | Na gravação — a edição a reenvia como veio, sem alterá-la 💻 |

---

## Comportamento de tela

### Onde fica
É a mesma tela do cadastro, aberta pelo ícone de lápis, com a dica "Editar Usuário", em cada linha da lista de usuários. O título e o botão de gravação passam a ser "Atualizar Usuário"; "Cancelar" volta à tela Usuários sem gravar.

O campo "Login" vem preenchido e bloqueado, sem os botões "Validar Login" e "Limpar". ⚠️ A imagem "Incluir / Editar Usuário" de GPE002 mostra o botão "Limpar" na edição e asterisco em "Cargo" 📄; a tela atual não tem nem um nem outro 💻 — a imagem parece ser de uma versão anterior 🔍.

Os painéis "Dados do Usuário" e "Perfil de acesso ao sistema" vêm preenchidos. Quando o usuário é interno, "Nome", "CPF", "Telefone", "Celular", "Email" e "Cargo" ficam bloqueados. O painel "Instituições Relacionadas" traz, na tabela "Instituições Selecionadas", as instituições que o usuário já tem; cada uma pode ser retirada pelo ícone de lixeira, e outra pode ser incluída por "Adicionar Instituição". ⚠️ Para os perfis oferecidos, adicionar uma entidade substitui a que estava na tabela, em vez de somar 💻.

⚠️ O formulário tem quadro de mensagens próprio, que mostra os avisos do carregamento e o erro "Formulário inválido". Já a mensagem de sucesso e os erros devolvidos na gravação saem por outro canal, que esse quadro não escuta, e a tela Usuários, para onde o sistema vai depois de gravar, não tem quadro de mensagens: essas mensagens tendem a não aparecer 🔍. A conclusão vem da leitura do código, sem execução.

🔍 A confirmar na tela em uso: na edição, a lista "Entidade" do painel "Instituições Relacionadas" pode ficar sem opções depois de qualquer alteração feita no formulário, voltando a ser carregada quando uma instituição é retirada da tabela.

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Sem indicador de carregamento 💻: o formulário aparece quando as consultas do usuário retornam |
| Erro de validação | "Campo obrigatório.", "CPF inválido" ou "Email inválido" abaixo do campo; ao concluir com erro, também o erro "Formulário inválido" com o detalhe "Preencha todos os campos obrigatórios corretamente" |
| Erro de servidor | No carregamento: erro "Erro" com o detalhe enviado pelo cadastro corporativo ou, na falta dele, "Serviço indisponível.". Na gravação: previsto o erro "Erro Interno" com o detalhe devolvido pelo cadastro corporativo ⚠️ 🔍 — tende a não aparecer; o formulário fica aberto |
| Sucesso | Volta à tela Usuários. Previsto: "Usuário Atualizado com Sucesso" ⚠️ 🔍 — a tela de destino não tem onde exibi-lo |
| Empty state | Na tabela "Instituições Selecionadas", "Nenhuma instituição selecionada." quando o usuário não tem instituição |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Uma alteração gravada aparece na pesquisa de usuários — por exemplo, o novo perfil na coluna "Perfil" | Cenário "Trocar o perfil de um usuário interno" |
| SC-02 | O login de um usuário é o mesmo antes e depois de qualquer edição | Regra 1 |
| SC-03 | Nome, CPF, telefone, celular, e-mail e cargo de um usuário interno não mudam por edição feita no GPE | Regra 2 |
| SC-04 | Nenhum usuário fica gravado com perfil diferente de Administrador, Secretaria Mesa ou Secretaria Check-In depois de editado | Regra 6 · cenário "Usuário com perfil que a tela não oferece" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Editar Usuário | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade Usuario

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Ícone "Editar Usuário" na lista | sistema_mesa_checkin_frontend | `src/app/admin/administracao/acessibilidade/usuarios/pages/usuarios/components/usuarios-list/usuarios-list.component.html` (linhas 48–54) | — |
| Formulário: carga, bloqueio do usuário interno e gravação | sistema_mesa_checkin_frontend | `src/app/admin/administracao/acessibilidade/usuarios/pages/usuario/usuario.component.ts` (linhas 84–116, 139–150, 163–217, 245–255 e 270–281) e `.html` (linhas 10–58 e 59–220) | — |
| Painel "Instituições Relacionadas" | sistema_mesa_checkin_frontend | `src/app/admin/administracao/acessibilidade/usuarios/pages/usuario/instituicoes-relacionadas/instituicoes-relacionadas.component.ts` (linhas 49–65, 96–145 e 254–284) | — |
| Consulta por login (`GET urlPesquisaUsuarioLogin`) e consulta no sistema (`GET urlPesquisaUsuarioSistemaCodigoUsuario`) | sistema_mesa_checkin_frontend | `src/app/admin/administracao/acessibilidade/usuarios/services/usuario.service.ts` (linhas 15–31) | — |
| Alteração no serviço corporativo (`PUT urlAtualizaUsuarioSistema`) | sistema_mesa_checkin_frontend | `src/app/shared/http-crud.service.ts` (linhas 42–45) | — |
| Endereços dos serviços corporativos (`GET /servicos/corporativo`) — única participação do servidor do GPE | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/corporativo/controller/RecursosController.java` (linhas 24–28) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

O servidor do GPE não implementa usuários: a tela chama direto o serviço corporativo. A edição é reconhecida pela ausência do parâmetro `novoUsuario` na rota e pelo retorno da consulta do usuário no sistema (`usuarioCadastrado`). O bloqueio dos dados depende do indicador `interno`; os valores bloqueados seguem na gravação, porque o corpo é montado com `getRawValue()`. O perfil fora da lista é comparado por `codigo`, enquanto a lista é filtrada pelos ids `SMC.1`, `SMC.2` e `SMC.5`. O `<p-toast />` do formulário usa o `MessageService` declarado no próprio componente; `handleErrorAlert` e a mensagem de sucesso saem pelo `AlertaService`, ligado ao `MessageService` da raiz.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE002 – Manter Usuário (funcionalidade "Editar Usuário") e do código |

---

*Feature Set: Usuários · Major Feature Set: Acesso e Usuários · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
