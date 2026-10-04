<!-- docqui: 4.0.2 | prompt: PROMPT_CONTAGEM | atualizado: 2026-10-04 -->
---
id: EVT-PAR-05
feature_set: EVT-PAR
dominio: EVT
entidade: EventoPessoaLegenda
data_model_ref: data-models/eventos.md#eventopessoalegenda
endpoints: []
error_codes: []
depende_de: ["EVT-PAR-04"]
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

# Alterar Legenda do Participante
> **Nível 3** - Feature Set: Participantes — Major Feature Set: Eventos - `EVT-PAR-05`

## Descrição

Permite que o Administrador altere a legenda de um participante do evento, atribuindo-lhe manualmente uma legenda do catálogo; a legenda escolhida passa a identificá-lo na lista e no mapa de assentos e não é desfeita quando as legendas do evento são geradas de novo.

Na janela Gerenciar Legenda da Pessoa, escolhe-se uma legenda em Selecione uma Legenda e aciona-se Salvar.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE005 – Gerenciar Participante v1.1, de 16/12/2025 (documento legado), funcionalidade "Alterar Legenda do Participante" ⚠️ sem chave na ferramenta de demandas | Criação | — Alterar a legenda de um participante e, quando ele não tem legenda, selecionar e atribuir uma, a partir da consulta de legenda |
| [`PDTIC25148-34`](../../../analise-impacto/AIM-PDTIC25148-34.md) | Alteração | — Sem critério numerado: a legenda escolhida nesta feature é a manual, única por participante e guardada na associação Evento – Pessoa – Legenda que o ticket descreve 💻. A preservação da legenda manual na geração é critério de Gerar Legendas do Evento `EVT-LEG-07`. A retirada de "Assento livre" das opções veio com o ticket `PDTIC25148-35` e pertence a Consultar Legenda do Participante `EVT-PAR-04`, que monta a lista |
<!-- trace-verified: PDTIC25148-34 @ f6bae69fe29f -->

---

<div class="dev-only">

## Superfície

**Ação em tela** — origem: Consultar Legenda do Participante `EVT-PAR-04` (janela "Gerenciar Legenda da Pessoa", sobre `/evento-pessoa/:id`), botão "Salvar"

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Consultar Legenda do Participante" de GPE005 (`GPE005-04.png`)

---

</div>

## Regras de negócio

1. A legenda atribuída por esta feature é manual. 💻
2. O participante tem no máximo uma legenda manual: atribuir outra substitui a anterior. 💻
3. A legenda manual é a que identifica o participante, à frente das que ele recebeu por regra. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 9
4. A legenda manual não é desfeita pela geração das legendas do evento. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 10
5. As legendas que o participante recebeu por regra continuam guardadas; apenas deixam de ser a que o identifica. 💻
6. Quando a legenda escolhida é uma que o participante já tinha recebido por regra, essa mesma atribuição passa a ser manual, sem duplicar. 💻
7. A legenda escolhida não precisa fazer parte da configuração do evento. 💻 ⚠️ Nesse caso o participante fica com uma legenda sem número de ordem no evento.
8. A alteração vale só para o evento aberto: a mesma pessoa mantém, em outros eventos, a legenda que tiver neles. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 8
9. "Assento livre" não é atribuída a participante. 💻 ⚠️ A restrição está apenas na relação de opções oferecida; o servidor não a recusaria.
10. Quem fez a alteração não fica guardado. 💻 ⚠️ O sistema não registra o autor de nenhuma ação.

---

## Cenários

```gherkin
Feature: Alterar legenda do participante

  Background:
    Given que o usuário está autenticado no GPE
    And abriu a janela "Gerenciar Legenda da Pessoa" de um participante

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Atribuir legenda a participante sem legenda manual
    Given que a participante "Ana Reis" não tem legenda manual
    When o usuário seleciona "Palestrantes" em "Selecione uma Legenda:"
    And aciona "Salvar"
    Then o sistema guarda "Palestrantes" como legenda manual de "Ana Reis"
    And exibe: "Sucesso" com o detalhe "Legenda atualizada com sucesso!"
    And fecha a janela e recarrega a página atual da lista de participantes
    And a linha de "Ana Reis" passa a mostrar "Palestrantes" e a cor dessa legenda

  Scenario: Trocar a legenda manual
    Given que o participante "Paulo Henrique" tem a legenda manual "Anfitrião"
    When o usuário seleciona "Palestrantes" e aciona "Salvar"
    Then "Palestrantes" passa a ser a única legenda manual de "Paulo Henrique"
    And exibe: "Sucesso" com o detalhe "Legenda atualizada com sucesso!"

  Scenario: Tornar manual uma legenda recebida por regra
    Given que o participante recebeu por regra as legendas "Comitê estratégico" e "Empresas – diretores"
    And a que o identifica é "Comitê estratégico"
    When o usuário seleciona "Empresas – diretores" e aciona "Salvar"
    Then "Empresas – diretores" passa a ser manual e a identificar o participante
    And "Comitê estratégico" continua guardada como legenda recebida por regra

  Scenario: Desistir da alteração
    Given que o usuário selecionou outra legenda
    When aciona "Cancelar"
    Then a janela é fechada e a legenda do participante continua a mesma

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Salvar sem legenda selecionada, sem legenda manual
    Given que o participante não tem legenda manual
    And nenhuma legenda está selecionada
    When o usuário aciona "Salvar"
    Then o sistema exibe o aviso "Atenção" com o detalhe "Esta pessoa já não possui legenda."
    And nada é alterado

  Scenario: Salvar sem legenda selecionada, com legenda manual
    Given que o participante tem legenda manual
    And o usuário selecionou a opção "Remover legenda"
    When aciona "Salvar"
    Then o sistema segue para a remoção da legenda, com o pedido de confirmação
    # a remoção está em Remover Legenda do Participante (EVT-PAR-06)

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Legenda excluída do catálogo depois de aberta a tela
    Given que a legenda selecionada foi excluída do catálogo por outro usuário
    When o usuário aciona "Salvar"
    Then o sistema exibe: "Erro" com o detalhe "Erro ao salvar legenda da pessoa."
    And a legenda do participante continua a mesma
    # ⚠️ o servidor informa o motivo ("Legenda inexistente:" seguido do identificador), mas a tela não o mostra 💻

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Alterar Legenda do Participante" na matriz do N2
    When o usuário vê a lista de participantes
    Then o valor da coluna "Assento" é texto simples e a janela de legenda não fica ao alcance dele
    # ⚠️ a tela só retira o atalho da Secretaria Check-In; ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Legenda fora da configuração do evento
    Given que a legenda "Diretores da CNI" está no catálogo e não está na configuração do evento
    When o usuário a seleciona e aciona "Salvar"
    Then o sistema a guarda como legenda manual do participante, sem restrição
    # ⚠️ a legenda fica sem número de ordem no evento; ver a regra 7 💻

  Scenario: Salvar sem mudar a legenda
    Given que a legenda manual do participante já está selecionada
    When o usuário aciona "Salvar"
    Then o sistema grava de novo a mesma legenda e exibe a mensagem de sucesso

  Scenario: Falha ao salvar
    Given que a gravação falha no servidor
    When o usuário aciona "Salvar"
    Then o sistema exibe: "Erro" com o detalhe "Erro ao salvar legenda da pessoa."
    And a janela continua aberta, com a seleção feita
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| "Selecione uma Legenda:" | Legenda | entrada do usuário | editável | seleção → Legenda | sim | Uma única legenda do catálogo; "Assento livre" não é oferecida 💻. Abre com a legenda manual do participante já destacada. ⚠️ GPE005 traz uma relação fixa de valores, de "1 – Anfitrião" a "16 – Assento livre" 📄; hoje as opções vêm do catálogo |

*Os dados do participante e a legenda atual, que a janela mostra acima da lista, são somente leitura e estão em Consultar Legenda do Participante (`EVT-PAR-04`).*

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| Manual | Sim | Ao salvar |
| Data de atribuição | Data e hora do salvamento 💻 | Quando a legenda escolhida ainda não estava atribuída ao participante. ⚠️ Quando ela já existia por regra e apenas se torna manual, a data não é atualizada 💻 |

---

## Dados lidos e gravados

| Entidade | Papel | Por que a feature a toca |
|---|---|---|
| EventoPessoaLegenda | lê e grava | Recebe a legenda manual do participante e perde a manual anterior (regras 1, 2 e 6) |
| EventoPessoa | lê | Confere que o participante existe antes de gravar a legenda |

---

## Comportamento de tela

### Onde fica
Na janela "Gerenciar Legenda da Pessoa", aberta pela coluna "Assento" da lista de participantes (Consultar Legenda do Participante, `EVT-PAR-04`). A legenda é escolhida com um toque na lista "Selecione uma Legenda:", que destaca a opção selecionada, e gravada pelo botão "Salvar", no rodapé da janela, ao lado de "Cancelar".

Depois de salvar, a janela se fecha e a lista de participantes é recarregada na mesma página, já com a nova legenda e a nova cor na linha do participante.

⚠️ O mapa de assentos pode continuar mostrando a cor anterior: a atualização automática da tela só refaz o mapa quando muda o check-in, a confirmação, o assento ou o número de participações de alguém, e a troca de legenda não está entre esses sinais 🔍 — conclusão tirada da leitura do código, sem execução. Recarregar a tela traz a cor nova.

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | O botão "Salvar" mostra o indicador de carregamento, e os botões da janela ficam desabilitados até a resposta |
| Erro de validação | Aviso "Atenção" com o detalhe "Esta pessoa já não possui legenda.", ao salvar sem legenda selecionada um participante que não tem legenda manual |
| Erro de servidor | "Erro" com o detalhe "Erro ao salvar legenda da pessoa."; a janela continua aberta. ⚠️ O motivo informado pelo servidor não é mostrado |
| Sucesso | "Sucesso" com o detalhe "Legenda atualizada com sucesso!"; a janela se fecha e a lista é recarregada |
| Empty state | Não se aplica — a ação só existe dentro da janela de legenda |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Depois de salvar, a lista de participantes mostra a legenda escolhida na linha do participante, e o mapa de assentos, ao ser aberto de novo, o identifica pela mesma legenda | Regra 3 · cenário "Atribuir legenda a participante sem legenda manual" |
| SC-02 | Uma nova geração das legendas do evento mantém a legenda atribuída manualmente | Regra 4 |
| SC-03 | Nenhum participante fica com duas legendas manuais | Regra 2 · cenário "Trocar a legenda manual" |

---

## Métricas de tamanho

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Alterar Legenda do Participante | principal | EE | 2 | 3 | Baixa | 3 | 2026-10-04 |

### Memória de cálculo

**Alterar Legenda do Participante** — EE · ALR 2 · DER 3 · Baixa · 3 PF

```json
{"pe": "Alterar Legenda do Participante",
 "alr": ["Evento", "Legenda"],
 "der": ["Selecione uma Legenda", "Mensagem", "Ação"],
 "nao_contados": "Manual e Data de atribuição são preenchidos pelo sistema. O participante é o da janela já aberta."}
```

Por que cada ALR:
1. `Evento` — grava a legenda manual do participante, retira a manual anterior e confere que o participante existe
2. `Legenda` — confere que a legenda escolhida existe no catálogo

Classificação: EE — a intenção primária é manter o arquivo lógico Evento, na legenda do participante, com as formas 1, 5, 6, 7 e 12.

**Total: 3 PF**

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade EventoPessoaLegenda

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Seleção da legenda, botão "Salvar" e mensagens | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/components/evento-pessoas-list/evento-pessoas-list.component.ts` (linhas 371–411 e 445–452) e `.html` (linhas 232–263 e 288–294) | — |
| Chamada ao servidor | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento/services/evento-legenda.service.ts` (linhas 59–61) | — |
| Operação `PUT /administracao/eventos/participante/legenda` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoController.java` (linhas 297–302) | — |
| Gravação da legenda manual | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/LegendaEventoServiceImpl.java` (linhas 459–504) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

Recusas do servidor, todas apresentadas pela tela com o mesmo texto genérico: "Participante não informado.", "Participante não encontrado." e "Legenda inexistente: " seguido do identificador. A tela tem ainda o aviso "Atenção" com o detalhe "Erro interno: pessoa não selecionada.", para o caso de não haver participante escolhido; nenhuma ação da tela chega a ele.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-10-04 | Claude (apf-cpm) | Contagem | Primeira contagem, pelo `PROMPT_CONTAGEM`: 3 PF — Alterar Legenda do Participante (EE Baixa, 3 PF). Confirmada em 2026-10-04 e espelhada em `global/CONTAGEM-PF.md` |
| 2026-10-04 | Claude (analise-impacto) | Origem atualizada | Elo com a AIM do ticket `PDTIC25148-34`, aberta na entrega: o ticket ganha linha própria na Origem, como Alteração, sem critério numerado; os critérios que a Origem citava aqui ficam em Gerar Legendas do Evento `EVT-LEG-07` e em Consultar Legenda do Participante `EVT-PAR-04`; regras, campos e cenários inalterados |
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE005 – Gerenciar Participante (funcionalidade "Alterar Legenda do Participante"), do código e dos tickets `PDTIC25148-34` e `PDTIC25148-35` do Jira |

---

*Feature Set: Participantes · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
