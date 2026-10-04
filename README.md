# GPE — Portal de Gestão de Participantes em Eventos — documentação

Instância do framework **docqui** (`docqui-engine`). A especificação vive em `modules/` (N0–N3), o contexto global em `global/` e os moldes/skills em `engine/` (somente-leitura, sincronizado do canônico).

A documentação foi gerada por engenharia reversa em 2026-09-30, a partir dos seis documentos legados em `arquivos/` (GPE001 a GPE006) e do código-fonte do back-end e do front-end (`repos/INDEX.md`). Todas as features estão em **rascunho**: o que precisa de olho humano antes da aprovação está em [`REVISAO-CONVERSAO.md`](REVISAO-CONVERSAO.md).

Para continuar a especificação, abra a sessão e acione a skill `analista-requisitos`.

## Site de documentação

O visualizador (`index.html` + `assets/`) lê artefatos **gerados**, não os `.md` em tempo real. Depois de mexer em qualquer `.md`, rode `node scripts/atualiza-pages.mjs` a partir da raiz — ele regenera, na ordem certa, o espelho da esteira, o mapa de features e a árvore; com `--com-docx`, também as Especificações Funcionais de `documentos/`. Para abrir, sirva a raiz (`npx serve` ou `python3 -m http.server`) e acesse a porta indicada. O `serve.json` mantém o `cleanUrls` desligado — ligado, toda página `.html` passa a redirecionar para o endereço sem a extensão — e traz uma regra só para a raiz, que entrega o `index.html` em vez da lista de arquivos.

O visualizador foi copiado do `transparencia-web` (repositório PHL) em 2026-10-01, com a identidade trocada para o GPE e quatro ajustes para o formato desta instância — todos comentados no `index.html`: o título do N1 no formato da 3.0.0 (`# Major Feature Set:`), a subseção dentro da `## Descrição` do N1, a leitura do front-matter em documento que abre com o carimbo docqui e o link de um N1 para outro.
