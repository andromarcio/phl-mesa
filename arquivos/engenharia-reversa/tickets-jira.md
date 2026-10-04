# Tickets do Jira — projeto PDTIC25148 "Solução para montagem e organização de mesas de reunião"

Consultados em 2026-09-30. NÃO há AIM aberta para nenhum deles nesta instância.

## Lista (chave | tipo | status | criado | resumo)

PDTIC25148-1 | Tarefa | Done | 2025-08-18 | Cadastro de Usuário
PDTIC25148-7 | Story | Done | 2025-08-18 | Cargas do evento
PDTIC25148-8 | Story | Done | 2025-08-18 | Carga de GT, Tema e Histórico de participações
PDTIC25148-10 | Tarefa | Done | 2025-08-21 | Cadastrar eventos
PDTIC25148-11 | Tarefa | Done | 2025-08-21 | Cadastrar pessoas
PDTIC25148-13 | Tarefa | To Do | 2025-08-22 | Visualizar dados da empresa
PDTIC25148-14 | Tarefa | Done | 2025-08-22 | Check-in
PDTIC25148-15 | Tarefa | Done | 2025-09-08 | Cadastro de Pessoas - No dia do evento
PDTIC25148-16 | Tarefa | Done | 2025-09-08 | Mapa de mesa
PDTIC25148-17 | Tarefa | Done | 2025-09-08 | Definir uma página de login para aplicação
PDTIC25148-18 | Tarefa | Done | 2025-09-08 | Classificar pessoas
PDTIC25148-20 | Tarefa | Done | 2025-09-29 | Pesquisa de participantes
PDTIC25148-21 | Tarefa | To Do | 2025-09-29 | Gerar um retrato dos dados dos participantes para um evento específico
PDTIC25148-22 | Bug | Done | 2025-09-30 | Cadastro de Pessoas - Ajustes
PDTIC25148-23 | Bug | Done | 2025-09-30 | Cadastro de usuários - Ajustes
PDTIC25148-24 | Tarefa | To Do | 2025-09-30 | Critérios por evento
PDTIC25148-25 | Tarefa | Done | 2025-09-30 | Responsivo - Ajustes
PDTIC25148-26 | Tarefa | To Do | 2025-09-30 | Construtor de mesa
PDTIC25148-27 | Bug | Done | 2025-09-30 | Exportação da Mesa
PDTIC25148-28 | Tarefa | Done | 2025-09-30 | Mapa de mesa - melhorias
PDTIC25148-29 | Bug | Done | 2025-10-06 | Corrigir o menu no Mobile (Celular/Tablet)
PDTIC25148-30 | Tarefa | To Do | 2025-10-10 | API CRM
PDTIC25148-31 | Tarefa | To Do | 2025-10-26 | Mapa de mesa - Permitir arrastar mais de uma cadeira ao mesmo tempo
PDTIC25148-32 | Tarefa | Done | 2025-10-26 | Ajustes na Mesa - Exibir a cabeceira no topo
PDTIC25148-33 | Tarefa | To Do | 2026-06-01 | Erro ao carregar convidados e confirmados ao mesmo tempo
PDTIC25148-34 | Tarefa | EM TESTE | 2026-09-04 | Configuração de Legendas por Evento
PDTIC25148-35 | Tarefa | EM TESTE | 2026-09-04 | Melhorias na Listagem de Pessoas Confirmadas
PDTIC25148-36 | Tarefa | EM TESTE | 2026-09-04 | CRM - Importação de convidados

Os documentos legados citam: GPE004 v1.1 → [DTIC25148-32] (composição e disposição da mesa); GPE005 v1.1 → [PDTIC25148-32], [PDTIC25148-20] e [PDTIC25148-28] (exportação de participantes, remoção da confirmação, check-in automático no cadastro de participante, consulta por legenda na alocação).

---

## PDTIC25148-34 — Configuração de Legendas por Evento (EM TESTE) — resumo fiel

História: como responsável pela configuração do evento, quero configurar e aplicar as legendas das pessoas por meio de blocos e regras reutilizáveis, para definir a identificação dos participantes de cada evento de forma flexível, reaproveitando configurações entre eventos.

Pontos da descrição:
- A tela (rota /regras-legenda/:eventoId) é reformulada para que as legendas sejam configuradas por evento. Blocos podem ser criados ou reutilizados entre eventos; ordem e regras são do evento. A legenda da pessoa passa a ser vinculada ao evento (Evento – Pessoa – Legenda).
- A tela permite: visualizar os blocos do evento; adicionar bloco existente do Catálogo; criar novo bloco; remover blocos do evento; alterar a ordem; configurar condições; salvar como preset; carregar configurações de outros eventos ou presets; simular; executar a geração das legendas.
- Todo bloco adicionado está em vigor. NÃO há bloco ativo/inativo; o que não deve valer é removido da configuração.
- Blocos do evento: adicionar, remover e reordenar alteram só o evento atual. Cada bloco tem Nº = posição (1, 2, 3…), recalculado ao reordenar. A ordem é a prioridade de aplicação. A numeração NÃO é do Catálogo.
- Catálogo de Blocos: ao adicionar, pesquisar e selecionar existente ou criar novo. Para criar: Nome; Cor da legenda; Composição de mesa. Pesquisa sem resultado → opção 'Adicionar bloco "<termo>"', que abre a criação com o Nome preenchido. Bloco novo entra no Catálogo e fica disponível a outros eventos. Catálogo sem número nem ordem.
- Gestão do Catálogo: criar, editar, excluir. Sem duplicar/copiar. Editar reflete nos eventos que usam o bloco. Excluir bloco em uso: informar que está em uso e que a exclusão o remove das configurações desses eventos; só após confirmação.
- Condições: Campo | Operador | Valor. Campos: Grupo de Trabalho; Tema/Grupo Temático; Cargo; Nome Fantasia; Papel Desempenhado. Operadores: Igual a; Diferente de; Contém; Em (lista). A partir da segunda condição: conector E / OU.
- Presets: salvar a configuração atual com um nome; guarda blocos e regras. Recuperar pela biblioteca de presets ou de outro evento. Ao carregar: Substituir (remove a atual e aplica a selecionada) ou Mesclar (mantém os blocos atuais e acrescenta os da selecionada). Excluir preset remove só o preset, sem alterar eventos onde foi aplicado.
- Execução: gera de novo as associações das pessoas do evento atual, considerando blocos, condições e ordem de prioridade. Não altera: legendas de outros eventos; cadastro da pessoa; legendas definidas manualmente.
- Legendas manuais (como Anfitrião e Palestrante) são preservadas; não são recalculadas nem removidas na regeneração.
- Simular: mostra quantas e quais pessoas seriam associadas a cada legenda; não altera dados.
- Executar: pede confirmação informando que as associações do evento serão recriadas, as manuais preservadas e outros eventos não afetados.

Critérios de aceite (numeração da fonte):
CA01 Adicionar bloco existente (pesquisar e selecionar no Catálogo)
CA02 Criar novo bloco (nome, cor da legenda e composição de mesa)
CA03 Criar bloco a partir da busca (opção 'Adicionar bloco ""', Nome preenchido com o termo)
CA04 Disponibilizar bloco no Catálogo (novo bloco disponível a outros eventos)
CA05 Catálogo sem numeração
CA06 Numeração por evento (Nº = posição)
CA07 Reordenar blocos (recalcula numeração; nova ordem = prioridade)
CA08 Blocos sem estado ativo/inativo
CA09 Remover bloco do evento (só a associação com o evento atual)
CA10 Editar bloco do Catálogo (reflete nos eventos)
CA11 Excluir bloco do Catálogo (avisa uso; confirma)
CA12 Não duplicar blocos
CA13 Configurar condições (Campo, Operador, Valor)
CA14 Utilizar múltiplas condições (alinhadas; conector E/OU a partir da segunda)
CA15 Salvar preset (informar nome)
CA16 Carregar preset (Substituir ou Mesclar)
CA17 Excluir preset (não altera eventos)
CA18 Recuperar configuração de outro evento
CA19 Simular regras (quantas e quais pessoas por legenda, sem alterar)
CA20 Confirmar execução (informa recriação, preservação das manuais, isolamento)
CA21 Regenerar legendas do evento (blocos, condições, ordem de prioridade)
CA22 Preservar legendas manuais
CA23 Isolar configuração por evento

Divergência ticket × código já conhecida: o ticket pede "Composição de mesa" na criação do bloco (CA02); o código só tem Nome e Cor (a composição foi descartada — comentário "D5" no código do back).

---

## PDTIC25148-35 — Melhorias na Listagem de Pessoas Confirmadas (EM TESTE) — resumo fiel

História: como responsável pela gestão do evento, quero visualizar e filtrar as pessoas confirmadas com informações e ações adicionais, para facilitar a consulta e a manutenção dos dados dos participantes.

Regras:
- Definição de critérios: ao definir um critério (legenda) para as pessoas confirmadas, não disponibilizar mais a opção "Assento Livre". Demais opções inalteradas.
- Acesso ao perfil da pessoa: o nome da pessoa é um link na listagem; abre o perfil da pessoa em nova aba.
- Filtro de pessoas sem foto: filtro que mostra somente pessoas confirmadas no evento que não possuem foto.

Critérios de aceite:
CA01 Remover opção Assento Livre (na definição de critério)
CA02 Acessar perfil da pessoa (nome abre o perfil em nova aba)
CA03 Filtrar pessoas sem foto

---

## PDTIC25148-36 — CRM - Importação de convidados (EM TESTE) — resumo fiel

História: como responsável pela gestão do evento, quero importar para o evento a lista de inscritos registrada no CRM, para utilizar as informações das pessoas vinculadas à campanha.

Pontos:
- Identificação pelo código da campanha. O cadastro do evento ganha o campo Código da Campanha.
- Evento sem Código da Campanha: a importação não é realizada e o sistema orienta a preencher o campo.
- Ação "Importar Inscritos do CRM": recupera o código, consulta o CRM, importa os registros, associa os inscritos ao evento. Sem digitação manual.
- Dados do CRM por registro: Data de envio do formulário; Status da Inscrição; Status Aprovação; Cód. Contato; Contato relacionado; Codinome; Nome; E-mail; Empresa; Cargo.
- Nova importação no mesmo evento consulta de novo; inscrito já associado não é duplicado; dados vindos do CRM são atualizados.

Critérios de aceite:
CA01 Código da Campanha no evento (campo no cadastro/edição)
CA02 Utilizar Código da Campanha na consulta
CA03 Impedir importação sem campanha (não consulta; informa que o campo deve ser preenchido)
CA04 Consultar inscritos no CRM
CA05 Importar dados dos inscritos (os 10 campos acima)
CA06 Associar inscritos ao evento
CA07 Evitar duplicidade
CA08 Atualizar dados em nova importação
CA09 Campanha sem inscritos (informa que não foram encontrados registros; não altera a lista)
CA10 Isolar importação por evento
