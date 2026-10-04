<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: ACE-USU-02
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

# Cadastrar Usuário
> **Nível 3** - Feature Set: Usuários — Major Feature Set: Acesso e Usuários - `ACE-USU-02`

## Descrição

Permite que o Administrador inclua um usuário no sistema a partir do login validado, informando os dados dele e o perfil de acesso; o usuário passa a constar na lista de usuários, com a situação Ativo.

Chega-se pelo botão "Adicionar" da tela Usuários. Informa-se o login e aciona-se "Validar Login"; aceito o login, o sistema abre o formulário — já preenchido e bloqueado quando o usuário é interno da CNI —, escolhe-se o perfil e conclui-se em "Cadastrar Usuário".

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE002 – Manter Usuário v1.0, de 03/10/2025 (documento legado), funcionalidade "Incluir Usuário" ⚠️ sem chave na ferramenta de demandas | Criação | — Incluir um usuário depois de validado o login: login do diretório corporativo para o usuário interno, endereço de e-mail para o externo. O envio da senha provisória após o cadastro, previsto no documento 📄, não é disparado nem confirmado pelo código do GPE: cabe ao cadastro corporativo ⚠️. As conferências de CPF e de e-mail e o bloqueio dos dados do usuário interno não estão no documento: vêm do código 💻. Pelo título, relaciona-se aos tickets do Jira `PDTIC25148-1` (Cadastro de Usuário) e `PDTIC25148-23` (Cadastro de usuários - Ajustes), ambos concluídos 🔍; o conteúdo deles não foi consultado e a AIM não foi aberta |

---

<div class="dev-only">

## Superfície

**Tela própria** — são **duas** rotas, uma para cada momento do cadastro:

- Informar o login — `/administracao-usuario`
- Dados do usuário, depois de "Validar Login" — `/administracao-usuario/:login`, com o parâmetro de consulta `novoUsuario`

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Incluir / Editar Usuário" de GPE002

---

</div>

## Regras de negócio

1. A inclusão só prossegue depois de validado o login informado.
2. O login que não existe no diretório corporativo só é aceito se tiver formato de e-mail. 💻 → ver [N1 Acesso e Usuários](../README.md): Regras transversais de negócio: 7
3. O login que já pertence a um usuário deste sistema não é incluído de novo. 💻
4. Os dados do usuário interno — nome, CPF, telefone, celular, e-mail e cargo — vêm do diretório corporativo e não são alterados na inclusão. 💻
5. Nome, CPF, e-mail e perfil são obrigatórios; telefone e celular são opcionais. ⚠️ GPE002 dá o cargo como obrigatório 📄; o sistema não o exige 💻.
6. Para o usuário interno, só o perfil é exigido: os dados vindos do diretório corporativo são aceitos como estão, sem conferência de preenchimento nem de validade. 💻
7. O CPF informado tem dígitos verificadores válidos, e o e-mail informado tem formato válido. 💻
8. Todo usuário é incluído com exatamente um perfil. → ver [N1 Acesso e Usuários](../README.md): Regras transversais de negócio: 2
9. O perfil é um dos atribuíveis no sistema. → ver [N1 Acesso e Usuários](../README.md): Regras transversais de negócio: 3
10. As instituições relacionadas ao usuário dependem do tipo do perfil: perfil do tipo Departamento Nacional pede a entidade; do tipo Departamento Regional, a entidade e o departamento regional; do tipo Unidade, também a unidade. 💻 Os perfis atribuíveis hoje são todos do tipo Departamento Nacional. ⚠️ GPE002 traz apenas o campo Entidade 📄.
11. A instituição relacionada é opcional: a inclusão se conclui sem nenhuma. ❓ Se o cadastro corporativo a exige, o código do GPE não mostra.
12. O usuário é incluído com a situação Ativo. 💻
13. Depois de incluído, o usuário recebe por e-mail uma senha provisória para o primeiro acesso. 📄 ⚠️ O envio cabe ao cadastro corporativo: o código do GPE não o dispara nem confirma que ocorreu.
14. O usuário é gravado no cadastro corporativo da CNI. → ver [N1 Acesso e Usuários](../README.md): Regras transversais de negócio: 1

---

## Cenários

```gherkin
Feature: Cadastrar usuário

  Background:
    Given que o usuário está autenticado no GPE
    And abriu a tela "Cadastrar Usuário" pelo botão "Adicionar" da tela "Usuários"

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Cadastrar usuário interno
    Given que o login "joao.silva" existe no diretório corporativo e ainda não está cadastrado no sistema
    When o usuário informa "joao.silva" em "Login" e aciona "Validar Login"
    Then o sistema abre o formulário com "Nome", "CPF", "Telefone", "Celular", "Email" e "Cargo" preenchidos pelo diretório corporativo e bloqueados
    And exibe o aviso "Usuário não cadastrado no sistema." com o detalhe "O usuário informado não foi encontrado no sistema."
    When o usuário escolhe "Secretaria Mesa" em "Perfil" e aciona "Cadastrar Usuário"
    Then o sistema inclui o usuário com a situação Ativo
    And volta à tela "Usuários"
    # ⚠️ 🔍 a mensagem de sucesso prevista é "Usuário Criado com Sucesso"; a tela "Usuários" não tem onde exibi-la

  Scenario: Cadastrar usuário externo
    Given que o login "maria.souza@empresa.com.br" não existe no cadastro corporativo
    When o usuário informa "maria.souza@empresa.com.br" em "Login" e aciona "Validar Login"
    Then o sistema abre o formulário em branco, com todos os campos liberados
    When o usuário preenche "Nome", "CPF" e "Email", escolhe o "Perfil" e aciona "Cadastrar Usuário"
    Then o sistema inclui o usuário com a situação Ativo
    And volta à tela "Usuários"
    # 📄 GPE002 diz que o novo usuário recebe uma senha provisória por e-mail; ⚠️ o código do GPE não dispara nem confirma esse envio

  Scenario: Informar a instituição relacionada
    Given que o formulário está aberto e um perfil foi escolhido
    When o usuário escolhe uma "Entidade" no painel "Instituições Relacionadas" e aciona "Adicionar Instituição"
    Then a entidade passa a constar na tabela "Instituições Selecionadas"
    And deixa de ser oferecida na lista "Entidade"
    # ⚠️ 💻 para os perfis oferecidos, adicionar uma segunda entidade substitui a primeira na tabela

  Scenario: Recomeçar com outro login
    Given que o formulário está aberto para um login validado
    When o usuário aciona "Limpar"
    Then o sistema descarta o que foi preenchido e volta a pedir o login

  Scenario: Desistir do cadastro
    When o usuário aciona "Cancelar"
    Then o sistema volta à tela "Usuários" sem incluir nenhum usuário

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Login não informado
    When o campo "Login" está vazio
    Then o botão "Validar Login" fica desabilitado

  Scenario: Login que não está no diretório nem é e-mail
    Given que o login "joao.inexistente" não existe no diretório corporativo
    When o usuário informa "joao.inexistente" em "Login" e aciona "Validar Login"
    Then o sistema não abre o formulário
    And exibe o aviso: "Para usuários internos, o login deve existir no Active Directory. Para usuários externos, o login deve ser um e-mail válido."

  Scenario: Campo obrigatório vazio
    Given que o formulário está aberto para um usuário externo
    When o usuário deixa "Nome", "CPF", "Email" ou "Perfil" sem preencher e aciona "Cadastrar Usuário"
    Then o sistema não inclui o usuário
    And exibe o erro "Formulário inválido" com o detalhe "Preencha todos os campos obrigatórios corretamente"
    And exibe abaixo de cada campo vazio: "Campo obrigatório."
    # ← MESSAGE-DICTIONARY: BASELINE

  Scenario: CPF inválido
    Given que o formulário está aberto para um usuário externo
    When o usuário informa em "CPF" um número cujos dígitos verificadores não conferem
    Then o sistema exibe abaixo do campo: "CPF inválido"
    # ⚠️ 🔍 quando o erro está no primeiro dígito verificador, o texto exibido tende a ser "Campo obrigatório." em vez de "CPF inválido"
    # ⚠️ 💻 CPF de dígitos todos iguais só é recusado quando é "000.000.000-00"; os demais, como "111.111.111-11", são aceitos

  Scenario: E-mail em formato inválido
    Given que o formulário está aberto para um usuário externo
    When o usuário informa "maria.souza@empresa" em "Email"
    Then o sistema exibe abaixo do campo: "Email inválido"

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Login já cadastrado no sistema
    Given que o login "joao.silva" já pertence a um usuário do sistema
    When o usuário informa "joao.silva" em "Login" e aciona "Validar Login"
    Then o sistema não abre o formulário
    And exibe o erro "Usuário já cadastrado no sistema." com o detalhe "O usuário informado já estas no sistema."
    # ⚠️ o detalhe traz "já estas" — erro de digitação na mensagem 💻

  Scenario: Inclusão recusada pelo cadastro corporativo
    Given que o cadastro corporativo recusa a inclusão
    When o usuário aciona "Cadastrar Usuário"
    Then o sistema mantém o formulário aberto, sem incluir o usuário
    # ❓ que conflitos o cadastro corporativo recusa — CPF ou e-mail já usados por outro usuário, por exemplo — o código do GPE não mostra
    # ⚠️ 🔍 a mensagem prevista é "Erro Interno" com o detalhe devolvido pelo cadastro corporativo; ela sai por um canal que o quadro de mensagens deste formulário não escuta e tende a não aparecer

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Cadastrar Usuário" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Administração › Usuários, e o botão "Adicionar" não fica ao alcance dele
    # ⚠️ a tela não confere o perfil; ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Usuário externo que já consta no cadastro corporativo
    Given que o login "maria.souza@empresa.com.br" existe no cadastro corporativo, não é de usuário interno e não está cadastrado no sistema
    When o usuário informa esse login e aciona "Validar Login"
    Then o sistema abre o formulário com os dados que o cadastro corporativo já tem, liberados para alteração
    And exibe o aviso "Usuário não cadastrado no sistema." com o detalhe "O usuário informado não foi encontrado no sistema."
    # 🔍 caminho deduzido do código: o bloqueio dos dados só vale para usuário interno

  Scenario: Falha ao validar o login
    Given que a consulta ao cadastro corporativo falha por motivo diferente de login não encontrado
    When o usuário aciona "Validar Login"
    Then o sistema não abre o formulário
    And exibe o erro "Erro" com o detalhe enviado pelo cadastro corporativo ou, na falta dele, "Serviço indisponível."

  Scenario: Falha ao conferir se o usuário já está no sistema
    Given que o login existe no cadastro corporativo
    And a consulta que confere se ele já está cadastrado no sistema falha
    When o usuário aciona "Validar Login"
    Then o sistema trata o login como ainda não cadastrado e abre o formulário
    And exibe o aviso "Usuário não cadastrado no sistema." com o detalhe "O usuário informado não foi encontrado no sistema."
    # ⚠️ 💻 qualquer falha nessa consulta, inclusive indisponibilidade, é lida como "não cadastrado"
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| Login | Usuario | entrada do usuário | imutável depois de validado | texto | sim | Validado por "Validar Login" antes dos demais campos; se não existe no diretório corporativo, tem de ser um e-mail. GPE002 fixa 255 caracteres 📄; a tela não limita o tamanho 💻 ⚠️ |
| Nome | Usuario | entrada do usuário; para usuário interno, externo: diretório corporativo da CNI | editável; somente leitura para usuário interno | texto | sim | GPE002 fixa 255 caracteres 📄; a tela não limita o tamanho 💻 ⚠️ |
| CPF | Usuario | entrada do usuário; para usuário interno, externo: diretório corporativo da CNI | editável; somente leitura para usuário interno | texto | sim | → ver FIELD-DICTIONARY: CPF |
| Telefone | Usuario | entrada do usuário; para usuário interno, externo: diretório corporativo da CNI | editável; somente leitura para usuário interno | texto | não | DDD de 2 dígitos e número de 8 dígitos, em duas caixas, com as máscaras (99) e 9999-9999; sem outra conferência 💻. ⚠️ GPE002 dá 11 posições 📄; a tela aceita 10 dígitos |
| Celular | Usuario | entrada do usuário; para usuário interno, externo: diretório corporativo da CNI | editável; somente leitura para usuário interno | texto | não | DDD de 2 dígitos e número de 9 dígitos, em duas caixas, com as máscaras (99) e 99999-9999; sem outra conferência 💻 |
| Email | Usuario | entrada do usuário; para usuário interno, externo: diretório corporativo da CNI | editável; somente leitura para usuário interno | texto | sim | → ver FIELD-DICTIONARY: E-mail. GPE002 fixa 256 caracteres 📄; a tela não limita o tamanho 💻 ⚠️ |
| Cargo | Usuario | entrada do usuário; para usuário interno, externo: diretório corporativo da CNI | editável; somente leitura para usuário interno | texto | não | ⚠️ GPE002 dá o campo como obrigatório, com 256 caracteres 📄; a tela não o exige nem limita o tamanho 💻 |
| Perfil | PerfilAcesso | entrada do usuário | editável | seleção → PerfilAcesso | sim | Oferece somente Administrador, Secretaria Mesa e Secretaria Check-In 💻 |
| Entidade | externo: Cadastro corporativo da CNI | entrada do usuário | editável | lista de opções | não | Fica no painel "Instituições Relacionadas", que aparece quando o perfil escolhido tem tipo. ⚠️ É o campo "Entidade" de GPE002 📄, que na tela virou esse painel 💻. Exigida apenas para acionar "Adicionar Instituição"; o cadastro se conclui sem instituição |
| Departamento Regional | externo: Cadastro corporativo da CNI | entrada do usuário | editável | lista de opções | não | Só para perfil do tipo Departamento Regional ou Unidade, o que nenhum dos perfis oferecidos é 💻; não consta em GPE002 |
| Unidade | externo: Cadastro corporativo da CNI | entrada do usuário | editável | lista de opções | não | Só para perfil do tipo Unidade; aceita mais de uma. ⚠️ A lista de unidades nunca é carregada, de modo que o campo não chega a aparecer 💻; não consta em GPE002 |

*Usuário interno é aquele cujo login foi encontrado no diretório corporativo. Para ele, "Nome", "CPF", "Telefone", "Celular", "Email" e "Cargo" chegam preenchidos e bloqueados, e só "Perfil" e as instituições relacionadas ficam por informar.*

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| Situação | Ativo | Na inclusão 💻 |
| Usuário interno | Sim, quando o login é encontrado no diretório corporativo; não, nos demais casos | Na validação do login — quem informa é o cadastro corporativo 💻 |
| Responsável Cadastro | Usuário que fez a inclusão | Na inclusão — preenchido pelo cadastro corporativo 🔍 |
| Data Cadastro | Data da inclusão | Na inclusão — preenchida pelo cadastro corporativo 🔍 |

*Junto com os dados, o formulário envia ao cadastro corporativo dois indicadores fixos, sem campo na tela: "recebe e-mail", sempre sim, e "envia pré-cadastro", sempre não 💻. O efeito deles no cadastro corporativo — inclusive sobre o envio da senha provisória — o código do GPE não mostra ❓.*

---

## Comportamento de tela

### Onde fica
Tela "Cadastrar Usuário", aberta pelo botão "Adicionar" da tela Usuários. No topo ficam os botões "Cadastrar Usuário" e "Cancelar"; abaixo, o campo "Login" com o botão "Validar Login". Enquanto o login não é validado, só isso aparece: "Cadastrar Usuário" fica desabilitado, e "Validar Login" só se habilita com o login preenchido.

Validado o login, o campo "Login" é bloqueado, "Validar Login" dá lugar a "Limpar" e surgem os painéis "Dados do Usuário", com "Nome", "CPF", "Telefone", "Celular", "Email" e "Cargo", e "Perfil de acesso ao sistema", com "Perfil". Os campos obrigatórios levam asterisco: "Nome", "CPF", "Email" e "Perfil". ⚠️ Na imagem de GPE002, "Cargo" também tem asterisco 📄; na tela atual não tem 💻.

Escolhido o perfil, aparece o painel "Instituições Relacionadas": a lista "Entidade", o botão "Adicionar Instituição" e a tabela "Instituições Selecionadas", com um ícone de lixeira por linha e o texto "Nenhuma instituição selecionada." quando vazia. Para os perfis oferecidos, o painel pede só a entidade. ⚠️ Adicionar uma segunda entidade substitui a primeira na tabela, em vez de somar 💻 — parece defeito, não intenção.

"Limpar" descarta o preenchimento e volta a pedir o login; "Cancelar" volta à tela Usuários sem incluir.

⚠️ O formulário tem quadro de mensagens próprio, que mostra os avisos da validação do login e o erro "Formulário inválido". Já a mensagem de sucesso e os erros devolvidos na gravação saem por outro canal, que esse quadro não escuta, e a tela Usuários, para onde o sistema vai depois de incluir, não tem quadro de mensagens: essas mensagens tendem a não aparecer 🔍. A conclusão vem da leitura do código, sem execução.

🔍 A confirmar na tela em uso: depois de um login recusado por já estar cadastrado, validar outro login sem sair da tela pode abrir o formulário ainda com os dados e o bloqueio do login anterior, porque o formulário não é esvaziado entre uma validação e outra.

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Sem indicador de carregamento 💻: o formulário aparece quando as consultas do login retornam |
| Erro de validação | "Campo obrigatório.", "CPF inválido" ou "Email inválido" abaixo do campo, depois de o campo ser tocado ou de se tentar concluir; ao concluir com erro, também o erro "Formulário inválido" com o detalhe "Preencha todos os campos obrigatórios corretamente" |
| Erro de servidor | Na validação do login: erro "Erro" com o detalhe enviado pelo cadastro corporativo ou, na falta dele, "Serviço indisponível.". Na gravação: previsto o erro "Erro Interno" com o detalhe devolvido pelo cadastro corporativo ⚠️ 🔍 — tende a não aparecer; o formulário fica aberto |
| Sucesso | Volta à tela Usuários. Previsto: "Usuário Criado com Sucesso" ⚠️ 🔍 — a tela de destino não tem onde exibi-lo |
| Empty state | Antes da validação do login, só o campo "Login" e os botões; na tabela "Instituições Selecionadas", "Nenhuma instituição selecionada." |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Um usuário incluído é encontrado pela pesquisa de usuários com o perfil escolhido e a situação Ativo | Regras 8 e 12 · cenários "Cadastrar usuário interno" e "Cadastrar usuário externo" |
| SC-02 | Nenhum usuário é incluído sem que o login tenha sido validado | Regra 1 · cenário "Login que não está no diretório nem é e-mail" |
| SC-03 | Um login já cadastrado no sistema não dá origem a um segundo usuário | Regra 3 · cenário "Login já cadastrado no sistema" |
| SC-04 | Nenhum usuário externo é incluído sem nome, CPF válido, e-mail válido e perfil | Regras 5 e 7 · cenários de erro de validação |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Cadastrar Usuário | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade Usuario

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Formulário, validação do login e gravação | sistema_mesa_checkin_frontend | `src/app/admin/administracao/acessibilidade/usuarios/pages/usuario/usuario.component.ts` (linhas 84–137, 163–217, 257–268 e 293–328) e `.html` (linhas 10–58 e 59–220) | — |
| Painel "Instituições Relacionadas" | sistema_mesa_checkin_frontend | `src/app/admin/administracao/acessibilidade/usuarios/pages/usuario/instituicoes-relacionadas/instituicoes-relacionadas.component.ts` (linhas 96–145 e 254–284) e `.html` (linhas 2–136) | — |
| Consulta por login (`GET urlPesquisaUsuarioLogin`) e consulta no sistema (`GET urlPesquisaUsuarioSistemaCodigoUsuario`) | sistema_mesa_checkin_frontend | `src/app/admin/administracao/acessibilidade/usuarios/services/usuario.service.ts` (linhas 15–31) | — |
| Inclusão no serviço corporativo (`POST urlNovoUsuarioSistema`) | sistema_mesa_checkin_frontend | `src/app/shared/http-crud.service.ts` (linhas 37–40) | — |
| Conferência de CPF e de e-mail e mensagem de campo | sistema_mesa_checkin_frontend | `src/app/shared/basic-validators.ts` (linhas 110–118 e 180–251) e `src/app/shared/form-component-base.ts` (linhas 61–77) | — |
| Endereços dos serviços corporativos (`GET /servicos/corporativo`) — única participação do servidor do GPE | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/corporativo/controller/RecursosController.java` (linhas 24–28) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

O servidor do GPE não implementa usuários: a tela chama direto o serviço corporativo. O bloqueio dos dados depende do indicador `interno` da resposta da consulta por login. Controles enviados sem campo na tela: `ativo` (`true`), `recebeEmail` (`true`), `enviaPreCadastro` (`false`), `areas` e `linhas` (vazios), `dataInicioVigenciaAcesso` e `dataFimVigenciaAcesso`. Os perfis são filtrados na tela pelos ids `SMC.1`, `SMC.2` e `SMC.5`. O `<p-toast />` do formulário usa o `MessageService` declarado no próprio componente; `handleErrorAlert` e a mensagem de sucesso saem pelo `AlertaService`, ligado ao `MessageService` da raiz. O validador de CPF devolve a chave `invalidCPF` para erro no primeiro dígito verificador, e `getErrors` só lê a chave `invalid`.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE002 – Manter Usuário (funcionalidade "Incluir Usuário") e do código |

---

*Feature Set: Usuários · Major Feature Set: Acesso e Usuários · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
