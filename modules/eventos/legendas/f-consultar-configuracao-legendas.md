<!-- docqui: 4.0.2 | prompt: PROMPT_CONTAGEM | atualizado: 2026-10-04 -->
---
id: EVT-LEG-01
feature_set: EVT-LEG
dominio: EVT
entidade: EventoLegenda
data_model_ref: data-models/eventos.md#eventolegenda
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
  pendente: false
  revisada_em: "2026-10-04"
  revisada_ate: "PDTIC25148-34"
---

# Consultar Configuração de Legendas
> **Nível 3** - Feature Set: Legendas — Major Feature Set: Eventos - `EVT-LEG-01`

## Descrição

Permite que o Administrador consulte a configuração de legendas de um evento: os blocos de legenda em ordem de prioridade, cada um com seu número, sua cor, seu nome e as condições que decidem quem recebe a legenda.

A consulta abre pelo ícone Configuração de Legendas, em cada linha da lista de eventos. A tela mostra um cartão por bloco, sem pedir nenhum dado, e é dela que partem as demais ações sobre a configuração, como adicionar bloco, simular e gerar as legendas. O que se altera nessa tela é gravado na hora, sem botão de salvar.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE006 – Gerenciar Regras de Legendas v1.0, de 03/10/2025 (documento legado), funcionalidade "Listar Regras de Legendas" ⚠️ sem chave na ferramenta de demandas | Criação | — Listar e consultar as regras de legendas de um evento |
| [`PDTIC25148-34`](../../../analise-impacto/AIM-PDTIC25148-34.md) | Alteração | `CA-06, CA-08` — numeração por evento (o número do bloco é a posição dele na configuração) e blocos sem estado ativo ou inativo. O ticket reformulou o que o documento descreve: em vez de todas as legendas configuráveis, ativas e inativas, a tela traz só os blocos adicionados ao evento 💻 |
<!-- trace-verified: PDTIC25148-34 @ f6bae69fe29f -->

---

<div class="dev-only">

## Superfície

**Tela própria** — rota `/regras-legenda/:eventoId`

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada. A imagem "Listar Regras de Legendas" de GPE006 retrata o modelo anterior ⚠️

---

</div>

## Regras de negócio

1. A configuração de legendas é do evento: os blocos, a ordem e as condições de um evento não interferem nos de outro. 💻
2. Todo bloco presente na configuração está em vigor. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 11 ⚠️ GPE006 diz que "A lista apresenta todas as legendas passíveis de configuração" e que só as ativas exibem as configurações 📄; hoje a configuração traz apenas os blocos que foram adicionados ao evento 💻.
3. O número do bloco é a posição que ele ocupa na configuração do evento — 1, 2, 3, sem saltos —, recalculada a cada alteração. O número não pertence ao catálogo: o mesmo bloco pode ter números diferentes em eventos diferentes. 💻
4. A posição do bloco é a ordem de aplicação e a prioridade da legenda. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 9
5. O nome e a cor de cada bloco são os do catálogo no momento da consulta: o que se altera no catálogo aparece na configuração de todos os eventos que usam o bloco. 💻
6. A configuração é gravada por inteiro a cada alteração concluída: os blocos, a ordem e as condições informados substituem o que estava gravado. Não há rascunho nem confirmação posterior. 💻 ⚠️ GPE006 traz, na imagem do documento, o comando "Salvar Regras" 📄, que não existe mais.
7. A configuração só é gravada quando o evento existe, cada bloco corresponde a uma legenda do catálogo, nenhuma legenda aparece em mais de um bloco e todo campo, operador e conectivo preenchido pertence à lista admitida. 💻
8. O bloco sem condição e a condição incompleta são aceitos na gravação; ficam fora apenas da avaliação. 💻 → ver Gerar Legendas do Evento `EVT-LEG-07`: regras 7 e 8
9. A alteração cuja gravação falha não permanece: a configuração volta a ser a que estava gravada. 💻
10. Não fica registrado quem alterou a configuração nem quando. 💻

---

## Cenários

```gherkin
Feature: Consultar configuração de legendas

  Background:
    Given que o usuário está autenticado no GPE
    And está na lista de eventos

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Abrir a configuração de um evento com blocos
    Given que o evento "Reunião da MEI" tem três blocos configurados
    When o usuário aciona "Configuração de Legendas" na linha de "Reunião da MEI"
    Then o sistema abre a tela "Configuração de Legendas" com o nome "Reunião da MEI" e a contagem "3 blocos configurados"
    And mostra um cartão por bloco, na ordem dos números 1, 2 e 3, cada um com o número, a cor e o nome da legenda

  Scenario: Ver as condições de um bloco
    Given que o bloco 1 "Comitê estratégico" tem duas condições
    When o usuário abre a configuração do evento
    Then o cartão do bloco mostra as condições sob os títulos "Conectivo", "Campo", "Operador" e "Valor"
    And a primeira condição não tem conectivo

  Scenario: Alteração gravada automaticamente
    Given que o usuário está na tela "Configuração de Legendas"
    When o usuário conclui uma alteração na configuração
    Then o sistema grava a configuração inteira do evento
    And a tela mostra "Salvando…" enquanto grava e "Salvo" quando termina
    # as alterações são as das features Adicionar Bloco, Configurar Condições, Reordenar Blocos, Remover Bloco e Carregar Configuração

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há dado a validar
    When o usuário aciona "Configuração de Legendas" na linha de um evento
    Then o sistema abre a configuração sem solicitar nenhum dado

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Gravação recusada pelo servidor
    Given que o usuário está na tela "Configuração de Legendas"
    And um bloco da configuração foi excluído do catálogo depois de aberta a tela
    When o usuário conclui uma alteração na configuração
    Then o sistema exibe o erro "Erro Interno" com o detalhe "Bloco de legenda inexistente: " seguido do número interno do bloco
    And a tela é recarregada com a configuração gravada, sem a alteração
    # 🔍 caminho deduzido do código; não foi executado

  Scenario: Evento que não existe
    Given que o endereço da tela traz o número de um evento que não existe
    When o usuário abre a tela
    Then a tela mostra "Nenhum bloco configurado", sem o nome do evento e sem aviso
    And qualquer alteração é recusada com o erro "Erro Interno" e o detalhe "Evento não encontrado."
    # ⚠️ a consulta não confere se o evento existe 💻

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Consultar Configuração de Legendas" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Eventos, de onde se chega à Configuração de Legendas, e a tela não fica ao alcance dele
    # ⚠️ a tela não confere o perfil; ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Evento sem nenhum bloco
    Given que o evento não tem nenhum bloco configurado
    When o usuário abre a configuração do evento
    Then a tela mostra a contagem "0 blocos configurados"
    And mostra "Nenhum bloco configurado" com o texto "Adicione o primeiro bloco de legenda para começar a montar as regras deste evento." e o botão "Adicionar bloco"

  Scenario: Bloco sem condições
    Given que um bloco do evento não tem nenhuma condição
    When o usuário abre a configuração do evento
    Then o cartão do bloco mostra "Nenhuma condição definida. Este bloco não será aplicado automaticamente até ter ao menos uma condição."

  Scenario: Endereço sem evento
    Given que o endereço da tela não traz um número de evento válido
    When o usuário abre a tela
    Then o sistema exibe o erro "Erro" com o detalhe "Evento não informado na URL."
    And a tela fica como a de um evento sem blocos

  Scenario: Falha ao carregar a configuração
    Given que a consulta à configuração falha
    When o usuário abre a configuração do evento
    Then o sistema exibe o erro "Erro Interno" com o detalhe "Ocorreu um erro inesperado. Contate o suporte."
    And a tela fica como a de um evento sem blocos, com "Nenhum bloco configurado"
    # ⚠️ a falha de carga e o evento sem blocos têm a mesma aparência; ver Comportamento de tela

  Scenario: Falha ao gravar uma alteração
    Given que o usuário está na tela "Configuração de Legendas"
    And a gravação da configuração falha
    When o usuário conclui uma alteração na configuração
    Then o sistema exibe o erro e deixa de mostrar "Salvando…"
    And a tela é recarregada com a configuração gravada, descartando o que não foi gravado

  Scenario: Servidor sem resposta
    Given que o servidor não responde
    When o usuário abre a configuração do evento
    Then o sistema exibe o erro "Erro" com o detalhe "Falha de comunicação com o servidor."
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| — | EventoLegenda | — | — | — | — | A consulta não tem campos de entrada nem filtros: abre a configuração do evento escolhido na lista de eventos |

---

## Colunas do resultado

| Coluna (Label PO) | Origem | Ordenação |
|---|---|---|
| Número do bloco (sem rótulo; dica "Ordem de aplicação") | Posição do bloco na configuração do evento | padrão ↑ — os cartões seguem a ordem dos números; não é ordenável |
| Cor (amostra, sem rótulo) | Cor do bloco no catálogo | — |
| Nome da legenda (sem rótulo) | Nome do bloco no catálogo | — |
| "Conectivo" | Condição do bloco; vazio na primeira condição | — |
| "Campo" | Condição do bloco | — |
| "Operador" | Condição do bloco | — |
| "Valor" | Condição do bloco | — |

*Cada bloco é um cartão; as quatro últimas linhas da tabela (Conectivo, Campo, Operador e Valor) se repetem para cada condição do bloco, na ordem em que as condições foram postas.*

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| — | — | A consulta não grava nada. A numeração dos blocos é recalculada pelas features que alteram a configuração |

---

## Dados lidos e gravados

| Entidade | Papel | Por que a feature a toca |
|---|---|---|
| Evento | lê | O nome do evento aparece no alto da tela |
| Legenda | lê | Nome e cor de cada bloco vêm do catálogo (regra 5) |
| EventoLegendaCondicao | lê | As condições de cada bloco aparecem no cartão |

---

## Comportamento de tela

### Onde fica
Na lista de eventos (Pesquisar Eventos `EVT-CAD-01`), o ícone "Configuração de Legendas" de cada linha abre a tela, que tem o título "Configuração de Legendas". ⚠️ GPE006 chama a opção de "Regras de Execução" e a tela de "Configuração de Regras de Legendas" 📄.

No alto ficam o título, o nome do evento e a contagem "{n} bloco configurado" ou "{n} blocos configurados". Abaixo, a barra de ações com os botões "Carregar configuração", "Salvar como preset", "Gerenciar catálogo" e "Adicionar bloco", à esquerda, e "Simular" e "Executar", à direita. ⚠️ Em GPE006 a barra tem "Salvar Regras", "Simular Execução", "Executar Regras" e "Resetar" 📄; "Salvar Regras" e "Resetar" não existem mais.

Segue um cartão por bloco. O cabeçalho do cartão traz o número do bloco, com a dica "Ordem de aplicação", a amostra da cor e o nome da legenda; à direita, as setas "Mover para cima" e "Mover para baixo" e o botão "Remover bloco do evento". O corpo traz as condições, uma por linha, sob os títulos "Conectivo", "Campo", "Operador" e "Valor", e o botão "Adicionar condição". ⚠️ A tela de GPE006 tinha, em cada legenda, a chave "Ativa" ou "Inativa", o quadro "Preview da condição", com a fórmula montada a partir das condições, e, no rodapé, os quadros "Importante" e "Dicas" 📄; nada disso existe hoje 💻.

A tela não confere o perfil de quem a abre; ver a nota da matriz de permissões no N2. ⚠️ Por um efeito da forma como os endereços foram declarados, o endereço da configuração sem o número do evento abre o Catálogo de blocos, e o endereço do catálogo seguido de um número abre a configuração daquele evento 💻.

### Gravação automática
Não há botão de salvar: cada alteração concluída na tela grava a configuração inteira do evento. Adicionar, remover e mover um bloco, adicionar e excluir uma condição e trocar o conectivo, o campo ou o operador gravam na hora. A digitação do valor de uma condição grava depois de uma pausa de pouco mais de meio segundo (600 milissegundos) e, de novo, quando o usuário sai do campo. Se uma alteração chega enquanto a gravação anterior ainda está em andamento, a tela deixa de esperar a anterior e envia a nova, que leva a configuração inteira. 💻

Ao lado do título, a tela mostra "Salvando…", com um indicador giratório, enquanto grava, e "Salvo" quando a gravação termina; "Salvo" some depois de 2,5 segundos.

Quando a gravação falha, a tela mostra o erro, deixa de mostrar "Salvando…" e busca de novo a configuração no servidor: o que não foi gravado é descartado e os cartões voltam a mostrar o que está gravado. 💻

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Na abertura não há indicador de carregamento: até a configuração chegar, a tela mostra "0 blocos configurados" e "Nenhum bloco configurado" 💻 ⚠️ parece defeito — uma alteração feita nesse intervalo, ou depois de uma falha de carga, gravaria por cima da configuração real 🔍. Durante a gravação: "Salvando…" |
| Erro de validação | Não se aplica — a consulta não tem campos |
| Erro de servidor | Erro "Erro Interno" com o detalhe enviado pelo servidor. Na gravação, o detalhe pode ser "Evento não encontrado.", "Bloco de legenda inexistente: " seguido do número interno do bloco, "A configuração tem blocos de legenda repetidos.", "Campo de condição inválido: ", "Operador de condição inválido: " ou "Conectivo inválido: " seguidos do valor recusado; em falha inesperada, "Ocorreu um erro inesperado. Contate o suporte."; sem resposta do servidor, erro "Erro" com o detalhe "Falha de comunicação com o servidor." ⚠️ O título é "Erro Interno" mesmo quando o detalhe é uma regra de negócio. O nome do evento que não pôde ser lido fica em branco, sem aviso |
| Sucesso | Cartões dos blocos na ordem dos números. Depois de cada gravação, "Salvo" por 2,5 segundos |
| Empty state | "Nenhum bloco configurado", com o texto "Adicione o primeiro bloco de legenda para começar a montar as regras deste evento." e o botão "Adicionar bloco". No cartão do bloco sem condições: "Nenhuma condição definida. Este bloco não será aplicado automaticamente até ter ao menos uma condição." |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Ao abrir a configuração de um evento, todos os blocos gravados aparecem na ordem dos seus números, cada um com cor, nome e condições | Cenários "Abrir a configuração de um evento com blocos" e "Ver as condições de um bloco" |
| SC-02 | Os números dos blocos de um evento formam sempre a sequência 1, 2, 3, sem saltos nem repetições | Regra 3 |
| SC-03 | Toda alteração concluída fica gravada sem nenhuma ação adicional do usuário e, se a gravação falha, a tela volta a mostrar o que está gravado | Regras 6 e 9 · cenários "Alteração gravada automaticamente" e "Falha ao gravar uma alteração" |

---

## Métricas de tamanho

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Consultar Configuração de Legendas | principal | CE | 2 | 10 | Média | 4 | 2026-10-04 |

### Memória de cálculo

**Consultar Configuração de Legendas** — CE · ALR 2 · DER 10 · Média · 4 PF

```json
{"pe": "Consultar Configuração de Legendas",
 "alr": ["Evento", "Legenda"],
 "der": ["Nome do evento", "Número do bloco", "Cor", "Nome da legenda", "Conectivo", "Campo", "Operador", "Valor", "Mensagem", "Ação"],
 "nao_contados": "A contagem de blocos configurados do alto da tela é o tamanho da lista exibida, informação de posicionamento (Guia STI 5.5). Os botões da barra de ações pertencem a outras features."}
```

Por que cada ALR:
1. `Evento` — lê os blocos da configuração, a ordem deles, as condições de cada bloco e o nome do evento mostrado no alto da tela
2. `Legenda` — lê o nome e a cor de cada bloco, que são os do catálogo

Classificação: CE — a intenção primária é apresentar, com as formas de lógica 7 (referencia arquivos lógicos), 8 (recupera dados), 11 (apresenta) e 13 (ordena pela posição). Não há cálculo nem dado derivado: o número do bloco é atributo guardado.

**Total: 4 PF**

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade EventoLegenda

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Tela: carga da configuração, indicador e gravação automática | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/pages/configuracao-legendas-evento/configuracao-legendas-evento.component.ts` (linhas 107–204) e `.html` (linhas 4–63) | — |
| Cartão de bloco | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/components/bloco-evento-card/bloco-evento-card.component.html` (linhas 1–74) | — |
| Serviço de leitura e de gravação | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento/services/evento-legenda.service.ts` (linhas 25–32) | — |
| Endereços da tela | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/legendas-routing.module.ts` (linhas 7–16) | — |
| Operações `GET` e `PUT /administracao/eventos/{id}/legendas` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoController.java` (linhas 261–270) | — |
| Leitura, gravação e exigências da gravação | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/LegendaEventoServiceImpl.java` (linhas 86–142 e 171–196) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-10-04 | Claude (apf-cpm) | Contagem | Primeira contagem, pelo `PROMPT_CONTAGEM`: 4 PF — Consultar Configuração de Legendas (CE Média, 4 PF). Confirmada em 2026-10-04 e espelhada em `global/CONTAGEM-PF.md` |
| 2026-10-04 | Claude (analise-impacto) | Origem atualizada | Elo com a AIM do ticket `PDTIC25148-34`, aberta na entrega: o ticket ganha linha própria na Origem, como Alteração, com os critérios CA-06 e CA-08; regras, campos e cenários inalterados |
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE006 – Gerenciar Regras de Legendas (funcionalidade "Listar Regras de Legendas"), do ticket `PDTIC25148-34` do Jira e do código |

---

*Feature Set: Legendas · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
