<!-- docqui: 4.0.2 | prompt: PROMPT_CONTAGEM | atualizado: 2026-10-04 -->
# ALI-AIE-MAP.md
> **Registro canônico** dos Arquivos Lógicos Internos (ALI) e Arquivos de Interface
> Externa (AIE) do sistema e das **entidades** que os constituem.
> Fonte de verdade para a **validade** de um ALI/AIE na contagem APF.
>
> O **dimensionamento** (RLR/DER/complexidade/PF) vive em
> `global/DATA-MODEL.md → ## Arquivos Lógicos (APF)`. Aqui fica o mapeamento
> ALI/AIE ↔ entidade e o status de cada um.

---

## Como usar

- Todo **ALR** (Arquivo Lógico Referenciado = IFPUG FTR) contado numa função de transação deve
  corresponder a um ALI ou AIE listado aqui.
- **Ao contar um ALR ainda não mapeado**, registre-o nesta tabela com as **entidades
  em branco** e status `pendente`. Isso marca que é um ALI/AIE **válido**; o
  detalhamento (entidades, domínio, sizing) é preenchido conforme o projeto evolui.
- **Arquivos de importação/transmissão** (XML, CSV, etc.) **não** são classificados
  como AIE por padrão — são dados processados por uma EE. Contá-los como AIE fica a
  **critério do Analista de Métricas**; se decidir contar, registre aqui.

---

## ALIs / AIEs registrados

| Nome | Tipo | Domínio | Entidades constituintes | Status |
|---|---|---|---|---|
| Evento | ALI | Eventos | Evento, CadeiraMesa, EventoPessoa, EventoLegenda, EventoLegendaCondicao, EventoPessoaLegenda | mapeado |
| Legenda | ALI | Eventos | Legenda | mapeado |
| PresetLegenda | ALI | Eventos | PresetLegenda | mapeado |
| Pessoa | ALI | Pessoas | (em branco) | pendente |

> **Pessoa está pendente.** Entrou aqui porque as transações de Eventos contadas em 2026-10-04 a leem; o domínio Pessoas ainda não foi dimensionado. Aquela contagem tratou Pessoa, GrupoTrabalhoPessoa e TemaPessoa como um arquivo lógico só 🔍 — os grupos de trabalho e os temas só existem ligados à pessoa. Se a contagem de Pessoas concluir diferente, o ALR das transações de Eventos que leem esses dados precisa ser revisto.


---

## Links
[DATA-MODEL.md](./DATA-MODEL.md) · [SIZING.md](./SIZING.md) · [INDEX geral](../modules/INDEX.md)
