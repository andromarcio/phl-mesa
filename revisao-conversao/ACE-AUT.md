<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
# Revisão da conversão — Autenticação

> Detalhe, feature a feature, do que precisa de olho humano no Feature Set **Autenticação** (`ACE-AUT`), gerado na engenharia reversa de 2026-09-30. O resumo e as prioridades estão em [`REVISAO-CONVERSAO.md`](../REVISAO-CONVERSAO.md).
>
> **Como ler.** Cada feature traz quatro listas: **⚠️ Divergências documento × código** (decidir qual vale), **❓ Lacunas** (nenhuma fonte responde — precisa do PO), **🔍 Inferências a confirmar** (provavelmente certas) e **⚠️ Suspeitas de defeito** (o código faz algo que parece errado). Tudo veio da **leitura** do código — nada foi executado; o que depende de execução está dito como inferência.
>
> **Referências.** `arquivo:linha` aponta para o código-fonte: no front, pelo nome do arquivo; no back, pelo caminho a partir de `br/com/cni/apimesacheckin/`. "Inventário", **FI** e **BI** são os inventários do front e do back, guardados em [`arquivos/engenharia-reversa/`](../arquivos/engenharia-reversa/README.md). 

---

## ACE-AUT-01 — Autenticar Usuário

**⚠️ Divergências documento × código**

- Destino depois de entrar: GPE001 diz que o usuário "é direcionado para a tela inicial do sistema", um destino só; o código manda Secretaria Mesa e Secretaria Check-In para os participantes do evento principal e os demais para a tela de boas-vindas (`login.component.ts:67-78`).
- Endereço de acesso: GPE001 dá como endereço da tela de login o da tela de pessoas (`…/administracao-pessoas`), que é interna; o código mostra a tela de acesso a quem não tem sessão e, depois de entrar, leva ao destino do perfil, não ao endereço digitado (`auth-guard.service.ts:11-18`; `login.component.ts:67-78`).
- Matriz de GPE001 lista só Administrador, Secretaria Mesa e Secretaria Check-in; o código autentica qualquer perfil devolvido pelo cadastro corporativo, inclusive Painel e Participante, e a comparação de perfil é pelo nome exato (`login.component.ts:68`).
- Regras de negócio: GPE001 diz "Não se aplica"; o código tem validação de campos (usuário obrigatório, senha obrigatória com mínimo de 8), desvio por senha provisória e sessão guardada no navegador (`login.component.ts:50-52`, `:91-100`; `auth.service.ts:104-124`).

**❓ Lacunas**

- Texto da mensagem quando usuário ou senha estão errados: vem do cadastro corporativo, no campo de detalhe; não está no código do GPE (`page-base.ts:92-108`).
- Prazo de validade da sessão e se há bloqueio por tentativas erradas: decisão do cadastro corporativo; o GPE não renova a credencial (`interceptor.service.ts:36-39`, `:105-133`; `auth.service.ts:63-74`).
- Critérios da tarefa do Jira `PDTIC25148-17` (Definir uma página de login para aplicação): `tickets-jira.md` só traz o resumo; não foram consultados.
- Tamanho máximo e máscara dos campos Usuário e Senha: não há na tela (inventário 3.3: "não encontrado no front").

**🔍 Inferências a confirmar**

- A senha enviada pela recuperação de senha é tratada como provisória e leva à troca obrigatória: depende de o cadastro corporativo responder com o sinal de troca (`login.component.ts:91-93`); o N2 já marca 🔍.
- No desvio para a troca obrigatória, o sistema emite antes a mensagem de erro comum ("Erro" com o detalhe ou "Serviço indisponível.") e muda de tela em seguida; é provável que a mensagem não seja vista (`login.component.ts:80-86`).
- Serviços corporativos fora do ar ao abrir: a rota é barrada sem mensagem e a página tende a ficar em branco (`servicos-guard.service.ts:13-27`).
- Secretaria que cai na tela de boas-vindas (ao reabrir o sistema com a sessão guardada) não tem caminho de menu até os participantes: pelo menu declarado no cadastro do sistema, esses perfis só têm Dashboard (`backend-inventory.md` 2.4, `configuracoes.json:349-503`; rota vazia em `app-routing.module.ts:6-10`).

**⚠️ Suspeitas de defeito**

- "Lembrar": o controle existe no formulário, sem elemento na tela, e não é respeitado — a sessão é sempre guardada no navegador (`login.component.ts:52`, `:64`; `auth.service.ts:47-56`). Inventário 8.4.1.
- Mensagem "A sua senha deve ter mais de 8 caracteres." com aceitação de 8 caracteres (`basic-validators.ts:127-128`). Inventário 8.4.2.
- Secretaria sem evento principal fica parada na tela de acesso, já autenticada, sem mensagem: o servidor responde sem corpo e a tela falha ao ler o identificador antes de testar a resposta; a tela de aviso `/nao-ha-principal` existe e nunca é aberta (`login.component.ts:69-75`; `backend-inventory.md` linha do endpoint 19 e `EventoServiceImpl.java:433-437`). Inventário 8.4.3 — inferência, sem execução.
- Reabrir o endereço do sistema com a sessão guardada leva sempre à tela de boas-vindas, inclusive Secretaria Mesa e Secretaria Check-In (`app-routing.module.ts:6-10`). Não estava no inventário.
- Quem já está autenticado e abre o endereço da tela de acesso vê a tela de acesso normalmente (`auth.routing.ts:13-16`, sem guard de sessão).
- Sem indicador de espera e sem bloqueio do botão "Entrar" durante a conferência (`login.component.html:32`).

---

## ACE-AUT-02 — Encerrar Sessão

**⚠️ Divergências documento × código**

- GPE001 só descreve a saída pela opção "Logout"; o código também encerra a sessão sozinho quando a credencial é recusada (`interceptor.service.ts:36-41`, `:135-151`) ou quando não há usuário em sessão (`auth-guard.service.ts:11-18`).
- GPE001 escreve "encerrar sua seção"; o termo correto é sessão (erro de grafia do documento, sem efeito no comportamento).

**❓ Lacunas**

- Se a credencial continua aceita pelo cadastro corporativo depois da saída: o GPE não avisa o cadastro corporativo (`auth.service.ts:126-134`).
- GPE001 não diz se deve haver confirmação; o código não pede.

**🔍 Inferências a confirmar**

- O que estiver preenchido e não salvo na tela aberta se perde sem aviso ao sair (não há verificação antes do encerramento — `topbar.component.ts:113-116`).
- Na queda por credencial recusada, a tela de acesso não explica o motivo; a tela de origem pode chegar a emitir a sua própria mensagem de erro antes da troca.

**⚠️ Suspeitas de defeito**

- A saída limpa o que está guardado no navegador, mas não o que está em memória; a exigência de sessão consulta a memória. Até recarregar a página, o botão de voltar do navegador reabre as telas internas, e a credencial em memória continua sendo enviada (`auth.service.ts:126-134`; `auth-guard.service.ts:12-15`). Inventário 8.4.7 — inferência, sem execução.
- A saída não remove o identificador do evento principal guardado no navegador (`auth.service.ts:126-134`; `login.component.ts:71`).
- Renovação automática da credencial pronta e desligada: qualquer recusa derruba a sessão (`interceptor.service.ts:37`, `:105-133`). Inventário 8.3.
- Duas rotinas de saída sem uso (`admin.component.ts:165-168`; `profile.component.ts:42-45`). Inventário 3.6.

---

## ACE-AUT-03 — Recuperar Senha

**⚠️ Divergências documento × código**

- GPE001 diz que "o sistema encaminhará um link para que o usuário defina uma nova senha de acesso"; o texto da tela diz "Digite seu login e uma senha temporária será enviada para redefinir a sua senha" e a confirmação é "Senha temporária enviada." (`recuperar-senha.component.html:7`; `RecuperarSenhaComponent.ts:51`). A imagem do próprio documento (`GPE001-03.png`) mostra o texto da senha temporária. O envio é do cadastro corporativo: o código não confirma qual dos dois chega ao usuário.
- Nome: o documento chama a funcionalidade de "Esqueci Minha Senha"; a tela diz "Esqueceu a senha?" (atalho) e "Recuperar senha" (botão) (`login.component.html:29`; `recuperar-senha.component.html:26`).

**❓ Lacunas**

- Por qual meio e para qual endereço a senha é enviada (presume-se o e-mail do cadastro).
- Validade da senha temporária e se a senha anterior continua valendo até ela ser usada.
- O que o cadastro corporativo responde a login inexistente, usuário inativo ou pedido sem login, e com que texto.
- Se há limite de pedidos por login.

**🔍 Inferências a confirmar**

- A senha temporária é provisória e leva à troca obrigatória ao entrar (N2 já marca 🔍).
- Com o campo vazio, o pedido vai com o login "null" (`auth.service.ts:96-102`).

**⚠️ Suspeitas de defeito**

- O botão "Recuperar senha" não confere o preenchimento: o pedido é enviado mesmo com o campo vazio (`RecuperarSenhaComponent.ts:48-56`). Inventário 8.4.6.
- A confirmação "Senha temporária enviada." provavelmente não aparece: é emitida pelo serviço de alertas da aplicação, enquanto a área de mensagens desta tela e a da tela de acesso escutam o serviço de mensagens do próprio componente, e a tela muda no mesmo instante (`RecuperarSenhaComponent.ts:26`, `:51-52`; `alerta.service.ts:5-11`; `login.component.ts:28`; `main.ts:43`). Não estava no inventário — inferência, sem execução.
- Basta conhecer o login de outro usuário para pedir a recuperação da senha dele; nenhum outro dado é exigido (`RecuperarSenhaComponent.ts:39-43`). Ponto de atenção de segurança, a avaliar com o PO.
- A moldura mantém a frase "Faça o login para acessar." nesta tela (`auth.component.html:10`).

---

## ACE-AUT-04 — Alterar Senha

**⚠️ Divergências documento × código**

- GPE001 só descreve a troca do primeiro acesso; o código tem também a troca voluntária, pela opção "Alterar Senha" do menu do usuário, com o campo "Senha Atual" (`topbar.component.html:54-59`; `alterar-senha.component.html:11-19`; `alterar-senha-guard.ts:12-18`). A opção aparece nas imagens `GPE001-02.png` e `-06.png`, sem descrição no texto.
- Destino depois da troca: o documento não diz; o código vai sempre para a tela de boas-vindas, sem o desvio por perfil que existe na autenticação (`alterar-senha.component.ts:71-78`).
- Aviso de troca obrigatória ("Alteração de senha obrigatória!" / "Para continuar altere a sua senha."): está no código (`alterar-senha.component.ts:28-32`) e não aparece na imagem `GPE001-04.png`.

**❓ Lacunas**

- Política de senha além do mínimo de 8 caracteres (composição, reuso, igualdade com a atual): só o cadastro corporativo sabe.
- Texto das recusas do cadastro corporativo (senha atual errada, nova senha fora da política).
- Se o cadastro corporativo registra data e autor da troca.
- Validade da senha provisória do primeiro acesso.

**🔍 Inferências a confirmar**

- O aviso de troca obrigatória não é exibido como previsto: o texto é passado como lista de objeto para dentro do componente de mensagem (`alterar-senha.component.html:3-5`). O inventário (8.4.4) infere que apareceria "[object Object]"; a imagem do documento não mostra aviso nenhum. Confirmar em execução.
- "As senhas não conferem." aparece assim que os dois valores diferem, inclusive enquanto a nova senha é digitada e a confirmação está vazia (`basic-validators.ts:133-143`; `alterar-senha.component.html:39-41`).
- Falha na autenticação automática depois da troca deixa o usuário na tela, sem mensagem, com a senha já trocada (`alterar-senha.component.ts:71-78`).

**⚠️ Suspeitas de defeito**

- Erros do cadastro corporativo não aparecem: a tela não tem área de mensagens, e o componente usa um serviço de mensagens próprio (`alterar-senha.component.html:6-8`; `alterar-senha.component.ts:23`). Inventário 8.4.4.
- Depois da troca, Secretaria Mesa e Secretaria Check-In vão para a tela de boas-vindas, e não para os participantes do evento principal (`alterar-senha.component.ts:74`). Inventário 8.4.4. Pelo menu declarado, esses perfis não têm caminho de menu de lá até os participantes 🔍.
- A troca obrigatória nunca é esquecida depois de concluída: na mesma sessão de página, "Alterar Senha" do menu abre no modo obrigatório, sem "Senha Atual" e com a senha provisória antiga (`auth.service.ts:14`; `login.component.ts:95-100`). Inventário 8.4.5 — inferência.
- Na troca voluntária, o usuário autenticado vê a moldura da tela de acesso ("Faça o login para acessar."), sem cabeçalho nem menu, e o botão "Voltar" o leva à tela de acesso, não à tela de onde veio (`auth.routing.ts:9-27`; `alterar-senha.component.html:47`).
- Mensagem "A sua senha deve ter mais de 8 caracteres." com aceitação de 8 (`basic-validators.ts:127-128`). Inventário 8.4.2.

---

## ACE-AUT-05 — Alterar Foto de Perfil

**⚠️ Divergências documento × código**

- GPE001 descreve a funcionalidade e mostra a janela "Alterar Imagem do Perfil", com "Selecionar Imagem" e "Salvar Imagem" (`GPE001-05.png`); no código o item de menu existe, mas a tela não tem a janela, o seletor de arquivo nem o botão de salvar — o clique não abre nada (`topbar.component.html:48-53`, `:1-70`; `topbar.component.ts:42-45`). **Feature documentada que hoje não funciona pela tela.**
- Nome da opção: o texto do documento diz "Alterar foto do perfil"; o título da janela na imagem diz "Alterar Imagem do Perfil"; a funcionalidade se chama "Alterar imagem de perfil"; o item de menu, no código, é "Alterar Foto do Perfil" (`topbar.component.html:51`).

**❓ Lacunas**

- Formato, tamanho e dimensões aceitos para a imagem: nem o documento nem a rotina existente definem (`topbar.component.ts:47-64`).
- Se há recorte ou ajuste da imagem: a biblioteca de recorte está importada e não é usada (`topbar.component.ts:7`, `:26`, `:48-50`).
- Se a ausência da janela é defeito ou retirada intencional — decisão a confirmar com o PO e com o time.
- Se o cadastro corporativo registra quem trocou a foto e quando.

**🔍 Inferências a confirmar**

- A nova foto substitui a anterior, sem histórico (a rotina grava por cima — `auth.service.ts:84-88`).
- O texto da instrução da janela ("Para trocar a foto do seu perfil click no botão Selecionar Imagem.") foi lido da imagem `GPE001-05.png`; não existe mais no código.
- Onde apareceriam "Foto Alterada" e a mensagem de erro: saem pelo serviço de alertas do cabeçalho, e só seriam vistas em tela que tenha área de mensagens ligada ao serviço da aplicação (`topbar.component.ts:19`, `:83-93`).

**⚠️ Suspeitas de defeito**

- "Alterar Foto do Perfil" não abre nada (`topbar.component.html:48-53`; `topbar.component.ts:42-45`). Inventário 8.4.8.
- Rotinas de selecionar, pré-visualizar e gravar a foto sem acionador (`topbar.component.ts:47-93`; `auth.service.ts:84-88`). Inventário 3.8 e 6.1.
- Mensagem de erro "Serviço indisponível" sem ponto final, diferente das demais telas de acesso (`topbar.component.ts:90`, `:104`).
- Instrução da janela, na imagem do documento, com "click" no lugar de "clique".

---

## ACE-AUT-06 — Consultar Dados do Usuário

**⚠️ Divergências documento × código**

- O texto de GPE001 não diz quais dados são consultados; a imagem (`GPE001-06.png`) e o código mostram Nome, Login, Perfil e Email (`topbar.component.html:23-47`). Sem conflito — o documento é que é omisso.
- GPE001 fala em "link do usuário"; na tela é a foto com o nome do usuário, no cabeçalho (`topbar.component.html:18-21`).

**❓ Lacunas**

- GPE001 não inclui a funcionalidade na matriz de perfis (só Efetuar Login e Efetuar Logout); o código não distingue perfil.
- Se o usuário deveria ver mais dados (CPF, telefone, cargo, instituições) — o documento não diz.

**🔍 Inferências a confirmar**

- Dados alterados no cadastro durante a sessão só aparecem depois de sair e entrar de novo, porque vêm do que a autenticação devolveu (`auth.service.ts:33-39`, `:104-117`; inventário 3.7).
- Usuário sem foto fica com o espaço da foto vazio, sem imagem padrão (`topbar.component.html:19`; `topbar.component.ts:66-81`).
- Dado sem valor no cadastro aparece só com o rótulo.
- A mensagem de erro da busca da foto só é vista em tela que tenha área de mensagens ligada ao serviço da aplicação (`topbar.component.ts:19`, `:96-107`).

**⚠️ Suspeitas de defeito**

- Erro na busca da foto usa o detalhe (ou "Serviço indisponível", sem ponto) como título da mensagem, com o detalhe vazio (`topbar.component.ts:104`; `alerta.service.ts:13`, `:35-38`).
- Sobras de depuração no cabeçalho (`topbar.component.ts:59`, `:120`). Inventário 8.2.

---

*Links: [Resumo da revisão](../REVISAO-CONVERSAO.md) · [N2 do Feature Set](../modules/acesso-usuarios/autenticacao/README.md) · [INDEX geral](../modules/INDEX.md)*
