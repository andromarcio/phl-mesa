<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: ACE-AUT-05
feature_set: ACE-AUT
dominio: ACE
entidade: Usuario
data_model_ref: data-models/acesso-usuarios.md#usuario
endpoints: []
error_codes: []
depende_de: ["ACE-AUT-01", "ACE-AUT-06"]
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

# Alterar Foto de Perfil
> **Nível 3** - Feature Set: Autenticação — Major Feature Set: Acesso e Usuários - `ACE-AUT-05`

## Descrição

Permite que o usuário altere a foto que o identifica no cabeçalho do sistema, escolhendo uma imagem do seu computador; a nova foto passa a aparecer ao lado do nome dele em todas as telas internas.

Pelo documento legado, o usuário aciona a opção Alterar Foto do Perfil, no menu do usuário, escolhe a imagem na janela que se abre e a salva 📄. ⚠️ **Hoje a troca não pode ser feita pela tela**: a opção existe no menu, mas não abre janela nenhuma — a rotina que grava a foto está no código e nada na tela a aciona 💻.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE001 – Efetuar Login v1.0, de 03/10/2025 (documento legado), funcionalidade "Alterar imagem de perfil" ⚠️ sem chave na ferramenta de demandas | Criação | — Alterar a imagem de perfil pela opção "Alterar foto do perfil" do menu suspenso do usuário. ⚠️ O documento e a imagem dele mostram uma janela de troca que a tela atual não tem: no código restam o item de menu e a rotina de gravar, sem ligação entre os dois 💻 |

---

<div class="dev-only">

## Superfície

**Modal** — origem: Consultar Dados do Usuário `ACE-AUT-06` (menu do usuário, no cabeçalho de todas as telas internas), item "Alterar Foto do Perfil"

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a imagem "Alterar imagem de perfil" de GPE001, porque a tela implementada não tem a janela

⚠️ A janela é a superfície que o documento descreve. No código atual só existem o item de menu e as rotinas de selecionar, pré-visualizar e gravar a foto; o trecho de tela que as acionaria não está no cabeçalho.

---

</div>

## Regras de negócio

1. Cada usuário altera só a própria foto de perfil; não há como alterar a de outro usuário por aqui. 💻
2. A foto de perfil é guardada no cadastro corporativo da CNI, junto do usuário; o GPE não a guarda. 💻 → ver [N1 Acesso e Usuários](../README.md): Regras transversais de negócio: 1
3. A nova foto substitui a anterior; não fica histórico das fotos trocadas. 🔍
4. Formato, tamanho e dimensões aceitos para a imagem não estão definidos: o documento não os traz 📄, e a rotina existente no código não confere nenhum deles 💻. ❓

---

## Cenários

```gherkin
Feature: Alterar foto de perfil

  Background:
    Given que o usuário está autenticado no GPE
    And abriu o menu do usuário, no cabeçalho de uma tela interna

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Trocar a foto de perfil, como o documento descreve
    When o usuário aciona "Alterar Foto do Perfil"
    And, na janela "Alterar Imagem do Perfil", escolhe uma imagem em "Selecionar Imagem" e aciona "Salvar Imagem"
    Then o cadastro corporativo guarda a nova foto do usuário
    And o sistema fecha a janela e exibe: "Foto Alterada"
    And a nova foto aparece no cabeçalho, ao lado do nome do usuário
    # 📄 a janela, o título e os rótulos dos botões vêm da imagem "Alterar imagem de perfil" de GPE001
    # ⚠️ 💻 este cenário não pode ser executado hoje: a janela não existe na tela atual. A rotina que grava a foto e a mensagem "Foto Alterada" estão no código, sem nada que as acione

  Scenario: Acionar a opção no sistema atual
    When o usuário aciona "Alterar Foto do Perfil"
    Then nenhuma janela se abre, e a foto continua a mesma
    # ⚠️ 💻 suspeita de defeito ou de funcionalidade retirada pela metade: é o comportamento de hoje

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há validação definida para a imagem
    When o usuário escolhe um arquivo qualquer em "Selecionar Imagem"
    Then nenhuma regra de formato, de tamanho ou de dimensão é aplicada ao arquivo
    # ❓ GPE001 não define o que é aceito; a rotina existente lê o arquivo escolhido sem conferir nada 💻

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Não há conflito com dados existentes
    Given que o usuário já tem uma foto de perfil
    When salva uma nova foto
    Then a nova foto substitui a anterior, sem pergunta
    # 🔍 inferido da rotina existente, que grava por cima

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Não há restrição por perfil para trocar a foto
    Given que o usuário está autenticado, com qualquer perfil
    When abre o menu do usuário
    Then a opção "Alterar Foto do Perfil" aparece para ele

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Falha ao gravar a foto
    Given que o cadastro corporativo recusa a gravação ou não responde
    When o usuário aciona "Salvar Imagem"
    Then a foto continua a mesma
    And o sistema exibe o detalhe enviado pelo cadastro corporativo ou, na falta dele, "Serviço indisponível"
    # 💻 previsto na rotina que hoje não tem acionador; o texto, aqui, não tem ponto final
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| Selecionar Imagem | Usuario | entrada do usuário | editável | arquivo | sim | Rótulo do botão de escolha na imagem de GPE001 📄; corresponde à Foto do usuário. Formato, tamanho e dimensões aceitos não estão definidos ❓. ⚠️ O campo não existe na tela atual 💻 |

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| — | — | Nenhum campo automático identificado. Se o cadastro corporativo registra quem trocou a foto e quando, o código do GPE não mostra ❓ |

---

## Comportamento de tela

### Onde fica
No menu do usuário, que se abre ao clicar na foto ou no nome, no cabeçalho de todas as telas internas. "Alterar Foto do Perfil" é o primeiro item de ação, com o ícone de imagem, acima de "Alterar Senha" e de "Logout".

Pelo documento, o clique abre sobre a tela a janela "Alterar Imagem do Perfil", com a foto atual em um círculo, a instrução "Para trocar a foto do seu perfil click no botão Selecionar Imagem.", os botões "Selecionar Imagem" e "Salvar Imagem" e o ícone de fechar. 📄 ⚠️ A instrução traz "click", grafia que não é português.

⚠️ No sistema atual, o clique não abre nada: a janela, o botão de escolha do arquivo e o botão de salvar não estão na tela. O código guarda as rotinas que leriam o arquivo escolhido, mostrariam a prévia e gravariam a foto no cadastro corporativo, mas nenhum elemento da tela as aciona. 💻 O que funciona hoje é só a exibição da foto no cabeçalho, descrita em Consultar Dados do Usuário `ACE-AUT-06`.

A foto de perfil é a do usuário que opera o sistema. Não é a foto da pessoa convidada para os eventos, que pertence ao cadastro de pessoas.

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | ❓ Não definido: a janela não existe na tela atual, e a rotina que grava não tem indicador de espera 💻 |
| Erro de validação | ❓ Não definido: nenhuma validação da imagem está no documento nem no código |
| Erro de servidor | Previsto na rotina sem acionador 💻: mensagem com o detalhe enviado pelo cadastro corporativo ou, na falta dele, "Serviço indisponível" |
| Sucesso | Previsto na rotina sem acionador 💻: mensagem "Foto Alterada", fechamento da janela e a nova foto no cabeçalho |
| Empty state | Não se aplica — a janela não lista dados |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | O usuário troca a própria foto pela tela, sem depender de terceiros ⚠️ hoje não atendido | Cenários "Trocar a foto de perfil, como o documento descreve" e "Acionar a opção no sistema atual" |
| SC-02 | Depois de salva, a nova foto é a que aparece no cabeçalho de todas as telas internas | Regras 2 e 3 · cenário "Trocar a foto de perfil, como o documento descreve" |
| SC-03 | A falha na gravação mantém a foto anterior e informa o motivo | Cenário "Falha ao gravar a foto" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Alterar Foto de Perfil | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade Usuario

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Item "Alterar Foto do Perfil" do menu do usuário, sem a janela | sistema_mesa_checkin_frontend | `src/app/shared/layout/topbar/topbar.component.html` (linhas 48–53) | — |
| Rotinas de abrir, selecionar, pré-visualizar e gravar a foto — sem acionador na tela | sistema_mesa_checkin_frontend | `src/app/shared/layout/topbar/topbar.component.ts` (linhas 42–93) | — |
| Envio da foto ao serviço corporativo — sem chamador ativo | sistema_mesa_checkin_frontend | `src/app/service/core/auth.service.ts` (linhas 84–88) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. ⚠️ A feature está documentada em GPE001, mas a tela implementada não a oferece; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

O item de menu chama `showModalCrop()`, que só marca `showCrop = true` e reaplica a foto atual; o template do cabeçalho não tem `p-dialog`, `p-fileUpload`, o elemento `#imagemCrop` nem botão que chame `salvarImagem()`, embora `Dialog`, `FileUpload` e `Croppie` estejam importados no componente. `salvarImagem()` chamaria o serviço corporativo com a imagem em base64, no endereço de `urlPesquisaUsuarios` seguido do identificador do usuário e de `/foto`. O servidor do GPE não tem operação de foto de usuário.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE001 – Efetuar Login (funcionalidade "Alterar imagem de perfil") e do código, que hoje não abre a janela de troca |

---

*Feature Set: Autenticação · Major Feature Set: Acesso e Usuários · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
