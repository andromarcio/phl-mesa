<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: PES-CAD-06
feature_set: PES-CAD
dominio: PES
entidade: TemaPessoa
data_model_ref: data-models/pessoas.md#temapessoa
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

# Carregar Temas
> **Nível 3** - Feature Set: Cadastro de Pessoas — Major Feature Set: Pessoas - `PES-CAD-06`

## Descrição

Permite que o Administrador traga, de uma planilha extraída do CRM, os temas de interesse a que as pessoas se vinculam; os temas que existiam no cadastro são todos substituídos pelos da planilha.

Parte-se do botão Carga de Temas, na tela Pessoas. O usuário escolhe a planilha, no formato .xlsx ou .xls, e aciona Enviar; ao terminar, o sistema informa quantos temas vinculou e quantas linhas ficaram sem pessoa correspondente.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE003 – Manter Pessoa v1.0, de 03/10/2025 (documento legado), funcionalidade "Realizar Carga de Temas" e regra de negócio "Carregar Temas" ⚠️ sem chave na ferramenta de demandas | Criação | — Carregar, de um arquivo Excel, os temas vinculados às pessoas, identificadas pelo `Cód. Contato`, com as colunas obrigatórias `Cód. Contato` e `Tema`. A substituição de todos os temas existentes, o resumo ao fim da carga e o tratamento das linhas sem pessoa não estão no documento: vêm do código 💻 |

---

<div class="dev-only">

## Superfície

**Modal** — origem: Pesquisar Pessoas `PES-CAD-01` (`/administracao-pessoas`), botão "Carga de Temas"

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Carga de Temas" de GPE003

---

</div>

## Regras de negócio

1. A pessoa de cada linha é reconhecida pelo `Cód. Contato`, que tem de ser igual ao CRM de uma pessoa do cadastro. → ver [N1 Pessoas](../README.md): Regras transversais de negócio: 1
2. A carga lê somente a primeira folha da planilha, e a primeira linha dela é o cabeçalho. 💻 → ver [N1 Pessoas](../README.md): Regras transversais de negócio: 5
3. A planilha vem no formato `.xlsx` ou `.xls`. → ver [N1 Pessoas](../README.md): Regras transversais de negócio: 6 ⚠️ O servidor não confere a extensão: abre a planilha pelo conteúdo. Quem restringe aos dois formatos é a interface 💻.
4. A carga exige as colunas `Cód. Contato` e `Tema`.
5. As colunas são reconhecidas pelo nome exato do cabeçalho — mesmas maiúsculas e minúsculas, mesmos acentos, mesma pontuação —, em qualquer posição da planilha. 💻
6. A carga substitui tudo: todos os temas de todas as pessoas são apagados antes da leitura das linhas, e ficam valendo só os que a planilha traz. 💻 ⚠️ GPE003 não fala em substituição 📄. Consequência: uma planilha parcial elimina os temas de quem não está nela.
7. Cada linha vincula uma pessoa a um tema; a mesma pessoa pode aparecer em várias linhas, uma para cada tema.
8. Quando a planilha repete a mesma pessoa e o mesmo tema, fica um só vínculo. 💻
9. A linha cujo `Cód. Contato` não corresponde a nenhuma pessoa do cadastro é desconsiderada: a carga não cria pessoas. 💻
10. Só a presença das colunas é conferida, não o preenchimento de cada linha: a linha com `Tema` em branco gera um vínculo sem nome de tema. 💻 ⚠️ GPE003 dá as colunas como obrigatórias 📄.
11. A carga vale por inteiro ou não vale: uma falha no meio do processamento desfaz tudo, inclusive a exclusão inicial. 💻
12. O `Cód. Contato` gravado na planilha como número de 8 dígitos ou mais não é reconhecido, porque nesse tamanho o número é lido em notação científica e deixa de coincidir com o CRM do cadastro. 🔍 ⚠️ Suspeita de defeito, a confirmar em execução.
13. Havendo no cadastro duas pessoas com o mesmo CRM, a carga falha ao chegar a esse código. 🔍 ⚠️ O cadastro não impede CRM repetido.

---

## Cenários

```gherkin
Feature: Carregar temas

  Background:
    Given que o usuário está autenticado no GPE
    And abriu a janela "Carga de Temas" pelo botão "Carga de Temas" da tela "Pessoas"

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Carregar temas
    Given uma planilha com as colunas "Cód. Contato" e "Tema" e 8 linhas, todas de pessoas cadastradas
    When o usuário adiciona a planilha
    Then o sistema exibe: "Planilha adicionada" com o detalhe "Planilha de Temas adicionada"
    When o usuário aciona "Enviar"
    Then a janela se fecha e o sistema exibe: "Carga em processamento." com o detalhe "Carga de Temas em processamento."
    And o sistema apaga os temas que existiam e grava os 8 vínculos da planilha, cada um com a data de vínculo
    And exibe: "Carga concluída" com o detalhe "8 temas vinculados."

  Scenario: Planilha com linha de pessoa não cadastrada
    Given uma planilha com 8 linhas, 2 delas com "Cód. Contato" que não é de nenhuma pessoa do cadastro
    When o usuário envia a planilha
    Then o sistema grava 6 vínculos e desconsidera as linhas sem pessoa
    And exibe: "Carga concluída" com o detalhe "6 temas vinculados e 2 pessoas não foram encontradas."
    # ⚠️ 💻 o sistema não diz quais linhas ficaram de fora

  Scenario: Planilha que repete pessoa e tema
    Given uma planilha com 3 linhas, 2 delas com a mesma pessoa e o mesmo tema
    When o usuário envia a planilha
    Then o sistema grava 2 vínculos e desconsidera a linha repetida
    And exibe: "Carga concluída" com o detalhe "2 temas vinculados e 1 foram atualizados."
    # ⚠️ 💻 o texto diz "foram atualizados", mas a linha repetida não altera nada

  Scenario: Retirar a planilha escolhida
    Given que o usuário adicionou uma planilha
    When o usuário aciona o ícone de lixeira ao lado do nome da planilha
    Then o sistema exibe: "Planilha removida" com o detalhe "Planilha de Temas removida"
    And o botão "Enviar" volta a ficar desabilitado

  Scenario: Fechar a janela sem enviar
    When o usuário fecha a janela
    Then nenhum tema é alterado

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Enviar sem planilha
    When nenhuma planilha foi adicionada
    Then o botão "Enviar" permanece desabilitado

  Scenario: Planilha sem uma das colunas exigidas
    Given uma planilha que não tem a coluna "Tema"
    When o usuário envia a planilha
    Then o sistema não altera nenhum tema
    And exibe: "Erro ao processar carga de Temas" com o detalhe "Cabeçalho incompleto na carga."

  Scenario: Cabeçalho com outra grafia
    Given uma planilha cuja coluna de tema se chama "Temas", e não "Tema"
    When o usuário envia a planilha
    Then o sistema não altera nenhum tema
    And exibe: "Erro ao processar carga de Temas" com o detalhe "Cabeçalho incompleto na carga."

  Scenario: Arquivo de tipo não aceito
    When o usuário escolhe um arquivo que não é .xlsx nem .xls
    Then o sistema recusa o arquivo e exibe, no próprio campo, o nome do arquivo seguido de ": Tipo de arquivo não permitido" e o detalhe "Tipos permitidos: .xlsx,.xls"

  Scenario: Arquivo acima do tamanho aceito
    When o usuário escolhe uma planilha com mais de 200 MB
    Then o sistema recusa o arquivo e exibe, no próprio campo: "O arquivo selecionado excede o tamanho máximo permitido", com o detalhe que começa por "O tamanho máximo de arquivo permitido é"

  Scenario: Planilha que o navegador não consegue ler
    When a leitura da planilha escolhida falha no navegador
    Then o sistema exibe: "Falha ao ler planilha." com o detalhe "Falha ao ler planilha de Temas."

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Temas de uma carga anterior
    Given que a pessoa "João Lima" tem 3 temas, trazidos por uma carga anterior
    And a nova planilha não tem nenhuma linha de "João Lima"
    When o usuário envia a nova planilha
    Then "João Lima" fica sem nenhum tema
    # ⚠️ 💻 a carga substitui os temas de todas as pessoas, e não só os de quem está na planilha

  Scenario: Duas pessoas com o mesmo CRM
    Given que o cadastro tem duas pessoas com o CRM "100200"
    And a planilha tem uma linha com o "Cód. Contato" "100200"
    When o usuário envia a planilha
    Then o sistema não altera nenhum tema
    And exibe: "Erro ao processar carga de Temas" com o detalhe "Ocorreu um erro inesperado. Contate o suporte."
    # ⚠️ 🔍 a confirmar em execução

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Carregar Temas" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Administração › Pessoas, e o botão "Carga de Temas" não fica ao alcance dele
    # ⚠️ a tela não confere o perfil; ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Planilha ilegível
    Given um arquivo com extensão .xlsx cujo conteúdo não é uma planilha
    When o usuário envia o arquivo
    Then o sistema não altera nenhum tema
    And exibe: "Carga concluída" com o detalhe "."
    # ⚠️ 💻 o servidor responde como sucesso, com as contagens zeradas — suspeita de defeito

  Scenario: Planilha só com o cabeçalho
    Given uma planilha com as colunas exigidas e nenhuma linha de dados
    When o usuário envia a planilha
    Then o sistema apaga os temas de todas as pessoas e não grava nenhum
    And exibe: "Carga concluída" com o detalhe "."
    # ⚠️ 💻 nenhum aviso de que o cadastro ficou sem temas

  Scenario: Falha inesperada durante a carga
    Given que o processamento falha no servidor
    When o usuário envia a planilha
    Then o sistema desfaz o que a carga já tinha feito, e os temas ficam como estavam
    And exibe: "Erro ao processar carga de Temas" com o detalhe "Ocorreu um erro inesperado. Contate o suporte."

  Scenario: Servidor não responde
    Given que o servidor não responde
    When o usuário envia a planilha
    Then o sistema exibe: "Erro ao processar carga de Temas" com o detalhe "Erro ao processar a carga de Temas. Verifique o arquivo e tente novamente."
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| Planilha | externo: Planilha extraída do CRM | entrada do usuário | editável | arquivo | sim | Único campo da janela, sem rótulo: a planilha é escolhida pelo botão "Adicionar" ou arrastada para a área indicada. Formato .xlsx ou .xls, até 200 MB 💻 |
| Cód. Contato | Pessoa | externo: Planilha extraída do CRM | — | texto | sim | Coluna da planilha. Tem de ser igual ao CRM de uma pessoa do cadastro; a linha sem correspondência é desconsiderada 💻 |
| Tema | TemaPessoa | externo: Planilha extraída do CRM | — | texto | sim | Coluna da planilha; nome do tema a que a pessoa se vincula. Célula em branco não é recusada 💻 ⚠️ |

*A obrigatoriedade das colunas `Cód. Contato` e `Tema` refere-se à presença delas no cabeçalho.*

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| Data de Vínculo | Data e hora da carga | Em cada vínculo criado pela carga |

---

## Comportamento de tela

### Onde fica
Janela "Carga de Temas", aberta sobre a tela "Pessoas" pelo botão "Carga de Temas" (Pesquisar Pessoas `PES-CAD-01`). Abaixo do título vem a instrução "A planilha deve conter as colunas Cód. Contato e Tema.". A janela pode ser arrastada, não muda de tamanho e fecha pelo X.

O campo da planilha tem o botão "Adicionar" e a área "Clique em adicionar ou arraste e solte os arquivos aqui...". Escolhida a planilha, a área mostra um botão com o nome do arquivo, com a dica "Download", que baixa a própria planilha, e um ícone de lixeira, com a dica "Excluir", que a retira. O botão "Enviar" fica desabilitado enquanto não houver planilha.

O resumo exibido ao fim da carga é montado com até três trechos, cada um presente só quando a sua contagem é maior que zero, unidos por vírgula e por "e" e terminados por ponto: "{n} temas vinculados" — vínculos criados; "{n} foram atualizados" — linhas que repetem pessoa e tema dentro da planilha, e que na verdade não alteram nada ⚠️; "{n} pessoas não foram encontradas" — linhas cujo `Cód. Contato` não é de nenhuma pessoa. Essa última contagem é de linhas, e não de pessoas: a pessoa ausente que aparece em três linhas conta três 💻. Quando as três contagens são zero, o detalhe é só um ponto ⚠️.

A lista de pessoas não é recarregada ao fim da carga; os temas trazidos são vistos na aba "Relacionamento" da tela de cada pessoa (Editar Pessoa `PES-CAD-03`).

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Ao acionar "Enviar", a janela se fecha e aparece o aviso "Carga em processamento." com o detalhe "Carga de Temas em processamento.". Não há indicador de progresso, e a tela "Pessoas" continua livre para uso |
| Erro de validação | No próprio campo, o arquivo de tipo ou de tamanho não aceito é recusado. Sem planilha, o botão "Enviar" fica desabilitado |
| Erro de servidor | Mensagem "Erro ao processar carga de Temas", com o detalhe que o servidor devolve — "Cabeçalho incompleto na carga." ou "Ocorreu um erro inesperado. Contate o suporte." — ou, sem resposta do servidor, "Erro ao processar a carga de Temas. Verifique o arquivo e tente novamente." |
| Sucesso | Aviso "Carga concluída", com o resumo no detalhe |
| Empty state | Janela recém-aberta: a área de seleção mostra "Clique em adicionar ou arraste e solte os arquivos aqui...", e o botão "Enviar" está desabilitado |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Depois da carga, cada pessoa da planilha mostra, na tela dela, os temas que a planilha traz | Regra 7 · cenário "Carregar temas" |
| SC-02 | Depois da carga, não resta no cadastro nenhum tema que não esteja na planilha | Regra 6 · cenário "Temas de uma carga anterior" |
| SC-03 | Uma planilha sem alguma das colunas exigidas não altera nenhum tema e informa "Cabeçalho incompleto na carga." | Regras 4 e 5 · cenário "Planilha sem uma das colunas exigidas" |
| SC-04 | O resumo ao fim da carga informa quantos temas foram vinculados e quantas linhas ficaram sem pessoa correspondente | Regra 9 · cenário "Planilha com linha de pessoa não cadastrada" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Carregar Temas | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade TemaPessoa

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Janela de carga: seleção da planilha e envio | sistema_mesa_checkin_frontend | `src/app/admin/administracao/acessibilidade/pessoas/pages/pessoas/components/pessoas-carga-tema/pessoas-carga-tema.component.html` (linhas 1–72) e `.ts` (linhas 66–131) | — |
| Botão "Carga de Temas", avisos e resumo da carga | sistema_mesa_checkin_frontend | `src/app/admin/administracao/acessibilidade/pessoas/pages/pessoas/components/pessoas-filter/pessoas-filter.component.html` (linhas 90–95 e 113–119) e `.ts` (linhas 133–162) | — |
| Chamada da carga | sistema_mesa_checkin_frontend | `src/app/admin/administracao/acessibilidade/pessoas/services/pessoa.service.ts` (linhas 52–55) | — |
| Operação `POST /administracao/pessoas/carga/tema` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/PessoaController.java` (linhas 138–142) | — |
| Processamento da planilha | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/TemaPessoaServiceImpl.java` (linhas 41–108) | — |
| Leitura de células e de cabeçalho | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/util/ExcelUtils.java` (linhas 104–148) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

A resposta do servidor traz só três contadores — `countSucesso`, `countErro` e `countExistentes` —, sem erro por linha. A planilha ilegível cai no `catch (IOException)` das linhas 68–70, que só imprime o erro e devolve os contadores zerados com `200`; a exclusão geral (`repository.deleteAll()`, linha 59) fica depois da conferência do cabeçalho e, por isso, não acontece nesse caso nem no de cabeçalho incompleto. O tema repetido só soma em `countExistentes` (linhas 96–99): nada é regravado, embora a tela o apresente como "foram atualizados".

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE003 – Manter Pessoa (funcionalidade "Realizar Carga de Temas" e regra "Carregar Temas") e do código |

---

*Feature Set: Cadastro de Pessoas · Major Feature Set: Pessoas · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
