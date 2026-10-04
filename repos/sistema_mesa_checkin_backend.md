<!-- docqui: 3.0.1 | prompt: PROMPT_REPO_MAPPING | atualizado: 2026-09-30 -->
# Repositório: sistema_mesa_checkin_backend

- **URL**: ❓ Azure DevOps da CNI (a cópia entregue não tem histórico git)
- **Domínio**: Acesso, Pessoas e Eventos — atende os três
- **Responsabilidade**: API do sistema. Guarda eventos, pessoas, participantes, assentos e legendas; processa as cargas por planilha; aplica as regras de legenda; consulta os inscritos no CRM; repassa ao serviço corporativo o que é de usuário, perfil e menu
- **Responsável técnico**: ❓
- **Stack**: Java 21 · Spring Boot 3.2.1 (web, data-jpa, validation, webflux) · Hibernate · SQL Server (`mssql-jdbc`) · Apache POI 5.2.5 (planilhas) · MapStruct 1.6.3 · Lombok · springdoc-openapi 2.2.0 · JUnit 5 + Mockito · JaCoCo · SonarQube
- **Banco de dados**: sim — SQL Server, dialeto `SQLServer2012Dialect`. As migrações em `db/migrations` são executadas à mão, em ordem numérica; não há Flyway nem Liquibase
- **Comunica com**: `sistema_mesa_checkin_frontend` (é a API dele) · serviço corporativo de autenticação e de configurações da CNI · CRM Dynamics 365

---

## Estrutura de pastas

```
sistema_mesa_checkin_backend/
├── db/migrations/                  ← 23 scripts SQL (V00001 a V00021), DDL e DML
├── configuracoes.json              ← cadastro do sistema no serviço corporativo: perfis, recursos e menus
├── Dockerfile                      ← imagem Tomcat 9 + JDK 21
├── azure-pipelines-{develop,homolog,main}.yml
├── pom.xml
└── src/
    ├── main/java/br/com/cni/apimesacheckin/
    │   ├── controller/             ← 9 controllers REST + CrudResource (base genérica)
    │   ├── corporativo/            ← autenticação, interceptor, configuração e tratamento de exceção corporativos
    │   ├── domain/                 ← 19 classes: entidades JPA e objetos de apoio
    │   ├── dto/                    ← 35 objetos de transferência
    │   ├── enumeration/            ← 9 listas fixas (sexo, tipo de cadastro, operadores de condição…)
    │   ├── mapper/                 ← conversores MapStruct entidade ↔ DTO
    │   ├── repository/             ← repositórios Spring Data + consulta customizada de participantes
    │   ├── service/ e service/impl ← regras de negócio
    │   ├── support/ e util/        ← datas, texto, planilhas, paginação, armazenamento
    │   └── exceptions/
    ├── main/resources/             ← application.properties, configuracoes.json, banner
    └── test/                       ← testes do pacote corporativo e de dois serviços
```

---

## Como rodar localmente

```bash
# Pré-requisitos
JDK 21, Maven (ou o wrapper ./mvnw), SQL Server com as migrações de db/migrations aplicadas em ordem

# Configuração
# definir as variáveis de ambiente listadas abaixo antes de subir

# Iniciar
./mvnw spring-boot:run
# API em http://localhost:8080/api-mesa-checkin
```

---

## Variáveis de ambiente

| Variável | Obrigatória | Descrição | Exemplo |
|---|---|---|---|
| `db_server`, `db_port`, `db_name` | sim | Endereço do banco | — |
| `db_username`, `db_password` | sim | Credenciais do banco | — |
| `db_encrypt`, `db_trust_certificate`, `db_login_timeout` | sim | Parâmetros da conexão | `true`, `true`, `30` |
| `show_sql` | sim | Registro das consultas no log | `0` |
| `URL_AUTENTICACAO` | sim | Obtenção de token no serviço corporativo | — |
| `URL_AUTENTICACAO_SERVICO` | sim | Validação do token do usuário | — |
| `URL_CORPORATIVO_CONFIGURACOES` | sim | Serviço corporativo de configurações | — |
| `DYNAMICS_URL`, `DYNAMICS_TENANT_ID`, `DYNAMICS_CLIENT_ID`, `DYNAMICS_CLIENT_SECRET` | não | Acesso ao CRM; em branco, a importação de inscritos fica indisponível 🔍 | — |

---

## Features implementadas neste repositório

→ ver a coluna **Repositórios** de [`modules/INDEX.md`](../modules/INDEX.md) e a seção `## Implementação` de cada N3.

---

## Convenções específicas deste repositório

### Padrão de testes
JUnit 5 com Mockito; cobertura medida pelo JaCoCo e enviada ao SonarQube pelo pipeline.

### Deploy
Azure Pipelines, um arquivo por ambiente (`develop`, `homolog`, `main`). A aplicação é empacotada e publicada como imagem Tomcat 9.

---

## Achados

- ⚠️ **Segredo escrito no repositório.** O `Dockerfile` traz, como valor padrão de variável de ambiente, o identificador e o segredo de cliente do serviço de autenticação; o `configuracoes.json` traz outro par. Segredo em arquivo versionado vaza para quem tem leitura do repositório e fica no histórico mesmo depois de removido. Os valores não foram copiados para esta documentação.
- ⚠️ Os dois `configuracoes.json` (raiz e `src/main/resources`) têm conteúdo diferente — não está claro qual vale.
