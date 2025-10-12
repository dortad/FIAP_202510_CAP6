# 🌾 Calculadora de Cana-de-Açúcar

**Sistema especializado para cálculo de material vegetal (toletes/mudas) necessário para plantio de cana-de-açúcar**

![Python](https://img.shields.io/badge/Python-3.14.0-blue.svg)
![Oracle](https://img.shields.io/badge/Oracle-Database-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![FIAP](https://img.shields.io/badge/FIAP-CAP6_2025-purple.svg)

---

## 📋 Visão Geral

A **Calculadora de Cana-de-Açúcar** é um sistema desenvolvido para auxiliar no **planejamento e dimensionamento do plantio** de cana-de-açúcar. O programa calcula a quantidade exata de material vegetal (toletes/mudas) necessária para plantar uma área específica, considerando diferentes variedades, épocas de plantio e métodos de cultivo.

### 🎯 Objetivo Principal

**Calcular a massa total de toletes (em toneladas) necessária para plantar uma área específica**, garantindo:
- ✅ Otimização do uso de material vegetal
- ✅ Redução de desperdícios
- ✅ Controle de qualidade do plantio
- ✅ Planejamento logístico eficiente

---

## 🚀 Funcionalidades

### 📊 Cálculos Técnicos
- **Densidade de plantio** (toletes por hectare)
- **Massa de material vegetal** necessária
- **Controle de qualidade** com sistema semáforo
- **Análise de produtividade** por linha de plantio
- **Consideração de perdas** por manobras e tráfego

### 📈 Relatórios Completos
- **Relatório TXT**: Detalhado com explicações técnicas e análise completa

### 🔗 Integração Oracle
- Conexão com banco de dados Oracle
- Gerenciamento de parâmetros técnicos
- Consulta automática de especificações por variedade

### ⚡ Interface Amigável
- Menu interativo no terminal
- Validação de entrada de dados
- Mensagens de status claras
- Suporte a múltiplas execuções

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Função |
|------------|--------|--------|
| **Python** | 3.14.0 | Linguagem principal |
| **Oracle Database** | - | Armazenamento de parâmetros |
| **pandas** | ≥2.2.0 | Manipulação de dados |
| **oracledb** | ≥2.3.0 | Conectividade Oracle |

---

## 📁 Estrutura do Projeto

```
FIAP_202510_CAP6/
│
├── 📄 calculadora_cana_principal_v1.1.py    # Programa principal
├── 📄 funcoes_calculadora.py                # Funções de cálculo e relatórios
├── 📄 rotinas_V2.py                         # Conexão Oracle e utilitários
├── 📄 parametros.json                       # Parâmetros técnicos (fallback)
├── 📄 requirements.txt                      # Dependências do projeto
│
├── 📁 venv_Cap6/                           # Ambiente virtual Python
├── 📁 __pycache__/                         # Cache Python
│
└── 📊 Resultados de exemplo:
    └── Calculadora_Cana_v1_1_resultados.txt
```

---

## 🔧 Instalação e Configuração

### 1️⃣ Pré-requisitos

- **Python 3.14.0** ou superior
- **Oracle Database** configurado e acessível
- **Git** para clone do repositório

### 2️⃣ Clone do Repositório

```bash
git clone https://github.com/dortad/FIAP_202510_CAP6.git
cd FIAP_202510_CAP6
```

### 3️⃣ Ambiente Virtual

```bash
# Windows
python -m venv venv_Cap6
venv_Cap6\Scripts\activate

# Linux/Mac
python -m venv venv_Cap6
source venv_Cap6/bin/activate
```

### 4️⃣ Instalação de Dependências

```bash
# Instalação completa
pip install -r requirements.txt

# Ou instalação manual
pip install oracledb pandas
```

### 5️⃣ Configuração do Oracle

Edite o arquivo `rotinas_V2.py` para configurar a conexão Oracle:

```python
# Configurações de conexão
DB_CONFIG = {
    'host': 'seu-servidor-oracle',
    'port': 1521,
    'service': 'seu-servico',
    'user': 'seu-usuario',
    'password': 'sua-senha'
}
```

---

## 🎮 Como Usar

### Execução Básica

```bash
python calculadora_cana_principal_v1.1.py
```

### Menu Principal

```
🌾 === CALCULADORA DE CANA-DE-AÇÚCAR v2 ===

1. 📊 Executar cálculo completo
2. 🔧 Configurar conexão Oracle  
3. 📋 Listar parâmetros disponíveis
4. ❓ Ajuda e documentação
5. 🚪 Sair

Escolha uma opção: 
```

### Exemplo de Uso

```
=== DADOS DE ENTRADA ===
Área total (hectares): 100.5
Variedade: RB867515
Época: Chuva
Processo: Mecanizado
Perdas por manobras (%): 3
Perdas por tráfego (%): 1

=== RESULTADOS ===
✅ Massa total necessária: 67.8 toneladas
✅ Status: OK (desvio: 2.1%)
📊 Relatório gerado em formato texto
```

---

## 📊 Conceitos Técnicos

### 🌱 Fundamentos da Cana

| Termo | Definição |
|-------|-----------|
| **Tolete** | Pedaço do colmo cortado para plantio (30-50 cm) |
| **Gema** | Broto que origina nova planta |
| **Espaçamento** | Distância entre fileiras de plantio |
| **Densidade** | Quantidade de material por área |

### ⚙️ Tipos de Plantio

- **Manual**: Toletes longos colocados manualmente no sulco
- **Mecanizado**: Toletes menores (billets) distribuídos por máquinas

### 📈 Fórmulas de Cálculo

```
Metros de fileira/ha = 10.000 ÷ Espaçamento
Toletes/metro = Gemas_finais ÷ (Gemas_úteis ÷ Tolete)
Massa/ha = Toletes/ha × Comprimento × Densidade ÷ 1000
Massa_total = Massa/ha × Área_efetiva
```

---

## 🎯 Sistema de Status (Semáforo)

| Status | Descrição | Tolerância |
|--------|-----------|------------|
| 🟢 **OK** | Dentro das especificações | ≤ 5% (Seca), ≤ 8% (Chuva) |
| 🟡 **ATENÇÃO** | Fora das tolerâncias | > tolerância definida |

---

## 📝 Exemplo de Saída

### Relatório Resumido (TXT)
```
🌾 CALCULADORA DE CANA-DE-AÇÚCAR - RESULTADOS

📊 RESUMO EXECUTIVO
Área Total: 100.5 ha
Variedade: RB867515
Época: Chuva  
Processo: Mecanizado
Massa Total: 67.8 toneladas
Status: ✅ OK (desvio: 2.1%)

📈 PRODUTIVIDADE POR LINHA
- Linha 1: 6.67 m/ha • 1.60 kg/m • Massa: 10.8 t
- Produtividade média: 674.6 kg/ha

📋 EXPLICAÇÃO DO STATUS/SEMÁFORO DE QUALIDADE
O status indica se o cálculo está dentro das tolerâncias técnicas:
🟢 OK: Desvio ≤ 5% (época seca) ou ≤ 8% (época chuva)
🟡 ATENÇÃO: Desvio > tolerância - revisar parâmetros
```

---

## 🧪 Testes e Validação

### Execução de Testes
```bash
# Teste com dados de exemplo
python calculadora_cana_principal_v1.1.py

# Validação com parâmetros conhecidos
python -m pytest tests/ -v
```

### Casos de Teste Incluídos
- ✅ Validação de fórmulas de cálculo
- ✅ Teste de conexão Oracle
- ✅ Geração de relatórios
- ✅ Validação de tolerâncias
- ✅ Teste de diferentes variedades

---

## 🤝 Contribuição

### Como Contribuir
1. **Fork** o repositório
2. Crie uma **branch** para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. **Commit** suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. **Push** para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um **Pull Request**

### Diretrizes
- Siga o padrão de código existente
- Adicione documentação para novas funcionalidades
- Inclua testes para novas features
- Mantenha compatibilidade com versões existentes

---

## 📚 Documentação Adicional

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