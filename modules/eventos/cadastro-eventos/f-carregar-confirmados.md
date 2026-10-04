<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: EVT-CAD-08
feature_set: EVT-CAD
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
  pendente: true
  revisada_em: ""
  revisada_ate: ""
---

# Carregar Confirmados
> **Nível 3** - Feature Set: Cadastro de Eventos — Major Feature Set: Eventos - `EVT-CAD-08`

## Descrição

Permite que o Administrador carregue de uma planilha a relação de quem confirmou presença em um evento; cada pessoa da planilha fica marcada como confirmada naquele evento, e a que ainda não tem cadastro é incluída no cadastro de pessoas.

A carga fica na janela Cargas de Convidados e Confirmados, aberta pelo ícone de pasta em cada linha da lista de eventos. O Administrador adiciona a planilha na seção Carga de Confirmados e aciona Enviar; a janela fecha, e o sistema avisa quando a carga termina.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE004 – Manter Evento v1.1, de 16/12/2025 (documento legado), funcionalidade "Carregar Lista de Confirmados" ⚠️ sem chave na ferramenta de demandas | Criação | — Carregar, de um arquivo Excel, a lista de convidados confirmados: cada pessoa da lista tem a participação confirmada no evento, a que não possui cadastro é cadastrada como pessoa, e a identificação é feita pelo Cód. Contato. A atualização dos dados de quem já existe não está no documento: vem do código 💻 |

---

<div class="dev-only">

## Superfície

**Modal** — origem: Pesquisar Eventos `EVT-CAD-01` (`/eventos`), ícone de pasta "Cargas de Convidados e Confirmados" em cada linha da lista; seção "Carga de Confirmados" da janela

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Carregar Convidados / Confirmados" de GPE004

---

</div>

## Regras de negócio

1. A lista de confirmados entra por planilha, nos formatos `.xls` e `.xlsx`. → ver [N1 Pessoas](../../pessoas/README.md): Regras transversais de negócio: 6
2. A carga lê só a primeira folha da planilha e despreza a primeira linha, tida como cabeçalho. → ver [N1 Pessoas](../../pessoas/README.md): Regras transversais de negócio: 5
3. A planilha de confirmados tem a mesma disposição da planilha de convidados: catorze colunas, reconhecidas pela posição e não pelo título, nesta ordem — Cód. Contato, Nome Completo, Codinome, Sexo, Cargo, Cargo do Cartão, Empresa/Entidade, Nome Fantasia (Empresa/Entidade) (Pessoa Jurídica), CNPJ (Empresa/Entidade) (Pessoa Jurídica), Telefone, Telefone Celular, Email Comercial, Estado e Estado (Empresa/Entidade) (Pessoa Jurídica). O cabeçalho não é conferido. 💻 ⚠️ GPE004 lista as mesmas colunas, sem dizer que a ordem importa 📄.
4. Só o Nome Completo é exigido em cada linha: a linha sem nome é desprezada. 💻 ⚠️ GPE004 dá como obrigatórios também Cód. Contato, Sexo, Cargo, Cargo do Cartão, Empresa/Entidade e Email Comercial 📄.
5. A pessoa é reconhecida pelo Cód. Contato. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 12
6. A pessoa confirmada que não tem cadastro é incluída no cadastro de pessoas. A origem do cadastro dela fica registrada como Carga 💻.
7. A pessoa cujo Cód. Contato já existe tem todos os dados trazidos pela planilha substituídos, inclusive por valor em branco. 💻 ⚠️ GPE004 só prevê o cadastro de quem não existe 📄.
8. A linha sem Cód. Contato sempre inclui uma pessoa nova, ainda que já exista no cadastro alguém com o mesmo nome. 💻 ⚠️ Carregar duas vezes a mesma planilha duplica essas pessoas.
9. A pessoa que já participa do evento passa a constar como confirmada; a condição de convidada, o check-in, o atendimento e o assento dela ficam como estavam. 💻 A confirmação feita pela carga não desfaz o check-in, ao contrário da alteração da confirmação feita participante a participante. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 7
10. A pessoa que ainda não participa do evento passa a participar como confirmada e não convidada, sem check-in e sem atendimento. 💻 ⚠️ GPE004 trata a lista como de "convidados confirmados" 📄; quem aparece só na planilha de confirmados fica no evento sem a marca de convidado.
11. A carga só acrescenta confirmações: quem não está na planilha continua no evento e mantém a confirmação que tinha. 💻
12. Telefone, Telefone Celular e CNPJ são guardados só com os dígitos; em Sexo, só "Masculino" e "Feminino", escritos exatamente assim, são reconhecidos, e qualquer outro valor vira Não informado. 💻
13. Ao atualizar uma pessoa já existente, a carga substitui o CPF dela pelo CNPJ da planilha — ou o apaga, quando a planilha não traz CNPJ. 💻 ⚠️ Suspeita de defeito: a planilha não tem coluna de CPF.
14. Cada linha é gravada por si: se a carga falha numa linha, as linhas anteriores permanecem carregadas e as seguintes ficam de fora. 🔍

---

## Cenários

```gherkin
Feature: Carregar confirmados

  Background:
    Given que o usuário está autenticado no GPE
    And abriu, na lista de eventos, a janela "Cargas de Convidados e Confirmados" do evento "Reunião de Diretoria"

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Confirmar quem já estava no evento como convidado
    Given que "Maria Souza", Cód. Contato "1001", participa do evento como convidada, ainda não confirmada
    And a planilha traz o Cód. Contato "1001"
    When o usuário adiciona a planilha na seção "Carga de Confirmados"
    Then o sistema exibe: "Planilha adicionada" com o detalhe "Planilha de confirmados adicionada"
    When o usuário aciona "Enviar"
    Then a janela é fechada, e o sistema exibe: "Cargas em processamento." com o detalhe "Por favor aguarde, as cargas estão em processamento."
    And "Maria Souza" passa a constar no evento como confirmada, e continua convidada
    And, ao fim da carga, o sistema exibe: "Carga concluída" com o detalhe "Lista de confirmados foi atualizada."

  Scenario: Confirmado que não estava no evento nem no cadastro de pessoas
    Given uma planilha com a linha de "Pedro Alves", Cód. Contato "4004", que não existe no cadastro de pessoas
    When o usuário envia a planilha de confirmados
    Then "Pedro Alves" é incluído no cadastro de pessoas, com origem Carga
    And passa a participar do evento como confirmado, sem a marca de convidado, sem check-in e sem atendimento
    # ⚠️ 💻 regra 10: a carga de confirmados não marca a pessoa como convidada

  Scenario: Confirmado que já fez check-in
    Given que "João Lima" participa do evento com check-in e assento, e não está confirmado
    And a planilha traz "João Lima"
    When o usuário envia a planilha de confirmados
    Then "João Lima" passa a constar como confirmado
    And o check-in e o assento dele ficam como estavam

  Scenario: Quem não está na planilha mantém a confirmação
    Given que "Ana Reis" participa do evento, confirmada, e não consta da planilha
    When o usuário envia a planilha de confirmados
    Then "Ana Reis" continua confirmada no evento

  Scenario: Retirar a planilha antes de enviar
    Given que o usuário adicionou uma planilha na seção "Carga de Confirmados"
    When aciona a lixeira ao lado do nome da planilha
    Then o sistema exibe: "Planilha removida" com o detalhe "Planilha de confirmados removida"

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Linha sem Nome Completo
    Given uma planilha em que uma das linhas não tem o Nome Completo
    When o usuário envia a planilha de confirmados
    Then a linha é desprezada, sem aviso, e as demais são carregadas
    # ⚠️ 💻 o usuário não fica sabendo que a linha ficou de fora

  Scenario: Linha sem Cód. Contato
    Given uma planilha em que a linha de "Carlos Dias" não tem o Cód. Contato
    When o usuário envia a planilha de confirmados
    Then "Carlos Dias" é incluído no cadastro como pessoa nova e passa a participar do evento como confirmado
    # ⚠️ mesmo que "Carlos Dias" já seja convidado do evento, ele não é reconhecido: fica no evento duas vezes 💻
    # ⚠️ GPE004 dá o Cód. Contato como obrigatório e manda usá-lo para identificar a pessoa 📄

  Scenario: Planilha com as colunas fora da ordem esperada
    Given uma planilha que traz as colunas da regra 3 em outra ordem
    When o usuário envia a planilha de confirmados
    Then o sistema carrega as linhas lendo cada coluna pela posição, e os dados ficam gravados nos campos errados, sem aviso
    # ⚠️ 💻 o cabeçalho não é conferido

  Scenario: Arquivo que não é planilha
    When o usuário adiciona na seção "Carga de Confirmados" um arquivo que não é `.xls` nem `.xlsx`
    Then o sistema recusa o arquivo e exibe "<nome do arquivo>: Tipo de arquivo não permitido" com o detalhe "Tipos permitidos: .xlsx,.xls"

  Scenario: Planilha acima do tamanho máximo
    When o usuário adiciona uma planilha com mais de 200 MB
    Then o sistema recusa a planilha e exibe "O arquivo selecionado excede o tamanho máximo permitido" com o detalhe "O tamanho máximo de arquivo permitido é <limite>"

  Scenario: Planilha que o navegador não consegue ler
    Given que o navegador não consegue ler o arquivo escolhido
    When o usuário o adiciona na seção "Carga de Confirmados"
    Then o sistema exibe: "Falha ao ler planilha." com o detalhe "Falha ao ler planilha de confirmados."

  Scenario: Arquivo com nome de planilha e conteúdo inválido
    Given um arquivo com a extensão `.xlsx` cujo conteúdo não é uma planilha
    When o usuário o envia como planilha de confirmados
    Then nada é carregado
    And o sistema exibe: "Carga concluída" com o detalhe "Lista de confirmados foi atualizada."
    # ⚠️ 💻 suspeita de defeito: o servidor não consegue abrir a planilha e responde como se a carga tivesse sido feita

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: CPF da pessoa trocado pelo CNPJ da planilha
    Given que "João Lima" está no cadastro com o Cód. Contato "2002" e o CPF "111.222.333-44"
    And a planilha traz o Cód. Contato "2002" com o CNPJ "12.345.678/0001-90"
    When o usuário envia a planilha de confirmados
    Then o CPF de "João Lima" passa a ser "12345678000190"
    # ⚠️ 💻 suspeita de defeito (regra 13); se a planilha não trouxesse CNPJ, o CPF ficaria em branco

  Scenario: Duas pessoas no cadastro com o mesmo Cód. Contato
    Given que o cadastro de pessoas tem duas pessoas com o Cód. Contato "3003"
    And a planilha traz o Cód. Contato "3003"
    When o usuário envia a planilha de confirmados
    Then a carga é interrompida naquela linha, e as linhas anteriores permanecem carregadas
    And o sistema exibe: "Erro ao processar carga." com o detalhe "Ocorreu um erro inesperado. Contate o suporte."
    # ⚠️ 🔍 inferido do código, sem execução: o sistema não impede dois cadastros com o mesmo código

  Scenario: Mesma planilha carregada duas vezes
    Given que o usuário já carregou a planilha de confirmados do evento
    When envia a mesma planilha outra vez
    Then as pessoas com Cód. Contato não são duplicadas, nem no cadastro nem no evento
    And as pessoas sem Cód. Contato são incluídas de novo no cadastro e no evento
    # ⚠️ 💻 regra 8

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Carregar Confirmados" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Eventos › Cadastro, e a carga não fica ao alcance dele
    # ⚠️ o ícone "Cargas de Convidados e Confirmados" não confere o perfil; quem recusa a carga é o servidor — ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Planilhas de convidados e de confirmados enviadas juntas
    Given que o usuário adicionou uma planilha em "Carga de Convidados" e outra em "Carga de Confirmados"
    When aciona "Enviar"
    Then a planilha de convidados é processada
    And a planilha de confirmados não é enviada, e nenhuma mensagem sobre a carga de confirmados aparece
    # ⚠️ 🔍 suspeita de defeito, inferida do código sem execução: ao fechar, a janela descarta as duas planilhas antes de chegar a vez da de confirmados
    # o Jira tem em aberto PDTIC25148-33, "Erro ao carregar convidados e confirmados ao mesmo tempo"; enviada sozinha, a planilha de confirmados é processada

  Scenario: Falha no processamento da carga
    Given que o processamento da planilha falha no servidor
    When o usuário envia a planilha de confirmados
    Then o sistema exibe: "Erro ao processar carga." com o detalhe enviado pelo servidor
    And, quando o servidor não envia detalhe, o detalhe é "Erro ao processar a carga de Confirmados. Verifique o arquivo e tente novamente."

  Scenario: Carga sem resumo
    Given uma planilha com 50 linhas, das quais 3 não têm o Nome Completo
    When o usuário envia a planilha de confirmados
    Then o sistema exibe apenas: "Carga concluída" com o detalhe "Lista de confirmados foi atualizada."
    # ⚠️ 💻 não há resumo: o sistema não diz quantas pessoas foram confirmadas, incluídas ou desprezadas, nem aponta erro por linha

  Scenario: Cód. Contato longo digitado como número
    Given uma planilha em que o Cód. Contato "12345678" está numa célula de formato numérico
    When o usuário envia a planilha de confirmados
    Then a pessoa já cadastrada com esse código não é reconhecida, e uma pessoa nova é incluída e confirmada
    # ⚠️ 🔍 inferido do código, sem execução: número com oito dígitos ou mais é lido em notação científica
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| Carga de Confirmados | EventoPessoa | entrada do usuário | editável | arquivo | sim | Uma planilha `.xls` ou `.xlsx`, de até 200 MB 💻 |
| Cód. Contato | Pessoa | entrada do usuário — 1ª coluna da planilha | — | texto | não | Reconhece a pessoa; é gravado no campo CRM dela. Sem ele, a linha sempre inclui pessoa nova 💻. ⚠️ GPE004 o dá como obrigatório 📄 |
| Nome Completo | Pessoa | entrada do usuário — 2ª coluna | — | texto | sim | A linha sem nome é desprezada. Caracteres invisíveis são retirados 💻 |
| Codinome | Pessoa | entrada do usuário — 3ª coluna | — | texto | não | Caracteres invisíveis são retirados 💻 |
| Sexo | dado de código | entrada do usuário — 4ª coluna | — | lista de opções | não | "Masculino" ou "Feminino"; outro valor, ou a falta dele, vira Não informado 💻. ⚠️ GPE004 o dá como obrigatório 📄 |
| Cargo | Pessoa | entrada do usuário — 5ª coluna | — | texto | não | ⚠️ GPE004 o dá como obrigatório 📄 |
| Cargo do Cartão | Pessoa | entrada do usuário — 6ª coluna | — | texto | não | ⚠️ GPE004 o dá como obrigatório 📄 |
| Empresa/Entidade | Pessoa | entrada do usuário — 7ª coluna | — | texto | não | Gravado na Razão Social da pessoa. ⚠️ GPE004 o dá como obrigatório 📄 |
| Nome Fantasia (Empresa/Entidade) (Pessoa Jurídica) | Pessoa | entrada do usuário — 8ª coluna | — | texto | não | Gravado no Nome Fantasia da pessoa |
| CNPJ (Empresa/Entidade) (Pessoa Jurídica) | Pessoa | entrada do usuário — 9ª coluna | — | texto | não | Guardado só com os dígitos; o formato não é conferido 💻. ⚠️ Vai também para o CPF de quem já existe (regra 13) |
| Telefone | Pessoa | entrada do usuário — 10ª coluna | — | texto | não | Guardado só com os dígitos, no Telefone Principal da pessoa 💻 |
| Telefone Celular | Pessoa | entrada do usuário — 11ª coluna | — | texto | não | Guardado só com os dígitos, no Celular da pessoa 💻 |
| Email Comercial | Pessoa | entrada do usuário — 12ª coluna | — | texto | não | Gravado no E-mail da pessoa; o formato não é conferido 💻. ⚠️ GPE004 o dá como obrigatório 📄 |
| Estado | Pessoa | entrada do usuário — 13ª coluna | — | texto | não | Gravado como vier, sem conferir se é uma UF 💻 |
| Estado (Empresa/Entidade) (Pessoa Jurídica) | Pessoa | entrada do usuário — 14ª coluna | — | texto | não | Gravado no Estado da organização, como vier 💻 |

*Só a primeira linha da tabela é campo da janela; as demais são as colunas da planilha, que a janela não mostra nem descreve. Os nomes são os de GPE004 e do código — a carga não os confere (regra 3).*

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| Confirmado | Sim | Em toda pessoa da planilha, ao entrar no evento ou já estando nele |
| Convidado | Não ⚠️ | Só quando a pessoa ainda não participava do evento (regra 10) |
| Check-In | Não | Só quando a pessoa ainda não participava do evento |
| Atendido | Não | Só quando a pessoa ainda não participava do evento |
| Origem do cadastro | Carga | Quando a carga inclui a pessoa |
| Data de Criação | Data e hora da carga | Quando a carga inclui a pessoa |
| Data de Alteração | Data e hora da carga | Quando a carga atualiza uma pessoa já existente |
| CPF ⚠️ | O CNPJ da planilha, ou vazio | Quando a carga atualiza uma pessoa já existente (regra 13) |

---

## Dados lidos e gravados

| Entidade | Papel | Por que a feature a toca |
|---|---|---|
| Evento | lê | Identifica o evento que recebe as confirmações |

---

## Comportamento de tela

### Onde fica
Na tela Eventos, o ícone de pasta com a dica "Cargas de Convidados e Confirmados", em cada linha da lista, abre uma janela sobre a tela. O cabeçalho da janela traz o nome do evento e, abaixo, o local e a data por extenso. A seção "Carga de Confirmados" é a segunda do corpo da janela, entre "Carga de Convidados" e "Inscritos do CRM"; o rodapé traz o botão "Enviar", comum às duas cargas de planilha.

A seção tem o botão "Adicionar" e a área "Clique em adicionar ou arraste e solte os arquivos aqui...". A planilha adicionada aparece como um botão com o nome do arquivo (dica "Download"), que a baixa de volta, ao lado de uma lixeira (dica "Excluir"), que a retira. O botão "Enviar" fica desabilitado enquanto não há nenhuma planilha adicionada e enquanto a importação do CRM está em andamento. Ao acionar "Enviar", a janela fecha na hora, e o resultado chega depois, por mensagem.

⚠️ A janela não diz quais colunas a planilha deve ter, nem em que ordem, e não oferece planilha-modelo 💻. ⚠️ Com planilhas nas duas seções de carga, há indício de que só a de convidados é enviada 🔍 — ver o cenário "Planilhas de convidados e de confirmados enviadas juntas".

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Ao acionar "Enviar", a janela fecha e aparece "Cargas em processamento." com o detalhe "Por favor aguarde, as cargas estão em processamento."; não há indicador de andamento |
| Erro de validação | Arquivo que não é planilha: "<nome do arquivo>: Tipo de arquivo não permitido" com o detalhe "Tipos permitidos: .xlsx,.xls". Acima de 200 MB: "O arquivo selecionado excede o tamanho máximo permitido". Falha na leitura: "Falha ao ler planilha." com o detalhe "Falha ao ler planilha de confirmados.". ⚠️ As linhas inválidas da planilha não geram aviso |
| Erro de servidor | "Erro ao processar carga." com o detalhe enviado pelo servidor ou, na falta dele, "Erro ao processar a carga de Confirmados. Verifique o arquivo e tente novamente." |
| Sucesso | "Carga concluída" com o detalhe "Lista de confirmados foi atualizada.", sem resumo do que foi carregado ⚠️. A lista de eventos não é recarregada |
| Empty state | Seção sem planilha: a área "Clique em adicionar ou arraste e solte os arquivos aqui..." e, se a outra seção de carga também estiver vazia, o botão "Enviar" desabilitado |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Toda linha da planilha que tem Nome Completo resulta em um participante do evento marcado como confirmado | Regras 4, 9 e 10 |
| SC-02 | A pessoa confirmada que não tinha cadastro passa a existir no cadastro de pessoas, e a que já tinha não é duplicada | Regras 5, 6 e 7 |
| SC-03 | Nenhum participante do evento perde o check-in, o atendimento ou o assento por causa da carga, e ninguém é desconfirmado por ela | Regras 9 e 11 · cenário "Confirmado que já fez check-in" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Carregar Confirmados | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade EventoPessoa

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Seção "Carga de Confirmados", botão "Enviar" e mensagens da carga | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento/pages/eventos/components/eventos-list/components/evento-participantes/evento-participantes.component.ts` (linhas 28–34, 117–158 e 202–226) e `.html` (linhas 66–107 e 129–138) | — |
| Fechamento da janela e aviso "Cargas em processamento." | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento/pages/eventos/components/eventos-list/evento-list.component.ts` (linhas 186–190) | — |
| Operação `POST /administracao/eventos/{id}/carga/confirmados` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoController.java` (linhas 142–146) | — |
| Leitura da planilha, pessoa e confirmação no evento | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/EventoPessoaServiceImpl.java` (linhas 183–201 e 329–408; CPF na linha 375) | — |
| Posição das colunas da planilha | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/enumeration/ExcelHeadersEnum.java` (linhas 7–20) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

A carga de confirmados usa a mesma rotina da carga de convidados; muda só a marcação gravada na participação. O envio das duas planilhas é sequencial na tela: ao emitir o aviso de envio, a tela-mãe fecha a janela, e o fechamento zera as duas planilhas guardadas — a de confirmados já não existe quando a de convidados termina 🔍.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE004 – Manter Evento (funcionalidade "Carregar Lista de Confirmados" e regra "Carregar Convidados Confirmados") e do código |

---

*Feature Set: Cadastro de Eventos · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
