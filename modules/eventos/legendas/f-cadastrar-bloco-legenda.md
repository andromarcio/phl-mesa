<!-- docqui: 4.0.2 | prompt: PROMPT_CONTAGEM | atualizado: 2026-10-04 -->
---
id: EVT-LEG-12
feature_set: EVT-LEG
dominio: EVT
entidade: Legenda
data_model_ref: data-models/eventos.md#legenda
endpoints: []
error_codes: []
depende_de: ["EVT-LEG-11"]
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

# Cadastrar Bloco de Legenda
> **Nível 3** - Feature Set: Legendas — Major Feature Set: Eventos - `EVT-LEG-12`

## Descrição

Permite que o Administrador inclua no catálogo um bloco de legenda, com nome e cor; o bloco fica disponível para ser usado na configuração de legendas de qualquer evento.

No Catálogo de blocos, o botão Novo bloco abre uma janela com o nome e a cor. O mesmo cadastro pode ser feito sem sair da configuração de um evento, pela aba Criar novo bloco da janela Adicionar bloco; nesse caso, o bloco criado já entra na configuração do evento.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| [`PDTIC25148-34`](../../../analise-impacto/AIM-PDTIC25148-34.md) | Criação | `CA-02, CA-03, CA-04` — criar um bloco no catálogo, inclusive a partir de uma busca sem resultado, com o nome já preenchido pelo termo buscado, e deixá-lo disponível aos demais eventos. O atalho que abre a criação a partir da busca fica na janela de Adicionar Bloco de Legenda ao Evento `EVT-LEG-02`. Especificada a partir do código-fonte (engenharia reversa de 2026-09-30); a funcionalidade não consta nos documentos legados ⚠️. ⚠️ `CA-02` pede nome, cor da legenda e composição de mesa; o código só tem nome e cor 💻 |
<!-- trace-verified: PDTIC25148-34 @ f6bae69fe29f -->

---

<div class="dev-only">

## Superfície

**Modal** — são **duas** origens, com o mesmo formulário:

- Catálogo — Pesquisar Blocos de Legenda `EVT-LEG-11` (`/catalogo-legendas`), botão "Novo bloco", que abre a janela "Novo bloco"
- Configuração do evento — Adicionar Bloco de Legenda ao Evento `EVT-LEG-02` (janela "Adicionar bloco", aberta sobre `/regras-legenda/:eventoId`), aba "Criar novo bloco"

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada, ainda em teste — os documentos legados não trazem imagem dela

---

</div>

## Regras de negócio

1. O bloco tem nome e cor, e os dois são obrigatórios. 💻 ⚠️ O ticket `PDTIC25148-34` pede também a composição de mesa na criação do bloco (CA02); no código o bloco só tem nome e cor — a composição de mesa foi retirada dele. Confirmar com o PO se o critério foi abandonado.
2. O nome do bloco é único no catálogo, sem diferenciar maiúsculas de minúsculas: "Palestrantes" e "palestrantes" são o mesmo nome. 💻
3. O nome é guardado sem espaços no início e no fim. 💻
4. A cor é guardada como código no formato `#RRGGBB` — o sinal `#` seguido de seis dígitos hexadecimais. 💻
5. Dois blocos podem ter a mesma cor: só o nome é único. 💻
6. O bloco cadastrado pertence ao catálogo e fica disponível a todos os eventos. 💻
7. Cadastrar o bloco não o põe em uso: ele só passa a valer num evento quando entra na configuração desse evento, o que é Adicionar Bloco de Legenda ao Evento `EVT-LEG-02`. 💻
8. O bloco do catálogo não tem número, posição nem condições: tudo isso pertence à configuração de cada evento. 💻
9. Cada bloco é cadastrado do zero: não há cópia de bloco existente. 💻

---

## Cenários

```gherkin
Feature: Cadastrar bloco de legenda

  Background:
    Given que o usuário está autenticado no GPE

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Cadastrar um bloco pelo catálogo
    Given que o usuário está na tela "Catálogo de blocos"
    When o usuário aciona "Novo bloco"
    And informa "Nome da legenda" com "Palestrantes"
    And escolhe uma cor na paleta de cores sugeridas
    And aciona "Salvar"
    Then o sistema inclui o bloco no catálogo
    And exibe: "Bloco criado" com o detalhe "O bloco foi criado com sucesso."
    And a janela se fecha e a lista é recarregada a partir da primeira página

  Scenario: Cadastrar um bloco com cor fora da paleta
    Given que o usuário está na janela "Novo bloco"
    When o usuário escolhe a cor no seletor de cor, em vez de usar a paleta
    And informa o nome e aciona "Salvar"
    Then o sistema inclui o bloco com a cor escolhida, guardada como código em letras maiúsculas

  Scenario: Cadastrar um bloco sem escolher cor
    Given que o usuário está na janela "Novo bloco"
    When o usuário informa só o nome e aciona "Salvar"
    Then o sistema inclui o bloco com a primeira cor da paleta, que já vem marcada

  Scenario: Cadastrar um bloco de dentro da configuração do evento
    Given que o usuário está na tela "Configuração de Legendas" de um evento
    When o usuário aciona "Adicionar bloco" e abre a aba "Criar novo bloco"
    And informa o nome e a cor
    And aciona "Criar e adicionar"
    Then o sistema inclui o bloco no catálogo
    And, em seguida, o bloco entra na configuração do evento, como último, sem condições
    # 💻 a entrada na configuração do evento é a feature Adicionar Bloco de Legenda ao Evento (EVT-LEG-02); aqui não há mensagem de sucesso do cadastro, só o indicador "Salvo" da configuração

  Scenario: Cadastrar um bloco a partir de uma busca sem resultado
    Given que o usuário está na janela "Adicionar bloco", na aba "Usar bloco existente"
    And que a busca por "Imprensa" não encontrou nenhum bloco
    When o usuário aciona o atalho 'Adicionar bloco "Imprensa"'
    Then a janela passa à aba "Criar novo bloco" com "Nome da legenda" já preenchido com "Imprensa"

  Scenario: Desistir do cadastro
    Given que o usuário está na janela "Novo bloco"
    When o usuário aciona "Cancelar" ou fecha a janela
    Then nenhum bloco é incluído

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Nome da legenda vazio
    When o usuário deixa "Nome da legenda" vazio
    And aciona "Salvar" ou "Criar e adicionar"
    Then a janela continua aberta e o sistema exibe abaixo do campo: "Este campo é obrigatório"
    And nenhum bloco é incluído

  Scenario: Nome da legenda só com espaços
    When o usuário preenche "Nome da legenda" só com espaços
    And aciona "Salvar"
    Then o sistema não inclui o bloco
    And exibe o erro "Erro Interno" com o detalhe "O nome do bloco de legenda é obrigatório."
    # ⚠️ a tela aceita o nome só com espaços e quem recusa é o servidor; o resumo é "Erro Interno" embora o motivo seja de preenchimento 💻

  Scenario: Nome da legenda além do tamanho aceito
    When o usuário digita em "Nome da legenda" além de 100 caracteres
    Then o campo deixa de aceitar caracteres ao atingir o limite
    # 💻 o limite é só da tela; o servidor não confere tamanho

  Scenario: Cor fora do formato
    When o cadastro chega ao servidor sem cor ou com cor fora do formato "#RRGGBB"
    Then o servidor recusa com a mensagem "A cor deve estar no formato #RRGGBB."
    # 💻 pela tela isso não acontece: a cor vem sempre da paleta ou do seletor, já no formato

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Já existe bloco com o mesmo nome
    Given que o catálogo já tem o bloco "Palestrantes"
    When o usuário informa "Nome da legenda" com "palestrantes" e aciona "Salvar"
    Then o sistema não inclui o bloco
    And exibe o erro "Erro Interno" com o detalhe "Já existe um bloco de legenda com este nome."
    And a janela continua aberta, com o que foi digitado
    # ⚠️ a tela não confere o nome repetido antes de enviar; o resumo é "Erro Interno" embora o motivo seja uma regra de negócio 💻

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Cadastrar Bloco de Legenda" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Administração › Catálogo de legendas nem Eventos › Cadastro, e a ação não fica ao alcance dele
    # ⚠️ a tela não confere o perfil; ver a nota da matriz no N2
    # 💻 no servidor, a inclusão de bloco está declarada só para o Administrador

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Falha inesperada ao cadastrar
    Given que o servidor falha ao gravar o bloco
    When o usuário aciona "Salvar"
    Then nenhum bloco é incluído e a janela continua aberta
    And o sistema exibe o erro "Erro Interno" com o detalhe "Ocorreu um erro inesperado. Contate o suporte."
    # 💻 no catálogo, a resposta de erro sem conteúdo produz "Erro" com o detalhe "Falha de comunicação com o servidor."; na janela "Adicionar bloco", não produz mensagem alguma ⚠️ 🔍

  Scenario: Bloco criado e não acrescentado ao evento
    Given que o usuário cadastrou o bloco pela janela "Adicionar bloco"
    And que a gravação da configuração do evento falhou logo depois
    When a tela volta a mostrar a configuração gravada
    Then o bloco novo existe no catálogo, mas não está na configuração do evento
    # 🔍 inferido da leitura do código: o cadastro e a entrada na configuração são duas gravações separadas
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| Nome da legenda | Legenda | entrada do usuário | editável | texto | sim | Até 100 caracteres, limite imposto pela tela; os espaços no início e no fim são descartados; não pode repetir o nome de outro bloco, sem diferenciar maiúsculas de minúsculas |
| Cor | Legenda | entrada do usuário | editável | texto | sim | Código de cor no formato `#RRGGBB`, escolhido na paleta de cores sugeridas ou no seletor de cor; vem preenchido com a primeira cor da paleta; é guardado em letras maiúsculas |

⚠️ O ticket `PDTIC25148-34` prevê um terceiro dado na criação do bloco, a composição de mesa (CA02). O código não tem esse campo 💻.

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| — | — | Nenhum campo é preenchido pelo sistema: o bloco guarda só o nome e a cor informados, sem data de criação nem autor 💻 |

---

## Comportamento de tela

### Onde fica
No Catálogo de blocos, o botão "Novo bloco", no cabeçalho, abre a janela "Novo bloco", com o formulário do bloco e os botões "Cancelar" e "Salvar"; "Salvar" fica desabilitado enquanto a gravação acontece. Na tela Configuração de Legendas de um evento, o mesmo formulário está na aba "Criar novo bloco" da janela "Adicionar bloco", com os botões "Cancelar" e "Criar e adicionar". Chega-se a essa aba diretamente ou pelo atalho 'Adicionar bloco "{termo}"', que aparece na aba "Usar bloco existente" quando a busca não encontra nenhum bloco e que leva o termo buscado para o nome. 💻

O formulário tem o campo "Nome da legenda", marcado com asterisco e com a dica "Digite o nome da legenda", e o campo "Cor", também com asterisco, formado por um seletor de cor, pelo código da cor escolhida, em maiúsculas, e por uma paleta de dezesseis cores sugeridas: `#2196F3`, `#4CAF50`, `#FF9800`, `#F44336`, `#9C27B0`, `#00BCD4`, `#FFEB3B`, `#795548`, `#607D8B`, `#E91E63`, `#3F51B5`, `#009688`, `#8BC34A`, `#FF5722`, `#673AB7` e `#CDDC39`. A cor marcada na paleta leva um sinal de conferido. O formulário abre com o nome vazio e a primeira cor da paleta marcada. 💻

Quando o servidor recusa o cadastro, a janela continua aberta com o que foi digitado, para correção. A tela não avisa, antes de enviar, que o nome já existe. 💻

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | O botão "Salvar" — ou "Criar e adicionar" — fica desabilitado enquanto a gravação acontece; não há outro indicador |
| Erro de validação | "Este campo é obrigatório", abaixo de "Nome da legenda", quando o campo é deixado vazio. O campo não aceita digitação além de 100 caracteres |
| Erro de servidor | Erro "Erro Interno" com o texto enviado pelo servidor no detalhe: "O nome do bloco de legenda é obrigatório.", "A cor deve estar no formato #RRGGBB.", "Já existe um bloco de legenda com este nome." ou, em falha inesperada, "Ocorreu um erro inesperado. Contate o suporte.". A janela continua aberta. ⚠️ O resumo é "Erro Interno" mesmo quando o motivo é uma regra de negócio |
| Sucesso | No catálogo: mensagem "Bloco criado" com o detalhe "O bloco foi criado com sucesso.", fechamento da janela e recarga da lista a partir da primeira página. Na configuração do evento: a janela se fecha e o bloco aparece como último cartão, sem mensagem própria do cadastro |
| Empty state | Não se aplica — a janela é um formulário |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | O bloco cadastrado é encontrado pela pesquisa do catálogo e pode ser adicionado à configuração de qualquer evento | Regras 6 e 7 · cenário "Cadastrar um bloco pelo catálogo" |
| SC-02 | Não existem no catálogo dois blocos com o mesmo nome, ainda que escritos com maiúsculas e minúsculas diferentes | Regra 2 · cenário "Já existe bloco com o mesmo nome" |
| SC-03 | Todo bloco do catálogo tem nome e cor | Regra 1 · cenários "Nome da legenda vazio" e "Cor fora do formato" |
| SC-04 | O bloco cadastrado de dentro da configuração de um evento aparece nessa configuração sem que o usuário precise procurá-lo | Cenário "Cadastrar um bloco de dentro da configuração do evento" |

---

## Métricas de tamanho

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Cadastrar Bloco de Legenda | principal | EE | 1 | 4 | Baixa | 3 | 2026-10-04 |

### Memória de cálculo

**Cadastrar Bloco de Legenda** — EE · ALR 1 · DER 4 · Baixa · 3 PF

```json
{"pe": "Cadastrar Bloco de Legenda",
 "alr": ["Legenda"],
 "der": ["Nome da legenda", "Cor", "Mensagem", "Ação"],
 "nao_contados": "A paleta de cores sugeridas é lista de valores fixos. Criado de dentro da configuração de um evento, o bloco entra no evento pela gravação de Adicionar Bloco de Legenda ao Evento, contada lá."}
```

Por que cada ALR:
1. `Legenda` — grava o bloco no catálogo e confere que o nome não se repete

Classificação: EE — a intenção primária é manter o arquivo lógico Legenda, com as formas 1, 6, 7 e 12. O cadastro pela janela Novo bloco e o cadastro pela aba Criar novo bloco usam o mesmo formulário e a mesma lógica: é um processo só.

**Total: 3 PF**

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade Legenda

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Formulário do bloco: nome, cor e paleta | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/components/bloco-form/bloco-form.component.ts` (linhas 31–116) e `.html` (linhas 1–37) | — |
| Janela "Novo bloco" do catálogo e mensagens | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/pages/catalogo-legendas/catalogo-legendas.component.ts` (linhas 160–217) e `.html` (linhas 90–103) | — |
| Aba "Criar novo bloco" e atalho da busca | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/components/adicionar-bloco-dialog/adicionar-bloco-dialog.component.ts` (linhas 115–157) e `.html` (linhas 39–51 e 62–63) | — |
| Operação `POST /administracao/legendas` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/LegendaController.java` (linhas 97–100) | — |
| Validação do nome e da cor, unicidade e gravação | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/LegendaServiceImpl.java` (linhas 96–110 e 177–187) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada e em teste (ticket `PDTIC25148-34`); o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

No armazenamento, o nome do bloco comporta 255 caracteres; o limite de 100 é só da tela. A unicidade do nome é garantida também por restrição do banco. A composição de mesa saiu do bloco pela decisão registrada no código como "D5".

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-10-04 | Claude (apf-cpm) | Contagem | Primeira contagem, pelo `PROMPT_CONTAGEM`: 3 PF — Cadastrar Bloco de Legenda (EE Baixa, 3 PF). Confirmada em 2026-10-04 e espelhada em `global/CONTAGEM-PF.md` |
| 2026-10-04 | Claude (analise-impacto) | Origem atualizada | Elo com a AIM do ticket `PDTIC25148-34`, aberta na entrega: o ticket passa a ser a Origem da feature (Criação), com os critérios CA-02, CA-03 e CA-04 — o CA-03 fica só nesta feature; regras, campos e cenários inalterados |
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do código e do ticket `PDTIC25148-34` do Jira (critérios CA02, CA03 e CA04); a funcionalidade não consta no documento legado GPE006 – Gerenciar Regras de Legendas |

---

*Feature Set: Legendas · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
