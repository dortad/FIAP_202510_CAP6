"""
Funções da Calculadora de Cana - v8.4 (SEM EMOJIS)
Arquivo separado contendo todas as funções auxiliares do programa principal.
Versão sem emojis para compatibilidade universal com terminais.
"""

import unicodedata
import pandas as pd
import os
from typing import Tuple, Dict, List
from datetime import datetime

# ============================== FUNÇÕES UTILITÁRIAS ==============================
def clear_screen():
    """
    Limpa a tela do terminal de forma compatível com Windows e Linux/Mac.
    
    Função utilitária que detecta o sistema operacional e executa o comando
    apropriado para limpar o terminal:
    - Windows: 'cls'
    - Linux/Mac: 'clear'
    
    Usado em:
    - calculadora_cana_principal_v1.1.py: menu_inicial() - linha 210
    - calculadora_cana_principal_v1.1.py: main() - linha 268
    
    Returns:
        None: Executa comando do sistema para limpar tela
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def strip_accents(text: str) -> str:
    """
    Remove acentos e caracteres especiais de uma string.
    
    Utiliza normalização Unicode NFD (Decomposição Canônica) para separar
    caracteres base de seus diacríticos e remove caracteres de marca (Mn).
    
    Args:
        text (str): Texto com possíveis acentos e caracteres especiais
        
    Returns:
        str: Texto sem acentos (ex: "São Paulo" -> "Sao Paulo")
        
    Usado em:
        - norm_key() - Para normalização de chaves de parâmetros
        - Comparação case-insensitive de variedades de cana
        
    Exemplo:
        >>> strip_accents("São José dos Campos")
        "Sao Jose dos Campos"
    """
    if text is None:
        return ""
    text = str(text)
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

def norm_key(s: str) -> str:
    """
    Normaliza uma string para uso como chave única (remove acentos, espaços e hífens).
    
    Processo de normalização:
    1. Remove acentos usando strip_accents()
    2. Remove hífens e espaços 
    3. Converte para maiúsculas
    
    Args:
        s (str): String a ser normalizada (ex: "RB867-515")
        
    Returns:
        str: String normalizada (ex: "RB867515")
        
    Usado em:
        - compute_row() - Para criar chaves de busca de parâmetros
        - calculadora_cana_principal_v1.1.py - Verificação de combinações
        - Mapeamento Variedade|Epoca|Processo -> Parâmetros
        
    Exemplo:
        >>> norm_key("RB-867 515")
        "RB867515"
    """
    if s is None:
        return ""
    s = strip_accents(s)
    return s.replace("-", "").replace(" ", "").upper()

def to_float_or_none(x):
    """
    Converte valor para float de forma segura ou retorna None se não for possível.
    
    Tenta converter diferentes tipos de entrada para float, tratando casos especiais:
    - Valores None
    - Strings vazias ou só com espaços
    - Substitui vírgulas por pontos (formato brasileiro)
    - Valores que não podem ser convertidos
    
    Args:
        x: Valor a ser convertido (int, str, float, etc.)
        
    Returns:
        float or None: Valor convertido ou None se conversão falhar
        
    Usado em:
        - compute_row() - Conversão segura de áreas e percentuais
        - Validação de parâmetros de entrada do usuário
        - Processamento de dados do Oracle/JSON
        
    Exemplo:
        >>> to_float_or_none("123,45")
        123.45
        >>> to_float_or_none("")
        None
    """
    try:
        if x is None or (isinstance(x, str) and x.strip() == ""):
            return None
        return float(str(x).replace(",", "."))
    except Exception:
        return None

# ======================= CONEXÃO E ORACLE =======================
def test_connection(oracle_user: str, oracle_password: str, oracle_dsn: str):
    """Testa a conexão com o banco Oracle."""
    try:
        import oracledb
    except Exception as e:
        raise RuntimeError("Módulo 'oracledb' não encontrado. Instale com: pip install oracledb") from e

    print("[TEST] Iniciando teste de conexão Oracle...")
    conn = oracledb.connect(user=oracle_user, password=oracle_password, dsn=oracle_dsn)
    try:
        try:
            conn.ping()
            print("[TEST] Ping OK.")
        except Exception as e:
            print(f"[TEST] Ping não suportado/necessário: {e} (seguindo)")

        try:
            drv = oracledb.__version__
        except Exception:
            drv = "desconhecido"
        print(f"[TEST] oracledb version: {drv}")

        try:
            with conn.cursor() as cur:
                cur.execute("SELECT sys_context('USERENV','DB_NAME'), sys_context('USERENV','SESSION_USER') FROM dual")
                row = cur.fetchone()
                if row:
                    print(f"[TEST] DB_NAME: {row[0]} | SESSION_USER: {row[1]}")
        except Exception as e:
            print(f"[TEST] Consulta de diagnóstico falhou (ok seguir): {e}")

        print("[TEST] Conexão Oracle validada com sucesso.\n")
    finally:
        try:
            conn.close()
        except Exception:
            pass

def load_params_from_oracle(oracle_user: str, oracle_password: str, oracle_dsn: str, 
                           params_sql: str, tol_chuva_override: float = 0.08, 
                           tol_seca_override: float = 0.05) -> Tuple[dict, dict, float, float]:
    """Carrega parâmetros do banco Oracle."""
    try:
        import oracledb
    except Exception as e:
        raise RuntimeError("Módulo 'oracledb' não encontrado. Instale com: pip install oracledb") from e

    test_connection(oracle_user, oracle_password, oracle_dsn)

    conn = oracledb.connect(user=oracle_user, password=oracle_password, dsn=oracle_dsn)
    try:
        PARAMS: Dict[str, dict] = {}
        MAP_DISPLAY: Dict[str, dict] = {}
        with conn.cursor() as cur:
            cur.execute(params_sql)
            cols = [d[0].lower() for d in cur.description]
            required = {"variedade","epoca","processo","e","gf","s","g","l","rho","d"}
            missing = required - set(cols)
            if missing:
                raise ValueError(f"A consulta de parâmetros não retornou colunas esperadas. Faltando: {sorted(missing)}")

            rows = cur.fetchall()
            if not rows:
                raise ValueError("A consulta de parâmetros retornou 0 linhas. Verifique a tabela/filtros.")

            print("[DIAG] Amostra (3 primeiras combinações):")
            for row in rows[:3]:
                rec = dict(zip(cols, row))
                print(f"  - {rec.get('variedade')} | {rec.get('epoca')} | {rec.get('processo')}")

            for row in rows:
                rec = dict(zip(cols, row))
                variedade = str(rec.get("variedade") or "").strip()
                epoca = str(rec.get("epoca") or "").strip()
                processo = str(rec.get("processo") or "").strip()
                nk = norm_key(f"{variedade}|{epoca}|{processo}")
                MAP_DISPLAY[nk] = {"Variedade": variedade, "Epoca": epoca, "Processo": processo}
                PARAMS[nk] = {
                    "E": to_float_or_none(rec.get("e")),
                    "Gf": to_float_or_none(rec.get("gf")),
                    "s": to_float_or_none(rec.get("s")),
                    "g": to_float_or_none(rec.get("g")),
                    "L": to_float_or_none(rec.get("l")),
                    "rho": to_float_or_none(rec.get("rho")),
                    "d": to_float_or_none(rec.get("d")),
                }

        print(f"[INFO] Parâmetros carregados do Oracle: {len(PARAMS)} combinações.\n")
        return PARAMS, MAP_DISPLAY, tol_chuva_override, tol_seca_override

    finally:
        try:
            conn.close()
        except Exception:
            pass

# ======================= CÁLCULO PRINCIPAL =======================
def compute_row(row: dict, PARAMS: dict, TOL_CHUVA: float, TOL_SECA: float) -> dict:
    """
    *** FUNÇÃO PRINCIPAL DE CÁLCULO ***
    Calcula todos os resultados agronômicos para uma linha de plantio de cana-de-açúcar.
    
    Esta função executa todos os cálculos necessários:
    1. Busca parâmetros técnicos no banco Oracle
    2. Calcula densidade de plantio (toletes/hectare)
    3. Calcula massa de material vegetal necessária
    4. Determina área efetiva (descontando perdas)
    5. Calcula desvio da recomendação técnica
    6. Define status de qualidade (sistema semáforo)
    
    Args:
        row (dict): Dados de entrada com chaves:
            - Variedade: Nome da variedade de cana
            - Epoca: "Seca" ou "Chuva"
            - Processo: "Manual" ou "Mecanizado"
            - Area_ha: Área em hectares
            - Perc_Manobra_%: Perdas por manobras (%)
            - Perc_Trafego_%: Perdas por tráfego (%)
        PARAMS (dict): Parâmetros técnicos do Oracle/JSON
        TOL_CHUVA (float): Tolerância para época chuvosa (ex: 0.08 = 8%)
        TOL_SECA (float): Tolerância para época seca (ex: 0.05 = 5%)
        
    Returns:
        dict: Resultados calculados com todas as métricas agronômicas
        
    Usado em:
        - calculadora_cana_principal_v1.1.py: main() - linha 406
        
    Fórmulas principais:
        - metros_fileira/ha = 10.000 / espaçamento
        - toletes/metro = gemas_finais / gemas_úteis
        - massa/ha = toletes/ha × comprimento × densidade ÷ 1000
        - status = "OK" se desvio ≤ tolerância, senão "ATENÇÃO"
    """
    res = {}
    variedade = row.get("Variedade")
    epoca     = row.get("Epoca")
    processo  = row.get("Processo")
    key = f"{variedade}|{epoca}|{processo}"
    nk  = norm_key(key)
    p   = PARAMS.get(nk, {})

    # Usando apenas os valores do Oracle
    E_usado    = p.get("E")
    Gf_usado   = p.get("Gf")
    s_usado    = p.get("s")
    g_to_usado = p.get("g")
    L_to_usado = p.get("L")
    rho_usado  = p.get("rho")
    d_usado    = p.get("d")

    m_linhas_por_ha   = (10000/E_usado) if E_usado and E_usado>0 else None
    gemas_plantadas_m = (Gf_usado/s_usado) if (Gf_usado and s_usado and s_usado>0) else None
    toletes_por_m     = (gemas_plantadas_m/g_to_usado) if (gemas_plantadas_m and g_to_usado and g_to_usado>0) else None
    toletes_por_ha    = (toletes_por_m*m_linhas_por_ha) if (toletes_por_m and m_linhas_por_ha) else None
    massa_t_ha_tolete = (toletes_por_ha*L_to_usado*rho_usado)/1000 if (toletes_por_ha and L_to_usado and rho_usado) else None
    massa_t_ha_por_d  = (m_linhas_por_ha*d_usado)/1000 if (m_linhas_por_ha and d_usado) else None
    # Usa sempre o cálculo por tolete como padrão
    massa_escolhida_t_ha = massa_t_ha_tolete

    area_efetiva_ha = None
    try:
        A = to_float_or_none(row.get("Area_ha"))
        B = to_float_or_none(row.get("Perc_Manobra_%"))
        C = to_float_or_none(row.get("Perc_Trafego_%"))
        if A is not None and B is not None and C is not None:
            area_efetiva_ha = A*(1-(B/100)-(C/100))
    except Exception:
        area_efetiva_ha = None

    massa_total_area_t = (massa_escolhida_t_ha*area_efetiva_ha) if (massa_escolhida_t_ha and area_efetiva_ha) else None

    d_rec_kg_m = p.get("d", None)
    desvio_d = None
    try:
        if d_usado and d_rec_kg_m and float(d_rec_kg_m) != 0:
            desvio_d = abs(float(d_usado) - float(d_rec_kg_m))/float(d_rec_kg_m)
    except Exception:
        desvio_d = None

    tolerancia_d = TOL_SECA if str(epoca).strip().lower() == "seca" else TOL_CHUVA
    semaforo = None
    if desvio_d is not None:
        semaforo = "OK" if desvio_d <= tolerancia_d else "ATENCAO"

    res.update({
        "Key": key, "Key_norm": nk, "E_usado": E_usado, "G_final_usado": Gf_usado,
        "s_usado": s_usado, "g_to_usado": g_to_usado, "L_to_usado": L_to_usado,
        "rho_usado": rho_usado, "d_usado": d_usado, "m_linhas_por_ha": m_linhas_por_ha,
        "gemas_plantadas_m": gemas_plantadas_m, "toletes_por_m": toletes_por_m,
        "toletes_por_ha": toletes_por_ha, "massa_t_ha_tolete": massa_t_ha_tolete,
        "massa_t_ha_por_d": massa_t_ha_por_d, "massa_escolhida_t_ha": massa_escolhida_t_ha,
        "Area_efetiva_ha": area_efetiva_ha, "massa_total_area_t": massa_total_area_t,
        "d_rec_kg_m": d_rec_kg_m, "desvio_d_%": desvio_d, "tolerancia_d_%": tolerancia_d,
        "semaforo": semaforo
    })
    return res

# ======================= CATÁLOGO & GLOSSÁRIO =======================
def build_catalog_from_params(PARAMS: Dict[str, dict]) -> Dict[str, dict]:
    """Constrói catálogo a partir dos parâmetros."""
    out = {}
    for nk in PARAMS.keys():
        parts = nk.split("|")
        v = parts[0] if len(parts)>0 else ""
        e = parts[1] if len(parts)>1 else ""
        p = parts[2] if len(parts)>2 else ""
        out[nk] = {"Variedade": v, "Epoca": e, "Processo": p}
    return out

def print_glossary():
    """Exibe o glossário de parâmetros técnicos."""
    print("\n" + "="*80)
    print("GLOSSARIO DE PARAMETROS TECNICOS")
    print("="*80)
    
    print("\n[SECAO 1] ENTRADAS DO USUARIO")
    print("-"*50)
    print("   Area_ha (ha)")
    print("      -> Area total da gleba a ser plantada")
    print("   Perc_Manobra_% (%)")
    print("      -> Perda percentual por manobras e curvas no campo")
    print("   Perc_Trafego_% (%)")
    print("      -> Perda percentual por trafego de maquinas")
    print("   Variedade")
    print("      -> Variedade da cana (ex: RB867515, CTC4, SP80-3280)")
    print("   Epoca")
    print("      -> Seca/Chuva (afeta a tolerancia de desvio nos calculos)")
    print("   Processo")
    print("      -> Manual/Mecanizado (metodo de plantio utilizado)")
    
    print("\n[SECAO 2] PARAMETROS TECNICOS (Oracle Database)")
    print("-"*50)
    print("   E (m)")
    print("      -> Espacamento entre fileiras de plantio")
    print("   Gf (gemas/m)")
    print("      -> Quantidade de gemas por metro desejadas")
    print("   s (gemas/tolete)")
    print("      -> Numero de gemas disponiveis por tolete")
    print("   g (gemas uteis/tolete)")
    print("      -> Gemas uteis/viaveis por tolete plantado")
    print("   L (m)")
    print("      -> Comprimento padrao do tolete")
    print("   rho (kg/m)")
    print("      -> Densidade linear do material de plantio")
    print("   d (kg/m)")
    print("      -> Massa por metro linear recomendada")
    
    print("\n[SECAO 3] FORMULAS DE CALCULO")
    print("-"*50)
    print("   Calculos de densidade:")
    print("      |- m_linhas_por_ha = 10.000 / E")
    print("      |- gemas_plantadas_m = Gf / s")
    print("      +- toletes_por_m = gemas_plantadas_m / g")
    print("")
    print("   Calculos de producao:")
    print("      |- toletes_por_ha = toletes_por_m x m_linhas_por_ha")
    print("      |- massa_t_ha = toletes_por_ha x L x rho / 1000")
    print("      +- Area_efetiva_ha = Area_ha x (1 - Manobra% - Trafego%)")
    print("")
    print("   Resultado final:")
    print("      +- massa_total_t = massa_t_ha x Area_efetiva_ha")
    
    print("\n[SECAO 4] SISTEMA DE ALERTAS (SEMAFORO)")
    print("-"*50)
    print("   [OK]: Dentro da tolerancia aceitavel")
    print("   [ATENCAO]: Fora da tolerancia (requer revisao)")
    print("   Tolerancias:")
    print("      |- Epoca Chuva: ate 8% de desvio")
    print("      +- Epoca Seca: ate 5% de desvio")
    
    print("\n" + "="*80)
    print("Este glossario pode ser acessado durante os calculos com :help+ ou :gloss")
    print("="*80)
    
    input("\n[ENTER] Pressione ENTER para voltar ao menu principal...")

def show_catalog(MAP_DISPLAY: dict, PARAMS: dict = None, page_size: int = 20, filter_var: str = None):
    """Exibe o catálogo de combinações disponíveis."""
    print("\n" + "="*80)
    print("CATALOGO DE COMBINACOES DISPONIVEIS")
    print("="*80)
    
    if (not MAP_DISPLAY) and PARAMS:
        MAP_DISPLAY = build_catalog_from_params(PARAMS)

    # Organizar dados por variedade
    variedades_dict = {}
    for nk, disp in (MAP_DISPLAY or {}).items():
        v = disp.get("Variedade","")
        e = disp.get("Epoca","")
        p = disp.get("Processo","")
        if filter_var and filter_var.lower() not in str(v).lower():
            continue
        
        if v not in variedades_dict:
            variedades_dict[v] = []
        variedades_dict[v].append((e, p, nk))
    
    # Contar totais
    total_variedades = len(variedades_dict)
    total_combinacoes = sum(len(combos) for combos in variedades_dict.values())
    
    print(f"[INFO] Estatisticas:")
    print(f"   • Variedades disponiveis: {total_variedades}")
    print(f"   • Total de combinacoes: {total_combinacoes}")
    if filter_var:
        print(f"   • Filtro aplicado: '{filter_var}' (apenas variedades que contem este termo)")
    
    print("\n" + "-"*80)
    
    # Exibir de forma organizada por variedade
    contador_var = 0
    for variedade in sorted(variedades_dict.keys()):
        contador_var += 1
        combinacoes = variedades_dict[variedade]
        combinacoes.sort(key=lambda x: (x[0], x[1]))  # Ordenar por Época, depois Processo
        
        print(f"\n[VAR] {contador_var:2d}. VARIEDADE: {variedade}")
        print("   " + "-"*50)
        
        # Agrupar por época para melhor visualização
        epocas_dict = {}
        for epoca, processo, nk in combinacoes:
            if epoca not in epocas_dict:
                epocas_dict[epoca] = []
            epocas_dict[epoca].append((processo, nk))
        
        for epoca in sorted(epocas_dict.keys()):
            processos = epocas_dict[epoca]
            processos.sort()
            
            # Indicador para época
            epoca_indicator = "[SECA]" if epoca.upper() == "SECA" else "[CHUVA]"
            print(f"   {epoca_indicator} Epoca: {epoca}")
            
            for processo, nk in processos:
                # Indicador para processo
                processo_indicator = "[MEC]" if "MECANIZADO" in processo.upper() else "[MAN]"
                print(f"      {processo_indicator} {processo:<12} [ID: {nk}]")
        
        # Separador entre variedades, exceto na última
        if contador_var < total_variedades:
            if contador_var % 3 == 0:  # Pausa a cada 3 variedades
                print("\n" + "."*80)
                resposta = input("[INFO] Pressione ENTER para continuar ou 'q' para sair: ").strip().lower()
                if resposta == 'q':
                    break
                print()
    
    print("\n" + "="*80)
    print("LEGENDA:")
    print("   [VAR] Variedade de cana-de-acucar")
    print("   [SECA] Epoca Seca    [CHUVA] Epoca Chuva")
    print("   [MEC] Processo Mecanizado    [MAN] Processo Manual")
    print("   [ID: xxx] Identificador unico da combinacao")
    print("="*80)

def mostrar_sobre_programa():
    """Exibe explicações sobre o que o programa faz no contexto do cultivo da cana-de-açúcar."""
    clear_screen()
    
    print("=" * 80)
    print("SOBRE A CALCULADORA DE CANA-DE-ACUCAR")
    print("=" * 80)
    
    print("\n[VISAO GERAL]")
    print("-" * 40)
    print("Esta Calculadora e um sistema especializado para PLANEJAMENTO e")
    print("DIMENSIONAMENTO do plantio de cana-de-acucar. Ela calcula a quantidade")
    print("exata de material vegetal (toletes/mudas) necessaria para plantar")
    print("uma area especifica.")
    
    print("\n[OBJETIVO PRINCIPAL]")
    print("-" * 40)
    print("[CALCULO] CALCULAR A MASSA TOTAL DE TOLETES (em toneladas)")
    print("   necessaria para plantar uma area de cana-de-acucar.")
    
    print("\n[CONCEITOS FUNDAMENTAIS]")
    print("-" * 40)
    print("• TOLETE = pedaco do colmo da cana cortado para plantio")
    print("           (tambem chamado rebolo, muda ou colmo-semente)")
    print("• GEMAS = 'brotos' que vao originar as novas plantas")
    print("• TAMANHO TIPICO = 30-50 cm (3-5 gemas por tolete)")
    print("• E a 'semente' da cana-de-acucar")
    
    print("\n[TIPOS DE PLANTIO]")
    print("-" * 40)
    print("[MAN] MANUAL: toletes longos, colocados manualmente no sulco")
    print("[MEC] MECANIZADO: toletes menores, distribuidos por maquinas")
    
    input("\n[ENTER] Pressione ENTER para continuar...")
    clear_screen()
    
    print("=" * 80)
    print("COMO O PROGRAMA FUNCIONA")
    print("=" * 80)
    
    print("\n[DADOS] 1. DADOS DE ENTRADA (fornecidos pelo usuario)")
    print("-" * 50)
    print("• Area total da gleba (hectares)")
    print("• Variedade da cana (ex: CTC4, RB867515, SP80-3280)")
    print("• Epoca de plantio (Seca ou Chuva)")
    print("• Processo de plantio (Manual ou Mecanizado)")
    print("• Perdas por manobras e trafego de maquinas (%)")
    
    print("\n[PARAMS] 2. PARAMETROS TECNICOS (obtidos do Oracle)")
    print("-" * 50)
    print("Para cada combinacao Variedade+Epoca+Processo:")
    print("• E = Espacamento entre fileiras (metros)")
    print("• Gf = Gemas desejadas por metro linear")
    print("• s = Gemas disponiveis por tolete")
    print("• g = Gemas uteis/viaveis por tolete")
    print("• L = Comprimento do tolete (metros)")
    print("• rho = Densidade do material (kg/metro)")
    print("• d = Massa recomendada por metro (kg/m)")
    
    print("\n[CALC] 3. CALCULOS REALIZADOS")
    print("-" * 50)
    print("[DENS] Densidade de Plantio:")
    print("   Metros/ha -> Gemas/metro -> Toletes/metro -> Toletes/hectare")
    print("")
    print("[MASSA] Massa de Material:")
    print("   Massa/hectare x Area efetiva = MASSA TOTAL (toneladas)")
    print("")
    print("[QC] Controle de Qualidade:")
    print("   Verifica se esta dentro das tolerancias tecnicas")
    print("   [OK]: dentro da tolerancia | [ATENCAO]: fora da tolerancia")
    
    input("\n[ENTER] Pressione ENTER para continuar...")
    clear_screen()
    
    print("=" * 80)
    print("BENEFICIOS PRATICOS NO CULTIVO")
    print("=" * 80)
    
    print("\n[LOG] 1. LOGISTICA DE MUDAS")
    print("-" * 30)
    print("• Saber exatamente quantas TONELADAS de toletes preparar")
    print("• Planejar TRANSPORTE do material vegetal")
    print("• Dimensionar EQUIPES de corte de mudas")
    print("• Calcular CUSTOS de producao de mudas")
    
    print("\n[PLAN] 2. PLANEJAMENTO DE PLANTIO")
    print("-" * 30)
    print("• Escolher a MELHOR COMBINACAO variedade+epoca+processo")
    print("• Otimizar RENDIMENTO por hectare")
    print("• Reduzir DESPERDICIO de material vegetal")
    print("• Ajustar para diferentes CONDICOES CLIMATICAS")
    
    print("\n[QC] 3. CONTROLE DE QUALIDADE")
    print("-" * 30)
    print("• Verificar se plantio esta DENTRO DAS ESPECIFICACOES")
    print("• Identificar quando ajustar PARAMETROS TECNICOS")
    print("• Monitorar DESVIOS das recomendacoes")
    print("• Garantir STAND ADEQUADO (populacao de plantas)")
    
    print("\n[ECO] 4. GESTAO ECONOMICA")
    print("-" * 30)
    print("• Calcular CUSTO EXATO do material vegetal")
    print("• Otimizar APROVEITAMENTO da area")
    print("• Reduzir PERDAS operacionais")
    print("• Planejar ORCAMENTO de plantio")
    
    input("\n[ENTER] Pressione ENTER para continuar...")
    clear_screen()
    
    print("=" * 80)
    print("EXEMPLO PRATICO")
    print("=" * 80)
    
    print("\n[SITUACAO]:")
    print("Fazenda com 100 hectares para plantar")
    print("Variedade: CTC4 | Epoca: Chuva | Processo: Mecanizado")
    print("Perdas: 5% manobra + 3% trafego")
    
    print("\n[RESULTADO] DO PROGRAMA:")
    print("• Area efetiva: 92 hectares")
    print("• Massa por hectare: 22,12 t/ha")
    print("• MASSA TOTAL NECESSARIA: 2.035 toneladas de toletes")
    print("• Status: [OK] (dentro da tolerancia)")
    
    print("\n[APLICACAO] PRATICA:")
    print("O fazendeiro agora sabe que precisa:")
    print("• Preparar/comprar EXATAMENTE 2.035 toneladas de mudas")
    print("• Organizar transporte para essa quantidade")
    print("• Calcular o custo real do material vegetal")
    print("• Planejar logistica de plantio")
    
    print("\n" + "=" * 80)
    print("[RESUMO]:")
    print("Este programa TRANSFORMA ESTIMATIVAS em CALCULOS PRECISOS,")
    print("permitindo ECONOMIA, EFICIENCIA e QUALIDADE no plantio!")
    print("=" * 80)
    
    input("\n[ENTER] Pressione ENTER para voltar ao menu principal...")

# ======================= EXPORTAÇÃO DE RELATÓRIOS =======================
def gerar_txt(df: pd.DataFrame, resumo: dict, saida_txt: str = "Calculadora_relatorio.txt"):
    """
    *** FUNÇÃO DE GERAÇÃO DE RELATÓRIOS ***
    Gera relatório completo em formato TXT com todos os resultados calculados.
    
    Estrutura do relatório gerado:
    1. Cabeçalho com data/hora e identificação do sistema
    2. Resumo executivo com totais e médias
    3. Produtividade por linha calculada
    4. Dados técnicos detalhados de cada linha
    5. Explicação completa do sistema semáforo/status
    6. Glossário de termos técnicos
    
    Args:
        df (pd.DataFrame): DataFrame com todos os resultados calculados
        resumo (dict): Dicionário com métricas resumidas:
            - linhas: número de linhas processadas
            - soma_massa_total: soma total de massa (toneladas)
            - media_massa_ha: média de massa por hectare
            - ok, atencao, na: contadores de status
        saida_txt (str): Nome do arquivo de saída
        
    Returns:
        None: Salva arquivo TXT no disco
        
    Usado em:
        - calculadora_cana_principal_v1.1.py: main() - linha 495
        
    Arquivo gerado contém ~40+ seções com análise completa dos resultados.
    """
    with open(saida_txt, 'w', encoding='utf-8') as f:
        # Cabeçalho do relatório
        f.write("=" * 80 + "\n")
        f.write("RELATORIO DE CALCULOS - CALCULADORA DE CANA-DE-ACUCAR\n")
        f.write("=" * 80 + "\n")
        f.write(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y as %H:%M:%S')}\n")
        f.write(f"Sistema: Calculadora CLI v8.4 (Oracle Integration)\n")
        f.write("=" * 80 + "\n\n")
        
        # Resumo executivo
        f.write("[RESUMO] EXECUTIVO\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total de linhas processadas: {resumo['linhas']}\n")
        f.write(f"Soma total de massa (t): {resumo['soma_massa_total']:.3f}\n")
        if resumo['media_massa_ha'] is not None:
            f.write(f"Media de massa por hectare: {resumo['media_massa_ha']:.3f} t/ha\n")
        else:
            f.write("Media de massa por hectare: Nao disponivel\n")
        f.write(f"Status dos calculos:\n")
        f.write(f"   [OK] (dentro da tolerancia): {resumo['ok']}\n")
        f.write(f"   [ATENCAO] (fora da tolerancia): {resumo['atencao']}\n")
        f.write(f"   [N/A] (sem dados suficientes): {resumo['na']}\n")
        
        # Produtividade por linha
        f.write(f"\nProdutividade por linha:\n")
        for i, (idx, row) in enumerate(df.iterrows(), 1):
            variedade = row.get('Variedade', 'N/A')
            processo = row.get('Processo', 'N/A')
            massa_ha = row.get('massa_escolhida_t_ha', None)
            massa_total = row.get('massa_total_area_t', None)
            area_efetiva = row.get('Area_efetiva_ha', None)
            status = row.get('semaforo', 'N/A')
            
            if massa_ha is not None:
                massa_ha_str = f"{massa_ha:.3f} t/ha"
            else:
                massa_ha_str = "N/A"
                
            if massa_total is not None:
                massa_total_str = f"{massa_total:.3f} t"
            else:
                massa_total_str = "N/A"
                
            if area_efetiva is not None:
                area_str = f"{area_efetiva:.2f} ha"
            else:
                area_str = "N/A"
            
            status_label = "[OK]" if status == "OK" else "[ATENCAO]" if status == "ATENCAO" else "[N/A]"
            processo_label = "[MEC]" if "MECANIZADO" in str(processo).upper() else "[MAN]"
            
            f.write(f"   Linha {i:02d}: {variedade} {processo_label} -> {massa_ha_str} | Area: {area_str} | Total: {massa_total_str} {status_label}\n")
        
        f.write("\n" + "=" * 80 + "\n\n")
        
        # Resultados detalhados
        f.write("[RESULTADOS] DETALHADOS POR LINHA\n")
        f.write("=" * 80 + "\n\n")
        
        for i, (idx, row) in enumerate(df.iterrows(), 1):
            f.write(f"[LINHA] {i:02d}\n")
            f.write("-" * 30 + "\n")
            
            # Informações básicas
            f.write("Dados de entrada:\n")
            if "Variedade" in row:
                f.write(f"   Variedade: {row['Variedade']}\n")
            if "Epoca" in row:
                epoca_label = "[SECA]" if str(row['Epoca']).upper() == "SECA" else "[CHUVA]"
                f.write(f"   {epoca_label} Epoca: {row['Epoca']}\n")
            if "Processo" in row:
                processo_label = "[MEC]" if "MECANIZADO" in str(row['Processo']).upper() else "[MAN]"
                f.write(f"   {processo_label} Processo: {row['Processo']}\n")
            if "Area_ha" in row:
                f.write(f"   Area total: {row['Area_ha']:.2f} ha\n")
            if "Perc_Manobra_%" in row:
                f.write(f"   Perda por manobra: {row['Perc_Manobra_%']:.1f}%\n")
            if "Perc_Trafego_%" in row:
                f.write(f"   Perda por trafego: {row['Perc_Trafego_%']:.1f}%\n")
            
            # Resultados calculados
            f.write("\nResultados calculados:\n")
            if "Area_efetiva_ha" in row and pd.notna(row['Area_efetiva_ha']):
                f.write(f"   Area efetiva: {row['Area_efetiva_ha']:.2f} ha\n")
            if "massa_escolhida_t_ha" in row and pd.notna(row['massa_escolhida_t_ha']):
                f.write(f"   Massa por hectare: {row['massa_escolhida_t_ha']:.3f} t/ha\n")
            if "massa_total_area_t" in row and pd.notna(row['massa_total_area_t']):
                f.write(f"   Massa total da area: {row['massa_total_area_t']:.3f} t\n")
            
            # Status/Semáforo
            if "semaforo" in row and pd.notna(row['semaforo']):
                status_label = "[OK]" if row['semaforo'] == "OK" else "[ATENCAO]" if row['semaforo'] == "ATENCAO" else "[N/A]"
                f.write(f"   Status: {status_label} {row['semaforo']}\n")
            
            # Parâmetros técnicos (se disponíveis)
            params_tecnicos = ["E_usado", "G_final_usado", "s_usado", "g_to_usado", "L_to_usado", "rho_usado", "d_usado"]
            params_disponiveis = [p for p in params_tecnicos if p in row and pd.notna(row[p])]
            
            if params_disponiveis:
                f.write(f"\nParametros tecnicos utilizados:\n")
                for param in params_disponiveis:
                    valor = row[param]
                    nome_param = {
                        "E_usado": "Espacamento (E)",
                        "G_final_usado": "Gemas finais (Gf)", 
                        "s_usado": "Gemas por tolete (s)",
                        "g_to_usado": "Gemas uteis (g)",
                        "L_to_usado": "Comprimento tolete (L)",
                        "rho_usado": "Densidade (rho)",
                        "d_usado": "Massa por metro (d)"
                    }.get(param, param)
                    f.write(f"   • {nome_param}: {valor}\n")
            
            f.write("\n")
        
        # Rodapé com explicação detalhada do Status/Semáforo
        f.write("=" * 80 + "\n")
        f.write("EXPLICACAO DO STATUS/SEMAFORO\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("[CONCEITO] O que e o Status/Semaforo?\n")
        f.write("-" * 50 + "\n")
        f.write("O Status e um sistema de CONTROLE DE QUALIDADE que verifica se\n")
        f.write("a quantidade de material vegetal calculada esta dentro dos\n")
        f.write("PADROES TECNICOS RECOMENDADOS para aquela variedade/epoca/processo.\n\n")
        
        f.write("[COMO FUNCIONA] Calculo do Status\n")
        f.write("-" * 50 + "\n")
        f.write("1. O programa calcula a massa por metro (d_usado) baseada nos parametros\n")
        f.write("2. Compara com a massa recomendada (d) do banco Oracle\n")
        f.write("3. Calcula o DESVIO PERCENTUAL entre estes valores\n")
        f.write("4. Verifica se esta dentro da TOLERANCIA permitida\n\n")
        
        f.write("[FORMULA] Calculo do Desvio\n")
        f.write("-" * 50 + "\n")
        f.write("desvio_d = |d_usado - d_recomendado| / d_recomendado\n")
        f.write("Onde:\n")
        f.write("  • d_usado = massa calculada pelo programa (kg/m)\n")
        f.write("  • d_recomendado = valor de referencia do Oracle (kg/m)\n\n")
        
        f.write("[TOLERANCIAS] Limites por Epoca\n")
        f.write("-" * 50 + "\n")
        f.write("• EPOCA SECA: ate 5% de desvio (TOL_SECA = 0.05)\n")
        f.write("• EPOCA CHUVA: ate 8% de desvio (TOL_CHUVA = 0.08)\n\n")
        f.write("Razao: Na epoca de chuva ha maior variabilidade nas\n")
        f.write("condicoes de campo, por isso a tolerancia e maior.\n\n")
        
        f.write("[RESULTADOS] Possiveis Status\n")
        f.write("-" * 50 + "\n")
        f.write("[OK] = Desvio <= Tolerancia\n")
        f.write("     → Plantio esta DENTRO das especificacoes tecnicas\n")
        f.write("     → Pode prosseguir sem ajustes\n\n")
        f.write("[ATENCAO] = Desvio > Tolerancia\n")
        f.write("     → Plantio esta FORA das especificacoes\n")
        f.write("     → REQUER REVISAO dos parametros ou processo\n\n")
        f.write("[N/A] = Dados insuficientes\n")
        f.write("     → Nao foi possivel calcular o desvio\n")
        f.write("     → Faltam parametros no banco Oracle\n\n")
        
        f.write("[IMPORTANCIA] Por que o Status e Crucial?\n")
        f.write("-" * 50 + "\n")
        f.write("• QUALIDADE: Garante plantio dentro dos padroes tecnicos\n")
        f.write("• ECONOMIA: Evita desperdicio de material vegetal\n")
        f.write("• PRODUTIVIDADE: Stand adequado resulta em melhor producao\n")
        f.write("• RASTREABILIDADE: Documenta conformidade tecnica\n\n")
        
        f.write("=" * 80 + "\n")
        f.write("[OBSERVACOES GERAIS]:\n")
        f.write("• Este relatorio foi gerado automaticamente pela Calculadora de Cana v8.4\n")
        f.write("• Os parametros tecnicos sao obtidos diretamente do banco Oracle\n")
        f.write("• O Status e um SEMAFORO DE QUALIDADE AGRONOMICA baseado em padroes cientificos\n")
        f.write("• Valores fora da tolerancia indicam necessidade de ajuste tecnico\n")
        f.write("="*80 + "\n")

# ======================= FUNÇÕES DE ENTRADA =======================
HELP_TEXT = """
Comandos disponiveis durante a entrada:
  :cat               -> mostrar catalogo completo de variedades
  :cat <texto>       -> catalogo filtrando Variedade (contem <texto>)
  :help              -> ajuda com comandos disponiveis
  :help+ ou :gloss   -> glossario completo de parametros tecnicos
  :skip              -> pular este campo (usa valor padrao se houver)
  :quit              -> encerrar preenchimento e processar dados inseridos
"""

def handle_command(raw: str) -> Tuple[str, str]:
    """Processa comandos especiais durante a entrada."""
    raw = raw.strip()
    if not raw.startswith(":"):
        return None, None
    parts = raw.split(maxsplit=1)
    cmd = parts[0][1:].lower()
    arg = parts[1] if len(parts) > 1 else None
    return cmd, arg

def ask_float(prompt: str, required: bool = False, default: float = None, 
              MAP_DISPLAY: dict = None, PARAMS: dict = None, 
              min_val: float = None, max_val: float = None, allow_zero: bool = False) -> float:
    """Solicita entrada de número com validação."""
    while True:
        raw = input(f"{prompt} " + (f"[default={default}] " if default is not None else ""))
        if raw.strip() == "":
            if required and default is None:
                print("Valor obrigatorio.")
                continue
            val = default
        else:
            if raw.startswith(":"):
                cmd, arg = handle_command(raw)
                if cmd == "help":
                    print(HELP_TEXT); continue
                if cmd in ("help+", "gloss"):
                    print_glossary(); continue
                if cmd == "cat":
                    show_catalog(MAP_DISPLAY, PARAMS=PARAMS, filter_var=arg); continue
                if cmd == "skip":
                    val = default
                elif cmd == "quit":
                    raise KeyboardInterrupt()
                else:
                    print("Comando desconhecido. Use :help"); continue
            else:
                try:
                    val = float(raw.replace(",", "."))
                except ValueError:
                    print("Digite um numero valido (use ponto ou virgula) ou um comando (:help).")
                    continue

        if val is None:
            return val
        if not allow_zero and val == 0:
            print("Valor nao pode ser zero."); continue
        if min_val is not None and val < min_val:
            print(f"Valor minimo e {min_val}."); continue
        if max_val is not None and val > max_val:
            print(f"Valor maximo e {max_val}."); continue
        return val

def ask_str(prompt: str, required: bool = False, choices: List[str] = None, 
            default: str = None, MAP_DISPLAY: dict = None, PARAMS: dict = None) -> str:
    """Solicita entrada de texto com validação."""
    choices_set = None
    if choices:
        choices_set = {c.lower(): c for c in choices}
    while True:
        suffix = ""
        if choices:
            suffix += " Opcoes: " + "/".join(choices)
        if default is not None:
            suffix += f" [default={default}]"
        raw = input(f"{prompt}{suffix} ").strip()
        if raw == "":
            if required and default is None:
                print("Valor obrigatorio.")
                continue
            return default
        if raw.startswith(":"):
            cmd, arg = handle_command(raw)
            if cmd == "help":
                print(HELP_TEXT); continue
            if cmd in ("help+", "gloss"):
                print_glossary(); continue
            if cmd == "cat":
                show_catalog(MAP_DISPLAY, PARAMS=PARAMS, filter_var=arg); continue
            if cmd == "skip":
                return default
            if cmd == "quit":
                raise KeyboardInterrupt()
            print("Comando desconhecido. Use :help"); continue
        if choices_set:
            key = raw.lower()
            if key in choices_set:
                return choices_set[key]
            print("Escolha invalida. Use :cat para consultar o catalogo ou :help.")
        else:
            return raw