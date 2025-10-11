# Importação dos módulos
import os
import oracledb
import pandas as pd
from datetime import datetime
import json
from rotinas import *


def carregar_parametros_no_oracle(dict_parametros: dict):
    # 1. Carregar dados do JSON como dicionário
    
    if not dict_parametros:
        print("Não foi possível carregar os dados. Encerrando...")
        return False

    # 2. Conectar ao Oracle
    conn = conectar_oracle()

    if not conn:
        print(" Não foi possível conectar ao Oracle. Encerrando...")
        return False
    # Inserir novos dados (ignora duplicados)
    registros_inseridos = inserir_dados_oracle(conn, dict_parametros)

    if registros_inseridos > 0:
        verificar_dados_inseridos(conn)
    else:
        print(f"\n Nenhum registro novo foi inserido")
        print(" Todos os registros já existem na tabela")




print("\n" )

dict_parametros = {}
dict_parametros = carregar_parametros_Json_como_dicionario()
carregar_parametros_no_oracle(dict_parametros)

print("\n" )