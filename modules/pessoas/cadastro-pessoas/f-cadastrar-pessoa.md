<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: PES-CAD-02
feature_set: PES-CAD
dominio: PES
entidade: Pessoa
data_model_ref: data-models/pessoas.md#pessoa
endpoints: []
error_codes: []
depende_de: ["PES-CAD-01"]
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

# Cadastrar Pessoa
> **Nível 3** - Feature Set: Cadastro de Pessoas — Major Feature Set: Pessoas - `PES-CAD-02`

## Descrição

Permite que o Administrador inclua uma pessoa no cadastro, com seus dados pessoais, de contato e da organização que representa; a pessoa incluída passa a ser encontrada pela pesquisa de pessoas e fica disponível para os eventos.

Parte-se do botão Adicionar, na tela Pessoas. O usuário preenche as abas Cadastro, Contatos e Perfil Corporativo — são obrigatórios o Nome, a Razão Social e o Cargo — e aciona Criar.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE003 – Manter Pessoa v1.0, de 03/10/2025 (documento legado), funcionalidade "Incluir Pessoa" ⚠️ sem chave na ferramenta de demandas | Criação | — Incluir uma nova pessoa com dados pessoais, contatos e perfil corporativo, a partir da opção "Adicionar" da pesquisa de pessoas. A origem do cadastro, a data de criação e o mínimo de 3 caracteres do nome não estão no documento: vêm do código 💻 |

---

<div class="dev-only">

## Superfície

**Tela própria** — rota `/administracao-pessoa`

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e as imagens "Incluir / Editar Pessoa" de GPE003, que mostram o formulário já no modo de edição

---

</div>

## Regras de negócio

1. A pessoa tem, obrigatoriamente, Nome, Razão Social e Cargo; os demais dados são facultativos. ⚠️ A obrigatoriedade é conferida só na interface: o servidor aceita a inclusão sem esses dados 💻.
2. O Nome tem no mínimo 3 e no máximo 255 caracteres. 💻 O mínimo de 3 não consta em GPE003, que informa só o tamanho máximo 📄.
3. CPF, CNPJ e e-mail são guardados como foram informados: os dígitos verificadores do CPF e do CNPJ e o formato do e-mail não são conferidos. 💻 ⚠️
4. Nenhuma unicidade é conferida: o cadastro aceita duas pessoas com o mesmo CPF, o mesmo CRM ou o mesmo e-mail. 💻 ⚠️ Duas pessoas com o mesmo CRM fazem falhar as cargas de planilha, que reconhecem a pessoa por esse código 🔍.
5. A pessoa incluída por esta feature tem a origem de cadastro Cadastro. 💻 → ver [N1 Pessoas](../README.md): Regras transversais de negócio: 4
6. A foto é facultativa e única por pessoa: uma imagem PNG ou JPG de até 200 MB. 💻 ⚠️ Formato e tamanho são conferidos só na interface; GPE003 diz apenas que a foto é uma imagem 📄.
7. Grupos de trabalho, temas e histórico de participação não são informados na inclusão. 💻 → ver [N1 Pessoas](../README.md): Regras transversais de negócio: 2

---

## Cenários

```gherkin
Feature: Cadastrar pessoa

  Background:
    Given que o usuário está autenticado no GPE
    And abriu a tela "Cadastrar Pessoa" pelo botão "Adicionar" da tela "Pessoas"

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Cadastrar pessoa só com os dados obrigatórios
    When o usuário preenche "Nome" com "Maria Souza", na aba "Cadastro"
    And preenche "Razão Social" com "Indústria Exemplo S.A." e "Cargo" com "Diretora", na aba "Perfil Corporativo"
    And aciona "Criar"
    Then o sistema inclui a pessoa, com a origem de cadastro Cadastro e a data de criação
    And exibe: "Sucesso" com o detalhe "Pessoa criada com sucesso"
    And permanece na mesma tela, com os dados preenchidos
    # ⚠️ 💻 a mensagem fica na tela até ser fechada, e a tela não volta para a lista de pessoas

  Scenario: Cadastrar pessoa com foto
    Given que o usuário preencheu "Nome", "Razão Social" e "Cargo"
    When o usuário aciona "Adicionar" no campo "Foto" e escolhe uma imagem PNG
    Then o campo "Foto" passa a mostrar o nome da imagem escolhida
    When o usuário aciona "Criar"
    Then o sistema inclui a pessoa e guarda a foto
    And exibe: "Sucesso" com o detalhe "Pessoa criada com sucesso"
    # 💻 ao escolher a imagem, o código emite o aviso "Foto adicionada"; ⚠️ 🔍 é provável que ele não apareça nesta tela

  Scenario: Desistir do cadastro
    When o usuário aciona "Cancelar"
    Then o sistema volta à tela "Pessoas" sem incluir nenhuma pessoa

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Dado obrigatório não preenchido
    When o usuário deixa "Nome", "Razão Social" ou "Cargo" vazio
    Then o botão "Criar" permanece desabilitado
    And, no campo vazio por onde o usuário já passou, o sistema exibe abaixo dele: "Este campo é obrigatório"
    # ← MESSAGE-DICTIONARY: BASELINE

  Scenario: Nome com menos de 3 caracteres
    When o usuário preenche "Nome" com "Jo"
    Then o botão "Criar" permanece desabilitado
    And o sistema exibe abaixo do campo: "Mínimo de 3 caracteres"
    # ← MESSAGE-DICTIONARY: BASELINE

  Scenario: Texto no limite do campo
    When o usuário digita 100 caracteres em "Codinome"
    Then o campo deixa de aceitar novos caracteres
    And o contador sob o campo mostra "100/100"

  Scenario: CPF, CNPJ e e-mail não são conferidos
    When o usuário informa um CPF com dígitos verificadores errados, ou um e-mail sem "@"
    And aciona "Criar"
    Then o sistema inclui a pessoa com os valores informados
    # ⚠️ 💻 não há conferência de CPF, de CNPJ nem de formato de e-mail

  Scenario: Foto em formato não aceito
    When o usuário escolhe para "Foto" um arquivo que não é PNG nem JPG
    Then o sistema recusa o arquivo e exibe, no próprio campo, o nome do arquivo seguido de ": Tipo de imagem não permitido" e o detalhe "Tipos permitidos: .png,.jpg,.jpeg"

  Scenario: Foto acima do tamanho aceito
    When o usuário escolhe para "Foto" uma imagem com mais de 200 MB
    Then o sistema recusa a imagem e exibe, no próprio campo: "A imagem selecionada excede o tamanho máximo permitido", com o detalhe que começa por "O tamanho máximo da imagem permitido é"

  Scenario: Envio com o formulário inválido
    Given que o formulário tem dado obrigatório faltando
    When o envio é disparado sem passar pelo botão "Criar"
    Then o sistema destaca os campos inválidos
    And exibe: "Formulário inválido" com o detalhe "Preencha todos os campos obrigatórios corretamente"
    # 🔍 como o botão "Criar" fica desabilitado, não se sabe se este caminho é alcançável na prática

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Pessoa com CPF, CRM ou e-mail já cadastrados
    Given que já existe uma pessoa com o CRM "100200"
    When o usuário cadastra outra pessoa com o CRM "100200"
    Then o sistema inclui a segunda pessoa, sem aviso
    # ⚠️ 💻 nenhuma unicidade é conferida; CRM repetido compromete as cargas de planilha 🔍

  Scenario: Acionar "Criar" outra vez na mesma tela
    Given que a pessoa "Maria Souza" acabou de ser incluída e a tela continua aberta com os dados dela
    When o usuário aciona "Criar" de novo
    Then o sistema inclui uma segunda pessoa com os mesmos dados
    # ⚠️ 🔍 suspeita de defeito: depois de incluir, a tela não passa ao modo de edição nem é limpa — a confirmar em execução

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Cadastrar Pessoa" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Administração › Pessoas, e o botão "Adicionar" não fica ao alcance dele
    # ⚠️ a tela não confere o perfil; ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Falha ao incluir
    Given que a inclusão falha no servidor
    When o usuário aciona "Criar"
    Then o sistema mantém os dados na tela, sem incluir a pessoa
    And exibe: "Erro" com o detalhe "Erro ao salvar pessoa. Verifique os dados e tente novamente."

  Scenario: Abas de consulta durante a inclusão
    When o usuário abre a aba "Relacionamento" ou a aba "Histórico"
    Then o sistema mostra "Nenhum tema vinculado", "Nenhum grupo de trabalho vinculado" e "Nenhum histórico de participação importado"
    # 💻 esses dados só entram por carga de planilha, depois que a pessoa existe
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| Nome | Pessoa | entrada do usuário | editável | texto | sim | De 3 a 255 caracteres 💻 — o mínimo não consta em GPE003 📄 |
| Codinome | Pessoa | entrada do usuário | editável | texto | não | Até 100 caracteres 💻 ⚠️ GPE003 informa 255 📄 |
| CRM | Pessoa | entrada do usuário | editável | texto | não | Até 50 caracteres; aceita letras e números 💻 ⚠️ GPE003 o descreve como campo numérico 📄. É o `Cód. Contato` da pessoa no CRM |
| Sexo | dado de código | entrada do usuário | editável | lista de opções | não | Masculino, Feminino ou Não informado |
| Estado | dado de código | entrada do usuário | editável | lista de opções | não | UF da pessoa: as 27 UF, exibidas pela sigla |
| CPF | Pessoa | entrada do usuário | editável | texto | não | Máscara 999.999.999-99; são guardados os 11 dígitos. Os dígitos verificadores não são conferidos 💻 ⚠️ |
| Foto | Arquivo | entrada do usuário | editável | arquivo | não | Imagem PNG, JPG ou JPEG de até 200 MB 💻 |
| E-mail | Pessoa | entrada do usuário | editável | texto | não | Até 255 caracteres; o formato não é conferido 💻 ⚠️ |
| Telefone Principal | Pessoa | entrada do usuário | editável | texto | não | Máscara (99) 99999-9999; são guardados os 11 dígitos, DDD e número. Se um telefone fixo de 10 dígitos pode ser informado, nenhuma fonte responde ❓ |
| Celular | Pessoa | entrada do usuário | editável | texto | não | Máscara (99) 99999-9999; são guardados os 11 dígitos, DDD e número |
| Razão Social | Pessoa | entrada do usuário | editável | texto | sim | Até 255 caracteres |
| Nome Fantasia | Pessoa | entrada do usuário | editável | texto | não | Até 255 caracteres |
| Cargo | Pessoa | entrada do usuário | editável | texto | sim | Até 100 caracteres |
| Cargo do Cartão | Pessoa | entrada do usuário | editável | texto | não | Até 100 caracteres |
| CNPJ | Pessoa | entrada do usuário | editável | texto | não | Máscara 99.999.999/9999-99; são guardados os 14 dígitos 💻 ⚠️ GPE003 informa tamanho 12 📄. Os dígitos verificadores não são conferidos 💻 ⚠️ |
| Estado (Perfil Corporativo) | dado de código | entrada do usuário | editável | lista de opções | não | UF da organização: as 27 UF, exibidas pela sigla. Na tela o rótulo é só "Estado" |

*Os campos estão na ordem das abas: de Nome a Foto, na aba "Cadastro"; E-mail, Telefone Principal e Celular, na aba "Contatos"; de Razão Social a Estado, na aba "Perfil Corporativo".*

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| Origem do cadastro | Cadastro | Na inclusão |
| Data de Criação | Data e hora da inclusão | Na inclusão |

---

## Comportamento de tela

### Onde fica
Tela "Cadastrar Pessoa", aberta pelo botão "Adicionar" da tela "Pessoas" (Pesquisar Pessoas `PES-CAD-01`). O formulário é o mesmo de Editar Pessoa `PES-CAD-03` e se organiza em abas: "Cadastro", "Contatos", "Perfil Corporativo", "Relacionamento" e "Histórico". Só as três primeiras recebem dados; "Relacionamento" e "Histórico" são de consulta e, na inclusão, aparecem com os textos de vazio.

Os campos obrigatórios trazem um asterisco ao lado do rótulo, e o rodapé informa "Campos com * são obrigatórios". O Nome fica na aba "Cadastro"; a Razão Social e o Cargo, na aba "Perfil Corporativo". ⚠️ O botão "Criar" fica desabilitado enquanto faltar um deles, e a tela não indica em que aba está o que falta: a mensagem sob o campo só aparece depois que o usuário passa por ele 💻.

Sob cada campo de texto com limite há um contador no formato "23/255", que muda de cor acima de 80% e de novo acima de 95% do limite. O campo não aceita digitação além do limite.

O campo "Foto" tem o botão "Adicionar" e a área "Clique em adicionar ou arraste e solte a foto aqui...". Escolhida a imagem, a área mostra um botão com o nome do arquivo, com a dica "Download", que baixa a imagem, e um ícone de lixeira, com a dica "Excluir", que a retira. O código emite os avisos "Foto adicionada", ao escolher, "Anexo removido", ao retirar, e "Falha ao ler o arquivo.", quando a imagem não pode ser lida 💻 ⚠️ 🔍 — pela forma como a tela foi montada, é provável que esses três avisos não apareçam: eles saem por um canal de mensagens diferente do que a tela exibe. A confirmar em execução.

No rodapé ficam os botões "Cancelar", que volta à tela "Pessoas" sem gravar, e "Criar". Depois de incluir, a tela não volta para a lista nem passa ao modo de edição: continua como "Cadastrar Pessoa", com os dados preenchidos e o botão "Criar" habilitado 💻 ⚠️.

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | O botão "Criar" mostra o indicador de carregamento enquanto a inclusão é processada |
| Erro de validação | Sob o campo, depois que o usuário passa por ele: "Este campo é obrigatório" ou "Mínimo de 3 caracteres". O botão "Criar" fica desabilitado enquanto houver dado obrigatório faltando ou inválido |
| Erro de servidor | Mensagem "Erro" com o detalhe "Erro ao salvar pessoa. Verifique os dados e tente novamente."; os dados continuam na tela |
| Sucesso | Mensagem "Sucesso" com o detalhe "Pessoa criada com sucesso", que fica na tela até ser fechada; a tela permanece aberta com os dados |
| Empty state | Formulário em branco; as abas "Relacionamento" e "Histórico" mostram "Nenhum tema vinculado", "Nenhum grupo de trabalho vinculado" e "Nenhum histórico de participação importado" |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Uma pessoa incluída com Nome, Razão Social e Cargo é encontrada em seguida pela pesquisa de pessoas | Cenário "Cadastrar pessoa só com os dados obrigatórios" |
| SC-02 | Pela tela, nenhuma pessoa é incluída sem Nome de pelo menos 3 caracteres, Razão Social e Cargo | Regras 1 e 2 · cenários "Dado obrigatório não preenchido" e "Nome com menos de 3 caracteres" |
| SC-03 | Toda pessoa incluída por esta feature tem a origem de cadastro Cadastro e a data de criação preenchida | Regra 5 · Campos automáticos |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Cadastrar Pessoa | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade Pessoa

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Formulário, validações e salvamento | sistema_mesa_checkin_frontend | `src/app/admin/administracao/acessibilidade/pessoas/pages/pessoa/pessoa.component.ts` (linhas 104–162 e 210–255) e `.html` (linhas 6–8 e 81–106) | — |
| Abas Cadastro, Contatos e Perfil Corporativo | sistema_mesa_checkin_frontend | `src/app/admin/administracao/acessibilidade/pessoas/pages/pessoa/components/cadastro/pessoa-cadastro.component.html` (linhas 8–176), `contato/pessoa-contato.component.html` (linhas 8–69) e `empresa/pessoa-empresa.component.html` (linhas 8–138) | — |
| Mensagens de validação e contador de caracteres | sistema_mesa_checkin_frontend | `src/app/shared/cadastro-helper.ts` (linhas 4–38) | — |
| Operação `POST /administracao/pessoas` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/PessoaController.java` (linhas 80–84) | — |
| Inclusão, origem do cadastro e data de criação | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/PessoaServiceImpl.java` (linhas 130–146) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

A tela `PessoaComponent` declara um `MessageService` próprio, e é ele que o `p-toast` da tela exibe; os avisos da foto saem pelo `AlertaService`, que usa o `MessageService` da raiz da aplicação (`pessoa.component.ts`, linha 35; `pessoa-cadastro.component.ts`, linhas 98, 100 e 129) — daí a suspeita de que não apareçam. Depois do `POST`, o identificador devolvido não é posto no formulário (`pessoa.component.ts`, linhas 229–241), o que explica a segunda inclusão ao acionar "Criar" outra vez.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE003 – Manter Pessoa (funcionalidade "Incluir Pessoa") e do código |

---

*Feature Set: Cadastro de Pessoas · Major Feature Set: Pessoas · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
