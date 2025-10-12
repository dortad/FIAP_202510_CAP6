# 📚 DOCUMENTAÇÃO TÉCNICA COMPLETA

## Calculadora de Cana-de-Açúcar v2.0

> **Documentação unificada do sistema de cálculo agronômico para plantio de cana-de-açúcar**
> **Data:** 12/10/2025 | **Status:** Atualizada - Estado Atual do Projeto

---

## 📋 ÍNDICE

1. [Visão Geral do Sistema](#-visão-geral-do-sistema)
2. [Arquitetura do Projeto](#-arquitetura-do-projeto)
3. [Funções Críticas](#-funções-críticas)
4. [Mapeamento Completo de Funções](#-mapeamento-completo-de-funções)
5. [Dependências entre Arquivos](#-dependências-entre-arquivos)
6. [Guia de Desenvolvimento](#-guia-de-desenvolvimento)
7. [Recursos de Documentação](#-recursos-de-documentação)

---

## 🎯 VISÃO GERAL DO SISTEMA

### 📊 Estatísticas Atuais (12/10/2025)

- **Versão**: 2.0 (Simplificada - Somente Relatórios TXT)
- **Total de funções documentadas**: 25+
- **Arquivos principais**: 3 core files
- **Linhas de código**: 1926 total (603+925+398)
- **Cobertura de documentação**: ~95% das funções principais
- **Comentários técnicos**: Detalhados com locais de uso

### 🎭 Funcionalidades Principais

- ✅ Cálculo de material vegetal necessário para plantio
- ✅ Sistema de qualidade com semáforo (OK/ATENÇÃO)
- ✅ Integração Oracle Database + JSON automático
- ✅ Relatórios técnicos completos **SOMENTE EM FORMATO TXT**
- ✅ Interface de menu interativa
- ✅ Validação de dados e sugestões inteligentes

## 🏗️ ARQUITETURA DO PROJETO

### 📄 Estrutura de Arquivos Atual

```
FIAP_202510_CAP6/
├── 📄 calculadora_cana_principal.py    # Programa principal (603 linhas)
├── 📄 funcoes_calculadora.py           # Biblioteca de funções (925 linhas)  
├── 📄 rotinas_V2.py                    # Integração Oracle (398 linhas)
├── 📄 parametros.json                  # Parâmetros técnicos (cultura agricola)
├── 📄 requirements.txt                 # Dependências Python (simplificadas)
├── 📊 Documentação/
│   ├── 📄 documentacao.md              # Esta documentação técnica
│   ├── 📄 INDICE_DOCUMENTACAO.md       # Índice de navegação
│   ├── 📄 README.md                    # Documentação principal
│   └── 📄 fontes_info.md               # Referências das variedades
└── 🔧 Ambiente/
    ├── 📁 venv_Cap6/                   # Ambiente virtual Python
    ├── 📁 __pycache__/                 # Cache Python
    └── 📄 .gitignore                   # Controle de versão
    ├── README.md
    ├── documentacao.md                 # Este arquivo
    └── Calculadora_Cana_resultados.txt # Exemplo de saída
```

### 🔗 Dependências Python - Versão Simplificada v2.0

#### 📦 Dependências Atuais (requirements.txt)

```python
# Dependências PRINCIPAIS (simplificadas)
pandas>=2.2.0          # Manipulação de dados e DataFrames
oracledb>=2.3.0        # Conectividade Oracle Database

# REMOVIDAS na v2.0:
# matplotlib (gráficos)
# openpyxl (Excel)
# xlsxwriter (Excel)
```

#### 🗂️ Dependências por Arquivo

#### calculadora_cana_principal.py

- **Função**: Programa principal, menu e orquestração
- **Imports**: `rotinas_V2.py`, `funcoes_calculadora.py`, `pandas`, `os`
- **Responsabilidades**:
  - Inicialização do sistema com JSON
  - Menu interativo
  - Fluxo principal de execução
  - Tratamento de erros Oracle

#### funcoes_calculadora.py

- **Função**: Biblioteca completa de cálculos e interface
- **Imports**: `pandas`, `unicodedata`, `os`, `datetime`, `typing`
- **Responsabilidades**:
  - Cálculos agronômicos
  - Sistema semáforo de qualidade
  - Geração de relatórios **SOMENTE TXT** (v2.0)
  - Interface do usuário (ask_float, ask_str)
  - Catálogo e glossário

#### rotinas_V2.py

- **Função**: Integração com Oracle Database
- **Imports**: `oracledb`, `pandas`, `json`, `datetime`
- **Responsabilidades**:
  - Conexão Oracle (produção/teste)
  - Sincronização JSON ↔ Oracle
  - Operações CRUD na base de dados

---

## ⭐ FUNÇÕES CRÍTICAS

### 1. **`compute_row()`** - funcoes_calculadora.py linha 219

```python
def compute_row(row: dict, PARAMS: dict, TOL_CHUVA: float, TOL_SECA: float) -> dict:
```

- **🎯 FUNÇÃO PRINCIPAL DE CÁLCULO**
- **Processo**: Executa todos os cálculos agronômicos para uma linha de plantio
- **Entrada**: Dados do usuário (área, variedade, época, processo, perdas)
- **Saída**: Resultados completos com status de qualidade
- **Fórmulas**:
  - `metros_fileira/ha = 10.000 ÷ espaçamento`
  - `toletes/metro = gemas_finais ÷ gemas_úteis`
  - `massa/ha = toletes/ha × comprimento × densidade ÷ 1000`
  - `status = "OK" se desvio ≤ tolerância, senão "ATENÇÃO"`
- **Usado em**: `main()` para processar cada linha de dados

### 2. **`gerar_txt()`** - funcoes_calculadora.py linha 620

```python
def gerar_txt(df: pd.DataFrame, resumo: dict, saida_txt: str):
```

- **📄 GERAÇÃO DE RELATÓRIOS COMPLETOS**
- **Processo**: Cria relatório TXT com 40+ seções explicativas
- **Conteúdo**:
  - Cabeçalho com timestamp
  - Resumo executivo
  - Produtividade por linha
  - Dados técnicos detalhados
  - Explicação do sistema semáforo
  - Glossário de termos
- **Usado em**: `main()` linha 495 para relatório final

### 3. **`main()`** - calculadora_cana_principal.py linha 327

```python
def main():
```

- **🎮 ORQUESTRAÇÃO DO SISTEMA**
- **Fluxo completo**:
  1. Inicialização (carregamento Oracle/JSON)
  2. Menu interativo (catálogo, glossário, sync)
  3. Loop de entrada de dados
  4. Processamento (compute_row para cada linha)
  5. Geração de relatórios
- **Tratamento**: Erros, validações, sugestões
- **Usado em**: Bloco `__main__` como ponto de entrada

### 4. **`load_params_from_oracle_v2()`** - calculadora_cana_principal.py linha 44

```python
def load_params_from_oracle_v2(tipo_conexao: str, params_sql: str, tol_chuva: float, tol_seca: float):
```

- **🚀 INICIALIZAÇÃO DO SISTEMA**
- **Processo**:
  1. Conecta ao Oracle via `rotinas_V2.conectar_oracle()`
  2. Verifica se tabela tem dados
  3. Se vazia: carrega do JSON automaticamente
  4. Executa SQL para buscar parâmetros
  5. Normaliza e mapeia dados
- **Retorno**: (PARAMS, MAP_DISPLAY, tolerâncias)
- **Usado em**: `main()` linha 273 para inicialização única

### 5. **`conectar_oracle()`** - rotinas_V2.py linha 152

```python
def conectar_oracle(tipo: str = 'producao'):
```

- **🔌 CONEXÃO ORACLE**
- **Ambientes**:
  - **Produção**: oracle.fiap.com.br:1521/ORCL
  - **Teste**: Configurações de desenvolvimento
- **Usado em**: Todas as operações que requerem acesso ao banco

---

## 🗺️ MAPEAMENTO COMPLETO DE FUNÇÕES

### 🔧 FUNÇÕES UTILITÁRIAS (funcoes_calculadora.py)

#### `clear_screen()` - Linha 14

- **Função**: Limpa tela do terminal (Windows/Linux compatível)
- **Usado em**:
  - `calculadora_cana_principal.py`: `menu_inicial()` linha 210
  - `calculadora_cana_principal.py`: `main()` linha 268

#### `strip_accents(text: str)` - Linha 32

- **Função**: Remove acentos usando normalização Unicode NFD
- **Processo**: Separa caracteres base de diacríticos
- **Usado em**:
  - `norm_key()` - Para normalização de chaves
  - Comparação case-insensitive de variedades

#### `norm_key(s: str)` - Linha 58

- **Função**: Normaliza string para chave única
- **Processo**: Remove acentos + espaços + hífens + maiúsculas
- **Usado em**:
  - `compute_row()` - Busca de parâmetros
  - Mapeamento Variedade|Época|Processo

#### `to_float_or_none(x)` - Linha 87

- **Função**: Conversão segura para float
- **Tratamento**: None, strings vazias, vírgulas brasileiras
- **Usado em**:
  - `compute_row()` - Conversão de áreas e percentuais
  - Validação de entrada do usuário

### 🧮 FUNÇÕES DE CÁLCULO (funcoes_calculadora.py)

#### `compute_row()` - Linha 219 ⭐

- **Ver seção "Funções Críticas"**

### 🎮 FUNÇÕES DE INTERFACE (funcoes_calculadora.py)

#### `ask_float()` - Linha 756

- **Função**: Entrada validada de números decimais
- **Recursos**: Default, min/max, comandos especiais (:help, :cat)
- **Usado em**: Coleta de área, percentuais de perdas

#### `ask_str()` - Linha 807

- **Função**: Entrada validada de strings
- **Recursos**: Choices, default, comandos especiais
- **Usado em**: Coleta de variedade, época, processo

#### `show_catalog()` - Linha 356

- **Função**: Exibe catálogo paginado de combinações
- **Recursos**: Paginação, filtros, busca por variedade
- **Usado em**: `menu_inicial()` opção 1

#### `print_glossary()` - Linha 297

- **Função**: Exibe glossário de termos técnicos
- **Conteúdo**: Definições de E, Gf, s, g, L, rho, d
- **Usado em**: `menu_inicial()` opção 2, comandos :help+

### 📊 FUNÇÕES DE RELATÓRIO (funcoes_calculadora.py)

#### `gerar_txt()` - Linha 620 ⭐

- **Ver seção "Funções Críticas"**

#### `build_catalog_from_params()` - Linha 286

- **Função**: Constrói catálogo a partir dos parâmetros
- **Usado em**: `show_catalog()` para exibição

### 🔗 FUNÇÕES ORACLE (rotinas_V2.py)

#### `conectar_oracle()` - Linha 152 ⭐

- **Ver seção "Funções Críticas"**

#### `desconectar_oracle(conn)` - Linha 204

- **Função**: Desconecta do Oracle de forma segura
- **Usado em**: Todas as funções após uso da conexão

#### `carregar_parametros_Json_como_dicionario()` - Linha 217

- **Função**: Carrega JSON com sincronização
- **Arquivo**: parametros.json (338 registros)
- **Usado em**: `load_params_from_oracle_v2()` quando Oracle vazio

#### `carregar_parametros_no_oracle()` - Linha 367

- **Função**: Insere/atualiza dados JSON no Oracle
- **Usado em**: Sincronização automática e manual

### 📋 FUNÇÕES PRINCIPAIS (calculadora_cana_principal.py)

#### `main()` - Linha 327 ⭐

- **Ver seção "Funções Críticas"**

#### `load_params_from_oracle_v2()` - Linha 44 ⭐

- **Ver seção "Funções Críticas"**

#### `menu_inicial()` - Linha 264

- **Função**: Menu interativo principal
- **Opções**:
  1. Ver catálogo de combinações
  2. Ver glossário de parâmetros
  3. Sobre o programa
  4. Sincronizar JSON → Oracle
  5. Iniciar cálculos
  6. Sair
- **Usado em**: `main()` linha 307

#### `sincronizar_json_oracle()` - Linha 198

- **Função**: Sincronização manual JSON → Oracle
- **Processo**: Conecta + carrega JSON + insere Oracle + commit
- **Usado em**: `menu_inicial()` opção 4

---

## 🔄 DEPENDÊNCIAS ENTRE ARQUIVOS

```
main() [calculadora_cana_principal.py]
├── load_params_from_oracle_v2()
│   ├── conectar_oracle() [rotinas_V2.py]
│   ├── carregar_parametros_Json_como_dicionario() [rotinas_V2.py]  
│   └── carregar_parametros_no_oracle() [rotinas_V2.py]
├── menu_inicial()
│   ├── show_catalog() [funcoes_calculadora.py]
│   ├── print_glossary() [funcoes_calculadora.py]
│   └── sincronizar_json_oracle()
├── ask_float() / ask_str() [funcoes_calculadora.py]
├── compute_row() [funcoes_calculadora.py]
│   ├── norm_key() [funcoes_calculadora.py]
│   └── to_float_or_none() [funcoes_calculadora.py]
└── gerar_txt() [funcoes_calculadora.py]
```

### 📊 Matriz de Dependências

| Arquivo                           | Depende de                            | Usado por                     |
| --------------------------------- | ------------------------------------- | ----------------------------- |
| `calculadora_cana_principal.py` | rotinas_V2.py, funcoes_calculadora.py | __main__                |
| `funcoes_calculadora.py`        | pandas, unicodedata, os, datetime     | calculadora_cana_principal.py |
| `rotinas_V2.py`                 | oracledb, pandas, json, datetime      | calculadora_cana_principal.py |

---

## 🛠️ GUIA DE DESENVOLVIMENTO

### 📝 Formato dos Comentários

Todas as funções seguem o padrão:

```python
def nome_funcao():
    """
    *** CATEGORIA DA FUNÇÃO ***
    Descrição concisa da função.
  
    Explicação detalhada do processo:
    1. Passo 1
    2. Passo 2
    3. Passo N
  
    Args:
        param1 (tipo): Descrição
        param2 (tipo): Descrição
    
    Returns:
        tipo: Descrição do retorno
    
    Usado em:
        - arquivo.py: funcao() - linha X
        - Contexto específico de uso
    
    Informações adicionais relevantes.
    """
```

### 🎯 Benefícios da Documentação

#### ✅ Para Desenvolvedores

- **Entendimento rápido** do código
- **Localização fácil** de dependências
- **Manutenção simplificada**
- **Onboarding eficiente**

#### ✅ Para Usuários

- **Compreensão do fluxo** do programa
- **Identificação de pontos** de entrada
- **Rastreamento de funcionalidades**

#### ✅ Para Manutenção

- **Impacto de mudanças** mapeado
- **Testes direcionados**
- **Refatoração segura**
- **Debug facilitado**

### 🔄 Próximos Passos Recomendados

1. **Manter sincronizado**: Atualizar documentação com mudanças
2. **Expandir testes**: Criar testes unitários para funções críticas
3. **Adicionar diagramas**: Fluxogramas para processos complexos
4. **Melhorar logging**: Sistema de logs para debug avançado
5. **Otimizar performance**: Profile das funções de cálculo

---

## 📈 RESUMO FINAL

### ✅ Status da Documentação

- **Cobertura**: ~90% das funções principais
- **Qualidade**: Comentários detalhados com exemplos
- **Mapeamento**: Dependências completas entre arquivos
- **Usabilidade**: Guia para desenvolvedores e usuários

### 🎯 Funções Mais Importantes

1. **`compute_row()`**: Núcleo dos cálculos agronômicos
2. **`gerar_txt()`**: Relatórios completos e educativos
3. **`main()`**: Orquestração de todo o sistema
4. **`load_params_from_oracle_v2()`**: Inicialização robusta
5. **`conectar_oracle()`**: Conectividade confiável

### 🔗 Arquitetura Robusta

- **Separação de responsabilidades**: Cada arquivo tem função específica
- **Interface amigável**: Validações e sugestões automáticas
- **Relatórios educativos**: Explicações técnicas detalhadas

---

## 📖 RECURSOS DE DOCUMENTAÇÃO

### 📚 Arquivos de Documentação Disponíveis

#### `README.md` - Documentação Principal

- **Propósito**: Visão geral do projeto e guia de uso
- **Conteúdo**:
  - Instalação e configuração
  - Como executar o programa
  - Exemplos de uso
  - Estrutura do projeto
- **Público**: Usuários finais e desenvolvedores iniciantes

#### `documentacao.md` - Esta Documentação Técnica

- **Propósito**: Documentação técnica completa do sistema
- **Conteúdo**:
  - Arquitetura detalhada
  - Mapeamento completo de funções
  - Dependências entre arquivos
  - Guia para desenvolvedores
- **Público**: Desenvolvedores e mantenedores do código

#### `INDICE_DOCUMENTACAO.md` - Índice de Navegação

- **Propósito**: Navegação rápida entre documentos
- **Conteúdo**:
  - Links para todos os arquivos de documentação
  - Descrição de cada documento
  - Guia de qual documento consultar
- **Público**: Todos os usuários do projeto

#### `fontes_info.md` - Referências das Variedades

- **Propósito**: Catálogo de fontes científicas e técnicas
- **Conteúdo**:
  - Referências para cada variedade de cana
  - Links para documentação oficial (RIDESA, CTC, IAC, Embrapa)
  - PDFs técnicos e bulas de variedades
- **Público**: Pesquisadores e técnicos agrícolas

### 🔗 Sistema de Navegação

```
README.md ←→ INDICE_DOCUMENTACAO.md ←→ documentacao.md
    ↓              ↓                        ↓
Uso Geral    Navegação Rápida      Detalhes Técnicos
    ↓              ↓                        ↓
fontes_info.md ←→ Referências Científicas
```

### 📊 Estatísticas da Documentação

- **Total de arquivos**: 4 documentos principais
- **Páginas totais**: ~15 páginas equivalentes
- **Cobertura**: 95% do código documentado
- **Linguagens**: Português (PT-BR)
- **Formato**: Markdown (.md) padrão GitHub

### 🎯 Como Navegar na Documentação

1. **Primeira vez no projeto?** → Comece pelo `README.md`
2. **Precisa de referência rápida?** → Use `INDICE_DOCUMENTACAO.md`
3. **Vai desenvolver/manter código?** → Consulte `documentacao.md`
4. **Busca fontes científicas?** → Veja `fontes_info.md`

---

**📚 Esta documentação serve como guia completo para entender, manter e expandir o sistema de Calculadora de Cana-de-Açúcar!**

*Última atualização: 12/10/2025 | Versão: 2.0 | Status: Documentação Atualizada com Estado Atual* ✅
