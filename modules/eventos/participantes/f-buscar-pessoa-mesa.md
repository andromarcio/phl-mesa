<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: EVT-PAR-12
feature_set: EVT-PAR
dominio: EVT
entidade: CadeiraMesa
data_model_ref: data-models/eventos.md#cadeiramesa
endpoints: []
error_codes: []
depende_de: ["EVT-PAR-07"]
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

# Buscar Pessoa na Mesa
> **Nível 3** - Feature Set: Participantes — Major Feature Set: Eventos - `EVT-PAR-12`

## Descrição

Permite que o Administrador e a Secretaria Mesa busquem, pelo nome, uma pessoa que já está sentada no mapa do evento; a busca informa em que assento ela está e destaca esse assento no mapa.

No campo de busca que fica acima do mapa de assentos, digita-se parte do nome; os resultados aparecem enquanto se digita e, ao escolher uma pessoa, o assento dela é levado ao centro da tela e fica destacado por 5 segundos. No mapa da Secretaria Mesa também se pode digitar a identificação de um assento, como "B15".

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE005 – Gerenciar Participante v1.1, de 16/12/2025 (documento legado), funcionalidade "Buscar Pessoa na Mesa" ⚠️ sem chave na ferramenta de demandas | Criação | — Identificar uma pessoa no mapa de assentos: busca pelo nome do participante e, ao selecionar um item da lista retornada, destaque sobre ele dentro do mapa. A busca por codinome, por legenda e por identificação do assento, a duração do destaque e as diferenças entre as versões do mapa vêm do código 💻. Ticket do Jira relacionado pelo título, concluído e sem AIM aberta 🔍: `PDTIC25148-28` (Mapa de mesa - melhorias) |

---

<div class="dev-only">

## Superfície

**Ação em tela** — origem: Consultar Mapa de Assentos `EVT-PAR-07` (`/evento-pessoa/:id`, visão Mapa de Assentos, nas versões do Administrador e da Secretaria Mesa), campo de busca acima do desenho dos assentos; a busca é refeita a cada tecla digitada. No mapa da Secretaria Mesa, o clique na etiqueta do assento de um cartão da lista "Pessoas Disponíveis" dispara o mesmo destaque

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e as imagens "Consultar Mapa de Assentos — Perfil Administrador" e "Perfil Secretaria Mesa" de GPE005

---

</div>

## Regras de negócio

1. A busca alcança somente os participantes que têm assento no mapa aberto. Quem está entre as pessoas disponíveis sem assento não é encontrado por ela.
2. Encontra-se a pessoa por qualquer parte do nome ou do codinome, sem diferenciar maiúsculas de minúsculas. ⚠️ GPE005 fala só em "nome do participante" 📄; o codinome vem do código 💻.
3. A busca diferencia letras acentuadas: "jose" não encontra "José". 💻 ⚠️ A busca de pessoas disponíveis, no mesmo mapa, ignora os acentos (→ ver Consultar Mapa de Assentos `EVT-PAR-07`); as duas deveriam se comportar da mesma forma. 🔍
4. No mapa do Administrador em formato Retangular, a pessoa também é encontrada pelo nome da sua legenda — menos quando está nos setores F e H, em que só valem o nome e o codinome. 💻 ⚠️ No formato Retangular Invertido e no mapa da Secretaria Mesa a legenda não é critério; nenhuma fonte explica a diferença, que parece esquecimento. ❓
5. No mapa da Secretaria Mesa, o termo formado por uma letra de A a H seguida de um número é tratado como identificação de assento: a busca localiza quem ocupa aquele assento e já o destaca, sem esperar a escolha. 💻 ⚠️ No mapa do Administrador essa forma de busca não existe: o mesmo termo é procurado como parte de um nome.
6. Cada resultado informa a localização da pessoa: a área do mapa e a identificação do assento.
7. Escolhido um resultado, o assento da pessoa fica destacado no mapa por 5 segundos. 💻 GPE005 prevê o destaque sem dizer por quanto tempo 📄.
8. A busca nada grava e não muda o mapa.

---

## Cenários

```gherkin
Feature: Buscar pessoa na mesa

  Background:
    Given que o usuário está autenticado no GPE
    And está no mapa de assentos de um evento com participantes sentados

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Buscar pela parte do nome
    Given que "Maria Souza" ocupa o assento "B12" e "Mariana Reis" ocupa o assento "F8"
    When o usuário digita "mari" no campo "Buscar pessoa na mesa..."
    Then o sistema mostra "2 pessoa(s) encontrada(s)"
    And lista "Maria Souza" com a localização "Mesa Principal - Lateral Esquerda - B12"
    And lista "Mariana Reis" com a localização "Assentos Laterais F - F8"
    # 💻 no mapa do Administrador em formato retangular, a localização termina com " - " e o nome da legenda, quando a pessoa tem legenda

  Scenario: Destacar o assento da pessoa escolhida
    Given que a busca listou "Maria Souza" no assento "B12"
    When o usuário clica no resultado "Maria Souza"
    Then a tela rola até o assento "B12" ficar no centro
    And o assento "B12" fica com o contorno pulsando entre azul e laranja por 5 segundos

  Scenario: Buscar pela identificação do assento, no mapa da Secretaria Mesa
    Given que o usuário está no mapa da Secretaria Mesa e "Pedro Alves" ocupa o assento "B15"
    When o usuário digita "b15" no campo de busca
    Then o sistema mostra "1 pessoa(s) encontrada(s)" e lista "Pedro Alves" com a localização "Mesa Principal - Lateral Esquerda - B15"
    And o assento "B15" já fica destacado, sem que o usuário escolha o resultado

  Scenario: Localizar pelo cartão da pessoa, no mapa da Secretaria Mesa
    Given que o cartão de "Ada Mota", na lista "Pessoas Disponíveis", mostra a etiqueta "A4"
    When o usuário clica na etiqueta "A4"
    Then o assento "A4" fica destacado no mapa por 5 segundos
    # 💻 só na lista vertical, do computador; no carrossel do tablet a etiqueta não reage ao toque

  Scenario: Buscar pelo nome da legenda, no mapa do Administrador em formato retangular
    Given que três participantes com a legenda "Palestrantes" estão sentados no setor A
    When o usuário digita "palest" no campo "Buscar pessoa na mesa..."
    Then o sistema lista os três, cada um com a localização seguida de " - Palestrantes"

  Scenario: Limpar a busca
    Given que o campo de busca tem um termo digitado
    When o usuário aciona o botão "×" do campo
    Then o campo fica vazio, a lista de resultados some e o destaque é retirado

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há dado a validar
    When o usuário apaga o termo ou digita só espaços
    Then o sistema não mostra resultados nem mensagem; o campo aceita qualquer texto, sem tamanho mínimo

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Buscar pela identificação do assento, no mapa do Administrador
    Given que o usuário está no mapa do Administrador, com o formato "Retangular Invertido"
    And o campo de busca traz a orientação "Buscar pessoa na mesa ou cadeira (ex: A3, B15)..."
    When o usuário digita "B15"
    Then o sistema procura "b15" nos nomes e mostra "Nenhuma pessoa encontrada nos assentos"
    # ⚠️ a orientação do campo promete a busca por assento, que neste mapa não existe 💻

  Scenario: Buscar pelo nome da legenda fora do mapa do Administrador em formato retangular
    Given que o usuário está no mapa do Administrador com formato "Retangular Invertido", ou no mapa da Secretaria Mesa
    When o usuário digita o nome de uma legenda
    Then o sistema não encontra ninguém por esse critério
    # ⚠️ critério diferente em cada versão do mapa 💻

  Scenario: Nome com acento digitado sem acento
    Given que "José Lima" ocupa o assento "C3"
    When o usuário digita "jose"
    Then o sistema mostra "Nenhuma pessoa encontrada nos assentos"
    # ⚠️ 🔍 a busca de pessoas disponíveis, ao lado, encontraria "José" com o mesmo termo

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Buscar Pessoa na Mesa" na matriz do N2
    When o usuário abre a tela de participantes do evento
    Then a tela não traz o mapa de assentos, e o campo de busca não fica ao alcance dele
    # ⚠️ a tela só confere o perfil para escolher o que mostra; ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Nenhuma pessoa encontrada
    When o usuário digita um termo que não está no nome nem no codinome de ninguém sentado
    Then o sistema mostra "Nenhuma pessoa encontrada nos assentos"

  Scenario: Assento vazio na busca por identificação
    Given que o usuário está no mapa da Secretaria Mesa e o assento "B20" está vazio
    When o usuário digita "B20"
    Then o sistema mostra "Nenhuma pessoa encontrada nos assentos" e não destaca o assento

  Scenario: Pessoa sentada mas ainda não gravada
    Given que o Administrador acabou de atribuir um assento e o mapa ainda não foi gravado
    When ele busca a pessoa pelo nome
    Then o sistema a encontra no assento novo, porque a busca olha o mapa como está na tela
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| "Buscar pessoa na mesa..." no formato Retangular, ou "Buscar pessoa na mesa ou cadeira (ex: A3, B15)..." no formato Retangular Invertido (texto de orientação do campo, que não tem rótulo) | Pessoa | entrada do usuário | editável | texto | não | Aceita qualquer texto; a busca é refeita a cada tecla. ⚠️ GPE005 informa tamanho 255 📄; a tela não limita o tamanho 💻. ⚠️ A orientação do campo não corresponde ao que cada mapa faz: ver a tabela de critérios em Comportamento de tela |

---

## Colunas do resultado

| Coluna (Label PO) | Origem | Ordenação |
|---|---|---|
| "{n} pessoa(s) encontrada(s)" | derivado: quantidade de resultados | — |
| Nome da pessoa | Pessoa: Codinome; na falta dele, Nome | ordem fixa das áreas do mapa — setores A, B, C, D, G, E, F e H — e, em cada uma, a posição do assento; o usuário não reordena |
| Localização, no formato "{área} - {assento}" | CadeiraMesa: Identificação e setor | — |
| Legenda, acrescentada à localização como " - {legenda}" — só no mapa do Administrador em formato Retangular | Legenda: nome da legenda prioritária do participante | — |

*As áreas aparecem com estes nomes: "Mesa Principal - Cabeçalho" (setor A), "Mesa Principal - Lateral Esquerda" (setor B), "Mesa Principal - Lateral Direita" (setor C), "Mesa Principal - Rodapé" (setor D), "Seção G", "Seção E", "Assentos Laterais F" e "Seção H". 💻 Ao passar o cursor sobre um resultado, a dica mostra "Localizado em: {localização}".*

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| — | — | Nenhum campo é gravado: a feature só consulta |

---

## Dados lidos e gravados

| Entidade | Papel | Por que a feature a toca |
|---|---|---|
| EventoPessoa | lê | O assento de cada participante sentado, onde a busca procura (regra 1) |
| CadeiraMesa | lê | A identificação do assento, mostrada na localização e usada na busca por assento (regras 5 e 6) |
| Legenda | lê | O nome da legenda prioritária, critério de busca e parte da localização no mapa do Administrador em formato Retangular (regra 4) |

---

## Comportamento de tela

### Onde fica
No mapa de assentos, acima do desenho, em um quadro próprio: o campo de busca, o botão "×" com a dica "Limpar busca" — que aparece quando há texto digitado — e, abaixo, a lista de resultados. Cada resultado mostra o nome em destaque e a localização em letra menor, e é clicável. 💻

A busca não consulta o servidor: procura entre os participantes que estão nos assentos do mapa já carregado na tela, e por isso é imediata e reflete inclusive as atribuições ainda não gravadas. 💻 Os resultados não são refeitos quando a atualização automática redesenha o mapa: valem até a próxima tecla. 🔍

Ao escolher um resultado, a tela rola suavemente até o assento ficar no centro, o assento cresce por meio segundo e o contorno pulsa entre azul e laranja; depois de 5 segundos o destaque some sozinho. 💻

Os critérios não são os mesmos nas quatro variações do mapa: 💻 ⚠️

| Versão e formato do mapa | Orientação do campo | Nome e codinome | Legenda | Identificação do assento |
|---|---|---|---|---|
| Administrador, Retangular | "Buscar pessoa na mesa..." | Sim | Sim, menos nos setores F e H | Não |
| Administrador, Retangular Invertido | "Buscar pessoa na mesa ou cadeira (ex: A3, B15)..." | Sim | Não | Não, embora a orientação prometa ⚠️ |
| Secretaria Mesa, Retangular | "Buscar pessoa na mesa..." | Sim | Não | Sim, embora a orientação não diga ⚠️ |
| Secretaria Mesa, Retangular Invertido | "Buscar pessoa na mesa ou cadeira (ex: A3, B15)..." | Sim | Não | Sim |

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Sem indicador: o resultado é imediato |
| Erro de validação | Não se aplica — o campo aceita qualquer texto; vazio ou só com espaços, a lista de resultados some |
| Erro de servidor | Não se aplica — a busca não consulta o servidor |
| Sucesso | "{n} pessoa(s) encontrada(s)" e uma linha por pessoa, com o nome e a localização; ao clicar, o assento é destacado por 5 segundos |
| Empty state | "Nenhuma pessoa encontrada nos assentos" |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Toda pessoa sentada cujo nome ou codinome contém o termo digitado aparece no resultado, com a área e a identificação do assento em que está | Regras 1, 2 e 6 · cenário "Buscar pela parte do nome" |
| SC-02 | Escolhido um resultado, o assento correspondente fica visível e destacado no mapa por 5 segundos | Regra 7 · cenário "Destacar o assento da pessoa escolhida" |
| SC-03 | No mapa da Secretaria Mesa, informada a identificação de um assento ocupado, o ocupante é localizado e destacado sem outra ação | Regra 5 · cenário "Buscar pela identificação do assento, no mapa da Secretaria Mesa" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Buscar Pessoa na Mesa | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade CadeiraMesa

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Busca e destaque, mapa do Administrador em formato retangular (nome, codinome e legenda) | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/components/mesa/components/retangular/retangular.component.ts` (linhas 1244–1410) e `.html` (linhas 49–78); estilo do destaque em `retangular.component.css` (linhas 944–966) | — |
| Busca, mapa do Administrador em formato invertido (nome e codinome) | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/components/mesa/components/retangular-invertido/retangular-invertido.component.ts` (linhas 1244–1397) e `.html` (linha 51) | — |
| Busca por nome ou por assento, mapa da Secretaria Mesa em formato retangular | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/components/mesa-recepcionista-checkin/components/retangular/retangular-recepcionista-checkin.component.ts` (linhas 946–1150) e `.html` (linhas 60, 132–155) | — |
| Busca por nome ou por assento, mapa da Secretaria Mesa em formato invertido | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/components/mesa-recepcionista-checkin/components/retangular-invertido/retangular-invertido-recepcionista-checkin.component.ts` (linhas 1274–1475) e `.html` (linhas 52, 123–146) | — |
| Operação do servidor | sistema_mesa_checkin_backend | — não há: a busca é feita no navegador, sobre os dados trazidos por Consultar Mapa de Assentos `EVT-PAR-07` | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

A busca por assento é reconhecida pela expressão `^[A-H]\d+$`, sem diferenciar maiúsculas, aplicada ao termo sem os espaços das pontas. A busca por nome compara em minúsculas, sem retirar acentos e sem aparar o termo.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE005 – Gerenciar Participante (funcionalidade "Buscar Pessoa na Mesa") e do código |

---

*Feature Set: Participantes · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
