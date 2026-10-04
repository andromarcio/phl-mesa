<!-- docqui: 4.0.2 | prompt: PROMPT_CONTAGEM | atualizado: 2026-10-04 -->
---
id: EVT-LEG-04
feature_set: EVT-LEG
dominio: EVT
entidade: EventoLegenda
data_model_ref: data-models/eventos.md#eventolegenda
endpoints: []
error_codes: []
depende_de: ["EVT-LEG-01", "EVT-LEG-02"]
origem:
  tipo: "issue"
  chave: "PDTIC25148-34"
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

# Reordenar Blocos de Legenda
> **Nível 3** - Feature Set: Legendas — Major Feature Set: Eventos - `EVT-LEG-04`

## Descrição

Permite que o Administrador reordene os blocos de legenda da configuração de um evento, movendo um bloco uma posição para cima ou para baixo; os números são recalculados e a nova ordem passa a ser a prioridade das legendas.

No cartão do bloco, na tela Configuração de Legendas, as setas Mover para cima e Mover para baixo trocam o bloco de lugar com o vizinho. A troca é gravada na hora.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| [`PDTIC25148-34`](../../../analise-impacto/AIM-PDTIC25148-34.md) | Criação | `CA-07` — alterar a ordem dos blocos de legenda do evento: a numeração é recalculada e a nova ordem é a prioridade de aplicação. Especificada a partir do código-fonte (engenharia reversa de 2026-09-30); a funcionalidade não consta nos documentos legados ⚠️. GPE006 só diz, na imagem do documento, que "As regras são aplicadas na ordem de prioridade das legendas", sem oferecer como mudar essa ordem 📄 |
<!-- trace-verified: PDTIC25148-34 @ f6bae69fe29f -->

---

<div class="dev-only">

## Superfície

**Ação em tela** — origem: Consultar Configuração de Legendas `EVT-LEG-01` (`/regras-legenda/:eventoId`), setas "Mover para cima" e "Mover para baixo" no cartão de cada bloco

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada

---

</div>

## Regras de negócio

1. O bloco se move uma posição por vez, trocando de lugar com o vizinho de cima ou de baixo. 💻
2. O primeiro bloco não sobe e o último não desce. 💻
3. A cada movimento os números de todos os blocos são recalculados pela posição. 💻 → ver Consultar Configuração de Legendas `EVT-LEG-01`: regra 3
4. A ordem dos blocos é a prioridade das legendas: o bloco de menor número prevalece. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 9
5. As condições acompanham o bloco na nova posição, sem mudança. 💻
6. A reordenação não cria nem apaga legenda de participante, e a ordem não muda quem recebe cada legenda, porque os blocos não se excluem. 💻 → ver Gerar Legendas do Evento `EVT-LEG-07`: regra 18
7. Para o participante que já tem legendas de mais de um bloco, a reordenação muda de imediato qual delas aparece, sem necessidade de nova geração: a prioridade é decidida pela ordem em vigor no momento em que a legenda é consultada. 🔍 Deduzido do código; não foi executado.
8. A reordenação altera somente a configuração do evento atual. 💻
9. A nova ordem é gravada de imediato, com a configuração inteira do evento. 💻 → ver Consultar Configuração de Legendas `EVT-LEG-01`: regras 6 e 7

---

## Cenários

```gherkin
Feature: Reordenar blocos de legenda

  Background:
    Given que o usuário está autenticado no GPE
    And está na tela Configuração de Legendas de um evento com os blocos 1 "Comitê estratégico", 2 "Diretores da CNI" e 3 "Assento livre"

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Subir um bloco
    When o usuário aciona "Mover para cima" no cartão de "Diretores da CNI"
    Then "Diretores da CNI" passa a ser o bloco 1 e "Comitê estratégico", o bloco 2
    And as condições de cada bloco continuam as mesmas
    And o sistema grava a configuração do evento

  Scenario: Descer um bloco
    When o usuário aciona "Mover para baixo" no cartão de "Diretores da CNI"
    Then "Diretores da CNI" passa a ser o bloco 3 e "Assento livre", o bloco 2
    And o sistema grava a configuração do evento

  Scenario: Mudar a legenda que aparece para quem tem duas
    Given que "Maria Souza" recebeu, na última geração, as legendas "Comitê estratégico" e "Diretores da CNI"
    When o usuário aciona "Mover para cima" no cartão de "Diretores da CNI"
    Then "Maria Souza" passa a aparecer com "Diretores da CNI" na lista de participantes e no mapa de assentos
    # 🔍 deduzido do código; ver a regra 7

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há dado a validar
    When o usuário aciona uma das setas do cartão
    Then o sistema move o bloco sem solicitar nenhum dado e sem pedir confirmação

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Primeiro bloco
    When o usuário olha o cartão de "Comitê estratégico", o bloco 1
    Then a seta "Mover para cima" está desabilitada

  Scenario: Último bloco
    When o usuário olha o cartão de "Assento livre", o bloco 3
    Then a seta "Mover para baixo" está desabilitada

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Reordenar Blocos de Legenda" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Eventos, de onde se chega à Configuração de Legendas, e a ação não fica ao alcance dele
    # ⚠️ a tela não confere o perfil; ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Evento com um só bloco
    Given que o evento tem um único bloco configurado
    When o usuário olha o cartão do bloco
    Then as setas "Mover para cima" e "Mover para baixo" estão desabilitadas

  Scenario: Falha ao gravar a nova ordem
    Given que a gravação da configuração falha
    When o usuário aciona uma das setas do cartão
    Then o sistema exibe o erro e a tela é recarregada com a ordem gravada
    # o comportamento é o da gravação automática; ver Consultar Configuração de Legendas EVT-LEG-01
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| — | EventoLegenda | — | — | — | — | A ação não tem campos: move o bloco do cartão em que a seta foi acionada |

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| Nº | Posição do bloco depois do movimento (1, 2, 3…), recalculada para todos os blocos | A cada movimento |

---

## Dados lidos e gravados

| Entidade | Papel | Por que a feature a toca |
|---|---|---|
| Evento | lê | A gravação confirma que o evento existe (regra 9) |
| Legenda | lê | A gravação confirma que cada bloco corresponde a uma legenda do catálogo (regra 9) |
| EventoLegendaCondicao | grava | A configuração é gravada por inteiro: as condições são regravadas sem mudança, cada uma com o seu bloco (regras 5 e 9) |

---

## Comportamento de tela

### Onde fica
Na tela Configuração de Legendas, no cabeçalho do cartão de cada bloco, à direita do nome da legenda: a seta para cima, com a dica "Mover para cima", e a seta para baixo, com a dica "Mover para baixo". A reordenação é feita só por essas setas; não há arrastar e soltar. Para levar um bloco do fim ao começo é preciso acionar a seta uma vez para cada posição, e cada acionamento grava a configuração. 💻

O número do bloco, à esquerda do nome, traz a dica "Ordem de aplicação" e muda assim que o bloco troca de lugar.

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | "Salvando…", ao lado do título da tela, enquanto a nova ordem é gravada; as setas continuam habilitadas |
| Erro de validação | Não se aplica — não há campos. A seta que não pode ser usada fica desabilitada: "Mover para cima" no primeiro bloco e "Mover para baixo" no último |
| Erro de servidor | Erro "Erro Interno" com o detalhe enviado pelo servidor, e a tela volta à ordem gravada |
| Sucesso | Os cartões trocam de lugar, os números são refeitos e a tela mostra "Salvo" por 2,5 segundos; não há mensagem de sucesso própria |
| Empty state | Não se aplica — as setas só existem no cartão de um bloco |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Depois de qualquer movimento, os números dos blocos do evento formam a sequência 1, 2, 3, sem saltos, na ordem em que os cartões aparecem | Regra 3 · cenários "Subir um bloco" e "Descer um bloco" |
| SC-02 | A ordem vista ao abrir de novo a configuração do evento é a do último movimento | Regra 9 |
| SC-03 | Nenhum movimento altera as condições dos blocos nem a configuração de outro evento | Regras 5 e 8 |

---

## Métricas de tamanho

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Reordenar Blocos de Legenda | principal | EE | 2 | 3 | Baixa | 3 | 2026-10-04 |

### Memória de cálculo

**Reordenar Blocos de Legenda** — EE · ALR 2 · DER 3 · Baixa · 3 PF

```json
{"pe": "Reordenar Blocos de Legenda",
 "alr": ["Evento", "Legenda"],
 "der": ["Bloco", "Mensagem", "Ação"],
 "nao_contados": "Nº é recalculado pelo sistema. O sentido do movimento está na seta acionada e conta como a própria ação."}
```

Por que cada ALR:
1. `Evento` — regrava a ordem dos blocos da configuração
2. `Legenda` — confere que cada bloco corresponde a uma legenda do catálogo

Classificação: EE — a intenção primária é manter o arquivo lógico Evento, com as formas 6, 7 e 12. Distingue-se de Remover Bloco de Legenda do Evento pela lógica: aqui os blocos trocam de posição, lá o bloco e as condições dele são apagados.

**Total: 3 PF**

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade EventoLegenda

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Setas "Mover para cima" e "Mover para baixo" | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/components/bloco-evento-card/bloco-evento-card.component.html` (linhas 5 e 11–30) | — |
| Troca de posição, renumeração e gravação | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/pages/configuracao-legendas-evento/configuracao-legendas-evento.component.ts` (linhas 201–224) | — |
| Operação `PUT /administracao/eventos/{id}/legendas` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoController.java` (linhas 266–270) | — |
| Gravação da ordem pela posição recebida | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/LegendaEventoServiceImpl.java` (linhas 106–119) | — |
| Uso da ordem na escolha da legenda prioritária | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/repository/impl/EventoPessoaRepositoryImpl.java` (linhas 44–68) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-10-04 | Claude (apf-cpm) | Contagem | Primeira contagem, pelo `PROMPT_CONTAGEM`: 3 PF — Reordenar Blocos de Legenda (EE Baixa, 3 PF). Confirmada em 2026-10-04 e espelhada em `global/CONTAGEM-PF.md` |
| 2026-10-04 | Claude (analise-impacto) | Origem atualizada | Elo com a AIM do ticket `PDTIC25148-34`, aberta na entrega: o ticket passa a ser a Origem da feature (Criação), com o critério CA-07; regras, campos e cenários inalterados |
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do código e do ticket `PDTIC25148-34` do Jira; a funcionalidade não consta no documento legado GPE006 |

---

*Feature Set: Legendas · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
