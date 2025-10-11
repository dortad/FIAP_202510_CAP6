
"""
Calculadora de Cana - CLI v8.3 (Oracle ONLY, sem cache)

Novidades v8.3:
- **Menu inicial** com opções: Catálogo, Glossário de parâmetros, Iniciar cálculos, Sair.
- **Glossário integrado** (detalhado) acessível no menu e durante a entrada via comandos
  `:gloss` ou `:help+` (além do `:help` básico).
- Mantém: teste de conexão, diagnóstico de amostra, catálogo desde Oracle, validações,
  resumo e exportações (XLSX/CSV/PDF).

Dependências:
  pip install oracledb pandas openpyxl matplotlib
"""

import unicodedata
import pandas as pd
import matplotlib.pyplot as plt
import os
from typing import Tuple, Dict, List
from rotinas_V2 import *

# ============================== FUNÇÕES UTILITÁRIAS ==============================
def clear_screen():
    """Limpa a tela do terminal de forma compatível com Windows e Linux/Mac."""
    os.system('cls' if os.name == 'nt' else 'clear')

# ============================== CONFIG ==============================
ORACLE_USER = "RM567007"
ORACLE_PASSWORD = "RM567007"
ORACLE_DSN = "localhost:1521/xe"   # Servidor FIAP Oracle

PARAMS_SQL = """
SELECT variedade as Variedade, epoca as Epoca, processo as Processo, 
       e_rec_m as E, g_final_rec as Gf, s_rec as s, g_to_rec as g, 
       l_to_rec as L, rho_rec as rho, d_rec_kg_m as d
FROM parametros
"""

# Tabela CANA_CONFIG não existe, usar valores padrão
TOL_SQL = None  # "SELECT tol_chuva, tol_seca FROM CANA_CONFIG WHERE id = 1"

TOL_CHUVA_OVERRIDE = 0.08  # Valor padrão para época de chuva
TOL_SECA_OVERRIDE  = 0.05  # Valor padrão para época seca

# ======================= Utilidades gerais =======================
def strip_accents(text: str) -> str:
    if text is None:
        return ""
    text = str(text)
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

def norm_key(s: str) -> str:
    if s is None:
        return ""
    s = strip_accents(s)
    return s.replace("-", "").replace(" ", "").upper()

def to_float_or_none(x):
    try:
        if x is None or (isinstance(x, str) and x.strip() == ""):
            return None
        return float(str(x).replace(",", "."))
    except Exception:
        return None

# Função choose() removida - não é mais necessária sem overrides

# ======================= Teste de conexão & diagnóstico =======================
def test_connection():
    try:
        import oracledb
    except Exception as e:
        raise RuntimeError("Módulo 'oracledb' não encontrado. Instale com: pip install oracledb") from e

    print("[TEST] Iniciando teste de conexão Oracle...")
    conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=ORACLE_DSN)
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

# ======================= Oracle (obrigatório) =======================
def load_params_from_oracle() -> Tuple[dict, dict, float, float]:
    try:
        import oracledb
    except Exception as e:
        raise RuntimeError("Módulo 'oracledb' não encontrado. Instale com: pip install oracledb") from e

    test_connection()

    conn = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=ORACLE_DSN)
    try:
        PARAMS: Dict[str, dict] = {}
        MAP_DISPLAY: Dict[str, dict] = {}
        with conn.cursor() as cur:
            cur.execute(PARAMS_SQL)
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

        TOL_CHUVA = None
        TOL_SECA  = None

        if TOL_CHUVA_OVERRIDE is not None:
            TOL_CHUVA = TOL_CHUVA_OVERRIDE
        if TOL_SECA_OVERRIDE is not None:
            TOL_SECA  = TOL_SECA_OVERRIDE

        if (TOL_CHUVA is None or TOL_SECA is None) and TOL_SQL:
            with conn.cursor() as cur:
                cur.execute(TOL_SQL)
                row = cur.fetchone()
                if row is not None:
                    try:
                        if TOL_CHUVA is None: TOL_CHUVA = to_float_or_none(row[0])
                        if TOL_SECA  is None: TOL_SECA  = to_float_or_none(row[1])
                    except Exception:
                        cols2 = [d[0].lower() for d in cur.description]
                        if TOL_CHUVA is None and "tol_chuva" in cols2:
                            TOL_CHUVA = to_float_or_none(row[cols2.index("tol_chuva")])
                        if TOL_SECA is None and "tol_seca" in cols2:
                            TOL_SECA  = to_float_or_none(row[cols2.index("tol_seca")])

        if TOL_CHUVA is None: TOL_CHUVA = 0.08
        if TOL_SECA  is None: TOL_SECA  = 0.05

        print(f"[INFO] Parâmetros carregados do Oracle: {len(PARAMS)} combinações.\n")
        return PARAMS, MAP_DISPLAY, TOL_CHUVA, TOL_SECA

    finally:
        try:
            conn.close()
        except Exception:
            pass

# ======================= Cálculo principal =======================
def compute_row(row: dict, PARAMS, TOL_CHUVA, TOL_SECA):
    res = {}
    variedade = row.get("Variedade")
    epoca     = row.get("Epoca")
    processo  = row.get("Processo")
    key = f"{variedade}|{epoca}|{processo}"
    nk  = norm_key(key)
    p   = PARAMS.get(nk, {})

    # Usando apenas os valores do Oracle (sem overrides)
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

# ======================= Catálogo & Glossário =======================
def build_catalog_from_params(PARAMS: Dict[str, dict]) -> Dict[str, dict]:
    out = {}
    for nk in PARAMS.keys():
        parts = nk.split("|")
        v = parts[0] if len(parts)>0 else ""
        e = parts[1] if len(parts)>1 else ""
        p = parts[2] if len(parts)>2 else ""
        out[nk] = {"Variedade": v, "Epoca": e, "Processo": p}
    return out

def print_glossary():
    print("\n" + "="*80)
    print("📚 GLOSSÁRIO DE PARÂMETROS TÉCNICOS")
    print("="*80)
    
    print("\n🔵 1. ENTRADAS DO USUÁRIO")
    print("─"*50)
    print("   📏 Area_ha (ha)")
    print("      └── Área total da gleba a ser plantada")
    print("   ⚙️  Perc_Manobra_% (%)")
    print("      └── Perda percentual por manobras e curvas no campo")
    print("   🚛 Perc_Trafego_% (%)")
    print("      └── Perda percentual por tráfego de máquinas")
    print("   🌱 Variedade")
    print("      └── Variedade da cana (ex: RB867515, CTC4, SP80-3280)")
    print("   🌦️  Epoca")
    print("      └── Seca/Chuva (afeta a tolerância de desvio nos cálculos)")
    print("   🔧 Processo")
    print("      └── Manual/Mecanizado (método de plantio utilizado)")
    
    print("\n🔴 2. PARÂMETROS TÉCNICOS (Oracle Database)")
    print("─"*50)
    print("   📐 E (m)")
    print("      └── Espaçamento entre fileiras de plantio")
    print("   🧬 Gf (gemas/m)")
    print("      └── Quantidade de gemas por metro desejadas")
    print("   🔢 s (gemas/tolete)")
    print("      └── Número de gemas disponíveis por tolete")
    print("   ✅ g (gemas úteis/tolete)")
    print("      └── Gemas úteis/viáveis por tolete plantado")
    print("   📏 L (m)")
    print("      └── Comprimento padrão do tolete")
    print("   ⚖️  rho (kg/m)")
    print("      └── Densidade linear do material de plantio")
    print("   📊 d (kg/m)")
    print("      └── Massa por metro linear recomendada")
    
    print("\n🟢 3. FÓRMULAS DE CÁLCULO")
    print("─"*50)
    print("   🧮 Cálculos de densidade:")
    print("      ├── m_linhas_por_ha = 10.000 ÷ E")
    print("      ├── gemas_plantadas_m = Gf ÷ s")
    print("      └── toletes_por_m = gemas_plantadas_m ÷ g")
    print("")
    print("   📈 Cálculos de produção:")
    print("      ├── toletes_por_ha = toletes_por_m × m_linhas_por_ha")
    print("      ├── massa_t_ha = toletes_por_ha × L × rho ÷ 1000")
    print("      └── Area_efetiva_ha = Area_ha × (1 - Manobra% - Tráfego%)")
    print("")
    print("   🎯 Resultado final:")
    print("      └── massa_total_t = massa_t_ha × Area_efetiva_ha")
    
    print("\n🟡 4. SISTEMA DE ALERTAS (SEMÁFORO)")
    print("─"*50)
    print("   🟢 OK: Dentro da tolerância aceitável")
    print("   🟡 ATENÇÃO: Fora da tolerância (requer revisão)")
    print("   📊 Tolerâncias:")
    print("      ├── 🌧️  Época Chuva: até 8% de desvio")
    print("      └── ☀️  Época Seca: até 5% de desvio")
    
    print("\n" + "="*80)
    print("💡 Este glossário pode ser acessado durante os cálculos com :help+ ou :gloss")
    print("="*80)
    
    input("\n📖 Pressione ENTER para voltar ao menu principal...")

def show_catalog(MAP_DISPLAY, PARAMS=None, page_size=20, filter_var=None):
    print("\n" + "="*80)
    print("📋 CATÁLOGO DE COMBINAÇÕES DISPONÍVEIS")
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
    
    print(f"📊 Estatísticas:")
    print(f"   • Variedades disponíveis: {total_variedades}")
    print(f"   • Total de combinações: {total_combinacoes}")
    if filter_var:
        print(f"   • Filtro aplicado: '{filter_var}' (apenas variedades que contêm este termo)")
    
    print("\n" + "-"*80)
    
    # Exibir de forma organizada por variedade
    contador_var = 0
    for variedade in sorted(variedades_dict.keys()):
        contador_var += 1
        combinacoes = variedades_dict[variedade]
        combinacoes.sort(key=lambda x: (x[0], x[1]))  # Ordenar por Época, depois Processo
        
        print(f"\n🌱 {contador_var:2d}. VARIEDADE: {variedade}")
        print("   " + "─"*50)
        
        # Agrupar por época para melhor visualização
        epocas_dict = {}
        for epoca, processo, nk in combinacoes:
            if epoca not in epocas_dict:
                epocas_dict[epoca] = []
            epocas_dict[epoca].append((processo, nk))
        
        for epoca in sorted(epocas_dict.keys()):
            processos = epocas_dict[epoca]
            processos.sort()
            
            # Ícone para época
            epoca_icon = "☀️" if epoca.upper() == "SECA" else "🌧️"
            print(f"   {epoca_icon} Época: {epoca}")
            
            for processo, nk in processos:
                # Ícone para processo
                processo_icon = "🚜" if "MECANIZADO" in processo.upper() else "👷"
                print(f"      {processo_icon} {processo:<12} [ID: {nk}]")
        
        # Separador entre variedades, exceto na última
        if contador_var < total_variedades:
            if contador_var % 3 == 0:  # Pausa a cada 3 variedades
                print("\n" + "."*80)
                resposta = input("🔄 Pressione ENTER para continuar ou 'q' para sair: ").strip().lower()
                if resposta == 'q':
                    break
                print()
    
    print("\n" + "="*80)
    print("💡 LEGENDA:")
    print("   🌱 Variedade de cana-de-açúcar")
    print("   ☀️ Época Seca    🌧️ Época Chuva")
    print("   🚜 Processo Mecanizado    👷 Processo Manual")
    print("   [ID: xxx] Identificador único da combinação")
    print("="*80)

HELP_TEXT = """
Comandos disponíveis durante a entrada:
  :cat               -> mostrar catálogo completo de variedades
  :cat <texto>       -> catálogo filtrando Variedade (contém <texto>)
  :help              -> ajuda com comandos disponíveis
  :help+ ou :gloss   -> glossário completo de parâmetros técnicos
  :skip              -> pular este campo (usa valor padrão se houver)
  :quit              -> encerrar preenchimento e processar dados inseridos
"""

def handle_command(raw):
    raw = raw.strip()
    if not raw.startswith(":"):
        return None, None
    parts = raw.split(maxsplit=1)
    cmd = parts[0][1:].lower()
    arg = parts[1] if len(parts) > 1 else None
    return cmd, arg

# ======================= Validação de entrada =======================
def ask_float(prompt, required=False, default=None, MAP_DISPLAY=None, PARAMS=None, min_val=None, max_val=None, allow_zero=False):
    while True:
        raw = input(f"{prompt} " + (f"[default={default}] " if default is not None else ""))
        if raw.strip() == "":
            if required and default is None:
                print("Valor obrigatório.")
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
                    val = default  # cai para validação adiante
                elif cmd == "quit":
                    raise KeyboardInterrupt()
                else:
                    print("Comando desconhecido. Use :help"); continue
            else:
                try:
                    val = float(raw.replace(",", "."))
                except ValueError:
                    print("Digite um número válido (use ponto ou vírgula) ou um comando (:help).")
                    continue

        if val is None:
            return val
        if not allow_zero and val == 0:
            print("Valor não pode ser zero."); continue
        if min_val is not None and val < min_val:
            print(f"Valor mínimo é {min_val}."); continue
        if max_val is not None and val > max_val:
            print(f"Valor máximo é {max_val}."); continue
        return val

def ask_str(prompt, required=False, choices=None, default=None, MAP_DISPLAY=None, PARAMS=None):
    choices_set = None
    if choices:
        choices_set = {c.lower(): c for c in choices}
    while True:
        suffix = ""
        if choices:
            suffix += " Opções: " + "/".join(choices)
        if default is not None:
            suffix += f" [default={default}]"
        raw = input(f"{prompt}{suffix} ").strip()
        if raw == "":
            if required and default is None:
                print("Valor obrigatório.")
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
            print("Escolha inválida. Use :cat para consultar o catálogo ou :help.")
        else:
            return raw

# ============================ MAIN ============================
def gerar_pdf(df, resumo, saida_pdf="Calculadora_relatorio.pdf"):
    fig = plt.figure(figsize=(11.69, 8.27))
    fig.suptitle("Relatório - Calculadora de Cana", fontsize=16)
    ax = fig.add_subplot(111)
    ax.axis('off')
    lines = [
        f"Linhas: {resumo['linhas']}",
        f"Soma Massa Total (t): {resumo['soma_massa_total']:.3f}",
        f"Média Massa t/ha: {resumo['media_massa_ha']:.3f}" if resumo['media_massa_ha'] is not None else "Média Massa t/ha: -",
        f"OK: {resumo['ok']} | ATENCAO: {resumo['atencao']} | N/A: {resumo['na']}",
    ]
    ax.text(0.01, 0.9, "\n".join(lines), va="top")
    fig.savefig(saida_pdf)

    remaining = df.copy()
    start = 0
    block = 18
    while start < len(remaining):
        end = min(start + block, len(remaining))
        sub = remaining.iloc[start:end]
        fig2 = plt.figure(figsize=(11.69, 8.27))
        ax2 = fig2.add_subplot(111)
        ax2.axis('off')
        tbl = ax2.table(cellText=sub.values, colLabels=sub.columns, loc='center')
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(8)
        tbl.scale(1, 1.2)
        fig2.tight_layout()
        fig2.savefig(saida_pdf, bbox_inches='tight', pad_inches=0.5)
        start = end
    plt.close('all')

def gerar_txt(df, resumo, saida_txt="Calculadora_relatorio.txt"):
    """Gera relatório formatado em arquivo de texto."""
    from datetime import datetime
    
    with open(saida_txt, 'w', encoding='utf-8') as f:
        # Cabeçalho do relatório
        f.write("=" * 80 + "\n")
        f.write("🌾 RELATÓRIO DE CÁLCULOS - CALCULADORA DE CANA-DE-AÇÚCAR 🌾\n")
        f.write("=" * 80 + "\n")
        f.write(f"📅 Data/Hora: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}\n")
        f.write(f"📊 Sistema: Calculadora CLI v8.3 (Oracle Integration)\n")
        f.write("=" * 80 + "\n\n")
        
        # Resumo executivo
        f.write("📈 RESUMO EXECUTIVO\n")
        f.write("-" * 40 + "\n")
        f.write(f"🔢 Total de linhas processadas: {resumo['linhas']}\n")
        f.write(f"⚖️  Soma total de massa (t): {resumo['soma_massa_total']:.3f}\n")
        if resumo['media_massa_ha'] is not None:
            f.write(f"📊 Média de massa por hectare: {resumo['media_massa_ha']:.3f} t/ha\n")
        else:
            f.write("📊 Média de massa por hectare: Não disponível\n")
        f.write(f"🚦 Status dos cálculos:\n")
        f.write(f"   🟢 OK (dentro da tolerância): {resumo['ok']}\n")
        f.write(f"   🟡 ATENÇÃO (fora da tolerância): {resumo['atencao']}\n")
        f.write(f"   ⚪ N/A (sem dados suficientes): {resumo['na']}\n")
        f.write("\n" + "=" * 80 + "\n\n")
        
        # Resultados detalhados
        f.write("📋 RESULTADOS DETALHADOS POR LINHA\n")
        f.write("=" * 80 + "\n\n")
        
        # Colunas principais para exibição
        colunas_principais = [
            "Variedade", "Epoca", "Processo", "Area_ha", "Area_efetiva_ha", 
            "massa_escolhida_t_ha", "massa_total_area_t", "semaforo"
        ]
        
        # Filtrar colunas que existem
        cols_existentes = [col for col in colunas_principais if col in df.columns]
        
        for i, (idx, row) in enumerate(df.iterrows(), 1):
            f.write(f"🌱 LINHA {i:02d}\n")
            f.write("-" * 30 + "\n")
            
            # Informações básicas
            f.write("📝 Dados de entrada:\n")
            if "Variedade" in row:
                f.write(f"   🌾 Variedade: {row['Variedade']}\n")
            if "Epoca" in row:
                epoca_icon = "☀️" if str(row['Epoca']).upper() == "SECA" else "🌧️"
                f.write(f"   {epoca_icon} Época: {row['Epoca']}\n")
            if "Processo" in row:
                processo_icon = "🚜" if "MECANIZADO" in str(row['Processo']).upper() else "👷"
                f.write(f"   {processo_icon} Processo: {row['Processo']}\n")
            if "Area_ha" in row:
                f.write(f"   📏 Área total: {row['Area_ha']:.2f} ha\n")
            if "Perc_Manobra_%" in row:
                f.write(f"   ⚙️ Perda por manobra: {row['Perc_Manobra_%']:.1f}%\n")
            if "Perc_Trafego_%" in row:
                f.write(f"   🚛 Perda por tráfego: {row['Perc_Trafego_%']:.1f}%\n")
            
            # Resultados calculados
            f.write("\n📊 Resultados calculados:\n")
            if "Area_efetiva_ha" in row and pd.notna(row['Area_efetiva_ha']):
                f.write(f"   🎯 Área efetiva: {row['Area_efetiva_ha']:.2f} ha\n")
            if "massa_escolhida_t_ha" in row and pd.notna(row['massa_escolhida_t_ha']):
                f.write(f"   ⚖️ Massa por hectare: {row['massa_escolhida_t_ha']:.3f} t/ha\n")
            if "massa_total_area_t" in row and pd.notna(row['massa_total_area_t']):
                f.write(f"   📦 Massa total da área: {row['massa_total_area_t']:.3f} t\n")
            
            # Status/Semáforo
            if "semaforo" in row and pd.notna(row['semaforo']):
                status_icon = "🟢" if row['semaforo'] == "OK" else "🟡" if row['semaforo'] == "ATENCAO" else "⚪"
                f.write(f"   {status_icon} Status: {row['semaforo']}\n")
            
            # Parâmetros técnicos (se disponíveis)
            params_tecnicos = ["E_usado", "G_final_usado", "s_usado", "g_to_usado", "L_to_usado", "rho_usado", "d_usado"]
            params_disponiveis = [p for p in params_tecnicos if p in row and pd.notna(row[p])]
            
            if params_disponiveis:
                f.write(f"\n🔧 Parâmetros técnicos utilizados:\n")
                for param in params_disponiveis:
                    valor = row[param]
                    nome_param = {
                        "E_usado": "Espaçamento (E)",
                        "G_final_usado": "Gemas finais (Gf)", 
                        "s_usado": "Gemas por tolete (s)",
                        "g_to_usado": "Gemas úteis (g)",
                        "L_to_usado": "Comprimento tolete (L)",
                        "rho_usado": "Densidade (rho)",
                        "d_usado": "Massa por metro (d)"
                    }.get(param, param)
                    f.write(f"   • {nome_param}: {valor}\n")
            
            f.write("\n")
        
        # Rodapé
        f.write("=" * 80 + "\n")
        f.write("💡 OBSERVAÇÕES:\n")
        f.write("• Este relatório foi gerado automaticamente pela Calculadora de Cana v8.3\n")
        f.write("• Os parâmetros técnicos são obtidos diretamente do banco Oracle\n")
        f.write("• Status 🟢 OK: dentro da tolerância | 🟡 ATENÇÃO: fora da tolerância\n")
        f.write("• Tolerâncias: Época Seca ≤ 5% | Época Chuva ≤ 8%\n")
        f.write("=" * 80 + "\n")

def menu_inicial(MAP_DISPLAY, PARAMS):
    while True:
        print("\n=== MENU ===")
        print("1) Ver catálogo de combinações")
        print("2) Ver glossário de parâmetros")
        print("3) Iniciar cálculos (nova execução)")
        print("4) Sair")
        op = input("Escolha uma opção [1-4]: ").strip()
        if op == "1":
            clear_screen()
            show_catalog(MAP_DISPLAY, PARAMS=PARAMS, page_size=20)
        elif op == "2":
            clear_screen()
            print_glossary()
        elif op == "3":
            return  # prossegue para o fluxo normal
        elif op == "4":
            raise SystemExit(0)
        else:
            print("Opção inválida. Tente novamente.")

def main():
    # 1) Carregar do Oracle (sem cache) + teste de conexão
    PARAMS, MAP_DISPLAY, TOL_CHUVA, TOL_SECA = load_params_from_oracle()

    print("=== Calculadora de Cana (CLI v8.3 – Oracle only) ===")
    print("Use o menu para consultar o catálogo e o glossário antes de começar.\n")

    # Menu inicial
    menu_inicial(MAP_DISPLAY, PARAMS)

    print("\nDica: durante a entrada, use :help, :help+ (ou :gloss) e :cat <texto>\n")

    # 2) Entrada e cálculos
    registros = []
    try:
        while True:
            print("-- Nova linha --")
            linha = {}
            linha["Area_ha"] = ask_float("Area_ha:", required=True, MAP_DISPLAY=MAP_DISPLAY, PARAMS=PARAMS, min_val=0.0001)
            linha["Perc_Manobra_%"] = ask_float("Perc_Manobra_%:", required=True, default=5.0, MAP_DISPLAY=MAP_DISPLAY, PARAMS=PARAMS, min_val=0, max_val=100, allow_zero=True)
            linha["Perc_Trafego_%"] = ask_float("Perc_Trafego_%:", required=True, default=3.0, MAP_DISPLAY=MAP_DISPLAY, PARAMS=PARAMS, min_val=0, max_val=100, allow_zero=True)
            # Solicitar variedade com verificação
            while True:
                variedade_digitada = ask_str("Variedade:", required=True, MAP_DISPLAY=MAP_DISPLAY, PARAMS=PARAMS)
                
                # Criar mapeamento de variedades (case-insensitive)
                variedades_map = {}  # {"ctc4": "CTC4", "rb867515": "RB867515", ...}
                variedades_originais = set()
                
                for disp in MAP_DISPLAY.values():
                    var_original = disp.get("Variedade", "").strip()
                    if var_original:
                        variedades_originais.add(var_original)
                        variedades_map[var_original.upper()] = var_original
                
                # Verificar se a variedade existe (case-insensitive)
                var_upper = variedade_digitada.upper()
                if var_upper in variedades_map:
                    # Usar o nome correto da variedade
                    linha["Variedade"] = variedades_map[var_upper]
                    break
                else:
                    print(f"❌ ERRO: Variedade '{variedade_digitada}' não encontrada no catálogo.")
                    print("📋 Variedades disponíveis:")
                    
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
                        print(f"� Sugestões baseadas em '{variedade_digitada}':")
                        for sug in sorted(sugestoes):
                            print(f"   ➤ {sug}")
                    
                    print("�💡 Dica: Use :cat <nome> para buscar variedades similares ou :cat para ver todas.")
                    continuar = input("Tentar novamente? (s/n) [default=s]: ").strip().lower()
                    if continuar == 'n':
                        print("Operação cancelada pelo usuário.")
                        return
            
            linha["Epoca"] = ask_str("Epoca (Seca/Chuva):", required=True, choices=["Seca","Chuva"], default="Chuva", MAP_DISPLAY=MAP_DISPLAY, PARAMS=PARAMS)
            linha["Processo"] = ask_str("Processo (Manual/Mecanizado):", required=True, choices=["Manual","Mecanizado"], default="Mecanizado", MAP_DISPLAY=MAP_DISPLAY, PARAMS=PARAMS)

            # Verificar se a combinação específica existe
            k = f"{linha['Variedade']}|{linha['Epoca']}|{linha['Processo']}"
            nk = norm_key(k)
            if nk not in PARAMS:
                print("⚠️  ATENÇÃO: Combinação específica Variedade|Epoca|Processo não encontrada.")
                print(f"   Combinação testada: {linha['Variedade']} | {linha['Epoca']} | {linha['Processo']}")
                
                # Mostrar combinações disponíveis para esta variedade
                print(f"📊 Combinações disponíveis para {linha['Variedade']}:")
                combinacoes_var = []
                for nk_test, disp in MAP_DISPLAY.items():
                    if disp.get("Variedade", "").upper() == linha["Variedade"].upper():
                        combinacoes_var.append(f"   • {disp['Variedade']} | {disp['Epoca']} | {disp['Processo']}")
                
                if combinacoes_var:
                    for comb in sorted(combinacoes_var):
                        print(comb)
                else:
                    print("   Nenhuma combinação encontrada para esta variedade.")
                
                print("💡 Dica: Use :cat para consultar o catálogo completo.\n")

            res = compute_row(linha, PARAMS, TOL_CHUVA, TOL_SECA)
            registros.append({**linha, **res})

            cont = ask_str("Adicionar outra linha? (s/n):", required=True, choices=["s","n"], default="n", MAP_DISPLAY=MAP_DISPLAY, PARAMS=PARAMS)
            if cont == "n":
                break
            print("")
    except KeyboardInterrupt:
        print("\nEncerrado a pedido do usuário. Prosseguindo com o que já foi inserido.")

    if not registros:
        print("Nenhum dado inserido. Encerrando.")
        return

    # 3) Montagem do DataFrame e resumo
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
    print("PRÉVIA DOS RESULTADOS")
    print("="*80)
    
    # Mostrar apenas as colunas mais importantes na prévia
    colunas_importantes = [
        "Variedade", "Epoca", "Processo", "Area_ha", "Area_efetiva_ha", 
        "massa_escolhida_t_ha", "massa_total_area_t", "semaforo"
    ]
    
    # Filtrar apenas colunas que existem no DataFrame
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

    print("\nResumo:")
    print(f"- Linhas: {resumo['linhas']}")
    print(f"- Soma Massa Total (t): {resumo['soma_massa_total']:.3f}")
    if resumo['media_massa_ha'] is not None:
        print(f"- Média Massa t/ha: {resumo['media_massa_ha']:.3f}")
    else:
        print("- Média Massa t/ha: -")
    print(f"- OK: {resumo['ok']} | ATENCAO: {resumo['atencao']} | N/A: {resumo['na']}")

    # 4) Exportação
    formato = ask_str("\nSalvar como (xlsx/csv/pdf/txt/all):", required=True, choices=["xlsx","csv","pdf","txt","all"], default="xlsx", MAP_DISPLAY=MAP_DISPLAY, PARAMS=PARAMS)
    nome = ask_str("Nome base do arquivo de saída (sem extensão):", required=False, default="Calculadora_resultados_cli", MAP_DISPLAY=MAP_DISPLAY, PARAMS=PARAMS)

    if formato in ("xlsx","all"):
        df.to_excel(f"{nome}.xlsx", index=False)
        print(f" - XLSX: {nome}.xlsx")
    if formato in ("csv","all"):
        df.to_csv(f"{nome}.csv", index=False)
        print(f" - CSV: {nome}.csv")
    if formato in ("pdf","all"):
        principais = ["Variedade","Epoca","Processo","Area_ha","Area_efetiva_ha","massa_escolhida_t_ha","massa_total_area_t","semaforo"]
        cols_pdf = [c for c in principais if c in df.columns]
        gerar_pdf(df[cols_pdf], resumo, saida_pdf=f"{nome}.pdf")
        print(f" - PDF: {nome}.pdf")
    if formato in ("txt","all"):
        gerar_txt(df, resumo, saida_txt=f"{nome}.txt")
        print(f" - TXT: {nome}.txt")

    print("\nConcluído.")

if __name__ == "__main__":
    main()
