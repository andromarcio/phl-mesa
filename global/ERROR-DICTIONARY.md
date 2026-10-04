<!-- docqui: 3.0.1 | prompt: PROMPT_CONVERSION | atualizado: 2026-09-30 -->
# ERROR-DICTIONARY.md
> Dicionário centralizado de códigos de erro de API.
> Todo novo código de erro criado durante a especificação técnica (N3)
> deve ser registrado aqui para evitar duplicidade de chaves e garantir
> consistência no frontend (internacionalização / i18n).
>
> Padrão: `[DOMINIO]_[DESCRICAO]` em SCREAMING_SNAKE_CASE
>
> **Como referenciar nos N3**:
> No Mapeamento de erros (seção dev-only), cite a chave:
> `→ ver ERROR-DICTIONARY: AUTH_UNAUTHENTICATED`

---

## 1. Erros globais (qualquer rota)

Estes erros podem ocorrer em qualquer endpoint do sistema
e não são específicos de um domínio. *(baseline reutilizável — ajuste conforme a stack)*

| Código de erro | HTTP | Situação |
|---|---|---|
| `AUTH_UNAUTHENTICATED` | 401 | Token ausente ou assinatura inválida |
| `AUTH_TOKEN_EXPIRED` | 401 | Token válido, mas expirado — renovar via refresh |
| `AUTH_FORBIDDEN` | 403 | Usuário autenticado, mas sem permissão para a ação |
| `VALIDATION_ERROR` | 422 | Um ou mais campos no body/query são inválidos (ver `details`) |
| `FIELD_IMMUTABLE` | 422 | Tentativa de alterar um campo protegido via PATCH |
| `RESOURCE_NOT_FOUND` | 404 | Registro não existe |
| `RATE_LIMIT_EXCEEDED` | 429 | Excedeu limite de requisições por IP ou token |
| `INTERNAL_ERROR` | 500 | Falha genérica de servidor — nunca expor stack trace |

---

## 2. Erros de Pessoas

> Levantado por engenharia reversa do código em 2026-09-30 💻.

| Código de erro | HTTP | Situação |
|---|---|---|
| `PESSOA_COM_VINCULO_EVENTO` | 409 | Tentativa de excluir pessoa que participa de algum evento. Mensagem: "Não é possível remover a pessoa, pois ela já possui vínculo com evento." |

---

## 3. Erros sem código

> ⚠️ O GPE quase não usa códigos de erro. Fora o caso acima, toda regra de negócio violada no servidor responde com o mesmo envelope — resumo "Erro de validação" e o texto da regra no detalhe —, e toda falha inesperada, com "Erro interno" e o detalhe "Ocorreu um erro inesperado. Contate o suporte." 💻. Não há chave a citar: os N3 escrevem o **texto literal** no cenário, e os textos recorrentes estão em `global/MESSAGE-DICTIONARY.md`. Os códigos da seção 1 são a linha de base do framework e **não existem** no sistema — ficam como referência para uma evolução.

---

## Como adicionar novos erros

Ao criar ou atualizar um N3 e identificar a necessidade de um código
não listado acima, adicione-o à tabela do domínio correspondente:

```markdown
| `[DOMINIO]_[NOME]` | [HTTP] | [Situação que dispara o erro] |
```

**Regras**:
- Prefixo = nome do domínio em maiúsculas (`CONTACT_`, `AUTH_`, `TASK_`, etc.)
- Descrição em inglês, substantivo ou verbo no passado (`NOT_FOUND`, `DUPLICATE`, `FAILED`)
- Nunca criar dois códigos com o mesmo significado em domínios diferentes
- Registrar aqui **antes** de usar no N3

---

## Instrução para a LLM

Ao gerar a seção `Mapeamento de erros` de um N3 técnico (PROMPT_3B):
1. Verificar se o erro já existe neste dicionário — usar a chave existente
2. Se for novo: propor com ⚠️, aguardar aprovação e adicionar ao dicionário
3. Nunca criar chaves ad-hoc sem registrar aqui
4. Referenciar no N3: `→ ver ERROR-DICTIONARY: [CODIGO]`

> **Usado em (não escreva à mão)**: a seção `## Usado em (índice reverso)` ao final
> é **gerada** por `scripts/generate-usage-index.mjs` a partir das referências
> `→ ver`/`←` dos N3. Não edite à mão — rode o gerador (o CI valida que está fresco).

<!-- usado-em:gerado -->
## Usado em (índice reverso)

> Gerado por `scripts/generate-usage-index.mjs` a partir das referências `→ ver`/`←` nos N3. **Não editar à mão.**

| Entrada | Usado em |
|---|---|
| `PESSOA_COM_VINCULO_EVENTO` | `PES-CAD-04` |
<!-- /usado-em -->
