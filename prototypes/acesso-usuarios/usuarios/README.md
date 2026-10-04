<!-- docqui: 4.1.0 | prompt: PROMPT_PROTOTYPE_FLOW_FULL | atualizado: 2026-10-04 -->
# Protótipo de Fluxo: Usuários
> Feature Set: Usuários — Major Feature Set: Acesso e Usuários
> Spec de referência: [../../../modules/acesso-usuarios/usuarios/README.md](../../../modules/acesso-usuarios/usuarios/README.md)

---

## Protótipos de fluxo

| Arquivo / Link | Formato | Status | Última revisão |
|---|---|---|---|
| [flow.html](./flow.html) | HTML gerado | 🎨 Mockup | 2026-10-04 |

---

## Telas cobertas neste fluxo

| Tela | Rota | Protótipo de estado |
|---|---|---|
| Usuários — filtros, lista, Editar Usuário e Remover Usuário em cada linha | `/administracao-usuarios` | — |
| Usuário — inclusão ("Cadastrar Usuário", a partir de "Validar Login") e edição ("Atualizar Usuário") | `/administracao-usuario` e `/administracao-usuario/:login` | — |
| Remover Usuário — confirmação | janela sobre a tela Usuários | — |

*O escopo desta geração é um fluxo por Feature Set; os protótipos de estado por feature (`PROMPT_PROTOTYPE_SCREEN_FULL`) não foram gerados.*

---

## Decisões de design deste fluxo

- As telas foram recuperadas do código-fonte da aplicação, e não desenhadas a partir do design system do kit: rótulos, botões, colunas, dicas e mensagens vêm do inventário extraído do `sistema_mesa_checkin_frontend` (`arquivos/engenharia-reversa/frontend-inventory.md`, seções 4.0, 4.2 e 4.3), e o visual, das imagens "Pesquisar Usuário" e "Incluir / Editar Usuário" de GPE002. A camada [`tema-gpe.css`](../../_biblioteca-ds/tema-gpe.css) reveste as classes `.dsc-*` com esse visual (decisão de 2026-10-04).
- O protótipo mostra o que o sistema faz hoje, inclusive o que o N3 marca com ⚠️: o filtro Departamento Regional que surge sem opções, o Cargo sem obrigatoriedade, os dados do usuário interno bloqueados também na edição, a segunda instituição que substitui a primeira, o CPF com o primeiro dígito errado que mostra "Campo obrigatório." e o texto literal "O usuário informado já estas no sistema.". Cada desvio está no painel de notas do protótipo.
- O desfecho de "Validar Login" depende do login digitado, para que os seis caminhos do N3 possam ser percorridos: login já cadastrado, login interno do diretório, externo já conhecido do cadastro corporativo, e-mail novo, login sem formato de e-mail e falha do serviço. Os logins de cada caminho estão no painel de notas.
- A tela Usuários não tem quadro de mensagens, e o N3 conclui, pela leitura do código, que as mensagens de sucesso de incluir, atualizar e remover tendem a não aparecer. O protótipo as exibe por padrão e traz, no painel de notas, uma opção para ver a tela como o código indica, sem elas.
- A inclusão e a edição usam a mesma tela, como o código: na inclusão aparece primeiro só o Login com "Validar Login"; validado o login, surgem os quadros "Dados do Usuário", "Perfil de acesso ao sistema" e, escolhido o perfil, "Instituições Relacionadas". Na edição, o título e o botão viram "Atualizar Usuário" e o Login fica bloqueado, sem "Validar Login" nem "Limpar".
- A situação Ativo ou Inativo é só exibida: a ação de inativar é pendência do N2 e não foi desenhada.
- O menu horizontal e o menu do usuário levam aos fluxos dos outros Feature Sets.

---

## Status geral

**Status**: 🎨 Mockup

**Aprovado por**: — *(preencher quando aprovado)*

---

*Links: [N2 da spec](../../../modules/acesso-usuarios/usuarios/README.md) · [Protótipos do domínio](../README.md) · [Manifesto de protótipos](../../INDEX.md)*
