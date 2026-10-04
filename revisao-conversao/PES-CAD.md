<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
# Revisão da conversão — Cadastro de Pessoas

> Detalhe, feature a feature, do que precisa de olho humano no Feature Set **Cadastro de Pessoas** (`PES-CAD`), gerado na engenharia reversa de 2026-09-30. O resumo e as prioridades estão em [`REVISAO-CONVERSAO.md`](../REVISAO-CONVERSAO.md).
>
> **Como ler.** Cada feature traz quatro listas: **⚠️ Divergências documento × código** (decidir qual vale), **❓ Lacunas** (nenhuma fonte responde — precisa do PO), **🔍 Inferências a confirmar** (provavelmente certas) e **⚠️ Suspeitas de defeito** (o código faz algo que parece errado). Tudo veio da **leitura** do código — nada foi executado; o que depende de execução está dito como inferência.
>
> **Referências.** `arquivo:linha` aponta para o código-fonte: no front, pelo nome do arquivo; no back, pelo caminho a partir de `br/com/cni/apimesacheckin/`. "Inventário", **FI** e **BI** são os inventários do front e do back, guardados em [`arquivos/engenharia-reversa/`](../arquivos/engenharia-reversa/README.md). A feature `PES-CAD-04 — Excluir Pessoa` não tem seção própria: seus pontos estão marcados no próprio N3.

---

## PES-CAD-01 — Pesquisar Pessoas

**⚠️ Divergências documento × código**
- Busca por trecho — GPE003 fala em "parte do nome" só para Razão Social e E-mail; para Nome e CRM diz "a partir do nome" / "a partir do número do CRM". O código busca por trecho, sem diferenciar maiúsculas, nos quatro filtros. BI §3.b (`service/impl/PessoaServiceImpl.java:68-91`).
- Ordem e paginação — GPE003 não descreve. O código fixa ordem alfabética de nome, crescente, e 10 pessoas por página. FI §4.4 (`pessoas-list.component.ts:97-120`).

**❓ Lacunas**
- Acentuação — se "Jose" encontra "José" depende da configuração do banco; nenhuma fonte responde. BI §3.b (`PessoaServiceImpl.java:68-91`).
- Ordenação — a imagem `GPE003-01.png` mostra ícones de ordenação em seis colunas, e o texto do documento não diz se a ordenação por coluna é requisito. FI §4.4.
- Resposta do servidor a perfil sem acesso — o recurso de pessoas não consta entre os protegidos; o que vale em produção não é verificável. BI §2.3 (`configuracoes.json:60`, `:86`, `:166`, `:258`).

**🔍 Inferências a confirmar**
- As dicas "Editar Pessoa" e "Remover Pessoa" provavelmente não aparecem (atributo de dica sem o módulo correspondente). FI §8.4 item 11 (`pessoas-list.component.ts:31-43`).
- Falha na consulta feita na abertura da tela deixa a lista vazia com "Nenhuma pessoa encontrada.", como se não houvesse pessoas. Código (`pessoas-list.component.ts:115-118`; `pessoas-list.component.html:87-95`).
- Acionar um ícone de ordenação volta à primeira página, além de não mudar a ordem (`pessoas-list.component.html:18`). Não foi para o N3.

**⚠️ Suspeitas de defeito**
- Ícones de ordenação em seis colunas, sem efeito: a consulta envia sempre a ordem por nome. FI §8.4 item 16 (`pessoas-list.component.ts:101-108`).
- Falha da consulta sem aviso ao usuário (só registro no navegador). FI §4.4 (`pessoas-list.component.ts:115-118`).
- Filtro preenchido só com o texto `null` é tratado como vazio. BI §3.b (`util/FilterUtils.java:11-14`); código (`page-helper.ts:44-50`).

---

## PES-CAD-02 — Cadastrar Pessoa

**⚠️ Divergências documento × código**
- Codinome — GPE003: tamanho 255. Código: 100. FI §4.5 (`pessoa-cadastro.component.html:30-51`; `pessoa.component.ts:121-126`).
- CNPJ — GPE003: tamanho 12. Código: máscara de 14 dígitos. FI §4.5 (`pessoa-empresa.component.html:104-118`).
- CRM — GPE003: "Campo texto numérico". Código: texto livre de até 50 caracteres. FI §4.5 (`pessoa-cadastro.component.html:54-75`).
- Nome — GPE003: só o máximo de 255. Código: mínimo de 3 e máximo de 255. FI §4.5 (`pessoa.component.ts:113-120`).
- Foto — GPE003: "Imagem", sem formato nem tamanho. Código: PNG, JPG ou JPEG de até 200 MB, conferidos só na tela. FI §4.5 (`pessoa-cadastro.component.html:136-176`); BI §3.h.
- Depois de incluir — GPE003 não diz o que acontece. Código: mensagem fixa "Pessoa criada com sucesso" e a tela não sai do lugar. FI §4.5 (`pessoa.component.ts:210-255`).

**❓ Lacunas**
- Telefone Principal — a máscara exige 11 dígitos; se um telefone fixo de 10 dígitos pode ser informado, nenhuma fonte responde. FI §4.5 (`pessoa-contato.component.html:32-48`).
- Intenção sobre CPF, CNPJ e e-mail — o documento dá só tamanho e tipo; não diz se devem ser validados nem se devem ser únicos.
- Jira — os tickets `PDTIC25148-11` (Cadastrar pessoas, concluído) e `PDTIC25148-22` (Cadastro de Pessoas - Ajustes, concluído) aparecem em `tickets-jira.md` só pelo título; sem o texto, não foram citados na `## Origem`.

**🔍 Inferências a confirmar**
- Acionar "Criar" duas vezes na mesma tela inclui duas pessoas: depois da inclusão o identificador devolvido não é posto no formulário e o botão volta a ficar habilitado. Código (`pessoa.component.ts:210-241`). Não consta nos inventários.
- Os avisos "Foto adicionada", "Anexo removido" e "Falha ao ler o arquivo." provavelmente não aparecem: a tela Pessoa declara um serviço de mensagens próprio, e esses avisos saem pelo serviço da raiz. Código (`pessoa.component.ts:35`; `pessoa-cadastro.component.ts:98-129`; `alerta.service.ts:5-11`; `main.ts:43`). Não consta nos inventários.
- O ramo "Formulário inválido" / "Preencha todos os campos obrigatórios corretamente" parece inalcançável, porque o botão fica desabilitado. FI §4.5 (`pessoa.component.ts:217-224`; `pessoa.component.html:32-34`).
- CRM repetido faz as cargas falharem. BI §6.1 item 19 (`repository/PessoaRepository.java:14`).

**⚠️ Suspeitas de defeito**
- CPF, CNPJ e e-mail sem validação. FI §8.4 item 18 (`pessoa.component.ts:139-140`, `:158`); BI §3.b (`PessoaServiceImpl.java:130-146`).
- Nenhuma unicidade (CPF, CRM, e-mail). BI §3.b (`repository/PessoaRepository.java:16`).
- Obrigatoriedade conferida só na tela; o servidor aceita pessoa sem Nome, Razão Social e Cargo. BI §3.b (`PessoaServiceImpl.java:130-146`).
- Não navega depois de salvar, e a mensagem de sucesso fica fixa. FI §8.4 item 15 (`pessoa.component.ts:210-241`).
- Campos obrigatórios em abas diferentes (Nome em Cadastro; Razão Social e Cargo em Perfil Corporativo), com o botão "Criar" desabilitado e sem indicação de onde está o que falta. Código (`pessoa.component.html:96-104`; `cadastro-helper.ts:4-7`).

---

## PES-CAD-03 — Editar Pessoa

**⚠️ Divergências documento × código**
- As mesmas de tamanho e tipo de `PES-CAD-02 — Cadastrar Pessoa` (Codinome 255 × 100; CNPJ 12 × 14; CRM numérico × texto; Nome sem mínimo × mínimo 3).
- Abas Relacionamento e Histórico — aparecem nas imagens `GPE003-05.png` e `GPE003-06.png`, mas a tabela de campos do documento não as descreve. O código exibe tema, grupo de trabalho, papel, data de vínculo, ano e participações. FI §4.5 (`pessoa-relacionamento.component.html:3-37`; `pessoa-historico.component.html:3-18`).
- Mensagem de sucesso — GPE003 não traz o texto. O código mostra "Pessoa criada com sucesso" também na alteração. FI §4.5 (`pessoa.component.ts:228-235`).
- Acesso pela lista de participantes — não está em GPE003; vem do ticket `PDTIC25148-35` (CA02). FI §4.14 (`evento-pessoas-list.component.html:59-71`).

**❓ Lacunas**
- Ordem dos temas, dos grupos de trabalho e dos anos nas abas de consulta — o código não define ordem. Código (`domain/Pessoa.java:113-120`).
- Alteração simultânea por dois usuários — não há controle no código; o comportamento esperado não está em nenhuma fonte.
- Intenção da regra da foto no servidor (retirar a foto quando ela não vem) — nenhuma fonte diz se é proposital.

**🔍 Inferências a confirmar**
- Alterar sem mexer na foto mantém a foto: a tela põe no formulário a referência da foto guardada e a reenvia; o servidor mantém o conteúdo quando recebe a referência sem novo conteúdo. Código (`pessoa.component.ts:164-188`, `:213`); BI §3.h (`service/impl/ArquivoServiceImpl.java:48-79`).
- Pessoa excluída por outro usuário com a tela aberta: "Atualizar" não grava nada e a tela mostra "Pessoa criada com sucesso" (o servidor responde como criado, sem conteúdo). Código (`PessoaServiceImpl.java:144-145`, `:161-195`; `controller/PessoaController.java:80-84`).
- Pessoa não encontrada ao abrir: campos vazios, sem mensagem (a consulta não trata falha). Código (`pessoa.component.ts:86-102`).
- Avisos da foto que provavelmente não aparecem — mesmo motivo de `PES-CAD-02 — Cadastrar Pessoa`.

**⚠️ Suspeitas de defeito**
- Edição mostra "Pessoa criada com sucesso" e não sai da tela. FI §8.4 item 15 (`pessoa.component.ts:210-241`).
- O servidor retira a foto quando a alteração chega sem ela. BI §6.1 item 28 (`PessoaServiceImpl.java:186-190`). Pela tela o efeito só aparece quando a foto é retirada de propósito (ver a inferência acima).
- A foto substituída ou retirada continua guardada. BI §3.h (`ArquivoServiceImpl.java:48-79`).
- "Data de Alteração" exibida não é atualizada depois de gravar. Código (`pessoa.component.ts:199-203`, `:229-241`).
- A alteração usa a operação de inclusão; a de alteração existe e não é usada pela tela. FI §6.3 (`pessoa.component.ts:228`; `pessoa.service.ts:32-35`).
- A tela fica ao alcance de qualquer perfil pelo atalho da lista de participantes. FI §4.14 (`evento-pessoas-list.component.html:59-71`); nota da matriz no N2.

---

## PES-CAD-05 — Carregar Grupos de Trabalho

**⚠️ Divergências documento × código**
- Substituição total — GPE003 não fala em substituir. O código apaga todos os grupos de trabalho de todas as pessoas antes de ler as linhas. BI §6.1 item 16 (`service/impl/GrupoTrabalhoPessoaServiceImpl.java:60`).
- Título da janela — imagem `GPE003-07.png`: "Carga de Grupos de Trabalho". Código: "Carga de Grupos Temáticos". FI §4.6 (`pessoas-carga-gt.component.html:12`).
- Instrução da janela — imagem e código dizem "Código ou Cód. Contato"; o servidor só reconhece "Cód. Contato". FI §4.6 (`pessoas-carga-gt.component.html:19`); BI §3.c (`enumeration/ExcelHeadersEnum.java:7`) e §6.2 (`ExcelHeadersEnum.java:24`, sem uso).
- Colunas obrigatórias — GPE003: `Grupos Temáticos` e `Papel Desempenhado` obrigatórios. Código: confere só a presença da coluna; célula em branco gera vínculo sem nome. Código (`GrupoTrabalhoPessoaServiceImpl.java:56-58`, `:96-110`).
- Alcance — GPE003 fala em carga dos grupos "vinculados a uma determinada pessoa". O código carrega a planilha inteira, de todas as pessoas. BI §3.c.

**❓ Lacunas**
- Papel Desempenhado com mais de 100 caracteres — o cadastro comporta 100; o que acontece acima disso não foi verificado.
- Intenção — substituição total ou acréscimo ao que existe? O documento não diz.
- Limite de tamanho da planilha no servidor — a tela limita a 200 MB; no servidor não há limite declarado. BI §3.h.
- Jira — a história `PDTIC25148-8` (Carga de GT, Tema e Histórico de participações, concluída) aparece em `tickets-jira.md` só pelo título; não foi citada na `## Origem`.

**🔍 Inferências a confirmar**
- `Cód. Contato` gravado como número de 8 dígitos ou mais não é reconhecido (leitura em notação científica). BI §6.1 item 18 (`util/ExcelUtils.java:107-109`).
- Duas pessoas com o mesmo CRM fazem a carga falhar. BI §6.1 item 19 (`repository/PessoaRepository.java:14`).
- Linha com `Cód. Contato` em branco é procurada como código vazio: conta como pessoa não encontrada — ou casa com uma pessoa cujo CRM foi gravado vazio. Código (`ExcelUtils.java:125-128`; `GrupoTrabalhoPessoaServiceImpl.java:83-94`). Não foi para o N3.
- Avisos sem detalhe ("Carga realizada com sucesso.") podem exibir o texto `&nbsp;`. FI §8.4 item 48 (`alerta.service.ts:13`).

**⚠️ Suspeitas de defeito**
- A carga apaga a base inteira de grupos de trabalho antes de processar. BI §6.1 item 16 (`GrupoTrabalhoPessoaServiceImpl.java:60`).
- Planilha ilegível respondida como sucesso, com contagens zeradas; a tela mostra "Grupos de trabalho foram atualizados" com o detalhe "." e "Carga realizada com sucesso.". BI §3.c (`GrupoTrabalhoPessoaServiceImpl.java:69-72`); FI §4.6 (`pessoas-filter.component.ts:107-127`).
- Planilha só com cabeçalho apaga todos os grupos de trabalho e mostra a mesma mensagem. Código (`GrupoTrabalhoPessoaServiceImpl.java:60-67`).
- Nenhum erro por linha, só contagens. BI §3.c (`dto/SituacaoCargaDTO.java:14-16`).
- O resumo não trata o singular ("1 pessoas não foram encontradas") e conta linhas, não pessoas. FI §4.6 (`pessoas-filter.component.ts:107-127`).
- O servidor não confere extensão nem tipo do arquivo. BI §3.c (`util/ExcelUtils.java:117-123`).

---

## PES-CAD-06 — Carregar Temas

**⚠️ Divergências documento × código**
- Substituição total — GPE003 não fala em substituir. O código apaga todos os temas de todas as pessoas antes de ler as linhas. BI §6.1 item 16 (`service/impl/TemaPessoaServiceImpl.java:59`).
- Coluna obrigatória — GPE003: `Tema` obrigatório. Código: confere só a presença da coluna; célula em branco gera vínculo sem nome de tema. Código (`TemaPessoaServiceImpl.java:55-57`, `:95-107`).
- Alcance — GPE003 fala em temas "vinculados a uma determinada pessoa". O código carrega a planilha inteira. BI §3.c.

**❓ Lacunas**
- Intenção — substituição total ou acréscimo? O documento não diz.
- Jira — `PDTIC25148-8` só pelo título (ver `PES-CAD-05 — Carregar Grupos de Trabalho`).

**🔍 Inferências a confirmar**
- `Cód. Contato` numérico de 8 dígitos ou mais não é reconhecido. BI §6.1 item 18 (`util/ExcelUtils.java:107-109`).
- Duas pessoas com o mesmo CRM fazem a carga falhar. BI §6.1 item 19 (`repository/PessoaRepository.java:14`).
- Linha com `Cód. Contato` em branco — mesmo efeito descrito em `PES-CAD-05 — Carregar Grupos de Trabalho`. Código (`TemaPessoaServiceImpl.java:81-93`).

**⚠️ Suspeitas de defeito**
- A carga apaga a base inteira de temas antes de processar. BI §6.1 item 16 (`TemaPessoaServiceImpl.java:59`).
- Planilha ilegível respondida como sucesso; a tela mostra "Carga concluída" com o detalhe ".". BI §3.c (`TemaPessoaServiceImpl.java:68-71`); FI §4.7 (`pessoas-filter.component.ts:142-162`).
- Planilha só com cabeçalho apaga todos os temas e mostra a mesma mensagem. Código (`TemaPessoaServiceImpl.java:59-66`).
- A linha repetida (mesma pessoa, mesmo tema) é mostrada como "{n} foram atualizados", embora nada seja alterado. BI §3.c (`TemaPessoaServiceImpl.java:96-99`); FI §4.7.
- Nenhum erro por linha; o resumo conta linhas, não pessoas, e não trata o singular. BI §3.c (`dto/SituacaoCargaDTO.java:14-16`); FI §4.7.
- O servidor não confere extensão nem tipo do arquivo. BI §3.c (`util/ExcelUtils.java:117-123`).

---

## PES-CAD-07 — Carregar Histórico de Participação

**⚠️ Divergências documento × código**
- Colunas — GPE003: `Cód. Contato` e `Ano participação`, as duas obrigatórias. Código: exige só `Cód. Contato` e lê cada outra coluna como um ano (cabeçalho = ano, célula = participações). BI §3.c (`service/impl/HistoricoPessoaServiceImpl.java:55-57`, `:93-105`).
- Consequência — a planilha montada como o documento descreve (coluna `Ano participação` com o ano na célula) interrompe a carga. Código (`HistoricoPessoaServiceImpl.java:97-103`).
- Substituição — GPE003 não fala em substituir. O código apaga e regrava o histórico de cada pessoa presente na planilha; quem não está nela não é tocado. BI §3.c (`HistoricoPessoaServiceImpl.java:91-92`, `:117-120`).
- `Cód. Contato` — nesta carga a célula tem de ser numérica; nas de grupos de trabalho e de temas, texto também serve. BI §3.c (`HistoricoPessoaServiceImpl.java:65-72`).
- Alcance — GPE003 fala em histórico "vinculado a uma determinada pessoa". O código carrega a planilha inteira. BI §3.c.

**❓ Lacunas**
- Formato pretendido da planilha — uma coluna por ano (código e instrução da janela) ou coluna única de ano (documento)?
- Ano — o cabeçalho numérico não é conferido como ano plausível; nenhuma fonte diz se deveria.
- Jira — `PDTIC25148-8` só pelo título.

**🔍 Inferências a confirmar**
- Coluna de cabeçalho não numérico com célula numérica: pela leitura do código a falha é respondida como erro de validação, com o texto técnico da conversão no detalhe, e não como erro genérico — o BI registra o contrário (ver "Erros nos insumos"). Código (`HistoricoPessoaServiceImpl.java:103`; `controller/handler/GlobalExceptionHandler.java:20-24`).
- Carga parcial quando há falha no meio. BI §6.1 item 17 (`HistoricoPessoaServiceImpl.java:42-43`).
- Duas pessoas com o mesmo CRM fazem a carga falhar, deixando gravadas as linhas anteriores. BI §6.1 item 19 (`repository/PessoaRepository.java:14`).

**⚠️ Suspeitas de defeito**
- A carga não é desfeita quando falha (não é transacional). BI §3.c e §6.1 item 17 (`HistoricoPessoaServiceImpl.java:42-43`).
- Qualquer coluna extra com número — por exemplo, um total — interrompe a carga. BI §6.1 item 17 (`HistoricoPessoaServiceImpl.java:103`).
- Planilha ilegível respondida como sucesso; a tela mostra "Carga concluída" com o detalhe ".". BI §3.c (`HistoricoPessoaServiceImpl.java:82-85`); FI §4.8 (`pessoas-filter.component.ts:173-185`).
- O resumo chama de "históricos de participação atualizados" a quantidade de linhas com pessoa encontrada, e de "pessoas não foram encontradas" também as linhas cujo código está gravado como texto. BI §3.c (`HistoricoPessoaServiceImpl.java:66-79`); FI §4.8.
- A pessoa encontrada sem nenhum ano maior que zero perde o histórico e é contada como atualizada. Código (`HistoricoPessoaServiceImpl.java:78-79`, `:91-105`).
- Pessoa em duas linhas: vale a última, sem aviso. Código (`HistoricoPessoaServiceImpl.java:91-92`).
- O servidor não confere extensão nem tipo do arquivo. BI §3.c (`util/ExcelUtils.java:117-123`).

---

*Links: [Resumo da revisão](../REVISAO-CONVERSAO.md) · [N2 do Feature Set](../modules/pessoas/cadastro-pessoas/README.md) · [INDEX geral](../modules/INDEX.md)*
