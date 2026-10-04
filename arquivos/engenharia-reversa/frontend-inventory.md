# Inventário factual das telas do frontend — Sistema de Mesa e Check-in (GPE / CNI)

- **Repositório analisado**: `sistema_mesa_checkin_frontend` (Angular 18 + PrimeNG 18; `package.json` → `"name": "mesa_checkin_frontend"`).
- **Escopo lido**: todos os `.ts` e `.html` de `src/app` (inclusive roteamento, guards, interceptor, `auth`, `service`, `shared`), `src/main.ts`, `src/index.html`, `src/environments/*`, `src/assets/i18n/pt-BR.json`, `angular.json` (configurações de build) e `tsconfig.json`. Ignorados: `src/assets/demo`, temas e CSS (CSS consultado só para confirmar cores do mapa de assentos).
- **Método**: leitura integral dos `.ts`/`.html` de `src/app`, com estas exceções declaradas: (a) os sete `.spec.ts` não foram lidos, salvo `painel.component.spec.ts`; (b) dos quatro componentes grandes do mapa de assentos, dois `.ts` e dois `.html` foram lidos por inteiro e os demais por `diff` contra o par mais próximo (o que foi lido de cada um está em 5); (c) `pessoas-carga-historico` foi lido por `diff` contra `pessoas-carga-tema`. Nada foi executado; afirmações marcadas como *inferência* decorrem de raciocínio sobre o código, não de teste.
- **Conferência mecânica feita no relatório**: 731 referências `arquivo:linha` conferidas quanto a existência do arquivo e faixa de linhas (0 problemas; a checagem foi provada com casos que devem falhar); 682 textos entre aspas confrontados com o código — os 52 não localizados literalmente são composições (texto + variável), termos explicativos do próprio relatório ou textos de `pt-BR.json`. Essa conferência não valida a interpretação, só a existência.
- **Convenção de referência**: `arquivo:linha` usa o **nome do arquivo** (único no repositório, salvo indicação). Caminhos completos na tabela abaixo. Quando uma célula traz só `html:NN` ou `ts:NN`, refere-se ao arquivo citado no início do mesmo item.
- **Nome do sistema na interface**: "Gestão de Participantes em Eventos" (`topbar.component.ts:24`, `painel.component.ts:10`); na tela de login, "Portal de Gestão de Participantes em Eventos" (`auth.component.html:6`). A sigla "GPE" e o nome "Sistema de Mesa e Check-in" não aparecem como texto de tela; o `<title>` da página é "Projeto - Base" (`index.html:5`).

### Índice de arquivos citados (caminho a partir de `src/app`, salvo indicação)

| Pasta | Arquivos |
|---|---|
| `src/` | `main.ts`, `index.html`, `environments/environment*.ts` |
| `.` | `app-routing.module.ts`, `app.component.*` |
| `auth/` | `auth.routing.ts`, `auth.component.*`, `login/login.component.*`, `alterar-senha/alterar-senha.component.*`, `alterar-senha/alterar-senha-guard.ts`, `recuperar-senha/RecuperarSenhaComponent.ts`, `recuperar-senha/recuperar-senha.component.html` |
| `service/core/` | `auth.service.ts`, `auth-guard.service.ts`, `servicos-guard.service.ts`, `servicos.service.ts`, `interceptor.service.ts`, `alerta.service.ts` |
| `service/cached/`, `service/crud/` | `entidade.service.ts`, `departamento-regional.service.ts`, `unidade.service.ts`, `areas-perfis.service.ts`, `area.service.ts`, `perfis.service.ts`, `categoria-tipo-atendimento.service.ts`, `configuracoes-indicador.service.ts`; `hint.service.ts`, `mensagens.service.ts`, `notificacao.service.ts` |
| `shared/` | `basic-validators.ts`, `page-base.ts`, `form-component-base.ts`, `form-base.ts`, `list-base.ts`, `crud-base.ts`, `cadastro-helper.ts`, `form-helper.ts`, `page-helper.ts`, `http.service.ts`, `http-crud.service.ts`, `http-cached.service.ts`, `http-routed.service.ts`, `arquivo.interface.ts`, `cadeira-mesa.interface.ts`, `carga.interface.ts`, `enum/*.enum.ts`, `converter/*.ts`, `hint/hint.component.*`, `error/error.component.*`, `layout/menu/menu.component.*`, `layout/menu/submenu/*`, `layout/topbar/topbar.component.*`, `layout/profile/profile.component.*`, `layout/footer/*`, `alerta/*`, `gauge/*`, `dados-cadastro/*`, `pipes/situacao.pipe.ts` |
| `admin/` | `admin.routing.ts`, `admin.module.ts`, `admin.component.*`, `painel/painel.*` |
| `admin/administracao/` | `administracao.routing.ts` |
| `admin/administracao/acessibilidade/` | `acessibilidade.routing.ts` |
| `…/acessibilidade/usuarios/` | `usuarios.routing.ts`; `pages/usuarios/usuarios.component.*`; `pages/usuarios/components/usuarios-filter/*`; `pages/usuarios/components/usuarios-list/*`; `pages/usuario/usuario.component.*`; `pages/usuario/instituicoes-relacionadas/*`; `pages/usuario/areas/*`; `pages/usuario/linhas-usuario/*` (inclui `adicionar-linhas-usuario/*`); `services/usuario.service.ts`, `usuario-acesso.service.ts`, `perfis-acesso.service.ts`, `usuario-copia.service.ts`, `instituicoes-conversor/instituicoes-conversor.service.ts`; `shared/filtro-usuarios.pipe.ts` |
| `…/acessibilidade/pessoas/` | `pessoas.routing.ts`; `pages/pessoas/pessoas.component.*`; `pages/pessoas/components/pessoas-filter/*`, `pessoas-list/*`, `pessoas-carga-gt/*`, `pessoas-carga-tema/*`, `pessoas-carga-historico/*`; `pages/pessoa/pessoa.component.*`; `pages/pessoa/components/cadastro/pessoa-cadastro.component.*`, `contato/pessoa-contato.component.*`, `empresa/pessoa-empresa.component.*`, `relacionamento/pessoa-relacionamento.component.*`, `historico/pessoa-historico.component.*`; `services/pessoa.service.ts`, `pessoa.interface.ts` |
| `admin/administracao/evento/` | `evento-routing.module.ts`, `evento.module.ts`; `pages/eventos/eventos.component.*`; `pages/eventos/components/eventos-filter/*`; `pages/eventos/components/eventos-list/evento-list.component.*`; `…/eventos-list/components/evento-participantes/*`; `pages/evento/create/evento-create.component.*`; `pages/nao-ha-principal/*`; `services/evento.service.ts`, `evento-legenda.service.ts`, `evento.interface.ts` |
| `admin/administracao/evento-pessoa/` | `evento-pessoa-routing.module.ts`, `evento-pessoa.module.ts`; `evento-pessoa/evento-pessoa.component.*`; `evento-pessoa/components/evento-pessoas-filter/*`, `evento-pessoas-list/*`, `pessoa-cadastro/pessoas-cadastro.component.*`, `evento-pessoa-principal/*`; `evento-pessoa/components/mesa/mesa.component.*`, `mesa/components/retangular/retangular.component.*`, `mesa/components/retangular-invertido/retangular-invertido.component.*`; `evento-pessoa/components/mesa-recepcionista-checkin/mesa-recepcionista-checkin.component.*`, `…/components/retangular/retangular-recepcionista-checkin.component.*`, `…/components/retangular-invertido/retangular-invertido-recepcionista-checkin.component.*`; `services/evento-pessoa.service.ts`, `evento-pessoa.interface.ts`, `legenda-mesa.helper.ts`; `mesa/mesa.component.*` (arquivos vazios) |
| `admin/administracao/legendas/` | `legendas-routing.module.ts`, `legendas.module.ts`; `pages/catalogo-legendas/*`; `pages/configuracao-legendas-evento/*`; `components/adicionar-bloco-dialog/*`, `bloco-form/*`, `bloco-evento-card/*`, `condicao-linha/*`, `salvar-preset-dialog/*`, `carregar-configuracao-dialog/*`, `simulacao-dialog/*`; `services/legenda-catalogo.service.ts`, `legenda.interface.ts` |

Observação: existem dois `mesa.component.ts` — o usado é `evento-pessoa/evento-pessoa/components/mesa/mesa.component.ts`; o de `evento-pessoa/mesa/` tem 0 bytes.

---

## 1. Rotas

`{baseUrl}` nas demais seções = `environment.baseUrl` (ver 3.1). Roteador sem *hash* (`HashLocationStrategy` comentado — `main.ts:36`); `APP_BASE_HREF = '/'` (`main.ts:39`).

| Path completo | Componente | Guards | Dados de rota | Perfis exigidos pela rota | Ref. |
|---|---|---|---|---|---|
| `/` (vazio) | redireciona para `/dashboard-simples` (`pathMatch: 'full'`) | — | — | — | `app-routing.module.ts:6-10` |
| `/login` | `LoginComponent` (dentro de `AuthComponent`) | `ServicosGuard` | — | nenhum | `app-routing.module.ts:11-18`; `auth.routing.ts:13-16` |
| `/alterar-senha` | `AlterarSenhaComponent` (dentro de `AuthComponent`) | `ServicosGuard`, `AlterarSenhaGuard` | — | nenhum (exige login pendente de troca ou usuário logado) | `auth.routing.ts:17-21`; `alterar-senha-guard.ts:12-18` |
| `/recuperar-senha` | `RecuperarSenhaComponent` (dentro de `AuthComponent`) | `ServicosGuard` | — | nenhum | `auth.routing.ts:22-25` |
| `/dashboard-simples` | `PainelComponent` | `AuthGuard`, `ServicosGuard` | — | nenhum | `app-routing.module.ts:18-25`; `admin.routing.ts:5-19`; `painel.routing.ts:4-7` |
| `/administracao-usuarios` | `UsuariosComponent` | idem | — | nenhum | `usuarios.routing.ts:6-9` |
| `/administracao-usuario` | `UsuarioComponent` | idem | — | nenhum | `usuarios.routing.ts:10-13` |
| `/administracao-usuario/:login` | `UsuarioComponent` (aceita *query* `novoUsuario`) | idem | — | nenhum | `usuarios.routing.ts:14-17`; `usuario.component.ts:85-87` |
| `/administracao-pessoas` | `PessoasComponent` | idem | — | nenhum | `pessoas.routing.ts:6-9` |
| `/administracao-pessoa` | `PessoaComponent` | idem | — | nenhum | `pessoas.routing.ts:10-13` |
| `/administracao-pessoa/:id` | `PessoaComponent` | idem | — | nenhum | `pessoas.routing.ts:14-17` |
| `/eventos` | `EventosComponent` | idem | `breadcrumb: 'Lista'` | nenhum | `administracao.routing.ts:17-26`; `evento-routing.module.ts:8` |
| `/eventos/detail` | `EventoCreateComponent` | idem | `breadcrumb: 'Controle'` | nenhum | `evento-routing.module.ts:9` |
| `/eventos/detail/edit/:id` | `EventoCreateComponent` | idem | `breadcrumb: 'Controle'` | nenhum | `evento-routing.module.ts:10` |
| `/eventos/detail/view/:id` | `EventoCreateComponent` | idem | `breadcrumb: 'Controle'`, `action: 'view'` | nenhum | `evento-routing.module.ts:11` |
| `/eventos/**` | redireciona para `/notfound` (rota que **não existe**) | idem | — | — | `evento-routing.module.ts:12` |
| `/evento-pessoa/principal` | `EventoPessoaPrincipalComponent` | idem | — | nenhum (o componente redireciona os perfis de secretaria) | `evento-pessoa-routing.module.ts:8`; duplicada em `administracao.routing.ts:61-64` |
| `/evento-pessoa/:id` | `EventoPessoaComponent` | idem | — | nenhum | `administracao.routing.ts:27-36`; `evento-pessoa-routing.module.ts:9` |
| `/regras-legenda/:eventoId` | `ConfiguracaoLegendasEventoComponent` | idem | `breadcrumb: 'Configuração de Legendas'` | nenhum | `administracao.routing.ts:37-46`; `legendas-routing.module.ts:15` |
| `/catalogo-legendas` | `CatalogoLegendasComponent` (aceita *query* `eventoId`) | idem | `breadcrumb: 'Catálogo de Legendas'` | nenhum | `administracao.routing.ts:47-56`; `legendas-routing.module.ts:13` |
| `/regras-legenda` (sem id) | `CatalogoLegendasComponent` — efeito do array de rotas compartilhado | idem | idem | nenhum | `legendas-routing.module.ts:7-16` |
| `/catalogo-legendas/:eventoId` | `ConfiguracaoLegendasEventoComponent` — idem | idem | idem | nenhum | `legendas-routing.module.ts:7-16` |
| `/nao-ha-principal` | `NaoHaPrincipalComponent` | idem | — | nenhum | `administracao.routing.ts:57-60` |

- Todas as rotas administrativas ficam dentro do *shell* `AdminComponent` (topbar + menu + `router-outlet`) (`admin.routing.ts:6-19`; `admin.component.html:11-15`).
- **Não existe guard de perfil nem `data` de perfis em nenhuma rota.** `AuthGuard` só verifica se há usuário em sessão (`auth-guard.service.ts:11-18`). Qualquer usuário autenticado alcança qualquer rota digitando a URL; o que diferencia perfis é o menu recebido do backend e as checagens pontuais listadas em 2.
- Rota curinga global (`**`): comentada (`app-routing.module.ts:26`).
- Os `breadcrumb` de rota não são exibidos por nenhum template.

---

## 2. Menu e perfis

### 2.1 Menu

- O menu **não é definido no front**: `MenuComponent` monta um `p-menubar` a partir de `auth.menus`, que vem na resposta do login (campo `menus`) e é guardado em `localStorage['menus']` (`admin.component.html:12`; `menu.component.ts:15-18`, `:30-40`; `auth.service.ts:36-37`, `:106`, `:116`).
- Mapeamento de cada item recebido (`menu.component.ts:31-38`): `menu` → rótulo; `icone` → classe `fa fa-fw {icone}`; `urlPagina` → `routerLink` `/{urlPagina}`; `subMenus` → subitens (recursivo); `visible` sempre `true`.
- **Rótulos literais dos itens de menu, ordem e perfis que enxergam cada item: não encontrado no front** (são dados do backend/serviço corporativo). O front não filtra itens de menu por perfil.
- Layout: menu horizontal fixo (`layoutMode = MenuOrientation.HORIZONTAL` — `admin.component.ts:25`).

### 2.2 Como o perfil é obtido

- `auth.usuario.perfil` (texto com o **nome** do perfil), vindo do objeto `usuario` da resposta do login e persistido em `localStorage['usuario']` (`auth.service.ts:33-35`, `:105`, `:115`). É exibido no menu suspenso do usuário ("Perfil: ") (`topbar.component.html:36-41`).
- **Não há enum nem constante de perfis de acesso no front**; as comparações são feitas com textos literais espalhados pelo código.
- Nomes literais comparados: `'Administrador'`, `'Gestor'`, `'Secretaria Mesa'`, `'Secretaria Check-In'` (no login também escrito `"Secretaria Check-In"`), e `'MASTER DN'` (sobra — ver 8).
- Códigos de perfil: na manutenção de usuários a lista de perfis do serviço corporativo é filtrada pelos ids **`"SMC.1"`, `"SMC.2"`, `"SMC.5"`** (`usuarios-filter.component.ts:75`; `usuario.component.ts:120`). A correspondência entre esses ids e os nomes (Administrador / Secretaria Mesa / Secretaria Check-In / Gestor): **não encontrado no front**.
- O enum `TipoPerfil` (`DN`, `DR`, `UA` — `tipo-perfil.enum.ts:1-5`) é o **tipo de abrangência** do perfil (`perfilAcesso.tipo`), usado só em "Instituições Relacionadas" (4.3); não representa os perfis do sistema.

### 2.3 Todas as checagens de perfil encontradas (`.ts` e `.html`)

| # | Local | Expressão | Efeito | Ref. |
|---|---|---|---|---|
| 1 | Login | `res.usuario.perfil == "Secretaria Mesa" \|\| == "Secretaria Check-In"` | após login, busca o evento principal e vai para `/evento-pessoa/{id}`; demais perfis vão para `/dashboard-simples` | `login.component.ts:68-78` |
| 2 | Rota `/evento-pessoa/principal` | `perfil === 'Secretaria Mesa' \|\| === 'Secretaria Check-In'` | redireciona para `/evento-pessoa/{eventoPrincipalId}` | `evento-pessoa-principal.component.ts:13-19` |
| 3 | Pesquisa de eventos | `perfil === 'Administrador' \|\| perfil === 'Gestor'` | exibe o botão "Adicionar" | `eventos-filter.component.html:71` |
| 4 | Participantes do evento | `isSecretariaMesa = perfil === 'Secretaria Mesa'`; `isSecretariaCheckin = perfil === 'Secretaria Check-In'` | definição das *flags* | `evento-pessoa.component.ts:51-52` |
| 5 | idem | `if (isSecretariaMesa) exibirParticipantes = false` | Secretaria Mesa abre direto no mapa | `evento-pessoa.component.ts:53-54` |
| 6 | idem | `*ngIf="isSecretariaMesa && !loading"` | indicador "Atualização automática ativa" e botão "Atualizar agora" só para Secretaria Mesa | `evento-pessoa.component.html:33` |
| 7 | idem | `@if (!isSecretariaMesa)` | botão "Cadastrar Pessoa" oculto para Secretaria Mesa | `evento-pessoa.component.html:62` |
| 8 | idem | `@if (!isSecretariaMesa && !isSecretariaCheckin)` | botões "Participantes" / "Mapa de Assentos" só para os demais perfis | `evento-pessoa.component.html:75` |
| 9 | idem | `@if (isSecretariaMesa) … @else …` | escolhe `app-mesa-recepcionista-checkin` (Secretaria Mesa) ou `app-mesa` | `evento-pessoa.component.html:118-122` |
| 10 | idem | `if (!isSecretariaCheckin) iniciarRefreshAutomaticoParticipantes()` e `if (isSecretariaCheckin) return` | Secretaria Check-In não tem atualização automática | `evento-pessoa.component.ts:78-80`, `:190` |
| 11 | idem | `isSecretariaCheckin: this.isSecretariaMesa` (parâmetro da consulta) | envia ao backend, sob o nome `isSecretariaCheckin`, se o usuário é Secretaria Mesa | `evento-pessoa.component.ts:106`, `:124` |
| 12 | idem | `if (!isSecretariaCheckin && id)` | após cadastro avulso, recarrega participantes do mapa (não para Secretaria Check-In) | `evento-pessoa.component.ts:156` |
| 13 | Filtro de participantes | `isSecretariaCheckin = perfil === 'Secretaria Check-In'`; `@if (!isSecretariaCheckin)` | oculta os filtros "Temas", "Grupos de Trabalho" e "Cargo" para Secretaria Check-In | `evento-pessoas-filter.component.ts:36`; `evento-pessoas-filter.component.html:42` |
| 14 | Lista de participantes | `isSecretariaCheckin = perfil === 'Secretaria Check-In'`; `isAdministrador = perfil === 'Administrador'` | definição das *flags* | `evento-pessoas-list.component.ts:87-88` |
| 15 | idem | `*ngIf="!isAdministrador"` / `*ngIf="isAdministrador"` | coluna "Confirmado": somente leitura para não administradores; clicável (confirmar / remover confirmação) para Administrador | `evento-pessoas-list.component.html:96`, `:103` |
| 16 | idem | `@if(!isSecretariaCheckin) … @else …` | coluna "Assento": clicável (abre "Gerenciar Legenda da Pessoa") exceto para Secretaria Check-In | `evento-pessoas-list.component.html:153-163` |
| 17 | Serviço de eventos | `isSecretariaCheckin = perfil === 'Secretaria Check-In'` | escolhe o endpoint de check-in: `secretaria/checkin/participante` (Secretaria Check-In) ou `administracao/eventos/participante/checkin` (demais) | `evento.service.ts:56-59` |
| 18 | Componente de ajuda (sobra) | `perfil !== 'MASTER DN'` / `=== 'MASTER DN'` | texto de ajuda somente leitura e botão "Salvar" só para "MASTER DN" | `hint.component.html:2`, `:5` |

Não há nenhuma outra checagem de perfil: os quatro componentes do mapa de assentos, as telas de usuários, pessoas, formulário de evento, lista de eventos (ações por linha), legendas e painel **não testam perfil**.

### 2.4 Resumo por perfil (somente o que o front decide)

| Tela / elemento | Administrador | Gestor | Secretaria Mesa | Secretaria Check-In |
|---|---|---|---|---|
| Destino após login | `/dashboard-simples` | `/dashboard-simples` | `/evento-pessoa/{evento principal}` | `/evento-pessoa/{evento principal}` |
| Botão "Adicionar" em Eventos | sim | sim | não | não |
| Participantes: visão inicial | lista | lista | mapa | lista |
| Alternar lista/mapa | sim | sim | não | não |
| "Cadastrar Pessoa" | sim | sim | não | sim |
| Filtros "Temas", "Grupos de Trabalho", "Cargo" | sim | sim | (não vê a lista) | não |
| Alterar "Confirmado" na lista | sim | não | (não vê a lista) | não |
| Alterar "Check-In" na lista | sim | sim | (não vê a lista) | sim (endpoint `secretaria/checkin/participante`) |
| Clicar em "Assento" (legenda da pessoa) | sim | sim | (não vê a lista) | não |
| Mapa de assentos | edição (`app-mesa`) | edição (`app-mesa`) | leitura + "Atender" (`app-mesa-recepcionista-checkin`) | não acessa pelo botão |
| Atualização automática (3 s) | sim | sim | sim (com indicador) | não |

"Gestor" e qualquer outro perfil caem no ramo "demais perfis" de todas as checagens, exceto a #3 e a #15. Demais telas (usuários, pessoas, legendas, ações da lista de eventos): sem distinção de perfil no front — dependem só do menu e do backend.

---

## 3. Autenticação

### 3.1 Inicialização e descoberta de serviços (pré-requisito de todas as telas)

- `ServicosGuard` roda antes das rotas de autenticação e das rotas administrativas (`app-routing.module.ts:14`, `app-routing.module.ts:20`). Ele dispara duas chamadas e só libera a rota quando ambas respondem; em erro resolve `false` (rota bloqueada, sem mensagem) (`servicos-guard.service.ts:13-27`).
  - `GET {baseUrl}servicos/corporativo` → resposta guardada em `ServicosService.urls` (`servicos.service.ts:33-40`). É o catálogo de URLs do **serviço corporativo externo**; o front só usa as chaves, os valores vêm do backend. Chaves lidas no front: `urlAutenticacaoSistemaV2` (`auth.service.ts:42`), `urlAlteracaoSenha` (`auth.service.ts:77`), `urlRecuperacaoSenha` (`auth.service.ts:97`), `urlPesquisaUsuarios` (`auth.service.ts:86`, `:92`), `urlPesquisaUsuarioLogin` (`usuario.service.ts:16`), `urlPesquisaUsuarioSistemaCodigoUsuario` (`usuario.service.ts:29`, `:34`), `urlPesquisaUsuariosSistema` (`usuario.service.ts:53`, `usuario-acesso.service.ts:11`), `urlNovoUsuarioSistema` (`http-crud.service.ts:38`), `urlAtualizaUsuarioSistema` (`http-crud.service.ts:43`, `:53`), `urlPerfisSistema` (`perfis-acesso.service.ts:11`), `urlEntidadesSistema` (`entidade.service.ts:17`), `urlDepartamentosSistema` (`departamento-regional.service.ts:39`), `urlUnidadesSistema` (`unidade.service.ts:47`), `urlNotificacoesSistema` (`mensagens.service.ts:14`, `notificacao.service.ts:13`).
  - `GET {baseUrl}servicos/privado` → resposta guardada em `ServicosService.modulos` (`servicos.service.ts:49-56`). Chaves lidas: `cliente_id` e `cliente_secret` (`auth.service.ts:43-44`), `administracao` (`usuario.service.ts:12`, `hint.service.ts:14`, serviços `cached/*`), `projeto` (`usuario.service.ts:83`).
- `baseUrl` por ambiente: local `http://localhost:8080/api-mesa-checkin/` (`environment.ts:3`); desenvolvimento `https://sistema-mesa.dev.sistemaindustria.com.br/api-mesa-checkin/` (`environment.development.ts:4`); homologação `https://sistema-mesa.hml.sistemaindustria.com.br/api-mesa-checkin/` (`environment.homolog.ts:4`); docker `app_base_url` (placeholder, `environment.docker.ts:3`). Ambiente de produção: não encontrado no front (não existe `environment.prod.ts` em `src/environments`).
- `TokenInterceptor` (registrado em `main.ts:37`) acrescenta `Authorization: Bearer {access_token}` e `Content-Type` em toda requisição (`interceptor.service.ts:81-103`). `Content-Type`: `application/json` quando a requisição não define o cabeçalho; `application/x-www-form-urlencoded` quando define qualquer outro valor; `multipart/form-data` quando define exatamente esse valor (`interceptor.service.ts:66-79`).
- Tratamento global de erro HTTP: status `401` → `AuthService.logout()` (limpa sessão e vai para `/login`) e repropaga o erro (`interceptor.service.ts:36-39`, `:148-151`); status `400` com `error.error.error === 'invalid_grant'` → logout (`interceptor.service.ts:40-41`, `:135-146`); demais → repropaga.
- Renovação de token: `handleTokenExpired` existe mas a chamada está comentada (`interceptor.service.ts:37`, `:105-133`); `AuthService.refreshToken()` usa `this.urlAutenticacaoSistema`, que nunca recebe valor (`auth.service.ts:21`, `:63-74`). Não há renovação de token em uso.

### 3.2 Moldura das telas de autenticação

- Componente `AuthComponent` envolve `/login`, `/alterar-senha` e `/recuperar-senha` (`auth.routing.ts:9-27`).
- Texto fixo: "Seja bem-vindo(a) ao Portal de Gestão de Participantes em Eventos!" (`auth.component.html:6`) e "Faça o login para acessar." (`auth.component.html:10`). Imagens de rodapé e imagem lateral `tela_inicial.png` (`auth.component.html:16-18`, `:25`).

### 3.3 Login — rota `/login` (`auth.routing.ts:14-15`)

| Campo (rótulo literal) | Controle | Obrigatório | Validador / mensagem | Ref. |
|---|---|---|---|---|
| "Usuário" | `input` texto (`formControlName="login"`) | Sim | `BasicValidators.required` → "Campo obrigatório." | `login.component.html:9-17`, `login.component.ts:50`, `basic-validators.ts:180-188` |
| "Senha" | `p-password` com `toggleMask` (olho) e sem medidor de força (`[feedback]="false"`) | Sim | `BasicValidators.password` → vazio: "Senha obrigatória"; menos de 8 caracteres: "A sua senha deve ter mais de 8 caracteres." (a checagem é `length < 8`, ou seja, 8 caracteres passam) | `login.component.html:20-26`, `login.component.ts:51`, `basic-validators.ts:120-131` |
| (sem rótulo) `lembrar` | controle de formulário sem elemento na tela, valor padrão `true` | — | — | `login.component.ts:52` |

- maxlength/máscara: não encontrado no front.
- Link "Esqueceu a senha?" → `/recuperar-senha` (`login.component.html:29`).
- Botão "Entrar" (submit) (`login.component.html:32`) → `LoginComponent.login()` (`login.component.ts:56-89`): limpa erros, marca campos como tocados e, se válido, chama `AuthService.login(login, senha, lembrar)`.
- `AuthService.login` (`auth.service.ts:47-56`): `POST` para `servicos.urls.urlAutenticacaoSistemaV2` (serviço corporativo) com corpo `{ informacoes: <base64> }`, em que o valor é `btoa( btoa(cliente_id) : btoa(login) : btoa(cliente_secret) : btoa("password") : btoa(senha) )` (`auth.service.ts:58-61`). `cliente_id`/`cliente_secret` vêm de `servicos/privado` (`auth.service.ts:43-44`).
- Em sucesso, `configurarSessao(res, true)` (`auth.service.ts:53`) — o segundo argumento é o literal `true`, então a sessão é **sempre** persistida em `localStorage`, independentemente do controle `lembrar`. Chaves gravadas: `access_token`, `token_type`, `expires_in`, `refresh_token`, `usuario` (JSON), `menus` (JSON) (`auth.service.ts:104-124`). Da resposta são usados `usuario`, `menus`, `access_token`.
- Redirecionamento pós-login (`login.component.ts:67-78`):
  - se `res.usuario.perfil == "Secretaria Mesa"` ou `== "Secretaria Check-In"` → `GET {baseUrl}administracao/eventos/evento-principal`; grava `localStorage['eventoPrincipalId'] = JSON.stringify(res.id)` e, se houver resposta, navega para `/evento-pessoa/{id}` (`login.component.ts:68-75`). Não há tratamento para erro dessa chamada nem para resposta vazia (o usuário permanece na tela de login).
  - caso contrário → `/dashboard-simples` (`login.component.ts:77`).
- Erro (`login.component.ts:80-86`): `handleError` → toast `severity: 'error'`, `summary: 'Erro'`, `detail: error.error.detalhe` ou, na falta dele, "Serviço indisponível." (`page-base.ts:92-108`). Toast renderizado por `<p-toast />` (`login.component.html:6`).
- **Primeiro acesso / troca obrigatória de senha**: detectado por `err.status === 302` na resposta do login (`login.component.ts:91-93`). Nesse caso grava `auth.alteracaoSenha = { login, senhaAtual: senha }` (`login.component.ts:95-100`) e navega para `/alterar-senha` (`login.component.ts:84`).

### 3.4 Alterar senha — rota `/alterar-senha` (`auth.routing.ts:17-21`)

- Guard `AlterarSenhaGuard`: libera se `auth.alteracaoSenha.login` estiver preenchido (fluxo de troca obrigatória) **ou** se houver usuário logado (`auth.usuario`); senão navega para `/login` (`alterar-senha-guard.ts:12-18`).
- Aberta por dois caminhos: (a) troca obrigatória vinda do login (3.3); (b) item "Alterar Senha" do menu suspenso do usuário (`topbar.component.html:54-59`).
- "Troca obrigatória" = `auth.alteracaoSenha.senhaAtual` preenchido (`alterar-senha.component.ts:80-82`).

| Campo (rótulo literal) | Controle | Exibição | Validador / mensagem | Ref. |
|---|---|---|---|---|
| "Senha Atual" | `input type="password"` | só quando **não** é troca obrigatória (`*ngIf="!alteracaoObrigatoria"`); na troca obrigatória o controle fica oculto e pré-preenchido com a senha digitada no login | `BasicValidators.password` ("Senha obrigatória" / "A sua senha deve ter mais de 8 caracteres.") | `alterar-senha.component.html:11-19`, `alterar-senha.component.ts:43` |
| "Nova Senha" | `input type="password"` | sempre | `BasicValidators.password` | `alterar-senha.component.html:22-30`, `alterar-senha.component.ts:44` |
| "Confirme a Nova Senha" | `input type="password"` | sempre | `BasicValidators.password`; validador de grupo `passwordsShouldMatch` → "As senhas não conferem." | `alterar-senha.component.html:31-42`, `alterar-senha.component.ts:45-47`, `basic-validators.ts:133-143` |

- Aviso de troca obrigatória: `<p-message>{{alterarSenhaAlerta}}</p-message>` exibido quando `alteracaoObrigatoria` (`alterar-senha.component.html:3-5`). `alterarSenhaAlerta` é um array de objeto com `summary: 'Alteração de senha obrigatória!'` e `detail: 'Para continuar altere a sua senha.'` (`alterar-senha.component.ts:28-32`) interpolado diretamente — ver Suspeitas.
- Botão "Alterar Senha" (`alterar-senha.component.html:44`) → `alterarSenha()` (`alterar-senha.component.ts:54-65`): valida; `AuthService.alterarSenha(form.value, login)` = `PUT servicos.urls.urlAlteracaoSenha` com `{login}` substituído, corpo `{senhaAtual, senhaNova, confirmaSenha}` (`auth.service.ts:76-82`). O login usado é `auth.alteracaoSenha.login` ou `auth.usuario.login` (`alterar-senha.component.ts:67-69`).
- Em sucesso: faz login automático com a nova senha e navega para `/dashboard-simples` (`alterar-senha.component.ts:60`, `:71-78`) — para qualquer perfil (não há o desvio por perfil que existe no login).
- Erro: `handleError` (toast "Erro" + detalhe ou "Serviço indisponível.") — porém o template não tem `<p-toast>`; tem `<p-message>{{error}}</p-message>` (`alterar-senha.component.html:6-8`).
- Botão "Voltar" → `/login` (`alterar-senha.component.html:47`).

### 3.5 Esqueci minha senha / Recuperar senha — rota `/recuperar-senha` (`auth.routing.ts:22-25`)

- Sem guard próprio. Aberta pelo link "Esqueceu a senha?" do login.
- Mensagem informativa fixa: "Digite seu login e uma senha temporária será enviada para redefinir a sua senha" (`recuperar-senha.component.html:7`).
- Campo "Usuário" (`input` texto, `formControlName="login"`, `size="30"`), `BasicValidators.required` → "Campo obrigatório." (`recuperar-senha.component.html:13-24`, `RecuperarSenhaComponent.ts:39-43`).
- Botão "Recuperar senha" (`recuperar-senha.component.html:26`) → `recuperarSenha()` (`RecuperarSenhaComponent.ts:48-56`): **não** chama `validateForm()` nem testa `form.valid`; chama direto `AuthService.recuperarSenha(login)` = `POST servicos.urls.urlRecuperacaoSenha` com `{login}` substituído, corpo `null`, cabeçalho `application/x-www-form-urlencoded` (`auth.service.ts:96-102`).
- Sucesso: toast de sucesso "Senha temporária enviada." e navega para `/login` (`RecuperarSenhaComponent.ts:51-52`). Erro: `handleError` (toast "Erro").
- Botão "Voltar" → `/login` (`recuperar-senha.component.html:27`).

### 3.6 Logout

- Item "Logout" do menu suspenso do usuário (`topbar.component.html:60-65`) → `TopbarComponent.logout()`: navega para `/login` e chama `AuthService.logout()` (`topbar.component.ts:113-116`).
- `AuthService.logout()` remove de `localStorage`: `access_token`, `token_type`, `expires_in`, `refresh_token`, `usuario`, `menus`, e navega para `/login` (`auth.service.ts:126-134`). Não chama endpoint. Não remove `eventoPrincipalId` nem zera as propriedades em memória `usuario`/`access_token`/`menus` (ver Suspeitas).
- Logout automático: `AuthGuard` sem usuário (`auth-guard.service.ts:11-18`); resposta `401`; resposta `400 invalid_grant` (3.1).
- `AdminComponent.logout()` (`admin.component.ts:165-168`) e `ProfileComponent.logout()` (`profile.component.ts:42-45`) existem mas não são acionados por nenhum template em uso (ver Suspeitas).

### 3.7 Dados do usuário no menu suspenso (topbar)

- Cabeçalho da aplicação: título `nomeSistema = 'Gestão de Participantes em Eventos'` (`topbar.component.ts:24`, `topbar.component.html:5`).
- Gatilho: foto (`img#fotoUsuario`) + nome do usuário `auth.usuario.nome` (`topbar.component.html:18-21`).
- Itens do menu suspenso, na ordem (`topbar.component.html:23-66`): "Nome: " `auth.usuario.nome`; "Login: " `auth.usuario.login`; "Perfil: " `auth.usuario.perfil`; "Email: " `auth.usuario.email`; "Alterar Foto do Perfil"; "Alterar Senha" (→ `/alterar-senha`); "Logout".
- Os dados vêm do objeto `usuario` da resposta do login guardado em `localStorage` (`auth.service.ts:33-39`, `:105`). Não há chamada de consulta de dados do usuário além da foto.

### 3.8 Foto de perfil

- Ao iniciar o topbar: `AuthService.buscarImagemUsuario()` = `GET servicos.urls.urlPesquisaUsuarios + usuario.id + '/foto'` (`topbar.component.ts:38-40`, `:96-107`; `auth.service.ts:90-94`). A propriedade `foto` da resposta é aplicada como `src` de `img#fotoUsuario` (`topbar.component.ts:66-81`). Erro → toast de erro com `err.error.detalhe` ou "Serviço indisponível" (`topbar.component.ts:104`).
- "Alterar Foto do Perfil" (`topbar.component.html:48-53`) → `showModalCrop()` faz `showCrop = true` e chama `crop(fotoUsuario)` (`topbar.component.ts:42-45`). **O template do topbar não contém diálogo, `p-fileUpload`, elemento `#imagemCrop` nem botão de salvar** (`topbar.component.html:1-70`), embora `Dialog`, `FileUpload` e `Croppie` estejam importados (`topbar.component.ts:7-12`). Logo, na tela, clicar no item não abre nada.
- Código existente mas inalcançável pela tela: `select(files, fileUpload)` lê o arquivo como DataURL (`topbar.component.ts:47-64`); `salvarImagem()` = `AuthService.alterarImagem({foto: imagemBase64})` → `PUT servicos.urls.urlPesquisaUsuarios + usuario.id + '/foto'` (`topbar.component.ts:83-93`, `auth.service.ts:84-88`), sucesso "Foto Alterada", erro `err.error.detalhe` ou "Serviço indisponível".

---

## 4. Telas, uma a uma

### 4.0 Comportamentos comuns a várias telas

**Moldura da área logada** (`admin.component.html:11-15`): topbar com o título "Gestão de Participantes em Eventos" e o menu suspenso do usuário (3.7); menu horizontal (2.1); área de conteúdo. Rodapé: não há (o `FooterComponent` existe mas não é usado).

**Mensagens (toasts)**: emitidas pelo `MessageService` do PrimeNG via `AlertaService` (`showSuccess`/`showInfo`/`showWarn`/`showError` — `alerta.service.ts:20-38`) ou diretamente. Quando o detalhe não é informado, o `AlertaService` envia o texto literal `&nbsp;` como detalhe (`alerta.service.ts:13`, `:20`). Só aparecem em telas cujo template contém `<p-toast>`.

**Tratamento de erro `handleErrorAlert`** (`page-base.ts:14-24`) — usado pela maioria das telas herdadas de `PageBase`/`FormBase`/`ListBase`:
1. se a resposta tem `error.detalhe` → toast de erro com resumo "Erro Interno" e detalhe = `detalhe`;
2. senão, se tem `error.erros` → "Erro Interno" e detalhe = mensagens (`mensagem` de cada item) seguidas de `&nbsp;`;
3. senão → mensagem genérica pelo status HTTP (`page-base.ts:26-64`): 400 "Requisição inválida."; 401 "Não autorizado."; 403 "Proibido."; 404 "Dados não encontrados."; 408 "Tempo de requisição esgotou."; 429 "Excesso de requisição."; 500 "Erro interno do servidor."; 502 "Bad Gateway."; 503 "Serviço indisponível."; outros "Serviço indisponível.". Severidade sempre `error` (`page-base.ts:66-90`).

**Tratamento de erro `handleError`** (`page-base.ts:92-108`) — usado nas telas de autenticação e em parte do formulário de usuário: toast `error`, resumo "Erro", detalhe `error.error.detalhe` ou "Serviço indisponível.".

**Formato de erro esperado do backend** (deduzido do que o front lê): `{ detalhe, titulo, erros: [{ mensagem }] }`; na remoção de pessoa também `{ code, message }` (`pessoas-list.component.ts:155-164`).

**Mensagens de validação**
- Formulários baseados em `BasicValidators` + `getErrors()` (login, senha, usuários): mostra `errors.invalid` ou, se não houver essa chave, "Campo obrigatório." — só depois de o campo ser tocado/alterado (`form-component-base.ts:61-77`).
- Formulários baseados em `Validators` do Angular + `CadastroHelper` (pessoa, evento, cadastro avulso, bloco de legenda): "Este campo é obrigatório", "Mínimo de {n} caracteres", "Máximo de {n} caracteres", "Valor mínimo é {n}", "Valor máximo é {n}" (`cadastro-helper.ts:9-23`).

**Paginação no servidor** (`PageHelper.findPage` — `page-helper.ts:36-61`): `GET {baseUrl}{endpoint}` com `rows`, `sort`, `direction`, `first` + cada chave do filtro; resposta no formato de página (`content`, `totalElements`, …). Usada em pessoas, eventos, tipos de evento, tipos de mesa e catálogo de legendas. A lista de participantes usa parâmetros próprios (`first`, `size`, `sortField`, `sortOrder` — 4.14).

**Arquivos** (fotos, anexos, planilhas): sempre enviados dentro do JSON como `{ id?, nome, mime, tamanho, conteudo }` com `conteudo` em base64 (`arquivo.interface.ts:3-9`); `mime` vazio vira `application/octet-stream`. Limite de tamanho declarado nos componentes de upload: 209715200 bytes.

**Componente de ajuda `app-hint`** (`hint.component.*`): está incluído nos templates de usuários, pessoas e participantes do evento, mas só é acionado pelos botões de ajuda de "Instituições Relacionadas" (4.3). Abre um painel com um `textarea` (somente leitura, exceto para o perfil `'MASTER DN'`) e botão "Salvar" (só `'MASTER DN'`); consulta `GET {modulos.administracao}/api/ajudas/{id}`; mensagens "Não há uma descrição de ajuda para esse campo. Essa é a hora!" e "Dica atualizada." (`hint.component.ts:73-124`). Tratado como sobra (ver 8).

**Calendário**: textos em português definidos em `FormComponentBase.pt` (`form-component-base.ts:10-53`) e, globalmente, só "Hoje" e "Limpar" (`main.ts:58-61`).

### 4.1 Painel / dashboard — rota `/dashboard-simples`

- Rota `dashboard-simples` → `PainelComponent` (`painel.routing.ts:4-7`); é o destino do redirect da rota vazia (`app-routing.module.ts:7-9`).
- Conteúdo integral da tela (`painel.component.html:2-5`): título `<h2>` com `nomeProjeto` = "Gestão de Participantes em Eventos" (`painel.component.ts:10`) e o parágrafo "Seja bem-vindo ao Gestão de Participantes em Eventos" (literal no template: `Seja bem-vindo ao {{nomeProjeto}}`).
- Campos, tabelas, gráficos, indicadores, chamadas HTTP: **não encontrado no front** (o componente não tem lógica — `painel.component.ts:9-16`).

### 4.2 Usuários — pesquisa — rota `/administracao-usuarios` (`usuarios.routing.ts:6-9`)

Composição: `UsuariosComponent` hospeda `app-usuarios-filter` e `app-usuarios-list`; o filtro emite `(filtro)` e a página repassa o valor para a lista (`usuarios.component.html:5-8`, `usuarios.component.ts:36-38`).

**Título**: `<h1>Usuários</h1>` (`usuarios-filter.component.html:4`).

**Campos do filtro** (nenhum obrigatório, sem validadores — `usuarios-filter.component.ts:145-155`):

| Rótulo literal | Controle | Lista / origem | Observações | Ref. |
|---|---|---|---|---|
| "Entidade" | `p-dropdown`, `showClear`, placeholder "Selecione", `emptyMessage` "Nenhum resultado encontrado" | `EntidadeService.listarDropdownCodigo()` → `GET servicos.urls.urlEntidadesSistema`; rótulo `nome` ou `descricao`; valor `codigo` (`entidade.service.ts:24-27`, `http.service.ts:15-17`, `:36-43`) | `(onChange)="listarDepartamentosRegionais()"` é chamado **sem argumento**, então `codigoEntidade` é `undefined` e a lista de DR nunca é carregada (`usuarios-filter.component.html:16`, `usuarios-filter.component.ts:94-113`) | `usuarios-filter.component.html:8-23` |
| "Departamento Regional" | `p-dropdown`, `showClear`, placeholder "Selecione" | `DepartamentoRegionalService.listar(codigoEntidade)` → `GET servicos.urls.urlDepartamentosSistema` com `{codigoEntidade}` e parâmetro `data=<timestamp>` (`departamento-regional.service.ts:38-46`) | Só é renderizado se `departamentosRegionais` for *truthy* (`*ngIf`); começa `undefined` e vira `[]` na primeira troca de entidade (`usuarios-filter.component.ts:140-143`), portanto aparece vazio | `usuarios-filter.component.html:24-40` |
| "Perfil" | `p-dropdown`, `showClear`, placeholder "Selecione" | `PerfisAcessoService.listarDropdown()` → `GET servicos.urls.urlPerfisSistema`; rótulo `nome` ou `descricao`; valor = objeto do perfil; **filtrado no front para os ids `"SMC.2"`, `"SMC.1"`, `"SMC.5"`** (`usuarios-filter.component.ts:72-81`) | — | `usuarios-filter.component.html:43-58` |
| "Nome" | `input` texto | — | — | `usuarios-filter.component.html:60-71` |
| "Login" | `input` texto | — | — | `usuarios-filter.component.html:72-83` |

Controles do formulário sem elemento na tela: `unidade`, `area` (`usuarios-filter.component.ts:149-150`).

**Botões do filtro** (`usuarios-filter.component.html:84-106`): "Pesquisar" (submit → `filtrar()` emite o valor do formulário); "Limpar" (`limpar()` → `form.reset()` e emite); "Adicionar" (`routerLink="/administracao-usuario"`).

**Lista** — legenda da tabela: "Lista de Usuários" (`usuarios-list.component.html:21`).

- Carga: `UsuarioAcessoService.listar2(filtro)` → `GET servicos.urls.urlPesquisaUsuariosSistema` com parâmetros `entidade`, `departamento`, `unidade`, `perfil`, `area`, `nome`, `login` (cada um `''` quando vazio) (`usuario-acesso.service.ts:14-27`). Sem filtro (carga inicial) não envia parâmetros. O filtro do formulário chama-se `departamentoRegional`, mas o serviço lê `filtro.departamento` → o parâmetro `departamento` vai sempre vazio (`usuarios-filter.component.ts:148`, `usuario-acesso.service.ts:19`).
- Antes de enviar, `filtro.perfil` é trocado pelo `id` do perfil (`usuarios-list.component.ts:70-71`); depois da resposta a lista é filtrada **de novo no front** por `item.perfilAcesso?.id === filtro.perfil` (`usuarios-list.component.ts:84-90`).
- Paginação no cliente: 10 linhas por página; paginador só aparece com mais de 10 itens; posição inferior; volta à primeira página a cada pesquisa (`usuarios-list.component.html:13-19`, `usuarios-list.component.ts:74`).
- Ordenação no cliente (`customSort` de `ListBase`, `list-base.ts:143-168`) nas colunas marcadas.

| Coluna (rótulo literal) | Campo | Ordenável | Formato | Ref. |
|---|---|---|---|---|
| (ações) | — | — | botões | `usuarios-list.component.html:47-61` |
| "Nome" | `nome` | Sim | texto | `usuarios-list.component.ts:160` |
| "Login" | `login` | Sim | texto | `:161` |
| "Email" | `email` | Sim | texto | `:162` |
| "Perfil" | `perfilAcesso.nome` | Não | texto | `:163` |
| "Situação" | `ativo` | Não | `true` → "Ativo"; `false` → "Inativo"; outro → vazio (`ativo-inativo-converter.ts:4-12`) | `:164` |
| "Responsável Cadastrado" | `responsavelCadastro.nome` | Não | texto | `:165` |
| "Data Cadastro" | `dataCadastro` | Não | se string com espaço, parte antes do espaço; senão `DD/MM/YYYY` (`date-converter.ts:62-74`) | `:166` |
| "Responsável Atualização" | `responsavelAtualizacao.nome` | Não | texto | `:167` |
| "Data Atualização" | `dataAtualizacao` | Não | idem Data Cadastro | `:168` |

O cabeçalho só é renderizado se houver itens (`usuarios-list.component.html:26`).

**Ações por linha**:
- Botão ícone lápis, `pTooltip="Editar Usuário"` → `/administracao-usuario/{login}` (`usuarios-list.component.html:48-54`).
- Botão ícone lixeira, `pTooltip="Remover Usuário"` → `remover(item.codigo, i)` (`usuarios-list.component.html:55-60`): diálogo de confirmação com cabeçalho "Remover Usuário", mensagem "Deseja remover este usuário?" (`usuarios-list.component.ts:131-138`; `nome` = 'Usuário', `:60`) e botões "Remover" / "Cancelar" (`usuarios-list.component.html:1-6`). Aceite → `UsuarioService.remover(codigo)` = `DELETE servicos.urls.urlAtualizaUsuarioSistema` com `{codigoUsuario}` (`http-crud.service.ts:52-55`); sucesso: toast "Usuário removido com Sucesso" e remove a linha da lista em memória (`usuarios-list.component.ts:140-152`); erro: `handleErrorAlert` (ver 4.0).

**Estado vazio**: "Nenhum usuário encontrado." (`usuarios-list.component.html:81`).

**Código sem uso na tela**: `mudarSituacao()` (PATCH `{modulos.administracao}/api/usuarios/{codigo}` com `{ativo}`; mensagem "Usuário Ativado com Sucesso." / "Usuário Desativado com Sucesso.") e `copiar()` não são chamados pelo template (`usuarios-list.component.ts:104-129`).

### 4.3 Usuário — formulário — rotas `/administracao-usuario` e `/administracao-usuario/:login` (`usuarios.routing.ts:10-17`)

**Título**: `<h2>` "Cadastrar Usuário" ou "Atualizar Usuário" conforme `usuarioCadastrado` (`usuario.component.html:10`).

**Fluxo de entrada (validação do login)**:
1. Sem `:login` na rota: o formulário é resetado e `permitirCadastro = false` — só aparecem o campo "Login" e o botão "Validar Login" (`usuario.component.ts:113-115`, `:283-286`; `usuario.component.html:59`).
2. "Validar Login" (visível quando `!permitirCadastro`, desabilitado sem login) → `cadastrarRoute()` navega para `/administracao-usuario/{login}?novoUsuario={login}` (`usuario.component.html:49-51`, `usuario.component.ts:320-322`).
3. Com `:login`: `UsuarioService.buscarPorLogin(login)` = `GET servicos.urls.urlPesquisaUsuarioLogin` com `{login}` (`usuario.service.ts:15-21`).
   - Sucesso: preenche o formulário com os dados corporativos; se `usuario.interno`, **desabilita** `nome`, `cpf`, `cargo`, `dddTelefone`, `numeroTelefone`, `dddCelular`, `numeroCelular`, `email` (`usuario.component.ts:139-150`); em seguida `UsuarioService.buscarBasi(codigo)` = `GET servicos.urls.urlPesquisaUsuarioSistemaCodigoUsuario` trocando `'{codigoUsuario}/'` pelo código (`usuario.service.ts:28-31`):
     - encontrado e veio de "Validar Login" (`novoUsuario`): toast erro, resumo "Usuário já cadastrado no sistema.", detalhe "O usuário informado já estas no sistema."; `permitirCadastro = false` (`usuario.component.ts:166-174`);
     - encontrado (edição): `usuarioCadastrado = true`, preenche o formulário, `permitirCadastro = true` (`usuario.component.ts:175-178`);
     - erro: `permitirCadastro = true`, `usuarioCadastrado = false`, toast aviso, resumo "Usuário não cadastrado no sistema.", detalhe "O usuário informado não foi encontrado no sistema." (`usuario.component.ts:180-188`).
   - Erro `404`: se o login tiver formato de e-mail (regex em `usuario.component.ts:324-328`) → `permitirCadastro = true` (usuário externo); senão `permitirCadastro = false` e toast aviso "Para usuários internos, o login deve existir no Active Directory.\n Para usuários externos, o login deve ser um e-mail válido." (`usuario.component.ts:126-137`).
   - Outro erro: `handleError` (toast "Erro") e `permitirCadastro = false` (`usuario.component.ts:107-110`).

**Campos**:

| Rótulo literal | Controle | Obrig. | Máscara / tamanho | Validador / mensagem | Habilitação | Ref. |
|---|---|---|---|---|---|---|
| "Login" | `input` texto (`ngModel`, fora do form) | `required` (atributo) | `size="50"` | — | desabilitado quando `permitirCadastro` | `usuario.component.html:32-41` |
| Painel "Dados do Usuário" | | | | | | `:66` |
| "Nome" + `*` | `input` texto | Sim | `size="40"` | `required` → "Campo obrigatório." | desabilitado p/ usuário interno | `:73-82`; `usuario.component.ts:297` |
| "CPF" + `*` | `p-inputMask` | Sim | `999.999.999-99` | `BasicValidators.cpf` → "CPF inválido"; `required` | idem | `:89-98`; `ts:298` |
| "Telefone" | dois `p-inputMask` (DDD + número) | Não | `(99)` e `9999-9999` | — | idem | `:108-124`; `ts:301-302` |
| "Celular" | dois `p-inputMask` (DDD + número) | Não | `(99)` e `99999-9999` | — | idem | `:132-148`; `ts:303-304` |
| "Email" + `*` | `input` texto | Sim | `size="100"` | `required`; `BasicValidators.email` → "Email inválido" | idem | `:158-167`; `ts:308` |
| "Cargo" | `input` texto | Não | — | — | idem | `:172-180`; `ts:300` |
| Painel "Perfil de acesso ao sistema" | | | | | | `:190` |
| "Perfil" + `*` | `p-dropdown`, `showClear`, `dataKey="codigo"`, placeholder "Selecione" | Sim | — | `required` | sempre | `:196-207`; `ts:299` |

- Lista de "Perfil": `PerfisAcessoService.listarDropdown()` → `GET servicos.urls.urlPerfisSistema`, filtrada no front para os ids `"SMC.2"`, `"SMC.1"`, `"SMC.5"` (`usuario.component.ts:118-124`). Os nomes exibidos vêm do serviço (não há rótulo fixo no front).
- Controles sem elemento na tela (enviados no corpo): `codigo`, `login`, `ativo` (padrão `true`), `recebeEmail` (padrão `true`, required), `enviaPreCadastro` (padrão `false`, required), `areas` (`[]`), `entidades`, `linhas` (`[]`), `dataInicioVigenciaAcesso`, `dataFimVigenciaAcesso` (validador `date` "Data inválida - Formato:  dd/mm/aaaa." e validador de grupo "A data de início deve ser menor do que a data de fim.") (`usuario.component.ts:294-317`).

**Subcomponente "Instituições Relacionadas"** (`app-instituicoes-relacionadas`, **em uso** — `usuario.component.html:214-217`):
- Só é renderizado quando o perfil selecionado tem `tipo` (`*ngIf="tipoPerfil"`, `instituicoes-relacionadas.component.html:3`); `tipoPerfil` = `usuario.perfilAcesso.tipo` e segue o enum `TipoPerfil` (`DN`, `DR`, `UA`) (`instituicoes-relacionadas.component.ts:50-65`, `tipo-perfil.enum.ts:1-5`). Trocar para um perfil de outro tipo limpa as instituições selecionadas (`:58-61`).
- Título do painel: "Instituições Relacionadas" (`instituicoes-relacionadas.component.html:10`).
- Campos: "Entidade" (`p-dropdown`, obrigatório, placeholder "Selecione"; `EntidadeService.listarDropdown()` → `GET urlEntidadesSistema`) (`html:15-31`); "Departamento Regional" (`p-dropdown`; visível se tipo `DR` ou `UA`, entidade escolhida e lista carregada; `DepartamentoRegionalService.listarDropdown(codigoEntidade)`) (`html:33-55`, `ts:210-218`); "Unidade" (`p-multiSelect`, placeholder "Selecione"; visível se tipo `UA`, com entidade e DR e lista de unidades não vazia) (`html:57-78`, `ts:220-228`) — a carga de unidades está **comentada** (`ts:193-208`), então o campo nunca aparece.
- Habilitação por tipo (`ts:254-284`): `DN` → só Entidade habilitada, coluna "Entidade"; `DR` → Entidade e Departamento Regional, colunas "Entidade", "Departamento Regional"; `UA` → os três, colunas "Entidade", "Departamento Regional", "Unidade".
- Botão "Adicionar Instituição" (submit) (`html:80-88`) → valida e acrescenta; sem unidades, a lista passa a conter **apenas** o item recém-escolhido (`this.instituicoes = [formValue]`, `ts:118-124`); mensagem informativa "Entidade já selecionada" (`ts:121`). Para `DN`/`DR`, as entidades já escolhidas saem da lista de opções (`ts:132-145`).
- Tabela "Instituições Selecionadas" (`html:91-132`): paginador com 5 linhas quando há mais de 5; coluna de ação com botão lixeira (`remover(i)` — remove da lista em memória e recarrega entidades, `ts:127-130`); estado vazio "Nenhuma instituição selecionada.".
- Botões de ajuda (ícone `fa-info-circle`) ao lado de "Departamento Regional" e "Unidade" abrem o `app-hint` (ver 4.0) (`html:36-42`, `:60-66`).

**Botões do formulário** (`usuario.component.html:19-27`, `:48-54`):
- "Cadastrar Usuário" / "Atualizar Usuário" (desabilitado quando `!permitirCadastro`) → `salvar()`.
- "Cancelar" → `/administracao-usuarios`.
- "Validar Login" (ver fluxo).
- "Limpar" (visível quando `permitirCadastro && !usuarioCadastrado`) → `/administracao-usuario`.

**Salvar** (`usuario.component.ts:195-217`): remove máscara do CPF e dos DDDs; se inválido → marca tudo como tocado e toast erro "Formulário inválido" / "Preencha todos os campos obrigatórios corretamente". Se válido: monta o usuário com `form.getRawValue()`, `login` e `entidades` (lista aninhada entidade → departamentos → unidades, `instituicoes-conversor.service.ts:7-18`); se o perfil escolhido não estiver na lista filtrada, limpa o campo Perfil e revalida (`:202-203`, `:245-255`); senão:
- edição: `PUT servicos.urls.urlAtualizaUsuarioSistema` com `{codigoUsuario}` (`http-crud.service.ts:42-45`) → navega para `/administracao-usuarios` e toast "Usuário Atualizado com Sucesso" (`usuario.component.ts:270-281`);
- inclusão: `POST servicos.urls.urlNovoUsuarioSistema` (`http-crud.service.ts:37-40`) → navega para `/administracao-usuarios` e toast "Usuário Criado com Sucesso" (`usuario.component.ts:257-268`).
- Erro: `handleErrorAlert` + `handleValidationErrors` (este só preenche `validationErrors`, cujo `<p-message>` está comentado — `usuario.component.html:13`, `:17`).

**"Áreas" e "Linhas do usuário" — sobras, não usadas**:
- `AreasComponent` (`app-areas`) e `LinhasUsuarioComponent` (`app-linhas-usuario`) são importados e declarados como `@ViewChild` em `usuario.component.ts:8-9`, `:58-61`, mas **não constam no array `imports` do componente** (`usuario.component.ts:30-44`) **nem no template** (`usuario.component.html`, 223 linhas, sem `app-areas`/`app-linhas-usuario`). Não têm rota. `AdicionarLinhasUsuarioComponent` só é usado por `LinhasUsuarioComponent` (`linhas-usuario.component.html:2`).
- Para registro (não ativos): `AreasComponent` é um `p-pickList` "Áreas de Negócio" × "Áreas do Usuário" com "Campo obrigatório" quando vazio (`areas.component.html:4-16`), carregando `{modulos.administracao}/api/areas-negocio-perfis` (`areas-perfis.service.ts:13-21`). `LinhasUsuarioComponent` é uma tabela "Linha(s) de Apoio Financeiro" com colunas "Modalidade", "Linha de Apoio Financeiro", "Linha de Transferência", "Recebe Email" e botão "Adicionar Linhas" (`linhas-usuario.component.html:4-12`, `linhas-usuario.component.ts:84-91`); o diálogo "Selecionar Linhas de Transferência" carrega `{modulos.administracao}/api/usuarios/modalidade-fomento-linha` (`adicionar-linhas-usuario.component.html:1`, `usuario.service.ts:88-91`). Vocabulário (modalidade, fomento, linha de transferência, apoio financeiro) alheio a mesa/check-in.

### 4.4 Pessoas — pesquisa — rota `/administracao-pessoas` (`pessoas.routing.ts:6-9`)

Composição: `PessoasComponent` com `app-pessoas-filter` e `app-pessoas-list` (`pessoas.component.html:5-8`).

**Título**: `<h1>Pessoas</h1>` (`pessoas-filter.component.html:5`).

**Campos do filtro** (todos `input` texto, opcionais, sem validador, sem maxlength — `pessoas-filter.component.ts:69-76`):

| Rótulo literal | Controle (`formControlName`) | Ref. |
|---|---|---|
| "Nome" | `nomeCompleto` | `pessoas-filter.component.html:9-19` |
| "CRM" | `crm` | `:22-32` |
| "Razão Social" | `razaoSocial` | `:35-45` |
| "E-mail" | `email` | `:48-58` |

**Botões** (`pessoas-filter.component.html:60-103`): "Pesquisar" (submit → emite filtro); "Limpar" (reset e pesquisa); "Adicionar" (→ `/administracao-pessoa`); "Carga de GT" (abre diálogo 4.6); "Carga de Temas" (abre 4.7); "Carga de Histórico" (abre 4.8). Nenhuma condição de perfil.

**Lista** — legenda "Lista de Pessoas" (`pessoas-list.component.html:32`).

- Carga paginada no servidor (`[lazy]="true"`): `PageHelper.findPage` → `GET {baseUrl}administracao/pessoas` com parâmetros `rows`, `sort=nomeCompleto`, `direction=asc`, `first` e cada campo do filtro (inclusive nulos) (`pessoas-list.component.ts:97-120`, `page-helper.ts:36-61`). A ordenação enviada é sempre fixa em `nomeCompleto asc`, mesmo que o usuário clique em outra coluna (o evento de ordenação só dispara nova chamada com os mesmos `sort`/`direction`).
- 10 linhas por página; paginador sempre visível, embaixo; relatório de página "[{first} a {last} de {totalRecords}]"; indicador de carregamento (`pessoas-list.component.html:14-30`).
- Resposta esperada no formato `Page` (`content`, `totalElements` — `page-helper.ts:5-32`).
- Erro de carga: só `console.error` (sem mensagem ao usuário) (`pessoas-list.component.ts:115-118`).

| Coluna (rótulo literal) | Campo | Ordenável (ícone) | Formato | Ref. |
|---|---|---|---|---|
| (ações) | — | — | botões | `pessoas-list.component.html:58-72` |
| "Nome" | `nomeCompleto` | Sim | texto | `pessoas-list.component.ts:181-186` |
| "Email" | `email` | Sim | texto | `:187-193` |
| "Codinome" | `codinome` | Sim | texto | `:194-200` |
| "CRM" | `crm` | Sim | texto | `:201-207` |
| "Razão Social" | `razaoSocial` | Sim | texto | `:208-214` |
| "Cargo" | `cargo` | Sim | texto | `:215-221` |
| "Data de Criação" | `dataCriacao` | Não | data sem hora (`DateStringWithoutTimeConverter`) | `:222-229` |

**Ações por linha**:
- Lápis, `pTooltip="Editar Pessoa"` → `/administracao-pessoa/{id}` (`pessoas-list.component.html:59-65`).
- Lixeira, `pTooltip="Remover Pessoa"` → `remover(item)` (`:66-71`): confirmação pelo `confirm()` nativo do navegador com o texto "Tem certeza que deseja remover a pessoa? Essa operação não poderá ser desfeita." (`pessoas-list.component.ts:129-134`); `DELETE {baseUrl}administracao/pessoas/{id}` (`form-helper.ts:75-83`).
  - Sucesso: toast sucesso, resumo "Sucesso", detalhe "Pessoa removido com sucesso"; recarrega a lista com `first: 0, rows: 100` (`pessoas-list.component.ts:140-152`).
  - Erro `409` com `error.code === 'PESSOA_COM_VINCULO_EVENTO'`: toast aviso, resumo "Não é possível remover", detalhe `error.error.message` ou "Pessoa possui vínculo com evento." (`:155-167`).
  - Outro erro: toast erro, resumo "Erro ao remover pessoa", detalhe "Contate o administrador do sistema." (`:168-173`).
- O `p-confirmDialog` "Remover Pessoa" com botões "Remover"/"Cancelar" está no template (`pessoas-list.component.html:1-6`) mas não é acionado (a remoção usa `confirm()` nativo).

**Estado vazio**: "Nenhuma pessoa encontrada." (`pessoas-list.component.html:92`).

### 4.5 Pessoa — formulário — rotas `/administracao-pessoa` e `/administracao-pessoa/:id` (`pessoas.routing.ts:10-17`)

**Título**: "Cadastrar Pessoa" (`<h1>`, só na inclusão — `pessoa.component.html:6-8`). Na edição, em vez do título aparece o cabeçalho de perfil: foto (se `anexo.id` e `anexo.mime` existirem) ou avatar com as iniciais (primeiras letras das duas primeiras palavras do nome, em maiúsculas — `pessoa.component.ts:257-266`) e o nome completo (`pessoa.component.html:10-28`).

**Carga na edição**: `GET {baseUrl}administracao/pessoas/{id}` (`pessoa.component.ts:86-102`, `form-helper.ts:34-42`); se houver `foto.id`, `PessoaService.findAnexo(id)` = `GET {baseUrl}administracao/pessoas/anexos/{id}` (`pessoa.component.ts:185-186`, `:206-208`; `pessoa.service.ts:42-45`).

**Abas** (`pessoa.component.html:36-43`): "Cadastro", "Contatos", "Perfil Corporativo", "Relacionamento", "Histórico". As três primeiras compartilham o mesmo `FormGroup`; as duas últimas são somente leitura.

Mensagens de validação comuns às abas (`cadastro-helper.ts:9-23`): "Este campo é obrigatório"; "Mínimo de {n} caracteres"; "Máximo de {n} caracteres"; "Valor mínimo é {n}"; "Valor máximo é {n}". Contador de caracteres `{n}/{limite}` sob os campos de texto, com classe de alerta acima de 80% e de perigo acima de 95% do limite (`cadastro-helper.ts:26-38`).

**Aba "Cadastro"** (`app-pessoa-cadastro`):

| Rótulo literal | Controle | Obrig. | maxlength / máscara | Validadores | Lista / padrão | Ref. |
|---|---|---|---|---|---|---|
| "Nome" + `*` | `input` texto, placeholder "Digite o nome da pessoa" | Sim | `maxlength="255"` | `required`, `minLength(3)`, `maxLength(255)` | — | `pessoa-cadastro.component.html:8-27`; `pessoa.component.ts:113-120` |
| "Codinome" | `input` texto, placeholder "Digite o codinome da pessoa" | Não | `maxlength="100"` | `maxLength(100)` | — | `html:30-51`; `ts:121-126` |
| "CRM" | `input` texto, placeholder "Digite o CRM da pessoa" | Não | `maxlength="50"` | `maxLength(50)` | — | `html:54-75`; `ts:107-112` |
| "Sexo" | `p-dropdown`, placeholder "Selecione o sexo" | Não | — | — | fixo no front `SEXO_OPTIONS`: "Masculino"=`MASCULINO`, "Feminino"=`FEMININO`, "Não informado"=`NAO_INFORMADO` (`sexo.enum.ts:9-13`) | `html:78-94` |
| "Estado" | `p-dropdown`, placeholder "Selecione o estado" | Não | — | — | fixo no front `ESTADO_OPTIONS` (27 UFs, rótulo = sigla — `estado.enum.ts:3-36`) | `html:97-113` |
| "CPF" | `p-inputMask`, placeholder "Digite o CPF", `[unmask]="true"` | Não | `999.999.999-99` | nenhum (não usa validador de CPF) | — | `html:116-133`; `ts:139` |
| "Foto" | `p-fileUpload` avançado, automático, botão "Adicionar" | Não | aceita `.png,.jpg,.jpeg`; tamanho máx. 209715200 bytes | — | — | `html:136-176` |

- Foto: texto de área vazia "Clique em adicionar ou arraste e solte a foto aqui..."; mensagens "{0}: Tipo de imagem não permitido" / "Tipos permitidos: {0}" / "A imagem selecionada excede o tamanho máximo permitido" / "O tamanho máximo da imagem permitido é {0}" (`html:146-157`). Ao escolher: lê em base64, grava em `form.foto` (`{nome, mime, tamanho, conteudo}`) e mostra "Foto adicionada"; falha de leitura: "Falha ao ler o arquivo." (`pessoa-cadastro.component.ts:77-107`). Com foto: botão com o nome do arquivo (título "Download") e botão lixeira (título "Excluir") → "Anexo removido" (`html:158-173`, `ts:109-130`).
- Somente leitura na edição: "Data de Criação: dd/MM/yyyy HH:mm" e "Data de Alteração: dd/MM/yyyy HH:mm" (`html:178-187`).

**Aba "Contatos"** (`app-pessoa-contato`):

| Rótulo literal | Controle | Obrig. | maxlength / máscara | Validadores | Ref. |
|---|---|---|---|---|---|
| "E-mail" | `input` texto, placeholder "Digite o e-mail" | Não | `maxlength="255"` | nenhum (sem validação de formato) | `pessoa-contato.component.html:8-27`; `pessoa.component.ts:140` |
| "Telefone Principal" | `p-inputMask`, placeholder "Digite o telefone", `[unmask]="true"` | Não | `(99) 99999-9999` | nenhum | `html:32-48` |
| "Celular" | `p-inputMask`, placeholder "Digite o celular", `[unmask]="true"` | Não | `(99) 99999-9999` | nenhum | `html:53-69` |

**Aba "Perfil Corporativo"** (`app-pessoa-empresa`):

| Rótulo literal | Controle | Obrig. | maxlength / máscara | Validadores | Ref. |
|---|---|---|---|---|---|
| "Razão Social" + `*` | `input` texto, placeholder "Digite a razão social" | Sim | 255 | `required`, `maxLength(255)` | `pessoa-empresa.component.html:8-27`; `pessoa.component.ts:145-151` |
| "Nome Fantasia" | `input` texto, placeholder "Digite o nome fantasia" | Não | 255 | `maxLength(255)` | `html:32-51`; `ts:152-157` |
| "Cargo" + `*` | `input` texto, placeholder "Digite o cargo" | Sim | 100 | `required`, `maxLength(100)` | `html:56-75`; `ts:128-133` |
| "Cargo do Cartão" | `input` texto, placeholder "Digite o cargo" | Não | 100 | `maxLength(100)` | `html:80-99`; `ts:134-138` |
| "CNPJ" | `p-inputMask`, placeholder "Digite o CNPJ", `[unmask]="true"` | Não | `99.999.999/9999-99` | nenhum | `html:104-118`; `ts:158` |
| "Estado" | `p-dropdown`, placeholder "Selecione o estado" (controle `estadoEmpresa`) | Não | — | — (lista `ESTADO_OPTIONS`) | `html:124-137` |

**Aba "Relacionamento"** (`app-pessoa-relacionamento`, somente leitura):
- Painel "Temas": para cada tema, `nomeTema` e "Data de Vínculo: dd/MM/yyyy"; vazio: "Nenhum tema vinculado" (`pessoa-relacionamento.component.html:3-18`).
- Painel "Grupos de Trabalho": para cada item, `nomeGrupoTrabalho`, "Papel Desempenhado: {papel}" (ou "Não especificado") e "Data de Vínculo: dd/MM/yyyy"; vazio: "Nenhum grupo de trabalho vinculado" (`html:21-37`).
- Dados vêm de `pessoa.temas` e `pessoa.gruposTrabalho` da mesma chamada de detalhe (`pessoa.component.ts:190-194`). Não há edição desses vínculos na tela (entram só pelas cargas 4.6/4.7).

**Aba "Histórico"** (`app-pessoa-historico`, somente leitura): título "Histórico de Participações"; para cada item "Ano: {ano}" e "Participações: {participacoes}"; vazio: "Nenhum histórico de participação importado" (`pessoa-historico.component.html:3-18`). Dados de `pessoa.historicos` (`pessoa.component.ts:196-197`).

**Rodapé / botões** (`pessoa.component.html:81-106`): texto "Campos com * são obrigatórios"; "Cancelar" → `/administracao-pessoas`; botão principal com rótulo "Criar" (inclusão, ícone `+`) ou "Atualizar" (edição, ícone ✓), **desabilitado enquanto o formulário for inválido**, com estado de carregamento.

**Salvar** (`pessoa.component.ts:210-255`): se válido, monta `form.getRawValue()`, zera `dataCriacao`/`dataAlteracao` e chama `create()` = `POST {baseUrl}administracao/pessoas` (`form-helper.ts:44-52`) — **tanto na inclusão quanto na edição** (o `id` vai no corpo; não há chamada `PUT`).
- Sucesso: toast fixo (`sticky`) sucesso, resumo "Sucesso", detalhe "Pessoa criada com sucesso" (mesma mensagem na edição); recarrega a foto se a resposta trouxer `foto.id`. **Não navega** — permanece na tela.
- Erro: toast erro, resumo "Erro", detalhe "Erro ao salvar pessoa. Verifique os dados e tente novamente.".
- Formulário inválido (o botão fica desabilitado nesse estado; o ramo só é alcançado se o `ngSubmit` do `<form>` disparar — `pessoa.component.html:32-34`): toast erro "Formulário inválido" / "Preencha todos os campos obrigatórios corretamente".

### 4.6 Diálogo "Carga de Grupos Temáticos" (botão "Carga de GT")

- Aberto de `pessoas-filter` (`pessoas-filter.component.html:83-88`, `:106-112`). Modal, arrastável, não redimensionável (`pessoas-carga-gt.component.html:1-9`).
- Título: "Carga de Grupos Temáticos" (`html:12`). Instrução: "A planilha deve conter as colunas Código ou Cód. Contato, Grupos Temáticos e Papel Desempenhado." (`html:19`).
- Upload: `p-fileUpload` avançado/automático; botão "Adicionar"; aceita `.xlsx,.xls`; máx. 209715200 bytes; área vazia "Clique em adicionar ou arraste e solte os arquivos aqui..."; mensagens "{0}: Tipo de arquivo não permitido", "Tipos permitidos: {0}", "O arquivo selecionado excede o tamanho máximo permitido", "O tamanho máximo de arquivo permitido é {0}" (`html:23-41`).
- Ao escolher: lê em base64 e guarda `{nome, mime, tamanho, conteudo}`; toast info "Planilha adicionada" / "Planilha de Grupos de Trabalho adicionada"; falha: aviso "Falha ao ler planilha." / "Falha ao ler planilha de Grupos de Trabalho." (`pessoas-carga-gt.component.ts:66-95`).
- Com arquivo: botão com o nome (título "Download", baixa o próprio arquivo) e lixeira (título "Excluir") → aviso "Planilha removida" / "Planilha de Grupos de Trabalho removida" (`html:42-57`, `ts:97-107`).
- Botão "Enviar" (desabilitado sem arquivo) (`html:63-70`) → `enviarArquivos()` (`ts:119-132`): emite `enviar` (o pai fecha o diálogo e mostra info "Carga em processamento." / "Carga de Grupos Temáticos em processamento." — `pessoas-filter.component.ts:102-105`); `PessoaService.processaCargaGt(anexo)` = `POST {baseUrl}administracao/pessoas/carga/gt` com o objeto do arquivo (`pessoa.service.ts:47-50`).
  - Sucesso: emite `cargaFinalizada` com `{countSucesso, countErro, countExistentes}` (`carga.interface.ts:1-5`) e mostra info "Carga realizada com sucesso."; o pai monta e mostra info com resumo "Grupos de trabalho foram atualizados" e detalhe composto por "{n} grupos de trabalho vinculados", "{n} foram atualizados", "{n} pessoas não foram encontradas", unidos por ", " / " e " e terminado em "." (`pessoas-filter.component.ts:107-127`).
  - Erro: emite `error` com `error.error.detalhe` ou "Erro ao processar a carga de Grupos Temáticos. Verifique o arquivo e tente novamente."; o pai mostra erro com resumo "Erro ao processar carga de Grupos Temáticos" (`ts:126-129`; `pessoas-filter.component.ts:129-131`).
- Fechar o diálogo (X) → `cancelar` (`html:8`).

### 4.7 Diálogo "Carga de Temas"

Idêntico ao 4.6, com estas diferenças (`pessoas-carga-tema.component.html`, `pessoas-carga-tema.component.ts`):
- Título "Carga de Temas" (`html:12`); instrução "A planilha deve conter as colunas Cód. Contato e Tema." (`html:19`).
- Mensagens: "Planilha de Temas adicionada", "Falha ao ler planilha de Temas.", "Planilha de Temas removida" (`ts:86-99`).
- Endpoint: `POST {baseUrl}administracao/pessoas/carga/tema` (`pessoa.service.ts:52-55`).
- Não mostra "Carga realizada com sucesso."; o pai mostra info "Carga em processamento." / "Carga de Temas em processamento." e, ao concluir, resumo "Carga concluída" com detalhe "{n} temas vinculados", "{n} foram atualizados", "{n} pessoas não foram encontradas" (`pessoas-filter.component.ts:133-162`).
- Erro padrão: "Erro ao processar a carga de Temas. Verifique o arquivo e tente novamente."; resumo no pai "Erro ao processar carga de Temas" (`ts:127`; `pessoas-filter.component.ts:138-140`).

### 4.8 Diálogo "Carga de Histórico"

Idêntico ao 4.7 (cópia com troca de texto — verificado por `diff`), com estas diferenças (`pessoas-carga-historico.component.html`, `pessoas-carga-historico.component.ts`):
- Título "Carga de Histórico" (`html:12`); instrução "A planilha deve conter as colunas Cód. Contato e os anos das participações." (`html:19`).
- Mensagens: "Planilha de Histórico adicionada", "Falha ao ler planilha de Histórico.", "Planilha de Histórico removida" (`ts:86-99`).
- Endpoint: `POST {baseUrl}administracao/pessoas/carga/historico` (`pessoa.service.ts:57-60`).
- Pai: info "Carga em processamento." / "Carga de Históricos em processamento."; conclusão "Carga concluída" com "{n} históricos de participação atualizados" e "{n} pessoas não foram encontradas" (sem o trecho de "foram atualizados"); erro com resumo "Erro ao processar carga de Históricos" e padrão "Erro ao processar a carga de Histórico. Verifique o arquivo e tente novamente." (`pessoas-filter.component.ts:164-185`; `ts:127`).

### 4.9 Eventos — pesquisa — rota `/eventos` (`administracao.routing.ts:17-26`, `evento-routing.module.ts:8`)

Composição: `EventosComponent` com `app-eventos-filter` e `app-eventos-list` (`eventos.component.html:4-7`). Dado de rota `breadcrumb: 'Lista'` (não é exibido em nenhum template).

**Título**: `<h1>Eventos</h1>` (`eventos-filter.component.html:4`).

**Campos do filtro** (todos opcionais, valor inicial `''`, sem validador — `eventos-filter.component.ts:59-68`):

| Rótulo literal | Controle | Lista / origem | Ref. |
|---|---|---|---|
| "Nome:" | `input` texto | — | `eventos-filter.component.html:6-13` |
| "Local:" | `input` texto | — | `:14-21` |
| "Tipo de Evento:" | `p-select`, `showClear`, sem seleção automática | `GET {baseUrl}administracao/tipo-eventos` (`first=0`, `rows=10000`, `sort=id`, `direction=desc`); rótulo `nome`, valor `id` (`eventos-filter.component.ts:70-83`) | `:22-32` |
| "Tipo de Mesa:" | `p-select`, `showClear` | `GET {baseUrl}administracao/tipo-mesas` (mesmos parâmetros); rótulo `nome`, valor `id` (`eventos-filter.component.ts:85-98`) | `:33-43` |
| "Data Inicial:" | `p-datePicker` sem hora, formato `dd/mm/yy`, navegador de mês/ano, faixa de anos `1950:2050`, ícone | — | `:44-54` |
| "Data Final:" | idem | — | `:55-65` |

- Datas são enviadas como `yyyy-MM-dd`; nulos viram `''` (`eventos-filter.component.ts:100-124`).
- Não há validação "data inicial ≤ data final" no front.
- Lista fixa `situacao` ("Todos"/"Ativo"/"Inativo") declarada e **não usada** no template (`eventos-filter.component.ts:22-26`).

**Botões** (`eventos-filter.component.html:67-74`): "Pesquisar" (submit); "Limpar" (recria o formulário e emite); **"Adicionar"** → `/eventos/detail`, exibido **somente** se `auth.usuario.perfil === 'Administrador'` ou `=== 'Gestor'` (`:71`).

A pesquisa é disparada automaticamente ao abrir a tela (`eventos-filter.component.ts:41-46`).

**Lista** (sem legenda/título de tabela):
- Carga paginada no servidor: `GET {baseUrl}administracao/eventos` com `rows`, `sort`, `direction`, `first` + campos do filtro (`evento-list.component.ts:79-102`, `page-helper.ts:36-61`). Ordenação padrão `id desc`; ao clicar num cabeçalho, envia o campo e `asc` se `sortOrder === 1`, senão `desc` (`:88-89`).
- 10 linhas por página, paginador sempre visível embaixo (`evento-list.component.html:5-7`).
- Erro de carga: apenas `console.error` (`evento-list.component.ts:97-100`).

| Coluna (rótulo literal) | Campo de ordenação | Conteúdo / formato | Ref. |
|---|---|---|---|
| "Nome" | `nome` | nome + selo "Finalizado" quando a data do evento é anterior a hoje 00:00 (`isEventoPassed`); a linha inteira fica com opacidade reduzida | `evento-list.component.html:20-21`, `:42-51`; `evento-list.component.ts:56-63`, `:148-150` |
| "Data e Horário" | `dataEvento` | `dd/MM/yyyy HH:mm` e, abaixo, texto relativo: "Hoje", "Amanhã", "Ontem", "Em {n} dias", "Há {n} dias" | `html:22-23`, `:52-57`; `ts:152-169` |
| "Local" | `local` | texto | `html:24-25`, `:58-60` |
| "Tipo" | `tipoEvento.nome` | selo com `tipoEvento.nome` | `html:26-28`, `:61-67` |
| "Formato da Mesa" | `tipoMesa.nome` | selo com `tipoMesa.nome` | `html:29-31`, `:68-74` |
| "Nº de Participantes" | `participantes` | número | `html:32-34`, `:75-80` |
| "Principal" | `principal` | "Sim" / "Não" | `html:35-37`, `:81-85` |
| "Ações" | — | ícones | `html:38`, `:86-105` |

**Ações por linha** (ícones com `title`; **nenhuma condição de perfil**):

| `title` literal | Condição | Efeito | Ref. |
|---|---|---|---|
| "Configuração de Legendas" | sempre | navega para `/regras-legenda/{id}` (4.17) | `evento-list.component.html:88-89` |
| "Tornar evento principal" | `!rowData.principal` | `EventosService.atualizarEventoPrincipal(id)` = `POST {baseUrl}administracao/eventos/{id}/principal` (corpo `{}`); sucesso: toast "Evento atualizado" / "O evento principal foi atualizado com sucesso." e recarrega; erro: sem tratamento | `html:90-91`; `evento-list.component.ts:207-219`; `evento.service.ts:83-86` |
| "Este evento é o principal" | `rowData.principal` | só indicador (sem clique) | `html:92-93` |
| "Cargas de Convidados e Confirmados" | sempre | abre o diálogo 4.11 | `html:94-95`; `ts:171-174` |
| "Participantes" | sempre | `window.open('/evento-pessoa/{id}', '_blank')` — abre 4.12 em **nova aba** | `html:96-97`; `ts:181-184` |
| "Visualizar evento" | sempre | `/eventos/detail/view/{id}` | `html:98-99` |
| "Editar evento" | sempre | `/eventos/detail/edit/{id}` | `html:100-101` |
| "Excluir evento" | sempre | `confirm()` nativo: "Tem certeza que deseja remover o evento? Essa operação não poderá ser desfeita."; `DELETE {baseUrl}administracao/eventos/{id}`; sucesso "Sucesso" / "Evento removido com sucesso" e recarrega; erro "Erro ao remover evento" / "Contate o administrador do sistema." | `html:102-103`; `ts:111-145` |

**Estado vazio**: ícone de calendário, "Nenhum evento encontrado" e botão "Criar Primeiro Evento" → `/eventos/detail` (sem condição de perfil) (`evento-list.component.html:108-120`).

### 4.10 Evento — formulário (criar / editar / visualizar)

Rotas (`evento-routing.module.ts:9-11`): `/eventos/detail` (novo), `/eventos/detail/edit/:id` (editar), `/eventos/detail/view/:id` (visualizar — dado de rota `action: 'view'`). O modo somente leitura é definido por `data.action === 'view'` (`evento-create.component.ts:49-56`).

**Título**: "Novo Evento" sem `id`; "Editar Evento" com `id` — **inclusive no modo visualizar** (`evento-create.component.html:7-10`).

**Carga**: com `id`, `GET {baseUrl}administracao/eventos/{id}` (`evento-create.component.ts:65-80`); listas `GET administracao/tipo-eventos` e `GET administracao/tipo-mesas` (`first=0`, `rows=1000`, `sort=id`, `direction=desc`) (`:85-111`).

| Rótulo literal | Controle | Obrig. | maxlength / limites | Validadores | Lista / observações | Ref. |
|---|---|---|---|---|---|---|
| "Nome do Evento" + `*` | `input` texto, placeholder "Digite o nome do evento", contador `n/100` | Sim | 100 | `required`, `minLength(3)`, `maxLength(100)` | — | `html:22-44`; `ts:116-123` |
| "Data e Hora" + `*` | `p-datePicker` com hora (24h), `dd/mm/yy`, placeholder "Selecione a data e hora", barra de botões (Hoje/Limpar) | Sim | — | `required` | sem restrição de data mínima | `html:49-73`; `ts:124` |
| "Local" + `*` | `input` texto, placeholder "Local do evento", contador `n/200` | Sim | 200 | `required`, `minLength(3)`, `maxLength(200)` | — | `html:78-100`; `ts:125-132` |
| "Tipo de Evento" + `*` | `p-select`, placeholder "Selecione o tipo" | Sim | — | `required` | endpoint `administracao/tipo-eventos`; rótulo `nome`; valor = objeto | `html:104-122`; `ts:133` |
| "Tipo de Mesa" + `*` | `p-select`, placeholder "Selecione o tipo" | Sim | — | `required` | endpoint `administracao/tipo-mesas`; rótulo `nome`; valor = objeto (o campo `indicador` decide o desenho da mesa — ver 5) | `html:127-145`; `ts:134` |
| "Participantes" + `*` | `p-inputNumber`, placeholder "Número de participantes" | Sim | mín. 1, máx. 10000 | `required`, `min(1)`, `max(10000)` | — | `html:150-168`; `ts:135-138` |
| "Código da Campanha" | `input` texto, placeholder "Ex.: CMP-03460-L2K8" | Não | 50 | `maxLength(50)` | ajuda: "Código da campanha no CRM usado para importar os inscritos." | `html:173-188`; `ts:139` |
| "Arquivo" | `p-fileUpload` avançado/automático, botão "Adicionar" | Não | `accept="image/*"`, máx. 209715200 bytes | — | ajuda: "Imagem relacionada"; área vazia "Clique em adicionar ou arraste e solte os arquivos aqui..." | `html:193-233` |

- Controles sem elemento na tela: `id`, `arquivo`, `excluido` (padrão `false`), `principal` (`ts:115`, `:140-142`).
- Mensagens de validação: as de `CadastroHelper` (ver 4.5).
- Mensagens do upload: "{0}: Tipo de arquivo não permitido", "Tipos permitidos: {0}", "O arquivo selecionado excede o tamanho máximo permitido", "O tamanho máximo de arquivo permitido é {0}" (`html:202-206`); ao anexar "Anexo adicionado"; falha "Falha ao ler o arquivo."; ao excluir "Anexo removido" (`ts:234-236`, `:267`). Download do anexo salvo: `GET {baseUrl}administracao/eventos/anexos/{id}` (`ts:248-263`, `evento.service.ts:26-29`).
- **Modo visualizar**: cada campo vira texto (`<span>`); data em `dd/MM/yyyy HH:mm`; anexo vira botão de download ou o texto "Nenhuma imagem inserida." (`html:43`, `:72`, `:99`, `:121`, `:144`, `:167`, `:187`, `:234-248`).

**Rodapé / botões** (`html:258-283`): "Campos com * são obrigatórios"; "Cancelar" (ou "Voltar" no modo visualizar) → `/eventos`; "Salvar" (oculto no modo visualizar; desabilitado com formulário inválido; ícone `+` na inclusão e ✓ na edição).

**Salvar** (`ts:172-210`): `POST {baseUrl}administracao/eventos` com o formulário completo (inclusive `id` e `arquivo`) — **mesma chamada para inclusão e edição**. Sucesso: toast fixo "Sucesso" / "Evento criado com sucesso" ou "Evento atualizado com sucesso" e navega para `/eventos`. Erro: "Erro" / "Erro ao salvar evento. Verifique os dados e tente novamente.". Inválido: "Formulário inválido" / "Preencha todos os campos obrigatórios corretamente".

### 4.11 Diálogo "Cargas de Convidados e Confirmados" (`app-evento-participantes`)

- Aberto pelo ícone de pasta da lista de eventos (`evento-list.component.html:94-95`, `:123-130`). Modal, arrastável; enquanto importa do CRM não pode ser fechado (`evento-participantes.component.html:1-10`).
- **Cabeçalho**: nome do evento e "{local} - {data por extenso com hora}" (`html:11-20`; `evento-participantes.component.ts:170-184`).
- **Seção "Carga de Convidados"** (`html:23-64`): `p-fileUpload` (botão "Adicionar"; `.xlsx,.xls`; máx. 209715200 bytes; "Clique em adicionar ou arraste e solte os arquivos aqui..."); mensagens "Planilha adicionada" / "Planilha de convidados adicionada"; "Falha ao ler planilha." / "Falha ao ler planilha de convidados."; "Planilha removida" / "Planilha de convidados removida" (`ts:74-108`). Botões do arquivo: nome (título "Download") e lixeira (título "Excluir").
- **Seção "Carga de Confirmados"** (`html:66-107`): idem, com "Planilha de confirmados adicionada", "Falha ao ler planilha de confirmados.", "Planilha de confirmados removida" (`ts:117-151`).
- Não há texto dizendo quais colunas as planilhas devem ter (não encontrado no front).
- **Seção "Inscritos do CRM"** (`html:109-127`): com `evento.codigoCampanha` preenchido mostra "Código da Campanha: **{código}**"; sem ele mostra "Informe o Código da Campanha no cadastro do evento para habilitar a importação.". Botão "Importar Inscritos do CRM" (desabilitado sem código ou durante a importação) → `EventosService.importarInscritosCrm(id)` = `POST {baseUrl}administracao/eventos/{id}/carga/crm` (corpo `{}`) (`ts:186-200`; `evento.service.ts:46-48`).
  - Sucesso: o pai mostra toast de sucesso "Importação do CRM concluída" com detalhe montado de "{n} inscrito(s) importado(s)", "{n} já vinculado(s) atualizado(s)", "{n} sem Cód. Contato (ignorado(s))" unidos por ", " e ponto final, ou "Nenhum registro foi alterado." (`evento-list.component.ts:192-201`). O diálogo permanece aberto.
  - Erro: toast "Erro ao importar inscritos do CRM" com `error.error.detalhe` ou "Erro ao importar inscritos do CRM. Tente novamente mais tarde." (`ts:196`; `evento-list.component.ts:203-205`).
- **Botão "Enviar"** (rodapé; desabilitado sem nenhuma planilha ou durante importação do CRM) (`html:129-138`) → `enviarArquivos()` (`ts:202-226`): emite `enviar` (o pai fecha o diálogo e mostra info "Cargas em processamento." / "Por favor aguarde, as cargas estão em processamento." — `evento-list.component.ts:186-190`); depois, em sequência:
  - convidados: `POST {baseUrl}administracao/eventos/{id}/carga/convidados` (`evento.service.ts:36-39`) → info "Carga concluída" / "Lista de convidados foi atualizada."; erro "Erro ao processar carga." com `detalhe` ou "Erro ao processar a carga de Convidados. Verifique o arquivo e tente novamente.";
  - confirmados: `POST {baseUrl}administracao/eventos/{id}/carga/confirmados` (`evento.service.ts:41-44`) → info "Carga concluída" / "Lista de confirmados foi atualizada."; erro "Erro ao processar carga." com `detalhe` ou "Erro ao processar a carga de Confirmados. Verifique o arquivo e tente novamente.".
  - Corpo de cada carga: `{nome, mime, tamanho, conteudo(base64)}` (`arquivo.interface.ts:3-9`).
- A lista de eventos **não** é recarregada após as cargas.

### 4.12 Participantes do evento — rota `/evento-pessoa/:id` (`evento-pessoa-routing.module.ts:9`)

Abre: (a) pelo ícone "Participantes" da lista de eventos, em nova aba; (b) automaticamente após o login dos perfis "Secretaria Mesa" e "Secretaria Check-In" (3.3); (c) via `/evento-pessoa/principal` (4.16).

**Perfis** (lidos de `auth.usuario.perfil` — `evento-pessoa.component.ts:51-54`): `isSecretariaMesa = (perfil === 'Secretaria Mesa')`; `isSecretariaCheckin = (perfil === 'Secretaria Check-In')`. Se `isSecretariaMesa`, a tela já abre no mapa de assentos (`exibirParticipantes = false`).

| Elemento | Administrador (e qualquer outro perfil) | Secretaria Mesa | Secretaria Check-In | Ref. |
|---|---|---|---|---|
| Visão inicial | lista de participantes | mapa de assentos | lista de participantes | `evento-pessoa.component.ts:23`, `:53-54` |
| Botões de alternância "Participantes" / "Mapa de Assentos" | sim | não | não | `evento-pessoa.component.html:75-94` |
| Botão "Cadastrar Pessoa" | sim | não | sim | `html:62-72` |
| Indicador "Atualização automática ativa" + botão "Atualizar agora" | não | sim | não | `html:33-56` |
| Componente de mapa usado | `app-mesa` | `app-mesa-recepcionista-checkin` | (não acessa o mapa) | `html:117-123` |
| Atualização automática dos participantes (3 s) | sim | sim | **não** | `evento-pessoa.component.ts:78-80`, `:189-206` |

**Cabeçalho (cartão do evento)** (`html:26-97`): nome do evento; "Tipo: {tipoEvento.nome}"; local; data `dd/MM/yyyy HH:mm`.

**Tela de carregamento** (`html:4-19`): "Carregando dados do evento...", "Carregando evento", "Carregando participantes" (cada item vira ✓ quando termina); some quando as duas cargas terminam (mesmo com erro) (`ts:86-121`, `:175-180`).

**Cargas**:
- Evento: `GET {baseUrl}administracao/eventos/{id}` (`ts:86-103`).
- Participantes (para o mapa): `EventoPessoaService.findParticipantesMesa` = `GET {baseUrl}administracao/evento-pessoas/mesa/participantes?idEvento={id}&isSecretariaCheckin={isSecretariaMesa}` — o parâmetro chamado `isSecretariaCheckin` recebe o valor de `isSecretariaMesa` (`ts:105-106`; `evento-pessoa.service.ts:35-38`).

**Atualização automática** (`ts:189-206`, `:123-140`, `:218-231`): depois da carga inicial, a cada 3000 ms repete a consulta de participantes em silêncio; calcula uma assinatura com `id`, `statusCheckin`, `statusConfirmacao`, `quantidadeHistoricoPessoa`, `cadeiraMesaId`, `identificacaoCadeira` de cada participante e **só substitui a lista se a assinatura mudou**. Erros só vão para o console. Não roda para "Secretaria Check-In".
- Indicador (só Secretaria Mesa): "Atualização automática ativa"; "Última verificação: {tempo}" com `title` "Última verificação em: dd/MM/yyyy HH:mm:ss"; `{tempo}` = "há alguns instantes" (< 30 s), "há {n} segundos" (< 60 s), "há {n} minuto(s)" (< 60 min) ou hora `HH:mm` (`ts:237-255`). Botão ícone `title="Atualizar agora"` → consulta imediata (`ts:163-167`).

**Alternância**: "Participantes" (lista 4.13 + filtro) e "Mapa de Assentos" (seção 5) (`html:76-92`, `ts:142-144`).

**Cadastrar Pessoa** → abre o diálogo 4.15; ao salvar, fecha o diálogo e (exceto Secretaria Check-In) refaz a consulta de participantes do mapa após 1 s (`ts:154-161`). A lista paginada de participantes não é recarregada por esse evento.

### 4.13 Participantes do evento — filtro (`app-evento-pessoas-filter`)

Sem título próprio. Todos os campos opcionais (`evento-pessoas-filter.component.ts:74-86`).

| Rótulo literal | Controle | Padrão | Lista / origem | Exibição | Ref. |
|---|---|---|---|---|---|
| "Busca" | `input` texto, placeholder "Buscar por nome, codinome, organização ou cargo" | `null` | — | todos | `evento-pessoas-filter.component.html:10-23` |
| "Legendas" | `p-multiselect`; rótulo vazio "Selecione legendas"; "{0} legendas selecionadas" (acima de 2) | `[]` | `LegendaCatalogoService.listarTodos(0, 1000, 'nomeLegenda', 'asc')` → `GET {baseUrl}administracao/legendas`; rótulo `nomeLegenda`, valor `id` (`ts:132-141`) | todos | `html:26-40` |
| "Temas" | `p-multiselect`; "Selecione temas"; "{0} temas selecionados" | `[]` | `GET {baseUrl}administracao/evento-pessoas/temas` (lista de textos) (`ts:110-119`) | oculto p/ Secretaria Check-In | `html:42-58` |
| "Grupos de Trabalho" | `p-multiSelect`; "Selecione"; "{0} grupos de trabalho selecionados" | `[]` | `GET {baseUrl}administracao/evento-pessoas/grupos-trabalho` (`ts:99-108`) | oculto p/ Secretaria Check-In | `html:61-77` |
| "Cargo" | `p-multiSelect`; "Selecione"; "{0} cargo selecionados" | `[]` | `GET {baseUrl}administracao/evento-pessoas/cargos` (`ts:121-130`) | oculto p/ Secretaria Check-In | `html:80-96` |
| "Convidado" | 3 `p-radioButton`: "Todos" (`todos`), "Sim" (`sim`), "Não" (`nao`) | `todos` | fixo no front | todos | `html:100-139` |
| "Confirmado" | idem | `todos` | fixo | todos | `html:142-181` |
| "Check-In" | idem | `todos` | fixo | todos | `html:184-223` |
| "Foto" | `p-checkbox` com rótulo "Somente pessoas sem foto" | `false` | — | todos | `html:226-237` |

- Botões: "Pesquisar" (submit) e "Limpar" (recria o formulário e pesquisa) (`html:239-254`).
- O campo "Busca" tem `(ngModelChange)="aoDigitar($event)"`, que chama `filtrar()` a cada alteração (sem espera/debounce) (`html:19`; `ts:88-90`).
- Filtro emitido (`ts:52-68`): `termoBusca`; `gruposTrabalho`, `temas`, `cargos`, `legendas` como texto com itens separados por `;`; `convidado`, `confirmado`, `checkin` (`todos`/`sim`/`nao`); `hasFoto: 'false'` apenas quando "Somente pessoas sem foto" está marcado.
- Na lista, o termo de busca é normalizado antes do envio: sem acentos, minúsculo, espaços colapsados (`evento-pessoas-list.component.ts:478-502`).
- O filtro **não persiste** entre navegações (é recriado a cada abertura).

### 4.14 Participantes do evento — lista (`app-participantes-list`)

**Legenda da tabela**: "Lista de Participantes" e, à direita, "Total: {totalRecords}" (`evento-pessoas-list.component.html:34-37`).

**Carga**: `EventoPessoaService.pesquisaParticipantes` = `GET {baseUrl}administracao/evento-pessoas` com os campos do filtro + `first`, `size` (10), `sortOrder` (0), `sortField` (`nomeCompleto`), `idEvento` (`evento-pessoas-list.component.ts:91-120`; `evento-pessoa.service.ts:16-18`). Resposta paginada (`content`, `totalElements`). 10 linhas por página; relatório "[{first} a {last} de {totalRecords}]"; paginador embaixo (`html:13-32`). Cabeçalhos **sem** ordenação por clique. Erro: só console.

| Coluna (rótulo literal) | Conteúdo | Interação | Ref. |
|---|---|---|---|
| (faixa lateral, sem rótulo) | célula pintada com `corLegenda` do participante ou `#f8f9fa` | — | `html:41`, `:55-57` |
| "Nome" | `nomeCompleto` | link para `/administracao-pessoa/{pessoaId}` em nova aba, `title` "Abrir o perfil da pessoa em nova aba" (texto simples se não houver `pessoaId`) | `html:42`, `:59-71` |
| "Organização" | `razaoSocial` ou, na falta, `nomeFantasia` | — | `html:43`, `:73-75` |
| "Cargo" | `cargo` | — | `html:44`, `:77-79` |
| "Legenda" | `nomeLegenda` | — | `html:45`, `:81-83` |
| "Convidado" | ícone por `statusConvite`: ✓ (`true`, `title` "Sim"), ✗ (`false`, "Não"), ? (nulo, "Pendente") | somente leitura | `html:46`, `:86-92`; `ts:212-234` |
| "Confirmado" | perfil ≠ Administrador: ícone ✓/✗/? somente leitura. **Administrador**: imagem clicável — pendente (`ic_status_pendente_selecionado.png`, alt "Pendente") quando `!statusConfirmacao`; confirmado (`ic_status_confirmado_selecionado.png`, alt "Confirmado") quando `true`; `title` "Confirmado" / "Não confirmado" / "Status desconhecido" | clique alterna (ver abaixo) | `html:47`, `:95-125`; `ts:236-240` |
| "Check-In" | imagem clicável pendente/confirmado conforme `statusCheckin` (mesmas imagens e `title`) | clique alterna, **para todos os perfis** | `html:48`, `:128-149` |
| "Assento" | `identificacaoCadeira` ou "Sem assento" | perfil ≠ Secretaria Check-In: clicável, `title` "Clique para gerenciar legenda da pessoa" → abre o diálogo de legenda; Secretaria Check-In: texto simples | `html:49`, `:152-164` |

O cabeçalho só aparece quando há itens (`html:40`).

**Check-in por linha** (`ts:126-158`): clique marca (`true`) ou desmarca (`false`) sem confirmação; o valor é alterado na linha antes da resposta. `EventosService.realizaCheckinParticipante({idEventoPessoa, statusCheckin})`:
- perfil "Secretaria Check-In" → `PUT {baseUrl}secretaria/checkin/participante`;
- demais → `PUT {baseUrl}administracao/eventos/participante/checkin` (`evento.service.ts:55-61`).
- Sucesso: "Check-in realizado." / "Check-in foi realizado com sucesso" (marcar); "Check-in não realizado." / "Check-in foi atualizado para não realizado" (desmarcar). Existe ainda o par "Check-in pendente." / "Check-in foi atualizado para pendente" para valor nulo, não acionável pela tela. Erro: "Erro ao realizar Check-in" / "Erro ao realizar Check-in" (o valor da linha não é revertido).
- Regra "só faz check-in quem está confirmado": não encontrado no front.

**Confirmação por linha — só Administrador** (`ts:160-210`): diálogo de confirmação com cabeçalho "Confirmar participante" e mensagem "Deseja confirmar o participante {nomeCompleto}?", ou cabeçalho "Remover confirmação" e mensagem "Deseja remover a confirmação do participante {nomeCompleto}?"; rótulos passados no código: "Sim" / "Não" (o `p-confirmDialog` do template, porém, tem cabeçalho fixo "Remover Pessoa" e rodapé próprio com botões "Remover" / "Cancelar" — `html:2-7`; ver Suspeitas). Ao aceitar: grava `statusConfirmacao` na linha; **ao remover a confirmação, também zera na linha `statusCheckin = false` e `identificacaoCadeira = null`** (`ts:173-177`); chama `PUT {baseUrl}administracao/eventos/participante/confirmacao` com `{idEventoPessoa, statusCheckin: <status da confirmação>}` (o atributo do corpo chama-se `statusCheckin`) (`ts:183-187`; `evento.service.ts:63-66`).
- Sucesso: "Confirmação realizada." / "Confirmação foi realizado com sucesso"; "Não confirmação realizada." / "A confirmação foi atualizada para não realizada"; (nulo, não acionável) "Confirmação pendente." / "Confirmação foi atualizada para pendente". Erro: "Erro ao realizar Confirmação" / "Erro ao realizar Confirmação".

**Diálogo "Gerenciar Legenda da Pessoa"** (`html:194-298`; aberto pela coluna "Assento", exceto Secretaria Check-In):
- Ao abrir: `EventoLegendaService.buscarLegendaParticipante(id)` = `GET {baseUrl}administracao/eventos/participante/{eventoPessoaId}/legenda` (`ts:342-361`; `evento-legenda.service.ts:54-56`).
- Mostra: nome; "{cargo} - {razaoSocial ou nomeFantasia}"; "Assento: {identificacaoCadeira}" (se houver) (`html:206-214`).
- "Legenda Atual:" com amostra de cor, nome e selo "Legenda manual" quando `legendaAtual.manual` (`html:217-226`); sem legenda: "Esta pessoa não possui legenda configurada." (`html:228-230`).
- "Selecione uma Legenda:" — lista do catálogo (`GET administracao/legendas`, 1000 itens por `nomeLegenda asc`, **excluída** a legenda cujo nome normalizado é "assento livre" — `ts:310-321`), cada uma com amostra de cor, nome e o texto "Configurada neste evento" quando faz parte dos blocos do evento (`GET administracao/eventos/{id}/legendas` — `ts:323-340`); opção final "Remover legenda" (`html:233-262`).
- Botões: "Remover Legenda" (só se há legenda atual), "Cancelar", "Salvar" (`html:266-297`).
- Salvar (`ts:379-411`): `PUT {baseUrl}administracao/eventos/participante/legenda` com `{eventoPessoaId, legendaId}` (`evento-legenda.service.ts:59-61`); sucesso "Sucesso" / "Legenda atualizada com sucesso!" + recarrega a página atual da lista; erro "Erro" / "Erro ao salvar legenda da pessoa.". Sem seleção e com legenda atual → segue o fluxo de remoção; sem seleção e sem legenda → aviso "Atenção" / "Esta pessoa já não possui legenda.". Aviso interno: "Atenção" / "Erro interno: pessoa não selecionada.".
- Remover (`ts:413-443`): confirmação "Tem certeza que deseja remover a legenda desta pessoa?" (cabeçalho "Confirmar Remoção"); `PUT` no mesmo endpoint com `legendaId: null`; sucesso "Sucesso" / "Legenda removida com sucesso!"; erro "Erro" / "Erro ao remover legenda da pessoa."; aviso "Atenção" / "Esta pessoa não possui legenda para remover.".
- Atribuir/alterar o **assento** por esta tela: não encontrado (a coluna só abre a legenda; assentos são atribuídos no mapa — seção 5).

**Exportação** — botão "Download" no rodapé da tabela, para todos os perfis (`html:168-181`) → `exportCSV()` (`ts:454-476`): aviso "Exportação em andamento." / "A exportação dos participantes está em andamento, por favor aguarde."; `EventosService.imprimirParticipantes` = `GET {baseUrl}administracao/eventos/participantes/excel` com o filtro atual + `first=0`, `size=100000`, `sortOrder`, `sortField`, `idEvento` (`evento.service.ts:93-100`); a resposta é um objeto `{content: <base64>, name}` e o arquivo é salvo com o nome recebido. Erro: "Erro" / "Erro ao exportar participantes.". Apesar do nome do método, o endpoint é `.../excel`; formato do arquivo: não determinável pelo front.

**Estado vazio**: "Nenhum participante encontrado." (`html:186`).

Lista fixa `statusOptions` ("Confirmado"/"Não confirmado"/"Pendente") declarada e não usada (`ts:25-29`).

### 4.15 Diálogo de cadastro avulso de pessoa ("Cadastrar Pessoa" — `app-pessoas-cadastro`)

- Aberto pelo botão "Cadastrar Pessoa" (4.12). Modal arrastável. **Cabeçalho**: nome do evento e "{local} - {data por extenso com hora}" (`pessoas-cadastro.component.html:10-19`).

| Rótulo literal | Controle | Obrig. | maxlength | Validadores | Padrão | Ref. |
|---|---|---|---|---|---|---|
| "Nome Completo: " + `*` | `input` texto (`nome`), contador `n/255` | Sim | 255 | `required`, `minLength(3)`, `maxLength(255)` | — | `html:26-47`; `pessoas-cadastro.component.ts:74-81` |
| "Instituição/Empresa" + `*` | `input` texto (`razaoSocial`), contador `n/255` | Sim | 255 | `required`, `maxLength(255)` | — | `html:50-71`; `ts:82-88` |
| "Cargo" + `*` | `input` texto, contador `n/100` | Sim | 100 | `required`, `maxLength(100)` | — | `html:74-95`; `ts:89-94` |
| "E-mail" + `*` | `input` texto, contador `n/255` | Sim | 255 | `required` (sem validação de formato) | — | `html:98-119`; `ts:95-99` |
| "Check-in Automático" | `p-checkbox`, `pTooltip` "Ao marcar esta opção, a pessoa cadastrada terá seu check-in realizado automaticamente" | Não | — | — | **marcado** (`true`) | `html:122-132`; `ts:100` |

- Botão "Enviar" (desabilitado com formulário inválido) (`html:135-145`) → `EventosService.salvarPessoaCadastroRapido(evento.id, {nome, razaoSocial, cargo, email, checkin})` = `POST {baseUrl}administracao/eventos/{id}/cadastro-rapido` (`ts:105-141`; `evento.service.ts:78-81`).
- Sucesso: toast fixo "Sucesso" / "Cadastro de pessoa na recepção realizado com sucesso"; limpa o formulário; emite `save`.
- Erro: toast com `severity: 'erro'` (valor fora do padrão do PrimeNG), "Erro" / "Erro ao cadastrar pessoa na recepção" (`ts:132-139`).
- Fechar o diálogo recria o formulário (`ts:61-64`).

### 4.16 Rotas auxiliares do evento principal

- `/evento-pessoa/principal` → `EventoPessoaPrincipalComponent` (template vazio, 0 bytes): se o perfil for "Secretaria Mesa" ou "Secretaria Check-In", navega para `/evento-pessoa/{localStorage['eventoPrincipalId']}`; para outros perfis não faz nada (tela em branco) (`evento-pessoa-principal.component.ts:12-20`). A rota está declarada duas vezes (`evento-pessoa-routing.module.ts:8` e `administracao.routing.ts:61-64`).
- `/nao-ha-principal` → `NaoHaPrincipalComponent`: cartão com `<h2>Não há evento principal.</h2>` (`nao-ha-principal.component.html:1-3`; `administracao.routing.ts:57-60`). **Nenhum código do front navega para essa rota** (busca por `nao-ha-principal` só encontra a declaração da rota e o componente).

### 4.17 Configuração de legendas do evento — rota `/regras-legenda/:eventoId` (`administracao.routing.ts:37-46`, `legendas-routing.module.ts:15`)

Abre pelo ícone "Configuração de Legendas" da lista de eventos (4.9). Dado de rota `breadcrumb: 'Configuração de Legendas'` (não exibido). Sem checagem de perfil.

**Cabeçalho** (`configuracao-legendas-evento.component.html:6-24`): título `<h2>Configuração de Legendas</h2>`; nome do evento (quando carregado); contagem "{n} bloco configurado" / "{n} blocos configurados"; indicador de persistência "Salvando…" (com spinner) e, depois, "Salvo" (some após 2500 ms — `configuracao-legendas-evento.component.ts:173-180`).

**Cargas iniciais** (`ts:107-161`):
- `EventoLegendaService.buscarConfiguracao(eventoId)` = `GET {baseUrl}administracao/eventos/{eventoId}/legendas`; os blocos são ordenados por `numero` crescente (`ts:143-151`; `evento-legenda.service.ts:25-27`).
- `GET {baseUrl}administracao/eventos/{eventoId}` só para o nome (falha silenciosa) (`ts:153-161`).
- Sem `eventoId` válido na URL: erro "Erro" / "Evento não informado na URL." (`ts:129-131`).

**Persistência automática (não há botão "Salvar configuração")** (`ts:39-48`, `:111-124`, `:165-188`): toda mudança estrutural (adicionar/remover/reordenar bloco, adicionar/remover condição, troca de conectivo/campo/operador, saída do campo de valor) dispara imediatamente `EventoLegendaService.salvarConfiguracao` = `PUT {baseUrl}administracao/eventos/{eventoId}/legendas` com `{eventoId, blocos[]}` (`evento-legenda.service.ts:30-32`); a digitação no valor de uma condição persiste após 600 ms de pausa. Um novo `PUT` cancela o anterior ainda em andamento (`switchMap`). Em falha: mostra o erro e **recarrega a configuração do servidor**, descartando o estado local (`ts:182-188`).

**Barra de ações** (`html:26-40`):

| Botão (rótulo literal) | Efeito | Ref. |
|---|---|---|
| "Carregar configuração" | abre o diálogo 4.20 | `html:27-28`; `ts:247-249` |
| "Salvar como preset" | abre o diálogo 4.19 | `html:29-30`; `ts:251-253` |
| "Gerenciar catálogo" | navega para `/catalogo-legendas?eventoId={eventoId}` (4.22) | `html:31-32`; `ts:243-245` |
| "Adicionar bloco" | abre o diálogo 4.18 | `html:33-34`; `ts:255-257` |
| "Simular" | `EventoLegendaService.simular` = `POST {baseUrl}administracao/eventos/{eventoId}/legendas/simular` com a configuração atual; abre o diálogo 4.21 com o resultado | `html:36-37`; `ts:259-267`; `evento-legenda.service.ts:35-37` |
| "Executar" | confirmação e execução (abaixo) | `html:38-39`; `ts:269-291` |

**Executar**: diálogo de confirmação com cabeçalho "Executar aplicação de legendas", mensagem "As associações de legenda deste evento serão recriadas a partir dos blocos configurados. As legendas atribuídas manualmente serão preservadas. Outros eventos não serão afetados. Deseja continuar?", botões "Executar" / "Cancelar" (`ts:269-280`). Aceite → `EventoLegendaService.executar` = `POST {baseUrl}administracao/eventos/{eventoId}/legendas/executar` com a configuração atual (`evento-legenda.service.ts:40-42`); sucesso: toast "Legendas aplicadas" / "{legendasAplicadas} legendas aplicadas, {manuaisPreservadas} manuais preservadas." (`ts:282-291`).

**Reset de legendas**: não encontrado no front (não há botão, método nem endpoint de "reset"/"limpar legendas" em `legendas/` nem em `evento/`; a busca por `reset` só encontra o reset do formulário de bloco).

**Estado vazio** (`html:43-48`): "Nenhum bloco configurado"; "Adicione o primeiro bloco de legenda para começar a montar as regras deste evento."; botão "Adicionar bloco".

**Cartão de bloco** (`app-bloco-evento-card`, um por bloco — `bloco-evento-card.component.html`):
- Cabeçalho: número do bloco (`pTooltip="Ordem de aplicação"`), amostra de cor, nome da legenda (`html:4-8`). O número é sempre recalculado pela posição (1, 2, 3…) a cada mudança (`configuracao-legendas-evento.component.ts:201-204`).
- Botões: seta para cima (`pTooltip="Mover para cima"`, desabilitada no primeiro); seta para baixo (`pTooltip="Mover para baixo"`, desabilitada no último); "Remover bloco do evento" → confirmação com cabeçalho "Remover bloco", mensagem "Remover o bloco '{nomeLegenda}' deste evento?", botões "Remover" / "Cancelar" (`html:11-38`; `bloco-evento-card.component.ts:74-84`).
- Reordenação apenas pelos botões (não há arrastar-e-soltar).
- Lista de condições com cabeçalho de colunas "Conectivo", "Campo", "Operador", "Valor" (só quando há condições) (`html:43-49`).
- Sem condições: "Nenhuma condição definida. Este bloco não será aplicado automaticamente até ter ao menos uma condição." (`html:60-62`).
- Botão "Adicionar condição" → acrescenta condição com `campo = 'grupoTrabalho'`, `operador = 'IGUAL'`, `valor = ''`, `conectivo = null` se for a primeira, senão `'E'` (`html:64-71`; `ts:41-51`). Ao remover uma condição, a que passa a ser a primeira tem o conectivo zerado (`ts:53-64`).

**Linha de condição** (`app-condicao-linha` — `condicao-linha.component.html`):

| Coluna | Controle | Valores (fixos no front — `legenda.interface.ts:134-154`) | Ref. |
|---|---|---|---|
| "Conectivo" | `p-select`; **não aparece na primeira condição** | "E" (`E`), "OU" (`OU`) | `html:4-15` |
| "Campo" | `p-select`, placeholder "Campo" | "Grupo de trabalho" (`grupoTrabalho`), "Tema" (`tema`), "Cargo" (`cargo`), "Nome fantasia" (`nomeFantasia`), "Papel desempenhado" (`papelDesempenhado`) | `html:18-29` |
| "Operador" | `p-select`, placeholder "Operador" | "Igual a" (`IGUAL`), "Diferente de" (`DIFERENTE`), "Contém" (`CONTEM`), "Em (lista)" (`EM`) | `html:32-43` |
| "Valor" | `input` texto; placeholder "Digite o valor" ou, com operador `EM`, "valores separados por vírgula" | texto livre, sem maxlength nem validação | `html:46-55`; `condicao-linha.component.ts:52-54` |
| (ação) | botão lixeira, `pTooltip="Remover condição"` (sem confirmação) | — | `html:58-68` |

Validação de condição (valor vazio, combinações inválidas): não encontrado no front.

### 4.18 Diálogo "Adicionar bloco" (`app-adicionar-bloco-dialog`)

- Cabeçalho "Adicionar bloco"; modal, não arrastável (`adicionar-bloco-dialog.component.html:1-2`). Ao abrir: volta à primeira aba, limpa busca e seleção, e carrega o catálogo (`GET {baseUrl}administracao/legendas`, `first=0`, `rows=1000`, `sort=nomeLegenda`, `direction=asc`) (`adicionar-bloco-dialog.component.ts:83-103`).
- **Aba "Usar bloco existente"** (`html:12-46`): campo de busca (placeholder "Buscar bloco pelo nome", filtro no cliente por "contém", sem diferenciar maiúsculas); lista com seleção múltipla por caixas (`p-listbox`), cada item com amostra de cor e nome; **os blocos já presentes no evento não aparecem** (`ts:106-113`); "Carregando catálogo…"; lista vazia: "Nenhum bloco disponível para adicionar."; busca sem resultado: "Nenhum bloco encontrado para "{termo}"." e o atalho "Adicionar bloco "{termo}"", que troca para a aba de criação com o nome preenchido (`ts:115-124`).
- **Aba "Criar novo bloco"** (`html:49-51`): formulário de bloco (abaixo).
- Rodapé (`html:55-64`): "Cancelar"; na 1ª aba "Adicionar ao evento" (desabilitado sem seleção); na 2ª aba "Criar e adicionar" (desabilitado enquanto cria).
- "Adicionar ao evento": os blocos escolhidos entram no fim da lista do evento, sem condições, e a configuração é salva (`ts:126-137`; `configuracao-legendas-evento.component.ts:296-308`).
- "Criar e adicionar": `LegendaCatalogoService.criar` = `POST {baseUrl}administracao/legendas` com `{id: 0, nomeLegenda, background}` e, em seguida, adiciona o bloco criado ao evento (`ts:139-157`; `legenda-catalogo.service.ts:32-34`).

**Formulário de bloco** (`app-bloco-form`, reutilizado em 4.18 e 4.22 — `bloco-form.component.html`):

| Rótulo literal | Controle | Obrig. | maxlength | Validador / mensagem | Padrão | Ref. |
|---|---|---|---|---|---|---|
| "Nome da legenda" + `*` | `input` texto, placeholder "Digite o nome da legenda" | Sim | 100 | `required` → "Este campo é obrigatório" | `''` | `html:3-11`; `bloco-form.component.ts:57` |
| "Cor" + `*` | `p-colorPicker` + valor em maiúsculas ao lado + paleta de 16 cores clicáveis | Sim | — | `required` | `#2196F3` (primeira da paleta) | `html:13-35`; `ts:32-36`, `:58` |

- Paleta fixa (`ts:32-36`): `#2196F3`, `#4CAF50`, `#FF9800`, `#F44336`, `#9C27B0`, `#00BCD4`, `#FFEB3B`, `#795548`, `#607D8B`, `#E91E63`, `#3F51B5`, `#009688`, `#8BC34A`, `#FF5722`, `#673AB7`, `#CDDC39`. O valor enviado é sempre em maiúsculas; o nome é enviado sem espaços nas pontas (`ts:73-77`).
- Validação de nome duplicado: não encontrado no front.

### 4.19 Diálogo "Salvar como preset" (`app-salvar-preset-dialog`)

- Cabeçalho "Salvar como preset" (`salvar-preset-dialog.component.html:1`).

| Rótulo literal | Controle | Obrig. | maxlength | Mensagem | Ref. |
|---|---|---|---|---|---|
| "Nome do preset" + `*` | `input` texto, placeholder "Digite um nome para o preset" | Sim | 100 | "Este campo é obrigatório" (após tocar ou tentar salvar com nome vazio/só espaços) | `html:5-11`; `salvar-preset-dialog.component.ts:47-49`, `:57-61` |
| "Descrição" | `textarea` 3 linhas, placeholder "Descrição opcional" | Não | 255 | — | `html:13-17` |

- Botões: "Cancelar"; "Salvar preset" (`html:20-23`).
- Ao confirmar: a página chama `LegendaCatalogoService.salvarPreset` = `POST {baseUrl}administracao/legendas/presets` com `{nome, descricao, eventoId, configuracao: {eventoId, blocos}}` (`configuracao-legendas-evento.component.ts:311-322`; `legenda-catalogo.service.ts:71-73`). Sucesso: toast "Preset salvo" / "O preset '{nome}' foi salvo.".

### 4.20 Diálogo "Carregar configuração" (`app-carregar-configuracao-dialog`)

- Cabeçalho "Carregar configuração" (`carregar-configuracao-dialog.component.html:1`).
- **Modo** — "Ao aplicar:" com duas opções (`p-radioButton`): "Substituir configuração atual" (`substituir`, **padrão**) e "Mesclar (adicionar blocos ausentes)" (`mesclar`) (`html:4-14`; `carregar-configuracao-dialog.component.ts:64`, `:85`).
- Ao abrir carrega (`ts:83-124`): ids do catálogo (`GET administracao/legendas`, 1000 itens); presets (`GET {baseUrl}administracao/legendas/presets`); eventos de origem (`GET {baseUrl}administracao/eventos/legendas/origens?excluirEventoId={eventoId}` — `evento-legenda.service.ts:45-51`).
- **Aba "Biblioteca de presets"** (`html:24-58`): "Carregando presets…"; vazio "Nenhum preset salvo ainda."; um cartão por preset com nome, "{n} bloco" / "{n} blocos", descrição (se houver) e uma etiqueta colorida por bloco; botões "Aplicar ao evento" e "Excluir preset".
  - "Aplicar ao evento": `GET {baseUrl}administracao/legendas/presets/{id}`; blocos cujo `legendaId` não existe mais no catálogo são descartados e contados (`ts:128-139`); a página mostra aviso "Blocos ignorados" / "{n} bloco(s) do preset não existe(m) mais no catálogo e foram ignorados." (`configuracao-legendas-evento.component.ts:329-334`).
  - "Excluir preset": confirmação com cabeçalho "Excluir preset", mensagem "Excluir o preset '{nome}'? Esta ação não pode ser desfeita.", botões "Excluir" / "Cancelar"; `DELETE {baseUrl}administracao/legendas/presets/{id}`; sucesso "Preset excluído" / "O preset '{nome}' foi removido." e recarrega a lista (`ts:151-171`).
- **Aba "De outro evento"** (`html:61-82`): "Carregando eventos…"; vazio "Nenhum outro evento com blocos configurados."; uma linha por evento com nome, "{data} · {n} bloco(s)" e botão "Aplicar ao evento" → `GET {baseUrl}administracao/eventos/{eventoId}/legendas` do evento de origem (`ts:141-149`).
- **Regra de aplicação** (`ts:173-198`): os blocos trazidos são copiados com suas condições (campo, operador, valor, conectivo). *Substituir*: a configuração passa a ser só os blocos trazidos. *Mesclar*: mantém os blocos atuais intactos e acrescenta, ao final, apenas os blocos cuja legenda ainda não está no evento. Em seguida os números são recalculados e a configuração é salva (`configuracao-legendas-evento.component.ts:325-335`). Não há confirmação antes de substituir.
- Rodapé: "Cancelar" (`html:86-88`).

### 4.21 Diálogo "Simulação de aplicação de legendas" (`app-simulacao-dialog`)

- Cabeçalho "Simulação de aplicação de legendas" (`simulacao-dialog.component.html:1`).
- Quatro cartões de totais: "Participantes" (`totalParticipantes`), "Legendas removidas" (`legendasRemovidas`), "Legendas aplicadas" (`legendasAplicadas`), "Manuais preservadas" (`manuaisPreservadas`) (`html:7-24`).
- Aviso "Blocos ignorados: {lista separada por vírgula}" quando `blocosIgnorados` não é vazio (`html:26-29`).
- Tabela por legenda (`html:31-75`): colunas "Nº" (`numero`), "Cor" (amostra), "Legenda" (`nomeLegenda`), "Quantidade" (`quantidade`); cada linha pode ser expandida para listar os nomes dos participantes; expansão vazia: "Nenhum participante nesta legenda."; tabela vazia: "Nenhum bloco produziu resultado.". Sem paginação nem ordenação.
- Rodapé: "Fechar"; "Executar" → fecha o diálogo e abre a mesma confirmação de execução de 4.17 (`html:79-83`; `configuracao-legendas-evento.component.ts:338-341`).

### 4.22 Catálogo de legendas — rota `/catalogo-legendas` (`administracao.routing.ts:47-56`, `legendas-routing.module.ts:13`)

Abre por "Gerenciar catálogo" (4.17, com `?eventoId=`) ou diretamente pela rota. Sem checagem de perfil.

**Título**: `<h2>Catálogo de blocos</h2>`; subtítulo "Blocos de legenda reutilizáveis nas configurações dos eventos." (`catalogo-legendas.component.html:9-10`).

**Botões do cabeçalho** (`html:13-16`): "Voltar" → `/regras-legenda/{eventoId}` se veio de um evento, senão `/eventos` (`catalogo-legendas.component.ts:111-117`); "Novo bloco" → abre o diálogo de bloco.

**Busca**: campo com placeholder "Buscar bloco pelo nome"; aplica após 300 ms sem digitar e só se o termo mudou; volta à primeira página; envia `nomeLegenda={termo}` (`html:20-26`; `ts:96-101`, `:148-156`).

**Lista**: `LegendaCatalogoService.listarTodos` = `GET {baseUrl}administracao/legendas` com `first`, `rows`, `sort`, `direction` e o filtro (`ts:130-146`; `legenda-catalogo.service.ts:45-53`). Paginação no servidor, 10 por página, paginador embaixo; ordenação padrão `nomeLegenda asc`.

| Coluna (rótulo literal) | Conteúdo | Ordenável | Ref. |
|---|---|---|---|
| "Nome" | `nomeLegenda` | Sim | `html:46-48`, `:56-58` |
| "Cor" | amostra de cor com `title` = código da cor | Não | `html:49`, `:59-62` |
| "Ações" | lápis (`pTooltip="Editar bloco"`), lixeira (`pTooltip="Excluir bloco"`) | Não | `html:50`, `:63-70` |

**Estado vazio**: "Nenhum bloco encontrado." (`html:79`).

**Diálogo "Novo bloco" / "Editar bloco"** (`html:90-103`; `ts:160-217`): contém o formulário de bloco (4.18); botões "Cancelar" e "Salvar" (desabilitado enquanto salva).
- Inclusão: `POST {baseUrl}administracao/legendas` com `{id: 0, nomeLegenda, background}` → toast "Bloco criado" / "O bloco foi criado com sucesso."; volta à primeira página.
- Edição: `PUT {baseUrl}administracao/legendas/{id}` com `{id, nomeLegenda, background}` → toast "Bloco atualizado" / "O bloco foi atualizado com sucesso."; mantém a página (`legenda-catalogo.service.ts:36-38`).

**Excluir bloco** (`ts:221-269`): primeiro consulta o uso — `LegendaCatalogoService.buscarUso` = `GET {baseUrl}administracao/legendas/{id}/uso` (resposta `{legendaId, quantidadeEventos, eventos[{id, nome}]}`); depois confirma (cabeçalho "Excluir bloco", botões "Excluir" / "Cancelar") com uma destas mensagens:
- em uso em outros eventos: "O bloco '{nome}' está em uso em outros eventos: {lista}. Excluir também o removerá dessas configurações e das legendas dos participantes. Deseja continuar?" (quando veio de um evento) ou "...está em uso nos eventos: {lista}. ..." (sem evento de origem);
- em uso só no evento de origem: "Excluir o bloco '{nome}'? Ele será removido da configuração deste evento e das legendas dos participantes.";
- sem uso: "Excluir o bloco '{nome}'?".
- Aceite: `DELETE {baseUrl}administracao/legendas/{id}` → toast "Bloco excluído" / "O bloco foi excluído com sucesso."; volta à primeira página.

**Erros** (4.17 a 4.22): `handleErrorAlert` (ver 4.0) quando a resposta tem corpo; sem corpo: "Erro" / "Falha de comunicação com o servidor." (`catalogo-legendas.component.ts:274-280`; `configuracao-legendas-evento.component.ts:191-197`).

### 4.23 Mapa de assentos (`app-mesa` e `app-mesa-recepcionista-checkin`)

Abre dentro de `/evento-pessoa/:id` (4.12). Título próprio: não há (o painel lateral tem o título "Pessoas Disponíveis ({n})" e o centro da mesa o texto "Mesa Principal"). Descrição completa — assentos, lista de pessoas, arrastar-e-soltar, remover, "Limpar Todas", "Atender", busca, cores/legendas, atualização e exportação — na seção 5.

---

## 5. Mapa de assentos em detalhe

Arquivos (abreviações usadas nesta seção):

| Sigla | Componente | Seletor | Arquivos | Linhas |
|---|---|---|---|---|
| **A** | `RetangularComponent` (mesa do administrador, retangular) | `app-retangular` | `retangular.component.ts` / `.html` | 2539 / 504 |
| **B** | `RetangularInvertidoComponent` (administrador, retangular invertido) | `app-retangular-invertido` | `retangular-invertido.component.ts` / `.html` | 2528 / 492 |
| **C** | `RetangularRecepcionistaCheckinComponent` (Secretaria Mesa, retangular) | `app-retangular-recepcionista-checkin` | `retangular-recepcionista-checkin.component.ts` / `.html` | 1541 / 403 |
| **D** | `RetangularInvertidoRecepcionistaCheckinComponent` (Secretaria Mesa, invertido) | `app-retangular-invertido-recepcionista-checkin` | `retangular-invertido-recepcionista-checkin.component.ts` / `.html` | 2756 / 453 |

Método de leitura (o que foi efetivamente lido de cada um):
- **A**: `.ts` e `.html` por inteiro.
- **B**: `.ts` por `diff` contra A (85 linhas diferentes); `.html` por `diff` contra A ignorando espaços, mais busca das linhas-chave.
- **D**: `.html` por inteiro; `.ts` por `diff` contra B (370 linhas diferentes).
- **C**: `.ts` por inteiro; `.html` por `diff` contra D (ignorando espaços) e busca das linhas-chave.

### 5.1 Quem vê qual componente

- O mapa fica dentro da tela `/evento-pessoa/:id` (4.12). Se o perfil é "Secretaria Mesa" a tela usa `app-mesa-recepcionista-checkin`; para qualquer outro perfil que chegue ao mapa (na prática o Administrador, pois "Secretaria Check-In" não tem o botão de alternância) usa `app-mesa` (`evento-pessoa.component.html:117-123`).
- Os dois invólucros escolhem a variação pelo `indicador` do tipo de mesa do evento: `'RETANGULAR'` → A (ou C); `'RETANGULAR_INVERTIDO'` → B (ou D). Qualquer outro indicador não renderiza nada (`mesa.component.html:1-8`, `mesa.component.ts:15-24`; `mesa-recepcionista-checkin.component.html:1-8`, `mesa-recepcionista-checkin.component.ts:15-24`). O valor inicial é `'RETANGULAR'`.
- Nenhum dos quatro componentes testa perfil internamente (busca por `perfil`/`isSecretaria`/`isAdministrador` nos oito arquivos: zero ocorrências). A diferença de permissão é dada pela escolha do componente.
- Apesar do nome "recepcionista-checkin", o componente é o exibido ao perfil **"Secretaria Mesa"**.

### 5.2 Comportamento comum (descrito sobre A — mesa do administrador, retangular)

**Dados de entrada**
- `participantes` (lista vinda da tela-mãe — `GET administracao/evento-pessoas/mesa/participantes`, 4.12) e `eventoSelecionado` (`retangular.component.ts:82-98`). Cada vez que a tela-mãe entrega uma nova lista não vazia, o mapa **zera todas as posições e remonta** a partir dos dados recebidos (`ts:83-91`, `:228-240`, `:353-368`).
- Cadeiras do evento: `EventosService.findCadeiras(eventoId)` = `GET {baseUrl}administracao/eventos/{id}/cadeiras` → lista de `{id, identificacaoCadeira, background, composicaoMesa, eventoId}` (`ts:242-252`; `evento.service.ts:31-34`; `cadeira-mesa.interface.ts:1-6`). `composicaoMesa` assume `'PRINCIPAL'` ou `'LATERAL'` (`ts:266-267`).
- Blocos de legenda do evento: `GET {baseUrl}administracao/eventos/{id}/legendas` (erro → lista vazia) (`ts:333-338`; `legenda-mesa.helper.ts:40-48`).
- Tela de carregamento "Carregando dados da mesa..." enquanto carrega ou salva (`retangular.component.html:5-10`).

**Identificação dos assentos (setores e numeração)** — fixa no front; a cadeira precisa existir na lista da API com a mesma `identificacaoCadeira` para ter estilo, dica e poder receber pessoa (`ts:746-793`, `:509-523`).

| Setor (letra) | Área no código | Faixa em A | Disposição | Composição enviada | Ref. |
|---|---|---|---|---|---|
| A | `cabecalho` (topo da mesa principal) | A1–A5, exibidos na ordem **A4, A2, A1, A3, A5** | 1 linha de 5 | `PRINCIPAL` | `ts:31`, `:762-763`, `:1683-1685`, `:1790` |
| B | `lateralEsquerda` | B1–B35 | 1 coluna de 35 | `PRINCIPAL` | `ts:32`, `:770`, `:1816-1824` |
| C | `lateralDireita` | C1–C35 | 1 coluna de 35 | `PRINCIPAL` | `ts:33`, `:773`, `:1829-1837` |
| D | `rodape` (base da mesa principal) | D1–D5, na ordem **D4, D2, D1, D3, D5** | 1 linha de 5 | `PRINCIPAL` | `ts:34`, `:766-767`, `:1696-1698`, `:1804` |
| F | `assentosLaterais` | F1–F32 | grade 8 linhas × 4 colunas (nº = linha×4 + coluna + 1) | `LATERAL` | `ts:36`, `:755-756`, `:1843-1855` |
| G | `secaoG` | G1–G10 | 1 coluna de 10 | `LATERAL` | `ts:37`, `:1663-1665`, `:1860-1868` |
| H | `secaoH` | H1–H36 | grade 9 × 4 | `LATERAL` | `ts:38`, `:1107-1109`, `:1874-1886` |
| E | `secaoE` | E1–E23 | 1 coluna de 23 | `LATERAL` | `ts:39`, `:1172`, `:1891-1899` |

- Total em A: 5 + 35 + 35 + 5 + 32 + 10 + 36 + 23 = **181** posições desenhadas. O centro da mesa mostra o texto "Mesa Principal" (`html:291`).
- Disposição na tela em A (esquerda → direita): bloco F, G e H empilhados; mesa principal (A no topo, B à esquerda, C à direita, D na base); coluna E (`html:123-384`).
- "Nomes de setor" derivados da letra, usados só na dica (tooltip) do assento (`ts:296-313`): A1 = "Anfitrião"; A2–A5 = "Palestrantes"; B e C: 1–5 "Presidência", 6–15 "Deputados Federais", 16–25 "Senadores", 26+ "Convidados Especiais"; D = "Governadores"; E = "Imprensa"; F = "Assessoria"; G = "Segurança"; H = "Técnicos"; demais = "Outros". Cores associadas a esses nomes existem em `getCorPorSetor` (`ts:315-331`) mas só entram como `background` da cadeira quando a API não manda cor, e esse `background` não é usado na pintura do assento (ver cores abaixo).

**Lista "Pessoas Disponíveis ({n})"** (painel lateral — `html:14-44`)
- Quem entra: todos os participantes recebidos que **não estão alocados em assento** (`ts:423-427`). "Alocado" = tem `identificacaoCadeira` e `cadeiraMesaId` (`ts:373-385`). Quem sai: ao ser colocado num assento sai da lista; ao ser removido do assento volta.
- Ordem: a mesma da lista recebida do backend (sem ordenação no front).
- Busca "Buscar pessoa..." (`html:19`): filtra enquanto digita, sem acento e sem diferenciar maiúsculas, por `nomeCompleto`, `codinome`, `cargo`, `razaoSocial`, `nomeFantasia` ou `nomeLegenda` (`ts:569-603`).
- Cada cartão mostra (`html:24-42`): nome (codinome, se preenchido; senão nome completo); "({quantidadeHistoricoPessoa})"; cargo; `nomeFantasia` ou `razaoSocial`; etiqueta colorida com o nome da legenda (só quando `numeroLegenda` é verdadeiro); etiqueta de status "Check in realizado" (verde) ou "Check in não identificado" (amarela) (`retangular.component.css:259-267`). `title` = "{cargo} - {razaoSocial}".
- Os cartões são arrastáveis, exceto durante carregamento/salvamento (`html:25-28`).

**Conteúdo de um assento** (`html:129-152` e blocos equivalentes)
- Vazio: mostra a identificação (ex.: "B12"). Dica: "Cadeira {id}\nSetor: {nome do setor}\nClique para atribuir uma pessoa" (`ts:879`).
- Ocupado: nome (codinome ou nome completo) e, abaixo, `nomeFantasia` ou `razaoSocial`; botão "×" com `title="Remover pessoa"`. Na seção E aparece também "({quantidadeHistoricoPessoa})" (`html:370-372`). Dica: "{id} - {setor}\nPessoa: {nomeCompleto}\nCargo: {cargo}\nInstituição: {razaoSocial}\nParticipações anteriores: {quantidadeHistoricoPessoa}\nStatus: {status}", com status "Check in realizado" / "Check in não identificado" (mesa principal e F — `ts:876-877`, `:1012-1013`) ou "Check in realizado" / "Check in não realizado" (G, H, E — `ts:1076`, `:1140`, `:1203`).

**Cores e legendas** (`legenda-mesa.helper.ts`)
- Cor da pessoa = `corLegenda` que já vem no participante; sem legenda usa `#f8f9fa` (`legenda-mesa.helper.ts:11`, `:51-53`).
- Assento ocupado **com check-in**: fundo na cor da legenda, texto branco. Ocupado **sem check-in**: fundo branco e borda na cor da legenda. Vazio: fundo branco, borda cinza (`ts:827-858`, `:989-1005`).
- Quadro "Legenda das Categorias" (`html:423-445`): um item por legenda com amostra de cor e o texto "{nome} ({quantidade})". Itens = blocos configurados no evento, na ordem; mais as legendas presentes em participantes que não estejam na configuração (legendas manuais); mais a linha "Assento livre" (`legenda-mesa.helper.ts:83-121`). Nome ausente vira "Sem descrição".
- Contagem (`legenda-mesa.helper.ts:128-140`): para "Assento livre" = nº de cadeiras retornadas pela API − nº de pessoas alocadas (mínimo 0); para as demais = nº de pessoas **alocadas** com aquela legenda. Qualquer legenda cujo nome normalizado seja "assento livre" é tratada como essa linha única (`:66-72`, `:91-99`).
- Legenda de status (`html:431-444`): "Check in realizado" (quadrado azul cheio), "Check in não identificado" (quadrado só com borda azul), "Vazio" (branco) (`retangular.component.css:176-198`).

**Colocar pessoa em assento**
- *Arrastar da lista para um assento* (`ts:686-744`): solta a pessoa no assento. Se ela já está alocada (veio da lista mas consta como alocada) a operação é ignorada.
- *Arrastar de um assento para outro* (`ts:978-986`, `:720-723`): a pessoa sai do assento de origem e vai para o destino.
- *Assento de destino ocupado*: **não há troca** — o ocupante anterior é desalocado (perde `cadeiraMesaId`, `identificacaoCadeira`, `composicaoMesa`) e volta para "Pessoas Disponíveis"; a pessoa arrastada assume o lugar (`ts:729-743`, `:543-555`).
- *Clique no assento* abre a janela "Selecionar Pessoa" (`html:388-417`): campo "Digite o nome para filtrar..." (mesmo filtro da lista lateral) e a lista de pessoas disponíveis — cada opção com nome, "({histórico})", `nomeFantasia` ou `razaoSocial`, `razaoSocial` e a etiqueta de check-in; clicar numa opção aloca a pessoa no assento (`ts:456-481`). Nos setores F, G, H e E o clique só abre a janela se o assento estiver **vazio** (`ts:1019-1031`, `:1083-1094`, `:1147-1158`, `:1210-1221`); na mesa principal (A, B, C, D) abre mesmo com o assento ocupado (ver Suspeitas) (`ts:436-454`).
- Todas as operações ficam bloqueadas enquanto há carregamento ou salvamento automático (`ts:438`, `:458`, `:485`, `:698`).

**Remover do assento**: botão "×" (`title="Remover pessoa"`) no assento ocupado — desaloca e devolve a pessoa à lista, sem confirmação (`ts:483-496`, `:1033-1041`, `:1096-1104`, `:1160-1168`, `:1223-1231`).

**Painel "Gerenciar Pessoas Alocadas na Mesa"** (oculto em tablet — `html:81-117`)
- "Salvar Alocações ({n})" (desabilitado sem pessoas alocadas ou durante carregamento/salvamento) → `EventosService.salvarComposicoesMesa(eventoId, pessoasAlocadas)` = `POST {baseUrl}administracao/eventos/{eventoId}/composicoes-mesa` com a lista completa das pessoas alocadas (objetos do participante com `cadeiraMesaId`, `identificacaoCadeira`, `composicaoMesa`) (`ts:1421-1463`; `evento.service.ts:68-71`). Sucesso: "Sucesso" / "Composições da mesa salvas com sucesso! {n} pessoas foram alocadas."; erro: "Erro" / "Erro ao salvar composições da mesa. Verifique o console para mais detalhes."; sem alocados: "Aviso" / "Não há pessoas alocadas na mesa para salvar.".
- "Limpar Todas" (mesmas condições de habilitação) → remove **todas** as alocações do mapa, sem confirmação; mensagem "Sucesso" / "Todas as alocações foram removidas da mesa." (`ts:1571-1605`). Ver Suspeitas sobre a persistência dessa limpeza.
- **Salvamento automático**: cada alocação/remoção agenda um salvamento para **30 000 ms** depois da última alteração (`DEBOUNCE_DELAY = 30000`; o comentário diz "5 segundos") (`ts:69`, `:1497-1512`). Na execução, envia a mesma requisição do "Salvar Alocações", bloqueia a tela e mostra "Salvando composição automaticamente..." (`html:85-88`); sucesso: "Salvo" / "Composição salva automaticamente"; erro: "Erro ao Salvar" / "Erro ao salvar composição automaticamente. Suas alterações podem não ter sido salvas." (`ts:1517-1556`). Não executa se não houver nenhuma pessoa alocada (`ts:1519`).
- "Controles de Zoom": botão diminuir (`title="Diminuir zoom"`), percentual atual, botão aumentar (`title="Aumentar zoom"`), botão "100%" (`title="Resetar zoom"`). Faixa 50%–150%, passo de 10% (`ts:72-76`, `:182-205`). Em telas de largura ≤ 1440 px aplica zoom automático proporcional (`ts:154-177`).

**"Buscar pessoa na mesa..."** (`html:49-78`)
- Pesquisa, a cada tecla, entre as pessoas **já assentadas**: em A casa por `nomeCompleto`, `codinome` ou `nomeLegenda` (minúsculas; com acento) nas áreas A, B, C, D, G e E, e só por nome/codinome nas grades F e H (`ts:1244-1319`).
- Resultado: "{n} pessoa(s) encontrada(s)" e uma linha por pessoa com o nome e a localização, no formato "{área} - {cadeira}[ - {legenda}]", sendo as áreas "Mesa Principal - Cabeçalho", "Mesa Principal - Lateral Esquerda", "Mesa Principal - Lateral Direita", "Mesa Principal - Rodapé", "Seção G", "Seção E", "Assentos Laterais F", "Seção H" (`ts:1255-1264`); `title` "Localizado em: {localização}". Sem resultado: "Nenhuma pessoa encontrada nos assentos". Botão "×" (`title="Limpar busca"`).
- **Destaque**: clicar num resultado aplica ao assento a classe `highlight-pulse` (borda pulsando entre azul e laranja, com leve aumento — `retangular.component.css:944-966`), rola a tela até o assento (centralizado, suave), dá um aumento momentâneo de 10% por 500 ms e remove o destaque após **5 segundos** (`ts:1321-1410`).

**Atualização periódica**: o mapa não consulta sozinho; ele recebe a lista da tela-mãe, que consulta a cada 3 s e só repassa quando algo mudou (4.12). Ao receber, remonta o mapa inteiro a partir do servidor (`ts:83-91`).

**Exportação** (seção "Exportações" — `html:447-471`; feita no navegador com `html2canvas` e `jsPDF`, sem chamada ao backend)

| Grupo / botão (`title`) | O que gera | Nome do arquivo | Ref. |
|---|---|---|---|
| "Mapa Completo:" → "PDF" ("Exportar mapa completo em PDF") / "PNG" ("Exportar mapa completo em PNG") | imagem do mapa inteiro (mesa + setores laterais, sem zoom e sem os botões "×") ao lado de um painel com: nome do evento, data por extenso com dia da semana, "Local: {local}", "Estatísticas", "• Pessoas Alocadas: {n}", "• Pessoas Disponíveis: {n}", "• Total de Participantes: {n}", "Gerado em: {data} às {hora}" | `Mapa_Mesa_Completo_{nome do evento ou "Evento"}_{ddMMyyyy_HHmm}.pdf` / `.png` | `ts:1914-1973`, `:2119-2268` |
| "Mesa do Presidente:" → "PDF" ("Exportar mesa do presidente em PDF") / "PNG" ("Exportar mesa do presidente em PNG") | página A4 retrato com: nome do evento, "Mesa Principal - {data}", **somente a mesa principal** (A, B, C, D), coluna "Legenda" (todas as legendas, sem contagem), "Status" ("Check-in realizado" / "Check-in pendente") e "Gerado automaticamente em {data hora}" | `Mesa_Presidente_{nome do evento ou "Evento"}_{ddMMyyyy_HHmm}.pdf` / `.png` | `ts:1978-2037`, `:2274-2526` |

- PDF sempre A4; mapa completo em paisagem ou retrato conforme a proporção; mesa do presidente sempre retrato (`ts:2042-2092`).
- Mensagens: "Exportação" / "Preparando exportação do mapa completo..." ou "Preparando exportação para o presidente..."; sucesso "Mapa completo exportado em PDF com sucesso!" (ou "PNG"), "Mesa do presidente exportada em PDF com sucesso!" (ou "PNG"); erro "Erro ao exportar o mapa. Tente novamente." / "Erro ao exportar a mesa do presidente. Tente novamente.".
- Impressão direta (window.print): não encontrado no front.

### 5.3 Diferenças (a) administrador × Secretaria Mesa

Comparação entre A/B (`app-mesa`) e C/D (`app-mesa-recepcionista-checkin`).

| Aspecto | Administrador (A, B) | Secretaria Mesa (C, D) | Ref. |
|---|---|---|---|
| Edição do mapa | arrastar-e-soltar, clique para selecionar pessoa, botão "×" | **somente leitura**: os assentos não têm eventos de arrastar, soltar ou clicar, nem botão "×" | D `html:154-359`; C `html` (nenhum `(drop)`, `draggable` ou `(click)` em assento) |
| Painel "Gerenciar Pessoas Alocadas na Mesa" ("Salvar Alocações", "Limpar Todas", zoom) | presente (exceto tablet) | **ausente** | D `html:120-150` |
| Seção "Exportações" | presente | **ausente** | D `html:396-421` |
| Quem aparece em "Pessoas Disponíveis" | participantes **sem assento** | participantes **com check-in realizado**, ainda **não atendidos** (`!statusAtendido`) e não atendidos nesta sessão — **tenham ou não assento** | A `ts:423-427`; D `ts:447-454`; C `ts:497-504` |
| Cartão da pessoa | nome, histórico, cargo, organização, etiqueta de legenda, etiqueta de check-in; arrastável | foto (miniatura) ou ícone de pessoa; nome; `nomeFantasia` ou `razaoSocial`; etiqueta com a **identificação do assento** (azul) ou "Não alocado" (vermelha); botão de atendimento | D `html:24-62`; D `ts:2665-2680`; css `:388-398` |
| Foto | não | `GET {baseUrl}administracao/arquivos/{arquivoId}/thumbnail` (blob) para cada participante com `arquivoId` | D `ts:2708-2734`; `evento-pessoa.service.ts:45-48` |
| Clicar na etiqueta do assento do cartão | — | localiza o assento da pessoa e aplica o destaque (mesmo efeito da busca) | D `html:52`; D `ts:1348-1353`; C `html:60` |
| **"Atender"** | não existe | botão com `title="Atender Pessoa"` e texto **"ATENDIDO"** (lista, desktop) ou **"ATENDER"** (carrossel, tablet) → `EventoPessoaService.atenderPessoa(id)` = `PUT {baseUrl}administracao/evento-pessoas/{id}/atender` (corpo `{}`); sucesso "Sucesso" / "Pessoa atendida com sucesso" e a pessoa sai da lista; erro "Erro" / "Erro ao atender pessoa". Sem confirmação | D `html:57-61`, `:109-113`; D `ts:2682-2703`; C `ts:1494-1516`; `evento-pessoa.service.ts:40-43` |
| Layout em tablet | o painel de controle é ocultado | a lista vira um carrossel horizontal (3 itens visíveis; 2 abaixo de 768 px) | D `html:66-117`; D `ts:52-63` |
| Busca na mesa | por nome/codinome (em A também por legenda) | por nome/codinome **ou por identificação de cadeira**: se o termo casar com `^[A-H]\d+$` (ex.: "B15") procura o ocupante daquela cadeira e já o destaca automaticamente | D `ts:1274-1305`, `:1358-1424`; C `ts:946-978`, `:1030` |
| Atualização automática | recebe a lista a cada mudança (3 s) | idem, com o indicador "Atualização automática ativa" na tela-mãe | 4.12 |
| Detecção de tablet | sim (oculta o painel de controle) | sim (troca lista por carrossel) | A `ts:143-149`; C `ts:152-159` |

Tablet = *user agent* com `tablet|ipad|android (sem mobile)|kindle|silk` ou largura entre 768 e 1024 px (A `ts:143-149`).

Particularidades de **C** (Secretaria Mesa, retangular) frente a **D**:
- Não tem zoom (nem automático) nem a janela "Selecionar Pessoa"; o campo de busca tem o placeholder "Buscar pessoa na mesa..." (D: "Buscar pessoa na mesa ou cadeira (ex: A3, B15)..."), embora a busca por cadeira exista no código de C (`retangular-recepcionista-checkin.component.html:134`; `.ts:958-964`).
- Contém um `p-confirmDialog` com cabeçalho "Remover Usuário" e botões "Remover"/"Cancelar" que nenhum código aciona (`retangular-recepcionista-checkin.component.html:1-6`).
- Contém `initializeCadeiras()`, nunca chamado, com um mapa fixo de setores ("MEI - Comitê Estratégico", "GT MEI - Coordenadores", "MEI Empresas presidentes", "MEI Empresas Vice-presidentes", "MEI-Gov - Presi", "MEI-Empresas - diretores", "GT MEI - Titulares", "MEI - ICT - Reitores", "MEI - ICT | Governo") por cadeira (`.ts:277-374`).

Em **D** permanece no `.ts` todo o código de edição herdado de B (arrastar, salvar, limpar, exportar, zoom manual), mas o template não o aciona; a janela "Selecionar Pessoa" está no template de D, porém nada a abre (D `html:363-392`, `:424-453`).

### 5.4 Diferenças (b) retangular × retangular invertido

| Aspecto | Retangular (A, C) | Retangular invertido (B, D) | Ref. |
|---|---|---|---|
| Disposição (esquerda → direita) | F, G, H empilhados → mesa principal → coluna E | **coluna E → mesa principal → F, G, H empilhados** (espelhado) | A `html:123-384`; B `html:121`, `:154`, `:273`, `:309`, `:339` |
| Laterais B e C | B1–B35, C1–C35 (35 cada) | B1–B34, C1–C34 (34 cada) | A `ts:32-33`; B `ts:32-33` |
| Setor F | F1–F32 (8 × 4) | F1–F28 (7 × 4) | A `ts:36`, `:1846`; B `ts:36`, `:1833` |
| Setor G | G1–G10 | G1–G10 (igual) | A `ts:37`; B `ts:37` |
| Setor H | H1–H36 (9 × 4) | H1–H28 (7 × 4) | A `ts:38`; B `ts:38` |
| Setor E | E1–E23 | E1–E30 | A `ts:39`, `:1894`; B `ts:39`, `:1881` |
| Cabeçalho A e rodapé D | A1–A5, D1–D5 | iguais | — |
| Total de posições | 181 | 5+34+34+5+28+10+28+30 = **174** | — |
| Busca na mesa (admin) | A: nome, codinome e legenda; localização inclui a legenda | B: só nome e codinome; placeholder "Buscar pessoa na mesa ou cadeira (ex: A3, B15)..." mas **sem** busca por cadeira no código de B | A `ts:1267-1290`; B `ts:1269-1278`; B `html:51` |
| "(histórico)" dentro do assento | só no setor E | só no setor E | A `html:371`; B `html:135` |
| Exportação "mesa do presidente" | fonte da legenda 10 px | B: 10 px; D: 7–8 px (código sem uso em D) | diff B×D |

Tudo o mais (regras de alocação, salvamento, cores, legenda, destaque, exportação) é idêntico entre A e B — o `diff` dos dois `.ts` só acusa os tamanhos acima, a função de busca e a posição de um trecho de estilo da exportação.

---

## 6. Serviços → endpoints

Legenda: `{baseUrl}` = `environment.baseUrl` (API do próprio sistema, `…/api-mesa-checkin/`); `urls.X` = URL do **serviço corporativo** obtida de `GET {baseUrl}servicos/corporativo` (o valor não está no front); `{adm}` = `servicos.modulos.administracao`; `{proj}` = `servicos.modulos.projeto` (ambos de `GET {baseUrl}servicos/privado`). Coluna "Uso": **Sim** = chamado por tela ativa; **Não** = sem chamador no front (ou chamador é componente sem uso).

### 6.1 Infraestrutura e autenticação

| Serviço#método | Verbo | URL | Uso | Ref. |
|---|---|---|---|---|
| `ServicosService#buscarUrlsCached` | GET | `{baseUrl}servicos/corporativo` | Sim (guard) | `servicos.service.ts:33-40` |
| `ServicosService#buscarModulosCached` | GET | `{baseUrl}servicos/privado` | Sim (guard) | `servicos.service.ts:49-56` |
| `AuthService#login` | POST | `urls.urlAutenticacaoSistemaV2` (corpo `{informacoes}`) | Sim | `auth.service.ts:47-56` |
| `AuthService#refreshToken` | POST | derivada de `urlAutenticacaoSistema` (nunca atribuída) | Não | `auth.service.ts:63-74` |
| `AuthService#alterarSenha` | PUT | `urls.urlAlteracaoSenha` (`{login}`) | Sim | `auth.service.ts:76-82` |
| `AuthService#recuperarSenha` | POST | `urls.urlRecuperacaoSenha` (`{login}`) | Sim | `auth.service.ts:96-102` |
| `AuthService#buscarImagemUsuario` | GET | `urls.urlPesquisaUsuarios` + `{usuario.id}` + `/foto` | Sim (topbar) | `auth.service.ts:90-94` |
| `AuthService#alterarImagem` | PUT | idem | Não (sem tela) | `auth.service.ts:84-88` |
| `LoginComponent` (direto) | GET | `{baseUrl}administracao/eventos/evento-principal` | Sim | `login.component.ts:69` |

### 6.2 Usuários (serviço corporativo)

| Serviço#método | Verbo | URL | Uso | Ref. |
|---|---|---|---|---|
| `UsuarioAcessoService#listar2` | GET | `urls.urlPesquisaUsuariosSistema` (`entidade`, `departamento`, `unidade`, `perfil`, `area`, `nome`, `login`) | Sim | `usuario-acesso.service.ts:14-27` |
| `UsuarioService#buscarPorLogin` | GET | `urls.urlPesquisaUsuarioLogin` (`{login}`) | Sim | `usuario.service.ts:15-21` |
| `UsuarioService#buscarBasi` | GET | `urls.urlPesquisaUsuarioSistemaCodigoUsuario` (troca `'{codigoUsuario}/'` pelo código) | Sim | `usuario.service.ts:28-31` |
| `UsuarioService#criar` (herdado) | POST | `urls.urlNovoUsuarioSistema` | Sim | `http-crud.service.ts:37-40` |
| `UsuarioService#atualizar` (herdado) | PUT | `urls.urlAtualizaUsuarioSistema` (`{codigoUsuario}`) | Sim | `http-crud.service.ts:42-45` |
| `UsuarioService#remover` (herdado) | DELETE | `urls.urlAtualizaUsuarioSistema` (`{codigoUsuario}`) | Sim | `http-crud.service.ts:52-55` |
| `PerfisAcessoService#listar` | GET | `urls.urlPerfisSistema` | Sim | `perfis-acesso.service.ts:18-21` |
| `EntidadeService#listar` | GET | `urls.urlEntidadesSistema` | Sim | `entidade.service.ts:24-27` |
| `DepartamentoRegionalService#listar` | GET | `urls.urlDepartamentosSistema` (`{codigoEntidade}`, `?data=timestamp`) | Sim (Instituições Relacionadas) | `departamento-regional.service.ts:23-27`, `:38-46` |
| `UnidadeService#listar` | GET | `urls.urlUnidadesSistema` (`{codigoEntidade}`, `{codigoDepartamento}`) | Não efetivo (chamada comentada / nunca alcançada) | `unidade.service.ts:18-25`, `:46-53` |
| `UsuarioService#mudarSituacao` | PATCH | `{adm}/api/usuarios/{codigo}` | Não (método da lista sem botão) | `usuario.service.ts:93-96` |
| `UsuarioService#buscar` (herdado) | GET | `{adm}/api/usuarios/{codigo}` | Não (idem, "copiar") | `http-crud.service.ts:17-20` |
| `UsuarioService#buscarUsuario` | GET | `{adm}/api/usuarios-combo/{codigo}` | Não | `usuario.service.ts:23-26` |
| `UsuarioService#buscarPorCodigoNoSistema` | GET | `urls.urlPesquisaUsuarioSistemaCodigoUsuario` | Não | `usuario.service.ts:33-39` |
| `UsuarioService#listarCorporativo` | GET | `urls.urlPesquisaUsuariosSistema` | Não | `usuario.service.ts:41-55` |
| `UsuarioService#listarUsuariosParaResponsaveis` / `listarUsuarios` / `listarUsuariosDropdown` | POST | `{adm}/api/usuarios-filtro[/]` | Não | `usuario.service.ts:57-75` |
| `UsuarioService#listarResponsaveisProjeto` | GET | `{proj}/api/projetos/{id}/usuarios-gestores-dr/` | Não | `usuario.service.ts:81-86` |
| `UsuarioService#listarModalidadesFomentosLinhas` | GET | `{adm}/api/usuarios/modalidade-fomento-linha` | Não (só componente sem uso) | `usuario.service.ts:88-91` |
| `UsuarioService#listarModalidadesProjeto`, `listarModalidades`, `listarFomentos`, `listarLinhas`, `listarModalidadesDr`, `listarFomentosDr`, `listarLinhasDr` | GET | `{adm}/api/usuarios/modalidades…`, `…/modalidade/{m}/fomentos`, `…/fomento/{f}/linhas`, `…-projeto/…/relacao-drs/{dr}` | Não | `usuario.service.ts:98-145` |
| `EntidadeService#listarComDepartamentos` | GET | `{adm}/api/entidades/` | Não | `entidade.service.ts:33-38`, `:55-58` |
| `AreasPerfisService#listar2` | GET | `{adm}/api/areas-negocio-perfis` | Não | `areas-perfis.service.ts:18-21` |
| `AreaService#listarAreas` / `listarTabelaRepasseLinha` | GET | `{adm}/api/areas-negocio/`, `…/{codigoArea}/tabelas-repasse` | Não | `area.service.ts:17-25` |
| `PerfisService`, `CategoriaTipoAtendimentoService`, `ConfiguracoesIndicadorService` (só `baseUrl`) | — | `{adm}/api/perfis`, `{adm}/api/categorias-tipo-atendimento/`, `{adm}/api/configuracoesIndicador` | Não | `perfis.service.ts:15`; `categoria-tipo-atendimento.service.ts:14-15`; `configuracoes-indicador.service.ts:14` |
| `MensagensService`, `NotificacaoService` (só `baseUrl`) | — | `urls.urlNotificacoesSistema` | Não | `mensagens.service.ts:14`; `notificacao.service.ts:13` |
| `HintService#buscar` (herdado) | GET | `{adm}/api/ajudas/{id}` | Só via botões de ajuda de "Instituições Relacionadas" | `hint.service.ts:14`; `http-crud.service.ts:17-20` |

Base genérica `HttpCrudService` (`http-crud.service.ts:17-60`): `buscar` GET `baseUrl+codigo`; `listar2` GET `baseUrl`; `copiar` POST `baseUrl+codigo+'/copias'`; `desativar` PUT `baseUrl+codigo+'/desativados'`; `salvar` PUT `baseUrl`; `mudarStatus` PATCH `baseUrl+codigo`; **`criar`, `atualizar` e `remover` apontam para as URLs corporativas de usuário** e valem para todo serviço que não os sobrescreva.

### 6.3 Pessoas

| Serviço#método | Verbo | URL | Uso | Ref. |
|---|---|---|---|---|
| `PageHelper.findPage` (em `pessoas-list`) | GET | `{baseUrl}administracao/pessoas` (`rows`, `sort`, `direction`, `first`, `nomeCompleto`, `crm`, `razaoSocial`, `email`) | Sim | `pessoas-list.component.ts:101-108`; `page-helper.ts:36-61` |
| `FormHelper.findOne` (em `pessoa`) | GET | `{baseUrl}administracao/pessoas/{id}` | Sim | `pessoa.component.ts:90-94`; `form-helper.ts:34-42` |
| `FormHelper.save` (em `pessoa`) | POST | `{baseUrl}administracao/pessoas` | Sim (inclusão e edição) | `pessoa.component.ts:228`; `form-helper.ts:44-52` |
| `FormHelper.delete` (em `pessoas-list`) | DELETE | `{baseUrl}administracao/pessoas/{id}` | Sim | `pessoas-list.component.ts:135-139`; `form-helper.ts:75-83` |
| `PessoaService#findAnexo` | GET | `{baseUrl}administracao/pessoas/anexos/{id}` | Sim | `pessoa.service.ts:42-45` |
| `PessoaService#processaCargaGt` | POST | `{baseUrl}administracao/pessoas/carga/gt` | Sim | `pessoa.service.ts:47-50` |
| `PessoaService#processaCargaTema` | POST | `{baseUrl}administracao/pessoas/carga/tema` | Sim | `pessoa.service.ts:52-55` |
| `PessoaService#processaCargaHistorico` | POST | `{baseUrl}administracao/pessoas/carga/historico` | Sim | `pessoa.service.ts:57-60` |
| `PessoaService#findAll` / `findById` / `create` / `update` / `delete` | GET / GET / POST / PUT / DELETE | `{baseUrl}administracao/pessoas[/{id}]` | Não (as telas usam os *helpers*) | `pessoa.service.ts:19-40` |

### 6.4 Eventos, participantes e mesa

| Serviço#método | Verbo | URL | Uso | Ref. |
|---|---|---|---|---|
| `PageHelper.findPage` (em `evento-list`) | GET | `{baseUrl}administracao/eventos` (`rows`, `sort`, `direction`, `first`, `nome`, `local`, `tipoEvento`, `tipoMesa`, `dataInicial`, `dataFinal`) | Sim | `evento-list.component.ts:83-91` |
| `PageHelper.findPage` (tipos de evento) | GET | `{baseUrl}administracao/tipo-eventos` | Sim | `eventos-filter.component.ts:71`; `evento-create.component.ts:86-94` |
| `PageHelper.findPage` (tipos de mesa) | GET | `{baseUrl}administracao/tipo-mesas` | Sim | `eventos-filter.component.ts:86`; `evento-create.component.ts:100-108` |
| `FormHelper.findOne` | GET | `{baseUrl}administracao/eventos/{id}` | Sim (formulário, participantes, legendas) | `evento-create.component.ts:69-73`; `evento-pessoa.component.ts:87-91`; `configuracao-legendas-evento.component.ts:155` |
| `FormHelper.save` | POST | `{baseUrl}administracao/eventos` | Sim (inclusão e edição) | `evento-create.component.ts:177` |
| `FormHelper.delete` | DELETE | `{baseUrl}administracao/eventos/{id}` | Sim | `evento-list.component.ts:117-121` |
| `EventosService#atualizarEventoPrincipal` | POST | `{baseUrl}administracao/eventos/{id}/principal` | Sim | `evento.service.ts:83-86` |
| `EventosService#getEventoPrincipal` | GET | `{baseUrl}administracao/eventos/evento-principal` | Não (o login chama a URL direto) | `evento.service.ts:88-91` |
| `EventosService#findAnexo` | GET | `{baseUrl}administracao/eventos/anexos/{id}` | Sim | `evento.service.ts:26-29` |
| `EventosService#processaCargaConvidados` | POST | `{baseUrl}administracao/eventos/{id}/carga/convidados` | Sim | `evento.service.ts:36-39` |
| `EventosService#processaCargaConfirmados` | POST | `{baseUrl}administracao/eventos/{id}/carga/confirmados` | Sim | `evento.service.ts:41-44` |
| `EventosService#importarInscritosCrm` | POST | `{baseUrl}administracao/eventos/{id}/carga/crm` | Sim | `evento.service.ts:46-48` |
| `EventosService#salvarPessoaCadastroRapido` | POST | `{baseUrl}administracao/eventos/{id}/cadastro-rapido` | Sim | `evento.service.ts:78-81` |
| `EventosService#realizaCheckinParticipante` | PUT | `{baseUrl}secretaria/checkin/participante` (perfil "Secretaria Check-In") **ou** `{baseUrl}administracao/eventos/participante/checkin` | Sim | `evento.service.ts:55-61` |
| `EventosService#realizaConfirmacaoParticipante` | PUT | `{baseUrl}administracao/eventos/participante/confirmacao` | Sim | `evento.service.ts:63-66` |
| `EventosService#imprimirParticipantes` | GET | `{baseUrl}administracao/eventos/participantes/excel` | Sim | `evento.service.ts:93-100` |
| `EventosService#findCadeiras` | GET | `{baseUrl}administracao/eventos/{id}/cadeiras` | Sim (mapa) | `evento.service.ts:31-34` |
| `EventosService#salvarComposicoesMesa` | POST | `{baseUrl}administracao/eventos/{id}/composicoes-mesa` | Sim (mapa do administrador) | `evento.service.ts:68-71` |
| `EventosService#carregarComposicoesMesa` | GET | `{baseUrl}administracao/eventos/{id}/composicoes-mesa` | Não | `evento.service.ts:73-76` |
| `EventosService#findParticipantesEvento` | GET | `{baseUrl}administracao/eventos/{id}/participantes` | Não | `evento.service.ts:50-53` |
| `EventoPessoaService#pesquisaParticipantes` | GET | `{baseUrl}administracao/evento-pessoas` (`idEvento`, `first`, `size`, `sortField`, `sortOrder`, `termoBusca`, `gruposTrabalho`, `temas`, `cargos`, `legendas`, `convidado`, `confirmado`, `checkin`, `hasFoto`) | Sim | `evento-pessoa.service.ts:16-18` |
| `EventoPessoaService#findParticipantesMesa` | GET | `{baseUrl}administracao/evento-pessoas/mesa/participantes` (`idEvento`, `isSecretariaCheckin`) | Sim | `evento-pessoa.service.ts:35-38` |
| `EventoPessoaService#findGruposTrabalho` | GET | `{baseUrl}administracao/evento-pessoas/grupos-trabalho` | Sim | `evento-pessoa.service.ts:20-23` |
| `EventoPessoaService#findTemas` | GET | `{baseUrl}administracao/evento-pessoas/temas` | Sim | `evento-pessoa.service.ts:25-28` |
| `EventoPessoaService#findCargos` | GET | `{baseUrl}administracao/evento-pessoas/cargos` | Sim | `evento-pessoa.service.ts:30-33` |
| `EventoPessoaService#atenderPessoa` | PUT | `{baseUrl}administracao/evento-pessoas/{id}/atender` | Sim (mapa da Secretaria Mesa) | `evento-pessoa.service.ts:40-43` |
| `EventoPessoaService#getArquivoThumbnail` | GET (blob) | `{baseUrl}administracao/arquivos/{arquivoId}/thumbnail` | Sim (mapa da Secretaria Mesa) | `evento-pessoa.service.ts:45-48` |

### 6.5 Legendas

| Serviço#método | Verbo | URL | Uso | Ref. |
|---|---|---|---|---|
| `EventoLegendaService#buscarConfiguracao` | GET | `{baseUrl}administracao/eventos/{eventoId}/legendas` | Sim | `evento-legenda.service.ts:25-27` |
| `EventoLegendaService#salvarConfiguracao` | PUT | `{baseUrl}administracao/eventos/{eventoId}/legendas` | Sim | `evento-legenda.service.ts:30-32` |
| `EventoLegendaService#simular` | POST | `{baseUrl}administracao/eventos/{eventoId}/legendas/simular` | Sim | `evento-legenda.service.ts:35-37` |
| `EventoLegendaService#executar` | POST | `{baseUrl}administracao/eventos/{eventoId}/legendas/executar` | Sim | `evento-legenda.service.ts:40-42` |
| `EventoLegendaService#listarOrigens` | GET | `{baseUrl}administracao/eventos/legendas/origens` (`excluirEventoId`) | Sim | `evento-legenda.service.ts:45-51` |
| `EventoLegendaService#buscarLegendaParticipante` | GET | `{baseUrl}administracao/eventos/participante/{eventoPessoaId}/legenda` | Sim | `evento-legenda.service.ts:54-56` |
| `EventoLegendaService#atualizarLegendaParticipante` | PUT | `{baseUrl}administracao/eventos/participante/legenda` | Sim | `evento-legenda.service.ts:59-61` |
| `LegendaCatalogoService#listarTodos` | GET | `{baseUrl}administracao/legendas` (`first`, `rows`, `sort`, `direction`, `nomeLegenda`) | Sim | `legenda-catalogo.service.ts:45-53` |
| `LegendaCatalogoService#criar` | POST | `{baseUrl}administracao/legendas` | Sim | `legenda-catalogo.service.ts:32-34` |
| `LegendaCatalogoService#atualizar` | PUT | `{baseUrl}administracao/legendas/{id}` | Sim | `legenda-catalogo.service.ts:36-38` |
| `LegendaCatalogoService#remover` | DELETE | `{baseUrl}administracao/legendas/{id}` | Sim | `legenda-catalogo.service.ts:40-42` |
| `LegendaCatalogoService#buscarUso` | GET | `{baseUrl}administracao/legendas/{id}/uso` | Sim | `legenda-catalogo.service.ts:56-58` |
| `LegendaCatalogoService#listarPresets` | GET | `{baseUrl}administracao/legendas/presets` | Sim | `legenda-catalogo.service.ts:61-63` |
| `LegendaCatalogoService#buscarPreset` | GET | `{baseUrl}administracao/legendas/presets/{id}` | Sim | `legenda-catalogo.service.ts:66-68` |
| `LegendaCatalogoService#salvarPreset` | POST | `{baseUrl}administracao/legendas/presets` | Sim | `legenda-catalogo.service.ts:71-73` |
| `LegendaCatalogoService#removerPreset` | DELETE | `{baseUrl}administracao/legendas/presets/{id}` | Sim | `legenda-catalogo.service.ts:76-78` |

*Helpers* sem uso: `FormHelper.update` (PUT), `FormHelper.saveAll` (POST `…/all`), `PageHelper.download` (GET blob) (`form-helper.ts:54-73`; `page-helper.ts:63-87`).

---

## 7. Enums e listas fixas do front

### 7.1 Em uso por telas ativas

| Nome | Valores → rótulos | Onde é usado | Ref. |
|---|---|---|---|
| `Sexo` / `SEXO_OPTIONS` | `MASCULINO` → "Masculino"; `FEMININO` → "Feminino"; `NAO_INFORMADO` → "Não informado" | Pessoa, aba Cadastro, campo "Sexo" | `sexo.enum.ts:3-13` |
| `Estado` / `ESTADO_OPTIONS` | AC, AL, AP, AM, BA, CE, DF, ES, GO, MA, MT, MS, MG, PA, PB, PR, PE, PI, RJ, RN, RS, RO, RR, SC, SP, SE, TO (rótulo = valor) | Pessoa: "Estado" (cadastro) e "Estado" (perfil corporativo) | `estado.enum.ts:3-36` |
| `TipoPerfil` | `DN`, `DR`, `UA` (sem rótulos) | Usuário → Instituições Relacionadas | `tipo-perfil.enum.ts:1-5` |
| Ids de perfil aceitos | `"SMC.1"`, `"SMC.2"`, `"SMC.5"` | filtro e formulário de usuário | `usuarios-filter.component.ts:75`; `usuario.component.ts:120` |
| Nomes de perfil comparados | `'Administrador'`, `'Gestor'`, `'Secretaria Mesa'`, `'Secretaria Check-In'` | ver 2.3 | — |
| `CAMPOS_CONDICAO` | `grupoTrabalho` → "Grupo de trabalho"; `tema` → "Tema"; `cargo` → "Cargo"; `nomeFantasia` → "Nome fantasia"; `papelDesempenhado` → "Papel desempenhado" | condição de legenda | `legenda.interface.ts:134-140` |
| `OPERADORES_CONDICAO` | `IGUAL` → "Igual a"; `DIFERENTE` → "Diferente de"; `CONTEM` → "Contém"; `EM` → "Em (lista)" | condição de legenda | `legenda.interface.ts:143-148` |
| `CONECTIVOS` | `E` → "E"; `OU` → "OU" | condição de legenda | `legenda.interface.ts:151-154` |
| Modo de carga de configuração | `substituir` → "Substituir configuração atual"; `mesclar` → "Mesclar (adicionar blocos ausentes)" | diálogo "Carregar configuração" | `carregar-configuracao-dialog.component.html:7-12` |
| Paleta de cores de bloco | 16 cores `#RRGGBB` (lista em 4.18) | formulário de bloco | `bloco-form.component.ts:32-36` |
| Filtros tri-estado de participante | `todos` → "Todos"; `sim` → "Sim"; `nao` → "Não" (para "Convidado", "Confirmado", "Check-In") | filtro de participantes | `evento-pessoas-filter.component.html:106-221` |
| Indicador de tipo de mesa | `'RETANGULAR'`, `'RETANGULAR_INVERTIDO'` (valores de `tipoMesa.indicador`) | escolha do desenho do mapa | `mesa.component.html:1`, `:5` |
| Composição da cadeira | `'PRINCIPAL'`, `'LATERAL'` | mapa de assentos | `retangular.component.ts:266-267` |
| Constantes de legenda da mesa | `COR_LEGENDA_PADRAO = '#f8f9fa'`; `NOME_ASSENTO_LIVRE = 'Assento livre'` | mapa, lista de participantes | `legenda-mesa.helper.ts:11`, `:14` |
| Setores por letra de cadeira | "Anfitrião", "Palestrantes", "Presidência", "Deputados Federais", "Senadores", "Convidados Especiais", "Governadores", "Imprensa", "Assessoria", "Segurança", "Técnicos", "Outros" (regra em 5.2) | dica do assento | `retangular.component.ts:296-313` |
| Constantes de endpoint | `PESSOA_ENDPOINT = 'administracao/pessoas'`; `EVENTO_ENDPOINT = 'administracao/eventos'`; `TIPO_EVENTO_ENDPOINT = 'administracao/tipo-eventos'`; `TIPO_MESA_ENDPOINT = 'administracao/tipo-mesas'` | *helpers* de página/formulário | `pessoa.interface.ts:3`; `evento.interface.ts:4-6` |
| `Genero` | `masculino = 'M'`, `feminino = 'F'` | concordância das mensagens de `ListBase` | `genero.enum.ts:1-4` |
| `Situacao` | `A`, `I` | `ListBase.mudarStatus` (sem tela) | `situacao.enum.ts:1-4` |
| Conversores | `AtivoInativoConverter`: `true` → "Ativo", `false` → "Inativo"; `DateStringWithoutTimeConverter`: data sem hora | lista de usuários / pessoas | `ativo-inativo-converter.ts:4-12`; `date-converter.ts:62-74` |
| Locale de calendário | dias, meses, "Hoje", "Limpar" | `p-datePicker` do filtro de eventos | `form-component-base.ts:10-53` |
| `MenuOrientation` | `STATIC`, `OVERLAY`, `SLIM`, `HORIZONTAL` (fixo em `HORIZONTAL`) | *shell* | `admin.component.ts:10-15`, `:25` |

Listas vindas de **endpoint** (não fixas): tipos de evento, tipos de mesa, perfis, entidades, departamentos regionais, legendas (catálogo), temas, grupos de trabalho, cargos, presets, eventos de origem.

### 7.2 Declarados e sem uso em tela

| Nome | Valores | Ref. |
|---|---|---|
| `situacao` (filtro de eventos) | "Todos" (`''`), "Ativo" (`true`), "Inativo" (`false`) | `eventos-filter.component.ts:22-26` |
| `statusOptions` (lista de participantes) | "Confirmado" (`true`), "Não confirmado" (`false`), "Pendente" (`null`) | `evento-pessoas-list.component.ts:25-29` |
| `opcoesVisualizacao` | "Participante" (`Participante`), "Mapa de Assentos" (`Mapa`) | `evento-pessoa.component.ts:24-27` |
| `meses` (`FormBase`) | Janeiro=1 … Dezembro=12 | `form-base.ts:15-28` |
| `AporteFinanceiro` | `PERCENTUAL`, `NOMINAL` | `aporte-financeiro.enum.ts:1-4` |
| `Campo` | `O` (obrigatório), `V` (visível), `I` (invisível) | `campo.enum.ts:1-5` |
| `Categoria` | `ESTIMULO PRODUCAO`, `PROJETO`, `PRONATEC` | `categoria.enum.ts:1-5` |
| `Categorias` | `projetos = 1`, `estimulosProducao = 2`, `atendimentosPronatec = 3` | `categorias.enum.ts:1-5` |
| `Modalidades` | `projetos = 1`, `auxilio = 2`, `estimuloProducao = 3`, `regulamentares = 4`, `terceiros = 5`, `convenio = 6`, `atendimentosPronatec = 7`, `termoDeAjusteAdministrativo = 8` | `modalidades.enum.ts:1-10` |
| `TipoApuracao` | `AC`, `VC` | `tipo-apuracao.enum.ts:1-4` |
| `TipoRepasseInicial` | `C`, `M`, `N` | `tipo-repasse-inicial.enum.ts:1-5` |
| `TipoRepasse` | `C`, `F`, `M`, `S`, `U` | `tipo-repasse.enum.ts:1-7` |
| `ARQUIVO_ENDPOINT` | `'arquivos'` | `arquivo.interface.ts:1` |
| `SimNaoConverter`, `AtivoInativoBooleanConverter`, `DateConverter`, `DateTimeConverter`, `DateWithTimeConverter`, `DateWithoutTimeConverter` | "Sim"/"Não"; "Ativo"/"Inativo" (por `value`); formatos de data | `sim-nao-converter.ts`; `ativo-inativo-boolean-converter.ts`; `date-converter.ts:4-60` |
| Setores "MEI" por cadeira | "MEI - Comitê Estratégico", "GT MEI - Coordenadores", "MEI Empresas presidentes", "MEI Empresas Vice-presidentes", "MEI-Gov - Presi", "MEI-Empresas - diretores", "GT MEI - Titulares", "MEI - ICT - Reitores", "MEI - ICT \| Governo" | `retangular-recepcionista-checkin.component.ts:279-315` |
| `src/assets/i18n/pt-BR.json` | traduções do PrimeNG ("Sim", "Não", "Escolher", "Enviar", "Cancelar", dias/meses, "Não há resultados" etc.) — nenhum código carrega esse arquivo | `pt-BR.json:1-48` |

Validadores de `BasicValidators` sem uso em tela: `maxLength`, `minLength`, `maxValue`, `minValue`, `digits`, `datetime`, `cnpj`, `cep`, `numeric`, `integer`, `porcentagem`, `telefone`, `celular`, `ano`, `atLeastOne` (usados: `required`, `password`, `passwordsShouldMatch`, `cpf`, `email`, `date`, `dataInicioDeveSerMenorDataFim`, `obrigatorio`).

---

## 8. Suspeitas

Itens marcados *(inferência)* resultam de leitura do código, sem execução.

### 8.1 Componentes não roteados / sem uso

| Item | Evidência | Ref. |
|---|---|---|
| `AreasComponent` (`app-areas`) | importado e `@ViewChild` em `UsuarioComponent`, mas fora do array `imports` e do template; sem rota | `usuario.component.ts:8`, `:30-44`, `:58-59`; `usuario.component.html` (sem `app-areas`) |
| `LinhasUsuarioComponent` (`app-linhas-usuario`) e `AdicionarLinhasUsuarioComponent` | idem; o segundo só é usado pelo primeiro | `usuario.component.ts:9`, `:60-61`; `linhas-usuario.component.html:2` |
| `ProfileComponent` (`app-inline-profile`) | importado em `AdminComponent`, ausente do template; textos em inglês ("Profile", "Privacy", "Settings", "Logout") | `admin.component.ts:7`, `:22`; `admin.component.html:11-15`; `profile.component.html:14-44` |
| `SubmenuComponent` (`[app-submenu]`) | só referenciado em comentário do menu; importa `LayoutModule` sem declará-lo | `menu.component.html:1`; `submenu.component.ts:33` |
| `FooterComponent`, `AlertaComponent`, `DadosCadastroComponent`, `GaugeComponent`/`GaugeModule`, `ErrorComponent` (`app-error`) | nenhum template os usa (`ErrorComponent` só aparece em `imports`/`@ViewChildren`) | `footer.component.ts:4`; `alerta.component.ts:5`; `dados-cadastro.component.ts:5`; `gauge.component.ts:6`; `form-base.ts:12` |
| `evento-pessoa/mesa/mesa.component.{ts,html,css}` | três arquivos com 0 bytes | listagem de diretório |
| `NaoHaPrincipalComponent` | roteado em `/nao-ha-principal`, mas nenhum código navega para lá | `administracao.routing.ts:57-60` |
| `CrudBase`, `HttpRoutedService`, `GaugeModule` | importam por *alias* `@shared/…`/`@service/…`, que não existe em `tsconfig.json` (sem `paths`); só não quebram o build porque `tsconfig.app.json` compila apenas o que é alcançável de `src/main.ts` | `crud-base.ts:1-10`; `http-routed.service.ts:4-5`; `gauge.module.ts:3`; `tsconfig.app.json` |
| `SituacaoPipe`, `FiltroUsuariosPipe` | o primeiro sem uso; o segundo só listado em `providers` | `situacao.pipe.ts:3-6`; `usuarios.component.ts:16` |
| Serviços `AreaService`, `AreasPerfisService`, `PerfisService`, `CategoriaTipoAtendimentoService`, `ConfiguracoesIndicadorService`, `MensagensService`, `NotificacaoService` | sem chamador ativo (ver 6.2) | `service/cached/*`, `service/crud/*` |
| Métodos de `UsuarioService` de modalidade/fomento/linha/projeto, `mudarSituacao`, `copiar` | sem chamador ativo | `usuario.service.ts:57-145`; `usuarios-list.component.ts:104-129` |
| `PessoaService` CRUD (`findAll`…`delete`), `EventosService#findParticipantesEvento`/`carregarComposicoesMesa`/`getEventoPrincipal`, `FormHelper.update`/`saveAll`, `PageHelper.download`, `AuthService#refreshToken` | sem chamador | ver 6 |
| Janela "Selecionar Pessoa" e todo o código de edição/exportação em D (mapa da Secretaria Mesa, invertido) | presentes no `.ts`/`.html`, sem acionador no template | `retangular-invertido-recepcionista-checkin.component.html:363-392`, `:424-453` |
| `initializeCadeiras()` em C | nunca chamado | `retangular-recepcionista-checkin.component.ts:277-374` |
| `p-confirmDialog` "Remover Pessoa" na lista de pessoas e "Remover Usuário" em C | nenhum `confirmationService.confirm` os aciona nessas telas | `pessoas-list.component.html:1-6`; `retangular-recepcionista-checkin.component.html:1-6` |

### 8.2 Sobras de template / sistema anterior

- `<title>Projeto - Base</title>` (`index.html:5`); dependência `"projeto-base": "file:"` (`package.json:55`); `README.md` com o texto-modelo do Azure DevOps (só "TODO: …"); URLs comentadas `…/api-projeto-base/` nos ambientes (`environment.development.ts:3`, `environment.homolog.ts:3`); `src/upload.php` ("Fake Upload Process"); comentário no `Dockerfile` citando `environment.prod.ts`, que não existe.
- Vocabulário de outro sistema (apoio financeiro / projetos — "SGF"): enums `AporteFinanceiro`, `Campo`, `Categoria`, `Categorias`, `Modalidades`, `TipoApuracao`, `TipoRepasse`, `TipoRepasseInicial` (7.2); "Linha(s) de Apoio Financeiro", "Linha de Transferência", "Áreas de Negócio" (4.3); comentário `http://localhost:8087/sgf-projeto/api/projetos/545/usuarios-gestores-dr?` (`usuario.service.ts:84`); comentário "Area Reponsavel pelo Apoio Financeiro" (`usuario.component.html:185`); `modulos.projeto`.
- Componente de ajuda `app-hint`: restringe edição ao perfil `'MASTER DN'` (inexistente neste sistema) e contém `console.log("Os perfis que acessam o menu “Usuário” são “Master DN” e “Técnico PMO DR”")` (`hint.component.html:2-5`; `hint.component.ts:100`). `HintService` não sobrescreve `criar`/`atualizar`, que herdam as URLs corporativas de **usuário** (`hint.service.ts:11-15`; `http-crud.service.ts:37-45`) *(inferência: gravar ajuda chamaria o endpoint errado)*.
- Estrutura hierárquica Entidade / Departamento Regional / Unidade e `TipoPerfil` `DN`/`DR`/`UA` no cadastro de usuário (4.3): em uso, mas com a carga de unidades comentada.
- `src/assets/i18n/pt-BR.json` não é carregado por nenhum código; a tradução do PrimeNG configurada é só `today`/`clear` (`main.ts:58-61`).
- `EventoPessoaPrincipalComponent` usa o seletor `'app-painel'`, o mesmo do `PainelComponent`, e declara `providers: [AuthService]` (instância própria) (`evento-pessoa-principal.component.ts:6-8`; `painel.component.ts:4`).
- Setores com nomes fixos nos mapas ("Anfitrião", "Deputados Federais", "Senadores", "Governadores", "Imprensa"… e, em C, "MEI - …") — parecem dados de um evento específico embutidos no código (`retangular.component.ts:296-331`; `retangular-recepcionista-checkin.component.ts:279-315`).
- `console.log` remanescentes: `pessoa.component.ts:236`; `topbar.component.ts:59`, `:120`; `submenu.component.ts:114`; `retangular-recepcionista-checkin.component.ts:153`, `:503`, `:1021`, `:1043`; `retangular-invertido-recepcionista-checkin.component.ts:453`, `:1349`.

### 8.3 Código comentado relevante

- Renovação de token no `401` (`// return this.handleTokenExpired(request, next);`) — hoje o `401` derruba a sessão (`interceptor.service.ts:36-39`).
- Carga de unidades em "Instituições Relacionadas" (`instituicoes-relacionadas.component.ts:197-206`).
- Exibição de erros/validações no formulário de usuário (`<p-message>{{error}}</p-message>`, `{{validationErrors}}`) (`usuario.component.html:13`, `:17`) e em recuperar senha (`recuperar-senha.component.html:9-11`).
- Rota curinga `{ path: '**', redirectTo: '/notfound' }` (`app-routing.module.ts:26`); `HashLocationStrategy` (`main.ts:36`).
- Menu antigo por `app-submenu` e `{{itens | json}}` (`menu.component.html:1`, `:7`).
- Implementação anterior do validador de CPF (`basic-validators.ts:191-210`).
- TODO/FIXME no código de `src/app`: **nenhum encontrado** (as ocorrências de "TODO" são as palavras "MÉTODOS"/"TODOS" em comentários; o `README.md` é só o modelo com "TODO").

### 8.4 Comportamentos que parecem defeito

**Autenticação**
1. "Lembrar": o controle `lembrar` existe, mas `AuthService.login` sempre persiste a sessão (`configurarSessao(res, true)`) (`login.component.ts:52`, `:64`; `auth.service.ts:47-56`).
2. Mensagem "A sua senha deve ter mais de 8 caracteres." com checagem `length < 8` (8 caracteres são aceitos) (`basic-validators.ts:127-128`).
3. Login de Secretaria Mesa / Check-In: sem tratamento de erro ou de resposta vazia de `evento-principal`; `localStorage.setItem` usa `res.id` antes de testar `res` (`login.component.ts:69-75`). A rota `/nao-ha-principal` não é usada. *(inferência: sem evento principal o usuário fica parado no login já autenticado)*.
4. Troca de senha: `{{alterarSenhaAlerta}}` interpola um array de objeto dentro de `<p-message>` *(inferência: exibiria "[object Object]")*; não há `<p-toast>` no template e o componente declara `MessageService` próprio, então os erros de `handleError` não têm onde aparecer; após trocar, vai sempre para `/dashboard-simples`, mesmo para perfis de secretaria (`alterar-senha.component.html:3-8`; `alterar-senha.component.ts:23`, `:28-32`, `:74`).
5. `auth.alteracaoSenha` nunca é limpo depois da troca obrigatória *(inferência: na mesma sessão, "Alterar Senha" do menu continuaria no modo obrigatório, com a senha antiga oculta)* (`auth.service.ts:14`; `login.component.ts:95-100`).
6. Recuperar senha chama o serviço sem validar o campo (`RecuperarSenhaComponent.ts:48-56`).
7. Logout não limpa `auth.usuario`/`access_token`/`menus` em memória nem `eventoPrincipalId`; `AuthGuard` consulta o valor em memória *(inferência: até recarregar a página as rotas continuam liberadas)* (`auth.service.ts:126-134`; `auth-guard.service.ts:12-15`).
8. "Alterar Foto do Perfil" não abre nada: o template não tem o diálogo (`topbar.component.html:48-53`; `topbar.component.ts:42-45`).

**Usuários**
9. Filtro "Entidade" chama `listarDepartamentosRegionais()` sem argumento → DR nunca carrega; o parâmetro enviado é `departamento`, mas o campo é `departamentoRegional` (`usuarios-filter.component.html:16`; `usuarios-filter.component.ts:94-113`, `:148`; `usuario-acesso.service.ts:19`).
10. A tela de pesquisa de usuários não tem `<p-toast>` (nem a página, nem o filtro, nem a lista) *(inferência: "Usuário removido com Sucesso", "Usuário Criado com Sucesso" e erros não aparecem nessa tela)* (`usuarios.component.html`, `usuarios-filter.component.html`, `usuarios-list.component.html`).
11. `pTooltip` usado na lista de usuários e de pessoas sem `TooltipModule` nos `imports` do componente (`usuarios-list.component.ts:30-40`; `pessoas-list.component.ts:31-43`).
12. Validador de CPF devolve a chave `invalidCPF` no primeiro dígito verificador e `invalid` nos demais casos; `getErrors` só lê `invalid` *(inferência: CPF com 1º dígito errado mostra "Campo obrigatório.")* (`basic-validators.ts:234-236`; `form-component-base.ts:69-74`).
13. "Instituições Relacionadas": ao adicionar sem unidade a lista é **substituída** (`this.instituicoes = [formValue]`); o teste de duplicidade compara `item.id` (inexistente) com `entidade.codigo`; unidades nunca carregam (`instituicoes-relacionadas.component.ts:118-124`, `:193-208`).
14. `buscarBasi` troca `'{codigoUsuario}/'` (com barra) enquanto `buscarPorCodigoNoSistema` troca `'{codigoUsuario}'` (`usuario.service.ts:29`, `:34-37`).

**Pessoas**
15. Edição de pessoa usa `POST` e mostra "Pessoa criada com sucesso"; não navega após salvar (`pessoa.component.ts:210-241`).
16. Lista de pessoas: ícones de ordenação em seis colunas, mas a consulta envia sempre `sort=nomeCompleto&direction=asc` (`pessoas-list.component.ts:101-108`).
17. Concordância: "Pessoa removido com sucesso" (`pessoas-list.component.ts:144`).
18. CPF, CNPJ e e-mail da pessoa sem validação de formato; e-mail do cadastro avulso só obrigatório (`pessoa.component.ts:139-140`, `:158`; `pessoas-cadastro.component.ts:95-99`).

**Eventos**
19. Título "Editar Evento" também no modo visualizar (`evento-create.component.html:9`).
20. "Adicionar" restrito a Administrador/Gestor, mas "Criar Primeiro Evento" (estado vazio) e todas as ações por linha (editar, excluir, tornar principal, cargas, legendas) sem checagem de perfil; rotas acessíveis por URL (`eventos-filter.component.html:71`; `evento-list.component.html:86-116`).
21. `getTiposMesa`, no erro, zera `tiposEvento` e registra "Erro ao carregar tipos de evento" (cópia) (`eventos-filter.component.ts:93-96`).
22. `colspan="7"` no estado vazio de uma tabela de 8 colunas; carga inicial pede 5 linhas e a tabela exibe 10 por página (`evento-list.component.html:7`, `:110`; `evento-list.component.ts:20`, `:67-72`, `:211-216`).
23. Cargas de convidados e confirmados: `enviarArquivos()` emite `enviar` antes de enviar; o pai fecha o diálogo e o *setter* `active` zera os dois anexos *(inferência: com as duas planilhas anexadas, a de confirmados pode não ser enviada, pois a variável é zerada antes do segundo `if`)* (`evento-participantes.component.ts:28-34`, `:202-226`; `evento-list.component.ts:186-190`).
24. `/eventos/**` redireciona para `/notfound`, rota inexistente (`evento-routing.module.ts:12`).

**Participantes do evento**
25. O parâmetro `isSecretariaCheckin` da consulta de participantes recebe `isSecretariaMesa`; o comentário do template diz "apenas para Check-In" mas a condição é `isSecretariaMesa` (`evento-pessoa.component.ts:106`, `:124`; `evento-pessoa.component.html:32-33`).
26. Confirmação do participante: o código passa `acceptLabel: 'Sim'`/`rejectLabel: 'Não'` e cabeçalho próprio, mas o `p-confirmDialog` do template tem cabeçalho fixo "Remover Pessoa" e rodapé com botões "Remover"/"Cancelar" (`evento-pessoas-list.component.html:2-7`; `evento-pessoas-list.component.ts:167-171`). O mesmo diálogo atende "Confirmar Remoção" de legenda.
27. O corpo da confirmação usa o atributo `statusCheckin` para transportar o status de **confirmação** (`evento-pessoas-list.component.ts:184-187`).
28. Check-in e confirmação alteram a linha antes da resposta e não revertem em caso de erro; a remoção de confirmação zera check-in e assento só na tela (o efeito real depende do backend) (`evento-pessoas-list.component.ts:126-129`, `:173-177`).
29. Tabela de participantes: `[paginator]` e `[lazy]` ligados duas vezes; `colspan` 7/8 numa tabela de 9 colunas; `dataKey="codigo"` (os itens têm `id`) (`evento-pessoas-list.component.html:12-13`, `:23-26`, `:170`, `:185`).
30. Cadastro avulso: erro com `severity: 'erro'`; `isLoading` só volta a `false` quando o diálogo é reaberto *(inferência: após erro o botão "Enviar" fica em carregamento)* (`pessoas-cadastro.component.ts:26-29`, `:107`, `:132-139`).
31. Após o cadastro avulso, a lista paginada não é recarregada (só os participantes do mapa) (`evento-pessoa.component.ts:154-161`).
32. Botão de exportação chama-se "Download", o método `exportCSV` e o endpoint `…/participantes/excel` (`evento-pessoas-list.component.html:175-176`; `evento.service.ts:94`).

**Mapa de assentos**
33. `DEBOUNCE_DELAY = 30000` com comentário "5 segundos de delay" (`retangular.component.ts:69`).
34. "Limpar Todas" *(inferência)* não é persistido: agenda o salvamento automático, mas `executarSalvamentoAutomatico` retorna sem salvar quando não há pessoas alocadas, e "Salvar Alocações" fica desabilitado/avisa "Não há pessoas alocadas na mesa para salvar." (`retangular.component.ts:1423-1431`, `:1519-1521`, `:1596-1597`; `retangular.component.html:91-92`).
35. Clique em assento **ocupado** da mesa principal: `openDropdown` retira o ocupante de `pessoasSelecionadas` e o devolve à lista de disponíveis antes de qualquer escolha *(inferência: fechando a janela sem escolher, a pessoa fica no assento e na lista ao mesmo tempo)* (`retangular.component.ts:436-454`).
36. O bloco da janela "Selecionar Pessoa" está duplicado no template (dois *overlays* com o mesmo `*ngIf`) (`retangular.component.html:388-417`, `:474-504`).
37. Exportação "PNG": a imagem é gerada como JPEG (`canvas.toDataURL('image/jpeg', …)`) e salva com extensão `.png` (`retangular.component.ts:1946`, `:2010`, `:2097-2102`).
38. Invertido (B e D): `resetarPosicoesVisuais()` (usado por "Limpar Todas") recria as áreas com os tamanhos do retangular (35/35, 8×4, 9×4, 23) em vez de 34/34, 7×4, 7×4, 30 (`retangular-invertido.component.ts:1599-1608`).
39. Invertido (B): faixas aceitas B/C até 35 e H até 36, contra arranjos de 34 e 7×4 *(inferência: H29–H36 causaria erro ao posicionar)*; em D a faixa de H foi corrigida para 28, mas B/C continuam 35 (`retangular-invertido.component.ts:32-38`, `:1806`, `:1819`, `:1864`; `retangular-invertido-recepcionista-checkin.component.ts:1953`, `:1966`, `:2012`).
40. Invertido do administrador (B): placeholder "Buscar pessoa na mesa ou cadeira (ex: A3, B15)..." sem busca por cadeira implementada; C faz a busca por cadeira mas o placeholder não a menciona (`retangular-invertido.component.html:51`; `retangular-recepcionista-checkin.component.html:134`).
41. A cada nova lista recebida da tela-mãe o mapa é remontado a partir do servidor *(inferência: alocações ainda não salvas — janela de até 30 s — podem ser descartadas quando outra alteração chega pelo polling)* (`retangular.component.ts:83-91`, `:228-240`).
42. Textos de status inconsistentes: "Check in não identificado" (lista, legenda e dica da mesa principal), "Check in não realizado" (dica de G/H/E), "Check-in pendente" (exportação) (`retangular.component.ts:876`, `:1076`, `:2517`).
43. Mapa da Secretaria Mesa: mesmo botão com texto "ATENDIDO" no desktop e "ATENDER" no tablet (`retangular-invertido-recepcionista-checkin.component.html:60`, `:112`).
44. Legenda no cartão do administrador só aparece se `numeroLegenda` for verdadeiro, embora o texto/cor venham de `nomeLegenda`/`corLegenda` (`retangular.component.html:33-38`).
44-A. No mapa somente leitura da Secretaria Mesa (C e D) a dica do assento vazio continua dizendo "Clique para atribuir uma pessoa", embora o assento não tenha clique (`retangular-recepcionista-checkin.component.ts:779`, `:810`, `:850`, `:891`, `:931`).

**Legendas e geral**
45. `/regras-legenda` sem id abre o Catálogo e `/catalogo-legendas/:id` abre a Configuração (efeito do array de rotas compartilhado, reconhecido em comentário) (`legendas-routing.module.ts:7-16`).
46. `handleErrorAlert` acessa `error.error.detalhe` sem testar `error.error` (as telas de legenda contornam com `tratarErro`) (`page-base.ts:14-24`; `catalogo-legendas.component.ts:273-280`).
47. Erros de negócio vindos em `detalhe` aparecem sempre com o resumo "Erro Interno" (`page-base.ts:15-16`).
48. `AlertaService` usa o texto literal `&nbsp;` como detalhe padrão dos toasts (`alerta.service.ts:13`).
49. Ausência de autorização por perfil nas rotas (ver 1 e 2.3): toda restrição de perfil do front é só de exibição.
