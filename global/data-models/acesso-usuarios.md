<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
# Data Model: Acesso e Usuários
> **Modelo de entidades (negocial)** — só a parte das entidades, **sem camada física** (sem nomes físicos, tipos de banco, chaves, índices ou contagem ALI/AIE). Cole apenas este fragmento nas sessões que envolvam o domínio Acesso e Usuários.

> Levantado por engenharia reversa em 2026-09-30. 📄 = consta nos documentos legados GPE001 ou GPE002 · 💻 = consta no código · 🔍 = inferido · ⚠️ = divergência ou ponto de atenção. Sem marcador = documento e código concordam.

> ⚠️ **As duas entidades deste domínio não são guardadas pelo GPE.** Usuário, senha e perfil vivem no cadastro corporativo da CNI; as telas do GPE consultam e alteram esse cadastro. O que está aqui é o que o GPE mostra e envia — a definição completa pertence ao serviço corporativo.

---

## Usuario
> Quem acessa o sistema, com o perfil que define o que pode fazer.

| Atributo (Label PO) | Tipo | Obrigatório | Notas |
|---|---|---|---|
| Login | texto | sim | Não muda depois da inclusão. Para usuário externo, é o endereço de e-mail |
| Senha | texto (mínimo de 8 caracteres) | sim | Guardada e conferida pelo cadastro corporativo; o GPE nunca a armazena. Nasce provisória, enviada por e-mail, e é trocada no primeiro acesso → ver FIELD-DICTIONARY: Senha |
| Nome | texto | sim | Preenchido pelo cadastro corporativo quando o usuário é interno 💻 |
| CPF | texto (11 dígitos) | sim | → ver FIELD-DICTIONARY: CPF |
| Telefone | texto (DDD + 8 dígitos) | não | — |
| Celular | texto (DDD + 9 dígitos) | não | — |
| Email | texto | sim | → ver FIELD-DICTIONARY: E-mail |
| Cargo | texto | não | ⚠️ GPE002 o dá como obrigatório 📄; a tela não exige 💻 |
| Perfil | seleção → PerfilAcesso | sim | A tela oferece Administrador, Secretaria Mesa e Secretaria Check-In 💻 |
| Instituições Relacionadas | lista de Entidade, Departamento Regional e Unidade | conforme o perfil | Aparece quando o perfil escolhido tem tipo; o tipo define até que nível se informa 💻. GPE002 traz só o campo Entidade 📄 |
| Situação | lista (Ativo, Inativo) | automático | Todo usuário é incluído como Ativo; não há ação de tela que o inative 💻 |
| Usuário interno | sim · não | automático | Sim quando o login existe no diretório corporativo; nesse caso os dados pessoais vêm de lá e não são editáveis 💻 |
| Responsável Cadastro | texto | automático | Quem incluiu o usuário |
| Data Cadastro | data | automático | — |
| Responsável Atualização | texto | automático | Quem alterou por último |
| Data Atualização | data | automático | — |
| Foto | imagem | não | Foto de perfil, exibida no cabeçalho |

---

## PerfilAcesso
> O papel do usuário no sistema. Lista mantida no cadastro corporativo.

| Atributo (Label PO) | Tipo | Obrigatório | Notas |
|---|---|---|---|
| Nome | texto | sim | Perfis cadastrados para o sistema: Administrador, Secretaria Mesa, Secretaria Check-In, Painel e Participante 💻. ⚠️ Os documentos legados só tratam dos três primeiros 📄, e só eles são oferecidos na tela de usuários |
| Tipo | lista (DN, DR, UA) | sim | Define quais instituições se informam para o usuário. O código só traz as siglas 💻; a leitura Departamento Nacional, Departamento Regional e Unidade é inferida 🔍. Os cinco perfis do sistema são do tipo DN 💻 |

---

## Relacionamentos

- **PerfilAcesso** [1 — N] **Usuario** — cada usuário tem um perfil no sistema

---

## Changelog

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Fragmento criado | Engenharia reversa dos documentos legados GPE001 – Efetuar Login e GPE002 – Manter Usuário e do código (telas de acesso e de usuários, cadastro do sistema no serviço corporativo) |
