<!-- docqui: 4.0.2 | prompt: PROMPT_CONTAGEM | atualizado: 2026-10-04 -->
---
id: EVT-LEG-08
feature_set: EVT-LEG
dominio: EVT
entidade: PresetLegenda
data_model_ref: data-models/eventos.md#presetlegenda
endpoints: []
error_codes: []
depende_de: ["EVT-LEG-01"]
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

# Salvar Preset de Legendas
> **Nível 3** - Feature Set: Legendas — Major Feature Set: Eventos - `EVT-LEG-08`

## Descrição

Permite que o Administrador guarde com um nome a configuração de legendas do evento — os blocos, a ordem e as condições —, deixando-a disponível na biblioteca de presets para ser aplicada a qualquer outro evento.

Na tela Configuração de Legendas do evento, o botão Salvar como preset abre uma janela que pede o nome e, se desejado, uma descrição. Confirmado, o preset passa a constar na Biblioteca de presets, de onde é aplicado por Carregar Configuração de Legendas.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| [`PDTIC25148-34`](../../../analise-impacto/AIM-PDTIC25148-34.md) | Criação | `CA-15` — guardar com um nome a configuração atual do evento, com os blocos e as regras, para reúso. Especificada a partir do código-fonte (engenharia reversa de 2026-09-30); a funcionalidade não consta nos documentos legados ⚠️. A descrição opcional, a unicidade do nome e o registro do evento de origem não estão no ticket: vêm do código 💻 |
<!-- trace-verified: PDTIC25148-34 @ f6bae69fe29f -->

---

<div class="dev-only">

## Superfície

**Modal** — origem: Consultar Configuração de Legendas `EVT-LEG-01` (`/regras-legenda/:eventoId`), botão "Salvar como preset" da barra de ações

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada, ainda em teste — os documentos legados não trazem imagem dela

---

</div>

## Regras de negócio

1. Todo preset tem nome. 💻
2. O nome identifica o preset na biblioteca e é único: não existem dois presets com o mesmo nome. 💻 ❓ Nenhuma fonte diz se nomes que só diferem por maiúsculas e minúsculas contam como iguais: o código compara o nome como foi escrito, e o resultado depende de como o sistema guarda e compara textos.
3. A descrição do preset é opcional. 💻
4. O preset guarda um retrato da configuração do evento no instante em que é salvo: os blocos, a ordem deles e as condições de cada bloco. O que mudar depois na configuração do evento não chega ao preset. 💻
5. O preset guarda o nome do evento de origem como cópia, sem ficar ligado a ele: não acompanha mudança de nome nem exclusão do evento. 💻
6. O preset pertence à biblioteca, não ao evento: salvo a partir de um evento, pode ser aplicado a qualquer outro. 💻
7. O conteúdo da configuração não é conferido ao salvar: blocos sem condição e condições incompletas entram no preset como estão, e a configuração sem nenhum bloco também é aceita. 💻 ⚠️ Um preset vazio, aplicado em modo de substituição, esvazia a configuração do evento de destino — ver Carregar Configuração de Legendas `EVT-LEG-09`.
8. Salvar o preset não altera o evento, a configuração dele nem as legendas dos participantes. 💻
9. O preset salvo não pode ser alterado: não há edição do nome, da descrição nem do conteúdo. Para corrigi-lo, exclui-se o preset (Excluir Preset de Legendas `EVT-LEG-10`) e salva-se outro. 💻

---

## Cenários

```gherkin
Feature: Salvar preset de legendas

  Background:
    Given que o usuário está autenticado no GPE
    And está na tela "Configuração de Legendas" de um evento

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Salvar a configuração do evento como preset
    Given que o evento "Reunião da MEI" tem os blocos "Anfitrião", "Palestrantes" e "Diretores da CNI", nessa ordem, cada um com as suas condições
    When o usuário aciona "Salvar como preset"
    And informa "Nome do preset" com "Reuniões da MEI" e "Descrição" com "Padrão das reuniões ordinárias"
    And aciona "Salvar preset"
    Then o sistema guarda o preset com os três blocos, na mesma ordem e com as mesmas condições, e com "Reunião da MEI" como evento de origem
    And exibe: "Preset salvo" com o detalhe "O preset 'Reuniões da MEI' foi salvo."
    And o preset passa a constar na "Biblioteca de presets" da janela "Carregar configuração" de qualquer evento
    And a configuração do evento continua como estava

  Scenario: Salvar preset sem descrição
    When o usuário aciona "Salvar como preset"
    And informa só o "Nome do preset"
    And aciona "Salvar preset"
    Then o sistema guarda o preset sem descrição

  Scenario: Desistir de salvar
    When o usuário aciona "Salvar como preset"
    And aciona "Cancelar" ou fecha a janela
    Then nenhum preset é criado
    And ao reabrir a janela os campos voltam em branco

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Nome do preset vazio
    When o usuário deixa "Nome do preset" vazio ou só com espaços
    And aciona "Salvar preset"
    Then a janela continua aberta e o sistema exibe abaixo do campo: "Este campo é obrigatório"
    And nenhum preset é criado
    # 💻 o servidor repete a conferência e tem a mensagem "O nome do preset é obrigatório."; pela tela ela não chega a aparecer, porque o nome vazio é barrado antes do envio

  Scenario: Nome ou descrição além do tamanho aceito
    When o usuário digita em "Nome do preset" além de 100 caracteres ou em "Descrição" além de 255
    Then o campo deixa de aceitar caracteres ao atingir o limite
    # 💻 o limite é só da tela; o servidor não confere tamanho

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Nome de preset já usado
    Given que já existe na biblioteca um preset chamado "Reuniões da MEI"
    When o usuário informa "Nome do preset" com "Reuniões da MEI" e aciona "Salvar preset"
    Then o sistema não cria o segundo preset
    And exibe o erro "Erro Interno" com o detalhe "Já existe um preset com este nome."
    # ⚠️ a janela se fecha ao acionar "Salvar preset", antes da resposta do servidor: a recusa chega com a janela já fechada, e o nome e a descrição digitados se perdem 💻
    # ⚠️ o resumo é "Erro Interno" embora o motivo seja uma regra de negócio 💻

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Salvar Preset de Legendas" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Eventos › Cadastro, por onde se chega à Configuração de Legendas, e a ação não fica ao alcance dele
    # ⚠️ a tela não confere o perfil; ver a nota da matriz no N2
    # 💻 no servidor, a gravação de preset está declarada só para o Administrador

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Evento sem nenhum bloco configurado
    Given que a configuração do evento está vazia
    When o usuário aciona "Salvar como preset", informa o nome e aciona "Salvar preset"
    Then o sistema guarda um preset sem nenhum bloco
    And exibe: "Preset salvo"
    # ⚠️ nada impede salvar preset vazio 💻; na biblioteca ele aparece com "0 blocos" e, aplicado em modo de substituição, esvazia a configuração do evento de destino

  Scenario: Configuração com bloco sem condição ou com condição incompleta
    Given que um bloco do evento não tem condição, ou tem condição sem valor
    When o usuário salva o preset
    Then o sistema guarda o bloco no preset como está, sem aviso

  Scenario: Falha inesperada ao salvar
    Given que o servidor falha ao gravar o preset
    When o usuário aciona "Salvar preset" com o nome preenchido
    Then nenhum preset é criado
    And o sistema exibe o erro "Erro Interno" com o detalhe "Ocorreu um erro inesperado. Contate o suporte."
    # 💻 quando a resposta de erro vem sem conteúdo, o texto é "Erro" com o detalhe "Falha de comunicação com o servidor."
    # 💻 o servidor tem ainda a mensagem "Não foi possível salvar a configuração do preset.", para o caso de não conseguir montar o retrato; pela tela não há como provocá-la
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| Nome do preset | PresetLegenda | entrada do usuário | editável | texto | sim | Até 100 caracteres, limite imposto pela tela; não pode ficar vazio nem só com espaços; os espaços no início e no fim são descartados; não pode repetir o nome de outro preset |
| Descrição | PresetLegenda | entrada do usuário | editável | texto | não | Até 255 caracteres, limite imposto pela tela; os espaços no início e no fim são descartados |

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| Evento de origem | Nome do evento em que o preset foi salvo, copiado como texto | Ao salvar |
| Data de criação | Data e hora do momento da gravação | Ao salvar |
| Configuração | Os blocos, a ordem e as condições do evento, como estão na tela | Ao salvar |

⚠️ O evento de origem e a data de criação são guardados, mas nenhuma tela os mostra 💻: na Biblioteca de presets, o cartão do preset traz só o nome, a quantidade de blocos, a descrição e os blocos.

---

## Dados lidos e gravados

| Entidade | Papel | Por que a feature a toca |
|---|---|---|
| Evento | lê | Fornece o nome gravado como evento de origem (regra 5) |
| EventoLegenda | lê | Os blocos e a ordem que compõem o retrato (regra 4). 💻 O retrato sai da configuração já aberta na tela, não de uma nova consulta — a contagem deve decidir se isso é leitura desta feature |
| EventoLegendaCondicao | lê | As condições de cada bloco do retrato (regra 4), com a mesma ressalva da linha acima |
| Legenda | lê | Cada bloco do retrato aponta para um bloco do catálogo e leva o nome e a cor que ele tinha ao salvar |

---

## Comportamento de tela

### Onde fica
Na tela Configuração de Legendas do evento, na barra de ações, o botão "Salvar como preset" fica entre "Carregar configuração" e "Gerenciar catálogo". Ele abre a janela "Salvar como preset" sobre a tela, com o campo "Nome do preset", marcado com asterisco e com a dica "Digite um nome para o preset", o campo "Descrição", de três linhas e com a dica "Descrição opcional", e os botões "Cancelar" e "Salvar preset". A janela abre sempre em branco. 💻

O que vai para o preset é a configuração como está na tela naquele instante. O botão fica disponível mesmo quando o evento não tem nenhum bloco. A janela se fecha assim que "Salvar preset" é acionado com o nome preenchido, sem esperar a resposta do servidor: se a gravação for recusada, a mensagem aparece com a janela já fechada e o que foi digitado se perde. 💻 ⚠️

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Sem indicador: a janela se fecha ao confirmar e nada sinaliza que a gravação está em andamento 💻 |
| Erro de validação | "Este campo é obrigatório", abaixo de "Nome do preset", quando o campo fica vazio ou só com espaços — ao sair dele ou ao acionar "Salvar preset". Os campos não aceitam digitação além do limite |
| Erro de servidor | Erro "Erro Interno" com o texto enviado pelo servidor no detalhe: "Já existe um preset com este nome." quando o nome se repete, "Ocorreu um erro inesperado. Contate o suporte." em falha inesperada. Resposta de erro sem conteúdo: "Erro" com o detalhe "Falha de comunicação com o servidor." |
| Sucesso | Mensagem "Preset salvo" com o detalhe "O preset '{nome}' foi salvo."; a tela da configuração continua como estava |
| Empty state | Não se aplica — a janela é um formulário. Evento sem blocos não impede o uso ⚠️ |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | O preset salvo aparece na Biblioteca de presets de qualquer evento com os mesmos blocos, na mesma ordem e com as mesmas condições que o evento tinha ao salvar | Regras 4 e 6 · cenário "Salvar a configuração do evento como preset" |
| SC-02 | Não existem dois presets com o mesmo nome, e a tentativa de repetir um nome informa o motivo | Regra 2 · cenário "Nome de preset já usado" |
| SC-03 | Alterar ou excluir o evento de origem depois de salvar não muda o conteúdo do preset | Regras 4 e 5 |

---

## Métricas de tamanho

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Salvar Preset de Legendas | principal | EE | 3 | 4 | Média | 4 | 2026-10-04 |

### Memória de cálculo

**Salvar Preset de Legendas** — EE · ALR 3 · DER 4 · Média · 4 PF

```json
{"pe": "Salvar Preset de Legendas",
 "alr": ["PresetLegenda", "Evento", "Legenda"],
 "der": ["Nome do preset", "Descrição", "Mensagem", "Ação"],
 "nao_contados": "Evento de origem, Data de criação e Configuração são preenchidos pelo sistema a partir do evento aberto e não são informados pelo usuário."}
```

Por que cada ALR:
1. `PresetLegenda` — grava o preset e confere que o nome não se repete
2. `Evento` — fornece a configuração que o preset copia e o nome gravado como evento de origem
3. `Legenda` — fornece o nome e a cor de cada bloco do retrato

Classificação: EE — a intenção primária é manter o arquivo lógico PresetLegenda, com as formas 1, 6, 7 e 12. O N3 registra que o retrato sai da configuração já aberta na tela; pela visão lógica, o processo copia dados do evento para o preset, e por isso Evento e Legenda entram como arquivos referenciados.

**Total: 4 PF**

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade PresetLegenda

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Janela "Salvar como preset" | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/components/salvar-preset-dialog/salvar-preset-dialog.component.ts` (linhas 43–69) e `.html` (linhas 1–25) | — |
| Botão, montagem do preset e mensagens | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/pages/configuracao-legendas-evento/configuracao-legendas-evento.component.ts` (linhas 251–253 e 310–322) e `.html` (linhas 29–30 e 74–77) | — |
| Serviço de presets | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/services/legenda-catalogo.service.ts` (linhas 70–73) | — |
| Operação `POST /administracao/legendas/presets` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/LegendaController.java` (linhas 77–80) | — |
| Validação do nome e gravação do retrato | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/PresetLegendaServiceImpl.java` (linhas 85–113 e 136–142) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada e em teste (ticket `PDTIC25148-34`); o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

No armazenamento, o nome do preset comporta 150 caracteres e a descrição, 500; os limites de 100 e 255 são só da tela. A unicidade do nome é garantida também por restrição do banco.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-10-04 | Claude (apf-cpm) | Contagem | Primeira contagem, pelo `PROMPT_CONTAGEM`: 4 PF — Salvar Preset de Legendas (EE Média, 4 PF). Confirmada em 2026-10-04 e espelhada em `global/CONTAGEM-PF.md` |
| 2026-10-04 | Claude (analise-impacto) | Origem atualizada | Elo com a AIM do ticket `PDTIC25148-34`, aberta na entrega: o ticket passa a ser a Origem da feature (Criação), com o critério CA-15; regras, campos e cenários inalterados |
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do código e do ticket `PDTIC25148-34` do Jira (critério CA15); a funcionalidade não consta no documento legado GPE006 – Gerenciar Regras de Legendas |

---

*Feature Set: Legendas · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
