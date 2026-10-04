# `_biblioteca-ds/` — biblioteca de componentes para protótipos

> ⚠️ **Exclusiva de protótipos.** As classes `.dsc-*` existem para tornar protótipos navegáveis — **nunca** aparecem no código de produção (lá entram os componentes reais do design system; ver o mapa de equivalência no README do tema do projeto). Recomenda-se regra de lint na CI do front proibindo `dsc-` em templates — a presença denuncia cópia de protótipo.

HTML/CSS **sem build e sem dependências** para os protótipos do docqui (classes `.dsc-*`, espelhando os componentes do Figma **CAIXA DS**). É consumida pelos prompts de protótipo (`6A`/`6B` FULL e `6C`/`6D` componente) e pela skill `/prototype` — todo protótipo gerado linka o `ds.css` daqui.

> ℹ️ **Template do kit.** Assim como o `global/DESIGN-SYSTEM.md` (a fonte desta implementação), esta biblioteca vem preenchida com o CAIXA DS como referência. Para outro produto, troque os valores de [`tokens.css`](tokens.css) pelos tokens do seu design system — os componentes em `ds.css` são token-driven e se adaptam. Confira os valores com o Figma da sua instância.

| Arquivo | O que é |
|---|---|
| [`ds.css`](ds.css) | Componentes `.dsc-*` (importa `tokens.css`) — **o link dos protótipos** |
| [`tokens.css`](tokens.css) | Tokens `--dsc-*`: cores, tipografia, espaçamento, raios, sombras |
| [`tema-gpe.css`](tema-gpe.css) | Camada de tema do GPE, linkada depois do `ds.css` — ver *Tema do GPE*, abaixo |
| [`index.html`](index.html) | **Catálogo navegável** — todos os componentes com markup de exemplo |
| [`shell-responsive.html`](shell-responsive.html) | Demo do shell (header + drawer + grid) nos breakpoints |

## Como linkar

O caminho relativo depende da profundidade do protótipo dentro de `prototypes/`:

```html
<!-- prototypes/[dominio]/[feature-set]/flow.html -->
<link rel="stylesheet" href="../../_biblioteca-ds/ds.css">

<!-- prototypes/[dominio]/[feature-set]/[feature]/form.html -->
<link rel="stylesheet" href="../../../_biblioteca-ds/ds.css">
```

## O shell (protótipos FULL)

Estrutura canônica — sidebar **oculta por padrão**, aberta como drawer pelo ☰ (classe `is-menu-open` no `.dsc-app`); o backdrop fecha ao clicar fora:

```html
<div class="dsc-app">
  <aside class="dsc-sidebar">
    <div class="dsc-sidebar-backdrop" onclick="dscToggleMenu()"></div>
    <div class="dsc-sidebar-brand"><span class="dsc-brand-mark">S</span> Sistema</div>
    <ul class="dsc-menu">
      <li class="dsc-menu-section">Seção</li>
      <li><a class="dsc-menu-item is-active" href="#">Item</a></li>
    </ul>
  </aside>
  <div class="dsc-shell-main">
    <header class="dsc-header">…</header>
    <main class="dsc-main">…</main>
  </div>
</div>
<script>
  function dscToggleMenu() {
    document.querySelector('.dsc-app').classList.toggle('is-menu-open');
  }
</script>
```

**Protótipo sem shell** (Storybook, iframe, doc técnica — prompts `6C`/`6D`): troque o bloco `.dsc-app` por `<main class="dsc-component-only">…</main>`.

**Tema escuro**: adicione a classe `app-dark` ao `<html>` ou `<body>`.

## Catálogo de classes

O markup de exemplo de cada componente está no [`index.html`](index.html) — **não invente variações**: se algo não está aqui, não existe na biblioteca.

| Grupo | Classes |
|---|---|
| Shell | `dsc-app` `is-menu-open` · `dsc-sidebar` `dsc-sidebar-backdrop` `dsc-sidebar-brand` `dsc-brand-mark` · `dsc-menu` `dsc-menu-section` `dsc-menu-item` `is-active` · `dsc-shell-main` · `dsc-header` `dsc-header-start` `dsc-header-actions` `dsc-header-logo` `dsc-header-item` `dsc-menu-toggle` · `dsc-hi-body` `dsc-hi-title` `dsc-hi-sub` `dsc-hi-caret` · `dsc-main` `is-narrow` · `dsc-page-header` `dsc-page-title` `dsc-page-subtitle` · `dsc-breadcrumb` `is-current` `dsc-sep` · `dsc-component-only` |
| Grid / utilitários | `dsc-row` `dsc-col-{1..12}` · `dsc-grid-{2,3,4}` `dsc-gap-{1,2,3}` · `dsc-flex` `dsc-items-center` `dsc-justify-between` · `dsc-divider` |
| Tipografia | `dsc-display` `dsc-title` `dsc-title-sm` `dsc-body` `dsc-body-sm` `dsc-caption` · `dsc-text-muted` `dsc-text-primary` · `dsc-req` |
| Card | `dsc-card` `dsc-card-title` |
| Botões | `dsc-btn` (+ `--outline` `--chromeless` `--danger` `--on-media` `--sm` `--icon` · `is-loading` `disabled`) · `dsc-segmented` · `dsc-icon-action` |
| Formulários | `dsc-field` (+ `is-invalid`) `dsc-field-label` `dsc-field-hint` `dsc-field-error` `dsc-field-action` · `dsc-input` `dsc-textarea` `dsc-select` `dsc-input-icon` `dsc-search` · `dsc-check` `dsc-radio` `dsc-switch` (+ `is-on`) `dsc-slider` `dsc-stepper` · `dsc-money` `dsc-pin` `dsc-input-chips` `dsc-account-select` `dsc-calendar` |
| Tabela | `dsc-table-wrap` `dsc-table` (+ `--dense`) · `dsc-table-toolbar` `dsc-table-footer` `dsc-table-empty` · `dsc-col-check` `dsc-col-actions` · `dsc-sortable` (+ `is-sorted`) `dsc-num` `dsc-cell-editable` · `tr.is-selected` · `dsc-lv` `dsc-lv-label` `dsc-lv-value` |
| Modal | `dsc-modal-mask` `dsc-modal` `dsc-modal-header` `dsc-modal-close` `dsc-modal-body` `dsc-modal-footer` |
| Feedback | `dsc-toast` (+ `--positive` `--danger` `--warning`) · `dsc-alert` (+ `--success` `--warning` `--danger`, `dsc-alert-cta`) · `dsc-tag` (+ `--highlight` `--neutral` `--success` `--warning` `--danger` `--sm` `--lg`) · `dsc-badge` (+ `--dot`) · `dsc-chip` · `dsc-avatar` (+ `--sm`) |
| Estados de tela | `dsc-skeleton` · `dsc-state` `dsc-state-icon` `dsc-state-title` `dsc-state-text` · `dsc-spinner` · `dsc-progress` |
| Protótipo | `dsc-proto-badge` · `dsc-proto-notes` · `dsc-screen` (+ `is-active`) |

## Fonte

A **CAIXA Std** é proprietária e **não** vem embutida — sem `@font-face` ou instalação local, o navegador usa o fallback (`Segoe UI`/Roboto/system-ui). Para fidelidade total, embuta os arquivos da fonte e declare o `@font-face` apontando para `--dsc-font-family-1`.

## Tema do GPE (`tema-gpe.css`)

Nesta instância os protótipos recuperam as telas como são no código-fonte da aplicação (Angular 18 + PrimeNG 18), e não o visual do CAIXA DS do kit. A camada [`tema-gpe.css`](tema-gpe.css) é linkada **depois** do `ds.css` e faz duas coisas: troca os tokens `--dsc-*` pelos valores aferidos nas capturas de tela dos documentos legados GPE001 a GPE006 (azul PrimeNG, cantos de 6px, fundo cinza) e acrescenta, com o prefixo `.gpe-*`, os componentes que o GPE tem e a biblioteca não.

```html
<!-- prototypes/[dominio]/[feature-set]/flow.html -->
<link rel="stylesheet" href="../../_biblioteca-ds/ds.css">
<link rel="stylesheet" href="../../_biblioteca-ds/tema-gpe.css">
```

| Grupo | Classes `.gpe-*` |
|---|---|
| Shell | O `.dsc-header` vira a barra azul com o título "Gestão de Participantes em Eventos"; não há `.dsc-sidebar` nem ☰ — o menu é horizontal: `gpe-menubar` `gpe-menu-item` (+ `is-open`) `gpe-menu-link` (+ `is-active`) `gpe-caret` `gpe-submenu` · menu do usuário `gpe-user-menu` (+ `is-open`) `gpe-user-dropdown` `gpe-ud-info` `gpe-ud-sep` |
| Botões | `gpe-btn--secondary` `gpe-btn--success` `gpe-btn--help` `gpe-btn--warn` `gpe-btn--indigo` `gpe-btn--block` `gpe-btn--upper` · ações de linha `gpe-icon-solid` (+ `--primary` `--danger`) e `gpe-icon-round` com as cores `gpe-c-blue` `gpe-c-orange` `gpe-c-yellow` `gpe-c-dark` `gpe-c-red` `gpe-c-green` `gpe-c-teal` |
| Formulários | `gpe-label-strong` `gpe-radio-group` `gpe-inline-check` `gpe-form-actions` (+ `--end`) `gpe-form-footer` `gpe-counter` (+ `is-warn` `is-limit`) `gpe-readonly-line` · envio de arquivo `gpe-upload` `gpe-upload-bar` `gpe-upload-drop` `gpe-upload-file` · abas `gpe-tabs` `gpe-tab` `gpe-tab-panel` (+ `is-active`) · lista com caixas `gpe-listbox` |
| Tabela | `gpe-table-caption` `gpe-left` `gpe-row-actions` `gpe-subtext` · paginador `gpe-paginator` `gpe-page-report` · ícones de status `gpe-status` (+ `--sim` `--nao` `--pendente` `is-clickable`) · `gpe-link` |
| Quadros e tags | `gpe-box` `gpe-box-head` `gpe-box-item` · `gpe-person-head` `gpe-initials` · `gpe-tag-check` `gpe-tag-finalizado` `gpe-swatch` (+ `--lg`) `gpe-color-bar` |
| Diálogos e mensagens | `gpe-modal--sm` `gpe-modal--lg` `gpe-confirm-body` · `gpe-toast-stack` (o `.dsc-toast` vira o p-toast: fundo claro, barra lateral da severidade, resumo e detalhe) |
| Evento e mapa de assentos | `gpe-event-header` `gpe-event-title` `gpe-event-type` `gpe-event-meta` `gpe-autorefresh` `gpe-view-switch` · `gpe-map-layout` `gpe-panel` `gpe-panel-soft` `gpe-panel-title` `gpe-person-card` `gpe-queue-card` `gpe-queue-photo` `gpe-queue-seat` (+ `--ok` `--none`) `gpe-zoom` `gpe-map` `gpe-map-grid` `gpe-sector` (+ `--f` `--col` `--row`) `gpe-seat` (+ `is-occupied` `is-checked` `is-found` `is-drop`) `gpe-seat-remove` `gpe-map-legend` `gpe-export-row` |
| Legendas | `gpe-block-card` `gpe-block-num` `gpe-block-body` `gpe-block-head` `gpe-cond-row` `gpe-palette` `gpe-sim-group` |
| Acesso | `gpe-login` `gpe-login-form` `gpe-login-art` `gpe-brand-cni` |
| Protótipo | `gpe-proto-perfil` — seletor de perfil simulado no painel de notas |

As `.gpe-*` seguem a mesma regra das `.dsc-*`: existem só para protótipo e nunca aparecem em código de produção. O `global/DESIGN-SYSTEM.md` desta instância ainda é o exemplo CAIXA do kit; enquanto não for substituído pela identidade da CNI, a referência visual dos protótipos é esta camada.
