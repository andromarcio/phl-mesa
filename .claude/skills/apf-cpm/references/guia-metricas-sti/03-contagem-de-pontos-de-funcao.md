# 3. Contagem de Pontos de Função:

> Guia de Métricas da STI · Versão 1.3 (Dez/2025)

A métrica PF mede o tamanho funcional de uma iniciativa de desenvolvimento de sistema, observando as funcionalidades implementadas, considerando a visão do usuário. O tamanho funcional é definido como tamanho do sistema a partir da contabilização dos requisitos funcionais do sistema que são observados pelo usuário. A métrica PF é independente da metodologia e tecnologia utilizadas. A Análise de Pontos de Função (APF) é um método padrão para a medição de iniciativas de desenvolvimento e de manutenção de sistemas, visando estabelecer uma medida de tamanho do software em pontos de função, com base na quantificação das funcionalidades solicitadas e entregues, sob o ponto de vista do usuário. Assim, a APF tem como objetivo medir o que o software faz, por meio de uma avaliação padronizada dos requisitos de negócio do sistema. O Manual de Práticas de Contagem (*CPM* 4.3.1.) [IFPUG, 2010b] apresenta as regras de contagem de pontos de função de iniciativas de desenvolvimento, iniciativas de melhoria e aplicações implantadas. A Figura 1 ilustra o procedimento de contagem de pontos de função, descrito nas seções seguintes.

![Figura 1: Procedimento de Contagem de Pontos de Função](images/p007-figura-1-procedimento-contagem-pf.png)

## 3.1. Determinar propósito, tipo e escopo da contagem e fronteira da aplicação

A contagem de pontos de função se inicia com a análise da documentação disponível da iniciativa em questão, visando a identificação dos requisitos funcionais. O próximo passo é o estabelecimento do propósito da contagem, o qual fornece uma resposta para uma questão de negócio a ser resolvida, por exemplo: necessidade de dimensionar uma iniciativa de um novo sistema para auxiliar o processo de contratação do mesmo. Com base no propósito da contagem são definidos o escopo da contagem e o tipo de contagem. O escopo da contagem identifica quais funcionalidades serão incluídas na contagem de pontos de função, e o tipo de contagem identifica se a iniciativa é de desenvolvimento, de melhoria ou aplicação instalada. A fronteira da aplicação, que é a interface conceitual que indica o limite lógico entre o sistema sendo medido e os usuários (pessoas, sistemas, dispositivos ou qualquer coisa que interaja com o sistema), deve ser definida com base na visão do usuário (do negócio), desconsiderando questões de implementação. Deve-se ressaltar que toda contagem de pontos de função é realizada dentro de uma fronteira estabelecida.

O estabelecimento da fronteira da aplicação pode ser subjetivo, por exemplo, em uma aplicação com vários módulos, a fronteira pode ser estabelecida para cada módulo ou subsistema ou, ainda, pode-se considerar toda a aplicação, dependendo da visão do usuário. De fato, a definição da fronteira depende de processos de negócios, além disso, o posicionamento da fronteira influencia fortemente a contagem de pontos de função. Desta forma, devido a essa subjetividade, em editais para contratação de iniciativas de manutenção é fortemente recomendado a definição das fronteiras de todas as aplicações a serem contratadas.

## 3.2. Identificação de processo elementar

Antes de identificarmos as funções, vale ressaltar o conceito básico acerca do processo elementar. Um Processo Elementar é a menor unidade de atividade que é significativa para o(s) usuário(s). O Processo Elementar deve ser autocontido e deixar o negócio da aplicação que está sendo contada em um estado consistente.

Um processo elementar com múltiplas formas de processamento lógico não deve ser dividido em múltiplos processos elementares. Se um processo elementar é subdividido inapropriadamente, o mesmo não reúne os critérios de um processo elementar.

Como exemplo pode-se destacar o recurso de abas para a construção de interfaces em sistemas computacionais. Em geral, cada aba de uma tela não representa uma transação completa e desta forma não deve ser considerada um processo elementar isolado. O adequado para este tipo de situação é identificar um processo elementar para um conjunto de abas que se relacionam em vez de considerar um processo elementar para cada aba.

Ressalta-se a importância do atendimento a todos os critérios listados no Manual de Práticas de Contagem do IFPUG e da observação dos seus exemplos para a correta identificação de um processo elementar evitando, por exemplo, relacionar processos elementares com telas ou abas de uma transação, considerar fluxos alternativos como processos elementares distintos ou considerar transações que atualizem dados de código.

## 3.3. Identificar Funções de Dados e Funções Transacionais

Uma vez estabelecida a fronteira da aplicação e o escopo, o próximo passo é o mapeamento dos requisitos de dados e de funções transacionais para os tipos funcionais da APF.

### 3.3.1. Funções do tipo dado:

a) Arquivo Lógico Interno (ALI): é um grupo de dados, logicamente relacionados, reconhecido pelo usuário, mantido por meio de um ou mais processos elementares da aplicação que está sendo contada.

b) Arquivo de Interface Externa (AIE): é um grupo de dados, logicamente relacionados, reconhecido pelo usuário, mantido em outra aplicação e referenciado pela aplicação que está sendo contada. O AIE é obrigatoriamente um ALI de outra aplicação.

### 3.3.2. Funções do tipo transação:

a) Entrada Externa (EE): é um processo elementar que processa dados ou informação de controle que entram pela fronteira da aplicação. Seu objetivo principal é manter um ou mais ALI ou alterar o comportamento do sistema.

b) Consulta Externa (CE): é um processo elementar que envia dados ou informação de controle para fora da fronteira da aplicação. Seu objetivo principal é apresentar informação para o usuário através da recuperação de dados ou informação de controle de ALI ou AIE.

c) Saída Externa (SE): é um processo elementar que envia dados ou informação de controle para fora da fronteira da aplicação. Seu objetivo principal é apresentar informação para um usuário ou outra aplicação através de um processamento lógico adicional à recuperação de dados ou informação de controle. O processamento lógico deve conter cálculo, ou criar dados derivados, ou manter ALI ou alterar o comportamento do sistema.

### 3.3.3. Contribuição dos tipos funcionais:

Após a identificação dos tipos funcionais para cada requisito funcional definido no documento de requisitos do sistema, deve-se avaliar a complexidade (Baixa, Média, Alta) e a contribuição funcional do mesmo para a contagem de pontos de função, observando as regras de contagem de pontos de função descritas no *CPM*. A identificação e a avaliação das complexidades dos tipos funcionais é feita pela avaliação objetiva de dois parâmetros, com suas regras de contagem descritas no *CPM*. A contagem de pontos de função deve seguir rigorosamente as regras de contagem do *CPM* e as definições complementares por ventura presentes neste guia. A Tabela 1 apresenta a contribuição dos tipos funcionais na contagem de pontos de função.

**Tabela 1: Contribuição Funcional dos Tipos Funcionais (Fonte: CPM 4.3)**

| Tipo Funcional | Baixa | Média | Alta |
|---|---|---|---|
| Arquivo Lógico Interno (ALI) | 7 PF | 10 PF | 15 PF |
| Arquivo de Interface Externa (AIE) | 5 PF | 7 PF | 10 PF |
| Entrada Externa (EE) | 3 PF | 4 PF | 6 PF |
| Saída Externa (SE) | 4 PF | 5 PF | 7 PF |
| Consulta Externa (CE) | 3 PF | 4 PF | 6 PF |

No *CPM* 4.3.1 não existe a distinção de tipos de contagem. Entende-se que o padrão descrito no *CPM* 4.3.1 fornece uma contagem com maior percentual de assertividade devido ao maior detalhamento dos requisitos de uma iniciativa e/ou grau de avanço da mesma. Desta forma, a Tabela 1, de Contribuição Funcional dos Tipos Funcionais, considerando também as regras para sua consecução, e, bem como, as derivadas dela, determinam o que chamaremos de Contagem Detalhada de Pontos de Função (ou, somente, Contagem Detalhada).

Porém, os clientes da STI possuem a necessidade de ter acesso a uma contagem que possa ser realizada seguindo-se um padrão técnico reconhecido pelo mercado e que afira um alto grau de confiabilidade ao dimensionamento realizado. Esta contagem deve ser realizada aportando-se em documentação menos vasta e em momentos primários da iniciativa, consumindo também menos recursos (tempo e pessoas) para sua finalização. Sendo assim, este guia apresenta as regras da Contagem Estimativa de Pontos de Função (CEPF) na seção 6.1.

## 3.4. Calcular tamanho funcional

Seguem as definições dos termos técnicos da Análise de Pontos de Função utilizados nas fórmulas de dimensionamento de iniciativas de sistemas propostas neste guia:

a) PF_INCLUÍDO: pontos de função associados às novas funcionalidades que farão parte da aplicação após uma iniciativa de desenvolvimento ou de manutenção.

b) PF_ALTERADO: pontos de função associados às funcionalidades existentes na aplicação que serão alteradas na iniciativa de manutenção.

c) PF_EXCLUÍDO: pontos de função associados às funcionalidades existentes na aplicação que serão excluídas na iniciativa de manutenção.

d) PF_CONVERSÃO: pontos de função associados às funcionalidades de conversão de dados das iniciativas de desenvolvimento ou de manutenção. Exemplos de funções de conversão incluem: migração ou carga inicial de dados para popular as novas tabelas criadas (Entradas Externas) e relatórios associados à migração de dados, caso requisitado pelo usuário (Saídas Externas ou Consultas Externas). Observe que os dados carregados em um processo de migração não devem ser contados como Arquivos de Interface Externa.

## 3.5. Requisitos não funcionais

A métrica Ponto de Função é uma métrica de tamanho funcional, ou seja, dimensiona iniciativa de sistemas com base nos requisitos funcionais da aplicação, não contemplando diretamente os requisitos não funcionais da iniciativa. Nesse sentido, em contratos de sistemas baseados na métrica Ponto de Função é fundamental definir claramente no edital os requisitos não funcionais da iniciativa a serem atendidos pela empresa contratada. Os requisitos não funcionais impactam no esforço e, consequentemente, no custo da iniciativa, porém, não apresentam contagem direta na métrica de pontos de função. Os requisitos não funcionais estão associados aos aspectos qualitativos de um sistema, considerando aspectos relacionados ao uso do mesmo. Seguem abaixo alguns tipos de requisitos não funcionais, com exemplos, que podem ser mencionados nos editais:

a) Usabilidade: a solução deve atender aos requisitos dos Padrões Web em Governo Eletrônico (e-PWG) – Cartilha de Usabilidade; a aplicação deve ter help on-line de sistema, tela e campo (sensível a contexto); a aplicação deve ser disponibilizada nos idiomas Português, Espanhol e Inglês.

b) Técnicos: a aplicação deve funcionar adequadamente nos navegadores: Internet Explorer 7.0 ou superior e Mozilla Firefox 3.0 ou superior; a solução deve ser desenvolvida em linguagem Java com banco de dados PostgreSQL; para o desenvolvimento da solução, deve ser utilizado preferencialmente um dos seguintes frameworks Java: Demoiselle, Jaguar e MDArt; a solução deve atender aos requisitos do e-PWG; deve utilizar as ferramentas AWSTATS e Google Analytics para gerar estatísticas de acesso.

c) Segurança: a aplicação deve realizar controle de segurança dos dados de acordo com política de backup definida em conformidade com a norma ISO/IEC 27002.

d) Acessibilidade: a solução deve ser aderente ao Modelo de Acessibilidade de Governo Eletrônico (e-MAG).

e) Performance: o tempo de resposta da aplicação não deve exceder 10 segundos; a solução deve suportar até 1.000 acessos simultâneos.

f) Interoperabilidade: a solução deve ser aderente aos Padrões de Interoperabilidade de Governo Eletrônico (e-PING).
