<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: EVT-PAR-11
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

# Liberar Todos os Assentos
> **Nível 3** - Feature Set: Participantes — Major Feature Set: Eventos - `EVT-PAR-11`

## Descrição

Permite que o Administrador libere de uma só vez todos os assentos do mapa do evento; o mapa fica vazio e todos os participantes que estavam sentados voltam à lista de pessoas disponíveis, para que a distribuição recomece.

No mapa de assentos, o botão "Limpar Todas", do painel "Gerenciar Pessoas Alocadas na Mesa", esvazia o mapa na hora, sem pedir confirmação.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE005 – Gerenciar Participante v1.1, de 16/12/2025 (documento legado), funcionalidade "Limpar Todas as Marcações de Assento do Participante" ⚠️ sem chave na ferramenta de demandas | Criação | — Remover todos os participantes dos seus assentos pela opção "Limpar Todas", deixando o mapa vazio e todas as pessoas disponíveis para novo vínculo. ⚠️ No código, o mapa é esvaziado só na tela de quem acionou a opção: a limpeza não é gravada 💻. Ticket do Jira relacionado pelo título, concluído e sem AIM aberta 🔍: `PDTIC25148-16` (Mapa de mesa) |

---

<div class="dev-only">

## Superfície

**Ação em tela** — origem: Consultar Mapa de Assentos `EVT-PAR-07` (`/evento-pessoa/:id`, visão Mapa de Assentos, versão do Administrador), botão "Limpar Todas" do painel "Gerenciar Pessoas Alocadas na Mesa"

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Consultar Mapa de Assentos — Perfil Administrador" de GPE005

---

</div>

## Regras de negócio

1. Liberar todos os assentos tira do assento cada participante sentado e devolve todos às pessoas disponíveis; o mapa fica sem nenhum assento ocupado.
2. A liberação não muda o convite, a confirmação nem o check-in de ninguém. 💻
3. A liberação não chega ao servidor: vale só no mapa aberto de quem a acionou. O mapa sem ninguém sentado nunca é enviado para gravação (→ ver Atribuir Assento ao Participante `EVT-PAR-08`: regra 6), e a operação do servidor que libera todos os assentos de um evento existe, mas nada na interface a aciona. 💻 ⚠️ Suspeita forte de defeito, conferida por leitura do código, sem execução. GPE005 diz que, acionada a opção, "o mapa de assentos é limpo, ficando vazio" 📄 — a intenção é que a limpeza valha para todos.
4. Enquanto nada é gravado, o servidor continua guardando os assentos anteriores: eles reaparecem quando o mapa é recarregado e quando a atualização automática percebe uma mudança feita em outro ponto do sistema. 💻 🔍
5. A liberação só se consolida se, depois dela, pelo menos um participante receber assento e o mapa for gravado: a gravação substitui todas as atribuições anteriores pelas novas. → ver Atribuir Assento ao Participante `EVT-PAR-08`: regra 4 💻
6. Se a operação do servidor fosse acionada, além de liberar os assentos ela devolveria a não atendido todo participante que tinha assento. 💻 ❓ Nenhuma fonte diz se liberar o mapa deve desfazer os atendimentos já registrados.

---

## Cenários

```gherkin
Feature: Liberar todos os assentos

  Background:
    Given que o usuário está autenticado no GPE
    And está no mapa de assentos de um evento, na versão do Administrador

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Liberar todos os assentos do mapa
    Given que há 12 participantes sentados no mapa
    When o usuário aciona "Limpar Todas"
    Then todos os assentos ficam vazios na tela
    And os 12 participantes voltam para a lista "Pessoas Disponíveis"
    And o sistema exibe: "Sucesso" com o detalhe "Todas as alocações foram removidas da mesa."
    And os botões "Salvar Alocações (0)" e "Limpar Todas" ficam desabilitados
    # ⚠️ não há pedido de confirmação 💻
    # ⚠️ a mensagem afirma a remoção, mas nada foi gravado: ver o grupo de conflitos

  Scenario: Montar um novo mapa depois de liberar
    Given que o usuário liberou todos os assentos
    When ele atribui assento a pelo menos um participante e o mapa é gravado
    Then o mapa gravado passa a ter só as novas atribuições, e as anteriores deixam de existir

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Mapa já vazio
    Given que nenhum participante está sentado
    When o usuário olha o painel "Gerenciar Pessoas Alocadas na Mesa"
    Then o botão "Limpar Todas" está desabilitado

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Recarregar a tela depois de liberar
    Given que o usuário liberou todos os assentos e não atribuiu nenhum outro
    When ele recarrega a tela, ou outro usuário abre o mapa do evento
    Then o mapa aparece com todos os participantes nos assentos que tinham antes da liberação
    # ⚠️ suspeita forte de defeito, conferida por leitura do código, sem execução: a liberação não é gravada 💻

  Scenario: Mudança de outro usuário chega depois de liberar
    Given que o usuário liberou todos os assentos e o mapa continua aberto
    When a recepção registra o check-in de um participante
    Then a atualização automática refaz o mapa com o que está gravado, e os assentos anteriores reaparecem na tela, sem aviso
    # ⚠️ 🔍 inferido da leitura do código, não executado

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Liberar Todos os Assentos" na matriz do N2
    When o usuário abre o mapa de assentos
    Then a tela não traz o painel "Gerenciar Pessoas Alocadas na Mesa" nem o botão "Limpar Todas"
    # ⚠️ quem não chega ao mapa nem vê a opção; ver a nota da matriz no N2 sobre o que o servidor confere

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Mapa carregando ou gravando
    Given que o mapa está sendo carregado ou gravado
    When o usuário olha o painel "Gerenciar Pessoas Alocadas na Mesa"
    Then o botão "Limpar Todas" está desabilitado

  Scenario: Administrador no tablet
    Given que o usuário está em um tablet
    When ele abre o mapa de assentos
    Then a tela não mostra o painel "Gerenciar Pessoas Alocadas na Mesa", e a liberação de todos os assentos não fica disponível

  Scenario: Liberar o mapa de um evento de mesa retangular invertida
    Given que o evento tem formato de mesa "Retangular Invertido"
    When o usuário aciona "Limpar Todas"
    Then o desenho do mapa passa a ter as quantidades de assentos do formato "Retangular": aparecem posições a mais nos setores B, C, F e H, e o setor E perde os assentos E24 a E30
    And o desenho só volta ao normal quando o mapa é refeito
    # ⚠️ 🔍 suspeita de defeito, lida no código e não executada: as posições a mais não correspondem a assento nenhum do evento
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| — | EventoPessoa | — | — | — | — | A ação não tem campos: alcança todos os participantes sentados no mapa, sem confirmação |

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| — | — | Nenhum campo é gravado: a liberação fica só no mapa aberto (regra 3) ⚠️ |

---

## Comportamento de tela

### Onde fica
No mapa de assentos do Administrador, no painel "Gerenciar Pessoas Alocadas na Mesa", acima do desenho dos assentos, o botão "Limpar Todas", com um ícone de lixeira, ao lado do botão "Salvar Alocações (n)". O botão fica desabilitado quando não há ninguém sentado e enquanto o mapa carrega ou grava. No tablet o painel inteiro não é mostrado. 💻

Não há pergunta de confirmação: um clique esvazia o mapa. ⚠️ A ação alcança o mapa inteiro e não tem como ser desfeita pela tela — embora hoje, por não ser gravada, se desfaça sozinha ao recarregar. A mensagem "Todas as alocações foram removidas da mesa." aparece sempre, mesmo sem nada ter sido gravado.

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Sem indicador próprio: a liberação acontece na tela, de imediato |
| Erro de validação | Não há mensagem: sem ninguém sentado, o botão "Limpar Todas" fica desabilitado |
| Erro de servidor | Não se aplica — a ação não consulta nem grava nada no servidor ⚠️ |
| Sucesso | "Sucesso" com o detalhe "Todas as alocações foram removidas da mesa."; todos os assentos vazios e todos os participantes em "Pessoas Disponíveis" |
| Empty state | Mapa sem ninguém sentado: os botões "Salvar Alocações (0)" e "Limpar Todas" ficam desabilitados |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Acionada a liberação, nenhum assento aparece ocupado e todos os participantes que estavam sentados constam na lista de pessoas disponíveis do Administrador | Regra 1 · cenário "Liberar todos os assentos do mapa" |
| SC-02 | Depois da liberação, o mapa aparece vazio para qualquer usuário que o abra, inclusive depois de recarregar a tela ⚠️ hoje não atendido | Regra 3 · cenário "Recarregar a tela depois de liberar" |
| SC-03 | Um mapa montado depois da liberação substitui por inteiro o anterior | Regra 5 · cenário "Montar um novo mapa depois de liberar" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Liberar Todos os Assentos | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade EventoPessoa

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Botão "Limpar Todas" e limpeza na tela | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/components/mesa/components/retangular/retangular.component.ts` (linhas 1571–1628) e `.html` (linhas 95–98) | — |
| Gravação que não envia mapa vazio | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/components/mesa/components/retangular/retangular.component.ts` (linhas 1421–1431, 1517–1521) e `.html` (linhas 91–92) | — |
| Formato invertido: limpeza que redesenha com as quantidades do retangular | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/components/mesa/components/retangular-invertido/retangular-invertido.component.ts` (linhas 1558–1615) | — |
| Serviço de eventos, sem chamada à operação de limpeza | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento/services/evento.service.ts` (linhas 68–76) | — |
| Operação `DELETE /administracao/eventos/{eventoId}/composicoes-mesa`, sem chamador na interface | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoController.java` (linhas 195–203) e `service/impl/EventoServiceImpl.java` (linhas 413–422) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

O que foi conferido no código: `limparComposicoesMesa()` da tela zera as listas locais e chama `agendarSalvamentoAutomatico()`; 30 s depois, `executarSalvamentoAutomatico()` retorna sem enviar nada porque não há pessoas alocadas; `salvarComposicoesMesa()` da tela só avisa "Não há pessoas alocadas na mesa para salvar."; e a busca por `composicoes-mesa` em todo o código da interface só encontra o `POST` e um `GET` sem chamador — o `DELETE` não é chamado em lugar nenhum.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE005 – Gerenciar Participante (funcionalidade "Limpar Todas as Marcações de Assento do Participante") e do código |

---

*Feature Set: Participantes · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
