<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: EVT-PAR-10
feature_set: EVT-PAR
dominio: EVT
entidade: EventoPessoa
data_model_ref: data-models/eventos.md#eventopessoa
endpoints: []
error_codes: []
depende_de: ["EVT-PAR-07", "EVT-PAR-03"]
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

# Registrar Atendimento
> **Nível 3** - Feature Set: Participantes — Major Feature Set: Eventos - `EVT-PAR-10`

## Descrição

Permite que a Secretaria Mesa registre que um participante que chegou ao evento já foi atendido; o participante sai da lista de pessoas disponíveis, que fica só com quem ainda aguarda ser conduzido ao seu lugar.

No mapa de assentos da Secretaria Mesa, cada pessoa da lista "Pessoas Disponíveis" traz o botão de atendimento — "ATENDIDO" no computador e "ATENDER" no tablet. Um toque no botão registra o atendimento, sem pedir confirmação.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE005 – Gerenciar Participante v1.1, de 16/12/2025 (documento legado), funcionalidade "Realizar Atendimento" ⚠️ sem chave na ferramenta de demandas | Criação | — Marcar que um participante teve o atendimento realizado, pela opção disponível em cada participante da lista de pessoas disponíveis do mapa, retirando-o dessa lista; cobre também a regra de negócio "Realizar Atendimento" do documento. A falta de uma forma de desfazer e a volta do participante a não atendido quando o mapa é gravado vêm do código 💻 |

---

<div class="dev-only">

## Superfície

**Ação em tela** — origem: Consultar Mapa de Assentos `EVT-PAR-07` (`/evento-pessoa/:id`, versão da Secretaria Mesa), botão "ATENDIDO" (lista, no computador) ou "ATENDER" (carrossel, no tablet), com a dica "Atender Pessoa", em cada cartão da lista "Pessoas Disponíveis"

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Consultar Mapa de Assentos — Perfil Secretaria Mesa" de GPE005

---

</div>

## Regras de negócio

1. O atendimento é uma marcação da participação, independente do convite, da confirmação e do check-in. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 4
2. Fica à espera de atendimento o participante que fez check-in e ainda não foi atendido, tenha ou não assento. → ver Consultar Mapa de Assentos `EVT-PAR-07` ⚠️ Ao registrar o atendimento, o servidor não confere se o participante fez check-in nem se tem assento. 💻
3. Registrado o atendimento, o participante deixa de constar entre as pessoas disponíveis da Secretaria Mesa.
4. O atendimento não muda o assento do participante nem a forma como ele aparece no mapa. 💻
5. Não existe ação que desfaça o atendimento. 💻 ❓ GPE005 não prevê o desfazer, e nenhuma fonte diz o que a secretaria deve fazer quando marca a pessoa errada.
6. A marcação de atendido é desfeita, sem ação da secretaria, quando o mapa de assentos é gravado pelo Administrador: sempre, para quem perdeu o assento; e, para quem continua sentado, quando o mapa do Administrador ainda mostrava o participante como não atendido. 💻 ⚠️ Suspeita de defeito, lida no código e não confirmada em execução → ver Atribuir Assento ao Participante `EVT-PAR-08`: regras 9 e 11. 🔍
7. O sistema não guarda quem registrou o atendimento nem quando. 💻

---

## Cenários

```gherkin
Feature: Registrar atendimento

  Background:
    Given que o usuário está autenticado no GPE
    And está no mapa de assentos do evento principal, na versão da Secretaria Mesa

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Registrar o atendimento de participante com assento
    Given que "Ada Mota" fez check-in, tem o assento "A4" e está na lista "Pessoas Disponíveis"
    When o usuário aciona o botão "ATENDIDO" no cartão de "Ada Mota"
    Then o sistema registra o atendimento de "Ada Mota"
    And exibe: "Sucesso" com o detalhe "Pessoa atendida com sucesso"
    And "Ada Mota" sai da lista "Pessoas Disponíveis" e continua no assento "A4" do mapa
    # ⚠️ no tablet o mesmo botão tem o texto "ATENDER"; "ATENDIDO" lê como situação, não como ação 💻

  Scenario: Registrar o atendimento de participante sem assento
    Given que "Adriana Alencar" fez check-in, não tem assento e aparece com a etiqueta "Não alocado"
    When o usuário aciona o botão de atendimento no cartão dela
    Then o sistema registra o atendimento e "Adriana Alencar" sai da lista "Pessoas Disponíveis"

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há dado a validar
    When o usuário aciona o botão de atendimento de uma pessoa
    Then o sistema registra o atendimento sem solicitar nenhum dado nem confirmação

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Atendimento desfeito pela gravação do mapa
    Given que "Ada Mota" foi atendida e tem o assento "A4"
    And o mapa aberto do Administrador ainda a mostra como não atendida
    When o Administrador grava o mapa de assentos
    Then "Ada Mota" volta a não atendida
    And reaparece na lista "Pessoas Disponíveis" de quem abrir o mapa da Secretaria Mesa depois disso
    # ⚠️ 🔍 suspeita de defeito, lida no código e não executada; na tela de quem registrou o atendimento ela só reaparece quando a tela é recarregada

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Registrar Atendimento" na matriz do N2
    When o usuário abre o mapa de assentos
    Then os cartões da lista "Pessoas Disponíveis" não trazem o botão de atendimento
    # ⚠️ o botão só existe no mapa da Secretaria Mesa; a operação do servidor não está entre as protegidas — ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Falha ao registrar o atendimento
    Given que o registro do atendimento falha
    When o usuário aciona o botão de atendimento
    Then o sistema exibe: "Erro" com o detalhe "Erro ao atender pessoa"
    And a pessoa continua na lista "Pessoas Disponíveis"

  Scenario: Outra tela da Secretaria Mesa aberta ao mesmo tempo
    Given que duas pessoas da secretaria estão com o mapa aberto, cada uma em um aparelho
    When uma delas registra o atendimento de "Ada Mota"
    Then "Ada Mota" sai da lista de quem registrou
    And continua na lista do outro aparelho até que a atualização automática perceba outra mudança, como um novo check-in
    # ⚠️ 🔍 lido no código: a atualização automática não considera o atendimento ao decidir se algo mudou
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| — | EventoPessoa | — | — | — | — | A ação não tem campos: opera sobre o participante do cartão escolhido, sem confirmação |

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| Atendido | Sim | Ao acionar o botão de atendimento |

---

## Comportamento de tela

### Onde fica
No mapa de assentos da Secretaria Mesa, na lista "Pessoas Disponíveis", à esquerda do mapa. Cada cartão mostra a foto da pessoa, o nome, a organização, a etiqueta com a identificação do assento — ou "Não alocado" — e, embaixo, o botão de atendimento, com a dica "Atender Pessoa". No computador a lista é vertical e o botão tem o texto "ATENDIDO"; no tablet a lista vira um carrossel horizontal e o botão tem o texto "ATENDER". 💻 ⚠️ São dois textos para a mesma ação; a imagem de GPE005 mostra "ATENDER" na lista vertical e o documento chama a opção de "Atender" 📄.

Não há pergunta de confirmação: um toque basta. No computador, tocar na etiqueta do assento localiza a pessoa no mapa antes do atendimento → ver Buscar Pessoa na Mesa `EVT-PAR-12`. O mapa do Administrador não tem o botão de atendimento nem mostra quem já foi atendido. 💻

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Sem indicador: o botão continua acionável enquanto o registro é enviado |
| Erro de validação | Não se aplica — não há campos |
| Erro de servidor | "Erro" com o detalhe "Erro ao atender pessoa"; a pessoa continua na lista |
| Sucesso | "Sucesso" com o detalhe "Pessoa atendida com sucesso"; o cartão sai da lista e o número do título "Pessoas Disponíveis (n)" diminui |
| Empty state | Sem ninguém à espera de atendimento, a lista fica vazia e o título mostra "Pessoas Disponíveis (0)", sem texto de aviso |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Registrado o atendimento, o participante não consta mais na lista de pessoas disponíveis da Secretaria Mesa | Regra 3 · cenário "Registrar o atendimento de participante com assento" |
| SC-02 | O atendimento registrado não altera o assento do participante | Regra 4 · cenário "Registrar o atendimento de participante com assento" |
| SC-03 | O participante atendido continua atendido depois que o mapa de assentos é gravado ⚠️ hoje não garantido | Regra 6 · cenário "Atendimento desfeito pela gravação do mapa" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Registrar Atendimento | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade EventoPessoa

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Botão de atendimento e mensagens, formato retangular | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/components/mesa-recepcionista-checkin/components/retangular/retangular-recepcionista-checkin.component.ts` (linhas 497–504, 1494–1516) e `.html` (linhas 64–69, 116–121) | — |
| Botão de atendimento e mensagens, formato invertido | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/components/mesa-recepcionista-checkin/components/retangular-invertido/retangular-invertido-recepcionista-checkin.component.ts` (linhas 447–454, 2682–2703) e `.html` (linhas 57–61, 109–113) | — |
| Serviço `atenderPessoa` | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/services/evento-pessoa.service.ts` (linhas 40–43) | — |
| Operação `PUT /administracao/evento-pessoas/{id}/atender` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoPessoaController.java` (linhas 97–101) | — |
| Marcação de atendido | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/EventoPessoaServiceImpl.java` (linhas 469–475) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

Depois do sucesso, a tela guarda o participante em uma relação de atendidos que vale só enquanto a página está aberta; é ela que tira o cartão da lista, porque a consulta periódica dos participantes não compara o indicador de atendido.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE005 – Gerenciar Participante (funcionalidade e regra de negócio "Realizar Atendimento") e do código |

---

*Feature Set: Participantes · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
