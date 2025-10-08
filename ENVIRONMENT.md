# Ambiente Python - FIAP_202510_CAP6

## Informações do Ambiente

**Tipo:** Ambiente Virtual (venv)  
**Versão do Python:** 3.14.0.final.0  
**Localização:** `venv_Cap6/`  
**Sistema:** Windows  

## Dependências Instaladas

### 📦 **Dependências Principais**
```
oracledb==3.4.0          # Conexão Oracle Database (✅ Atualizado)
pandas==2.3.3            # Análise de dados (✅ Compatível Python 3.14)
numpy==2.3.3             # Dependência do pandas (✅ Auto-instalado)
```

### 🔐 **Dependências de Segurança**
```
cryptography==46.0.2     # Criptografia para conexões seguras
cffi==2.0.0              # Interface C para Python
pycparser==2.23          # Parser C para cffi
```

### 📅 **Dependências de Data/Hora**
```
python-dateutil==2.9.0.post0  # Manipulação de datas
pytz==2025.2                   # Fusos horários
tzdata==2025.2                 # Dados de timezone
```

### 🛠️ **Utilitários**
```
six==1.17.0              # Compatibilidade Python 2/3
typing_extensions==4.15.0 # Extensões de tipos
pip==25.2                # Gerenciador de pacotes
```

## Dependências Faltantes (opcionais)

### 📊 **Para trabalhar com Excel** (não instaladas ainda):
```
openpyxl>=3.1.0          # Leitura/escrita de arquivos Excel (.xlsx)
xlsxwriter>=3.1.0        # Criação de arquivos Excel com formatação
```

## Como instalar dependências faltantes

```bash
# Instalar dependências do Excel
pip install openpyxl>=3.1.0 xlsxwriter>=3.1.0

# Ou instalar todas do requirements.txt
pip install -r requirements.txt
```

## Status das Dependências

| Dependência | Status | Versão Instalada | Versão Requerida |
|-------------|--------|------------------|------------------|
| oracledb | ✅ OK | 3.4.0 | >=2.3.0 |
| pandas | ✅ OK | 2.3.3 | >=2.2.0 |
| openpyxl | ❌ Faltando | - | >=3.1.0 |
| xlsxwriter | ❌ Faltando | - | >=3.1.0 |

## Arquivos do Projeto que usam as dependências

### **oracledb + pandas:**
- `main.py`
- `manutencao_oracle_paramentros.py` 
- `Exemplos/oracle.py`

### **json + os (bibliotecas padrão):**
- `carga_parametros_json.py`
- `parametros_com_dicionarios.py`
- `Exemplos/exemplo_json.py`
- `Exemplos/exemplo_parametros_json.py`
- `Exemplos/guia_json_para_dict.py`

### **openpyxl + xlsxwriter (quando necessário):**
- Futuros arquivos para manipulação de Excel

## Comandos Úteis

```bash
# Verificar dependências instaladas
pip list

# Verificar se há atualizações
pip list --outdated

# Congelar dependências atuais
pip freeze > requirements_current.txt

# Instalar ambiente limpo
pip install -r requirements.txt
```