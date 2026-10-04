<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
---
id: EVT-PAR-15
feature_set: EVT-PAR
dominio: EVT
entidade: EventoPessoa
data_model_ref: data-models/eventos.md#eventopessoa
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

# Exportar Mapa de Assentos
> **Nível 3** - Feature Set: Participantes — Major Feature Set: Eventos - `EVT-PAR-15`

## Descrição

Permite que o Administrador exporte o mapa de assentos do evento, inteiro ou só com a mesa principal, em um arquivo PDF ou de imagem que retrata os assentos e seus ocupantes como estão no mapa naquele momento.

Na seção "Exportações", abaixo do mapa de assentos, há as linhas "Mapa Completo:" e "Mesa do Presidente:", cada uma com os botões "PDF" e "PNG". Um clique gera o arquivo e o baixa para o computador do usuário.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| Código-fonte (engenharia reversa de 2026-09-30) — a funcionalidade não consta nos documentos legados ⚠️ | Criação | — Gerar o arquivo do mapa completo ou da mesa principal, em PDF ou imagem. A seção "Exportações" aparece na imagem "Consultar Mapa de Assentos — Perfil Administrador" de GPE005 – Gerenciar Participante v1.1, mas o texto do documento não a descreve nem a inclui na tabela de permissões 📄. Ticket do Jira relacionado pelo título, concluído e sem AIM aberta 🔍: `PDTIC25148-27` (bug "Exportação da Mesa") |

---

<div class="dev-only">

## Superfície

**Ação em tela** — origem: Consultar Mapa de Assentos `EVT-PAR-07` (`/evento-pessoa/:id`, visão Mapa de Assentos, versão do Administrador), botões "PDF" e "PNG" das linhas "Mapa Completo:" e "Mesa do Presidente:" da seção "Exportações"

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Consultar Mapa de Assentos — Perfil Administrador" de GPE005

---

</div>

## Regras de negócio

1. A exportação retrata o mapa como ele está aberto no momento, com os assentos e ocupantes que o Administrador vê — inclusive as atribuições ainda não gravadas. Ela não consulta o servidor. 💻
2. Há duas saídas. O Mapa Completo traz todos os setores, de A a H, e um resumo do evento com a contagem de participantes. A Mesa do Presidente traz somente a mesa principal — setores A, B, C e D — e a relação das legendas. 💻
3. Cada saída pode ser gerada em PDF, sempre em página A4, ou em imagem. 💻
4. O arquivo de imagem é oferecido como PNG, mas é gerado no formato JPEG e baixado com a extensão de PNG. 💻 ⚠️ Suspeita de defeito: o conteúdo do arquivo não corresponde ao formato que o nome indica.
5. O nome do arquivo é formado pelo tipo da saída, pelo nome do evento e pela data e hora da geração. 💻
6. No resumo do Mapa Completo, o total de participantes conta só quem faz parte do mapa — os confirmados e os que fizeram check-in —, e não todos os convidados do evento. 💻 → ver Consultar Mapa de Assentos `EVT-PAR-07`
7. A exportação nada grava, e o sistema não guarda registro de quem exportou nem de quando. 💻

---

## Cenários

```gherkin
Feature: Exportar mapa de assentos

  Background:
    Given que o usuário está autenticado no GPE
    And está no mapa de assentos de um evento, na versão do Administrador

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Exportar o mapa completo em PDF
    Given que o evento se chama "Reunião do Comitê" e são 14h05 de 30/09/2026
    When o usuário aciona "PDF" na linha "Mapa Completo:"
    Then o sistema exibe: "Exportação" com o detalhe "Preparando exportação do mapa completo..."
    And baixa o arquivo "Mapa_Mesa_Completo_Reunião do Comitê_30092026_1405.pdf", em página A4
    And o arquivo traz todos os setores do mapa e, ao lado, o nome do evento, a data, o local e as estatísticas
    And o sistema exibe: "Sucesso" com o detalhe "Mapa completo exportado em PDF com sucesso!"

  Scenario: Exportar o mapa completo em imagem
    When o usuário aciona "PNG" na linha "Mapa Completo:"
    Then o sistema baixa um arquivo de imagem com o mesmo conteúdo, de nome terminado em ".png"
    And exibe: "Sucesso" com o detalhe "Mapa completo exportado em PNG com sucesso!"
    # ⚠️ o arquivo é gerado em formato JPEG, embora o nome termine em ".png" 💻

  Scenario: Exportar a mesa do presidente em PDF
    When o usuário aciona "PDF" na linha "Mesa do Presidente:"
    Then o sistema exibe: "Exportação" com o detalhe "Preparando exportação para o presidente..."
    And baixa o arquivo "Mesa_Presidente_Reunião do Comitê_30092026_1405.pdf", em página A4 em pé
    And o arquivo traz só a mesa principal, com os setores A, B, C e D, e ao lado a relação das legendas
    And o sistema exibe: "Sucesso" com o detalhe "Mesa do presidente exportada em PDF com sucesso!"

  Scenario: Exportar a mesa do presidente em imagem
    When o usuário aciona "PNG" na linha "Mesa do Presidente:"
    Then o sistema baixa um arquivo de imagem com o mesmo conteúdo, de nome terminado em ".png"
    And exibe: "Sucesso" com o detalhe "Mesa do presidente exportada em PNG com sucesso!"
    # ⚠️ mesma divergência de formato do mapa completo 💻

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há dado a validar
    When o usuário aciona qualquer um dos botões da seção "Exportações"
    Then o sistema gera o arquivo sem solicitar nenhum dado nem confirmação

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Mapa com alteração ainda não gravada
    Given que o usuário atribuiu um assento e o mapa ainda não foi gravado
    When ele exporta o mapa
    Then o arquivo já traz a pessoa no assento novo, que os demais usuários ainda não veem
    # 🔍 consequência da regra 1: o arquivo pode divergir do mapa gravado

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Exportar Mapa de Assentos" na matriz do N2
    When o usuário abre o mapa de assentos
    Then a tela não traz a seção "Exportações"
    # ⚠️ a exportação só existe no mapa do Administrador; não há o que o servidor conferir, pois ela é feita no navegador

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Falha ao gerar o mapa completo
    Given que a geração do arquivo falha
    When o usuário aciona "PDF" ou "PNG" na linha "Mapa Completo:"
    Then o sistema exibe: "Erro" com o detalhe "Erro ao exportar o mapa. Tente novamente."

  Scenario: Falha ao gerar a mesa do presidente
    Given que a geração do arquivo falha
    When o usuário aciona "PDF" ou "PNG" na linha "Mesa do Presidente:"
    Then o sistema exibe: "Erro" com o detalhe "Erro ao exportar a mesa do presidente. Tente novamente."

  Scenario: Exportar o mapa sem ninguém sentado
    Given que nenhum participante está sentado
    When o usuário exporta o mapa completo
    Then o arquivo traz todos os assentos vazios, com as suas identificações, e "Pessoas Alocadas: 0" nas estatísticas

  Scenario: Exportar com o desenho ampliado ou reduzido
    Given que o usuário alterou o tamanho do desenho pelos controles de zoom
    When ele exporta o mapa completo
    Then o arquivo traz o mapa no tamanho normal, sem o zoom e sem os botões "×" dos assentos
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| "Mapa Completo:" — botões "PDF" e "PNG" | dado de código | entrada do usuário | editável | lista de opções | sim | A escolha do botão define a saída e o formato; não há outro dado a informar |
| "Mesa do Presidente:" — botões "PDF" e "PNG" | dado de código | entrada do usuário | editável | lista de opções | sim | A escolha do botão define a saída e o formato; não há outro dado a informar |

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| — | — | Nenhum campo é gravado: a exportação só lê o mapa aberto |

---

## Dados lidos e gravados

| Entidade | Papel | Por que a feature a toca |
|---|---|---|
| EventoPessoa | lê | Os participantes sentados e os disponíveis, com o check-in de cada um (regras 1 e 6) |
| CadeiraMesa | lê | Os assentos desenhados, com as suas identificações (regra 2) |
| Pessoa | lê | O nome e a organização mostrados em cada assento ocupado |
| Evento | lê | O nome, a data e o local do evento, no arquivo e no nome do arquivo (regras 2 e 5) |
| Legenda | lê | A cor de cada assento e a relação de legendas da Mesa do Presidente (regra 2) |

---

## Comportamento de tela

### Onde fica
No mapa de assentos do Administrador, no fim da página, abaixo do quadro "Legenda das Categorias", a seção "Exportações", com as linhas "Mapa Completo:" e "Mesa do Presidente:". Cada linha tem o botão "PDF" e o botão "PNG", com as dicas "Exportar mapa completo em PDF", "Exportar mapa completo em PNG", "Exportar mesa do presidente em PDF" e "Exportar mesa do presidente em PNG". A seção não existe no mapa da Secretaria Mesa. 💻

O arquivo é montado no próprio navegador, a partir do desenho que está na tela, e baixado em seguida; não há tela de prévia nem opção de impressão direta. 💻

### O que cada arquivo traz

| Saída | Conteúdo | Página do PDF | Nome do arquivo |
|---|---|---|---|
| Mapa Completo | O desenho de todos os setores, sem o zoom e sem os botões "×"; ao lado, um quadro com o nome do evento, a data por extenso com o dia da semana, "Local: {local}", o título "Estatísticas" com "• Pessoas Alocadas: {n}", "• Pessoas Disponíveis: {n}" e "• Total de Participantes: {n}", e "Gerado em: {data} às {hora}" | A4, deitada ou em pé conforme a proporção do desenho | "Mapa_Mesa_Completo_{nome do evento}_{dia, mês e ano}_{hora e minuto}", com final ".pdf" ou ".png" |
| Mesa do Presidente | O nome do evento e "Mesa Principal - {data do evento}"; o desenho da mesa principal, com os setores A, B, C e D; ao lado, o título "Legenda" com todas as legendas do quadro do mapa, sem as quantidades, e o título "Status" com "Check-in realizado" e "Check-in pendente"; no rodapé, "Gerado automaticamente em {data e hora}" | A4, sempre em pé | "Mesa_Presidente_{nome do evento}_{dia, mês e ano}_{hora e minuto}", com final ".pdf" ou ".png" |

⚠️ O Mapa Completo não traz o quadro de legendas, de modo que as cores dos assentos ficam sem explicação no arquivo. 💻 ⚠️ A situação de quem ainda não fez check-in aparece no arquivo como "Check-in pendente", enquanto a tela diz "Check in não identificado". 💻 ❓ O nome do evento entra no nome do arquivo como está cadastrado; nenhuma fonte diz o que acontece quando ele tem caracteres que o sistema operacional não aceita em nome de arquivo.

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Mensagem "Exportação" com o detalhe "Preparando exportação do mapa completo..." ou "Preparando exportação para o presidente..."; a tela não é bloqueada |
| Erro de validação | Não se aplica — não há campos a preencher |
| Erro de servidor | Não se aplica — a exportação não consulta o servidor. Falha na geração do arquivo: "Erro" com o detalhe "Erro ao exportar o mapa. Tente novamente." ou "Erro ao exportar a mesa do presidente. Tente novamente." |
| Sucesso | O arquivo é baixado e aparece "Sucesso" com o detalhe "Mapa completo exportado em PDF com sucesso!", "Mapa completo exportado em PNG com sucesso!", "Mesa do presidente exportada em PDF com sucesso!" ou "Mesa do presidente exportada em PNG com sucesso!" |
| Empty state | Mapa sem ninguém sentado: o arquivo é gerado com todos os assentos vazios |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | O arquivo do Mapa Completo traz todos os setores do mapa, com os mesmos ocupantes que a tela mostrava no momento da exportação | Regras 1 e 2 · cenário "Exportar o mapa completo em PDF" |
| SC-02 | O arquivo da Mesa do Presidente traz somente os setores A, B, C e D | Regra 2 · cenário "Exportar a mesa do presidente em PDF" |
| SC-03 | O arquivo baixado tem o formato indicado pelo botão acionado ⚠️ hoje não atendido no botão "PNG" | Regra 4 · cenário "Exportar o mapa completo em imagem" |

---

## Métricas de tamanho

> ❓ Ainda não contada. A contagem nasce depois que o PO validar este N3, pela opção **CT** (`PROMPT_CONTAGEM`). A feature consta em `global/CONTAGEM-PF.md` → *Pendências de contagem*.

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Exportar Mapa de Assentos | — | — | — | — | — | — | — |

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade EventoPessoa

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Seção "Exportações" e botões | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/components/mesa/components/retangular/retangular.component.html` (linhas 446–471); formato invertido em `../retangular-invertido/retangular-invertido.component.html` (linhas 432–456) | — |
| Geração do arquivo, PDF, imagem e nome do arquivo | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/components/mesa/components/retangular/retangular.component.ts` (linhas 1914–2114) | — |
| Conteúdo do Mapa Completo e da Mesa do Presidente | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento-pessoa/evento-pessoa/components/mesa/components/retangular/retangular.component.ts` (linhas 2119–2268, 2274–2526); o formato invertido repete o código em `../retangular-invertido/retangular-invertido.component.ts` (a partir da linha 1901) | — |
| Operação do servidor | sistema_mesa_checkin_backend | — não há: o arquivo é gerado no navegador, com as bibliotecas `html2canvas` e `jsPDF` | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

A imagem é obtida com `canvas.toDataURL('image/jpeg', …)` — qualidade 85% no Mapa Completo e 90% na Mesa do Presidente — e gravada por `baixarPNG` com a extensão `.png`. O mesmo código de exportação existe, sem acionador na tela, no componente do mapa da Secretaria Mesa em formato invertido.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do código; a funcionalidade não consta no texto dos documentos legados, só na imagem da tela do Administrador em GPE005 – Gerenciar Participante |

---

*Feature Set: Participantes · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
