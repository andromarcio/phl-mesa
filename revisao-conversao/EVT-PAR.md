<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
# Revisão da conversão — Participantes

> Detalhe, feature a feature, do que precisa de olho humano no Feature Set **Participantes** (`EVT-PAR`), gerado na engenharia reversa de 2026-09-30. O resumo e as prioridades estão em [`REVISAO-CONVERSAO.md`](../REVISAO-CONVERSAO.md).
>
> **Como ler.** Cada feature traz quatro listas: **⚠️ Divergências documento × código** (decidir qual vale), **❓ Lacunas** (nenhuma fonte responde — precisa do PO), **🔍 Inferências a confirmar** (provavelmente certas) e **⚠️ Suspeitas de defeito** (o código faz algo que parece errado). Tudo veio da **leitura** do código — nada foi executado; o que depende de execução está dito como inferência.
>
> **Referências.** `arquivo:linha` aponta para o código-fonte: no front, pelo nome do arquivo; no back, pelo caminho a partir de `br/com/cni/apimesacheckin/`. "Inventário", **FI** e **BI** são os inventários do front e do back, guardados em [`arquivos/engenharia-reversa/`](../arquivos/engenharia-reversa/README.md). As features estão em duas partes: primeiro as da lista de participantes (`EVT-PAR-01` a `06`, `13` e `14`), depois as do mapa de assentos (`EVT-PAR-07` a `12` e `15`).

---

> **Nesta parte (lista de participantes)**, a referência seguida de "(código)" não estava nos inventários e foi conferida direto no código.

## Três achados que mudam a leitura do Feature Set

1. **EVT-PAR-04 — Consultar Legenda do Participante mostra só a legenda MANUAL.** A operação que a janela chama devolve a primeira atribuição manual e nada mais (`LegendaEventoServiceImpl.java:441-457`; `EventoController.java:290-295`). Quem tem legenda só por regra aparece como "Esta pessoa não possui legenda configurada.", embora a lista e o mapa o identifiquem pela legenda. GPE005 descreve a consulta da legenda "atribuída ao participante após o processamento das regras". O N2 ("Ver a legenda atual de um participante") está impreciso nesse ponto.
2. **A lista de participantes NÃO se atualiza sozinha.** A atualização a cada 3 segundos refaz só o conjunto de participantes do mapa (`evento-pessoa.component.ts:123-140`, `:189-206`); a lista paginada só é refeita ao pesquisar, limpar ou paginar (`evento-pessoas-list.component.ts:62-74`, `:122-124`). A premissa do pedido ("a tela se atualiza sozinha a cada 3 segundos — isso alimenta o mapa") vale para o mapa, não para a lista; o N3 de EVT-PAR-01 — Pesquisar Participantes registra assim.
3. **As listas de Temas, Grupos de Trabalho e Cargo do filtro são do sistema inteiro, não do evento.** As três consultas não recebem o evento (`EventoPessoaController.java:65-81`; `TemaPessoaRepository.java:16-17`, `GrupoTrabalhoPessoaRepository.java:16-17`, `PessoaRepository.java:19-20` — código). GPE005 pede "todos os temas vinculados aos participantes do respectivo evento".

---

## EVT-PAR-01 — Pesquisar Participantes

**⚠️ Divergências documento × código**
- Busca: o documento diz "permite informar parte do nome" (tabela) e "nome da pessoa, organização e cargo" (descrição), tamanho 255; o código procura em nome, codinome, razão social, nome fantasia e cargo, exige todas as palavras, ignora acento e caixa, e a tela não limita o tamanho — `evento-pessoas-filter.component.html:10-23`; `EventoPessoaRepositoryImpl.java:107-129`.
- Critérios "Legendas" e "Foto": não constam no documento; existem no código — `evento-pessoas-filter.component.html:26-40`, `:226-237`. "Foto" corresponde a `PDTIC25148-35` CA03.
- Opções de Temas, Grupos de Trabalho e Cargo: o documento pede os valores dos participantes do evento; o código traz os de todas as pessoas do sistema — ver achado 3.
- Colunas do resultado: o documento lista 7 (Nome, Organização, Cargo, Convidado, Confirmado, Check-In, Assento); o código tem mais a coluna "Legenda" e a faixa de cor — `evento-pessoas-list.component.html:41-49`, `:55-57`, `:81-83`.
- Botão do cabeçalho: a imagem `GPE005-01.png` mostra "Cadastrar Participante"; a tela (e a imagem `GPE005-03.png` do próprio documento) mostra "Cadastrar Pessoa" — `evento-pessoa.component.html:62-72`.
- Texto de apoio da busca: imagem `GPE005-01.png` "Buscar por nome, organização ou cargo"; código "Buscar por nome, codinome, organização ou cargo" — `evento-pessoas-filter.component.html:20`.
- Secretaria Check-In: o documento só registra a restrição ao evento principal; o código também oculta Temas, Grupos de Trabalho e Cargo — `evento-pessoas-filter.component.html:42`; `evento-pessoas-filter.component.ts:36`.
- `PDTIC25148-35` CA03: o ticket fala em "pessoas confirmadas no evento que não possuem foto"; o código não exige confirmação — `EventoPessoaRepositoryImpl.java:233-234`, `:334-342`.

**❓ Lacunas**
- Qual dado deve aparecer em "Organização": razão social ou nome fantasia? O código mostra o nome fantasia e, na falta, a razão social, por efeito de uma troca registrada como "comportamento a preservar".
- Em que situação real um participante fica sem informação de convite ou de confirmação ("Pendente")? Cargas, importação do CRM e cadastro na recepção sempre gravam valor (`EventoPessoaServiceImpl.java:250-253`, `:345-349`, `:444-446`); só a regravação do mapa poderia deixá-lo vazio.
- O servidor aceita ordenar por organização e por assento (`EventoPessoaRepositoryImpl.java:253-264`); a tela não oferece. Intenção?

**🔍 Inferências a confirmar**
- Ao alternar para o mapa e voltar, os critérios reaparecem em branco e a lista volta filtrada pela última pesquisa: o filtro fica guardado na tela-mãe e o formulário é recriado — `evento-pessoa.component.ts:20`, `:60-62`; `evento-pessoa.component.html:104-116`; `evento-pessoas-list.component.ts:62-74` (não executado).
- O ticket `PDTIC25148-20` (Pesquisa de participantes) é a origem da funcionalidade no Jira.

**⚠️ Suspeitas de defeito**
- Razão social e nome fantasia trocados na coluna "Organização" — `EventoPessoaRepositoryImpl.java:237-249`; `EventoPessoaListDTO.java:30-35`; `evento-pessoas-list.component.html:73-75` (backend 6.1 item 11).
- "Não" tratado de forma desigual: Convidado e Confirmado = só quem está marcado como não; Check-In = não ou vazio — `EventoPessoaRepositoryImpl.java:209-231`.
- Temas, Grupos de Trabalho e Cargo comparados por trecho (contém), não por igualdade — `EventoPessoaRepositoryImpl.java:132-186`.
- A pesquisa por legenda considera qualquer legenda do participante, não só a exibida — `EventoPessoaRepositoryImpl.java:189-207`.
- Falha na pesquisa sem mensagem ao usuário — `evento-pessoas-list.component.ts:111-114`.
- Se o evento não carrega, a tela fica só com o cartão vazio, sem mensagem — `evento-pessoa.component.ts:97-101`; `evento-pessoa.component.html:103`.
- Concordância: "{0} cargo selecionados" — `evento-pessoas-filter.component.html:91`.
- O nome do participante abre a tela de edição da pessoa para qualquer perfil que veja a lista, inclusive Secretaria Check-In; a rota não confere perfil — `evento-pessoas-list.component.html:59-71`; frontend 1 (rotas sem guard de perfil).
- Sem o evento na consulta, o servidor pesquisa os participantes de todos os eventos, e o recurso não consta entre os protegidos — `EventoPessoaRepositoryImpl.java:102-105`; backend 2.3.
- Tabela com `[paginator]` e `[lazy]` duplicados, `colspan` 7/8 em tabela de 9 colunas, `dataKey="codigo"` — frontend 8.4 item 29 (não entrou no N3: sem efeito para o PO).

---

## EVT-PAR-02 — Cadastrar Participante

**⚠️ Divergências documento × código**
- Nome da opção: o documento diz "Cadastrar Participante"; a tela diz "Cadastrar Pessoa" — `evento-pessoa.component.html:62-72`.
- "Check-in automático": o documento o dá como obrigatório (S); no código é uma caixa de marcar sem obrigatoriedade, que vem marcada — `pessoas-cadastro.component.ts:100`; `pessoas-cadastro.component.html:122-132`.
- Tamanho mínimo do nome (3): só no código — `pessoas-cadastro.component.ts:74-81`.
- "A pessoa é incluída como participante do evento e no cadastro de pessoas" (documento): o código cria SEMPRE pessoa nova, sem procurar existente — `EventoPessoaServiceImpl.java:438-462`.

**❓ Lacunas**
- Qual dos tickets citados na v1.1 (`PDTIC25148-32`, `-20`, `-28`) originou o check-in automático.
- A recepção deveria poder escolher uma pessoa já cadastrada, em vez de sempre criar outra?
- Quem entra pela recepção fica como não convidado e não confirmado: é a intenção?

**🔍 Inferências a confirmar**
- `PDTIC25148-15` (Cadastro de Pessoas - No dia do evento) é o ticket de origem.
- Sem `Cód. Contato`, uma carga ou importação posterior com a mesma pessoa cria outro cadastro (as cargas reconhecem pelo código) — `EventoPessoaServiceImpl.java:333-338` (código).
- Check-in automático sem data e hora põe a pessoa à frente de todos na fila da Secretaria Mesa (ordem crescente da data; valor vazio vem primeiro no SQL Server) — `EventoPessoaRepositoryImpl.java:544-549`.
- "Atendido" fica sem valor (o construtor do objeto não aplica o padrão) — backend 6.1 item 9; na exportação sai "Pendente".
- Depois de uma falha, o botão "Enviar" fica em carregamento até a janela ser reaberta; o tipo da mensagem de erro (`erro`) não é reconhecido pela tela — `pessoas-cadastro.component.ts:26-29`, `:107`, `:132-139` (frontend 8.4 item 30).
- Evento excluído (a exclusão é lógica) continua aceitando cadastro; evento inexistente responde sucesso sem fazer nada — `EventoPessoaServiceImpl.java:440`. Não entrou como cenário: nenhuma tela chega a isso.

**⚠️ Suspeitas de defeito**
- Check-in automático grava o indicador e não grava a data e a hora — `EventoPessoaServiceImpl.java:442-448` (backend 6.1 item 9).
- A lista de participantes não é recarregada depois do cadastro — `evento-pessoa.component.ts:154-161` (frontend 8.4 item 31).
- O servidor não valida nenhum campo, nem o nome — backend 3.d; `PessoaCadastroRapidoDTO.java:8-12`.
- E-mail sem conferência de formato — `pessoas-cadastro.component.ts:95-99` (frontend 8.4 item 18).
- Mensagens de sucesso e de erro ficam na tela até serem fechadas (`sticky`) — `pessoas-cadastro.component.ts:123-138`.
- A mensagem "Formulário inválido" / "Preencha todos os campos obrigatórios corretamente" existe no código e é inalcançável: o botão fica desabilitado com o formulário inválido — `pessoas-cadastro.component.ts:110-116`; `pessoas-cadastro.component.html:143`.
- Permissão: o servidor declara toda inclusão sob eventos só para o Administrador; a tela oferece o cadastro à Secretaria Check-In — já anotado no N2.

---

## EVT-PAR-03 — Registrar Check-in

**⚠️ Divergências documento × código**
- O documento chama a opção de "Realizar check-in"; a tela não tem esse texto, só a imagem da coluna "Check-In" — `evento-pessoas-list.component.html:127-149`.
- O documento não fala de pré-condição; o código aceita check-in de quem não foi convidado nem confirmou — `EventoPessoaServiceImpl.java:410-419`; frontend 4.14 ("Regra 'só faz check-in quem está confirmado': não encontrado").

**❓ Lacunas**
- O check-in de quem não confirmou deveria ser aceito?
- Quem fez o check-in não é guardado (MASTER, decisão transversal 2). É requisito?

**🔍 Inferências a confirmar**
- `PDTIC25148-14` (Check-in) é o ticket de origem.
- Com dois usuários na lista, a ação envia o contrário do que a linha mostra; se outro já marcou, o segundo toque regrava "feito" com nova data e hora — `evento-pessoas-list.component.html:131-147`; `evento-pessoas-list.component.ts:126-129` (não executado).

**⚠️ Suspeitas de defeito**
- Desmarcar o check-in regrava a data e a hora em vez de apagar — `EventoPessoaServiceImpl.java:415-416` (backend 6.1 item 8).
- O valor muda na linha antes da resposta e não volta em caso de erro — `evento-pessoas-list.component.ts:126-129` (frontend 8.4 item 28).
- As dicas da imagem de check-in são "Confirmado" / "Não confirmado" / "Status desconhecido" — `evento-pessoas-list.component.ts:236-240`; `evento-pessoas-list.component.html:136`, `:145`.
- Mensagem de erro com título e detalhe iguais ("Erro ao realizar Check-in") — `evento-pessoas-list.component.ts:155`.
- Duas operações para a mesma regra: a da administração (declarada só para Administrador) e a da secretaria (declarada só para Secretaria Check-In) — `evento.service.ts:55-61`; backend 1.1 e 6.3.
- Participante inexistente: o servidor responde sucesso sem fazer nada — backend 4.2 "Respostas silenciosas". Não entrou como cenário: nenhuma tela retira participante.
- Par de mensagens "Check-in pendente." inalcançável — `evento-pessoas-list.component.ts:138-141`.

---

## EVT-PAR-04 — Consultar Legenda do Participante

**⚠️ Divergências documento × código**
- Legenda consultada: o documento fala da legenda atribuída pelo processamento das regras; a janela mostra só a manual — ver achado 1; `evento-pessoas-list.component.ts:342-361`.
- Opções: o documento traz relação fixa e numerada ("1 – Anfitrião" … "13 – Presidentes e Diretores de Associações Brasileiras", "16 – Assento livre", "Remover legenda" — faltam 14 e 15 no próprio documento); o código lista o catálogo, em ordem alfabética — `evento-pessoas-list.component.ts:310-321`.
- "Assento livre": o documento a traz como opção; o código a exclui (`PDTIC25148-35` CA01) — `evento-pessoas-list.component.ts:313-314`; `legenda-mesa.helper.ts:66-72`.
- Imagem `GPE005-04.png`: legendas com número e composição ("PRINCIPAL"); a tela atual não mostra número nem composição e acrescenta "Configurada neste evento" — `evento-pessoas-list.component.html:236-249`.

**❓ Lacunas**
- A consulta deveria mostrar a legenda prioritária (manual ou de regra), como a lista e o mapa?
- O atalho na coluna "Assento" para uma janela que só trata de legenda é intencional? (O documento descreve assim.)

**🔍 Inferências a confirmar**
- A lista vinda do catálogo e a marca "Configurada neste evento" decorrem de `PDTIC25148-34`.
- "Assento livre" é reconhecida só pelo nome: renomeá-la no catálogo a faria voltar à lista — `legenda-mesa.helper.ts:14`, `:66-72`.
- Catálogo e configuração do evento são lidos uma vez, ao abrir a tela; legenda criada depois só aparece ao recarregar — `evento-pessoas-list.component.ts:54-60`, `:86`.

**⚠️ Suspeitas de defeito**
- Falha ao buscar a legenda: a janela abre como se não houvesse legenda, sem mensagem — `evento-pessoas-list.component.ts:355-359`.
- Falha ao carregar o catálogo: lista vazia, sem mensagem — `evento-pessoas-list.component.ts:316-319`.
- Catálogo lido com teto de 1.000 legendas — `evento-pessoas-list.component.ts:311`.
- Organização na janela com a mesma troca razão social × nome fantasia da lista — `evento-pessoas-list.component.html:209`.

---

## EVT-PAR-05 — Alterar Legenda do Participante

**⚠️ Divergências documento × código**
- O documento fala em "alterar a legenda" e "selecionar e atribuir"; não distingue legenda manual. No código a escolha vira legenda manual, única por participante, que prevalece e resiste à geração — `LegendaEventoServiceImpl.java:459-504`; backend 3.f "Legenda manual por participante".
- Opções fixas do documento × catálogo — idem EVT-PAR-04 — Consultar Legenda do Participante.

**❓ Lacunas**
- Legenda que não está na configuração do evento pode ser atribuída (fica sem número): é a intenção? — backend 3.f ("Não exige que a legenda esteja na configuração do evento").
- Quem alterou a legenda não é guardado.

**🔍 Inferências a confirmar**
- O mapa de assentos não percebe a troca de legenda pela atualização automática (a assinatura comparada não inclui legenda) — `evento-pessoa.component.ts:218-231` (não executado).

**⚠️ Suspeitas de defeito**
- As recusas do servidor ("Participante não informado.", "Participante não encontrado.", "Legenda inexistente: …") chegam ao usuário como "Erro ao salvar legenda da pessoa." — `evento-pessoas-list.component.ts:405-409`; `LegendaEventoServiceImpl.java:462-481`.
- A data de atribuição não é atualizada quando uma legenda de regra é tornada manual — `LegendaEventoServiceImpl.java:492-503`.
- "Assento livre" barrada só na lista da tela; o servidor aceitaria — `evento-pessoas-list.component.ts:313-314`.
- Aviso "Erro interno: pessoa não selecionada." inalcançável — `evento-pessoas-list.component.ts:380-383`.

---

## EVT-PAR-06 — Remover Legenda do Participante

**⚠️ Divergências documento × código**
- O documento fala em "remover a legenda de um determinado participante"; o código remove só a manual e deixa as de regra — `LegendaEventoServiceImpl.java:471-478`.

**❓ Lacunas**
- A remoção individual deveria alcançar a legenda recebida por regra? Hoje não há como tirá-la de um participante isolado.
- Título que a caixa de confirmação mostra em execução ("Confirmar Remoção", pedido pela ação, ou "Remover Pessoa", da caixa da tela).

**🔍 Inferências a confirmar**
- Legenda manual que nasceu de uma legenda de regra: a remoção apaga a atribuição inteira, e a legenda de regra só volta na próxima geração — `LegendaEventoServiceImpl.java:471-478`, `:492-503` (dedução do código, não executado).
- Os botões da caixa são "Remover" e "Cancelar" (rodapé próprio da caixa) — `evento-pessoas-list.component.html:2-7`; `evento-pessoas-list.component.ts:419-423`.

**⚠️ Suspeitas de defeito**
- Aviso "Esta pessoa não possui legenda para remover." inalcançável: o botão e o caminho da lista só existem com legenda manual — `evento-pessoas-list.component.ts:414-417`; `evento-pessoas-list.component.html:270`.
- Dois caminhos para a mesma ação (botão "Remover Legenda" e opção "Remover legenda" + "Salvar") — `evento-pessoas-list.component.html:251-261`, `:269-277`.

---

## EVT-PAR-13 — Alterar Confirmação de Presença

**⚠️ Divergências documento × código**
- O documento só prevê REMOVER a confirmação; o código alterna nos dois sentidos — `evento-pessoas-list.component.html:103-123`; `EventoPessoaServiceImpl.java:421-436`.
- O documento chama a opção de "Confirmação"; a coluna é "Confirmado".
- O documento não fala de assento nem de check-in; o código libera o assento ao retirar e desfaz o check-in em qualquer alteração (N1, regras 6 e 7).
- A matriz de perfis do documento não traz a funcionalidade; no código é só do Administrador — já anotado no N2.

**❓ Lacunas**
- Qual dos tickets citados na v1.1 originou a funcionalidade.
- Texto que a caixa de pergunta mostra em execução (título e botões) — frontend 8.4 item 26.
- A confirmação retirada deveria resistir a uma nova carga de confirmados ou a uma nova importação do CRM? Hoje ela é remarcada — `EventoPessoaServiceImpl.java:259-262`, `:356-359` (código).

**🔍 Inferências a confirmar**
- Na caixa de pergunta, o título pedido pela ação prevalece e os botões são "Remover" e "Cancelar"; para confirmar um participante o usuário acionaria "Remover" — `evento-pessoas-list.component.html:2-7`; `evento-pessoas-list.component.ts:167-171` (não executado).

**⚠️ Suspeitas de defeito**
- Confirmar desfaz o check-in (N1, regra 7; backend 6.1 item 7), e a tela não mostra: a linha continua com o check-in feito até nova pesquisa, porque a tela só zera check-in e assento ao retirar — `evento-pessoas-list.component.ts:173-177`; `EventoPessoaServiceImpl.java:427-430`. Caso concreto: quem foi cadastrado na recepção com check-in automático e depois é confirmado perde o check-in.
- Retirada a confirmação, o participante some do mapa (assento e lista de disponíveis), pois o mapa só reúne confirmado ou com check-in — `EventoPessoaRepositoryImpl.java:538-542`.
- A linha muda antes da resposta e não volta em caso de erro — frontend 8.4 item 28.
- O valor da confirmação viaja no atributo de nome `statusCheckin` — frontend 8.4 item 27.
- Concordância: "Confirmação foi realizado com sucesso"; redação: "Não confirmação realizada." — `evento-pessoas-list.component.ts:194-200`.
- Para o Administrador, o participante sem informação de confirmação aparece como não confirmado, com a dica "Status desconhecido" — `evento-pessoas-list.component.html:106-112`; `evento-pessoas-list.component.ts:236-240`.

---

## EVT-PAR-14 — Exportar Participantes

**⚠️ Divergências documento × código**
- Nenhuma nas colunas: as 14 do documento e as 14 do código têm os mesmos títulos, na mesma ordem — `EventoPessoaServiceImpl.java:580-639`; `ExcelHeadersEnum.java:7-33`.
- A matriz de perfis do documento não traz a funcionalidade; a tela a oferece a todo perfil que vê a lista — já anotado no N2.

**❓ Lacunas**
- Qual dos tickets citados na v1.1 originou a funcionalidade.
- "Legendas", no plural, deveria trazer todas as legendas do participante? Hoje sai só a prioritária — `EventoPessoaServiceImpl.java:557-559`.
- Convite e assento ficam fora da planilha (no documento e no código): é a intenção?

**🔍 Inferências a confirmar**
- Com a pesquisa sem resultado, o botão continua disponível e a planilha sai só com a linha de títulos — `evento-pessoas-list.component.html:168-181` (não executado).
- O botão pode ser acionado de novo enquanto o arquivo é gerado (não há bloqueio) — `evento-pessoas-list.component.ts:454-476`.

**⚠️ Suspeitas de defeito**
- A exportação reaproveita a consulta paginada: só exporta tudo porque a tela pede 100.000 linhas; sem esse tamanho o servidor devolveria 10 — backend 6.1 item 10; `evento-pessoas-list.component.ts:455-462`.
- Nomes desencontrados: botão "Download", método `exportCSV`, operação `…/excel`, registro do servidor falando em xlsx, arquivo `.xls` — frontend 8.4 item 32; backend 6.1 item 10.
- O aviso "Exportação em andamento." não tem contrapartida de conclusão — `evento-pessoas-list.component.ts:463`.
- "Atendido" sai "Pendente" para quem foi cadastrado na recepção (indicador sem valor) — ver EVT-PAR-02 — Cadastrar Participante.

---

> **Abreviações desta parte (mapa de assentos).** `FI §5.2` = seção do inventário do front · `FI 8.4-34` = item 34 da lista de suspeitas do front · `BI 6.1-6` = item 6 da lista de suspeitas do back · `retangular.ts` = `…/mesa/components/retangular/retangular.component.ts` (mapa do Administrador, retangular) · `invertido.ts` = `…/mesa/components/retangular-invertido/retangular-invertido.component.ts` · `sec-ret.ts` e `sec-inv.ts` = os dois componentes do mapa da Secretaria Mesa · `evento-pessoa.ts` = a tela que hospeda o mapa.

## EVT-PAR-07 — Consultar Mapa de Assentos

**⚠️ Divergências documento × código**

- Faixas de assentos: GPE004 traz uma única composição (A1–A5, B1–B34, C1–C34, D1–D5, E1–E30, F1–F28, G1–G10, H1–H28); no código ela é a do Retangular Invertido (174 assentos), e o Retangular tem B/C até 35, E até 23, F até 32 e H até 36 (181). Tela e servidor concordam entre si. — FI §5.2 e §5.4 (`retangular.ts:31-39`, `invertido.ts:31-39`); BI §3.e (`CadeiraMesaServiceImpl.java:88-210`).
- Tipo de mesa: GPE004 só lista "Retangular"; o código tem dois formatos. — BI §3.e; FI §5.1 (`mesa.component.html:1-8`).
- Mesa principal × laterais: GPE004 lista os oito setores sem distinguir; o código separa A–D (principal) de E–H (lateral). — BI §3.e (`CadeiraMesaServiceImpl.java:88-210`).
- Cartão do participante: GPE005 descreve "Nome Completo (qtd de participações histórica) / Legenda / Cargo / Organização / Informação de check-in", que é o cartão do Administrador; o cartão da Secretaria Mesa (foto, nome, organização, assento, botão) só aparece na tabela de permissões do documento. — FI §5.3 (`sec-inv.html:24-62`).
- Campo "Buscar pessoa...": GPE005 diz "parte do nome" e tamanho 255; a tela busca em nome, codinome, cargo, razão social, nome fantasia e legenda, sem limite de tamanho. — FI §5.2 (`retangular.ts:569-603`, `retangular.html:19`).
- Quadro "Legenda das Categorias": a imagem `GPE005-05.png` mostra só o nome de cada legenda; a tela mostra "{nome} ({quantidade})". — FI §5.2 (`legenda-mesa.helper.ts:128-140`).
- Quem entra no mapa: GPE005 fala em "todos os assentos … e o seu respectivo participante", sem restringir; o código só traz ao mapa quem está confirmado ou fez check-in. — BI §3.d "Participantes da mesa" (`EventoPessoaRepositoryImpl.java:538-542`).
- Atualização automática a cada 3 s e indicador "Atualização automática ativa": não constam no texto do documento (o indicador aparece na imagem `GPE005-06.png`). — FI §4.12 (`evento-pessoa.ts:189-206`, `.html:33-56`).

**❓ Lacunas**

- Nenhuma fonte diz se os nomes de setor das dicas ("Anfitrião", "Palestrantes", "Presidência", "Deputados Federais", "Senadores", "Convidados Especiais", "Governadores", "Imprensa", "Assessoria", "Segurança", "Técnicos") devem existir; parecem dados de um evento específico embutidos no código. — FI §5.2 e FI 8.2 (`retangular.ts:296-331`).
- Nenhuma fonte diz o que o mapa deve fazer quando o formato de mesa do evento é trocado depois da inclusão (os assentos não são refeitos). — BI 6.1-3 (`EventoServiceImpl.java:190-210`).
- Perfil "Gestor": a tela o trata como Administrador no mapa (FI §2.4); não consta no N2 nem no documento. Não tratei no N3 (permissão é do N2).

**🔍 Inferências a confirmar**

- A busca por legenda em "Buscar pessoa..." seria a "permissão para consulta por legenda durante a alocação de participantes" do histórico da versão 1.1 de GPE005. — `GPE005.txt:19`; FI §5.2 (`retangular.ts:592`).
- Tickets do Jira relacionados só pelo título: `PDTIC25148-16`, `-28` e `-32` (este último citado no histórico de GPE004 v1.1 e GPE005 v1.1). — `tickets-jira.md`.
- `depende_de: ["EVT-CAD-02"]` — escolhi Cadastrar Evento, que gera os assentos, como pré-requisito de uso. Confirmar se o critério da instância é esse ou a tela que dá acesso.
- Ordem das pessoas disponíveis do Administrador: legenda (sem legenda por último), participações (maior primeiro), nome. — BI §3.d (`EventoPessoaRepositoryImpl.java:550-554`); a tela não reordena.

**⚠️ Suspeitas de defeito**

- Mudança só de legenda, de atendimento ou de dados da pessoa não redesenha o mapa aberto: a conferência de mudanças só olha id, check-in, confirmação, participações e assento. — FI §4.12 (`evento-pessoa.ts:218-231`). Não está na lista de suspeitas do inventário.
- Ordem de chegada da Secretaria Mesa depende da data do check-in, que a gravação do mapa apaga (BI 6.1-6) e que o cadastro de recepção com check-in automático não grava (BI 6.1-9); sem data, a pessoa vai para o início da fila (o banco ordena vazio primeiro). — BI §3.d (`EventoPessoaRepositoryImpl.java:544-549`).
- Falha ao carregar os assentos deixa "Carregando dados da mesa..." para sempre, sem mensagem. — `retangular.ts:108`, `:242-252`. Não está no inventário.
- Lista de participantes que fica vazia com o mapa aberto é ignorada (o mapa não se limpa). — `retangular.ts:83-84`. Não está no inventário.
- Formato trocado depois da inclusão: desenho e assentos não coincidem; no mapa do Administrador invertido, participante em H29–H36 pode quebrar a montagem. — FI 8.4-39 (`invertido.ts:32-38`, `:1806`, `:1819`, `:1864`).
- Parâmetro da consulta chamado `isSecretariaCheckin` recebe a indicação de Secretaria Mesa. — FI 8.4-25 (`evento-pessoa.ts:106`, `:124`).
- Etiqueta da legenda no cartão do Administrador só aparece se a legenda está na configuração do evento; a manual fora da configuração pinta o assento mas não aparece no cartão. — FI 8.4-44 (`retangular.html:33-38`).
- Dica do assento vazio diz "Clique para atribuir uma pessoa" no mapa só de consulta da Secretaria Mesa. — FI 8.4-44-A (`sec-ret.ts:779`).
- Três redações para a mesma situação: "Check in não identificado", "Check in não realizado", "Check-in pendente". — FI 8.4-42 (`retangular.ts:876`, `:1076`, `:2517`).

---

## EVT-PAR-08 — Atribuir Assento ao Participante

**⚠️ Divergências documento × código**

- Assento ocupado: GPE005 diz "arrastando o participante para um assento vazio ou ocupado", sem dizer o que acontece com o ocupante; no código o ocupante volta para a lista — não há troca. — FI §5.2 (`retangular.ts:729-743`, `:543-555`).
- Gravação: GPE005 descreve a marcação como imediata; no código ela só chega ao servidor na gravação do mapa inteiro, 30 s depois da última alteração ou pelo botão "Salvar Alocações (n)". — FI §5.2 (`retangular.ts:1421-1463`, `:1497-1556`); BI §3.e (`EventoServiceImpl.java:221-274`).
- Formas de atribuir: GPE005 só cita o arraste; o código também atribui por clique + janela "Selecionar Pessoa" e por arraste entre assentos. — FI §5.2 (`retangular.ts:456-481`, `:978-986`).

**❓ Lacunas**

- Intervalo desejado da gravação automática: 30 s no valor, "5 segundos" no comentário do código. — FI 8.4-33 (`retangular.ts:69`).
- Nenhuma fonte diz o que deve acontecer quando dois Administradores montam o mesmo mapa ao mesmo tempo.
- Nenhuma fonte diz se deve haver registro de quem montou o mapa (não há). — BI §5.

**🔍 Inferências a confirmar**

- Dois Administradores: prevalece por inteiro a última gravação. Decorre de o servidor substituir o mapa inteiro. — BI §3.e (`EventoServiceImpl.java:228`).
- `PDTIC25148-31` (arrastar mais de uma cadeira), a fazer: confirma que hoje só se arrasta uma pessoa por vez.

**⚠️ Suspeitas de defeito**

- A gravação do mapa regrava a participação de cada pessoa sentada só com as quatro marcações, o assento e a pessoa: apaga a data do check-in e os cinco dados do CRM, e sobrepõe Convidado/Confirmado/Check-In/Atendido com o que a tela tinha. Confirmado por leitura (`EventoServiceImpl.java:276-312`, `EventoPessoaMapper.java`, `EventoPessoaDTO.java`); o cadastro da pessoa não é afetado (a associação não propaga a gravação). Não executado. — BI 6.1-6.
- Alteração ainda não gravada é descartada quando a atualização automática percebe mudança vinda de outro ponto (um check-in, por exemplo) e refaz o mapa. Confirmado por leitura. — FI 8.4-41 (`retangular.ts:83-91`, `:228-240`; `evento-pessoa.ts:123-140`).
- Sair do mapa (alternar para "Participantes" ou fechar) cancela a gravação automática pendente, sem aviso. — `retangular.ts:126-132`; `evento-pessoa.component.html:104-123`. Não está no inventário.
- Clique em assento ocupado da mesa principal devolve o ocupante à lista antes de qualquer escolha; fechada a janela, ele fica no assento e na lista ao mesmo tempo. — FI 8.4-35 (`retangular.ts:436-454`).
- Mapa sem ninguém sentado nunca é gravado (base das suspeitas de EVT-PAR-09 e EVT-PAR-11). — FI 8.4-34 (`retangular.ts:1423-1431`, `:1519-1521`).
- O servidor não confere dois participantes no mesmo assento. — BI §3.e "Trocar com assento ocupado".
- Mensagem de erro manda o usuário ao "console"; o motivo do servidor ("Cadeira não encontrada: …") não é mostrado. — FI §5.2 (`retangular.ts:1453-1460`); BI §4.2.
- Pessoa solta em posição desenhada que não tem assento no evento aparece na tela e some da lista, mas nunca é gravada. — `retangular.ts:509-523`, `:736-741`. Não está no inventário.
- No tablet, o Administrador não tem "Salvar Alocações (n)" nem "Limpar Todas": só a gravação automática. — FI §5.2 (`retangular.html:81`).
- Campo de filtro da janela "Selecionar Pessoa" e campo "Buscar pessoa..." são a mesma variável. — `retangular.html:19`, `:397`. Não está no inventário.
- Janela "Selecionar Pessoa" duplicada no modelo da tela. — FI 8.4-36 (`retangular.html:388-417`, `:474-504`).
- A opção da janela repete a organização (nome fantasia e razão social) e não mostra cargo nem legenda. — `retangular.html:402-413`.

---

## EVT-PAR-09 — Remover Assento do Participante

**⚠️ Divergências documento × código**

- GPE005 descreve a remoção como efetiva ao acionar a opção; no código ela só é gravada com o mapa (→ EVT-PAR-08 — Atribuir Assento ao Participante). — FI §5.2 (`retangular.ts:483-496`, `:543-555`).
- Sem confirmação: o documento não fala de confirmação; o código remove direto. — FI §5.2.

**❓ Lacunas**

- Nenhuma fonte diz se a retirada do assento deve desfazer o atendimento.

**🔍 Inferências a confirmar**

- Participante atendido que perde o assento volta a não atendido e reaparece na fila da Secretaria Mesa, como "Não alocado". — BI §3.e passo 1 (`EventoServiceImpl.java:413-422`).

**⚠️ Suspeitas de defeito**

- Remover o último participante sentado não é gravado: o mapa vazio não é enviado e o botão "Salvar Alocações (0)" fica desabilitado. Mesmo mecanismo de FI 8.4-34, não listado no inventário para a remoção. — `retangular.ts:1519-1521`; `retangular.html:91-92`.
- Remoção ainda não gravada é desfeita pela atualização automática (mesma suspeita de EVT-PAR-08 — Atribuir Assento ao Participante). — FI 8.4-41.

---

## EVT-PAR-10 — Registrar Atendimento

**⚠️ Divergências documento × código**

- Texto do botão: GPE005 chama a opção de "Atender" e a imagem `GPE005-06.png` mostra "ATENDER" na lista; no código a lista do computador diz "ATENDIDO" e só o carrossel do tablet diz "ATENDER". — FI 8.4-43 (`sec-inv.html:60`, `:112`; `sec-ret.html:68`, `:120`).
- "A lista é atualizada à medida que os check-ins são realizados e em ordem de check-in" (GPE005): o código segue, com a ressalva da data de check-in apagada (ver EVT-PAR-07 — Consultar Mapa de Assentos).

**❓ Lacunas**

- Não há como desfazer o atendimento; nenhuma fonte diz o que fazer quando a pessoa errada é marcada. — BI §3.d "Atendimento".
- Nenhuma fonte diz se deve ficar registro de quem atendeu e quando (não fica). — BI §5.

**🔍 Inferências a confirmar**

- O atendimento é desfeito pela gravação do mapa: sempre para quem perdeu o assento; para quem continua sentado, quando o mapa do Administrador ainda o tinha como não atendido. — BI §3.e passos 1 e 3 (`EventoServiceImpl.java:228`, `:252-257`, `:413-422`).
- Com duas telas da Secretaria Mesa abertas, o atendimento feito em uma só some da outra quando a atualização automática percebe outra mudança. — FI §4.12 (`evento-pessoa.ts:218-231`).

**⚠️ Suspeitas de defeito**

- A operação de atendimento não está entre as protegidas pelo servidor (já anotado no N2). — BI 6.1-23.
- O servidor não confere check-in nem assento ao atender e responde sucesso mesmo quando o participante não existe. — BI §3.d e §4.2 "Respostas silenciosas" (`EventoPessoaServiceImpl.java:469-475`).
- O botão continua acionável durante o envio (sem indicador nem bloqueio). — `sec-inv.ts:2682-2703`.

---

## EVT-PAR-11 — Liberar Todos os Assentos

**⚠️ Divergências documento × código**

- GPE005: "todas as pessoas ficam disponíveis para serem vinculadas e o mapa de assentos é limpo, ficando vazio". No código o mapa é esvaziado só na tela de quem acionou; nada é gravado. — FI 8.4-34.
- Sem confirmação antes de esvaziar o mapa inteiro (o documento não fala de confirmação). — FI §5.2 (`retangular.ts:1571-1605`).

**❓ Lacunas**

- Nenhuma fonte diz se liberar o mapa deve desfazer os atendimentos (a operação do servidor, se fosse chamada, desfaria). — BI §3.e "Limpar todas".

**🔍 Inferências a confirmar**

- Os assentos anteriores reaparecem ao recarregar e quando a atualização automática percebe mudança de outro ponto. — `evento-pessoa.ts:123-140`.
- A liberação só se consolida se depois dela alguém for sentado e o mapa gravado. — BI §3.e passo 1.

**⚠️ Suspeitas de defeito**

- **Verificado no código, como pedido**: "Limpar Todas" NÃO é gravado. `limparComposicoesMesa()` (`retangular.ts:1571-1605`) zera as listas locais e chama `agendarSalvamentoAutomatico()`; `executarSalvamentoAutomatico()` (`:1517-1521`) retorna sem enviar quando não há pessoas alocadas; `salvarComposicoesMesa()` (`:1421-1431`) só avisa; o botão fica desabilitado (`retangular.html:91-92`). `evento.service.ts` só tem `POST` (`:68-71`) e um `GET` sem chamador (`:73-76`) para `composicoes-mesa`; a busca por `composicoes-mesa` e por `http.delete` em todo `src/` não encontra chamada ao `DELETE …/composicoes-mesa` (`EventoController.java:195-203`). Leitura estática, sem execução.
- A mensagem "Todas as alocações foram removidas da mesa." aparece mesmo sem nada ter sido gravado. — `retangular.ts:1599-1604`.
- No formato invertido, a limpeza redesenha o mapa com as quantidades do retangular (B35, C35, F29–F32 e H29–H36 a mais; E24–E30 a menos) até o mapa ser refeito. — FI 8.4-38 (`invertido.ts:1597-1608`).

---

## EVT-PAR-12 — Buscar Pessoa na Mesa

**⚠️ Divergências documento × código**

- GPE005: "a busca é realizada pelo nome do participante". O código busca por nome e codinome; no mapa do Administrador retangular também por legenda; no mapa da Secretaria Mesa também por identificação do assento. — FI §5.2, §5.3 e §5.4 (`retangular.ts:1267-1319`; `invertido.ts:1269-1300`; `sec-ret.ts:946-1098`; `sec-inv.ts:1274-1424`).
- Tamanho 255 no documento; sem limite na tela. — `retangular.html:51-55`.
- Duração do destaque (5 s): o documento não diz. — FI §5.2 (`retangular.ts:1338-1341`).

**❓ Lacunas**

- Nenhuma fonte explica por que a legenda só é critério no mapa do Administrador retangular (e, nele, não nos setores F e H).
- Nenhuma fonte diz se a busca por assento deveria existir também para o Administrador.

**🔍 Inferências a confirmar**

- Os resultados não são refeitos quando a atualização automática redesenha o mapa; valem até a próxima tecla. — `retangular.ts:1244-1265`.
- Relação com `PDTIC25148-28` (Mapa de mesa - melhorias) só pelo título.

**⚠️ Suspeitas de defeito**

- Critérios diferentes nos quatro desenhos do mapa (tabela no N3). — FI §5.3 e §5.4.
- Orientação do campo desencontrada: o Administrador invertido promete busca por cadeira que não existe; a Secretaria Mesa retangular faz a busca por cadeira sem anunciar. — FI 8.4-40 (`invertido.html:51`; `sec-ret.html:134`).
- A busca na mesa diferencia acentos; a busca de pessoas disponíveis, no mesmo mapa, não. — FI §5.2 (`retangular.ts:1251`, `:569-575`).
- A busca por nome não apara espaços do termo (um espaço no fim muda o resultado). — `retangular.ts:1251`.
- Destaque: escolher outro resultado antes dos 5 s deixa o primeiro temporizador apagar o segundo destaque antes da hora. — `retangular.ts:1321-1342`. Não está no inventário.
- No tablet, a etiqueta do assento no cartão da Secretaria Mesa não reage ao toque (só a lista do computador tem a ação). — `sec-inv.html:52` (lista, com a ação) × carrossel (`sec-inv.html:66-117`, sem a ação). Não está no inventário.
- Clicar na etiqueta do assento com um termo digitado acrescenta o resultado à lista sem limpá-la (pode duplicar linhas). — `sec-inv.ts:1348-1424`.

---

## EVT-PAR-15 — Exportar Mapa de Assentos

**⚠️ Divergências documento × código**

- A funcionalidade não consta no texto nem na tabela de permissões de GPE005; só a seção "Exportações" aparece na imagem `GPE005-05.png`. — FI §5.2 "Exportação" (`retangular.html:447-471`).

**❓ Lacunas**

- O que acontece quando o nome do evento tem caracteres inválidos para nome de arquivo.
- Se o Mapa Completo deveria trazer o quadro de legendas (hoje não traz; as cores ficam sem explicação no arquivo).
- Conteúdo do bug `PDTIC25148-27` (só tenho o título "Exportação da Mesa").

**🔍 Inferências a confirmar**

- O arquivo retrata o mapa da tela, inclusive atribuições não gravadas. — `retangular.ts:2139-2152`, `:2352-2375`.
- "Total de Participantes" das estatísticas = participantes do mapa (confirmados ou com check-in), não todos os convidados. — `retangular.ts:2236-2237`.

**⚠️ Suspeitas de defeito**

- Botão "PNG" gera JPEG com extensão `.png`. — FI 8.4-37 (`retangular.ts:1946`, `:2010`, `:2097-2102`).
- "Check-in pendente" no arquivo × "Check in não identificado" na tela. — FI 8.4-42 (`retangular.ts:2517`).
- Código de exportação sem acionador no mapa da Secretaria Mesa invertido. — FI 8.1 (`sec-inv.ts:2046-2229`).

---

*Links: [Resumo da revisão](../REVISAO-CONVERSAO.md) · [N2 do Feature Set](../modules/eventos/participantes/README.md) · [INDEX geral](../modules/INDEX.md)*
