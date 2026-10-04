<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: PES-CAD-07
feature_set: PES-CAD
dominio: PES
entidade: HistoricoPessoa
data_model_ref: data-models/pessoas.md#historicopessoa
endpoints: []
error_codes: []
depende_de: ["PES-CAD-01"]
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

# Carregar Histórico de Participação
> **Nível 3** - Feature Set: Cadastro de Pessoas — Major Feature Set: Pessoas - `PES-CAD-07`

## Descrição

Permite que o Administrador traga, de uma planilha extraída do CRM, quantas vezes cada pessoa participou de eventos em cada ano; o histórico das pessoas presentes na planilha é substituído pelo que ela traz, e o das demais não muda.

Parte-se do botão Carga de Histórico, na tela Pessoas. O usuário escolhe a planilha, no formato .xlsx ou .xls, e aciona Enviar; ao terminar, o sistema informa de quantas linhas atualizou o histórico e quantas ficaram sem pessoa correspondente.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE003 – Manter Pessoa v1.0, de 03/10/2025 (documento legado), funcionalidade "Realizar Carga de Histórico" e regra de negócio "Carregar Histórico" ⚠️ sem chave na ferramenta de demandas | Criação | — Carregar, de um arquivo Excel, o histórico de participação das pessoas, identificadas pelo `Cód. Contato`. O documento descreve as colunas `Cód. Contato` e `Ano participação` 📄; o código exige só o `Cód. Contato` e lê cada outra coluna como um ano 💻 ⚠️. A substituição do histórico por pessoa e o resumo ao fim da carga não estão no documento: vêm do código 💻 |

---

<div class="dev-only">

## Superfície

**Modal** — origem: Pesquisar Pessoas `PES-CAD-01` (`/administracao-pessoas`), botão "Carga de Histórico"

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Carga de Histórico" de GPE003

---

</div>

## Regras de negócio

1. A pessoa de cada linha é reconhecida pelo `Cód. Contato`, que tem de ser igual ao CRM de uma pessoa do cadastro. → ver [N1 Pessoas](../README.md): Regras transversais de negócio: 1 ⚠️ Nesta carga o código precisa estar gravado na planilha como número: gravado como texto, a linha é desconsiderada 💻. Por isso, a pessoa cujo CRM tem letras não é alcançada por esta carga.
2. A carga lê somente a primeira folha da planilha, e a primeira linha dela é o cabeçalho. 💻 → ver [N1 Pessoas](../README.md): Regras transversais de negócio: 5
3. A planilha vem no formato `.xlsx` ou `.xls`. → ver [N1 Pessoas](../README.md): Regras transversais de negócio: 6 ⚠️ O servidor não confere a extensão: abre a planilha pelo conteúdo. Quem restringe aos dois formatos é a interface 💻.
4. A carga exige só a coluna `Cód. Contato`, reconhecida pelo nome exato do cabeçalho, em qualquer posição. Cada uma das demais colunas é lida como um ano: o cabeçalho é o ano — por exemplo, `2023` — e a célula é a quantidade de participações da pessoa naquele ano. 💻 ⚠️ GPE003 descreve duas colunas obrigatórias, `Cód. Contato` e `Ano participação` 📄.
5. A carga substitui o histórico por pessoa: de cada pessoa encontrada na planilha, todo o histórico anterior é apagado e regravado com o que a linha traz. O histórico de quem não está na planilha não é alterado. 💻
6. Só gera histórico o ano cuja célula traz um número maior que zero; a célula vazia, com texto, com zero ou com número negativo é ignorada, e a parte decimal do número é descartada. 💻
7. A pessoa encontrada cuja linha não traz nenhum ano com número maior que zero fica sem histórico. 💻
8. A linha cujo `Cód. Contato` não corresponde a nenhuma pessoa do cadastro é desconsiderada: a carga não cria pessoas. 💻
9. Quando a planilha traz duas linhas da mesma pessoa, vale a última. 💻
10. A coluna cujo cabeçalho não é um número interrompe a carga quando traz um número maior que zero na linha de uma pessoa encontrada — é o caso de uma coluna de total. 💻 ⚠️ Suspeita de defeito: a planilha montada como GPE003 descreve, com a coluna `Ano participação`, cai nesta situação.
11. A carga não vale por inteiro: cada pessoa é gravada à medida que a planilha é lida, e uma falha no meio deixa gravado o histórico das linhas já lidas. 💻 ⚠️ As cargas de grupos de trabalho e de temas, ao contrário, desfazem tudo quando falham.
12. Havendo no cadastro duas pessoas com o mesmo CRM, a carga falha ao chegar a esse código. 🔍 ⚠️ O cadastro não impede CRM repetido.

---

## Cenários

```gherkin
Feature: Carregar histórico de participação

  Background:
    Given que o usuário está autenticado no GPE
    And abriu a janela "Carga de Histórico" pelo botão "Carga de Histórico" da tela "Pessoas"

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Carregar histórico de participação
    Given uma planilha com as colunas "Cód. Contato", "2023" e "2024" e 4 linhas, todas de pessoas cadastradas
    And a linha de "Maria Souza" traz 2 na coluna "2023" e 1 na coluna "2024"
    When o usuário adiciona a planilha
    Then o sistema exibe: "Planilha adicionada" com o detalhe "Planilha de Histórico adicionada"
    When o usuário aciona "Enviar"
    Then a janela se fecha e o sistema exibe: "Carga em processamento." com o detalhe "Carga de Históricos em processamento."
    And o sistema apaga o histórico anterior das 4 pessoas e grava o que a planilha traz
    And "Maria Souza" passa a ter 2 participações em 2023 e 1 participação em 2024
    And exibe: "Carga concluída" com o detalhe "4 históricos de participação atualizados."

  Scenario: Planilha com linha de pessoa não cadastrada
    Given uma planilha com 4 linhas, 1 delas com "Cód. Contato" que não é de nenhuma pessoa do cadastro
    When o usuário envia a planilha
    Then o sistema atualiza o histórico de 3 pessoas e desconsidera a linha sem pessoa
    And exibe: "Carga concluída" com o detalhe "3 históricos de participação atualizados e 1 pessoas não foram encontradas."
    # ⚠️ 💻 o texto não trata o singular, e o sistema não diz quais linhas ficaram de fora

  Scenario: Ano sem participação
    Given que a linha de "João Lima" traz 3 na coluna "2023" e a coluna "2024" vazia
    When o usuário envia a planilha
    Then "João Lima" fica com 3 participações em 2023 e sem registro para 2024

  Scenario: Retirar a planilha escolhida
    Given que o usuário adicionou uma planilha
    When o usuário aciona o ícone de lixeira ao lado do nome da planilha
    Then o sistema exibe: "Planilha removida" com o detalhe "Planilha de Histórico removida"
    And o botão "Enviar" volta a ficar desabilitado

  Scenario: Fechar a janela sem enviar
    When o usuário fecha a janela
    Then nenhum histórico é alterado

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Enviar sem planilha
    When nenhuma planilha foi adicionada
    Then o botão "Enviar" permanece desabilitado

  Scenario: Planilha sem a coluna do código
    Given uma planilha que não tem a coluna "Cód. Contato"
    When o usuário envia a planilha
    Then o sistema não altera nenhum histórico
    And exibe: "Erro ao processar carga de Históricos" com o detalhe "Cabeçalho incompleto na carga."

  Scenario: Código gravado como texto
    Given uma planilha em que o "Cód. Contato" de uma linha está gravado como texto
    When o usuário envia a planilha
    Then o sistema desconsidera essa linha e a conta entre as pessoas não encontradas
    # ⚠️ 💻 o resumo diz "pessoas não foram encontradas" mesmo quando a pessoa existe e só o formato da célula difere

  Scenario: Planilha no formato descrito em GPE003
    Given uma planilha com as colunas "Cód. Contato" e "Ano participação", com o ano em cada célula dessa segunda coluna
    When o usuário envia a planilha
    Then o sistema interrompe a carga na primeira linha de pessoa encontrada, cujo histórico anterior já foi apagado
    And exibe: "Erro ao processar carga de Históricos" com um detalhe técnico, em inglês, que cita o cabeçalho da coluna
    # ⚠️ 🔍 divergência documento × código; pela leitura do código o detalhe é o texto da falha de conversão do cabeçalho em número — a confirmar em execução

  Scenario: Arquivo de tipo não aceito
    When o usuário escolhe um arquivo que não é .xlsx nem .xls
    Then o sistema recusa o arquivo e exibe, no próprio campo, o nome do arquivo seguido de ": Tipo de arquivo não permitido" e o detalhe "Tipos permitidos: .xlsx,.xls"

  Scenario: Arquivo acima do tamanho aceito
    When o usuário escolhe uma planilha com mais de 200 MB
    Then o sistema recusa o arquivo e exibe, no próprio campo: "O arquivo selecionado excede o tamanho máximo permitido", com o detalhe que começa por "O tamanho máximo de arquivo permitido é"

  Scenario: Planilha que o navegador não consegue ler
    When a leitura da planilha escolhida falha no navegador
    Then o sistema exibe: "Falha ao ler planilha." com o detalhe "Falha ao ler planilha de Histórico."

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Pessoa com histórico de uma carga anterior
    Given que "Maria Souza" tem histórico de 2021 e 2022, trazido por uma carga anterior
    And a nova planilha traz, para "Maria Souza", só a coluna "2024" preenchida
    When o usuário envia a nova planilha
    Then "Maria Souza" fica só com o histórico de 2024
    # 💻 o histórico da pessoa é substituído inteiro, e não ano a ano

  Scenario: Pessoa que não está na planilha
    Given que "João Lima" tem histórico de uma carga anterior
    And a nova planilha não tem nenhuma linha de "João Lima"
    When o usuário envia a nova planilha
    Then o histórico de "João Lima" continua como estava

  Scenario: Mesma pessoa em duas linhas
    Given uma planilha com duas linhas de "Maria Souza", a primeira com 2 em "2023" e a segunda com 1 em "2024"
    When o usuário envia a planilha
    Then "Maria Souza" fica só com 1 participação em 2024
    And o resumo conta as duas linhas como históricos atualizados

  Scenario: Duas pessoas com o mesmo CRM
    Given que o cadastro tem duas pessoas com o CRM "100200"
    And a planilha tem uma linha com o "Cód. Contato" 100200
    When o usuário envia a planilha
    Then a carga é interrompida nessa linha, e o histórico das linhas anteriores fica gravado
    And exibe: "Erro ao processar carga de Históricos" com o detalhe "Ocorreu um erro inesperado. Contate o suporte."
    # ⚠️ 🔍 a confirmar em execução

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Carregar Histórico de Participação" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Administração › Pessoas, e o botão "Carga de Histórico" não fica ao alcance dele
    # ⚠️ a tela não confere o perfil; ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Planilha ilegível
    Given um arquivo com extensão .xlsx cujo conteúdo não é uma planilha
    When o usuário envia o arquivo
    Then o sistema não altera nenhum histórico
    And exibe: "Carga concluída" com o detalhe "."
    # ⚠️ 💻 o servidor responde como sucesso, com as contagens zeradas — suspeita de defeito

  Scenario: Planilha só com o cabeçalho
    Given uma planilha com a coluna "Cód. Contato" e nenhuma linha de dados
    When o usuário envia a planilha
    Then o sistema não altera nenhum histórico
    And exibe: "Carga concluída" com o detalhe "."

  Scenario: Falha no meio da carga
    Given que o processamento falha no servidor depois de algumas linhas
    When o usuário envia a planilha
    Then o histórico das linhas já lidas fica gravado, e o das seguintes não é alterado
    And exibe: "Erro ao processar carga de Históricos" com o detalhe "Ocorreu um erro inesperado. Contate o suporte."
    # ⚠️ 💻 a carga não é desfeita; o sistema não diz até que linha chegou

  Scenario: Servidor não responde
    Given que o servidor não responde
    When o usuário envia a planilha
    Then o sistema exibe: "Erro ao processar carga de Históricos" com o detalhe "Erro ao processar a carga de Histórico. Verifique o arquivo e tente novamente."
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| Planilha | externo: Planilha extraída do CRM | entrada do usuário | editável | arquivo | sim | Único campo da janela, sem rótulo: a planilha é escolhida pelo botão "Adicionar" ou arrastada para a área indicada. Formato .xlsx ou .xls, até 200 MB 💻 |
| Cód. Contato | Pessoa | externo: Planilha extraída do CRM | — | número | sim | Coluna da planilha. A célula tem de ser numérica e igual ao CRM de uma pessoa do cadastro; a linha sem correspondência é desconsiderada 💻 |
| Ano | HistoricoPessoa | externo: Planilha extraída do CRM | — | número | não | Cabeçalho de cada coluna além do `Cód. Contato`; tem de ser um número, como 2023. Não se confere se o número é um ano plausível 💻 ⚠️ GPE003 descreve uma coluna única `Ano participação` 📄 |
| Participações | HistoricoPessoa | externo: Planilha extraída do CRM | — | número | não | Célula da coluna do ano, na linha da pessoa; só o número maior que zero é gravado 💻 |

*A planilha tem uma coluna por ano: o Ano está no cabeçalho, e as Participações, nas células. Nenhuma coluna de ano é obrigatória.*

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| — | — | Nenhum campo é preenchido pelo sistema: o histórico guarda só a pessoa, o ano e a quantidade de participações, sem data da carga 💻 |

---

## Comportamento de tela

### Onde fica
Janela "Carga de Histórico", aberta sobre a tela "Pessoas" pelo botão "Carga de Histórico" (Pesquisar Pessoas `PES-CAD-01`). Abaixo do título vem a instrução "A planilha deve conter as colunas Cód. Contato e os anos das participações.". A janela pode ser arrastada, não muda de tamanho e fecha pelo X.

O campo da planilha tem o botão "Adicionar" e a área "Clique em adicionar ou arraste e solte os arquivos aqui...". Escolhida a planilha, a área mostra um botão com o nome do arquivo, com a dica "Download", que baixa a própria planilha, e um ícone de lixeira, com a dica "Excluir", que a retira. O botão "Enviar" fica desabilitado enquanto não houver planilha.

O resumo exibido ao fim da carga é montado com até dois trechos, cada um presente só quando a sua contagem é maior que zero, unidos por "e" e terminados por ponto: "{n} históricos de participação atualizados" — linhas cuja pessoa foi encontrada; "{n} pessoas não foram encontradas" — linhas sem `Cód. Contato` numérico ou cujo código não é de nenhuma pessoa. As duas contagens são de linhas da planilha: a primeira não é de anos gravados, e a pessoa que aparece em duas linhas conta duas vezes 💻. Quando as duas contagens são zero, o detalhe é só um ponto ⚠️.

A lista de pessoas não é recarregada ao fim da carga; o histórico trazido é visto na aba "Histórico" da tela de cada pessoa (Editar Pessoa `PES-CAD-03`).

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Ao acionar "Enviar", a janela se fecha e aparece o aviso "Carga em processamento." com o detalhe "Carga de Históricos em processamento.". Não há indicador de progresso, e a tela "Pessoas" continua livre para uso |
| Erro de validação | No próprio campo, o arquivo de tipo ou de tamanho não aceito é recusado. Sem planilha, o botão "Enviar" fica desabilitado |
| Erro de servidor | Mensagem "Erro ao processar carga de Históricos", com o detalhe que o servidor devolve — "Cabeçalho incompleto na carga.", "Ocorreu um erro inesperado. Contate o suporte." ou um texto técnico da falha 🔍 — ou, sem resposta do servidor, "Erro ao processar a carga de Histórico. Verifique o arquivo e tente novamente." |
| Sucesso | Aviso "Carga concluída", com o resumo no detalhe |
| Empty state | Janela recém-aberta: a área de seleção mostra "Clique em adicionar ou arraste e solte os arquivos aqui...", e o botão "Enviar" está desabilitado |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Depois da carga, cada pessoa da planilha mostra, na tela dela, os anos e as quantidades de participações que a planilha traz, e nenhum outro | Regras 5 e 6 · cenários "Carregar histórico de participação" e "Pessoa com histórico de uma carga anterior" |
| SC-02 | O histórico de quem não está na planilha é o mesmo antes e depois da carga | Regra 5 · cenário "Pessoa que não está na planilha" |
| SC-03 | Uma planilha sem a coluna `Cód. Contato` não altera nenhum histórico e informa "Cabeçalho incompleto na carga." | Regra 4 · cenário "Planilha sem a coluna do código" |
| SC-04 | O resumo ao fim da carga informa quantas linhas tiveram o histórico atualizado e quantas ficaram sem pessoa correspondente | Regra 8 · cenário "Planilha com linha de pessoa não cadastrada" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Carregar Histórico de Participação | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade HistoricoPessoa

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Janela de carga: seleção da planilha e envio | sistema_mesa_checkin_frontend | `src/app/admin/administracao/acessibilidade/pessoas/pages/pessoas/components/pessoas-carga-historico/pessoas-carga-historico.component.html` (linhas 1–72) e `.ts` (linhas 66–131) | — |
| Botão "Carga de Histórico", avisos e resumo da carga | sistema_mesa_checkin_frontend | `src/app/admin/administracao/acessibilidade/pessoas/pages/pessoas/components/pessoas-filter/pessoas-filter.component.html` (linhas 97–102 e 120–126) e `.ts` (linhas 164–185) | — |
| Chamada da carga | sistema_mesa_checkin_frontend | `src/app/admin/administracao/acessibilidade/pessoas/services/pessoa.service.ts` (linhas 57–60) | — |
| Operação `POST /administracao/pessoas/carga/historico` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/PessoaController.java` (linhas 144–148) | — |
| Processamento da planilha | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/HistoricoPessoaServiceImpl.java` (linhas 42–120) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

O método `processarCarga` não é transacional (linhas 42–43); só a limpeza do histórico de cada pessoa é (`limpaHistoricoPessoa`, linhas 117–120). O ano sai de `Double.parseDouble` sobre o texto do cabeçalho (linha 103), executado depois de a célula ter passado nos testes de tipo e de valor: o cabeçalho não numérico lança `NumberFormatException`, que é uma `IllegalArgumentException` e, por isso, deve ser respondida com `400` e a mensagem da exceção no detalhe 🔍 — o inventário do servidor registra `500` para o mesmo caso. O contador `countExistentes` fica sempre em zero nesta carga.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE003 – Manter Pessoa (funcionalidade "Realizar Carga de Histórico" e regra "Carregar Histórico") e do código |

---

*Feature Set: Cadastro de Pessoas · Major Feature Set: Pessoas · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
