# FIAP_202510_CAP6 - Sistema CRUD PetShop

Projeto da disciplina CAP6 - Fase 2 2025

## Descrição

Sistema CRUD (Create, Read, Update, Delete) para gerenciamento de pets em um petshop, desenvolvido em Python com integração ao Oracle Database.

## Funcionalidades
- ✅ Cadastrar Pet
- ✅ Listar Pets
- ✅ Alterar Pet
- ✅ Excluir Pet
- ✅ Excluir Todos os Pets

## Pré-requisitos
- Python 3.8 ou superior
- Oracle Database (acesso ao servidor oracle.fiap.com.br)
- Credenciais de banco de dados válidas

## Instalação

### 1. Instalar Python
- **Windows**: Baixe de [python.org](https://www.python.org/downloads/) ou instale via Microsoft Store
- **Durante a instalação**: Marque "Add Python to PATH"

### 2. Clonar o repositório
```bash
git clone https://github.com/dortad/FIAP_202510_CAP6.git
cd FIAP_202510_CAP6
```

### 3. Criar ambiente virtual (recomendado)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 4. Instalar dependências
```bash
pip install -r requirements.txt
```

## Como executar
```bash
python main.py
```

## Estrutura do Banco de Dados
```sql
CREATE TABLE petshop (
    pet_id NUMBER GENERATED AS IDENTITY,
    tipo_pet VARCHAR2(10),
    nome_pet VARCHAR2(50),
    idade NUMBER(20,2),
    CONSTRAINT pk_petshop PRIMARY KEY (pet_id)
);
```

## Tecnologias utilizadas
- **Python 3.x** - Linguagem principal
- **oracledb** - Conexão com Oracle Database  
- **pandas** - Manipulação de dados
- **Oracle Database** - Sistema de gerenciamento de banco de dados

## Configuração do Banco
O sistema se conecta ao Oracle Database da FIAP:
- Servidor: `oracle.fiap.com.br:1521/ORCL`
- Usuário: RM567007
- **Nota**: As credenciais estão no código para fins acadêmicos

## Contribuidores
- Durval (@dortad)
- Murilo
