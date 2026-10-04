<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: EVT-PAR-07
feature_set: EVT-PAR
dominio: EVT
entidade: CadeiraMesa
data_model_ref: data-models/eventos.md#cadeiramesa
endpoints: []
error_codes: []
depende_de: ["EVT-CAD-02"]
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

# Consultar Mapa de Assentos
> **Nível 3** - Feature Set: Participantes — Major Feature Set: Eventos - `EVT-PAR-07`

## Descrição

Permite que o Administrador e a Secretaria Mesa consultem o mapa de assentos de um evento, vendo cada assento com a sua identificação e o participante que o ocupa, ao lado da lista de pessoas disponíveis.

O Administrador chega ao mapa pela opção "Mapa de Assentos" da tela de participantes do evento; a Secretaria Mesa já entra nele ao se autenticar, no evento principal. O mapa é montado conforme o formato de mesa do evento e se atualiza sozinho enquanto está aberto.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE005 – Gerenciar Participante v1.1, de 16/12/2025 (documento legado), funcionalidade "Consultar Mapa de Assentos" ⚠️ sem chave na ferramenta de demandas | Criação | — Apresentar o mapa com todos os assentos enumerados conforme o formato definido para o evento, o participante de cada um e a lista de pessoas disponíveis, nas versões do Administrador e da Secretaria Mesa. Os setores e as faixas de numeração vêm de GPE004 – Manter Evento v1.1, regra "Composição da mesa". As cores, o quadro de legendas, a atualização automática e o segundo formato de mesa vêm do código 💻. Tickets do Jira relacionados pelo título, todos concluídos e sem AIM aberta 🔍: `PDTIC25148-16` (Mapa de mesa), `PDTIC25148-28` (Mapa de mesa - melhorias) e `PDTIC25148-32` (Ajustes na Mesa - Exibir a cabeceira no topo) |

---

<div class="dev-only">

## Superfície

**Tela própria** — rota `/evento-pessoa/:id`, visão Mapa de Assentos, em **duas** versões conforme o perfil:

- Administrador — visão alternada com a lista de participantes, pelo botão "Mapa de Assentos"
- Secretaria Mesa — a tela já abre no mapa, em versão só de consulta

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e as imagens "Consultar Mapa de Assentos — Perfil Administrador" e "Perfil Secretaria Mesa" de GPE005

---

</div>

## Regras de negócio

1. O mapa mostra todos os assentos do evento, cada um com a sua identificação — a letra do setor seguida de um número — e, quando ocupado, com o participante que o ocupa.
2. Os assentos se dividem em oito setores, de A a H. Os setores A, B, C e D formam a mesa principal; os setores E, F, G e H, os assentos laterais. 💻 GPE004 lista os oito setores sem distinguir a mesa principal dos assentos laterais 📄.
3. A quantidade de assentos de cada setor é fixa e depende do formato de mesa do evento. No formato Retangular são 181 assentos: A1 a A5, B1 a B35, C1 a C35, D1 a D5, E1 a E23, F1 a F32, G1 a G10 e H1 a H36. No formato Retangular Invertido são 174: A1 a A5, B1 a B34, C1 a C34, D1 a D5, E1 a E30, F1 a F28, G1 a G10 e H1 a H28. 💻 ⚠️ GPE004 traz uma única composição — A1 a A5, B1 a B34, C1 a C34, D1 a D5, E1 a E30, F1 a F28, G1 a G10 e H1 a H28 —, que no código é a do Retangular Invertido; as faixas do formato Retangular não constam no documento, que também só cita o tipo de mesa Retangular 📄.
4. Os assentos são os gerados na inclusão do evento, e o desenho do mapa segue o formato de mesa que o evento tem no momento da consulta. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 5 ⚠️ Se o formato de mesa foi trocado depois da inclusão, o desenho e os assentos deixam de coincidir. 💻
5. Fazem parte do mapa — em um assento ou entre as pessoas disponíveis — somente os participantes com presença confirmada ou com check-in feito. O convidado que não confirmou nem chegou fica fora do mapa. 💻
6. No mapa do Administrador, pessoas disponíveis são os participantes do mapa que ainda não têm assento. Elas vêm em ordem de legenda — da legenda de menor número para a de maior, e por último quem não tem legenda —, depois pelo maior número de participações anteriores e, por fim, pelo nome. 💻
7. No mapa da Secretaria Mesa, pessoas disponíveis são os participantes com check-in feito e ainda não atendidos, tenham ou não assento, em ordem de chegada: do check-in mais antigo para o mais recente. ⚠️ A ordem de chegada depende da data e hora do check-in, que pode ser apagada quando o mapa é gravado (→ ver Atribuir Assento ao Participante `EVT-PAR-08`) e não é registrada no cadastro feito na recepção com check-in automático; nesses casos a pessoa perde a posição que tinha na fila. 🔍
8. Cada participante é identificado no mapa pela cor da sua legenda prioritária; quem não tem legenda recebe uma cor neutra. 💻 → ver [N1 Eventos](../README.md): Regras transversais de negócio: 9
9. O mapa distingue o assento de quem já fez check-in, o assento de quem ainda não fez e o assento vazio. 💻
10. O mapa aberto se atualiza sozinho quando muda, por ação feita em outro ponto do sistema, o check-in, a confirmação, o assento ou o número de participações de algum participante, e quando alguém entra no mapa ou sai dele. 💻 ⚠️ Uma mudança só de legenda, de atendimento ou de dados cadastrais da pessoa não é percebida: só aparece junto com a próxima mudança percebida, ou quando o mapa é reaberto. 🔍

---

## Cenários

```gherkin
Feature: Consultar mapa de assentos

  Background:
    Given que o usuário está autenticado no GPE
    And o evento tem os assentos gerados na sua inclusão

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Administrador abre o mapa de um evento de mesa retangular
    Given que o evento tem formato de mesa "Retangular" e participantes confirmados, alguns já com assento
    When o Administrador aciona "Mapa de Assentos" na tela de participantes do evento
    Then o sistema desenha os 181 assentos dos setores A a H, com a mesa principal ao centro
    And cada assento ocupado mostra o nome e a organização do participante, na cor da legenda dele
    And cada assento vazio mostra a sua identificação, como "B12"
    And a lista "Pessoas Disponíveis" traz os participantes confirmados ou com check-in que ainda não têm assento

  Scenario: Mapa de um evento de mesa retangular invertida
    Given que o evento tem formato de mesa "Retangular Invertido"
    When o usuário abre o mapa de assentos
    Then o sistema desenha os 174 assentos desse formato, com o setor E à esquerda da mesa principal e os setores F, G e H à direita

  Scenario: Secretaria Mesa entra direto no mapa do evento principal
    Given que o usuário tem o perfil Secretaria Mesa
    When ele se autentica
    Then o sistema abre a tela do evento principal já no mapa de assentos, em versão só de consulta
    And a lista "Pessoas Disponíveis" traz quem fez check-in e ainda não foi atendido, em ordem de chegada, com foto, organização e o assento ou "Não alocado"
    And o cabeçalho mostra "Atualização automática ativa" e "Última verificação: há alguns instantes"

  Scenario: Mapa acompanha a mudança feita por outro usuário
    Given que o mapa está aberto
    When a recepção registra o check-in de um participante que já tem assento
    Then em poucos segundos o assento dele passa a aparecer preenchido com a cor da legenda, sem que o usuário recarregue a tela
    And na versão da Secretaria Mesa o participante entra na lista "Pessoas Disponíveis"

  Scenario: Secretaria Mesa pede a atualização na hora
    Given que o usuário tem o perfil Secretaria Mesa e está no mapa
    When ele aciona "Atualizar agora"
    Then o sistema consulta os participantes de imediato e refaz o mapa se algo mudou

  Scenario: Filtrar a lista de pessoas disponíveis
    When o usuário digita "silva" em "Buscar pessoa..."
    Then a lista "Pessoas Disponíveis" passa a mostrar só quem tem "silva" no nome, no codinome, no cargo, na razão social, no nome fantasia ou na legenda, sem diferenciar maiúsculas nem acentos
    And o número no título "Pessoas Disponíveis (n)" continua contando todas as pessoas disponíveis
    # 💻 o filtro age enquanto se digita; não há botão de busca

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há dado a validar
    When o usuário abre o mapa de assentos
    Then o sistema monta o mapa sem solicitar nenhum dado; o único campo, "Buscar pessoa...", é opcional e aceita qualquer texto

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Formato de mesa trocado depois da inclusão do evento
    Given que o evento foi incluído com o formato "Retangular" e depois editado para "Retangular Invertido"
    When o usuário abre o mapa de assentos
    Then o sistema desenha o mapa do formato atual, mas com os assentos gerados para o formato antigo
    And as posições do desenho que não têm assento correspondente aparecem sem dica, e o participante colocado nelas não é gravado
    And os assentos que o formato atual não desenha ficam fora da tela, com quem estiver neles
    # ⚠️ 🔍 inferido da leitura do código, não executado: a edição do evento não refaz os assentos 💻
    # ⚠️ 🔍 no mapa do Administrador em formato invertido, um participante que esteja em assento de H29 a H36 pode interromper a montagem do mapa

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Consultar Mapa de Assentos" na matriz do N2
    When o usuário abre a tela de participantes do evento
    Then a tela não traz os botões "Participantes" e "Mapa de Assentos", e o mapa não fica ao alcance dele
    # ⚠️ a tela só confere o perfil para escolher o que mostra; ver a nota da matriz no N2

  Scenario: Secretaria Mesa não altera o mapa
    Given que o usuário tem o perfil Secretaria Mesa
    When ele abre o mapa de assentos
    Then os assentos não aceitam arraste nem clique e não têm o botão "×"
    And a tela não traz o painel "Gerenciar Pessoas Alocadas na Mesa" nem a seção "Exportações"

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Evento sem participante confirmado nem com check-in
    Given que nenhum participante do evento confirmou presença nem fez check-in
    When o usuário abre o mapa de assentos
    Then o sistema desenha todos os assentos vazios
    And o título da lista mostra "Pessoas Disponíveis (0)"

  Scenario: Falha ao carregar os assentos
    Given que a consulta dos assentos do evento falha
    When o usuário abre o mapa de assentos
    Then a tela permanece com o indicador "Carregando dados da mesa...", sem mensagem de erro
    # ⚠️ 💻 a falha fica registrada só para diagnóstico técnico; o usuário não é avisado nem tem como tentar de novo sem recarregar a página

  Scenario: Falha na atualização automática
    Given que o mapa está aberto
    When uma das consultas periódicas falha
    Then o sistema mantém o mapa como estava e tenta de novo na consulta seguinte, sem avisar o usuário

  Scenario: Falha ao carregar as legendas do evento
    Given que a consulta da configuração de legendas do evento falha
    When o usuário abre o mapa de assentos
    Then o quadro "Legenda das Categorias" traz só as legendas presentes entre os participantes e a linha "Assento livre"

  Scenario: Formato de mesa não reconhecido
    Given que o formato de mesa do evento não é "Retangular" nem "Retangular Invertido"
    When o usuário abre o mapa de assentos
    Then a tela não desenha nenhum mapa e não exibe aviso
    # 💻 hoje só existem esses dois formatos
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| Nome do evento (sem rótulo, no cabeçalho) | Evento | exibido do cadastro | somente leitura | texto | — | — |
| "Tipo:" | TipoEvento | exibido do cadastro | somente leitura | texto | — | — |
| Local do evento (sem rótulo, ao lado do ícone de localização) | Evento | exibido do cadastro | somente leitura | texto | — | — |
| Data e hora do evento (sem rótulo, ao lado do ícone de calendário) | Evento | exibido do cadastro | somente leitura | data e hora | — | Formato dia/mês/ano hora:minuto |
| "Buscar pessoa..." (texto de orientação do campo, que não tem rótulo) | Pessoa | entrada do usuário | editável | texto | não | Filtra a lista de pessoas disponíveis enquanto se digita, por nome, codinome, cargo, razão social, nome fantasia ou legenda, sem diferenciar maiúsculas nem acentos. ⚠️ GPE005 descreve a busca por "parte do nome" e tamanho 255 📄; a tela busca em mais dados e não limita o tamanho 💻 |
| "Pessoas Disponíveis (n)" | derivado ↓ | calculado | somente leitura | número | — | — |
| "Legenda das Categorias" — "{nome da legenda} (n)" | derivado ↓ | calculado | somente leitura | número | — | Uma linha por legenda; legenda sem nome aparece como "Sem descrição" 💻 |
| "Legenda das Categorias" — "Assento livre (n)" | derivado ↓ | calculado | somente leitura | número | — | — |

*A busca por legenda no campo "Buscar pessoa..." parece ser a "permissão para consulta por legenda durante a alocação de participantes" registrada no histórico da versão 1.1 de GPE005 🔍.*

---

## Derivações

| Campo derivado | Fórmula (Label PO) | Campos-fonte (Entidade) |
|---|---|---|
| Pessoas Disponíveis (n) | No mapa do Administrador: quantidade de participantes do mapa sem Assento. No mapa da Secretaria Mesa: quantidade de participantes com Check-In e sem Atendido | Assento (EventoPessoa), Check-In (EventoPessoa), Atendido (EventoPessoa) |
| {nome da legenda} (n) | Quantidade de participantes com Assento cuja legenda prioritária é aquela | Assento (EventoPessoa), Legenda (EventoPessoaLegenda), Nome da legenda (Legenda) |
| Assento livre (n) | Quantidade de assentos do evento menos a quantidade de participantes com Assento, nunca menor que zero | Identificação (CadeiraMesa), Assento (EventoPessoa) |

---

## Colunas do resultado

| Coluna (Label PO) | Origem | Ordenação |
|---|---|---|
| Assento vazio — identificação, como "B12" | CadeiraMesa: Identificação | posição fixa no desenho do formato de mesa |
| Assento ocupado — nome do participante | Pessoa: Codinome; na falta dele, Nome | — |
| Assento ocupado — organização | Pessoa: Nome Fantasia; na falta dele, Razão Social | — |
| Assento ocupado — "(n)" participações anteriores, só no setor E | HistoricoPessoa: soma das Participações de todos os anos | — |
| Assento ocupado — cor de fundo ou de contorno | Legenda prioritária do participante (cor) e Check-In do participante | — |
| Pessoa disponível, Administrador — nome | Pessoa: Codinome; na falta dele, Nome | legenda, depois participações anteriores (da maior para a menor), depois nome; o usuário não reordena |
| Pessoa disponível, Administrador — "(n)" participações anteriores | HistoricoPessoa: soma das Participações de todos os anos | — |
| Pessoa disponível, Administrador — cargo | Pessoa: Cargo | — |
| Pessoa disponível, Administrador — organização | Pessoa: Nome Fantasia; na falta dele, Razão Social | — |
| Pessoa disponível, Administrador — etiqueta com o nome da legenda, na cor dela | Legenda prioritária do participante ⚠️ a etiqueta só aparece quando a legenda está na configuração de legendas do evento; a legenda manual fora da configuração não é mostrada no cartão, embora pinte o assento 💻 | — |
| Pessoa disponível, Administrador — etiqueta "Check in realizado" ou "Check in não identificado" | EventoPessoa: Check-In | — |
| Pessoa disponível, Secretaria Mesa — foto | Arquivo: miniatura da foto da pessoa; sem foto, um ícone de pessoa | — |
| Pessoa disponível, Secretaria Mesa — nome | Pessoa: Codinome; na falta dele, Nome | ordem de chegada: check-in mais antigo primeiro; o usuário não reordena |
| Pessoa disponível, Secretaria Mesa — organização | Pessoa: Nome Fantasia; na falta dele, Razão Social | — |
| Pessoa disponível, Secretaria Mesa — etiqueta com a identificação do assento ou "Não alocado" | EventoPessoa: Assento | — |

*O cartão da Secretaria Mesa traz ainda o botão de atendimento → ver Registrar Atendimento `EVT-PAR-10`. ⚠️ GPE005 descreve o cartão do participante como "Nome Completo (qtd de participações histórica) / Legenda / Cargo / Organização / Informação de check-in" 📄, o que corresponde ao cartão do Administrador; o cartão da Secretaria Mesa, com foto e assento, só aparece na tabela de permissões do documento.*

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| — | — | Nenhum campo é gravado: a feature só consulta |

---

## Dados lidos e gravados

| Entidade | Papel | Por que a feature a toca |
|---|---|---|
| CadeiraMesa | lê | Os assentos do evento, com identificação e composição (regras 1 a 4) |
| EventoPessoa | lê | Os participantes do mapa, com confirmação, check-in, atendimento e assento (regras 5 a 7) |
| TipoMesa | lê | O formato de mesa do evento decide o desenho do mapa (regras 3 e 4) |
| Legenda | lê | Nome e cor da legenda prioritária de cada participante (regra 8) |
| EventoLegenda | lê | Os blocos de legenda configurados no evento, na ordem, para o quadro "Legenda das Categorias" |
| EventoPessoaLegenda | lê | As legendas de cada participante, de onde sai a prioritária (regra 8) |
| HistoricoPessoa | lê | A soma das participações anteriores, mostrada ao lado do nome e usada na ordem das pessoas disponíveis (regra 6) |
| Arquivo | lê | A foto da pessoa, no cartão da Secretaria Mesa |

---

## Comportamento de tela

### Onde fica
Na tela de participantes do evento, que tem no alto um cabeçalho com o nome do evento, o tipo, o local e a data e hora. Para o Administrador, o cabeçalho traz os botões "Participantes" e "Mapa de Assentos", que alternam entre a lista e o mapa; a tela abre na lista. Para a Secretaria Mesa, não há alternância: a tela abre direto no mapa, e o cabeçalho mostra o indicador "Atualização automática ativa", o texto "Última verificação: {tempo}" e um botão de ícone com a dica "Atualizar agora". 💻

O mapa ocupa a tela em duas partes. À esquerda fica a lista "Pessoas Disponíveis (n)", com o campo "Buscar pessoa..." e um cartão por pessoa. À direita ficam o campo "Buscar pessoa na mesa..." (→ ver Buscar Pessoa na Mesa `EVT-PAR-12`) e o desenho dos assentos. Abaixo do mapa vem o quadro "Legenda das Categorias", com uma amostra de cor e o texto "{nome} (n)" para cada legenda — primeiro os blocos configurados no evento, na ordem; depois as legendas manuais que algum participante tenha e que não estejam na configuração; por fim "Assento livre" — e a explicação das situações de assento: "Check in realizado", "Check in não identificado" e "Vazio". 💻

A mesa principal é desenhada com o setor A no alto, em uma linha, na ordem A4, A2, A1, A3, A5; o setor B em coluna à esquerda; o setor C em coluna à direita; o setor D embaixo, na ordem D4, D2, D1, D3, D5; e o texto "Mesa Principal" no centro. O setor F é uma grade de quatro assentos por linha, o setor G uma coluna, o setor H outra grade de quatro por linha, e o setor E uma coluna. 💻

O assento ocupado por quem já fez check-in aparece preenchido com a cor da legenda, com o texto em branco; o de quem ainda não fez, com fundo branco e só o contorno na cor da legenda; o assento vazio, em branco com contorno cinza. O participante sem legenda usa um cinza muito claro. 💻

Ao passar o cursor sobre um assento vazio, a dica mostra "Cadeira {identificação}", "Setor: {nome do setor}" e "Clique para atribuir uma pessoa"; sobre um assento ocupado, mostra a identificação e o setor, "Pessoa: {nome completo}", "Cargo: {cargo}", "Instituição: {razão social}", "Participações anteriores: {n}" e "Status: {situação do check-in}". 💻 ⚠️ Os nomes de setor das dicas são fixos no código e não vêm de cadastro nenhum: A1 é "Anfitrião"; A2 a A5, "Palestrantes"; nos setores B e C, os assentos 1 a 5 são "Presidência", 6 a 15 "Deputados Federais", 16 a 25 "Senadores" e os demais "Convidados Especiais"; D é "Governadores"; E, "Imprensa"; F, "Assessoria"; G, "Segurança"; H, "Técnicos". Parecem dados de um evento específico que ficaram embutidos no sistema — confirmar com o PO se devem existir. ⚠️ A situação do check-in aparece com três redações: "Check in não identificado" (lista, quadro de legendas e dicas dos setores A, B, C, D e F), "Check in não realizado" (dicas dos setores G, H e E) e "Check-in pendente" (arquivo exportado).

Enquanto o mapa está aberto, a tela consulta os participantes a cada 3 segundos e só refaz o mapa quando algo mudou (regra 10). 💻 O indicador da Secretaria Mesa mostra o tempo desde a última consulta: "há alguns instantes" até 30 segundos, "há {n} segundos" até 1 minuto, "há {n} minuto(s)" até 1 hora e, depois disso, a hora da consulta. ⚠️ O perfil Secretaria Check-In não tem atualização automática nem acesso ao mapa.

### O que muda conforme o perfil

| Aspecto | Administrador | Secretaria Mesa |
|---|---|---|
| Uso do mapa | Edição: atribuir, remover e liberar assentos | Só consulta: os assentos não reagem a arraste nem a clique |
| Quem aparece em "Pessoas Disponíveis" | Participantes do mapa sem assento | Participantes com check-in feito e ainda não atendidos, com ou sem assento |
| Cartão da pessoa | Nome, participações anteriores, cargo, organização, etiqueta da legenda e etiqueta do check-in | Foto, nome, organização, etiqueta do assento e botão de atendimento |
| Painel "Gerenciar Pessoas Alocadas na Mesa" | Presente, com "Salvar Alocações (n)", "Limpar Todas" e "Controles de Zoom"; oculto no tablet | Ausente |
| Seção "Exportações" | Presente | Ausente |
| Indicador de atualização automática | Não é mostrado, embora a atualização aconteça | Mostrado no cabeçalho |
| Tablet | O painel de controle some | A lista vira um carrossel horizontal, com três cartões visíveis, ou dois em telas mais estreitas |

⚠️ No mapa da Secretaria Mesa, a dica do assento vazio continua dizendo "Clique para atribuir uma pessoa", embora o assento não reaja a clique. 💻 ⚠️ O Administrador pode ajustar o tamanho do desenho entre 50% e 150%, de 10 em 10, pelos botões "Diminuir zoom", "Aumentar zoom" e "100%" ("Resetar zoom"); em telas de até 1.440 pontos de largura o desenho já abre reduzido. Na versão da Secretaria Mesa não há os botões de ajuste: no formato Retangular Invertido só existe a redução automática, e no formato Retangular o desenho aparece sempre no tamanho normal. 💻

### O que muda conforme o formato da mesa

| Aspecto | Retangular | Retangular Invertido |
|---|---|---|
| Disposição, da esquerda para a direita | Setores F, G e H empilhados, mesa principal, setor E | Setor E, mesa principal, setores F, G e H empilhados |
| Setores B e C | 35 assentos cada | 34 assentos cada |
| Setor E | 23 assentos | 30 assentos |
| Setor F | 32 assentos, em 8 linhas de 4 | 28 assentos, em 7 linhas de 4 |
| Setor H | 36 assentos, em 9 linhas de 4 | 28 assentos, em 7 linhas de 4 |
| Setores A, D e G | 5, 5 e 10 assentos | 5, 5 e 10 assentos |
| Total | 181 assentos | 174 assentos |

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Ao abrir a tela, "Carregando dados do evento...", com os itens "Carregando evento" e "Carregando participantes"; ao montar o mapa, "Carregando dados da mesa...", com a tela esmaecida |
| Erro de validação | Não se aplica — a consulta não tem campo obrigatório |
| Erro de servidor | Sem mensagem: se a consulta dos assentos falha, o indicador "Carregando dados da mesa..." permanece ⚠️; se falha a atualização automática, o mapa fica como estava |
| Sucesso | O mapa desenhado, a lista "Pessoas Disponíveis (n)" e o quadro "Legenda das Categorias" |
| Empty state | Sem participante confirmado ou com check-in: todos os assentos vazios e "Pessoas Disponíveis (0)". Sem pessoa que case com o filtro: a lista fica vazia, sem texto de aviso |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Todo assento gerado para o evento aparece no mapa com a sua identificação, e todo participante com assento aparece exatamente no assento que lhe foi atribuído | Regras 1 e 3 · cenário "Administrador abre o mapa de um evento de mesa retangular" |
| SC-02 | A lista de pessoas disponíveis da Secretaria Mesa traz somente quem fez check-in e ainda não foi atendido, em ordem de chegada | Regra 7 · cenário "Secretaria Mesa entra direto no mapa do evento principal" |
| SC-03 | Uma mudança de check-in ou de assento feita por outro usuário aparece no mapa aberto sem que a tela seja recarregada | Regra 10 · cenário "Mapa acompanha a mudança feita por outro usuário" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Consultar Mapa de Assentos | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade CadeiraMesa

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Tela que hospeda o mapa: perfil, alternância e atualização a cada 3 s | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/evento-pessoa.component.ts` (linhas 51–54, 105–140, 189–235) e `.html` (linhas 33–56, 75–94, 117–123) | — |
| Mapa do Administrador: setores, pessoas disponíveis, cores e dicas | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/components/mesa/components/retangular/retangular.component.ts` (linhas 31–39, 82–91, 242–427, 746–881) e `.html` (linhas 12–44, 119–445); formato invertido em `../retangular-invertido/retangular-invertido.component.ts` (linhas 31–39) | — |
| Mapa da Secretaria Mesa: pessoas disponíveis, foto e etiqueta do assento | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/components/mesa-recepcionista-checkin/components/retangular/retangular-recepcionista-checkin.component.ts` (linhas 419–454, 497–504, 1520–1535) e `../retangular-invertido/retangular-invertido-recepcionista-checkin.component.ts` (linhas 447–454, 2665–2734) | — |
| Cor da pessoa e quadro de legendas | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/services/legenda-mesa.helper.ts` (linhas 40–140) | — |
| Operações `GET /administracao/eventos/{id}/cadeiras` e `GET /administracao/evento-pessoas/mesa/participantes` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoController.java` (linhas 130–134), `controller/EventoPessoaController.java` (linhas 83–95) e `repository/impl/EventoPessoaRepositoryImpl.java` (linhas 502–593) | — |
| Geração dos assentos por formato de mesa | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/CadeiraMesaServiceImpl.java` (linhas 42–210) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

A consulta dos participantes do mapa recebe o parâmetro `isSecretariaCheckin`, que a tela preenche com a indicação de que o usuário é **Secretaria Mesa**; é ele que troca a ordem para a de chegada. O nome do parâmetro e o conteúdo não coincidem.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa dos documentos legados GPE005 – Gerenciar Participante (funcionalidade "Consultar Mapa de Assentos") e GPE004 – Manter Evento (regra "Composição da mesa") e do código |

---

*Feature Set: Participantes · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
