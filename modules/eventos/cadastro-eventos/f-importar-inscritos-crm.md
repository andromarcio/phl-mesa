<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: EVT-CAD-09
feature_set: EVT-CAD
dominio: EVT
entidade: EventoPessoa
data_model_ref: data-models/eventos.md#eventopessoa
endpoints: []
error_codes: []
depende_de: ["EVT-CAD-01", "EVT-CAD-02"]
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

# Importar Inscritos do CRM
> **Nível 3** - Feature Set: Cadastro de Eventos — Major Feature Set: Eventos - `EVT-CAD-09`

## Descrição

Permite que o Administrador importe do CRM os inscritos aprovados e confirmados da campanha de um evento, sem digitação; cada inscrito passa a constar no evento como convidado e confirmado, e a pessoa é incluída no cadastro de pessoas ou atualizada nele.

A importação fica na seção Inscritos do CRM da janela Cargas de Convidados e Confirmados, aberta pelo ícone de pasta em cada linha da lista de eventos. O evento precisa ter o Código da Campanha; o Administrador aciona Importar Inscritos do CRM e recebe o resumo do que foi importado.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| Código-fonte (engenharia reversa de 2026-09-30) — a funcionalidade não consta nos documentos legados ⚠️ | Criação | — Importar para o evento os inscritos da campanha registrada no CRM, a partir do Código da Campanha do evento, sem duplicar quem já está associado e atualizando os dados a cada nova importação. Corresponde ao ticket do Jira `PDTIC25148-36`, "CRM - Importação de convidados", em teste, critérios CA01 a CA10: esta feature realiza CA02 a CA10, e o CA01 — o campo Código da Campanha no evento — é realizado por Cadastrar Evento `EVT-CAD-02` e Editar Evento `EVT-CAD-03`; AIM ainda não aberta. ⚠️ O código diverge do ticket em CA04, CA05, CA07, CA08, CA09 e CA10 — ver o confronto abaixo |

Confronto dos critérios do ticket com o código:

- **CA01 — Código da Campanha no evento**: atendido fora desta feature, em Cadastrar Evento `EVT-CAD-02` e Editar Evento `EVT-CAD-03`.
- **CA02 — Utilizar o Código da Campanha na consulta**: atendido (regra 1).
- **CA03 — Impedir a importação sem campanha**: atendido — sem o código, a ação fica indisponível e a janela orienta o preenchimento (cenário "Evento sem Código da Campanha").
- **CA04 — Consultar os inscritos no CRM**: atendido com recorte ⚠️ — só vêm os inscritos aprovados e confirmados (regra 2); o resumo do ticket fala em "lista de inscritos", sem esse recorte.
- **CA05 — Importar os dados dos inscritos**: atendido ⚠️ — os dez dados são lidos (regra 4), mas Data de envio do formulário, Status da Inscrição e Status Aprovação ficam guardados sem aparecer em nenhum ponto do sistema (regra 12).
- **CA06 — Associar os inscritos ao evento**: atendido (regras 10 e 11).
- **CA07 — Evitar duplicidade**: atendido (regras 7 e 11) ⚠️ — o inscrito sem Cód. Contato é deixado de fora (regra 6), o que o ticket não prevê.
- **CA08 — Atualizar os dados em nova importação**: atendido (regras 9 e 11) ⚠️ — a atualização apaga Codinome, E-mail, Razão Social e Cargo da pessoa quando o CRM não os traz.
- **CA09 — Campanha sem inscritos**: diverge ⚠️ — o ticket pede informar que não foram encontrados registros; o sistema trata o caso como erro, sob o título "Erro ao importar inscritos do CRM". A lista de participantes não é alterada, como o critério pede.
- **CA10 — Isolar a importação por evento**: atendido quanto aos participantes ⚠️ — os dados da pessoa que a importação atualiza valem para todos os eventos (regra 14).

---

<div class="dev-only">

## Superfície

**Modal** — origem: Pesquisar Eventos `EVT-CAD-01` (`/eventos`), ícone de pasta "Cargas de Convidados e Confirmados" em cada linha da lista; seção "Inscritos do CRM" da janela

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada. A imagem "Carregar Convidados / Confirmados" de GPE004 é anterior a esta funcionalidade e não a mostra

---

</div>

## Regras de negócio

1. A importação exige que o evento tenha o Código da Campanha; é por ele que a campanha é localizada no CRM. 💻
2. São importados somente os inscritos da campanha que estão aprovados e com a inscrição confirmada no CRM. 💻 🔍 Os nomes das duas situações vêm da mensagem do sistema; no código, Status Aprovação e Status da Inscrição são comparados com o mesmo valor interno do CRM.
3. A integração com o CRM é só de leitura: a importação não altera nada no CRM. 💻
4. De cada inscrito vêm dez dados: `Data de envio do formulário`, `Status da Inscrição`, `Status Aprovação`, `Cód. Contato`, `Contato relacionado`, `Codinome`, `Nome`, `E-mail`, `Empresa` e `Cargo`. 💻
5. Quando o registro da inscrição não traz Nome, Codinome, E-mail ou Cargo, vale o dado correspondente do contato relacionado; a Empresa vem só do registro da inscrição. 💻
6. O inscrito sem Cód. Contato não é importado. 💻 ⚠️ O ticket não prevê esse caso.
7. Quando a campanha traz mais de um registro para o mesmo Cód. Contato, vale o de alteração mais recente no CRM. 💻
8. A pessoa é reconhecida pelo Cód. Contato. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 12
9. A pessoa que já existe no cadastro tem Codinome, E-mail, Razão Social e Cargo substituídos pelos do CRM, inclusive por valor em branco; o Nome só é substituído quando o CRM traz um nome. 💻 ⚠️ A Empresa do CRM é gravada na Razão Social da pessoa.
10. A pessoa que ainda não existe é incluída no cadastro com origem Carga; quando o CRM não traz o nome, o codinome faz as vezes dele, e o inscrito sem nome e sem codinome não é importado. 💻
11. O inscrito que ainda não participa do evento entra como convidado e confirmado, sem check-in e sem atendimento. O inscrito que já participa não é duplicado: passa a convidado e confirmado, e o check-in, a data do check-in, o atendimento e o assento dele são preservados. 💻
12. A participação guarda os dados da inscrição no CRM — `Data de envio do formulário`, `Status da Inscrição`, `Status Aprovação` e as identificações da inscrição e do contato —, renovados a cada importação. 💻 ⚠️ Esses dados não são mostrados em nenhum ponto do sistema. Quando o CRM não informa o nome da situação, fica guardado o código numérico dela.
13. A importação só acrescenta e atualiza: quem deixou de constar no CRM continua no evento, com as marcações que tinha. 💻
14. A importação cria e altera participantes apenas do evento em que foi acionada. 💻 ⚠️ Os dados da pessoa que ela atualiza (regra 9) pertencem ao cadastro de pessoas, que é único, e passam a valer para todos os eventos.
15. A importação é indivisível: se falhar no meio, nada do que ela fez permanece. 💻
16. A importação só acontece a pedido: não há importação automática nem agendada. 💻
17. Havendo no cadastro mais de uma pessoa com o mesmo Cód. Contato, a importação usa a mais antiga. 💻 ⚠️ As cargas de planilha, na mesma situação, falham.

---

## Cenários

```gherkin
Feature: Importar inscritos do CRM

  Background:
    Given que o usuário está autenticado no GPE
    And abriu, na lista de eventos, a janela "Cargas de Convidados e Confirmados" do evento "Reunião de Diretoria"
    And o evento tem o Código da Campanha "CMP-03460-L2K8"

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Importar inscritos que ainda não estão no evento
    Given que a campanha tem no CRM 3 inscritos aprovados e confirmados, nenhum deles no evento
    When o usuário aciona "Importar Inscritos do CRM"
    Then o botão fica em carregamento, e a janela não pode ser fechada até a resposta
    And o sistema inclui no cadastro as pessoas que faltam e vincula os 3 inscritos ao evento, como convidados e confirmados
    And exibe: "Importação do CRM concluída" com o detalhe "3 inscrito(s) importado(s)."
    And a janela permanece aberta

  Scenario: Repetir a importação
    Given que 2 inscritos da campanha já participam do evento, um deles com check-in e assento
    And a campanha tem mais 1 inscrito aprovado e confirmado, que ainda não está no evento
    When o usuário aciona "Importar Inscritos do CRM"
    Then o sistema exibe: "Importação do CRM concluída" com o detalhe "1 inscrito(s) importado(s), 2 já vinculado(s) atualizado(s)."
    And nenhum participante é duplicado
    And o check-in e o assento de quem já os tinha são preservados

  Scenario: Inscrito sem Cód. Contato
    Given que a campanha tem 2 inscritos aprovados e confirmados, um deles sem Cód. Contato no CRM
    When o usuário aciona "Importar Inscritos do CRM"
    Then o sistema importa o inscrito que tem o código e deixa o outro de fora
    And exibe: "Importação do CRM concluída" com o detalhe "1 inscrito(s) importado(s), 1 sem Cód. Contato (ignorado(s))."
    # ⚠️ 💻 a mesma contagem inclui o inscrito novo sem nome e sem codinome, embora a mensagem fale só em Cód. Contato

  Scenario: Mesmo contato com mais de um registro na campanha
    Given que a campanha traz dois registros para o Cód. Contato "1001", alterados em datas diferentes
    When o usuário aciona "Importar Inscritos do CRM"
    Then o sistema usa o registro de alteração mais recente e vincula a pessoa ao evento uma única vez

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Evento sem Código da Campanha
    Given que o evento não tem o Código da Campanha
    When a janela "Cargas de Convidados e Confirmados" é aberta
    Then a seção "Inscritos do CRM" mostra o aviso "Informe o Código da Campanha no cadastro do evento para habilitar a importação."
    And o botão "Importar Inscritos do CRM" fica desabilitado

  Scenario: Código da Campanha retirado com a lista ainda aberta
    Given que o Código da Campanha foi apagado do evento por outro Administrador depois de a lista ter sido carregada
    When o usuário aciona "Importar Inscritos do CRM"
    Then o sistema não consulta o CRM
    And exibe: "Erro ao importar inscritos do CRM" com o detalhe "O Código da Campanha deve ser preenchido no cadastro do evento."

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Campanha sem inscritos aprovados e confirmados
    Given que a campanha não tem no CRM nenhum inscrito aprovado e confirmado
    When o usuário aciona "Importar Inscritos do CRM"
    Then o sistema não altera os participantes do evento
    And exibe: "Erro ao importar inscritos do CRM" com o detalhe "Não foram encontrados inscritos aprovados e confirmados no CRM para a campanha CMP-03460-L2K8."
    # ⚠️ o critério CA09 do ticket pede informar que não foram encontrados registros; o sistema apresenta o caso como erro 💻
    # 🔍 o texto "Nenhum registro foi alterado.", previsto na tela para um resumo sem contagem, não chega a ser exibido: quando há inscritos, alguma contagem é maior que zero

  Scenario: Inscrito que já está no cadastro de pessoas
    Given que "Maria Souza" está no cadastro com o Cód. Contato "1001" e o cargo "Diretora"
    And o CRM traz o Cód. Contato "1001" com o cargo "Presidente" e sem e-mail
    When o usuário aciona "Importar Inscritos do CRM"
    Then o cargo de "Maria Souza" passa a "Presidente", e o e-mail dela fica em branco
    # ⚠️ 💻 regra 9: o dado ausente no CRM apaga o que estava no cadastro; a mudança vale para todos os eventos

  Scenario: Duas pessoas no cadastro com o mesmo Cód. Contato
    Given que o cadastro de pessoas tem duas pessoas com o Cód. Contato "3003"
    And a campanha traz um inscrito com o Cód. Contato "3003"
    When o usuário aciona "Importar Inscritos do CRM"
    Then o sistema atualiza e vincula ao evento a pessoa cadastrada há mais tempo
    # 💻 regra 17

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Importar Inscritos do CRM" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Eventos › Cadastro, e a importação não fica ao alcance dele
    # ⚠️ o ícone "Cargas de Convidados e Confirmados" não confere o perfil; quem recusa a importação é o servidor — ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Integração com o CRM sem configuração
    Given que a integração com o CRM não está configurada no ambiente
    When o usuário aciona "Importar Inscritos do CRM"
    Then o sistema exibe: "Erro ao importar inscritos do CRM" com o detalhe "Integração com o CRM não configurada."

  Scenario: CRM recusa a credencial da integração
    Given que o CRM não aceita a credencial usada pela integração
    When o usuário aciona "Importar Inscritos do CRM"
    Then o sistema exibe: "Erro ao importar inscritos do CRM" com o detalhe "Não foi possível autenticar no CRM. Verifique as credenciais de integração."

  Scenario: CRM indisponível
    Given que o CRM está fora do ar, recusa a consulta ou não responde em 60 segundos
    When o usuário aciona "Importar Inscritos do CRM"
    Then o sistema exibe: "Erro ao importar inscritos do CRM" com o detalhe "Não foi possível consultar o CRM. Tente novamente mais tarde."
    And nenhum participante do evento é alterado

  Scenario: Falha inesperada durante a importação
    Given que a gravação de um inscrito falha no meio da importação
    When o usuário aciona "Importar Inscritos do CRM"
    Then nada do que a importação fez permanece
    And o sistema exibe: "Erro ao importar inscritos do CRM" com o detalhe "Ocorreu um erro inesperado. Contate o suporte."

  Scenario: Falha sem detalhe do servidor
    Given que o servidor não responde, ou responde sem detalhe
    When o usuário aciona "Importar Inscritos do CRM"
    Then o sistema exibe: "Erro ao importar inscritos do CRM" com o detalhe "Erro ao importar inscritos do CRM. Tente novamente mais tarde."
    # 💻 é o que acontece também quando o evento não existe mais no servidor
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| Código da Campanha | Evento | exibido do cadastro | somente leitura | texto | sim | Mostrado como "Código da Campanha: <código>". Sem ele, a importação fica indisponível |
| Cód. Contato | externo: CRM da CNI | externo: CRM da CNI | somente leitura | texto | sim | Reconhece a pessoa; é gravado no campo CRM dela. O inscrito sem o código não é importado 💻 |
| Nome | externo: CRM da CNI | externo: CRM da CNI | somente leitura | texto | não | Gravado no Nome da pessoa. Na falta dele, vale o do contato relacionado e, depois, o codinome 💻 |
| Codinome | externo: CRM da CNI | externo: CRM da CNI | somente leitura | texto | não | Gravado no Codinome da pessoa |
| E-mail | externo: CRM da CNI | externo: CRM da CNI | somente leitura | texto | não | Gravado no E-mail da pessoa; o formato não é conferido 💻 |
| Empresa | externo: CRM da CNI | externo: CRM da CNI | somente leitura | texto | não | Gravada na Razão Social da pessoa 💻 |
| Cargo | externo: CRM da CNI | externo: CRM da CNI | somente leitura | texto | não | Gravado no Cargo da pessoa |
| Contato relacionado | externo: CRM da CNI | externo: CRM da CNI | somente leitura | texto | não | Identificação do contato no CRM; fica guardada na participação 💻 |
| Data de envio do formulário | externo: CRM da CNI | externo: CRM da CNI | somente leitura | data e hora | não | Fica guardada na participação; data em formato inválido é desprezada 💻 |
| Status da Inscrição | externo: CRM da CNI | externo: CRM da CNI | somente leitura | texto | não | Fica guardado na participação. Só entram inscritos com a inscrição confirmada (regra 2) |
| Status Aprovação | externo: CRM da CNI | externo: CRM da CNI | somente leitura | texto | não | Fica guardado na participação. Só entram inscritos aprovados (regra 2) |

*Só o Código da Campanha aparece na janela. Os demais são os dados que vêm do CRM, sem rótulo em tela: os nomes são os do ticket `PDTIC25148-36` e do modelo de dados.*

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| Convidado | Sim | Em todo inscrito importado, novo no evento ou já participante |
| Confirmado | Sim | Em todo inscrito importado, novo no evento ou já participante |
| Check-In | Não | Só quando o inscrito ainda não participava do evento |
| Atendido | Não | Só quando o inscrito ainda não participava do evento |
| Identificação da inscrição no CRM | A do registro importado | A cada importação |
| Origem do cadastro | Carga | Quando a importação inclui a pessoa |
| Data de Criação | Data e hora da importação | Quando a importação inclui a pessoa |
| Data de Alteração | Data e hora da importação | Quando a importação atualiza uma pessoa já existente |

---

## Dados lidos e gravados

| Entidade | Papel | Por que a feature a toca |
|---|---|---|
| EventoPessoa | lê e grava | Cria a participação do inscrito no evento ou atualiza a que já existe, com as marcações e os dados da inscrição (regras 11 e 12) |
| Pessoa | lê e grava | Reconhece a pessoa pelo Cód. Contato, inclui a que falta e atualiza a que existe (regras 8 a 10) |

---

## Comportamento de tela

### Onde fica
Na tela Eventos, o ícone de pasta com a dica "Cargas de Convidados e Confirmados", em cada linha da lista, abre uma janela sobre a tela. A seção "Inscritos do CRM" é a última do corpo da janela, depois de "Carga de Convidados" e "Carga de Confirmados". Com o Código da Campanha preenchido no evento, a seção mostra "Código da Campanha:" seguido do código, em destaque; sem ele, mostra o aviso "Informe o Código da Campanha no cadastro do evento para habilitar a importação.". Abaixo fica o botão "Importar Inscritos do CRM", desabilitado quando não há código.

Durante a importação, o botão fica em carregamento, a janela não pode ser fechada e o botão "Enviar", das cargas de planilha, fica desabilitado. Ao terminar, a janela continua aberta, e o resultado aparece em mensagem. A importação independe do botão "Enviar".

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Botão "Importar Inscritos do CRM" em carregamento e desabilitado; a janela não pode ser fechada |
| Erro de validação | Sem Código da Campanha: o aviso "Informe o Código da Campanha no cadastro do evento para habilitar a importação." e o botão desabilitado |
| Erro de servidor | "Erro ao importar inscritos do CRM" com o detalhe enviado pelo servidor — o motivo da falha — ou, na falta dele, "Erro ao importar inscritos do CRM. Tente novamente mais tarde." |
| Sucesso | "Importação do CRM concluída" com o resumo: "{n} inscrito(s) importado(s)", "{n} já vinculado(s) atualizado(s)" e "{n} sem Cód. Contato (ignorado(s))", separados por vírgula, só as contagens maiores que zero. A janela permanece aberta, e a lista de eventos não é recarregada |
| Empty state | Campanha sem inscritos aprovados e confirmados: tratada como erro ⚠️ (cenário "Campanha sem inscritos aprovados e confirmados") |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Depois da importação, todo inscrito aprovado e confirmado da campanha que tem Cód. Contato consta no evento como convidado e confirmado | Regras 2, 6 e 11 |
| SC-02 | Repetir a importação não duplica participante nem desfaz check-in, atendimento ou assento | Regra 11 · cenário "Repetir a importação" |
| SC-03 | Ao fim da importação, o Administrador recebe a quantidade de inscritos importados, de já vinculados atualizados e de ignorados | Cenários do caminho feliz |
| SC-04 | Cada motivo de falha da integração — campanha não informada, sem inscritos, integração não configurada, credencial recusada, CRM indisponível — é comunicado com a sua própria mensagem | Cenários de erros e de estados especiais |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Importar Inscritos do CRM | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade EventoPessoa

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Seção "Inscritos do CRM" e botão de importação | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento/pages/eventos/components/eventos-list/components/evento-participantes/evento-participantes.component.ts` (linhas 59–61 e 186–200) e `.html` (linhas 6 e 109–127) | — |
| Mensagens de resultado e de erro | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento/pages/eventos/components/eventos-list/evento-list.component.ts` (linhas 192–205) | — |
| Operação `POST /administracao/eventos/{id}/carga/crm` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoController.java` (linhas 148–152) | — |
| Regras da importação: pessoa, participação e contagens | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/EventoPessoaServiceImpl.java` (linhas 203–327) | — |
| Consulta ao CRM, mapeamento dos dados e mensagens de falha | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/DynamicsCrmServiceImpl.java` (linhas 39–41 e 76–256) | — |
| Testes que confirmam as regras | sistema_mesa_checkin_backend | `src/test/java/br/com/cni/apimesacheckin/service/impl/EventoPessoaServiceImplImportarCrmTest.java` (linhas 67–206) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature está em teste (ticket `PDTIC25148-36`); o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

O CRM é o Dynamics 365; a consulta filtra a campanha pelo código e as duas situações (Status Aprovação e Status da Inscrição) pelo mesmo valor (`124070000`), segue a paginação até o fim e, diante de credencial vencida, renova a credencial e repete a consulta uma única vez. Evento inexistente devolve resposta sem conteúdo, e a tela mostra a mensagem genérica. A mensagem "Informe o código da campanha do CRM." existe no serviço de consulta e não chega a ser emitida por esta feature, porque o evento sem código é barrado antes 🔍.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-10-04 | Claude (sync do engine 4.0.2) | Correção | Na `## Implementação`, a frase das duas situações passa a nomeá-las (Status Aprovação e Status da Inscrição), como a regra 2 já fazia: o FD-9 do engine 4.0 só aceita a quantidade nomeada na própria frase ou em tabela/lista do mesmo substantivo. Nenhuma regra muda. |
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do código e dos testes, confrontada com o ticket `PDTIC25148-36` do Jira (em teste); a funcionalidade não consta em GPE004 |

---

*Feature Set: Cadastro de Eventos · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
