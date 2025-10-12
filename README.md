# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Calculadora de Cana-de-Açúcar

## CAP6 - Fase 2 (2025)

## 👨‍🎓 Integrante:

- `<a href="https://www.linkedin.com/in/seu-perfil">`Seu Nome Completo`</a>`

## 👩‍🏫 Professor:

### Coordenador

- `<a href="https://www.linkedin.com/company/fiap">`Prof. FIAP`</a>`

![Python](https://img.shields.io/badge/Python-3.14.0-blue.svg)
![Oracle](https://img.shields.io/badge/Oracle-Database-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![FIAP](https://img.shields.io/badge/FIAP-CAP6_2025-purple.svg)

## � Descrição

A **Calculadora de Cana-de-Açúcar** é um sistema especializado desenvolvido para o **CAP6 - Fase 2 (2025)** da FIAP, focado em auxiliar produtores e técnicos agrícolas no planejamento e dimensionamento preciso do plantio de cana-de-açúcar.

O sistema utiliza **algoritmos agronômicos avançados** para calcular a quantidade exata de material vegetal (toletes/mudas) necessária para plantar uma área específica, considerando múltiplas variáveis como variedades de cana, épocas de plantio, métodos de cultivo e condições do campo.

Desenvolvido com integração **Oracle Database** e interface em Python, o programa oferece cálculos precisos baseados em parâmetros técnicos de instituições renomadas como RIDESA, CTC, IAC e Embrapa, garantindo confiabilidade e precisão nos resultados.

### 🎯 Objetivo Principal

**Calcular a massa total de toletes (em toneladas) necessária para plantar uma área específica**, proporcionando:

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

| Tecnologia                | Versão | Função                     |
| ------------------------- | ------- | ---------------------------- |
| **Python**          | 3.14.0  | Linguagem principal          |
| **Oracle Database** | -       | Armazenamento de parâmetros |
| **pandas**          | ≥2.2.0 | Manipulação de dados       |
| **oracledb**        | ≥2.3.0 | Conectividade Oracle         |

## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- **assets**: aqui estão os arquivos relacionados a elementos não-estruturados deste repositório, como imagens e logos.
- **document**: aqui estão todos os documentos do projeto que as atividades poderão pedir. Na subpasta "other", foram adicionados documentos complementares e arquivos de exemplo.
- **src**: Todo o código fonte criado para o desenvolvimento do projeto ao longo das fases do CAP6.
- **README.md**: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

```
FIAP_202510_CAP6/
│
├── � assets/                              # Recursos gráficos e imagens
│   ├── logo-fiap.png                      # Logo oficial da FIAP
│   └── README.md                          # Documentação dos assets
│
├── 📁 document/                           # Documentação do projeto
│   ├── documentacao.md                    # Documentação técnica completa
│   ├── INDICE_DOCUMENTACAO.md             # Índice de navegação
│   └── 📁 other/                          # Documentos complementares
│       ├── fontes_info.md                 # Referências das variedades
│       └── Calculadora_Cana_resultados.txt # Exemplo de saída
│
├── 📁 src/                               # Código fonte auxiliar
│   ├── funcoes_calculadora.py            # Funções de cálculo
│   ├── rotinas_V2.py                     # Integração Oracle
│   ├── parametros.json                   # Parâmetros técnicos
│   ├── requirements.txt                  # Dependências Python
│   └── README.md                         # Documentação do código
│
├── calculadora_cana_principal.py         # 🚀 PROGRAMA PRINCIPAL
│
├── 📁 template-main/                     # Template FIAP original
├── 📁 venv_Cap6/                        # Ambiente virtual Python
└── � README.md                         # Este arquivo
```

---

## 🔧 Como executar o código

### Pré-requisitos

- **Python 3.10+** instalado no sistema
- **Oracle Database** (opcional - sistema possui fallback)
- **Git** para clone do repositório

### Instalação e Execução

#### 1️⃣ Clone e Navegação

```bash
git clone https://github.com/dortad/FIAP_202510_CAP6.git
cd FIAP_202510_CAP6
```

#### 2️⃣ Ambiente Virtual (Recomendado)

```bash
# Criar ambiente virtual
python -m venv venv_Cap6

# Ativar ambiente virtual
# Windows:
venv_Cap6\Scripts\activate
# Linux/Mac:
source venv_Cap6/bin/activate
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
python calculadora_cana_principal.py
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

| Termo                  | Definição                                      |
| ---------------------- | ------------------------------------------------ |
| **Tolete**       | Pedaço do colmo cortado para plantio (30-50 cm) |
| **Gema**         | Broto que origina nova planta                    |
| **Espaçamento** | Distância entre fileiras de plantio             |
| **Densidade**    | Quantidade de material por área                 |

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

| Status                | Descrição                 | Tolerância                 |
| --------------------- | --------------------------- | --------------------------- |
| 🟢**OK**        | Dentro das especificações | ≤ 5% (Seca), ≤ 8% (Chuva) |
| 🟡**ATENÇÃO** | Fora das tolerâncias       | > tolerância definida      |

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
python calculadora_cana_principal.py

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

- � **[documentacao.md](documentacao.md)**: Documentação técnica completa com mapeamento de funções
- 🀽� **[O_que_faz_o_programa.md](O_que_faz_o_programa.md)**: Explicação detalhada das funcionalidades
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

## � Histórico de lançamentos

* 2.0.0 - 12/10/2025

  * Versão simplificada (somente relatórios TXT)
  * Remoção de funcionalidades de fallback JSON
  * Estruturação seguindo template FIAP
  * Documentação técnica completa
* 1.1.0 - 10/10/2025

  * Adição de múltiplos formatos de saída (TXT, Excel, PDF)
  * Sistema de fallback JSON implementado
  * Comentários e documentação das funções
* 1.0.0 - 08/10/2025

  * Versão inicial do sistema
  * Cálculos básicos de material vegetal
  * Integração com Oracle Database
  * Interface de menu interativa

---

## 👥 Equipe

| Papel                             | Nome       | Contato               |
| --------------------------------- | ---------- | --------------------- |
| **Desenvolvedor Principal** | Seu Nome   | seu.email@fiap.com.br |
| **Orientador Acadêmico**   | Prof. FIAP | prof@fiap.com.br      |

---

## � Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/dortad/FIAP_202510_CAP6">Calculadora de Cana-de-Açúcar</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">FIAP</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>

---

**🎓 Desenvolvido para FIAP - CAP6 Fase 2 (2025)**
