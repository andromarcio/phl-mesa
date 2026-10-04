<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: EVT-CAD-03
feature_set: EVT-CAD
dominio: EVT
entidade: Evento
data_model_ref: data-models/eventos.md#evento
endpoints: []
error_codes: []
depende_de: ["EVT-CAD-01"]
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

# Editar Evento
> **Nível 3** - Feature Set: Cadastro de Eventos — Major Feature Set: Eventos - `EVT-CAD-03`

## Descrição

Permite que o Administrador altere os dados básicos de um evento já cadastrado, inclusive o nome; a pesquisa de eventos e as demais telas do evento passam a mostrar os dados novos, sem que os participantes, os check-ins e os assentos sejam tocados.

A edição é aberta pelo ícone Editar evento, em cada linha da lista de eventos. A tela vem preenchida com os dados atuais; o Administrador altera o que precisa e aciona Salvar, e o sistema volta à lista de eventos.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE004 – Manter Evento v1.1, de 16/12/2025 (documento legado), funcionalidade "Editar Evento" ⚠️ sem chave na ferramenta de demandas | Criação | — Alterar os dados básicos do cadastro do evento, inclusive o nome, deixando participantes, check-in e demais funcionalidades de administração do evento para outras funcionalidades. O campo Código da Campanha não está no documento: vem do ticket do Jira `PDTIC25148-36`, em teste, critério CA01; AIM ainda não aberta 💻 |

---

<div class="dev-only">

## Superfície

**Tela própria** — rota `/eventos/detail/edit/:id`

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Incluir / Editar Evento" de GPE004

---

</div>

## Regras de negócio

1. Todos os dados básicos do evento podem ser alterados, inclusive o nome.
2. A alteração obedece às mesmas exigências da inclusão: Nome do Evento (de 3 a 100 caracteres), Data e Hora, Local (de 3 a 200 caracteres), Tipo de Evento, Tipo de Mesa e Participantes (de 1 a 10.000) são necessários; o Código da Campanha (até 50 caracteres) e a imagem são opcionais. 💻 ⚠️ GPE004 informa tamanho 255 para o nome e para o local 📄.
3. A edição altera somente os dados básicos: os participantes, os check-ins e os assentos do evento ficam como estavam.
4. Trocar o tipo de mesa não refaz os assentos gerados na inclusão. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 5
5. ⚠️ Depois da troca do tipo de mesa, o evento fica com o desenho do tipo novo e os assentos do tipo antigo: de Retangular para Retangular Invertido, sobram os assentos B35, C35, F29 a F32 e H29 a H36 e faltam os assentos E24 a E30; no sentido contrário, é o inverso. 💻 Suspeita de defeito; o efeito sobre o mapa foi inferido do código, sem execução 🔍.
6. A edição conserva a condição de evento principal que o evento tinha no momento em que foi aberto para edição. 💻
7. A imagem do evento pode ser trocada ou retirada; a imagem anterior continua guardada, sem uso. 💻 ⚠️
8. Todo salvamento regrava o evento como não excluído. 💻 ⚠️ O evento excluído, aberto por quem tem o endereço dele e salvo, volta a constar na pesquisa de eventos 🔍 — suspeita de defeito.
9. Não há controle de alteração simultânea: entre duas edições do mesmo evento, vale a que salvar por último. 🔍

---

## Cenários

```gherkin
Feature: Editar evento

  Background:
    Given que o usuário está autenticado no GPE
    And está na lista de eventos

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Abrir a edição
    When o usuário aciona "Editar evento" na linha de "Reunião de Diretoria"
    Then o sistema abre a tela "Editar Evento" com os campos preenchidos com os dados atuais do evento

  Scenario: Alterar dados básicos
    Given que o usuário abriu a edição de "Reunião de Diretoria"
    When altera "Local" para "Auditório da CNI" e "Participantes" para "120"
    And aciona "Salvar"
    Then o sistema grava os novos dados do evento
    And exibe: "Sucesso" com o detalhe "Evento atualizado com sucesso"
    And volta à tela Eventos, onde a linha do evento mostra os dados alterados
    # 💻 a mensagem de sucesso fica na tela até ser fechada pelo usuário

  Scenario: Alterar o nome do evento
    Given que o usuário abriu a edição de "Reunião de Diretoria"
    When altera "Nome do Evento" para "Reunião Ordinária de Diretoria" e aciona "Salvar"
    Then o evento passa a ser listado com o novo nome
    And seus participantes, check-ins e assentos permanecem os mesmos

  Scenario: Informar o Código da Campanha em evento que não o tinha
    Given que o usuário abriu a edição de um evento sem Código da Campanha
    When preenche "Código da Campanha" com "CMP-03460-L2K8" e aciona "Salvar"
    Then o sistema grava o código
    And a importação de inscritos do CRM fica habilitada para o evento

  Scenario: Trocar a imagem do evento
    Given que o evento em edição tem uma imagem
    When o usuário adiciona outra imagem em "Arquivo" e aciona "Salvar"
    Then o evento passa a ter a nova imagem
    # 💻 a imagem anterior continua guardada, sem uso

  Scenario: Retirar a imagem do evento
    Given que o evento em edição tem uma imagem
    When o usuário aciona a lixeira ao lado do nome do arquivo
    Then o sistema exibe: "Anexo removido"
    And, depois de "Salvar", o evento fica sem imagem

  Scenario: Desistir da edição
    When o usuário aciona "Cancelar" na tela "Editar Evento"
    Then o sistema volta à tela Eventos sem gravar nada

  # ── Erros de validação ─────────────────────────────────────────

  # ← MESSAGE-DICTIONARY: BASELINE
  Scenario: Campo obrigatório esvaziado
    Given que o usuário abriu a edição de um evento
    When apaga o conteúdo de "Nome do Evento"
    Then o sistema exibe abaixo do campo: "Este campo é obrigatório"
    And o botão "Salvar" fica desabilitado
    # o mesmo vale para "Data e Hora", "Local", "Tipo de Evento", "Tipo de Mesa" e "Participantes"

  # ← MESSAGE-DICTIONARY: BASELINE
  Scenario: Nome ou local com menos de 3 caracteres
    Given que o usuário abriu a edição de um evento
    When altera "Local" para "AB"
    Then o sistema exibe abaixo do campo: "Mínimo de 3 caracteres"
    And o botão "Salvar" fica desabilitado

  Scenario: Arquivo que não é imagem
    Given que o usuário abriu a edição de um evento
    When adiciona em "Arquivo" um arquivo que não é imagem
    Then o sistema recusa o arquivo e exibe "<nome do arquivo>: Tipo de arquivo não permitido" com o detalhe "Tipos permitidos: image/*"

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Trocar o tipo de mesa de evento que já tem assentos
    Given que o evento foi incluído com o tipo de mesa "Retangular" e tem 181 assentos
    When o usuário altera "Tipo de Mesa" para "Retangular Invertido" e aciona "Salvar"
    Then o sistema grava o novo tipo de mesa
    And o evento continua com os 181 assentos gerados na inclusão
    # ⚠️ 💻 suspeita de defeito: o mapa passa a ser desenhado no formato invertido, com assentos que não correspondem a ele (regra 5)
    # ❓ nenhuma fonte diz o que deve acontecer com os participantes já colocados em assentos que o novo formato não tem

  Scenario: Evento principal trocado enquanto a edição estava aberta
    Given que o usuário abriu a edição de "Reunião de Diretoria", que era o evento principal
    And nesse intervalo outro Administrador definiu "Comitê de Inovação" como principal
    When o usuário aciona "Salvar"
    Then "Reunião de Diretoria" é regravado como principal, e o sistema fica com dois eventos principais
    # ⚠️ 🔍 inferido do código (regra 6), sem execução: contraria a regra de um único evento principal

  Scenario: Dois Administradores editam o mesmo evento
    Given que dois Administradores abriram a edição do mesmo evento
    When cada um altera um dado e aciona "Salvar"
    Then prevalecem, por inteiro, os dados de quem salvou por último
    # 🔍 não há controle de alteração simultânea

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Editar Evento" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Eventos › Cadastro, e a edição não fica ao alcance dele
    # ⚠️ o ícone "Editar evento" e a tela "Editar Evento" não conferem o perfil; quem recusa a gravação é o servidor — ver a nota da matriz no N2
    # ❓ o que a tela mostra quando o servidor recusa depende da resposta do serviço corporativo de acesso, que o código não revela

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Falha ao salvar
    Given que a gravação do evento falha no servidor
    When o usuário aciona "Salvar"
    Then o sistema permanece na tela "Editar Evento", com os dados digitados
    And exibe: "Erro" com o detalhe "Erro ao salvar evento. Verifique os dados e tente novamente."

  Scenario: Evento não encontrado
    Given que o evento não existe mais no servidor
    When o usuário abre a edição pelo endereço da tela
    Then a tela "Editar Evento" abre com os campos em branco, sem nenhum aviso
    # ⚠️ 🔍 a falha na leitura do evento não é tratada pela tela

  Scenario: Evento excluído editado pelo endereço
    Given que o evento "Reunião de Diretoria" foi excluído
    When o usuário abre a edição dele pelo endereço da tela e aciona "Salvar"
    Then o evento volta a constar na pesquisa de eventos
    # ⚠️ 🔍 suspeita de defeito (regra 8): salvar desfaz a exclusão
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| Nome do Evento | Evento | entrada do usuário | editável | texto | sim | De 3 a 100 caracteres, com contador ao lado do campo 💻. ⚠️ GPE004 informa tamanho 255 📄 |
| Data e Hora | Evento | entrada do usuário | editável | data e hora | sim | Dia, mês, ano e hora no formato de 24 horas. Aceita qualquer data, inclusive passada 💻 |
| Local | Evento | entrada do usuário | editável | texto | sim | De 3 a 200 caracteres, com contador ao lado do campo 💻. ⚠️ GPE004 informa tamanho 255 📄 |
| Tipo de Evento | TipoEvento | entrada do usuário | editável | seleção → TipoEvento | sim | Uma opção. Tipos existentes: Reunião, Comitê e Seminário |
| Tipo de Mesa | TipoMesa | entrada do usuário | editável | seleção → TipoMesa | sim | Uma opção. Tipos existentes: Retangular e Retangular Invertido 💻. ⚠️ A troca não refaz os assentos (regras 4 e 5) |
| Participantes | Evento | entrada do usuário | editável | número | sim | Inteiro de 1 a 10.000 💻. Não interfere nos assentos |
| Código da Campanha | Evento | entrada do usuário | editável | texto | não | Até 50 caracteres 💻. Não consta em GPE004: vem do ticket `PDTIC25148-36` |
| Arquivo | Arquivo | entrada do usuário | editável | arquivo | não | Uma imagem, com até 200 MB 💻. Pode ser trocada ou retirada |

*Todos os campos vêm preenchidos com o que está gravado no evento. Não há campo somente leitura: GPE004 diz que "todos os dados podem ser editados, inclusive o nome".*

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| Principal | O que o evento tinha quando a edição foi aberta (regra 6) 💻 | A cada salvamento |
| Excluído | Não (regra 8) 💻 ⚠️ | A cada salvamento |

*O evento não guarda data de alteração nem quem o alterou 💻.*

---

## Comportamento de tela

### Onde fica
Na tela "Editar Evento", aberta pelo ícone de lápis com a dica "Editar evento", em cada linha da lista de eventos. É a mesma tela do cadastro, com os mesmos campos, textos de orientação e ajudas; muda o título, e o botão "Salvar" traz um ícone de confirmação no lugar do sinal de mais. O rodapé traz o texto "Campos com * são obrigatórios" e os botões "Cancelar" e "Salvar"; o botão "Salvar" fica desabilitado enquanto houver campo obrigatório vazio ou inválido.

A imagem já gravada aparece como um botão com o nome do arquivo (dica "Download"), que a baixa, ao lado de uma lixeira (dica "Excluir"), que a retira do evento.

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Sem indicador na abertura: os campos são preenchidos instantes depois de a tela abrir 💻. Botão "Salvar" em estado de carregamento enquanto a gravação não responde |
| Erro de validação | Mensagem em vermelho abaixo do campo — "Este campo é obrigatório", "Mínimo de 3 caracteres" — e botão "Salvar" desabilitado |
| Erro de servidor | "Erro" com o detalhe "Erro ao salvar evento. Verifique os dados e tente novamente."; a tela permanece aberta com os dados digitados. ⚠️ A falha ao ler o evento, na abertura, não gera aviso 🔍 |
| Sucesso | "Sucesso" com o detalhe "Evento atualizado com sucesso", que fica visível até ser fechada, e retorno à tela Eventos |
| Empty state | Não se aplica — a tela abre com os dados do evento |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Depois de salvar, a pesquisa de eventos e a visualização do evento mostram os dados alterados | Cenário "Alterar dados básicos" |
| SC-02 | Nenhuma edição altera os participantes, os check-ins ou os assentos do evento | Regra 3 · cenário "Alterar o nome do evento" |
| SC-03 | Nenhuma alteração é gravada pela tela com campo obrigatório vazio ou fora dos limites | Regra 2 · cenário "Campo obrigatório esvaziado" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Editar Evento | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade Evento

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Tela "Editar Evento" — a mesma do cadastro: leitura do evento, preenchimento e gravação | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento/pages/evento/create/evento-create.component.ts` (linhas 65–80 e 147–210) e `.html` (linhas 7–10 e 258–283) | — |
| Leitura do evento — operação `GET /administracao/eventos/{id}` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoController.java` (linhas 85–90) | — |
| Gravação usada pela tela — operação `POST /administracao/eventos`, a mesma da inclusão, com o identificador do evento | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/EventoServiceImpl.java` (linhas 166–178) | — |
| Operação `PUT /administracao/eventos/{id}` — existe e não é chamada pela tela | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/EventoServiceImpl.java` (linhas 190–210) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

⚠️ A tela grava a edição pela operação de inclusão, que regrava o evento inteiro — daí as regras 6 e 8 — e grava o conteúdo da imagem nova. A operação de alteração (`PUT`), que a tela não usa, preserva Excluído e Principal, mas não grava o conteúdo de uma imagem nova. Nenhuma das duas refaz os assentos.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE004 – Manter Evento (funcionalidade "Editar Evento"), do código e do ticket `PDTIC25148-36` (campo Código da Campanha) |

---

*Feature Set: Cadastro de Eventos · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
