<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
<!--
  CONVENÇÃO DE VISIBILIDADE
  Blocos <div class="dev-only"> contêm detalhes técnicos.
  Versão PO  → CSS: .dev-only { display: none; }
  Versão DEV → sem CSS adicional
-->

# Major Feature Set: Acesso e Usuários
> **Nível 1** - Visão estratégica do domínio - `ACE`

## Descrição
Cuida de quem entra no sistema e do que cada um pode fazer. Reúne a entrada e a saída do sistema, a recuperação e a troca de senha, os dados do usuário logado e a manutenção dos usuários com seus perfis. Atende os três perfis que operam o GPE — Administrador, Secretaria Mesa e Secretaria Check-In — e, na manutenção de usuários, só o Administrador.

> Marcadores usados neste domínio: 📄 consta nos documentos legados · 💻 consta no código · 🔍 inferido · ❓ nenhuma fonte responde · ⚠️ divergência ou ponto de atenção. Sem marcador = documento e código concordam.

### O que este domínio NÃO faz
| Descrição | Pertence a |
|---|---|
| Guardar usuário, senha e perfil — isso fica no cadastro corporativo da CNI; o GPE opera sobre ele | Serviços corporativos da CNI (externo) |
| Decidir, a cada operação, se o perfil do usuário pode executá-la | Serviços corporativos da CNI (externo) |
| Cadastrar as pessoas convidadas para os eventos — usuário é quem opera o sistema, pessoa é quem participa do evento | Pessoas |
| Definir os itens de menu que cada perfil enxerga — vêm do cadastro corporativo, na resposta da autenticação 💻 | Serviços corporativos da CNI (externo) |

---

## Feature Sets

| Feature Set | Descrição | Features |
|---|---|---|
| [**Autenticação**](./autenticacao/README.md) <small>ACE-AUT</small> | Entrar e sair do sistema, recuperar e alterar a senha, consultar os próprios dados e trocar a foto de perfil — documento legado GPE001 – Efetuar Login | 6 |
| [**Usuários**](./usuarios/README.md) <small>ACE-USU</small> | Pesquisar, cadastrar, editar e excluir os usuários do sistema e seus perfis — documento legado GPE002 – Manter Usuário | 4 |

---

## Regras transversais de negócio

1. O GPE não mantém base própria de usuários: autenticação, senha, usuário e perfil são operados no cadastro corporativo da CNI. 💻
2. Todo usuário tem exatamente um perfil no sistema. 🔍
3. Os perfis atribuíveis a um usuário pela tela são Administrador, Secretaria Mesa e Secretaria Check-In. 💻 ⚠️ O cadastro corporativo do sistema tem ainda os perfis Painel e Participante, que nenhuma tela oferece.
4. Toda tela, exceto as de acesso (entrar, recuperar senha e alterar senha obrigatória), exige usuário autenticado. 💻
5. A senha tem no mínimo 8 caracteres. 💻
6. O login identifica o usuário e não muda depois da inclusão.
7. O usuário interno da CNI é reconhecido pelo login no diretório corporativo; o usuário externo usa o próprio e-mail como login.

---

## Integrações com outros domínios

### Leitura — domínios que consomem dados deste domínio
| Domínio | O que consome | Como |
|---|---|---|
| Eventos | Perfil do usuário logado — define a tela de entrada, os botões e as colunas disponíveis na lista de participantes e no mapa de assentos | Serviço |
| Pessoas | Usuário autenticado — condição para abrir as telas | Serviço |

### Escrita — domínios que criam ou alteram dados deste domínio
| Domínio | O que altera | Situação |
|---|---|---|
| — | Nenhum outro domínio altera usuários ou perfis | — |

---

<div class="dev-only">

## Entidades do domínio

| Entidade | Descrição | Campos no DATA-MODEL.md |
|---|---|---|
| Usuario | Quem acessa o sistema — mantido no cadastro corporativo, não no banco do GPE | → ver DATA-MODEL.md: Usuario |
| PerfilAcesso | Papel do usuário no sistema — mantido no cadastro corporativo | → ver DATA-MODEL.md: PerfilAcesso |

---

## Dependências externas

| Serviço | Uso | Lib sugerida |
|---|---|---|
| Serviço corporativo de autenticação da CNI | Autenticar o usuário, validar a credencial a cada operação e decidir o acesso por recurso e tipo de operação | — (integração já existente) |
| Serviço corporativo de configurações da CNI | Entregar os endereços dos demais serviços e os dados de identificação do sistema | — |
| Cadastro básico corporativo da CNI | Usuários, perfis, entidades, departamentos regionais e unidades | — |

---

## Regras de acesso consolidadas

| Role | Pode fazer |
|---|---|
| Administrador | Tudo de Autenticação e toda a manutenção de usuários |
| Secretaria Mesa | Autenticação |
| Secretaria Check-In | Autenticação |

⚠️ Na interface, a manutenção de usuários não confere o perfil: quem a esconde dos demais perfis é o menu, que só traz o item para o Administrador. Um usuário autenticado de outro perfil que digite o endereço da tela chega a ela 💻.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | N1 criado | Engenharia reversa dos documentos legados GPE001 – Efetuar Login e GPE002 – Manter Usuário e do código (telas de acesso e de usuários; cadastro do sistema no serviço corporativo) |

---

*Última revisão: —*

*Links: [Autenticação](./autenticacao/README.md) · [Usuários](./usuarios/README.md) · [INDEX geral](../INDEX.md)*
