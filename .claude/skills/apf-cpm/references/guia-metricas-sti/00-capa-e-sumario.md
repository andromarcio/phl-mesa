# Guia de Métricas da STI — Versão 1.3 · Capa e Sumário

> Guia de Métricas da STI · Versão 1.3 (Dez/2025)

**Guia de Métricas da Superintendência de Tecnologia da Informação – STI**

**Versão 1.3**

Brasília/DF – Dezembro de 2025

---

## Sumário

- 1. Introdução — 4
- 2. Objetivo — 6
- 3. Contagem de Pontos de Função: — 7
  - 3.1. Determinar propósito, tipo e escopo da contagem e fronteira da aplicação — 8
  - 3.2. Identificação de processo elementar — 8
  - 3.3. Identificar Funções de Dados e Funções Transacionais — 9
    - 3.3.1. Funções do tipo dado: — 9
    - 3.3.2. Funções do tipo transação: — 10
    - 3.3.3. Contribuição dos tipos funcionais: — 10
  - 3.4. Calcular tamanho funcional — 11
  - 3.5. Requisitos não funcionais — 12
- 4. Cálculo de pontos de função — 14
  - 4.1. Iniciativa de desenvolvimento — 14
  - 4.2. Iniciativa de melhoria — 14
    - 4.2.1. Observações sobre alterações: — 16
    - 4.2.2. Outros tipos de funções alteradas: — 17
  - 4.3. Iniciativa de migração de dados – PF_CONVERSÃO — 18
  - 4.4. Manutenção corretiva — 18
  - 4.5. Mudança de plataforma — 20
    - 4.5.1. Mudança de plataforma – Linguagem de programação: — 20
    - 4.5.2. Mudança de plataforma – Banco de dados: — 22
  - 4.6. Atualização de versão — 23
    - 4.6.1. Atualização de versão – Linguagem de programação: — 24
    - 4.6.2. Atualização de versão – Browser: — 24
    - 4.6.3. Atualização de versão – Banco de dados: — 25
  - 4.7. Manutenção em interface — 25
  - 4.8. Adaptação em funcionalidades sem alteração de requisitos funcionais — 26
  - 4.9. Apuração especial — 27
    - 4.9.1. Apuração especial – Base de dados: — 28
    - 4.9.2. Apuração especial – Geração de relatórios: — 29
    - 4.9.3. Apuração especial – Reexecução: — 30
  - 4.10. Atualização de dados — 31
  - 4.11. Desenvolvimento, manutenção e publicação de páginas estáticas de intranet, internet ou portal — 32
  - 4.12. Verificação de erros — 32
  - 4.13. Pontos de função de teste — 33
  - 4.14. Componente interno reusável — 34
  - 4.15. Dados de Código (*code tables*) — 35
- 5. Orientações complementares para contagem — 36
  - 5.1. Contagem de pontos de função com múltiplas mídias — 36
    - 5.1.1. Cenário 1 - Mesmos dados apresentados em tela e impressos: — 38
    - 5.1.2. Cenário 2 - Mesmos dados de saída como dados em arquivo e relatório impresso: — 38
    - 5.1.3. Cenário 3 - Mesmos dados de entrada batch e on-line: — 39
    - 5.1.4. Cenário 4 - Múltiplos canais de entrega da mesma funcionalidade: — 39
    - 5.1.5. Cenário 5 - Relatório em múltiplos formatos: — 39
  - 5.2. Log, trilha de auditoria e histórico — 40
    - 5.2.1. Log: — 40
    - 5.2.2. Trilha de auditoria: — 40
    - 5.2.3. Histórico: — 41
  - 5.3. Arquivos para processamento — 41
  - 5.4. API/Webservices — 43
  - 5.5. Principais falhas da contagem identificadas — 46
- 6. Regras auxiliares — 46
  - 6.1. Contagem estimativa de pontos de função (CEPF) — 46
  - 6.2. Distribuição de esforço por fase da iniciativa — 52
    - 6.2.1. Evidências de entrega: — 52
    - 6.2.2. Estratégias de desenvolvimento de *back* e *frontend* em separado: — 53
  - 6.3. Fator de ajuste — 53
- 7. Referências bibliográficas — 54
- 8. Controle de versão — 56
