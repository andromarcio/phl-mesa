<!-- docqui: 4.0.2 | prompt: PROMPT_AIM | atualizado: 2026-10-04 -->
---
id: PES-CAD-03
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

# Editar Pessoa
> **Nível 3** - Feature Set: Cadastro de Pessoas — Major Feature Set: Pessoas - `PES-CAD-03`

## Descrição

Permite que o Administrador altere os dados pessoais, de contato e da organização de uma pessoa já cadastrada, e consulte na mesma tela os grupos de trabalho, os temas e o histórico de participação que as cargas de planilha trouxeram para ela.

Parte-se do ícone de lápis, em cada linha da lista de pessoas. A tela abre com os dados gravados; o usuário altera o que precisar nas abas Cadastro, Contatos e Perfil Corporativo e aciona Atualizar. As abas Relacionamento e Histórico servem só para consulta.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE003 – Manter Pessoa v1.0, de 03/10/2025 (documento legado), funcionalidade "Editar Pessoa" ⚠️ sem chave na ferramenta de demandas | Criação | — Alterar os dados pessoais, os contatos e o perfil corporativo de uma pessoa, a partir da opção de edição de cada registro da pesquisa. As abas de relacionamento e de histórico aparecem nas imagens do documento, sem descrição de campos 📄. A abertura da tela pelo nome da pessoa, na lista de participantes de um evento, veio com o ticket do Jira `PDTIC25148-35`; o critério que a pede é de Pesquisar Participantes `EVT-PAR-01`, onde fica o atalho, e esta feature não entrou na [AIM do ticket](../../../analise-impacto/AIM-PDTIC25148-35.md) porque a edição da pessoa em si não mudou |

---

<div class="dev-only">

## Superfície

**Tela própria** — rota `/administracao-pessoa/:id`

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e as imagens "Incluir / Editar Pessoa" de GPE003

---

</div>

## Regras de negócio

1. Todos os dados pessoais, de contato e de perfil corporativo da pessoa podem ser alterados, inclusive o CRM. ⚠️ O CRM é o código pelo qual as cargas de planilha reconhecem a pessoa: alterá-lo muda a quem os dados das próximas cargas serão atribuídos 💻.
2. Valem na alteração as mesmas exigências da inclusão: Nome, Razão Social e Cargo obrigatórios, e Nome com 3 a 255 caracteres. ⚠️ São conferidas só na interface: o servidor aceita a alteração sem esses dados 💻.
3. CPF, CNPJ e e-mail são guardados como foram informados, sem conferência de dígitos verificadores nem de formato, e nenhuma unicidade é conferida: a alteração pode deixar duas pessoas com o mesmo CPF, o mesmo CRM ou o mesmo e-mail. 💻 ⚠️
4. A origem do cadastro e a data de criação da pessoa não mudam com a alteração. 💻
5. Grupos de trabalho, temas e histórico de participação são apenas consultados: nenhum deles é alterado por esta feature. 💻 → ver [N1 Pessoas](../README.md): Regras transversais de negócio: 2
6. A pessoa fica sem foto quando a alteração chega ao servidor sem a foto. 💻 ⚠️ Pela interface isso só acontece quando a foto é retirada de propósito, porque a referência da foto guardada segue junto a cada alteração 🔍; a regra, porém, atinge qualquer outro meio que altere a pessoa sem reenviar a foto — suspeita de defeito do servidor.
7. A foto substituída ou retirada continua guardada. 💻 ⚠️ Parece resíduo, não intenção.

---

## Cenários

```gherkin
Feature: Editar pessoa

  Background:
    Given que o usuário está autenticado no GPE
    And abriu a pessoa "Maria Souza" pelo ícone de lápis, na lista de pessoas

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Alterar dados da pessoa
    When o usuário altera "Cargo" para "Presidente", na aba "Perfil Corporativo"
    And aciona "Atualizar"
    Then o sistema grava a alteração e a data de alteração
    And exibe: "Sucesso" com o detalhe "Pessoa criada com sucesso"
    And permanece na mesma tela
    # ⚠️ 💻 a mensagem fala em criação, embora a operação seja uma alteração, e fica na tela até ser fechada

  Scenario: Alterar sem mexer na foto
    Given que "Maria Souza" tem foto
    When o usuário altera "Celular" e aciona "Atualizar"
    Then o sistema grava a alteração e mantém a foto
    # 🔍 a tela reenvia a referência da foto guardada; ver a regra 6

  Scenario: Trocar a foto
    Given que "Maria Souza" tem foto
    When o usuário aciona "Adicionar" no campo "Foto", escolhe outra imagem e aciona "Atualizar"
    Then o sistema passa a usar a nova foto, e o cabeçalho da tela a exibe
    # ⚠️ 💻 a foto anterior continua guardada

  Scenario: Retirar a foto
    Given que "Maria Souza" tem foto
    When o usuário aciona o ícone de lixeira ao lado do nome do arquivo da foto e aciona "Atualizar"
    Then a pessoa fica sem foto
    And o cabeçalho da tela passa a mostrar as iniciais "MS"

  Scenario: Consultar temas e grupos de trabalho
    Given que as cargas trouxeram para "Maria Souza" o tema "Inovação" e o grupo de trabalho "GT Indústria 4.0", com o papel "Coordenadora"
    When o usuário abre a aba "Relacionamento"
    Then o quadro "Temas" mostra "Inovação" e a "Data de Vínculo"
    And o quadro "Grupos de Trabalho" mostra "GT Indústria 4.0", "Papel Desempenhado: Coordenadora" e a "Data de Vínculo"

  Scenario: Consultar histórico de participação
    Given que a carga de histórico trouxe para "Maria Souza" 2 participações em 2024
    When o usuário abre a aba "Histórico"
    Then o quadro "Histórico de Participações" mostra "Ano: 2024" e "Participações: 2"

  Scenario: Desistir da alteração
    When o usuário altera algum campo e aciona "Cancelar"
    Then o sistema volta à tela "Pessoas" sem gravar a alteração

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Dado obrigatório apagado
    When o usuário apaga "Nome", "Razão Social" ou "Cargo"
    Then o botão "Atualizar" fica desabilitado
    And o sistema exibe abaixo do campo: "Este campo é obrigatório"
    # ← MESSAGE-DICTIONARY: BASELINE

  Scenario: Nome com menos de 3 caracteres
    When o usuário altera "Nome" para "Ma"
    Then o botão "Atualizar" fica desabilitado
    And o sistema exibe abaixo do campo: "Mínimo de 3 caracteres"
    # ← MESSAGE-DICTIONARY: BASELINE

  Scenario: CPF, CNPJ e e-mail não são conferidos
    When o usuário altera "CNPJ" para um número com dígitos verificadores errados e aciona "Atualizar"
    Then o sistema grava o valor informado
    # ⚠️ 💻 não há conferência de CPF, de CNPJ nem de formato de e-mail

  Scenario: Foto em formato não aceito
    When o usuário escolhe para "Foto" um arquivo que não é PNG nem JPG
    Then o sistema recusa o arquivo e exibe, no próprio campo, o nome do arquivo seguido de ": Tipo de imagem não permitido" e o detalhe "Tipos permitidos: .png,.jpg,.jpeg"

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Alterar para CPF, CRM ou e-mail de outra pessoa
    Given que outra pessoa tem o CRM "100200"
    When o usuário altera o "CRM" de "Maria Souza" para "100200" e aciona "Atualizar"
    Then o sistema grava a alteração, sem aviso
    # ⚠️ 💻 nenhuma unicidade é conferida; CRM repetido compromete as cargas de planilha 🔍

  Scenario: Pessoa excluída enquanto a tela estava aberta
    Given que "Maria Souza" foi excluída por outro usuário depois que a tela foi aberta
    When o usuário aciona "Atualizar"
    Then o sistema não grava nada
    And exibe: "Sucesso" com o detalhe "Pessoa criada com sucesso"
    # ⚠️ 🔍 suspeita de defeito: o servidor responde como sucesso, sem conteúdo, e a tela não distingue — a confirmar em execução

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Editar Pessoa" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Administração › Pessoas, e o ícone de lápis da lista de pessoas não fica ao alcance dele
    # ⚠️ a tela não confere o perfil; ver a nota da matriz no N2

  Scenario: Abrir a pessoa pela lista de participantes de um evento
    Given que o usuário, de qualquer perfil, vê a lista de participantes de um evento
    When o usuário aciona o nome de uma pessoa nessa lista
    Then a tela da pessoa abre em outra aba do navegador, com os mesmos campos e o botão "Atualizar"
    # ⚠️ 💻 o atalho existe para todo perfil que vê a lista, inclusive a Secretaria Check-In; ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Pessoa sem dados de carga
    Given que nenhuma carga trouxe temas, grupos de trabalho ou histórico para "Maria Souza"
    When o usuário abre as abas "Relacionamento" e "Histórico"
    Then o sistema mostra "Nenhum tema vinculado", "Nenhum grupo de trabalho vinculado" e "Nenhum histórico de participação importado"

  Scenario: Grupo de trabalho sem papel
    Given que "Maria Souza" tem um grupo de trabalho cujo papel está vazio
    When o usuário abre a aba "Relacionamento"
    Then o sistema mostra, para esse grupo, "Papel Desempenhado: Não especificado"

  Scenario: Pessoa sem foto
    Given que "Maria Souza" não tem foto
    When a tela é aberta
    Then o cabeçalho mostra as iniciais "MS" no lugar da foto

  Scenario: Falha ao gravar
    Given que a alteração falha no servidor
    When o usuário aciona "Atualizar"
    Then o sistema mantém na tela os dados digitados, sem gravar
    And exibe: "Erro" com o detalhe "Erro ao salvar pessoa. Verifique os dados e tente novamente."

  Scenario: Pessoa não encontrada ao abrir
    Given que o endereço da tela aponta para uma pessoa que não existe
    When a tela é aberta
    Then os campos ficam vazios e o botão "Atualizar" fica desabilitado
    And o sistema não informa que a pessoa não foi encontrada
    # ⚠️ 🔍 a falha ao carregar não é tratada pela tela — a confirmar em execução
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
| Foto | Arquivo | entrada do usuário | editável | arquivo | não | Imagem PNG, JPG ou JPEG de até 200 MB 💻. Pode ser mantida, trocada ou retirada |
| Data de Criação | Pessoa | exibido do cadastro | somente leitura | data e hora | — | Formato dd/mm/aaaa hh:mm; aparece só quando preenchida |
| Data de Alteração | Pessoa | exibido do cadastro | somente leitura | data e hora | — | Formato dd/mm/aaaa hh:mm; aparece só quando a pessoa já foi alterada alguma vez |
| E-mail | Pessoa | entrada do usuário | editável | texto | não | Até 255 caracteres; o formato não é conferido 💻 ⚠️ |
| Telefone Principal | Pessoa | entrada do usuário | editável | texto | não | Máscara (99) 99999-9999; são guardados os 11 dígitos, DDD e número |
| Celular | Pessoa | entrada do usuário | editável | texto | não | Máscara (99) 99999-9999; são guardados os 11 dígitos, DDD e número |
| Razão Social | Pessoa | entrada do usuário | editável | texto | sim | Até 255 caracteres |
| Nome Fantasia | Pessoa | entrada do usuário | editável | texto | não | Até 255 caracteres |
| Cargo | Pessoa | entrada do usuário | editável | texto | sim | Até 100 caracteres |
| Cargo do Cartão | Pessoa | entrada do usuário | editável | texto | não | Até 100 caracteres |
| CNPJ | Pessoa | entrada do usuário | editável | texto | não | Máscara 99.999.999/9999-99; são guardados os 14 dígitos 💻 ⚠️ GPE003 informa tamanho 12 📄. Os dígitos verificadores não são conferidos 💻 ⚠️ |
| Estado (Perfil Corporativo) | dado de código | entrada do usuário | editável | lista de opções | não | UF da organização: as 27 UF, exibidas pela sigla. Na tela o rótulo é só "Estado" |
| Temas | TemaPessoa | exibido do cadastro | somente leitura | texto | — | Nome de cada tema a que a pessoa se vincula 💻 |
| Data de Vínculo (do tema) | TemaPessoa | exibido do cadastro | somente leitura | data | — | Formato dd/mm/aaaa: a data da carga que trouxe o tema 💻. Na tela o rótulo é só "Data de Vínculo" |
| Grupos de Trabalho | GrupoTrabalhoPessoa | exibido do cadastro | somente leitura | texto | — | Nome de cada grupo de trabalho de que a pessoa participa 💻 |
| Papel Desempenhado | GrupoTrabalhoPessoa | exibido do cadastro | somente leitura | texto | — | Papel da pessoa no grupo; "Não especificado" quando está vazio 💻 |
| Data de Vínculo (do grupo de trabalho) | GrupoTrabalhoPessoa | exibido do cadastro | somente leitura | data | — | Formato dd/mm/aaaa: a data da carga que trouxe o grupo 💻. Na tela o rótulo é só "Data de Vínculo" |
| Ano | HistoricoPessoa | exibido do cadastro | somente leitura | número | — | Ano das participações 💻 |
| Participações | HistoricoPessoa | exibido do cadastro | somente leitura | número | — | Quantidade de participações da pessoa naquele ano 💻 |

*Os campos estão na ordem das abas: de Nome a Data de Alteração, na aba "Cadastro"; E-mail, Telefone Principal e Celular, na aba "Contatos"; de Razão Social a Estado, na aba "Perfil Corporativo"; de Temas a Data de Vínculo do grupo de trabalho, na aba "Relacionamento"; Ano e Participações, na aba "Histórico". GPE003 mostra as abas "Relacionamento" e "Histórico" nas imagens e não descreve os campos delas 📄. Em que ordem os temas, os grupos e os anos são listados, nenhuma fonte responde ❓.*

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| Data de Alteração | Data e hora da alteração | A cada alteração gravada |

---

## Comportamento de tela

### Onde fica
Na tela da pessoa, aberta pelo ícone de lápis de cada linha da lista de pessoas (Pesquisar Pessoas `PES-CAD-01`). O formulário é o mesmo de Cadastrar Pessoa `PES-CAD-02`. Há um segundo caminho: na lista de participantes de um evento, o nome da pessoa é um atalho, com a dica "Abrir o perfil da pessoa em nova aba", que abre esta mesma tela em outra aba do navegador 💻.

No lugar do título, a tela mostra um cabeçalho com a foto da pessoa e o nome completo. Sem foto, o cabeçalho mostra um círculo com as iniciais — a primeira letra de cada uma das duas primeiras palavras do nome, em maiúsculas. O nome e as iniciais do cabeçalho acompanham o que é digitado no campo "Nome", antes mesmo de gravar.

O formulário se organiza em abas: "Cadastro", "Contatos", "Perfil Corporativo", "Relacionamento" e "Histórico". As três primeiras têm os campos que podem ser alterados; na aba "Cadastro", abaixo dos campos, aparecem "Data de Criação" e "Data de Alteração". A aba "Relacionamento" tem os quadros "Temas" e "Grupos de Trabalho", e a aba "Histórico", o quadro "Histórico de Participações"; nenhuma das duas tem campo de entrada.

O campo "Foto" mostra, para a pessoa que tem foto, um botão com o nome do arquivo, com a dica "Download", que baixa a imagem, e um ícone de lixeira, com a dica "Excluir", que a retira; o botão "Adicionar" escolhe outra imagem. A troca e a retirada só valem depois de "Atualizar". O código emite os avisos "Foto adicionada" e "Anexo removido" 💻 ⚠️ 🔍 — pela forma como a tela foi montada, é provável que não apareçam; a confirmar em execução.

No rodapé ficam o texto "Campos com * são obrigatórios" e os botões "Cancelar", que volta à tela "Pessoas" sem gravar, e "Atualizar", desabilitado enquanto houver dado obrigatório faltando ou inválido. Depois de gravar, a tela não volta para a lista 💻 ⚠️, e a "Data de Alteração" exibida só muda quando a pessoa é aberta de novo 💻.

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Sem indicador na abertura: os campos aparecem preenchidos assim que os dados chegam. Ao gravar, o botão "Atualizar" mostra o indicador de carregamento |
| Erro de validação | Sob o campo: "Este campo é obrigatório" ou "Mínimo de 3 caracteres". O botão "Atualizar" fica desabilitado enquanto houver dado obrigatório faltando ou inválido |
| Erro de servidor | Ao gravar: mensagem "Erro" com o detalhe "Erro ao salvar pessoa. Verifique os dados e tente novamente."; os dados digitados continuam na tela. Ao abrir: nenhuma mensagem — os campos ficam vazios ⚠️ 🔍 |
| Sucesso | Mensagem "Sucesso" com o detalhe "Pessoa criada com sucesso" ⚠️ — o mesmo texto da inclusão —, que fica na tela até ser fechada; a tela permanece aberta |
| Empty state | Abas de consulta sem dados: "Nenhum tema vinculado", "Nenhum grupo de trabalho vinculado" e "Nenhum histórico de participação importado" |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Um dado alterado e gravado aparece com o novo valor quando a pessoa é aberta de novo e, se for nome, CRM, razão social, e-mail, codinome ou cargo, também na lista de pessoas | Regra 1 · cenário "Alterar dados da pessoa" |
| SC-02 | Uma alteração que não mexe na foto mantém a foto da pessoa | Regra 6 · cenário "Alterar sem mexer na foto" |
| SC-03 | Os temas, os grupos de trabalho e o histórico trazidos pelas cargas são exibidos na tela da pessoa e não mudam com a alteração | Regra 5 · cenários de consulta |
| SC-04 | Pela tela, nenhuma alteração é gravada sem Nome de pelo menos 3 caracteres, Razão Social e Cargo | Regra 2 |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Editar Pessoa | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade Pessoa

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Carga dos dados, cabeçalho e salvamento | sistema_mesa_checkin_frontend | `src/app/admin/administracao/acessibilidade/pessoas/pages/pessoa/pessoa.component.ts` (linhas 86–102 e 164–266) e `.html` (linhas 10–28 e 81–106) | — |
| Abas Relacionamento e Histórico, e datas da aba Cadastro | sistema_mesa_checkin_frontend | `src/app/admin/administracao/acessibilidade/pessoas/pages/pessoa/components/relacionamento/pessoa-relacionamento.component.html` (linhas 3–37), `historico/pessoa-historico.component.html` (linhas 3–18) e `cadastro/pessoa-cadastro.component.html` (linhas 178–187) | — |
| Atalho pelo nome, na lista de participantes | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/components/evento-pessoas-list/evento-pessoas-list.component.html` (linhas 59–71) | — |
| Operações `GET /administracao/pessoas/{id}`, `POST /administracao/pessoas` e `GET /administracao/pessoas/anexos/{id}` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/PessoaController.java` (linhas 73–84 e 112–130) | — |
| Alteração, data de alteração e regra da foto | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/PessoaServiceImpl.java` (linhas 130–146 e 161–195) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

A tela grava a alteração pela mesma operação da inclusão — `POST /administracao/pessoas`, com o identificador no corpo —, e o servidor desvia para a alteração quando o identificador vem preenchido (`PessoaServiceImpl.java`, linhas 144–145); a operação `PUT /administracao/pessoas/{id}` existe e não é usada pela tela. Quando o identificador não corresponde a nenhuma pessoa, o serviço devolve vazio e a operação responde `201` sem corpo. A foto é retirada pelo `else` das linhas 189–190, sempre que a alteração chega sem ela.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-10-04 | Claude (analise-impacto) | Origem atualizada | Origem ajustada com a abertura da AIM do ticket `PDTIC25148-35`: o critério do atalho pelo nome fica em Pesquisar Participantes `EVT-PAR-01`, e esta feature não entra na AIM; regras, campos e cenários inalterados |
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE003 – Manter Pessoa (funcionalidade "Editar Pessoa") e do código |

---

*Feature Set: Cadastro de Pessoas · Major Feature Set: Pessoas · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
