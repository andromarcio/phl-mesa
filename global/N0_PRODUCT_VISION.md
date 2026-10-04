<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
# Visão de Produto: Portal de Gestão de Participantes em Eventos
> **Nível 0** - Visão de Produto - `GPE`

> O documento de referência mais alto do sistema: define **por que** o produto existe, para **quem** e **que valor** entrega. Os níveis N1–N3 são confrontados contra ele para garantir que não extrapolam o escopo nem contradizem os objetivos do produto. O N0 dá a direção; não detalha funcionalidades, telas ou campos.
>
> **Identidade**: o nome e a sigla vêm de `global/MASTER.md` → *Identificação do sistema*, a fonte única — aqui eles só se repetem (o `validate-doc` reprova sigla divergente).
>
> **Quem mantém**: PO / Liderança de Produto
> **Atualização**: revisado quando a estratégia do produto muda — não a cada feature.

> ⚠️ **Visão reconstruída, não declarada.** Este N0 foi montado por engenharia reversa em 2026-09-30, a partir dos documentos legados GPE001 a GPE006, do código e do projeto `PDTIC25148` no Jira. Nenhuma dessas fontes traz uma visão de produto escrita: propósito, objetivos e personas foram **inferidos 🔍** do que o sistema faz, e as metas não constam em fonte nenhuma ❓. O PO precisa validar este documento antes que ele sirva de régua para os demais níveis.

---

## Propósito

🔍 A CNI organiza reuniões, comitês e seminários com mesa — encontros em que importa quem está presente, de que organização vem, que papel tem e **onde se senta**. Montar essa mesa exige juntar a lista de convidados que sai do CRM, saber quem confirmou, acompanhar quem chegou e posicionar cada pessoa segundo a sua categoria. Sem um sistema, esse trabalho se espalha por planilhas e depende da memória de quem organiza. O GPE existe para reunir tudo num lugar só: recebe as listas, registra a chegada, classifica os participantes por legenda e mantém o mapa de assentos que a equipe consulta durante o evento.

---

## Proposta de valor

🔍 Quem organiza o evento monta a mesa a partir dos dados que já existem no CRM, em vez de redigitá-los, e enxerga pela cor da legenda a categoria de cada participante. Quem está na recepção e na secretaria de mesa trabalha sobre a mesma informação, atualizada enquanto o evento acontece: a recepção marca a chegada e a secretaria vê, em instantes, quem chegou e para qual assento deve ser conduzido.

---

## Público-alvo e personas

| Persona | Quem é | Principal dor | O que espera do produto |
|---|---|---|---|
| Administrador | Quem organiza o evento na CNI: cadastra pessoas e eventos, carrega as listas, configura as legendas e monta o mapa de assentos | Juntar convidados, confirmados e histórico vindos de fontes diferentes e decidir a posição de cada um 🔍 | Preparar o evento inteiro num só lugar e ajustar a mesa até o último momento |
| Secretaria Check-In | Quem recebe os participantes na entrada do evento | Localizar depressa quem chegou e registrar a presença, inclusive de quem não estava na lista 🔍 | Achar a pessoa pelo nome, marcar o check-in e cadastrar na hora quem não constava |
| Secretaria Mesa | Quem conduz os participantes aos seus lugares | Saber quem já chegou e qual é o assento de cada um 🔍 | Ver a fila de quem fez check-in, localizar o assento no mapa e marcar quem já foi atendido |
| Participante | O convidado do evento | — | Não usa o sistema; é quem se beneficia de uma recepção ágil e de um lugar definido 🔍 |

> ⚠️ O cadastro corporativo do sistema traz ainda os perfis **Painel** e **Participante**, que nenhuma tela usa e que os documentos legados não mencionam. Não está claro a que uso se destinam ❓.

---

## Objetivos do produto

> O **quê** o produto busca alcançar — em linguagem de negócio, sem soluções técnicas.

1. 🔍 Reunir num só lugar as pessoas convidadas e o que se sabe sobre elas — organização, cargo, grupos de trabalho, temas e histórico de participação.
2. 🔍 Receber do CRM, por planilha ou por integração, quem foi convidado e quem confirmou presença em cada evento.
3. 🔍 Registrar a chegada dos participantes durante o evento e deixá-la visível, de imediato, para quem conduz à mesa.
4. 🔍 Classificar os participantes por legenda segundo regras que o organizador define para cada evento.
5. 🔍 Montar e manter o mapa de assentos, e entregá-lo em formato que possa ser impresso ou compartilhado.

---

## Métricas de sucesso (KPIs)

> Como saberemos que o produto está cumprindo seus objetivos.

| KPI | O que mede | Meta |
|---|---|---|
| ❓ a definir | Nenhuma das fontes — documentos legados, código, Jira — traz indicador ou meta | ❓ |

---

## Escopo

### Está dentro

- Acesso ao sistema e manutenção dos usuários, sobre o cadastro corporativo da CNI
- Cadastro de pessoas e carga de seus grupos de trabalho, temas e histórico de participação
- Cadastro de eventos, com a escolha do evento principal
- Lista de participantes de cada evento: carga de convidados e de confirmados, importação de inscritos do CRM e cadastro na recepção
- Check-in, confirmação de presença e atendimento durante o evento
- Mapa de assentos: atribuição, consulta, busca e exportação
- Legendas: catálogo, configuração por evento, simulação e geração

### Está fora (não-objetivos)

- 🔍 Envio de convites e coleta de confirmações — isso acontece no CRM; o GPE recebe o resultado
- 🔍 Inscrição do próprio participante — não há tela para o convidado
- 🔍 Gravação de dados no CRM — a integração é só de leitura
- 🔍 Emissão de crachás e cartões de mesa — o sistema guarda o cargo do cartão, mas não imprime
- Cadastro de tipos de evento e de tipos de mesa — as duas listas são mantidas fora das telas
- ⚠️ Desenho livre da mesa — os formatos e a quantidade de assentos são fixos (o Jira tem em aberto o item *Construtor de mesa*, `PDTIC25148-26`)

---

## Major Feature Sets previstos (N1)

> Visão preliminar das grandes áreas que comporão o sistema. Cada uma será detalhada em seu próprio N1. Mantenha esta lista alinhada com `modules/INDEX.md`.

| Major Feature Set | SIGLA | O que cuida |
|---|---|---|
| Acesso e Usuários | ACE | Entrada no sistema, senha, dados do usuário logado e manutenção dos usuários e de seus perfis |
| Pessoas | PES | Cadastro das pessoas que podem ser convidadas e das informações que as qualificam: grupos de trabalho, temas e histórico |
| Eventos | EVT | Cadastro dos eventos, participantes de cada um, check-in, mapa de assentos e legendas |

---

## Tom de voz e princípios de experiência

- **Tom**: 🔍 direto e objetivo — as mensagens do sistema são curtas ("Check-in realizado.", "Evento removido com sucesso"). ❓ Não há guia de tom de voz em fonte nenhuma
- **Princípios**: 🔍 o que acontece na recepção aparece para a secretaria de mesa sem que ninguém precise recarregar a tela · a cor da legenda identifica a categoria do participante na lista e no mapa · o mapa é manipulado diretamente, arrastando a pessoa para o assento

---

## Restrições e premissas

- O sistema não tem base própria de usuários: depende dos serviços corporativos da CNI para autenticar, para manter usuários e para decidir o que cada perfil pode fazer.
- A pessoa é reconhecida pelo `Cód. Contato` do CRM. ⚠️ Premissa: esse código é único e estável — o sistema não o garante.
- Os formatos de mesa são dois, Retangular e Retangular Invertido, com quantidade fixa de assentos por setor.
- ⚠️ O sistema não registra quem executou as ações; só algumas datas. Se a organização precisa de trilha de auditoria, ela ainda não existe.
- ❓ Volume esperado (pessoas na base, participantes por evento, eventos simultâneos) não consta em fonte nenhuma.

---

## Changelog

<!-- Ordem decrescente por data: a entrada mais recente fica sempre no topo, logo abaixo do cabeçalho. -->

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-09-30 | Claude (analista-requisitos) | N0 criado | Visão reconstruída por engenharia reversa dos documentos legados GPE001 a GPE006, do código e do projeto `PDTIC25148` no Jira — a validar com o PO |

---

## Instrução para a LLM

Ao gerar ou alterar qualquer N1/N2/N3:
1. Confronte o artefato com este N0 — escopo, objetivos e público-alvo.
2. Sinalize com ⚠️ qualquer divergência (funcionalidade que extrapola a visão, contradição de objetivo, persona não prevista).
3. O N0 é documento de visão — **não o reestruture** para acomodar detalhes de implementação. Proponha ajustes e peça aprovação antes de alterá-lo.
