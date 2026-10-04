  // ============================================================================
  // LOGICA DO COMPORTAMENTO DO VISUALIZADOR DE DOCS
  // ============================================================================

  // Nome do projeto vindo de config.js (com fallback seguro)
  const APP_NAME = (globalThis.DOCS_CONFIG && DOCS_CONFIG.name) || "Docs";

  let currentFilePath = "";
  let inSearchMode = false;
  let openingResult = false;

  // Customização do marked para injetar tags customizadas para diagrama Mermaid e outros
  const renderer = new marked.Renderer();
  const originalCodeRenderer = renderer.code;

  renderer.code = function(code, language, escaped) {
    if (language === 'mermaid') {
      return `<div class="mermaid">${code}</div>`;
    }
    // Para blocos de código com linguagem normal, vamos renderizar normalmente
    return originalCodeRenderer.call(this, code, language, escaped);
  };
  
  // No Marked mais recente, podemos passar as opções no marked.parse ou setOptions
  // Links para protótipos abrem em outra aba: o protótipo é uma página inteira, e
  // trocar o documento em leitura pelo protótipo faz o leitor perder o lugar.
  const origLink = renderer.link;
  renderer.link = function (href, title, text) {
    let h = href, ti = title, tx = text;
    if (typeof href === 'object' && href !== null) { h = href.href; ti = href.title; tx = href.text; }
    const html = origLink.call(this, href, title, text);
    return /^prototypes\/.*\.html$/.test(String(h || ''))
      ? html.replace('<a ', '<a target="_blank" rel="noopener" ')
      : html;
  };

  marked.setOptions({
    renderer: renderer,
    gfm: true,
    // breaks: false (padrão) — quebra simples dentro do parágrafo NÃO vira <br>;
    // linhas "quebradas na fonte" fluem como texto corrido, igual ao GitHub.
    breaks: false,
    headerIds: true,
    mangle: false
  });

  // Carregar preferência de tema ANTES de inicializar o Mermaid (o tema dele depende disso)
  const savedTheme = localStorage.getItem('theme-pref');
  if (savedTheme === 'dark' || (!savedTheme && globalThis.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('app-dark');
  }

  // Carregar preferência de exibição dos detalhes técnicos (3B/dev-only).
  // Padrão: oculto (Modo PO) — só mostra se o usuário já ligou antes.
  if (localStorage.getItem('dev-only-pref') === 'show') {
    document.documentElement.classList.add('app-show-dev');
  }

  // Alterna a exibição das seções técnicas (bloco <div class="dev-only">, gerado
  // pela passada 3B do N3 — e, quando presente, pelo 1B do N1). Puro CSS: não
  // precisa re-renderizar o arquivo aberto.
  function toggleDevOnly() {
    const isOn = document.documentElement.classList.toggle('app-show-dev');
    localStorage.setItem('dev-only-pref', isOn ? 'show' : 'hide');
  }

  // Inicializa o diagrama Mermaid acompanhando o tema claro/escuro do app
  function initMermaid() {
    mermaid.initialize({
      startOnLoad: false,
      theme: document.documentElement.classList.contains('app-dark') ? 'dark' : 'default',
      securityLevel: 'loose',
      flowchart: { useMaxWidth: true, htmlLabels: true }
    });
  }
  initMermaid();

  // Função para mudar o tema claro/escuro
  function toggleTheme() {
    const isDark = document.documentElement.classList.toggle('app-dark');
    localStorage.setItem('theme-pref', isDark ? 'dark' : 'light');

    // Atualiza tema do Mermaid e redesenha se houver algum exibido
    initMermaid();
    if (currentFilePath === '__mapa__') {
      renderMapa();
    } else if (currentFilePath) {
      loadFile(currentFilePath, true);
    }
  }

  // Restaura a largura da sidebar definida pelo usuário (antes do render para evitar flash)
  const savedSidebarWidth = localStorage.getItem('sidebar-width');
  if (savedSidebarWidth) {
    document.documentElement.style.setProperty('--sidebar-width', savedSidebarWidth);
  }

  // Restaura o estado recolhido da sidebar (padrão: recolhida em telas estreitas)
  (function restoreSidebarCollapsed() {
    const saved = localStorage.getItem('sidebar-collapsed');
    const collapsed = saved === '1' || (saved === null && globalThis.innerWidth <= 1024);
    if (collapsed) document.getElementById('app').classList.add('is-sidebar-collapsed');
  })();

  // Redimensionamento da sidebar via arraste da alça
  (function enableSidebarResize() {
    const resizer = document.getElementById('resizer');
    const MIN_WIDTH = 200;
    let isResizing = false;

    function onMouseMove(e) {
      if (!isResizing) return;
      const maxWidth = Math.min(640, globalThis.innerWidth * 0.6);
      const width = Math.max(MIN_WIDTH, Math.min(maxWidth, e.clientX));
      document.documentElement.style.setProperty('--sidebar-width', width + 'px');
    }

    function onMouseUp() {
      if (!isResizing) return;
      isResizing = false;
      resizer.classList.remove('is-dragging');
      document.body.style.userSelect = '';
      document.body.style.cursor = '';
      const width = document.documentElement.style.getPropertyValue('--sidebar-width');
      if (width) localStorage.setItem('sidebar-width', width);
    }

    resizer.addEventListener('mousedown', (e) => {
      isResizing = true;
      resizer.classList.add('is-dragging');
      document.body.style.userSelect = 'none';
      document.body.style.cursor = 'col-resize';
      e.preventDefault();
    });

    document.addEventListener('mousemove', onMouseMove);
    document.addEventListener('mouseup', onMouseUp);
  })();

  // Recolhe/expande a sidebar EM FLUXO (nunca sobreposta — regra do PO: o menu
  // fica visível ou não). O estado é persistido; o hambúrguer alterna.
  function setSidebarCollapsed(collapsed) {
    document.getElementById('app').classList.toggle('is-sidebar-collapsed', collapsed);
    localStorage.setItem('sidebar-collapsed', collapsed ? '1' : '0');
    // O mapa escala para a largura disponível — re-layout ao mudar a largura útil.
    if (document.getElementById('mm-canvas')) requestAnimationFrame(mmLayout);
  }
  function toggleSidebar() {
    const app = document.getElementById('app');
    setSidebarCollapsed(!app.classList.contains('is-sidebar-collapsed'));
  }

  // Navega para um arquivo. Força o carregamento quando o hash já é o atual
  // (ex.: sair do modo pesquisa clicando no próprio doc/Home).
  function navigateTo(path) {
    // Em telas estreitas, escolher um item recolhe o menu para liberar a leitura.
    if (globalThis.innerWidth <= 1024) setSidebarCollapsed(true);
    // Tela especial "Mapa de features" (não é um arquivo .md).
    if (path === '__mapa__') {
      if (globalThis.location.hash.substring(1) === '__mapa__') renderMapa();
      else globalThis.location.hash = '__mapa__';
      return;
    }
    if (globalThis.location.hash.substring(1) === path) {
      loadFile(path, true);
    } else {
      globalThis.location.hash = path;
    }
  }

  // Estrutura a lista de arquivos de tree.js em uma árvore dsc-tree aninhada
  function buildTree(files) {
    const root = { name: "Root", type: "dir", children: {}, path: "" };
    
    files.forEach(filePath => {
      const parts = filePath.split('/');
      let current = root;
      
      parts.forEach((part, index) => {
        const isLast = index === parts.length - 1;
        const currentPath = parts.slice(0, index + 1).join('/');
        
        if (isLast) {
          current.children[part] = {
            name: part,
            type: "file",
            path: currentPath
          };
        } else {
          if (!current.children[part]) {
            current.children[part] = {
              name: part,
              type: "dir",
              children: {},
              path: currentPath
            };
          }
          current = current.children[part];
        }
      });
    });
    
    return root;
  }

  // Extrai um título legível do conteúdo Markdown (primeiro H1), sem prefixos como 'Domínio:', 'Feature Set:', 'Data Model:'
  function titleFromMarkdown(content) {
    const match = content.match(/^#\s+(.+)$/m);
    if (!match) return null;
    return match[1].replace(/^\s*(Major Feature Set|Domínio|Dominio|Feature Set|Data[\s-]Model)\s*[:\-—]*\s*/i, '').replace(/`/g, '').trim();
  }

  // Remove a extensão (.md, .html, .htm) para exibição
  function stripExt(name) {
    return name.replace(/\.(md|html?)$/i, '');
  }

  // Front-matter YAML e carimbo do engine no topo dos .md são metadados internos:
  // renderizados, os '---' viram réguas e o YAML vira prosa no topo da página.
  // Remove-os do texto exibido; sem front-matter, devolve o texto intacto.
  function stripFrontMatter(md) {
    const m = md.match(/^\uFEFF?(?:\s*<!--(?:(?!-->)[\s\S])*-->)*\s*---[ \t]*\r?\n([\s\S]*?)\r?\n---[ \t]*\r?\n?/);
    return (m && /^[\w-]+\s*:/m.test(m[1])) ? md.slice(m[0].length) : md;
  }

  // No engine o front-matter É conteúdo (templates com placeholders e
  // comentários didáticos) e permanece — mas os comentários YAML começam com
  // '#', que o Markdown lê como cabeçalho. Envolve o bloco '---...---' num
  // fence ```yaml``` para que apareça como código, não como títulos soltos.
  function fenceFrontMatter(md) {
    const re = /^(﻿?(?:\s*<!--[\s\S]*?-->)*\s*)---[ \t]*\r?\n([\s\S]*?)\r?\n---[ \t]*\r?\n?/;
    const m = md.match(re);
    if (!m || !/^[\w-]+\s*:/m.test(m[2])) return md;
    return m[1] + '```yaml\n' + m[2] + '\n```\n\n' + md.slice(m[0].length);
  }

  // O que vai para a tela: no engine o front-matter É conteúdo e permanece
  // (como código); no restante é ocultado por ser metadado interno.
  function contentForDisplay(path, md) {
    return path.startsWith('engine/') ? fenceFrontMatter(md) : stripFrontMatter(md);
  }

  // Resolve o rótulo de exibição de uma pasta na árvore lateral:
  // 'modules' vira 'Documentação' e seus subdiretórios usam o título do README.
  const FOLDER_LABELS = {
    'global/data-models': 'Mapa de Entidades por Domínio',
    'engine/templates/global/data-models': 'Mapa de Entidades por Domínio',
    'engine': 'Engine (doc-template-engine)',
  };

  function getFolderDisplayName(item) {
    if (item.path in FOLDER_LABELS) return FOLDER_LABELS[item.path];
    if (item.path === 'modules') return 'Documentação';

    if (item.path.startsWith('modules/') && typeof repoFilesContent !== 'undefined') {
      const readme = repoFilesContent[item.path + '/README.md'];
      if (readme) {
        const title = titleFromMarkdown(readme);
        if (title) return title;
      }
    }

    // Diretórios da raiz: exibe com a primeira letra maiúscula
    if (!item.path.includes('/')) {
      return item.name.charAt(0).toUpperCase() + item.name.slice(1);
    }

    return item.name;
  }

  // Pastas cujos arquivos .md devem ter o rótulo lido do primeiro H1 do conteúdo
  const TITLE_FROM_CONTENT_DIRS = [
    'global/data-models',
    'engine/templates/global/data-models',
  ];

  // Resolve o rótulo de um arquivo na árvore lateral.
  // Para arquivos de feature (3º nível de modules) e para arquivos dentro de
  // TITLE_FROM_CONTENT_DIRS, usa o título H1 do conteúdo Markdown.
  function getFileDisplayName(item) {
    if (typeof repoFilesContent !== 'undefined') {
      const parts = item.path.split('/');
      const parentPath = parts.slice(0, -1).join('/');

      const useTitleFromContent =
        (parts[0] === 'modules' && parts.length === 4) ||
        TITLE_FROM_CONTENT_DIRS.includes(parentPath);

      if (useTitleFromContent) {
        const content = repoFilesContent[item.path];
        if (content) {
          const title = titleFromMarkdown(content);
          if (title) return title;
        }
      }
    }

    return stripExt(item.name);
  }

  // Nome de exibição de um item da árvore (pasta ou arquivo)
  function getDisplayName(item) {
    return item.type === "dir" ? getFolderDisplayName(item) : getFileDisplayName(item);
  }

  // Localiza o arquivo de índice (INDEX.md ou README.md) dentro de uma pasta, se houver
  function findFolderIndexFile(dirNode) {
    const keys = Object.keys(dirNode.children);
    const pick = (name) => keys.find(k => k.toLowerCase() === name);
    const key = pick('index.md') || pick('readme.md');
    const child = key ? dirNode.children[key] : null;
    return child && child.type === 'file' ? child : null;
  }

  // Renderiza recursivamente o HTML da árvore de diretórios
  function renderTreeHTML(node, filterActive = false, isRoot = false) {
    let html = "";
    // Arquivo de índice da pasta: ocultado da listagem, pois a pasta o exibe ao ser clicada (mantido na busca)
    const indexFile = filterActive ? null : findFolderIndexFile(node);
    const childrenKeys = Object.keys(node.children).sort((a, b) => {
      const itemA = node.children[a];
      const itemB = node.children[b];
      // Pastas primeiro, depois arquivos
      if (itemA.type !== itemB.type) {
        return itemA.type === "dir" ? -1 : 1;
      }
      // Ordem alfabética pelo nome exibido (sem diferenciar acento/maiúsculas)
      return getDisplayName(itemA).localeCompare(getDisplayName(itemB), 'pt', { sensitivity: 'base' });
    });

    childrenKeys.forEach(key => {
      const item = node.children[key];
      // Oculta arquivos soltos na raiz do repositório (ex.: README.md, N0_PRODUCT_VISION.md)
      if (isRoot && item.type === "file") return;
      // Oculta o INDEX/README da própria pasta (acessível ao clicar nela)
      if (item === indexFile) return;
      if (item.type === "dir") {
        // Se a busca estiver ativa, deixamos as pastas abertas ('open') para exibir os resultados
        const isOpen = filterActive ? "open" : "";
        // Se a pasta tiver INDEX/README, clicar nela exibe esse arquivo
        const indexFile = findFolderIndexFile(item);
        const indexAttr = indexFile ? ` data-index-path="${indexFile.path}"` : "";
        const folderActive = indexFile && indexFile.path === currentFilePath ? " is-active" : "";
        html += `
          <details class="dsc-tree-folder" data-path="${item.path}" ${isOpen}>
            <summary class="dsc-tree-folder-title${folderActive}"${indexAttr}>
              <svg class="dsc-icon-folder" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
              </svg>
              <span>${getFolderDisplayName(item)}</span>
            </summary>
            <div class="dsc-tree-folder-content">
              ${renderTreeHTML(item, filterActive)}
            </div>
          </details>
        `;
      } else {
        const fileTitle = getFileDisplayName(item);
        const isActive = item.path === currentFilePath ? "is-active" : "";
        const isHtml = /\.html?$/i.test(item.path);
        const icon = isHtml
          ? `<svg class="dsc-icon-file" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>`
          : `<svg class="dsc-icon-file" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>`;
        html += `
          <a class="dsc-tree-file ${isActive}" href="#${item.path}" data-path="${item.path}">
            ${icon}
            <span>${fileTitle}</span>
          </a>
        `;
      }
    });
    
    return html || `<div style="padding: 8px 12px; font-size:12px; color:var(--text-muted)">Sem arquivos markdown.</div>`;
  }

  // Escapa HTML para inserir com segurança texto vindo dos arquivos
  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  }

  // Escapa o texto e destaca (mark) as ocorrências do termo
  function highlightTerm(text, term) {
    const escaped = escapeHtml(text);
    if (!term) return escaped;
    const re = new RegExp(escapeHtml(term).replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
    return escaped.replace(re, m => `<mark>${m}</mark>`);
  }

  // Monta um trecho do conteúdo ao redor da primeira ocorrência do termo
  function buildSnippet(content, lowerTerm, term) {
    const idx = content.toLowerCase().indexOf(lowerTerm);
    if (idx === -1) return '';
    const start = Math.max(0, idx - 50);
    const end = Math.min(content.length, idx + lowerTerm.length + 90);
    const raw = content.slice(start, end).replace(/\s+/g, ' ').trim();
    return (start > 0 ? '… ' : '') + highlightTerm(raw, term) + (end < content.length ? ' …' : '');
  }

  // Botão "voltar aos resultados" (reaproveitado por docs Markdown e protótipos)
  function backToResultsHtml(term) {
    return `
      <button type="button" class="dsc-search-back" onclick="handleSearch()">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="19" y1="12" x2="5" y2="12"></line>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
        <span>Voltar aos resultados de "${escapeHtml(term)}"</span>
      </button>
    `;
  }

  // Pesquisa: exibe os resultados na área de conteúdo, sem alterar o menu lateral
  function handleSearch() {
    const term = document.getElementById('searchInput').value.trim();

    if (!term) {
      // Sai do modo pesquisa e restaura o documento atual
      if (currentFilePath) loadFile(currentFilePath, true);
      return;
    }

    const lowerTerm = term.toLowerCase();
    const results = repoFiles.filter(path => {
      const parts = path.split('/');
      const filename = parts[parts.length - 1].replace(/\.md$/i, '').toLowerCase();
      const folderPath = parts.slice(0, -1).join('/').toLowerCase();
      const content = (typeof repoFilesContent !== 'undefined') ? repoFilesContent[path] : undefined;

      return filename.includes(lowerTerm) || folderPath.includes(lowerTerm)
        || (content !== undefined && content.toLowerCase().includes(lowerTerm));
    });

    renderSearchResults(term, lowerTerm, results);
  }

  // Renderiza a lista de resultados na área de conteúdo
  function renderSearchResults(term, lowerTerm, results) {
    inSearchMode = true;

    globalThis.document.title = `Pesquisa: ${term} — Documentação ${APP_NAME}`;
    document.getElementById('breadcrumb').innerHTML =
      '<li class="dsc-breadcrumb-item">Documentação</li><li class="dsc-breadcrumb-item">Pesquisa</li>';

    const contentDiv = document.getElementById('markdownContent');

    if (results.length === 0) {
      contentDiv.innerHTML = `
        <div class="dsc-empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <h2 class="dsc-title-sm">Nenhum resultado</h2>
          <p class="dsc-body-sm">Nada encontrado para <strong>"${escapeHtml(term)}"</strong>.</p>
        </div>
      `;
      return;
    }

    const itemsHtml = results.map(path => {
      const content = (typeof repoFilesContent !== 'undefined') ? repoFilesContent[path] : undefined;
      const fallback = stripExt(path.split('/').pop());
      const title = (content && titleFromMarkdown(content)) || fallback;
      const snippet = content ? buildSnippet(contentForDisplay(path, content), lowerTerm, term) : '';
      return `
        <a class="dsc-search-result" href="#${path}" data-path="${path}">
          <div class="dsc-search-result-title">${highlightTerm(title, term)}</div>
          <div class="dsc-search-result-path">${escapeHtml(path)}</div>
          ${snippet ? `<div class="dsc-search-result-snippet">${snippet}</div>` : ''}
        </a>
      `;
    }).join('');

    contentDiv.innerHTML = `
      <div class="dsc-search-results">
        <p class="dsc-search-results-count">${results.length} resultado(s) para "${escapeHtml(term)}"</p>
        ${itemsHtml}
      </div>
    `;

    // Ao escolher um resultado, abre o doc mantendo o termo (permite voltar aos resultados)
    contentDiv.querySelectorAll('.dsc-search-result').forEach(el => {
      el.addEventListener('click', function(e) {
        e.preventDefault();
        // Sem isto, o clique também é tratado pelo handler delegado de links
        // internos do Markdown (mais abaixo), que trata href="#..." como
        // âncora da página atual e sobrescreve o hash com
        // "arquivoAtual.md#resultado.md" — hash inválido, navegação quebrada.
        e.stopPropagation();
        openingResult = true;
        navigateTo(this.dataset.path);
      });
    });
  }

  // Marca um único item da árvore (arquivo ou pasta) como selecionado
  function setActiveTreeItem(el) {
    document.querySelectorAll('.dsc-sidebar .is-active').forEach(a => a.classList.remove('is-active'));
    if (el) el.classList.add('is-active');
  }

  // Renderiza a navegação inicial
  function renderNavigationTree(filesList, filterActive) {
    const treeData = buildTree(filesList);
    const nav = document.getElementById('treeNav');
    nav.innerHTML = renderTreeHTML(treeData, filterActive, true);
    
    // Vincular os cliques nos links gerados dinamicamente
    nav.querySelectorAll('.dsc-tree-file').forEach(el => {
      el.addEventListener('click', function(e) {
        e.preventDefault();
        navigateTo(this.dataset.path);
      });
    });

    // Clicar numa pasta: com INDEX/README exibe esse arquivo; sem índice apenas seleciona (destaca)
    nav.querySelectorAll('.dsc-tree-folder-title').forEach(el => {
      el.addEventListener('click', function(e) {
        const target = this.dataset.indexPath;
        if (target) {
          e.preventDefault();
          const details = this.parentElement;
          if (globalThis.location.hash.substring(1) === target) {
            if (inSearchMode) {
              // Em pesquisa: sai dos resultados e exibe o doc da pasta
              loadFile(target, true);
            } else {
              // Doc já exibido: alterna expandir/recolher
              details.open = !details.open;
            }
          } else {
            // Exibe o doc e garante a pasta expandida (loadFile aplica o destaque)
            details.open = true;
            globalThis.location.hash = target;
          }
        } else {
          // Pasta sem índice: apenas marca como selecionada (expande/recolhe nativamente)
          setActiveTreeItem(this);
        }
      });
    });
  }

  // Reconstrói e exibe o breadcrumb de forma intuitiva
  function updateBreadcrumb(path) {
    const bc = document.getElementById('breadcrumb');
    bc.innerHTML = '<li class="dsc-breadcrumb-item">Documentação</li>';
    
    if (!path) return;
    
    const parts = path.split('/');
    parts.forEach((part, index) => {
      const isLast = index === parts.length - 1;
      const cleanName = isLast ? stripExt(part) : part;
      
      const li = document.createElement('li');
      li.className = 'dsc-breadcrumb-item';
      li.innerText = cleanName;
      bc.appendChild(li);
    });
  }

  // Exibe um protótipo HTML em um iframe (preserva seus próprios estilos e caminhos relativos)
  function renderPrototype(path, fromSearch) {
    const contentDiv = document.getElementById('markdownContent');
    const searchEl = document.getElementById('searchInput');
    const term = searchEl ? searchEl.value.trim() : '';
    const backBar = (fromSearch && term) ? backToResultsHtml(term) : '';
    contentDiv.innerHTML = backBar + `
      <div class="dsc-proto-toolbar">
        <span class="dsc-badge-path">${path}</span>
        <a class="dsc-proto-open" href="${path}" target="_blank" rel="noopener">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
            <polyline points="15 3 21 3 21 9"></polyline>
            <line x1="10" y1="14" x2="21" y2="3"></line>
          </svg>
          <span>Abrir em nova aba</span>
        </a>
      </div>
      <iframe class="dsc-proto-frame" src="${path}" title="Protótipo: ${escapeHtml(path)}"></iframe>
    `;
  }

  // ── Tela "Mapa de features" ────────────────────────────────────────────────
  // Mesmo molde do protótipo (prototypes/aval/mapa-features.html): árvore
  // navegável Produto → domínios (N1) → feature sets (N2) → features (N3), com a
  // descrição sob cada nó. Cada nó abre o respectivo artefato numa NOVA aba.
  // Dados: assets/mapa-data.js (window.AVAL_MAPA), gerado por gera-mapa-features.mjs.

  function mmEsc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

  // Link "abrir artefato" — nova aba, e não dispara o recolher do card.
  function mmOpenLink(path) {
    if (!path) return '';
    return '<a class="mm-open" href="index.html#' + encodeURI(path) + '" target="_blank" rel="noopener"'
      + ' title="Abrir o artefato em nova aba" onclick="event.stopPropagation()">'
      + '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
      + '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>'
      + '<span>abrir</span></a>';
  }

  function mmCard(cls, dataText, badge, nome, desc, foot, kidsHTML, leaf) {
    return '<div class="mm-node ' + cls + (leaf ? ' mm-leaf' : '') + '" data-text="' + mmEsc(dataText).toLowerCase() + '">'
      + '<div class="mm-card" onclick="mmToggle(this)">'
      + '<div class="mm-badge">' + badge + '</div>'
      + '<div class="mm-name">' + mmEsc(nome) + '</div>'
      + (desc ? '<div class="mm-desc">' + mmEsc(desc) + '</div>' : '')
      + (foot || '')
      + '</div>'
      + (kidsHTML ? '<div class="mm-kids"><div class="mm-bus"></div>' + kidsHTML + '</div>' : '')
      + '</div>';
  }

  // Camada de código de uma feature: os arquivos reais do back/front, agrupados por
  // camada (back) e tipo (front). Rastreabilidade spec → código dentro do mapa.
  const MM_COD_ORDEM_BACK = ['api', 'aplicação', 'domínio', 'workers', 'infra', 'migração', 'config', 'outro', 'teste'];
  const MM_COD_ORDEM_FRONT = ['rota', 'componente', 'template', 'estilo', 'serviço', 'spec', 'outro'];
  function mmCodeRepo(titulo, arr, ordem) {
    if (!arr || !arr.length) return '';
    const grupos = {};
    arr.forEach(function (x) { (grupos[x.kind] = grupos[x.kind] || []).push(x.path); });
    const corpo = ordem.filter(k => grupos[k]).map(function (k) {
      const files = grupos[k].map(p => '<li class="mm-cf">' + mmEsc(p) + '</li>').join('');
      return '<div class="mm-cg"><span class="mm-ck">' + mmEsc(k) + '</span><ul class="mm-cfl">' + files + '</ul></div>';
    }).join('');
    return '<div class="mm-crepo"><div class="mm-crh">' + titulo + '<span class="mm-crn">' + arr.length + ' arq.</span></div>' + corpo + '</div>';
  }
  function mmCodeLayer(f) {
    const c = f.codigo; if (!c || (!c.back.length && !c.front.length)) return '';
    return '<div class="mm-code">'
      + mmCodeRepo('back-end · siesa-backend', c.back, MM_COD_ORDEM_BACK)
      + mmCodeRepo('front-end · siesa-frontend', c.front, MM_COD_ORDEM_FRONT)
      + '</div>';
  }

  // Zoom manual dos nós: null = auto-ajuste à largura; número = override do usuário.
  let mmZoom = null;

  function renderMapa() {
    currentFilePath = '__mapa__';
    inSearchMode = false;
    const searchEl = document.getElementById('searchInput');
    if (searchEl) searchEl.value = '';
    globalThis.document.title = 'Mapa de features — Documentação ' + APP_NAME;

    // Estado ativo no menu lateral
    document.querySelectorAll('.dsc-sidebar .is-active').forEach(el => el.classList.remove('is-active'));
    document.querySelectorAll('.dsc-tree-file').forEach(el => { if (el.dataset.path === '__mapa__') el.classList.add('is-active'); });

    const bc = document.getElementById('breadcrumb');
    if (bc) bc.innerHTML = '<li class="dsc-breadcrumb-item">Documentação</li><li class="dsc-breadcrumb-item">Mapa de features</li>';

    const contentDiv = document.getElementById('markdownContent');
    const M = globalThis.AVAL_MAPA;
    if (!M) {
      contentDiv.innerHTML = '<div class="dsc-empty-state">'
        + '<h2 class="dsc-title-sm">Mapa de features indisponível</h2>'
        + '<p class="dsc-body-sm">O arquivo <strong>assets/mapa-data.js</strong> não foi carregado. Rode <code>scripts/regen.sh</code> (ou <code>node scripts/gera-mapa-features.mjs</code>) e recarregue a página.</p></div>';
      return;
    }

    const prodOpen = M.produto.path
      ? '<p class="mm-product-open">' + mmOpenLink(M.produto.path).replace('<span>abrir</span>', '<span>abrir a visão do produto</span>') + '</p>'
      : '';
    contentDiv.innerHTML = ''
      + '<div class="mapa-screen">'
      +   '<div class="mm-top">'
      +     '<div class="mm-top-row">'
      +       '<div class="mm-product">'
      +         '<div class="mm-product-name">' + mmEsc(M.produto.nome) + ' <small>· Mapa de features</small></div>'
      +         prodOpen
      +       '</div>'
      +       '<div class="mm-right">'
      +         '<div class="mm-controls">'
      +           '<span class="mm-kpi" id="mm-kpi-dom">— domínios</span>'
      +           '<span class="mm-kpi" id="mm-kpi-fs">— feature sets</span>'
      +           '<span class="mm-kpi" id="mm-kpi-feat">— features</span>'
      +           '<span class="mm-kpi" id="mm-kpi-gap">— cobertura</span>'
      +           '<span class="mm-kpi" id="mm-kpi-code">— código</span>'
      +           '<span class="mm-search"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><path d="m21 21-4.35-4.35"></path></svg>'
      +             '<input type="search" id="mm-busca" placeholder="Filtrar por nome ou ID" oninput="mmSearch(this.value)" aria-label="Filtrar o mapa"></span>'
      +         '</div>'
      +         '<div class="mm-actions">'
      +           '<button class="mm-btn" onclick="mmAll(false)">Expandir tudo</button>'
      +           '<button class="mm-btn" onclick="mmAll(true)">Recolher tudo</button>'
      +           '<button class="mm-btn" id="mm-btn-desc" aria-pressed="false" onclick="mmToggleDesc()">Ocultar descrição</button>'
      +           '<button class="mm-btn" id="mm-btn-gaps" onclick="mmOnlyGaps(this.classList.toggle(\'is-on\'))">Só lacunas</button>'
      +           '<span class="mm-zoom" role="group" aria-label="Zoom dos nós">'
      +             '<button class="mm-btn mm-zoom-btn" onclick="mmZoomBy(-0.1)" aria-label="Reduzir zoom — visão mais ampla" title="Reduzir — visão mais ampla">&minus;</button>'
      +             '<button class="mm-btn mm-zoom-fit" onclick="mmZoomFit()" title="Ajustar à largura" aria-label="Ajustar à largura"><span id="mm-zoom-val">100%</span></button>'
      +             '<button class="mm-btn mm-zoom-btn" onclick="mmZoomBy(0.1)" aria-label="Aumentar zoom" title="Aumentar">+</button>'
      +           '</span>'
      +         '</div>'
      +       '</div>'
      +     '</div>'
      +     '<p class="mm-product-desc"><strong>Domínios</strong> (N1) → <strong>feature sets</strong> (N2) → <strong>features</strong> (N3). Clique num nó para abrir ou fechar; <strong>abrir</strong> leva ao artefato em nova aba. Cada feature abre a <strong>camada de código</strong> — os arquivos reais do <strong>back-end</strong> e do <strong>front-end</strong> que a implementam.</p>'
      +     '<div class="mm-legend">'
      +       '<span class="lg"><span class="sw" style="border-left-color:#005CA9"></span> N1 · Domínio</span>'
      +       '<span class="lg"><span class="sw" style="border-left-color:#2E86C1"></span> N2 · Feature set</span>'
      +       '<span class="lg"><span class="sw" style="border-left-color:#7C93A8"></span> N3 · Feature</span>'
      +       '<span class="lg"><span class="mm-status st-em-desenvolvimento"></span> requisitos aprovados / implementado</span>'
      +       '<span class="lg"><span class="mm-status st-rascunho"></span> rascunho</span>'
      +       '<span class="lg"><span class="mm-code-badge">‹›</span> abre o código back/front</span>'
      +     '</div>'
      +   '</div>'
      +   '<div class="mm-wrap"><div id="mm-canvas"></div></div>'
      + '</div>';

    const doms = M.dominios.map(function (d) {
      if (!d.fss.length) {
        const gfoot = '<div class="mm-foot"><span class="mm-gap-badge">sem feature sets — a especificar</span>' + mmOpenLink(d.path) + '</div>';
        return mmCard('lvl-n1 mm-gap', 'lacuna a especificar ' + d.sigla + ' ' + d.nome + ' ' + d.desc, 'N1 · ' + mmEsc(d.sigla), d.nome, d.desc, gfoot, '', true);
      }
      const fss = d.fss.map(function (fs) {
        if (!fs.feats.length) {
          const gfoot = '<div class="mm-foot"><span class="mm-gap-badge">sem N3 — a especificar</span>' + mmOpenLink(fs.path) + '</div>';
          return mmCard('lvl-n2 mm-gap', 'lacuna a especificar ' + fs.sigla + ' ' + fs.nome + ' ' + fs.desc, 'N2 · ' + mmEsc(fs.sigla), fs.nome, fs.desc, gfoot, '', true);
        }
        const feats = fs.feats.map(function (f) {
          const nBE = f.codigo ? f.codigo.back.length : 0, nFE = f.codigo ? f.codigo.front.length : 0;
          const temCod = (nBE + nFE) > 0;
          const codeBadge = '<span class="mm-code-badge' + (temCod ? '' : ' mm-code-none') + '" title="arquivos de código vinculados (back/front)">‹›'
            + (nBE ? ' BE ' + nBE : '') + (nFE ? ' FE ' + nFE : '') + (temCod ? '' : ' —') + '</span>';
          const foot = '<div class="mm-foot"><span class="mm-status st-' + mmEsc(f.estado) + '"></span>'
            + (f.mvp ? '<span class="mm-mvp">MVP</span>' : '')
            + mmOpenLink(f.path) + codeBadge
            + (temCod ? '<span class="mm-caret">▸</span>' : '') + '</div>';
          const codeText = temCod ? f.codigo.back.concat(f.codigo.front).map(x => x.path).join(' ') : '';
          return mmCard('lvl-n3' + (temCod ? ' mm-codeonly' : ''), f.id + ' ' + f.nome + ' ' + f.desc + ' ' + codeText,
            'N3 · ' + mmEsc(f.id), f.nome, f.desc, foot, mmCodeLayer(f), !temCod);
        }).join('');
        const foot = '<div class="mm-foot"><span class="mm-count">' + fs.feats.length + ' feature' + (fs.feats.length === 1 ? '' : 's') + '</span>' + mmOpenLink(fs.path) + '<span class="mm-caret">▸</span></div>';
        return mmCard('lvl-n2', fs.sigla + ' ' + fs.nome + ' ' + fs.desc, 'N2 · ' + mmEsc(fs.sigla), fs.nome, fs.desc, foot, feats, false);
      }).join('');
      const foot = '<div class="mm-foot"><span class="mm-count">' + d.fss.length + ' feature set' + (d.fss.length === 1 ? '' : 's') + '</span>' + mmOpenLink(d.path) + '<span class="mm-caret">▸</span></div>';
      return mmCard('lvl-n1', d.sigla + ' ' + d.nome + ' ' + d.desc, 'N1 · ' + mmEsc(d.sigla), d.nome, d.desc, foot, fss, false);
    }).join('');
    document.getElementById('mm-canvas').innerHTML = doms;

    document.getElementById('mm-kpi-dom').textContent = M.kpi.dominios + ' domínios';
    document.getElementById('mm-kpi-fs').textContent = M.kpi.fss + ' feature sets';
    document.getElementById('mm-kpi-feat').textContent = M.kpi.feats + ' features';
    const _gaps = (M.kpi.fssVazios || 0) + (M.kpi.domsVazios || 0);
    const _kg = document.getElementById('mm-kpi-gap');
    if (_kg) {
      const totN2 = M.kpi.fss || 0;
      const cob = totN2 ? Math.round(100 * (totN2 - (M.kpi.fssVazios || 0)) / totN2) : 100;
      _kg.textContent = _gaps ? (_gaps + ' lacuna' + (_gaps === 1 ? '' : 's') + ' · cobertura ' + cob + '%') : ('cobertura ' + cob + '% · sem lacunas');
      _kg.classList.toggle('is-gap', _gaps > 0);
    }
    const _bg = document.getElementById('mm-btn-gaps');
    if (_bg) _bg.style.display = _gaps ? '' : 'none';

    const _kc = document.getElementById('mm-kpi-code');
    if (_kc) {
      if (M.kpi.codBackend || M.kpi.codFrontend) {
        _kc.textContent = 'código: ' + (M.kpi.arqBack || 0) + ' back · ' + (M.kpi.arqFront || 0) + ' front';
        _kc.title = (M.kpi.featComBack || 0) + ' de ' + M.kpi.feats + ' features com back-end · ' + (M.kpi.featComFront || 0) + ' com front-end';
      } else { _kc.style.display = 'none'; }
    }

    mmZoom = null; // cada render (re)começa em auto-ajuste à largura
    mmResetCollapse();
    // Preferência "ocultar descrição" (persistida): reaplica e reposiciona os buses.
    let _hideDesc = false;
    try { _hideDesc = localStorage.getItem('mapa-hide-desc') === '1'; } catch (e) {}
    mmSetDesc(_hideDesc);
    const scroller = document.querySelector('.dsc-main-content-scroll');
    if (scroller) scroller.scrollTop = 0;
  }

  // Estado inicial: domínios (N1) abertos, feature sets (N2) recolhidos, e as features
  // (N3) recolhidas — a camada de código fica escondida até clicar na feature.
  function mmResetCollapse() {
    document.querySelectorAll('#mm-canvas .mm-node').forEach(n => n.classList.remove('mm-collapsed'));
    document.querySelectorAll('#mm-canvas .mm-node.lvl-n2, #mm-canvas .mm-node.lvl-n3').forEach(n => n.classList.add('mm-collapsed'));
  }
  function mmToggle(card) {
    const n = card.closest('.mm-node');
    if (n.classList.contains('mm-leaf')) return;
    n.classList.toggle('mm-collapsed');
    mmLayout();
  }
  function mmAll(collapse) {
    document.querySelectorAll('#mm-canvas .mm-node:not(.mm-leaf)').forEach(n => n.classList.toggle('mm-collapsed', collapse));
    mmLayout();
  }
  // Escala o canvas: zoom manual do usuário (mmZoom) ou, se null, auto-ajuste à largura.
  function mmFit() {
    const canvas = document.getElementById('mm-canvas');
    if (!canvas) return;
    const wrap = canvas.parentElement;
    if (!wrap) return;
    canvas.style.zoom = '1';
    if (mmZoom != null) {
      canvas.style.zoom = String(mmZoom);
    } else {
      const content = canvas.scrollWidth;
      if (content > 0) canvas.style.zoom = String(Math.max(1, Math.min((wrap.clientWidth - 30) / content, 2)));
    }
    mmZoomLabel();
  }
  // Zoom manual dos nós: −/+ passo de 10%, entre 30% e 200%; o % clica para "ajustar".
  const MM_ZOOM_MIN = 0.3, MM_ZOOM_MAX = 2;
  function mmZoomEfetivo() {
    if (mmZoom != null) return mmZoom;
    const canvas = document.getElementById('mm-canvas');
    return canvas ? (parseFloat(canvas.style.zoom) || 1) : 1;
  }
  function mmZoomLabel() {
    const el = document.getElementById('mm-zoom-val');
    if (el) el.textContent = Math.round(mmZoomEfetivo() * 100) + '%';
    const fit = document.querySelector('.mm-zoom-fit');
    if (fit) fit.classList.toggle('is-on', mmZoom != null);
  }
  function mmZoomBy(step) {
    mmZoom = Math.max(MM_ZOOM_MIN, Math.min(mmZoomEfetivo() + step, MM_ZOOM_MAX));
    const canvas = document.getElementById('mm-canvas');
    if (canvas) canvas.style.zoom = String(mmZoom);
    mmZoomLabel();
  }
  function mmZoomFit() { // volta ao auto-ajuste à largura
    mmZoom = null;
    mmLayout();
  }
  // Posiciona a barra vertical (bus) entre o centro do 1º e do último filho visível.
  function mmLayout() {
    const canvas = document.getElementById('mm-canvas');
    if (!canvas) return;
    canvas.style.zoom = '1';
    document.querySelectorAll('#mm-canvas .mm-kids').forEach(function (k) {
      const bus = k.querySelector(':scope > .mm-bus');
      if (!bus) return;
      if (!k.offsetParent) return; // dentro de nó recolhido
      const nodes = [].slice.call(k.children).filter(c => c.classList && c.classList.contains('mm-node') && !c.classList.contains('mm-hidden'));
      if (nodes.length < 1) { bus.style.display = 'none'; return; }
      bus.style.display = 'block';
      const f = nodes[0], l = nodes[nodes.length - 1];
      const top = f.offsetTop + f.offsetHeight / 2;
      const bot = l.offsetTop + l.offsetHeight / 2;
      bus.style.top = top + 'px';
      bus.style.height = Math.max(0, bot - top) + 'px';
    });
    mmFit();
  }
  function mmFilterNode(n, term) {
    const kids = n.querySelector(':scope > .mm-kids');
    let childMatch = false;
    if (kids) {
      [].slice.call(kids.children).forEach(function (c) {
        if (c.classList && c.classList.contains('mm-node')) { if (mmFilterNode(c, term)) childMatch = true; }
      });
    }
    const selfMatch = term && (n.getAttribute('data-text') || '').indexOf(term) >= 0;
    n.classList.toggle('mm-hit', !!selfMatch);
    const keep = selfMatch || childMatch;
    n.classList.toggle('mm-hidden', !keep);
    if (childMatch) n.classList.remove('mm-collapsed');
    return keep;
  }
  function mmSearch(v) {
    const term = (v || '').trim().toLowerCase();
    if (!term) {
      document.querySelectorAll('#mm-canvas .mm-node').forEach(n => n.classList.remove('mm-hidden', 'mm-hit'));
      mmResetCollapse();
      mmLayout();
      return;
    }
    document.querySelectorAll('#mm-canvas > .mm-node').forEach(r => mmFilterNode(r, term));
    mmLayout();
  }

  // Filtro "só lacunas": mantém visíveis apenas os ramos com lacuna (mm-gap) e seus ancestrais.
  function mmGapKeep(n) {
    const kids = n.querySelector(':scope > .mm-kids');
    let childKeep = false;
    if (kids) [].slice.call(kids.children).forEach(function (c) {
      if (c.classList && c.classList.contains('mm-node')) { if (mmGapKeep(c)) childKeep = true; }
    });
    const keep = n.classList.contains('mm-gap') || childKeep;
    n.classList.toggle('mm-hidden', !keep);
    if (childKeep) n.classList.remove('mm-collapsed');
    return keep;
  }
  function mmOnlyGaps(on) {
    if (!document.getElementById('mm-canvas')) return;
    if (on) {
      document.querySelectorAll('#mm-canvas > .mm-node').forEach(r => mmGapKeep(r));
    } else {
      document.querySelectorAll('#mm-canvas .mm-node').forEach(n => n.classList.remove('mm-hidden'));
      mmResetCollapse();
    }
    mmLayout();
  }

  // Alterna a densidade dos nós: oculta a descrição, deixando só o código (badge),
  // o nome e o status. Preferência persistida — sobrevive à navegação e ao tema.
  function mmSetDesc(hide) {
    const canvas = document.getElementById('mm-canvas');
    if (canvas) canvas.classList.toggle('mm-hide-desc', !!hide);
    const btn = document.getElementById('mm-btn-desc');
    if (btn) {
      btn.classList.toggle('is-on', !!hide);
      btn.textContent = hide ? 'Mostrar descrição' : 'Ocultar descrição';
      btn.setAttribute('aria-pressed', hide ? 'true' : 'false');
    }
    try { localStorage.setItem('mapa-hide-desc', hide ? '1' : '0'); } catch (e) {}
    mmLayout();
  }
  function mmToggleDesc() {
    const canvas = document.getElementById('mm-canvas');
    mmSetDesc(!(canvas && canvas.classList.contains('mm-hide-desc')));
  }

  // Faz o fetch do arquivo Markdown e renderiza na tela
  async function loadFile(path, forceRerender = false) {
    if (!path) return;
    
    // Evita recarregar se for o mesmo arquivo e não for pedido rerender
    if (currentFilePath === path && !forceRerender) return;

    // Abrir um documento encerra a lista de resultados. Se veio de um resultado,
    // mantém o termo para permitir "voltar aos resultados"; caso contrário, limpa a busca.
    const fromSearch = openingResult;
    openingResult = false;
    const searchEl = document.getElementById('searchInput');
    if (!fromSearch && searchEl) searchEl.value = '';
    inSearchMode = false;

    currentFilePath = path;

    // Atualiza a seleção no menu lateral: limpa tudo e marca o arquivo atual
    // e a pasta cujo índice (INDEX/README) está sendo exibido
    document.querySelectorAll('.dsc-sidebar .is-active').forEach(el => el.classList.remove('is-active'));
    document.querySelectorAll('.dsc-tree-file').forEach(el => {
      if (el.dataset.path === path) el.classList.add('is-active');
    });
    document.querySelectorAll('.dsc-tree-folder-title[data-index-path]').forEach(el => {
      if (el.dataset.indexPath === path) el.classList.add('is-active');
    });

    const contentDiv = document.getElementById('markdownContent');
    
    // Nome limpo para o título da aba do navegador
    const parts = path.split('/');
    const cleanTitle = stripExt(parts[parts.length - 1]);
    globalThis.document.title = `${cleanTitle} — Documentação ${APP_NAME}`;
    
    updateBreadcrumb(path);

    // Protótipos HTML: exibidos em iframe (não renderizados como Markdown)
    if (/\.html?$/i.test(path)) {
      renderPrototype(path, fromSearch);
      return;
    }

    // Adiciona loader na tela de leitura
    contentDiv.innerHTML = `
      <div class="dsc-loader">
        <div class="dsc-spinner"></div>
        <p class="dsc-body-sm dsc-text-muted">Carregando conteúdo de [${cleanTitle}]...</p>
      </div>
    `;
    
    try {
      let mdText = "";
      
      // Tenta obter o conteúdo embutido no tree.js (resolve CORS no file://)
      if (typeof repoFilesContent !== 'undefined' && repoFilesContent[path] !== undefined) {
        mdText = repoFilesContent[path];
      } else {
        // Fallback de requisição de rede
        const response = await fetch(path);
        if (!response.ok) {
          throw new Error(`Erro HTTP: ${response.status} - ${response.statusText}`);
        }
        mdText = await response.text();
      }
      
      // Renderiza Markdown (sem o front-matter/carimbo do topo — metadados internos)
      const htmlText = marked.parse(contentForDisplay(path, mdText));

      // Barra "voltar aos resultados" quando o doc foi aberto a partir da pesquisa
      const term = searchEl ? searchEl.value.trim() : '';
      const backBar = (fromSearch && term) ? backToResultsHtml(term) : '';

      // Renderiza o HTML do Markdown (o caminho já aparece no breadcrumb)
      contentDiv.innerHTML = backBar + `
        <div class="dsc-markdown-body-rendered">
          ${htmlText}
        </div>
      `;
      
      // Marca células <td> cujo único conteúdo é <code> (sem texto fora do elemento) para remover estilo badge
      contentDiv.querySelectorAll('.dsc-markdown-body-rendered td').forEach(td => {
        let hasOutsideText = false;
        for (const node of td.childNodes) {
          if (node.nodeType === Node.TEXT_NODE && node.textContent.trim()) {
            hasOutsideText = true;
            break;
          }
        }
        if (!hasOutsideText && td.querySelector('code')) {
          td.classList.add('td-code-only');
        }
      });

      // Tabelas cuja primeira coluna do cabeçalho é "#" (números P-NNN das
      // pendências, IDs de contagem/critérios): 80px fixos e sem quebra de linha
      contentDiv.querySelectorAll('.dsc-markdown-body-rendered table').forEach(tb => {
        const th = tb.querySelector('th');
        if (th && th.textContent.trim() === '#') tb.classList.add('tbl-col-num');
      });

      // Tabela de Changelog (primeira coluna do cabeçalho "Data"): exibe a data
      // em DD/MM/AAAA (a fonte continua em AAAA-MM-DD, formato ordenável) e
      // fixa a largura da coluna para nunca quebrar linha.
      contentDiv.querySelectorAll('.dsc-markdown-body-rendered table').forEach(tb => {
        const th = tb.querySelector('th');
        if (!th || th.textContent.trim() !== 'Data') return;
        tb.classList.add('tbl-col-date');
        tb.querySelectorAll('td:first-child').forEach(td => {
          const m = td.textContent.trim().match(/^(\d{4})-(\d{2})-(\d{2})$/);
          if (m) td.textContent = `${m[3]}/${m[2]}/${m[1]}`;
        });
      });

      // Exibição dos blocos ```gherkin: título do Cenário em negrito, as
      // palavras-chave (Dado/Quando/Então/E/Mas) traduzidas e esmaecidas (o
      // texto do passo é o conteúdo principal) e as linhas de comentário (#)
      // esmaecidas — só na renderização; o .md fonte continua em inglês
      // (Given/When/Then/And/But) e sem essas marcações.
      const GHERKIN_KEYWORDS = { Given: 'Dado', When: 'Quando', Then: 'Então', And: 'E', But: 'Mas' };
      contentDiv.querySelectorAll('.dsc-markdown-body-rendered pre code.language-gherkin').forEach(el => {
        const html = el.innerHTML.split('\n').map(line => {
          const scenarioMatch = line.match(/^(\s*)(Scenario(?:\s+Outline)?:.*)$/);
          if (scenarioMatch) return `${scenarioMatch[1]}<strong>${scenarioMatch[2]}</strong>`;
          const commentMatch = line.match(/^(\s*)(#.*)$/);
          if (commentMatch) return `${commentMatch[1]}<span class="dsc-gherkin-comment">${commentMatch[2]}</span>`;
          const stepMatch = line.match(/^(\s*)(Given|When|Then|And|But)\b/);
          if (stepMatch) {
            const [, indent, kw] = stepMatch;
            const rest = line.slice(indent.length + kw.length);
            return `${indent}<strong class="dsc-gherkin-kw">${GHERKIN_KEYWORDS[kw]}</strong>${rest}`;
          }
          return line;
        }).join('\n');
        el.innerHTML = html;
      });

      // Pré-processamento robusto de blocos Mermaid gerados pelo interpretador Markdown (evita falhas de versão do marked)
      contentDiv.querySelectorAll('pre code.language-mermaid, pre code.mermaid, code.language-mermaid').forEach(el => {
        const parent = el.closest('pre');
        const codeText = el.textContent || el.innerText;
        const div = document.createElement('div');
        div.className = 'mermaid';
        div.textContent = codeText;
        if (parent) {
          parent.parentNode.replaceChild(div, parent);
        } else {
          el.parentNode.replaceChild(div, el);
        }
      });
      
      // Renderizar Mermaid se houver diagramas na tela
      if (mdText.includes('```mermaid') || mdText.includes('class="mermaid"')) {
        try {
          // No Mermaid moderno, a chamada para renderizar os elementos do DOM é assíncrona
          await mermaid.run({
            nodes: document.querySelectorAll('.mermaid')
          });
        } catch (mermaidError) {
          console.error("Erro ao inicializar diagrama Mermaid:", mermaidError);
        }
      }
      
      // Títulos ganham id navegável (o marked v18 não gera ids) — âncoras dependem disto
      atribuirIdsDeTitulos(contentDiv);

      // Faz scroll do contêiner de exibição de volta para o topo ao carregar o arquivo
      document.querySelector('.dsc-main-content-scroll').scrollTop = 0;

      // Navegação trouxe âncora ("arquivo.md#seção")? Rola até a seção
      rolarParaAncora();

    } catch (err) {
      console.error("Erro ao carregar o arquivo markdown:", err);
      contentDiv.innerHTML = `
        <div class="dsc-empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="color: var(--dsc-color-negative-90)">
            <polygon points="7.86 2 16.14 2 22 7.86 22 16.14 16.14 22 7.86 22 2 16.14 2 7.86 7.86 2"></polygon>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <h2 class="dsc-title-sm dsc-text-negative" style="color: var(--dsc-color-negative-90) !important;">Erro ao abrir arquivo</h2>
          <p class="dsc-body-sm">Não foi possível carregar o arquivo em <strong>${path}</strong>.</p>
          <p class="dsc-caption dsc-text-muted" style="margin-top:12px;">Detalhes: ${err.message}</p>
        </div>
      `;
    }
  }

  // Resolve caminhos relativos de forma simples e limpa preservando navegação
  function resolveRelativePath(currentFile, relPath) {
    if (relPath.startsWith('/')) {
      return relPath.substring(1);
    }
    
    // Documento na raiz (ex.: APROVACOES.md) tem currentDir vazio — ainda assim
    // o href precisa ser normalizado ('./modules/x.md' → 'modules/x.md'),
    // senão o hash não casa com repoFiles e o roteador volta ao Home.
    const slash = currentFile.lastIndexOf('/');
    const currentDir = slash === -1 ? '' : currentFile.substring(0, slash);

    const joinedPath = (currentDir ? currentDir + '/' : '') + relPath;
    const parts = joinedPath.split('/');
    const resolved = [];
    
    for (const part of parts) {
      if (part === '.' || part === '') continue;
      if (part === '..') {
        resolved.pop();
      } else {
        resolved.push(part);
      }
    }
    
    return resolved.join('/');
  }

  // ── Âncoras dentro dos documentos ──────────────────────────────────────────
  // O hash da SPA aceita "caminho.md#seção"; a âncora fica pendente aqui até o
  // documento terminar de renderizar (aí rolamos até o título correspondente).
  let pendingAnchor = '';

  // Slug de título no estilo do GitHub: minúsculas, pontuação removida e CADA
  // espaço vira um hífen, sem colapsar ("A · B" → "a--b") — é assim que os TOCs
  // escritos à mão referenciam as seções (ex.: global/NFR.md).
  function slugDeTitulo(texto) {
    return texto.trim().toLowerCase().replace(/[^\p{L}\p{N} -]/gu, '').replace(/ /g, '-');
  }

  // O marked v18 não gera ids de título (headerIds foi removido) — atribuímos
  // aqui, com sufixo -1, -2… para títulos repetidos, como o GitHub faz.
  function atribuirIdsDeTitulos(container) {
    const usados = new Set();
    container.querySelectorAll('h1, h2, h3, h4, h5, h6').forEach(h => {
      if (h.id) { usados.add(h.id); return; }
      const base = slugDeTitulo(h.textContent) || 'secao';
      let id = base, n = 1;
      while (usados.has(id)) id = base + '-' + (n++);
      usados.add(id);
      h.id = id;
    });
  }

  // Rola a leitura até a âncora pendente: primeiro pelo id exato; se falhar,
  // compara sem acentos — links escritos em ASCII ("#usuario") encontram o
  // título acentuado ("Usuário").
  function rolarParaAncora() {
    if (!pendingAnchor) return;
    let bruto = pendingAnchor;
    pendingAnchor = '';
    try { bruto = decodeURIComponent(bruto); } catch { /* âncora malformada — usa como veio */ }
    const corpo = document.querySelector('.dsc-markdown-body-rendered');
    if (!corpo) return;
    let alvo = corpo.querySelector('#' + CSS.escape(bruto));
    if (!alvo) {
      const semAcento = s => s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
      const procurado = semAcento(bruto);
      alvo = [...corpo.querySelectorAll('[id]')].find(el => semAcento(el.id) === procurado);
    }
    if (alvo) alvo.scrollIntoView();
  }

  // Gerencia cliques nos links internos do Markdown renderizado para permitir navegação SPA fluida
  document.getElementById('markdownContent').addEventListener('click', function(e) {
    const link = e.target.closest('a');
    if (!link) return;

    const href = link.getAttribute('href');
    if (!href) return;

    // Links absolutos (http/https) seguem o comportamento normal do navegador
    if (href.startsWith('http')) return;

    // Âncora da própria página (TOC): vira "arquivo.md#seção" no hash — sem
    // isto o roteador não reconhece o hash e devolve o leitor ao Home
    if (href.startsWith('#')) {
      e.preventDefault();
      globalThis.location.hash = currentFilePath + href;
      return;
    }

    // Link interno .md, com ou sem âncora: navegação SPA
    const pos = href.indexOf('#');
    const doc = pos === -1 ? href : href.substring(0, pos);
    if (doc.toLowerCase().endsWith('.md')) {
      e.preventDefault();
      const targetPath = resolveRelativePath(currentFilePath, doc);
      globalThis.location.hash = targetPath + (pos === -1 ? '' : href.substring(pos));
    }
  });

  // Escuta mudanças de hash e carrega o arquivo correto
  function handleHashRoute() {
    const bruto = globalThis.location.hash.substring(1); // remove o '#' do início
    const pos = bruto.indexOf('#');
    const hash = pos === -1 ? bruto : bruto.substring(0, pos);   // caminho do arquivo
    pendingAnchor = pos === -1 ? '' : bruto.substring(pos + 1);  // âncora de "arquivo.md#seção"
    // Tela especial "Mapa de features" (não é um arquivo do repositório)
    if (hash === '__mapa__') { renderMapa(); return; }
    // Arquivo .md fora do tree.js (ex.: quadro gerado após a última regeneração)
    // ainda navega — o loadFile busca pela rede; erro real vira o card de erro.
    if (hash && (repoFiles.includes(hash) || /\.md$/i.test(hash))) {
      // Mesmo documento já na tela (âncora do TOC, voltar/avançar): só rola
      if (hash === currentFilePath && document.querySelector('.dsc-markdown-body-rendered')) {
        if (pendingAnchor) rolarParaAncora();
        else document.querySelector('.dsc-main-content-scroll').scrollTop = 0;
        return;
      }
      loadFile(hash);

      // Abre todos os details pai daquele arquivo ativo na árvore para destacar onde ele está situado!
      openParentFolders(hash);
    } else if (repoFiles.includes("README.md")) {
      globalThis.location.hash = "README.md";
    } else if (repoFiles.length > 0) {
      globalThis.location.hash = repoFiles[0];
    }
  }

  // Abre recursivamente as pastas pai na listagem do menu para mostrar o arquivo ativo
  function openParentFolders(filePath) {
    const parts = filePath.split('/');
    if (parts.length <= 1) return;
    
    // Vai abrindo cada subnível progressivamente
    let buildingPath = "";
    for (let i = 0; i < parts.length - 1; i++) {
      buildingPath += (buildingPath ? "/" : "") + parts[i];
      const detailsEl = document.querySelector(`.dsc-tree-folder[data-path="${buildingPath}"]`);
      if (detailsEl) {
        detailsEl.setAttribute('open', '');
      }
    }
  }

  // Inicialização Geral da SPA
  globalThis.addEventListener('DOMContentLoaded', () => {
    // Título da aba usa o nome do projeto (config.js); a marca no header é a
    // logo vetorial do Aval (index.html) — a identidade proíbe redigitar "AVAL".
    document.title = `Documentação ${APP_NAME}`;

    // Carrega a listagem de navegação na sidebar
    if (typeof repoFiles !== 'undefined' && Array.isArray(repoFiles)) {
      renderNavigationTree(repoFiles, false);
      handleHashRoute();
    } else {
      document.getElementById('treeNav').innerHTML = `
        <div class="dsc-text-negative" style="padding:12px; font-size:13px;">
          Erro: A variável 'repoFiles' não foi encontrada. Certifique-se de que o arquivo 'tree.js' foi gerado corretamente.
        </div>
      `;
    }
  });

  // Escuta rota de hash no browser para navegação fluida de histórico (Voltar / Avançar)
  globalThis.addEventListener('hashchange', handleHashRoute);

  // O mapa de features escala para a largura útil — re-layout ao redimensionar.
  globalThis.addEventListener('resize', () => { if (document.getElementById('mm-canvas')) mmLayout(); });
