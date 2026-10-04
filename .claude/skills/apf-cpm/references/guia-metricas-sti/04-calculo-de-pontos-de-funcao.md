# 4. Cálculo de pontos de função

> Guia de Métricas da STI · Versão 1.3 (Dez/2025)

Este capítulo tem como propósito descrever os diversos tipos de iniciativas de sistemas e definir métricas para seu dimensionamento baseadas nas regras de contagem de pontos de função do *CPM*.

Existe a previsão para tratamento dos casos onde não há a necessidade de contratar todas as fases do ciclo de vida do sistema. Dessa forma, a contratada será remunerada pela contagem de pontos de função considerando apenas os percentuais das fases contratadas, conforme os níveis percentuais sugeridos na Tabela 7, seção 6.2. Exemplo: para uma nova iniciativa de desenvolvimento de um sistema de treinamentos, que não exista a intenção de contratar as fases de refinamento e de testes, a contratada será remunerada pela contagem de pontos de função desconsiderando os percentuais dessas fases.

## 4.1. Iniciativa de desenvolvimento

É a iniciativa para desenvolver e entregar a primeira versão de uma aplicação de sistema. Seu tamanho funcional é a medida das funcionalidades entregues ao usuário no final da iniciativa. Também são consideradas as funcionalidades de conversão de dados. Segue a fórmula de cálculo utilizada no dimensionamento de iniciativas de desenvolvimento de sistemas:

```
PF_DESENVOLVIMENTO = PF_INCLUIDO + PF_CONVERSÃO
```

## 4.2. Iniciativa de melhoria

A iniciativa de melhoria (iniciativa de melhoria funcional ou manutenção evolutiva), está associado às mudanças em requisitos funcionais da aplicação, ou seja, à inclusão de novas funcionalidades, alteração ou exclusão de funcionalidades em aplicações implantadas. Trata-se de modificação de um produto de software existente para mantê-lo funcionando adequadamente em um ambiente que sofre mudanças.

A iniciativa de melhoria é considerada um tipo de iniciativa de manutenção adaptativa com mudanças em requisitos funcionais da aplicação, ou seja, com funcionalidades incluídas, alteradas ou excluídas na aplicação, segundo o *CPM* 4.3.1.

Este guia separa a iniciativa de melhoria (quando as mudanças são associadas aos requisitos funcionais) da iniciativa de manutenção adaptativa (quando as mudanças estão associadas aos requisitos não funcionais da aplicação). Uma iniciativa de melhoria consiste em demandas de criação de novas funcionalidades (grupos de dados ou processos elementares), demandas de exclusão de funcionalidades (grupos de dados ou processos elementares) e demandas de alteração de funcionalidades (grupos de dados ou processos elementares) em aplicações implantadas em produção. Segue a fórmula de cálculo utilizada no dimensionamento de iniciativas de melhoria de sistemas:

```
PF_MELHORIA = PF_INCLUIDO + (FI x PF_ALTERADO) + (0,30 x PF_EXCLUIDO) + PF_CONVERSÃO
```

a) FI (Fator de Impacto) pode variar de 50% a 90% conforme condições abaixo:

- FI = 50% para funcionalidade de sistema desenvolvida ou mantida por meio de uma iniciativa de melhoria pela empresa contratada.
- FI = 75% para funcionalidade de sistema não desenvolvida ou mantida por meio de uma iniciativa de melhoria pela empresa contratada e sem necessidade de redocumentação da funcionalidade.
- FI = 90% para funcionalidade de sistema não desenvolvida ou mantida por meio de uma iniciativa de melhoria pela empresa contratada e com necessidade de redocumentação da funcionalidade. FI = 90% representa a adição de 15% como fator de redocumentação ao Fator de Impacto anterior (75%). Nesse caso, a contratada deve redocumentar a funcionalidade mantida, gerando a documentação completa da mesma, aderente ao processo de software da contratante. Se houver uma nova demanda de iniciativa de melhoria na funcionalidade em questão, será considerado que a contratada desenvolveu a funcionalidade. Observe que o percentual de 90% apenas será considerado na primeira demanda de iniciativa de melhoria em cada funcionalidade

Este guia propõe um fator de redocumentação menor para iniciativas de manutenção (melhoria, corretiva e adaptativa) do que o fator proposto em iniciativas específicas de redocumentação seção 4.12 deste guia. Isso porque, em iniciativas de manutenção de uma funcionalidade sem documentação, é necessário realizar o entendimento da funcionalidade para poder modificá-la e testá-la, ou seja, é necessário realizar a engenharia reversa da funcionalidade para executar os testes corretamente. Assim sendo, a redocumentação requisitada em iniciativas de melhoria requer um esforço menor do que em iniciativas de redocumentação, descritos na seção 4.12, onde é necessário remunerar todo o esforço de engenharia reversa e a atividade de documentação. Em iniciativas de manutenção, o fator de 15% está remunerando apenas a atividade de documentação.

O PF_INCLUIDO e PF_ALTERADO preveem a contratação e realização de todas as fases do processo de desenvolvimento de software. Caso alguma fase não seja contratada ou realizada, deve-se aplicar, em cada um deles, um redutor que corresponde ao percentual da fase não contratada ou não realizada, conforme percentuais inseridos na Tabela 7, seção 6.2.

### 4.2.1. Observações sobre alterações:

a) Função de dados: Uma função de dados (Arquivo Lógico Interno ou Arquivo de Interface Externa) é considerada alterada quando houver inclusão ou exclusão de Tipos de Dados (TD). De acordo com o glossário do *CPM* 4.3.1, um Tipo de Dados (*DET – Data Element Type*) é um atributo único, reconhecido pelo usuário e não repetido. Também é considerada alterada se algum tipo de dado sofrer mudança de tamanho (número de posições) ou tipo de campo (por exemplo: mudança de numérico ou alfanumérico), caso a mudança decorra de alteração de regra de negócio.

b) Função de transação: Uma função transacional (Entrada Externa, Consulta Externa e Saída Externa) é considerada alterada, quando a alteração contemplar:

- Mudança de tipos de dados;
- Mudança de arquivos referenciados;
- Mudança de lógica de processamento.

c) Sobre a lógica de processamento: O *CPM* 4.3.1 define lógica de processamento como requisitos especificamente solicitados pelo usuário para completar um processo elementar. Esses requisitos devem incluir uma ou mais das seguintes ações:

- Condições são analisadas para verificar quais são aplicáveis;
- Dados derivados são criados através da transformação de dados existentes, para criar dados adicionais;
- Dados ou informações de controle são recuperados;
- Dados são filtrados e selecionados através da utilização de critérios;
- Dados são reordenados;
- Fórmulas matemáticas e cálculos são executados;
- O comportamento do sistema é alterado;
- Preparar e apresentar informações para fora da fronteira;
- Receber dados ou informações de controle que entram pela fronteira da aplicação;
- Um ou mais ALIs ou AIEs são referenciados;
- Um ou mais ALIs são atualizados;
- Validações são executadas;
- Valores equivalentes são convertidos.

### 4.2.2. Outros tipos de funções alteradas:

Este guia considera como função alterada qualquer mudança em funcionalidades da aplicação devido às mudanças de regras de negócio. Por exemplo, uma funcionalidade de cadastro envolvia a inclusão de um telefone do gerente. Devido a mudanças no processo de negócio, a funcionalidade deve sofrer uma manutenção para cadastrar dois telefones do gerente. Desta forma, o guia considera esta função como uma Entrada Externa alterada, PF_ALTERADO em uma iniciativa de melhoria, mesmo que não existam mudanças de lógica de processamento, de tipos de dados ou de arquivos referenciados. Serão tratadas como manutenções adaptativas apenas as manutenções que implicarem exclusivamente em mudanças em requisitos não funcionais. Se uma mesma funcionalidade tiver mudanças em requisitos funcionais e não funcionais, esta deve ser contada apenas uma vez, como função alterada em uma iniciativa de melhoria.

## 4.3. Iniciativa de migração de dados – PF_CONVERSÃO

As iniciativas de migração de dados devem ser contadas como nova iniciativa de desenvolvimento de um sistema, seguindo a fórmula abaixo:

```
PF_CONVERSÃO = PF_INCLUIDO
```

Uma iniciativa de migração deve contemplar minimamente: as Entradas Externas – considerando as cargas de dados nos ALI – e, caso seja solicitado pelo usuário, os relatórios gerenciais das cargas, que serão contados como Saídas Externas. Todas as contagens de PF devem ser realizadas com base nas funcionalidades requisitadas e recebidas pelo usuário.

É importante ressaltar que as funções de dados associadas aos dados atualizados não devem ser contadas, considerando que não há mudanças nas estruturas dos Arquivos Lógicos Internos.

## 4.4. Manutenção corretiva

Mesmo com a execução de atividades de garantia da qualidade, pode-se identificar defeitos na aplicação entregue. A manutenção corretiva altera o software para correção de defeitos. Encontra-se nesta categoria, as demandas de correção de erros (bugs) em funcionalidades de sistemas em produção.

É importante destacar que as demandas de manutenção corretiva frequentemente precisam ser atendidas com urgência. Assim, o grau de criticidade da iniciativa poderá trazer impacto nas estimativas de custo e esforço.

Quando o sistema em produção tiver sido desenvolvido pela contratada, a manutenção corretiva será do tipo Garantia se estiver no período de cobertura e em conformidade com as demais condições de garantia previstas em contrato. Caso não exista cláusula contratual de garantia, deve ser considerada a garantia preconizada por lei (Código do Consumidor). Desta forma, não é aplicável a mensuração de pontos de função, e, tampouco, o pagamento destas manutenções.

Quando o sistema estiver fora da garantia ou não tenha sido desenvolvido pela empresa contratada, deverá ser estimado e calculado o tamanho da iniciativa de manutenção corretiva. Nestes casos, a aferição do tamanho em pontos de função da funcionalidade ou das funcionalidades corrigidas deve considerar um fator de impacto (FI) sobre o PF_ALTERADO.

```
PF_CORRETIVA = FI x PF_ALTERADO
```

a) Fator de Impacto (FI):

- 50% quando estiver fora da garantia e a correção for feita pela mesma empresa que desenvolveu a funcionalidade.
- 75% quando estiver fora da garantia e a correção for feita por empresa diferente daquela que desenvolveu a funcionalidade.

As demandas de manutenção corretiva não contemplam atualização de documentação da funcionalidade corrigida, pois este guia considera que, normalmente, manutenção corretiva não se refere a erros de requisitos. Caso seja erro em requisitos, essa demanda deve ser tratada como iniciativa de melhoria (alteração de funcionalidade), descrito na seção 4.2. Porém, quando o erro for causado por documentação dúbia ou imprecisa (elaborada pela contratada) da funcionalidade corrigida, a manutenção corretiva poderá contemplar os ajustes na documentação, mesmo fora da garantia, mediante negociação entre as partes.

Caso seja demandada a redocumentação da funcionalidade corrigida, porque a documentação não existe ou está desatualizada, deve-se adicionar ao FI um fator de redocumentação de 15%, conforme descrito na seção 4.2.

## 4.5. Mudança de plataforma

São considerados nesta categoria, iniciativas que tratam a migração de software para outra plataforma. Por exemplo, um sistema legado em COBOL que necessita ser redesenvolvido em JAVA; o banco de dados de um sistema legado que precisa ser migrado para o DB2.

Recomenda-se enfaticamente a realização da análise de impacto das mudanças propostas, para efeito de determinação do percentual adequado para aplicação sobre o total de pontos de função das funcionalidades impactadas. Por exemplo, em uma análise de impacto pode ser identificado que não haverá mudanças no código-fonte ou em função transacional, sendo necessário apenas testar o sistema, então deve-se utilizar um percentual contemplando apenas a fase de testes. No caso de o teste apontar a necessidade de atualizar alguma função transacional, não deve ser contado o esforço do teste, mas sim o esforço abordado nesta seção, conforme as fórmulas apresentadas nos tópicos seguintes.

As próximas subseções apresentam os tipos de iniciativas de mudança de plataforma. As iniciativas de mudança de plataforma que se enquadram em mais de uma subseção, devem ser contados apenas uma vez, considerando o tipo de iniciativa com maior contagem de pontos de função.

### 4.5.1. Mudança de plataforma – Linguagem de programação:

Nos projetos de redesenvolvimento de sistemas em uma nova linguagem de programação (também conhecidos como migração ou modernização de plataforma ou refatoração), a contagem das funções de dados e de transação seguirão os critérios a seguir:

a) Redesenvolvimento sem Evolução Funcional:

Ocorre quando o sistema é reescrito em uma nova linguagem ou plataforma sem alterações nas funcionalidades existentes e mantendo-se a mesma base de dados. Sendo assim, temos as seguintes regras quanto a funções de dados e transações:

- Funções de Dados:
  - Para fins de Remuneração: Não devem ser contadas pois não há esforço de desenvolvimento ou alteração na estrutura lógica dos dados.
  - Para fins de Documentação: Devem ser contadas com Fator de Impacto (FI) de 100% para compor o tamanho funcional total da aplicação em seu estado final.
- Funções de Transação (Entradas, Saídas e Consultas Externas):
  - Devem ser contadas como em uma iniciativa de desenvolvimento, ou seja, com Fator de Impacto (FI) de 100%. A justificativa é que toda a lógica de processamento é reconstruída na nova linguagem, resultando em uma nova entrega funcional para o usuário.

b) Redesenvolvimento com Melhorias Funcionais:

Ocorre quando durante o projeto de reescrita aproveita-se para incluir melhorias ou novas funcionalidades que impactam o comportamento original do sistema. É necessário também que as funções de dados sejam impactadas e/ou incluídas. Sendo assim, temos as seguintes regras quanto a funções de dados e transações:

- Funções de Dados:
  - Para fins de Remuneração: As funções de dados que forem adicionadas ou modificadas pela melhoria funcional poderão ser contadas. Recomenda-se a aplicação de um Fator de Impacto (FI) de 50% quando a função de dados for impactada, alinhando-se ao critério mínimo para projetos de melhoria apresentado neste documento e representando o esforço de alteração. Já para os casos de funções de dados inteiramente e totalmente incluídas, recomenda-se a aplicação de um Fator de Impacto (FI) de 100%, alinhando-se de desenvolvimento apresentado neste documento.
  - Para fins de Documentação: Todas as funções de dados (mantidas, alteradas e novas) devem ser contadas com FI de 100% para registrar o tamanho funcional completo da aplicação.
- Funções de Transação:
  - A regra é a da letra ‘a’ desta seção: Todas as funções de transação (mantidas, alteradas e novas) são contadas como em uma iniciativa de desenvolvimento (FI de 100%).

c) Outras regras:

Outro ponto a ser observado são as fases contratadas. Caso a iniciativa já possua documentação de requisitos, a fase de refino não será contratada. Deve-se considerar apenas os percentuais das fases contratadas, aplicando-se sobre o PF_INCLUIDO o fator de ponderação previsto na Tabela 7, seção 6.2.

```
PF_REDESENVOLVIMENTO_LINGUAGEM = PF_INCLUÍDO + PF_CONVERSÃO
```

Este guia recomenda a supressão do PF_CONVERSÃO da fórmula de contagem de pontos de função de iniciativas de redesenvolvimento quando for caracterizado um esforço relativamente maior dessa atividade, conforme descrito na seção 3.4.

### 4.5.2. Mudança de plataforma – Banco de dados:

Nesta categoria encontram-se as demandas de redesenvolvimento de sistemas para utilizar um outro sistema gerenciador de banco de dados.

Observe que caso não exista mudança nas funções de dados, ou seja, o banco de dados da aplicação seja mantido, então as funções de dados não devem ser contadas. No entanto, nesse caso, deve ser realizada a contagem das funções de dados a fim de compor a documentação da contagem final da iniciativa.

Caso a iniciativa já possua documentação de requisitos, então a fase de refino não deve ser contratada. É importante destacar que isso se aplica a qualquer fase que não se deseja contratar. Deve-se considerar apenas os percentuais das fases contratadas, aplicando-se sobre o PF_INCLUIDO o fator de ponderação previsto na Tabela 7, seção 6.2. Desta forma, a seguinte forma deve ser utilizada:

```
PF_REDESENVOLVIMENTO_BD_RELACIONAL = (PF_ALTERADO X 0,30) + PF_CONVERSÃO
```

O PF_ALTERADO deve considerar apenas as funcionalidades impactadas. As funcionalidades que possuem apenas demandas de testes, devem ser contadas usando o percentual da fase de testes (ver Tabela 7 – seção 6.2).

Indica-se tratar o PF_CONVERSÃO dentro da mesma iniciativa. Geralmente a estrutura de dados não é alterada, desta forma não contamos as funções de dados.

## 4.6. Atualização de versão

São consideradas nesta categoria, demandas para uma aplicação existente - ou parte de uma aplicação existente - executar em versões diferentes de browsers (ex: Internet Explorer, Firefox, Chrome, etc) ou de linguagens de programação (ex: versão mais atual do JAVA). Também são consideradas nesta categoria atualização de versão de banco de dados.

Outro ponto a ser observado é a classificação, em alguns casos, dessas demandas como componente interno reusável (seção 4.15).

Recomenda-se enfaticamente a realização da análise de impacto das mudanças propostas para efeito de determinação do percentual adequado para aplicação sobre o total de pontos de função das funcionalidades impactadas. Por exemplo, em uma análise de impacto, pode ser identificado que não haverá mudanças no código-fonte ou em função transacional, sendo necessário somente testar o sistema, então deve-se utilizar um percentual contemplando apenas a fase de testes. No caso de o teste apontar a necessidade de atualizar alguma função transacional, não deve ser contado o esforço do teste, mas sim o esforço abordado nesta seção, conforme as fórmulas apresentadas nas subseções seguintes.

### 4.6.1. Atualização de versão – Linguagem de programação:

Nesta categoria encontram-se as demandas de atualização de versão de linguagem de programação de sistemas. As funções de dados não devem ser contadas. Estas demandas devem ser dimensionadas de acordo com a fórmula a seguir.

```
PF_ATUALIZAÇÃO_VERSÃO_LINGUAGEM = PF_ALTERADO x 0,30
```

O PF_ALTERADO deve considerar apenas as funcionalidades impactadas. As funcionalidades que possuem apenas demandas de testes, devem ser contadas usando o percentual da fase de testes (ver Tabela 7 – seção 6.2).

### 4.6.2. Atualização de versão – Browser:

Nesta categoria encontram-se as demandas de atualização de aplicações Web para executar em novas versões de um mesmo browser e para suportar a execução em mais de um browser. É importante destacar que este tipo de procedimento usualmente é realizado quando é necessário resolver algum problema de incompatibilidade. As funções de dados não devem ser contadas. Estas demandas devem ser dimensionadas de acordo com a fórmula abaixo.

```
PF_ATUALIZAÇÃO_VERSÃO_BROWSER = PF_ALTERADO x 0,30
```

O PF_ALTERADO deve considerar apenas as funcionalidades impactadas. As funcionalidades que possuem apenas demandas de testes, devem ser contadas usando o percentual da fase de testes (ver Tabela 7 – seção 6.2).

Essas atualizações podem implicar em manutenções em componentes específicos da plataforma utilizada. Nesse caso, a demanda deve ser contada como componente interno reusável, descrita na seção 4.15 deste guia.

### 4.6.3. Atualização de versão – Banco de dados:

Nesta categoria encontram-se as demandas de atualização de versão do sistema gerenciador de banco de dados. As funções de dados não devem ser contadas. Estas demandas devem ser dimensionadas de acordo com a fórmula a seguir.

```
PF_ ATUALIZAÇÃO_VERSÃO_BD = PF_ALTERADO x 0,30
```

O PF_ALTERADO deve considerar apenas as funcionalidades impactadas. As funcionalidades que possuem apenas demandas de testes, devem ser contadas usando o percentual da fase de testes (ver Tabela 7 – seção 6.2).

## 4.7. Manutenção em interface

A manutenção em interface, denominada na literatura de manutenção cosmética, é associada às demandas de alterações de interface, por exemplo: fonte de letra, cores de telas, logotipos, mudança de botões na tela, mudança de posição de campos ou texto na tela. Também se enquadram nessa categoria as seguintes manutenções:

- Alteração de *labels* de uma tela de consulta;
- Alteração de título de um relatório;
- Desenvolvimento ou atualização de help estático de funcionalidades;
- Mudanças de texto em mensagens de erro, validação, aviso, alerta, confirmação de cadastro ou conclusão de processamento;
- Mudança em texto estático de e-mail enviado para o usuário em uma funcionalidade de cadastro. A demanda deve ser contada como manutenção em interface na funcionalidade de cadastro.

Nestes casos, a aferição do tamanho em pontos de função das funções transacionais impactadas será realizada com a aplicação de um fator de redução de modo a considerar 20% da contagem de uma função transacional de mais baixa complexidade (3 PF), ou seja 0,6 PF, independentemente da complexidade da funcionalidade alterada. Neste tipo de manutenção não são contadas funções de dados.

```
PF_INTERFACE = 0,6 PF x QUANTIDADE DE FUNÇÕES TRANSACIONAIS IMPACTADAS
```

## 4.8. Adaptação em funcionalidades sem alteração de requisitos funcionais

São consideradas nesta categoria as demandas de manutenção adaptativa associadas a solicitações que envolvem aspectos não funcionais, sem alteração em requisitos funcionais. Seguem alguns exemplos:

- Adaptação de uma funcionalidade para possibilitar a chamada por um webservice ou para outro tipo de integração com outros sistemas;
- Adequar mensagem do sistema que em algumas telas apresenta “Usuário Não está Habilitado a ver esta Página”, para que passe a enviar uma mensagem mais adequada ao fato do usuário não possuir mais uma sessão ativa e ainda estar navegando no sistema. A demanda deve ser contada como manutenção adaptativa considerando as funcionalidades impactadas. Observe que se trata de mudança em validação com regra de negócio não funcional;
- Alteração na aplicação para adaptação às alterações realizadas na interface com rotinas de integração com outros softwares, por exemplo, alteração em subrotinas chamadas por este software;
- Aumentar a quantidade de linhas por página em um relatório;
- Colocar paginação em um relatório;
- Limitar a quantidade de linhas por página em uma consulta existente;
- Modificar o servidor a ser acessado em uma funcionalidade de download de arquivo;
- Permitir exclusões múltiplas em uma funcionalidade que antes só possibilitava a exclusão de um item;
- Replicação de funcionalidade: chamar uma consulta existente em outra tela da aplicação.

Nestes casos, a aferição do tamanho em pontos de função da funcionalidade ou das funcionalidades que sofreram impacto deve considerar um fator de impacto (FI) sobre o PF_ALTERADO, seguindo os conceitos do *CPM* 4.3.1, apresentados na seção 4.2.

```
PF_ADAPTATIVA = FI x PF_ALTERADO
```

a) FI (Fator de Impacto) pode variar conforme condições abaixo:

- FI = 50% para funcionalidade de sistema desenvolvida ou mantida por meio de uma iniciativa de melhoria pela empresa contratada.
- FI = 75% para funcionalidade de sistema não desenvolvida ou mantida por meio de uma iniciativa de melhoria pela empresa contratada.

Deve-se destacar que além da adequação das funcionalidades em questão, a documentação da iniciativa de manutenção adaptativa deve ser realizada. Além disso, caso exista a documentação das funcionalidades impactadas, estas deverão ser atualizadas, caso contrário, se for demandada a redocumentação dessas funcionalidades, deve-se adicionar ao FI um fator de redocumentação de 15%, conforme descrito na seção 4.2.

O PF_ALTERADO deve considerar apenas as funcionalidades impactadas. As funcionalidades que possuem apenas demandas de testes, devem ser contadas usando o percentual da fase de testes (ver Tabela 7 – seção 6.2).

## 4.9. Apuração especial

São funcionalidades executadas apenas uma vez para:

- Corrigir problemas de dados incorretos na base de dados das aplicações ou atualizar dados em bases de dados de aplicações, detalhados na subseção 4.9.1;
- Gerar um relatório específico ou arquivo para o usuário por meio de recuperação de informações nas bases da aplicação, detalhados na subseção 4.9.2;
- A subseção 4.9.3 considera os casos de reexecução de uma apuração especial.

Caso a apuração seja de correção de dados devido a erros de funcionalidades de aplicações desenvolvidas pela contratada, observar as cláusulas contratuais com relação a garantias e prazos de correção.

Recomenda-se fortemente ao contratante sempre solicitar formalmente para a empresa contratada o armazenamento do script para permitir posterior reexecução.

Cabe ressaltar que é necessário avaliar a complexidade das demandas típicas de apuração especial, podendo utilizar um percentual redutor nas fórmulas descritas nas subseções seguintes. Por exemplo, o redutor percentual pode ser aplicado em função da complexidade das demandas, documentação demandada e/ou do processo de desenvolvimento utilizado.

### 4.9.1. Apuração especial – Base de dados:

Este tipo de apuração especial é uma iniciativa que inclui a geração de procedimentos para atualização da base de dados. Deve-se destacar que estas funções são executadas apenas uma vez, não fazendo parte da aplicação, visando a correção de dados incorretos na base de dados da aplicação ou atualização em função de modificação da estrutura de dados, por exemplo inclusão de valor “sim” ou “não” no campo “indicador de matriz” referente ao CNPJ. Normalmente, nesse tipo de atualização são afetados múltiplos registros.

Nestes casos, considera-se a contagem de pontos de função das funcionalidades desenvolvidas. Geralmente, estas funcionalidades são classificadas como Entradas Externas. Nesse caso, como artefato de homologação da demanda, deve ser gerado um relatório para validação do usuário.

É importante ressaltar que as funções de dados associadas aos dados atualizados não devem ser contadas, considerando que não há mudanças nas estruturas dos Arquivos Lógicos Internos.

Foram identificados três tipos de Apuração Especial - Base de Dados, cujas fórmulas de cálculo são apresentadas a seguir:

a) Atualização de dados sem consulta prévia:

```
PF_APURAÇÃO_BD = PF_INCLUÍDO
```

b) Consulta prévia sem atualização:

Em alguns casos de Apuração Especial – Base de Dados, o usuário solicita uma consulta prévia das informações. Deve-se ressaltar que essa consulta deve ser realizada antes da construção da funcionalidade, não se trata de homologação. A consulta prévia não é definida pela empresa contratada, obrigatoriamente essa deve ser solicitada pelo contratante para a avaliação da viabilidade de implementar a Apuração Especial - Base de Dados. De fato, é uma prática interessante para evitar informações errôneas na base de produção dos sistemas. Esta consulta prévia, classificada como Consulta Externa ou Saída Externa deve ser dimensionada considerando-se o tamanho da funcionalidade em questão, conforme a fórmula a seguir:

```
PF _CONSULTA_PRÉVIA = PF_INCLUÍDO
```

c) Atualização de dados com consulta prévia:

Caso a Apuração Especial - Base de Dados seja solicitada após uma demanda de consulta prévia, deve-se aplicar um fator de 60% na fórmula de contagem da Apuração Especial - Base de Dados, conforme fórmula a seguir:

```
PF_APURAÇÃO_BD_PÓS_CONSULTA_PRÉVIA = PF_INCLUÍDO x 0,60
```

### 4.9.2. Apuração especial – Geração de relatórios:

Este tipo de apuração especial é uma iniciativa que inclui a geração de relatórios em uma ou mais mídias para o usuário. Em alguns casos, são solicitadas extrações de dados e envio dos dados para outros sistemas. Caso, neste envio de dados, sejam requisitadas atualizações no sistema de origem, então essas funções transacionais são Saídas Externas, devido à atualização do Arquivo Lógico Interno.

Deve-se destacar que essas funções são executadas apenas uma vez, não fazendo parte da aplicação. Nestes casos, considera-se contagem de pontos de função das funcionalidades desenvolvidas. Frequentemente, estas funcionalidades são classificadas como Saídas Externas. Também podem ser classificadas como Consultas Externas, caso não possuam cálculos ou criação de dados derivados.

É importante ressaltar que as funções de dados associadas aos dados atualizados não devem ser contadas, considerando que não há mudanças nas estruturas dos Arquivos Lógicos.

```
PF_APURAÇÃO_RELATÓRIOS = PF_INCLUÍDO
```

### 4.9.3. Apuração especial – Reexecução:

Em determinadas situações, pode ser necessário para a empresa contratante a execução de uma apuração especial mais de uma vez. Nesses casos, será considerada “reexecução” quando o mesmo fornecedor, já tendo elaborado um script de banco de dados, precisar realizar novas parametrizações para uma nova execução deste script, a fim de atender à demanda do contratante. Essas parametrizações podem incluir, por exemplo, alterações, exclusões ou inclusões de parâmetros como meses, códigos específicos de localidades, produtos, tipos de dados, entre outros.

Assim, quando caracterizada uma reexecução, esta deverá ser dimensionada aplicando-se um fator redutor de 10% na contagem de pontos de função da apuração especial, conforme descrito a seguir:

```
PF_REEXECUÇÃO_APURAÇÃO = PF_NÃO_AJUSTADO x 0,10
```

Vale ressaltar que a reexecução será considerada a partir da segunda execução de um mesmo script de banco de dados, não havendo limite de reexecuções, desde que obedecidas as regras para sua caracterização que foram apresentadas no parágrafo anterior. Outro ponto de atenção é que a caracterização de reexecução independe de solicitação formal do contratante para armazenamento do script de banco de dados para futura reexecução por parte do fornecedor.

Também é considerado como um tipo de apuração especial de reexecução as situações onde é repassado para o fornecedor scripts prontos onde o fornecedor precisará realizar somente parametrizações para sua execução. Regra e exemplos de parametrizações já foram definidas ao longo desta seção deste documento.

## 4.10. Atualização de dados

Em alguns casos, as demandas de correção de problemas em base de dados estão associadas a atualizações manuais (de forma interativa), diretamente no banco de dados em um único registro, e que não envolvem cálculos ou procedimentos complexos. São exemplos desse tipo de demanda, a atualização do valor de um campo de uma tabela cadastrado erroneamente ou a exclusão de um registro de uma tabela.

Nestes casos, a aferição do tamanho em Pontos de Função deve considerar 10% do PF de uma Entrada Externa e os Tipos de Dados da Entrada Externa são todos os TD considerados na funcionalidade – campos atualizados e campos utilizados para a seleção do registro.

```
PF_ATUALIZAÇÃO_BD = PF_INCLUÍDO x 0,10
```

Deve-se ressaltar que neste tipo de demanda não há gestão de configuração (armazenamento de script, versionamento, etc) das atualizações. Caso a contratante identifique a necessidade de realização de gestão de configuração das atualizações no banco de dados, então a demanda será classificada como Apuração Especial - Base de Dados (subseção 4.9.1).

## 4.11. Desenvolvimento, manutenção e publicação de páginas estáticas de intranet, internet ou portal

Nesta seção são tratados desenvolvimentos e manutenções específicas em páginas estáticas de portais, intranets ou websites. As demandas desta seção abrangem a publicação de páginas Web com conteúdo estático. Por exemplo: criação de página *HTML*, atualização de menu estático, atualização de texto ou banner estáticos em páginas *HTML* existentes.

Caso o desenvolvimento de páginas estáticas esteja contido em uma iniciativa de desenvolvimento, então elas serão contabilizadas na iniciativa de desenvolvimento e não devem ser mensuradas em separado. Ou seja, esta seção 4.11 se aplica quando ocorrer a demanda exclusivamente para o desenvolvimento ou manutenção de páginas estáticas.

Estas demandas são consideradas como desenvolvimento de consultas. Nestes casos, considera-se 20% dos pontos de função das consultas desenvolvidas. Cada página é contada como uma consulta. As consultas são consideradas consultas externas simples (3 PF). Ou seja, 0,6 PF por cada página desenvolvida ou mantida, de acordo com a fórmula a seguir:

```
PF_PUBLICAÇÃO = 0,6 PF x Quantidade de Páginas Alteradas ou Incluídas
```

É recomendada a construção de portais com ferramentas que apoiem a construção de conteúdo pelo usuário, os chamados Gerenciadores de Conteúdo, de modo a minimizar as demandas de criação de páginas estáticas.

## 4.12. Verificação de erros

As verificações de erro ou análise e solução de problemas são as demandas referentes a todo comportamento anormal ou indevido apontado pelo cliente nos sistemas aplicativos. Neste caso, a equipe de desenvolvimento da contratada se mobilizará para encontrar as causas do problema ocorrido. Se for constatado algum erro de sistema, a demanda será atendida como manutenção corretiva (seção 4.4).

Entretanto, uma vez não constatado o problema apontado pelo cliente ou o mesmo for decorrente de regras de negócio implementadas ou utilização incorreta das funcionalidades, será realizada a aferição do tamanho em pontos de função das funcionalidades (devem ser consideradas somente as funções de transação) verificadas que o cliente reportou erro. Será considerado 20% do tamanho funcional dessas funcionalidades com solicitação de análise pelo contratante, segundo a fórmula a seguir:

```
PF_VERIFICAÇÃO = PF_Funcionalidade_Reportada_Com_Erro x 0,20
```

É importante ressaltar que a demanda de verificação de erros deve ser associada a uma funcionalidade específica. Os casos de sistema fora do ar por conta de problemas de rede ou banco de dados devem ser tratados como serviços de suporte e não serviços de desenvolvimento e manutenção de sistemas. Esses serviços de suporte não fazem parte do escopo desse guia de métricas, não se aplicando verificação de erros nestes casos.

## 4.13. Pontos de função de teste

Muitas vezes, em iniciativas de manutenção, o conjunto de funções transacionais a serem testadas é maior do que a quantidade de funções a serem implementadas, isto é, além das funcionalidades que são afetadas diretamente pela iniciativa de manutenção, outras precisam ser testadas. O tamanho das funções a serem apenas testadas deve ser aferido em Pontos de Função de Teste (PFT). Não considerar as funcionalidades incluídas, alteradas ou excluídas da iniciativa de manutenção na contagem de Pontos de Função de Teste.

A contagem de PFT será o somatório dos tamanhos em pontos de função das funções transacionais envolvidas no teste:

```
PFT = Somatório dos Tamanhos das Funções Transacionais Testadas
```

A conversão do PFT em ponto de função deve ser feita de acordo com a fórmula a seguir:

```
PF_TESTES = PFT X 0,20
```

É importante ressaltar que no caso de uma função ser testada várias vezes, com cenários diferentes, a função só pode ser contada uma vez. Outra observação é que as funções testadas, previstas no PFT, devem ser registradas pela contratada considerando-se a documentação de testes definida no processo de desenvolvimento da contratante.

## 4.14. Componente interno reusável

Em alguns casos são demandadas manutenções em componentes, que implementam regras de negócio, específicos de uma aplicação e estes são reusados por várias funcionalidades da aplicação. Por exemplo, uma mudança em uma rotina de validação de um CPF usada em várias funcionalidades de cadastro. Se considerarmos o método de contagem de iniciativas de melhoria do *CPM*, seriam contadas todas as funcionalidades impactadas por essa mudança.

No entanto, este guia propõe que o componente, o qual deverá ser testado, seja considerado como um processo elementar independente e sua alteração seja contada aplicando-se um fator de impacto (FI) sobre o PF_ALTERADO, seguindo os conceitos do *CPM* 4.3.1, apresentados na seção 4.2 – Iniciativa de Melhoria. Além disso, as funcionalidades da aplicação que necessitem de teste devem ser requisitadas pela contratante e dimensionadas por meio da métrica Pontos de Função de Teste proposta na seção 4.14.

```
PF_COMPONENTE = FI x PF_ALTERADO
```

Exemplo de manutenção de componentes:

- Mudança em tópico de um menu de um sistema em PHP que aparece em todas as telas da aplicação. A contagem pode ser realizada considerando o componente “Apresentar Menu”.

Além do item descrito anteriormente, existem casos onde são realizadas manutenções de valores de elementos internos de configuração que afetam o comportamento ou a apresentação do sistema de forma geral, tais como páginas de estilos (arquivos CSS de sistemas Web), arquivos com mensagens de erro, arquivos de configuração de sistema e arquivos de internacionalização. Nestes casos, a aferição do tamanho em pontos de função será realizada com a aplicação de um fator de redução de modo a considerar 20% da contagem de uma função transacional de mais baixa complexidade (3 PF), ou seja 0,6 PF. Assim sendo, deve ser utilizada a seguinte fórmula de cálculo:

```
PF_COMPONENTE_ARQUIVO = 0,6 PF x QTD_ARQUIVOS_ALTERADOS
```

## 4.15. Dados de Código (*code tables*)

Os dados de código em geral estão relacionados a tabelas de domínio que são utilizadas pela aplicação para decodificar valores, metadados, dados e tabelas estáticas. Não raramente dados de código também estão associados a utilização de estruturas adicionais de banco tanto para oferecer uma maior performance a aplicação, na emissão de relatórios (exemplo: tabela de vendas diárias derivada de tabela de vendas onde a emissão de relatórios enxerga a tabela de vendas diária), como para guardar dados de configuração técnica (dados de IP, porta de conexão, string de conexão de banco de dados, etc).

O manual do IFPUG aborda em um capítulo inteiro o assunto Dados de Código, e é taxativo em afirmar que Dados de Código são relativos a requisitos não funcionais e que, portanto, não devem ser medidos como parte do tamanho funcional.

Para o contexto de um contrato de desenvolvimento/manutenção de sistemas baseado em PF, é comum que o escopo do trabalho do fornecedor em uma determinada demanda, abranja Dados de Código. Em sendo o escopo desta demanda a criação de novas funcionalidades, e derivadas delas a criação de dados de código, então nada deve ser medido para a parte de dados de código. A remuneração do fornecedor é feita pela medição exclusiva dos PF e o trabalho de dados de código é remunerado indiretamente pelo preço do PF do contrato.

Em sendo o escopo de trabalho da demanda a criação ou manutenção de dados de código que não estejam associados a requisitos funcionais novos na mesma demanda, então haverá uma medição a ser aplicada à parte de dados de código, conforme definido a seguir. A eventual alteração de conteúdo ou criação de listas estáticas também deverá ser medida da mesma forma.

```
PF_CODETABLE = 0,3 PF x QUANTIDADE DE TABELAS E TRANSAÇÕES DE MANUTENÇÃO/CONSULTA AOS DADOS INCLUÍDAS, ALTERADAS E EXCLUÍDAS
```
