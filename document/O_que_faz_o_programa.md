# 🌱 O Que Faz o Programa - Calculadora de Cana-de-Açúcar

## Visão Geral

A **Calculadora de Cana-de-Açúcar** é um sistema desenvolvido para auxiliar produtores rurais, técnicos agrícolas e agrônomos no planejamento do plantio de cana-de-açúcar, calculando precisamente a quantidade de material vegetal necessário.

## 🎯 Objetivo Principal

Calcular **quantas toneladas de mudas** (material vegetal) são necessárias para plantar uma área específica de cana-de-açúcar, considerando:

- **Área a ser plantada** (em hectares)
- **Variedade de cana** escolhida
- **Espaçamento entre fileiras**
- **Qualidade das mudas** disponíveis

## 🔧 Como Funciona

### 1. Entrada de Dados
O usuário fornece:
- **Área**: Tamanho da propriedade em hectares
- **Variedade**: Escolhe entre 15+ variedades catalogadas (RB, SP, CTC, etc.)
- **Espaçamento**: Distância entre fileiras (1,0m a 1,8m)
- **Fonte das mudas**: Viveiro, canavial próprio ou terceiros

### 2. Processamento
O sistema:
- Consulta banco de dados Oracle com parâmetros técnicos
- Aplica fórmulas agronômicas validadas
- Considera fatores como:
  - Densidade de plantio por metro linear
  - Peso médio dos colmos da variedade
  - Número de gemas viáveis por tonelada
  - Perdas estimadas no processo

### 3. Resultados
Gera relatório completo com:
- **Quantidade total de mudas necessárias** (em toneladas)
- **Número de colmos** requeridos
- **Análise de qualidade** com sistema semáforo
- **Recomendações técnicas** específicas da variedade
- **Custos estimados** (quando aplicável)

## 📊 Exemplo Prático

**Cenário**: Plantar 10 hectares com variedade RB92579, espaçamento 1,4m

**Entrada**:
- Área: 10 ha
- Variedade: RB92579 
- Espaçamento: 1,4m
- Qualidade: Boa (viveiro)

**Resultado**:
- Material necessário: **18,2 toneladas**
- Número de colmos: **1.820 unidades**
- Status: **✅ OK** - Dentro dos padrões recomendados
- Custo estimado: R$ 2.730,00

## 🎯 Benefícios

### Para o Produtor Rural
- **Economia**: Evita desperdício calculando exatamente o necessário
- **Planejamento**: Permite orçamento preciso antes do plantio
- **Qualidade**: Garante densidade adequada para máxima produtividade
- **Facilidade**: Interface simples, sem necessidade de conhecimento técnico avançado

### Para Técnicos e Agrônomos
- **Precisão**: Cálculos baseados em parâmetros científicos validados
- **Agilidade**: Relatórios automáticos em segundos
- **Rastreabilidade**: Histórico completo das recomendações
- **Padronização**: Metodologia uniforme para todos os projetos

## 🌟 Diferenciais do Sistema

1. **Base Científica**: Parâmetros baseados em pesquisas da RIDESA, CTC, IAC e Embrapa
2. **Flexibilidade**: Funciona com 15+ variedades comerciais
3. **Integração**: Conecta com banco Oracle para dados atualizados
4. **Simplicidade**: Interface amigável para usuários não técnicos
5. **Confiabilidade**: Validação automática de dados de entrada

## 📋 Tipos de Relatório

### Relatório Técnico Completo (TXT)
- Detalhes completos do cálculo
- Parâmetros utilizados
- Recomendações específicas da variedade
- Análise de viabilidade econômica

## 🎪 Quando Usar

- **Planejamento de safra**: Dimensionar necessidade de mudas
- **Orçamentos**: Calcular custos de implantação
- **Projetos técnicos**: Elaborar laudos e pareceres
- **Consultoria**: Atender produtores com precisão
- **Estudos acadêmicos**: Pesquisas em agronegócio

---

## 📞 Suporte Técnico

Para dúvidas sobre:
- **Variedades disponíveis**: Consulte `fontes_info.md`
- **Aspectos técnicos**: Veja `documentacao.md`
- **Instalação**: Consulte `README.md` principal

---

*Sistema desenvolvido para FIAP - Faculdade de Informática e Administração Paulista*
*Projeto CAP6 - Fase 2 - 2025*