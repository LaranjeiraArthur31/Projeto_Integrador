
#Menu e Fluxo

usuarios = []
solicitacoes = []
id_solicitacao = 1

def menu():
    print("\n===== HELP DESK =====")
    print("1 - Cadastrar usuário")
    print("2 - Abrir solicitação")
    print("3 - Listar solicitações")
    print("4 - Atualizar status")
    print("5 - Ver estatísticas")
    print("0 - Sair")

def cadastrar_usuario():
    nome = input("Digite o nome do usuário: ")
    usuarios.append(nome)
    print(f"Usuário '{nome}' cadastrado com sucesso!")

def abrir_solicitacao():
    global id_solicitacao

    if not usuarios:
        print("Nenhum usuário cadastrado!")
        return

    print("Usuários disponíveis:")
    for i, u in enumerate(usuarios):
        print(f"{i} - {u}")

    indice = int(input("Escolha o usuário: "))
    descricao = input("Descreva o problema: ")

    solicitacao = {
        "id": id_solicitacao,
        "usuario": usuarios[indice],
        "descricao": descricao,
        "status": "Aberta"
    }

    solicitacoes.append(solicitacao)
    print(f"Solicitação {id_solicitacao} criada com sucesso!")
    id_solicitacao += 1

def listar_solicitacoes():
    if not solicitacoes:
        print("Nenhuma solicitação encontrada.")
        return

    print("\n===== SOLICITAÇÕES =====")
    for s in solicitacoes:
        print(f"ID: {s['id']} | Usuário: {s['usuario']} | Status: {s['status']}")
        print(f"Descrição: {s['descricao']}")
        print("-" * 40)

def atualizar_status():
    if not solicitacoes:
        print("Nenhuma solicitação disponível.")
        return

    listar_solicitacoes()
    id_busca = int(input("Digite o ID da solicitação: "))

    for s in solicitacoes:
        if s["id"] == id_busca:
            print("1 - Aberta")
            print("2 - Em andamento")
            print("3 - Resolvida")
            opcao = input("Novo status: ")

            if opcao == "1":
                s["status"] = "Aberta"
            elif opcao == "2":
                s["status"] = "Em andamento"
            elif opcao == "3":
                s["status"] = "Resolvida"
            else:
                print("Opção inválida!")
                return

            print("Status atualizado com sucesso!")
            return

    print("Solicitação não encontrada.")

def ver_estatisticas():
    total = len(solicitacoes)
    abertas = sum(1 for s in solicitacoes if s["status"] == "Aberta")
    andamento = sum(1 for s in solicitacoes if s["status"] == "Em andamento")
    resolvidas = sum(1 for s in solicitacoes if s["status"] == "Resolvida")

    print("\n===== ESTATÍSTICAS =====")
    print(f"Total: {total}")
    print(f"Abertas: {abertas}")
    print(f"Em andamento: {andamento}")
    print(f"Resolvidas: {resolvidas}")

# LOOP PRINCIPAL
while True:
    menu()
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cadastrar_usuario()
    elif opcao == "2":
        abrir_solicitacao()
    elif opcao == "3":
        listar_solicitacoes()
    elif opcao == "4":
        atualizar_status()
    elif opcao == "5":
        ver_estatisticas()
    elif opcao == "0":
        print("Saindo do sistema...")
        break
    else:
        print("Opção inválida!")