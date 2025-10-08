# FIAP_202510_CAP6 - Sistema de Parâmetros e Manipulação JSON

🎓 **Projeto da disciplina CAP6 - Fase 2 2025**
🏫 **FIAP - Faculdade de Informática e Administração Paulista**

## 📖 Descrição

Sistema abrangente desenvolvido em Python para gerenciamento de parâmetros de processo e manipulação de dados JSON, com integração completa ao Oracle Database. O projeto evoluiu de um sistema CRUD simples para uma solução robusta de análise e processamento de dados.

## 🚀 Funcionalidades Principais

### 🗂️ **Sistema CRUD de Parâmetros**

- ✅ Cadastrar Parâmetros (Variedade, Época, Processo)
- ✅ Listar Parâmetros com análise estatística
- ✅ Alterar Parâmetros por chave composta
- ✅ Excluir Parâmetros individuais ou em massa
- ✅ Conexão Oracle Database com tratamento de erros

### 📊 **Manipulação de Dados JSON**

- ✅ Carregamento e conversão de arquivos JSON
- ✅ Conversão Lista ↔ Dicionário
- ✅ Análise estatística de dados
- ✅ Filtragem por múltiplos critérios
- ✅ Exportação em diferentes formatos

### 🔍 **Análise de Dados**

- ✅ Estatísticas automáticas por categoria
- ✅ Contadores de variedades, épocas e processos
- ✅ Busca otimizada por chave descritiva
- ✅ Visualização formatada de resultados

## 🔧 Pré-requisitos

- ✅ **Python 3.14+** (testado e otimizado)
- 🗄️ **Oracle Database** (acesso ao servidor oracle.fiap.com.br)
- 🔐 **Credenciais válidas** (RM567007 para acesso acadêmico)
- 💾 **Git** (para clonagem do repositório)

## 📦 Instalação

### 1️⃣ **Instalar Python 3.14**

**Windows:**

```bash
# Via Microsoft Store (recomendado)
# Busque por "Python 3.12" ou versão mais recente
# OU baixe de: https://www.python.org/downloads/
```

**⚠️ IMPORTANTE:** Marque "Add Python to PATH" durante a instalação

### 2️⃣ **Clonar o repositório**

```bash
git clone https://github.com/dortad/FIAP_202510_CAP6.git
cd FIAP_202510_CAP6
```

### 3️⃣ **Configurar ambiente virtual**

```bash
# Criar ambiente virtual
python -m venv venv_Cap6

# Ativar ambiente (Windows)
venv_Cap6\Scripts\activate

# Ativar ambiente (Linux/Mac)
source venv_Cap6/bin/activate
```

### 4️⃣ **Instalar dependências**

```bash
# Instalar todas as dependências
pip install -r requirements.txt

# Verificar instalação
pip list
```

## 🚀 Como Executar

### **Sistema CRUD de Parâmetros:**

```bash
python main.py
# ou
python manutencao_oracle_paramentros.py
```

### **Manipulação de JSON:**

```bash
# Trabalhar com listas
python carga_parametros_json.py

# Trabalhar com dicionários  
python parametros_com_dicionarios.py
```

### **Exemplos educativos:**

```bash
# Navegue para a pasta de exemplos
cd Exemplos

# Execute exemplos específicos
python exemplo_json.py
python guia_json_para_dict.py
```

## 📁 Estrutura do Projeto

```txt
FIAP_202510_CAP6/
├── 📄 README.md                          # Documentação do projeto
├── 📄 requirements.txt                   # Dependências do projeto
├── 🐍 main.py                           # Sistema CRUD principal
├── 🐍 manutencao_oracle_paramentros.py  # Manutenção Oracle
├── 🐍 carga_parametros_json.py          # Processamento JSON (listas)
├── 🐍 parametros_com_dicionarios.py     # Processamento JSON (dicionários)
├── 📊 parametros.json                    # Base de dados JSON (28 registros)
├── 📊 parametros_dicionario.json        # Versão dicionário
├── 📊 parametros_extras.json           # Dados adicionais
├── 📁 venv_Cap6/                        # Ambiente virtual Python
└── 📁 Exemplos/                         # Códigos educativos
    ├── 🐍 exemplo_json.py
    ├── 🐍 guia_json_para_dict.py
    └── 📊 pessoas.json
```

## 🗄️ Estrutura do Banco de Dados

```sql
-- Tabela principal de parâmetros (usada pelo sistema CRUD)
CREATE TABLE parametros (
    variedade VARCHAR2(10),              -- Variedade do produto (ex: Arabica, Robusta)
    epoca VARCHAR2(10),                  -- Época/sazonalidade (ex: Seca, Chuva)
    processo VARCHAR2(10),               -- Processo aplicado (ex: Mecanico, Manual)
    e_rec_m NUMBER(3,2),                 -- Parâmetro de eficiência (% decimal)
    g_final_rec NUMBER,                  -- Grau final de recuperação (inteiro)
    s_rec NUMBER(3,2),                   -- Parâmetro S de recuperação (% decimal)
    g_to_rec NUMBER(3,2),                -- Grau TO de recuperação (% decimal)
    l_to_rec NUMBER(3,2),                -- Parâmetro L TO de recuperação (% decimal)
    rho_rec NUMBER(3,2),                 -- Densidade de recuperação (% decimal)
    d_rec_kg_m NUMBER(3,2),              -- Densidade kg/m de recuperação (% decimal)
    CONSTRAINT pk_parametros PRIMARY KEY (variedade, epoca, processo)
);

-- Tabela legada (PetShop) - mantida para compatibilidade
CREATE TABLE petshop (
    pet_id NUMBER GENERATED AS IDENTITY,
    tipo_pet VARCHAR2(10),
    nome_pet VARCHAR2(50),
    idade NUMBER(20,2),
    CONSTRAINT pk_petshop PRIMARY KEY (pet_id)
);

```

## 🛠️ Tecnologias Utilizadas

### **Backend & Processamento:**

- 🐍 **Python 3.14+** - Linguagem principal
- 🗄️ **Oracle Database** - Sistema de banco de dados
- 📦 **oracledb 2.3.0+** - Driver nativo Oracle
- 🐼 **pandas 2.2.0+** - Análise e manipulação de dados

### **Estruturas de Dados:**

- 📋 **JSON nativo** - Processamento de arquivos
- 📚 **Listas Python** - Estruturas sequenciais
- 📖 **Dicionários Python** - Mapeamento chave-valor
- 🔍 **Algoritmos de busca** - Pesquisa por critérios

### **Ferramentas de Desenvolvimento:**

- 📁 **Git** - Controle de versão
- 🏠 **venv** - Ambientes virtuais
- 📝 **Markdown** - Documentação
- 🔧 **pip** - Gerenciamento de pacotes

## ⚙️ Configuração do Banco

### **Parâmetros de Conexão:**

- 🌐 **Servidor:** `oracle.fiap.com.br:1521/ORCL`
- 👤 **Usuário:** `RM567007` (ambiente acadêmico)
- 🔐 **Senha:** Configurada em variável de ambiente
- 📡 **Driver:** oracledb (modo Thin)

### **Configuração de Ambiente:**

```bash
# Definir variável de ambiente (Windows)
set ORACLE_PASSWORD=sua_senha_aqui

# Verificar conexão
python -c "import oracledb; print('Oracle client ready')"
```

## � Exemplos de Uso

### **Processamento com Listas:**

```python
from carga_parametros_json import *

# Carregar dados
parametros = carregar_parametros_json()
print(f"Total de parâmetros: {len(parametros)}")

# Buscar por variedade
resultados = buscar_por_variedade(parametros, "Arabica")
```

### **Processamento com Dicionários:**

```python
from parametros_com_dicionarios import *

# Carregar como dicionário
dict_parametros = carregar_parametros_como_dicionario()

# Buscar por critérios múltiplos
resultados = buscar_por_criterios(dict_parametros, 
                                variedade="Robusta", 
                                epoca="Seca")
```

### **Sistema CRUD Oracle:**

```python
# Executar o sistema de manutenção Oracle
python manutencao_oracle_paramentros.py

# Exemplo de dados para cadastro:
# Variedade: Arabica
# Época: Seca  
# Processo: Natural
# e_rec_m: 0.85
# g_final_rec: 95
# s_rec: 0.12
# g_to_rec: 0.78
# l_to_rec: 0.65
# rho_rec: 0.92
# d_rec_kg_m: 1.25
```

**Estrutura dos parâmetros técnicos:**

- 🌱 **variedade**: Tipo de café (Arabica, Robusta, etc.)
- 📅 **epoca**: Sazonalidade (Seca, Umida)
- ⚙️ **processo**: Método de processamento (Natural, Lavado, etc.)
- 📊 **e_rec_m**: Eficiência de recuperação média (decimal)
- 🎯 **g_final_rec**: Grau final de recuperação (inteiro)
- 📈 **s_rec, g_to_rec, l_to_rec**: Parâmetros de recuperação específicos
- 🧮 **rho_rec**: Densidade de recuperação
- ⚖️ **d_rec_kg_m**: Densidade por kg/m

## 🔧 Solução de Problemas

### **Erro: Módulo 'oracledb' não encontrado**

```bash
pip install oracledb>=2.3.0
```

### **Erro: Incompatibilidade pandas/Python 3.14**

```bash
pip install pandas>=2.2.0
```

### **Erro: Conflito de nomes (json.py)**

- ❌ **Não usar:** arquivos nomeados `json.py`
- ✅ **Usar:** nomes como `manipula_json.py`, `processa_dados.py`

### **Conexão Oracle falhando:**

1. Verificar credenciais no arquivo de configuração
2. Testar conectividade com o servidor FIAP
3. Validar versão do driver oracledb

## 🎯 Próximos Passos

- [ ] 🔐 **Implementar logica para a aplicação**

## 🀽� Contribuidores

- 🎓 **Durval (@dortad)**
- 🏫 **Murilo**

---

**Licença:** Projeto acadêmico - FIAP 2025 | Fase 2 CAP6

---

*Projeto desenvolvido como parte do curso de Análise e Desenvolvimento de Sistemas da FIAP* 🎓
