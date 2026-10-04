<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: ACE-USU-01
feature_set: ACE-USU
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

# Pesquisar Usuários
> **Nível 3** - Feature Set: Usuários — Major Feature Set: Acesso e Usuários - `ACE-USU-01`

## Descrição

Permite que o Administrador localize os usuários do sistema por entidade, perfil, nome ou login e veja, de cada um, o login, o e-mail, o perfil, a situação e quem o cadastrou e o alterou por último.

Chega-se pela opção de menu Administração › Usuários. A tela abre já com todos os usuários listados; para restringir a lista, informam-se os filtros e aciona-se "Pesquisar". É da lista que partem a inclusão, a edição e a exclusão de usuário.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE002 – Manter Usuário v1.0, de 03/10/2025 (documento legado), funcionalidade "Pesquisar Usuários" ⚠️ sem chave na ferramenta de demandas | Criação | — Pesquisar os usuários cadastrados por um ou vários filtros e, a partir do resultado, gerir cada usuário. A listagem completa ao abrir a tela e o filtro "Departamento Regional" não estão no documento: vêm do código 💻. Pelo título, relaciona-se aos tickets do Jira `PDTIC25148-1` (Cadastro de Usuário) e `PDTIC25148-23` (Cadastro de usuários - Ajustes), ambos concluídos 🔍; o conteúdo deles não foi consultado e a AIM não foi aberta |

---

<div class="dev-only">

## Superfície

**Tela própria** — rota `/administracao-usuarios`

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Pesquisar Usuário" de GPE002

---

</div>

## Regras de negócio

1. A pesquisa traz os usuários cadastrados neste sistema, e não todos os do cadastro corporativo da CNI. 🔍 A consulta é feita ao cadastro corporativo; o recorte por sistema é o que o nome da operação consultada indica.
2. Os dados exibidos são os que o cadastro corporativo guarda. → ver [N1 Acesso e Usuários](../README.md): Regras transversais de negócio: 1
3. Nenhum critério de pesquisa é obrigatório. Sem critério algum, a pesquisa traz todos os usuários do sistema. 💻
4. Os critérios podem ser combinados, e o resultado atende a todos os informados. 🔍 GPE002 diz que a pesquisa aceita uma ou várias opções ao mesmo tempo 📄; quem aplica a combinação é o cadastro corporativo.
5. Nome e login são pesquisados por parte do texto. 📄 O GPE repassa o texto digitado; como a correspondência é feita, só o cadastro corporativo decide ❓.
6. A pesquisa por perfil admite somente os perfis atribuíveis no sistema. → ver [N1 Acesso e Usuários](../README.md): Regras transversais de negócio: 3
7. Sem critério de perfil, a pesquisa traz também o usuário que tenha outro perfil do sistema, se houver. 🔍
8. A pesquisa não distingue usuário ativo de inativo: a situação é exibida, mas não é critério. 💻 ❓ Se o cadastro corporativo devolve os inativos, o código do GPE não mostra.

---

## Cenários

```gherkin
Feature: Pesquisar usuários

  Background:
    Given que o usuário está autenticado no GPE
    And abriu a tela "Usuários" pelo menu Administração › Usuários

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Ver todos os usuários ao abrir a tela
    When a tela "Usuários" é aberta
    Then o sistema lista todos os usuários do sistema, sem que nenhum filtro seja informado
    And mostra 10 usuários por página

  Scenario: Pesquisar por parte do nome
    Given que existe a usuária "Maria Souza"
    When o usuário informa "Maria" no filtro "Nome"
    And aciona "Pesquisar"
    Then o sistema lista os usuários cujo nome contém "Maria"
    And volta à primeira página da lista
    # 📄 a busca por parte do texto é o que GPE002 descreve; quem a executa é o cadastro corporativo

  Scenario: Pesquisar por perfil
    When o usuário escolhe "Secretaria Mesa" no filtro "Perfil"
    And aciona "Pesquisar"
    Then o sistema lista somente os usuários com o perfil "Secretaria Mesa"
    # 💻 além de enviar o perfil na consulta, a tela descarta do resultado quem tiver outro perfil

  Scenario: Combinar filtros
    When o usuário escolhe uma "Entidade", escolhe um "Perfil" e informa parte do "Login"
    And aciona "Pesquisar"
    Then o sistema lista somente os usuários que atendem aos três filtros informados

  Scenario: Limpar os filtros
    Given que a lista está restrita por algum filtro
    When o usuário aciona "Limpar"
    Then o sistema esvazia os filtros
    And lista de novo todos os usuários do sistema

  Scenario: Ordenar a lista
    When o usuário clica no título da coluna "Nome", "Login" ou "Email"
    Then o sistema ordena a lista por essa coluna, em ordem crescente
    And um segundo clique inverte a ordem

  Scenario: Percorrer as páginas
    Given que a pesquisa trouxe mais de 10 usuários
    When o usuário avança no paginador
    Then o sistema mostra os 10 usuários seguintes, sem refazer a consulta

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há dado a validar
    When o usuário aciona "Pesquisar" com qualquer combinação de filtros, inclusive nenhum
    Then o sistema executa a pesquisa: nenhum filtro é obrigatório nem tem formato conferido

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Não há conflito possível
    When o usuário pesquisa
    Then o sistema apenas consulta os usuários, sem alterar nenhum dado

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Pesquisar Usuários" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Administração › Usuários, e a tela não fica ao alcance dele
    # ⚠️ a tela não confere o perfil; ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Nenhum usuário encontrado
    Given que nenhum usuário atende aos filtros informados
    When o usuário aciona "Pesquisar"
    Then o sistema exibe, no lugar da lista: "Nenhum usuário encontrado."
    And não mostra o cabeçalho das colunas

  Scenario: Filtro de departamento regional sem opções
    When o usuário escolhe uma "Entidade"
    Then o filtro "Departamento Regional" aparece, sem nenhuma opção a escolher
    # ⚠️ suspeita de defeito 💻: a lista de departamentos nunca é carregada, e o valor do filtro não entra na consulta

  Scenario: Falha na consulta
    Given que a consulta ao cadastro corporativo falha
    When a tela é aberta ou o usuário aciona "Pesquisar"
    Then o sistema mantém a lista como estava
    # ⚠️ 🔍 a mensagem prevista é "Erro Interno", com o detalhe enviado pelo cadastro corporativo, ou um texto genérico como "Serviço indisponível."; a tela não tem onde exibi-la, e a falha tende a passar sem aviso
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| Entidade | externo: Cadastro corporativo da CNI | entrada do usuário | editável | lista de opções | não | Entidades do sistema no cadastro corporativo; a escolha pode ser desfeita. GPE002 dá como valor válido "Confederação Nacional da Indústria" 📄 |
| Departamento Regional | externo: Cadastro corporativo da CNI | entrada do usuário | editável | lista de opções | não | Só aparece depois de escolhida uma entidade. ⚠️ A lista nunca é carregada e o valor não entra na pesquisa 💻; o filtro não consta em GPE002 |
| Perfil | PerfilAcesso | entrada do usuário | editável | seleção → PerfilAcesso | não | Oferece somente Administrador, Secretaria Mesa e Secretaria Check-In 💻; a escolha pode ser desfeita |
| Nome | Usuario | entrada do usuário | editável | texto | não | Parte do nome do usuário 📄; sem limite de tamanho na tela 💻 |
| Login | Usuario | entrada do usuário | editável | texto | não | Parte do login do usuário 📄; sem limite de tamanho na tela 💻 |

*Todos os campos desta tabela são filtros da pesquisa. As listas de "Entidade" e de "Perfil" mostram "Selecione" enquanto nada é escolhido.*

---

## Colunas do resultado

| Coluna (Label PO) | Origem | Ordenação |
|---|---|---|
| Nome | cadastro | ordenável |
| Login | cadastro | ordenável |
| Email | cadastro | ordenável |
| Perfil | entidade relacionada — nome do perfil do usuário no sistema | — |
| Situação | cadastro — exibida como "Ativo" ou "Inativo" | — |
| Responsável Cadastrado | cadastro — nome de quem incluiu o usuário. ⚠️ GPE002 chama a coluna de "Responsável Cadastro" 📄; na tela o título é "Responsável Cadastrado" 💻 | — |
| Data Cadastro | cadastro — data da inclusão, sem a hora | — |
| Responsável Atualização | cadastro — nome de quem alterou o usuário por último | — |
| Data Atualização | cadastro — data da última alteração, sem a hora | — |

*A tela não define ordem inicial: a lista vem na ordem em que o cadastro corporativo a devolve ❓. Antes das colunas de dados, cada linha traz os ícones de edição e de exclusão.*

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| — | — | Nenhum campo é gravado: a pesquisa só consulta |

---

## Comportamento de tela

### Onde fica
Tela "Usuários", aberta pela opção de menu Administração › Usuários. Em cima ficam os filtros "Entidade", "Perfil", "Nome" e "Login" e os botões "Pesquisar", "Limpar" e "Adicionar"; embaixo, a tabela "Lista de Usuários".

A lista é carregada ao abrir a tela, sem filtro 💻. "Pesquisar" refaz a consulta com os filtros preenchidos e volta à primeira página; "Limpar" esvazia os filtros e lista tudo de novo; "Adicionar" leva a Cadastrar Usuário `ACE-USU-02`.

A tabela mostra 10 usuários por página, e o paginador, na parte de baixo, só aparece quando há mais de 10 💻. As colunas "Nome", "Login" e "Email" ordenam a lista a cada clique no título, alternando entre crescente e decrescente; ordenação e paginação operam sobre o resultado já recebido, sem nova consulta 💻. No início de cada linha ficam o ícone de lápis, com a dica "Editar Usuário", que leva a Editar Usuário `ACE-USU-03`, e o ícone de lixeira, com a dica "Remover Usuário", que aciona Excluir Usuário `ACE-USU-04`.

⚠️ O filtro "Departamento Regional" não aparece ao abrir a tela: surge depois da primeira escolha de "Entidade" e fica sempre sem opções, com o texto "Nenhum resultado encontrado", porque a lista de departamentos nunca é carregada; além disso, o valor dele não é enviado na consulta 💻. Parece defeito ou sobra de outro sistema, não intenção: o filtro não consta em GPE002.

⚠️ A tela não tem quadro de mensagens. As mensagens emitidas nela ou destinadas a ela — os erros de consulta e as mensagens de sucesso de Cadastrar Usuário `ACE-USU-02`, Editar Usuário `ACE-USU-03` e Excluir Usuário `ACE-USU-04` — não têm onde aparecer 🔍. A conclusão vem da leitura do código, sem execução.

🔍 Dois comportamentos a confirmar na tela em uso: acionar "Pesquisar" duas vezes seguidas, sem mudar nenhum filtro, não refaz a consulta; e as dicas dos ícones de lápis e de lixeira podem não aparecer, porque o recurso de dica não está ligado nesta lista.

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Sem indicador de carregamento 💻: a lista aparece quando a consulta retorna |
| Erro de validação | Não se aplica — nenhum filtro é obrigatório nem tem formato conferido |
| Erro de servidor | Previsto: erro "Erro Interno" com o detalhe enviado pelo cadastro corporativo ou, na falta dele, um texto genérico conforme a falha, como "Serviço indisponível.". ⚠️ 🔍 A tela não tem onde exibir a mensagem; a lista fica como estava |
| Sucesso | Lista atualizada, na primeira página; sem mensagem |
| Empty state | "Nenhum usuário encontrado.", no lugar das linhas; o cabeçalho das colunas não é exibido |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Ao abrir a tela, o Administrador vê todos os usuários do sistema sem informar nenhum filtro | Regra 3 · cenário "Ver todos os usuários ao abrir a tela" |
| SC-02 | Uma pesquisa por perfil traz somente usuários daquele perfil | Cenário "Pesquisar por perfil" |
| SC-03 | Cada usuário listado mostra nome, login, e-mail, perfil, situação e os responsáveis e as datas de cadastro e de atualização | Seção "Colunas do resultado" |
| SC-04 | Uma pesquisa sem resultado informa "Nenhum usuário encontrado." | Cenário "Nenhum usuário encontrado" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Pesquisar Usuários | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade Usuario

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Tela Usuários (filtro + lista) | sistema_mesa_checkin_frontend | `src/app/admin/administracao/acessibilidade/usuarios/pages/usuarios/usuarios.component.html` (linhas 1–11) | — |
| Filtros e botões "Pesquisar", "Limpar" e "Adicionar" | sistema_mesa_checkin_frontend | `src/app/admin/administracao/acessibilidade/usuarios/pages/usuarios/components/usuarios-filter/usuarios-filter.component.html` (linhas 3–108) e `.ts` (linhas 57–155) | — |
| Lista, colunas, paginação e ordenação | sistema_mesa_checkin_frontend | `src/app/admin/administracao/acessibilidade/usuarios/pages/usuarios/components/usuarios-list/usuarios-list.component.html` (linhas 7–86) e `.ts` (linhas 63–90 e 158–170) | — |
| Consulta de usuários no serviço corporativo (`GET urlPesquisaUsuariosSistema`) | sistema_mesa_checkin_frontend | `src/app/admin/administracao/acessibilidade/usuarios/services/usuario-acesso.service.ts` (linhas 14–27) | — |
| Endereços dos serviços corporativos (`GET /servicos/corporativo`) — única participação do servidor do GPE | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/corporativo/controller/RecursosController.java` (linhas 24–28) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

O servidor do GPE não implementa usuários: a tela chama direto o serviço corporativo, com os parâmetros `entidade`, `departamento`, `unidade`, `perfil`, `area`, `nome` e `login`. O controle do filtro chama-se `departamentoRegional`, mas o serviço lê `departamento`, que vai sempre vazio; `unidade` e `area` não têm campo na tela. A lista de perfis é filtrada na tela pelos ids `SMC.1`, `SMC.2` e `SMC.5`. A tela não contém `<p-toast>`, e as mensagens saem pelo `AlertaService`, ligado ao `MessageService` da raiz.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE002 – Manter Usuário (funcionalidade "Pesquisar Usuários") e do código |

---

*Feature Set: Usuários · Major Feature Set: Acesso e Usuários · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
