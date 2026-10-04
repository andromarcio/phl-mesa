<!-- docqui: 3.0.1 | prompt: PROMPT_REPO_MAPPING | atualizado: 2026-09-30 -->
# Repositório: sistema_mesa_checkin_frontend

- **URL**: ❓ Azure DevOps da CNI (a cópia entregue não tem histórico git)
- **Domínio**: Acesso, Pessoas e Eventos — atende os três
- **Responsabilidade**: interface web do sistema. Telas de acesso, de administração de usuários e pessoas, de eventos, de participantes e check-in, do mapa de assentos e da configuração de legendas
- **Responsável técnico**: ❓
- **Stack**: Angular 18.2 · PrimeNG 18 · PrimeFlex · TypeScript 5.5 · RxJS 6.6 · FontAwesome · html2canvas e jsPDF (captura e PDF) · file-saver · Karma + Jasmine
- **Banco de dados**: não
- **Comunica com**: `sistema_mesa_checkin_backend`, pela API em `/api-mesa-checkin/`

---

## Estrutura de pastas

```
sistema_mesa_checkin_frontend/
├── Dockerfile                       ← imagem nginx que serve o build
├── azure-pipelines-{develop,homolog,main}.yml
├── angular.json · package.json
└── src/
    ├── environments/                ← endereço da API por ambiente (local, development, homolog, docker)
    ├── assets/                      ← i18n, imagens, tema do layout
    └── app/
        ├── auth/                    ← login, recuperar senha, alterar senha
        ├── admin/
        │   ├── painel/              ← tela inicial
        │   └── administracao/
        │       ├── acessibilidade/usuarios/   ← pesquisa e cadastro de usuários
        │       ├── acessibilidade/pessoas/    ← pesquisa, cadastro e cargas de pessoas
        │       ├── evento/                    ← pesquisa e cadastro de eventos
        │       ├── evento-pessoa/             ← participantes, check-in e mapa de assentos
        │       └── legendas/                  ← catálogo e configuração de legendas por evento
        ├── service/                 ← núcleo: autenticação, interceptor, base de CRUD, cache
        └── shared/                  ← layout, bases de tela, validadores, listas fixas
```

---

## Como rodar localmente

```bash
# Pré-requisitos
Node.js compatível com Angular 18, back-end no ar em http://localhost:8080/api-mesa-checkin/

# Instalação
npm install

# Iniciar
npm start
```

---

## Variáveis de ambiente

| Variável | Obrigatória | Descrição | Exemplo |
|---|---|---|---|
| `app_base_url` | sim, na imagem | Endereço da API; substituído no build ao iniciar o contêiner | — |

---

## Features implementadas neste repositório

→ ver a coluna **Repositórios** de [`modules/INDEX.md`](../modules/INDEX.md) e a seção `## Implementação` de cada N3.

---

## Convenções específicas deste repositório

### Padrão de testes
Karma + Jasmine, com cobertura enviada ao SonarQube pelo pipeline.

### Deploy
Azure Pipelines, um arquivo por ambiente (`develop`, `homolog`, `main`). O build é servido por nginx.
