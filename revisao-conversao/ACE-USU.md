<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
# Revisão da conversão — Usuários

> Detalhe, feature a feature, do que precisa de olho humano no Feature Set **Usuários** (`ACE-USU`), gerado na engenharia reversa de 2026-09-30. O resumo e as prioridades estão em [`REVISAO-CONVERSAO.md`](../REVISAO-CONVERSAO.md).
>
> **Como ler.** Cada feature traz quatro listas: **⚠️ Divergências documento × código** (decidir qual vale), **❓ Lacunas** (nenhuma fonte responde — precisa do PO), **🔍 Inferências a confirmar** (provavelmente certas) e **⚠️ Suspeitas de defeito** (o código faz algo que parece errado). Tudo veio da **leitura** do código — nada foi executado; o que depende de execução está dito como inferência.
>
> **Referências.** `arquivo:linha` aponta para o código-fonte: no front, pelo nome do arquivo; no back, pelo caminho a partir de `br/com/cni/apimesacheckin/`. "Inventário", **FI** e **BI** são os inventários do front e do back, guardados em [`arquivos/engenharia-reversa/`](../arquivos/engenharia-reversa/README.md). 

---

## ACE-USU-01 — Pesquisar Usuários

**⚠️ Divergências documento × código**
- Carga inicial — o documento descreve pesquisa por filtros; o código lista todos os usuários ao abrir a tela, sem filtro (`usuarios-list.component.ts:47-50`, `:63-66`; `usuario-acesso.service.ts:14-27`).
- Filtro "Departamento Regional" — não consta no documento (filtros: Entidade, Perfil, Nome, Login); existe na tela, aparece depois de escolhida a entidade (`usuarios-filter.component.html:24-40`).
- Título de coluna — o documento diz "Responsável Cadastro"; a tela diz "Responsável Cadastrado" (`usuarios-list.component.ts:165`).
- Nome das opções de linha — o documento diz "Editar" e "Excluir"; a tela usa as dicas "Editar Usuário" e "Remover Usuário" (`usuarios-list.component.html:48-60`).
- Grafia dos perfis — a tabela de filtros do documento traz "Secretária Mesa / Secretária Check-in"; a do formulário, "Secretaria Mesa / Secretaria Check-in"; o cadastro corporativo devolve "Secretaria Mesa" e "Secretaria Check-In" (`configuracoes.json:23-54` do backend; `usuarios-filter.component.ts:72-81`).

**❓ Lacunas**
- Busca por parte do nome e do login — o documento afirma; o GPE só repassa o texto ao cadastro corporativo (`usuario-acesso.service.ts:14-27`). Como a correspondência é feita não aparece em fonte nenhuma.
- Combinação dos filtros (todos ao mesmo tempo) — decidida pelo cadastro corporativo.
- Ordem inicial da lista — a tela não define; vem na ordem devolvida pelo serviço.
- Usuários inativos — a coluna "Situação" admite "Inativo" (`ativo-inativo-converter.ts:4-12`), mas não há filtro de situação nem dá para saber se o serviço os devolve.
- Recorte por sistema — se a operação consultada devolve só os usuários deste sistema.

**🔍 Inferências a confirmar**
- A pesquisa traz só usuários deste sistema (regra 1) — deduzido do nome da operação (`urlPesquisaUsuariosSistema`, `usuario-acesso.service.ts:11`).
- Usuário de perfil Painel ou Participante, se existir, aparece na lista sem filtro de perfil (a restrição aos três perfis é só da lista de opções) (`usuarios-filter.component.ts:75`; `usuarios-list.component.ts:84-90`).
- A tela não tem onde exibir mensagens — item 10 de 8.4: não há `<p-toast>` na página, no filtro nem na lista, nem na moldura (`usuarios.component.html`, `usuarios-filter.component.html`, `usuarios-list.component.html`, `admin.component.html:11-15`); as mensagens saem pelo `AlertaService`, ligado ao `MessageService` da raiz (`alerta.service.ts:5-11`; `main.ts:43`).
- Acionar "Pesquisar" duas vezes sem mudar filtro não refaz a consulta — o filtro emite o mesmo objeto (`usuarios-filter.component.ts:68-70`), a página o repassa por atribuição (`usuarios.component.ts:36-38`) e a lista só consulta quando a entrada muda de referência (`usuarios-list.component.ts:46-50`).
- As dicas "Editar Usuário" e "Remover Usuário" podem não aparecer — item 11 de 8.4 (`usuarios-list.component.ts:30-40`).

**⚠️ Suspeitas de defeito**
- Item 9 de 8.4 — o filtro "Entidade" chama a carga de departamentos sem argumento: a lista nunca carrega, o campo aparece vazio e o parâmetro enviado (`departamento`) não é o do formulário (`departamentoRegional`) (`usuarios-filter.component.html:16`; `usuarios-filter.component.ts:94-113`, `:140-143`, `:148`; `usuario-acesso.service.ts:19`).
- O perfil é filtrado duas vezes (no serviço e de novo na tela), e a lista altera o objeto de filtro recebido, trocando o perfil pelo id (`usuarios-list.component.ts:68-71`, `:84-90`).
- A consulta inicial é disparada duas vezes ao abrir a tela (pela entrada `filtro` e pelo `ngOnInit`) (`usuarios-list.component.ts:47-50`, `:63-66`).
- Controles `unidade` e `area` sem campo na tela, enviados sempre vazios (`usuarios-filter.component.ts:149-150`; `usuario-acesso.service.ts:20-22`).
- Falha na carga dos perfis, das entidades ou da lista passa sem aviso (consequência do item 10).

---

## ACE-USU-02 — Cadastrar Usuário

**⚠️ Divergências documento × código**
- Senha provisória — o documento diz que, após o cadastro, o sistema encaminha uma senha provisória; o código do GPE só chama a inclusão no cadastro corporativo e não dispara nem confirma envio (`usuario.component.ts:257-268`; `http-crud.service.ts:37-40`). Detalhe relevante: o formulário envia, sem campo na tela, `enviaPreCadastro = false` e `recebeEmail = true` (`usuario.component.ts:306-307`).
- Cargo — obrigatório no documento (256 caracteres); opcional na tela, sem asterisco e sem limite (`usuario.component.ts:300`; `usuario.component.html:172-180`). A imagem `GPE002-02.png` mostra "Cargo*".
- Entidade — no documento, campo de seleção única "Entidade", opcional, valor "Confederação Nacional da Indústria"; na tela, painel "Instituições Relacionadas", que só aparece quando o perfil tem tipo e pede Entidade, Departamento Regional e Unidade conforme o tipo (`usuario.component.html:214-217`; `instituicoes-relacionadas.component.html:3-31`; `instituicoes-relacionadas.component.ts:254-284`).
- Tamanhos — o documento fixa Login 255, Nome 255, Email 256, Cargo 256; a tela não limita nenhum (`usuario.component.html:35-41`, `:76-80`, `:161-165`, `:175-178`).
- Telefone — o documento dá 11 posições numéricas; a tela aceita DDD de 2 dígitos e número de 8 (`usuario.component.html:111-121`).
- Conferência de CPF e de e-mail — o documento não prevê; a tela valida, com "CPF inválido" e "Email inválido" (`usuario.component.ts:298`, `:308`; `basic-validators.ts:110-118`, `:190-251`).
- Bloqueio dos dados do usuário interno — o documento não menciona; a tela bloqueia nome, CPF, cargo, telefone, celular e e-mail (`usuario.component.ts:139-150`).
- Login já cadastrado — o documento não trata; a tela recusa com "Usuário já cadastrado no sistema." (`usuario.component.ts:166-174`).
- Texto da validação do login — o documento fala em "login" e "endereço de e-mail externo"; a mensagem da tela cita "Active Directory" (`usuario.component.ts:132-135`).

**❓ Lacunas**
- O envio da senha provisória acontece? Quem o dispara, e que efeito têm `enviaPreCadastro = false` e `recebeEmail = true` no cadastro corporativo.
- Que conflitos o cadastro corporativo recusa na inclusão (CPF ou e-mail já usados, por exemplo) e com que texto.
- A instituição relacionada é exigida pelo cadastro corporativo? A tela não exige (`usuario.component.ts:310`).
- Quem preenche "Responsável Cadastro" e "Data Cadastro" — a tela não os envia.
- Que dados o diretório devolve para o usuário interno, e o que acontece se vier sem CPF ou sem e-mail (os campos bloqueados não são validados).
- Significado das siglas de tipo de perfil `DN`, `DR`, `UA` — o código não traz rótulos (`tipo-perfil.enum.ts:1-5`); os N3 usam os nomes do modelo de dados.

**🔍 Inferências a confirmar**
- Mensagem de sucesso e erros da gravação não aparecem — o `<p-toast />` do formulário (`usuario.component.html:14`) é alimentado pelo `MessageService` declarado no próprio componente (`usuario.component.ts:29`); "Usuário Criado com Sucesso" e `handleErrorAlert` saem pelo `AlertaService`, ligado ao `MessageService` da raiz (`usuario.component.ts:261`, `:264`; `page-base.ts:14-24`; `alerta.service.ts:5-11`), e a exibição de `validationErrors` está comentada (`usuario.component.html:13`, `:17`). Os avisos da validação do login e "Formulário inválido" usam o serviço do componente e aparecem.
- Usuário externo que já existe no cadastro corporativo abre o formulário preenchido e editável (o bloqueio só vale para `interno`) (`usuario.component.ts:97-103`, `:139-150`, `:180-188`).
- Item 12 de 8.4 — CPF com o primeiro dígito verificador errado mostra "Campo obrigatório." (`basic-validators.ts:234-236`; `form-component-base.ts:69-74`).
- Validar um segundo login sem sair da tela reaproveita os dados e o bloqueio do login anterior — a rota `:login` reutiliza o mesmo componente, e o formulário só é esvaziado quando a rota vem sem login (`usuario.component.ts:84-92`, `:94-116`, `:139-150`, `:166-174`, `:283-286`; `usuarios.routing.ts:10-17`). Na gravação, iria inclusive o código do usuário anterior.
- Controles obrigatórios sem campo na tela (`recebeEmail`, `enviaPreCadastro`) e validadores de data de vigência sem campo: se o cadastro corporativo devolver esses valores nulos ou em outro formato, o formulário fica inválido sem campo marcado (`usuario.component.ts:305-317`).
- O número de telefone e de celular segue com a máscara; só o DDD e o CPF são limpos antes do envio (`usuario.component.ts:219-236`).

**⚠️ Suspeitas de defeito**
- Item 13 de 8.4 — em "Instituições Relacionadas", adicionar sem unidade substitui a lista; o teste de duplicidade compara `item.id`, que não existe; a carga de unidades está comentada, e o campo "Unidade" nunca aparece (`instituicoes-relacionadas.component.ts:118-124`, `:193-208`, `:220-228`).
- Qualquer falha na consulta do usuário no sistema — não só "não encontrado" — é lida como "não cadastrado" e abre o formulário de inclusão (`usuario.component.ts:180-188`).
- CPF de dígitos todos iguais só é recusado quando é zero; os demais passam pela conta dos dígitos verificadores (`basic-validators.ts:218-220`).
- Erro de digitação na mensagem: "O usuário informado já estas no sistema." (`usuario.component.ts:170`).
- Item 14 de 8.4 — `buscarBasi` troca `'{codigoUsuario}/'` com barra, enquanto `buscarPorCodigoNoSistema` troca sem barra (`usuario.service.ts:28-31`, `:33-39`).
- A mensagem do login recusado vai inteira no resumo, com quebra de linha no meio do texto (`usuario.component.ts:132-135`).

---

## ACE-USU-03 — Editar Usuário

**⚠️ Divergências documento × código**
- Dados editáveis — o documento diz que "todos os dados podem ser editados, com exceção do login"; para usuário interno, a tela bloqueia nome, CPF, cargo, telefone, celular e e-mail (`usuario.component.ts:139-150`).
- Botão "Limpar" e asterisco em "Cargo" — a imagem `GPE002-02.png` ("Atualizar Usuário") mostra os dois; na tela atual "Limpar" só existe no cadastro e "Cargo" não tem asterisco (`usuario.component.html:52-53`, `:172`).
- Nome da opção — o documento diz "Editar"; a tela usa a dica "Editar Usuário" e o título "Atualizar Usuário" (`usuarios-list.component.html:48-54`; `usuario.component.html:10`, `:22`).
- Cargo obrigatório e tamanhos dos campos — as mesmas divergências de ACE-USU-02 — Cadastrar Usuário.

**❓ Lacunas**
- Que alterações o cadastro corporativo recusa e com que texto.
- Quem preenche "Responsável Atualização" e "Data Atualização" — a tela não os envia.
- Editar o próprio usuário: se a troca do próprio perfil vale na sessão em curso (o perfil fica guardado desde a autenticação, `auth.service.ts:33-35`).
- Editar usuário inativo: nenhuma restrição no código; o cadastro corporativo aceita?

**🔍 Inferências a confirmar**
- Mensagem "Usuário Atualizado com Sucesso" e erros da gravação não aparecem — mesmo mecanismo de ACE-USU-02 — Cadastrar Usuário (`usuario.component.ts:29`, `:270-281`; `usuario.component.html:14`).
- Usuário com perfil fora dos três oferecidos só é gravado depois de receber um deles; a tela esvazia "Perfil" e mostra "Campo obrigatório.", sem "Formulário inválido" (`usuario.component.ts:202-203`, `:245-255`).
- Aberta pelo endereço para um login que o cadastro corporativo conhece e o sistema não, a tela vira "Cadastrar Usuário"; para um e-mail desconhecido, abre o cadastro em branco (`usuario.component.ts:126-131`, `:180-188`).
- Na edição, a lista "Entidade" de "Instituições Relacionadas" pode ficar sem opções depois de qualquer alteração no formulário: o painel nasce já com o perfil, guarda a lista de entidades antes de ela ser carregada e a reaplica a cada mudança (`instituicoes-relacionadas.component.ts:49-65`, `:92-94`, `:132-145`, `:167-176`; `usuario.component.html:59`, `:214-217`).
- O e-mail do usuário externo pode ser alterado sem que o login — o e-mail original — mude.
- "Responsável Atualização" e "Data Atualização" são preenchidos pelo cadastro corporativo.

**⚠️ Suspeitas de defeito**
- Falha na consulta do usuário no sistema durante a abertura da edição faz a tela se apresentar como inclusão; concluir tentaria incluir um usuário que já existe (`usuario.component.ts:180-188`, `:204-208`).
- Item 13 de 8.4 — adicionar instituição substitui a existente (`instituicoes-relacionadas.component.ts:118-124`).
- Item 12 de 8.4 — mensagem do CPF (`basic-validators.ts:234-236`).

---

## ACE-USU-04 — Excluir Usuário

**⚠️ Divergências documento × código**
- Nome da opção — o documento diz "Excluir"; a tela diz "Remover Usuário", com a pergunta "Deseja remover este usuário?" e os botões "Remover" e "Cancelar" (`usuarios-list.component.html:1-6`, `:55-60`; `usuarios-list.component.ts:131-138`).
- Confirmação — o documento não menciona; a tela exige.

**❓ Lacunas**
- Exclusão lógica ou definitiva — o documento diz "passa a não ser exibido no sistema"; o código chama a exclusão no cadastro corporativo (`http-crud.service.ts:52-55`) e não mostra o que acontece lá.
- Alcance — se a exclusão retira o usuário só deste sistema ou do cadastro corporativo inteiro.
- Auto-exclusão e exclusão do último Administrador — a tela não tem trava; o cadastro corporativo recusa?
- O que acontece com a sessão em curso do usuário excluído.
- Um login excluído pode ser incluído de novo? Depende de a exclusão ser lógica ou definitiva.

**🔍 Inferências a confirmar**
- A exclusão alcança só este sistema — deduzido do nome do endereço (`urlAtualizaUsuarioSistema`, o mesmo da alteração).
- "Usuário removido com Sucesso" e os erros não aparecem — item 10 de 8.4 (`usuarios-list.component.ts:140-152`).

**⚠️ Suspeitas de defeito**
- Sem aviso de sucesso nem de falha: no sucesso a linha some; na falha nada muda na tela.
- Nenhuma trava contra a exclusão do próprio usuário (`usuarios-list.component.html:55-60`).
- Código sem uso na lista: `mudarSituacao` (ativar e desativar) e `copiar` (`usuarios-list.component.ts:104-129`) — coerente com a nota "Não faz" do N2.

---

## Sobras citadas e não especificadas

- "Áreas" (`AreasComponent`) e "Linhas do usuário" (`LinhasUsuarioComponent`, `AdicionarLinhasUsuarioComponent`) — importados, mas fora da tela e sem rota; vocabulário de outro sistema (`usuario.component.ts:8-9`, `:30-44`, `:58-61`; 8.1 e 8.2 do inventário). Não fazem parte do sistema e não entraram em nenhum N3. Os controles `areas` e `linhas` seguem vazios no envio (`usuario.component.ts:309`, `:311`).
- Ajuda de campo (`app-hint`) ao lado de "Departamento Regional" e "Unidade" — só editável pelo perfil "MASTER DN", que não existe neste sistema (`instituicoes-relacionadas.component.html:36-42`, `:60-66`). Como esses dois campos não aparecem para os perfis oferecidos, não foi especificada.
- Datas de vigência de acesso (`dataInicioVigenciaAcesso`, `dataFimVigenciaAcesso`) — controles com validador e sem campo na tela (`usuario.component.ts:312-317`).

---

*Links: [Resumo da revisão](../REVISAO-CONVERSAO.md) · [N2 do Feature Set](../modules/acesso-usuarios/usuarios/README.md) · [INDEX geral](../modules/INDEX.md)*
