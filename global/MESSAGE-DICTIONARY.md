<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
# MESSAGE-DICTIONARY.md
> Dicionário de **mensagens de UI** que a pessoa usuária lê — e o **baseline** de
> validação (obrigatório, formato, sucesso, estados de tela).
>
> Garante texto **literal e consistente** em todo o sistema. Nos cenários, escreva
> sempre o texto final do catálogo — nunca "conforme o Design System" (isso é
> gatilho de busca, não texto entregável).
>
> **Como referenciar nos N3**:
> - Mensagens genéricas (obrigatório/formato/sucesso): `# ← MESSAGE-DICTIONARY: BASELINE`
> - Mensagem específica: cite a chave e escreva o texto literal.
>
> **Precedência**: mensagem de campo canônico vem do **FIELD-DICTIONARY** (tem
> precedência sobre o baseline daqui).

---

## Baseline de validação

> Mensagens genéricas reutilizadas por qualquer campo/feature. Use o marcador `# ← MESSAGE-DICTIONARY: BASELINE` nos cenários em vez de reescrevê-las.

> ⚠️ **Levantado do código em 2026-09-30 💻.** O GPE tem **duas famílias** de mensagem de validação, conforme a tela: as de acesso e de usuários usam um conjunto; as de pessoa, evento, participante e legenda usam outro. As duas estão abaixo — a coluna Onde diz qual vale em cada tela. Não há guia de redação: os textos divergem em pontuação e em maiúsculas, e foram transcritos como estão.

| Chave | Situação | Texto literal | Onde |
|---|---|---|---|
| `REQUIRED` | Campo obrigatório não preenchido | "Campo obrigatório." | Acesso e usuários |
| `REQUIRED_CADASTRO` | Campo obrigatório não preenchido | "Este campo é obrigatório" | Pessoa, evento, participante, legenda |
| `MIN_LENGTH` | Abaixo do comprimento mínimo | "Mínimo de [N] caracteres" | Pessoa, evento, participante |
| `MAX_LENGTH` | Excedeu o comprimento máximo | "Máximo de [N] caracteres" | Pessoa, evento, participante |
| `MIN_VALUE` | Abaixo do valor mínimo | "Valor mínimo é [N]" | Evento |
| `MAX_VALUE` | Acima do valor máximo | "Valor máximo é [N]" | Evento |
| `INVALID_FORM` | Tentativa de salvar com o formulário inválido | "Formulário inválido" com o detalhe "Preencha todos os campos obrigatórios corretamente" | Usuário, pessoa, evento |
| `GENERIC_ERROR` | Falha sem detalhe vindo do servidor | "Serviço indisponível." | Acesso e usuários |
| `SERVER_ERROR_DETAIL` | Falha com detalhe vindo do servidor | Resumo "Erro Interno" e, no detalhe, o texto que o servidor enviou. ⚠️ O resumo é "Erro Interno" mesmo quando o detalhe é uma regra de negócio | Telas de lista e de formulário em geral |
| `NO_PERMISSION` | Operação recusada por falta de permissão | "Proibido." 🔍 — é o texto genérico que a tela mostra quando o servidor recusa por permissão; o caso comum é a opção nem aparecer | Todas |
| `UNAUTHORIZED` | Credencial recusada | Sem mensagem: a sessão é encerrada e o usuário volta à tela de acesso | Todas |
| `NO_SERVER` | Sem resposta do servidor | "Erro" com o detalhe "Falha de comunicação com o servidor." | Legendas |
| `ADMIN_CONTACT` | Detalhe da falha ao remover pessoa ou evento | "Contate o administrador do sistema." | Lista de pessoas, lista de eventos |
| `FILE_READ_ERROR` | O arquivo escolhido não pôde ser lido pelo navegador | "Falha ao ler o arquivo." | Foto da pessoa, imagem do evento |
| `SHEET_READ_ERROR` | A planilha escolhida não pôde ser lida pelo navegador | "Falha ao ler planilha." | Janelas de carga |
| `HTTP_400` | Falha sem detalhe — pedido recusado | "Requisição inválida." | Telas de lista e de formulário em geral |
| `HTTP_404` | Falha sem detalhe — dado não encontrado | "Dados não encontrados." | Telas de lista e de formulário em geral |
| `HTTP_408` | Falha sem detalhe — tempo esgotado | "Tempo de requisição esgotou." | Telas de lista e de formulário em geral |
| `HTTP_429` | Falha sem detalhe — excesso de pedidos | "Excesso de requisição." | Telas de lista e de formulário em geral |
| `HTTP_500` | Falha sem detalhe — erro no servidor | "Erro interno do servidor." | Telas de lista e de formulário em geral |

> As chaves `SAVE_SUCCESS`, `DELETE_SUCCESS` e `DELETE_CONFIRM` da linha de base do framework **não existem** no GPE: cada tela tem o seu próprio texto de sucesso e de confirmação, transcrito no N3 da feature.

---

## Estados de tela

> Textos dos estados de lista. Cada lista tem o seu; não há texto único.

| Chave | Estado | Texto literal | Onde |
|---|---|---|---|
| `EMPTY_USUARIOS` | Sem dados | "Nenhum usuário encontrado." | Lista de usuários |
| `EMPTY_PESSOAS` | Sem dados | "Nenhuma pessoa encontrada." | Lista de pessoas |
| `EMPTY_EVENTOS` | Sem dados | "Nenhum evento encontrado" | Lista de eventos |
| `EMPTY_PARTICIPANTES` | Sem dados | "Nenhum participante encontrado." | Lista de participantes |
| `EMPTY_BLOCOS` | Sem dados | "Nenhum bloco encontrado." | Catálogo de blocos |
| `EMPTY_CONFIGURACAO` | Sem dados | "Nenhum bloco configurado" | Configuração de legendas |
| `LOADING_EVENTO` | Carregando | "Carregando dados do evento..." | Participantes do evento |
| `LOADING_MESA` | Carregando | "Carregando dados da mesa..." | Mapa de assentos |

---

## Mensagens específicas por domínio

> Catálogo das mensagens que os cenários dos N3 citam, levantadas do código em 2026-09-30 💻 — as da tela e as que o servidor devolve por regra de negócio. O texto é o **literal do sistema**, inclusive com os erros de redação que ele tem (marcados ⚠️). Trecho entre colchetes é valor variável. A coluna Feature diz onde a mensagem aparece.

### Acesso e Usuários

| Chave | Situação | Texto literal | Feature |
|---|---|---|---|
| `ACE_SENHA_TEMPORARIA_ENVIADA` | Pedido de recuperação de senha aceito | "Senha temporária enviada." | `ACE-AUT-03` |
| `ACE_USUARIO_NAO_CADASTRADO` | Login validado que ainda não é usuário do sistema — resumo do aviso | "Usuário não cadastrado no sistema." | `ACE-USU-02`, `ACE-USU-03` |
| `ACE_USUARIO_NAO_ENCONTRADO` | Login validado que ainda não é usuário do sistema — detalhe do aviso | "O usuário informado não foi encontrado no sistema." | `ACE-USU-02`, `ACE-USU-03` |
| `ACE_LOGIN_INVALIDO` | Login que não existe no diretório corporativo e não tem formato de e-mail | "Para usuários internos, o login deve existir no Active Directory. Para usuários externos, o login deve ser um e-mail válido." | `ACE-USU-02`, `ACE-USU-03` |
| `ACE_USUARIO_JA_CADASTRADO` | Login validado que já é usuário do sistema — resumo do erro | "Usuário já cadastrado no sistema." | `ACE-USU-02` |
| `ACE_USUARIO_JA_NO_SISTEMA` | Login validado que já é usuário do sistema — detalhe do erro. ⚠️ O texto tem erro de redação ("já estas") | "O usuário informado já estas no sistema." | `ACE-USU-02` |

### Pessoas

| Chave | Situação | Texto literal | Feature |
|---|---|---|---|
| `PES_COM_VINCULO_EVENTO` | Excluir pessoa que participa de evento | "Não é possível remover a pessoa, pois ela já possui vínculo com evento." | `PES-CAD-04` |
| `PES_ERRO_SALVAR` | Falha ao incluir ou alterar pessoa | "Erro ao salvar pessoa. Verifique os dados e tente novamente." | `PES-CAD-02`, `PES-CAD-03` |
| `PES_CARGA_CABECALHO_INCOMPLETO` | Planilha de grupos de trabalho, de temas ou de histórico sem as colunas exigidas | "Cabeçalho incompleto na carga." | `PES-CAD-05`, `PES-CAD-06`, `PES-CAD-07` |
| `PES_CARGA_EM_PROCESSAMENTO` | Planilha enviada — resumo do aviso | "Carga em processamento." | `PES-CAD-05`, `PES-CAD-06`, `PES-CAD-07` |
| `PES_CARGA_GT_EM_PROCESSAMENTO` | Planilha de grupos de trabalho enviada — detalhe do aviso | "Carga de Grupos Temáticos em processamento." | `PES-CAD-05` |
| `PES_CARGA_GT_SUCESSO` | Carga de grupos de trabalho concluída | "Carga realizada com sucesso." | `PES-CAD-05` |
| `PES_CARGA_GT_FALHA_LEITURA` | A planilha de grupos de trabalho não pôde ser lida pelo navegador | "Falha ao ler planilha de Grupos de Trabalho." | `PES-CAD-05` |
| `PES_CARGA_GT_ERRO` | Falha no processamento da carga de grupos de trabalho | "Erro ao processar a carga de Grupos Temáticos. Verifique o arquivo e tente novamente." | `PES-CAD-05` |
| `PES_CARGA_TEMAS_EM_PROCESSAMENTO` | Planilha de temas enviada — detalhe do aviso | "Carga de Temas em processamento." | `PES-CAD-06` |
| `PES_CARGA_TEMAS_FALHA_LEITURA` | A planilha de temas não pôde ser lida pelo navegador | "Falha ao ler planilha de Temas." | `PES-CAD-06` |
| `PES_CARGA_TEMAS_ERRO` | Falha no processamento da carga de temas | "Erro ao processar a carga de Temas. Verifique o arquivo e tente novamente." | `PES-CAD-06` |
| `PES_CARGA_HISTORICO_EM_PROCESSAMENTO` | Planilha de histórico enviada — detalhe do aviso | "Carga de Históricos em processamento." | `PES-CAD-07` |
| `PES_CARGA_HISTORICO_FALHA_LEITURA` | A planilha de histórico não pôde ser lida pelo navegador | "Falha ao ler planilha de Histórico." | `PES-CAD-07` |
| `PES_CARGA_HISTORICO_ERRO` | Falha no processamento da carga de histórico | "Erro ao processar a carga de Histórico. Verifique o arquivo e tente novamente." | `PES-CAD-07` |

### Eventos — cadastro e cargas

| Chave | Situação | Texto literal | Feature |
|---|---|---|---|
| `EVT_ERRO_SALVAR` | Falha ao incluir ou alterar evento | "Erro ao salvar evento. Verifique os dados e tente novamente." | `EVT-CAD-02`, `EVT-CAD-03` |
| `EVT_PRINCIPAL_ATUALIZADO` | Evento definido como principal | "O evento principal foi atualizado com sucesso." | `EVT-CAD-06` |
| `EVT_CARGAS_EM_PROCESSAMENTO` | Planilhas de convidados ou de confirmados enviadas — resumo do aviso | "Cargas em processamento." | `EVT-CAD-07`, `EVT-CAD-08` |
| `EVT_CARGAS_AGUARDE` | Planilhas de convidados ou de confirmados enviadas — detalhe do aviso | "Por favor aguarde, as cargas estão em processamento." | `EVT-CAD-07`, `EVT-CAD-08` |
| `EVT_CARGA_CONVIDADOS_CONCLUIDA` | Carga de convidados concluída | "Lista de convidados foi atualizada." | `EVT-CAD-07` |
| `EVT_CARGA_CONVIDADOS_FALHA_LEITURA` | A planilha de convidados não pôde ser lida pelo navegador | "Falha ao ler planilha de convidados." | `EVT-CAD-07` |
| `EVT_CARGA_CONFIRMADOS_CONCLUIDA` | Carga de confirmados concluída | "Lista de confirmados foi atualizada." | `EVT-CAD-08` |
| `EVT_CARGA_CONFIRMADOS_FALHA_LEITURA` | A planilha de confirmados não pôde ser lida pelo navegador | "Falha ao ler planilha de confirmados." | `EVT-CAD-08` |
| `EVT_CARGA_ERRO` | Falha no processamento da carga de convidados ou de confirmados — resumo do erro | "Erro ao processar carga." | `EVT-CAD-07`, `EVT-CAD-08` |
| `EVT_CRM_SEM_CAMPANHA` | Importar inscritos de evento sem Código da Campanha | "O Código da Campanha deve ser preenchido no cadastro do evento." | `EVT-CAD-09` |
| `EVT_CRM_SEM_INSCRITOS` | A campanha não tem inscritos aprovados e confirmados | "Não foram encontrados inscritos aprovados e confirmados no CRM para a campanha [código]." | `EVT-CAD-09` |
| `EVT_CRM_NAO_CONFIGURADO` | Integração com o CRM sem configuração | "Integração com o CRM não configurada." | `EVT-CAD-09` |
| `EVT_CRM_FALHA_AUTENTICACAO` | O CRM recusou a credencial da integração | "Não foi possível autenticar no CRM. Verifique as credenciais de integração." | `EVT-CAD-09` |
| `EVT_CRM_FALHA_CONSULTA` | Falha na consulta ao CRM | "Não foi possível consultar o CRM. Tente novamente mais tarde." | `EVT-CAD-09` |
| `EVT_CRM_ERRO_IMPORTAR` | Falha na importação sem detalhe vindo do servidor | "Erro ao importar inscritos do CRM. Tente novamente mais tarde." | `EVT-CAD-09` |

### Eventos — participantes e mapa de assentos

| Chave | Situação | Texto literal | Feature |
|---|---|---|---|
| `EVT_CHECKIN_REALIZADO` | Check-in marcado — resumo do aviso | "Check-in realizado." | `EVT-PAR-03` |
| `EVT_CHECKIN_NAO_REALIZADO` | Check-in desmarcado — resumo do aviso | "Check-in não realizado." | `EVT-PAR-03` |
| `EVT_CONFIRMACAO_REALIZADA` | Confirmação de presença reposta — resumo do aviso | "Confirmação realizada." | `EVT-PAR-13` |
| `EVT_CONFIRMACAO_RETIRADA` | Confirmação de presença retirada — resumo do aviso. ⚠️ Redação truncada | "Não confirmação realizada." | `EVT-PAR-13` |
| `EVT_LEGENDA_ATUALIZADA` | Legenda manual atribuída ao participante | "Legenda atualizada com sucesso!" | `EVT-PAR-05` |
| `EVT_LEGENDA_ERRO_SALVAR` | Falha ao atribuir a legenda manual | "Erro ao salvar legenda da pessoa." | `EVT-PAR-05` |
| `EVT_LEGENDA_JA_SEM` | Salvar sem escolher legenda, para participante que não tem legenda manual | "Esta pessoa já não possui legenda." | `EVT-PAR-05`, `EVT-PAR-06` |
| `EVT_LEGENDA_REMOVIDA` | Legenda manual retirada do participante | "Legenda removida com sucesso!" | `EVT-PAR-06` |
| `EVT_LEGENDA_ERRO_REMOVER` | Falha ao retirar a legenda manual | "Erro ao remover legenda da pessoa." | `EVT-PAR-06` |
| `EVT_PARTICIPANTE_NAO_ENCONTRADO` | Legenda manual para participante que não existe mais | "Participante não encontrado." | `EVT-PAR-05` |
| `EVT_EXPORTACAO_EM_ANDAMENTO` | Exportação de participantes iniciada — resumo do aviso | "Exportação em andamento." | `EVT-PAR-14` |
| `EVT_EXPORTACAO_AGUARDE` | Exportação de participantes iniciada — detalhe do aviso | "A exportação dos participantes está em andamento, por favor aguarde." | `EVT-PAR-14` |
| `EVT_EXPORTACAO_ERRO` | Falha na exportação de participantes | "Erro ao exportar participantes." | `EVT-PAR-14` |
| `EVT_MAPA_SALVO` | Mapa de assentos gravado pelo botão Salvar Alocações | "Composições da mesa salvas com sucesso! [n] pessoas foram alocadas." | `EVT-PAR-08` |
| `EVT_MAPA_ERRO_SALVAR` | Falha ao gravar o mapa pelo botão. ⚠️ O texto manda o usuário ao console do navegador | "Erro ao salvar composições da mesa. Verifique o console para mais detalhes." | `EVT-PAR-08` |
| `EVT_MAPA_ERRO_SALVAR_AUTOMATICO` | Falha na gravação automática do mapa | "Erro ao salvar composição automaticamente. Suas alterações podem não ter sido salvas." | `EVT-PAR-08` |
| `EVT_MAPA_LIMPO` | Todos os assentos liberados na tela. ⚠️ A liberação não é gravada | "Todas as alocações foram removidas da mesa." | `EVT-PAR-11` |
| `EVT_MAPA_EXPORTANDO_COMPLETO` | Exportação do mapa completo iniciada | "Preparando exportação do mapa completo..." | `EVT-PAR-15` |
| `EVT_MAPA_EXPORTADO_PDF` | Mapa completo exportado em PDF | "Mapa completo exportado em PDF com sucesso!" | `EVT-PAR-15` |
| `EVT_MAPA_EXPORTADO_PNG` | Mapa completo exportado em imagem | "Mapa completo exportado em PNG com sucesso!" | `EVT-PAR-15` |
| `EVT_MAPA_ERRO_EXPORTAR` | Falha na exportação do mapa completo | "Erro ao exportar o mapa. Tente novamente." | `EVT-PAR-15` |
| `EVT_MESA_PRESIDENTE_EXPORTANDO` | Exportação da mesa do presidente iniciada | "Preparando exportação para o presidente..." | `EVT-PAR-15` |
| `EVT_MESA_PRESIDENTE_EXPORTADA_PDF` | Mesa do presidente exportada em PDF | "Mesa do presidente exportada em PDF com sucesso!" | `EVT-PAR-15` |
| `EVT_MESA_PRESIDENTE_EXPORTADA_PNG` | Mesa do presidente exportada em imagem | "Mesa do presidente exportada em PNG com sucesso!" | `EVT-PAR-15` |
| `EVT_MESA_PRESIDENTE_ERRO_EXPORTAR` | Falha na exportação da mesa do presidente | "Erro ao exportar a mesa do presidente. Tente novamente." | `EVT-PAR-15` |

### Eventos — legendas

| Chave | Situação | Texto literal | Feature |
|---|---|---|---|
| `EVT_LEG_EVENTO_NAO_INFORMADO` | Configuração de legendas aberta sem o evento no endereço | "Evento não informado na URL." | `EVT-LEG-01` |
| `EVT_LEG_EVENTO_NAO_ENCONTRADO` | Salvar, simular ou gerar legendas de evento que não existe | "Evento não encontrado." | `EVT-LEG-01`, `EVT-LEG-06`, `EVT-LEG-07` |
| `EVT_LEG_BLOCO_REPETIDO` | A mesma legenda em dois blocos do evento | "A configuração tem blocos de legenda repetidos." | `EVT-LEG-01`, `EVT-LEG-07` |
| `EVT_LEG_PRESET_SALVO` | Preset salvo | "O preset '[nome]' foi salvo." | `EVT-LEG-08` |
| `EVT_LEG_PRESET_NOME_OBRIGATORIO` | Preset sem nome | "O nome do preset é obrigatório." | `EVT-LEG-08` |
| `EVT_LEG_PRESET_NOME_DUPLICADO` | Já existe preset com o mesmo nome | "Já existe um preset com este nome." | `EVT-LEG-08` |
| `EVT_LEG_PRESET_ILEGIVEL` | A configuração guardada no preset não pôde ser lida | "Não foi possível ler a configuração do preset." | `EVT-LEG-09` |
| `EVT_LEG_PRESET_REMOVIDO` | Preset excluído | "O preset '[nome]' foi removido." | `EVT-LEG-10` |
| `EVT_LEG_PRESET_NAO_ENCONTRADO` | Excluir preset que não existe mais | "Preset não encontrado." | `EVT-LEG-10` |
| `EVT_LEG_BLOCO_CRIADO` | Bloco incluído no catálogo | "O bloco foi criado com sucesso." | `EVT-LEG-12` |
| `EVT_LEG_BLOCO_ATUALIZADO` | Bloco do catálogo alterado | "O bloco foi atualizado com sucesso." | `EVT-LEG-13` |
| `EVT_LEG_BLOCO_EXCLUIDO` | Bloco excluído do catálogo | "O bloco foi excluído com sucesso." | `EVT-LEG-14` |
| `EVT_LEG_NOME_OBRIGATORIO` | Bloco de legenda sem nome | "O nome do bloco de legenda é obrigatório." | `EVT-LEG-12`, `EVT-LEG-13` |
| `EVT_LEG_COR_INVALIDA` | Cor ausente ou fora do formato | "A cor deve estar no formato #RRGGBB." | `EVT-LEG-12`, `EVT-LEG-13` |
| `EVT_LEG_NOME_DUPLICADO` | Já existe bloco com o mesmo nome | "Já existe um bloco de legenda com este nome." | `EVT-LEG-12`, `EVT-LEG-13` |
| `EVT_LEG_BLOCO_NAO_ENCONTRADO` | Editar ou excluir bloco que não existe mais | "Bloco de legenda não encontrado." | `EVT-LEG-13`, `EVT-LEG-14` |

> ⚠️ **Catálogo parcial.** Estão aqui as mensagens que os cenários citam em passo de exibição e que terminam em ponto — é o recorte que o validador confere. As demais mensagens das telas (títulos de aviso sem ponto, textos de confirmação, dicas) estão literais no N3 de cada feature e ainda não foram catalogadas.

---

## Como adicionar uma mensagem

1. Use o **baseline** sempre que a mensagem for genérica — não crie variações desnecessárias.
2. Mensagem nova e específica: adicione à seção do domínio com chave e texto literal.
3. Mensagem de **campo canônico**: defina no FIELD-DICTIONARY, não aqui.

---

## Instrução para a LLM

Ao escrever cenários/telas em um N3:
1. Use o **texto literal** do catálogo — nunca "conforme o Design System".
2. Para obrigatório/formato/sucesso genéricos, use `# ← MESSAGE-DICTIONARY: BASELINE`.
3. Mensagem de campo canônico vem do FIELD-DICTIONARY (precedência).
4. Mensagem inexistente no catálogo: proponha com ⚠️, aguarde aprovação e instrua a adição aqui.

> **Usado em (não escreva à mão)**: a seção `## Usado em (índice reverso)` ao final
> é **gerada** por `scripts/generate-usage-index.mjs` a partir das referências
> `→ ver`/`←` dos N3. Não edite à mão — rode o gerador (o CI valida que está fresco).

<!-- usado-em:gerado -->
## Usado em (índice reverso)

> Gerado por `scripts/generate-usage-index.mjs` a partir das referências `→ ver`/`←` nos N3. **Não editar à mão.**

| Entrada | Usado em |
|---|---|
| `BASELINE` | `ACE-AUT-01` · `ACE-AUT-03` · `ACE-USU-02` · `ACE-USU-03` · `EVT-CAD-02` · `EVT-CAD-03` · `EVT-PAR-02` · `PES-CAD-02` · `PES-CAD-03` |
<!-- /usado-em -->
