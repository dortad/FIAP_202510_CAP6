# Importação dos módulos
import os
import oracledb
import pandas as pd

''' comando no oracle
DROP TABLE parametros;

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

# Try para tentativa de Conexão com o Banco de Dados
try:
    # Efetua a conexão com o Usuário no servidor
    conn = oracledb.connect(user='RM567007', password='Fiap#2025', dsn='oracle.fiap.com.br:1521/ORCL')
    # Cria as instruções para cada módulo
    inst_cadastro = conn.cursor()
    inst_consulta = conn.cursor()
    inst_alteracao = conn.cursor()
    inst_exclusao = conn.cursor()
except Exception as e:
    # Informa o erro
    print("Erro: ", e)
    # Flag para não executar a Aplicação
    conexao = False
else:
    # Flag para executar a Aplicação
    conexao = True

margem = ' ' * 4  # Define uma margem para a exibição da aplicação

# Enquanto o flag conexao estiver apontado com True
while conexao:
    # Limpa a tela via SO
    os.system('cls')
    # Apresenta o menu
    print("------- CRUD - Parametros -------")
    print("""
1 - Cadastrar Parametro    
2 - Listar Parametros
3 - Alterar Parametro
4 - Excluir Parametro
5 - EXCLUIR TODOS OS PARAMETROS
6 - SAIR
""")
    # Captura a escolha do usuário
    escolha = input(margem + "Escolha -> ")
    # Verifica se o número digitado é um valor numérico
    if escolha.isdigit():
        escolha = int(escolha)
    else:
        escolha = 6
        print("Digite um número.\nReinicie a Aplicação!")
    os.system('cls')  # Limpa a tela via SO
    # VERIFICA QUAL A ESCOLHA DO USUÁRIO
    match escolha:
        # CADASTRAR UM PARAMETRO
        case 1:
            try:
                print("----- CADASTRAR PARAMETRO -----\n")
                # Recebe os valores para cadastro
                variedade = input(margem + "Digite a variedade...: ")
                epoca = input(margem + "Digite a epoca.......: ")
                processo = input(margem + "Digite o processo....: ")
                e_rec_m = float(input(margem + "Digite e_rec_m.......: "))
                g_final_rec = int(input(margem + "Digite g_final_rec...: "))
                s_rec = float(input(margem + "Digite s_rec.........: "))
                g_to_rec = float(input(margem + "Digite g_to_rec......: "))
                l_to_rec = float(input(margem + "Digite l_to_rec......: "))
                rho_rec = float(input(margem + "Digite rho_rec.......: "))
                d_rec_kg_m = float(input(margem + "Digite d_rec_kg_m....: "))
                # Monta a instrução SQL de cadastro em uma string
                cadastro = f""" INSERT INTO parametros (variedade, epoca, processo, e_rec_m, g_final_rec, s_rec, g_to_rec, l_to_rec, rho_rec, d_rec_kg_m)
                               VALUES ('{variedade}', '{epoca}', '{processo}', {e_rec_m}, {g_final_rec}, {s_rec}, {g_to_rec}, {l_to_rec}, {rho_rec}, {d_rec_kg_m}) """
                # Executa e grava o Registro na Tabela
                inst_cadastro.execute(cadastro)
                conn.commit()
            except ValueError:
                # Erro de número não digitar um número nos campos numéricos
                print("Digite valores numéricos válidos nos campos apropriados!")
            except Exception as e:
                # Caso ocorra algum erro de conexão ou no BD
                print("Erro na transação do BD")
                # Informa o erro
                print("Erro: ", e)
            else:
                # Caso haja sucesso na gravação
                print("\n##### Parametro GRAVADO #####")

        # LISTAR TODOS OS PARAMETROS
        case 2:
            print("----- LISTAR PARAMETROS -----\n")
            lista_dados = []  # Lista para captura de dados do Banco
            # Monta a instrução SQL de seleção de todos os registros da tabela
            inst_consulta.execute('SELECT * FROM parametros')
            # Captura todos os registros da tabela e armazena no objeto data
            data = inst_consulta.fetchall()
            # Insere os valores da tabela na Lista
            for dt in data:
                lista_dados.append(dt)
            # ordena a lista
            lista_dados = sorted(lista_dados)
            # Gera um DataFrame com os dados da lista utilizando o Pandas
            dados_df = pd.DataFrame.from_records(lista_dados,
                                               columns=['Variedade', 'Epoca', 'Processo', 'E_rec_m', 'G_final_rec', 'S_rec', 'G_to_rec', 'L_to_rec', 'Rho_rec', 'D_rec_kg_m'])
            # Verifica se não há registro através do dataframe
            if dados_df.empty:
                print(f"Não há Parametros cadastrados!")
            else:
                print(dados_df)  # Exibe os dados selecionados da tabela
            print("\n##### PARAMETROS LISTADOS! #####")

        # ALTERAR OS DADOS DE UM REGISTRO
        case 3:
            try:
                # ALTERANDO UM REGISTRO
                print("----- ALTERAR DADOS DO PARAMETRO -----\n")
                lista_dados = []  # Lista para captura de dados da tabela
                # Chave composta: variedade, epoca, processo
                variedade_busca = input(margem + "Digite a variedade para buscar: ")
                epoca_busca = input(margem + "Digite a epoca para buscar: ")
                processo_busca = input(margem + "Digite o processo para buscar: ")
                # Constrói a instrução de consulta para verificar a existência ou não do registro
                consulta = f""" SELECT * FROM parametros WHERE variedade = '{variedade_busca}' AND epoca = '{epoca_busca}' AND processo = '{processo_busca}'"""
                inst_consulta.execute(consulta)
                data = inst_consulta.fetchall()
                # Preenche a lista com o registro encontrado (ou não)
                for dt in data:
                    lista_dados.append(dt)
                # analisa se foi encontrado algo
                if len(lista_dados) == 0:  # se não há o registro
                    print(f"Não há parametro cadastrado com Variedade={variedade_busca}, Epoca={epoca_busca}, Processo={processo_busca}")
                    input("\nPressione ENTER")
                else:
                    # Captura os novos dados (apenas campos não-chave)
                    novo_e_rec_m = float(input(margem + "Digite novo e_rec_m: "))
                    novo_g_final_rec = int(input(margem + "Digite novo g_final_rec: "))
                    novo_s_rec = float(input(margem + "Digite novo s_rec: "))
                    novo_g_to_rec = float(input(margem + "Digite novo g_to_rec: "))
                    novo_l_to_rec = float(input(margem + "Digite novo l_to_rec: "))
                    novo_rho_rec = float(input(margem + "Digite novo rho_rec: "))
                    novo_d_rec_kg_m = float(input(margem + "Digite novo d_rec_kg_m: "))
                    # Constrói a instrução de edição do registro com os novos dados
                    alteracao = f"""
                        UPDATE parametros SET e_rec_m={novo_e_rec_m}, g_final_rec={novo_g_final_rec}, 
                        s_rec={novo_s_rec}, g_to_rec={novo_g_to_rec}, l_to_rec={novo_l_to_rec}, 
                        rho_rec={novo_rho_rec}, d_rec_kg_m={novo_d_rec_kg_m} 
                        WHERE variedade='{variedade_busca}' AND epoca='{epoca_busca}' AND processo='{processo_busca}'
                    """
                    inst_alteracao.execute(alteracao)
                    conn.commit()
            except ValueError:
                print("Digite valores numéricos válidos!")
            except Exception as e:
                print(margem + "Erro na transação do BD")
                print("Erro: ", e)
            else:
                print("\n##### Parametro ATUALIZADO! #####")

        # EXCLUIR UM REGISTRO
        case 4:
            print("----- EXCLUIR PARAMETRO -----\n")
            lista_dados = []  # Lista para captura de dados da tabela
            # Chave composta: variedade, epoca, processo
            variedade_excluir = input(margem + "Digite a variedade para excluir: ")
            epoca_excluir = input(margem + "Digite a epoca para excluir: ")
            processo_excluir = input(margem + "Digite o processo para excluir: ")
            
            consulta = f""" SELECT * FROM parametros WHERE variedade = '{variedade_excluir}' AND epoca = '{epoca_excluir}' AND processo = '{processo_excluir}'"""
            inst_consulta.execute(consulta)
            data = inst_consulta.fetchall()
            # Insere os valores da tabela na lista
            for dt in data:
                lista_dados.append(dt)
            # Verifica se o registro está cadastrado
            if len(lista_dados) == 0:
                print(f"Não há parametro cadastrado com Variedade={variedade_excluir}, Epoca={epoca_excluir}, Processo={processo_excluir}")
            else:
                # Cria a instrução SQL de exclusão pela chave composta
                exclusao = f"DELETE FROM parametros WHERE variedade='{variedade_excluir}' AND epoca='{epoca_excluir}' AND processo='{processo_excluir}'"
                # Executa a instrução e atualiza a tabela
                inst_exclusao.execute(exclusao)
                conn.commit()
                print("\n##### Parametro APAGADO! #####")  # Exibe mensagem caso haja sucesso

        # EXCLUIR TODOS OS REGISTROS
        case 5:
            print("\n!!!!! EXCLUI TODOS OS DADOS DA TABELA !!!!!!\n")
            confirma = input(margem + "CONFIRMA A EXCLUSÃO DE TODOS OS PARAMETROS? [S]im ou [N]ÃO? ")
            if confirma.upper() == "S":
                # Apaga todos os registros
                exclusao = "DELETE FROM parametros"
                inst_exclusao.execute(exclusao)
                conn.commit()
                print("##### Todos os parametros foram excluídos! #####")
            else:
                print(margem + "Operação cancelada pelo usuário!")

        # SAI DA APLICAÇÃO
        case 6:
            # Modificando o flag da conexão
            conexao = False

        # CASO O NUMERO DIGITADO NÃO SEJA UM DO MENU
        case _:
            input(margem + "Digite um número entre 1 e 6.")

    # Pausa o fluxo da aplicação para a leitura das informações
    input(margem + "Pressione ENTER")
else:
    print("Obrigado por utilizar a nossa aplicação! :)")