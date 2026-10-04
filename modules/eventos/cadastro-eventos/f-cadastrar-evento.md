<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: EVT-CAD-02
feature_set: EVT-CAD
dominio: EVT
entidade: Evento
data_model_ref: data-models/eventos.md#evento
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
  pendente: true
  revisada_em: ""
  revisada_ate: ""
---

# Cadastrar Evento
> **Nível 3** - Feature Set: Cadastro de Eventos — Major Feature Set: Eventos - `EVT-CAD-02`

## Descrição

Permite que o Administrador cadastre um evento com nome, data e hora, local, tipo de evento, tipo de mesa e quantidade prevista de participantes; o evento passa a constar na pesquisa de eventos, já com os assentos do mapa gerados conforme o tipo de mesa.

O cadastro é aberto pelo botão Adicionar da tela Eventos. O Administrador preenche os campos, pode informar o Código da Campanha do CRM e anexar uma imagem, e aciona Salvar; o sistema volta à lista de eventos.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE004 – Manter Evento v1.1, de 16/12/2025 (documento legado), funcionalidade "Incluir Evento" ⚠️ sem chave na ferramenta de demandas | Criação | — Incluir um evento a partir de nome, local, data e quantidade de participantes, e compor a mesa com assentos de identificador fixo — regra "Composição da mesa", alterada na v1.1 do documento (ticket citado nele como DTIC25148-32). O campo Código da Campanha não está no documento: vem do ticket do Jira `PDTIC25148-36`, em teste, critério CA01; AIM ainda não aberta 💻 |

---

<div class="dev-only">

## Superfície

**Tela própria** — rota `/eventos/detail`

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Incluir / Editar Evento" de GPE004

---

</div>

## Regras de negócio

1. Nome do Evento, Data e Hora, Local, Tipo de Evento, Tipo de Mesa e Participantes são necessários para incluir o evento. ⚠️ A conferência é feita só na interface: o servidor aceita o evento sem conferir nenhum dado 💻.
2. O nome do evento tem de 3 a 100 caracteres. 💻 ⚠️ GPE004 informa tamanho 255 e não cita mínimo 📄.
3. O local tem de 3 a 200 caracteres. 💻 ⚠️ GPE004 informa tamanho 255 e não cita mínimo 📄.
4. A quantidade de participantes é um número inteiro de 1 a 10.000. 💻 GPE004 só diz que é um número inteiro 📄.
5. A data do evento pode ser qualquer uma, inclusive uma data que já passou. 💻
6. Dois eventos podem ter o mesmo nome: não há verificação de duplicidade. 💻
7. O Código da Campanha é opcional e tem até 50 caracteres; é ele que habilita a importação dos inscritos do CRM para o evento. 💻
8. A imagem do evento é opcional, e o evento guarda uma só. 💻 ⚠️ GPE004 fala em "anexar arquivos", no plural e sem restringir a imagem 📄.
9. O evento nasce sem ser o principal. 💻
10. O evento nasce com os assentos do mapa, em quantidade fixa por tipo de mesa. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 5
11. Cada assento é identificado pela letra do setor seguida de um número sequencial que começa em 1, e o identificador é único dentro do evento.
12. A composição da mesa depende do tipo de mesa escolhido: 💻
    - **Retangular** — A1 a A5, B1 a B35, C1 a C35, D1 a D5, E1 a E23, F1 a F32, G1 a G10 e H1 a H36, num total de 181 assentos.
    - **Retangular Invertido** — A1 a A5, B1 a B34, C1 a C34, D1 a D5, E1 a E30, F1 a F28, G1 a G10 e H1 a H28, num total de 174 assentos.
13. ⚠️ As faixas que GPE004 lista em "Composição da mesa" — A1 a A5, B1 a B34, C1 a C34, D1 a D5, E1 a E30, F1 a F28, G1 a G10 e H1 a H28 📄 — são, no código, as do tipo Retangular Invertido 💻; e o documento só conhece o tipo de mesa "Retangular", que no código tem outra composição. Confirmar com o PO qual composição vale para cada tipo.
14. Os setores A, B, C e D compõem a mesa principal; os setores E, F, G e H, as laterais. 💻
15. A quantidade informada em Participantes não altera o número de assentos gerados. 💻 ⚠️ O código traz, desativado, o cálculo que usaria essa quantidade — indício de que a intenção já foi outra.

---

## Cenários

```gherkin
Feature: Cadastrar evento

  Background:
    Given que o usuário está autenticado no GPE
    And abriu a tela "Novo Evento" pelo botão "Adicionar" da tela Eventos

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Cadastrar evento com mesa Retangular
    When o usuário preenche "Nome do Evento" com "Reunião de Diretoria", "Data e Hora" com "20/10/2026 09:00", "Local" com "Sede da CNI" e "Participantes" com "80"
    And escolhe "Reunião" em "Tipo de Evento" e "Retangular" em "Tipo de Mesa"
    And aciona "Salvar"
    Then o sistema grava o evento e gera os 181 assentos do tipo Retangular
    And exibe: "Sucesso" com o detalhe "Evento criado com sucesso"
    And volta à tela Eventos, onde o evento aparece na lista com "Não" na coluna "Principal"
    # 💻 a mensagem de sucesso fica na tela até ser fechada pelo usuário

  Scenario: Cadastrar evento com mesa Retangular Invertido
    When o usuário preenche os campos obrigatórios e escolhe "Retangular Invertido" em "Tipo de Mesa"
    And aciona "Salvar"
    Then o sistema grava o evento e gera os 174 assentos do tipo Retangular Invertido
    # ⚠️ GPE004 não conhece este tipo de mesa; as faixas que o documento lista são as deste tipo — ver a regra 13

  Scenario: Informar o Código da Campanha
    When o usuário preenche os campos obrigatórios e "Código da Campanha" com "CMP-03460-L2K8"
    And aciona "Salvar"
    Then o sistema grava o evento com o código
    And a importação de inscritos do CRM fica habilitada para o evento

  Scenario: Anexar a imagem do evento
    When o usuário adiciona uma imagem em "Arquivo"
    Then o sistema exibe: "Anexo adicionado"
    And mostra a imagem como um botão com o nome do arquivo, ao lado de uma lixeira

  Scenario: Retirar a imagem antes de salvar
    Given que o usuário adicionou uma imagem em "Arquivo"
    When aciona a lixeira ao lado do nome do arquivo
    Then o sistema exibe: "Anexo removido"
    And o evento será gravado sem imagem

  Scenario: Desistir do cadastro
    When o usuário aciona "Cancelar"
    Then o sistema volta à tela Eventos sem gravar nada

  # ── Erros de validação ─────────────────────────────────────────

  # ← MESSAGE-DICTIONARY: BASELINE
  Scenario: Campo obrigatório vazio
    When o usuário passa pelo campo "Nome do Evento" e o deixa vazio
    Then o sistema exibe abaixo do campo: "Este campo é obrigatório"
    And o botão "Salvar" fica desabilitado
    # o mesmo vale para "Data e Hora", "Local", "Tipo de Evento", "Tipo de Mesa" e "Participantes"

  # ← MESSAGE-DICTIONARY: BASELINE
  Scenario: Nome ou local com menos de 3 caracteres
    When o usuário preenche "Nome do Evento" com "AB"
    Then o sistema exibe abaixo do campo: "Mínimo de 3 caracteres"
    And o botão "Salvar" fica desabilitado
    # o mesmo vale para "Local"

  Scenario: Texto acima do limite
    When o usuário digita em "Nome do Evento" mais de 100 caracteres
    Then o campo deixa de aceitar caracteres ao chegar a 100, e o contador mostra "100/100"
    # 💻 "Local" para em 200 e "Código da Campanha" em 50; a mensagem "Máximo de {n} caracteres" existe no código, mas o próprio campo impede o excesso 🔍

  Scenario: Participantes fora da faixa
    When o usuário informa "0" ou "10001" em "Participantes"
    Then o campo ajusta o valor para dentro da faixa de 1 a 10.000
    # 🔍 as mensagens "Valor mínimo é 1" e "Valor máximo é 10000" existem no código; o ajuste automático do campo não foi observado em execução

  Scenario: Arquivo que não é imagem
    When o usuário adiciona em "Arquivo" um arquivo que não é imagem
    Then o sistema recusa o arquivo e exibe "<nome do arquivo>: Tipo de arquivo não permitido" com o detalhe "Tipos permitidos: image/*"

  Scenario: Imagem acima do tamanho máximo
    When o usuário adiciona em "Arquivo" uma imagem com mais de 200 MB
    Then o sistema recusa a imagem e exibe "O arquivo selecionado excede o tamanho máximo permitido" com o detalhe "O tamanho máximo de arquivo permitido é <limite>"

  Scenario: Imagem que não pôde ser lida
    Given que o navegador não consegue ler a imagem escolhida
    When o usuário a adiciona em "Arquivo"
    Then o sistema exibe: "Falha ao ler o arquivo."

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Evento com o mesmo nome de outro
    Given que já existe o evento "Reunião de Diretoria"
    When o usuário cadastra outro evento com o nome "Reunião de Diretoria"
    Then o sistema grava o novo evento normalmente
    # 💻 não há verificação de duplicidade

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Cadastrar Evento" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Eventos › Cadastro, e o cadastro não fica ao alcance dele
    # ⚠️ a tela "Novo Evento" não confere o perfil e abre para quem digita o endereço dela; quem recusa a gravação é o servidor — ver a nota da matriz no N2
    # ❓ o que a tela mostra quando o servidor recusa depende da resposta do serviço corporativo de acesso, que o código não revela

  Scenario: Botão Adicionar conforme o perfil
    Given que o usuário chegou à tela Eventos com um perfil diferente de Administrador
    When a tela é exibida
    Then o botão "Adicionar" não aparece
    # ⚠️ 💻 o botão aparece também para um perfil "Gestor", inexistente no cadastro corporativo; e o botão "Criar Primeiro Evento", da lista vazia, aparece para qualquer perfil

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Falha ao salvar
    Given que a gravação do evento falha no servidor
    When o usuário aciona "Salvar"
    Then o sistema permanece na tela "Novo Evento", com os dados digitados
    And exibe: "Erro" com o detalhe "Erro ao salvar evento. Verifique os dados e tente novamente."
    # ⚠️ 🔍 a imagem, o evento e os assentos são gravados em etapas independentes: a falha numa etapa não desfaz as anteriores, e o evento pode ficar gravado sem assentos 💻

  Scenario: Tipos de evento ou de mesa não carregam
    Given que a lista de tipos de evento ou de tipos de mesa não pôde ser carregada
    When a tela "Novo Evento" é aberta
    Then o campo correspondente fica sem opções, sem nenhum aviso
    And o evento não pode ser salvo, porque o campo é obrigatório
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| Nome do Evento | Evento | entrada do usuário | editável | texto | sim | De 3 a 100 caracteres, com contador ao lado do campo 💻. ⚠️ GPE004 informa tamanho 255 📄 |
| Data e Hora | Evento | entrada do usuário | editável | data e hora | sim | Dia, mês, ano e hora no formato de 24 horas. Aceita qualquer data, inclusive passada 💻 |
| Local | Evento | entrada do usuário | editável | texto | sim | De 3 a 200 caracteres, com contador ao lado do campo 💻. ⚠️ GPE004 informa tamanho 255 📄 |
| Tipo de Evento | TipoEvento | entrada do usuário | editável | seleção → TipoEvento | sim | Uma opção. Tipos existentes: Reunião, Comitê e Seminário |
| Tipo de Mesa | TipoMesa | entrada do usuário | editável | seleção → TipoMesa | sim | Uma opção. Tipos existentes: Retangular e Retangular Invertido 💻 ⚠️ GPE004 só lista Retangular 📄. Define os assentos gerados (regra 12) |
| Participantes | Evento | entrada do usuário | editável | número | sim | Inteiro de 1 a 10.000 💻. Não interfere nos assentos (regra 15) |
| Código da Campanha | Evento | entrada do usuário | editável | texto | não | Até 50 caracteres 💻. Não consta em GPE004: vem do ticket `PDTIC25148-36` |
| Arquivo | Arquivo | entrada do usuário | editável | arquivo | não | Uma imagem, de qualquer formato de imagem, com até 200 MB 💻. ⚠️ GPE004 fala em "anexar arquivos" 📄 |

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| Principal | Não — o evento nasce sem ser o principal 💻 | Ao salvar |
| Excluído | Não | Ao salvar |
| Identificação e Composição de cada assento | Letra do setor mais número sequencial, e Principal ou Lateral conforme o setor (regras 11 a 14) | Logo depois de o evento ser gravado |

*O evento não guarda data de inclusão nem quem o incluiu 💻.*

---

## Dados lidos e gravados

| Entidade | Papel | Por que a feature a toca |
|---|---|---|
| CadeiraMesa | grava | Recebe os assentos gerados para o evento, conforme o tipo de mesa (regras 10 a 15) |

---

## Comportamento de tela

### Onde fica
Na tela "Novo Evento", aberta pelo botão "Adicionar" da tela Eventos — e pelo botão "Criar Primeiro Evento", quando a lista de eventos está vazia. Os campos vêm na ordem da tabela de Campos, com asterisco nos obrigatórios; o rodapé traz o texto "Campos com * são obrigatórios" e os botões "Cancelar" e "Salvar". O botão "Salvar" fica desabilitado enquanto houver campo obrigatório vazio ou inválido.

Cada campo traz um texto de orientação: "Digite o nome do evento", "Selecione a data e hora", "Local do evento", "Selecione o tipo" (nos tipos de evento e de mesa), "Número de participantes" e "Ex.: CMP-03460-L2K8". Sob o Código da Campanha fica a ajuda "Código da campanha no CRM usado para importar os inscritos."; sob o Arquivo, "Imagem relacionada". O calendário da Data e Hora oferece os atalhos "Hoje" e "Limpar". O campo Arquivo tem o botão "Adicionar" e a área "Clique em adicionar ou arraste e solte os arquivos aqui..."; a imagem adicionada aparece como um botão com o nome do arquivo (dica "Download"), ao lado de uma lixeira (dica "Excluir").

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Botão "Salvar" em estado de carregamento enquanto a gravação não responde, e também enquanto a imagem é lida |
| Erro de validação | Mensagem em vermelho abaixo do campo, depois que o usuário passa por ele: "Este campo é obrigatório", "Mínimo de 3 caracteres". O botão "Salvar" fica desabilitado. O código traz ainda o aviso "Formulário inválido" com o detalhe "Preencha todos os campos obrigatórios corretamente", para a tentativa de salvar com erro — a que não se chega pelo botão, já que ele fica desabilitado 🔍 |
| Erro de servidor | "Erro" com o detalhe "Erro ao salvar evento. Verifique os dados e tente novamente."; a tela permanece aberta com os dados digitados |
| Sucesso | "Sucesso" com o detalhe "Evento criado com sucesso", que fica visível até ser fechada, e retorno à tela Eventos |
| Empty state | Não se aplica — a tela abre com os campos em branco |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | O evento salvo aparece na pesquisa de eventos logo em seguida, com os dados informados | Cenário "Cadastrar evento com mesa Retangular" |
| SC-02 | Todo evento incluído tem, desde o primeiro momento, o conjunto completo de assentos do seu tipo de mesa: 181 no Retangular e 174 no Retangular Invertido | Regras 10 e 12 |
| SC-03 | Nenhum evento é gravado pela tela sem Nome do Evento, Data e Hora, Local, Tipo de Evento, Tipo de Mesa e Participantes válidos | Regra 1 · cenário "Campo obrigatório vazio" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Cadastrar Evento | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade Evento

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Tela "Novo Evento": campos, validação, imagem e gravação | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento/pages/evento/create/evento-create.component.ts` (linhas 113–145 e 172–268) e `.html` (linhas 1–285) | — |
| Mensagens de validação dos campos | sistema_mesa_checkin_frontend | `src/app/shared/cadastro-helper.ts` (linhas 9–23) | — |
| Operação `POST /administracao/eventos` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoController.java` (linhas 92–96) | — |
| Gravação do evento e da imagem | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/EventoServiceImpl.java` (linhas 166–178) | — |
| Geração dos assentos por tipo de mesa | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/CadeiraMesaServiceImpl.java` (linhas 40–50 e 88–210) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

Os assentos são gerados pelo indicador do tipo de mesa que a tela envia junto com o evento, e não pelo que está guardado no servidor: uma chamada que mande só o identificador do tipo de mesa grava o evento sem assentos 🔍.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE004 – Manter Evento (funcionalidade "Incluir Evento" e regra "Composição da mesa"), do código e do ticket `PDTIC25148-36` (campo Código da Campanha) |

---

*Feature Set: Cadastro de Eventos · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
