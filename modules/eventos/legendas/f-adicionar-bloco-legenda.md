<!-- docqui: 4.0.2 | prompt: PROMPT_CONTAGEM | atualizado: 2026-10-04 -->
---
id: EVT-LEG-02
feature_set: EVT-LEG
dominio: EVT
entidade: EventoLegenda
data_model_ref: data-models/eventos.md#eventolegenda
endpoints: []
error_codes: []
depende_de: ["EVT-LEG-01", "EVT-LEG-12"]
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
  pendente: false
  revisada_em: "2026-10-04"
  revisada_ate: "PDTIC25148-34"
---

# Adicionar Bloco de Legenda ao Evento
> **Nível 3** - Feature Set: Legendas — Major Feature Set: Eventos - `EVT-LEG-02`

## Descrição

Permite que o Administrador adicione à configuração de legendas de um evento um ou mais blocos do catálogo; cada bloco entra no fim da ordem, ainda sem condições, e passa a fazer parte das legendas daquele evento.

Na tela Configuração de Legendas, o botão Adicionar bloco abre uma janela com os blocos do catálogo que ainda não estão no evento. O usuário busca pelo nome, marca os blocos que quer e aciona Adicionar ao evento.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE006 – Gerenciar Regras de Legendas v1.0, de 03/10/2025 (documento legado), funcionalidade "Incluir Regra de Legenda" ⚠️ sem chave na ferramenta de demandas | Criação | — Pôr uma legenda em vigor no evento, o que o documento fazia ativando a legenda antes de incluir a regra. As condições, que o documento trata na mesma funcionalidade, estão em Configurar Condições de Legenda `EVT-LEG-03` |
| [`PDTIC25148-34`](../../../analise-impacto/AIM-PDTIC25148-34.md) | Alteração | `CA-01` — adicionar bloco existente, pesquisando e selecionando no catálogo. O atalho "Adicionar bloco", oferecido quando a busca não encontra nada, fica nesta janela, mas o critério que o pede (criar bloco a partir da busca) pertence a Cadastrar Bloco de Legenda `EVT-LEG-12`, que faz a criação |
<!-- trace-verified: PDTIC25148-34 @ f6bae69fe29f -->

---

<div class="dev-only">

## Superfície

**Modal** — origem: Consultar Configuração de Legendas `EVT-LEG-01` (`/regras-legenda/:eventoId`), botão "Adicionar bloco" da barra de ações e do estado vazio

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada. A imagem "Listar Regras de Legendas" de GPE006 mostra a chave "Ativa" ou "Inativa", que fazia o papel desta feature no modelo anterior ⚠️

---

</div>

## Regras de negócio

1. Só entra na configuração do evento o bloco que existe no catálogo. 💻
2. Uma mesma legenda aparece uma única vez na configuração do evento: o bloco que já está no evento não pode ser adicionado de novo. 💻
3. Qualquer bloco do catálogo pode ser adicionado a qualquer evento. 💻 ⚠️ GPE006 lista doze legendas configuráveis fixas, de "Comitê estratégico" a "Assento livre", e diz, na imagem do documento, que "Anfitrião e Palestrantes são definidos manualmente" 📄. Hoje não há lista fixa nem legenda reservada à atribuição manual: um bloco chamado Anfitrião recebe condições como qualquer outro.
4. O bloco adicionado entra no fim da configuração, com o número seguinte ao do último bloco. Adicionados vários de uma vez, entram em sequência, na ordem em que foram marcados 🔍. 💻
5. O bloco entra sem condições. Enquanto não tiver ao menos uma condição completa, é ignorado na simulação e na geração. 💻 → ver Gerar Legendas do Evento `EVT-LEG-07`: regra 8 ⚠️ GPE006 não diz o que acontece com a legenda ativa que ainda não tem condição 📄.
6. Adicionar o bloco altera somente a configuração do evento atual; o catálogo e os outros eventos não mudam. 💻
7. Adicionar o bloco não atribui legenda a nenhum participante: a atribuição só acontece na geração. 💻
8. A adição é gravada de imediato, com a configuração inteira do evento. 💻 → ver Consultar Configuração de Legendas `EVT-LEG-01`: regras 6 e 7

---

## Cenários

```gherkin
Feature: Adicionar bloco de legenda ao evento

  Background:
    Given que o usuário está autenticado no GPE
    And está na tela Configuração de Legendas de um evento

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Adicionar um bloco do catálogo
    Given que o catálogo tem o bloco "Diretores da CNI", que ainda não está no evento
    And o evento tem dois blocos configurados
    When o usuário aciona "Adicionar bloco"
    And marca "Diretores da CNI" na aba "Usar bloco existente"
    And aciona "Adicionar ao evento"
    Then a janela se fecha e o bloco aparece como o último cartão, com o número 3 e sem condições
    And o sistema grava a configuração do evento

  Scenario: Adicionar vários blocos de uma vez
    Given que o evento tem dois blocos configurados
    When o usuário marca "Diretores da CNI" e "ICT – Reitores" na janela "Adicionar bloco"
    And aciona "Adicionar ao evento"
    Then os dois blocos entram no fim da configuração, com os números 3 e 4

  Scenario: Buscar o bloco pelo nome
    When o usuário digita "dire" no campo de busca da janela "Adicionar bloco"
    Then a lista mostra só os blocos cujo nome contém "dire", sem diferenciar maiúsculas de minúsculas

  Scenario: Desistir de adicionar
    When o usuário aciona "Cancelar" na janela "Adicionar bloco"
    Then a janela se fecha e a configuração do evento continua como estava

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Nenhum bloco marcado
    Given que a janela "Adicionar bloco" está aberta
    When o usuário não marca nenhum bloco
    Then o botão "Adicionar ao evento" fica desabilitado

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Bloco que já está no evento
    Given que o bloco "Comitê estratégico" já está na configuração do evento
    When o usuário aciona "Adicionar bloco"
    Then "Comitê estratégico" não aparece na lista da aba "Usar bloco existente"

  Scenario: Busca sem resultado
    Given que nenhum bloco disponível tem "Imprensa" no nome
    When o usuário digita "Imprensa" no campo de busca
    Then a janela mostra "Nenhum bloco encontrado para "Imprensa"." e o atalho "Adicionar bloco "Imprensa""
    And o atalho leva à aba "Criar novo bloco", com o nome "Imprensa" já preenchido
    # a criação é a feature Cadastrar Bloco de Legenda EVT-LEG-12

  Scenario: Bloco excluído do catálogo antes da gravação
    Given que o bloco marcado foi excluído do catálogo depois de aberta a janela
    When o usuário aciona "Adicionar ao evento"
    Then o sistema exibe o erro "Erro Interno" com o detalhe "Bloco de legenda inexistente: " seguido do número interno do bloco
    And a tela é recarregada com a configuração gravada, sem o bloco
    # 🔍 caminho deduzido do código; não foi executado

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Adicionar Bloco de Legenda ao Evento" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Eventos, de onde se chega à Configuração de Legendas, e a ação não fica ao alcance dele
    # ⚠️ a tela não confere o perfil; ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Nenhum bloco disponível
    Given que o catálogo está vazio ou todos os blocos do catálogo já estão no evento
    When o usuário aciona "Adicionar bloco"
    Then a aba "Usar bloco existente" mostra "Nenhum bloco disponível para adicionar."

  Scenario: Catálogo em carregamento
    When o usuário aciona "Adicionar bloco"
    Then a janela mostra "Carregando catálogo…" até a lista de blocos chegar

  Scenario: Falha ao carregar o catálogo
    Given que a consulta ao catálogo falha
    When o usuário aciona "Adicionar bloco"
    Then a janela abre sem blocos e o sistema avisa da falha
    # 🔍 o texto do aviso depende do tipo de falha; não foi executado

  Scenario: Falha ao gravar a adição
    Given que a gravação da configuração falha
    When o usuário aciona "Adicionar ao evento"
    Then o sistema exibe o erro e a tela é recarregada com a configuração gravada, sem o bloco
    # o comportamento é o da gravação automática; ver Consultar Configuração de Legendas EVT-LEG-01
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| Busca (sem rótulo; texto de orientação "Buscar bloco pelo nome") | Legenda | entrada do usuário | editável | texto | não | Filtra a lista pelos blocos cujo nome contém o termo, sem diferenciar maiúsculas de minúsculas; não é gravado |
| Lista de blocos (sem rótulo) | Legenda | entrada do usuário | editável | seleção múltipla → Legenda | sim | Ao menos um bloco marcado. A lista traz os blocos do catálogo que ainda não estão no evento, em ordem alfabética, cada um com a amostra da cor e o nome |

*A busca só restringe o que a lista mostra; os blocos já marcados continuam marcados quando o termo muda 🔍.*

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| Evento | O evento da tela | Ao adicionar o bloco |
| Nº | Posição seguinte à do último bloco da configuração | Ao adicionar o bloco |

---

## Dados lidos e gravados

| Entidade | Papel | Por que a feature a toca |
|---|---|---|
| Evento | lê | A gravação confirma que o evento existe (regra 8) |
| EventoLegendaCondicao | grava | A configuração é gravada por inteiro: as condições dos blocos que já estavam no evento são regravadas sem mudança (regra 8) |

---

## Comportamento de tela

### Onde fica
Na tela Configuração de Legendas, o botão "Adicionar bloco" fica na barra de ações e, quando o evento não tem nenhum bloco, também no centro da tela. Ele abre a janela "Adicionar bloco", com duas abas: "Usar bloco existente", que é esta feature, e "Criar novo bloco", que é a feature Cadastrar Bloco de Legenda `EVT-LEG-12` acionada de dentro da configuração. A janela sempre abre na aba "Usar bloco existente", com a busca vazia e nenhum bloco marcado.

A aba "Usar bloco existente" tem o campo de busca, com o texto de orientação "Buscar bloco pelo nome", e a lista de blocos com caixas de marcação. No rodapé ficam os botões "Cancelar" e "Adicionar ao evento"; na aba "Criar novo bloco", o segundo botão passa a ser "Criar e adicionar". ⚠️ GPE006 não tem janela de inclusão: as doze legendas já vinham listadas na tela, cada uma com a chave "Ativa" ou "Inativa" 📄.

A lista é montada com até mil blocos do catálogo 💻 ⚠️; um catálogo maior que isso não apareceria inteiro 🔍.

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | "Carregando catálogo…", com indicador giratório, enquanto a lista de blocos é buscada. Depois de "Adicionar ao evento", o indicador "Salvando…" da tela |
| Erro de validação | Sem bloco marcado, o botão "Adicionar ao evento" fica desabilitado; não há mensagem |
| Erro de servidor | Falha ao carregar o catálogo: aviso de erro, e a lista fica vazia. Falha ao gravar: erro "Erro Interno" com o detalhe enviado pelo servidor, e a tela volta à configuração gravada |
| Sucesso | A janela se fecha, o bloco aparece como último cartão e a tela mostra "Salvando…" e depois "Salvo"; não há mensagem de sucesso própria |
| Empty state | Sem bloco disponível: "Nenhum bloco disponível para adicionar.". Busca sem resultado: "Nenhum bloco encontrado para "{termo}"." e o atalho "Adicionar bloco "{termo}"" |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Todo bloco adicionado aparece na configuração do evento como último, com o número seguinte ao do bloco anterior e sem condições | Regras 4 e 5 · cenário "Adicionar um bloco do catálogo" |
| SC-02 | Nenhum evento fica com a mesma legenda em dois blocos | Regra 2 · cenário "Bloco que já está no evento" |
| SC-03 | Adicionar um bloco a um evento não altera o catálogo, a configuração de outro evento nem a legenda de nenhum participante | Regras 6 e 7 |

---

## Métricas de tamanho

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Adicionar Bloco de Legenda ao Evento | principal | EE | 2 | 3 | Baixa | 3 | 2026-10-04 |
| Consultar Lista de blocos (combo) | acessório | CE | 2 | 3 | Baixa | 3 | 2026-10-04 |

### Memória de cálculo

**Adicionar Bloco de Legenda ao Evento** — EE · ALR 2 · DER 3 · Baixa · 3 PF

```json
{"pe": "Adicionar Bloco de Legenda ao Evento",
 "alr": ["Evento", "Legenda"],
 "der": ["Lista de blocos", "Mensagem", "Ação"],
 "nao_contados": "Busca é parâmetro da lista consultada, contada à parte. Evento e Nº são preenchidos pelo sistema e não são informados pelo usuário nesta transação."}
```

Por que cada ALR:
1. `Evento` — grava o bloco na configuração do evento e confere que o evento existe
2. `Legenda` — confere que o bloco marcado existe no catálogo

Classificação: EE — a intenção primária é manter o arquivo lógico Evento, com as formas 1 (valida), 6 (atualiza), 7 (referencia) e 12 (recebe o bloco marcado).

**Consultar Lista de blocos (combo)** — CE · ALR 2 · DER 3 · Baixa · 3 PF

```json
{"pe": "Consultar Lista de blocos (combo)",
 "alr": ["Legenda", "Evento"],
 "der": ["Cor", "Nome da legenda", "Ação"],
 "nao_contados": "Busca filtra pelo nome, que já é DER da lista. A lista consultada não conta Mensagem."}
```

Por que cada ALR:
1. `Legenda` — lê os blocos do catálogo, com a cor e o nome
2. `Evento` — lê os blocos que já estão na configuração, para deixá-los fora da lista

Classificação: CE — lista consultada (SIZING, Regra da lista consultada): recupera e apresenta, com as formas 4 (filtra), 7, 8, 11 e 13. O filtro não é cálculo nem dado derivado, e por isso a lista não é SE (Guia STI 3.3.2).

**Total: 6 PF**

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade EventoLegenda

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Janela "Adicionar bloco", aba "Usar bloco existente" | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/components/adicionar-bloco-dialog/adicionar-bloco-dialog.component.ts` (linhas 83–137) e `.html` (linhas 1–46 e 55–60) | — |
| Entrada do bloco na configuração e gravação | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/pages/configuracao-legendas-evento/configuracao-legendas-evento.component.ts` (linhas 255–257 e 296–308) | — |
| Serviço de gravação da configuração | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento/services/evento-legenda.service.ts` (linhas 30–32) | — |
| Operação `PUT /administracao/eventos/{id}/legendas` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoController.java` (linhas 266–270) | — |
| Gravação e exigências da gravação | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/LegendaEventoServiceImpl.java` (linhas 96–142 e 171–196) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-10-04 | Claude (apf-cpm) | Contagem | Primeira contagem, pelo `PROMPT_CONTAGEM`: 6 PF — Adicionar Bloco de Legenda ao Evento (EE Baixa, 3 PF); Consultar Lista de blocos (combo) (CE Baixa, 3 PF). Confirmada em 2026-10-04 e espelhada em `global/CONTAGEM-PF.md` |
| 2026-10-04 | Claude (analise-impacto) | Origem atualizada | Elo com a AIM do ticket `PDTIC25148-34`, aberta na entrega: o ticket ganha linha própria na Origem, como Alteração, com o critério CA-01; o critério de criar bloco a partir da busca, que a Origem repetia aqui, fica só em Cadastrar Bloco de Legenda `EVT-LEG-12`; regras, campos e cenários inalterados |
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE006 – Gerenciar Regras de Legendas (funcionalidade "Incluir Regra de Legenda"), do ticket `PDTIC25148-34` do Jira e do código |

---

*Feature Set: Legendas · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
