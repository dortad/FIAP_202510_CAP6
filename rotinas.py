# Importação dos módulos
import os
import oracledb
import pandas as pd
from datetime import datetime
import json
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
            'l_to_rec': float(param_json['l_to_rec']),  # Nota: JSON usa 'L_to_rec' (maiúsculo)
            'rho_rec': float(param_json['rho_rec']),
            'd_rec_kg_m': float(param_json['d_rec_kg_m'])
        }
        
        return dados_oracle
        
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
            cursor.execute("""
                SELECT variedade, epoca, processo, e_rec_m, g_final_rec 
                FROM parametros 
                WHERE ROWNUM <= 5
                ORDER BY variedade, epoca, processo
            """)
            
            resultados = cursor.fetchall()
            print(f"\n Primeiros 5 registros inseridos:")
            print("-" * 70)
            print("Variedade  | Época     | Processo  | E_rec_m | G_final")
            print("-" * 70)
            
            for row in resultados:
                print(f"{row[0]:<10} | {row[1]:<9} | {row[2]:<9} | {row[3]:7.2f} | {row[4]:7d}")
        
        cursor.close()
        
    except Exception as e:
        print(f" Erro ao verificar dados: {e}")

# ========== FUNÇÃO PARA INSERIR DADOS NO ORACLE ==========
def inserir_dados_oracle(conn, dicionario_parametros):
    """Insere todos os dados do dicionário na tabela Oracle"""
    
    print(f"\n💾 Iniciando inserção de {len(dicionario_parametros)} registros...")
    
    cursor = conn.cursor()
    registros_inseridos = 0
    registros_com_erro = 0
    registros_duplicados = 0
    
    # SQL de inserção
    sql_insert = """
        INSERT INTO parametros (
            variedade, epoca, processo, e_rec_m, g_final_rec, 
            s_rec, g_to_rec, l_to_rec, rho_rec, d_rec_kg_m
        ) VALUES (
            :variedade, :epoca, :processo, :e_rec_m, :g_final_rec,
            :s_rec, :g_to_rec, :l_to_rec, :rho_rec, :d_rec_kg_m
        )
    """
    
    print("\n Progresso da inserção:")
    print("-" * 50)
    
    for i, (chave, param_json) in enumerate(dicionario_parametros.items(), 1):
        try:
            # Mapeia os dados do JSON para o formato Oracle
            dados_oracle = mapear_dados_para_oracle(param_json)
            
            if dados_oracle is None:
                print(f" Registro {i:3d}: Erro no mapeamento - {chave}")
                registros_com_erro += 1
                continue
                
            # Executa a inserção
            cursor.execute(sql_insert, dados_oracle)
            
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
    print(f"  Registros duplicados (ignorados): {registros_duplicados}")
    print(f" Registros com erro: {registros_com_erro}")
    
    if registros_inseridos > 0:
        percentual = (registros_inseridos / len(dicionario_parametros)) * 100
        print(f" Taxa de sucesso: {percentual:.1f}%")
    
    cursor.close()
    return registros_inseridos

# ========== FUNÇÃO PARA CONECTAR AO ORACLE ==========
def conectar_oracle():
    """Estabelece conexão com o banco Oracle"""
    print("\n Conectando ao Oracle Database...")
    
    try:
        # Configurações de conexão (mesmas do manutencao_oracle_paramentros.py)
        conn = oracledb.connect(
            user='RM567007', 
            password='Fiap#2025', 
            dsn='oracle.fiap.com.br:1521/ORCL'
        )
        
        print(" Conexão com Oracle estabelecida com sucesso!")
        return conn
        
    except Exception as e:
        print(f" Erro ao conectar com Oracle: {e}")
        print(" Verifique suas credenciais e conectividade de rede")
        return None

# ========== FUNÇÃO PARA CARREGAR DADOS JSON COMO DICIONÁRIO ==========






