# 💾 Código Fonte - Calculadora de Cana-de-Açúcar

Esta pasta contém todos os arquivos de código fonte do projeto desenvolvido ao longo das fases do CAP6.

## 📂 Estrutura dos Arquivos

### Arquivos Principais
- **`calculadora_cana_principal.py`** - Programa principal com menu e orquestração do sistema
- **`funcoes_calculadora.py`** - Biblioteca completa de cálculos agronômicos e interface
- **`rotinas_V2.py`** - Integração com Oracle Database e operações de dados

### Arquivos de Configuração
- **`requirements.txt`** - Dependências Python necessárias
- **`parametros.json`** - Parâmetros técnicos das variedades de cana-de-açúcar

## 🚀 Como Executar

1. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Executar o programa:**
   ```bash
   python calculadora_cana_principal.py
   ```

## 🔧 Pré-requisitos

- Python 3.10+
- Oracle Database (opcional - sistema possui fallback JSON)
- Bibliotecas: pandas, oracledb

## 📈 Versões

- **v2.0** - Versão atual simplificada (apenas relatórios TXT)
- **v1.1** - Versão com múltiplos formatos de saída
- **v1.0** - Versão inicial

---

*Este código foi desenvolvido como parte do projeto FIAP CAP6 - Fase 2 (2025)*