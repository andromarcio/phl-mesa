# 5. Orientações complementares para contagem

> Guia de Métricas da STI · Versão 1.3 (Dez/2025)

Este capítulo tem o propósito de apresentar diretrizes complementares ao Manual de Práticas de Contagem do IFPUG para contagens de pontos de função e reforçar pontos sensíveis nas contratações atuais que podem impactar significativamente o resultado de uma contagem em caso de falhas.

## 5.1. Contagem de pontos de função com múltiplas mídias

A contagem de PF de funcionalidades entregues em mais de uma mídia, na aplicação das regras de contagem de pontos de função definidas no *CPM*, tem levado a duas abordagens alternativas, a saber: *single instance* e *multiple instance*.

É importante enfatizar que o IFPUG reconhece ambas abordagens, *single instance* e *multiple instance*, para a aplicação das regras definidas no *CPM*. A determinação da contagem de PF seguindo a abordagem *multiple instance* ou *single instance* depende da avaliação dos especialistas em contagem da contratante em acordo com os especialistas da contratada.

As estimativas e contagens de PF abordadas neste documento são baseadas em *multiple instance*, com exceção dos casos de consultas em .pdf, .doc, .xls e consultas idênticas em tela e papel, que serão consideradas uma única funcionalidade.

A seguir são descritos os termos comuns definidos pelo:

- Canal: também se refere a mídia. Múltiplos canais é sinônimo de múltiplas mídias.
- Mídia: descreve a maneira como os dados ou informações se movimentam para dentro e para fora de uma fronteira de aplicação, por exemplo, apresentação de dados em tela, impressora, arquivo, voz. Este termo é utilizado para incluir, dentre outros, diferentes plataformas técnicas e formatos de arquivos como diferentes mídias.
- Múltiplas Mídias: quando a mesma funcionalidade é entregue em mais de uma mídia. Frequentemente, apenas uma mídia é requisitada para um usuário específico em um determinado momento, por exemplo consulta de extrato bancário via Internet como oposto a consulta de extrato bancário via terminal do banco.
- Multi-Mídia: quando mais de uma mídia é necessária para entregar a funcionalidade, por exemplo, uma nova notícia publicada na Internet que é apresentada em vídeo e texto. Observe que a notícia completa só é apresentada para o usuário se ele ler o texto e assistir o vídeo.
- Abordagem *Single Instance*: esta abordagem não reconhece que a mídia utilizada na entrega da função transacional é uma característica de diferenciação na identificação da unicidade da função transacional. Se duas funções entregam a mesma funcionalidade usando mídias diferentes, elas são consideradas a mesma funcionalidade em uma contagem de pontos de função.
- Abordagem *Multiple Instance*: esta abordagem especifica que o tamanho funcional é obtido no contexto do objetivo da contagem, permitindo uma função de negócio ser reconhecida no contexto das mídias que são requisitadas para que a funcionalidade seja entregue. A abordagem *multiple instance* reconhece que a mídia para entrega constitui uma característica de diferenciação na identificação da unicidade da função transacional.

Os cenários descritos nas seções seguintes não representam uma lista completa de situações de múltiplas mídias. O entendimento dos exemplos a seguir facilitará o entendimento de outros cenários envolvendo múltiplas mídias. Deve-se atentar que o cenário de múltiplas mídias existe somente no contexto de um único sistema (fronteira). Quando há mais de uma fronteira envolvida, conta-se a função em cada um dos sistemas.

### 5.1.1. Cenário 1 - Mesmos dados apresentados em tela e impressos:

Neste cenário, uma aplicação apresenta uma informação em uma consulta em tela. A mesma informação pode ser impressa, caso requisitado pelo usuário, na tela em questão.

Nesses casos, sugere-se a abordagem *single instance*, considerando que dados idênticos sendo apresentados em tela e em relatório impresso devem ser contados como uma única função. Caso as lógicas de processamento da consulta em tela e do relatório em papel sejam distintas, o processo elementar não é único e, portanto, a funcionalidade será contada duas vezes (*multiple instance*). Neste caso, duas funções são contadas: apresentação de dados em tela e apresentação de dados impressos.

### 5.1.2. Cenário 2 - Mesmos dados de saída como dados em arquivo e relatório impresso:

Uma aplicação grava dados em um arquivo de saída e imprime um relatório com informações idênticas às gravadas no arquivo.

Nesses casos, sugere-se a utilização da abordagem *single instance* considerando que os dados impressos e os dados apresentados no arquivo de saída sejam idênticos e que a ferramenta de desenvolvimento apoie a geração dessas múltiplas saídas. Assim, apenas uma funcionalidade será incluída na contagem de pontos de função. Caso as lógicas de processamento da geração do arquivo de saída e do relatório em papel sejam distintas, o processo elementar não é único e, portanto, a funcionalidade será contada duas vezes. Além disso, se a geração das múltiplas saídas não seguirem o padrão da ferramenta de desenvolvimento e tiverem que ser customizadas para o cliente, então será utilizada a abordagem *multiple instance*.

### 5.1.3. Cenário 3 - Mesmos dados de entrada batch e on-line:

Uma informação pode ser carregada na aplicação por meio de dois métodos: arquivo *batch* e entrada *on-line*. O processamento do arquivo *batch* executa validações durante o processamento, da mesma forma que o processamento da entrada *on-line* também executa validações das informações. Neste caso, sugere-se a utilização da abordagem *multiple instance*, que conta duas funcionalidades: a entrada de dados *batch* e a entrada de dados *on-line*. Geralmente, a lógica de processamento utilizada nas validações em modo *batch* é diferente da lógica de processamento das validações nas entradas de dados *on-line*.

### 5.1.4. Cenário 4 - Múltiplos canais de entrega da mesma funcionalidade:

Numa estratégia de desenvolvimento de software orientada a serviços, é comum que a camada de backend seja toda exposta para consumo por sistemas externos, além de ser também consumida pela sua camada de front-end. Em não existindo diferença de lógica ou campos quando a funcionalidade é acionada via tela por um usuário humano ou via sistema pelo webservice, deve-se contar sempre uma única função.

### 5.1.5. Cenário 5 - Relatório em múltiplos formatos:

Um relatório deve ser entregue em diferentes formatos, por exemplo: um arquivo *html* e um arquivo com valores separados por vírgula (.csv).

Nestes casos, conforme sugerido na abordagem *multiple instance*, considera-se a ferramenta utilizada na geração dos relatórios. Se a equipe de desenvolvimento precisar desenvolver o relatório nos dois formatos na ferramenta em questão, serão contadas duas funcionalidades. No entanto, se a ferramenta de desenvolvimento suportar um gerador de relatórios que o usuário visualize o relatório em tela e o gerador permita ao usuário imprimir o relatório, salvar em *html* ou salvar no formato de valores separados por vírgula, então se contará apenas uma vez (*single instance*), observando que a funcionalidade será da ferramenta e não da aplicação.

## 5.2. Log, trilha de auditoria e histórico

O objetivo dessa sessão é descrever orientações sucintas a respeito de contagem de log, trilha de auditoria e histórico.

### 5.2.1. Log:

Conceituamos o termo “Log” como o registro de procedimentos ou ações realizadas pela aplicação, em determinado período de tempo, com o objetivo de apoiar a auditoria do ambiente tecnológico e a identificação das causas raízes de falhas em sistemas. Diante desse conceito, definimos que o Log não deve ser mensurado com Pontos de Função, já que ele não armazena informações negociais reconhecidas pelo usuário da aplicação.

### 5.2.2. Trilha de auditoria:

Conceituamos “Trilha de Auditoria” como a funcionalidade que tem o objetivo de armazenar informações referentes às ações realizadas pelos usuários da aplicação no passado, de modo que seja possível apurar quais foram as ações executadas quando da utilização do sistema.

Para isso, devem existir no mínimo as informações para identificar quem realizou a ação, quando e o que foi realizado, além de outras informações que o usuário da aplicação defina como necessárias.

A trilha de auditoria deve ser solicitada pelo usuário da aplicação e, para a contagem, deve existir funcionalidade de consulta a tais dados.

Caso a trilha de auditoria faça parte da política corporativa de segurança da informação do contratante, ela deve ser considerada como um requisito não funcional e, portanto, não será mensurável em ponto de função.

Diante do exposto, a principal diferença entre o Log e a Trilha de Auditoria é:

- Log: apoia a coleta de informações no âmbito tecnológico, ou seja, em problemas decorrentes da arquitetura tecnológica que precisam ser investigados, por meio da análise do conjunto de procedimentos executadas pela aplicação, como exemplo a baixa performance no sistema, travamentos e outros comportamentos inesperados.
- Trilha de Auditoria: apoia a auditoria para os dados de negócio, armazenando informações das ações realizadas pelo usuário na aplicação.

### 5.2.3. Histórico:

Conceituamos “Histórico” como um registro de estados com informações anteriores de um registro em determinado momento. O usuário poderá consultar a evolução dessas informações em uma linha do tempo e sua existência é justificada pelo negócio. Assim, para fazer parte do tamanho funcional, deve ser solicitado pelo gestor e deverá existir funcionalidade de consulta a tais dados.

A função de consulta aos dados de um histórico deverá ser contada de acordo com as regras de contagem das funções transacionais do *CPM*.

Não devem ser consideradas na contagem funções de transação separadas para incluir, alterar e excluir as informações históricas, pois o armazenamento dessas informações é parte integrante das mesmas funcionalidades que processam os dados de negócio. Apenas quando o histórico for mantido de forma independente do registro principal, por exemplo no caso do ALI principal ter sido excluído, o histórico se torna um ALI independente e não um registro lógico do ALI relacionado.

## 5.3. Arquivos para processamento

É um requisito bastante comum que uma aplicação se comunique com outras trocando dados através de arquivos (neste caso o termo arquivo é o de um arquivo para o sistema operacional, não de arquivo lógico para a APF). Estes arquivos possuem leiaute pré-definido e acordado entre as aplicações e podem ser arquivos texto com campos de tamanho fixo, arquivos texto com campos delimitados por caracteres especiais, arquivos XML, etc. Um exemplo é a Solução Integradora que recebe mensalmente dados de produção de atendimento dos vários Departamentos Regionais através do envio de arquivos CSV por cada DR. Provavelmente, cada DR gera o arquivo a ser enviado à Solução Integradora através de um sistema distinto.

O primeiro passo na análise deste cenário é delimitar as fronteiras dos sistemas envolvidos: a Solução Integradora e o sistema do DR que produz o arquivo a ser carregado.

O arquivo gerado para processamento não deve ser contado como arquivo lógico (nem ALI, nem AIE) em nenhum dos sistemas, pois não representa requisitos de armazenamento de nenhum deles, mas sim requisitos de processamento que serão medidos como transações.

Do ponto de vista do sistema do DR (origem) que produz o arquivo para envio à Solução Integradora existe meramente um relatório, que em vez de impresso, está em formato CSV. Mede-se a transação que é responsável por gerar o arquivo como uma CE ou SE.

Do ponto de vista da Solução Integradora (destino), o processamento do arquivo carregado é classificado como EE, que cumpre o papel de uma tela em que o usuário poderia digitar os dados presentes no arquivo carregado.

Atenção especial quando o processamento do arquivo recebido contiver várias lógicas de processamento distintas para cada tipo de informação a ser processada. Nesse caso, podem existir várias EE, em vez de uma única. Exemplo: o arquivo de produção de serviços de Atendimentos de Tecnologia e Inovação processado pela Solução Integradora possui cinco tipos de registro: atendimento, produção, cliente PF, cliente PJ e parceiros. Cada tipo de registro possui um conjunto distinto de atributos e validações específicas. Portanto o processamento do arquivo abrangeria cinco EEs. No entanto, três destes tipos de registro permitem dois tipos de operação distintas no processamento: inclusão de registro e exclusão de registro. Então, para cada um dos três tipos de registro com duas operações possíveis se contaria uma EE, somando com a EE de processamento dos outros dois tipos de registro que possuem um único tipo de operação, chega-se a um total de 8 EEs.

Neste exemplo do tipo de operação da Solução Integradora, o tipo de operação com valor branco indica que o registro será incluído (caso não exista) ou atualizado (caso já exista), porém na ótica da APF conta-se uma única transação, pois a decisão de que ação tomar é interna à transação, não do ponto de vista externo (do usuário). Caso houvesse a distinção explícita dos tipos de operação inclusão e alteração na definição de leiaute do arquivo, aí sim se contaria duas transações.

Um requisito comum no processamento de arquivo é o de gerar um relatório de erros ou de críticas com as situações de erro ou exceção ocorridos durante o processamento do arquivo recebido. Nesse caso, o relatório é parte do requisito de processamento do arquivo e deve ser contado como parte da EE original. Os erros listados neste relatório são como mensagens de erro em uma tela de entrada de dados.

## 5.4. API/Webservices

Uma API (ou Interface de Programação de Aplicativos) é um conjunto de rotinas e padrões estabelecidos por um software para uso de suas funções por programas que não querem se envolver nos detalhes de implementação, apenas usar seus serviços. A API é composta por funções acessíveis somente via programação e que permitem usar características do software às vezes não disponível ao usuário final. Um webservice é um exemplo de API que permite a interação entre sistemas na plataforma web. Uma DLL no sistema operacional Windows é um exemplo de API que possibilita a interação de um aplicativo com outro.

Delimitando o contexto, há um sistema que provê serviços via API e outro que consome estes serviços. Do ponto de vista da APF, o consumidor da API é um usuário do primeiro sistema. Porém há casos em que a API é criada exclusivamente para consumo do próprio sistema. Por exemplo, a lógica de cálculo do dígito verificador do CPF foi implementada numa API do sistema e é consumida somente por ele. Neste caso não há funções a serem medidas relativas à API, pois um sistema não pode ser usuário de si mesmo.

Do ponto de vista do sistema usuário da API, não há medição de funções de transação para a API. Há casos em que o sistema usa a API com a finalidade de referenciar dados que estão armazenados no sistema origem. Se o uso da API foi por uma decisão de implementação, e um acesso direto à tabela origem dos dados também funcionasse, os dados referenciados via API são contados como AIE no sistema usuário. Se os dados consumidos não puderem ser acessados diretamente porque é necessário conhecer regras do negócio da origem para derivar os dados, então não se mede estes dados como AIE. Neste caso e para todas as outras situações de uso da API pelo sistema consumidor, a influência na medição funcional do consumidor se dará apenas na complexidade da sua transação que dispara o uso da API, considerando os campos passados para e recebidos da API como tipos de dados desta transação.

Do ponto de vista do sistema origem que fornece a API, as funções expostas ao mundo externo serão medidas como transações, conforme sua intenção principal seja atualizar dados internos (EE) ou apresentar dados ao exterior (CE ou SE). Na avaliação da complexidade da transação, considera-se os parâmetros de entrada e saída como seus tipos de dados (sem repetição).

Exemplo 1: Os Correios possuem uma função implementada através de um webservice que fornece o logradouro, bairro, cidade, estado de um determinado CEP. Esta função será medida como uma CE para o sistema dos Correios, pois é uma simples recuperação de dados e os parâmetros do webservice contam como seus tipos de dados. Na loja virtual Americanas.com, durante o registro de um novo cliente, ao usuário informar o CEP do cliente, o sistema de comércio eletrônico invoca o serviço dos Correios para recuperar o logradouro, bairro, cidade e estado. Para o sistema de comércio eletrônico da Americanas.com, a função Registrar Cliente será contada como uma EE, e na classificação de sua complexidade, o AIE CEP será contado como mais um arquivo referenciado. A passagem e recebimento de parâmetros para o webservice não computam como seus tipos de dados.

Exemplo 2: Os Correios possuem uma função implementada através de um webservice que fornece o valor do Sedex, dados o CEP origem e destino, peso e dimensões da encomenda. Assumindo que o valor do serviço é fruto de um cálculo, esta função será contada como uma SE para o sistema dos Correios, e os parâmetros do webservice contam como seus tipos de dados. Na loja virtual Americanas.com, durante o processo de compra, o cliente é informado do valor da remessa da sua encomenda via Sedex dos Correios. Para o sistema de comércio eletrônico da Americanas.com, a função Compra será contada como uma EE. Durante a compra há o acionamento do webservice dos Correios que fornece o valor do Sedex. A transação continua a ser a mesma (Compra), e na classificação de sua complexidade, os campos informados e recebidos dos Correios serão contados como seus tipos de dados. Não se mede os dados derivados do Sedex como AIE.

Exemplo 3: O sistema de Internet Banking necessita atualizar o saldo da conta corrente sempre que o cliente efetuar um pagamento de boleto. Porém o sistema responsável pelo saldo da conta corrente é o Conta Corrente. Atualizar o saldo de uma conta corrente compreende diversas regras de negócio, por exemplo: saber o saldo disponível para a operação envolve considerar o saldo das aplicações com resgate automático e o limite do cheque especial; toda atualização de saldo deve também gerar um lançamento de movimentação da conta corrente. Enfim, todo sistema que pretendesse atualizar o saldo da conta diretamente deveria ter completo conhecimento das regras de negócio envolvidas com a sensibilização do saldo, o que na prática é inviável. O Conta Corrente fornece então uma função para atualização de saldo da conta corrente que pode ser usada por quaisquer outros sistemas sem que estes precisem conhecer as regras de negócio envolvidas. Para a transação Pagar Boleto (EE) do Internet Banking o uso da função de atualização de saldo implica na contagem de tipos de dados adicionais relativos aos parâmetros do webservice.

## 5.5. Principais falhas da contagem identificadas

A listagem abaixo apresenta situações que constituem falhas de contagem:

- Contar DER (Dado Elementar Referenciado) para variáveis de paginação, número de páginas e informação de posicionamento;
- Contar DER para ajudas de navegação como habilidade de navegar com uma lista utilizando “anterior”, “próximo”, “primeiro”, “último” e seus equivalentes gráficos;
- Contar mais de um DER por função de transação para a habilidade de iniciar ações quando há múltiplos meios para isso;
- Contar mais de um DER quando a função de transação tem capacidade de enviar várias mensagens;
- Considerar fluxos alternativos como processos elementares distintos não levando em consideração as regras de identificação e unidade do processo elementar;
- Considerar transações que atualizam dados de código;
- Identificação de um ALI para armazenamento de dados de código;
- Relacionar processos elementares com telas ou abas de uma transação não levando em consideração as regras de identificação e unicidade do processo elementar.
