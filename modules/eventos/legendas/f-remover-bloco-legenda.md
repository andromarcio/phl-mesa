<!-- docqui: 4.0.2 | prompt: PROMPT_CONTAGEM | atualizado: 2026-10-04 -->
---
id: EVT-LEG-05
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

# Remover Bloco de Legenda do Evento
> **Nível 3** - Feature Set: Legendas — Major Feature Set: Eventos - `EVT-LEG-05`

## Descrição

Permite que o Administrador remova um bloco de legenda da configuração de um evento, com as condições que ele tinha ali; o bloco deixa de valer naquele evento e continua no catálogo, disponível para os demais eventos e para ser adicionado de novo.

No cartão do bloco, na tela Configuração de Legendas, o botão Remover bloco do evento pede confirmação e, confirmada, retira o bloco e renumera os que ficam.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| [`PDTIC25148-34`](../../../analise-impacto/AIM-PDTIC25148-34.md) | Criação | `CA-09` — retirar um bloco da configuração de legendas do evento, desfazendo só a associação com o evento atual. Especificada a partir do código-fonte (engenharia reversa de 2026-09-30); a funcionalidade não consta nos documentos legados ⚠️. No modelo de GPE006 o que havia de equivalente era inativar a legenda, pela chave "Ativa" ou "Inativa" 📄; hoje não há bloco inativo, e o que não deve valer é removido 💻 |
<!-- trace-verified: PDTIC25148-34 @ f6bae69fe29f -->

---

<div class="dev-only">

## Superfície

**Ação em tela** — origem: Consultar Configuração de Legendas `EVT-LEG-01` (`/regras-legenda/:eventoId`), botão "Remover bloco do evento" no cartão de cada bloco

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada

---

</div>

## Regras de negócio

1. A remoção desfaz só a presença do bloco no evento atual: o bloco continua no catálogo e na configuração dos outros eventos que o usam. 💻
2. Remover é a forma de tirar o bloco de vigor no evento. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 11
3. As condições que o bloco tinha naquele evento são apagadas com ele; adicionado de novo, o bloco volta sem condições. 💻 ⚠️ É diferente de inativar, como fazia GPE006 📄: a legenda inativa podia ser reativada, e o documento não diz se as condições dela se perdiam.
4. Os blocos que ficam são renumerados em sequência. 💻 → ver Consultar Configuração de Legendas `EVT-LEG-01`: regra 3
5. A remoção não apaga as legendas já atribuídas aos participantes: quem recebeu a legenda do bloco continua com ela até a geração seguinte, que apaga todas as legendas não manuais do evento. 💻 ⚠️ Nesse intervalo a legenda fica fora da configuração: aparece sem número de bloco e perde a prioridade para qualquer legenda de bloco configurado. → ver Gerar Legendas do Evento `EVT-LEG-07`: regra 3
6. A legenda do bloco atribuída manualmente a um participante não é afetada pela remoção nem pela geração seguinte. 💻 → ver [N1 Eventos](../README.md): Regras transversais de negócio: 10
7. A remoção é gravada de imediato, com a configuração inteira do evento. 💻 → ver Consultar Configuração de Legendas `EVT-LEG-01`: regras 6 e 7
8. A remoção é definitiva: não há como desfazê-la, a não ser adicionando o bloco de novo e refazendo as condições. 💻

---

## Cenários

```gherkin
Feature: Remover bloco de legenda do evento

  Background:
    Given que o usuário está autenticado no GPE
    And está na tela Configuração de Legendas de um evento com os blocos 1 "Comitê estratégico", 2 "Diretores da CNI" e 3 "Assento livre"

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Remover um bloco do evento
    When o usuário aciona "Remover bloco do evento" no cartão de "Diretores da CNI"
    And confirma a pergunta "Remover o bloco 'Diretores da CNI' deste evento?"
    Then o cartão de "Diretores da CNI" sai da tela, com as condições que tinha
    And "Assento livre" passa a ser o bloco 2
    And o sistema grava a configuração do evento
    And "Diretores da CNI" continua no catálogo de blocos

  Scenario: Desistir da remoção
    When o usuário aciona "Remover bloco do evento" no cartão de um bloco
    And escolhe "Cancelar" na pergunta de confirmação
    Then o sistema mantém o bloco e a configuração como estavam

  Scenario: Adicionar de novo o bloco removido
    Given que o usuário removeu "Diretores da CNI" do evento
    When o usuário abre a janela "Adicionar bloco"
    Then "Diretores da CNI" volta a aparecer na lista de blocos disponíveis
    And, adicionado, entra no fim da configuração e sem condições

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há dado a validar
    When o usuário aciona "Remover bloco do evento"
    Then o sistema pede apenas a confirmação, sem solicitar nenhum dado

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Bloco cuja legenda já foi atribuída a participantes
    Given que três participantes receberam "Diretores da CNI" na última geração
    When o usuário remove "Diretores da CNI" do evento
    Then o sistema remove o bloco sem avisar que há participantes com a legenda
    And os três participantes continuam com "Diretores da CNI" até a geração seguinte
    # ⚠️ a pergunta de confirmação não menciona as legendas já atribuídas; ver a regra 5

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Remover Bloco de Legenda do Evento" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Eventos, de onde se chega à Configuração de Legendas, e a ação não fica ao alcance dele
    # ⚠️ a tela não confere o perfil; ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Remover o único bloco do evento
    Given que o evento tem um único bloco configurado
    When o usuário remove o bloco e confirma
    Then a tela mostra "0 blocos configurados" e "Nenhum bloco configurado", com o botão "Adicionar bloco"

  Scenario: Falha ao gravar a remoção
    Given que a gravação da configuração falha
    When o usuário remove um bloco e confirma
    Then o sistema exibe o erro e a tela é recarregada com a configuração gravada, em que o bloco continua
    # o comportamento é o da gravação automática; ver Consultar Configuração de Legendas EVT-LEG-01
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| — | EventoLegenda | — | — | — | — | A ação não tem campos: opera sobre o bloco do cartão escolhido e pede só a confirmação |

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| Nº | Posição de cada bloco que ficou (1, 2, 3…), recalculada | Ao remover o bloco |

---

## Dados lidos e gravados

| Entidade | Papel | Por que a feature a toca |
|---|---|---|
| EventoLegendaCondicao | grava | As condições do bloco removido são apagadas com ele; as dos demais blocos são regravadas sem mudança (regras 3 e 7) |
| Evento | lê | A gravação confirma que o evento existe (regra 7) |
| Legenda | lê | A gravação confirma que cada bloco que ficou corresponde a uma legenda do catálogo (regra 7) |

---

## Comportamento de tela

### Onde fica
Na tela Configuração de Legendas, no cabeçalho do cartão de cada bloco, à direita das setas de reordenação: o botão "Remover bloco do evento", com o ícone de lixeira. A confirmação é uma caixa com o título "Remover bloco", a pergunta "Remover o bloco '{nome da legenda}' deste evento?" e os botões "Remover" e "Cancelar". ⚠️ A pergunta não diz que as condições do bloco se perdem nem que as legendas já atribuídas ficam até a geração seguinte 💻.

Não há ação para remover todos os blocos de uma vez: cada bloco é removido no seu cartão. ⚠️ GPE006 tinha o comando "Resetar", que excluía todas as regras do evento 📄 e não existe mais; hoje o efeito é obtido removendo os blocos um a um.

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | "Salvando…", ao lado do título da tela, enquanto a remoção é gravada |
| Erro de validação | Não se aplica — não há campos |
| Erro de servidor | Erro "Erro Interno" com o detalhe enviado pelo servidor, e a tela volta à configuração gravada, em que o bloco continua |
| Sucesso | O cartão sai da tela, os números dos demais são refeitos, a contagem de blocos do alto da tela diminui e a tela mostra "Salvo" por 2,5 segundos; não há mensagem de sucesso própria |
| Empty state | Removido o último bloco: "Nenhum bloco configurado", com o texto "Adicione o primeiro bloco de legenda para começar a montar as regras deste evento." e o botão "Adicionar bloco" |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | O bloco removido deixa de aparecer na configuração do evento e volta a ser oferecido na janela de adição de bloco | Cenários "Remover um bloco do evento" e "Adicionar de novo o bloco removido" |
| SC-02 | O bloco removido de um evento continua no catálogo e na configuração de todos os outros eventos que o usam | Regra 1 |
| SC-03 | Nenhuma remoção acontece sem a confirmação do usuário | Cenário "Desistir da remoção" |
| SC-04 | Depois da remoção, os números dos blocos que ficaram formam a sequência 1, 2, 3, sem saltos | Regra 4 |

---

## Métricas de tamanho

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Remover Bloco de Legenda do Evento | principal | EE | 2 | 3 | Baixa | 3 | 2026-10-04 |

### Memória de cálculo

**Remover Bloco de Legenda do Evento** — EE · ALR 2 · DER 3 · Baixa · 3 PF

```json
{"pe": "Remover Bloco de Legenda do Evento",
 "alr": ["Evento", "Legenda"],
 "der": ["Bloco", "Mensagem", "Ação"],
 "nao_contados": "Nº dos blocos que ficam é recalculado pelo sistema."}
```

Por que cada ALR:
1. `Evento` — apaga o bloco e as condições dele da configuração e renumera os que ficam
2. `Legenda` — confere que cada bloco que fica corresponde a uma legenda do catálogo

Classificação: EE — a intenção primária é manter o arquivo lógico Evento, com as formas 6, 7 e 12.

**Total: 3 PF**

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade EventoLegenda

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Botão "Remover bloco do evento" e confirmação | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/components/bloco-evento-card/bloco-evento-card.component.ts` (linhas 74–84) e `.html` (linhas 31–38) | — |
| Retirada do bloco, renumeração e gravação | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/pages/configuracao-legendas-evento/configuracao-legendas-evento.component.ts` (linhas 201–204 e 226–230) | — |
| Operação `PUT /administracao/eventos/{id}/legendas` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoController.java` (linhas 266–270) | — |
| Substituição da configuração inteira | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/LegendaEventoServiceImpl.java` (linhas 96–142) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-10-04 | Claude (apf-cpm) | Contagem | Primeira contagem, pelo `PROMPT_CONTAGEM`: 3 PF — Remover Bloco de Legenda do Evento (EE Baixa, 3 PF). Confirmada em 2026-10-04 e espelhada em `global/CONTAGEM-PF.md` |
| 2026-10-04 | Claude (analise-impacto) | Origem atualizada | Elo com a AIM do ticket `PDTIC25148-34`, aberta na entrega: o ticket passa a ser a Origem da feature (Criação), com o critério CA-09; regras, campos e cenários inalterados |
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do código e do ticket `PDTIC25148-34` do Jira; a funcionalidade não consta no documento legado GPE006, que tratava de inativar a legenda |

---

*Feature Set: Legendas · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
