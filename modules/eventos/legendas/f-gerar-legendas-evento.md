<!-- docqui: 4.0.2 | prompt: PROMPT_CONTAGEM | atualizado: 2026-10-04 -->
---
id: EVT-LEG-07
feature_set: EVT-LEG
dominio: EVT
entidade: EventoPessoaLegenda
data_model_ref: data-models/eventos.md#eventopessoalegenda
endpoints: []
error_codes: []
depende_de: ["EVT-LEG-01", "EVT-LEG-02", "EVT-LEG-03"]
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
  revisada_ate: "PDTIC25148-34"
---

# Gerar Legendas do Evento
> **Nível 3** - Feature Set: Legendas — Major Feature Set: Eventos - `EVT-LEG-07`

## Descrição

Permite que o Administrador gere as legendas dos participantes de um evento: o sistema apaga as legendas atribuídas por regra, avalia as condições de cada bloco da configuração e atribui a legenda a quem as atende, preservando as legendas atribuídas manualmente.

Na tela Configuração de Legendas, o botão Executar pede confirmação e, confirmada, aplica a configuração que está na tela. O mesmo botão existe na janela da simulação. Ao final, o sistema informa quantas legendas foram aplicadas e quantas manuais foram preservadas.

---

## Origem

| Ticket (AIM) | Tipo | Critérios cobertos |
|---|---|---|
| GPE006 – Gerenciar Regras de Legendas v1.0, de 03/10/2025 (documento legado), funcionalidade "Executar Regras" ⚠️ sem chave na ferramenta de demandas | Criação | — Aplicar as regras de legendas configuradas para o evento, atualizando a legenda de cada convidado |
| [`PDTIC25148-34`](../../../analise-impacto/AIM-PDTIC25148-34.md) | Alteração | `CA-20, CA-21, CA-22, CA-23` — confirmar a execução, gerar de novo as legendas do evento a partir dos blocos, das condições e da ordem, preservar as legendas manuais e isolar a configuração por evento. O ticket reformulou o que o documento descreve: a legenda manual passou a ser preservada e a regra deixou de ser ativada ou inativada 💻 |
<!-- trace-verified: PDTIC25148-34 @ f6bae69fe29f -->

---

<div class="dev-only">

## Superfície

**Ação em tela** — origem: Consultar Configuração de Legendas `EVT-LEG-01` (`/regras-legenda/:eventoId`), botão "Executar" da barra de ações; e Simular Aplicação de Legendas `EVT-LEG-06`, botão "Executar" da janela da simulação

**Fidelidade ao protótipo**: n/a · não há protótipo; a referência é a tela implementada e a imagem "Listar Regras de Legendas" de GPE006, que retrata o modelo anterior ⚠️

---

</div>

## Regras de negócio

1. A geração alcança somente o evento da configuração: as legendas dos participantes de outros eventos e o cadastro das pessoas não são alterados.
2. A geração aplica a configuração como está no momento do acionamento e a grava antes de avaliar, com as mesmas exigências de qualquer gravação da configuração. 💻 → ver Consultar Configuração de Legendas `EVT-LEG-01`: regra 7
3. Antes de avaliar, todas as legendas do evento que não são manuais são apagadas — as de todos os blocos, inclusive as de legendas que já saíram da configuração. 💻 ⚠️ GPE006 diz, na imagem do documento, que "A execução REMOVE TODAS as legendas existentes antes de aplicar as novas regras" 📄; hoje as manuais ficam.
4. A legenda manual não é apagada nem recalculada. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 10
5. Entram na avaliação todos os participantes do evento, qualquer que seja a situação de convite, de confirmação ou de check-in. 💻 ⚠️ GPE006 fala em atualizar a legenda "de cada convidado do respectivo evento" 📄 e não diz se quem não confirmou presença deve receber legenda.
6. Os blocos são avaliados um a um, na ordem dos seus números. 💻
7. Só a condição completa — com campo, operador e valor preenchidos — entra na avaliação; a incompleta é desconsiderada, como se não existisse. 💻 ⚠️ GPE006 trata Campo, Operador e Valor como obrigatórios 📄 e, no lugar disso, diz que "São aplicadas apenas as regras que estejam ativas".
8. O bloco sem nenhuma condição completa é ignorado: não atribui legenda a ninguém e entra na relação de blocos ignorados. O mesmo vale para o bloco cujas condições completas se resumem a listas sem nenhum valor aproveitável. 💻
9. As condições de um bloco são combinadas da esquerda para a direita, na ordem em que estão, sem precedência do E sobre o OU: "A OU B E C" vale como "(A OU B) E C". 💻 ⚠️ Não é a convenção usual, em que o E é resolvido antes do OU; GPE006 só exemplifica blocos de uma e de duas condições 📄 e não diz como combinar três ou mais.
10. O conectivo que liga uma condição ao que veio antes é o da própria condição; na falta dele, vale E. A primeira condição completa do bloco entra sem conectivo, ainda que tenha um. 💻
11. Com o operador Igual a, a condição é atendida quando o dado da pessoa é igual ao valor. Se o valor tem vírgula, Igual a se comporta como Em (lista). 💻 ⚠️ Por isso não há como exigir igualdade com um texto que contenha vírgula.
12. Com o operador Contém, a condição é atendida quando o dado da pessoa contém o valor, em qualquer posição.
13. Com o operador Em (lista), o valor é separado nas vírgulas, cada item perde os espaços das pontas e os itens vazios são descartados; a condição é atendida quando o dado da pessoa é igual a um dos itens. 💻
14. Com o operador Diferente de, a regra muda conforme o campo. Para os dois campos de valor único (Cargo e Nome fantasia), a condição é atendida quando o dado da pessoa é diferente do valor; a pessoa com o dado em branco não atende 🔍. Para os três campos de que a pessoa pode ter vários (Grupo de trabalho, Papel desempenhado e Tema), a condição é atendida quando a pessoa não tem nenhum registro com aquele valor — o que inclui quem não tem nenhum grupo de trabalho ou nenhum tema. 💻 ⚠️ As duas metades da regra tratam de modo oposto a pessoa sem o dado.
15. Para Grupo de trabalho, Papel desempenhado e Tema, com os operadores Igual a, Contém e Em (lista), basta que um dos registros da pessoa atenda à condição. 💻
16. Cada condição sobre grupo de trabalho, papel desempenhado ou tema é avaliada sozinha: a condição sobre o grupo e a condição sobre o papel podem ser atendidas por vínculos diferentes da mesma pessoa. 💻 ⚠️ Parece defeito: "Grupo de trabalho Igual a Inovação E Papel desempenhado Igual a Coordenador" alcança quem é coordenador de outro grupo e apenas integrante do grupo Inovação.
17. O valor é comparado sem os espaços das pontas. ❓ Nenhuma fonte diz se a comparação diferencia maiúsculas de minúsculas e letras com acento de letras sem acento: o código não trata disso e o resultado depende de como os dados estão guardados.
18. Os blocos não se excluem: o participante recebe uma legenda para cada bloco cujas condições atende. 💻 ⚠️ GPE006 diz, na imagem do documento, que "As regras são aplicadas na ordem de prioridade das legendas" 📄, e o ticket fala em "ordem de prioridade"; nos dois casos a leitura possível é a de uma só legenda por pessoa. Hoje a ordem não decide quem recebe: decide só qual legenda aparece.
19. Quando o participante tem mais de uma legenda, a que aparece é a prioritária. → ver [N1 Eventos](../README.md): Regras transversais de negócio: 9
20. O participante que já tem a legenda de um bloco atribuída manualmente não a recebe de novo por aquele bloco nem entra na quantidade dele; continua podendo receber as legendas dos demais blocos. 💻
21. Cada legenda gerada é registrada como não manual, com a data e a hora da geração. 💻
22. O resultado da geração traz dois totais: as legendas aplicadas, que são a soma, bloco a bloco, dos participantes que receberam a legenda — quem atende a dois blocos conta duas vezes —, e as manuais preservadas, que são todas as legendas manuais do evento, inclusive as de legendas que não estão na configuração. 💻
23. A geração com a configuração vazia, ou só com blocos ignorados, apaga as legendas não manuais do evento e não atribui nenhuma. 💻 ⚠️ É o que resta do "Resetar Regras" de GPE006, que excluía de uma vez todas as regras do evento 📄 e não existe mais: hoje o caminho é remover os blocos e gerar.
24. A geração é integral: se a gravação da configuração ou a avaliação de qualquer bloco falha, nem a configuração nem as legendas dos participantes mudam. 💻

---

## Cenários

```gherkin
Feature: Gerar legendas do evento

  Background:
    Given que o usuário está autenticado no GPE
    And está na tela Configuração de Legendas de um evento

  # ── Caminho feliz ──────────────────────────────────────────────

  Scenario: Gerar as legendas do evento
    Given que a configuração tem o bloco 1 "Diretores da CNI" com a condição Campo "Cargo", Operador "Contém", Valor "Diretor"
    And três participantes do evento têm cargo que contém "Diretor"
    And um participante tem a legenda "Anfitrião" atribuída manualmente
    When o usuário aciona "Executar"
    And confirma a pergunta "As associações de legenda deste evento serão recriadas a partir dos blocos configurados. As legendas atribuídas manualmente serão preservadas. Outros eventos não serão afetados. Deseja continuar?"
    Then o sistema grava a configuração, apaga as legendas não manuais do evento e atribui "Diretores da CNI" aos três participantes
    And exibe: "Legendas aplicadas" com o detalhe "3 legendas aplicadas, 1 manuais preservadas."
    # ⚠️ o texto usa sempre o plural: com uma legenda sai "1 legendas aplicadas" e "1 manuais preservadas" 💻

  Scenario: Participante que atende a dois blocos
    Given que "Maria Souza" atende às condições do bloco 1 "Comitê estratégico" e do bloco 3 "Diretores da CNI"
    When o usuário aciona "Executar" e confirma
    Then "Maria Souza" recebe as duas legendas
    And na lista de participantes e no mapa de assentos ela aparece com "Comitê estratégico", a do bloco de menor número
    # ⚠️ GPE006 sugere uma só legenda por pessoa, pela ordem de prioridade; ver a regra 18

  Scenario: Legenda manual preservada
    Given que "João Lima" tem a legenda "Anfitrião" atribuída manualmente
    And atende às condições do bloco "Diretores da CNI"
    When o usuário aciona "Executar" e confirma
    Then "João Lima" continua com "Anfitrião" como legenda manual e passa a ter também "Diretores da CNI"
    And continua aparecendo com "Anfitrião", porque a legenda manual é a prioritária

  Scenario: Participante que já tem a legenda do bloco como manual
    Given que "João Lima" tem a legenda "Diretores da CNI" atribuída manualmente
    And atende às condições do bloco "Diretores da CNI"
    When o usuário aciona "Executar" e confirma
    Then "João Lima" fica com uma só legenda "Diretores da CNI", a manual
    And não é contado entre as legendas aplicadas

  Scenario: Gerar a partir da simulação
    Given que a janela "Simulação de aplicação de legendas" está aberta
    When o usuário aciona "Executar" na janela
    Then a janela se fecha e o sistema faz a mesma pergunta de confirmação da tela

  Scenario: Desistir da geração
    When o usuário aciona "Executar"
    And escolhe "Cancelar" na pergunta de confirmação
    Then o sistema mantém a configuração e as legendas dos participantes como estavam

  # ── Erros de validação ─────────────────────────────────────────

  Scenario: Não há dado a validar
    When o usuário aciona "Executar"
    Then o sistema pede apenas a confirmação, sem solicitar nenhum dado

  Scenario: Bloco sem condição completa
    Given que o bloco "Assento livre" não tem nenhuma condição com campo, operador e valor preenchidos
    When o usuário aciona "Executar" e confirma
    Then o sistema gera as legendas dos demais blocos e não atribui "Assento livre" a ninguém
    And o resultado informa só os totais, sem dizer que o bloco foi ignorado
    # ⚠️ a relação de blocos ignorados só aparece na simulação 💻

  # ── Conflitos com dados existentes ────────────────────────────

  Scenario: Bloco excluído do catálogo depois de aberta a tela
    Given que um bloco da configuração foi excluído do catálogo enquanto a tela estava aberta
    When o usuário aciona "Executar" e confirma
    Then o sistema mantém a configuração e as legendas como estavam
    And exibe o erro "Erro Interno" com o detalhe "Bloco de legenda inexistente: " seguido do número interno do bloco
    # 🔍 caminho deduzido do código; não foi executado

  Scenario: Evento que não existe mais
    Given que o evento da tela não existe
    When o usuário aciona "Executar" e confirma
    Then o sistema exibe o erro "Erro Interno" com o detalhe "Evento não encontrado."

  # ── Restrições de acesso ───────────────────────────────────────

  Scenario: Usuário sem acesso a esta feature
    Given que o perfil do usuário não tem acesso a "Gerar Legendas do Evento" na matriz do N2
    When o usuário entra no sistema
    Then o menu não traz Eventos, de onde se chega à Configuração de Legendas, e a ação não fica ao alcance dele
    # ⚠️ a tela não confere o perfil; ver a nota da matriz no N2

  # ── Estados especiais ──────────────────────────────────────────

  Scenario: Configuração vazia
    Given que o evento não tem nenhum bloco configurado
    And os participantes têm legendas de uma geração anterior
    When o usuário aciona "Executar" e confirma
    Then o sistema apaga as legendas não manuais do evento e não atribui nenhuma
    And exibe: "Legendas aplicadas" com o detalhe "0 legendas aplicadas, 2 manuais preservadas."
    # ⚠️ é o efeito que GPE006 dava a "Resetar Regras", que não existe mais; ver a regra 23

  Scenario: Evento sem participantes
    Given que o evento não tem nenhum participante
    When o usuário aciona "Executar" e confirma
    Then o sistema grava a configuração
    And exibe: "Legendas aplicadas" com o detalhe "0 legendas aplicadas, 0 manuais preservadas."

  Scenario: Falha durante a geração
    Given que a geração falha por motivo inesperado
    When o usuário aciona "Executar" e confirma
    Then o sistema mantém a configuração e as legendas como estavam
    And exibe o erro "Erro Interno" com o detalhe "Ocorreu um erro inesperado. Contate o suporte."

  Scenario: Servidor sem resposta
    Given que o servidor não responde
    When o usuário aciona "Executar" e confirma
    Then o sistema exibe o erro "Erro" com o detalhe "Falha de comunicação com o servidor."
```

---

## Campos

| Label PO | Entidade | Preenchimento | Edição | Tipo | Obrigatório | Validação |
|---|---|---|---|---|---|---|
| — | EventoPessoaLegenda | — | — | — | — | A ação não tem campos: aplica a configuração que está na tela e pede só a confirmação |

---

## Campos automáticos

| Label PO | Valor | Quando |
|---|---|---|
| Manual | Não | Em cada legenda atribuída pela geração |
| Data de atribuição | Data e hora da geração, a mesma para todas as legendas daquela geração | Em cada legenda atribuída pela geração |
| Nº | Posição do bloco na configuração (1, 2, 3…) | Na gravação da configuração que antecede a avaliação |

---

## Dados lidos e gravados

| Entidade | Papel | Por que a feature a toca |
|---|---|---|
| Evento | lê | Confirma que o evento existe antes de gravar a configuração (regra 2) |
| EventoPessoa | lê | Os participantes do evento, todos, são os avaliados (regra 5) |
| Pessoa | lê | Cargo e Nome fantasia entram nas condições; o nome compõe o resultado de cada bloco (regras 11 a 14) |
| GrupoTrabalhoPessoa | lê | Grupo de trabalho e Papel desempenhado entram nas condições (regras 14 a 16) |
| TemaPessoa | lê | Tema entra nas condições (regras 14 a 16) |
| Legenda | lê | Confirma que cada bloco existe no catálogo e dá o nome e a cor de cada legenda (regra 2) |
| EventoLegenda | lê e grava | A configuração é gravada antes da avaliação, e os blocos são avaliados na ordem dos números (regras 2 e 6) |
| EventoLegendaCondicao | lê e grava | As condições são gravadas com a configuração e decidem quem recebe a legenda (regras 2 e 7 a 16) |

---

## Comportamento de tela

### Onde fica
Na tela Configuração de Legendas, o botão "Executar" fica na barra de ações, à direita, ao lado de "Simular". Na janela "Simulação de aplicação de legendas" há outro botão "Executar", que fecha a janela e leva à mesma confirmação. A confirmação é uma caixa com o título "Executar aplicação de legendas", a pergunta "As associações de legenda deste evento serão recriadas a partir dos blocos configurados. As legendas atribuídas manualmente serão preservadas. Outros eventos não serão afetados. Deseja continuar?" e os botões "Executar" e "Cancelar". ⚠️ Em GPE006 o comando se chama "Executar Regras" 📄; na tela, "Executar" 💻.

O botão fica disponível mesmo com a configuração vazia. Depois da geração a tela não muda: os cartões dos blocos continuam como estavam e o resultado aparece só na mensagem. Para ver quem recebeu cada legenda é preciso simular antes ou consultar a lista de participantes do evento.

### Estados da tela

| Estado | Comportamento |
|---|---|
| Loading | Não há indicador de processamento, e o botão "Executar" continua habilitado enquanto a geração acontece 💻 ⚠️ nada impede um segundo acionamento antes do fim do primeiro |
| Erro de validação | Não se aplica — a ação não tem campos |
| Erro de servidor | Erro "Erro Interno" com o detalhe enviado pelo servidor: "Evento não encontrado.", "Bloco de legenda inexistente: " seguido do número interno do bloco, "A configuração tem blocos de legenda repetidos." ou, em falha inesperada, "Ocorreu um erro inesperado. Contate o suporte."; sem resposta do servidor, erro "Erro" com o detalhe "Falha de comunicação com o servidor." ⚠️ O título é "Erro Interno" mesmo quando o detalhe é uma regra de negócio |
| Sucesso | Mensagem "Legendas aplicadas" com o detalhe "{n} legendas aplicadas, {m} manuais preservadas."; a tela permanece como estava. ⚠️ Os blocos ignorados não são informados, e o texto usa o plural mesmo com uma só legenda |
| Empty state | Com a configuração vazia a geração é aceita: apaga as legendas não manuais do evento e informa "0 legendas aplicadas" |

---

## Critérios de sucesso

| # | Critério mensurável | Origem |
|---|---|---|
| SC-01 | Depois da geração, todo participante que atende às condições de um bloco tem a legenda desse bloco, e nenhum participante mantém legenda não manual de geração anterior | Regras 3, 5 e 18 · cenário "Gerar as legendas do evento" |
| SC-02 | Nenhuma legenda manual é apagada ou alterada pela geração | Regra 4 · cenário "Legenda manual preservada" |
| SC-03 | A geração de um evento não altera as legendas dos participantes de nenhum outro evento | Regra 1 |
| SC-04 | Nenhuma geração acontece sem a confirmação do usuário | Cenário "Desistir da geração" |

---

## Métricas de tamanho

| Função de Transação | Papel | Tipo | ALR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Gerar Legendas do Evento | principal | EE | 3 | 2 | Média | 4 | 2026-10-04 |

### Memória de cálculo

**Gerar Legendas do Evento** — EE · ALR 3 · DER 2 · Média · 4 PF

```json
{"pe": "Gerar Legendas do Evento",
 "alr": ["Evento", "Pessoa", "Legenda"],
 "der": ["Mensagem", "Ação"],
 "nao_contados": "Manual, Data de atribuição e Nº são preenchidos pelo sistema e não cruzam a fronteira. Os totais de legendas aplicadas e de manuais preservadas vêm dentro da mensagem de sucesso e contam como a Mensagem."}
```

Por que cada ALR:
1. `Evento` — grava a configuração, apaga as legendas não manuais dos participantes e grava as novas
2. `Pessoa` — lê o cargo, o nome fantasia, os grupos de trabalho, os papéis e os temas que as condições avaliam
3. `Legenda` — confere que cada bloco existe no catálogo

Classificação: EE — a intenção primária é manter o arquivo lógico Evento, nas legendas dos participantes, com as formas 4, 5, 6, 7 e 12.

**Total: 4 PF**

---

<div class="dev-only">

## Mapeamento de campos
→ ver DATA-MODEL.md: Entidade EventoPessoaLegenda

---

## Implementação

| Item | Repositório | Caminho | Branch/Tag |
|---|---|---|---|
| Botão "Executar", confirmação e mensagem de resultado | sistema_mesa_checkin_frontend | `src/app/admin/administracao/legendas/pages/configuracao-legendas-evento/configuracao-legendas-evento.component.ts` (linhas 269–291 e 338–341) e `.html` (linhas 38–39) | — |
| Serviço de execução | sistema_mesa_checkin_frontend | `src/app/admin/administracao/evento/services/evento-legenda.service.ts` (linhas 40–42) | — |
| Operação `POST /administracao/eventos/{id}/legendas/executar` | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/controller/EventoController.java` (linhas 278–282) | — |
| Gravação da configuração, limpeza e avaliação dos blocos | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/service/impl/LegendaEventoServiceImpl.java` (linhas 212–220 e 229–419) | — |
| Exclusão das legendas não manuais do evento | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/repository/EventoPessoaLegendaRepository.java` (linhas 24–32) | — |
| Escolha da legenda prioritária na leitura | sistema_mesa_checkin_backend | `src/main/java/br/com/cni/apimesacheckin/repository/impl/EventoPessoaRepositoryImpl.java` (linhas 44–68) | — |

**Status**: definido pela **esteira de checkpoints** no front-matter (`estado` + `gates`) no topo deste arquivo. A feature já está implementada no código; o estado `rascunho` diz respeito a esta especificação, que ainda não foi validada pelo PO.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-10-04 | Claude (apf-cpm) | Contagem | Primeira contagem, pelo `PROMPT_CONTAGEM`: 4 PF — Gerar Legendas do Evento (EE Média, 4 PF). Confirmada em 2026-10-04 e espelhada em `global/CONTAGEM-PF.md` |
| 2026-10-04 | Claude (analise-impacto) | Origem atualizada | Elo com a AIM do ticket `PDTIC25148-34`, aberta na entrega: o ticket ganha linha própria na Origem, como Alteração, com os critérios CA-20 a CA-23; regras, campos e cenários inalterados |
| 2026-09-30 | Claude (analista-requisitos) | Feature criada | Engenharia reversa do documento legado GPE006 – Gerenciar Regras de Legendas (funcionalidade "Executar Regras"), do ticket `PDTIC25148-34` do Jira e do código |

---

*Feature Set: Legendas · Major Feature Set: Eventos · Última revisão: —*

*Links: [N2 do Feature Set](./README.md) · [N1 do domínio](../README.md) · [INDEX geral](../../INDEX.md)*
