<!-- docqui: 4.0.2 | prompt: PROMPT_CONTAGEM | atualizado: 2026-10-04 -->
---
id: EVT-PAR-01
feature_set: EVT-PAR
dominio: EVT
entidade: EventoPessoa
data_model_ref: data-models/eventos.md#eventopessoa
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
  revisada_ate: "PDTIC25148-35"
---

# Pesquisar Participantes
> **Nível 3** - Feature Set: Participantes — Major Feature Set: Eventos - `EVT-PAR-01`

## Descrição

Permite que a equipe do evento pesquise os participantes por nome, organização, cargo, legenda, tema, grupo de trabalho ou situação de convite, confirmação e check-in; o resultado mostra, para cada pessoa, a legenda, a situação no evento e o assento.

A pesquisa fica na tela de participantes, aberta pela opção Participantes de cada evento na pesquisa de eventos. Informam-se os critérios desejados, como o texto da busca, as legendas e a situação de check-in, e aciona-se Pesquisar; o texto da busca pesquisa sozinho, enquanto é digitado.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE005 – Gerenciar Participante v1.1, de 16/12/2025 (documento legado), funcionalidade "Pesquisar Participantes" ⚠️ sem chave na ferramenta de demandas | Criação | — Pesquisar as pessoas de um evento por um ou mais critérios e ver, no resultado, se foram convidadas, se confirmaram, se fizeram check-in e qual é o assento. No Jira, a pesquisa de participantes é o ticket `PDTIC25148-20`, um dos que a v1.1 do documento cita. O critério Legendas, a coluna Legenda e a faixa de cor da lista vêm do código 💻 |
| [`PDTIC25148-35`](../../../analise-impacto/AIM-PDTIC25148-35.md) | Alteração | `CA-02, CA-03` — o nome do participante como atalho que abre o cadastro da pessoa em nova aba, e o critério "Somente pessoas sem foto". ⚠️ O ticket fala em pessoas confirmadas sem foto; o código não exige a confirmação 💻 |
<!-- trace-verified: PDTIC25148-35 @ 8882df4a0634 -->

---

<div class="dev-only">

## Superfície

**Tela própria** — rota `/evento-pessoa/:id`, na visão Participantes

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Pesquisar Participantes" de GPE005 (`GPE005-01.png`)

---

</div>

## Regras de negócio

1. A pesquisa alcança somente os participantes do evento aberto.
2. Os critérios informados se somam: só aparece o participante que atende a todos eles. 💻
3. O texto da busca é procurado no nome, no codinome, na razão social, no nome fantasia e no cargo da pessoa, sem diferenciar maiúsculas de minúsculas nem letras acentuadas; quando há mais de uma palavra, todas precisam aparecer, cada uma em qualquer desses dados. 💻 ⚠️ GPE005 diz que a busca "permite informar parte do nome" e, na descrição da funcionalidade, cita nome, organização e cargo 📄; o codinome e a exigência de todas as palavras só estão no código.
4. Em Legendas, Temas, Grupos de Trabalho e Cargo, quando mais de um valor é escolhido, basta o participante atender a um deles. 💻
5. Temas, grupos de trabalho e cargos são comparados por trecho: o valor escolhido traz também quem tem um valor mais longo que o contenha. 💻 ⚠️ Escolher o cargo "Diretor" traz também "Diretor Executivo"; parece efeito não pretendido.
6. A pesquisa por legenda considera todas as legendas que o participante tem no evento — a manual e as recebidas por regra —, e não só a que aparece para ele. 💻 ⚠️ O resultado pode trazer participante cuja legenda exibida é outra.
7. A legenda que acompanha cada participante no resultado é a prioritária. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 9
8. Convidado, Confirmado e Check-In são situações independentes, e cada uma pode restringir a pesquisa a quem está em Sim ou a quem está em Não. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 4
9. Em Convidado e em Confirmado, a opção Não traz apenas quem está marcado como não; em Check-In, a opção Não traz também o participante que nunca teve o check-in marcado nem desmarcado. 💻 ⚠️ As três situações não recebem o mesmo tratamento: o participante sem informação de convite ou de confirmação só é encontrado com Todos.
10. A restrição por foto traz apenas os participantes cuja pessoa não tem foto. 💻 ⚠️ O ticket `PDTIC25148-35` fala em "pessoas confirmadas no evento que não possuem foto"; o código não exige a confirmação — para isso é preciso combinar com Confirmado igual a Sim.
11. As opções de Temas, de Grupos de Trabalho e de Cargo reúnem, sem repetição e em ordem alfabética, os valores de todas as pessoas cadastradas no sistema. 💻 ⚠️ GPE005 pede apenas os valores "vinculados aos participantes do respectivo evento" 📄.
12. As opções de Legendas são todas as do catálogo, em ordem alfabética, estejam ou não na configuração do evento. 💻
13. A Secretaria Check-In pesquisa somente os participantes do evento principal. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 2

---

## Cenários

```gherkin
Feature: Pesquisar participantes

  Background:
    Given que o usuário está autenticado no GPE
    And abriu os participantes de um evento

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Abrir a lista de participantes do evento
    Given que o evento tem 35 participantes
    When a tela de participantes é aberta
    Then o sistema lista os 10 primeiros participantes, em ordem alfabética de nome
    And mostra "Total: 35" e o indicador "[1 a 10 de 35]"
    And cada linha traz a cor e o nome da legenda, a organização, o cargo, a situação de convite, de confirmação e de check-in e o assento

  Scenario: Pesquisar pelo texto da busca
    Given que "José Antônio Araújo", de cargo "Diretor", é participante do evento
    When o usuário digita "jose araujo" em "Busca"
    Then o sistema refaz a pesquisa a cada caractere digitado
    And o resultado traz "José Antônio Araújo"

  Scenario: Pesquisar combinando critérios
    When o usuário escolhe "Sim" em "Confirmado" e "Não" em "Check-In"
    And aciona "Pesquisar"
    Then o sistema lista somente os participantes confirmados que ainda não fizeram check-in
    And volta à primeira página do resultado

  Scenario: Pesquisar por legenda
    When o usuário escolhe "Anfitrião" e "Palestrantes" em "Legendas" e aciona "Pesquisar"
    Then o sistema lista os participantes que têm pelo menos uma dessas legendas no evento
    # ⚠️ entram também os participantes cuja legenda exibida é outra, quando uma das escolhidas está entre as que ele recebeu 💻

  Scenario: Pesquisar somente pessoas sem foto
    When o usuário marca "Somente pessoas sem foto" e aciona "Pesquisar"
    Then o sistema lista somente os participantes cuja pessoa não tem foto cadastrada

  Scenario: Limpar a pesquisa
    Given que há critérios preenchidos
    When o usuário aciona "Limpar"
    Then os critérios voltam ao padrão, com "Todos" em "Convidado", "Confirmado" e "Check-In"
    And o sistema lista de novo todos os participantes do evento

  Scenario: Abrir o cadastro da pessoa pelo nome
    When o usuário aciona o nome de um participante na lista
    Then o cadastro da pessoa abre em nova aba
    And a lista de participantes continua aberta, como estava

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há dado a validar
    When o usuário pesquisa com qualquer combinação de critérios, inclusive nenhum
    Then o sistema executa a pesquisa, pois todos os critérios são opcionais

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Não há conflito com dados existentes
    When o usuário pesquisa
    Then o sistema apenas consulta os participantes, sem alterar nenhum dado

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Pesquisar Participantes" na matriz do N2
    When o usuário entra no sistema
    Then a tela de participantes abre direto no mapa de assentos, sem os botões "Participantes" e "Mapa de Assentos"
    And a lista de participantes não fica ao alcance dele
    # ⚠️ a tela decide pelo nome do perfil e não há conferência no endereço da tela; ver a nota da matriz no N2

  Scenario: Recepção pesquisa com menos critérios
    Given que o usuário é da Secretaria Check-In
    When a tela de participantes é aberta
    Then os critérios "Temas", "Grupos de Trabalho" e "Cargo" não são exibidos
    And os demais critérios e a lista funcionam da mesma forma
    # ⚠️ GPE005 só registra, para esse perfil, a restrição ao evento principal; a retirada dos três critérios vem do código 💻

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Nenhum participante atende à pesquisa
    When o usuário pesquisa por um texto que nenhum participante do evento tem
    Then o sistema exibe: "Nenhum participante encontrado."
    And mostra "Total: 0"

  Scenario: Participante sem legenda e sem assento
    Given que um participante não tem legenda nem assento
    When ele aparece no resultado
    Then a faixa de cor da linha fica cinza-clara e a coluna "Legenda" fica vazia
    And a coluna "Assento" mostra "Sem assento"

  Scenario: Situação de convite não informada
    Given que um participante não tem a informação de convite
    When ele aparece no resultado
    Then a coluna "Convidado" mostra o ícone de interrogação, com a dica "Pendente"
    # ⚠️ esse participante só é encontrado com "Todos" em "Convidado": nem "Sim" nem "Não" o trazem 💻
    # ❓ não se sabe em que situação real um participante fica sem a informação de convite

  Scenario: Alteração feita por outro usuário
    Given que outro usuário registra o check-in de um participante exibido na lista
    When o usuário permanece na lista sem pesquisar de novo
    Then a linha continua mostrando a situação anterior
    # ⚠️ a lista não se atualiza sozinha; só a consulta que alimenta o mapa de assentos é repetida a cada 3 segundos 💻

  Scenario: Falha na pesquisa
    Given que a pesquisa falha no servidor
    When o usuário pesquisa
    Then a lista permanece como estava, sem nenhuma mensagem
    # ⚠️ a falha não é informada a quem usa a tela 💻
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| Nome do evento (sem rótulo na tela) | Evento | exibido do cadastro | somente leitura | texto | — | Título do cabeçalho da tela |
| "Tipo:" | TipoEvento | exibido do cadastro | somente leitura | texto | — | Nome do tipo do evento |
| Local do evento (sem rótulo na tela) | Evento | exibido do cadastro | somente leitura | texto | — | — |
| Data e hora do evento (sem rótulo na tela) | Evento | exibido do cadastro | somente leitura | data e hora | — | Formato dd/mm/aaaa hh:mm |
| "Busca" | Pessoa | entrada do usuário | editável | texto | não | Texto de apoio "Buscar por nome, codinome, organização ou cargo". Sem limite de tamanho 💻 ⚠️ GPE005 informa 255 📄 |
| "Legendas" | Legenda | entrada do usuário | editável | seleção → Legenda | não | Seleção múltipla; texto de apoio "Selecione legendas". 💻 Não consta em GPE005 |
| "Temas" | TemaPessoa | entrada do usuário | editável | seleção → TemaPessoa | não | Seleção múltipla; texto de apoio "Selecione temas". Não é exibido para a Secretaria Check-In 💻 |
| "Grupos de Trabalho" | GrupoTrabalhoPessoa | entrada do usuário | editável | seleção → GrupoTrabalhoPessoa | não | Seleção múltipla; texto de apoio "Selecione". Não é exibido para a Secretaria Check-In 💻 |
| "Cargo" | Pessoa | entrada do usuário | editável | seleção → Pessoa | não | Seleção múltipla entre os cargos já cadastrados; texto de apoio "Selecione". Não é exibido para a Secretaria Check-In 💻 |
| "Convidado" | dado de código | entrada do usuário | editável | lista de opções | não | "Todos", "Sim" ou "Não"; vem em "Todos" |
| "Confirmado" | dado de código | entrada do usuário | editável | lista de opções | não | "Todos", "Sim" ou "Não"; vem em "Todos" |
| "Check-In" | dado de código | entrada do usuário | editável | lista de opções | não | "Todos", "Sim" ou "Não"; vem em "Todos" |
| "Foto" | Pessoa | entrada do usuário | editável | sim·não | não | Caixa de marcar "Somente pessoas sem foto"; vem desmarcada. 💻 Não consta em GPE005 |

*Nos critérios de seleção múltipla, com mais de dois valores escolhidos o campo passa a mostrar a contagem — "{0} legendas selecionadas", "{0} temas selecionados", "{0} grupos de trabalho selecionados" e "{0} cargo selecionados" ⚠️ (o último com erro de concordância).*

---

## Colunas do resultado

| Coluna (Label PO) | Origem | Ordenação |
|---|---|---|
| Faixa de cor (sem título) | Legenda — a cor da legenda prioritária do participante; cinza-claro quando ele não tem legenda 💻 | — |
| "Nome" | Pessoa — nome completo | padrão ↑ |
| "Organização" | Pessoa — o nome fantasia e, na falta dele, a razão social 💻 ⚠️ | — |
| "Cargo" | Pessoa — cargo | — |
| "Legenda" | Legenda — o nome da legenda prioritária do participante 💻 | — |
| "Convidado" | EventoPessoa — Sim, Não ou Pendente | — |
| "Confirmado" | EventoPessoa — confirmado ou não | — |
| "Check-In" | EventoPessoa — check-in feito ou não | — |
| "Assento" | CadeiraMesa — a identificação do assento, ou "Sem assento" | — |

⚠️ **Organização**: o servidor entrega a razão social e o nome fantasia em posições trocadas, e a tela mostra "a razão social e, na falta, o nome fantasia" — o resultado, para quem lê, é o inverso: aparece o nome fantasia e, só quando ele não existe, a razão social 💻. O código registra a troca como comportamento a preservar; confirmar com o PO qual dos dois deve aparecer. Na exportação, os dois saem nas colunas certas.

⚠️ **Colunas**: GPE005 lista Nome, Organização, Cargo, Convidado, Confirmado, Check-In e Assento 📄; a coluna "Legenda" e a faixa de cor só existem no código 💻.

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| — | — | Nenhum campo é gravado: a feature só consulta |

---

## Dados lidos e gravados

| Entidade | Papel | Por que a feature a toca |
|---|---|---|
| EventoPessoa | lê | É o participante: dele vêm a situação de convite, de confirmação e de check-in, que são colunas do resultado e critérios da pesquisa |
| CadeiraMesa | lê | Identificação do assento do participante, na coluna "Assento" |
| EventoPessoaLegenda | lê | Legendas que o participante tem no evento: sustentam o critério Legendas (regra 6) e a escolha da legenda prioritária (regra 7) |
| EventoLegenda | lê | Posição de cada legenda na configuração do evento, que decide a prioritária quando não há legenda manual (regra 7) |

---

## Comportamento de tela

### Onde fica
Na tela de participantes do evento, que abre em nova aba pela opção "Participantes" de cada evento na pesquisa de eventos (Pesquisar Eventos, `EVT-CAD-01`). A Secretaria Check-In não passa pela pesquisa de eventos: ao entrar no sistema é levada direto a esta tela, no evento principal 💻.

O alto da tela traz um cartão com os dados do evento — o nome, "Tipo:" seguido do tipo, o local e a data e hora —, o botão "Cadastrar Pessoa" (Cadastrar Participante, `EVT-PAR-02`) e, para o Administrador, os botões "Participantes" e "Mapa de Assentos", que alternam entre a lista e o mapa. ⚠️ Na imagem "Pesquisar Participantes" de GPE005 o botão se chama "Cadastrar Participante" 📄; na tela é "Cadastrar Pessoa" 💻.

Abaixo vem o cartão dos critérios, com os botões "Pesquisar" e "Limpar". O campo "Busca" pesquisa sozinho a cada caractere digitado, levando junto os demais critérios que estiverem preenchidos 💻; mudar os outros critérios só tem efeito depois de "Pesquisar". "Limpar" devolve todos os critérios ao padrão e refaz a pesquisa. Os critérios não ficam guardados: ao sair da tela e voltar, estão em branco 💻.

Por último vem a lista, com o título "Lista de Participantes" e, à direita, "Total: " seguido da quantidade encontrada. São 10 participantes por página, em ordem alfabética de nome, com o indicador no formato "[1 a 10 de 35]" e a paginação embaixo; os títulos das colunas não reordenam a lista 💻. O nome do participante é um atalho que abre o cadastro da pessoa em nova aba, com a dica "Abrir o perfil da pessoa em nova aba" 💻. Em "Convidado", um ícone mostra a situação, com as dicas "Sim", "Não" e "Pendente". As colunas "Confirmado", "Check-In" e "Assento" são o ponto de partida de outras features — Alterar Confirmação de Presença (`EVT-PAR-13`), Registrar Check-in (`EVT-PAR-03`) e Consultar Legenda do Participante (`EVT-PAR-04`) —, e no rodapé da lista fica o botão "Download" (Exportar Participantes, `EVT-PAR-14`).

⚠️ A lista não se atualiza sozinha. Depois de aberta, a tela repete a cada 3 segundos a consulta dos participantes usados pelo mapa de assentos — menos para a Secretaria Check-In —, mas a lista paginada só é refeita ao pesquisar, ao limpar ou ao mudar de página 💻.

⚠️ Ao alternar para o mapa de assentos e voltar, os critérios reaparecem em branco, mas a lista volta restrita pela última pesquisa feita 🔍 — conclusão tirada da leitura do código, sem execução.

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Ao abrir, uma camada cobre a tela com "Carregando dados do evento..." e os itens "Carregando evento" e "Carregando participantes", cada um marcado quando termina; a cada pesquisa, a lista mostra o seu indicador de carregamento |
| Erro de validação | Não se aplica — todos os critérios são opcionais e aceitam qualquer valor |
| Erro de servidor | ⚠️ Nenhuma mensagem: se a pesquisa falha, a lista fica como estava. Se o evento não puder ser carregado, o cartão do evento fica vazio e os critérios e a lista não aparecem 💻 |
| Sucesso | Lista preenchida, com "Total: " e a quantidade encontrada |
| Empty state | "Nenhum participante encontrado.", sem a linha de títulos das colunas |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Todo participante do evento que atende a todos os critérios informados aparece no resultado, e nenhum participante de outro evento aparece | Regras 1 e 2 · cenário "Pesquisar combinando critérios" |
| SC-02 | A busca encontra a pessoa mesmo quando o texto é digitado sem acento e em minúsculas | Regra 3 · cenário "Pesquisar pelo texto da busca" |
| SC-03 | Uma pesquisa sem resultado informa "Nenhum participante encontrado." e total zero | Cenário "Nenhum participante atende à pesquisa" |
| SC-04 | A legenda mostrada em cada linha é a mesma que identifica o participante no mapa de assentos | Regra 7 |

---

## Métricas de tamanho

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Pesquisar Participantes | principal | CE | 3 | 19 | Média | 4 | 2026-10-04 |
| Consultar Legendas (combo) | acessório | CE | 1 | 2 | Baixa | 3 | 2026-10-04 |
| Consultar Temas (combo) | acessório | CE | 1 | 2 | Baixa | 3 | 2026-10-04 |
| Consultar Grupos de Trabalho (combo) | acessório | CE | 1 | 2 | Baixa | 3 | 2026-10-04 |
| Consultar Cargo (combo) | acessório | CE | 1 | 2 | Baixa | 3 | 2026-10-04 |

### Memória de cálculo

**Pesquisar Participantes** — CE · ALR 3 · DER 19 · Média · 4 PF

```json
{"pe": "Pesquisar Participantes",
 "alr": ["Evento", "Pessoa", "Legenda"],
 "der": ["Nome do evento", "Tipo", "Local do evento", "Data e hora do evento", "Busca", "Legendas", "Temas", "Grupos de Trabalho", "Cargo", "Convidado", "Confirmado", "Check-In", "Foto", "Faixa de cor", "Nome", "Organização", "Assento", "Mensagem", "Ação"],
 "nao_contados": "Cargo, Legenda, Convidado, Confirmado e Check-In aparecem no filtro e na coluna e contam uma vez. Total e o indicador de páginas são informação de posicionamento (Guia STI 5.5). TipoEvento é dado de código e não é arquivo referenciado. O perfil do usuário, que decide o que a tela mostra, é controle de acesso."}
```

Por que cada ALR:
1. `Evento` — lê os dados do evento mostrados no cabeçalho, os participantes com a situação de convite, confirmação e check-in, o assento, as legendas de cada participante e a ordem dos blocos, que decide a legenda prioritária
2. `Pessoa` — lê o nome, a organização, o cargo, a foto, os temas e os grupos de trabalho
3. `Legenda` — lê o nome e a cor da legenda prioritária

Classificação: CE — a intenção primária é apresentar, com as formas 3 (situação sem valor vira Pendente), 4, 5 (escolhe a legenda prioritária e a organização), 7, 8, 11 e 13. Não há cálculo nem dado derivado.

**Consultar Legendas (combo)** — CE · ALR 1 · DER 2 · Baixa · 3 PF

```json
{"pe": "Consultar Legendas (combo)",
 "alr": ["Legenda"],
 "der": ["Legenda", "Ação"],
 "nao_contados": "A lista consultada não conta Mensagem."}
```

Por que cada ALR:
1. `Legenda` — lê todas as legendas do catálogo, em ordem alfabética

Classificação: CE — lista consultada (SIZING, Regra da lista consultada), com as formas 7, 8, 11 e 13.

**Consultar Temas (combo)** — CE · ALR 1 · DER 2 · Baixa · 3 PF

```json
{"pe": "Consultar Temas (combo)",
 "alr": ["Pessoa"],
 "der": ["Tema", "Ação"],
 "nao_contados": "A lista consultada não conta Mensagem."}
```

Por que cada ALR:
1. `Pessoa` — lê os temas de todas as pessoas cadastradas, sem repetição

Classificação: CE — lista consultada, com as formas 4, 7, 8, 11 e 13. Tirar as repetições não é cálculo nem dado derivado (Guia STI 3.3.2).

**Consultar Grupos de Trabalho (combo)** — CE · ALR 1 · DER 2 · Baixa · 3 PF

```json
{"pe": "Consultar Grupos de Trabalho (combo)",
 "alr": ["Pessoa"],
 "der": ["Grupo de Trabalho", "Ação"],
 "nao_contados": "A lista consultada não conta Mensagem."}
```

Por que cada ALR:
1. `Pessoa` — lê os grupos de trabalho de todas as pessoas cadastradas, sem repetição

Classificação: CE — lista consultada, com as formas 4, 7, 8, 11 e 13.

**Consultar Cargo (combo)** — CE · ALR 1 · DER 2 · Baixa · 3 PF

```json
{"pe": "Consultar Cargo (combo)",
 "alr": ["Pessoa"],
 "der": ["Cargo", "Ação"],
 "nao_contados": "A lista consultada não conta Mensagem."}
```

Por que cada ALR:
1. `Pessoa` — lê os cargos de todas as pessoas cadastradas, sem repetição

Classificação: CE — lista consultada, com as formas 4, 7, 8, 11 e 13.

**Total: 16 PF**

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade EventoPessoa

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Tela de participantes: cabeçalho do evento, alternância lista e mapa, atualização a cada 3 segundos | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/evento-pessoa.component.ts` (linhas 51–140 e 189–206) e `.html` (linhas 26–124) | — |
| Critérios da pesquisa | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/components/evento-pessoas-filter/evento-pessoas-filter.component.ts` (linhas 39–141) e `.html` (linhas 10–254) | — |
| Lista de participantes | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/components/evento-pessoas-list/evento-pessoas-list.component.ts` (linhas 54–124 e 478–502) e `.html` (linhas 9–92 e 183–190) | — |
| Operações `GET /administracao/evento-pessoas`, `/grupos-trabalho`, `/temas` e `/cargos` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoPessoaController.java` (linhas 53–81) | — |
| Consulta dos participantes e escolha da legenda prioritária | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/repository/impl/EventoPessoaRepositoryImpl.java` (linhas 44–68 e 92–342) | — |
| Ordem dos dados entregues à lista (razão social e nome fantasia trocados) | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/dto/EventoPessoaListDTO.java` (linhas 30–56) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

O servidor não exige o evento na consulta: sem ele, a pesquisa alcança os participantes de todos os eventos. A tela sempre o envia.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-10-04 | Claude (apf-cpm) | Contagem | Primeira contagem, pelo `PROMPT_CONTAGEM`: 16 PF — Pesquisar Participantes (CE Média, 4 PF); Consultar Legendas (combo) (CE Baixa, 3 PF); Consultar Temas (combo) (CE Baixa, 3 PF); Consultar Grupos de Trabalho (combo) (CE Baixa, 3 PF); Consultar Cargo (combo) (CE Baixa, 3 PF). Confirmada em 2026-10-04 e espelhada em `global/CONTAGEM-PF.md` |
| 2026-10-04 | Claude (analise-impacto) | Origem atualizada | Elo com a AIM do ticket `PDTIC25148-35`, aberta na entrega: o ticket ganha linha própria na Origem, como Alteração, com os critérios CA-02 e CA-03; regras, campos e cenários inalterados |
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE005 – Gerenciar Participante (funcionalidade "Pesquisar Participantes"), do código e do ticket `PDTIC25148-35` do Jira |

---

*Feature Set: Participantes · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
