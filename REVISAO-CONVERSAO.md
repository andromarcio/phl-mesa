<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
# Revisão da conversão — GPE

> Gerado pelo `PROMPT_CONVERSION` na engenharia reversa de 2026-09-30. Esta instância foi escrita de uma vez, a partir dos seis documentos legados (GPE001 a GPE006), do código do back-end e do front-end e de três tickets do Jira. **Nenhuma feature foi validada por alguém do negócio**: as 55 estão em rascunho. Este arquivo diz onde olhar primeiro.

---

## Como ler

Os N1, N2 e N3 usam os mesmos marcadores: 💻 só o código mostra · 📄 só o documento diz · 🔍 inferido · ❓ nenhuma fonte responde · ⚠️ divergência, suspeita de defeito ou ponto de atenção. **O que está sem marcador veio de documento e código concordantes e dispensa revisão.**

Onde documento e código divergem, o N3 descreve **o que o código faz** e anota o que o documento dizia. Isso não é uma decisão de que o código está certo — é o retrato do que existe. Cabe ao PO dizer, caso a caso, qual dos dois vale.

Tudo o que vem do código saiu da **leitura** dele. Nada foi compilado nem executado, e as cópias lidas não tinham histórico git. O que depende de comportamento em execução está dito como inferência.

O detalhe, feature a feature, está em seis arquivos:

| Feature Set | Features | Divergências | Lacunas | Inferências | Suspeitas de defeito | Detalhe |
|---|---|---|---|---|---|---|
| Autenticação `ACE-AUT` | 6 | 15 | 20 | 18 | 25 | [revisao-conversao/ACE-AUT.md](./revisao-conversao/ACE-AUT.md) |
| Usuários `ACE-USU` | 4 | 20 | 20 | 19 | 17 | [revisao-conversao/ACE-USU.md](./revisao-conversao/ACE-USU.md) |
| Cadastro de Pessoas `PES-CAD` | 7 | 25 | 18 | 21 | 33 | [revisao-conversao/PES-CAD.md](./revisao-conversao/PES-CAD.md) |
| Cadastro de Eventos `EVT-CAD` | 9 | 39 | 23 | 24 | 34 | [revisao-conversao/EVT-CAD.md](./revisao-conversao/EVT-CAD.md) |
| Participantes `EVT-PAR` | 15 | 48 | 35 | 34 | 83 | [revisao-conversao/EVT-PAR.md](./revisao-conversao/EVT-PAR.md) |
| Legendas `EVT-LEG` | 14 | 45 | 37 | 37 | 52 | [revisao-conversao/EVT-LEG.md](./revisao-conversao/EVT-LEG.md) |
| **Total** | **55** | **192** | **153** | **153** | **244** | — |

> Os números contam **itens de lista** nos arquivos de detalhe, não achados distintos: o mesmo ponto aparece em cada feature que ele afeta. Servem para dimensionar o esforço de revisão, não para medir a qualidade do sistema.

---

## 1. Segurança e acesso — olhar antes de qualquer outra coisa

Estes pontos não são de especificação: são achados do código que alguém da CNI precisa conhecer. Os seis primeiros foram conferidos diretamente no código-fonte.

1. **Segredo escrito em arquivo versionado.** O `Dockerfile` do back-end traz, como valor padrão de variável de ambiente, o identificador e o segredo de cliente do serviço de autenticação; os dois `configuracoes.json` trazem outro par. Os valores **não** foram copiados para esta documentação. Quem tem leitura do repositório tem o segredo, e ele permanece no histórico mesmo depois de removido.
2. **O servidor entrega as configurações privadas ao navegador.** A operação que devolve as configurações privadas do serviço corporativo não está entre os recursos protegidos declarados, e a tela de acesso a usa para obter o identificador e o segredo de cliente com que monta o pedido de autenticação. O segredo, portanto, chega a qualquer navegador que abra a tela de acesso.
3. **Recursos de negócio fora da lista protegida.** O cadastro do sistema no serviço corporativo declara quatro recursos protegidos: eventos, legendas, a integração de planilha e o check-in da secretaria. **Não constam** pessoas (inclusive exclusão e as três cargas), participantes (inclusive o registro de atendimento), arquivos (fotos e imagens) e as listas de tipo. Se o serviço corporativo espelha esse cadastro, essas operações respondem **sem credencial**. O código não permite confirmar o que vale em produção ❓.
4. **Tudo público em caso de falha.** Se o servidor não consegue obter a lista de recursos protegidos ao subir, ele inicia com **todos** os recursos sem autenticação e apenas registra isso no log.
5. **O servidor não confere perfil.** Nenhuma regra do servidor lê quem é o usuário ou qual é o seu perfil. A única distinção é feita fora dele, por recurso e tipo de operação — granularidade que não separa, por exemplo, o check-in da gravação do mapa de assentos, nem a consulta de eventos da consulta de participantes.
6. **A interface não tem controle de perfil nas rotas.** Qualquer usuário autenticado alcança qualquer tela digitando o endereço. O que separa os perfis é o menu e poucas conferências pontuais; as ações por linha da lista de eventos, as telas de usuários, de pessoas e de legendas não conferem perfil.
7. **Recuperação de senha só pelo login.** Basta conhecer o login de outra pessoa para pedir a troca da senha dela; nenhum outro dado é exigido 🔍.
8. **A saída não limpa a sessão em memória.** Depois de sair, até a página ser recarregada, o botão de voltar do navegador reabre as telas internas 🔍.
9. **Nenhuma ação registra o autor.** O sistema não guarda quem fez check-in, quem alterou legenda, quem carregou planilha ou quem excluiu um evento. Não há trilha de auditoria.
10. **Há dados pessoais reais nas imagens dos documentos legados.** As telas de GPE003 mostram nome, e-mail, CPF e telefone de pessoas reais. Os cenários dos N3 usam nomes fictícios; os `.docx` em `arquivos/` continuam como vieram.

---

## 2. Defeitos que perdem ou corrompem dado

Suspeitas de defeito em que o dado gravado fica errado ou some. As marcadas ✔ foram conferidas diretamente no código-fonte; as demais vêm da leitura feita na redação dos N3. Nenhuma foi reproduzida em execução.

| # | O que acontece | Feature | Conferido |
|---|---|---|---|
| 1 | **Limpar o mapa não é gravado.** O botão "Limpar Todas" esvazia o mapa na tela, mostra "Todas as alocações foram removidas da mesa." e agenda a gravação automática — que desiste quando não há ninguém sentado. A operação de limpeza do servidor existe e a tela nunca a chama. Ao reabrir, os assentos estão como antes | `EVT-PAR-11 — Liberar Todos os Assentos` | ✔ |
| 2 | A retirada do **último** participante sentado, pelo mesmo motivo, também não é gravada | `EVT-PAR-09 — Remover Assento do Participante` | — |
| 3 | **Gravar o mapa reescreve o participante.** O servidor reconstrói cada participante sentado a partir do que a tela enviou — identificação, quatro marcações e assento — e grava por cima. A data e hora do check-in e os cinco dados vindos do CRM voltam a vazio, e convite, confirmação, check-in e atendimento passam a valer o que a tela do Administrador tinha, mesmo que a recepção os tenha mudado depois | `EVT-PAR-08 — Atribuir Assento ao Participante` | ✔ |
| 4 | Alteração do mapa ainda não gravada (a janela é de 30 segundos) é descartada quando chega a atualização automática com mudança feita em outro ponto, como um check-in; sair do mapa cancela a gravação pendente sem aviso | `EVT-PAR-08 — Atribuir Assento ao Participante` | — |
| 5 | **A carga de convidados e a de confirmados gravam o CNPJ no CPF** da pessoa que já existe — e apagam o CPF quando a planilha não traz CNPJ | `EVT-CAD-07 — Carregar Convidados` · `EVT-CAD-08 — Carregar Confirmados` | ✔ |
| 6 | **As cargas de grupos de trabalho e de temas apagam a base inteira** antes de carregar. Uma planilha parcial elimina os vínculos de todas as pessoas que não estão nela; uma planilha só com cabeçalho apaga tudo e a tela mostra sucesso | `PES-CAD-05 — Carregar Grupos de Trabalho` · `PES-CAD-06 — Carregar Temas` | — |
| 7 | **Editar um evento regrava o que não está na tela.** A edição usa a mesma operação da inclusão e grava de volta Excluído e a condição de principal como estavam quando a tela abriu: um evento excluído editado pelo endereço volta à lista, e pode haver dois eventos principais, ou nenhum 🔍 | `EVT-CAD-03 — Editar Evento` | ✔ |
| 8 | Trocar o tipo de mesa de um evento já incluído não refaz os assentos: o desenho passa a ser o do tipo novo, com os assentos do tipo antigo | `EVT-CAD-03 — Editar Evento` | — |
| 9 | **Com as duas planilhas anexadas, a de confirmados não é enviada** 🔍 — a janela se fecha e esvazia os anexos antes do segundo envio. É o que o ticket `PDTIC25148-33` descreve, ainda em aberto | `EVT-CAD-08 — Carregar Confirmados` | ✔ |
| 10 | **Alterar a confirmação desfaz o check-in** — inclusive ao confirmar quem já havia chegado. A linha continua mostrando o check-in como feito até a próxima pesquisa | `EVT-PAR-13 — Alterar Confirmação de Presença` | — |
| 11 | Desmarcar o check-in grava nova data e hora em vez de limpar; o check-in automático do cadastro na recepção fica sem data e hora | `EVT-PAR-03 — Registrar Check-in` · `EVT-PAR-02 — Cadastrar Participante` | — |
| 12 | **Excluir um bloco do catálogo apaga também as legendas manuais** dos participantes, em todos os eventos. A pergunta de confirmação só considera a configuração dos eventos: um bloco fora de todas elas, mas atribuído manualmente, é tratado como sem uso | `EVT-LEG-14 — Excluir Bloco de Legenda` | — |
| 13 | Carregar uma configuração no modo Substituir, a partir de um preset vazio ou com todos os blocos já fora do catálogo, esvazia a configuração do evento sem pedir confirmação | `EVT-LEG-09 — Carregar Configuração de Legendas` | — |
| 14 | A tela de configuração de legendas mostra "Nenhum bloco configurado" enquanto carrega ou depois de uma falha; uma alteração feita nesse estado gravaria por cima da configuração real 🔍 | `EVT-LEG-01 — Consultar Configuração de Legendas` | — |
| 15 | **O filtro Data Final da pesquisa de eventos não funciona**: o servidor usa a data inicial no lugar dela | `EVT-CAD-01 — Pesquisar Eventos` | ✔ |
| 16 | Repetir "Criar" na tela de pessoa, depois de incluir, inclui a pessoa de novo: a tela não passa para o modo de edição | `PES-CAD-02 — Cadastrar Pessoa` | — |
| 17 | Na lista de participantes, razão social e nome fantasia chegam trocados do servidor; a coluna Organização mostra o nome fantasia | `EVT-PAR-01 — Pesquisar Participantes` | — |

---

## 3. Funcionalidades documentadas que hoje não funcionam ou não existem

| Documento | Funcionalidade | Situação no código | Onde ficou |
|---|---|---|---|
| GPE001 | Alterar imagem de perfil | O item "Alterar Foto do Perfil" existe no menu do usuário, mas a tela não tem a janela de troca: o clique não abre nada. A rotina de gravar existe e é inalcançável | `ACE-AUT-05 — Alterar Foto de Perfil`, especificada com ⚠️ |
| GPE006 | Resetar Regras | Não existe mais, nem na tela nem no servidor. Gerar as legendas com a configuração vazia tem efeito parecido | Sem N3. Pendência em `modules/INDEX.md` |
| GPE006 | Ativar e inativar a legenda no evento | Substituído: o bloco que não deve valer é removido da configuração (`PDTIC25148-34`) | `EVT-LEG-05 — Remover Bloco de Legenda do Evento` |
| GPE006 | Preview da condição (fórmula) | Não existe mais | Anotado em `EVT-LEG-03 — Configurar Condições de Legenda` |
| GPE002 | Envio de senha provisória depois da inclusão do usuário | O GPE não dispara nem confirma o envio: é do cadastro corporativo ❓ | `ACE-USU-02 — Cadastrar Usuário` |

---

## 4. Divergências de fundo entre os documentos e o código

Pontos em que o sistema mudou e o documento não acompanhou. O N3 segue o código; a decisão do que vale é do PO.

- **O modelo de legendas é outro.** GPE006 descreve doze legendas fixas, cada uma ativa ou inativa, com regras gravadas por um botão. O código tem um catálogo de blocos comum a todos os eventos, blocos por evento com ordem de prioridade, presets e gravação automática a cada alteração — o que o ticket `PDTIC25148-34`, em teste, pediu. Das 14 features de `EVT-LEG`, 9 não constam em GPE006.
- **A legenda manual era apagada, e agora é preservada.** A tela reproduzida em GPE006 avisa que "a execução REMOVE TODAS as legendas existentes"; o código preserva a manual.
- **Uma legenda por pessoa, ou várias?** O documento e o ticket sugerem uma; o código atribui uma legenda por bloco em que a pessoa se encaixa e exibe a prioritária ❓.
- **Os assentos do documento são os de um só formato.** As faixas de GPE004 — B e C até 34, E até 30, F até 28, H até 28 — são, no código, as do **Retangular Invertido**. O formato **Retangular** tem B e C até 35, E até 23, F até 32 e H até 36. O documento só lista o tipo de mesa Retangular.
- **Há mais perfis do que o documento conhece.** O cadastro corporativo tem cinco: Administrador, Secretaria Mesa, Secretaria Check-In, Painel e Participante. Os documentos tratam dos três primeiros; nenhuma tela usa os dois últimos. O código cita ainda um perfil Gestor, que não existe no cadastro ❓.
- **O destino depois de entrar depende do perfil.** GPE001 fala de uma tela inicial; o código leva as secretarias direto aos participantes do evento principal — e, se não houver evento principal, deixa-as paradas na tela de acesso 🔍.
- **A confirmação de presença pode ser reposta.** GPE005 só fala em removê-la; o código alterna nos dois sentidos.
- **Recuperar senha: link ou senha temporária.** GPE001 fala em link; a tela fala em senha temporária.
- **As planilhas não são conferidas como o documento diz.** GPE004 dá várias colunas das cargas de convidados e de confirmados como obrigatórias; o código lê as colunas pela posição, não confere o cabeçalho e só exige o nome. GPE003 descreve o histórico com uma coluna de ano; o código espera uma coluna por ano.
- **Funcionalidades que só o código tem:** importação de inscritos do CRM (`EVT-CAD-09`, do ticket `PDTIC25148-36`), exportação do mapa de assentos (`EVT-PAR-15`), filtros por legenda e por pessoa sem foto e o atalho para o cadastro da pessoa (`PDTIC25148-35`), o formato de mesa Retangular Invertido e a troca voluntária de senha.
- **Tamanhos de campo diferentes** entre documento e tela: nome do evento (255 e 100), local (255 e 200), codinome (255 e 100), CNPJ (12 e 14 dígitos). O cargo do usuário é obrigatório no documento e opcional na tela.

---

## 5. O que só o PO responde

As lacunas de maior alcance. As demais estão nos arquivos de detalhe.

1. **Visão do produto.** O N0 foi reconstruído: propósito, objetivos e personas são inferência, e não há indicador nem meta em fonte nenhuma.
2. **Para que servem os perfis Painel e Participante**, e se o perfil Gestor deveria existir.
3. **A exclusão da pessoa deve ser definitiva?** GPE003 diz que ela "passa a não ser exibida"; o código a apaga. No evento, a exclusão é lógica.
4. **O Cód. Contato é único?** Todo o reconhecimento de pessoas depende dele, e o sistema não o garante. Com o campo em branco, cada carga cria uma pessoa nova.
5. **As cargas de grupos de trabalho e de temas devem substituir tudo?** O documento não diz; o código apaga a base inteira a cada carga.
6. **Quem não confirmou presença deve receber legenda?** O código aplica as regras a todos os participantes do evento.
7. **A comparação das condições de legenda diferencia maiúsculas e acentos?** O código deixa isso por conta do banco.
8. **"Grupo Temático" é o grupo de trabalho ou o tema?** GPE006 e o ticket usam o termo de modos diferentes.
9. **A secretaria deve ver só o evento principal?** O documento diz que sim; nada no código a impede de abrir outro.
10. **Precisa haver trilha de auditoria?** Hoje não há.
11. **Volume esperado** — pessoas na base, participantes por evento — não consta em fonte nenhuma, e várias consultas trazem tudo de uma vez.
12. **Política de senha, validade da sessão e bloqueio por tentativas** são do cadastro corporativo; o GPE só exige 8 caracteres.

---

## 6. Decisões tomadas na conversão

Escolhas feitas para caber no padrão do engine. Todas reversíveis; estão aqui para o PO confirmar.

- **Estrutura**: 3 domínios e 6 Feature Sets, um por documento legado — decisão do responsável pela documentação, em 2026-09-30.
- **Perfil da instância**: `requisitos`, como as demais instâncias da PHL. Os N3 trazem, além do negocial, a seção técnica `## Implementação`, com o caminho do código de cada feature — é o lastro da engenharia reversa.
- **Nomes de feature**: verbo do vocabulário do engine, no infinitivo. Onde o documento legado usava outro verbo, o nome mudou e a `## Origem` do N3 guarda o nome antigo:

| Nome no documento legado | Feature |
|---|---|
| Efetuar Login | `ACE-AUT-01 — Autenticar Usuário` |
| Efetuar Logout | `ACE-AUT-02 — Encerrar Sessão` |
| Esqueci Minha Senha | `ACE-AUT-03 — Recuperar Senha` |
| Alterar senha do primeiro acesso | `ACE-AUT-04 — Alterar Senha` |
| Alterar imagem de perfil | `ACE-AUT-05 — Alterar Foto de Perfil` |
| Incluir Usuário · Incluir Pessoa · Incluir Evento · Incluir Participante | `ACE-USU-02 — Cadastrar Usuário` · `PES-CAD-02 — Cadastrar Pessoa` · `EVT-CAD-02 — Cadastrar Evento` · `EVT-PAR-02 — Cadastrar Participante` |
| Realizar Carga de GT · de Temas · de Histórico | `PES-CAD-05 — Carregar Grupos de Trabalho` · `PES-CAD-06 — Carregar Temas` · `PES-CAD-07 — Carregar Histórico de Participação` |
| Tornar Evento como Principal | `EVT-CAD-06 — Definir Evento Principal` |
| Carregar Lista de Convidados · de Confirmados | `EVT-CAD-07 — Carregar Convidados` · `EVT-CAD-08 — Carregar Confirmados` |
| Realizar Check-in | `EVT-PAR-03 — Registrar Check-in` |
| Marcar Assento do Participante | `EVT-PAR-08 — Atribuir Assento ao Participante` |
| Excluir Marcação de Assento do Participante | `EVT-PAR-09 — Remover Assento do Participante` |
| Realizar Atendimento | `EVT-PAR-10 — Registrar Atendimento` |
| Limpar Todas as Marcações de Assento do Participante | `EVT-PAR-11 — Liberar Todos os Assentos` |
| Remover confirmação de presença | `EVT-PAR-13 — Alterar Confirmação de Presença` |
| Listar Regras de Legendas | `EVT-LEG-01 — Consultar Configuração de Legendas` |
| Incluir Regra de Legenda · Editar Regra de Legenda | `EVT-LEG-02 — Adicionar Bloco de Legenda ao Evento` · `EVT-LEG-03 — Configurar Condições de Legenda` |
| Simular Execução das Regras de Legendas | `EVT-LEG-06 — Simular Aplicação de Legendas` |
| Executar Regras | `EVT-LEG-07 — Gerar Legendas do Evento` |

- **A gravação do mapa de assentos não é feature.** Atribuir, remover e liberar assentos se concluem pela gravação do mapa inteiro; ela está descrita em `EVT-PAR-08 — Atribuir Assento ao Participante`.
- **`EVT-PAR-12 — Buscar Pessoa na Mesa` é feature**, embora a busca seja feita sobre o que já está na tela: está no documento legado, com permissão própria, e entrega a localização do assento.
- **As três ações de legenda do participante** — consultar, alterar e remover — ficaram como três features, como no documento, embora a tela seja uma janela só.
- **Tickets do Jira citados em texto.** A `## Origem` dos N3 cita as chaves `PDTIC25148-…` sem link, porque nenhuma AIM foi aberta; a tabela de rastreabilidade do `modules/INDEX.md` está vazia por isso.
- **O critério CA03 do ticket `PDTIC25148-34`** aparece em duas features: o atalho de criação em `EVT-LEG-02 — Adicionar Bloco de Legenda ao Evento` e a criação em si em `EVT-LEG-12 — Cadastrar Bloco de Legenda`. Quando a AIM for aberta, decide-se a qual das duas ele pertence.

---

## 7. O que não foi feito

- **Contagem de Pontos de Função.** Nenhuma feature foi contada; as 55 estão em `global/CONTAGEM-PF.md` → *Pendências de contagem*.
- **AIMs dos tickets.** Em especial as dos três tickets em teste — `PDTIC25148-34`, `-35` e `-36` —, cujos critérios de aceite já estão confrontados com o código na `## Origem` dos N3 correspondentes.
- **Protótipos.** Não há; cada N3 aponta a tela implementada e a imagem do documento legado.
- **Requisitos não-funcionais, autorização, padrões de API, Design System e padrões de projeto.** `global/NFR.md`, `AUTHZ.md`, `API-PATTERNS.md`, `DESIGN-SYSTEM.md`, `PATTERNS.md`, `SIZING.md` e `ALI-AIE-MAP.md` continuam como os moldes do engine — nada foi derivado do código para eles.
- **Painel de pendências (PD) e plano de testes (QA).** Não foram rodados.
- **Catálogo completo de mensagens.** `global/MESSAGE-DICTIONARY.md` tem as mensagens que os cenários citam em passo de exibição; as demais estão literais nos N3.
- **Itens em aberto no Jira** não viraram feature: `PDTIC25148-21` (retrato dos dados dos participantes), `-24` (critérios por evento), `-26` (construtor de mesa), `-30` (API CRM) e `-31` (arrastar mais de uma cadeira).

---

## 8. Por onde começar

1. Levar os itens da **seção 1** a quem responde pela segurança do sistema — não dependem de especificação.
2. Decidir, com o time de desenvolvimento, quais itens da **seção 2** são defeito a corrigir. Para cada um que for, o N3 já descreve o comportamento atual; a correção entra por `PROMPT_4A`.
3. Validar o **N0** e a matriz de permissões dos seis N2 com o PO — são a régua do resto.
4. Rodar o `PROMPT_3A` nas features com mais lacunas de negócio, nesta ordem sugerida: `EVT-LEG-07 — Gerar Legendas do Evento`, `EVT-PAR-08 — Atribuir Assento ao Participante`, `EVT-CAD-07 — Carregar Convidados`, `PES-CAD-05 — Carregar Grupos de Trabalho` e `ACE-AUT-05 — Alterar Foto de Perfil`.
5. Abrir as AIMs dos três tickets em teste e, depois da validação dos N3, rodar a contagem.

---

*Links: [INDEX geral](./modules/INDEX.md) · [Visão de Produto](./global/N0_PRODUCT_VISION.md) · [Material da engenharia reversa](./arquivos/engenharia-reversa/README.md)*
