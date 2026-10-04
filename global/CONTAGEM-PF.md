<!-- docqui: 4.0.2 | prompt: PROMPT_CONTAGEM | atualizado: 2026-10-04 -->
# CONTAGEM-PF.md
> **Registro consolidado da contagem de Pontos de Função (APF / IFPUG CPM 4.3.1)**
> do sistema. Reúne num só lugar **todos os Processos Elementares (PE)** — as
> Funções de Transação EE/SE/CE — e **todas as entidades que possuem contagem**
> — as Funções de Dados ALI/AIE.
>
> Este arquivo é o **consolidado** (índice de leitura); as **fontes de cálculo** são:
> - **Funções de Transação (PE)** → a seção `## Métricas de tamanho` de cada **N3**.
> - **Funções de Dados (ALI/AIE)** → `global/DATA-MODEL.md → ## Arquivos Lógicos (APF)`
>   (validade do ALI/AIE em `global/ALI-AIE-MAP.md`).
>
> Critérios de contagem: `global/SIZING.md`.
>
> ⚠️ **Contagem parcial.** Em 2026-10-04 foram contadas 17 das 55 features — as que os tickets `PDTIC25148-34` e `PDTIC25148-35` alcançaram: as 14 de Legendas e, de Participantes, Pesquisar Participantes, Consultar Legenda do Participante e Alterar Legenda do Participante — e os três arquivos lógicos do domínio Eventos. As outras 38 features e os arquivos lógicos de Pessoas e de Acesso e Usuários seguem em *Pendências de contagem*. As 55 features estão em rascunho: a contagem foi feita sobre N3 ainda não validados pelo PO e acompanha o que eles disserem.

---

## ⚙️ Regra de manutenção (LEIA ANTES DE EDITAR)

> **Gatilho:** *sempre que um N3 for criado/alterado ou uma entidade (ALI/AIE) for
> criada/alterada, a contagem deve ser revisada e — havendo alteração — este arquivo
> deve ser atualizado.*
>
> **Quem edita este arquivo é a revisão de contagem** — a opção `CT`
> (`PROMPT_CONTAGEM`), depois da confirmação do Tech Lead/PO. O `PROMPT_3B` e o
> `PROMPT_4B` contam na fonte e pedem a revisão; não tocam este arquivo.

Procedimento da revisão, para um N3 ou uma entidade:

1. **Reconte na fonte** seguindo `global/SIZING.md`:
   - mudou um N3? → revise a tabela `## Métricas de tamanho` do próprio N3;
   - mudou uma entidade/ALI? → revise a linha em `global/DATA-MODEL.md → ## Arquivos Lógicos (APF)`.
2. **Compare com o valor registrado aqui.** Se for igual, as tabelas não mudam — mas a revisão foi feita: a feature sai de `## Pendências de contagem` e fica com `contagem.pendente: false` (registre no Changelog do N3 que a contagem permanece inalterada).
3. **Havendo alteração**, atualize **neste arquivo**: a linha do PE/entidade, os subtotais e o **Total do sistema**.
4. **Propague o total** para `modules/INDEX.md` (tabela de rastreabilidade + linha de total).
5. **Registre** a recontagem no `## Changelog` do N3 (ou no histórico desta página, para mudança de entidade).

> ⚠️ **Mudança puramente técnica** que **não** altera a lógica de processamento sob a
> ótica do usuário (tipo físico de campo, otimização de banco, refactor interno)
> **não gera nova contagem** — ver `SIZING.md → Regras de medição de serviços, item 5`.
> Nesse caso, a contagem permanece e este arquivo **não** muda.

> Regra de ouro: **as fontes (N3 e DATA-MODEL.md) mandam; este arquivo as espelha.**
> Nunca registre aqui um número que não exista na fonte.

---

## Pendências de contagem

> Features cuja **última alteração ainda não foi revisada** para Pontos de Função —
> espelho de `contagem.pendente: true` no front-matter dos N3 (status **independente**
> da esteira de gates). Uma feature entra aqui quando é criada/alterada (3A/4A/CRUD/WIZARD/RT/R1/R3)
> e **sai** quando a contagem é revisada (opção `CT` / `PROMPT_CONTAGEM`) — mesmo que a
> revisão conclua **Δ PF = 0** (o que se registra é a *revisão feita*, não a mudança do número).

| Feature (N3) | Domínio | Alteração pendente (ticket) | Desde |
|---|---|---|---|
| [ACE-AUT-01 — Autenticar Usuário](../modules/acesso-usuarios/autenticacao/f-autenticar-usuario.md) | Acesso e Usuários | criação | 2026-09-30 |
| [ACE-AUT-02 — Encerrar Sessão](../modules/acesso-usuarios/autenticacao/f-encerrar-sessao.md) | Acesso e Usuários | criação | 2026-09-30 |
| [ACE-AUT-03 — Recuperar Senha](../modules/acesso-usuarios/autenticacao/f-recuperar-senha.md) | Acesso e Usuários | criação | 2026-09-30 |
| [ACE-AUT-04 — Alterar Senha](../modules/acesso-usuarios/autenticacao/f-alterar-senha.md) | Acesso e Usuários | criação | 2026-09-30 |
| [ACE-AUT-05 — Alterar Foto de Perfil](../modules/acesso-usuarios/autenticacao/f-alterar-foto-perfil.md) | Acesso e Usuários | criação | 2026-09-30 |
| [ACE-AUT-06 — Consultar Dados do Usuário](../modules/acesso-usuarios/autenticacao/f-consultar-dados-usuario.md) | Acesso e Usuários | criação | 2026-09-30 |
| [ACE-USU-01 — Pesquisar Usuários](../modules/acesso-usuarios/usuarios/f-pesquisar-usuarios.md) | Acesso e Usuários | criação | 2026-09-30 |
| [ACE-USU-02 — Cadastrar Usuário](../modules/acesso-usuarios/usuarios/f-cadastrar-usuario.md) | Acesso e Usuários | criação | 2026-09-30 |
| [ACE-USU-03 — Editar Usuário](../modules/acesso-usuarios/usuarios/f-editar-usuario.md) | Acesso e Usuários | criação | 2026-09-30 |
| [ACE-USU-04 — Excluir Usuário](../modules/acesso-usuarios/usuarios/f-excluir-usuario.md) | Acesso e Usuários | criação | 2026-09-30 |
| [PES-CAD-01 — Pesquisar Pessoas](../modules/pessoas/cadastro-pessoas/f-pesquisar-pessoas.md) | Pessoas | criação | 2026-09-30 |
| [PES-CAD-02 — Cadastrar Pessoa](../modules/pessoas/cadastro-pessoas/f-cadastrar-pessoa.md) | Pessoas | criação | 2026-09-30 |
| [PES-CAD-03 — Editar Pessoa](../modules/pessoas/cadastro-pessoas/f-editar-pessoa.md) | Pessoas | criação | 2026-09-30 |
| [PES-CAD-04 — Excluir Pessoa](../modules/pessoas/cadastro-pessoas/f-excluir-pessoa.md) | Pessoas | criação | 2026-09-30 |
| [PES-CAD-05 — Carregar Grupos de Trabalho](../modules/pessoas/cadastro-pessoas/f-carregar-grupos-trabalho.md) | Pessoas | criação | 2026-09-30 |
| [PES-CAD-06 — Carregar Temas](../modules/pessoas/cadastro-pessoas/f-carregar-temas.md) | Pessoas | criação | 2026-09-30 |
| [PES-CAD-07 — Carregar Histórico de Participação](../modules/pessoas/cadastro-pessoas/f-carregar-historico-participacao.md) | Pessoas | criação | 2026-09-30 |
| [EVT-CAD-01 — Pesquisar Eventos](../modules/eventos/cadastro-eventos/f-pesquisar-eventos.md) | Eventos | criação | 2026-09-30 |
| [EVT-CAD-02 — Cadastrar Evento](../modules/eventos/cadastro-eventos/f-cadastrar-evento.md) | Eventos | criação | 2026-09-30 |
| [EVT-CAD-03 — Editar Evento](../modules/eventos/cadastro-eventos/f-editar-evento.md) | Eventos | criação | 2026-09-30 |
| [EVT-CAD-04 — Visualizar Evento](../modules/eventos/cadastro-eventos/f-visualizar-evento.md) | Eventos | criação | 2026-09-30 |
| [EVT-CAD-05 — Excluir Evento](../modules/eventos/cadastro-eventos/f-excluir-evento.md) | Eventos | criação | 2026-09-30 |
| [EVT-CAD-06 — Definir Evento Principal](../modules/eventos/cadastro-eventos/f-definir-evento-principal.md) | Eventos | criação | 2026-09-30 |
| [EVT-CAD-07 — Carregar Convidados](../modules/eventos/cadastro-eventos/f-carregar-convidados.md) | Eventos | criação | 2026-09-30 |
| [EVT-CAD-08 — Carregar Confirmados](../modules/eventos/cadastro-eventos/f-carregar-confirmados.md) | Eventos | criação | 2026-09-30 |
| [EVT-CAD-09 — Importar Inscritos do CRM](../modules/eventos/cadastro-eventos/f-importar-inscritos-crm.md) | Eventos | criação | 2026-09-30 |
| [EVT-PAR-02 — Cadastrar Participante](../modules/eventos/participantes/f-cadastrar-participante.md) | Eventos | criação | 2026-09-30 |
| [EVT-PAR-03 — Registrar Check-in](../modules/eventos/participantes/f-registrar-check-in.md) | Eventos | criação | 2026-09-30 |
| [EVT-PAR-06 — Remover Legenda do Participante](../modules/eventos/participantes/f-remover-legenda-participante.md) | Eventos | criação | 2026-09-30 |
| [EVT-PAR-07 — Consultar Mapa de Assentos](../modules/eventos/participantes/f-consultar-mapa-assentos.md) | Eventos | criação | 2026-09-30 |
| [EVT-PAR-08 — Atribuir Assento ao Participante](../modules/eventos/participantes/f-atribuir-assento-participante.md) | Eventos | criação | 2026-09-30 |
| [EVT-PAR-09 — Remover Assento do Participante](../modules/eventos/participantes/f-remover-assento-participante.md) | Eventos | criação | 2026-09-30 |
| [EVT-PAR-10 — Registrar Atendimento](../modules/eventos/participantes/f-registrar-atendimento.md) | Eventos | criação | 2026-09-30 |
| [EVT-PAR-11 — Liberar Todos os Assentos](../modules/eventos/participantes/f-liberar-assentos.md) | Eventos | criação | 2026-09-30 |
| [EVT-PAR-12 — Buscar Pessoa na Mesa](../modules/eventos/participantes/f-buscar-pessoa-mesa.md) | Eventos | criação | 2026-09-30 |
| [EVT-PAR-13 — Alterar Confirmação de Presença](../modules/eventos/participantes/f-alterar-confirmacao-presenca.md) | Eventos | criação | 2026-09-30 |
| [EVT-PAR-14 — Exportar Participantes](../modules/eventos/participantes/f-exportar-participantes.md) | Eventos | criação | 2026-09-30 |
| [EVT-PAR-15 — Exportar Mapa de Assentos](../modules/eventos/participantes/f-exportar-mapa-assentos.md) | Eventos | criação | 2026-09-30 |

> Vazia = nenhuma contagem pendente (toda alteração já foi revisada). A visão por feature
> fica na coluna **Contagem** (📋/✅) de `modules/INDEX.md`.

---

## 1. Funções de Transação — Processos Elementares (PE)

> Unidade de contagem = a **feature (N3) inteira** (front + BFF), não o endpoint.
> Ver *Arquitetura BFF* em `global/SIZING.md`. Cada PE classifica-se como **EE**, **SE** ou **CE**.

| # | Feature (N3) | Papel | Domínio | Tipo | ALR | DER | Complexidade | PF | Data | Status | Observação |
|---|---|---|---|---|---|---|---|---|---|---|---|
| EVT-LEG-01 | [Consultar Configuração de Legendas](../modules/eventos/legendas/f-consultar-configuracao-legendas.md) | principal | Eventos | CE | 2 | 10 | Média | 4 | 2026-10-04 | ✏️ |  |
| EVT-LEG-02 | [Adicionar Bloco de Legenda ao Evento](../modules/eventos/legendas/f-adicionar-bloco-legenda.md) | principal | Eventos | EE | 2 | 3 | Baixa | 3 | 2026-10-04 | ✏️ |  |
| EVT-LEG-02 | [Consultar Lista de blocos (combo)](../modules/eventos/legendas/f-adicionar-bloco-legenda.md) | acessório | Eventos | CE | 2 | 3 | Baixa | 3 | 2026-10-04 | ✏️ | lê `Legenda` e `Evento`: os blocos do catálogo que ainda não estão no evento |
| EVT-LEG-03 | [Configurar Condições de Legenda](../modules/eventos/legendas/f-configurar-condicoes-legenda.md) | principal | Eventos | EE | 2 | 7 | Média | 4 | 2026-10-04 | ✏️ |  |
| EVT-LEG-04 | [Reordenar Blocos de Legenda](../modules/eventos/legendas/f-reordenar-blocos-legenda.md) | principal | Eventos | EE | 2 | 3 | Baixa | 3 | 2026-10-04 | ✏️ | mesmos DER e ALR de Remover Bloco de Legenda do Evento; a lógica é outra (troca de posição) |
| EVT-LEG-05 | [Remover Bloco de Legenda do Evento](../modules/eventos/legendas/f-remover-bloco-legenda.md) | principal | Eventos | EE | 2 | 3 | Baixa | 3 | 2026-10-04 | ✏️ |  |
| EVT-LEG-06 | [Simular Aplicação de Legendas](../modules/eventos/legendas/f-simular-aplicacao-legendas.md) | principal | Eventos | SE | 3 | 12 | Média | 5 | 2026-10-04 | ✏️ | as condições em tela entram como parâmetro e não foram contadas como DER; com elas seriam 16, na mesma faixa |
| EVT-LEG-07 | [Gerar Legendas do Evento](../modules/eventos/legendas/f-gerar-legendas-evento.md) | principal | Eventos | EE | 3 | 2 | Média | 4 | 2026-10-04 | ✏️ | os dois totais da mensagem de sucesso contam como a Mensagem; contados como dados, seriam 4 DER e a complexidade continuaria Média — a Alta só viria com 5 |
| EVT-LEG-08 | [Salvar Preset de Legendas](../modules/eventos/legendas/f-salvar-preset-legendas.md) | principal | Eventos | EE | 3 | 4 | Média | 4 | 2026-10-04 | ✏️ | Evento e Legenda contados como referenciados pela visão lógica; só com PresetLegenda, seria Baixa, 3 PF |
| EVT-LEG-09 | [Carregar Configuração de Legendas](../modules/eventos/legendas/f-carregar-configuracao-legendas.md) | principal | Eventos | EE | 3 | 5 | Alta | 6 | 2026-10-04 | ✏️ | preset e outro evento são fluxos alternativos do mesmo processo (Guia STI 3.2): DER e ALR são a união dos dois |
| EVT-LEG-09 | [Consultar Biblioteca de presets (combo)](../modules/eventos/legendas/f-carregar-configuracao-legendas.md) | acessório | Eventos | SE | 2 | 6 | Média | 5 | 2026-10-04 | ✏️ | SE: a quantidade de blocos de cada preset é cálculo; lê `PresetLegenda` e `Legenda` |
| EVT-LEG-09 | [Consultar De outro evento (combo)](../modules/eventos/legendas/f-carregar-configuracao-legendas.md) | acessório | Eventos | SE | 1 | 3 | Baixa | 4 | 2026-10-04 | ✏️ | SE: a quantidade de blocos de cada evento é cálculo; lê `Evento` |
| EVT-LEG-10 | [Excluir Preset de Legendas](../modules/eventos/legendas/f-excluir-preset-legendas.md) | principal | Eventos | EE | 1 | 3 | Baixa | 3 | 2026-10-04 | ✏️ |  |
| EVT-LEG-11 | [Pesquisar Blocos de Legenda](../modules/eventos/legendas/f-pesquisar-blocos-legenda.md) | principal | Eventos | CE | 1 | 4 | Baixa | 3 | 2026-10-04 | ✏️ |  |
| EVT-LEG-12 | [Cadastrar Bloco de Legenda](../modules/eventos/legendas/f-cadastrar-bloco-legenda.md) | principal | Eventos | EE | 1 | 4 | Baixa | 3 | 2026-10-04 | ✏️ |  |
| EVT-LEG-13 | [Editar Bloco de Legenda](../modules/eventos/legendas/f-editar-bloco-legenda.md) | principal | Eventos | EE | 1 | 4 | Baixa | 3 | 2026-10-04 | ✏️ |  |
| EVT-LEG-13 | [Consultar Bloco de Legenda (implícita)](../modules/eventos/legendas/f-editar-bloco-legenda.md) | acessório | Eventos | — | — | — | — | 0 | 2026-10-04 | ✏️ | 0 PF: a janela Editar bloco abre com o nome e a cor, que a lista do catálogo já mostrava — nada novo cruza a fronteira |
| EVT-LEG-14 | [Excluir Bloco de Legenda](../modules/eventos/legendas/f-excluir-bloco-legenda.md) | principal | Eventos | EE | 2 | 4 | Baixa | 3 | 2026-10-04 | ✏️ | a consulta de uso alimenta só a pergunta de confirmação e é passo deste processo |
| EVT-PAR-01 | [Pesquisar Participantes](../modules/eventos/participantes/f-pesquisar-participantes.md) | principal | Eventos | CE | 3 | 19 | Média | 4 | 2026-10-04 | ✏️ | 19 DER, a um da faixa Alta; Total e paginação não contam (Guia STI 5.5) |
| EVT-PAR-01 | [Consultar Legendas (combo)](../modules/eventos/participantes/f-pesquisar-participantes.md) | acessório | Eventos | CE | 1 | 2 | Baixa | 3 | 2026-10-04 | ✏️ | lê `Legenda` |
| EVT-PAR-01 | [Consultar Temas (combo)](../modules/eventos/participantes/f-pesquisar-participantes.md) | acessório | Eventos | CE | 1 | 2 | Baixa | 3 | 2026-10-04 | ✏️ | lê `Pessoa`: os temas de todas as pessoas, sem repetição |
| EVT-PAR-01 | [Consultar Grupos de Trabalho (combo)](../modules/eventos/participantes/f-pesquisar-participantes.md) | acessório | Eventos | CE | 1 | 2 | Baixa | 3 | 2026-10-04 | ✏️ | lê `Pessoa`: os grupos de trabalho de todas as pessoas, sem repetição |
| EVT-PAR-01 | [Consultar Cargo (combo)](../modules/eventos/participantes/f-pesquisar-participantes.md) | acessório | Eventos | CE | 1 | 2 | Baixa | 3 | 2026-10-04 | ✏️ | lê `Pessoa`: os cargos de todas as pessoas, sem repetição |
| EVT-PAR-04 | [Consultar Legenda do Participante](../modules/eventos/participantes/f-consultar-legenda-participante.md) | principal | Eventos | CE | 3 | 8 | Média | 4 | 2026-10-04 | ✏️ |  |
| EVT-PAR-04 | [Consultar Selecione uma Legenda (combo)](../modules/eventos/participantes/f-consultar-legenda-participante.md) | acessório | Eventos | CE | 2 | 4 | Baixa | 3 | 2026-10-04 | ✏️ | lê `Legenda` e `Evento`; é o processo que os tickets `PDTIC25148-34` e `PDTIC25148-35` alteraram na feature |
| EVT-PAR-05 | [Alterar Legenda do Participante](../modules/eventos/participantes/f-alterar-legenda-participante.md) | principal | Eventos | EE | 2 | 3 | Baixa | 3 | 2026-10-04 | ✏️ |  |

> **PE reutilizado** — a linha `↪ [ID](…)` da tabela de um N3 — **não** ganha linha aqui: cada PE conta uma vez na aplicação, na feature onde é contado (`SIZING.md` → *PE reutilizado*).

> A coluna **Papel** espelha a da `## Métricas de tamanho` do N3 (`principal` · `acessório`; PE sem feature — workflow, integração, notificação — sai com `—`). Por feature, a soma de PF dos principais tem de bater com a da fonte — `SIZING.md` → *Papel do PE em relação à feature*.

> A coluna **Observação** guarda o que é do **processo elementar**, não de uma contagem específica: por que uma linha ficou sem PF, que convenção a equipe de métricas aplicou ali, que armadilha de leitura ela esconde. É o lugar de registrar o critério **uma vez**, para que a próxima recontagem não precise redescobri-lo — e para que uma linha zerada não se confunda com linha por preencher.


**Subtotal Funções de Transação: 89 PF** (25 PE contados, em 17 features; mais uma linha de 0 PF).

> Features `❌ Deprecadas` saem do total vigente (mantêm-se no histórico).

---

## 2. Funções de Dados — entidades com contagem (ALI / AIE)

> Espelho de `global/DATA-MODEL.md → ## Arquivos Lógicos (APF)`. A contagem de DER
> **exclui** os campos globais técnicos (createdAt, updatedAt, deletedAt) e conta o `id`
> como **1 DER por ALI**, não por tabela. Validade do
> ALI/AIE em `global/ALI-AIE-MAP.md`.

### ALIs — Arquivos Lógicos Internos

| ALI | Domínio | Entidades constituintes | RLR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Evento | Eventos | Evento (principal) · CadeiraMesa, EventoPessoa, EventoLegenda, EventoLegendaCondicao, EventoPessoaLegenda (subgrupos) | 6 | 33 | Alta | 15 | 2026-10-04 |
| Legenda | Eventos | Legenda (principal) | 1 | 3 | Baixa | 7 | 2026-10-04 |
| PresetLegenda | Eventos | PresetLegenda (principal) | 1 | 5 | Baixa | 7 | 2026-10-04 |

**Subtotal ALIs: 29 PF.**

#### Memória de cálculo — Evento

**RLR (6)** — subgrupos lógicos do arquivo:

1. `Evento` — os dados do evento
2. `CadeiraMesa` — os assentos nascem com o evento e se repetem para cada um
3. `EventoPessoa` — o participante: entidade associativa com atributos, sem regra que mande guardá-la de forma independente (CPM, Parte 3, cap. 2, situação 2)
4. `EventoLegenda` — o bloco de legenda na configuração do evento, pela mesma regra
5. `EventoLegendaCondicao` — as condições, entidade atributiva do bloco
6. `EventoPessoaLegenda` — a legenda que o participante recebeu, pela mesma regra do participante

**DER (33)** — atributos únicos reconhecidos pelo usuário:

- `Evento` (9): Nome do Evento · Data e Hora · Local · Tipo de Evento · Tipo de Mesa · Participantes · Código da Campanha · Arquivo · Principal
- `CadeiraMesa` (2): Identificação · Composição
- `EventoPessoa` (11): Pessoa · Convidado · Confirmado · Check-In · Data e hora do check-in · Atendido · Data de envio do formulário · Status da Inscrição · Status Aprovação · Identificação da inscrição no CRM · Identificação do contato no CRM
- `EventoLegenda` (2): Legenda · Nº
- `EventoLegendaCondicao` (5): Ordem · Conectivo · Campo · Operador · Valor
- `EventoPessoaLegenda` (3): Legenda do participante · Manual · Data de atribuição
- **+1** identificador (uma vez por ALI, não por tabela)

> Não contados: Excluído, marcador técnico da exclusão lógica · as ligações internas ao arquivo (do assento, do participante e do bloco ao evento; da condição ao bloco; da legenda ao participante) · o Assento do participante, que repete a Identificação já contada. Com cinco registros lógicos em vez de seis, a complexidade seria Média, 10 PF.

#### Memória de cálculo — Legenda

**RLR (1)**: `Legenda`. **DER (3)**: Nome da legenda · Cor · **+1** identificador.

#### Memória de cálculo — PresetLegenda

**RLR (1)**: `PresetLegenda`. **DER (5)**: Nome do preset · Descrição · Evento de origem · Configuração · **+1** identificador.

> Não contado: Data de criação, campo técnico que nenhuma tela mostra. A Configuração conta como um atributo, como o modelo a descreve; desdobrada em blocos e condições, a complexidade continuaria Baixa.

### AIEs — Arquivos de Interface Externa

| AIE | Sistema externo | Entidades / estruturas usadas | RLR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| — | — | Nenhum AIE contado ainda. Candidatos conhecidos: o cadastro corporativo de usuários e perfis da CNI e os inscritos do CRM | — | — | — | — | — |

**Subtotal AIEs: — PF.**

**Subtotal Funções de Dados: 29 PF** (só o domínio Eventos).

---

## 3. Total do sistema

| Categoria | PF |
|---|---|
| Funções de Transação (PE: EE/SE/CE) | 89 |
| Funções de Dados (ALI/AIE) | 29 |
| **Total não ajustado (PF)** | **118** |

> Total **parcial**: 17 das 55 features e só os arquivos lógicos de Eventos.

> **PF não ajustado** (FSM puro) — não adotar VAF/PF ajustado (ver `SIZING.md`).

---

## Histórico de recontagens

| Data | Autor | O que mudou | Δ PF | Total |
|---|---|---|---|---|
| 2026-10-04 | Claude (apf-cpm) | Primeira contagem, pelo `PROMPT_CONTAGEM`, confirmada no mesmo dia: 17 features dos tickets `PDTIC25148-34` e `PDTIC25148-35` (89 PF em 25 processos elementares) e os arquivos lógicos Evento, Legenda e PresetLegenda (29 PF) | +118 | 118 |
| 2026-09-30 | Claude (analista-requisitos) | Registro aberto na engenharia reversa: 55 features pendentes de contagem, nenhuma contada | — | — |

---

## Links
[SIZING.md](./SIZING.md) · [DATA-MODEL.md](./DATA-MODEL.md) · [ALI-AIE-MAP.md](./ALI-AIE-MAP.md) · [MASTER.md](./MASTER.md) · [INDEX geral](../modules/INDEX.md)
