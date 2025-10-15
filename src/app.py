"""
Calculadora de Cana-de-Açúcar v1

Tabela: parametros

  • variedade      → Variedade da cana
  • epoca          → Seca/Chuva
  • processo       → Manual/Mecanizado
  • d_rec_kg_m     → MASSA RECOMENDADA (kg/m) ← ESTE!
  • e_rec_m        → Espaçamento (m)
  • g_final_rec    → Gemas finais
  • s_rec          → Gemas por tolete
  • g_to_rec       → Gemas úteis
  • l_to_rec       → Comprimento tolete
  • rho_rec        → Densidade

"""

import os
import pandas as pd

# Importar módulos da mesma pasta (agora está dentro de src)
from rotinas_V2 import *
from funcoes_calculadora import *

# ============================== CONFIGURAÇÕES ==============================

# Configurações para conexão Oracle usando rotinas_V2.py
TIPO_CONEXAO = 'producao'  # 'producao' ou 'teste' - definido em rotinas_V2.py

# SQL para carregar parâmetros (adaptado para usar rotinas_V2.py)
PARAMS_SQL = """
SELECT variedade as Variedade, epoca as Epoca, processo as Processo, 
       e_rec_m as E, g_final_rec as Gf, s_rec as s, g_to_rec as g, 
       l_to_rec as L, rho_rec as rho, d_rec_kg_m as d
FROM parametros
"""

TOL_CHUVA_OVERRIDE = 0.08  # Valor padrão para época de chuva
TOL_SECA_OVERRIDE  = 0.05  # Valor padrão para época seca

# ============================== FUNÇÕES ORACLE ADAPTADAS ==============================

def load_params_from_oracle_v2(tipo_conexao: str, params_sql: str, tol_chuva: float, tol_seca: float):
    """
    *** FUNÇÃO DE INICIALIZAÇÃO DO SISTEMA ***
    Carrega parâmetros técnicos do Oracle usando rotinas_V2.py.
    
    Processo completo de inicialização:
    1. Conecta ao Oracle usando rotinas_V2.conectar_oracle()
    2. Testa a conexão com query simples
    3. Verifica se tabela 'parametros' tem dados
    4. Se vazia: carrega dados do JSON automaticamente
    5. Executa SQL para buscar parâmetros técnicos
    6. Processa e normaliza dados para uso no programa
    7. Cria mapeamentos PARAMS e MAP_DISPLAY
    
    Args:
        tipo_conexao (str): 'producao' ou 'teste'
        params_sql (str): Query SQL para buscar parâmetros
        tol_chuva (float): Tolerância para época chuvosa (0.08)
        tol_seca (float): Tolerância para época seca (0.05)
        
    Returns:
        tuple: (PARAMS, MAP_DISPLAY, TOL_CHUVA, TOL_SECA)
        
    Usado em:
        - main() linha 273 - Inicialização única do programa
        

    """
    print("\n=== CARREGAMENTO DE PARAMETROS (usando rotinas_V2.py) ===")
    
    # 1) Conectar ao Oracle usando rotinas_V2.py
    conn = conectar_oracle(tipo=tipo_conexao)
    if not conn:
        print("[ERRO] Não foi possível conectar ao Oracle.")
        raise SystemExit(1)
    
    try:
        # 2) Testar conexão
        print("[INFO] Testando conexão...")
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM dual")
        resultado = cursor.fetchone()
        if resultado and resultado[0] == 1:
            print("[OK] Conexão Oracle testada com sucesso!")
        else:
            print("[AVISO] Teste de conexão retornou resultado inesperado.")
        cursor.close()
        
        # 3) Verificar se há dados na tabela
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM parametros")
        total_registros = cursor.fetchone()[0]
        print(f"[INFO] Total de registros encontrados na tabela: {total_registros}")
        
        if total_registros == 0:
            print("[AVISO] Tabela vazia! Tentando carregar dados do JSON...")
            
            # Carregar parâmetros do JSON usando rotinas_V2.py
            dict_parametros = carregar_parametros_Json_como_dicionario()
            
            if dict_parametros:
                print(f"[INFO] JSON carregado: {len(dict_parametros)} registros encontrados.")
                sucesso = carregar_parametros_no_oracle(dict_parametros, conn)
                
                if sucesso:
                    print("[OK] Dados carregados do JSON para o Oracle com sucesso!")
                else:
                    print("[ERRO] Erro ao carregar dados do JSON para o Oracle.")
                    desconectar_oracle(conn)
                    raise SystemExit(1)
            else:
                print("[ERRO] Não foi possível carregar dados do JSON.")
                desconectar_oracle(conn)
                raise SystemExit(1)
        
        # 4) Carregar parâmetros da tabela
        print("[INFO] Carregando parâmetros da tabela Oracle...")
        cursor = conn.cursor()
        cursor.execute(params_sql)
        
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()
        
        if not rows:
            print("[ERRO] Nenhum parâmetro encontrado na consulta.")
            desconectar_oracle(conn)
            raise SystemExit(1)
            
        print(f"[OK] {len(rows)} parâmetros carregados com sucesso!")
        
        # 5) Processar dados (mesmo código da função original)
        PARAMS = {}
        MAP_DISPLAY = {}
        
        for row in rows:
            row_dict = dict(zip(columns, row))
            
            # Mapear colunas Oracle (maiúsculas) para nomes esperados
            # Oracle retorna: VARIEDADE, EPOCA, PROCESSO, E, GF, S, G, L, RHO, D
            variedade = row_dict.get('VARIEDADE', row_dict.get('Variedade', ''))
            epoca = row_dict.get('EPOCA', row_dict.get('Epoca', ''))
            processo = row_dict.get('PROCESSO', row_dict.get('Processo', ''))
            
            # Chave normalizada
            key = f"{variedade}|{epoca}|{processo}"
            norm_key_str = norm_key(key)
            
            # Armazenar parâmetros (considerando nomes Oracle em maiúsculas)
            PARAMS[norm_key_str] = {
                'E': float(row_dict.get('E', row_dict.get('e_rec_m', 0))) if row_dict.get('E', row_dict.get('e_rec_m')) is not None else 0.0,
                'Gf': int(row_dict.get('GF', row_dict.get('Gf', row_dict.get('g_final_rec', 0)))) if row_dict.get('GF', row_dict.get('Gf', row_dict.get('g_final_rec'))) is not None else 0,
                's': float(row_dict.get('S', row_dict.get('s', row_dict.get('s_rec', 0)))) if row_dict.get('S', row_dict.get('s', row_dict.get('s_rec'))) is not None else 0.0,
                'g': float(row_dict.get('G', row_dict.get('g', row_dict.get('g_to_rec', 0)))) if row_dict.get('G', row_dict.get('g', row_dict.get('g_to_rec'))) is not None else 0.0,
                'L': float(row_dict.get('L', row_dict.get('l_to_rec', 0))) if row_dict.get('L', row_dict.get('l_to_rec')) is not None else 0.0,
                'rho': float(row_dict.get('RHO', row_dict.get('rho', row_dict.get('rho_rec', 0)))) if row_dict.get('RHO', row_dict.get('rho', row_dict.get('rho_rec'))) is not None else 0.0,
                'd': float(row_dict.get('D', row_dict.get('d', row_dict.get('d_rec_kg_m', 0)))) if row_dict.get('D', row_dict.get('d', row_dict.get('d_rec_kg_m'))) is not None else 0.0
            }
            
            # Armazenar dados para display
            MAP_DISPLAY[norm_key_str] = {
                'Variedade': variedade,
                'Epoca': epoca, 
                'Processo': processo
            }
        
        # 6) Mostrar amostra dos dados carregados
        print("\n[INFO] Amostra dos dados carregados:")
        amostra_keys = list(PARAMS.keys())[:3]
        for i, nk in enumerate(amostra_keys, 1):
            disp = MAP_DISPLAY[nk]
            param = PARAMS[nk]
            print(f"  {i}. {disp['Variedade']} | {disp['Epoca']} | {disp['Processo']}")
            print(f"     E={param['E']:.2f}, Gf={param['Gf']}, s={param['s']:.2f}")
        
        if len(PARAMS) > 3:
            print(f"     ... e mais {len(PARAMS) - 3} combinações.")
        
        print(f"\n[RESUMO] Total de combinações disponíveis: {len(PARAMS)}")
        
        # 7) Desconectar do Oracle usando rotinas_V2.py
        desconectar_oracle(conn)
        
        return PARAMS, MAP_DISPLAY, tol_chuva, tol_seca
        
    except Exception as e:
        print(f"[ERRO] Erro durante carregamento: {e}")
        desconectar_oracle(conn)
        raise SystemExit(1)

def sincronizar_json_oracle():
    """
    *** FUNÇÃO DE SINCRONIZAÇÃO MANUAL ***
    Sincroniza dados entre arquivo JSON e tabela Oracle.
    
    Processo de sincronização:
    1. Conecta ao Oracle
    2. Carrega dados do parametros.json
    3. Insere/atualiza dados na tabela Oracle
    4. Confirma operação (commit)
    
    Returns:
        bool: True se sincronização bem-sucedida, False caso contrário
        
    Usado em:
        - menu_inicial() opção 4 - Sincronização manual pelo usuário
        
    Permite ao usuário atualizar manualmente a tabela Oracle com dados
    mais recentes do arquivo JSON de parâmetros técnicos.
    """
    print("\n=== SINCRONIZACAO JSON -> ORACLE ===")
    
    # Conectar ao Oracle
    conn = conectar_oracle(tipo=TIPO_CONEXAO)
    if not conn:
        return False
    
    try:
        # Carregar dados do JSON
        dict_parametros = carregar_parametros_Json_como_dicionario()
        
        if not dict_parametros:
            print("[ERRO] Não foi possível carregar dados do JSON.")
            desconectar_oracle(conn)
            return False
        
        print(f"[INFO] JSON carregado: {len(dict_parametros)} registros.")
        
        # Sincronizar com Oracle
        sucesso = carregar_parametros_no_oracle(dict_parametros, conn)
        
        # Desconectar
        desconectar_oracle(conn)
        
        return sucesso
        
    except Exception as e:
        print(f"[ERRO] Erro durante sincronização: {e}")
        desconectar_oracle(conn)
        return False

# ============================== MENU PRINCIPAL ==============================
def menu_inicial(MAP_DISPLAY: dict, PARAMS: dict):
    """
    *** MENU INTERATIVO PRINCIPAL ***
    Exibe menu principal do programa com opções para o usuário.
    
    Opções disponíveis:
    1. Ver catálogo de combinações - Mostra variedades disponíveis
    2. Ver glossário de parâmetros - Explica termos técnicos  
    3. Sobre este programa - Informações do sistema
    4. Sincronizar JSON -> Oracle - Sincronização manual
    5. Iniciar cálculos - Execução principal do programa
    6. Sair - Encerra o programa
    
    Args:
        MAP_DISPLAY (dict): Mapeamento para exibição de variedades
        PARAMS (dict): Parâmetros técnicos carregados
        
    Returns:
        None: Loop até usuário escolher sair ou iniciar cálculos
        
    Usado em:
        - main() linha 307 - Após carregamento dos parâmetros
        
    Interface principal do usuário com validação de opções e navegação.
    """
    while True:
        clear_screen()
        print("\n" + "="*60)
        print("    CALCULADORA DE CANA-DE-ACUCAR - MENU PRINCIPAL")
        print("="*60)
        print("1.  Ver catálogo de combinações")
        print("2.  Ver glossário de parâmetros") 
        print("3.  Sobre este programa (o que faz)")
        print("4.  Sincronizar JSON -> Oracle")
        print("5.  Iniciar cálculos (nova execução)")
        print("6.  Sair")
        print("="*60)
        
        op = input("Escolha uma opção [1-6]: ").strip()
        
        if op == "1":
            clear_screen()
            show_catalog(MAP_DISPLAY, PARAMS=PARAMS, page_size=20)
            input("\n[ENTER] Pressione ENTER para voltar ao menu...")
            
        elif op == "2":
            clear_screen()
            print_glossary()
            input("\n[ENTER] Pressione ENTER para voltar ao menu...")
            
        elif op == "3":
            clear_screen()
            mostrar_sobre_programa()
            input("\n[ENTER] Pressione ENTER para voltar ao menu...")
            
        elif op == "4":
            clear_screen()
            print("[INFO] Iniciando sincronização...")
            sucesso = sincronizar_json_oracle()
            if sucesso:
                print("[OK] Sincronização concluída com sucesso!")
                print("[DICA] Reinicie o programa para usar os dados atualizados.")
            else:
                print("[ERRO] Erro durante a sincronização.")
            input("\n[ENTER] Pressione ENTER para voltar ao menu...")
            
        elif op == "5":
            clear_screen()
            return  # prossegue para o fluxo normal
            
        elif op == "6":
            clear_screen()
            print("Obrigado por usar a Calculadora de Cana!")
            print("Até a próxima!")
            raise SystemExit(0)
            
        else:
            print("[ERRO] Opção inválida. Tente novamente.")
            input("[ENTER] Pressione ENTER para continuar...")

# ============================== FUNÇÃO PRINCIPAL ==============================
def main():
    """
    *** FUNÇÃO PRINCIPAL DO PROGRAMA ***
    Ponto de entrada e orquestração de todo o fluxo do sistema.
    
    Fluxo completo de execução:
    1. Inicialização do sistema
       - Carrega parâmetros do Oracle/JSON
       - Configura tolerâncias de qualidade
    2. Menu interativo
       - Permite consultar catálogo e documentação
       - Opção de sincronização manual
    3. Loop de entrada de dados
       - Solicita dados do usuário (área, variedade, época, etc.)
       - Valida entradas e oferece sugestões
       - Permite múltiplas linhas de cálculo
    4. Processamento
       - Executa cálculos agronômicos via compute_row()
       - Acumula resultados em DataFrame
    5. Geração de relatórios
       - Cria relatório TXT completo
       - Exibe resumo no terminal
    
    Returns:
        None: Executa fluxo completo até conclusão ou erro
        
    Usado em:
        - Bloco __main__ linha 556 - Entry point do programa
        
    Centraliza toda a lógica de negócio e fluxo do usuário.
    """
    clear_screen()
    
    print("=" + "="*58 + "=")
    print("= CALCULADORA DE CANA-DE-ACUCAR v1.1 (com rotinas_V2.py) =")
    print("=" + "="*58 + "=")
    print()
    
    # 1) Carregar parâmetros do Oracle usando rotinas_V2.py
    try:
        PARAMS, MAP_DISPLAY, TOL_CHUVA, TOL_SECA = load_params_from_oracle_v2(
            TIPO_CONEXAO, PARAMS_SQL, TOL_CHUVA_OVERRIDE, TOL_SECA_OVERRIDE
        )
    except SystemExit:
        return
    except Exception as e:
        print(f"[ERRO] Erro crítico durante inicialização: {e}")
        return

    print("\n[DICA] Use o menu para consultar o catálogo e o glossário antes de começar.")
    print("[INFO] A opção 'Sobre este programa' explica o funcionamento completo.")
    input("\n[ENTER] Pressione ENTER para continuar...")

    # 2) Menu inicial
    menu_inicial(MAP_DISPLAY, PARAMS)
    clear_screen()
    print("\n[DICAS] Para entrada de dados:")
    print("   • :help     -> Ajuda básica")
    print("   • :help+ ou :gloss -> Ver glossário completo")
    print("   • :cat <texto> -> Buscar variedades")
    print("   • :cat -> Ver todas as combinações")
    print()

    # 3) Entrada e cálculos (mantém o código original)
    registros = []
    try:
        while True:
            print("\n" + "-"*50)
            print("NOVA LINHA DE CALCULO")
            print("-"*50)
            
            linha = {}
            linha["Area_ha"] = ask_float("Area_ha:", required=True, MAP_DISPLAY=MAP_DISPLAY, PARAMS=PARAMS, min_val=0.0001)
            
            # Solicitar processo primeiro para definir valores padrão de perdas
            linha["Processo"] = ask_str("Processo (Manual/Mecanizado):", required=True, choices=["Manual","Mecanizado"], default="Mecanizado", MAP_DISPLAY=MAP_DISPLAY, PARAMS=PARAMS)
            
            # Definir valores padrão baseados no processo (conforme perdas_explicadas.txt)
            if linha["Processo"].upper() == "MANUAL":
                # Manual: valores médios das faixas recomendadas
                default_manobra = 3.0  # Faixa: 2-7% (regular a pequeno)
                default_trafego = 1.0  # Faixa: 0.5-2% (regular a pequeno)
                processo_desc = "[MANUAL] Valores baseados em perdas_explicadas.txt"
                faixas_info = "Faixas típicas - Manobra: 2-7%, Tráfego: 0.5-2%"
            else:
                # Mecanizado: valores médios das faixas recomendadas  
                default_manobra = 5.0  # Faixa: 3-9% (regular a pequeno/declivoso)
                default_trafego = 3.0  # Faixa: 2-6% (regular a pequeno/declivoso)
                processo_desc = "[MECANIZADO] Valores baseados em perdas_explicadas.txt"
                faixas_info = "Faixas típicas - Manobra: 3-9%, Tráfego: 2-6%"
            
            print(f"[INFO] {processo_desc}")
            print(f"[INFO] {faixas_info}")
            print(f"[INFO] Padrões sugeridos: Manobra={default_manobra}%, Tráfego={default_trafego}%")
            
            # Solicitar perdas com valores padrão específicos do processo
            linha["Perc_Manobra_%"] = ask_float("Perc_Manobra_%:", required=True, default=default_manobra, MAP_DISPLAY=MAP_DISPLAY, PARAMS=PARAMS, min_val=0, max_val=100, allow_zero=True)
            linha["Perc_Trafego_%"] = ask_float("Perc_Trafego_%:", required=True, default=default_trafego, MAP_DISPLAY=MAP_DISPLAY, PARAMS=PARAMS, min_val=0, max_val=100, allow_zero=True)
            
            # Solicitar variedade com verificação
            while True:
                variedade_digitada = ask_str("Variedade:", required=True, MAP_DISPLAY=MAP_DISPLAY, PARAMS=PARAMS)
                
                # Criar mapeamento de variedades (case-insensitive)
                variedades_map = {}
                variedades_originais = set()
                
                for disp in MAP_DISPLAY.values():
                    var_original = disp.get("Variedade", "").strip()
                    if var_original:
                        variedades_originais.add(var_original)
                        variedades_map[var_original.upper()] = var_original
                
                # Verificar se a variedade existe (case-insensitive)
                var_upper = variedade_digitada.upper()
                if var_upper in variedades_map:
                    linha["Variedade"] = variedades_map[var_upper]
                    break
                else:
                    print(f"[ERRO] Variedade '{variedade_digitada}' não encontrada no catálogo.")
                    print("[INFO] Variedades disponíveis:")
                    
                    # Mostrar variedades disponíveis ordenadas
                    variedades_ordenadas = sorted(list(variedades_originais))
                    for i, var in enumerate(variedades_ordenadas, 1):
                        print(f"   {i:2d}. {var}")
                    
                    # Sugerir variedades similares
                    sugestoes = []
                    var_digitada_upper = variedade_digitada.upper()
                    for var_orig in variedades_originais:
                        if var_digitada_upper in var_orig.upper() or var_orig.upper().startswith(var_digitada_upper[:3]):
                            sugestoes.append(var_orig)
                    
                    if sugestoes:
                        print(f"[SUGESTAO] Baseadas em '{variedade_digitada}':")
                        for sug in sorted(sugestoes):
                            print(f"   -> {sug}")
                    
                    print("[DICA] Use :cat <nome> para buscar variedades ou :cat para ver todas.")
                    continuar = input("Tentar novamente? (s/n) [default=s]: ").strip().lower()
                    if continuar == 'n':
                        print("[AVISO] Operação cancelada pelo usuário.")
                        return
            
            linha["Epoca"] = ask_str("Epoca (Seca/Chuva):", required=True, choices=["Seca","Chuva"], default="Chuva", MAP_DISPLAY=MAP_DISPLAY, PARAMS=PARAMS)

            # Verificar se a combinação específica existe
            k = f"{linha['Variedade']}|{linha['Epoca']}|{linha['Processo']}"
            nk = norm_key(k)
            if nk not in PARAMS:
                print("[AVISO] Combinação específica Variedade|Epoca|Processo não encontrada.")
                print(f"   Combinação testada: {linha['Variedade']} | {linha['Epoca']} | {linha['Processo']}")
                
                # Mostrar combinações disponíveis para esta variedade
                print(f"[INFO] Combinações disponíveis para {linha['Variedade']}:")
                combinacoes_var = []
                for nk_test, disp in MAP_DISPLAY.items():
                    if disp.get("Variedade", "").upper() == linha["Variedade"].upper():
                        combinacoes_var.append(f"   • {disp['Variedade']} | {disp['Epoca']} | {disp['Processo']}")
                
                if combinacoes_var:
                    for comb in sorted(combinacoes_var):
                        print(comb)
                else:
                    print("   Nenhuma combinação encontrada para esta variedade.")
                
                print("[DICA] Use :cat para consultar o catálogo completo.")

            # Realizar cálculos
            res = compute_row(linha, PARAMS, TOL_CHUVA, TOL_SECA)
            registros.append({**linha, **res})

            cont = ask_str("Adicionar outra linha? (s/n):", required=True, choices=["s","n"], default="n", MAP_DISPLAY=MAP_DISPLAY, PARAMS=PARAMS)
            if cont == "n":
                break
                
    except KeyboardInterrupt:
        print("\n[AVISO] Encerrado a pedido do usuário (Ctrl+C).")
        print("[INFO] Prosseguindo com os dados já inseridos...")

    if not registros:
        print("[ERRO] Nenhum dado inserido. Encerrando.")
        return

    # 4) Montagem do DataFrame e resumo (código original mantido)
    df = pd.DataFrame(registros)
    ordered_cols = [
        "Area_ha","Perc_Manobra_%","Perc_Trafego_%","Variedade","Epoca","Processo",
        "Key","Key_norm","E_usado","G_final_usado","s_usado","g_to_usado","L_to_usado","rho_usado","d_usado",
        "m_linhas_por_ha","gemas_plantadas_m","toletes_por_m","toletes_por_ha",
        "massa_t_ha_tolete","massa_t_ha_por_d","massa_escolhida_t_ha","Area_efetiva_ha",
        "massa_total_area_t","d_rec_kg_m","desvio_d_%","tolerancia_d_%","semaforo"
    ]
    cols = [c for c in ordered_cols if c in df.columns] + [c for c in df.columns if c not in ordered_cols]
    df = df[cols]

    print("\n" + "="*80)
    print("PREVIA DOS RESULTADOS CALCULADOS")
    print("="*80)
    
    # Mostrar apenas as colunas mais importantes na prévia
    colunas_importantes = [
        "Variedade", "Epoca", "Processo", "Area_ha", "Area_efetiva_ha", 
        "massa_escolhida_t_ha", "massa_total_area_t", "semaforo"
    ]
    
    colunas_previa = [col for col in colunas_importantes if col in df.columns]
    
    if len(df) > 0:
        df_previa = df[colunas_previa].copy()
        
        # Formatar números para melhor legibilidade
        if "Area_ha" in df_previa.columns:
            df_previa["Area_ha"] = df_previa["Area_ha"].round(2)
        if "Area_efetiva_ha" in df_previa.columns:
            df_previa["Area_efetiva_ha"] = df_previa["Area_efetiva_ha"].round(2)
        if "massa_escolhida_t_ha" in df_previa.columns:
            df_previa["massa_escolhida_t_ha"] = df_previa["massa_escolhida_t_ha"].round(3)
        if "massa_total_area_t" in df_previa.columns:
            df_previa["massa_total_area_t"] = df_previa["massa_total_area_t"].round(3)
        
        print(df_previa.to_string(index=False, max_colwidth=15))
    else:
        print("Nenhum registro encontrado.")
    
    print("="*80)

    # Cálculos do resumo
    soma_massa_total = float(df["massa_total_area_t"].sum(skipna=True)) if "massa_total_area_t" in df else 0.0
    media_massa_ha = float(df["massa_escolhida_t_ha"].mean(skipna=True)) if "massa_escolhida_t_ha" in df else None
    ok = int((df["semaforo"]=="OK").sum()) if "semaforo" in df else 0
    atencao = int((df["semaforo"]=="ATENCAO").sum()) if "semaforo" in df else 0
    na = int(df["semaforo"].isna().sum()) if "semaforo" in df else 0

    resumo = {
        "linhas": len(df),
        "soma_massa_total": soma_massa_total,
        "media_massa_ha": media_massa_ha,
        "ok": ok,
        "atencao": atencao,
        "na": na,
    }

    print("\n[RESUMO] DOS RESULTADOS:")
    print(f"   Linhas processadas: {resumo['linhas']}")
    print(f"   Soma Massa Total (t): {resumo['soma_massa_total']:.3f}")
    if resumo['media_massa_ha'] is not None:
        print(f"   Média Massa t/ha: {resumo['media_massa_ha']:.3f}")
    else:
        print("   Média Massa t/ha: N/A")
    print(f"   Status: [OK]: {resumo['ok']} | [ATENCAO]: {resumo['atencao']} | [N/A]: {resumo['na']}")

    # 5) Exportação
    print("\n" + "="*60)
    print("EXPORTACAO DE RESULTADOS")
    print("="*60)
    
    nome = ask_str("Nome base do arquivo (sem extensão):", required=False, default="Calculadora_Cana_resultados", MAP_DISPLAY=MAP_DISPLAY, PARAMS=PARAMS)

    print(f"\n[INFO] Gerando relatório em texto...")

    gerar_txt(df, resumo, saida_txt=f"{nome}.txt")
    print(f"[OK] TXT: {nome}.txt")

    print("\n[SUCESSO] Processo concluído com sucesso!")
    print("Obrigado por usar a Calculadora de Cana de Açúcar!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[AVISO] Programa interrompido pelo usuário (Ctrl+C).")
        print("Até a próxima!")
    except Exception as e:
        print(f"\n[ERRO] Erro crítico não tratado: {e}")
        print("Contate o suporte técnico se o problema persistir.")