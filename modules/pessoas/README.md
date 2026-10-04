<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
<!--
  CONVENÇÃO DE VISIBILIDADE
  Blocos <div class="dev-only"> contêm detalhes técnicos.
  Versão PO  → CSS: .dev-only { display: none; }
  Versão DEV → sem CSS adicional
-->

# Major Feature Set: Pessoas
> **Nível 1** - Visão estratégica do domínio - `PES`

## Descrição
Mantém as pessoas que podem ser convidadas para os eventos e o que se sabe sobre cada uma: dados pessoais, contatos, a organização que representa, os grupos de trabalho de que participa, os temas a que se vincula e quantas vezes já participou de eventos. É a base de onde os eventos tiram seus participantes e de onde as regras de legenda tiram os dados que avaliam. Atende o Administrador.

> Marcadores usados neste domínio: 📄 consta nos documentos legados · 💻 consta no código · 🔍 inferido · ❓ nenhuma fonte responde · ⚠️ divergência ou ponto de atenção. Sem marcador = documento e código concordam.

### O que este domínio NÃO faz
| Descrição | Pertence a |
|---|---|
| Vincular a pessoa a um evento, como convidada ou confirmada | Eventos |
| Cadastrar a pessoa na recepção, no dia do evento | Eventos |
| Criar e atualizar pessoas a partir das listas de convidados, de confirmados e dos inscritos do CRM — quem faz é a carga do evento, que grava neste domínio | Eventos |
| Atribuir legenda à pessoa — a legenda pertence à participação dela em um evento | Eventos |
| Editar na tela os grupos de trabalho, os temas e o histórico — só entram por carga de planilha | — (não existe) |
| Manter os usuários que operam o sistema | Acesso e Usuários |

---

## Feature Sets

| Feature Set | Descrição | Features |
|---|---|---|
| [**Cadastro de Pessoas**](./cadastro-pessoas/README.md) <small>PES-CAD</small> | Pesquisar, cadastrar, editar e excluir pessoas, e carregar por planilha seus grupos de trabalho, temas e histórico de participação — documento legado GPE003 – Manter Pessoa | 7 |

---

## Regras transversais de negócio

1. Nas cargas de planilha, a pessoa é reconhecida pelo `Cód. Contato`, o código dela no CRM — o campo CRM do cadastro.
2. Grupos de trabalho, temas e histórico de participação da pessoa entram no sistema apenas por carga de planilha. 💻
3. A pessoa vinculada a algum evento não é excluída. 💻 → ver RULES-DICTIONARY: RC-09 — Registro vinculado não pode ser excluído (parâmetro: entidade vinculada = participação em evento)
4. Toda pessoa guarda a origem do seu cadastro: Cadastro, Carga ou Recepção. 💻
5. Toda carga lê a primeira aba da planilha e trata a primeira linha como cabeçalho. 💻
6. As cargas aceitam planilha nos formatos `.xls` e `.xlsx`. 💻 GPE003 diz só "arquivo Excel" 📄; quem restringe às duas extensões é a tela — o servidor não confere a extensão e reconhece o formato pelo conteúdo.

---

## Integrações com outros domínios

### Leitura — domínios que consomem dados deste domínio
| Domínio | O que consome | Como |
|---|---|---|
| Eventos | Pessoa — nome, codinome, organização, cargo e foto, exibidos na lista de participantes e no mapa de assentos | FK |
| Eventos | Grupo de Trabalho, Papel Desempenhado, Tema, Cargo e Nome Fantasia — avaliados pelas condições das legendas | Serviço |
| Eventos | Histórico de participação — a soma das participações acompanha o nome no mapa e ordena a fila de atendimento | Serviço |

### Escrita — domínios que criam ou alteram dados deste domínio
| Domínio | O que altera | Situação |
|---|---|---|
| Eventos | Cria a pessoa, ou atualiza os dados dela, a partir da planilha | Carga de convidados e carga de confirmados |
| Eventos | Cria a pessoa, ou atualiza nome, codinome, e-mail, organização e cargo | Importação de inscritos do CRM |
| Eventos | Cria a pessoa com origem Recepção | Cadastro de participante na recepção |

---

<div class="dev-only">

## Entidades do domínio

| Entidade | Descrição | Campos no DATA-MODEL.md |
|---|---|---|
| Pessoa | Quem pode participar de um evento | → ver DATA-MODEL.md: Pessoa |
| GrupoTrabalhoPessoa | Participação da pessoa em um grupo de trabalho, com o papel | → ver DATA-MODEL.md: GrupoTrabalhoPessoa |
| TemaPessoa | Tema a que a pessoa se vincula | → ver DATA-MODEL.md: TemaPessoa |
| HistoricoPessoa | Participações da pessoa por ano | → ver DATA-MODEL.md: HistoricoPessoa |
| Arquivo | Foto da pessoa e imagem do evento | → ver DATA-MODEL.md: Arquivo |

---

## Dependências externas

| Serviço | Uso | Lib sugerida |
|---|---|---|
| Planilhas extraídas do CRM da CNI | Origem dos grupos de trabalho, temas e histórico, com o `Cód. Contato` como chave | Apache POI (já em uso) |

---

## Regras de acesso consolidadas

| Role | Pode fazer |
|---|---|
| Administrador | Tudo: pesquisar, cadastrar, editar, excluir e executar as três cargas |
| Secretaria Mesa | Nada neste domínio |
| Secretaria Check-In | Nada neste domínio |

⚠️ No servidor, o recurso de pessoas **não consta** entre os recursos protegidos declarados no cadastro corporativo do sistema — pesquisar, incluir, excluir e as três cargas dependem só do que esse cadastro devolve em produção, o que o código não permite confirmar 💻. Na interface, quem esconde a tela dos demais perfis é o menu.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | N1 criado | Engenharia reversa do documento legado GPE003 – Manter Pessoa e do código (telas de pessoa, cargas de planilha e estrutura do banco) |

---

*Última revisão: —*

*Links: [Cadastro de Pessoas](./cadastro-pessoas/README.md) · [INDEX geral](../INDEX.md)*
