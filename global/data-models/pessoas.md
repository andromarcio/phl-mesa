<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
# Data Model: Pessoas
> **Modelo de entidades (negocial)** — só a parte das entidades, **sem camada física** (sem nomes físicos, tipos de banco, chaves, índices ou contagem ALI/AIE). Cole apenas este fragmento nas sessões que envolvam o domínio Pessoas.

> Levantado por engenharia reversa em 2026-09-30. 📄 = consta no documento legado GPE003 · 💻 = consta no código · 🔍 = inferido · ⚠️ = divergência ou ponto de atenção. Sem marcador = documento e código concordam.

---

## Pessoa
> Quem pode participar de um evento: a pessoa convidada, com seus dados pessoais, de contato e da organização que representa.

| Atributo (Label PO) | Tipo | Obrigatório | Notas |
|---|---|---|---|
| CRM | texto (até 50) | não | É o `Cód. Contato` da pessoa no CRM da CNI — a chave pela qual as cargas e a importação de inscritos reconhecem a pessoa. ⚠️ O sistema não impede duas pessoas com o mesmo código; quando isso acontece, as cargas de planilha tendem a falhar 🔍; a importação de inscritos do CRM não falha — usa o registro mais antigo 💻. O documento legado o descreve como numérico; a tela aceita texto 💻 |
| Nome | texto (3 a 255) | sim | Nome completo |
| Codinome | texto (até 100) | não | Nome de tratamento, usado no crachá. ⚠️ GPE003 informa 255 📄; a tela limita a 100 💻 |
| Sexo | lista (Masculino, Feminino, Não informado) | não | Nas cargas, qualquer valor diferente de `Masculino` e `Feminino` vira Não informado 💻 |
| Estado | lista (as 27 UF) | não | UF da pessoa |
| CPF | texto (11 dígitos) | não | ⚠️ A tela aplica a máscara e não confere os dígitos verificadores 💻. ⚠️ As cargas de convidados e de confirmados sobrescrevem o CPF da pessoa já cadastrada com o CNPJ da planilha, ou o apagam quando a planilha não traz CNPJ — defeito 💻 |
| Foto | seleção → Arquivo | não | Imagem PNG ou JPG |
| E-mail | texto (até 255) | não | ⚠️ O formato não é conferido 💻 |
| Telefone Principal | texto (11 dígitos) | não | DDD + número. ⚠️ A máscara é a de celular, com 11 dígitos; nenhuma fonte diz como se informa um telefone fixo, de 10 💻 |
| Celular | texto (11 dígitos) | não | DDD + número |
| Razão Social | texto (até 255) | sim | Organização que a pessoa representa. ⚠️ Na lista de participantes, a coluna Organização mostra o Nome Fantasia e, só na falta dele, a Razão Social — os dois chegam trocados do servidor 💻 |
| Nome Fantasia | texto (até 255) | não | Um dos campos que as regras de legenda avaliam |
| Cargo | texto (até 100) | sim | Um dos campos que as regras de legenda avaliam |
| Cargo do Cartão | texto (até 100) | não | Cargo como deve sair impresso no cartão de mesa 🔍 |
| CNPJ | texto (14 dígitos) | não | ⚠️ GPE003 informa tamanho 12 📄; a tela usa a máscara de 14 dígitos 💻. Os dígitos verificadores não são conferidos |
| Estado da organização | lista (as 27 UF) | não | Rótulo `Estado` na aba Perfil Corporativo |
| Origem do cadastro | lista (Cadastro, Carga, Recepção) | automático | Cadastro = incluída pela tela de pessoas · Carga = criada por planilha ou pela importação do CRM · Recepção = incluída na recepção do evento 💻. Não aparece em tela nenhuma |
| Data de Criação | data e hora | automático | Momento da inclusão |
| Data de Alteração | data e hora | automático | Momento da última alteração, pela tela, por carga ou pelo CRM |

---

## GrupoTrabalhoPessoa
> Participação da pessoa em um grupo de trabalho, com o papel que ela desempenha nele. Só entra no sistema por carga de planilha.

| Atributo (Label PO) | Tipo | Obrigatório | Notas |
|---|---|---|---|
| Pessoa | seleção → Pessoa | sim | Reconhecida pelo `Cód. Contato` da planilha |
| Grupo de Trabalho | texto | sim | Coluna `Grupos Temáticos` da planilha. ⚠️ A coluna é exigida, mas a carga aceita a célula em branco 💻. Um dos campos que as regras de legenda avaliam |
| Papel Desempenhado | texto (até 100) | sim | Papel da pessoa no grupo. Um dos campos que as regras de legenda avaliam |
| Data de Vínculo | data e hora | automático | Momento da carga 💻 |

---

## TemaPessoa
> Tema de interesse ao qual a pessoa está vinculada. Só entra no sistema por carga de planilha.

| Atributo (Label PO) | Tipo | Obrigatório | Notas |
|---|---|---|---|
| Pessoa | seleção → Pessoa | sim | Reconhecida pelo `Cód. Contato` da planilha |
| Tema | texto | sim | Um dos campos que as regras de legenda avaliam. ⚠️ A coluna é exigida, mas a carga aceita a célula em branco 💻 |
| Data de Vínculo | data e hora | automático | Momento da carga 💻 |

---

## HistoricoPessoa
> Quantas vezes a pessoa participou de eventos em um ano. Só entra no sistema por carga de planilha.

| Atributo (Label PO) | Tipo | Obrigatório | Notas |
|---|---|---|---|
| Pessoa | seleção → Pessoa | sim | Reconhecida pelo `Cód. Contato` da planilha |
| Ano | número | sim | Cada coluna da planilha, além do código, é um ano 💻; a carga aceita qualquer cabeçalho numérico, sem conferir se tem 4 dígitos. ⚠️ GPE003 descreve uma coluna única `Ano participação` 📄 |
| Participações | número inteiro maior que zero | sim | Quantidade de participações naquele ano. A soma de todos os anos é o número que acompanha o nome da pessoa no mapa de assentos |

---

## Arquivo
> Imagem guardada pelo sistema: a foto da pessoa e a imagem anexada ao evento.

| Atributo (Label PO) | Tipo | Obrigatório | Notas |
|---|---|---|---|
| Nome do arquivo | texto (até 255) | sim | Como veio do computador de quem enviou |
| Tipo do arquivo | texto | sim | Formato informado no envio (por exemplo, imagem PNG) |
| Tamanho | número | sim | Em bytes |
| Conteúdo | arquivo | sim | Guardado junto dos demais dados do sistema 💻. ⚠️ O arquivo substituído ou removido não é apagado |

---

## Relacionamentos

- **Pessoa** [1 — N] **GrupoTrabalhoPessoa** — uma pessoa participa de vários grupos de trabalho, cada um com seu papel
- **Pessoa** [1 — N] **TemaPessoa** — uma pessoa se vincula a vários temas
- **Pessoa** [1 — N] **HistoricoPessoa** — uma linha por ano em que a pessoa participou de eventos
- **Pessoa** [N — 1] **Arquivo** — a foto da pessoa, quando há
- **Pessoa** [1 — N] **EventoPessoa** — cada participação da pessoa em um evento → ver data-models/eventos.md

---

## Changelog

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Fragmento criado | Engenharia reversa do documento legado GPE003 – Manter Pessoa e do código (entidades, estrutura do banco e telas de pessoa) |
