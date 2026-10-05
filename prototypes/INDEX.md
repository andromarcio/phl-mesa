<!-- docqui: 4.1.0 | prompt: PROMPT_PROTOTYPE_FLOW_FULL | atualizado: 2026-10-04 -->
# Protótipos — Manifesto de fidelidade e aprovação
> Fonte de verdade do vínculo **protótipo ↔ N3**, do nível de **fidelidade** e do **status de aprovação**. Uma tela com fidelidade **obrigatória** só vira **contrato de implementação** quando o protótipo está **aprovado** aqui (com quem e quando).

> ⚠️ **Protótipos recuperados do sistema existente.** Os protótipos desta instância são de fluxo, um por Feature Set (`PROMPT_PROTOTYPE_FLOW_FULL`) — seis arquivos que cobrem as 55 features —, e reproduzem as telas como estão no código-fonte da aplicação — o inventário de telas em `arquivos/engenharia-reversa/frontend-inventory.md` e as imagens dos documentos legados GPE001 a GPE006 —, revestidos pela camada [`_biblioteca-ds/tema-gpe.css`](./_biblioteca-ds/tema-gpe.css). O endereço após o `#` abre direto a tela indicada. A fidelidade registrada aqui é **referência**; os N3 continuam com `Fidelidade ao protótipo: n/a`, por decisão de 2026-10-04 de não alterar as specs para registrar o vínculo. Quando um N3 for revisto pelo `PROMPT_4A`, a linha da `## Superfície` passa a apontar o protótipo.

| Protótipo | Feature (N3) | Fidelidade | Status | Aprovado por | Data |
|---|---|---|---|---|---|
| [acesso-usuarios/autenticacao/flow.html#login](./acesso-usuarios/autenticacao/flow.html#login) — tela de acesso | `ACE-AUT-01` | referência | rascunho | — | — |
| [acesso-usuarios/autenticacao/flow.html#inicio](./acesso-usuarios/autenticacao/flow.html#inicio) — menu do usuário, Logout | `ACE-AUT-02` | referência | rascunho | — | — |
| [acesso-usuarios/autenticacao/flow.html#recuperar-senha](./acesso-usuarios/autenticacao/flow.html#recuperar-senha) — tela Recuperar senha | `ACE-AUT-03` | referência | rascunho | — | — |
| [acesso-usuarios/autenticacao/flow.html#alterar-senha](./acesso-usuarios/autenticacao/flow.html#alterar-senha) — tela Alterar senha (voluntária e obrigatória) | `ACE-AUT-04` | referência | rascunho | — | — |
| [acesso-usuarios/autenticacao/flow.html#foto](./acesso-usuarios/autenticacao/flow.html#foto) — janela Alterar Imagem do Perfil ⚠️ só existe no GPE001 | `ACE-AUT-05` | referência | rascunho | — | — |
| [acesso-usuarios/autenticacao/flow.html#inicio](./acesso-usuarios/autenticacao/flow.html#inicio) — menu do usuário, dados do usuário | `ACE-AUT-06` | referência | rascunho | — | — |
| [acesso-usuarios/usuarios/flow.html](./acesso-usuarios/usuarios/flow.html) — tela Usuários | `ACE-USU-01` | referência | rascunho | — | — |
| [acesso-usuarios/usuarios/flow.html#usuario-novo](./acesso-usuarios/usuarios/flow.html#usuario-novo) — tela Usuário, inclusão com Validar Login | `ACE-USU-02` | referência | rascunho | — | — |
| [acesso-usuarios/usuarios/flow.html#usuario-editar](./acesso-usuarios/usuarios/flow.html#usuario-editar) — tela Usuário, edição | `ACE-USU-03` | referência | rascunho | — | — |
| [acesso-usuarios/usuarios/flow.html](./acesso-usuarios/usuarios/flow.html) — tela Usuários, confirmação Remover Usuário | `ACE-USU-04` | referência | rascunho | — | — |
| [pessoas/cadastro-pessoas/flow.html](./pessoas/cadastro-pessoas/flow.html) — tela Pessoas | `PES-CAD-01` | referência | rascunho | — | — |
| [pessoas/cadastro-pessoas/flow.html#pessoa-nova](./pessoas/cadastro-pessoas/flow.html#pessoa-nova) — tela Pessoa, inclusão | `PES-CAD-02` | referência | rascunho | — | — |
| [pessoas/cadastro-pessoas/flow.html#pessoa](./pessoas/cadastro-pessoas/flow.html#pessoa) — tela Pessoa, edição | `PES-CAD-03` | referência | rascunho | — | — |
| [pessoas/cadastro-pessoas/flow.html](./pessoas/cadastro-pessoas/flow.html) — tela Pessoas, Remover Pessoa | `PES-CAD-04` | referência | rascunho | — | — |
| [pessoas/cadastro-pessoas/flow.html](./pessoas/cadastro-pessoas/flow.html) — janela Carga de Grupos Temáticos | `PES-CAD-05` | referência | rascunho | — | — |
| [pessoas/cadastro-pessoas/flow.html](./pessoas/cadastro-pessoas/flow.html) — janela Carga de Temas | `PES-CAD-06` | referência | rascunho | — | — |
| [pessoas/cadastro-pessoas/flow.html](./pessoas/cadastro-pessoas/flow.html) — janela Carga de Histórico | `PES-CAD-07` | referência | rascunho | — | — |
| [eventos/cadastro-eventos/flow.html](./eventos/cadastro-eventos/flow.html) — tela Eventos | `EVT-CAD-01` | referência | rascunho | — | — |
| [eventos/cadastro-eventos/flow.html#evento-novo](./eventos/cadastro-eventos/flow.html#evento-novo) — tela Evento, inclusão | `EVT-CAD-02` | referência | rascunho | — | — |
| [eventos/cadastro-eventos/flow.html#evento](./eventos/cadastro-eventos/flow.html#evento) — tela Evento, edição | `EVT-CAD-03` | referência | rascunho | — | — |
| [eventos/cadastro-eventos/flow.html#evento-visualizar](./eventos/cadastro-eventos/flow.html#evento-visualizar) — tela Evento, visualização | `EVT-CAD-04` | referência | rascunho | — | — |
| [eventos/cadastro-eventos/flow.html](./eventos/cadastro-eventos/flow.html) — tela Eventos, Excluir evento | `EVT-CAD-05` | referência | rascunho | — | — |
| [eventos/cadastro-eventos/flow.html](./eventos/cadastro-eventos/flow.html) — tela Eventos, Tornar evento principal | `EVT-CAD-06` | referência | rascunho | — | — |
| [eventos/cadastro-eventos/flow.html#cargas](./eventos/cadastro-eventos/flow.html#cargas) — janela Cargas de Convidados e Confirmados, Carga de Convidados | `EVT-CAD-07` | referência | rascunho | — | — |
| [eventos/cadastro-eventos/flow.html#cargas](./eventos/cadastro-eventos/flow.html#cargas) — janela Cargas de Convidados e Confirmados, Carga de Confirmados | `EVT-CAD-08` | referência | rascunho | — | — |
| [eventos/cadastro-eventos/flow.html#cargas](./eventos/cadastro-eventos/flow.html#cargas) — janela Cargas de Convidados e Confirmados, Inscritos do CRM | `EVT-CAD-09` | referência | rascunho | — | — |
| [eventos/participantes/flow.html#lista](./eventos/participantes/flow.html#lista) — lista de participantes (Administrador e Secretaria Check-In) | `EVT-PAR-01` | referência | rascunho | — | — |
| [eventos/participantes/flow.html#lista](./eventos/participantes/flow.html#lista) — janela Cadastrar Pessoa | `EVT-PAR-02` | referência | rascunho | — | — |
| [eventos/participantes/flow.html#checkin](./eventos/participantes/flow.html#checkin) — lista de participantes, coluna Check-In | `EVT-PAR-03` | referência | rascunho | — | — |
| [eventos/participantes/flow.html#lista](./eventos/participantes/flow.html#lista) — janela Gerenciar Legenda da Pessoa, consulta | `EVT-PAR-04` | referência | rascunho | — | — |
| [eventos/participantes/flow.html#lista](./eventos/participantes/flow.html#lista) — janela Gerenciar Legenda da Pessoa, alteração | `EVT-PAR-05` | referência | rascunho | — | — |
| [eventos/participantes/flow.html#lista](./eventos/participantes/flow.html#lista) — janela Gerenciar Legenda da Pessoa, remoção | `EVT-PAR-06` | referência | rascunho | — | — |
| [eventos/participantes/flow.html#mapa](./eventos/participantes/flow.html#mapa) — mapa de assentos (Administrador e Secretaria Mesa) | `EVT-PAR-07` | referência | rascunho | — | — |
| [eventos/participantes/flow.html#mapa](./eventos/participantes/flow.html#mapa) — mapa do Administrador, arrastar ou escolher a pessoa do assento | `EVT-PAR-08` | referência | rascunho | — | — |
| [eventos/participantes/flow.html#mapa](./eventos/participantes/flow.html#mapa) — mapa do Administrador, retirar a pessoa do assento | `EVT-PAR-09` | referência | rascunho | — | — |
| [eventos/participantes/flow.html#mapa-secretaria](./eventos/participantes/flow.html#mapa-secretaria) — mapa da Secretaria Mesa, fila de check-in e ATENDIDO | `EVT-PAR-10` | referência | rascunho | — | — |
| [eventos/participantes/flow.html#mapa](./eventos/participantes/flow.html#mapa) — mapa do Administrador, Limpar Todas | `EVT-PAR-11` | referência | rascunho | — | — |
| [eventos/participantes/flow.html#mapa](./eventos/participantes/flow.html#mapa) — mapas, Buscar pessoa na mesa | `EVT-PAR-12` | referência | rascunho | — | — |
| [eventos/participantes/flow.html#lista](./eventos/participantes/flow.html#lista) — lista de participantes, coluna Confirmado | `EVT-PAR-13` | referência | rascunho | — | — |
| [eventos/participantes/flow.html#lista](./eventos/participantes/flow.html#lista) — lista de participantes, Download | `EVT-PAR-14` | referência | rascunho | — | — |
| [eventos/participantes/flow.html#mapa](./eventos/participantes/flow.html#mapa) — mapa do Administrador, Exportações PDF e PNG | `EVT-PAR-15` | referência | rascunho | — | — |
| [eventos/legendas/flow.html#configuracao](./eventos/legendas/flow.html#configuracao) — tela Configuração de Legendas | `EVT-LEG-01` | referência | rascunho | — | — |
| [eventos/legendas/flow.html#configuracao](./eventos/legendas/flow.html#configuracao) — janela Adicionar bloco, Usar bloco existente | `EVT-LEG-02` | referência | rascunho | — | — |
| [eventos/legendas/flow.html#configuracao](./eventos/legendas/flow.html#configuracao) — Configuração de Legendas, condições do bloco | `EVT-LEG-03` | referência | rascunho | — | — |
| [eventos/legendas/flow.html#configuracao](./eventos/legendas/flow.html#configuracao) — Configuração de Legendas, subir e descer bloco | `EVT-LEG-04` | referência | rascunho | — | — |
| [eventos/legendas/flow.html#configuracao](./eventos/legendas/flow.html#configuracao) — Configuração de Legendas, remover bloco | `EVT-LEG-05` | referência | rascunho | — | — |
| [eventos/legendas/flow.html#configuracao](./eventos/legendas/flow.html#configuracao) — janela Simulação de aplicação de legendas | `EVT-LEG-06` | referência | rascunho | — | — |
| [eventos/legendas/flow.html#configuracao](./eventos/legendas/flow.html#configuracao) — Configuração de Legendas, Executar | `EVT-LEG-07` | referência | rascunho | — | — |
| [eventos/legendas/flow.html#configuracao](./eventos/legendas/flow.html#configuracao) — janela Salvar como preset | `EVT-LEG-08` | referência | rascunho | — | — |
| [eventos/legendas/flow.html#configuracao](./eventos/legendas/flow.html#configuracao) — janela Carregar configuração | `EVT-LEG-09` | referência | rascunho | — | — |
| [eventos/legendas/flow.html#configuracao](./eventos/legendas/flow.html#configuracao) — janela Carregar configuração, excluir preset | `EVT-LEG-10` | referência | rascunho | — | — |
| [eventos/legendas/flow.html#catalogo](./eventos/legendas/flow.html#catalogo) — tela Catálogo de blocos | `EVT-LEG-11` | referência | rascunho | — | — |
| [eventos/legendas/flow.html#catalogo](./eventos/legendas/flow.html#catalogo) — janela do bloco, Novo bloco (e aba Criar novo bloco) | `EVT-LEG-12` | referência | rascunho | — | — |
| [eventos/legendas/flow.html#catalogo](./eventos/legendas/flow.html#catalogo) — janela do bloco, Editar bloco | `EVT-LEG-13` | referência | rascunho | — | — |
| [eventos/legendas/flow.html#catalogo](./eventos/legendas/flow.html#catalogo) — Catálogo de blocos, excluir bloco | `EVT-LEG-14` | referência | rascunho | — | — |

## Como manter

- A pasta `prototypes/` **espelha `modules/`**: `prototypes/[dominio]/[feature-set]/[feature]/`, com os mesmos nomes de pasta e um `README.md` em cada nível — domínio (índice dos Feature Sets com protótipo), Feature Set (protótipo de fluxo) e feature (protótipos de estado). Modelos em `engine/templates/prototypes/_template/`.
- Ao **gerar** um protótipo, registre a linha com status **rascunho** e a fidelidade lida do N3 (linha `Fidelidade ao protótipo` na `## Superfície`).
- Na **aprovação**, troque o status para **aprovado** e preencha **quem** e **quando**. Só então a tela é **contrato** para a codificação.
- A implementação de telas **obrigatória** exige a **checklist de fidelidade** — `node scripts/fidelity-checklist.mjs <pasta-do-protótipo> <N3.md>` — com **todos os estados cobertos** (✅, ou ⚠️ com desvio aprovado; nenhum ❌).
- **Especificação Funcional (.docx):** cada `flow.html` traz o manifesto `<script id="docx-telas">`, com as telas de cada feature e o passo que as exibe. O `scripts/gera-docx.py` captura essas telas para a seção *Telas e Protótipos* de cada funcionalidade e, quando o N3 não aponta protótipo na `## Superfície`, encontra-o por este manifesto. As capturas ficam em cache em `documentos/_prototipos/`; depois de mudar um protótipo, rode `python3 scripts/gera-docx.py --refaz-figuras-velhas` e grave `documentos/`.
- **Reforço opcional (CI, onde há runtime):** regressão visual `node scripts/proto-visual-diff.mjs <protótipo> <tela-implementada>` — roda no **repositório de código** (Playwright + app), não aqui. Ver o cabeçalho do script.

## Legenda

- **Fidelidade** — `obrigatória`: a implementação reproduz o protótipo; `referência`: guia a intenção.
- **Status** — `rascunho`: em elaboração; `aprovado`: travado como contrato (registrar quem/quando).
