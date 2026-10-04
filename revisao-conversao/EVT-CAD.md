<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
# Revisão da conversão — Cadastro de Eventos

> Detalhe, feature a feature, do que precisa de olho humano no Feature Set **Cadastro de Eventos** (`EVT-CAD`), gerado na engenharia reversa de 2026-09-30. O resumo e as prioridades estão em [`REVISAO-CONVERSAO.md`](../REVISAO-CONVERSAO.md).
>
> **Como ler.** Cada feature traz quatro listas: **⚠️ Divergências documento × código** (decidir qual vale), **❓ Lacunas** (nenhuma fonte responde — precisa do PO), **🔍 Inferências a confirmar** (provavelmente certas) e **⚠️ Suspeitas de defeito** (o código faz algo que parece errado). Tudo veio da **leitura** do código — nada foi executado; o que depende de execução está dito como inferência.
>
> **Referências.** `arquivo:linha` aponta para o código-fonte: no front, pelo nome do arquivo; no back, pelo caminho a partir de `br/com/cni/apimesacheckin/`. "Inventário", **FI** e **BI** são os inventários do front e do back, guardados em [`arquivos/engenharia-reversa/`](../arquivos/engenharia-reversa/README.md). 

---

## EVT-CAD-01 — Pesquisar Eventos

**⚠️ Divergências documento × código**
- Filtro Data Final: GPE004 o lista ao lado da Data Inicial, como período de realização; o código não o usa como limite — repete a comparação da Data Inicial (`>=`) e, informado sozinho, é ignorado (`service/impl/EventoServiceImpl.java:147-153`).
- Tipo de Mesa: GPE004 só lista "Retangular"; o código tem Retangular e Retangular Invertido, vindos do servidor (`eventos-filter.component.ts:85-98`; `enumeration/TipoMesaEnum.java:5`).
- Selo "Finalizado", linha esmaecida e texto relativo da data: aparecem na imagem "Pesquisar Evento" de GPE004, mas o texto do documento não os descreve; no código, `evento-list.component.html:42-57` e `evento-list.component.ts:148-169`.
- Ícones de ação por linha: aparecem na imagem, sem descrição no texto (o documento só diz que "a partir do resultado, é possível realizar a gestão de cada evento"); no código, oito ícones (`evento-list.component.html:86-105`).
- Paginador: a imagem de GPE004 mostra o total de registros ("[1 a 4 de 4]") e um seletor de linhas por página; o template atual não tem nenhum dos dois (`evento-list.component.html:3-17`).

**❓ Lacunas**
- Se a pesquisa por Nome e Local ignora acentos: depende da configuração do banco; o código só trata maiúsculas e minúsculas (`service/impl/EventoServiceImpl.java:102-110`).
- O que a Data Final deveria fazer exatamente (incluir o próprio dia até 23h59?): o documento não diz e o código não implementa.
- Rótulo e ordem do menu "Eventos › Cadastro": vêm do serviço corporativo, não do front (`menu.component.ts:30-40`); usei o texto de GPE004 e a declaração do back (`configuracoes.json:392-503`).

**🔍 Inferências a confirmar**
- A primeira página pode vir com 5 linhas numa lista de 10: a carga inicial pede 5, a tabela pede 10, e não se sabe qual resposta prevalece (`evento-list.component.ts:20`, `:67-72`; `evento-list.component.html:7`).
- Na falha de consulta a lista "permanece como estava": deduzido de o erro só ir para o console (`evento-list.component.ts:97-100`).

**⚠️ Suspeitas de defeito**
- Filtro Data Final sem efeito — item 1 de 6.1 do `backend-inventory.md` (`service/impl/EventoServiceImpl.java:147-153`).
- **Novo, não consta nos inventários** — texto relativo da data calculado em blocos de 24 horas a partir de agora, e não por dia do calendário: o evento de hoje que ainda vai começar aparece como "Amanhã"; "Hoje" só aparece para o evento que começou há menos de 24 horas (`evento-list.component.ts:152-169`).
- Falha ao carregar os tipos de mesa zera a lista de tipos de evento — item 21 de 8.4 (`eventos-filter.component.ts:93-96`).
- Falha na consulta de eventos sem nenhum aviso ao usuário (`evento-list.component.ts:97-100`).
- Carga inicial de 5 linhas × 10 por página e `colspan="7"` em tabela de 8 colunas — item 22 de 8.4 (`evento-list.component.html:7`, `:110`; `evento-list.component.ts:20`, `:67-72`, `:211-216`).
- "Criar Primeiro Evento" e todas as ações por linha sem conferência de perfil — item 20 de 8.4 (`evento-list.component.html:86-116`).
- `/eventos/**` redireciona para `/notfound`, rota inexistente — item 24 de 8.4 (`evento-routing.module.ts:12`). Não entrou no N3: é rota técnica, sem comportamento de negócio.

---

## EVT-CAD-02 — Cadastrar Evento

**⚠️ Divergências documento × código**
- Nome do Evento: GPE004 informa tamanho 255, sem mínimo; a tela exige de 3 a 100 (`evento-create.component.html:22-44`; `evento-create.component.ts:116-123`).
- Local: GPE004 informa 255; a tela exige de 3 a 200 (`evento-create.component.html:78-100`; `evento-create.component.ts:125-132`).
- Participantes: GPE004 diz "numérico inteiro", sem faixa; a tela limita de 1 a 10.000 (`evento-create.component.ts:135-138`).
- Tipo de Mesa: GPE004 só lista "Retangular"; o código tem dois tipos.
- **Composição da mesa**: as faixas de GPE004 (A1–A5, B1–B34, C1–C34, D1–D5, E1–E30, F1–F28, G1–G10, H1–H28 = 174 assentos) são, no código, as do tipo Retangular Invertido; o tipo Retangular do código tem B1–B35, C1–C35, E1–E23, F1–F32, H1–H36 = 181 assentos (`service/impl/CadeiraMesaServiceImpl.java:88-121`, `:123-156`, `:158-210`). Conferido no código-fonte.
- Arquivo: GPE004 diz "Permite anexar arquivos ao cadastro do evento"; o código aceita uma única imagem (`accept="image/*"`, 200 MB) (`evento-create.component.html:193-233`).
- Código da Campanha: não existe em GPE004 nem na imagem "Incluir / Editar Evento"; existe no código (`evento-create.component.html:173-188`; `evento-create.component.ts:139`) — ticket `PDTIC25148-36`, CA01.
- Obrigatoriedade: GPE004 marca seis campos como obrigatórios; no código só a tela confere — o servidor não valida nada (`service/impl/EventoServiceImpl.java:166-178`).

**❓ Lacunas**
- Qual composição vale para cada tipo de mesa: o documento só conhece um tipo, e o código tem dois com quantidades diferentes. Decisão do PO.
- Se a quantidade de Participantes deveria definir o número de assentos: o cálculo que a usaria está desativado no código (`service/impl/CadeiraMesaServiceImpl.java:90-91`, `:125-126`).
- Se dois eventos podem ter o mesmo nome: o documento não fala; o código permite.
- O que a tela mostra quando o servidor recusa a gravação por falta de permissão: depende do código de resposta do serviço corporativo de acesso, que o back apenas repassa (`corporativo/service/AccessTokenAutenticadoService.java:40-43`). Vale para todas as features de gravação deste Feature Set.
- GPE004 cita o ticket da v1.1 como "DTIC25148-32" (sem o P); no Jira, `PDTIC25148-32` é "Ajustes na Mesa - Exibir a cabeceira no topo". Presumi que são o mesmo e mantive a grafia do documento.

**🔍 Inferências a confirmar**
- As mensagens "Máximo de {n} caracteres", "Valor mínimo é 1" e "Valor máximo é 10000" existem (`cadastro-helper.ts:9-23`), mas o campo impede o excesso (`maxlength`) e o campo numérico ajusta o valor — não observei em execução.
- O aviso "Formulário inválido" / "Preencha todos os campos obrigatórios corretamente" não é alcançável pelo botão "Salvar", que fica desabilitado com o formulário inválido (`evento-create.component.ts:202-209`; `evento-create.component.html:273-281`).
- Imagem, evento e assentos são gravados em etapas sem transação: falha na geração dos assentos deixaria o evento gravado sem assentos (`service/impl/EventoServiceImpl.java:166-167`).
- Os assentos são gerados pelo indicador do tipo de mesa enviado pela tela, não pelo relido do banco (`service/impl/EventoServiceImpl.java:169-176`) — inferência do próprio inventário (3.e).

**⚠️ Suspeitas de defeito**
- Quantidade de assentos fixa no código, com o uso de Participantes comentado — item 4 de 6.1 (`service/impl/CadeiraMesaServiceImpl.java:90-91`, `:125-126`).
- `excluido` não é inicializado pelo servidor — item 15 de 6.1; a tela envia `false`, e `principal` vai nulo (`evento-create.component.ts:141-142`).
- Botão "Adicionar" liberado para um perfil "Gestor" inexistente, e "Criar Primeiro Evento" sem conferência de perfil — item 20 de 8.4 (`eventos-filter.component.html:71`; `evento-list.component.html:108-120`).
- Listas de tipos que não carregam não geram aviso (`evento-create.component.ts:85-111`).

---

## EVT-CAD-03 — Editar Evento

**⚠️ Divergências documento × código**
- Tamanhos de Nome do Evento e Local: 255 no documento; 100 e 200 na tela (mesmas referências do cadastro).
- Código da Campanha: não está no documento (ticket `PDTIC25148-36`, CA01).
- O documento diz que a edição "consiste em alterar os dados básicos"; no código, salvar a edição também regrava Excluído (sempre "não") e Principal (o valor de quando a tela abriu) (`evento-create.component.ts:141-158`, `:176-177`; `service/impl/EventoServiceImpl.java:166-178`).

**❓ Lacunas**
- O que deve acontecer com os assentos — e com os participantes já sentados — quando o tipo de mesa muda: nenhuma fonte responde.
- Se a edição deveria registrar quem alterou e quando: o sistema não guarda nada (`backend-inventory.md` §5).

**🔍 Inferências a confirmar**
- Depois da troca do tipo de mesa, o mapa é desenhado no formato novo com os assentos do antigo: de Retangular para Invertido sobram B35, C35, F29–F32, H29–H36 e faltam E24–E30 (deduzido de `mesa.component.html:1-8`, `retangular.component.ts:746-793` e das faixas de 3.e).
- **Novo** — a edição reenvia a condição de principal lida na abertura da tela; se o principal mudar nesse intervalo, salvar pode deixar dois eventos principais ou nenhum (`evento-create.component.ts:157`, `:176`; `service/impl/EventoServiceImpl.java:169-174`). Com dois principais, a consulta do principal (`repository/EventoRepository.java:13`) tende a falhar.
- **Novo** — o formulário sempre envia Excluído = não; um evento excluído, aberto pelo endereço e salvo, volta à pesquisa (`evento-create.component.ts:141`; `service/impl/EventoServiceImpl.java:161-164`).
- Sem controle de alteração simultânea: vale o último que salvar.
- Evento inexistente abre a tela em branco, sem aviso: a leitura não tem tratamento de erro (`evento-create.component.ts:69-78`).

**⚠️ Suspeitas de defeito**
- Trocar o tipo de mesa não refaz os assentos — item 3 de 6.1 (`service/impl/EventoServiceImpl.java:166-178` no caminho que a tela usa; `:190-210` no `PUT`).
- **Correção ao ponto de atenção recebido** — "a edição não grava o conteúdo de um arquivo novo" (item 2 de 6.1) vale para a operação `PUT /administracao/eventos/{id}` (`service/impl/EventoServiceImpl.java:204`), que **a tela não chama**. A tela grava a edição por `POST /administracao/eventos` com o identificador (`evento-create.component.ts:177`; `form-helper.ts:44-52`), e esse caminho grava o conteúdo da imagem (`service/impl/EventoServiceImpl.java:170-173`; `service/impl/ArquivoServiceImpl.java:48-79`). Não registrei a suspeita como defeito no N3; deixei as duas operações descritas no bloco dev-only.
- A imagem trocada ou retirada continua guardada — 3.h (`service/impl/ArquivoServiceImpl.java:48-79`).

---

## EVT-CAD-04 — Visualizar Evento

**⚠️ Divergências documento × código**
- Título da tela: a imagem "Detalhar Evento" de GPE004 mostra "Dados do Evento"; o código mostra "Editar Evento" — item 19 de 8.4 (`evento-create.component.html:7-10`).
- Nome da funcionalidade no próprio documento: "Visualizar Evento" na descrição, "Detalhar Evento" na tela e na tabela de perfis.
- Código da Campanha: exibido pelo código (`evento-create.component.html:187`); não está na imagem.
- Evento excluído: GPE004 diz que ele "passa a não ser exibido no sistema"; a leitura de um evento não filtra o excluído (`service/impl/EventoServiceImpl.java:161-164`).

**❓ Lacunas**
- Se a visualização deveria mostrar a condição de principal e a quantidade de participantes do evento: nenhuma fonte pede; o código não mostra.

**🔍 Inferências a confirmar**
- Evento inexistente: tela em branco, sem aviso (`evento-create.component.ts:69-78`).
- Falha no download da imagem sem aviso (`evento-create.component.ts:248-263`); imagem inexistente gera erro 500 no servidor — item 13 de 6.1.

**⚠️ Suspeitas de defeito**
- Título "Editar Evento" no modo de leitura — item 19 de 8.4.
- Asteriscos de obrigatório e "Campos com * são obrigatórios" continuam na tela de leitura (`evento-create.component.html:22-24`, `:258-263`) — presente também na imagem de GPE004.

---

## EVT-CAD-05 — Excluir Evento

**⚠️ Divergências documento × código**
- GPE004: "o evento passa a não ser exibido no sistema"; no código o excluído só sai da pesquisa de eventos, da consulta do principal e da lista de eventos de origem de legendas — a leitura por identificador e as operações de participantes não o distinguem (`service/impl/EventoServiceImpl.java:89`, `:161-164`; `repository/EventoRepository.java:13`). Conferido por busca do campo no código do back.
- Mensagem de confirmação "Essa operação não poderá ser desfeita." × exclusão lógica: os dados ficam guardados (`evento-list.component.ts:111-116`; `service/impl/EventoServiceImpl.java:180-188`).

**❓ Lacunas**
- Se a exclusão do evento principal deveria ser impedida ou avisar: nenhuma fonte responde.
- Se deveria existir restauração do evento excluído: não existe operação para isso.

**🔍 Inferências a confirmar**
- Excluído o evento principal, as secretarias ficam sem evento: decorre de a consulta do principal exigir "não excluído" (`service/impl/EventoServiceImpl.java:433-437`) e do item 3 de 8.4 (login sem evento principal).

**⚠️ Suspeitas de defeito**
- Exclusão sem verificação de vínculos — 3.a (`service/impl/EventoServiceImpl.java:180-188`).
- A exclusão do evento principal mantém a marcação de principal no evento excluído e deixa o sistema sem principal disponível.
- O servidor responde sucesso também para evento inexistente ou já excluído — 4.2, "Respostas silenciosas" (`controller/EventoController.java:104-108`).
- Ícone sem conferência de perfil — item 20 de 8.4.

---

## EVT-CAD-06 — Definir Evento Principal

**⚠️ Divergências documento × código**
- Sem divergência de regra: documento e código concordam em um único principal. Nome: "Tornar Evento como Principal" no documento, dica "Tornar evento principal" na tela; o N2 fixou "Definir Evento Principal".
- O documento não fala em confirmação; o código não pede nenhuma (`evento-list.component.html:90-91`).

**❓ Lacunas**
- Se um evento finalizado pode ser o principal: nenhuma fonte restringe.
- Se deve existir uma forma de deixar o sistema sem evento principal: não há ação para isso.

**🔍 Inferências a confirmar**
- Evento excluído por outra pessoa, acionado numa lista desatualizada, passa a principal e o sistema fica sem principal disponível (`service/impl/EventoServiceImpl.java:424-431`, `:433-437`).
- A troca não é indivisível: falha no meio deixa marcações misturadas (sem transação).

**⚠️ Suspeitas de defeito**
- Regrava todos os eventos, inclusive excluídos, sem transação e sem validar o identificador; texto de erro copiado de outra operação — item 14 de 6.1 (`service/impl/EventoServiceImpl.java:424-431`; `controller/EventoController.java:223`).
- A tela não trata o erro: nenhuma mensagem na falha (`evento-list.component.ts:207-219`).
- A recarga depois da troca pede 5 linhas — item 22 de 8.4 (`evento-list.component.ts:211-216`).
- Ícone sem conferência de perfil — item 20 de 8.4.

---

## EVT-CAD-07 — Carregar Convidados

**⚠️ Divergências documento × código**
- Colunas obrigatórias: GPE004 dá sete (Cód. Contato, Nome Completo, Sexo, Cargo, Cargo do Cartão, Empresa/Entidade, Email Comercial); o código só exige Nome Completo (`service/impl/EventoPessoaServiceImpl.java:364-365`).
- Leitura das colunas: GPE004 diz que "o arquivo deve conter as seguintes colunas"; o código as lê por posição fixa e não confere o cabeçalho (`enumeration/ExcelHeadersEnum.java:7-20`; `service/impl/EventoPessoaServiceImpl.java:334-407`).
- Pessoa já existente: GPE004 só fala em cadastrar e em validar a existência pelo Cód. Contato; o código atualiza todos os campos da pessoa, inclusive com valores em branco (`service/impl/EventoPessoaServiceImpl.java:367-387`).
- Janela: a imagem de GPE004 tem duas seções; o código tem três, com "Inscritos do CRM" (`evento-participantes.component.html:109-127`).
- Extensões: GPE004 diz "apenas arquivos do .xls e xlsx"; só a tela restringe — o servidor não confere extensão, tipo nem tamanho (`backend-inventory.md` §3.c).

**❓ Lacunas**
- Se uma nova carga deveria retirar do evento quem saiu da lista: o código só acrescenta; o documento não fala.
- O que fazer com a linha sem Cód. Contato: o documento a proíbe (obrigatória), o código cria pessoa nova a cada carga.
- Se existe planilha-modelo: a tela não oferece nem descreve as colunas (`evento-participantes.component.html`).

**🔍 Inferências a confirmar**
- Duas pessoas com o mesmo Cód. Contato fazem a carga falhar — item 19 de 6.1 (`repository/PessoaRepository.java:14`); a mensagem que chega à tela seria "Ocorreu um erro inesperado. Contate o suporte." (`controller/handler/GlobalExceptionHandler.java:26-31`).
- Cód. Contato, telefone e CNPJ em célula numérica com oito dígitos ou mais são lidos em notação científica — item 18 de 6.1 (`util/ExcelUtils.java:107-109`).
- Carga não transacional: falha numa linha mantém as anteriores (`service/impl/EventoPessoaServiceImpl.java:163-164`).

**⚠️ Suspeitas de defeito**
- CNPJ da planilha gravado no CPF ao atualizar pessoa existente — item 5 de 6.1 (`service/impl/EventoPessoaServiceImpl.java:375`). **Acréscimo**: sem CNPJ na planilha, o CPF da pessoa é apagado (a mesma linha grava vazio).
- Planilha ilegível responde sucesso, e a tela mostra "Carga concluída" — item 20 de 6.1 (`service/impl/EventoPessoaServiceImpl.java:177-179`).
- Sem resumo e sem erro por linha; linhas sem nome descartadas em silêncio — item 20 de 6.1.
- Envio das duas planilhas: a de confirmados deixa de ser enviada — item 23 de 8.4 e Jira `PDTIC25148-33` (detalhe em EVT-CAD-08 — Carregar Confirmados).
- Ícone sem conferência de perfil — item 20 de 8.4.

---

## EVT-CAD-08 — Carregar Confirmados

**⚠️ Divergências documento × código**
- As mesmas de EVT-CAD-07 — Carregar Convidados: colunas obrigatórias, leitura por posição, atualização de quem já existe, janela com três seções.
- GPE004 chama a lista de "convidados confirmados"; no código, quem entra no evento só pela carga de confirmados fica com Convidado = não (`service/impl/EventoPessoaServiceImpl.java:194`, `:342-350`).
- A confirmação pela carga não desfaz o check-in, ao contrário da alteração manual da confirmação (regra transversal 7 do N1 Eventos) (`service/impl/EventoPessoaServiceImpl.java:356-359` × `:427-430`).

**❓ Lacunas**
- Se a carga de confirmados deveria desconfirmar quem não está na planilha: o código nunca desconfirma.
- Se o confirmado que não era convidado deveria receber também a marca de convidado.

**🔍 Inferências a confirmar**
- **Planilhas enviadas juntas**: li `enviarArquivos()` e o *setter* `active` — o aviso de envio é emitido antes; a tela-mãe fecha a janela; ao fechar, as duas planilhas guardadas são zeradas; quando a carga de convidados termina, a de confirmados já não existe e não é enviada (`evento-participantes.component.ts:28-34`, `:202-226`; `evento-list.component.ts:186-190`). Enviada sozinha, a de confirmados é processada. Não executado.
- Demais inferências iguais às de EVT-CAD-07 — Carregar Convidados.

**⚠️ Suspeitas de defeito**
- Planilha de confirmados não enviada quando há também a de convidados — item 23 de 8.4; coincide com o Jira `PDTIC25148-33` (To Do, 2026-06-01).
- CPF trocado pelo CNPJ, falha silenciosa com planilha ilegível e ausência de resumo — as mesmas de EVT-CAD-07 — Carregar Convidados.
- Linha sem Cód. Contato de alguém que já é convidado: a pessoa entra no evento uma segunda vez (`service/impl/EventoPessoaServiceImpl.java:367`, `:390-407`).

---

## EVT-CAD-09 — Importar Inscritos do CRM

**⚠️ Divergências ticket × código** (a funcionalidade não consta em GPE004)
- CA04: o resumo do ticket fala em "lista de inscritos"; o código só traz inscritos com Status Aprovação e Status da Inscrição iguais a um mesmo valor (`service/impl/DynamicsCrmServiceImpl.java:107-109`, `:46`).
- CA05: os dez dados são lidos, mas Data de envio do formulário, Status da Inscrição e Status Aprovação ficam guardados na participação sem aparecer em tela nenhuma — busca pelos campos no front não retorna nada (`service/impl/EventoPessoaServiceImpl.java:287-293`).
- CA07: o inscrito sem Cód. Contato é ignorado, o que o ticket não prevê (`service/impl/EventoPessoaServiceImpl.java:228-235`).
- CA08: a atualização apaga Codinome, E-mail, Razão Social e Cargo quando o CRM não os traz (`service/impl/EventoPessoaServiceImpl.java:306-310`).
- **CA09**: o ticket pede informar que não foram encontrados registros; o servidor devolve erro, e a tela o apresenta sob o título "Erro ao importar inscritos do CRM" (`service/impl/EventoPessoaServiceImpl.java:214-218`; `evento-list.component.ts:203-205`). A lista não é alterada, como o critério pede.
- CA10: os participantes são isolados por evento, mas os dados da pessoa atualizados valem para todos os eventos (`service/impl/EventoPessoaServiceImpl.java:304-313`).
- Empresa do CRM é gravada na Razão Social da pessoa (`service/impl/EventoPessoaServiceImpl.java:309`, `:322`).

**❓ Lacunas**
- Os nomes de negócio das duas situações filtradas: o código compara Status Aprovação e Status da Inscrição com o mesmo valor interno; usei "aprovados e confirmados", da mensagem do servidor.
- Se os dados da inscrição guardados na participação deveriam aparecer em alguma tela.
- Se a importação deveria retirar do evento quem deixou de constar no CRM: o código só acrescenta.

**🔍 Inferências a confirmar**
- O texto "Nenhum registro foi alterado." (`evento-list.component.ts:199`) não chega a ser exibido: com inscritos, alguma contagem é maior que zero; sem inscritos, o servidor devolve erro.
- A mensagem "Informe o código da campanha do CRM." (`service/impl/DynamicsCrmServiceImpl.java:79-82`) não é alcançável: o evento sem código é barrado antes (`service/impl/EventoPessoaServiceImpl.java:209-212`).
- Código da Campanha apagado com a lista aberta leva à mensagem do servidor: a janela usa o evento da linha da lista, que pode estar desatualizado (`evento-participantes.component.ts:59-61`).

**⚠️ Suspeitas de defeito**
- A contagem "sem Cód. Contato (ignorado(s))" inclui o inscrito novo sem nome e sem codinome (`service/impl/EventoPessoaServiceImpl.java:241-245`; `evento-list.component.ts:196`).
- Fora deste Feature Set, mas afeta o que esta feature grava: salvar o mapa de assentos apagaria os dados da inscrição no CRM e a data do check-in — item 6 de 6.1 (inferência do inventário).

---

*Links: [Resumo da revisão](../REVISAO-CONVERSAO.md) · [N2 do Feature Set](../modules/eventos/cadastro-eventos/README.md) · [INDEX geral](../modules/INDEX.md)*
