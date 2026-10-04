<!-- docqui: 3.0.1 | prompt: PROMPT_REPO_MAPPING | atualizado: 2026-09-30 -->
# Repositórios do sistema

> Inventário canônico dos repositórios do GPE. Levantado por leitura direta das cópias de código-fonte entregues para a engenharia reversa de 2026-09-30 — as cópias não trazem histórico git, então URL e responsável ficam ❓ até alguém da CNI informar.

| Repositório | URL | Domínio | Responsabilidade | Stack | BD próprio |
|---|---|---|---|---|---|
| gpe-doc | https://github.com/andromarcio/gpe-doc | — | Documentação e especificações (esta instância docqui) | Markdown | não |
| [sistema_mesa_checkin_backend](./sistema_mesa_checkin_backend.md) | ❓ Azure DevOps da CNI | Acesso, Pessoas, Eventos | API do sistema: regras de negócio, persistência, cargas por planilha e integração com o CRM | Java 21 · Spring Boot 3.2.1 · JPA/Hibernate · Apache POI · MapStruct | sim — SQL Server |
| [sistema_mesa_checkin_frontend](./sistema_mesa_checkin_frontend.md) | ❓ Azure DevOps da CNI | Acesso, Pessoas, Eventos | Interface web: telas de administração, pesquisa de participantes, check-in e mapa de assentos | Angular 18 · PrimeNG 18 · TypeScript 5.5 | não |

---

## Como rodar cada repositório

| Repositório | Comando | Porta | Pré-requisitos |
|---|---|---|---|
| sistema_mesa_checkin_backend | `./mvnw spring-boot:run` | 8080 (contexto `/api-mesa-checkin`) | JDK 21 · SQL Server · variáveis de ambiente de banco e de autenticação |
| sistema_mesa_checkin_frontend | `npm start` | 4200 🔍 padrão do Angular CLI | Node.js compatível com Angular 18 · back-end no ar |

---

## Variáveis de ambiente

> Só os nomes — os valores não são registrados aqui. ⚠️ O `Dockerfile` e o `configuracoes.json` do back-end trazem identificador e segredo de cliente escritos no próprio arquivo; ver *Achados* em [sistema_mesa_checkin_backend](./sistema_mesa_checkin_backend.md).

| Variável | Repositório(s) | Descrição | Exemplo |
|---|---|---|---|
| `db_server`, `db_port`, `db_name` | backend | Endereço do banco SQL Server | — |
| `db_username`, `db_password` | backend | Credenciais do banco | — |
| `db_encrypt`, `db_trust_certificate`, `db_login_timeout` | backend | Parâmetros da conexão | `true`, `true`, `30` |
| `show_sql` | backend | Liga o registro das consultas no log | `0` |
| `URL_AUTENTICACAO` | backend | Endereço de obtenção de token do serviço corporativo de autenticação | — |
| `URL_AUTENTICACAO_SERVICO` | backend | Endereço de validação do token do usuário autenticado | — |
| `URL_CORPORATIVO_CONFIGURACOES` | backend | Endereço do serviço corporativo de configurações | — |
| `DYNAMICS_URL`, `DYNAMICS_TENANT_ID`, `DYNAMICS_CLIENT_ID`, `DYNAMICS_CLIENT_SECRET` | backend | Acesso ao CRM (Dynamics 365) | — |
| `app_base_url` | frontend | Endereço da API, injetado na imagem no início do contêiner | — |

---

## Relação entre repositórios

```
sistema_mesa_checkin_frontend  ──→  sistema_mesa_checkin_backend  ──→  SQL Server
                                              │
                                              ├──→  Serviço corporativo de autenticação (CNI)
                                              ├──→  Serviço corporativo de configurações (CNI)
                                              └──→  CRM — Dynamics 365
```

---

## Padrão de branches

> 🔍 Inferido dos arquivos de pipeline (`azure-pipelines-develop.yml`, `-homolog.yml`, `-main.yml`), presentes nos dois repositórios de código.

| Branch | Propósito | Merge via |
|---|---|---|
| `main` | Produção | ❓ |
| `homolog` | Homologação | ❓ |
| `develop` | Desenvolvimento | ❓ |
