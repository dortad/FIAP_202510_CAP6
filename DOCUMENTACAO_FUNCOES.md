# DOCUMENTAÇÃO COMPLETA - MAPEAMENTO DE FUNÇÕES
# Calculadora de Cana-de-Açúcar v1.1
# Data: 12/10/2025

## VISÃO GERAL DOS ARQUIVOS

### 📄 calculadora_cana_principal_v1.1.py (PROGRAMA PRINCIPAL)
- **Função**: Programa principal com menu e fluxo de execução
- **Linhas**: 512 total
- **Dependências**: rotinas_V2.py, funcoes_calculadora.py

### 📄 funcoes_calculadora.py (BIBLIOTECA DE FUNÇÕES)  
- **Função**: Biblioteca com todas as funções de cálculo, interface e relatórios
- **Linhas**: 920+ total
- **Dependências**: pandas, unicodedata, os, datetime

### 📄 rotinas_V2.py (INTEGRAÇÃO ORACLE)
- **Função**: Funções para conexão e manipulação de dados Oracle
- **Linhas**: 400+ total  
- **Dependências**: oracledb, pandas, json, datetime

---

## MAPEAMENTO DETALHADO DE FUNÇÕES

### 🔧 FUNÇÕES UTILITÁRIAS (funcoes_calculadora.py)

#### `clear_screen()` - Linha 14
```python
def clear_screen():
```
**Função**: Limpa tela do terminal (Windows/Linux compatível)
**Usado em**:
- calculadora_cana_principal_v1.1.py: menu_inicial() linha 210
- calculadora_cana_principal_v1.1.py: main() linha 268

#### `strip_accents(text: str)` - Linha 32
```python  
def strip_accents(text: str) -> str:
```
**Função**: Remove acentos usando normalização Unicode NFD
**Usado em**:
- norm_key() - Para normalização de chaves
- Comparação case-insensitive de variedades

#### `norm_key(s: str)` - Linha 58
```python
def norm_key(s: str) -> str:
```
**Função**: Normaliza string para chave única (remove acentos, espaços, hífens)
**Usado em**:
- compute_row() - Busca de parâmetros técnicos
- calculadora_cana_principal_v1.1.py - Verificação de combinações
- Mapeamento Variedade|Epoca|Processo -> Parâmetros

#### `to_float_or_none(x)` - Linha 87
```python
def to_float_or_none(x):
```
**Função**: Conversão segura para float (trata vírgulas brasileiras)
**Usado em**:
- compute_row() - Conversão de áreas e percentuais
- Validação de entrada do usuário
- Processamento dados Oracle/JSON

---

### 🧮 FUNÇÕES DE CÁLCULO (funcoes_calculadora.py)

#### `compute_row(row, PARAMS, TOL_CHUVA, TOL_SECA)` - Linha 219
```python
def compute_row(row: dict, PARAMS: dict, TOL_CHUVA: float, TOL_SECA: float) -> dict:
```
**Função**: *** FUNÇÃO PRINCIPAL DE CÁLCULO ***
- Calcula densidade de plantio (toletes/hectare)
- Calcula massa de material vegetal
- Determina área efetiva (descontando perdas)  
- Calcula desvio da recomendação
- Define status semáforo (OK/ATENÇÃO)

**Usado em**:
- calculadora_cana_principal_v1.1.py: main() linha 406

**Fórmulas implementadas**:
- metros_fileira/ha = 10.000 / espaçamento
- toletes/metro = gemas_finais / gemas_úteis  
- massa/ha = toletes/ha × comprimento × densidade ÷ 1000
- desvio = |massa_calculada - massa_recomendada| / massa_recomendada
- status = "OK" se desvio ≤ tolerância, senão "ATENÇÃO"

---

### 📊 FUNÇÕES DE INTERFACE E CATÁLOGO (funcoes_calculadora.py)

#### `build_catalog_from_params(PARAMS)` - Linha 320
```python
def build_catalog_from_params(PARAMS: Dict[str, dict]) -> Dict[str, dict]:
```
**Função**: Constrói catálogo de variedades a partir dos parâmetros
**Usado em**:
- Funções de exibição de catálogo

#### `print_glossary()` - Linha 332
```python  
def print_glossary():
```
**Função**: Imprime glossário completo de termos técnicos
**Usado em**:
- calculadora_cana_principal_v1.1.py: menu_inicial() opção 2

#### `show_catalog(MAP_DISPLAY, PARAMS, page_size, filter_var)` - Linha 399
```python
def show_catalog(MAP_DISPLAY: dict, PARAMS: dict = None, page_size: int = 20, filter_var: str = None):
```
**Função**: Exibe catálogo paginado de combinações disponíveis
**Usado em**:
- calculadora_cana_principal_v1.1.py: menu_inicial() opção 1

#### `mostrar_sobre_programa()` - Linha 480
```python
def mostrar_sobre_programa():
```
**Função**: Exibe informações detalhadas sobre o programa
**Usado em**:
- calculadora_cana_principal_v1.1.py: menu_inicial() opção 3

---

### 📄 FUNÇÃO DE RELATÓRIOS (funcoes_calculadora.py)

#### `gerar_txt(df, resumo, saida_txt)` - Linha 620
```python
def gerar_txt(df: pd.DataFrame, resumo: dict, saida_txt: str = "Calculadora_relatorio.txt"):
```
**Função**: *** GERAÇÃO DE RELATÓRIOS COMPLETOS ***
- Cabeçalho com data/hora
- Resumo executivo com totais  
- Produtividade por linha
- Dados técnicos detalhados
- Explicação sistema semáforo
- Glossário de termos

**Usado em**:
- calculadora_cana_principal_v1.1.py: main() linha 495

---

### 🎮 FUNÇÕES DE ENTRADA DO USUÁRIO (funcoes_calculadora.py)

#### `handle_command(raw: str)` - Linha 807
```python
def handle_command(raw: str) -> Tuple[str, str]:
```
**Função**: Processa comandos especiais do usuário (:help, :cat, etc.)
**Usado em**:
- ask_float() e ask_str() - Processamento de comandos

#### `ask_float(prompt, required, default, ...)` - Linha 817
```python  
def ask_float(prompt: str, required: bool = False, default: float = None, ...):
```
**Função**: Solicita entrada numérica do usuário com validação
**Usado em**:
- calculadora_cana_principal_v1.1.py: main() - Entrada de área, percentuais

#### `ask_str(prompt, required, choices, ...)` - Linha 860
```python
def ask_str(prompt: str, required: bool = False, choices: List[str] = None, ...):
```
**Função**: Solicita entrada de texto do usuário com validação
**Usado em**:  
- calculadora_cana_principal_v1.1.py: main() - Entrada de variedade, época, processo

---

## FUNÇÕES DO PROGRAMA PRINCIPAL (calculadora_cana_principal_v1.1.py)

#### `load_params_from_oracle_v2(tipo_conexao, params_sql, tol_chuva, tol_seca)` - Linha 44
```python
def load_params_from_oracle_v2(tipo_conexao: str, params_sql: str, tol_chuva: float, tol_seca: float):
```
**Função**: Carrega parâmetros do Oracle usando rotinas_V2.py
- Conecta ao Oracle
- Testa conexão  
- Carrega dados da tabela parametros
- Fallback para JSON se tabela vazia
- Processa e normaliza dados

**Usado em**:
- main() linha 273 - Inicialização do programa

#### `sincronizar_json_oracle()` - Linha 171  
```python
def sincronizar_json_oracle():
```
**Função**: Sincroniza dados entre JSON e Oracle
**Usado em**:
- menu_inicial() opção 4 - Sincronização manual

#### `menu_inicial(MAP_DISPLAY, PARAMS)` - Linha 207
```python
def menu_inicial(MAP_DISPLAY: dict, PARAMS: dict):
```
**Função**: Menu principal interativo do programa
**Opções**:
1. Ver catálogo de combinações
2. Ver glossário de parâmetros
3. Sobre este programa  
4. Sincronizar JSON -> Oracle
5. Iniciar cálculos
6. Sair

**Usado em**:
- main() linha 284 - Após carregamento dos parâmetros

#### `main()` - Linha 265
```python  
def main():
```
**Função**: *** FUNÇÃO PRINCIPAL DO PROGRAMA ***
- Carrega parâmetros do Oracle
- Exibe menu inicial
- Processa entradas do usuário
- Executa cálculos linha por linha
- Gera relatórios finais

**Usado em**:
- Bloco __main__ linha 509 - Entry point do programa

---

## FUNÇÕES DE INTEGRAÇÃO ORACLE (rotinas_V2.py)

#### `conectar_oracle(tipo)` - Linha 152
```python
def conectar_oracle(tipo: str = 'producao'):
```
**Função**: Conecta ao banco Oracle (produção/teste)
**Usado em**:
- calculadora_cana_principal_v1.1.py: load_params_from_oracle_v2()
- Todas as operações que precisam de conexão Oracle

#### `desconectar_oracle(conn)` - Linha 182
```python  
def desconectar_oracle(conn):
```
**Função**: Desconecta do Oracle de forma segura
**Usado em**:
- Após todas as operações com Oracle

#### `carregar_parametros_Json_como_dicionario()` - Linha 195
```python
def carregar_parametros_Json_como_dicionario():
```
**Função**: Carrega parâmetros do arquivo parametros.json
**Usado em**:
- load_params_from_oracle_v2() - Fallback quando Oracle vazio

#### `carregar_parametros_no_oracle(dict_parametros, conn)` - Linha 345
```python
def carregar_parametros_no_oracle(dict_parametros: dict, conn):
```
**Função**: Carrega dados do JSON para tabela Oracle
**Usado em**:
- sincronizar_json_oracle() - Sincronização de dados

---

## FLUXO DE EXECUÇÃO PRINCIPAL

```
1. main() 
   ↓
2. load_params_from_oracle_v2()
   ↓ 
3. conectar_oracle() → Carrega parametros.json → Processa dados
   ↓
4. menu_inicial() → Opções do usuário
   ↓
5. Loop de entrada: ask_str(), ask_float()
   ↓
6. compute_row() → Cálculos agronômicos  
   ↓
7. gerar_txt() → Relatório final
```

## DEPENDÊNCIAS ENTRE ARQUIVOS

```
calculadora_cana_principal_v1.1.py
├── rotinas_V2.py (conexão Oracle)
│   ├── oracledb (driver Oracle)
│   ├── pandas (manipulação dados)
│   └── json (parametros.json)
└── funcoes_calculadora.py (cálculos e interface)
    ├── pandas (DataFrames)
    ├── unicodedata (normalização)
    └── datetime (timestamps)
```

---

## ARQUIVO DE CONFIGURAÇÃO

### 📄 parametros.json
**Função**: Arquivo de fallback com parâmetros técnicos
**Estrutura**: Array de objetos com chaves:
- Variedade, Epoca, Processo  
- e_rec_m, g_final_rec, s_rec, g_to_rec
- l_to_rec, rho_rec, d_rec_kg_m

**Usado quando**: Tabela Oracle vazia ou inacessível

---

## TOLERÂNCIAS E CONSTANTES

### Definidas em calculadora_cana_principal_v1.1.py:
```python
TOL_CHUVA_OVERRIDE = 0.08  # 8% para época chuvosa
TOL_SECA_OVERRIDE  = 0.05  # 5% para época seca
```

### Usadas em:
- compute_row() - Cálculo do status semáforo
- Sistema de qualidade agronômica

---

## RESUMO ESTATÍSTICO

- **Total de funções**: 23+
- **Arquivos principais**: 3
- **Linhas de código**: ~1400+  
- **Funções críticas**: compute_row(), gerar_txt(), main()
- **Integrações**: Oracle Database, JSON, Terminal UI