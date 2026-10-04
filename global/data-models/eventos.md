<!-- docqui: 4.0.2 | prompt: PROMPT_CONTAGEM | atualizado: 2026-10-04 -->
# Data Model: Eventos
> **Modelo de entidades (negocial)** — só a parte das entidades, **sem camada física** (sem nomes físicos, tipos de banco, chaves ou índices). A contagem dos arquivos lógicos está no fim, em *Arquivos Lógicos (APF)*. Cole apenas este fragmento nas sessões que envolvam o domínio Eventos.

> Levantado por engenharia reversa em 2026-09-30. 📄 = consta nos documentos legados GPE004, GPE005 ou GPE006 · 💻 = consta no código · 🔍 = inferido · ⚠️ = divergência ou ponto de atenção. Sem marcador = documento e código concordam.

---

## Evento
> **ALI: Evento** · entidade principal
>
> A reunião, o comitê ou o seminário que a CNI organiza: o que acontece, quando, onde e com que formato de mesa.

| Atributo (Label PO) | Tipo | Obrigatório | Notas |
|---|---|---|---|
| Nome do Evento | texto (3 a 100) | sim | ⚠️ GPE004 informa tamanho 255 📄; a tela limita a 100 💻 |
| Data e Hora | data e hora | sim | Sem restrição de data mínima. Evento com data anterior a hoje aparece como Finalizado na pesquisa 💻 |
| Local | texto (3 a 200) | sim | ⚠️ GPE004 informa tamanho 255 📄; a tela limita a 200 💻 |
| Tipo de Evento | seleção → TipoEvento | sim | — |
| Tipo de Mesa | seleção → TipoMesa | sim | Define o desenho do mapa e os assentos gerados na inclusão do evento |
| Participantes | número inteiro (1 a 10.000) | sim | Quantidade prevista. ⚠️ Não interfere na quantidade de assentos, que é fixa por tipo de mesa 💻 |
| Código da Campanha | texto (até 50) | não | Código da campanha no CRM; habilita a importação de inscritos 💻 |
| Arquivo | seleção → Arquivo | não | Imagem relacionada ao evento |
| Principal | sim · não | automático | Só um evento é o principal; é ele que a recepção e a secretaria de mesa enxergam |
| Excluído | sim · não | automático | Exclusão lógica: o evento excluído permanece guardado e deixa de ser exibido |

---

## TipoEvento
> **Dado de código** · não é arquivo lógico: lista de valores válidos, mantida fora das telas (CPM 5.4.2d)
>
> Classificação do evento. Lista mantida fora das telas do sistema 💻.

| Atributo (Label PO) | Tipo | Obrigatório | Notas |
|---|---|---|---|
| Nome | texto | sim | Valores existentes: Reunião, Comitê e Seminário |

---

## TipoMesa
> **Dado de código** · não é arquivo lógico: lista de valores válidos, mantida fora das telas (CPM 5.4.2d)
>
> Formato da mesa do evento. Lista mantida fora das telas do sistema 💻.

| Atributo (Label PO) | Tipo | Obrigatório | Notas |
|---|---|---|---|
| Nome | texto | sim | Valores existentes: Retangular e Retangular Invertido. ⚠️ GPE004 só lista Retangular 📄 |
| Disposição | lista (Retangular, Retangular Invertido) | sim | É o que decide quantos assentos cada setor recebe e como o mapa é desenhado 💻 |

---

## CadeiraMesa
> **ALI: Evento** · subgrupo (os assentos nascem com o evento)
>
> Um assento do mapa do evento, com identificador fixo. Os assentos nascem com o evento.

| Atributo (Label PO) | Tipo | Obrigatório | Notas |
|---|---|---|---|
| Evento | seleção → Evento | sim | Cada evento tem o seu conjunto de assentos |
| Identificação | texto (letra do setor + número) | automático | Por exemplo `A1`, `B12`. Único dentro do evento |
| Composição | lista (Principal, Lateral) | automático | Setores A, B, C e D compõem a mesa principal; E, F, G e H, as laterais 💻 |

---

## EventoPessoa
> **ALI: Evento** · subgrupo (entidade associativa com atributos, dependente do evento)
>
> A participação de uma pessoa em um evento — o **participante**. Guarda o que aconteceu com ela naquele evento: convite, confirmação, check-in, atendimento e assento.

| Atributo (Label PO) | Tipo | Obrigatório | Notas |
|---|---|---|---|
| Evento | seleção → Evento | sim | — |
| Pessoa | seleção → Pessoa | sim | → ver data-models/pessoas.md. ⚠️ O sistema não impede a mesma pessoa duas vezes no mesmo evento 💻 |
| Convidado | sim · não | automático | Ligado pela carga de convidados e pela importação do CRM; não há ação de tela que o altere. Pode ficar sem valor, e então a lista e a planilha mostram Pendente 💻 |
| Confirmado | sim · não | não | Ligado pela carga de confirmados e pela importação do CRM; o Administrador pode alterá-lo na lista de participantes. Pode ficar sem valor (Pendente) 💻 |
| Check-In | sim · não | não | Marcado e desmarcado na lista de participantes |
| Data e hora do check-in | data e hora | automático | ⚠️ É regravada também quando o check-in é desmarcado; fica vazia quando o check-in nasce do cadastro na recepção com check-in automático; e é apagada quando a confirmação é alterada e, para quem está sentado, quando o mapa de assentos é gravado 💻 |
| Atendido | sim · não | não | Marcado pela secretaria de mesa. ⚠️ A gravação do mapa de assentos pode desfazê-lo: volta a não quem perdeu o assento, e quem continua sentado recebe o valor que a tela do Administrador tinha 💻 |
| Assento | seleção → CadeiraMesa | não | Assento atribuído no mapa |
| Data de envio do formulário | data e hora | não | Vem do CRM, na importação de inscritos 💻. ⚠️ Este e os outros quatro dados vindos do CRM são apagados, para quem está sentado, quando o mapa de assentos é gravado 💻 |
| Status da Inscrição | texto | não | Vem do CRM 💻 |
| Status Aprovação | texto | não | Vem do CRM 💻 |
| Identificação da inscrição no CRM | texto | não | Vem do CRM; liga o participante ao registro de origem 💻 |
| Identificação do contato no CRM | texto | não | Vem do CRM 💻 |

---

## Legenda
> **ALI: Legenda** · entidade principal
>
> Um bloco do catálogo de legendas: a categoria que classifica o participante (por exemplo, Anfitrião ou Palestrantes), com a cor que a identifica na lista e no mapa. Na tela é chamada de **bloco**.

| Atributo (Label PO) | Tipo | Obrigatório | Notas |
|---|---|---|---|
| Nome da legenda | texto (até 100) | sim | Único no catálogo, sem diferenciar maiúsculas de minúsculas 💻 |
| Cor | cor (formato `#RRGGBB`) | sim | — |

---

## EventoLegenda
> **ALI: Evento** · subgrupo (entidade associativa com atributos, dependente do evento)
>
> Um bloco de legenda colocado na configuração de um evento. É a presença do bloco que o põe em vigor naquele evento.

| Atributo (Label PO) | Tipo | Obrigatório | Notas |
|---|---|---|---|
| Evento | seleção → Evento | sim | — |
| Legenda | seleção → Legenda | sim | Uma mesma legenda aparece uma única vez na configuração do evento 💻 |
| Nº | número inteiro | automático | Posição do bloco na configuração; é a ordem de aplicação e a prioridade. Recalculado a cada alteração 💻 |

---

## EventoLegendaCondicao
> **ALI: Evento** · subgrupo (entidade atributiva do bloco do evento)
>
> Uma condição de um bloco: o teste que decide se o participante recebe a legenda.

| Atributo (Label PO) | Tipo | Obrigatório | Notas |
|---|---|---|---|
| Bloco | seleção → EventoLegenda | sim | — |
| Ordem | número inteiro | automático | Posição da condição dentro do bloco |
| Conectivo | lista (E, OU) | não | Liga a condição à anterior; não existe na primeira condição do bloco |
| Campo | lista (Grupo de trabalho, Tema, Cargo, Nome fantasia, Papel desempenhado) | não | Dado da pessoa que a condição avalia |
| Operador | lista (Igual a, Diferente de, Contém, Em (lista)) | não | — |
| Valor | texto (até 1.000) | não | Com o operador Em (lista), os valores vêm separados por vírgula |

---

## EventoPessoaLegenda
> **ALI: Evento** · subgrupo (entidade associativa com atributos, dependente do participante)
>
> A legenda que um participante recebeu num evento — por regra ou manualmente.

| Atributo (Label PO) | Tipo | Obrigatório | Notas |
|---|---|---|---|
| Participante | seleção → EventoPessoa | sim | — |
| Legenda | seleção → Legenda | sim | O participante pode ter mais de uma legenda atribuída por regra; a exibida é a prioritária 💻 |
| Manual | sim · não | automático | Sim quando foi atribuída na tela, participante por participante; a legenda manual não é desfeita pela geração das legendas |
| Data de atribuição | data e hora | automático | ⚠️ Não é atualizada quando uma legenda recebida por regra é tornada manual 💻 |

---

## PresetLegenda
> **ALI: PresetLegenda** · entidade principal
>
> Uma configuração de legendas guardada com nome, para ser reaproveitada em outros eventos.

| Atributo (Label PO) | Tipo | Obrigatório | Notas |
|---|---|---|---|
| Nome do preset | texto (até 100) | sim | Único 💻 |
| Descrição | texto (até 255) | não | — |
| Evento de origem | texto | automático | Cópia do nome do evento em que o preset foi salvo; não acompanha mudanças posteriores no evento |
| Data de criação | data e hora | automático | — |
| Configuração | conjunto de blocos e condições | sim | Retrato dos blocos, da ordem e das condições no momento em que o preset foi salvo |

---

## Relacionamentos

- **Evento** [N — 1] **TipoEvento** — todo evento tem um tipo
- **Evento** [N — 1] **TipoMesa** — todo evento tem um formato de mesa
- **Evento** [N — 1] **Arquivo** — a imagem do evento, quando há → ver data-models/pessoas.md
- **Evento** [1 — N] **CadeiraMesa** — os assentos do mapa do evento
- **Evento** [1 — N] **EventoPessoa** — os participantes do evento
- **Pessoa** [1 — N] **EventoPessoa** — os eventos de que a pessoa participa → ver data-models/pessoas.md
- **CadeiraMesa** [1 — 1] **EventoPessoa** — o participante que ocupa o assento, quando ocupado. ⚠️ O sistema não impede dois participantes no mesmo assento ao gravar o mapa 💻
- **Evento** [1 — N] **EventoLegenda** — os blocos de legenda configurados no evento, em ordem
- **Legenda** [1 — N] **EventoLegenda** — os eventos em que o bloco do catálogo está em uso
- **EventoLegenda** [1 — N] **EventoLegendaCondicao** — as condições do bloco, em ordem
- **EventoPessoa** [1 — N] **EventoPessoaLegenda** — as legendas do participante naquele evento
- **Legenda** [1 — N] **EventoPessoaLegenda** — os participantes que receberam a legenda

---

## Arquivos Lógicos (APF)

| ALI / AIE | Tipo | Entidades constituintes | RLR | DER | Complexidade | PF | Data |
|---|---|---|---|---|---|---|---|
| Evento | ALI | Evento (principal) · CadeiraMesa, EventoPessoa, EventoLegenda, EventoLegendaCondicao, EventoPessoaLegenda (subgrupos) | 6 | 33 | Alta | 15 | 2026-10-04 |
| Legenda | ALI | Legenda (principal) | 1 | 3 | Baixa | 7 | 2026-10-04 |
| PresetLegenda | ALI | PresetLegenda (principal) | 1 | 5 | Baixa | 7 | 2026-10-04 |

**Total deste domínio: 29 PF**

### Memória de cálculo

**ALI: Evento** — RLR 6 · DER 33 · Alta · 15 PF

Agrupamento: o assento, o participante, o bloco de legenda do evento, a condição do bloco e a legenda do participante não têm significado para o negócio sem o evento a que pertencem — excluído o evento, nenhum deles subsiste —, e por isso são entidades dependentes, agrupadas no arquivo lógico do evento (CPM 4.3.1, Parte 3, cap. 2, subpasso 1.3b). EventoPessoa, EventoLegenda e EventoPessoaLegenda são entidades associativas com atributos de negócio e sem regra que mande guardá-las de forma independente: contam como registro lógico, e não como arquivo próprio (mesmo capítulo, *Analisando Entidades Associativas*, situação 2). O participante é gerido pelo lado do evento — nenhuma tela de pessoa o mostra —, então o registro entra só neste arquivo, e não também no de Pessoa.

RLR (6):

1. Evento — os dados do evento
2. CadeiraMesa — os assentos, que se repetem para cada evento
3. EventoPessoa — o participante, com o que aconteceu com ele no evento
4. EventoLegenda — o bloco de legenda na configuração do evento, com o Nº
5. EventoLegendaCondicao — as condições, que se repetem para cada bloco
6. EventoPessoaLegenda — a legenda que o participante recebeu, com a marca de manual

DER (33):

- Evento (10): Nome do Evento, Data e Hora, Local, Tipo de Evento, Tipo de Mesa, Participantes, Código da Campanha, Arquivo, Principal e o identificador
- CadeiraMesa (2): Identificação e Composição
- EventoPessoa (11): Pessoa, Convidado, Confirmado, Check-In, Data e hora do check-in, Atendido, Data de envio do formulário, Status da Inscrição, Status Aprovação, Identificação da inscrição no CRM e Identificação do contato no CRM
- EventoLegenda (2): Legenda e Nº
- EventoLegendaCondicao (5): Ordem, Conectivo, Campo, Operador e Valor
- EventoPessoaLegenda (3): Legenda do participante, Manual e Data de atribuição

Não contados: Excluído, que é o marcador da exclusão lógica e faz o papel do campo técnico de exclusão (`global/SIZING.md` → *Como contar DER*); as referências de CadeiraMesa, EventoPessoa e EventoLegenda ao evento, de EventoLegendaCondicao ao bloco e de EventoPessoaLegenda ao participante, que são ligações internas ao arquivo lógico; e o Assento do participante, que repete a Identificação do assento, já contada. Tipo de Evento e Tipo de Mesa contam como atributos do evento, embora as duas listas sejam dado de código. Pessoa e as duas Legendas são referências a outros arquivos lógicos e contam um DER cada.

Margem: seis registros lógicos são o primeiro valor da faixa mais alta. Com cinco — se o bloco e as condições dele fossem lidos como um registro só —, a complexidade seria Média, 10 PF. Em DER a folga é larga: a faixa vai de 20 a 50.

**ALI: Legenda** — RLR 1 · DER 3 · Baixa · 7 PF

O bloco do catálogo é independente: existe sem evento nenhum e é mantido por Cadastrar, Editar e Excluir Bloco de Legenda. RLR (1): Legenda. DER (3): Nome da legenda, Cor e o identificador.

**ALI: PresetLegenda** — RLR 1 · DER 5 · Baixa · 7 PF

O preset é independente do evento em que foi salvo: guarda cópia da configuração e continua existindo depois que o evento muda ou é excluído. RLR (1): PresetLegenda. DER (5): Nome do preset, Descrição, Evento de origem, Configuração e o identificador. Não contado: Data de criação, campo técnico de criação que nenhuma tela mostra. A Configuração foi contada como o modelo a descreve, um atributo só; desdobrada em blocos e condições, seriam 3 RLR e 11 DER, e a complexidade continuaria Baixa.

**Dados de código** — TipoEvento e TipoMesa não são arquivos lógicos nem entram como arquivo referenciado nas transações: são listas de valores válidos, mantidas fora das telas (CPM 5.4.2d; Guia de Métricas da STI, 4.15 e 5.5).

**Referenciado de outro domínio** — Pessoa, do domínio Pessoas, é lido pelas transações de Eventos. Está registrado em `global/ALI-AIE-MAP.md` como pendente: o tamanho dele sai da contagem do domínio Pessoas.

**AIE** — nenhum nas features contadas até aqui. A importação de inscritos do CRM grava dados no arquivo lógico Evento e será avaliada na contagem de Importar Inscritos do CRM `EVT-CAD-09`.

---

## Changelog

| Data | Autor | Tipo | Descrição |
|---|---|---|---|
| 2026-10-04 | Claude (apf-cpm) | Contagem | Funções de dados do domínio dimensionadas pelo `PROMPT_CONTAGEM`: Evento (Alta, 15 PF), Legenda (Baixa, 7 PF) e PresetLegenda (Baixa, 7 PF) — 29 PF; cada entidade anotada com o arquivo lógico a que pertence. Confirmada em 2026-10-04 e espelhada em `global/CONTAGEM-PF.md` |
| 2026-09-30 | Claude (analista-requisitos) | Fragmento criado | Engenharia reversa dos documentos legados GPE004 – Manter Evento, GPE005 – Gerenciar Participante e GPE006 – Gerenciar Regras de Legendas e do código (entidades, estrutura do banco e telas) |
