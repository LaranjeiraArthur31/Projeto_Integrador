import mysql.connector
from mysql.connector import Error
from datetime import datetime

def obtemConexao(servidor, usuario, senha, bd):
    return mysql.connector.connect(
        host=servidor,
        user=usuario,
        password=senha,
        database=bd
    )

SERVIDOR = 'BD-ACD'
USUARIO  = "BD24022611"
SENHA    = "Ldxti2"
BD       = "BD24022611"


# FUNÇÕES AUXILIARES DE ENTRADA


def escolher_opcao_menu(opcoes_dict, titulo):
    print(f"\n--- {titulo} ---")
    for k, v in opcoes_dict.items():
        print(f"  {k}) {v}")
    while True:
        try:
            opcao = int(input("Escolha uma opção: "))
            if opcao in opcoes_dict:
                return opcao
            print(f"Deve ser entre {min(opcoes_dict)} e {max(opcoes_dict)}!")
        except ValueError:
            print("Digite apenas números!")

def buscar_opcoes_banco(cursor, tabela, campo="nome"):
    cursor.execute(f"SELECT id, {campo} FROM {tabela} ORDER BY id")
    rows = cursor.fetchall()
    return {r[0]: r[1] for r in rows}

def escolher_urgencia():
    print("\n--- Urgência ---")
    while True:
        try:
            valor = int(input("Digite a urgência (1 a 3): "))
            if 1 <= valor <= 3:
                return valor
            print("Digite um valor entre 1 e 3!")
        except ValueError:
            print("Digite apenas números!")

def escolher_impacto():
    print("\n--- Impacto ---")
    while True:
        try:
            valor = int(input("Digite o impacto (1 a 3): "))
            if 1 <= valor <= 3:
                return valor
            print("Digite um valor entre 1 e 3!")
        except ValueError:
            print("Digite apenas números!")


# CÁLCULO DE PRIORIDADE


def calcular_prioridade(urgencia, impacto):
    soma = urgencia + impacto
    if soma <= 2:
        nivel = "Baixa"
    elif soma <= 4:
        nivel = "Média"
    else:
        nivel = "Alta"
    return nivel


# ABERTURA DO CHAMADO


def abrir_chamado():
    conn = obtemConexao(SERVIDOR, USUARIO, SENHA, BD)
    try:
        cursor = conn.cursor()

        # Usuário
        usuarios = buscar_opcoes_banco(cursor, "usuarios", "nome")
        if not usuarios:
            print("Nenhum usuário cadastrado. Cadastre um usuário primeiro.")
            return
        usuario_id = escolher_opcao_menu(usuarios, "Selecione o usuário")

        # Título e descrição
        titulo = input("\nTítulo do chamado: ").strip()
        if not titulo:
            titulo = "Sem título informado."
        descricao = input("Descrição do problema: ").strip()
        if not descricao:
            descricao = "Sem descrição informada."

        # Categoria (tipo do problema)
        categorias = buscar_opcoes_banco(cursor, "categorias")
        if not categorias:
            print("Nenhuma categoria cadastrada no banco.")
            return
        categoria_id = escolher_opcao_menu(categorias, "Tipo do problema")

        # Urgência e impacto → calcula nível de prioridade
        urgencia = escolher_urgencia()
        impacto  = escolher_impacto()
        nivel    = calcular_prioridade(urgencia, impacto)

        # Busca o id da prioridade correspondente ao nível calculado
        cursor.execute("SELECT id FROM prioridades WHERE nivel = %s LIMIT 1", (nivel,))
        row = cursor.fetchone()
        if not row:
            print(f"[ERRO] Prioridade '{nivel}' não encontrada na tabela prioridades.")
            return
        prioridade_id = row[0]

        # Status
        statuses = buscar_opcoes_banco(cursor, "status")
        if not statuses:
            print("Nenhum status cadastrado no banco.")
            return
        print("\n--- Status do chamado ---")
        print("  (pressione Enter para 'Aberta' automaticamente)")
        for k, v in statuses.items():
            print(f"  {k}) {v}")
        while True:
            try:
                entrada = input("Escolha o status (ou Enter para Aberta): ").strip()
                if entrada == "":
                    cursor.execute("SELECT id FROM status WHERE nome = 'Aberta' LIMIT 1")
                    row = cursor.fetchone()
                    if not row:
                        print("[ERRO] Status 'Aberta' não encontrado no banco.")
                        return
                    status_id   = row[0]
                    status_nome = "Aberta"
                    break
                opcaoS = int(entrada)
                if opcaoS in statuses:
                    status_id   = opcaoS
                    status_nome = statuses[opcaoS]
                    break
                print(f"Deve ser entre {min(statuses)} e {max(statuses)}!")
            except ValueError:
                print("Digite apenas números!")

        # Resumo 
        print("\n" + "=" * 42)
        print("           RESUMO DO CHAMADO")
        print("=" * 42)
        print(f"  Usuário......: {usuarios[usuario_id]}")
        print(f"  Título.......: {titulo}")
        print(f"  Descrição....: {descricao}")
        print(f"  Categoria....: {categorias[categoria_id]}")
        print(f"  Urgência.....: {urgencia}  |  Impacto: {impacto}")
        print(f"  Prioridade...: {nivel}")
        print(f"  Status.......: {status_nome}")
        print("=" * 42)

        confirma = input("\nConfirmar abertura do chamado? (S/N): ").strip().upper()
        if confirma != "S":
            print("Chamado cancelado.")
            return

        # INSERT no banco
        agora = datetime.now()
        cursor.execute(
            """INSERT INTO tickets
               (titulo, descricao, categoria_id, prioridade_id, status_id,
                usuario_abertura_id, data_abertura, data_atualizacao)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (titulo, descricao, categoria_id, prioridade_id, status_id,
             usuario_id, agora, agora)
        )
        ticket_id = cursor.lastrowid

        # Registra histórico inicial
        cursor.execute(
            """INSERT INTO ticket_historico (ticket_id, status_id, comentario, data)
               VALUES (%s, %s, %s, %s)""",
            (ticket_id, status_id, "Chamado aberto.", agora)
        )

        conn.commit()
        print(f"\n✔ Chamado #{ticket_id} registrado com sucesso!")

    except Error as e:
        print(f"[ERRO] {e}")
    except ValueError:
        print("[ERRO] Entrada inválida.")
    finally:
        cursor.close()
        conn.close()

 
# PROGRAMA PRINCIPAL
 

def main():
    print("\n" + "=" * 42)
    print("         ABERTURA DE CHAMADO")
    print("=" * 42)
    abrir_chamado()

if __name__ == "__main__":
    main()
