<!-- docqui: 4.0.2 | prompt: PROMPT_CONTAGEM | atualizado: 2026-10-04 -->
---
id: EVT-LEG-06
feature_set: EVT-LEG
dominio: EVT
entidade: EventoPessoaLegenda
data_model_ref: data-models/eventos.md#eventopessoalegenda
endpoints: []
error_codes: []
depende_de: ["EVT-LEG-01", "EVT-LEG-02", "EVT-LEG-03"]
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

# Simular Aplicação de Legendas
> **Nível 3** - Feature Set: Legendas — Major Feature Set: Eventos - `EVT-LEG-06`

## Descrição

Permite que o Administrador simule a aplicação da configuração de legendas de um evento e veja quantos e quais participantes receberiam cada legenda, sem alterar nenhuma legenda nem a configuração gravada.

Na tela Configuração de Legendas, o botão Simular avalia a configuração como está na tela e abre uma janela com os totais (Participantes, Legendas removidas, Legendas aplicadas e Manuais preservadas) e uma tabela por legenda, que se expande para mostrar os nomes dos participantes. Da janela pode-se seguir direto para a geração, pelo botão Executar.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE006 – Gerenciar Regras de Legendas v1.0, de 03/10/2025 (documento legado), funcionalidade "Simular Execução das Regras de Legendas" ⚠️ sem chave na ferramenta de demandas | Criação | — Aplicar as regras configuradas sem gravar e apresentar o resumo da quantidade de pessoas selecionadas para cada legenda |
| [`PDTIC25148-34`](../../../analise-impacto/AIM-PDTIC25148-34.md) | Alteração | `CA-19` — simular as regras: quantas e quais pessoas seriam associadas a cada legenda, sem alterar dados. A relação nominal dos participantes vem do ticket; o documento pede só a quantidade 📄 |
<!-- trace-verified: PDTIC25148-34 @ f6bae69fe29f -->

---

<div class="dev-only">

## Superfície

**Modal** — origem: Consultar Configuração de Legendas `EVT-LEG-01` (`/regras-legenda/:eventoId`), botão "Simular" da barra de ações

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada. A imagem "Listar Regras de Legendas" de GPE006 mostra o comando "Simular Execução", mas não a tela do resultado

---

</div>

## Regras de negócio

1. A simulação não altera nada: nenhuma legenda de participante é atribuída ou apagada, e a configuração gravada do evento permanece como estava.
2. A simulação avalia a configuração como está no momento do acionamento, inclusive a alteração que ainda não terminou de ser gravada. 💻
3. A avaliação é a mesma da geração: quem entra, o que conta como condição completa, como as condições se combinam, o que cada operador faz e quem recebe a legenda de cada bloco. → ver Gerar Legendas do Evento `EVT-LEG-07`: regras 5 a 20
4. O resultado traz quatro totais: Participantes, que são todos os participantes do evento; Legendas removidas, que são as legendas não manuais que o evento tem hoje e que a geração apagaria; Legendas aplicadas, que é a soma, bloco a bloco, dos participantes que receberiam a legenda; e Manuais preservadas, que são as legendas manuais que o evento tem hoje. 💻
5. O total Legendas aplicadas conta atribuições, não pessoas: quem atende às condições de dois blocos é contado duas vezes, e por isso o total pode passar do total Participantes. 💻
6. Para cada bloco avaliado, o resultado traz o número, a cor e o nome da legenda, a quantidade de participantes que a receberiam e o nome de cada um. O bloco avaliado que não alcança ninguém aparece com quantidade zero. 💻 ⚠️ GPE006 pede só "um resumo da quantidade de pessoas selecionadas para cada legenda" 📄; os nomes vêm do ticket.
7. O bloco ignorado não entra no resultado por legenda: aparece, pelo nome, na relação de blocos ignorados. 💻 → ver Gerar Legendas do Evento `EVT-LEG-07`: regra 8
8. A simulação exige só que o evento exista. Ao contrário da gravação, não confere se há legenda repetida na configuração nem se o bloco ainda existe no catálogo; o bloco que saiu do catálogo é simulado com o nome e a cor que tinha quando a configuração foi aberta. 💻
9. Nada fica registrado da simulação: o resultado existe só enquanto a janela está aberta. 💻

---

## Cenários

```gherkin
Feature: Simular aplicação de legendas

  Background:
    Given que o usuário está autenticado no GPE
    And está na tela Configuração de Legendas de um evento

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Simular a configuração do evento
    Given que a configuração tem o bloco 1 "Comitê estratégico" e o bloco 2 "Diretores da CNI", os dois com condições completas
    When o usuário aciona "Simular"
    Then o sistema abre a janela "Simulação de aplicação de legendas"
    And a janela mostra os totais "Participantes", "Legendas removidas", "Legendas aplicadas" e "Manuais preservadas"
    And mostra uma linha por bloco, com "Nº", "Cor", "Legenda" e "Quantidade"
    And nenhuma legenda de participante é alterada

  Scenario: Ver quem receberia uma legenda
    Given que a janela da simulação mostra o bloco "Diretores da CNI" com quantidade 3
    When o usuário expande a linha do bloco
    Then o sistema lista os nomes dos três participantes que receberiam a legenda

  Scenario: Simular uma alteração recém-feita
    Given que o usuário acabou de digitar o valor de uma condição
    When o usuário aciona "Simular"
    Then o sistema avalia a configuração com o valor que está na tela

  Scenario: Seguir para a geração
    Given que a janela da simulação está aberta
    When o usuário aciona "Executar" na janela
    Then a janela se fecha e o sistema pede a confirmação da geração
    # a geração é a feature Gerar Legendas do Evento EVT-LEG-07

  Scenario: Fechar a simulação
    Given que a janela da simulação está aberta
    When o usuário aciona "Fechar"
    Then a janela se fecha e a tela Configuração de Legendas continua como estava

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há dado a validar
    When o usuário aciona "Simular"
    Then o sistema avalia a configuração sem solicitar nenhum dado e sem pedir confirmação

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Bloco sem condição completa
    Given que o bloco "Assento livre" não tem nenhuma condição com campo, operador e valor preenchidos
    When o usuário aciona "Simular"
    Then a janela mostra o aviso "Blocos ignorados: Assento livre"
    And o bloco não aparece na tabela por legenda

  Scenario: Participante que já tem a legenda do bloco como manual
    Given que "João Lima" tem a legenda "Diretores da CNI" atribuída manualmente
    And atende às condições do bloco "Diretores da CNI"
    When o usuário aciona "Simular"
    Then "João Lima" não é contado nem listado no bloco "Diretores da CNI"
    And a legenda manual dele entra no total "Manuais preservadas"

  Scenario: Evento que não existe mais
    Given que o evento da tela não existe
    When o usuário aciona "Simular"
    Then a janela não se abre
    And o sistema exibe o erro "Erro Interno" com o detalhe "Evento não encontrado."

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Simular Aplicação de Legendas" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Eventos, de onde se chega à Configuração de Legendas, e a ação não fica ao alcance dele
    # ⚠️ a tela não confere o perfil; ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Bloco que não alcança nenhum participante
    Given que nenhum participante atende às condições do bloco "ICT – Reitores"
    When o usuário aciona "Simular" e expande a linha do bloco
    Then a linha mostra quantidade 0
    And a parte expandida mostra "Nenhum participante nesta legenda."

  Scenario: Nenhum bloco avaliado
    Given que a configuração está vazia ou todos os blocos foram ignorados
    When o usuário aciona "Simular"
    Then a janela mostra os totais e, no lugar da tabela, "Nenhum bloco produziu resultado."

  Scenario: Falha na simulação
    Given que a simulação falha por motivo inesperado
    When o usuário aciona "Simular"
    Then a janela não se abre
    And o sistema exibe o erro "Erro Interno" com o detalhe "Ocorreu um erro inesperado. Contate o suporte."

  Scenario: Servidor sem resposta
    Given que o servidor não responde
    When o usuário aciona "Simular"
    Then o sistema exibe o erro "Erro" com o detalhe "Falha de comunicação com o servidor."
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| "Participantes" | derivado ↓ | calculado | somente leitura | número | — | Total de participantes do evento |
| "Legendas removidas" | derivado ↓ | calculado | somente leitura | número | — | Legendas não manuais que o evento tem no momento da simulação |
| "Legendas aplicadas" | derivado ↓ | calculado | somente leitura | número | — | Soma das quantidades de todos os blocos avaliados |
| "Manuais preservadas" | derivado ↓ | calculado | somente leitura | número | — | Legendas manuais que o evento tem no momento da simulação |
| "Blocos ignorados" | derivado ↓ | calculado | somente leitura | texto | — | Nomes dos blocos ignorados, separados por vírgula; só aparece quando há algum |

*A simulação não tem campos de entrada: avalia a configuração que está na tela.*

---

## Derivações

| Campo derivado | Fórmula (Label PO) | Campos-fonte (Entidade) |
|---|---|---|
| Participantes | Quantidade de participantes do evento, em qualquer situação de convite, confirmação ou check-in | Evento (EventoPessoa) |
| Legendas removidas | Quantidade de legendas do evento em que Manual é não | Manual (EventoPessoaLegenda) |
| Legendas aplicadas | Soma, bloco a bloco, da Quantidade de participantes que atendem às condições do bloco | Cargo e Nome fantasia (Pessoa), Grupo de Trabalho e Papel Desempenhado (GrupoTrabalhoPessoa), Tema (TemaPessoa) |
| Manuais preservadas | Quantidade de legendas do evento em que Manual é sim | Manual (EventoPessoaLegenda) |
| Blocos ignorados | Nome da legenda de cada bloco sem condição completa | Nome da legenda (Legenda), Campo, Operador e Valor (EventoLegendaCondicao) |

---

## Colunas do resultado

| Coluna (Label PO) | Origem | Ordenação |
|---|---|---|
| "Nº" | Posição do bloco na configuração simulada | padrão ↑ — a tabela segue a ordem dos blocos; não é ordenável |
| "Cor" | Cor da legenda, do catálogo de blocos | — |
| "Legenda" | Nome da legenda, do catálogo de blocos | — |
| "Quantidade" | derivado: participantes que atendem às condições do bloco e não têm a mesma legenda como manual | — |
| Nomes dos participantes (parte expandida da linha, sem rótulo) | Nome da pessoa de cada participante que receberia a legenda | ❓ nenhuma fonte define a ordem dos nomes |

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| — | — | Nenhum campo é gravado: a simulação só calcula e mostra |

---

## Dados lidos e gravados

| Entidade | Papel | Por que a feature a toca |
|---|---|---|
| Evento | lê | Confirma que o evento existe (regra 8) |
| EventoLegenda | lê | Os blocos avaliados são os da configuração do evento, como estão na tela (regra 2) |

---

## Comportamento de tela

### Onde fica
Na tela Configuração de Legendas, o botão "Simular" fica na barra de ações, à direita, ao lado de "Executar". O resultado abre numa janela com o título "Simulação de aplicação de legendas", sobre a tela. ⚠️ Em GPE006 o comando se chama "Simular Execução" 📄; na tela, "Simular" 💻.

A janela mostra, de cima para baixo: quatro cartões de totais, com os rótulos "Participantes", "Legendas removidas", "Legendas aplicadas" e "Manuais preservadas"; o aviso "Blocos ignorados: " seguido dos nomes, quando há bloco ignorado; e a tabela por legenda, com as colunas "Nº", "Cor", "Legenda" e "Quantidade". Cada linha da tabela tem uma seta que a expande para listar os nomes dos participantes. A tabela não tem paginação nem ordenação. No rodapé ficam os botões "Fechar" e "Executar".

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Não há indicador de processamento: a janela só aparece quando o resultado chega 💻 |
| Erro de validação | Não se aplica — a simulação não tem campos de entrada |
| Erro de servidor | A janela não se abre. Erro "Erro Interno" com o detalhe enviado pelo servidor — "Evento não encontrado." ou, em falha inesperada, "Ocorreu um erro inesperado. Contate o suporte."; sem resposta do servidor, erro "Erro" com o detalhe "Falha de comunicação com o servidor." |
| Sucesso | Janela "Simulação de aplicação de legendas" com os totais, o aviso de blocos ignorados, quando há, e a tabela por legenda |
| Empty state | Tabela sem nenhum bloco avaliado: "Nenhum bloco produziu resultado."; linha expandida de bloco sem participantes: "Nenhum participante nesta legenda." |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Depois de qualquer simulação, as legendas dos participantes e a configuração gravada do evento são as mesmas de antes | Regra 1 |
| SC-02 | Para a mesma configuração e os mesmos participantes, a quantidade e os nomes mostrados em cada bloco coincidem com quem recebe a legenda na geração | Regra 3 |
| SC-03 | Todo bloco da configuração aparece no resultado: na tabela por legenda, se foi avaliado, ou na relação de blocos ignorados | Regras 6 e 7 |

---

## Métricas de tamanho

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Simular Aplicação de Legendas | principal | SE | 3 | 12 | Média | 5 | 2026-10-04 |

### Memória de cálculo

**Simular Aplicação de Legendas** — SE · ALR 3 · DER 12 · Média · 5 PF

```json
{"pe": "Simular Aplicação de Legendas",
 "alr": ["Evento", "Pessoa", "Legenda"],
 "der": ["Participantes", "Legendas removidas", "Legendas aplicadas", "Manuais preservadas", "Blocos ignorados", "Nº", "Cor", "Legenda", "Quantidade", "Nome do participante", "Mensagem", "Ação"],
 "nao_contados": "As condições da configuração em tela entram como parâmetro e não estão descritas como campo desta feature; contadas, seriam mais 4 DER e a faixa não mudaria."}
```

Por que cada ALR:
1. `Evento` — lê os participantes, as legendas que eles já têm e os blocos e as condições da configuração
2. `Pessoa` — lê o cargo, o nome fantasia, os grupos de trabalho, os papéis e os temas que as condições avaliam, e o nome mostrado em cada legenda
3. `Legenda` — lê o nome e a cor de cada bloco avaliado

Classificação: SE — a intenção primária é apresentar, com processamento além da recuperação: forma 2 (os quatro totais e a quantidade por bloco são cálculos) e forma 9 (a relação de quem receberia cada legenda é dado derivado). Não atualiza arquivo lógico.

**Total: 5 PF**

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade EventoPessoaLegenda

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Botão "Simular" e abertura da janela | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/pages/configuracao-legendas-evento/configuracao-legendas-evento.component.ts` (linhas 259–267) e `.html` (linhas 36–37 e 87–91) | — |
| Janela do resultado | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/components/simulacao-dialog/simulacao-dialog.component.html` (linhas 1–85) e `.ts` (linhas 21–38) | — |
| Serviço de simulação | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento/services/evento-legenda.service.ts` (linhas 35–37) | — |
| Operação `POST /administracao/eventos/{id}/legendas/simular` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoController.java` (linhas 272–276) | — |
| Avaliação dos blocos sem gravar | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/LegendaEventoServiceImpl.java` (linhas 202–210 e 229–405) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-10-04 | Claude (apf-cpm) | Contagem | Primeira contagem, pelo `PROMPT_CONTAGEM`: 5 PF — Simular Aplicação de Legendas (SE Média, 5 PF). Confirmada em 2026-10-04 e espelhada em `global/CONTAGEM-PF.md` |
| 2026-10-04 | Claude (analise-impacto) | Origem atualizada | Elo com a AIM do ticket `PDTIC25148-34`, aberta na entrega: o ticket ganha linha própria na Origem, como Alteração, com o critério CA-19; regras, campos e cenários inalterados |
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE006 – Gerenciar Regras de Legendas (funcionalidade "Simular Execução das Regras de Legendas"), do ticket `PDTIC25148-34` do Jira e do código |

---

*Feature Set: Legendas · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
