# Importação dos módulos
import os
import oracledb
import pandas as pd
from datetime import datetime
import json
from rotinas import *


def carregar_parametros_Json_como_dicionario():
    """
    Carrega os parâmetros do arquivo JSON e converte para dicionário
    Chave: combinação de Variedade_Epoca_Processo
    Valor: dicionário com todos os dados do parâmetro
    """
    #print(" Lendo arquivo parametros.json...")
    
    try:
        arquivo_json = "parametros.json"
        
        # Carregando o arquivo JSON para uma lista.
        with open(arquivo_json, "r", encoding='utf-8') as file:
            lista_original = json.load(file)

        # Convertendo lista em dicionário
        dicionario_parametros = {}
        registros_duplicados = 0
        
        for i, param in enumerate(lista_original):
            # Criando chave única combinando Variedade, Epoca e Processo
            chave = f"{param['Variedade']}_{param['Epoca']}_{param['Processo']}"
            
            # Se a chave já existe, adiciona um número para torná-la única
            chave_original = chave
            contador = 1
            while chave in dicionario_parametros:
                chave = f"{chave_original}_{contador}"
                contador += 1
                registros_duplicados += 1
            
            # Adiciona o parâmetro no dicionário
            dicionario_parametros[chave] = param

        if registros_duplicados > 0:
            print(f"  Registros com chaves duplicadas encontrados: {registros_duplicados}")
            
        return dicionario_parametros
        
    except FileNotFoundError:
        print(" Arquivo parametros.json não encontrado!")
        print(" Verifique se o arquivo existe no diretório pai")
        return {}
    except json.JSONDecodeError as e:
        print(f" Erro ao decodificar JSON: {e}")
        return {}
    except Exception as e:
        print(f" Erro inesperado ao carregar JSON: {e}")
        return {}

def carregar_parametros_no_oracle(dict_parametros: dict):
    # 1. Carregar dados do JSON como dicionário
    

    dict_parametros.clear()
    dict_parametros = carregar_parametros_Json_como_dicionario()

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
        #print(f"\nProcesso concluído com sucesso!")
        #print(f" {registros_inseridos} registros carregados na tabela Oracle")
    else:
        print(f"\n Nenhum registro novo foi inserido")
        print(" Todos os registros já existem na tabela")

print("\n" )

dict_parametros = {}

carregar_parametros_no_oracle(dict_parametros)

print("\n" )