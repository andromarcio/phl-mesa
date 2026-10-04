# Engenharia reversa — material de apoio

Insumos intermediários da engenharia reversa de 2026-09-30, que deu origem a esta instância. Não são especificação: são o **levantamento factual** de onde os N1, N2 e N3 foram tirados, guardado para que cada afirmação marcada 💻 possa ser conferida.

| Arquivo | O que é |
|---|---|
| [`backend-inventory.md`](./backend-inventory.md) | Inventário do servidor (`sistema_mesa_checkin_backend`): as 63 operações, autenticação e autorização, regras por área, mensagens literais, o que é gravado automaticamente, suspeitas de defeito e o que os testes cobrem — com `arquivo:linha` |
| [`frontend-inventory.md`](./frontend-inventory.md) | Inventário das telas (`sistema_mesa_checkin_frontend`): rotas, menu e perfis, cada tela com campos, colunas, ações e mensagens literais, o mapa de assentos em detalhe, serviços e operações chamadas, listas fixas e suspeitas — com `arquivo:linha` |
| [`tickets-jira.md`](./tickets-jira.md) | Lista dos tickets do projeto `PDTIC25148` no Jira e resumo fiel dos três que estavam em teste na data: `PDTIC25148-34`, `-35` e `-36` |

Os documentos legados (GPE001 a GPE006) estão na pasta acima, [`arquivos/`](../).

## Como foram produzidos

Os dois inventários saíram da **leitura** integral do código — nada foi compilado nem executado. O que depende de comportamento em execução está marcado, neles, como inferência. As cópias de código lidas não tinham histórico git; não se sabe a que versão correspondem, além de serem as entregues em 2026-09-30.

## Errata — o que a redação dos N3 corrigiu nos inventários

Ao escrever cada N3, o código foi relido nos pontos de dúvida. Onde o inventário e o código divergiam, **vale o código**, e o N3 já traz a versão corrigida. Os inventários foram mantidos como estavam; as correções são estas:

**Inventário do servidor**

- **Suspeita 2 (seção 6.1) — "a edição de evento não grava o conteúdo do anexo".** Vale para a operação de alteração, que a tela **não chama**: a tela grava a edição pela mesma operação da inclusão, que grava a imagem. Em troca, essa operação regrava Excluído = não e a condição de principal lida quando a tela abriu — efeito que o inventário não aponta. Ver `EVT-CAD-03 — Editar Evento`.
- **Suspeita 5 — CNPJ gravado no CPF.** Incompleta: além de gravar o CNPJ no CPF, a carga **apaga** o CPF da pessoa quando a planilha não traz CNPJ. Ver `EVT-CAD-07 — Carregar Convidados`.
- **Suspeita 17 — a carga de histórico "quebra (500)" com coluna extra.** Pelo código, a falha responde como erro de validação, com o texto técnico da conversão no detalhe. Ver `PES-CAD-07 — Carregar Histórico de Participação`.
- **Suspeita 19 — código de contato duplicado faz a consulta falhar.** Vale para as cargas de planilha. A importação de inscritos do CRM usa outra consulta e não falha: fica com o registro mais antigo. Ver `EVT-CAD-09 — Importar Inscritos do CRM`.
- **Suspeita 28 — "editar pessoa sem enviar a foto remove a foto".** É verdade para o servidor; pela tela a foto é mantida, porque o formulário reenvia a referência da foto guardada. Ver `PES-CAD-03 — Editar Pessoa`.
- **Seção 3.c — "linhas totalmente vazias são puladas".** Só é pulada a linha que não existe na planilha; a linha existente com células em branco conta como pessoa não encontrada.
- **Seção 1.3, operações 29 a 31.** Falta dizer que as listas de grupos de trabalho, temas e cargos **não** são filtradas por evento — vêm do sistema inteiro. Ver `EVT-PAR-01 — Pesquisar Participantes`.

**Inventário das telas**

- **Seção 4.12 — atualização automática.** A consulta repetida a cada 3 segundos refaz só os participantes do **mapa**; a lista paginada de participantes não se atualiza sozinha. Ver `EVT-PAR-01 — Pesquisar Participantes`.
- **Seção 4.14 — janela Gerenciar Legenda da Pessoa.** Falta dizer que "Legenda Atual" recebe só a legenda **manual**. Ver `EVT-PAR-04 — Consultar Legenda do Participante`.
- **Seção 4.19 — janela Salvar como preset.** Falta dizer que a janela se fecha antes da resposta do servidor: com nome repetido, o erro chega com a janela fechada. Ver `EVT-LEG-08 — Salvar Preset de Legendas`.
- **Seção 4.20 — aba De outro evento.** O inventário diz que a aba mostra a data do evento; a tela lê um campo com nome diferente do que o servidor envia, e a data não aparece. Ver `EVT-LEG-09 — Carregar Configuração de Legendas`.
- **Suspeita 46 (seção 8.4) — tratamento de erro das telas de legenda.** O contorno existe só nas duas páginas; as janelas Adicionar bloco e Carregar configuração não o têm.
- **Seção 4.5 — tela Pessoa.** Faltam dois comportamentos: os avisos da foto saem por um serviço de mensagens que a tela não exibe, e, depois de incluir, a tela não passa para o modo de edição — repetir "Criar" inclui outra pessoa. Ver `PES-CAD-02 — Cadastrar Pessoa`.
- **Seção 5 — mapa de assentos.** Faltam: a gravação automática pendente é cancelada ao sair do mapa; o atendimento e a legenda ficam fora da conferência que decide se o mapa mudou; a retirada do último participante sentado, como a limpeza geral, não é gravada. Ver `EVT-PAR-08`, `EVT-PAR-09` e `EVT-PAR-10`.
- **Seção 3 — telas de acesso.** Falta: a confirmação "Senha temporária enviada." sai por um serviço de mensagens que nenhuma das telas de acesso exibe. Ver `ACE-AUT-03 — Recuperar Senha`.

**Documento legado**

- GPE004 cita, no histórico da versão 1.1, o ticket "DTIC25148-32"; no Jira a chave é `PDTIC25148-32`.
