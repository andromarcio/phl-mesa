# Inventário factual do backend — Sistema de Mesa e Check-in (api-mesa_checkin)

**Repositório lido:** `sistema_mesa_checkin_backend`
**Método:** leitura integral de todos os arquivos de `src/main/java`, `src/main/resources`, `src/test`, `configuracoes.json` (raiz), `pom.xml`, `Dockerfile`, `README.md` e pipelines. Nada foi executado (nem build, nem testes) — todo comportamento descrito é o que o código diz, não o que foi observado em execução. Onde a conclusão depende de semântica de framework/linguagem e não só do texto do código, está marcado como **[inferência]**.

**Convenção de referência:** caminhos sem prefixo são relativos a `src/main/java/br/com/cni/apimesacheckin/`. Ex.: `controller/EventoController.java:74`. Arquivos fora desse pacote aparecem com caminho a partir da raiz do repositório (ex.: `configuracoes.json:166`, `src/main/resources/application.properties:23`).

**Dados gerais**
- Spring Boot 3.2.1, Java 21, empacotado como JAR (`pom.xml:9`, `pom.xml:20`, `pom.xml:15`). Banco SQL Server (`src/main/resources/application.properties:13-18`).
- Context path: `/api-mesa-checkin` (`src/main/resources/application.properties:23`). Todas as rotas abaixo ficam sob esse prefixo.
- Swagger/springdoc ligado para `/**` (`src/main/resources/application.properties:26`; `corporativo/config/AutenticacaoConfig.java:135-147`, título "API-MESA_CHECKIN").
- Sigla no arquivo de configuração corporativa: **`SMC`**, código de sistema **652** (`configuracoes.json:2-5`). A sigla "GPE" **não aparece no back**. O nome do sistema difere entre os dois arquivos: "Portal de Gestão de Participantes em Eventos" (`configuracoes.json:3`) e "Sistema de mesa e Check-in" (`src/main/resources/configuracoes.json:3`).
- Contagem conferida por `grep -o` das anotações de mapeamento: **63 endpoints** em 11 controllers.

---

## 1. Endpoints

### 1.0 O que vem de `CrudResource`

`CrudResource` (`controller/CrudResource.java:29`) **não declara nenhum endpoint**. É uma classe utilitária (estende `support/ResourceSupport.java:14`) com: classes internas `ResourceFile` (`:33`), `Message` (`:75`), `ValidationResults` (`:122`); conversores reflexivos `map(...)` (`:170`, `:174`, `:270`, `:274`), `getAllPropertyNames` (`:247`), `page` (`:288`); e montadores de paginação `pageableGet`/`pageablePost` (`:296`, `:314`, `:330`).

- Controllers que a estendem: **`EventoController`** (`controller/EventoController.java:58`) e **`PessoaController`** (`controller/PessoaController.java:45`). Herdam só os utilitários; usam de fato `map(...)` (`EventoController.java:114`, `:246`; `PessoaController.java:116`), `getAllPropertyNames` (`EventoController.java:246`) e `ResourceFile` (`EventoController.java:241`).
- Os demais controllers (`EventoPessoaController`, `LegendaController`, `ArquivoController`, `DynamicsController`, `SecretariaCheckinController`, `TipoEventoController`, `TipoMesaController`) **não** estendem `CrudResource`.
- `ValidationResults`, `Message`, `page`, `pageableGet`, `pageablePost` não têm nenhum chamador (ver §6).

### 1.1 Como ler a coluna "Permissão"

O back **não tem checagem de perfil no código** (ver §2). O que existe é: um interceptor que, para as rotas registradas como "recurso" no serviço corporativo, envia `token + recurso + método HTTP` a um serviço externo, que decide. O "recurso" é formado pelos **dois primeiros segmentos** da rota (`corporativo/interceptor/Interceptor.java:55-57`). A coluna abaixo indica o recurso que seria enviado e o que o arquivo declarativo `configuracoes.json` (raiz) diz sobre ele — esse arquivo **não é lido por nenhum código Java** (busca por `configuracoes.json` em `*.java/*.properties/*.xml/Dockerfile` não retorna nada); é a declaração que, presumivelmente, é carregada no serviço corporativo.

| Código | Recurso (2 primeiros segmentos) | Declarado em `configuracoes.json` (raiz) |
|---|---|---|
| **P-EVT** | `/administracao/eventos` (`configuracoes.json:166`) | GET: Administrador, Secretaria Mesa, Secretaria Check-In (`:223-240`). POST, PUT, DELETE: só Administrador (`:169-172`, `:187-190`, `:205-208`) |
| **P-LEG** | `/administracao/legendas` (`configuracoes.json:258`) | GET: Administrador, Secretaria Mesa, Secretaria Check-In (`:261-278`). POST, PUT, DELETE: só Administrador (`:291-294`, `:309-312`, `:327-330`) |
| **P-DYN** | `/administracao/dynamics` (`configuracoes.json:86`) | POST, PUT, DELETE, GET: só Administrador (`:89-146`) |
| **P-SEC** | `/secretaria/checkin` (`configuracoes.json:60`) | PUT: só **Secretaria Check-In** (`:63-67`) — Administrador não está listado |
| **P-NÃO-DECL** | recurso **não declarado** em `configuracoes.json` | Se a lista de recursos devolvida pelo serviço corporativo espelhar o arquivo, o interceptor **não é aplicado** a essas rotas → sem token (ver §2.3) |

### 1.2 `EventoController` — base `/administracao/eventos` (`controller/EventoController.java:50-58`)

`produces = application/json`; `consumes = form-urlencoded | json` (`:51-55`). Estende `CrudResource`.

| # | Método | Rota | Controller#método | O que faz | Parâmetros / body | Resposta | Permissão |
|---|---|---|---|---|---|---|---|
| 1 | GET | `/administracao/eventos` | `EventoController#findAll` (`:74`) | Pesquisa paginada de eventos não excluídos | Query: `generalFilter`, `nome`, `local`, `tipoEvento`, `tipoMesa`, `participantesMin`, `participantesMax`, `hasArquivo`, `dataInicial`, `dataFinal` + paginação `first`, `rows`, `sort` (obrigatório), `direction` | 200 `Page<EventoDTO>`; qualquer exceção → 500 corpo texto `Erro ao buscar eventos.` (`:81`) | P-EVT GET |
| 2 | GET | `/administracao/eventos/{id}` | `#findById` (`:85`) | Busca evento por id (não filtra excluídos) | path `id` | 200 `EventoDTO` / 404 | P-EVT GET |
| 3 | POST | `/administracao/eventos` | `#create` (`:92`) | Cria evento (e gera as cadeiras da mesa) | Body `EventoDTO` {id, nome, dataEvento, local, tipoEvento{id,nome,indicador}, tipoMesa{id,nome,indicador}, participantes, arquivo{id,nome,mime,tamanho,stored,conteudo}, excluido, principal, codigoCampanha} (`dto/EventoDTO.java:9-19`) | 201 `EventoDTO` | P-EVT POST |
| 4 | PUT | `/administracao/eventos/{id}` | `#update` (`:98`) | Edita evento | path `id` + body `EventoDTO` | 200 `EventoDTO` / 404 se não existir | P-EVT PUT |
| 5 | DELETE | `/administracao/eventos/{id}` | `#delete` (`:104`) | Exclusão **lógica** do evento | path `id` | 204 sempre (mesmo se o id não existir) | P-EVT DELETE |
| 6 | GET | `/administracao/eventos/anexos/{id}` | `#findAnexo` (`:110`) | Devolve metadados + conteúdo do arquivo anexo | path `id` (id do **arquivo**) | 200 mapa {id, nome, mime, tamanho, conteudo} (`domain/Arquivo.java:20`; `:126`) | P-EVT GET |
| 7 | GET | `/administracao/eventos/{id}/cadeiras` | `#findCadeirasMesaEvento` (`:130`) | Lista as cadeiras da mesa do evento | path `id` | 200 `List<CadeiraMesaDTO>` {id, identificacaoCadeira, background, composicaoMesa, eventoId}; lista vazia se evento não existe | P-EVT GET |
| 8 | POST | `/administracao/eventos/{id}/carga/convidados` | `#processaCargaConvidados` (`:136`) | Carga Excel de convidados | path `id` + body `ArquivoDTO` (planilha em `conteudo`) | 200 **sem corpo** | P-EVT POST |
| 9 | POST | `/administracao/eventos/{id}/carga/confirmados` | `#processaCargaConfirmados` (`:142`) | Carga Excel de confirmados | idem | 200 **sem corpo** | P-EVT POST |
| 10 | POST | `/administracao/eventos/{id}/carga/crm` | `#importarInscritosCrm` (`:148`) | Importa inscritos da campanha do Dynamics CRM | path `id` (sem body) | 200 `SituacaoCargaDTO` {countSucesso, countErro, countExistentes}; 404 se evento não existe (`:151`) | P-EVT POST |
| 11 | GET | `/administracao/eventos/{id}/participantes` | `#findParticipantesEvento` (`:154`) | Lista todos os participantes do evento (sem paginação) | path `id` | 200 `List<EventoPessoaDTO>` ordenada por nome | P-EVT GET |
| 12 | PUT | `/administracao/eventos/participante/checkin` | `#realizaCheckinParticipante` (`:160`) | Marca/desmarca check-in | Body `EventoPessoaCheckinDTO` {idEventoPessoa, statusCheckin} (`dto/EventoPessoaCheckinDTO.java:8-9`) | 200 sem corpo | P-EVT PUT |
| 13 | PUT | `/administracao/eventos/participante/confirmacao` | `#realizaConfirmacaoParticipante` (`:166`) | Altera a confirmação do participante | Body `EventoPessoaCheckinDTO` (o campo `statusCheckin` carrega o valor da **confirmação**) | 200 sem corpo | P-EVT PUT |
| 14 | POST | `/administracao/eventos/{eventoId}/composicoes-mesa` | `#salvarComposicoesMesa` (`:172`) | Substitui todo o mapa de assentos do evento | path `eventoId` + body `List<ParticipanteMesaDTO>` (`dto/ParticipanteMesaDTO.java:15-36`) | 200 `List<ParticipanteMesaDTO>`; exceção → 400 texto `Erro ao salvar composições: ` + msg (`:181`) | P-EVT POST |
| 15 | GET | `/administracao/eventos/{eventoId}/composicoes-mesa` | `#carregarComposicoesMesa` (`:185`) | Lista participantes com cadeira alocada | path `eventoId` | 200 `List<EventoPessoaDTO>`; exceção → 400 sem corpo | P-EVT GET |
| 16 | DELETE | `/administracao/eventos/{eventoId}/composicoes-mesa` | `#limparComposicoesMesa` (`:195`) | Remove todas as alocações de cadeira | path `eventoId` | 200 texto `Composições removidas com sucesso` (`:199`); exceção → 400 `Erro ao limpar composições: ` + msg | P-EVT DELETE |
| 17 | POST | `/administracao/eventos/{eventoId}/cadastro-rapido` | `#salvarComposicoesMesa` (sobrecarga, `:205-215`) | Inclui participante avulso (cria pessoa + vínculo) | path `eventoId` + body `PessoaCadastroRapidoDTO` {nome, razaoSocial, email, cargo, checkin} (`dto/PessoaCadastroRapidoDTO.java:8-12`) | 200 sem corpo; exceção → 400 `Erro ao criar pessoa na recepção: ` + msg (`:213`) | P-EVT POST |
| 18 | POST | `/administracao/eventos/{eventoId}/principal` | `#alterarEventoPrincipal` (`:217`) | Torna o evento o principal | path `eventoId` | 200 sem corpo; exceção → 400 `Erro ao salvar composições: ` + msg (`:223`, texto copiado) | P-EVT POST |
| 19 | GET | `/administracao/eventos/evento-principal` | `#findEventoPrincipal` (`:227`) | Devolve o evento principal | — | 200 `EventoDTO` (ou corpo nulo se não houver); exceção → 400 `Erro ao buscar evento principal: ` + msg | P-EVT GET |
| 20 | GET | `/administracao/eventos/participantes/excel` | `#imprimirParticipantes` (`:237`) | Exporta participantes para `.xls` | Mesmos query params do endpoint 28 | 200 JSON {contentType:`application/vnd.ms-excel`, name:`Participantes.xls`, content:(base64), size} (`:241-246`); erro → 500 {status:500, error: msg} (`:250-253`) | P-EVT GET |
| 21 | GET | `/administracao/eventos/{id}/legendas` | `#buscarConfiguracaoLegendas` (`:261`) | Lê a configuração de legendas do evento | path `id` | 200 `ConfiguracaoLegendaEventoDTO` {eventoId, blocos[]} | P-EVT GET |
| 22 | PUT | `/administracao/eventos/{id}/legendas` | `#salvarConfiguracaoLegendas` (`:266`) | Substitui a configuração de legendas | path `id` + body `ConfiguracaoLegendaEventoDTO` | 200 configuração regravada | P-EVT PUT |
| 23 | POST | `/administracao/eventos/{id}/legendas/simular` | `#simularLegendas` (`:272`) | Roda o motor de regras sem gravar | path `id` + body `ConfiguracaoLegendaEventoDTO` | 200 `ResultadoExecucaoDTO` | P-EVT POST |
| 24 | POST | `/administracao/eventos/{id}/legendas/executar` | `#executarLegendas` (`:278`) | Salva a configuração e aplica as legendas | idem | 200 `ResultadoExecucaoDTO` | P-EVT POST |
| 25 | GET | `/administracao/eventos/legendas/origens` | `#buscarOrigensLegendas` (`:284`) | Lista eventos que têm blocos configurados (candidatos a origem de cópia) | Query `excluirEventoId` (opcional) | 200 `List<EventoOrigemLegendaDTO>` {eventoId, nome, dataEvento, quantidadeBlocos} | P-EVT GET |
| 26 | GET | `/administracao/eventos/participante/{eventoPessoaId}/legenda` | `#buscarLegendaManualParticipante` (`:290`) | Lê a legenda manual do participante | path `eventoPessoaId` | 200 `LegendaParticipanteDTO` {eventoPessoaId, legendaId, nomeLegenda, background, manual} / **204** se não houver (`:294`) | P-EVT GET |
| 27 | PUT | `/administracao/eventos/participante/legenda` | `#atualizarLegendaManualParticipante` (`:297`) | Define/remove a legenda manual do participante | Body `LegendaParticipanteAtualizacaoDTO` {eventoPessoaId, legendaId} | 200 sem corpo | P-EVT PUT |

### 1.3 `EventoPessoaController` — base `/administracao/evento-pessoas` (`controller/EventoPessoaController.java:32-40`)

| # | Método | Rota | Controller#método | O que faz | Parâmetros | Resposta | Permissão |
|---|---|---|---|---|---|---|---|
| 28 | GET | `/administracao/evento-pessoas` | `EventoPessoaController#findAll` (`:54`) | Pesquisa paginada de participantes | Query: `idEvento`, `termoBusca`, `temas`, `gruposTrabalho`, `cargos`, `legendas`, `convidado`, `confirmado`, `checkin`, `hasFoto`, `sortField`, `sortOrder`, `page`, `size`, `first` | 200 `Page<EventoPessoaListDTO>`; exceção → 500 corpo = `e.getMessage()` (`:61`) | P-NÃO-DECL |
| 29 | GET | `/administracao/evento-pessoas/grupos-trabalho` | `#findAllGruposTrabalho` (`:65`) | Lista nomes distintos de grupos de trabalho (ordem alfabética) | — | 200 `List<String>` | P-NÃO-DECL |
| 30 | GET | `/administracao/evento-pessoas/temas` | `#findAllTemas` (`:71`) | Lista nomes distintos de temas | — | 200 `List<String>` | P-NÃO-DECL |
| 31 | GET | `/administracao/evento-pessoas/cargos` | `#findAllCargos` (`:77`) | Lista cargos distintos das pessoas | — | 200 `List<String>` | P-NÃO-DECL |
| 32 | GET | `/administracao/evento-pessoas/mesa/participantes` | `#pesquisaParticipantesMesa` (`:83`) | Lista participantes para a tela de mesa/check-in | Query `idEvento` (obrigatório), `statusCheckin` (opcional), `isSecretariaCheckin` (opcional) | 200 `List<ParticipanteMesaDTO>` | P-NÃO-DECL |
| 33 | PUT | `/administracao/evento-pessoas/{id}/atender` | `#atenderPessoa` (`:97`) | Marca o participante como atendido | path `id` (id do EventoPessoa) | 200 sem corpo | P-NÃO-DECL |

### 1.4 `LegendaController` — base `/administracao/legendas` (`controller/LegendaController.java:36-44`)

| # | Método | Rota | Controller#método | O que faz | Parâmetros / body | Resposta | Permissão |
|---|---|---|---|---|---|---|---|
| 34 | GET | `/administracao/legendas` | `LegendaController#findAll` (`:52`) | Pesquisa paginada do catálogo de legendas | Query `generalFilter`, `nomeLegenda`, `background`, `first`, `rows`, `sort` (padrão `nomeLegenda`), `direction` | 200 `Page<LegendaDTO>`; exceção → 500 corpo = msg | P-LEG GET |
| 35 | GET | `/administracao/legendas/presets` | `#listarPresets` (`:65`) | Lista presets | — | 200 `List<PresetLegendaDTO>` | P-LEG GET |
| 36 | GET | `/administracao/legendas/presets/{id}` | `#buscarPreset` (`:70`) | Detalhe do preset com a configuração | path `id` | 200 `PresetLegendaDetalheDTO` / 404 | P-LEG GET |
| 37 | POST | `/administracao/legendas/presets` | `#criarPreset` (`:77`) | Salva preset | Body `PresetLegendaCriacaoDTO` {nome, descricao, eventoId, configuracao} | 201 `PresetLegendaDTO` | P-LEG POST |
| 38 | DELETE | `/administracao/legendas/presets/{id}` | `#excluirPreset` (`:82`) | Exclui preset | path `id` | 204 | P-LEG DELETE |
| 39 | GET | `/administracao/legendas/{id}` | `#findById` (`:90`) | Busca legenda do catálogo | path `id` | 200 `LegendaDTO` {id, nomeLegenda, background} / 404 | P-LEG GET |
| 40 | POST | `/administracao/legendas` | `#create` (`:97`) | Cria legenda do catálogo | Body `LegendaDTO` | 201 `LegendaDTO` | P-LEG POST |
| 41 | PUT | `/administracao/legendas/{id}` | `#update` (`:102`) | Edita legenda | path `id` + body `LegendaDTO` | 200 `LegendaDTO` | P-LEG PUT |
| 42 | GET | `/administracao/legendas/{id}/uso` | `#uso` (`:107`) | Em quantos/quais eventos a legenda é usada | path `id` | 200 `LegendaUsoDTO` {legendaId, quantidadeEventos, eventos[{id,nome}]} | P-LEG GET |
| 43 | DELETE | `/administracao/legendas/{id}` | `#delete` (`:112`) | Exclui legenda (física, em cascata) | path `id` | 204 | P-LEG DELETE |

### 1.5 `PessoaController` — base `/administracao/pessoas` (`controller/PessoaController.java:37-45`)

Estende `CrudResource`.

| # | Método | Rota | Controller#método | O que faz | Parâmetros / body | Resposta | Permissão |
|---|---|---|---|---|---|---|---|
| 44 | GET | `/administracao/pessoas` | `PessoaController#findAll` (`:62`) | Pesquisa paginada de pessoas | Query `generalFilter`, `nomeCompleto`, `codinome`, `crm`, `email`, `razaoSocial`, `sexo`, `cargo`, `cpf`, `estado`, `hasFoto`, `first`, `rows`, `sort` (obrigatório), `direction` | 200 `Page<PessoaDTO>`; exceção → 500 texto `Erro ao buscar pessoas.` (`:69`) | P-NÃO-DECL |
| 45 | GET | `/administracao/pessoas/{id}` | `#findById` (`:73`) | Busca pessoa | path `id` | 200 `PessoaDTO` / 404 | P-NÃO-DECL |
| 46 | POST | `/administracao/pessoas` | `#create` (`:80`) | Cria pessoa (ou edita, se o body vier com `id`) | Body `PessoaDTO` (`dto/PessoaDTO.java:12-34`) | 201 `PessoaDTO` | P-NÃO-DECL |
| 47 | PUT | `/administracao/pessoas/{id}` | `#update` (`:86`) | Edita pessoa | path `id` + body `PessoaDTO` (só JSON) | 200 `PessoaDTO` / 404 | P-NÃO-DECL |
| 48 | DELETE | `/administracao/pessoas/{id}` | `#delete` (`:96`) | Exclui pessoa (física) se não tiver vínculo com evento | path `id` | 204; ou **409** {code:`PESSOA_COM_VINCULO_EVENTO`, message:`Não é possível remover a pessoa, pois ela já possui vínculo com evento.`} (`:101-106`) | P-NÃO-DECL |
| 49 | GET | `/administracao/pessoas/anexos/{id}` | `#findFoto` (`:112`) | Devolve metadados + conteúdo da foto | path `id` (id do **arquivo**) | 200 mapa {id, nome, mime, tamanho, conteudo} | P-NÃO-DECL |
| 50 | POST | `/administracao/pessoas/carga/gt` | `#processaCargaGt` (`:132`) | Carga Excel de Grupos de Trabalho | Body `ArquivoDTO` | 200 `SituacaoCargaDTO` | P-NÃO-DECL |
| 51 | POST | `/administracao/pessoas/carga/tema` | `#processaCargaTema` (`:138`) | Carga Excel de Temas | Body `ArquivoDTO` | 200 `SituacaoCargaDTO` | P-NÃO-DECL |
| 52 | POST | `/administracao/pessoas/carga/historico` | `#processaHistorico` (`:144`) | Carga Excel de Histórico de participações | Body `ArquivoDTO` | 200 `SituacaoCargaDTO` | P-NÃO-DECL |

### 1.6 Demais controllers

| # | Método | Rota | Controller#método | O que faz | Parâmetros | Resposta | Permissão |
|---|---|---|---|---|---|---|---|
| 53 | GET | `/administracao/arquivos/{id}` | `ArquivoController#getConteudo` (`controller/ArquivoController.java:43`) | Download do conteúdo binário do arquivo | path `id` | 200 bytes com `Content-Type` = mime gravado, `Cache-Control: public, max-age=604800` (`:81-83`); 404 se não há conteúdo | P-NÃO-DECL |
| 54 | GET | `/administracao/arquivos/{id}/thumbnail` | `ArquivoController#getThumbnail` (`:48`) | Miniatura JPEG (máx. 150 px) | path `id` | 200 `image/jpeg`, `Cache-Control: public, max-age=2592000`, `ETag "<id>-thumb"` (`:67-70`); 404 | P-NÃO-DECL |
| 55 | POST | `/administracao/dynamics/import` | `DynamicsController#importDynamics` (`controller/DynamicsController.java:45`) | Recebe planilha e **só imprime o conteúdo no log** | multipart `file` | 200 {message:`Importação concluída.`, tipo:`XLS`\|`XLSX`}; 400; 415; 500 (ver §4) | P-DYN POST |
| 56 | PUT | `/secretaria/checkin/participante` | `SecretariaCheckinController#realizaCheckinParticipante` (`controller/SecretariaCheckinController.java:30`) | Marca/desmarca check-in (mesmo serviço do endpoint 12) | Body `EventoPessoaCheckinDTO` | 200 sem corpo | P-SEC PUT |
| 57 | GET | `/administracao/tipo-eventos` | `TipoEventoController#findAll` (`controller/TipoEventoController.java:37`) | Pesquisa paginada de tipos de evento | Query `generalFilter`, `nome`, `indicador`, `first`, `rows`, `sort` (obrigatório), `direction` | 200 `Page<TipoEventoDTO>` {id, nome, indicador}; exceção → 500 corpo = msg | P-NÃO-DECL |
| 58 | GET | `/administracao/tipo-eventos/{id}` | `TipoEventoController#findById` (`:48`) | Busca tipo de evento | path `id` | 200 / 404 | P-NÃO-DECL |
| 59 | GET | `/administracao/tipo-mesas` | `TipoMesaController#findAll` (`controller/TipoMesaController.java:35`) | Pesquisa paginada de tipos de mesa | idem 57 | 200 `Page<TipoMesaDTO>` {id, nome, indicador} | P-NÃO-DECL |
| 60 | GET | `/administracao/tipo-mesas/{id}` | `TipoMesaController#findById` (`:46`) | Busca tipo de mesa | path `id` | 200 / 404 | P-NÃO-DECL |
| 61 | GET | `/liveness` | `LivenessController#getLiveness` (`corporativo/controller/LivenessController.java:13`) | Sonda de vida | — | 200 texto `Liveness date: <data>` | P-NÃO-DECL |
| 62 | GET | `/servicos/corporativo` | `RecursosController#findUrlServicos` (`corporativo/controller/RecursosController.java:24`) | Devolve o mapa de configurações **públicas** obtido do serviço corporativo | — | 200 `Map<String,String>` | P-NÃO-DECL |
| 63 | GET | `/servicos/privado` | `RecursosController#privado` (`:30`) | Devolve o mapa de configurações **privadas** | — | 200 `Map<String,String>` | P-NÃO-DECL |

**Não existe controller de `CadeiraMesa`.** O mapa de assentos é servido pelos endpoints 7, 14, 15 e 16 do `EventoController`.
**Não existem endpoints de criar/editar/excluir** tipo de evento ou tipo de mesa (só leitura — 57 a 60).

---

## 2. Autenticação e autorização

### 2.1 Como o back autentica

1. **Token da aplicação (na inicialização).** `AutenticacaoConfig#accessToken` faz `POST` em `${url.autenticacao}` e guarda o token (`corporativo/config/AutenticacaoConfig.java:49-58`; propriedade em `src/main/resources/application.properties:2`, variável `URL_AUTENTICACAO`). No `Dockerfile:17` o valor aponta para `https://dev-api.apps.ocp.sistemaindustria.com.br/api-autenticacao/oauth2/token?grant_type=client_credentials&client_id=…&client_secret=…`.
2. **Configurações corporativas.** `ConfiguracaoService` faz `GET ${url.api.corporativo.configuracoes}` com o token da aplicação e recebe `{publico:{…}, privado:{…}}` (`corporativo/service/ConfiguracaoService.java:33-50`; `corporativo/domain/Configuracao.java:17-21`). No `Dockerfile:19`: `…/api-corporativo/configuracao`. Se vier vazio: `IllegalStateException("Nenhuma configuração foi localizada para a inicialização do sistema;")` (`ConfiguracaoService.java:47-48`). Chaves usadas pelo back: `url.servicos.api.basi`, `sistema.codigo`, `url.servicos.api.autenticacao` (`AutenticacaoConfig.java:73-74`, `:105`, `:124-125`).
3. **Lista de recursos protegidos (na inicialização).** `AutenticacaoConfig#getRecursos` faz `GET {url.servicos.api.basi}/corporativo/sistemas/{sistema.codigo}/recursos` e transforma cada `url` devolvida em padrão `url + "/**"` (`AutenticacaoConfig.java:70-92`). O interceptor é registrado **só para esses padrões** (`:66-68`).
4. **Validação por requisição.** Para toda requisição que casa com um padrão registrado, `Interceptor#preHandle` (`corporativo/interceptor/Interceptor.java:25-53`):
   - ignora requisições `OPTIONS` (`:27`);
   - grava cabeçalhos CORS na resposta (`:78-83`: `Allow-Origin: *`, métodos `POST, GET, PUT, OPTIONS, DELETE`, `Max-Age 3600`, cabeçalhos `Authorization, X-requested-with, Content-Type`);
   - exige cabeçalho `Authorization` com mais de 6 caracteres e prefixo exatamente `Bearer`; senão lança `HeaderAuthorizationException("Não foi localizado o Header Authorization.")` (`:30-43`, constante em `:20`);
   - monta o recurso `/<segmento1>/<segmento2>` da rota (`:55-62`; ex.: `/administracao/eventos`);
   - chama `AccessTokenAutenticadoService#autenticarRequisicao` com token, tipo, recurso e método HTTP (`:47-50`).
5. **Serviço externo que decide.** `AccessTokenAutenticadoService` faz `GET` em `${url.servicos.api.autenticacao}<token>&tokenType=<tipo>&urlRecurso=<recurso>&metodo=<método>` (`corporativo/service/AccessTokenAutenticadoService.java:30-38`, `:100-111`; propriedade em `application.properties:3`, variável `URL_AUTENTICACAO_SERVICO`; no `Dockerfile:18`: `…/api-autenticacao/token/autenticado?accessToken=`).
   - Sucesso: guarda `AccessTokenAutenticado` no bean de escopo de requisição (`@RequestScope`, `:20`), com `codigoUsuario`, `nomeUsuario`, `loginUsuario`, `codigoPerfilAcesso`, `perfilACesso`, `tipoPerfilAcesso`, `valido` (`corporativo/domain/AccessTokenAutenticado.java:16-38`).
   - Erro HTTP do serviço: `ResponseException` com a mensagem extraída do corpo (4º trecho após dividir por `:`) e **o mesmo status HTTP** devolvido pelo serviço (`AccessTokenAutenticadoService.java:40-43`, `:52-55`).
   - Qualquer outro erro: `AccessTokenException("Ocorreu um erro ao autenticar o usuário da requisição.")` → 500 (`:44-47`; `corporativo/exception/handle/ExceptionHandle.java:23-28`).

**Conclusão:** a autenticação é por **Bearer token validado em serviço corporativo externo** (`api-autenticacao`). O back não emite token, não tem Spring Security (busca por `@PreAuthorize|@Secured|RolesAllowed|hasRole|SecurityFilterChain|spring-security` em `src/main` não retorna nada).

### 2.2 De onde vêm usuário e perfis

Do retorno do serviço externo, a cada requisição (item 5 acima). O back expõe getters (`getCodigoUsuario`, `getNomeUsuario`, `getLoginUsuario`, `getCodigoPerfilAcessoUsuario`, `getPerfilUsuario`, `getTipoPerfilUsuario` — `AccessTokenAutenticadoService.java:68-90`), mas **nenhum código de negócio os chama**: os únicos usos estão em `service/impl/BaseServiceImpl.java:193-203`, classe abstrata sem subclasse concreta (ver §6). Ou seja, **o back nunca lê quem é o usuário nem qual é o perfil**.

### 2.3 Rotas públicas

- É pública **toda rota que não casar com um recurso devolvido pelo serviço corporativo** — o interceptor simplesmente não é aplicado (`AutenticacaoConfig.java:66-68`).
- Se a chamada à lista de recursos falhar ou vier nula, o back registra apenas o padrão `publicas/**` e loga "Aplicação com nenhum recurso privado definido, iniciando aplicação com todos os recursos como público" (`AutenticacaoConfig.java:88-99`) — nesse caso **todos** os endpoints ficam sem autenticação.
- Pela declaração de `configuracoes.json` (raiz), os recursos são só quatro: `/secretaria/checkin` (`:60`), `/administracao/dynamics` (`:86`), `/administracao/eventos` (`:166`), `/administracao/legendas` (`:258`). **Não estão declarados**: `/administracao/pessoas`, `/administracao/evento-pessoas`, `/administracao/arquivos`, `/administracao/tipo-eventos`, `/administracao/tipo-mesas`, `/liveness`, `/servicos`. Se o serviço corporativo espelhar esse arquivo, essas rotas (endpoints 28–33, 44–54, 57–63) ficam **sem exigência de token**. O back não permite confirmar o que o serviço corporativo devolve em produção — **não encontrado no back**.
- O arquivo `src/main/resources/configuracoes.json` é uma versão diferente e mais antiga: perfis "Secretaria", "Painel", "Participante", "Administrador" (`:28-53`), sem "Secretaria Mesa" e sem o recurso de legendas; GET de `/administracao/eventos` só para Administrador (`:195-204`); referencia o perfil `SMC.5 Secretaria Check-In` em `/secretaria/checkin` (`:225-226`) sem declará-lo na lista de perfis.

### 2.4 Checagem de perfil por endpoint

**Não existe nenhuma checagem de perfil (Administrador / Secretaria Mesa / Secretaria Check-In) no código do back.** Nenhum controller, serviço ou repositório consulta o perfil do usuário. A única diferenciação possível é a feita **fora** do back, pelo `api-autenticacao`, com base em `recurso (2 segmentos) + método HTTP`. Consequências diretas dessa granularidade, segundo a declaração de `configuracoes.json` (raiz):

- Perfis declarados: `SMC.1 Administrador`, `SMC.2 Secretaria Mesa`, `SMC.3 Painel`, `SMC.4 Participante`, `SMC.5 Secretaria Check-In` (`configuracoes.json:23-54`).
- Todo `PUT`/`POST`/`DELETE` sob `/administracao/eventos` está declarado **só para Administrador** — inclusive check-in (endpoint 12), confirmação (13), salvar mapa de assentos (14), cadastro rápido (17), legenda manual (27) e executar legendas (24). Pelo arquivo, "Secretaria Mesa" só tem `GET` em `/administracao/eventos` e em `/administracao/legendas`.
- `PUT /secretaria/checkin/participante` (56) está declarado **só para Secretaria Check-In**.
- O parâmetro `isSecretariaCheckin` do endpoint 32 é um **query param enviado pelo cliente** (`controller/EventoPessoaController.java:87`), não derivado do perfil; só altera a ordenação (`repository/impl/EventoPessoaRepositoryImpl.java:544-554`).

Menus declarados (consumidos pelo front, não pelo back): Dashboard `dashboard-simples` para os 5 perfis (`configuracoes.json:349-385`); Administração › Pessoas `administracao-pessoas`, Usuários `administracao-usuarios`, Catálogo de legendas `catalogo-legendas` e Eventos › Cadastro `eventos`, todos só para Administrador (`:392-503`).

### 2.5 Cadastro de usuários, login, troca de senha, foto de perfil

**Nada disso é implementado neste back.** Não há endpoint de login, usuário, senha ou foto de perfil (ver lista completa em §1).

- O que existe são **resquícios não utilizados**: `domain/UrlServico.java:10-34` declara campos como `urlRecuperacaoSenha`, `urlAlteracaoSenha`, `urlNovoUsuarioSistema`, `urlAtualizaUsuarioSistema`, `urlReativaUsuarioSistema`, `urlAutenticacaoSistema`, `urlRefreshToken`, `urlPerfisSistema`, `urlMenusSistema`; e `service/impl/BaseServiceImpl.java:207-277` / `service/impl/AbstractCrudService.java:54-94` têm métodos para consultar usuários e perfis no serviço corporativo. Nenhum deles tem chamador nem bean concreto (ver §6).
- A delegação a serviço externo se dá por: `api-autenticacao` (URLs em `application.properties:2-3`), `api-corporativo` (`application.properties:4`) e `api-basi` (chave `url.servicos.api.basi`, `AutenticacaoConfig.java:73`). O endpoint 62 (`GET /servicos/corporativo`) entrega ao front o mapa de configurações públicas vindo do `api-corporativo` (`RecursosController.java:26-28`); o back **não mostra** quais chaves existem nesse mapa (vêm em tempo de execução) — **não encontrado no back**.
- A página "Usuários" (`administracao-usuarios`) aparece apenas como item de menu (`configuracoes.json:432-437`). Foto de perfil de usuário: **não encontrado no back** (a única foto é a da **Pessoa** — §3.b).

---

## 3. Regras de negócio por área

### 3.a Evento

**Paginação comum (`util/PageRequestUtils.java:30-65`)** — usada por Evento, Pessoa, Legenda, TipoEvento, TipoMesa: página = `first / rows` (0 se algum não for numérico, `:30-36`); tamanho = `rows` (ou `Integer.MAX_VALUE` se ausente, `:45-50`); ordenação = campo `sort` + `direction` (padrão ASC, `:52-61`). **`sort` é obrigatório**: sem ele `Sort.by` lança exceção (comentário confirma em `service/impl/LegendaServiceImpl.java:54`), que o controller converte em 500. Só o catálogo de legendas define padrão (`nomeLegenda`, `LegendaServiceImpl.java:55-57`).

**Criar — `EventoServiceImpl#save` (`service/impl/EventoServiceImpl.java:166-178`)**
- Não há nenhuma validação de campos obrigatórios, datas, unicidade de nome etc. O `EventoDTO` é convertido direto em entidade (`:169`).
- Se vier `arquivo`, ele é gravado primeiro via `ArquivoService.save` com o conteúdo do DTO (`:170-173`).
- É "criação" quando `dto.id == null` (`:168`); nesse caso, depois de salvar, gera as cadeiras da mesa (`:175-176`; regra em §3.e).
- `excluido` e `principal` são gravados **como vierem no DTO**; o back não inicializa `excluido = false` (`:169`, `dto/EventoDTO.java:17-18`). Como a pesquisa filtra `excluido = FALSE` (`:89`), um evento criado com `excluido` nulo não aparece na listagem — depende do que o front envia.
- O método não é `@Transactional` (`:166-167`): arquivo, evento e cadeiras são gravados em transações separadas.
- Se o body vier **com** `id`, o mesmo método regrava a entidade inteira (inclusive `excluido`/`principal`) sem gerar cadeiras (`:168-177`).

**Editar — `EventoServiceImpl#update` (`:190-210`)**
- Evento inexistente → devolve `null` → 404 (`controller/EventoController.java:101`).
- Atualiza apenas: `nome`, `dataEvento`, `local`, `participantes`, `tipoEvento`, `tipoMesa`, `arquivo`, `codigoCampanha` (`:198-205`). **Não** altera `excluido` nem `principal`.
- **Não regenera as cadeiras** quando o tipo de mesa muda (não há chamada a `createCadeiraMesaEvento` aqui).
- O anexo é só reatribuído (`e.setArquivo(updated.getArquivo())`, `:204`) — **não** chama `ArquivoService.save`, portanto o conteúdo de um arquivo novo não é gravado na edição (ver §6).

**Excluir — `EventoServiceImpl#delete` (`:180-188`)**: exclusão **lógica** (`excluido = true`, `:185`). Sem verificação de vínculos (participantes, cadeiras, legendas). Id inexistente: nada acontece e o controller devolve 204.

**Visualizar — `#findById` (`:161-164`)**: por id, **sem** filtrar excluídos.

**Pesquisar — `#findAll` (`:82-159`)**. Sempre aplica `excluido = FALSE` (`:89`). Filtros (todos combinados por E):

| Parâmetro | Como é aplicado | Ref. |
|---|---|---|
| `generalFilter` | `LIKE %x%` sem diferenciar maiúsculas em `nome` **OU** `local` **OU** nome do tipo de evento **OU** nome do tipo de mesa | `:90-100` |
| `nome` | `LIKE %x%` (minúsculas) em `nome` | `:102-105` |
| `local` | `LIKE %x%` (minúsculas) em `local` | `:107-110` |
| `tipoEvento` | igualdade com o **id** do tipo de evento | `:112-115` |
| `tipoMesa` | igualdade com o **id** do tipo de mesa | `:117-120` |
| `participantesMin` | `participantes >= valor` | `:122-125` |
| `participantesMax` | `participantes <= valor` | `:127-130` |
| `hasArquivo` | ignorado se vazio ou `T`; senão `true` → tem anexo, qualquer outro → sem anexo | `:132-136` |
| `dataInicial` (`yyyy-MM-dd`) | `dataEvento >= data`; data inválida é ignorada em silêncio | `:138-145` |
| `dataFinal` | **não funciona como limite superior**: o código faz o parse de `dataInicial` de novo e aplica `>=` (`:150-151`); erro é engolido | `:147-153` |

**Tornar principal — `#atualizarEventoPrincipal` (`:424-431`)**
- Carrega **todos** os eventos (`repository.findAll()`, inclusive excluídos, `:426`) e grava em cada um `principal = (id == eventoId)` (`:428-429`). É assim que garante um único principal: todos os outros são forçados a `false` a cada chamada.
- Não verifica se `eventoId` existe (se não existir, **nenhum** evento fica principal) nem se está excluído. Não é `@Transactional`.
- Consulta do principal: `findByPrincipalTrueAndExcluidoFalse` (`repository/EventoRepository.java:13`; `EventoServiceImpl.java:433-437`). Sem principal → 200 com corpo nulo.

**Anexar arquivo**: não há endpoint de upload separado. O arquivo viaja dentro do `EventoDTO.arquivo` (`dto/EventoDTO.java:16`), com `conteudo` em bytes (base64 no JSON). Só é gravado na **criação** (`EventoServiceImpl.java:170-173`). Leitura pelos endpoints 6, 53 e 54. Detalhes em §3.h.

**Tipos de evento e tipos de mesa**
- Somente leitura (endpoints 57–60). Filtros: `generalFilter` (`nome` OU `indicador`, `LIKE`), `nome`, `indicador` (`service/impl/TipoEventoServiceImpl.java:39-56`; `service/impl/TipoMesaServiceImpl.java:38-55`).
- Tipo de mesa tem `indicador` enumerado: `RETANGULAR`, `RETANGULAR_INVERTIDO` (`enumeration/TipoMesaEnum.java:5`). Tipo de evento tem `indicador` texto livre (`domain/TipoEvento.java:28-29`).
- Cadastro/edição/exclusão desses tipos: **não encontrado no back**.

### 3.b Pessoa

**Criar — `PessoaServiceImpl#save` (`service/impl/PessoaServiceImpl.java:130-146`)**
- Se `dto.id == null`: grava com `dataCriacao = agora` e `tipoCadastro = CADASTRO` (`:135-136`). Foto, se enviada, é gravada via `ArquivoService.save` (`:137-139`).
- Se `dto.id != null`: desvia para a edição (`:144-145`).
- **Nenhuma validação** de obrigatoriedade, formato (CPF, CNPJ, e-mail, telefone) ou unicidade.

**Editar — `#update` (`:161-195`)**: inexistente → `null` → 404. Atualiza `crm`, `nomeCompleto`, `codinome`, `sexo`, `cargo`, `cargoCartao`, `cpf`, `email`, `telefonePrincipal`, `celular`, `estado`, `estadoEmpresa`, `razaoSocial`, `nomeFantasia`, `cnpj` e grava `dataAlteracao = agora` (`:169-184`). Não altera `tipoCadastro`, `dataCriacao`, grupos, temas, históricos. Foto: se o DTO traz foto, regrava; **se não traz, remove a foto da pessoa** (`:186-190`).

**Excluir — `#delete` (`:148-159`)**: se existir qualquer `EventoPessoa` da pessoa, não exclui e devolve `false` → 409 `PESSOA_COM_VINCULO_EVENTO` (`:151-155`; `controller/PessoaController.java:98-107`). Caso contrário, exclusão **física** (`deleteById`, `:157`). Grupos de trabalho, temas e históricos saem junto por cascata (`domain/Pessoa.java:113-120`). O arquivo da foto não é excluído.

**Pesquisar — `#findAll` (`:49-123`)** (um filtro é considerado quando não é vazio nem a string `null` — `util/FilterUtils.java:11-14`):

| Parâmetro | Como é aplicado | Ref. |
|---|---|---|
| `generalFilter` | `LIKE %x%` (minúsculas) em `nomeCompleto` OU `codinome` OU `cargo` OU `cargoCartao` OU `email` OU `estado` | `:55-66` |
| `nomeCompleto`, `codinome`, `crm`, `email`, `razaoSocial`, `cargo` | `LIKE %x%` (minúsculas) no campo homônimo | `:68-91`, `:98-101` |
| `sexo` | igualdade (minúsculas) | `:93-96` |
| `cpf` | igualdade exata | `:103-106` |
| `estado` | igualdade (minúsculas) | `:108-111` |
| `hasFoto` | ignorado se vazio ou `T`; `true` → com foto; outro valor → sem foto | `:113-117` |

**Foto**: campo `foto` (`ArquivoDTO`) dentro do `PessoaDTO` (`dto/PessoaDTO.java:31`). Leitura pelos endpoints 49, 53 e 54 (miniatura). Sem limite de tamanho/tipo no back (§3.h).

**Unicidade**: o serviço **não verifica** unicidade de CPF, código CRM nem e-mail. Os próprios comentários do repositório dizem que `CD_CRM` não tem índice único (`repository/PessoaRepository.java:16`) e que não há UNIQUE em evento × pessoa (`repository/EventoPessoaRepository.java:21`). O código CRM é a chave de identificação da pessoa em todas as cargas (§3.c), via `findByCrm` (retorno único — falha se houver duas pessoas com o mesmo CRM, ver §6).

**Dados de empresa/contato**: campos `razaoSocial`, `nomeFantasia`, `cnpj`, `estadoEmpresa`, `telefonePrincipal`, `celular`, `email`, `estado` (`dto/PessoaDTO.java:20-27`). No cadastro manual são gravados como chegam; nas cargas de convidados/confirmados, telefone, celular e CNPJ são reduzidos a dígitos (`util/NumericoUtils.java:13-16`). `sexo` aceita `MASCULINO`, `FEMININO`, `NAO_INFORMADO` (`enumeration/SexoEnum.java:5`). `tipoCadastro`: `CARGA`, `RECEPCAO`, `CADASTRO` (`enumeration/TipoCadastroEnum.java:5`).

**Listas auxiliares**: cargos distintos não nulos em ordem alfabética (`repository/PessoaRepository.java:19-20`).

### 3.c Cargas por Excel

**Comum a todas**
- O arquivo chega como `ArquivoDTO` em JSON; só o campo `conteudo` (bytes) é usado — `nome` e `mime` são ignorados (`dto/ArquivoDTO.java:8-13`).
- **Extensões aceitas**: não há checagem de extensão nem de MIME. O workbook é aberto por `WorkbookFactory.create`, que detecta `.xls` e `.xlsx` pelo conteúdo (`util/ExcelUtils.java:117-123`).
- Só a **primeira aba** é lida (`getSheetAt(0)`); a linha 0 é o cabeçalho e os dados começam na linha 1; linhas totalmente vazias são puladas.
- Leitura de célula (`ExcelUtils.java:104-128`): texto → texto; numérica → `String.valueOf(double)` (ex.: `123.0`); data → `toString()` da data; fórmula → **o texto da fórmula**, não o resultado; vazia → `""`; outro tipo → `Tipo desconhecido`.
- Arquivo ilegível (`IOException`): o erro é só impresso em `System.err` (`Erro ao abrir o arquivo Excel: …`) e a resposta é **200** — com contadores zerados nas cargas de pessoa, ou sem corpo nas cargas de evento (`service/impl/GrupoTrabalhoPessoaServiceImpl.java:69-72`; `TemaPessoaServiceImpl.java:68-71`; `HistoricoPessoaServiceImpl.java:82-85`; `EventoPessoaServiceImpl.java:177-179`, `:197-199`).
- **Nenhuma carga devolve erros por linha.** As de pessoa devolvem só três contadores (`dto/SituacaoCargaDTO.java:14-16`); as de evento não devolvem nada.

#### Carga de GT — `POST /administracao/pessoas/carga/gt` (`service/impl/GrupoTrabalhoPessoaServiceImpl.java:42-114`)

| Coluna (cabeçalho exato) | Obrigatória | Ref. |
|---|---|---|
| `Cód. Contato` | sim | `enumeration/ExcelHeadersEnum.java:7` |
| `Grupos Temáticos` | sim | `ExcelHeadersEnum.java:22` |
| `Papel Desempenhado` | sim | `ExcelHeadersEnum.java:23` |

- Colunas localizadas **pelo nome** do cabeçalho (comparação exata após `trim`, sensível a maiúsculas/acentos — `ExcelUtils.java:130-148`); a posição não importa. Faltando qualquer uma: `IllegalArgumentException("Cabeçalho incompleto na carga.")` → 400 (`:56-58`).
- **Substitui tudo**: antes de processar, apaga **todos** os vínculos de grupo de trabalho de **todas** as pessoas (`repository.deleteAll()`, `:60`).
- Identificação da pessoa: `Cód. Contato` (removendo `.0` final de célula numérica — `util/StringUtils.java:18-21`) → `pessoaRepository.findByCrm` (`:83`, `:90`).
- Linha inválida: pessoa não encontrada → `countErro + 1` e segue (`:91-94`).
- Linha válida: se a pessoa já tem aquele grupo (mesmo nome, dentro do próprio arquivo) → atualiza o papel e conta em `countExistentes` (`:98-102`); senão cria com `dataVinculo = agora` e conta em `countSucesso` (`:103-110`).
- Transacional (`:43`). Retorno: `{countSucesso, countErro, countExistentes}`.

#### Carga de Temas — `POST /administracao/pessoas/carga/tema` (`service/impl/TemaPessoaServiceImpl.java:41-108`)

| Coluna (cabeçalho exato) | Obrigatória | Ref. |
|---|---|---|
| `Cód. Contato` | sim | `ExcelHeadersEnum.java:7` |
| `Tema` | sim | `ExcelHeadersEnum.java:21` |

- Cabeçalho incompleto → `Cabeçalho incompleto na carga.` (400) (`:55-57`).
- **Substitui tudo**: apaga todos os temas de todas as pessoas antes (`:59`).
- Pessoa pelo `Cód. Contato` → `findByCrm` (`:87-89`); não encontrada → `countErro` (`:90-93`).
- Tema já existente para a pessoa (repetido no arquivo) → `countExistentes`, não regrava (`:96-99`); senão cria com `dataVinculo = agora` → `countSucesso` (`:101-107`).
- Transacional (`:42`).

#### Carga de Histórico — `POST /administracao/pessoas/carga/historico` (`service/impl/HistoricoPessoaServiceImpl.java:42-120`)

| Coluna | Obrigatória | Ref. |
|---|---|---|
| `Cód. Contato` | sim (única exigida) | `:55-57` |
| **Todas as demais colunas** | não — cada uma é tratada como **um ano**; o nome do cabeçalho tem de ser um número (ex.: `2023`) | `:93-105` |

- Cabeçalho sem `Cód. Contato` → `Cabeçalho incompleto na carga.` (400).
- Pessoa: a célula de `Cód. Contato` precisa ser **numérica**; é convertida para inteiro longo e buscada por `findByCrm` (`:65-72`). Célula ausente/não numérica ou pessoa não encontrada → `countErro + 1` (`:66-69`, `:73-76`).
- **Substitui por pessoa**: para cada pessoa presente no arquivo, apaga todo o histórico dela e regrava (`:91-92`, `:117-120`). Pessoas que não estão no arquivo não são tocadas.
- Para cada coluna de ano: célula não numérica é ignorada; valor `<= 0` é ignorado; senão grava `{pessoa, ano, participacoes}` (`:97-105`, `:109-115`).
- Cada linha processada soma em `countSucesso` (`:78-79`). `countExistentes` fica sempre 0.
- **Não é transacional** no método principal (`:42-43`): falha no meio deixa carga parcial.

#### Carga de Convidados e de Confirmados — `POST /administracao/eventos/{id}/carga/convidados|confirmados` (`service/impl/EventoPessoaServiceImpl.java:163-201`, `:329-408`)

As duas usam o mesmo layout e a mesma rotina; muda só o indicador gravado. **O cabeçalho não é validado**: as colunas são lidas **por posição fixa**, e a linha 0 é simplesmente pulada.

| Posição | Cabeçalho esperado (nome no enum) | Destino na Pessoa | Ref. enum |
|---|---|---|---|
| 0 | `Cód. Contato` | `crm` | `ExcelHeadersEnum.java:7` |
| 1 | `Nome Completo` | `nomeCompleto` (**única obrigatória por linha**) | `:8` |
| 2 | `Codinome` | `codinome` | `:9` |
| 3 | `Sexo` | `sexo` — `Masculino`/`Feminino` exatos; qualquer outro → `NAO_INFORMADO` (`enumeration/SexoEnum.java:7-15`) | `:10` |
| 4 | `Cargo` | `cargo` | `:11` |
| 5 | `Cargo do Cartão` | `cargoCartao` | `:12` |
| 6 | `Empresa/Entidade` | `razaoSocial` | `:13` |
| 7 | `Nome Fantasia (Empresa/Entidade) (Pessoa Jurídica)` | `nomeFantasia` | `:14` |
| 8 | `CNPJ (Empresa/Entidade) (Pessoa Jurídica)` | `cnpj` (só dígitos) | `:15` |
| 9 | `Telefone` | `telefonePrincipal` (só dígitos) | `:16` |
| 10 | `Telefone Celular` | `celular` (só dígitos) | `:17` |
| 11 | `Email Comercial` | `email` | `:18` |
| 12 | `Estado` | `estado` | `:19` |
| 13 | `Estado (Empresa/Entidade) (Pessoa Jurídica)` | `estadoEmpresa` | `:20` |

- Evento inexistente: nada é feito e a resposta é 200 (`:165`, `:185`).
- Linha inválida: `Nome Completo` em branco → linha ignorada **em silêncio** (`:364-365`, `:339`).
- Identificação da pessoa: `Cód. Contato` (sem `.0` final, `:334-335`). Se preenchido e já existir pessoa com esse CRM → **atualiza todos os campos** da pessoa e grava `dataAlteracao = agora` (`:367-387`). Senão → **cria** pessoa com `tipoCadastro = CARGA` e `dataCriacao = agora` (`:390-407`). CRM em branco sempre cria pessoa nova (não há outra chave de deduplicação).
- Vínculo com o evento (`:340-360`):
  - não existe → cria `EventoPessoa` com `statusConvite` e `statusConfirmacao` conforme a carga, `statusCheckin = false`, `statusAtendido = false`. Convidados: convite=`true`, confirmação=`false` (`:174`). Confirmados: convite=`false`, confirmação=`true` (`:194`).
  - já existe → carga de convidados põe `statusConvite = true`; carga de confirmados põe `statusConfirmacao = true`; os demais indicadores ficam como estavam.
- **Acumula**: nenhuma das duas remove participantes nem desmarca indicadores de quem não veio no arquivo.
- Retorno: **nenhum** (200 sem corpo) — sem resumo, sem contagem, sem erros por linha (`controller/EventoController.java:137-146`).
- Não é transacional (`:163-164`, `:183-184`): cada linha é gravada isoladamente.

#### Carga pelo CRM — ver §3.g.

### 3.d Participante do evento (EventoPessoa)

**Pesquisar — `GET /administracao/evento-pessoas` → `EventoPessoaRepositoryImpl#buscaListaParticipantesEvento` (`repository/impl/EventoPessoaRepositoryImpl.java:92-284`)**

Consulta Criteria sobre `EventoPessoa` com `INNER JOIN pessoa`, `INNER JOIN evento`, `LEFT JOIN cadeiraMesa` (`:95-98`), `DISTINCT` (`:250`). Filtros (combinados por E; cada um só vale se não for vazio nem `null`):

| Parâmetro | Como é aplicado | Ref. |
|---|---|---|
| `idEvento` | igualdade com o id do evento. **Se ausente, pesquisa em todos os eventos** | `:102-105` |
| `termoBusca` | o termo é normalizado (sem acentos, minúsculas) e quebrado por espaços; **cada palavra** tem de aparecer (E) em **algum** (OU) de: `nomeCompleto`, `codinome`, `razaoSocial`, `nomeFantasia`, `cargo`. No banco, compara com `lower(translate(campo, acentuadas, sem acento))` | `:107-129`, `:70-86`, `:36-42` |
| `temas` | lista separada por `;`; casa se a pessoa tem (EXISTS) **algum** tema cujo nome contenha (`LIKE %x%`, minúsculas) um dos itens | `:132-152` |
| `gruposTrabalho` | lista separada por `;`; idem sobre o nome do grupo de trabalho | `:155-175` |
| `cargos` | lista separada por `;`; `LIKE %x%` (minúsculas) em `pessoa.cargo`, OU entre os itens | `:177-186` |
| `legendas` | lista de **ids** separada por `;`; casa se o participante tem (EXISTS) **qualquer** legenda atribuída com id na lista — não só a prioritária | `:189-207` |
| `convidado` | ignorado se `todos`; `sim` → `statusConvite = true`; qualquer outro valor → `= false` | `:209-213` |
| `confirmado` | ignorado se `todos`; `sim` → `statusConfirmacao = true`; outro → `= false` | `:215-219` |
| `checkin` | ignorado se `todos`; `sim` → `statusCheckin = true`; outro → `statusCheckin = false` **OU nulo** | `:221-231` |
| `hasFoto` | `true` → pessoa com foto; `false` → sem foto; outro valor ignorado | `:233-234`, `:334-342` |

- Ordenação: `sortField` ∈ {`nomeCompleto` (padrão), `razaoSocial`, `identificacaoCadeira`}; qualquer outro vira `nomeCompleto`; `sortOrder` = `desc` → decrescente, senão crescente (`:253-264`).
- Paginação: `first` (padrão 0) é o deslocamento, `size` (padrão 10) o tamanho, `page` (padrão 0) só rotula a página devolvida (`:266-272`, `:283`). Total por `COUNT DISTINCT` com os mesmos filtros (`:344-492`).
- Campos devolvidos (`dto/EventoPessoaListDTO.java:12-28`): `id`, `statusConfirmacao`, `statusConvite`, `statusCheckin`, `nomeCompleto`, `razaoSocial`, `nomeFantasia`, `cargo`, `identificacaoCadeira`, `pessoaId`, `numeroLegenda`, `legendaId`, `nomeLegenda`, `corLegenda`.
  - **Atenção**: a projeção passa `pessoa.nomeFantasia` no parâmetro `razaoSocial` e `pessoa.razaoSocial` no parâmetro `nomeFantasia` — os dois campos chegam **trocados** no DTO, e o código documenta isso como comportamento a preservar (`EventoPessoaRepositoryImpl.java:237-249`; `EventoPessoaListDTO.java:30-35`).
- A legenda devolvida é a **prioritária** do participante (regra em §3.f), buscada depois em uma consulta nativa só para os registros da página (`:290-331`).

**Listar todos do evento — `GET /administracao/eventos/{id}/participantes`**: todos os vínculos do evento, ordenados por nome sem diferenciar maiúsculas; evento inexistente → lista vazia (`service/impl/EventoPessoaServiceImpl.java:153-161`).

**Participantes da mesa — `GET /administracao/evento-pessoas/mesa/participantes` → `#pesquisaParticipantesMesa` (`EventoPessoaRepositoryImpl.java:501-593`)**
- Filtro por evento (`:535-537`).
- Se `statusCheckin` foi informado: `IND_STATUS_CHECKIN = valor`. **Se não foi**: só entra quem tem `confirmação = 1` **OU** `check-in = 1` (`:538-542`).
- Ordenação com `isSecretariaCheckin = true`: check-in (feitos primeiro), data/hora do check-in crescente, número da legenda (sem legenda = 99, por último), total de participações no histórico decrescente, nome (`:544-549`). Sem o parâmetro: número da legenda, histórico decrescente, nome (`:550-554`).
- Devolve também `quantidadeHistoricoPessoa` = soma de `NR_PARTICIPACOES` do histórico da pessoa (`:524-525`) e `arquivoId` (foto).

**Incluir participante avulso — `POST /administracao/eventos/{eventoId}/cadastro-rapido` (`EventoPessoaServiceImpl.java:438-462`)**
- Campos recebidos: `nome`, `razaoSocial`, `email`, `cargo`, `checkin` (`dto/PessoaCadastroRapidoDTO.java:8-12`). **Nenhum é validado** (nem o nome).
- Cria **sempre uma nova Pessoa** (sem procurar existente) com `tipoCadastro = RECEPCAO`, `sexo = NAO_INFORMADO`, `dataCriacao = agora` (`:452-462`).
- Cria o vínculo com `statusConvite = false`, `statusConfirmacao = false`, `statusCheckin = dto.checkin` (`:442-448`).
- **"Check-in automático"** = o valor de `checkin` enviado pelo cliente vai direto para `statusCheckin`. A **data/hora do check-in não é gravada** nesse caminho e `statusAtendido` não é definido (`:442-448`).
- Evento inexistente: nada é feito, 200 (`:440`).

**Check-in — `PUT /administracao/eventos/participante/checkin` e `PUT /secretaria/checkin/participante` (`EventoPessoaServiceImpl.java:410-419`)**
- Grava `statusCheckin` = valor recebido (marca **ou** desmarca) e `dataCheckin = agora` (`:415-416`). A data/hora é regravada **também ao desmarcar**.
- **Quem** fez o check-in: **não é gravado** (não encontrado no back).
- Não há pré-condição: não exige convite nem confirmação. Vínculo inexistente → nada acontece, 200.

**Confirmação — `PUT /administracao/eventos/participante/confirmacao` (`:421-436`)**
- Grava `statusConfirmacao` = valor recebido (alterna nos dois sentidos) (`:426`).
- Se o participante estava com check-in feito → **desfaz o check-in** e zera `dataCheckin`, qualquer que seja o novo valor da confirmação (`:427-430`).
- Se o novo valor é `false` → **libera a cadeira** (`cadeiraMesa = null`) (`:431-432`).

**Convidado**: não existe endpoint para marcar/desmarcar convite individualmente — **não encontrado no back**. `statusConvite` só é gravado pelas cargas (§3.c), pela importação do CRM (§3.g), pelo cadastro rápido (`false`) e pelo salvamento do mapa de assentos (que regrava o valor que o cliente enviar — §3.e).

**Atendimento — `PUT /administracao/evento-pessoas/{id}/atender` (`:469-475`)**: grava `statusAtendido = true`. Não há "desatender" direto; o indicador volta a `false` ao limpar o mapa de assentos (§3.e) ou ao regravá-lo com o valor enviado pelo cliente.

**Exportação — `GET /administracao/eventos/participantes/excel` (`:477-574`, `:580-639`)**
- Formato: **`.xls`** (HSSF), aba `Participantes` (`:481-482`). Entregue dentro de um JSON em base64 (endpoint 20).
- Usa **a mesma consulta paginada** da pesquisa (`:492`) — exporta só o que couber em `first`/`size` (padrão **10 registros**) se o cliente não mandar um `size` maior.
- Colunas, **na ordem exata**:

| # | Cabeçalho | Conteúdo | Ref. |
|---|---|---|---|
| 1 | `Cód. Contato` | `pessoa.crm` | `:586`, `:518` |
| 2 | `Nome Completo` | `pessoa.nomeCompleto` | `:590`, `:519` |
| 3 | `Codinome` | `pessoa.codinome` | `:594`, `:520` |
| 4 | `Cargo` | `pessoa.cargo` | `:598`, `:521` |
| 5 | `Cargo do Cartão` | `pessoa.cargoCartao` | `:602`, `:522` |
| 6 | `Razão Social` | `pessoa.razaoSocial` | `:606`, `:523` |
| 7 | `Nome Fantasia` | `pessoa.nomeFantasia` | `:610`, `:524` |
| 8 | `Grupos de Trabalho` | grupos da pessoa como `Nome (Papel)`, separados por `; ` | `:614`, `:526-536` |
| 9 | `Temas` | temas separados por `; ` | `:618`, `:538-544` |
| 10 | `Nro. Participações` | soma das participações do histórico (`0` se não houver) | `:622`, `:546-555` |
| 11 | `Legendas` | nome da legenda prioritária | `:626`, `:557-559` |
| 12 | `Confirmado` | `Sim` / `Não` / `Pendente` (nulo) | `:630`, `:561`; `util/StringUtils.java:23-25` |
| 13 | `Checkin` | idem | `:634`, `:562` |
| 14 | `Atendido` | idem | `:638`, `:563` |

### 3.e Mapa de assentos (CadeiraMesa)

**Identificação das cadeiras**: `identificacaoCadeira` = letra do setor + número sequencial a partir de 1 (ex.: `A1`, `B12`), mais a `composicaoMesa` (`PRINCIPAL` ou `LATERAL` — `enumeration/ComposicaoMesaEnum.java:5`). Setores `A`, `B`, `C`, `D` são `PRINCIPAL`; `E`, `F`, `G`, `H` são `LATERAL` (`service/impl/CadeiraMesaServiceImpl.java:88-210`).

**Geração (única regra por tipo de mesa)** — `#createCadeiraMesaEvento` (`:40-50`), chamada **só na criação do evento**: apaga as cadeiras do evento e recria conforme `tipoMesa.indicador`:

| Tipo de mesa | A | D | B | C | E | F | G | H | Total | Ref. |
|---|---|---|---|---|---|---|---|---|---|---|
| `RETANGULAR` | 1–5 | 1–5 | 1–35 | 1–35 | 1–23 | 1–32 | 1–10 | 1–36 | 181 (80 principais + 101 laterais) | `:88-121`, `:158-183` |
| `RETANGULAR_INVERTIDO` | 1–5 | 1–5 | 1–34 | 1–34 | 1–30 | 1–28 | 1–10 | 1–28 | 174 (78 principais + 96 laterais) | `:123-156`, `:185-210` |

- As quantidades são **fixas no código** (80 e 78 principais). O campo `participantes` do evento **não é usado** — a linha que o usaria está comentada (`:90-91`, `:125-126`).
- O indicador usado é o que veio no `tipoMesa` do DTO de criação, não o relido do banco (`service/impl/EventoServiceImpl.java:169-176`): se o cliente mandar só o id do tipo de mesa, nenhuma cadeira é gerada **[inferência]**.

**Listar cadeiras**: endpoint 7 (`EventoServiceImpl.java:212-219`).

**Marcar assento / trocar / remover**: o back **não tem operação por assento**. Existe só o salvamento do mapa **inteiro** — `POST /administracao/eventos/{eventoId}/composicoes-mesa` → `EventoServiceImpl#salvarComposicoesMesa` (`:221-274`):
1. Remove **todas** as alocações do evento e põe `statusAtendido = false` em quem tinha cadeira (`:228`, `:413-422`).
2. Para cada item recebido: localiza a cadeira por `identificacaoCadeira` + evento; se não achar, lança `Cadeira não encontrada: <id>` (`:241-248`), embrulhada em `Erro ao salvar composições da mesa: …` (`:272`) e devolvida como 400 `Erro ao salvar composições: …` (`controller/EventoController.java:181`).
3. Grava o vínculo com a cadeira e com os indicadores **que vieram do cliente** (`statusCheckin`, `statusConfirmacao`, `statusConvite`, `statusAtendido`; `statusAtendido` nulo vira `false`) (`:276-285`, `:252-257`).
4. Devolve a lista gravada já com a legenda prioritária (`:263-268`).
- Transacional: erro em qualquer item desfaz tudo (`:222`, `:270-273`).
- **Trocar com assento ocupado**: regra **não encontrada no back**. O serviço não verifica se dois participantes receberam a mesma cadeira nem se a cadeira estava ocupada; a troca é resolvida no cliente, que manda a lista final.

**Limpar todas** — `DELETE …/composicoes-mesa` → `#limparComposicoesMesa` (`:413-422`): para todo participante com cadeira, `cadeiraMesa = null` e `statusAtendido = false`.

**Busca**: endpoint 15 devolve os participantes com cadeira (`:399-407`); a busca de participantes para alocar é a do endpoint 32. Busca de cadeira por texto: **não encontrado no back**.

**Outras regras que tocam a cadeira**: desconfirmar o participante libera a cadeira (§3.d). O campo `background` da cadeira existe mas nenhum código o grava.

### 3.f Legendas

#### Catálogo de legendas (`service/impl/LegendaServiceImpl.java`)

CRUD completo (endpoints 34, 39–43). Cada legenda tem só `nomeLegenda` e `background` (cor) (`dto/LegendaDTO.java:13-15`).

| Operação | Regra | Mensagem literal | Ref. |
|---|---|---|---|
| Criar / editar | nome obrigatório (após `trim`) | `O nome do bloco de legenda é obrigatório.` | `:99-100`, `:118-119`, `:177-181` |
| Criar / editar | cor obrigatória no formato `#RRGGBB` (regex `^#[0-9A-Fa-f]{6}$`) | `A cor deve estar no formato #RRGGBB.` | `:37`, `:101`, `:120`, `:183-187` |
| Criar | nome único, sem diferenciar maiúsculas | `Já existe um bloco de legenda com este nome.` | `:102-104` |
| Editar | nome único ignorando o próprio registro | `Já existe um bloco de legenda com este nome.` | `:121-123` |
| Editar / excluir | registro tem de existir | `Bloco de legenda não encontrado.` | `:115-116`, `:147-148` |
| Pesquisar | `generalFilter` (nome OU cor, `LIKE`), `nomeLegenda`, `background`; ordenação padrão por nome | — | `:53-88` |
| Uso | conta e lista os eventos distintos que têm a legenda configurada (não filtra eventos excluídos) | — | `:131-142`; `repository/EventoLegendaRepository.java:28-33` |
| Excluir | **física e em cascata, sem bloqueio por uso**: (1) apaga todas as atribuições da legenda a participantes, inclusive manuais; (2) apaga os blocos dessa legenda em todos os eventos (condições saem junto); (3) apaga a legenda; (4) renumera os blocos restantes de cada evento afetado em 1..N | — | `:144-175` |

#### Legendas por evento (`service/impl/LegendaEventoServiceImpl.java`)

- A configuração do evento é uma **lista ordenada de blocos**; cada bloco referencia uma legenda do catálogo e tem uma lista ordenada de condições (`dto/ConfiguracaoLegendaEventoDTO.java:14-15`; `dto/BlocoEventoDTO.java:14-19`; `dto/CondicaoLegendaDTO.java:12-15`).
- **Ativar/inativar**: não existe indicador de ativo/inativo. Uma legenda "vale" para o evento quando há um bloco dela na configuração; tirar o bloco é a forma de desativar. Indicador explícito: **não encontrado no back**.
- **Ordem/prioridade**: a ordem do bloco é a **posição no array recebido** (1, 2, 3…), recalculada a cada gravação; o `numero` enviado pelo cliente é ignorado (`:110-119`, `:247`). Essa ordem é o "número da legenda" exibido e o critério de prioridade.
- **Ler** (endpoint 21): blocos em ordem, com `eventoLegendaId`, `legendaId`, `nomeLegenda`, `background`, `numero`, `condicoes` (`:86-94`; `mapper/EventoLegendaMapper.java:19-25`). Não verifica se o evento existe.
- **Salvar** (endpoint 22) — `#salvarConfiguracao` (`:96-142`): **substitui a configuração inteira** (apaga todos os blocos do evento e reinsere). Validações (`:171-196`):

| Condição | Mensagem literal | Ref. |
|---|---|---|
| evento não existe | `Evento não encontrado.` | `:99-100` |
| bloco sem legenda ou com legenda inexistente | `Bloco de legenda inexistente: <id>` | `:175-177`, `:112-114` |
| mesma legenda em dois blocos | `A configuração tem blocos de legenda repetidos.` | `:178-180` |
| campo preenchido fora da lista permitida | `Campo de condição inválido: <campo>` | `:185-187`; `enumeration/CampoCondicaoEnum.java:43` |
| operador preenchido inválido | `Operador de condição inválido: <op>` | `:188-190`; `enumeration/OperadorCondicaoEnum.java:22` |
| conectivo preenchido inválido | `Conectivo inválido: <c>` | `:191-193`; `enumeration/ConectivoEnum.java:37` |

  Bloco sem condição e condição incompleta **são aceitos e gravados** (o motor os ignora depois) (`:164-170`). O conectivo da primeira condição do bloco é sempre gravado como nulo (`:132-133`).

#### Condições

- **Campos** (`enumeration/CampoCondicaoEnum.java:10-14`): `grupoTrabalho` (nome do grupo de trabalho da pessoa), `tema` (nome do tema), `cargo`, `nomeFantasia`, `papelDesempenhado` (papel no grupo de trabalho).
- **Operadores** (`enumeration/OperadorCondicaoEnum.java:9`): `IGUAL`, `DIFERENTE`, `CONTEM`, `EM`.
- **Conectivos** (`enumeration/ConectivoEnum.java:9-10`): `E` (AND), `OU` (OR).

#### Algoritmo de avaliação — `#processar` (`:229-303`), passo a passo

1. Conta os participantes do evento — **todos** os vínculos, sem filtrar por convite/confirmação/check-in (`:230`, `:421-426`).
2. Conta as legendas manuais existentes no evento (`manuaisPreservadas`) (`:231`, `:428-435`).
3. Conta as legendas automáticas existentes (`legendasRemovidas`: as que serão — ou seriam, na simulação — apagadas) (`:233`).
4. **Só na execução**: apaga **todas** as legendas automáticas do evento, de todos os blocos (`:235-237`; `repository/EventoPessoaLegendaRepository.java:24-28`).
5. Percorre os blocos **na ordem do array**; para cada bloco:
   1. Nome e cor vêm do catálogo; se a legenda não existir (só possível na simulação), usa o que veio no DTO (`:251-255`).
   2. Filtra as condições **completas** — campo, operador **e** valor preenchidos (`:257`, `:306-315`). Se o bloco não tem legenda ou não tem nenhuma condição completa, ele é **ignorado** e seu nome vai para `blocosIgnorados` (`:258-262`).
   3. Monta a expressão (`#montarWhereCondicoes`, `:322-341`): a primeira condição efetiva entra sem conectivo; cada condição seguinte é combinada como `( <tudo que veio antes> <conectivo dela> <condição> )`. O conectivo usado é o **da própria condição**; ausente → `E` (`:335-337`).
      - **Precedência**: **não há precedência de E sobre OU**. A avaliação é estritamente **da esquerda para a direita**, com parênteses progressivos: `((c0 conj c1) conj c2) conj c3` (`:317-321`). Ex.: `A OU B E C` é avaliado como `(A OU B) E C`.
   4. Cada condição vira um predicado (`#montarFragmento`, `:350-405`), com o valor sem espaços nas pontas e sempre como parâmetro:
      - `IGUAL` → `campo = valor`. **Se o valor contém vírgula, `IGUAL` é tratado como `EM`** (`:356-359`).
      - `CONTEM` → `campo LIKE %valor%` (`:372-375`).
      - `EM` → valor separado por vírgula, itens sem espaços e não vazios → `campo IN (…)`; lista vazia → condição descartada (`:376-386`).
      - `DIFERENTE` → `campo <> valor` (`:387-390`).
      - Campos de coleção (`grupoTrabalho`, `papelDesempenhado`, `tema`): o predicado vira "**existe** um registro da pessoa que satisfaz" (`EXISTS`) (`:403-404`). Para `DIFERENTE`, vira "**não existe** registro da pessoa com aquele valor" (`NOT EXISTS … = valor`) — pessoa sem nenhum grupo/tema também casa (`:399-402`).
      - Cada condição gera seu **próprio** `EXISTS`: duas condições sobre grupo de trabalho (ex.: `grupoTrabalho IGUAL X` E `papelDesempenhado IGUAL Y`) **não** exigem que sejam o mesmo vínculo de GT (`:395-405`).
      - Campos simples (`cargo`, `nomeFantasia`): comparação direta na pessoa (`:395-397`). Diferença de maiúsculas/acentos não é tratada no código (fica por conta do banco).
   5. Se todas as condições foram descartadas na montagem, o bloco é ignorado (`:267-272`).
   6. Consulta os participantes do evento que satisfazem a expressão **e que não têm essa mesma legenda atribuída manualmente** (`:274-284`).
   7. **Só na execução**: insere, em lote, uma atribuição automática (`manual = N`, `dataCriacao = agora`) para cada participante encontrado (`:286-288`, `:407-419`).
   8. Acumula em `legendasAplicadas` e registra o detalhe do bloco: legenda, nome, cor, número (posição), quantidade e lista `{eventoPessoaId, nomeCompleto}` (`:290-291`).
6. Devolve `ResultadoExecucaoDTO`: `simulacao`, `totalParticipantes`, `legendasRemovidas`, `legendasAplicadas`, `manuaisPreservadas`, `blocosIgnorados`, `detalhesPorLegenda` (`:294-302`; `dto/ResultadoExecucaoDTO.java:19-25`).

**Quando mais de uma legenda casa**: os blocos **não são excludentes** — o participante recebe **uma atribuição para cada bloco** em que casar (o laço não para no primeiro; `:245-292`). A legenda **exibida** é a "prioritária", escolhida na leitura por esta ordem: (1) a **manual**; (2) senão a do bloco de **menor ordem** na configuração do evento; (3) senão (legenda fora da configuração) a de **menor id** (`repository/impl/EventoPessoaRepositoryImpl.java:44-68`; mesma regra em Java em `service/impl/EventoServiceImpl.java:360-385`). `numeroLegenda` = ordem do bloco, nulo se a legenda não está na configuração.

**Simular** (endpoint 23, `:202-210`): exige evento existente (`Evento não encontrado.`); roda o algoritmo com a configuração **recebida no body**, sem salvar nada e sem apagar nada.

**Executar** (endpoint 24, `:212-220`): primeiro **salva a configuração** (mesmas validações do PUT), depois roda o algoritmo gravando. Transacional.

**Resetar**: não há endpoint próprio — **não encontrado no back**. O efeito equivalente decorre do passo 4: executar com lista de blocos vazia apaga a configuração e todas as legendas automáticas do evento, preservando as manuais.

**Copiar de outro evento**: o back só oferece a lista de eventos-origem (endpoint 25: eventos **não excluídos** com ao menos um bloco, exceto o informado em `excluirEventoId` — `:144-162`; `repository/EventoLegendaRepository.java:38-41`). A cópia em si não existe no back; o cliente lê a configuração da origem (endpoint 21) e grava no destino (22/24).

#### Presets (`service/impl/PresetLegendaServiceImpl.java`)

| Operação | Regra | Mensagem literal | Ref. |
|---|---|---|---|
| Salvar (endpoint 37) | nome obrigatório (após `trim`) | `O nome do preset é obrigatório.` | `:88-91` |
| Salvar | nome único | `Já existe um preset com este nome.` | `:92-94` |
| Salvar | grava `descricao`; `eventoOrigem` = **cópia do nome** do evento informado (sem vínculo; nulo se o evento não existir); `dataCriacao = agora`; a configuração é guardada como **JSON** do `ConfiguracaoLegendaEventoDTO`. O conteúdo da configuração **não é validado** | — | `:96-105`, `:136-142` |
| Listar (endpoint 35) | devolve resumo: id, nome, descrição, evento de origem, data, e os blocos (legenda, nome, cor) — **blocos cuja legenda não existe mais no catálogo são omitidos** do resumo e da contagem | — | `:52-73`, `:163-184` |
| Carregar (endpoint 36) | devolve o preset com a configuração completa desserializada | `Não foi possível ler a configuração do preset.` (JSON inválido) | `:75-83`, `:125-134` |
| Excluir (endpoint 38) | só apaga o preset; não mexe em nenhum evento | `Preset não encontrado.` | `:115-123` |
| Editar | **não encontrado no back** | — | — |
| Aplicar a um evento | não há endpoint; o cliente carrega (36) e grava no evento (22/24) | — | — |

#### Legenda manual por participante (`LegendaEventoServiceImpl.java:441-504`)

- **Ler** (endpoint 26): devolve a primeira atribuição manual do participante, ou 204 (`:441-457`).
- **Alterar/remover** (endpoint 27) — `#atualizarLegendaManual`:

| Condição | Efeito | Mensagem literal | Ref. |
|---|---|---|---|
| body nulo ou sem `eventoPessoaId` | erro | `Participante não informado.` | `:462-464` |
| participante inexistente | erro | `Participante não encontrado.` | `:465-466` |
| `legendaId` nulo | **remove** todas as atribuições manuais do participante (as automáticas ficam) | — | `:471-478` |
| `legendaId` inexistente | erro | `Legenda inexistente: <id>` | `:480-481` |
| `legendaId` válido | apaga as manuais de **outras** legendas (um participante tem no máximo uma manual); se já existe atribuição dessa legenda (mesmo automática), **promove a manual**; senão cria nova com `dataCriacao = agora` | — | `:483-503` |

- Não exige que a legenda esteja na configuração do evento (legenda "fora da configuração" fica sem número).
- **A execução sobrescreve a legenda manual? Não.** A execução só apaga atribuições automáticas (`:235-237`), nunca insere sobre um par participante×legenda já manual (`:278-280`), e a manual sempre vence na escolha da legenda exibida.

### 3.g Integração com Dynamics CRM

Há **duas coisas distintas** com o nome "Dynamics":

**(1) `POST /administracao/dynamics/import`** (`controller/DynamicsController.java:45-82`): recebe um arquivo multipart, detecta `.xls`/`.xlsx` pelo conteúdo (ou, na falta, pela extensão — `util/ExcelUtils.java:42-57`) e **apenas imprime todas as abas/linhas no log** (`ExcelUtils.java:71-102`). **Não grava nada.** A própria descrição do endpoint diz isso (`DynamicsController.java:31-33`).

**(2) Importação de inscritos — `POST /administracao/eventos/{id}/carga/crm`** (`service/impl/EventoPessoaServiceImpl.java:203-327`; `service/impl/DynamicsCrmServiceImpl.java`).

- **Quando é acionada**: só por esse endpoint, manualmente. **Não há agendamento** (busca por `@Scheduled|EnableScheduling|@Async` em `src/main` não retorna nada).
- **O que é enviado ao CRM**: nada é gravado no CRM. A integração é **somente leitura** (um `POST` de token e `GET`s de consulta).
- **Configuração**: `dynamics.url`, `dynamics.tenant-id`, `dynamics.client-id`, `dynamics.client-secret` (`src/main/resources/application.properties:7-10`), todas opcionais na subida; se alguma estiver em branco no momento da chamada → `Integração com o CRM não configurada.` (`DynamicsCrmServiceImpl.java:227-232`).
- **Autenticação no CRM**: OAuth2 *client credentials* em `https://login.microsoftonline.com/<tenant>/oauth2/v2.0/token`, escopo `<dynamics.url>/.default` (`:180-199`); token mantido em memória até 60 s antes de expirar (`:47`, `:206-208`).
- **Consulta**: `GET <dynamics.url>/api/data/v9.2/l3_historicodeparticipacaodeeventoses` (`:43`, `:105-131`) com:
  - filtro: `l3_Nomedacampanha/codename eq '<código da campanha>' and l3_statusaprovacao eq 124070000 and l3_statusdoconvite eq 124070000` (`:107-109`, `:46`);
  - campos: `l3_historicodeparticipacaodeeventosid`, `l3_datadeenviodoformulario`, `l3_statusdoconvite`, `l3_statusaprovacao`, `_l3_contatorelacionado_value`, `l3_nomedecracha`, `l3_name`, `l3_email`, `l3_empresa`, `l3_cargodoconvidado`, `modifiedon` (`:110-121`);
  - expansão do contato: `contactid`, `si_codcontato`, `fullname`, `nickname`, `jobtitle`, `emailaddress1` (`:122`);
  - paginação seguindo `@odata.nextLink` até acabar (`:85-98`); tempo-limite de resposta 60 s e até 16 MB em memória (`:48-49`).
- **Mapeamento CRM → inscrito** (`#mapearInscrito`, `:237-256`): para cada campo, usa o do histórico e, se vazio, cai para o do contato.

| Dado | 1ª fonte (histórico) | 2ª fonte (contato) |
|---|---|---|
| id do histórico | `l3_historicodeparticipacaodeeventosid` | — |
| id do contato | `_l3_contatorelacionado_value` | — |
| código do contato | — | `si_codcontato` |
| nome | `l3_name` | `fullname` |
| codinome | `l3_nomedecracha` | `nickname` |
| e-mail | `l3_email` | `emailaddress1` |
| empresa | `l3_empresa` | — |
| cargo | `l3_cargodoconvidado` | `jobtitle` |
| data de envio do formulário | `l3_datadeenviodoformulario` | — |
| status da inscrição | rótulo formatado de `l3_statusdoconvite`; senão o valor numérico | — |
| status da aprovação | rótulo formatado de `l3_statusaprovacao`; senão o valor numérico | — |
| data de modificação | `modifiedon` | — |

- **Regras da importação** (`EventoPessoaServiceImpl.java:203-327`):

| Condição | Efeito | Mensagem literal / ref. |
|---|---|---|
| evento não existe | devolve nulo → 404 | `:206-207`; `controller/EventoController.java:151` |
| evento sem código de campanha | erro 400, CRM não é chamado | `O Código da Campanha deve ser preenchido no cadastro do evento.` (`:209-212`) |
| CRM não devolve ninguém | erro 400, nada é gravado | `Não foram encontrados inscritos aprovados e confirmados no CRM para a campanha <código>.` (`:214-218`) |
| inscrito sem código de contato | não é importado; conta em `countErro` | `:228-235` |
| mais de um registro do mesmo contato | fica só o de **maior data de modificação** | `:225-234`, `:279-285` |
| pessoa já existe com esse código CRM | atualiza `nomeCompleto` (se vier), `codinome`, `email`, `razaoSocial` (= empresa), `cargo` e `dataAlteracao` | `:304-313` |
| pessoa não existe | cria com `tipoCadastro = CARGA` e `dataCriacao = agora`; sem nome **e** sem codinome → não cria, conta em `countErro` | `:300-302`, `:315-326`, `:241-245` |
| vínculo com o evento não existe | cria com convite=`true`, confirmação=`true`, check-in=`false`, atendido=`false` + dados de rastreio do CRM; conta em `countSucesso` | `:248-259` |
| vínculo já existe | põe convite=`true` e confirmação=`true` e atualiza os dados de rastreio; **check-in, data do check-in, atendido e cadeira são preservados**; conta em `countExistentes` | `:260-266` |

  Dados de rastreio gravados no vínculo: `idHistoricoCrm`, `idContatoCrm`, `dataEnvioFormularioCrm`, `statusInscricaoCrm`, `statusAprovacaoCrm` (`:287-293`). Transacional (`:204`): erro no meio desfaz tudo. Acumula — não remove quem deixou de constar no CRM.

- **Em falha** (tudo vira 400 com `{mensagem:"Erro de validação", detalhe:<mensagem>}` — `controller/handler/GlobalExceptionHandler.java:20-24`):

| Situação | Mensagem literal | Ref. |
|---|---|---|
| configuração incompleta | `Integração com o CRM não configurada.` | `DynamicsCrmServiceImpl.java:39`, `:227-232` |
| falha ao obter token (HTTP, rede, resposta sem token) | `Não foi possível autenticar no CRM. Verifique as credenciais de integração.` | `:40`, `:201-219` |
| falha na consulta (HTTP ≠ 401, rede, inesperado) | `Não foi possível consultar o CRM. Tente novamente mais tarde.` | `:41`, `:167-176` |
| HTTP 401 na consulta | descarta o token, obtém outro e **repete uma única vez** | `:133-152` |
| código de campanha em branco (no serviço CRM) | `Informe o código da campanha do CRM.` | `:79-82` |

### 3.h Arquivos

- **Upload**: **não há endpoint de upload**. O arquivo chega embutido no JSON de Evento (`arquivo`) ou de Pessoa (`foto`), como `ArquivoDTO` {`id`, `nome`, `mime`, `tamanho`, `stored`, `conteudo` (bytes em base64)} (`dto/ArquivoDTO.java:8-13`). Os metadados (`nome`, `mime`, `tamanho`) são gravados **como o cliente enviar**, sem conferência.
- **Onde é guardado**: no **banco**. Metadados em `tb_arquivo` (`domain/Arquivo.java:11`) e conteúdo binário em `tb_conteudo_arquivo.bl_conteudo`, com o mesmo id (`domain/ConteudoArquivo.java:11`, `:24-26`; `service/impl/ArquivoServiceImpl.java:159-164`).
  - Existe código para ler de **sistema de arquivos** (`util/StorageUtils.java:15-38`, propriedade de JVM `storage.path`), acionado quando o arquivo está marcado como `stored` (`controller/EventoController.java:116-122`; `controller/PessoaController.java:118-124`). Na prática esse ramo **nunca é executado** (ver §6). Gravação em sistema de arquivos: **não encontrado no back**.
- **Regra de gravação** — `ArquivoServiceImpl#save` (`:48-79`): sem id → insere metadados e, se houver bytes, o conteúdo; com id → atualiza metadados e (a) sem bytes e sem nome → apaga o conteúdo; (b) com bytes → insere/atualiza o conteúdo; (c) sem bytes e com nome → mantém o conteúdo.
- **Download**: endpoint 53 (bytes puros com o mime gravado; 404 se não houver conteúdo); endpoints 6 e 49 (JSON com metadados + conteúdo); endpoint 54 (miniatura).
- **Miniatura** — `#findThumbnailById`/`#generateThumbnail` (`:81-149`): redimensiona para no máximo 150 px no maior lado, mantendo proporção, JPEG com qualidade 80 %. Se a geração falhar (ex.: não é imagem), devolve **o conteúdo original** com `Content-Type: image/jpeg` (`:90-94`; `controller/ArquivoController.java:67`).
- **Limites de tamanho/tipo**: **não encontrado no back**. Não há validação de extensão, MIME ou tamanho em nenhum ponto, nem configuração de multipart/limite em `application.properties`.
- **Exclusão de arquivo**: ao trocar/remover foto ou anexo, o arquivo antigo permanece no banco. Há uma rotina de limpeza sem chamador (§6).

---

## 4. Mensagens e erros

### 4.1 Tratadores globais

| Exceção | Status | Corpo | Ref. |
|---|---|---|---|
| `IllegalArgumentException` (todas as regras de negócio abaixo) | **400** | `{mensagem: "Erro de validação", detalhe: <mensagem da exceção>}` | `controller/handler/GlobalExceptionHandler.java:16`, `:20-24`; `dto/ErroDTO.java:13-14` |
| qualquer outra `Exception` | **500** | `{mensagem: "Erro interno", detalhe: "Ocorreu um erro inesperado. Contate o suporte."}` | `GlobalExceptionHandler.java:17-18`, `:26-31` |
| `ResponseException` (erro devolvido pelo serviço de autenticação) | status do serviço externo | `{message, statusCode, statusName}` | `corporativo/exception/handle/ExceptionHandle.java:17-21` |
| `AccessTokenException` | 500 | `{message, statusCode: 500, statusName: "INTERNAL_SERVER_ERROR"}` | `ExceptionHandle.java:23-28` |
| `MethodArgumentNotValidException` | 400 | `{message, 400, "BAD_REQUEST"}` (nenhum DTO usa validação — ver §6) | `ExceptionHandle.java:30-36` |
| `HeaderAuthorizationException` | 401 | `{message, 401, "UNAUTHORIZED"}` | `ExceptionHandle.java:39-44` |

Há **dois** tratadores globais sem ordem definida entre si; ver risco em §6.

### 4.2 Mensagens literais

| Mensagem (texto exato) | Status | Quando | Ref. |
|---|---|---|---|
| `Não foi localizado o Header Authorization.` | 401 | cabeçalho ausente, curto ou sem `Bearer` | `corporativo/interceptor/Interceptor.java:20`, `:32-35`, `:40-43` |
| `A URL não está no padrão modulo/recurso.` | 500 (genérico) | rota com menos de dois segmentos | `Interceptor.java:59-60` |
| `A URL não foi localizada no path da requisição.` | 500 (genérico) | requisição sem caminho | `Interceptor.java:74` |
| `Ocorreu um erro ao autenticar o usuário da requisição.` | 500 | falha não-HTTP ao validar o token | `corporativo/service/AccessTokenAutenticadoService.java:45` |
| `Nenhuma configuração foi localizada para a inicialização do sistema;` | (falha na subida) | serviço corporativo sem configurações | `corporativo/service/ConfiguracaoService.java:48` |
| `Erro ao buscar eventos.` | 500 (texto) | qualquer erro na pesquisa de eventos | `controller/EventoController.java:81` |
| `Erro ao buscar pessoas.` | 500 (texto) | qualquer erro na pesquisa de pessoas | `controller/PessoaController.java:69` |
| `<mensagem da exceção>` (sem texto fixo) | 500 (texto) | erro nas pesquisas de participantes, legendas, tipos de evento e de mesa | `controller/EventoPessoaController.java:61`; `LegendaController.java:59`; `TipoEventoController.java:44`; `TipoMesaController.java:42` |
| `Erro ao salvar composições: ` + msg | 400 (texto) | erro ao salvar o mapa de assentos | `EventoController.java:181` |
| `Erro ao salvar composições: ` + msg | 400 (texto) | erro ao **tornar principal** (texto reaproveitado) | `EventoController.java:223` |
| `Erro ao salvar composições da mesa: ` + msg | (embrulhada na anterior) | qualquer falha no salvamento do mapa | `service/impl/EventoServiceImpl.java:272` |
| `Cadeira não encontrada: ` + identificação | (embrulhada) | cadeira inexistente no evento | `EventoServiceImpl.java:246-248` |
| `Composições removidas com sucesso` | 200 (texto) | mapa limpo | `EventoController.java:199` |
| `Erro ao limpar composições: ` + msg | 400 (texto) | erro ao limpar o mapa | `EventoController.java:201` |
| `Erro ao criar pessoa na recepção: ` + msg | 400 (texto) | erro no cadastro rápido | `EventoController.java:213` |
| `Erro ao buscar evento principal: ` + msg | 400 (texto) | erro ao buscar o principal | `EventoController.java:233` |
| `{status: 500, error: <msg>}` | 500 | erro na exportação | `EventoController.java:250-253` |
| `{code: "PESSOA_COM_VINCULO_EVENTO", message: "Não é possível remover a pessoa, pois ela já possui vínculo com evento."}` | **409** | excluir pessoa vinculada a evento | `controller/PessoaController.java:101-106` |
| `Cabeçalho incompleto na carga.` | 400 | cargas de GT, Temas e Histórico sem as colunas exigidas | `service/impl/GrupoTrabalhoPessoaServiceImpl.java:57`; `TemaPessoaServiceImpl.java:56`; `HistoricoPessoaServiceImpl.java:56` |
| `O Código da Campanha deve ser preenchido no cadastro do evento.` | 400 | importar do CRM sem código de campanha | `service/impl/EventoPessoaServiceImpl.java:211` |
| `Não foram encontrados inscritos aprovados e confirmados no CRM para a campanha ` + código + `.` | 400 | CRM sem inscritos | `EventoPessoaServiceImpl.java:216-217` |
| `Integração com o CRM não configurada.` | 400 | configuração do Dynamics incompleta | `service/impl/DynamicsCrmServiceImpl.java:39` |
| `Não foi possível autenticar no CRM. Verifique as credenciais de integração.` | 400 | falha de token do Dynamics | `DynamicsCrmServiceImpl.java:40` |
| `Não foi possível consultar o CRM. Tente novamente mais tarde.` | 400 | falha na consulta ao Dynamics | `DynamicsCrmServiceImpl.java:41` |
| `Informe o código da campanha do CRM.` | 400 | código de campanha vazio no serviço CRM | `DynamicsCrmServiceImpl.java:81` |
| `Arquivo não enviado ou vazio.` | 400 `{message}` | `/dynamics/import` sem arquivo | `controller/DynamicsController.java:57` |
| `Tipo de arquivo não suportado. Envie .xls ou .xlsx.` | 415 `{message}` | `/dynamics/import` com arquivo não Excel | `DynamicsController.java:65` |
| `Importação concluída.` | 200 `{message, tipo}` | `/dynamics/import` com sucesso | `DynamicsController.java:74` |
| `Erro ao processar a planilha: ` + msg | 500 `{message}` | erro no `/dynamics/import` | `DynamicsController.java:80` |
| `Arquivo não é um Excel válido.` | (interna; chega ao usuário só via a mensagem anterior) | planilha inválida | `util/ExcelUtils.java:66`, `:121` |
| `Evento não encontrado.` | 400 | salvar/simular/executar legendas de evento inexistente | `service/impl/LegendaEventoServiceImpl.java:100`, `:206` |
| `Bloco de legenda inexistente: ` + id | 400 | bloco sem legenda válida | `LegendaEventoServiceImpl.java:114`, `:176` |
| `A configuração tem blocos de legenda repetidos.` | 400 | legenda duplicada na configuração | `LegendaEventoServiceImpl.java:179` |
| `Campo de condição inválido: ` + campo | 400 | campo fora da lista | `enumeration/CampoCondicaoEnum.java:43` |
| `Operador de condição inválido: ` + operador | 400 | operador fora da lista | `enumeration/OperadorCondicaoEnum.java:22` |
| `Conectivo inválido: ` + conectivo | 400 | conectivo fora da lista | `enumeration/ConectivoEnum.java:37` |
| `Participante não informado.` | 400 | legenda manual sem participante | `LegendaEventoServiceImpl.java:463` |
| `Participante não encontrado.` | 400 | legenda manual para participante inexistente | `LegendaEventoServiceImpl.java:466` |
| `Legenda inexistente: ` + id | 400 | legenda manual inexistente | `LegendaEventoServiceImpl.java:481` |
| `O nome do bloco de legenda é obrigatório.` | 400 | criar/editar legenda sem nome | `service/impl/LegendaServiceImpl.java:179` |
| `A cor deve estar no formato #RRGGBB.` | 400 | cor ausente ou fora do formato | `LegendaServiceImpl.java:185` |
| `Já existe um bloco de legenda com este nome.` | 400 | nome de legenda repetido | `LegendaServiceImpl.java:103`, `:122` |
| `Bloco de legenda não encontrado.` | 400 | editar/excluir legenda inexistente | `LegendaServiceImpl.java:116`, `:148` |
| `O nome do preset é obrigatório.` | 400 | preset sem nome | `service/impl/PresetLegendaServiceImpl.java:90` |
| `Já existe um preset com este nome.` | 400 | nome de preset repetido | `PresetLegendaServiceImpl.java:93` |
| `Preset não encontrado.` | 400 | excluir preset inexistente | `PresetLegendaServiceImpl.java:120` |
| `Não foi possível ler a configuração do preset.` | 400 | JSON do preset ilegível | `PresetLegendaServiceImpl.java:132` |
| `Não foi possível salvar a configuração do preset.` | 400 | falha ao serializar a configuração | `PresetLegendaServiceImpl.java:140` |
| `Erro ao mapear propriedades do objeto.` | 500 (genérico) | falha no conversor reflexivo | `controller/CrudResource.java:241` |
| `Sim` / `Não` / `Pendente` | — | valores das colunas de status na exportação | `util/StringUtils.java:23-25` |
| `Tipo desconhecido` | — | valor lido de célula Excel de tipo não tratado | `util/ExcelUtils.java:113` |
| `Liveness date: ` + data | 200 | sonda de vida | `corporativo/controller/LivenessController.java:15` |

Mensagens que **não chegam ao usuário** (só log/console): `Erro ao abrir o arquivo Excel: …` (`System.err`, nas cinco cargas); `Não foi possível ler a imagem` (`service/impl/ArquivoServiceImpl.java:106`, tratada internamente); mensagem de `storage.path` (`util/StorageUtils.java:27`, ramo inalcançável); `There is no authentication token available.` (`service/impl/BaseServiceImpl.java:196`) e `Erro ao definir atributo em lista.` (`service/impl/AbstractCrudService.java:107`) — ambas em código sem uso.

**Respostas silenciosas** (200/204 sem mensagem mesmo quando nada foi feito): excluir evento inexistente; check-in, confirmação e atender com id inexistente; cadastro rápido e cargas de convidados/confirmados com evento inexistente; cargas com arquivo ilegível.

---

## 5. Auditoria e campos automáticos

| O que | Onde é gravado | Ref. |
|---|---|---|
| `Pessoa.dataCriacao = agora` | cadastro manual; carga de convidados/confirmados; importação CRM; cadastro rápido | `service/impl/PessoaServiceImpl.java:135`; `service/impl/EventoPessoaServiceImpl.java:406`, `:325`, `:460` |
| `Pessoa.dataAlteracao = agora` | edição manual; atualização por carga; atualização pelo CRM | `PessoaServiceImpl.java:184`; `EventoPessoaServiceImpl.java:384`, `:311` |
| `Pessoa.tipoCadastro` (origem) | `CADASTRO` (manual), `CARGA` (planilha e CRM), `RECEPCAO` (cadastro rápido) | `PessoaServiceImpl.java:136`; `EventoPessoaServiceImpl.java:405`, `:324`, `:458` |
| `GrupoTrabalhoPessoa.dataVinculo = agora` | carga de GT | `service/impl/GrupoTrabalhoPessoaServiceImpl.java:108` |
| `TemaPessoa.dataVinculo = agora` | carga de Temas | `service/impl/TemaPessoaServiceImpl.java:104` |
| `EventoPessoa.dataCheckin = agora` | ao marcar **ou desmarcar** check-in; zerada ao alterar a confirmação de quem tinha check-in | `EventoPessoaServiceImpl.java:416`, `:429` |
| Rastreio do CRM no vínculo (`idHistoricoCrm`, `idContatoCrm`, `dataEnvioFormularioCrm`, `statusInscricaoCrm`, `statusAprovacaoCrm`) | importação CRM | `EventoPessoaServiceImpl.java:287-293` |
| `EventoPessoaLegenda.dataCriacao = agora` e `manual` (`S`/`N`) | execução das regras (automática) e legenda manual | `service/impl/LegendaEventoServiceImpl.java:407-419`, `:496-503` |
| `PresetLegenda.dataCriacao = agora` e `eventoOrigem` (cópia do nome do evento) | criação de preset | `service/impl/PresetLegendaServiceImpl.java:100-104` |
| Exclusão lógica: `Evento.excluido = true` (gravado como `S`/`N`) | excluir evento | `service/impl/EventoServiceImpl.java:185`; `domain/converter/SimNaoConverter.java:12-18` |

**O que não existe:**
- **Usuário de criação/alteração**: em nenhuma entidade. O back não grava quem fez nada (nem quem fez o check-in, nem quem alterou legenda, nem quem importou).
- **Data de criação/alteração do Evento**, da Legenda, da configuração de legendas do evento, da cadeira.
- **Auditoria automática do JPA**: busca por `@CreatedDate|@LastModifiedDate|@EntityListeners|@PrePersist|@PreUpdate|@CreatedBy|EnableJpaAuditing` em `src/main` não retorna nada — toda data é atribuída à mão nos serviços.
- **Trilha/histórico de alterações** (log de auditoria): não encontrado no back.
- **Exclusão lógica** só existe para Evento. Pessoa, Legenda e Preset têm exclusão física.

---

## 6. Suspeitas

Não há nenhum `TODO`/`FIXME` no código (busca em `src/main` e `src/test` só encontra a constante `TODOS_STRING`).

### 6.1 Comportamento que parece defeito

1. **Filtro `dataFinal` da pesquisa de eventos não funciona.** O bloco faz o parse de `dtInicio` em vez de `dtFim` e aplica `>=` (`service/impl/EventoServiceImpl.java:147-153`). Com só `dataFinal` informada, o parse de nulo falha e o erro é engolido.
2. **Edição de evento não grava o conteúdo do anexo.** `update` só reatribui a referência (`EventoServiceImpl.java:204`), ao contrário de `save` (`:170-173`). Arquivo novo enviado na edição (sem id) tende a falhar na gravação **[inferência]**.
3. **Edição de evento não regenera cadeiras** ao mudar o tipo de mesa (`EventoServiceImpl.java:190-210`); as cadeiras são geradas só na criação.
4. **Quantidade de cadeiras fixa no código** (80/78 principais), com o uso de `evento.participantes` comentado (`service/impl/CadeiraMesaServiceImpl.java:90-91`, `:125-126`).
5. **Carga de convidados/confirmados grava o CNPJ no CPF** ao atualizar pessoa existente: `existente.setCpf(limpaNumericos(getValue(row, CNPJ_EMPRESA_PESSOA…)))` (`service/impl/EventoPessoaServiceImpl.java:375`). Na criação o CPF não é preenchido.
6. **Salvar o mapa de assentos sobrescreve dados do participante.** O vínculo é reconstruído a partir do DTO recebido, que só carrega id, quatro indicadores, cadeira e pessoa (`EventoServiceImpl.java:276-312`), e é regravado por inteiro (`:257`). Efeito esperado: `dataCheckin` e os cinco campos de rastreio do CRM dos participantes alocados voltam a nulo, e os indicadores de convite/confirmação/check-in passam a valer o que o cliente mandou **[inferência — não executado]**.
7. **Confirmar desfaz o check-in.** `realizaConfirmacaoParticipante` zera o check-in sempre que ele estava marcado, mesmo quando a confirmação está sendo ligada (`EventoPessoaServiceImpl.java:427-430`).
8. **Desmarcar check-in grava nova data/hora** em vez de limpar (`EventoPessoaServiceImpl.java:415-416`).
9. **Cadastro rápido com "check-in automático" não grava data/hora do check-in** e deixa `statusAtendido` indefinido (`EventoPessoaServiceImpl.java:442-448`). Os valores padrão `= FALSE` da entidade (`domain/EventoPessoa.java:71`, `:74`) não valem para objetos criados pelo *builder*, pois não há `@Builder.Default` em lugar nenhum **[inferência]**.
10. **Exportação limitada à página.** `imprimirParticipantes` reaproveita a consulta paginada, cujo tamanho padrão é 10 (`EventoPessoaServiceImpl.java:492`; `repository/impl/EventoPessoaRepositoryImpl.java:266-272`). O log do controller fala em "xlsx", mas o arquivo é `.xls` (`controller/EventoController.java:243`, `:249`).
11. **`razaoSocial` e `nomeFantasia` trocados** na lista de participantes (`EventoPessoaRepositoryImpl.java:237-249`) — comentado como intencional ("preserva o comportamento pré-existente"), mas a ordenação por `razaoSocial` usa a razão social verdadeira (`:258`), enquanto o campo `razaoSocial` devolvido contém o nome fantasia.
12. **Leitura por sistema de arquivos nunca ocorre.** `Boolean.TRUE.equals(arquivo.getStored())` compara `Boolean` com `String` (`dto/ArquivoDTO.java:12`) e é sempre falso (`controller/EventoController.java:116`; `controller/PessoaController.java:118`) — o conteúdo vem sempre do banco.
13. **Anexo/foto inexistente gera 500**: `findAnexo`/`findFoto` usam o DTO sem checar nulo (`EventoController.java:113-116`; `PessoaController.java:115-118`).
14. **Tornar principal** varre e regrava todos os eventos, inclusive excluídos, sem transação e sem validar o id (`EventoServiceImpl.java:424-431`); mensagem de erro copiada de outra operação (`EventoController.java:223`).
15. **`excluido` não é inicializado na criação do evento** (`EventoServiceImpl.java:166-178`); a coluna é anulável e sem padrão (`db/migrations/V00008__ddl.sql:2`), e a pesquisa exige `excluido = FALSE`.
16. **Cargas de GT e de Temas apagam a base inteira** antes de processar (`GrupoTrabalhoPessoaServiceImpl.java:60`; `TemaPessoaServiceImpl.java:59`): um arquivo parcial elimina os vínculos de quem não está nele. Histórico substitui só por pessoa.
17. **Carga de Histórico** quebra (500) se houver coluna extra com cabeçalho não numérico e célula numérica (`HistoricoPessoaServiceImpl.java:103`) e, por não ser transacional, deixa carga parcial **[inferência]**.
18. **Código de contato numérico longo**: nas cargas de GT, Temas e Convidados/Confirmados a célula numérica é lida via `String.valueOf(double)` (`util/ExcelUtils.java:107-109`), que usa notação científica a partir de 10⁷ — códigos com 8+ dígitos (e telefones/CNPJ em célula numérica) não seriam reconhecidos **[inferência — não executado]**. A carga de Histórico converte para inteiro e não tem esse problema (`HistoricoPessoaServiceImpl.java:71`).
19. **CRM duplicado ou em branco**: `findByCrm` devolve um único resultado (`repository/PessoaRepository.java:14`) e não há unicidade de `CD_CRM`; duas pessoas com o mesmo código (ou várias com código vazio, que as cargas de convidados criam) fazem a consulta falhar **[inferência]**. O mesmo vale para `findByEventoAndPessoa` (`repository/EventoPessoaRepository.java:19`).
20. **Cargas de evento não devolvem resultado** e respondem 200 mesmo com arquivo ilegível (`EventoPessoaServiceImpl.java:177-179`); linhas sem nome são descartadas sem aviso.
21. **Dois tratadores globais de exceção sem `@Order`** (`controller/handler/GlobalExceptionHandler.java:11`; `corporativo/exception/handle/ExceptionHandle.java:14`). O primeiro captura `Exception` genérica; se ele tiver precedência, os erros de autenticação (401 e o status do serviço externo) seriam devolvidos como 500 "Erro interno" **[inferência — ordem não verificada em execução]**.
22. **`/servicos/privado` expõe as configurações privadas** do serviço corporativo (`corporativo/controller/RecursosController.java:30-34`) e `/servicos` não consta como recurso protegido em `configuracoes.json`.
23. **Recursos de negócio fora da lista protegida** em `configuracoes.json`: pessoas (incluindo excluir e as três cargas), participantes (incluindo `atender`), arquivos e tipos (§2.3).
24. **Fallback "tudo público"** quando a lista de recursos não pode ser obtida na subida (`corporativo/config/AutenticacaoConfig.java:88-99`).
25. **Segredos em claro no repositório**: `client_id`/`client_secret` no `Dockerfile:17-22` e em `configuracoes.json:13-20` / `src/main/resources/configuracoes.json:17-26`.
26. **Condições de legenda sobre grupo e papel não são correlacionadas** (cada uma é um `EXISTS` próprio — `LegendaEventoServiceImpl.java:395-405`); pode casar grupo de um vínculo com papel de outro.
27. **Excluir legenda do catálogo apaga também atribuições manuais** e blocos de todos os eventos, sem aviso nem bloqueio (`service/impl/LegendaServiceImpl.java:144-175`); o endpoint `/uso` existe, mas o back não o exige antes da exclusão.
28. **Pessoa: editar sem enviar a foto remove a foto** (`service/impl/PessoaServiceImpl.java:186-190`).
29. **Divergência entre os dois `configuracoes.json`** (raiz × `src/main/resources`): nome do sistema, perfis, recursos e menus diferentes (§2.3).

### 6.2 Código morto / sem uso aparente

- `service/impl/BaseServiceImpl.java` e `service/impl/AbstractCrudService.java`: classes abstratas **sem nenhuma subclasse concreta**; dependem de beans (`UrlServico`, `Supplier<AccessToken>`) que não são declarados em lugar nenhum. Todo o conteúdo (consulta de usuários, perfis, diretorias, áreas, gerências, colaboradores) é inalcançável. Idem `service/BaseService.java`, `service/CrudService.java`, `domain/UrlServico.java`, `exceptions/Exception.java`.
- `EventoPessoaServiceImpl#findAll` (`service/impl/EventoPessoaServiceImpl.java:110-140`) e `#findOne` (`:148-151`): sem chamador. O `findAll` ainda referencia atributos que não existem na entidade (`pessoa.nome`, `pessoa.cpf` com `LIKE`).
- `ArquivoService#clean` (`service/impl/ArquivoServiceImpl.java:151-157`) e as consultas `clean()` dos três repositórios: sem chamador. Se fosse chamada, apagaria todo arquivo não referenciado por `tb_evento` — **inclusive as fotos de pessoas** (`repository/ArquivoRepository.java:22-33`).
- `ArquivoService#findByUuid`/`#findConteudoByUuid` e a entidade `DownloadArquivo` (download por UUID): sem chamador nem endpoint.
- `CadeiraMesaService#findByEventoId`, `#findByEventoIdAndComposicaoMesa`, `#findById`: sem chamador.
- `CrudResource`: `ValidationResults`, `Message`, `page`, `pageableGet` (duas versões), `pageablePost`, `fixMapEncoding`. `ResourceSupport`: todos os métodos.
- `util/ExcelUtils`: `getBasicStyleCenter`, `getDateTimeStyle`. `util/PageRequestUtils`: `size`, `ilike`, `equal`, `equalBoolean`, `convertDayStartParam`, `convertDayEndParam`. `util/DateUtils` inteiro. `support/StringUtils`: `formatarString`, `isValidParam`, `getColumns`. `support/DateUtils`: só `convertStringDate` é referenciado, por método também sem uso.
- `ExcelHeadersEnum.CODIGO` (`enumeration/ExcelHeadersEnum.java:24`): sem uso.
- `AutenticacaoConfig#aplicacaoCliente` e `#urlServicosApiAutenticacao` (`corporativo/config/AutenticacaoConfig.java:102-120`): beans criados na subida e não injetados em nenhum lugar.
- `ExceptionHandle#handleMethodArgumentNotValidException`: nenhum DTO/controller usa `@Valid`/Bean Validation (busca não retorna nada), apesar de `spring-boot-starter-validation` estar no `pom.xml:61-64`.
- `pom.xml:71-74`: driver Oracle (`ojdbc8`) como dependência, com banco SQL Server.

### 6.3 Endpoint sem uso aparente (do ponto de vista do back)

- `POST /administracao/dynamics/import` (55): só imprime a planilha no log — aparenta ser protótipo.
- `GET /administracao/eventos/{id}/participantes` (11) e `GET /administracao/evento-pessoas` (28) se sobrepõem; uso real depende do front (não verificável aqui).
- `PUT /secretaria/checkin/participante` (56) duplica o endpoint 12; existe só para ter um recurso com permissão distinta.

---

## 7. O que os testes cobrem

**70 ocorrências de `@Test`** em 17 classes (contagem por `grep -o`); uma está comentada (`src/test/java/br/com/cni/apimesacheckin/corporativo/config/AutenticacaoConfigTest.java:55`), restando **69 ativos**. Os testes **não foram executados** nesta análise. O pipeline de `develop` roda os testes com Sonar (`azure-pipelines-develop.yml:48-56`).

### 7.1 Testes de infraestrutura corporativa (15 classes) — pouca ou nenhuma regra de negócio

| Classe | O que verifica |
|---|---|
| `ServletInitializerTest` | só chama `configure`; asserção trivial (`:21`) |
| `corporativo/config/AutenticacaoConfigTest` | que as chamadas externas lançam exceção sem rede; que `getRecursos` devolve lista não nula (cai no fallback) (`:66-76`) |
| `corporativo/controller/LivenessControllerTest` | retorno não nulo |
| `corporativo/domain/*Test` (6 classes) | getters/setters |
| `corporativo/exception/*Test` (3 classes) | construção dos objetos de erro; `handleResponseException` com mock sem status lança `IllegalArgumentException` (`ExceptionHandleTest.java:29-32`) |
| `corporativo/interceptor/InterceptorTest` | `preHandle` devolve `true` com `Bearer …` e serviço de autenticação simulado (`:52-65`); `extrairUrlRecurso` lança `IllegalStateException` com menos de 3 segmentos (`:80-84`) |
| `corporativo/service/AccessTokenAutenticadoServiceTest`, `ConfiguracaoServiceTest` | apenas que os métodos lançam exceção ou não quebram; várias asserções `assertTrue(true)` |

### 7.2 Testes com regra de negócio (2 classes) — só integração CRM

**`service/impl/DynamicsCrmServiceImplTest`** (5 testes) — confirma o mapeamento descrito em §3.g:
- campos do histórico têm prioridade sobre os do contato; valores chegam sem espaços nas pontas; status usa o rótulo formatado (`:26-68`);
- campo do histórico vazio/nulo cai para o do contato; sem rótulo formatado, o status vira o **valor numérico como texto** (ex.: `124070000`); `empresa` não tem substituto no contato (`:70-104`);
- registro sem contato relacionado não gera erro; data em formato inválido vira nulo (`:106-130`);
- datas com deslocamento explícito (`-03:00`) são aceitas (`:132-136`);
- configuração incompleta gera exatamente `Integração com o CRM não configurada.` (`:138-146`).

**`service/impl/EventoPessoaServiceImplImportarCrmTest`** (4 testes) — confirma as regras de §3.g:
- evento inexistente → retorno nulo, CRM não é chamado (`:67-74`);
- código de campanha em branco → mensagem exata `O Código da Campanha deve ser preenchido no cadastro do evento.`, nada gravado (`:76-88`);
- CRM vazio → mensagem exata `Não foram encontrados inscritos aprovados e confirmados no CRM para a campanha CAMP-2026.`, nada gravado (`:90-102`);
- cenário combinado (`:104-206`): dois registros do mesmo contato → prevalece o mais recente; inscrito sem código → 1 erro; contato novo → pessoa criada com `tipoCadastro = CARGA` e vínculo com convite/confirmação `true`, check-in/atendido `false`; contato já vinculado → pessoa atualizada, convite/confirmação passam a `true` e **check-in, data do check-in e atendido são preservados**; contadores finais 1 sucesso / 1 existente / 1 erro.

**Comportamento que só os testes revelam:** nenhum que contradiga o código; eles deixam explícita a intenção de que a reimportação do CRM **não desfaça check-in nem atendimento** e de que o status sem rótulo seja gravado como número em texto.

### 7.3 O que não tem teste nenhum

Controllers; Evento (criar, editar, pesquisar, principal); Pessoa; cargas por Excel (GT, Temas, Histórico, Convidados, Confirmados); check-in, confirmação, atendimento, cadastro rápido; pesquisa e exportação de participantes; mapa de assentos; todo o módulo de legendas (catálogo, configuração por evento, motor de regras, presets, legenda manual); arquivos e miniatura; tratadores de exceção de negócio.
