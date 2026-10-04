<!-- docqui: 4.1.0 | prompt: PROMPT_PROTOTYPE_FLOW_FULL | atualizado: 2026-10-04 -->
# Protótipo de Fluxo: Autenticação
> Feature Set: Autenticação — Major Feature Set: Acesso e Usuários
> Spec de referência: [../../../modules/acesso-usuarios/autenticacao/README.md](../../../modules/acesso-usuarios/autenticacao/README.md)

---

## Protótipos de fluxo

| Arquivo / Link | Formato | Status | Última revisão |
|---|---|---|---|
| [flow.html](./flow.html) | HTML gerado | 🎨 Mockup | 2026-10-04 |

---

## Telas cobertas neste fluxo

| Tela | Rota | Protótipo de estado |
|---|---|---|
| Acesso — Usuário, Senha com o olho, "Esqueceu a senha?" e Entrar | `/login` | — |
| Recuperar senha — aviso, Usuário, Recuperar senha e Voltar | `/recuperar-senha` | — |
| Alterar senha — troca obrigatória (aviso, sem Senha Atual) e troca voluntária (com Senha Atual) | `/alterar-senha` | — |
| Tela inicial — saudação "Seja bem-vindo ao Gestão de Participantes em Eventos" | `/dashboard-simples` | — |
| Menu do usuário — Nome, Login, Perfil e Email, Alterar Foto do Perfil, Alterar Senha e Logout | cabeçalho das telas internas | — |
| Alterar Imagem do Perfil — janela descrita só em GPE001 ⚠️ | janela sobre a tela inicial | — |

*O escopo desta geração é um fluxo por Feature Set; os protótipos de estado por feature (`PROMPT_PROTOTYPE_SCREEN_FULL`) não foram gerados.*

---

## Decisões de design deste fluxo

- As telas foram recuperadas do código-fonte da aplicação, e não desenhadas a partir do design system do kit: rótulos, mensagens e comportamento vêm do inventário extraído do `sistema_mesa_checkin_frontend` (`arquivos/engenharia-reversa/frontend-inventory.md`, seções 2.1 a 2.4, 3.1 a 3.8, 4.0 e 4.1), e o visual, das imagens de GPE001. A camada [`tema-gpe.css`](../../_biblioteca-ds/tema-gpe.css) reveste as classes `.dsc-*` com esse visual (decisão de 2026-10-04).
- As telas de acesso, de recuperação e de alteração de senha não têm o shell interno: ocupam a página inteira, com o formulário à esquerda e a área azul à direita, como no sistema. A ilustração da área azul não foi reproduzida. Os rótulos das telas de recuperação e de alteração aparecem com a fonte serifada que a aplicação deixa sem estilo; a regra `gpe-label-plain` ficou no próprio `flow.html`, como candidata ao tema.
- O acesso é simulado pelo login digitado: `ana.costa` (Administrador) chega à tela inicial; `secretaria.mesa` e `secretaria.checkin` seguem para os participantes do evento principal no fluxo de [Participantes](../../eventos/participantes/flow.html); `novo.usuario` cai na troca obrigatória; `secretaria.semprincipal`, `servico.fora` e qualquer outro login mostram os desvios descritos no N3. O painel de notas lista os logins e tem um seletor que preenche o acesso.
- O protótipo mostra o que o sistema faz hoje, inclusive o que o N3 marca com ⚠️: a troca voluntária na moldura de acesso, o "Voltar" que leva à tela de acesso, o destino único depois da troca de senha, as recusas da troca sem mensagem e a troca obrigatória que não é esquecida na mesma sessão. Onde o texto previsto provavelmente não aparece no sistema — o aviso "Alteração de senha obrigatória!" e a confirmação "Senha temporária enviada." —, o protótipo mostra o texto previsto e registra a dúvida no painel de notas.
- A janela "Alterar Imagem do Perfil" reproduz a imagem de GPE001, porque no sistema atual o item do menu não abre nada; a própria janela traz o aviso, e um seletor no painel de notas reproduz o comportamento atual.
- O menu do usuário traz os dados com o rótulo em negrito, como descreve o N3 de Consultar Dados do Usuário. O cabeçalho mostra as iniciais no lugar da foto e o perfil sob o nome, como nos demais protótipos.
- Os campos obrigatórios levam o asterisco do protótipo, que a tela real não mostra.

---

## Status geral

**Status**: 🎨 Mockup

**Aprovado por**: — *(preencher quando aprovado)*

---

*Links: [N2 da spec](../../../modules/acesso-usuarios/autenticacao/README.md) · [Protótipos do domínio](../README.md) · [Manifesto de protótipos](../../INDEX.md)*
