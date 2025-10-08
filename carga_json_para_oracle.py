# CARREGAMENTO DE DADOS JSON PARA TABELA ORACLE - VERSÃO DICIONÁRIO
# Este programa lê dados do arquivo parametros.json (estrutura de dicionário)
# e os carrega diretamente na tabela Oracle 'parametros'

import json
import os
import oracledb
from datetime import datetime

print("=" * 80)
print("🚀 SISTEMA DE CARGA: JSON → ORACLE DATABASE")
print("Carregando dados do dicionário JSON na tabela Oracle")
print("=" * 80)

# ========== FUNÇÃO DE MENU ==========
def exibir_menu():
    """Exibe o menu de opções para o usuário"""
    print("\n📋 OPÇÕES DE EXECUÇÃO:")
    print("1. 📥 Inserir novos dados (ignora duplicados)")
    print("2. 🔄 Limpar tabela e inserir todos os dados")
    print("3. 📊 Apenas verificar dados existentes")
    print("4. 🚪 Sair")
    
    while True:
        try:
            escolha = input("\n🎯 Escolha uma opção (1-4): ").strip()
            if escolha in ['1', '2', '3', '4']:
                return int(escolha)
            else:
                print("❌ Opção inválida! Digite 1, 2, 3 ou 4.")
        except KeyboardInterrupt:
            print("\n\n👋 Programa interrompido pelo usuário")
            return 4

# ========== CONFIGURAÇÕES DO ORACLE ==========
# Estrutura da tabela Oracle (mesma do manutencao_oracle_paramentros.py):
'''
create table parametros
(   variedade varchar2(10),
    epoca varchar2(10),
    processo varchar2(10), 
    e_rec_m number(3,2),
    g_final_rec number,
    s_rec number(3,2),
    g_to_rec number(3,2),
    l_to_rec number(3,2),
    rho_rec number(3,2),
    d_rec_kg_m number(3,2),
    CONSTRAINT pk_parametros PRIMARY KEY (variedade, epoca, processo)
);
'''

# ========== FUNÇÃO PARA CARREGAR DADOS JSON COMO DICIONÁRIO ==========
def carregar_parametros_como_dicionario():
    """
    Carrega os parâmetros do arquivo JSON e converte para dicionário
    Chave: combinação de Variedade_Epoca_Processo
    Valor: dicionário com todos os dados do parâmetro
    """
    print("📋 Lendo arquivo parametros.json...")
    
    try:
        arquivo_json = "parametros.json"
        
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
            
        print(f"✅ Arquivo JSON carregado com sucesso!")
        print(f"📊 Total de registros: {len(dicionario_parametros)}")
        if registros_duplicados > 0:
            print(f"⚠️  Registros com chaves duplicadas encontrados: {registros_duplicados}")
            
        return dicionario_parametros
        
    except FileNotFoundError:
        print("❌ Arquivo parametros.json não encontrado!")
        print("💡 Verifique se o arquivo existe no diretório pai")
        return {}
    except json.JSONDecodeError as e:
        print(f"❌ Erro ao decodificar JSON: {e}")
        return {}
    except Exception as e:
        print(f"❌ Erro inesperado ao carregar JSON: {e}")
        return {}

# ========== FUNÇÃO PARA CONECTAR AO ORACLE ==========
def conectar_oracle():
    """Estabelece conexão com o banco Oracle"""
    print("\n🔗 Conectando ao Oracle Database...")
    
    try:
        # Configurações de conexão (mesmas do manutencao_oracle_paramentros.py)
        conn = oracledb.connect(
            user='RM567007', 
            password='Fiap#2025', 
            dsn='oracle.fiap.com.br:1521/ORCL'
        )
        
        print("✅ Conexão com Oracle estabelecida com sucesso!")
        return conn
        
    except Exception as e:
        print(f"❌ Erro ao conectar com Oracle: {e}")
        print("💡 Verifique suas credenciais e conectividade de rede")
        return None

# ========== FUNÇÃO PARA LIMPAR TABELA ==========
def limpar_tabela(conn):
    """Remove todos os registros da tabela parametros"""
    print("\n🗑️ Limpando tabela 'parametros'...")
    
    try:
        cursor = conn.cursor()
        
        # Conta registros antes de limpar
        cursor.execute("SELECT COUNT(*) FROM parametros")
        total_antes = cursor.fetchone()[0]
        
        if total_antes == 0:
            print("ℹ️ Tabela já está vazia")
            cursor.close()
            return True
            
        # Confirma a limpeza
        print(f"⚠️ Foram encontrados {total_antes} registros na tabela")
        confirma = input("🔥 Tem certeza que deseja EXCLUIR TODOS os dados? (S/N): ").strip().upper()
        
        if confirma != 'S':
            print("❌ Operação cancelada pelo usuário")
            cursor.close()
            return False
            
        # Executa a limpeza
        cursor.execute("DELETE FROM parametros")
        conn.commit()
        
        print(f"✅ Tabela limpa com sucesso! {total_antes} registros removidos")
        cursor.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao limpar tabela: {e}")
        try:
            conn.rollback()
        except:
            pass
        return False

# ========== FUNÇÃO PARA MAPEAR DADOS JSON → ORACLE ==========
def mapear_dados_para_oracle(param_json):
    """
    Converte os dados do JSON para o formato esperado pela tabela Oracle
    
    Mapeamento de campos:
    JSON → Oracle
    Variedade → variedade
    Epoca → epoca  
    Processo → processo
    E_rec_m → e_rec_m
    G_final_rec → g_final_rec
    s_rec → s_rec
    g_to_rec → g_to_rec
    L_to_rec → l_to_rec
    rho_rec → rho_rec
    d_rec_kg_m → d_rec_kg_m
    """
    
    # Mapeamento direto dos campos (JSON tem capitalização diferente)
    try:
        dados_oracle = {
            'variedade': param_json['Variedade'][:10],  # Trunca para VARCHAR2(10)
            'epoca': param_json['Epoca'][:10],          # Trunca para VARCHAR2(10)  
            'processo': param_json['Processo'][:10],    # Trunca para VARCHAR2(10)
            'e_rec_m': float(param_json['E_rec_m']),
            'g_final_rec': int(param_json['G_final_rec']),
            's_rec': float(param_json['s_rec']),
            'g_to_rec': float(param_json['g_to_rec']),
            'l_to_rec': float(param_json['L_to_rec']),  # Nota: JSON usa 'L_to_rec' (maiúsculo)
            'rho_rec': float(param_json['rho_rec']),
            'd_rec_kg_m': float(param_json['d_rec_kg_m'])
        }
        
        return dados_oracle
        
    except KeyError as e:
        print(f"❌ Campo obrigatório não encontrado no JSON: {e}")
        return None
    except (ValueError, TypeError) as e:
        print(f"❌ Erro na conversão de tipos: {e}")
        return None

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
    
    print("\n📊 Progresso da inserção:")
    print("-" * 50)
    
    for i, (chave, param_json) in enumerate(dicionario_parametros.items(), 1):
        try:
            # Mapeia os dados do JSON para o formato Oracle
            dados_oracle = mapear_dados_para_oracle(param_json)
            
            if dados_oracle is None:
                print(f"❌ Registro {i:3d}: Erro no mapeamento - {chave}")
                registros_com_erro += 1
                continue
                
            # Executa a inserção
            cursor.execute(sql_insert, dados_oracle)
            
            # Mostra progresso a cada 5 registros
            if i % 5 == 0 or i == len(dicionario_parametros):
                print(f"✅ Registro {i:3d}: {dados_oracle['variedade']}-{dados_oracle['epoca']}-{dados_oracle['processo']}")
            
            registros_inseridos += 1
            
        except oracledb.IntegrityError as e:
            # Violação de chave primária (registro duplicado)
            if "unique constraint" in str(e).lower() or "pk_parametros" in str(e):
                print(f"⚠️  Registro {i:3d}: Duplicado ignorado - {chave}")
                registros_duplicados += 1
            else:
                print(f"❌ Registro {i:3d}: Erro de integridade - {e}")
                registros_com_erro += 1
                
        except Exception as e:
            print(f"❌ Registro {i:3d}: Erro inesperado - {e}")
            registros_com_erro += 1
    
    # Confirma as alterações
    try:
        conn.commit()
        print(f"\n✅ Transação confirmada (COMMIT realizado)")
    except Exception as e:
        print(f"❌ Erro no COMMIT: {e}")
        conn.rollback()
        print("↶ ROLLBACK executado")
    
    # Relatório final
    print("\n" + "=" * 50)
    print("📊 RELATÓRIO FINAL DA CARGA")
    print("=" * 50)
    print(f"📥 Total de registros processados: {len(dicionario_parametros)}")
    print(f"✅ Registros inseridos com sucesso: {registros_inseridos}")
    print(f"⚠️  Registros duplicados (ignorados): {registros_duplicados}")
    print(f"❌ Registros com erro: {registros_com_erro}")
    
    if registros_inseridos > 0:
        percentual = (registros_inseridos / len(dicionario_parametros)) * 100
        print(f"🎯 Taxa de sucesso: {percentual:.1f}%")
    
    cursor.close()
    return registros_inseridos

# ========== FUNÇÃO PARA VERIFICAR DADOS INSERIDOS ==========
def verificar_dados_inseridos(conn):
    """Verifica e mostra alguns registros inseridos na tabela"""
    
    print(f"\n🔍 Verificando dados inseridos na tabela...")
    
    try:
        cursor = conn.cursor()
        
        # Conta total de registros
        cursor.execute("SELECT COUNT(*) FROM parametros")
        total = cursor.fetchone()[0]
        print(f"📊 Total de registros na tabela: {total}")
        
        if total > 0:
            # Mostra os primeiros 5 registros
            cursor.execute("""
                SELECT variedade, epoca, processo, e_rec_m, g_final_rec 
                FROM parametros 
                WHERE ROWNUM <= 5
                ORDER BY variedade, epoca, processo
            """)
            
            resultados = cursor.fetchall()
            print(f"\n📋 Primeiros 5 registros inseridos:")
            print("-" * 70)
            print("Variedade  | Época     | Processo  | E_rec_m | G_final")
            print("-" * 70)
            
            for row in resultados:
                print(f"{row[0]:<10} | {row[1]:<9} | {row[2]:<9} | {row[3]:7.2f} | {row[4]:7d}")
        
        cursor.close()
        
    except Exception as e:
        print(f"❌ Erro ao verificar dados: {e}")

# ========== PROGRAMA PRINCIPAL ==========
def main():
    """Função principal que orquestra todo o processo"""
    
    print(f"🕐 Início do processo: {datetime.now().strftime('%H:%M:%S')}")
    
    # Exibir menu e capturar escolha
    escolha = exibir_menu()
    
    if escolha == 4:
        print("👋 Programa encerrado pelo usuário")
        return True
    
    # 1. Carregar dados do JSON como dicionário
    dict_parametros = carregar_parametros_como_dicionario()
    
    if not dict_parametros:
        print("❌ Não foi possível carregar os dados. Encerrando...")
        return False
    
    # 2. Conectar ao Oracle
    conn = conectar_oracle()
    
    if not conn:
        print("❌ Não foi possível conectar ao Oracle. Encerrando...")
        return False
    
    try:
        # 3. Executar ação baseada na escolha do usuário
        if escolha == 1:
            # Inserir novos dados (ignora duplicados)
            print("\n🔄 Modo: Inserção de novos dados")
            registros_inseridos = inserir_dados_oracle(conn, dict_parametros)
            
            if registros_inseridos > 0:
                verificar_dados_inseridos(conn)
                print(f"\n🎉 Processo concluído com sucesso!")
                print(f"💾 {registros_inseridos} registros carregados na tabela Oracle")
            else:
                print(f"\n⚠️ Nenhum registro novo foi inserido")
                print("💡 Todos os registros já existem na tabela")
                verificar_dados_inseridos(conn)
                
        elif escolha == 2:
            # Limpar tabela e inserir todos os dados
            print("\n🔄 Modo: Limpar e recarregar todos os dados")
            
            if limpar_tabela(conn):
                registros_inseridos = inserir_dados_oracle(conn, dict_parametros)
                verificar_dados_inseridos(conn)
                
                if registros_inseridos > 0:
                    print(f"\n🎉 Recarga concluída com sucesso!")
                    print(f"💾 {registros_inseridos} registros carregados na tabela Oracle")
                else:
                    print(f"\n❌ Erro na recarga dos dados")
            else:
                print("❌ Recarga cancelada devido ao erro na limpeza")
                
        elif escolha == 3:
            # Apenas verificar dados existentes
            print("\n🔍 Modo: Verificação de dados existentes")
            verificar_dados_inseridos(conn)
            print(f"\n📊 Verificação concluída!")
            
    except Exception as e:
        print(f"❌ Erro durante o processo principal: {e}")
        return False
        
    finally:
        # Fechar conexão
        try:
            conn.close()
            print(f"🔌 Conexão com Oracle encerrada")
        except:
            pass
    
    print(f"🕐 Fim do processo: {datetime.now().strftime('%H:%M:%S')}")
    return True

# ========== EXECUÇÃO ==========
if __name__ == "__main__":
    print("🚀 INICIANDO SISTEMA DE CARGA JSON → ORACLE")
    print("📁 Arquivo: carga_json_para_oracle.py")
    print("🎯 Objetivo: Carregar dados de parametros.json na tabela Oracle")
    
    sucesso = main()
    
    if sucesso:
        print("\n" + "=" * 80)
        print("✅ PROCESSO FINALIZADO COM SUCESSO!")
        print("=" * 80)
        print("""
💡 FUNCIONALIDADES DISPONÍVEIS:
1. 📥 Inserção de novos dados (preserva dados existentes)
2. 🔄 Recarga completa (limpa e reinsere todos os dados)
3. 📊 Verificação de dados (apenas consulta, sem alterações)

🎯 PRÓXIMOS PASSOS:
1. Execute manutencao_oracle_paramentros.py para CRUD completo
2. Use a opção '2 - Listar Parametros' para ver todos os registros
3. Teste as operações de inserção, alteração e exclusão

🔄 PARA NOVA EXECUÇÃO:
- Opção 1: Ignora registros duplicados
- Opção 2: Remove todos e reinsere (cuidado!)
- Opção 3: Apenas visualiza dados atuais
        """)
    else:
        print("\n" + "=" * 80)
        print("❌ PROCESSO FINALIZADO COM PROBLEMAS!")
        print("=" * 80)
        print("""
💡 POSSÍVEIS CAUSAS:
1. Arquivo parametros.json não encontrado no diretório atual
2. Problemas de conexão com Oracle Database
3. Credenciais inválidas ou expiradas
4. Tabela 'parametros' não existe no schema

🔧 SOLUÇÕES RECOMENDADAS:
1. Verifique se parametros.json está no mesmo diretório
2. Teste conectividade: ping oracle.fiap.com.br
3. Valide credenciais RM567007 no Oracle
4. Execute o CREATE TABLE da estrutura comentada no código
5. Execute manutencao_oracle_paramentros.py para validar ambiente
        """)
    
    input("\n⏸️  Pressione Enter para finalizar...")