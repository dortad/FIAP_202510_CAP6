# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Calculadora de Cana-de-Açúcar

## CAP6 - Fase 2 (2025)

## 👨‍🎓 Integrantes:

- Durval de Oliveira Dorta Junior RM567007
- Murilo Ferreira Borges  RM567738

## 👩‍🏫 Professores:

### Tutor(a)

- Ana Cristina dos Santos

### Coordenador(a)

- André Godoi Chiovato

## 📜 Descrição

Este projeto implementa uma **Calculadora de Produtividade de Cana-de-Açúcar** desenvolvida como parte das atividades acadêmicas da FIAP. O sistema permite calcular estimativas de produção agrícola com base em parâmetros técnicos e dados históricos.

### Funcionalidades Principais:

- Cálculo de produtividade estimada por hectare
- Análise de dados históricos de produção
- Integração com banco de dados Oracle para armazenamento
- Interface de linha de comando intuitiva
- Sistema de configuração flexível via JSON

### Objetivo Acadêmico:

O projeto visa aplicar conceitos de programação Python, integração com bancos de dados Oracle, e boas práticas de desenvolvimento de software no contexto do agronegócio brasileiro, especificamente no setor sucroenergético.

## 📁 Estrutura de pastas

```
.
├── assets/
├── document/
└── src/
    ├── app.py
    ├── funcoes_calculadora.py
    ├── rotinas_V2.py
    └── parametros.json
```

Descrição das pastas e arquivos principais:

- **assets**: Arquivos relacionados a elementos não-estruturados como imagens e recursos visuais
- **document**: Documentos do projeto e atividades acadêmicas
- **src**: Código fonte modularizado do projeto
  - `app.py`: **Programa principal** (executar este arquivo)
  - `funcoes_calculadora.py`: Funções principais de cálculo
  - `rotinas_V2.py`: Integração com Oracle Database
  - `parametros.json`: Configurações e parâmetros do sistema

## 🔧 Como executar o código

### Pré-requisitos

- Python 3.10 ou superior
- Oracle Database (opcional - sistema funciona sem banco)
- IDE de sua preferência (VS Code recomendado)

### Bibliotecas necessárias

```bash
pip install cx-Oracle
```

### Instalação e execução

1. **Clone o repositório:**

   ```bash
   git clone <url-do-repositorio>
   cd FIAP_202510_CAP6
   ```
2. **Configure os parâmetros (opcional):**

   - Edite o arquivo `src/parametros.json` com suas configurações
   - Para banco Oracle, configure as credenciais apropriadas
3. **Execute o programa principal:**

   ```bash
   python src/app.py
   ```

### Estrutura de execução

- O programa principal está em `src/app.py`
- Os módulos auxiliares estão em `src/`
- Configurações em `src/parametros.json`

## 🗃 Histórico de lançamentos

- 1.0.0 - 10/01/2025
  - Versão inicial da calculadora de cana-de-açúcar
  - Implementação da integração com Oracle Database
  - Sistema de configuração via JSON
  - Funções de cálculo de produtividade
  - Aplicação da estrutura FIAP template
  - Programa principal movido para raiz do projeto

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
