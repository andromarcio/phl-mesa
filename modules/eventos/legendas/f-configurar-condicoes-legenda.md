<!-- docqui: 4.0.2 | prompt: PROMPT_CONTAGEM | atualizado: 2026-10-04 -->
---
id: EVT-LEG-03
feature_set: EVT-LEG
dominio: EVT
entidade: EventoLegendaCondicao
data_model_ref: data-models/eventos.md#eventolegendacondicao
endpoints: []
error_codes: []
depende_de: ["EVT-LEG-01", "EVT-LEG-02"]
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

# Configurar Condições de Legenda
> **Nível 3** - Feature Set: Legendas — Major Feature Set: Eventos - `EVT-LEG-03`

## Descrição

Permite que o Administrador configure, em um bloco de legenda do evento, as condições de campo, operador e valor que decidem quais participantes recebem a legenda, combinando-as com os conectivos E e OU.

No cartão do bloco, na tela Configuração de Legendas, o botão Adicionar condição cria uma linha; o usuário escolhe o campo e o operador, digita o valor e, a partir da segunda condição, escolhe o conectivo. A lixeira da linha exclui a condição. Cada mudança é gravada na hora.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE006 – Gerenciar Regras de Legendas v1.0, de 03/10/2025 (documento legado), funcionalidades "Incluir Regra de Legenda" e "Editar Regra de Legenda" ⚠️ sem chave na ferramenta de demandas | Criação | — Incluir uma regra escolhendo campo, operador e valor de comparação, e editar as regras de uma legenda, incluindo ou excluindo condições. A ativação da legenda, que o documento põe como primeiro passo da inclusão, deu lugar a Adicionar Bloco de Legenda ao Evento `EVT-LEG-02` |
| [`PDTIC25148-34`](../../../analise-impacto/AIM-PDTIC25148-34.md) | Alteração | `CA-13, CA-14` — configurar condições com Campo, Operador e Valor, e usar várias condições, com o conector E ou OU a partir da segunda |
<!-- trace-verified: PDTIC25148-34 @ f6bae69fe29f -->

---

<div class="dev-only">

## Superfície

**Ação em tela** — origem: Consultar Configuração de Legendas `EVT-LEG-01` (`/regras-legenda/:eventoId`), no cartão de cada bloco: botão "Adicionar condição", os controles de cada linha de condição e a lixeira "Remover condição"

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Listar Regras de Legendas" de GPE006, que mostra as condições no modelo anterior ⚠️

---

</div>

## Regras de negócio

1. A condição é formada por um campo, um operador e um valor; a partir da segunda condição do bloco, também por um conectivo, que a liga ao que vem antes.
2. O campo é um dado cadastral do participante, entre cinco: Grupo de trabalho, Tema, Cargo, Nome fantasia e Papel desempenhado. ⚠️ GPE006 chama o primeiro de "Grupo Temático" 📄 e o sistema, de "Grupo de trabalho" 💻; é o mesmo dado, o grupo de que o participante faz parte. O ticket lista "Grupo de Trabalho" e "Tema/Grupo Temático", o que deixa em dúvida a que dado o nome "Grupo Temático" se refere.
3. O operador é um entre quatro: Igual a, Diferente de, Contém e Em (lista).
4. O conectivo é E ou OU. A primeira condição do bloco não tem conectivo.
5. A condição nova nasce com o campo Grupo de trabalho, o operador Igual a e o valor vazio; da segunda em diante, nasce também com o conectivo E. 💻
6. Quando a primeira condição do bloco é excluída, a seguinte passa a ser a primeira e perde o conectivo. 💻
7. O valor é texto livre e não é conferido contra os dados existentes: nada garante que o grupo de trabalho, o tema, o cargo, o nome fantasia ou o papel digitado exista. 💻 ⚠️ Um erro de digitação faz a condição não alcançar ninguém, sem que o sistema acuse.
8. Com o operador Em (lista), o valor reúne vários valores separados por vírgula.
9. A condição incompleta — sem valor — é aceita e gravada, mas fica fora da avaliação; o bloco sem nenhuma condição completa é ignorado na simulação e na geração. 💻 → ver Gerar Legendas do Evento `EVT-LEG-07`: regras 7 e 8 ⚠️ GPE006 dá Campo, Operador e Valor como obrigatórios 📄.
10. Duas condições iguais no mesmo bloco são aceitas, e não há limite de condições por bloco. 💻
11. As condições pertencem ao bloco naquele evento: o mesmo bloco do catálogo tem condições próprias em cada evento. 💻
12. Mudar as condições não altera as legendas já atribuídas aos participantes; a mudança só produz efeito na geração seguinte. 💻
13. Cada mudança — incluir, alterar ou excluir uma condição — é gravada de imediato, com a configuração inteira do evento. 💻 → ver Consultar Configuração de Legendas `EVT-LEG-01`: regras 6 e 7
14. O modo como as condições se combinam e o que cada operador faz com cada campo pertencem à avaliação. → ver Gerar Legendas do Evento `EVT-LEG-07`: regras 9 a 17

---

## Cenários

```gherkin
Feature: Configurar condições de legenda

  Background:
    Given que o usuário está autenticado no GPE
    And está na tela Configuração de Legendas de um evento que tem o bloco "Diretores da CNI"

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Incluir a primeira condição do bloco
    Given que o bloco "Diretores da CNI" não tem condições
    When o usuário aciona "Adicionar condição" no cartão do bloco
    Then o cartão ganha uma linha com Campo "Grupo de trabalho", Operador "Igual a" e Valor vazio, sem conectivo
    And o sistema grava a configuração do evento

  Scenario: Preencher a condição
    Given que o bloco tem uma condição recém-incluída
    When o usuário escolhe o Campo "Cargo" e o Operador "Contém"
    And digita "Diretor" no Valor
    Then o sistema grava a troca do campo e a do operador na hora
    And grava o valor depois de uma pausa na digitação e ao sair do campo

  Scenario: Incluir a segunda condição
    Given que o bloco tem uma condição
    When o usuário aciona "Adicionar condição"
    Then a nova linha nasce com o Conectivo "E", o Campo "Grupo de trabalho", o Operador "Igual a" e o Valor vazio

  Scenario: Trocar o conectivo
    Given que o bloco tem duas condições
    When o usuário escolhe "OU" no Conectivo da segunda condição
    Then o sistema grava a configuração com as duas condições ligadas por OU

  Scenario: Informar vários valores
    Given que o bloco tem uma condição com o Campo "Papel desempenhado"
    When o usuário escolhe o Operador "Em (lista)"
    Then o campo Valor passa a orientar "valores separados por vírgula"
    And o usuário digita "CEO, Presidente"

  Scenario: Excluir uma condição
    Given que o bloco tem três condições
    When o usuário aciona "Remover condição" na segunda linha
    Then a condição é excluída sem pedido de confirmação
    And o sistema grava a configuração do evento

  Scenario: Excluir a primeira condição
    Given que o bloco tem duas condições, a segunda com o Conectivo "OU"
    When o usuário aciona "Remover condição" na primeira linha
    Then a condição que restou passa a ser a primeira e deixa de ter conectivo

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Valor em branco
    Given que o bloco tem uma condição com o Valor vazio
    When o usuário sai do campo sem digitar
    Then o sistema grava a condição incompleta, sem nenhum aviso
    # ⚠️ GPE006 dá o Valor como obrigatório; hoje a condição sem valor é aceita e fica fora da avaliação

  Scenario: Valor que não corresponde a nenhum dado
    When o usuário digita no Valor um cargo que nenhuma pessoa tem
    Then o sistema grava a condição, sem nenhum aviso
    # ⚠️ o valor não é conferido contra os dados existentes; ver a regra 7

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Condição repetida no mesmo bloco
    Given que o bloco tem a condição Campo "Cargo", Operador "Contém", Valor "Diretor"
    When o usuário inclui outra condição com os mesmos campo, operador e valor
    Then o sistema grava as duas, sem comparar uma com a outra

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Configurar Condições de Legenda" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Eventos, de onde se chega à Configuração de Legendas, e a ação não fica ao alcance dele
    # ⚠️ a tela não confere o perfil; ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Bloco sem nenhuma condição
    Given que o usuário excluiu a única condição do bloco
    When a tela é atualizada
    Then o cartão mostra "Nenhuma condição definida. Este bloco não será aplicado automaticamente até ter ao menos uma condição."
    And os títulos "Conectivo", "Campo", "Operador" e "Valor" deixam de aparecer

  Scenario: Falha ao gravar a mudança
    Given que a gravação da configuração falha
    When o usuário muda uma condição
    Then o sistema exibe o erro e a tela é recarregada com a configuração gravada, sem a mudança
    # o comportamento é o da gravação automática; ver Consultar Configuração de Legendas EVT-LEG-01

  Scenario: Valor maior do que o sistema comporta
    Given que o usuário digitou no Valor um texto com mais de 1.000 caracteres
    When o sistema tenta gravar a configuração
    Then a gravação falha e a tela é recarregada com a configuração gravada
    # 🔍 a tela não limita o tamanho do valor e o limite de 1.000 caracteres vem de onde o dado é guardado; não foi executado
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| "Conectivo" | dado de código | entrada do usuário | editável | lista de opções | sim, a partir da segunda condição | "E" ou "OU"; nasce "E". Não existe na primeira condição do bloco |
| "Campo" | dado de código | entrada do usuário | editável | lista de opções | sim | "Grupo de trabalho", "Tema", "Cargo", "Nome fantasia" ou "Papel desempenhado"; nasce "Grupo de trabalho" e a lista não permite deixar em branco |
| "Operador" | dado de código | entrada do usuário | editável | lista de opções | sim | "Igual a", "Diferente de", "Contém" ou "Em (lista)"; nasce "Igual a" e a lista não permite deixar em branco |
| "Valor" | EventoLegendaCondicao | entrada do usuário | editável | texto | não ⚠️ | Texto livre de até 1.000 caracteres, sem conferência de conteúdo; a tela não limita o tamanho 💻. Com o operador "Em (lista)", valores separados por vírgula. GPE006 o dá como obrigatório 📄 |

*O texto de orientação do campo "Valor" é "Digite o valor"; com o operador "Em (lista)", "valores separados por vírgula".*

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| Bloco | O bloco em cujo cartão a condição foi incluída | Ao incluir a condição |
| Ordem | Posição da condição dentro do bloco (1, 2, 3…) | A cada gravação da configuração |
| Conectivo | Vazio na primeira condição do bloco, qualquer que seja o valor que ela tinha | A cada gravação da configuração |

---

## Dados lidos e gravados

| Entidade | Papel | Por que a feature a toca |
|---|---|---|
| EventoLegenda | lê e grava | A condição pertence a um bloco do evento, e a configuração é gravada por inteiro (regras 11 e 13) |
| Evento | lê | A gravação confirma que o evento existe (regra 13) |
| Legenda | lê | A gravação confirma que cada bloco corresponde a uma legenda do catálogo (regra 13) |

---

## Comportamento de tela

### Onde fica
Na tela Configuração de Legendas, dentro do cartão de cada bloco. As condições aparecem uma por linha, sob os títulos "Conectivo", "Campo", "Operador" e "Valor"; os títulos só aparecem quando o bloco tem ao menos uma condição. Em cada linha, o conectivo, o campo e o operador são listas de escolha, o valor é um campo de texto e, no fim, fica a lixeira com a dica "Remover condição". Na primeira linha o lugar do conectivo fica vazio, para manter as colunas alinhadas. Abaixo das linhas fica o botão "Adicionar condição".

Não há modo de edição nem botão de confirmar: a condição é alterada no lugar. A exclusão não pede confirmação. A ordem das condições é a de inclusão e não pode ser mudada; para trocar a ordem é preciso excluir e incluir de novo. 💻

⚠️ Diferenças em relação à tela de GPE006 📄: lá os rótulos ficam sobre cada campo ("Campo:", "Operador:", "Valor:"), o conectivo aparece entre as duas condições, o botão se chama "Adicionar Condição", o campo Valor traz sempre a dica "Para operador "Em (lista)", separe valores com vírgula" e, abaixo das condições, o quadro "Preview da condição" mostra a fórmula montada — por exemplo, "Tema igual 'Empresa'" seguida de "E Papeldesempenhado igual 'CEO'". O quadro de fórmula não existe hoje 💻.

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | "Salvando…", ao lado do título da tela, enquanto a mudança é gravada |
| Erro de validação | Não há: nenhum campo da condição é validado na tela, e o valor em branco é aceito ⚠️ |
| Erro de servidor | Erro "Erro Interno" com o detalhe enviado pelo servidor, e a tela volta à configuração gravada, descartando a mudança |
| Sucesso | "Salvo", ao lado do título da tela, por 2,5 segundos; não há mensagem de sucesso própria |
| Empty state | Bloco sem condições: "Nenhuma condição definida. Este bloco não será aplicado automaticamente até ter ao menos uma condição." |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Toda condição incluída, alterada ou excluída aparece do mesmo modo quando a configuração do evento é aberta de novo | Regra 13 · cenários do caminho feliz |
| SC-02 | Em todo bloco, a primeira condição não tem conectivo e cada uma das demais tem E ou OU | Regras 4 e 6 |
| SC-03 | As condições de um bloco em um evento não mudam quando o mesmo bloco é configurado em outro evento | Regra 11 |

---

## Métricas de tamanho

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Configurar Condições de Legenda | principal | EE | 2 | 7 | Média | 4 | 2026-10-04 |

### Memória de cálculo

**Configurar Condições de Legenda** — EE · ALR 2 · DER 7 · Média · 4 PF

```json
{"pe": "Configurar Condições de Legenda",
 "alr": ["Evento", "Legenda"],
 "der": ["Bloco", "Conectivo", "Campo", "Operador", "Valor", "Mensagem", "Ação"],
 "nao_contados": "Ordem é gerada pelo sistema. As listas de Conectivo, Campo e Operador são valores fixos, dado de código, e não geram lista consultada."}
```

Por que cada ALR:
1. `Evento` — grava as condições do bloco, que pertencem à configuração do evento
2. `Legenda` — confere que cada bloco da configuração corresponde a uma legenda do catálogo

Classificação: EE — a intenção primária é manter o arquivo lógico Evento, com as formas 1, 6, 7 e 12. Incluir, alterar e excluir a condição são o mesmo processo: a tela não tem modo de edição, e cada mudança regrava a condição.

**Total: 4 PF**

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade EventoLegendaCondicao

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Linha de condição | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/components/condicao-linha/condicao-linha.component.html` (linhas 1–70) e `.ts` (linhas 44–70) | — |
| Inclusão e exclusão de condição no cartão do bloco | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/components/bloco-evento-card/bloco-evento-card.component.ts` (linhas 41–72) e `.html` (linhas 42–72) | — |
| Listas fixas de campos, operadores e conectivos | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/services/legenda.interface.ts` (linhas 134–154) | — |
| Gravação imediata e gravação com pausa | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/pages/configuracao-legendas-evento/configuracao-legendas-evento.component.ts` (linhas 111–124 e 232–238) | — |
| Operação `PUT /administracao/eventos/{id}/legendas` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoController.java` (linhas 266–270) | — |
| Gravação das condições e listas admitidas | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/LegendaEventoServiceImpl.java` (linhas 121–137 e 171–196) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-10-04 | Claude (apf-cpm) | Contagem | Primeira contagem, pelo `PROMPT_CONTAGEM`: 4 PF — Configurar Condições de Legenda (EE Média, 4 PF). Confirmada em 2026-10-04 e espelhada em `global/CONTAGEM-PF.md` |
| 2026-10-04 | Claude (analise-impacto) | Origem atualizada | Elo com a AIM do ticket `PDTIC25148-34`, aberta na entrega: o ticket ganha linha própria na Origem, como Alteração, com os critérios CA-13 e CA-14; regras, campos e cenários inalterados |
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE006 – Gerenciar Regras de Legendas (funcionalidades "Incluir Regra de Legenda" e "Editar Regra de Legenda"), do ticket `PDTIC25148-34` do Jira e do código |

---

*Feature Set: Legendas · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
