#20251011
# Importação dos módulos
import os
import oracledb
import pandas as pd
from datetime import datetime
import json
from rotinas import *





       
print("\n" )

dict_parametros = {}
dict_parametros = carregar_parametros_Json_como_dicionario()

# Conectar ao Oracle
conn = conectar_oracle('teste')

if not conn:
    print(" Não foi possível conectar ao Oracle. Encerrando...")
    exit()

# Inserir novos dados (ignora duplicados)
carregar_parametros_no_oracle(dict_parametros, conn)

# desconectar do Oracle
desconectar_oracle(conn)

print("\n" )