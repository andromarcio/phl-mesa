<!-- docqui: 4.0.2 | prompt: PROMPT_AIM | atualizado: 2026-10-04 -->
# Índice geral de módulos
> Visão consolidada de todos os domínios do sistema.
> Mantido via PROMPT 1A/1B — atualizar após cada N1 aprovado.

> Gerado por engenharia reversa em 2026-09-30, a partir dos documentos legados GPE001 a GPE006 e do código. **Todas as features estão em rascunho**; o que precisa de revisão humana está em [`REVISAO-CONVERSAO.md`](../REVISAO-CONVERSAO.md).

---

## Domínios

| Domínio | Pasta | Responsabilidade | Feature Sets |
|---|---|---|---|
| [Acesso e Usuários](./acesso-usuarios/README.md) <small>`ACE`</small> | `modules/acesso-usuarios/` | Entrada no sistema, senha, dados do usuário logado e manutenção dos usuários e de seus perfis | 2 |
| [Pessoas](./pessoas/README.md) <small>`PES`</small> | `modules/pessoas/` | Cadastro das pessoas que podem ser convidadas e do que as qualifica: grupos de trabalho, temas e histórico de participação | 1 |
| [Eventos](./eventos/README.md) <small>`EVT`</small> | `modules/eventos/` | Cadastro dos eventos, participantes de cada um, check-in, mapa de assentos e legendas | 3 |

### Feature Sets e documentos legados

| Feature Set | ID | Documento legado | Features |
|---|---|---|---|
| [Autenticação](./acesso-usuarios/autenticacao/README.md) | `ACE-AUT` | GPE001 – Efetuar Login | 6 |
| [Usuários](./acesso-usuarios/usuarios/README.md) | `ACE-USU` | GPE002 – Manter Usuário | 4 |
| [Cadastro de Pessoas](./pessoas/cadastro-pessoas/README.md) | `PES-CAD` | GPE003 – Manter Pessoa | 7 |
| [Cadastro de Eventos](./eventos/cadastro-eventos/README.md) | `EVT-CAD` | GPE004 – Manter Evento | 9 |
| [Participantes](./eventos/participantes/README.md) | `EVT-PAR` | GPE005 – Gerenciar Participante | 15 |
| [Legendas](./eventos/legendas/README.md) | `EVT-LEG` | GPE006 – Gerenciar Regras de Legendas | 14 |

**55 features** em 6 Feature Sets e 3 domínios.

---

## Rastreabilidade: ticket → spec → código

| Ticket (AIM) | Feature | Domínio | Status | Contagem | PF | CFP | Repositórios |
|---|---|---|---|---|---|---|---|
| [`PDTIC25148-34`](../analise-impacto/AIM-PDTIC25148-34.md) | [EVT-LEG-01: Consultar Configuração de Legendas](./eventos/legendas/f-consultar-configuracao-legendas.md) | Eventos | ✏️ Rascunho | ✅ | 4 | — | sistema_mesa_checkin_frontend · sistema_mesa_checkin_backend |
| [`PDTIC25148-34`](../analise-impacto/AIM-PDTIC25148-34.md) | [EVT-LEG-02: Adicionar Bloco de Legenda ao Evento](./eventos/legendas/f-adicionar-bloco-legenda.md) | Eventos | ✏️ Rascunho | ✅ | 6 | — | sistema_mesa_checkin_frontend · sistema_mesa_checkin_backend |
| [`PDTIC25148-34`](../analise-impacto/AIM-PDTIC25148-34.md) | [EVT-LEG-03: Configurar Condições de Legenda](./eventos/legendas/f-configurar-condicoes-legenda.md) | Eventos | ✏️ Rascunho | ✅ | 4 | — | sistema_mesa_checkin_frontend · sistema_mesa_checkin_backend |
| [`PDTIC25148-34`](../analise-impacto/AIM-PDTIC25148-34.md) | [EVT-LEG-04: Reordenar Blocos de Legenda](./eventos/legendas/f-reordenar-blocos-legenda.md) | Eventos | ✏️ Rascunho | ✅ | 3 | — | sistema_mesa_checkin_frontend · sistema_mesa_checkin_backend |
| [`PDTIC25148-34`](../analise-impacto/AIM-PDTIC25148-34.md) | [EVT-LEG-05: Remover Bloco de Legenda do Evento](./eventos/legendas/f-remover-bloco-legenda.md) | Eventos | ✏️ Rascunho | ✅ | 3 | — | sistema_mesa_checkin_frontend · sistema_mesa_checkin_backend |
| [`PDTIC25148-34`](../analise-impacto/AIM-PDTIC25148-34.md) | [EVT-LEG-06: Simular Aplicação de Legendas](./eventos/legendas/f-simular-aplicacao-legendas.md) | Eventos | ✏️ Rascunho | ✅ | 5 | — | sistema_mesa_checkin_frontend · sistema_mesa_checkin_backend |
| [`PDTIC25148-34`](../analise-impacto/AIM-PDTIC25148-34.md) | [EVT-LEG-07: Gerar Legendas do Evento](./eventos/legendas/f-gerar-legendas-evento.md) | Eventos | ✏️ Rascunho | ✅ | 4 | — | sistema_mesa_checkin_frontend · sistema_mesa_checkin_backend |
| [`PDTIC25148-34`](../analise-impacto/AIM-PDTIC25148-34.md) | [EVT-LEG-08: Salvar Preset de Legendas](./eventos/legendas/f-salvar-preset-legendas.md) | Eventos | ✏️ Rascunho | ✅ | 4 | — | sistema_mesa_checkin_frontend · sistema_mesa_checkin_backend |
| [`PDTIC25148-34`](../analise-impacto/AIM-PDTIC25148-34.md) | [EVT-LEG-09: Carregar Configuração de Legendas](./eventos/legendas/f-carregar-configuracao-legendas.md) | Eventos | ✏️ Rascunho | ✅ | 15 | — | sistema_mesa_checkin_frontend · sistema_mesa_checkin_backend |
| [`PDTIC25148-34`](../analise-impacto/AIM-PDTIC25148-34.md) | [EVT-LEG-10: Excluir Preset de Legendas](./eventos/legendas/f-excluir-preset-legendas.md) | Eventos | ✏️ Rascunho | ✅ | 3 | — | sistema_mesa_checkin_frontend · sistema_mesa_checkin_backend |
| [`PDTIC25148-34`](../analise-impacto/AIM-PDTIC25148-34.md) | [EVT-LEG-11: Pesquisar Blocos de Legenda](./eventos/legendas/f-pesquisar-blocos-legenda.md) | Eventos | ✏️ Rascunho | ✅ | 3 | — | sistema_mesa_checkin_frontend · sistema_mesa_checkin_backend |
| [`PDTIC25148-34`](../analise-impacto/AIM-PDTIC25148-34.md) | [EVT-LEG-12: Cadastrar Bloco de Legenda](./eventos/legendas/f-cadastrar-bloco-legenda.md) | Eventos | ✏️ Rascunho | ✅ | 3 | — | sistema_mesa_checkin_frontend · sistema_mesa_checkin_backend |
| [`PDTIC25148-34`](../analise-impacto/AIM-PDTIC25148-34.md) | [EVT-LEG-13: Editar Bloco de Legenda](./eventos/legendas/f-editar-bloco-legenda.md) | Eventos | ✏️ Rascunho | ✅ | 3 | — | sistema_mesa_checkin_frontend · sistema_mesa_checkin_backend |
| [`PDTIC25148-34`](../analise-impacto/AIM-PDTIC25148-34.md) | [EVT-LEG-14: Excluir Bloco de Legenda](./eventos/legendas/f-excluir-bloco-legenda.md) | Eventos | ✏️ Rascunho | ✅ | 3 | — | sistema_mesa_checkin_frontend · sistema_mesa_checkin_backend |
| [`PDTIC25148-34`](../analise-impacto/AIM-PDTIC25148-34.md) | [EVT-PAR-04: Consultar Legenda do Participante](./eventos/participantes/f-consultar-legenda-participante.md) | Eventos | ✏️ Rascunho | ✅ | 7 | — | sistema_mesa_checkin_frontend · sistema_mesa_checkin_backend |
| [`PDTIC25148-34`](../analise-impacto/AIM-PDTIC25148-34.md) | [EVT-PAR-05: Alterar Legenda do Participante](./eventos/participantes/f-alterar-legenda-participante.md) | Eventos | ✏️ Rascunho | ✅ | 3 | — | sistema_mesa_checkin_frontend · sistema_mesa_checkin_backend |
| [`PDTIC25148-35`](../analise-impacto/AIM-PDTIC25148-35.md) | [EVT-PAR-01: Pesquisar Participantes](./eventos/participantes/f-pesquisar-participantes.md) | Eventos | ✏️ Rascunho | ✅ | 16 | — | sistema_mesa_checkin_frontend · sistema_mesa_checkin_backend |
| [`PDTIC25148-35`](../analise-impacto/AIM-PDTIC25148-35.md) | [EVT-PAR-04: Consultar Legenda do Participante](./eventos/participantes/f-consultar-legenda-participante.md) | Eventos | ✏️ Rascunho | ✅ | 7 | — | sistema_mesa_checkin_frontend · sistema_mesa_checkin_backend |

> ⚠️ **A tabela traz só os tickets com AIM aberta.** As 55 features nasceram por engenharia reversa: a origem da maioria é o documento legado e o código, não um ticket com AIM, e esta tabela só recebe o par ticket ↔ feature quando a AIM existe (`audit-trace-links`). Em 2026-10-04 foram abertas, já na entrega, as AIMs de `PDTIC25148-34` *Configuração de Legendas por Evento* e de `PDTIC25148-35` *Melhorias na Listagem de Pessoas Confirmadas*; os demais tickets do Jira (`PDTIC25148`) seguem citados em texto na `## Origem` dos N3. A lista completa das features está na *Esteira de checkpoints*, abaixo. Falta abrir a AIM de `PDTIC25148-36` *CRM - Importação de convidados*, o terceiro ticket que estava em teste em 2026-09-30.

<!--
  Ticket: chave do ticket que originou ou alterou a feature (seção "Origem" do N3),
  com o link da AIM do ticket (`analise-impacto/AIM-<CHAVE>.md`).
  Uma feature pode ter mais de um ticket; um ticket, mais de uma feature.
  Status: o `estado` do front-matter do N3, com o ícone da legenda abaixo — um N3
    recém-gerado é ✏️ Rascunho. Avança com os gates (um PR por checkpoint, que
    regenera a seção Esteira de checkpoints); nunca se escreve adiantado. Vale o mesmo
    na ## Features da AIM do ticket: o audit compara as duas.
  PF: a opção CT (PROMPT_CONTAGEM, passo 5) o propaga depois da revisão — o 3B e o 4B
    contam só no N3. Ver critérios em global/SIZING.md.
  Contagem: status de contagem APF da feature — espelha `contagem.pendente` do
    front-matter do N3 (INDEPENDENTE dos gates/Status). ✅ = contada (revisão de PF
    feita para a última alteração do changelog, mesmo Δ PF = 0) · 📋 = pendente
    (há alteração ainda não revisada). Alteração de spec (3A/4A/CRUD/WIZARD/RT/R1/R3) → 📋;
    revisão via opção CT / PROMPT_CONTAGEM → ✅. Lista consolidada de pendentes em
    global/CONTAGEM-PF.md → ## Pendências de contagem.
  Totais vigentes excluem features ❌ Deprecadas.

  GATES DETERMINÍSTICOS desta tabela:
  - `node scripts/audit-trace-links.mjs` prova que cada par ticket↔feature está
    nos TRÊS lugares (## Origem do N3 + ## Features da AIM + esta linha)
    — roda no hook de gravação e no CI (engine/templates/ci/spec-guard.yml).
  - `node scripts/suspect-links.mjs --mark` troca o Status para ⚠️ Revisão necessária
    quando o outro lado do elo mudou depois da última verificação (carimbos
    trace-verified). O ⚠️ gravado por ele é tolerado pelo audit até a reverificação.
-->

**Total vigente: 118 PF · — CFP** *(parcial: 89 PF de transações, em 17 das 55 features, e 29 PF dos arquivos lógicos de Eventos, contados em 2026-10-04; as outras 38 features estão em `global/CONTAGEM-PF.md` → Pendências de contagem; critérios em `global/SIZING.md`)*

---

<!-- GATES:INICIO -->
## Esteira de checkpoints (gates)

> ⚙️ **Seção gerada por `scripts/gates.py` — não editar à mão.** Espelha o estado de cada feature na esteira (CP1 requisitos (PO/Negócio) → CP2 modelo-dados (DBA/Arquiteto)). Reflete o estado em **2026-10-04**.

| Feature | Origem | Estado | Situação |
|---|---|---|---|
| `EVT-LEG-04` ([spec](./eventos/legendas/f-reordenar-blocos-legenda.md)) | PDTIC25148-34 | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-LEG-05` ([spec](./eventos/legendas/f-remover-bloco-legenda.md)) | PDTIC25148-34 | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-LEG-08` ([spec](./eventos/legendas/f-salvar-preset-legendas.md)) | PDTIC25148-34 | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-LEG-09` ([spec](./eventos/legendas/f-carregar-configuracao-legendas.md)) | PDTIC25148-34 | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-LEG-10` ([spec](./eventos/legendas/f-excluir-preset-legendas.md)) | PDTIC25148-34 | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-LEG-11` ([spec](./eventos/legendas/f-pesquisar-blocos-legenda.md)) | PDTIC25148-34 | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-LEG-12` ([spec](./eventos/legendas/f-cadastrar-bloco-legenda.md)) | PDTIC25148-34 | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-LEG-13` ([spec](./eventos/legendas/f-editar-bloco-legenda.md)) | PDTIC25148-34 | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-LEG-14` ([spec](./eventos/legendas/f-excluir-bloco-legenda.md)) | PDTIC25148-34 | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `ACE-AUT-01` ([spec](./acesso-usuarios/autenticacao/f-autenticar-usuario.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `ACE-AUT-02` ([spec](./acesso-usuarios/autenticacao/f-encerrar-sessao.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `ACE-AUT-03` ([spec](./acesso-usuarios/autenticacao/f-recuperar-senha.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `ACE-AUT-04` ([spec](./acesso-usuarios/autenticacao/f-alterar-senha.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `ACE-AUT-05` ([spec](./acesso-usuarios/autenticacao/f-alterar-foto-perfil.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `ACE-AUT-06` ([spec](./acesso-usuarios/autenticacao/f-consultar-dados-usuario.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `ACE-USU-01` ([spec](./acesso-usuarios/usuarios/f-pesquisar-usuarios.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `ACE-USU-02` ([spec](./acesso-usuarios/usuarios/f-cadastrar-usuario.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `ACE-USU-03` ([spec](./acesso-usuarios/usuarios/f-editar-usuario.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `ACE-USU-04` ([spec](./acesso-usuarios/usuarios/f-excluir-usuario.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-CAD-01` ([spec](./eventos/cadastro-eventos/f-pesquisar-eventos.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-CAD-02` ([spec](./eventos/cadastro-eventos/f-cadastrar-evento.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-CAD-03` ([spec](./eventos/cadastro-eventos/f-editar-evento.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-CAD-04` ([spec](./eventos/cadastro-eventos/f-visualizar-evento.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-CAD-05` ([spec](./eventos/cadastro-eventos/f-excluir-evento.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-CAD-06` ([spec](./eventos/cadastro-eventos/f-definir-evento-principal.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-CAD-07` ([spec](./eventos/cadastro-eventos/f-carregar-convidados.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-CAD-08` ([spec](./eventos/cadastro-eventos/f-carregar-confirmados.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-CAD-09` ([spec](./eventos/cadastro-eventos/f-importar-inscritos-crm.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-LEG-01` ([spec](./eventos/legendas/f-consultar-configuracao-legendas.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-LEG-02` ([spec](./eventos/legendas/f-adicionar-bloco-legenda.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-LEG-03` ([spec](./eventos/legendas/f-configurar-condicoes-legenda.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-LEG-06` ([spec](./eventos/legendas/f-simular-aplicacao-legendas.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-LEG-07` ([spec](./eventos/legendas/f-gerar-legendas-evento.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-PAR-01` ([spec](./eventos/participantes/f-pesquisar-participantes.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-PAR-02` ([spec](./eventos/participantes/f-cadastrar-participante.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-PAR-03` ([spec](./eventos/participantes/f-registrar-check-in.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-PAR-04` ([spec](./eventos/participantes/f-consultar-legenda-participante.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-PAR-05` ([spec](./eventos/participantes/f-alterar-legenda-participante.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-PAR-06` ([spec](./eventos/participantes/f-remover-legenda-participante.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-PAR-07` ([spec](./eventos/participantes/f-consultar-mapa-assentos.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-PAR-08` ([spec](./eventos/participantes/f-atribuir-assento-participante.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-PAR-09` ([spec](./eventos/participantes/f-remover-assento-participante.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-PAR-10` ([spec](./eventos/participantes/f-registrar-atendimento.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-PAR-11` ([spec](./eventos/participantes/f-liberar-assentos.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-PAR-12` ([spec](./eventos/participantes/f-buscar-pessoa-mesa.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-PAR-13` ([spec](./eventos/participantes/f-alterar-confirmacao-presenca.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-PAR-14` ([spec](./eventos/participantes/f-exportar-participantes.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `EVT-PAR-15` ([spec](./eventos/participantes/f-exportar-mapa-assentos.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `PES-CAD-01` ([spec](./pessoas/cadastro-pessoas/f-pesquisar-pessoas.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `PES-CAD-02` ([spec](./pessoas/cadastro-pessoas/f-cadastrar-pessoa.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `PES-CAD-03` ([spec](./pessoas/cadastro-pessoas/f-editar-pessoa.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `PES-CAD-04` ([spec](./pessoas/cadastro-pessoas/f-excluir-pessoa.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `PES-CAD-05` ([spec](./pessoas/cadastro-pessoas/f-carregar-grupos-trabalho.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `PES-CAD-06` ([spec](./pessoas/cadastro-pessoas/f-carregar-temas.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |
| `PES-CAD-07` ([spec](./pessoas/cadastro-pessoas/f-carregar-historico-participacao.md)) | — | ✏️ rascunho | aguardando **requisitos** (PO/Negócio) |

**0** de **55** feature(s) prontas para desenvolvimento.
<!-- GATES:FIM -->

---

<!-- PENDENCIAS:INICIO -->
## Pendências de especificação

> ⚙️ **Seção gerada pelo PROMPT_PENDENCIAS (PD) — não editar à mão.**
> Varre as fontes (AIMs em `analise-impacto/`, READMEs de N2, N3 com ⚠️) e espelha aqui o que está
> **pendente de especificar**. Edições manuais entre os marcadores são sobrescritas na
> próxima execução. Reflete o estado em **2026-09-30** — rode o **PD** para atualizar.

> ⚠️ O **PD ainda não foi rodado** nesta instância. As tabelas abaixo trazem só o que a engenharia reversa já sabe que falta; as lacunas (❓), as inferências (🔍) e as divergências (⚠️) de cada feature estão consolidadas em [`REVISAO-CONVERSAO.md`](../REVISAO-CONVERSAO.md).

### Existência (falta N3)

> Algo é conhecido como necessário mas ainda **não tem N3**. Resolva pela rota indicada.

| Item | Nível | Origem | Rota |
|---|---|---|---|
| Resetar Regras de Legenda | N3 | GPE006 – Gerenciar Regras de Legendas (documento legado) · N2 [Legendas](./eventos/legendas/README.md) | ⚠️ Decisão do PO: a funcionalidade está no documento e **não existe mais** no sistema (modelo reformulado). Ou sai do documento, ou volta a ser pedida — rota 3A |
| Inativar Usuário | N3 | Código (rotina existente e sem acionamento na tela) · N2 [Usuários](./acesso-usuarios/usuarios/README.md) | ❓ Decisão do PO: a situação Ativo ou Inativo é exibida, mas não há ação de tela — rota 3A, se for desejada |

### Conteúdo (⚠️ em aberto)

> O artefato **existe**, mas tem lacunas/suposições aguardando esclarecimento.

| Feature | Lacuna | Arquivo |
|---|---|---|
| Todas as 55 features | Divergências documento × código, lacunas e suspeitas de defeito levantadas na engenharia reversa | [REVISAO-CONVERSAO.md](../REVISAO-CONVERSAO.md) |
<!-- PENDENCIAS:FIM -->

---

## Entidades consolidadas

| Entidade | Domínio | N1 de origem |
|---|---|---|
| Usuario | Acesso e Usuários | [acesso-usuarios/README.md](./acesso-usuarios/README.md) |
| PerfilAcesso | Acesso e Usuários | [acesso-usuarios/README.md](./acesso-usuarios/README.md) |
| Pessoa | Pessoas | [pessoas/README.md](./pessoas/README.md) |
| GrupoTrabalhoPessoa | Pessoas | [pessoas/README.md](./pessoas/README.md) |
| TemaPessoa | Pessoas | [pessoas/README.md](./pessoas/README.md) |
| HistoricoPessoa | Pessoas | [pessoas/README.md](./pessoas/README.md) |
| Arquivo | Pessoas | [pessoas/README.md](./pessoas/README.md) |
| Evento | Eventos | [eventos/README.md](./eventos/README.md) |
| TipoEvento | Eventos | [eventos/README.md](./eventos/README.md) |
| TipoMesa | Eventos | [eventos/README.md](./eventos/README.md) |
| CadeiraMesa | Eventos | [eventos/README.md](./eventos/README.md) |
| EventoPessoa | Eventos | [eventos/README.md](./eventos/README.md) |
| Legenda | Eventos | [eventos/README.md](./eventos/README.md) |
| EventoLegenda | Eventos | [eventos/README.md](./eventos/README.md) |
| EventoLegendaCondicao | Eventos | [eventos/README.md](./eventos/README.md) |
| EventoPessoaLegenda | Eventos | [eventos/README.md](./eventos/README.md) |
| PresetLegenda | Eventos | [eventos/README.md](./eventos/README.md) |

---

## Eventos do sistema

| Evento | Publicado por | Consumido por | Payload principal |
|---|---|---|---|
| — | — | — | O sistema não publica nem consome eventos entre domínios: as integrações são chamadas diretas 💻 |

---

## Mapa de integrações entre domínios

| Domínio origem | Depende de | Tipo | Descrição |
|---|---|---|---|
| Eventos | Pessoas | Leitura | Dados da pessoa na lista de participantes e no mapa; grupo de trabalho, papel, tema, cargo e nome fantasia nas condições de legenda; histórico de participação no mapa |
| Eventos | Pessoas | Escrita | As cargas de convidados e de confirmados, a importação do CRM e o cadastro na recepção criam ou atualizam a pessoa |
| Pessoas | Eventos | Leitura | A participação em evento impede a exclusão da pessoa |
| Eventos | Acesso e Usuários | Leitura | O perfil do usuário define o que a lista de participantes e o mapa mostram |
| Acesso e Usuários | Eventos | Leitura | O evento principal é o destino da Secretaria Mesa e da Secretaria Check-In depois de entrar |
| Acesso e Usuários | Serviços corporativos da CNI (externo) | Leitura / Escrita | Autenticação, senha, usuários e perfis |
| Eventos | CRM da CNI — Dynamics 365 (externo) | Leitura | Inscritos aprovados e confirmados da campanha do evento |

---

## Legenda de status

Estados da **esteira de checkpoints**, derivados dos `gates` no front-matter de cada N3.
A próxima etapa só ocorre após a aprovação da anterior — ordem: requisitos → modelo-dados → testes → código.

| Ícone | Estado | Checkpoint | Descrição |
|---|---|---|---|
| ✏️ | rascunho | — | N3 em elaboração, nenhum gate aprovado |
| 📝 | requisitos-aprovados | CP1 (PO) | Requisitos validados — aguardando modelo de dados |
| 🧱 | modelo-validado | CP2 (DBA) | Modelo físico de dados validado — aguardando testes |
| 📋 | especificado | CP3 (QA) | **Pronto para desenvolvimento** (CP1+CP2+CP3 aprovados) |
| 🔄 | em-desenvolvimento | — | Implementação em andamento (estado manual) |
| ✅ | implementado | CP4 (code review) | Em produção, rastreabilidade preenchida |
| ⚠️ | revisao-necessaria | — | Spec e código (ou spec e ticket) divergem — a spec mudou depois da implementação, o código mudou sem a spec, ou o outro lado de um elo mudou (estado manual; o `suspect-links` também o marca) |
| ❌ | deprecado | — | Feature removida do sistema |
