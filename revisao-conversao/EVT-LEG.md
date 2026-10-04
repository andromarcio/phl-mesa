<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
# Revisão da conversão — Legendas

> Detalhe, feature a feature, do que precisa de olho humano no Feature Set **Legendas** (`EVT-LEG`), gerado na engenharia reversa de 2026-09-30. O resumo e as prioridades estão em [`REVISAO-CONVERSAO.md`](../REVISAO-CONVERSAO.md).
>
> **Como ler.** Cada feature traz quatro listas: **⚠️ Divergências documento × código** (decidir qual vale), **❓ Lacunas** (nenhuma fonte responde — precisa do PO), **🔍 Inferências a confirmar** (provavelmente certas) e **⚠️ Suspeitas de defeito** (o código faz algo que parece errado). Tudo veio da **leitura** do código — nada foi executado; o que depende de execução está dito como inferência.
>
> **Referências.** `arquivo:linha` aponta para o código-fonte: no front, pelo nome do arquivo; no back, pelo caminho a partir de `br/com/cni/apimesacheckin/`. "Inventário", **FI** e **BI** são os inventários do front e do back, guardados em [`arquivos/engenharia-reversa/`](../arquivos/engenharia-reversa/README.md). As features estão em duas partes: primeiro a configuração do evento (`EVT-LEG-01` a `07`), depois presets e catálogo (`EVT-LEG-08` a `14`).

---

> **Abreviações desta parte (configuração do evento).** **cfg.ts / cfg.html** = `configuracao-legendas-evento.component.ts / .html` · **card** = `bloco-evento-card.component` · **cond** = `condicao-linha.component` · **add** = `adicionar-bloco-dialog.component` · **sim** = `simulacao-dialog.component` · **LES** = `service/impl/LegendaEventoServiceImpl.java`.

## EVT-LEG-01 — Consultar Configuração de Legendas

**⚠️ Divergências documento × código**
- Lista: GPE006 diz que "A lista apresenta todas as legendas passíveis de configuração", ativas e inativas (`GPE006.txt:21`); o código mostra só os blocos adicionados ao evento (FI 4.17, `cfg.html:50-63`; BI 3.f "Ativar/inativar: não existe").
- Acesso: GPE006 diz que se chega pela opção "Regras de Execução" (`GPE006.txt:22`); na lista de eventos o ícone se chama "Configuração de Legendas" (FI 4.9, `evento-list.component.html:88-89`).
- Título: imagem de GPE006 traz "Configuração de Regras de Legendas" e o subtítulo "Configure as regras automáticas para aplicação de legendas às pessoas" (`GPE006-01.png`); a tela traz "Configuração de Legendas", o nome do evento e a contagem de blocos (FI 4.17, `cfg.html:6-24`).
- Barra de ações: GPE006 tem "Salvar Regras", "Simular Execução", "Executar Regras" e "Resetar" (`GPE006-01.png`); a tela tem "Carregar configuração", "Salvar como preset", "Gerenciar catálogo", "Adicionar bloco", "Simular" e "Executar" (FI 4.17, `cfg.html:26-40`).
- Salvar: GPE006 tem o comando "Salvar Regras" (`GPE006-01.png`); o código grava a cada alteração, sem botão (FI 4.17 "Persistência automática", `cfg.ts:39-48`, `:111-124`, `:165-188`).
- Chave "Ativa/Inativa" por legenda (`GPE006.txt:51`) não existe; o que não deve valer é removido (BI 3.f; ticket CA08).
- Quadro "Preview da condição" (`GPE006.txt:56`) e quadros "Importante" e "Dicas" do rodapé (`GPE006-01.png`) não existem no código (FI 4.17 não os lista; `card.html` e `cfg.html` conferidos).
- Numeração: GPE006 não numera as legendas; o código numera cada bloco pela posição no evento (FI 4.17, `cfg.ts:201-204`; BI 3.f "Ordem/prioridade", `LES:110-119`).

**❓ Lacunas**
- Nenhuma fonte diz o que a tela deve mostrar para evento excluído (exclusão lógica): a leitura e a gravação não filtram evento excluído (BI 3.f "Ler: não verifica se o evento existe", `LES:86-94`, `:99-100`).
- Nenhuma fonte define o que acontece quando duas pessoas editam a configuração do mesmo evento ao mesmo tempo.

**🔍 Inferências a confirmar**
- Com a configuração gravada por inteiro a cada alteração, a última gravação vence: duas sessões na mesma configuração se sobrescrevem (`LES:106-108`). Não entrou no N3; fica aqui para decisão.
- Evento inexistente: a consulta devolve configuração vazia sem aviso e o nome fica em branco (`LES:86-94`; `cfg.ts:153-161`); a primeira alteração é recusada com "Evento não encontrado." (`LES:99-100`). No N3 como cenário "Evento que não existe".
- Cenário "Gravação recusada pelo servidor" (bloco excluído do catálogo com a tela aberta → "Bloco de legenda inexistente: <id>") foi deduzido de `LES:175-177` e `cfg.ts:182-188`; não executado.

**⚠️ Suspeitas de defeito**
- Sem indicador de carga na abertura: até a resposta chegar — e depois de uma falha de carga — a tela mostra "0 blocos configurados" e "Nenhum bloco configurado", iguais aos de um evento vazio (`cfg.html:43-48`; `cfg.ts:143-151`). Uma alteração feita nesse estado gravaria a configuração "vazia + alteração" por cima da real (🔍, não executado).
- Endereços trocados: `/regras-legenda` sem número abre o Catálogo e `/catalogo-legendas/:id` abre a Configuração (FI 8.4 item 45, `legendas-routing.module.ts:7-16`).
- Erro de regra de negócio aparece com o título "Erro Interno" (FI 8.4 item 47, `page-base.ts:15-16`).
- Mensagem "Evento não informado na URL." usa termo técnico na interface (FI 4.17, `cfg.ts:129-131`).
- A tela não confere o perfil (FI 4.17 "Sem checagem de perfil"); já está na nota da matriz do N2.

---

## EVT-LEG-02 — Adicionar Bloco de Legenda ao Evento

**⚠️ Divergências documento × código**
- GPE006 lista 12 legendas configuráveis fixas (`GPE006.txt:60-72`: Comitê estratégico; GT da MEI – coordenadores; Empresas – presidentes; Empresas - vice-presidentes; Governo/Parceiros (BNDES, FINEP e EMBRAPII) presidentes e/ou diretores; Empresas – diretores; GT da MEI – titulares; ICT – Reitores; Governo/Parceiros - presidentes e/ou secretários; Diretores da CNI; Presidentes e Diretores de Associações Brasileiras; Assento livre); o código aceita qualquer bloco do catálogo (FI 4.18, `add.ts:83-113`; BI 3.f, `LES:171-180`).
- GPE006 diz, na imagem, "Anfitrião e Palestrantes são definidos manualmente" (`GPE006-01.png`); o código não reserva legenda nenhuma à atribuição manual — um bloco "Anfitrião" pode receber condições.
- GPE006: "Para realizar a inclusão, é necessário ativar a legenda" (`GPE006.txt:25`); no código, pôr a legenda em vigor é adicionar o bloco ao evento (FI 4.18 "Adicionar ao evento", `add.ts:126-137`; `cfg.ts:296-308`).
- GPE006 não tem janela de inclusão nem busca; o código tem a janela "Adicionar bloco" com busca e seleção múltipla (FI 4.18, `add.html:12-46`).

**❓ Lacunas**
- GPE006 não diz o que acontece com a legenda ativa que ainda não tem condição; no código o bloco sem condição completa é ignorado (BI 3.f passo 5.2, `LES:258-262`).

**🔍 Inferências a confirmar**
- Vários blocos marcados entram na ordem em que foram marcados (comportamento da lista de seleção; `add.ts:126-137` só repassa a seleção).
- Os blocos já marcados continuam marcados quando o termo da busca muda (`add.ts:106-113`; não executado).
- Catálogo com mais de mil blocos não apareceria inteiro: a janela pede 1000 itens (FI 4.18, `add.ts:91-103`).
- Cenário "Bloco excluído do catálogo antes da gravação" deduzido de `LES:175-177`; não executado.
- Texto do aviso na falha de carga do catálogo: depende do formato da falha (`add.ts:98-101`); o N3 não fixa o texto.

**⚠️ Suspeitas de defeito**
- A janela "Adicionar bloco" trata erro sem a proteção que a página tem: numa resposta de erro sem corpo, a rotina de erro quebra antes de mostrar a mensagem (`add.ts:98-101`, `:152-155`; FI 8.4 item 46 descreve o problema em `page-base.ts:14-24`).
- Não há mensagem de sucesso: o retorno é só o cartão novo e o indicador "Salvo".

---

## EVT-LEG-03 — Configurar Condições de Legenda

**⚠️ Divergências documento × código**
- Rótulos do campo: GPE006 "Grupo Temático / Tema / Cargo / Nome Fantasia / Papel Desempenhado" (`GPE006.txt:52`, `:75-79`); tela "Grupo de trabalho", "Tema", "Cargo", "Nome fantasia", "Papel desempenhado" (FI 7.1 `CAMPOS_CONDICAO`, `legenda.interface.ts:134-140`). "Grupo Temático" de GPE006 é o grupo de trabalho: a fórmula da imagem mostra "Grupotrabalho" para o campo "Grupo Temático" (`GPE006-01.png`).
- Obrigatoriedade: GPE006 dá Campo, Operador e Valor como obrigatórios (`GPE006.txt:52-54`); o código aceita e grava valor vazio, e a tela não valida nada (FI 4.17 "Validação de condição: não encontrado no front"; BI 3.f "Bloco sem condição e condição incompleta são aceitos e gravados", `LES:164-170`).
- "Preview da condição" com a fórmula (`GPE006.txt:56`, `:93-94`, `:105-106`; `GPE006-02.png`, `GPE006-03.png`) não existe no código.
- Rótulos e disposição: GPE006 tem "Campo:", "Operador:", "Valor:" sobre cada campo, conectivo entre as condições, botão "Adicionar Condição" e a dica fixa 'Para operador "Em (lista)", separe valores com vírgula' (`GPE006-01.png`); a tela tem os títulos de coluna "Conectivo", "Campo", "Operador", "Valor", o botão "Adicionar condição" e o texto de orientação "valores separados por vírgula" só com o operador Em (lista) (FI 4.17, `card.html:43-49`, `:64-71`; `cond.ts:52-54`).
- Texto de orientação do Valor: GPE006 "Digite o valor..." (`GPE006-01.png`); tela "Digite o valor" (FI 4.17 "Linha de condição").
- Edição: GPE006 separa "Incluir Regra" e "Editar Regra" (`GPE006.txt:23-31`); no código não há modo de edição — a condição é alterada no lugar e gravada na hora.

**❓ Lacunas**
- O ticket lista "Grupo de Trabalho" e "Tema/Grupo Temático" (`tickets-jira.md:51`): não fica claro se "Grupo Temático" é o grupo de trabalho (GPE006) ou o tema (ticket). Confirmar o vocabulário com o PO.
- Nenhuma fonte diz se o valor deveria ser escolhido de uma lista dos valores existentes (grupos, temas, cargos) em vez de digitado.
- Nenhuma fonte diz se a ordem das condições deveria poder ser mudada; hoje só excluindo e incluindo de novo.

**🔍 Inferências a confirmar**
- Valor com mais de 1.000 caracteres: a tela não limita (FI 4.17 "sem maxlength") e o dado comporta 1.000 (`global/data-models/eventos.md`, EventoLegendaCondicao); a gravação falharia com erro inesperado. Não executado.
- Campo e Operador nunca ficam em branco pela tela: nascem preenchidos e a lista não tem opção de limpar (`card.ts:41-51`; `cond.html:18-43`).

**⚠️ Suspeitas de defeito**
- Valor não conferido contra os dados existentes: erro de digitação faz a condição não alcançar ninguém, sem aviso (FI 4.17; BI 3.f).
- Exclusão de condição sem confirmação e sem desfazer (FI 4.17 "sem confirmação", `cond.html:58-68`).
- Condição nova já nasce gravada, incompleta, a cada clique em "Adicionar condição" (`card.ts:41-51`).

---

## EVT-LEG-04 — Reordenar Blocos de Legenda

**⚠️ Divergências documento × código**
- A funcionalidade não consta em GPE006; o documento só diz, na imagem, "As regras são aplicadas na ordem de prioridade das legendas" (`GPE006-01.png`), sem oferecer como mudar a ordem. O código tem as setas "Mover para cima" e "Mover para baixo" (FI 4.17, `card.html:11-30`; `cfg.ts:206-224`). Origem: ticket CA07.

**❓ Lacunas**
- Nenhuma fonte diz se a mudança de ordem deveria exigir nova geração para valer na lista e no mapa.

**🔍 Inferências a confirmar**
- A reordenação muda de imediato a legenda exibida de quem tem legendas de mais de um bloco, sem nova geração: a prioridade é resolvida na leitura, pela ordem atual dos blocos (BI 3.f "Quando mais de uma legenda casa", `repository/impl/EventoPessoaRepositoryImpl.java:44-68`). Não executado. Está no N3 como regra 7, marcada 🔍.

**⚠️ Suspeitas de defeito**
- Só há setas, uma posição por vez, e cada acionamento grava a configuração inteira (FI 4.17 "Reordenação apenas pelos botões"); levar um bloco do fim ao começo exige vários acionamentos e várias gravações.

---

## EVT-LEG-05 — Remover Bloco de Legenda do Evento

**⚠️ Divergências documento × código**
- A funcionalidade não consta em GPE006; o equivalente era inativar a legenda pela chave "Ativa/Inativa" (`GPE006.txt:51`). No código o bloco é removido, com as condições (FI 4.17, `card.ts:74-84`; `cfg.ts:226-230`; BI 3.f "tirar o bloco é a forma de desativar"). Origem: ticket CA09.
- "Resetar Regras" de GPE006 (`GPE006.txt:40-42`, `:115`) não existe mais (FI 4.17 "Reset de legendas: não encontrado no front"; BI 3.f "Resetar: não há endpoint próprio"). Não virou N3. Hoje: remover os blocos um a um e, para apagar as legendas já geradas, gerar com a configuração vazia.

**❓ Lacunas**
- GPE006 não diz se a legenda inativada conservava as condições; no código, remover apaga as condições do bloco naquele evento.
- Nenhuma fonte diz o que deve acontecer com as legendas já atribuídas quando o bloco sai da configuração.

**🔍 Inferências a confirmar**
- Enquanto não há nova geração, a legenda do bloco removido continua atribuída, sem número e com a menor prioridade entre as não manuais (`EventoPessoaRepositoryImpl.java:44-68`; BI 3.f "legenda fora da configuração"). Não executado.
- No mapa de assentos do Administrador, a legenda sem número não seria mostrada (FI 8.4 item 44, `retangular.component.html:33-38`) — efeito sobre o Feature Set Participantes.

**⚠️ Suspeitas de defeito**
- A pergunta "Remover o bloco '{nome}' deste evento?" não avisa que as condições se perdem nem que as legendas já atribuídas permanecem até a geração seguinte (FI 4.17, `card.ts:74-84`).

---

## EVT-LEG-06 — Simular Aplicação de Legendas

**⚠️ Divergências documento × código**
- Nome do comando: GPE006 "Simular Execução" (`GPE006.txt:35`; `GPE006-01.png`); tela "Simular" (FI 4.17, `cfg.html:36-37`).
- Resultado: GPE006 pede "um resumo da quantidade de pessoas selecionadas para cada legenda" (`GPE006.txt:34`); o código mostra também quatro totais (Participantes, Legendas removidas, Legendas aplicadas, Manuais preservadas), os blocos ignorados e os nomes dos participantes de cada legenda (FI 4.21, `sim.html:7-75`). Os nomes vêm do ticket (CA19).

**❓ Lacunas**
- Ordem dos nomes dos participantes na parte expandida: a consulta não ordena (`LES:274-284`).
- GPE006 não mostra a tela do resultado da simulação.

**🔍 Inferências a confirmar**
- A simulação usa a configuração da tela, inclusive o valor digitado que ainda não foi gravado (`cfg.ts:259-267`).
- A simulação não aplica as exigências da gravação (legenda repetida, bloco fora do catálogo): só confere o evento (BI 3.f "Simular", `LES:202-210`); bloco fora do catálogo é simulado com o nome e a cor da tela (`LES:251-255`).
- "Legendas aplicadas" pode passar de "Participantes", porque conta atribuições (`LES:290`).
- A mesma pessoa incluída duas vezes no evento apareceria duas vezes na relação (o modelo de dados registra que o sistema não impede a duplicidade).

**⚠️ Suspeitas de defeito**
- Sem indicador de processamento: a janela só aparece quando o resultado chega (`cfg.ts:259-267`).
- O servidor declara a simulação como inclusão (só Administrador), embora não grave nada; já está na nota da matriz do N2.

---

## EVT-LEG-07 — Gerar Legendas do Evento

**⚠️ Divergências documento × código**
- Nome do comando: GPE006 "Executar Regras" (`GPE006.txt:36-39`; `GPE006-01.png`); tela "Executar" (FI 4.17, `cfg.html:38-39`).
- Limpeza: GPE006 diz, na imagem, "A execução REMOVE TODAS as legendas existentes antes de aplicar as novas regras" (`GPE006-01.png`); o código apaga só as não manuais e preserva as manuais (BI 3.f passo 4, `LES:235-237`; ticket CA22).
- Regras ativas: GPE006 "São aplicadas apenas as regras que estejam ativas" (`GPE006.txt:87`); no código todo bloco presente vale, e o que fica de fora é o bloco sem condição completa (BI 3.f passo 5.2, `LES:257-262`).
- Uma legenda por pessoa: GPE006 "Uma vez que o valor corresponda ao configurado, a legenda é atribuída" e "As regras são aplicadas na ordem de prioridade das legendas" (`GPE006.txt:86`; `GPE006-01.png`), e o ticket fala em "ordem de prioridade" (CA21); o código atribui uma legenda por bloco atendido — os blocos não se excluem — e usa a ordem só para escolher a que aparece (BI 3.f "Quando mais de uma legenda casa", `LES:245-292`).
- Público: GPE006 "atualiza a legenda de cada convidado do respectivo evento" (`GPE006.txt:38`); o código avalia todos os participantes, sem olhar convite, confirmação nem check-in (BI 3.f passo 1, `LES:230`, `:421-426`).
- Confirmação: GPE006 não descreve pergunta de confirmação; o código pergunta antes de gerar (FI 4.17 "Executar", `cfg.ts:269-280`; ticket CA20).
- "Resetar Regras" (`GPE006.txt:40-42`) não existe; gerar com a configuração vazia apaga as legendas não manuais (BI 3.f "Resetar"). Registrado como regra 23 do N3.

**❓ Lacunas**
- A comparação diferencia maiúsculas de minúsculas e letras acentuadas? O código não trata; depende de como os dados estão guardados (BI 3.f passo 5.4 "Diferença de maiúsculas/acentos não é tratada no código").
- Quem não confirmou presença deve receber legenda? Nenhuma fonte responde.
- A intenção é uma só legenda por pessoa (a do bloco prioritário) ou várias, com a prioritária em exibição? GPE006 e ticket sugerem a primeira; o código faz a segunda.
- A precedência entre E e OU não é definida em GPE006, que só exemplifica uma e duas condições (`GPE006.txt:88-106`).

**🔍 Inferências a confirmar**
- "Diferente de" em Cargo e Nome fantasia não alcança a pessoa com o dado em branco, ao contrário do que acontece com grupo de trabalho, papel e tema (leitura de `LES:387-402`; depende de o dado em branco estar guardado como vazio ou como ausente). Não executado. No N3 como parte da regra 14.
- A geração é integral — falha em qualquer etapa desfaz tudo (BI 3.f "Executar: Transacional", `LES:212-220`). Não executado.
- Um segundo acionamento de "Executar" antes do fim do primeiro é possível, porque o botão não é desabilitado (`cfg.ts:282-291`).
- Cenário "Bloco excluído do catálogo depois de aberta a tela" deduzido de `LES:175-177`; não executado.

**⚠️ Suspeitas de defeito**
- Condições sobre grupo e papel não são correlacionadas: grupo de um vínculo casa com papel de outro (BI 6.1 item 26, `LES:395-405`).
- "Igual a" com vírgula no valor vira "Em (lista)": não há como exigir igualdade com texto que contenha vírgula (BI 3.f passo 5.4, `LES:356-359`).
- Sem precedência de E sobre OU: avaliação da esquerda para a direita (BI 3.f passo 5.3, `LES:317-341`).
- "Diferente de" em grupo de trabalho, papel e tema casa também quem não tem nenhum (BI 3.f passo 5.4, `LES:399-402`).
- O resultado não informa os blocos ignorados; só a simulação informa (`cfg.ts:282-291` × `sim.html:26-29`).
- Texto com plural fixo: "1 legendas aplicadas, 1 manuais preservadas." (FI 4.17, `cfg.ts:284-288`).
- Sem indicador de processamento nem bloqueio do botão durante a geração (`cfg.ts:282-291`).
- Quando "Executar" falha, a tela não é recarregada (ao contrário da gravação automática): os cartões podem ficar diferentes do que está gravado (`cfg.ts:289` × `:182-188`).
- "Manuais preservadas" conta todas as legendas manuais do evento, inclusive as de legendas fora da configuração (`LES:428-435`); "Legendas aplicadas" conta atribuições, não pessoas (`LES:290`).
- Não fica registrado quem gerou as legendas (BI 5 "Usuário de criação/alteração: em nenhuma entidade").

---

## "Resetar Regras" de GPE006 — não virou N3

GPE006 descreve "Resetar Regras": "excluir todas as regras de legendas cadastradas para o respectivo evento", pela opção "Resetar" (`GPE006.txt:40-42`; perfil Administrador em `:115`). Não existe no código — nem botão, nem operação (FI 4.17 "Reset de legendas: não encontrado no front"; BI 3.f "Resetar: não encontrado no back"). O N2 já registra a ausência no "Não faz". Nos N3: `EVT-LEG-07 — Gerar Legendas do Evento`, regra 23 e cenário "Configuração vazia" (gerar com a configuração vazia apaga as legendas não manuais); `EVT-LEG-05 — Remover Bloco de Legenda do Evento`, Comportamento de tela (não há remoção de todos os blocos de uma vez); `EVT-LEG-01 — Consultar Configuração de Legendas`, Comportamento de tela (o botão não existe mais).

---

> **Abreviações desta parte (presets e catálogo).** `front:` = `sistema_mesa_checkin_frontend/src/app/admin/administracao/` · `back:` = `sistema_mesa_checkin_backend/src/main/java/br/com/cni/apimesacheckin/`. Entre parênteses, a seção do inventário.

## EVT-LEG-08 — Salvar Preset de Legendas

**⚠️ Divergências documento × código**
- Ticket (CA15) pede só "informar nome" para salvar o preset; o código tem também a Descrição opcional, a unicidade do nome e a cópia do nome do evento de origem — `front:legendas/components/salvar-preset-dialog/salvar-preset-dialog.component.html:5-17`; `back:service/impl/PresetLegendaServiceImpl.java:88-105` (front 4.19; back 3.f Presets).
- GPE006 não tem preset: não há o que comparar com o documento legado.

**❓ Lacunas**
- Nomes de preset que só diferem por maiúsculas e minúsculas contam como iguais? O código compara o nome como foi escrito (`back:repository/PresetLegendaRepository.java:10`) e o resultado depende do banco (restrição `UK_PRESET_LEGENDA_01`, `db/migrations/V00018__ddl.sql`).
- O preset deveria poder ser renomeado ou regravado? O ticket não pede; o código não tem edição (back 3.f Presets, linha "Editar: não encontrado no back").
- Para que servem o evento de origem e a data de criação, se nenhuma tela os mostra? São gravados (`PresetLegendaServiceImpl.java:100-104`) e chegam à tela (`front:legendas/services/legenda.interface.ts:38-50`), mas o cartão do preset não os exibe (`front:legendas/components/carregar-configuracao-dialog/carregar-configuracao-dialog.component.html:34-56`).
- Preset de configuração vazia deve ser aceito? Hoje é.

**🔍 Inferências a confirmar**
- "Erro" / "Falha de comunicação com o servidor." só aparece quando a resposta de erro vem sem conteúdo; numa queda de conexão a tela cairia na mensagem genérica "Serviço indisponível." — leitura de `front:legendas/pages/configuracao-legendas-evento/configuracao-legendas-evento.component.ts:191-197` e `shared/page-base.ts:14-24`, não executada.
- Tratei os blocos e as condições (EventoLegenda, EventoLegendaCondicao) como "lidos" pela feature, embora o retrato saia da configuração já aberta na tela e não de nova consulta ao servidor (`configuracao-legendas-evento.component.ts:311-317`). A contagem deve decidir.

**⚠️ Suspeitas de defeito**
- A janela se fecha antes da resposta do servidor: com nome repetido, o erro "Já existe um preset com este nome." aparece com a janela já fechada, e o nome e a descrição digitados se perdem — `salvar-preset-dialog.component.ts:57-64`; `configuracao-legendas-evento.component.ts:311-322`.
- O conteúdo do preset não é validado e o evento sem blocos também gera preset ("0 blocos") — `PresetLegendaServiceImpl.java:96-105` (back 3.f). Combinado com o modo Substituir de EVT-LEG-09 — Carregar Configuração de Legendas, esvazia a configuração do evento de destino.
- Limites de tamanho só na tela (100 e 255); o servidor não confere e o armazenamento comporta 150 e 500 — `back:domain/PresetLegenda.java:46-50`.
- Resumo "Erro Interno" para regra de negócio — `page-base.ts:15-16` (front 8.4 item 47).
- Nenhum indicador de gravação em andamento depois de fechar a janela.

---

## EVT-LEG-09 — Carregar Configuração de Legendas

**⚠️ Divergências documento × código**
- Ticket (CA16), Mesclar: "mantém os blocos atuais e acrescenta os da selecionada". Código: acrescenta só os blocos cuja legenda ainda não está no evento; para a legenda presente dos dois lados, ficam as condições do evento e as da origem são descartadas — `carregar-configuracao-dialog.component.ts:190-198` (front 4.20).
- Ticket não prevê bloco de preset que saiu do catálogo. Código: descarta o bloco e avisa "Blocos ignorados" — `carregar-configuracao-dialog.component.ts:128-139`; `configuracao-legendas-evento.component.ts:329-334`.
- Ticket (CA18) fala em "outro evento", sem restrição. Código: só eventos não excluídos com ao menos um bloco, exceto o próprio — `back:service/impl/LegendaEventoServiceImpl.java:144-162`; `back:repository/EventoLegendaRepository.java:35-41` (back 3.f "Copiar de outro evento").
- Ticket pede confirmação em Executar (CA20) e em Excluir bloco (CA11), e não diz nada de Substituir. Código: Substituir não pede confirmação (front 4.20).

**❓ Lacunas**
- Substituir deveria pedir confirmação ou permitir desfazer?
- Em que ordem os presets e os eventos de origem devem aparecer? Não há ordenação declarada em nenhuma das duas listas — `PresetLegendaServiceImpl.java:55`; `EventoLegendaRepository.java:38-41`.
- Carregar deveria tratar as legendas já atribuídas aos participantes? Hoje ficam como estavam até EVT-LEG-07 — Gerar Legendas do Evento, inclusive as de blocos que saíram da configuração.
- A entidade principal do front-matter ficou `PresetLegenda`, como pedido; a entidade que a feature de fato grava é `EventoLegenda` (com `EventoLegendaCondicao`). Confirmar para a contagem.

**🔍 Inferências a confirmar**
- A data do evento não aparece na aba "De outro evento": o servidor envia `dataEvento` e a tela lê `data` — `back:dto/EventoOrigemLegendaDTO.java:16`; `front:legendas/services/legenda.interface.ts:71-76`; `carregar-configuracao-dialog.component.html:74`. Não executado.
- Bloco excluído do catálogo depois de a janela ser aberta: a gravação é recusada com "Bloco de legenda inexistente: <id>" e a tela recarrega a configuração — `LegendaEventoServiceImpl.java:112-114` e `:175-177`; `configuracao-legendas-evento.component.ts:182-188`.
- Bloco trazido de preset aparece na tela com o nome e a cor do retrato (antigos) até a tela ser reaberta, porque a resposta da gravação não é usada para atualizar os cartões — `carregar-configuracao-dialog.component.ts:174-188`; `configuracao-legendas-evento.component.ts:124` e `:173-180`.
- Preset excluído por outra pessoa com a janela aberta: a resposta vem sem conteúdo e o tratamento de erro da janela, sem guarda, não mostra nada — `carregar-configuracao-dialog.component.ts:129-138`; `back:controller/LegendaController.java:70-75`; `shared/page-base.ts:14-24`.
- Preset com conteúdo ilegível derruba a listagem inteira da biblioteca ("Não foi possível ler a configuração do preset.") — `PresetLegendaServiceImpl.java:54-64` e `:125-134`. Não reproduzível pela tela.

**⚠️ Suspeitas de defeito**
- Substituir com preset vazio, ou com todos os blocos fora do catálogo, esvazia a configuração do evento sem confirmação e sem desfazer — `carregar-configuracao-dialog.component.ts:191-194`; `configuracao-legendas-evento.component.ts:325-328`.
- Corrida na abertura da janela: a relação de blocos do catálogo é lida em paralelo; se a leitura falhar ou ainda não tiver chegado quando o usuário aciona "Aplicar ao evento", todos os blocos do preset são tratados como inexistentes e, em Substituir, a configuração fica vazia — `carregar-configuracao-dialog.component.ts:71`, `:91-96` e `:128-135`. Inferência, não executada.
- A relação do catálogo é lida com limite de 1.000 blocos (`:92`); além disso, blocos válidos seriam ignorados.
- Tratamento de erro da janela sem guarda: resposta de erro sem conteúdo não gera mensagem — `:94`, `:107`, `:121`, `:137`, `:147`, `:169` (front 8.4 item 46, que afirma o contrário para as telas de legenda).
- A tela é quem copia: lê a origem e grava o destino. Duas pessoas configurando o mesmo evento se sobrescrevem sem aviso.

---

## EVT-LEG-10 — Excluir Preset de Legendas

**⚠️ Divergências documento × código**
- Ticket (CA17) não menciona confirmação; o código pede — `carregar-configuracao-dialog.component.ts:151-161` (front 4.20).

**❓ Lacunas**
- Não há autoria do preset: qualquer Administrador exclui preset salvo por outro. É a intenção?
- Não há tela própria de presets: só se exclui passando pela configuração de legendas de algum evento.

**🔍 Inferências a confirmar**
- Resposta de erro sem conteúdo não gera mensagem (mesmo tratamento sem guarda) — `carregar-configuracao-dialog.component.ts:169`.

**⚠️ Suspeitas de defeito**
- Depois do erro "Preset não encontrado." a lista não é recarregada: o cartão do preset inexistente continua na janela — `carregar-configuracao-dialog.component.ts:163-171`; `PresetLegendaServiceImpl.java:115-123`.
- Resumo "Erro Interno" para regra de negócio (front 8.4 item 47).

---

## EVT-LEG-11 — Pesquisar Blocos de Legenda

**⚠️ Divergências documento × código**
- O ticket descreve a consulta ao catálogo dentro de "adicionar bloco" e a "Gestão do Catálogo" (criar, editar, excluir); a tela própria, com busca e paginação, não está nos critérios — `front:legendas/pages/catalogo-legendas/catalogo-legendas.component.html:5-88` (front 4.22). CA05 (catálogo sem numeração) está atendido.
- GPE006 lista doze legendas fixas, em tela única por evento; o código tem catálogo livre, comum a todos os eventos.

**❓ Lacunas**
- A pesquisa diferencia acentuação? O código só iguala maiúsculas e minúsculas — `back:service/impl/LegendaServiceImpl.java:71-74`.
- A lista deveria mostrar em quantos eventos cada bloco está em uso? Hoje só a pergunta da exclusão mostra.

**🔍 Inferências a confirmar**
- Falha da pesquisa: o servidor responde com texto solto e a tela cai na mensagem genérica "Erro interno do servidor." — `back:controller/LegendaController.java:52-61`; `shared/page-base.ts:21-23`. Não executado.
- O menu "Administração › Catálogo de legendas" vem do arquivo declarativo do servidor (`configuracoes.json`, raiz do backend, linhas 449-468), não do front (front 2.1).

**⚠️ Suspeitas de defeito**
- `/regras-legenda` sem identificador abre o Catálogo e `/catalogo-legendas/{id}` abre a Configuração do evento — `front:legendas/legendas-routing.module.ts:7-16` (front 8.4 item 45).
- Mensagem genérica acompanhada do detalhe literal `&nbsp;` — `service/core/alerta.service.ts:13` (front 8.4 item 48).
- A consulta ao catálogo está declarada no servidor para os três perfis, e a tela não confere perfil: quem chega pelo endereço vê a lista (nota da matriz do N2).
- O servidor aceita busca geral (nome ou cor) e filtro por cor que a tela não usa — `LegendaServiceImpl.java:62-82`.

---

## EVT-LEG-12 — Cadastrar Bloco de Legenda

**⚠️ Divergências documento × código**
- Ticket (CA02): criar bloco com nome, cor da legenda e composição de mesa. Código: só nome e cor; a composição foi retirada (decisão "D5") — `front:legendas/components/bloco-form/bloco-form.component.ts:12-15` e `:56-59`; `back:dto/LegendaDTO.java:13-15`; `back:domain/Legenda.java:37-38`; `db/migrations/V00020__ddl.sql` (front 4.18; back 3.f Catálogo).
- GPE006: as legendas são uma lista fixa de doze; não há inclusão de legenda. Código: catálogo aberto.

**❓ Lacunas**
- A composição de mesa foi abandonada de vez? O critério CA02 continua pedindo.
- Qual é o tamanho máximo do nome? A tela limita a 100, o servidor não confere e o armazenamento comporta 255 — `bloco-form.component.html:6`; `db/migrations/V00004__ddl.sql:4`.
- Dois blocos com a mesma cor devem ser aceitos? Hoje são.
- CA03 aparece também na Origem de EVT-LEG-02 — Adicionar Bloco de Legenda ao Evento (o atalho fica na aba dela; o preenchimento do nome, nesta). O molde pede que cada critério apareça numa feature só: decidir qual das duas fica com o CA03.

**🔍 Inferências a confirmar**
- Cadastro feito de dentro da configuração do evento: o bloco é criado no catálogo e só depois a configuração é gravada; se a segunda gravação falhar, o bloco fica no catálogo e fora do evento — `front:legendas/components/adicionar-bloco-dialog/adicionar-bloco-dialog.component.ts:139-157`; `configuracao-legendas-evento.component.ts:296-308`.
- Na janela "Adicionar bloco", a resposta de erro sem conteúdo não gera mensagem (tratamento sem guarda) — `adicionar-bloco-dialog.component.ts:152-155`.

**⚠️ Suspeitas de defeito**
- Nome só com espaços passa pela validação da tela e é recusado pelo servidor ("O nome do bloco de legenda é obrigatório."), com resumo "Erro Interno" — `bloco-form.component.ts:57` e `:73-77`; `LegendaServiceImpl.java:99-100` e `:177-181`.
- A tela não confere nome duplicado antes de enviar (front 4.18).
- No cadastro feito pela configuração do evento não há mensagem de sucesso do cadastro.
- Sem data de criação nem autor (back 5).

---

## EVT-LEG-13 — Editar Bloco de Legenda

**⚠️ Divergências documento × código**
- Ticket (CA10): "editar reflete nos eventos que usam o bloco" — atendido. O ticket não diz o que pode ser editado; no código, nome e cor — `LegendaServiceImpl.java:112-129`.

**❓ Lacunas**
- A alteração deveria avisar que o bloco está em uso, ou pedir confirmação? Hoje não avisa.
- A alteração deve alcançar eventos já realizados (o mapa de um evento passado muda de cor e de nome)?
- Não há histórico nem registro de quem alterou.

**🔍 Inferências a confirmar**
- O reflexo na lista de participantes e no mapa decorre de as legendas apontarem para o bloco do catálogo — `back:repository/impl/EventoPessoaRepositoryImpl.java:44-68`. Não executado.
- Biblioteca de presets mostra nome e cor atuais; bloco aplicado de preset mostra os antigos até reabrir a tela (ver EVT-LEG-09 — Carregar Configuração de Legendas).

**⚠️ Suspeitas de defeito**
- Depois de "Bloco de legenda não encontrado." a janela continua aberta e a lista não é recarregada — `catalogo-legendas.component.ts:212-215`.
- Resumo "Erro Interno" para regra de negócio (front 8.4 item 47).

---

## EVT-LEG-14 — Excluir Bloco de Legenda

**⚠️ Divergências documento × código**
- Ticket (CA11): informar que o bloco está em uso e que a exclusão o remove das configurações desses eventos. Código: além disso, apaga todas as legendas do bloco atribuídas a participantes, em todos os eventos, **inclusive as manuais** — `LegendaServiceImpl.java:144-175` (back 3.f Catálogo; back 6.1 item 27).
- Ticket (CA22): legendas manuais são preservadas. Vale para a geração; a exclusão do bloco as apaga.
- Ticket (CA12): não duplicar blocos — atendido: não há ação de copiar.

**❓ Lacunas**
- A exclusão deveria ser impedida, ou pedir confirmação reforçada, quando há legenda manual ou evento já realizado?
- A pergunta deveria dizer quantos participantes perdem a legenda?
- O que fazer com os presets que contêm o bloco? Hoje ficam com o bloco "fantasma", ignorado na listagem e na aplicação.

**🔍 Inferências a confirmar**
- Atomicidade (tudo ou nada) lida da marcação de transação do serviço; não executada — `LegendaServiceImpl.java:144-146`.
- Bloco já excluído por outra pessoa: a consulta de uso responde "sem uso" e a recusa só vem na exclusão — `LegendaServiceImpl.java:131-142` e `:147-148`.

**⚠️ Suspeitas de defeito**
- Apaga legendas manuais sem aviso específico — ponto de atenção forte (back 6.1 item 27).
- A consulta de uso só olha a configuração dos eventos: bloco fora de todas as configurações, mas atribuído manualmente a participantes, é tratado como sem uso ("Excluir o bloco '…'?") e tem as legendas manuais apagadas — `back:repository/EventoLegendaRepository.java:27-33`; `front:legendas/pages/catalogo-legendas/catalogo-legendas.component.ts:228-248`.
- A consulta de uso lista eventos excluídos (back 3.f, linha "Uso").
- O servidor não exige a consulta de uso: a operação de exclusão, chamada direto, apaga em cascata sem aviso (back 6.1 item 27).
- A pergunta omite o evento de onde o usuário veio quando o bloco está nele e em outros — `catalogo-legendas.component.ts:230-241`.
- Sem registro de quem excluiu nem de quando (back 5).

---

*Links: [Resumo da revisão](../REVISAO-CONVERSAO.md) · [N2 do Feature Set](../modules/eventos/legendas/README.md) · [INDEX geral](../modules/INDEX.md)*
