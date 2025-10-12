# 🌾 Calculadora de Cana-de-Açúcar# FIAP_202510_CAP6 - Sistema de Parâmetros e Manipulação JSON



<div align="center">🎓 **Projeto da disciplina CAP6 - Fase 2 2025**

🏫 **FIAP - Faculdade de Informática e Administração Paulista**

![Python](https://img.shields.io/badge/Python-3.14.0-blue.svg)

![Oracle](https://img.shields.io/badge/Oracle-Database-red.svg)## 📖 Descrição

![License](https://img.shields.io/badge/License-MIT-green.svg)

![FIAP](https://img.shields.io/badge/FIAP-CAP6_2025-purple.svg)Sistema abrangente desenvolvido em Python para gerenciamento de parâmetros de processo e manipulação de dados JSON, com integração completa ao Oracle Database. O projeto evoluiu de um sistema CRUD simples para uma solução robusta de análise e processamento de dados.



**Sistema especializado para cálculo de material vegetal (toletes/mudas) necessário para plantio de cana-de-açúcar**## 🚀 Funcionalidades Principais



</div>### 🗂️ **Sistema CRUD de Parâmetros**



---- ✅ Cadastrar Parâmetros (Variedade, Época, Processo)

- ✅ Listar Parâmetros com análise estatística

## 📋 Visão Geral- ✅ Alterar Parâmetros por chave composta

- ✅ Excluir Parâmetros individuais ou em massa

A **Calculadora de Cana-de-Açúcar** é um sistema desenvolvido para auxiliar no **planejamento e dimensionamento do plantio** de cana-de-açúcar. O programa calcula a quantidade exata de material vegetal (toletes/mudas) necessária para plantar uma área específica, considerando diferentes variedades, épocas de plantio e métodos de cultivo.- ✅ Conexão Oracle Database com tratamento de erros



### 🎯 Objetivo Principal### 📊 **Manipulação de Dados JSON**



**Calcular a massa total de toletes (em toneladas) necessária para plantar uma área específica**, garantindo:- ✅ Carregamento e conversão de arquivos JSON

- ✅ Otimização do uso de material vegetal- ✅ Conversão Lista ↔ Dicionário

- ✅ Redução de desperdícios- ✅ Análise estatística de dados

- ✅ Controle de qualidade do plantio- ✅ Filtragem por múltiplos critérios

- ✅ Planejamento logístico eficiente- ✅ Exportação em diferentes formatos



---### 🔍 **Análise de Dados**



## 🚀 Funcionalidades- ✅ Estatísticas automáticas por categoria

- ✅ Contadores de variedades, épocas e processos

### 📊 Cálculos Técnicos- ✅ Busca otimizada por chave descritiva

- **Densidade de plantio** (toletes por hectare)- ✅ Visualização formatada de resultados

- **Massa de material vegetal** necessária

- **Controle de qualidade** com sistema semáforo## 🔧 Pré-requisitos

- **Análise de produtividade** por linha de plantio

- **Consideração de perdas** por manobras e tráfego- ✅ **Python 3.14+** (testado e otimizado)

- 🗄️ **Oracle Database** (acesso ao servidor oracle.fiap.com.br)

### 📈 Relatórios Completos- 🔐 **Credenciais válidas** (RM567007 para acesso acadêmico)

- **Relatório TXT**: Detalhado com explicações técnicas- 💾 **Git** (para clonagem do repositório)

- **Relatório PDF**: Formatado com gráficos e tabelas

- **Planilha XLSX**: Para análise de dados## 📦 Instalação

- **Arquivo CSV**: Para integração com outros sistemas

### 1️⃣ **Instalar Python 3.14**

### 🔗 Integração Oracle

- Conexão com banco de dados Oracle**Windows:**

- Gerenciamento de parâmetros técnicos

- Consulta automática de especificações por variedade```bash

# Via Microsoft Store (recomendado)

### ⚡ Interface Amigável# Busque por "Python 3.12" ou versão mais recente

- Menu interativo no terminal# OU baixe de: https://www.python.org/downloads/

- Validação de entrada de dados```

- Mensagens de status claras

- Suporte a múltiplas execuções**⚠️ IMPORTANTE:** Marque "Add Python to PATH" durante a instalação



---### 2️⃣ **Clonar o repositório**



## 🛠️ Tecnologias Utilizadas```bash

git clone https://github.com/dortad/FIAP_202510_CAP6.git

| Tecnologia | Versão | Função |cd FIAP_202510_CAP6

|------------|--------|--------|```

| **Python** | 3.14.0 | Linguagem principal |

| **Oracle Database** | - | Armazenamento de parâmetros |### 3️⃣ **Configurar ambiente virtual**

| **pandas** | ≥2.2.0 | Manipulação de dados |

| **matplotlib** | ≥3.7.0 | Geração de gráficos e PDF |```bash

| **oracledb** | ≥2.3.0 | Conectividade Oracle |# Criar ambiente virtual

| **openpyxl** | ≥3.1.0 | Geração de arquivos Excel |python -m venv venv_Cap6



---# Ativar ambiente (Windows)

venv_Cap6\Scripts\activate

## 📁 Estrutura do Projeto

# Ativar ambiente (Linux/Mac)

```source venv_Cap6/bin/activate

FIAP_202510_CAP6/```

│

├── 📄 calculadora_cana_principal_v1.1.py    # Programa principal### 4️⃣ **Instalar dependências**

├── 📄 funcoes_calculadora.py                # Funções de cálculo e relatórios

├── 📄 rotinas_V2.py                         # Conexão Oracle e utilitários```bash

├── 📄 parametros.json                       # Parâmetros técnicos (fallback)# Instalar todas as dependências

├── 📄 requirements.txt                      # Dependências do projetopip install -r requirements.txt

│

├── 📁 Excel base/                           # Templates Excel# Verificar instalação

├── 📁 venv_Cap6/                           # Ambiente virtual Pythonpip list

├── 📁 __pycache__/                         # Cache Python```

│

└── 📊 Resultados de exemplo:## 🚀 Como Executar

    ├── Calculadora_Cana_v1_1_resultados.txt

    ├── Calculadora_Cana_v1_1_resultados.pdf### **Sistema CRUD de Parâmetros:**

    ├── Calculadora_Cana_v1_1_resultados.xlsx

    └── Calculadora_Cana_v1_1_resultados.csv```bash

```python main.py

# ou

---python manutencao_oracle_paramentros.py

```

## 🔧 Instalação e Configuração

### **Manipulação de JSON:**

### 1️⃣ Pré-requisitos

```bash

- **Python 3.14.0** ou superior# Trabalhar com listas

- **Oracle Database** configurado e acessívelpython carga_parametros_json.py

- **Git** para clone do repositório

# Trabalhar com dicionários  

### 2️⃣ Clone do Repositóriopython parametros_com_dicionarios.py

```

```bash

git clone https://github.com/dortad/FIAP_202510_CAP6.git### **Exemplos educativos:**

cd FIAP_202510_CAP6

``````bash

# Navegue para a pasta de exemplos

### 3️⃣ Ambiente Virtualcd Exemplos



```bash# Execute exemplos específicos

# Windowspython exemplo_json.py

python -m venv venv_Cap6python guia_json_para_dict.py

venv_Cap6\Scripts\activate```



# Linux/Mac## 📁 Estrutura do Projeto

python -m venv venv_Cap6

source venv_Cap6/bin/activate```txt

```FIAP_202510_CAP6/

├── 📄 README.md                          # Documentação do projeto

### 4️⃣ Instalação de Dependências├── 📄 requirements.txt                   # Dependências do projeto

├── 🐍 main.py                           # Sistema CRUD principal

```bash├── 🐍 manutencao_oracle_paramentros.py  # Manutenção Oracle

# Instalação completa├── 🐍 carga_parametros_json.py          # Processamento JSON (listas)

pip install -r requirements.txt├── 🐍 parametros_com_dicionarios.py     # Processamento JSON (dicionários)

├── 📊 parametros.json                    # Base de dados JSON (28 registros)

# Ou instalação manual├── 📊 parametros_dicionario.json        # Versão dicionário

pip install oracledb pandas matplotlib openpyxl xlsxwriter├── 📊 parametros_extras.json           # Dados adicionais

```├── 📁 venv_Cap6/                        # Ambiente virtual Python

└── 📁 Exemplos/                         # Códigos educativos

### 5️⃣ Configuração do Oracle    ├── 🐍 exemplo_json.py

    ├── 🐍 guia_json_para_dict.py

Edite o arquivo `rotinas_V2.py` para configurar a conexão Oracle:    └── 📊 pessoas.json

```

```python

# Configurações de conexão## 🗄️ Estrutura do Banco de Dados

DB_CONFIG = {

    'host': 'seu-servidor-oracle',```sql

    'port': 1521,-- Tabela principal de parâmetros (usada pelo sistema CRUD)

    'service': 'seu-servico',CREATE TABLE parametros (

    'user': 'seu-usuario',    variedade VARCHAR2(10),              -- Variedade do produto (ex: Arabica, Robusta)

    'password': 'sua-senha'    epoca VARCHAR2(10),                  -- Época/sazonalidade (ex: Seca, Chuva)

}    processo VARCHAR2(10),               -- Processo aplicado (ex: Mecanico, Manual)

```    e_rec_m NUMBER(3,2),                 -- Parâmetro de eficiência (% decimal)

    g_final_rec NUMBER,                  -- Grau final de recuperação (inteiro)

---    s_rec NUMBER(3,2),                   -- Parâmetro S de recuperação (% decimal)

    g_to_rec NUMBER(3,2),                -- Grau TO de recuperação (% decimal)

## 🎮 Como Usar    l_to_rec NUMBER(3,2),                -- Parâmetro L TO de recuperação (% decimal)

    rho_rec NUMBER(3,2),                 -- Densidade de recuperação (% decimal)

### Execução Básica    d_rec_kg_m NUMBER(3,2),              -- Densidade kg/m de recuperação (% decimal)

    CONSTRAINT pk_parametros PRIMARY KEY (variedade, epoca, processo)

```bash);

python calculadora_cana_principal_v1.1.py

```



### Menu Principal```



```## 🛠️ Tecnologias Utilizadas

🌾 === CALCULADORA DE CANA-DE-AÇÚCAR v2 ===

### **Backend & Processamento:**

1. 📊 Executar cálculo completo

2. 🔧 Configurar conexão Oracle  - 🐍 **Python 3.14+** - Linguagem principal

3. 📋 Listar parâmetros disponíveis- 🗄️ **Oracle Database** - Sistema de banco de dados

4. ❓ Ajuda e documentação- 📦 **oracledb 2.3.0+** - Driver nativo Oracle

5. 🚪 Sair- 🐼 **pandas 2.2.0+** - Análise e manipulação de dados



Escolha uma opção: ### **Estruturas de Dados:**

```

- 📋 **JSON nativo** - Processamento de arquivos

### Exemplo de Uso- 📚 **Listas Python** - Estruturas sequenciais

- 📖 **Dicionários Python** - Mapeamento chave-valor

```- 🔍 **Algoritmos de busca** - Pesquisa por critérios

=== DADOS DE ENTRADA ===

Área total (hectares): 100.5### **Ferramentas de Desenvolvimento:**

Variedade: RB867515

Época: Chuva- 📁 **Git** - Controle de versão

Processo: Mecanizado- 🏠 **venv** - Ambientes virtuais

Perdas por manobras (%): 3- 📝 **Markdown** - Documentação

Perdas por tráfego (%): 1- 🔧 **pip** - Gerenciamento de pacotes



=== RESULTADOS ===## ⚙️ Configuração do Banco

✅ Massa total necessária: 67.8 toneladas

✅ Status: OK (desvio: 2.1%)### **Parâmetros de Conexão:**

📊 Relatórios gerados em múltiplos formatos

```- 🌐 **Servidor:** `oracle.fiap.com.br:1521/ORCL`

- 👤 **Usuário:** `RM567007` (ambiente acadêmico)

---- 🔐 **Senha:** Configurada em variável de ambiente

- 📡 **Driver:** oracledb (modo Thin)

## 📊 Conceitos Técnicos

### **Configuração de Ambiente:**

### 🌱 Fundamentos da Cana

```bash

| Termo | Definição |# Definir variável de ambiente (Windows)

|-------|-----------|set ORACLE_PASSWORD=sua_senha_aqui

| **Tolete** | Pedaço do colmo cortado para plantio (30-50 cm) |

| **Gema** | Broto que origina nova planta |# Verificar conexão

| **Espaçamento** | Distância entre fileiras de plantio |python -c "import oracledb; print('Oracle client ready')"

| **Densidade** | Quantidade de material por área |```



### ⚙️ Tipos de Plantio## � Exemplos de Uso



- **Manual**: Toletes longos colocados manualmente no sulco### **Processamento com Listas:**

- **Mecanizado**: Toletes menores (billets) distribuídos por máquinas

```python

### 📈 Fórmulas de Cálculofrom carga_parametros_json import *



```# Carregar dados

Metros de fileira/ha = 10.000 ÷ Espaçamentoparametros = carregar_parametros_json()

Toletes/metro = Gemas_finais ÷ (Gemas_úteis ÷ Tolete)print(f"Total de parâmetros: {len(parametros)}")

Massa/ha = Toletes/ha × Comprimento × Densidade ÷ 1000

Massa_total = Massa/ha × Área_efetiva# Buscar por variedade

```resultados = buscar_por_variedade(parametros, "Arabica")

```

---

### **Processamento com Dicionários:**

## 🎯 Sistema de Status (Semáforo)

```python

| Status | Descrição | Tolerância |from parametros_com_dicionarios import *

|--------|-----------|------------|

| 🟢 **OK** | Dentro das especificações | ≤ 5% (Seca), ≤ 8% (Chuva) |# Carregar como dicionário

| 🟡 **ATENÇÃO** | Fora das tolerâncias | > tolerância definida |dict_parametros = carregar_parametros_como_dicionario()



---# Buscar por critérios múltiplos

resultados = buscar_por_criterios(dict_parametros, 

## 📝 Exemplos de Saída                                variedade="Robusta", 

                                epoca="Seca")

### Relatório Resumido```

```

🌾 CALCULADORA DE CANA-DE-AÇÚCAR - RESULTADOS### **Sistema CRUD Oracle:**



📊 RESUMO EXECUTIVO```python

Área Total: 100.5 ha# Executar o sistema de manutenção Oracle

Variedade: RB867515python manutencao_oracle_paramentros.py

Época: Chuva  

Processo: Mecanizado# Exemplo de dados para cadastro:

Massa Total: 67.8 toneladas# Variedade: Arabica

Status: ✅ OK (desvio: 2.1%)# Época: Seca  

# Processo: Natural

📈 PRODUTIVIDADE POR LINHA# e_rec_m: 0.85

- Linha 1: 6.67 m/ha • 1.60 kg/m • Massa: 10.8 t# g_final_rec: 95

- Produtividade média: 674.6 kg/ha# s_rec: 0.12

```# g_to_rec: 0.78

# l_to_rec: 0.65

### Status Detalhado# rho_rec: 0.92

```# d_rec_kg_m: 1.25

📋 EXPLICAÇÃO DO STATUS/SEMÁFORO DE QUALIDADE```



O status indica se o cálculo está dentro das tolerâncias técnicas:**Estrutura dos parâmetros técnicos:**



🟢 OK: Desvio ≤ 5% (época seca) ou ≤ 8% (época chuva)- 🌱 **variedade**: Tipo de café (Arabica, Robusta, etc.)

🟡 ATENÇÃO: Desvio > tolerância - revisar parâmetros- 📅 **epoca**: Sazonalidade (Seca, Umida)

- ⚙️ **processo**: Método de processamento (Natural, Lavado, etc.)

Tolerâncias baseadas em:- 📊 **e_rec_m**: Eficiência de recuperação média (decimal)

- Variabilidade natural da cultura- 🎯 **g_final_rec**: Grau final de recuperação (inteiro)

- Precisão dos equipamentos de plantio- 📈 **s_rec, g_to_rec, l_to_rec**: Parâmetros de recuperação específicos

- Condições climáticas da época- 🧮 **rho_rec**: Densidade de recuperação

```- ⚖️ **d_rec_kg_m**: Densidade por kg/m



---## 🔧 Solução de Problemas



## 🧪 Testes e Validação### **Erro: Módulo 'oracledb' não encontrado**



### Execução de Testes```bash

```bashpip install oracledb>=2.3.0

# Teste com dados de exemplo```

python calculadora_cana_principal_v1.1.py

### **Erro: Incompatibilidade pandas/Python 3.14**

# Validação com parâmetros conhecidos

python -m pytest tests/ -v```bash

```pip install pandas>=2.2.0

```

### Casos de Teste Incluídos

- ✅ Validação de fórmulas de cálculo### **Erro: Conflito de nomes (json.py)**

- ✅ Teste de conexão Oracle

- ✅ Geração de relatórios- ❌ **Não usar:** arquivos nomeados `json.py`

- ✅ Validação de tolerâncias- ✅ **Usar:** nomes como `manipula_json.py`, `processa_dados.py`

- ✅ Teste de diferentes variedades

### **Conexão Oracle falhando:**

---

1. Verificar credenciais no arquivo de configuração

## 🤝 Contribuição2. Testar conectividade com o servidor FIAP

3. Validar versão do driver oracledb

### Como Contribuir

1. **Fork** o repositório## 🎯 Próximos Passos

2. Crie uma **branch** para sua feature (`git checkout -b feature/nova-funcionalidade`)

3. **Commit** suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)- [ ] 🔐 **Implementar logica para a aplicação**

4. **Push** para a branch (`git push origin feature/nova-funcionalidade`)

5. Abra um **Pull Request**## 🀽� Contribuidores



### Diretrizes- 🎓 **Durval (@dortad)**

- Siga o padrão de código existente- 🏫 **Murilo**

- Adicione documentação para novas funcionalidades

- Inclua testes para novas features---

- Mantenha compatibilidade com versões existentes

**Licença:** Projeto acadêmico - FIAP 2025 | Fase 2 CAP6

---

---

## 📚 Documentação Adicional

*Projeto desenvolvido como parte do curso de Análise e Desenvolvimento de Sistemas da FIAP* 🎓

- 📖 **[O_que_faz_o_programa.md](O_que_faz_o_programa.md)**: Explicação detalhada das funcionalidades
- 🔧 **[requirements.txt](requirements.txt)**: Lista completa de dependências
- 📊 **[parametros.json](parametros.json)**: Estrutura de parâmetros técnicos

---

## 📋 Roadmap

### 🎯 Próximas Versões
- [ ] Interface web (Flask/Django)
- [ ] API REST para integração
- [ ] Suporte a PostgreSQL/MySQL
- [ ] Módulo de análise econômica
- [ ] Dashboard de monitoramento
- [ ] Integração com sistemas ERP

### 🔮 Ideias Futuras
- [ ] Machine Learning para otimização de parâmetros
- [ ] Integração com dados climáticos
- [ ] Aplicativo mobile
- [ ] Análise de sustentabilidade

---

## 👥 Equipe

| Papel | Nome | Contato |
|-------|------|---------|
| **Desenvolvedor Principal** | Seu Nome | seu.email@fiap.com.br |
| **Orientador Acadêmico** | Prof. FIAP | prof@fiap.com.br |

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 🏫 Informações Acadêmicas

- **Instituição**: FIAP (Faculdade de Informática e Administração Paulista)
- **Curso**: Análise e Desenvolvimento de Sistemas
- **Disciplina**: CAP6 - Capstone Project
- **Período**: 2025.1 (Fase 2)
- **Semestre**: 09-10/2025

---

## 📞 Suporte

### 🐛 Relatório de Bugs
- Abra uma [Issue no GitHub](https://github.com/dortad/FIAP_202510_CAP6/issues)
- Inclua detalhes do erro e steps para reproduzir

### 💬 Discussões
- Use as [Discussions do GitHub](https://github.com/dortad/FIAP_202510_CAP6/discussions)
- Perguntas, sugestões e feedback são bem-vindos

### 📧 Contato Direto
- Email institucional: **seu.email@fiap.com.br**
- LinkedIn: **[Seu Nome](https://linkedin.com/in/seu-perfil)**

---

<div align="center">

### 🌟 **Desenvolvido com ❤️ na FIAP** 🌟

**"Transformando conhecimento em soluções práticas para o agronegócio"**

---

![FIAP Logo](https://img.shields.io/badge/FIAP-2025-blueviolet.svg?style=for-the-badge)

</div>