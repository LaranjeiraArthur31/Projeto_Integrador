
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

SERVIDOR = "localhost"
USUARIO  = "root"
SENHA    = "senha"
BD       = "helpdesk"

#MENU 

def menu():
    print("\n" + "=" * 40)
    print("         HELP DESK SYSTEM")
    print("=" * 40)
    print("  1 - Cadastrar usuário")
    print("  2 - Abrir ticket")
    print("  3 - Listar tickets")
    print("  4 - Atualizar status do ticket")
    print("  5 - Ver histórico do ticket")
    print("  6 - Ver estatísticas")
    print("  0 - Sair")
    print("=" * 40)

#USUÁRIOS

def cadastrar_usuario():
    nome    = input("Nome: ").strip()
    email   = input("E-mail: ").strip()
    empresa = input("Empresa: ").strip()

    conn = obtemConexao(SERVIDOR, USUARIO, SENHA, BD)
    if not conn:
        return

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email, empresa) VALUES (%s, %s, %s)",
            (nome, email, empresa)
        )
        conn.commit()
        print(f"✔ Usuário '{nome}' cadastrado! (ID {cursor.lastrowid})")
    except Error as e:
        print(f"[ERRO] {e}")
    finally:
        cursor.close()
        conn.close()

def listar_usuarios(conn, cursor):
    """Utilitário: exibe usuários e retorna a lista."""
    cursor.execute("SELECT id, nome, email FROM usuarios ORDER BY nome")
    usuarios = cursor.fetchall()
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return []
    print("\n--- Usuários ---")
    for u in usuarios:
        print(f"  [{u[0]}] {u[1]} <{u[2]}>")
    return usuarios

#CATEGORIAS / PRIORIDADES / STATUS

def listar_opcoes(conn, cursor, tabela, campo="nome"):
    cursor.execute(f"SELECT id, {campo} FROM {tabela} ORDER BY id")
    rows = cursor.fetchall()
    print(f"\n--- {tabela.capitalize()} ---")
    for r in rows:
        print(f"  [{r[0]}] {r[1]}")
    return rows

#TICKETS

def abrir_ticket():
    conn = obtemConexao(SERVIDOR, USUARIO, SENHA, BD)
    if not conn:
        return

    try:
        cursor = conn.cursor()

        usuarios = listar_usuarios(conn, cursor)
        if not usuarios:
            return
        usuario_id = int(input("ID do usuário: "))

        titulo    = input("Título do ticket: ").strip()
        descricao = input("Descrição do problema: ").strip()

        cats = listar_opcoes(conn, cursor, "categorias")
        if not cats:
            print("Cadastre categorias no banco antes de abrir tickets.")
            return
        cat_id = int(input("ID da categoria: "))

        prios = listar_opcoes(conn, cursor, "prioridades", "nivel")
        if not prios:
            print("Cadastre prioridades no banco antes de abrir tickets.")
            return
        prio_id = int(input("ID da prioridade: "))

        # Status inicial = 1 (Aberto) 
        cursor.execute("SELECT id FROM estado WHERE nome = 'Aberta' LIMIT 1")
        row = cursor.fetchone()
        status_id = row[0] if row else 1

        agora = datetime.now()
        cursor.execute(
            """INSERT INTO tickets
               (titulo, descricao, categoria_id, prioridade_id, status_id,
                usuario_abertura_id, data_abertura, data_atualizacao)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (titulo, descricao, cat_id, prio_id, status_id, usuario_id, agora, agora)
        )
        ticket_id = cursor.lastrowid

        # Registra histórico inicial
        cursor.execute(
            """INSERT INTO ticket_historico (ticket_id, status_id, comentario, data)
               VALUES (%s, %s, %s, %s)""",
            (ticket_id, status_id, "Ticket aberto.", agora)
        )

        conn.commit()
        print(f"✔ Ticket #{ticket_id} criado com sucesso!")

    except Error as e:
        print(f"[ERRO] {e}")
    except ValueError:
        print("[ERRO] Entrada inválida.")
    finally:
        cursor.close()
        conn.close()

def listar_tickets():
    conn = obtemConexao(SERVIDOR, USUARIO, SENHA, BD)
    if not conn:
        return

    try:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT t.id, t.titulo, u.nome, c.nome, p.nivel, s.nome, t.data_abertura
               FROM tickets t
               JOIN usuarios   u ON u.id = t.usuario_abertura_id
               JOIN categorias c ON c.id = t.categoria_id
               JOIN prioridades p ON p.id = t.prioridade_id
               JOIN estado     s ON s.id = t.status_id
               ORDER BY t.id DESC"""
        )
        tickets = cursor.fetchall()

        if not tickets:
            print("Nenhum ticket encontrado.")
            return

        print("\n" + "=" * 70)
        print(f"{'ID':<5} {'Título':<25} {'Usuário':<15} {'Cat.':<12} {'Prior.':<10} {'Status':<12} {'Abertura'}")
        print("-" * 70)
        for t in tickets:
            dt = t[6].strftime("%d/%m/%Y %H:%M") if t[6] else "-"
            print(f"{t[0]:<5} {t[1][:24]:<25} {t[2][:14]:<15} {t[3][:11]:<12} {t[4][:9]:<10} {t[5][:11]:<12} {dt}")
        print("=" * 70)

    except Error as e:
        print(f"[ERRO] {e}")
    finally:
        cursor.close()
        conn.close()

def atualizar_status():
    conn = obtemConexao(SERVIDOR, USUARIO, SENHA, BD)
    if not conn:
        return

    try:
        cursor = conn.cursor()
        ticket_id = int(input("ID do ticket: "))

        # Verifica se existe
        cursor.execute("SELECT id, titulo FROM tickets WHERE id = %s", (ticket_id,))
        ticket = cursor.fetchone()
        if not ticket:
            print("Ticket não encontrado.")
            return
        print(f"Ticket: [{ticket[0]}] {ticket[1]}")

        statuses = listar_opcoes(conn, cursor, "estado")
        if not statuses:
            return
        novo_status_id = int(input("ID do novo status: "))

        comentario = input("Comentário (opcional): ").strip() or "Status atualizado."
        agora = datetime.now()

        cursor.execute(
            "UPDATE tickets SET status_id=%s, data_atualizacao=%s WHERE id=%s",
            (novo_status_id, agora, ticket_id)
        )

        # Fecha o ticket
        cursor.execute("SELECT nome FROM estado WHERE id=%s", (novo_status_id,))
        nome_status = cursor.fetchone()[0]
        if nome_status.lower() in ("resolvida", "fechada", "encerrada"):
            cursor.execute("UPDATE tickets SET data_fechamento=%s WHERE id=%s", (agora, ticket_id))

        cursor.execute(
            "INSERT INTO ticket_historico (ticket_id, status_id, comentario, data) VALUES (%s,%s,%s,%s)",
            (ticket_id, novo_status_id, comentario, agora)
        )

        conn.commit()
        print(f"✔ Status do ticket #{ticket_id} atualizado para '{nome_status}'.")

    except Error as e:
        print(f"[ERRO] {e}")
    except ValueError:
        print("[ERRO] Entrada inválida.")
    finally:
        cursor.close()
        conn.close()

def ver_historico():
    conn = obtemConexao(SERVIDOR, USUARIO, SENHA, BD)
    if not conn:
        return

    try:
        cursor = conn.cursor()
        ticket_id = int(input("ID do ticket: "))

        cursor.execute(
            """SELECT h.data, s.nome, h.comentario
               FROM ticket_historico h
               JOIN estado s ON s.id = h.status_id
               WHERE h.ticket_id = %s
               ORDER BY h.data""",
            (ticket_id,)
        )
        rows = cursor.fetchall()

        if not rows:
            print("Nenhum histórico encontrado para este ticket.")
            return

        print(f"\n===== Histórico — Ticket #{ticket_id} =====")
        for r in rows:
            dt = r[0].strftime("%d/%m/%Y %H:%M") if r[0] else "-"
            print(f"  {dt} | [{r[1]}] {r[2]}")
        print("=" * 40)

    except Error as e:
        print(f"[ERRO] {e}")
    except ValueError:
        print("[ERRO] Entrada inválida.")
    finally:
        cursor.close()
        conn.close()

#ESTATÍSTICAS 

def ver_estatisticas():
    conn = obtemConexao(SERVIDOR, USUARIO, SENHA, BD)
    if not conn:
        return

    try:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM tickets")
        total = cursor.fetchone()[0]

        cursor.execute(
            """SELECT s.nome, COUNT(*) as qtd
               FROM tickets t JOIN estado s ON s.id = t.status_id
               GROUP BY s.nome ORDER BY qtd DESC"""
        )
        por_status = cursor.fetchall()

        cursor.execute(
            """SELECT p.nivel, COUNT(*) as qtd
               FROM tickets t JOIN prioridades p ON p.id = t.prioridade_id
               GROUP BY p.nivel ORDER BY qtd DESC"""
        )
        por_prioridade = cursor.fetchall()

        cursor.execute(
            """SELECT c.nome, COUNT(*) as qtd
               FROM tickets t JOIN categorias c ON c.id = t.categoria_id
               GROUP BY c.nome ORDER BY qtd DESC"""
        )
        por_categoria = cursor.fetchall()

        print("\n" + "=" * 40)
        print("         ESTATÍSTICAS")
        print("=" * 40)
        print(f"  Total de tickets: {total}")

        print("\n  Por Status:")
        for r in por_status:
            print(f"    {r[0]:<20} {r[1]}")

        print("\n  Por Prioridade:")
        for r in por_prioridade:
            print(f"    {r[0]:<20} {r[1]}")

        print("\n  Por Categoria:")
        for r in por_categoria:
            print(f"    {r[0]:<20} {r[1]}")

        print("=" * 40)

    except Error as e:
        print(f"[ERRO] {e}")
    finally:
        cursor.close()
        conn.close()

#FECHAR CONEXAO
def fechaConexao():
    return

#LOOP PRINCIPAL 

def main():
    while True:
        menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            abrir_ticket()
        elif opcao == "3":
            listar_tickets()
        elif opcao == "4":
            atualizar_status()
        elif opcao == "5":
            ver_historico()
        elif opcao == "6":
            ver_estatisticas()
        elif opcao == "0":
            print("Saindo do sistema. Até logo!")
            fechaConexao()
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()