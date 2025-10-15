# Importação dos módulos
import os
from unittest import case
import oracledb
import pandas as pd
from datetime import datetime
import json


''' comando no oracle
DROP TABLE PARAMETROS;
  CREATE TABLE PARAMETROS 
   (	"VARIEDADE" VARCHAR2(10 BYTE), 
	"EPOCA" VARCHAR2(10 BYTE), 
	"PROCESSO" VARCHAR2(10 BYTE), 
	"E_REC_M" NUMBER(3,2), 
	"G_FINAL_REC" NUMBER, 
	"S_REC" NUMBER(3,2), 
	"G_TO_REC" NUMBER(3,2), 
	"L_TO_REC" NUMBER(3,2), 
	"RHO_REC" NUMBER(3,2), 
	"D_REC_KG_M" NUMBER(3,2), 
	 CONSTRAINT "PK_PARAMETROS" PRIMARY KEY ("VARIEDADE", "EPOCA", "PROCESSO"))
    
'''
# ========== FUNÇÃO PARA MAPEAR DADOS JSON → ORACLE ==========
def seletor_parametros_sql(sql_acao: str) -> str:
    match sql_acao.lower():
        case "i":
            # SQL de inserção
            sql_comando = """
                        INSERT INTO parametros (
                            variedade, epoca, processo, e_rec_m, g_final_rec, 
                            s_rec, g_to_rec, l_to_rec, rho_rec, d_rec_kg_m
                        ) VALUES (
                            :variedade, :epoca, :processo, :e_rec_m, :g_final_rec,
                            :s_rec, :g_to_rec, :l_to_rec, :rho_rec, :d_rec_kg_m
                        )
                        """
        case "a":
            # SQL de alteração
            sql_comando = """
                    UPDATE parametros SET
                        e_rec_m = :e_rec_m,
                            g_final_rec = :g_final_rec,
                            s_rec = :s_rec,
                            g_to_rec = :g_to_rec,
                            l_to_rec = :l_to_rec,
                            rho_rec = :rho_rec,
                            d_rec_kg_m = :d_rec_kg_m
                        WHERE
                            variedade = :variedade AND
                            epoca = :epoca AND
                            processo = :processo
                    """
        case "l":
            # SQL de leitura
            sql_comando = """
                SELECT * FROM parametros
                WHERE variedade = :variedade AND
                      epoca = :epoca AND
                      processo = :processo
            """
        case "v":
            # SQL de verificação (exibe alguns registros)
            sql_comando = """
                SELECT variedade, epoca, processo, e_rec_m, g_final_rec 
                FROM parametros 
                WHERE ROWNUM <= 5
                ORDER BY variedade, epoca, processo
            """
    return sql_comando
 

# ========== FUNÇÃO PARA MAPEAR DADOS JSON → ORACLE ==========
def mapear_dados_para_oracle(param_json):
    """
    Converte os dados do JSON para o formato esperado pela tabela Oracle
    

    """
    
    # Mapeamento direto dos campos (JSON tem capitalização diferente)
    try:
        dados_oracle = {
            'variedade': param_json['Variedade'][:10],  # Trunca para VARCHAR2(10)
            'epoca': param_json['Epoca'][:10],          # Trunca para VARCHAR2(10)  
            'processo': param_json['Processo'][:10],    # Trunca para VARCHAR2(10)
            'e_rec_m': float(param_json['e_rec_m']),
            'g_final_rec': int(param_json['g_final_rec']),
            's_rec': float(param_json['s_rec']),
            'g_to_rec': float(param_json['g_to_rec']),
            'l_to_rec': float(param_json['l_to_rec']), 
            'rho_rec': float(param_json['rho_rec']),
            'd_rec_kg_m': float(param_json['d_rec_kg_m'])
        }
        chave_oracle = {
            'variedade': dados_oracle['variedade'],
            'epoca': dados_oracle['epoca'],
            'processo': dados_oracle['processo']
        }
        
        return dados_oracle, chave_oracle
        
    except KeyError as e:
        print(f" Campo obrigatório não encontrado no JSON: {e}")
        return None
    except (ValueError, TypeError) as e:
        print(f" Erro na conversão de tipos: {e}")
        return None

# ========== FUNÇÃO PARA VERIFICAR DADOS INSERIDOS ==========
def verificar_dados_inseridos(conn):
    """Verifica e mostra alguns registros inseridos na tabela"""
    
    print(f"\n Verificando dados inseridos na tabela...")
    
    try:
        cursor = conn.cursor()
        
        # Conta total de registros
        cursor.execute("SELECT COUNT(*) FROM parametros")
        total = cursor.fetchone()[0]
        print(f" Total de registros na tabela: {total}")
        
        if total > 0:
            # Mostra os primeiros 5 registros
            # Executa a Leitura
            sql_comando = ""

            sql_comando = seletor_parametros_sql('v')     # ============ Seletor acao SQL ============ #

            cursor.execute(sql_comando)
            
            resultados = cursor.fetchall()
            print(f"\n Primeiros 5 registros de parametros no Oracle:")
            print("-" * 70)
            print("Variedade  | Época      | Processo          | E_rec_m | G_final")
            print("-" * 70)
            
            for row in resultados:
                print(f"{row[0]:<10} | {row[1]:<10} | {row[2]:<10}        | {row[3]:7.2f} | {row[4]:7d}")
        
        cursor.close()
        
    except Exception as e:
        print(f" Erro ao verificar dados: {e}")



# ========== FUNÇÃO PARA CONECTAR AO ORACLE ==========
def conectar_oracle(tipo: str = 'producao'):
    """
    *** FUNÇÃO DE CONEXÃO ORACLE ***
    Estabelece conexão com o banco Oracle Database (produção ou teste).
    
    Gerencia configurações de conexão para diferentes ambientes:
    - Produção: Servidor FIAP oficial
    - Teste: Configurações de desenvolvimento
    
    Args:
        tipo (str): Tipo de conexão ('producao' ou 'teste')
        
    Returns:
        oracledb.Connection: Objeto de conexão Oracle ou None se falhar
        
    Usado em:
        - calculadora_cana_principal.py: load_params_from_oracle_v2()
        - sincronizar_json_oracle()
        - Todas as operações que requerem acesso ao banco
        
    Configurações:
        - Produção: oracle.fiap.com.br:1521/ORCL
        - Teste: Configurações locais/desenvolvimento
    """
    print("\n Conectando ao Oracle Database...")

    if tipo.lower() == 'producao':
        user = 'RM567007'
        password = 'Fiap#2025'
        dsn = 'oracle.fiap.com.br:1521/ORCL'   
    elif tipo.lower() == 'teste':
        user = 'RM567007'
        password = 'RM567007'
        dsn = 'localhost:1521/xe'

    try:
        # Configurações de conexão 
        conn = oracledb.connect(
            user=user, 
            password=password, 
            dsn=dsn
        )
        
        print(" Conexão com Oracle estabelecida com sucesso!")
        return conn
        
    except Exception as e:
        print(f" Erro ao conectar com Oracle: {e}")
        print(" Verifique suas credenciais e conectividade de rede")
        return None
# 
# ========== FUNÇÃO PARA DESCONECTAR AO ORACLE ==========
def desconectar_oracle(conn):
    """Desconecta do banco Oracle"""
    if conn:
        try:
            conn.close()
            print(" Desconexão do Oracle estabelecida com sucesso!")
        except Exception as e:
            print(f" Erro ao desconectar do Oracle: {e}")


        

# ========== FUNÇÃO PARA CARREGAR DADOS JSON COMO DICIONÁRIO ==========
def carregar_parametros_Json_como_dicionario():
    """
    *** FUNÇÃO PARA CARREGAR JSON ***
    Carrega os parâmetros do arquivo JSON e converte para dicionário.
    
   
    Estrutura de retorno:
    - Chave: combinação "Variedade_Epoca_Processo" 
    - Valor: dicionário com todos os parâmetros técnicos
    
    Returns:
        dict: Dicionário com parâmetros ou None se erro
        
    Usado em:
        - load_params_from_oracle_v2() - Quando Oracle vazio
        - sincronizar_json_oracle() - Para sincronização
        - Inicialização do sistema
        
    Arquivo lido: parametros.json (338 registros de variedades)
    """
    #print(" Lendo arquivo parametros.json...")

    try:
        # Buscar o arquivo parametros.json na mesma pasta do script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        arquivo_json = os.path.join(script_dir, "parametros.json")
        
        # Carregando o arquivo JSON para uma lista.
        with open(arquivo_json, "r", encoding='utf-8') as file:
            lista_original = json.load(file)

        # Convertendo lista em dicionário
        dicionario_parametros = {}
        registros_duplicados = 0
        
        for i, param in enumerate(lista_original):
            # Criando chave única combinando Variedade, Epoca e Processo
            chave = f"{param['Variedade']}_{param['Epoca']}_{param['Processo']}"
            
            # Se a chave já existe, registra a ocorrencia da duplicação no contador registros_duplicados
            chave_original = chave
            contador = 1
            while chave in dicionario_parametros:
                #chave = f"{chave_original}_{contador}"
                #contador += 1
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







# ========== FUNÇÃO PARA INSERIR DADOS NO ORACLE ==========

def manutencao_dados_oracle(conn, dicionario_parametros):
    """Insere/altera/lê os dados do dicionário na tabela Oracle"""
    
    #print(f"\n Iniciando inserção de {len(dicionario_parametros)} registros...")
    
    cursor = conn.cursor()
    registros_inseridos = 0
    registros_com_erro = 0
    registros_atualizados = 0
    registros_duplicados = 0
    


    for i, (chave, param_json) in enumerate(dicionario_parametros.items(), 1):
        try:
            # Mapeia os dados do JSON para o formato da tabela do Oracle
            dados_oracle, chave_oracle = mapear_dados_para_oracle(param_json)
            
            if dados_oracle is None:
                print(f" Registro {i:3d}: Erro no mapeamento - {chave}")
                registros_com_erro += 1
                continue
                
            # Executa a Leitura
            sql_comando = seletor_parametros_sql('l')     # ============ Seletor acao leitura SQL ============ #

            cursor.execute(sql_comando, chave_oracle)

            # Consulta realizada para verificação de existência do registro

            resultado = cursor.fetchone()

            if resultado is None:
                # Executa a Inserção
                sql_comando = seletor_parametros_sql('i')    # ============ Seletor acao inserçãoSQL ============ #
                cursor.execute(sql_comando, dados_oracle)
                #print(f"  Registro {i:3d}: Inserido com sucesso - {chave}")
            else:
                # Executa a Alteração
                sql_comando = seletor_parametros_sql('a')     # ============ Seletor acao alteração SQL ============ #
                #print(f"  Registro {i:3d}: Já existe - Atualizando - {chave}")
                cursor.execute(sql_comando, dados_oracle)
                # Registro Já existe na tabela foi atualizado
                registros_atualizados += 1
                continue

                       
            # Mostra progresso a cada 5 registros
            if i % 5 == 0 or i == len(dicionario_parametros):
                print(f" Registro {i:3d}: {dados_oracle['variedade']}-{dados_oracle['epoca']}-{dados_oracle['processo']}")
            
            registros_inseridos += 1
            
        except oracledb.IntegrityError as e:
            # Violação de chave primária (registro duplicado)
            if "unique constraint" in str(e).lower() or "pk_parametros" in str(e):
                print(f"  Registro {i:3d}: Duplicado ignorado - {chave}")
                registros_duplicados += 1
            else:
                print(f" Registro {i:3d}: Erro de integridade - {e}")
                registros_com_erro += 1
                
        except Exception as e:
            print(f" Registro {i:3d}: Erro inesperado - {e}")
            registros_com_erro += 1
    
    # Confirma as alterações
    try:
        conn.commit()
        print(f"\n Transação confirmada (COMMIT realizado)")
    except Exception as e:
        print(f" Erro no COMMIT: {e}")
        conn.rollback()
        print("↶ ROLLBACK executado")
    
    # Relatório final
    print("\n" + "=" * 50)
    print(" RELATÓRIO FINAL DA CARGA")
    print("=" * 50)
    print(f" Total de registros processados: {len(dicionario_parametros)}")
    print(f" Registros inseridos com sucesso: {registros_inseridos}")
    print(f" Registros alterados (atualizados): {registros_atualizados}")
    print(f" Registros com erro: {registros_com_erro}")
    
    if registros_inseridos > 0:
        percentual = (registros_inseridos / len(dicionario_parametros)) * 100
        print(f" Taxa de sucesso: {percentual:.1f}%")
    
    cursor.close()
    return registros_inseridos, registros_atualizados, registros_com_erro, registros_duplicados

# ========== FUNÇÃO PARA CARREGAR PARAMETROS NO ORACLE ==========
def carregar_parametros_no_oracle(dict_parametros: dict, conn):
    # 1. Carregar dados do JSON como dicionário
    
    if not dict_parametros:
        print("Não foi possível carregar os dados. Encerrando...")
        return False


    registros_inseridos, registros_atualizados, registros_com_erro, registros_duplicados = manutencao_dados_oracle(conn, dict_parametros)

    if registros_inseridos > 0 or registros_atualizados > 0:
        verificar_dados_inseridos(conn)
        print(f"\nProcesso concluído com sucesso!")
        return True
