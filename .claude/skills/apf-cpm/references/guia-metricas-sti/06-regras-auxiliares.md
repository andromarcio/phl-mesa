# 6. Regras auxiliares

> Guia de Métricas da STI · Versão 1.3 (Dez/2025)

Este capítulo visa compilar as regras auxiliares deste guia para sua perfeita aplicação, trazendo assim indicações complementares para a realização das contagens sob responsabilidade da STI.

## 6.1. Contagem estimativa de pontos de função (CEPF)

Esta seção tem o objetivo de suportar e normatizar ações da STI que visam apoiar processo decisório que, para sua realização, necessita de estimativa do tamanho do desenvolvimento ou manutenção que se pretende realizar. A partir das regras descritas nesta seção será permitida a definição de uma estimativa, em pontos de função, da forma mais eficiente e coerente possível.

A Contagem Estimativa de Pontos de Função – CEPF, significa fornecer uma avaliação aproximada do tamanho de um software utilizando métodos diferentes da contagem de pontos de função do IFPUG.

A CEPF foi definida com base nas diretrizes adotadas no método Contagem Estimada de Pontos de Função da NESMA [NESMA, 2005]. A diferença é que o método da NESMA não recomenda a análise da complexidade das funções identificadas, considerando todas as funções de dados identificadas com complexidade Baixa e as funções transacionais com complexidade Média.

Primeiramente, os requisitos funcionais iniciais do sistema são mapeados nos tipos funcionais da Análise de Pontos de Função: Arquivo Lógico Interno (ALI), Arquivo de Interface Externa (AIE), Entrada Externa (EE), Consulta Externa (CE) e Saída Externa (SE) (Figura 2). Posteriormente, os pontos de função são associados a cada função identificada, baseando-se nas tabelas de complexidade e de contribuição funcional do *CPM* (Tabela 1).

O estimador deve realizar uma leitura do documento inicial de requisitos, buscando informações relevantes para a identificação de processos elementares. O processo elementar é definido como a menor unidade de atividade significativa para o usuário. Em outras palavras, os processos elementares são funções transacionais independentes, isto é, funções sequenciais pertencem a um mesmo processo elementar e funções independentes constituem processos elementares diferentes.

**FIGURA 2 — Modelo Lógico da Análise de Pontos de Função**

![Figura 2 — Modelo Lógico da Análise de Pontos de Função](images/p048-figura-2-modelo-logico-apf.png)

Uma vez identificado o processo elementar, o estimador deve buscar o entendimento deste para classificá-lo em Entrada Externa, Consulta Externa ou Saída Externa. Adicionalmente, o estimador deve descobrir os dados associados ao processo elementar, visando a determinação da complexidade funcional da função identificada. Caso não seja possível a identificação da complexidade da funcionalidade em questão, recomenda-se a utilização da complexidade Média. Na análise do processo elementar também são identificados os grupos de dados lógicos da aplicação, que são classificados como Arquivos Lógicos Internos ou Arquivos de Interface Externa. Caso não seja possível a identificação da complexidade da função de dados em questão, recomenda-se a utilização da complexidade Baixa. É importante ressaltar que se o estimador identificar mais de um Registro Lógico no Arquivo Lógico Interno, recomenda-se utilizar a complexidade Média.

A seguir são apresentadas dicas para ajudar no mapeamento dos requisitos funcionais da aplicação nos tipos funcionais da APF. As necessidades e funcionalidades especificadas para a iniciativa, contidas no documento inicial de requisitos, devem ser enquadradas em uma das seguintes tabelas:

a) Tabela 2 – Contagem dos Arquivos Lógicos Internos (ALI): banco de dados lógico da aplicação (tabelas e arquivos mantidos pela aplicação).

- Considerações: É necessário identificar os grupos de dados lógicos de aplicação nos modelos de dados ou diagrama de classes ou a partir dos requisitos funcionais, descritos nos documentos de requisitos. Arquivos físicos, arquivos de índices, arquivos de trabalho e tabelas de relacionamento sem atributos próprios (tabelas que existem para quebrar o relacionamento m x n e apenas transportam as chaves estrangeiras) devem ser desconsiderados. As entidades fracas também não são consideradas um ALI. É opcional a identificação dos atributos lógicos, campos reconhecidos pelo usuário, e subgrupos de dados existentes para obter a complexidade funcional, segundo as regras de contagem do *CPM*. Caso não seja possível, a experiência tem mostrado que a maioria dos ALI dos sistemas são de complexidade Baixa.

**Tabela 2: Identificação dos Arquivos Lógicos Internos da Aplicação**

|  |  |
| --- | --- |
| Nº ALI Baixa: | X 7 PF |
| Nº ALI Média: | X 10 PF |
| Nº ALI Alta: | X 15 PF |
| Total PF: | |

b) Tabela 3 – Contagem de Arquivos de Interface Externa (AIE): banco de dados de outras aplicações, apenas referenciados pela aplicação que está sendo estimada (tabelas e arquivos mantidos por outra aplicação).

- Considerações: É necessário identificar os grupos de dados lógicos de outras aplicações referenciados pela aplicação que está sendo estimada. Frequentemente, o referenciamento de dados ocorre para a validação de informações em cadastros ou consultas. Algumas vezes, relatórios ou consultas referenciam dados externos de outras aplicações, também considerados AIE. Não são considerados AIE arquivos físicos, arquivos de índice, arquivos de trabalho, tabelas de relacionamento sem atributos próprios e entidades fracas. Geralmente, os AIE dos sistemas possuem a classificação de complexidade Baixa, porque são considerados para a determinação da complexidade funcional do AIE apenas os atributos referenciados pela aplicação que está sendo contada.

**Tabela 3: Identificação dos Arquivos de Interface Externa da Aplicação**

|  |  |
| --- | --- |
| Nº AIE Baixa: | X 5 PF |
| Nº AIE Média: | X 7 PF |
| Nº AIE Alta: | X 10 PF |
| Total PF: | |

c) Tabela 4 - Contagem de Entradas Externas (EE): funcionalidades que mantêm os Arquivos Lógicos Internos (ALI) ou alteram o comportamento da aplicação.

- Considerações: É necessário identificar as funcionalidades de manutenção de dados. Inclusão, alteração e exclusão de dados, isto é, cada função independente de inclusão, alteração ou exclusão devem ser contadas separadamente. Caso a aplicação possua funções de entrada de dados que alteram o comportamento dela, por exemplo: processamentos batch ou processamento de informações de controle, estas funções também devem ser identificadas como Entradas Externas. Não sendo possível definir a complexidade, considere as Entradas Externas identificadas com complexidade Média.

**Tabela 4: Identificação das Entradas Externas da Aplicação**

|  |  |
| --- | --- |
| Nº EE Baixa: | X 3 PF |
| Nº EE Média: | X 4 PF |
| Nº EE Alta: | X 6 PF |
| Total PF: | |

d) Tabela 5 – Contagem de Consultas Externas (CE): funcionalidades que apresentam informações para o usuário sem a utilização de cálculos ou algoritmos. São os processos elementares do tipo “lê - imprime”, “lê - apresenta dados”, incluindo consultas, relatórios, geração de arquivos pdf, xls, downloads, entre outros.

- Considerações: Caso a função vise apresentar informações para o usuário (uma consulta, relatório, listbox, download, geração de um arquivo, geração de arquivo pdf, xls), caso não possua cálculos ou algoritmos para derivação dos dados referenciados, caso não altere um Arquivo Lógico Interno e nem mude o comportamento do sistema, esta função deve ser identificada como Consultas Externa. Não sendo possível definir a complexidade, considere as Consultas Externas identificadas com complexidade Média.

**Tabela 5: Identificação das Consultas Externas da Aplicação**

|  |  |
| --- | --- |
| Nº CE Baixa: | X 3 PF |
| Nº CE Média: | X 4 PF |
| Nº CE Alta: | X 6 PF |
| Total PF: | |

e) Tabela 6 - Contagem de Saídas Externas (SE): funcionalidades que apresentam informações para o usuário com utilização de cálculos ou algoritmos para derivação de dados ou atualização de Arquivos Lógicos Internos ou mudança de comportamento da aplicação. São as consultas ou relatórios com totalização de dados, relatórios estatísticos, gráficos, geração de arquivos com atualização log, downloads com cálculo de percentual, entre outros.

- Considerações: Caso a função vise apresentar informações para o usuário que necessitarão ser calculadas, de alguma forma (uma consulta ou relatório com totalização de dados, etiquetas de código de barras, gráficos, relatórios estatísticos, download com percentual calculado, geração de arquivo com atualização de log) esta função deve ser identificada como Saída Externa. Observe que esta função deve ter cálculos ou algoritmos para processar os dados referenciados nos arquivos lógicos ou atualizar campos (normalmente indicadores) nos arquivos ou mudar o comportamento da aplicação. Não sendo possível definir a complexidade, considere as Saídas Externas identificadas com complexidade Média.

**Tabela 6: Identificação das Saídas Externas da Aplicação**

|  |  |
| --- | --- |
| Nº SE Baixa: | X 4 PF |
| Nº SE Média: | X 5 PF |
| Nº SE Alta: | X 7 PF |
| Total PF: | |

A estimativa de tamanho da iniciativa em PF deve ser gerada com a totalização dos PF obtidos nas Tabelas 2, 3, 4, 5 e 6.

## 6.2. Distribuição de esforço por fase da iniciativa

Na Tabela 7 temos a distribuição de esforços pelas macroatividades (fases) relacionadas ao ciclo de vida de desenvolvimento de um software. Os percentuais indicados nesta tabela são um fator de ponderação a ser aplicado no cálculo dos pontos de função das iniciativas com o objetivo de racionalizar a sua aferição, prevendo assim somente a remuneração das ações que foram efetivamente empregadas na iniciativa.

**Tabela 7: Distribuição de Esforço por Macroatividades da Iniciativa**

| Macroatividades do Processo de Desenvolvimento de Software | Percentual de Esforço (%) |
| --- | --- |
| Refino | 20% |
| Implementação | 60% |
| Teste | 20% |

### 6.2.1. Evidências de entrega:

Para caracterizar a efetiva entrega de cada uma das 3 fases descritas na tabela 7 é necessário convencionar o que será aceito como entrega.

Salvo especificidades que podem ser inseridas no contexto de gestão e contratação de determinados sistemas, considera-se os seguintes cenários como padrões de evidências de entrega e, por consequência, como critérios válidos para aplicação do fator de ponderação em torno dos percentuais de esforço para remuneração:

a) Refino: Demanda refinada e com história de usuário e seus critérios de aceitação.

b) Implementação: Código fonte versionado e no padrão de codificação entregue no repositório indicado.

c) Teste: Evidência de teste para cada um dos critérios de aceitação da história.

### 6.2.2. Estratégias de desenvolvimento de *back* e *frontend* em separado:

Nos casos em que o cliente aprovar estratégia de desenvolvimento que divida em Sprints distintas as camadas de uma funcionalidade (por exemplo, primeira realiza-se o desenvolvimento e entrega do *backend*, e, depois realiza-se o desenvolvimento do *frontend*), para efeito de remuneração parcial deve-se adotar uma relação de 60% para *backend* e 40% para *frontend* considerando-se somente o percentual da macroatividade de Implementação.

## 6.3. Fator de ajuste

O fator de ajuste não faz mais parte do processo de medição funcional aderente à ISO/IEC 14133, contudo, ainda é parte do *CPM* 4.3.1 como um apêndice, para manter a compatibilidade com aqueles usuários que usam pontos de função com a sua aplicação.

Complementando este caráter opcional de sua aplicação, o que acusa algum nível de obsolescência da mesma, também podemos considerar que esta mesma técnica apresenta alto grau de subjetividade, inter-relacionamento entre variáveis, incompletude de questões técnicas, conceituais e metodológicas envolvidas na sua aplicação e não traz benefícios para otimizar questões relacionadas a estimativas de esforço. Por isso, este guia segue recomendação da comunidade de contagem de pontos de função e assim determina o não uso de fator de ajuste nas contagens sob responsabilidade da STI.
