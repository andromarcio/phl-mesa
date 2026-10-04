# Guia de Métricas da STI, versão 1.3 — índice e precedência

Transcrição integral do Guia de Métricas da Superintendência de Tecnologia da Informação (STI), versão 1.3, de dezembro de 2025, incorporada à skill como **fonte normativa do contrato**. É o guia que rege as contagens entregues à equipe de métricas da STI — a planilha de entrega (`scripts/gera-planilha-contagem.py`) preenche o modelo dele.

> **Precedência** *(decisão do usuário, 2026-10-04)*: **as regras deste Guia se sobrepõem às definições do CPM.** Onde o Guia dispõe, vale o Guia; onde ele cala, vale o CPM 4.3.1 (`../cpm-4.3.1/`) — o próprio Guia manda seguir as regras do CPM "e as definições complementares" dele (3.3.3). Na memória de cálculo, cite a seção do Guia quando a regra vier dele: `Guia STI 5.1.4`.

> **Figuras.** As duas figuras do Guia (o procedimento de contagem e o modelo lógico da APF) **não** foram copiadas: só o texto. Elas vivem no repositório de origem, `andromarcio/metricas-software`, pasta `STI/images/`, ao lado do PDF original (`GUIA_DE_METRICAS_STI_V1.3.pdf`). Os links `![…](images/…)` foram mantidos. Em caso de divergência entre a transcrição e o PDF, prevalece o PDF.

## O que está em cada capítulo

| Arquivo | Conteúdo | Quando abrir |
|---|---|---|
| `03-contagem-de-pontos-de-funcao.md` | O procedimento: propósito, escopo e fronteira; processo elementar (aba não é processo elementar); funções de dados e de transação; a contagem **detalhada** e a **estimativa**; PF incluído, alterado, excluído e de conversão; requisitos não funcionais | Dúvida sobre o que entra na contagem e com que nome a STI chama cada parcela |
| `04-calculo-de-pontos-de-funcao.md` | **As fórmulas por tipo de iniciativa**: desenvolvimento, melhoria (com o Fator de Impacto), migração de dados, corretiva, mudança de plataforma, atualização de versão, manutenção em interface, adaptativa, apuração especial, atualização de dados, páginas estáticas, verificação de erros, pontos de função de teste, componente reusável e dados de código | Sempre que a iniciativa **não** for desenvolvimento puro — é aqui que o Guia vai além do CPM |
| `05-orientacoes-complementares.md` | **Os casos que mudam a contagem**: múltiplas mídias, log, trilha de auditoria e histórico, arquivos para processamento, API e webservice, e a lista das falhas de contagem | Antes de contar exportação em mais de um formato, a mesma função por tela e por API, carga por arquivo, auditoria ou integração |
| `06-regras-auxiliares.md` | A **contagem estimativa (CEPF)**, a distribuição de esforço por fase (refino, implementação, teste) e a dispensa do fator de ajuste | Ao estimar um ticket antes de haver especificação, e ao medir entrega parcial |
| `01-introducao.md`, `02-objetivo.md` | Contexto e objetivo do Guia | Raramente numa contagem |
| `07-referencias-bibliograficas.md`, `08-controle-de-versao.md` | Referências e histórico do documento | Para conferir a versão em vigor |
| `README.md`, `00-capa-e-sumario.md` | A apresentação da transcrição e o sumário do original, com as páginas | Para localizar uma seção pelo número |

## Onde o Guia decide diferente do CPM, ou além dele

O que está nesta tabela é o resumo; a regra é o texto do capítulo.

| Assunto | O que o Guia dispõe | Seção |
|---|---|---|
| Tipos de contagem | Há duas: a **detalhada**, pelas regras do CPM, e a **estimativa** (CEPF), para quando a documentação ainda é pouca | 3.3.3 · 6.1 |
| Contagem estimativa | Usa a complexidade quando dá para identificá-la; quando não dá, transação é **Média** (EE 4 · CE 4 · SE 5) e função de dados é **Baixa** (ALI 7 · AIE 5) — salvo o ALI com mais de um registro lógico, que é **Média** (10) | 6.1 |
| Projeto de melhoria | `PF_MELHORIA = PF_INCLUIDO + (FI × PF_ALTERADO) + (0,30 × PF_EXCLUIDO) + PF_CONVERSÃO`. O Fator de Impacto é 50% para a função desenvolvida ou já mantida pela contratada, 75% para a que não foi, e 90% quando além disso há redocumentação (só na primeira melhoria da função). O CPM soma as parcelas sem fator | 4.2 |
| O que é função alterada | Função de dados: inclusão ou exclusão de tipo de dado, ou mudança de tamanho ou de tipo de campo por regra de negócio. Transação: mudança de tipos de dados, de arquivos referenciados ou de lógica — **e também** qualquer mudança por regra de negócio, ainda que nenhum dos três mude | 4.2.1 · 4.2.2 |
| Migração de dados | Conta como desenvolvimento: as cargas são Entradas Externas e os relatórios da carga, quando pedidos, Saídas Externas; as funções de dados não contam, e o dado migrado não é AIE | 3.4 d · 4.3 |
| Iniciativas sem mudança funcional | Têm medição própria, que o CPM não traz: corretiva (FI sobre o alterado), mudança de plataforma, atualização de versão (30% do alterado), manutenção em interface (0,6 PF por transação), adaptativa (FI sobre o alterado), apuração especial, atualização de dados (10% de uma EE), página estática (0,6 PF por página), verificação de erros (20%), pontos de função de teste (20%) e componente reusável | 4.4 a 4.14 |
| Dados de código | Não são função de dados nem geram transação (falha de contagem). Só se medem quando o pedido é criar ou manter dados de código **sem** requisito funcional novo: 0,3 PF por tabela e por transação de manutenção ou consulta | 4.15 · 5.5 |
| Múltiplas mídias | A base é o *multiple instance*, **com exceções**: consulta em `.pdf`, `.doc` e `.xls` e consulta idêntica em tela e papel são **uma** função. Entrada por lote e entrada on-line são duas. Relatório em mais de um formato conta por formato só quando a equipe desenvolve cada um; se a ferramenta gera os formatos, conta uma vez | 5.1 |
| Mesma função por tela e por serviço | Sem diferença de lógica nem de campos entre a tela e o webservice, conta-se **uma** função | 5.1.4 |
| Log, auditoria e histórico | Log não se mede. Trilha de auditoria só conta se pedida pelo usuário e com consulta aos dados; como política corporativa de segurança, é requisito não funcional. Histórico conta pela consulta; gravar o histórico é parte da função que grava o dado | 5.2 |
| Arquivo para processamento | O arquivo trocado entre sistemas não é ALI nem AIE. Na origem, gerar o arquivo é CE ou SE; no destino, processar é EE — uma por tipo de registro e por operação explícita no leiaute. O relatório de erros da carga é parte da EE | 5.3 |
| API e webservice | Quem fornece a API mede as funções expostas como transação, com os parâmetros como tipos de dados. Quem consome não mede transação da API: os campos trocados entram na complexidade da transação que a aciona, e o dado só é AIE se o acesso direto à origem também servisse. API consumida só pelo próprio sistema não se mede | 5.4 |
| Processo elementar | Aba de tela não é processo elementar, nem fluxo alternativo, nem transação que atualiza dado de código | 3.2 · 5.5 |
| O que não é tipo de dado | Paginação e posicionamento, ajudas de navegação, mais de um meio de disparar a ação, mais de uma mensagem | 5.5 |
| Entrega parcial | Refino 20%, implementação 60%, teste 20%; com *backend* e *frontend* em sprints separadas, 60% e 40% da implementação | 6.2 |
| Fator de ajuste | Não se usa | 6.3 |

## Onde o engine ainda não segue o Guia

Levantado em 2026-10-04, na incorporação. São pontos a decidir com a equipe de métricas — a skill não os resolve sozinha.

- **Formatos de saída.** O `SIZING.md`, na seção *Regras de medição de serviços (CAIXA)*, item 9, diz que formato diferente nunca conta de novo e que não se adota *multiple media*; o Guia parte do *multiple instance*, com as exceções da seção 5.1. Vale o Guia. Nos dois sentidos há contagem a conferir: instâncias contam hoje uma exportação por formato (`XLSX`, `ODS`, `HTML`) e a mesma função por tela e por `API` como processos distintos.
- **Contagem estimada da AIM.** O engine usa peso fixo por tipo (EE 4 · CE 4 · SE 5 · ALI 7 · AIE 5). O Guia manda usar a complexidade quando ela é identificável e dá Média (10) ao ALI com mais de um registro lógico.
- **PFL.** O engine aplica 100% à função incluída e 50% à alterada. O Guia tem ainda o FI de 75% e de 90%, para a função que a contratada não desenvolveu, e 30% para a excluída — na planilha de entrega, é o Tipo Projeto que escolhe o fator.
