<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: EVT-PAR-09
feature_set: EVT-PAR
dominio: EVT
entidade: EventoPessoa
data_model_ref: data-models/eventos.md#eventopessoa
endpoints: []
error_codes: []
depende_de: ["EVT-PAR-07", "EVT-PAR-08"]
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

# Remover Assento do Participante
> **Nível 3** - Feature Set: Participantes — Major Feature Set: Eventos - `EVT-PAR-09`

## Descrição

Permite que o Administrador remova um participante do assento que ele ocupa no mapa do evento; o assento fica vazio e o participante volta à lista de pessoas disponíveis, pronto para receber outro lugar.

No mapa de assentos, cada assento ocupado traz o botão "×". Acionado, ele tira a pessoa do assento na hora, sem pedir confirmação; a remoção é gravada junto com o mapa, como na atribuição de assento.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE005 – Gerenciar Participante v1.1, de 16/12/2025 (documento legado), funcionalidade "Excluir Marcação de Assento do Participante" ⚠️ sem chave na ferramenta de demandas | Criação | — Remover um participante de um assento pela opção disponível em cada participante dentro do mapa, devolvendo-o à lista de pessoas disponíveis. A gravação junto com o mapa inteiro, a perda da marcação de atendido e o caso do último participante sentado vêm do código 💻. Ticket do Jira relacionado pelo título, concluído e sem AIM aberta 🔍: `PDTIC25148-16` (Mapa de mesa) |

---

<div class="dev-only">

## Superfície

**Ação em tela** — origem: Consultar Mapa de Assentos `EVT-PAR-07` (`/evento-pessoa/:id`, visão Mapa de Assentos, versão do Administrador), botão "×" com a dica "Remover pessoa" em cada assento ocupado

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Consultar Mapa de Assentos — Perfil Administrador" de GPE005

---

</div>

## Regras de negócio

1. Remover o participante do assento deixa o assento vazio e devolve o participante às pessoas disponíveis do mapa do Administrador.
2. A remoção só passa a valer para quem mais consulta o mapa depois de gravada, e é gravada como toda alteração do mapa: o mapa inteiro, sozinho depois de 30 segundos ou de imediato a pedido. → ver Atribuir Assento ao Participante `EVT-PAR-08` 💻
3. Remover o último participante sentado deixa o mapa sem ninguém, e o mapa sem ninguém sentado nunca é enviado para gravação: essa remoção fica só no mapa aberto do Administrador, e o servidor continua guardando o participante no assento. 💻 ⚠️ Suspeita de defeito, lida no código e não confirmada em execução → ver Atribuir Assento ao Participante `EVT-PAR-08`: regra 6. 🔍
4. Gravada a remoção, o participante que perdeu o assento volta a não atendido. 💻 ⚠️ Se ele tem check-in feito, reaparece entre as pessoas disponíveis da Secretaria Mesa, agora sem assento → ver Registrar Atendimento `EVT-PAR-10`. 🔍
5. A remoção não muda o convite, a confirmação nem o check-in do participante. 💻
6. Perder o assento não acontece só por esta ação: retirar a confirmação de presença também libera o assento. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 6
7. O sistema não guarda quem removeu o participante do assento nem quando. 💻

---

## Cenários

```gherkin
Feature: Remover assento do participante

  Background:
    Given que o usuário está autenticado no GPE
    And está no mapa de assentos de um evento, na versão do Administrador

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Remover o participante do assento
    Given que "Maria Souza" ocupa o assento "B12" e há outros participantes sentados
    When o usuário aciona o botão "×" do assento "B12"
    Then o assento "B12" fica vazio e volta a mostrar a sua identificação
    And "Maria Souza" volta para a lista "Pessoas Disponíveis"
    And o número do botão "Salvar Alocações (n)" diminui em um
    And a gravação automática fica marcada para 30 segundos depois
    # ⚠️ a remoção é imediata, sem pedido de confirmação 💻

  Scenario: Remoção gravada com o mapa
    Given que o usuário removeu "Maria Souza" do assento "B12"
    When o mapa é gravado, sozinho ou pelo botão "Salvar Alocações (n)"
    Then o assento "B12" aparece vazio para quem abrir o mapa do evento
    And "Maria Souza" volta a não atendida

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há dado a validar
    When o usuário aciona o botão "×" de um assento ocupado
    Then o sistema remove o participante sem solicitar nenhum dado nem confirmação

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Remover o único participante sentado
    Given que "Pedro Alves" é o único participante sentado no mapa
    When o usuário aciona o botão "×" do assento dele
    Then o assento fica vazio na tela e "Pedro Alves" volta para a lista "Pessoas Disponíveis"
    And o botão "Salvar Alocações (0)" fica desabilitado, e a gravação automática não envia o mapa
    And ao recarregar a tela, "Pedro Alves" reaparece no assento
    # ⚠️ 🔍 suspeita de defeito, lida no código e não executada: a retirada do último participante não é gravada

  Scenario: Participante já atendido perde o assento
    Given que "Maria Souza" fez check-in, foi atendida e ocupa o assento "B12"
    When o usuário a remove do assento e o mapa é gravado
    Then "Maria Souza" volta a não atendida
    And reaparece na lista "Pessoas Disponíveis" da Secretaria Mesa, com a etiqueta "Não alocado"
    # 🔍 consequência lida no código: a gravação do mapa desfaz o atendimento de quem perdeu o assento

  Scenario: Mudança de outro usuário chega antes da gravação
    Given que o usuário removeu um participante do assento e a gravação automática ainda não aconteceu
    When a recepção registra o check-in de um participante
    Then a atualização automática refaz o mapa com o que está gravado, e o participante removido reaparece no assento
    # ⚠️ 🔍 mesma suspeita descrita em Atribuir Assento ao Participante EVT-PAR-08

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Remover Assento do Participante" na matriz do N2
    When o usuário abre o mapa de assentos
    Then os assentos ocupados não trazem o botão "×"
    # ⚠️ quem não chega ao mapa nem vê a opção; ver a nota da matriz no N2 sobre o que o servidor confere

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Mapa carregando ou gravando
    Given que o mapa está sendo carregado ou gravado
    When o usuário tenta acionar o botão "×" de um assento
    Then a tela está bloqueada e a remoção não acontece

  Scenario: Falha ao gravar a remoção
    Given que a gravação do mapa falha
    When o sistema tenta gravar a remoção
    Then exibe a mensagem de erro da gravação do mapa, e a remoção continua só na tela
    # → ver Atribuir Assento ao Participante EVT-PAR-08, cenários "Falha na gravação automática" e "Assento que não existe no evento"
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| — | EventoPessoa | — | — | — | — | A ação não tem campos: opera sobre o participante do assento escolhido, sem confirmação |

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| Assento | Vazio | Na gravação do mapa que se segue à remoção (regras 2 e 3) |
| Atendido | Não | Na mesma gravação, para o participante que perdeu o assento (regra 4) |

---

## Dados lidos e gravados

| Entidade | Papel | Por que a feature a toca |
|---|---|---|
| Evento | lê | A gravação localiza pelo evento as atribuições a substituir (regra 2) |
| CadeiraMesa | lê | O assento de que o participante é retirado |

---

## Comportamento de tela

### Onde fica
No mapa de assentos do Administrador, em cada assento ocupado, o botão "×" no canto do assento, com a dica "Remover pessoa". Não há pergunta de confirmação nem mensagem depois da remoção: o assento fica vazio e a pessoa reaparece na lista "Pessoas Disponíveis". A gravação segue o que está descrito em Atribuir Assento ao Participante `EVT-PAR-08`: sozinha depois de 30 segundos, ou pelo botão "Salvar Alocações (n)". 💻

Arrastar o ocupante para fora do assento não o remove: o arraste só serve para levá-lo a outro assento. O botão "×" não aparece nos arquivos exportados nem no mapa da Secretaria Mesa. 💻

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Sem indicador próprio; enquanto o mapa carrega ou grava, a tela fica bloqueada e o botão "×" não age |
| Erro de validação | Não se aplica — não há campos |
| Erro de servidor | Os da gravação do mapa → ver Atribuir Assento ao Participante `EVT-PAR-08`. A remoção em si acontece só na tela e não falha |
| Sucesso | Sem mensagem: o assento volta a mostrar a identificação e a pessoa volta para "Pessoas Disponíveis". A mensagem de sucesso é a da gravação do mapa |
| Empty state | Não se aplica — a ação só existe em assento ocupado |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Removido o participante, o assento aparece vazio e o participante consta na lista de pessoas disponíveis do Administrador | Regra 1 · cenário "Remover o participante do assento" |
| SC-02 | Depois da gravação, o assento aparece vazio para qualquer usuário que abra o mapa do evento | Regra 2 · cenário "Remoção gravada com o mapa" |
| SC-03 | A remoção do último participante sentado também fica gravada ⚠️ hoje não atendido | Regra 3 · cenário "Remover o único participante sentado" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Remover Assento do Participante | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade EventoPessoa

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Botão "×" e remoção em cada setor | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/components/mesa/components/retangular/retangular.component.ts` (linhas 483–496, 543–555, 1033–1041, 1096–1104, 1160–1168, 1223–1231) e `.html` (linhas 136–139, 240–243); o formato invertido repete o código em `../retangular-invertido/retangular-invertido.component.ts` | — |
| Gravação do mapa, que não envia mapa vazio | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/components/mesa/components/retangular/retangular.component.ts` (linhas 1421–1431, 1517–1521) e `.html` (linhas 91–92) | — |
| Operação `POST /administracao/eventos/{eventoId}/composicoes-mesa` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoController.java` (linhas 172–183) | — |
| Liberação das atribuições anteriores e volta a não atendido | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/EventoServiceImpl.java` (linhas 221–274, 413–422) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

Não há operação do servidor para um assento só: a remoção chega ao servidor porque o participante removido deixa de constar na relação enviada pela gravação do mapa.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE005 – Gerenciar Participante (funcionalidade "Excluir Marcação de Assento do Participante") e do código |

---

*Feature Set: Participantes · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
