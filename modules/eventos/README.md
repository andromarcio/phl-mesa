<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
<!--
  CONVENÇÃO DE VISIBILIDADE
  Blocos <div class="dev-only"> contêm detalhes técnicos.
  Versão PO  → CSS: .dev-only { display: none; }
  Versão DEV → sem CSS adicional
-->

# Major Feature Set: Eventos
> **Nível 1** - Visão estratégica do domínio - `EVT`

## Descrição
Cuida do evento do começo ao fim: o cadastro da reunião, do comitê ou do seminário; a lista de quem foi convidado e de quem confirmou; a chegada dos participantes no dia; o lugar de cada um na mesa; e a legenda que classifica cada participante. Atende o Administrador, que prepara o evento, a Secretaria Check-In, que recebe os participantes, e a Secretaria Mesa, que os conduz aos lugares.

> Marcadores usados neste domínio: 📄 consta nos documentos legados · 💻 consta no código · 🔍 inferido · ❓ nenhuma fonte responde · ⚠️ divergência ou ponto de atenção. Sem marcador = documento e código concordam.

### O que este domínio NÃO faz
| Descrição | Pertence a |
|---|---|
| Manter o cadastro completo da pessoa, seus grupos de trabalho, temas e histórico | Pessoas |
| Enviar convites e coletar confirmações — o GPE recebe o resultado, por planilha ou pelo CRM | CRM da CNI (externo) |
| Gravar qualquer dado no CRM — a integração é só de leitura 💻 | CRM da CNI (externo) |
| Cadastrar tipos de evento e tipos de mesa — as listas são mantidas fora das telas 💻 | — (não existe) |
| Desenhar a mesa livremente ou alterar a quantidade de assentos — os formatos são fixos 💻 | — (não existe) |
| Manter usuários e perfis | Acesso e Usuários |

---

## Feature Sets

| Feature Set | Descrição | Features |
|---|---|---|
| [**Cadastro de Eventos**](./cadastro-eventos/README.md) <small>EVT-CAD</small> | Pesquisar, cadastrar, editar, visualizar e excluir eventos, definir o evento principal e trazer para o evento os convidados, os confirmados e os inscritos do CRM — documento legado GPE004 – Manter Evento | 9 |
| [**Participantes**](./participantes/README.md) <small>EVT-PAR</small> | Pesquisar os participantes do evento, registrar check-in, confirmação e atendimento, tratar a legenda de cada um e montar, consultar e exportar o mapa de assentos — documento legado GPE005 – Gerenciar Participante | 15 |
| [**Legendas**](./legendas/README.md) <small>EVT-LEG</small> | Manter o catálogo de blocos de legenda, configurar os blocos e as condições de cada evento, reaproveitar configurações, simular e gerar as legendas dos participantes — documento legado GPE006 – Gerenciar Regras de Legendas | 14 |

---

## Regras transversais de negócio

1. Existe no máximo um evento principal. Definir um evento como principal retira essa condição de todos os demais.
2. A Secretaria Check-In e a Secretaria Mesa trabalham somente sobre o evento principal. 📄 ⚠️ Na interface, as duas são levadas ao evento principal ao entrar; nada impede que abram outro evento pelo endereço da tela 💻.
3. O evento excluído permanece guardado e deixa de ser exibido — a exclusão é lógica.
4. O participante é a pessoa dentro de um evento. Convidado, Confirmado, Check-In e Atendido são marcações independentes da participação. 💻
5. Os assentos de um evento nascem com ele, em quantidade fixa por tipo de mesa, e cada identificador de assento é único dentro do evento. ⚠️ Mudar o tipo de mesa depois da inclusão não refaz os assentos 💻.
6. Retirar a confirmação de um participante libera o assento que ele ocupava. 💻
7. Alterar a confirmação de um participante que já tinha check-in desfaz o check-in. 💻 ⚠️ Vale nos dois sentidos — inclusive ao confirmar —, o que parece defeito.
8. A legenda pertence à participação da pessoa em um evento, não à pessoa: o mesmo convidado pode ter legendas diferentes em eventos diferentes. 💻
9. A legenda exibida para o participante é a prioritária: a manual, se houver; senão a do bloco de menor número na configuração do evento. 💻
10. A legenda atribuída manualmente não é desfeita pela geração das legendas. 💻 ⚠️ A tela reproduzida em GPE006 avisava o contrário — "A execução REMOVE TODAS as legendas existentes antes de aplicar as novas regras" 📄; a preservação veio com `PDTIC25148-34`.
11. Todo bloco presente na configuração de legendas do evento está em vigor; não existe bloco inativo. 💻 ⚠️ GPE006 descreve legendas ativas e inativas 📄 — o modelo mudou com `PDTIC25148-34`.
12. Nas cargas de planilha e na importação do CRM, a pessoa é reconhecida pelo `Cód. Contato`. → ver [N1 Pessoas](../pessoas/README.md): Regras transversais de negócio: 1

---

## Integrações com outros domínios

### Leitura — domínios que consomem dados deste domínio
| Domínio | O que consome | Como |
|---|---|---|
| Pessoas | Participação em evento — impede a exclusão da pessoa que tem vínculo | FK |
| Acesso e Usuários | Evento principal — destino da Secretaria Mesa e da Secretaria Check-In logo após a autenticação | Serviço |

### Escrita — domínios que criam ou alteram dados deste domínio
| Domínio | O que altera | Situação |
|---|---|---|
| — | Nenhum outro domínio altera eventos, participantes, assentos ou legendas | — |

---

<div class="dev-only">

## Entidades do domínio

| Entidade | Descrição | Campos no DATA-MODEL.md |
|---|---|---|
| Evento | A reunião, o comitê ou o seminário | → ver DATA-MODEL.md: Evento |
| TipoEvento | Classificação do evento | → ver DATA-MODEL.md: TipoEvento |
| TipoMesa | Formato da mesa | → ver DATA-MODEL.md: TipoMesa |
| CadeiraMesa | Assento do mapa do evento | → ver DATA-MODEL.md: CadeiraMesa |
| EventoPessoa | Participação da pessoa no evento — o participante | → ver DATA-MODEL.md: EventoPessoa |
| Legenda | Bloco do catálogo de legendas | → ver DATA-MODEL.md: Legenda |
| EventoLegenda | Bloco de legenda configurado no evento | → ver DATA-MODEL.md: EventoLegenda |
| EventoLegendaCondicao | Condição de um bloco | → ver DATA-MODEL.md: EventoLegendaCondicao |
| EventoPessoaLegenda | Legenda recebida pelo participante | → ver DATA-MODEL.md: EventoPessoaLegenda |
| PresetLegenda | Configuração de legendas guardada para reúso | → ver DATA-MODEL.md: PresetLegenda |

---

## Dependências externas

| Serviço | Uso | Lib sugerida |
|---|---|---|
| CRM da CNI (Dynamics 365) | Consultar os inscritos aprovados e confirmados de uma campanha | — (integração já existente, só leitura) |
| Planilhas extraídas do CRM da CNI | Listas de convidados e de confirmados | Apache POI (já em uso) |
| Geração de imagem e PDF no navegador | Exportar o mapa de assentos | html2canvas e jsPDF (já em uso) |

---

## Regras de acesso consolidadas

| Role | Pode fazer |
|---|---|
| Administrador | Tudo dos três Feature Sets, exceto registrar atendimento |
| Secretaria Check-In | No evento principal: pesquisar participantes, cadastrar participante na recepção, registrar check-in e exportar a lista |
| Secretaria Mesa | No evento principal: consultar o mapa de assentos, buscar pessoa na mesa e registrar atendimento |

⚠️ As três camadas de controle não coincidem 💻. O **menu** só traz Eventos e Catálogo de legendas para o Administrador. A **interface** confere o perfil em poucos pontos — o botão Adicionar da pesquisa de eventos, a tela de participantes e o mapa — e não nas ações por linha da pesquisa de eventos nem nas telas de legendas. O **servidor** decide por recurso e tipo de operação: toda inclusão, alteração e exclusão sob o recurso de eventos está declarada só para o Administrador — o que inclui o cadastro na recepção, usado pela Secretaria Check-In, e deixa sem proteção declarada a pesquisa de participantes e o registro de atendimento. O detalhe está na matriz de cada N2.

---

</div>

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | N1 criado | Engenharia reversa dos documentos legados GPE004 – Manter Evento, GPE005 – Gerenciar Participante e GPE006 – Gerenciar Regras de Legendas, do código e dos tickets `PDTIC25148-34`, `-35` e `-36` do Jira |

---

*Última revisão: —*

*Links: [Cadastro de Eventos](./cadastro-eventos/README.md) · [Participantes](./participantes/README.md) · [Legendas](./legendas/README.md) · [INDEX geral](../INDEX.md)*
