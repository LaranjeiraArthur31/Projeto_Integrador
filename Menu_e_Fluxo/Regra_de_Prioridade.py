import mysql.connector
from mysql.connector import Error

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
# regras do sistema

print("1)TI")
print("2)RH")
print("3)Financeiro")
print("4)Administrativo")

while True:
    try:
        opcao = int(input('Qual o problema? '))

        if opcao == 1:
            tipo = "TI"
            break
        elif opcao == 2:
            tipo = "RH"
            break
        elif opcao == 3:
            tipo = "Financeiro"
            break
        elif opcao == 4:
            tipo = "Administrativo"
            break
        else:
            print("Deve ser entre 1 e 4!")
    except:
        print("Digite apenas números!")
print("Tipo escolhido:", tipo)

print("\nEscolha o status:")

print("1) Abrir(utilizada no início do processo, quando o chamado acabou de ser criado)")
print("2) Em andamento(quando o chamado já está sendo analisado pelo suporte)")
print("3) Fechada(quando o atendimento foi concluído)")

while True:
    try:
        opcaoS = int(input("Escolha o status: "))

        if opcaoS == 1:
            status = "Aberta"
            break
        elif opcaoS == 2:
            status = "Em andamento"
            break
        elif opcaoS == 3:
            status = "Fechada"
            break
        else:
            print("Deve ser entre 1 e 3!")
    except:
        print("Digite apenas números!")
print("Status escolhido:", status)


# EXIBINDO OS DADOS
print("Tipo escolhido:", tipo)
print("Status:", status)


# FUNÇÃO PARA CALCULAR PRIORIDADE
def calcular_prioridade(urgencia, impacto):
    prioridade = urgencia + impacto

    if prioridade <= 2:
        nivel = "Baixa"
    elif prioridade <= 4:
        nivel = "Média"
    else:
        nivel = "Alta"

    return prioridade, nivel

# urgência
while True:
    try:
        urgencia = int(input("\nDigite a urgência (1 a 3): "))
        if 1 <= urgencia <= 3:
            break
        else:
            print("Digite um valor entre 1 e 3!")
    except:
        print("Digite apenas números!")

# impacto
while True:
    try:
        impacto = int(input("Digite o impacto (1 a 3): "))
        if 1 <= impacto <= 3:
            break
        else:
            print("Digite um valor entre 1 e 3!")
    except:
        print("Digite apenas números!")


#PRIORIDADE
resultado, nivel = calcular_prioridade(urgencia, impacto)

print("\nUrgência:", urgencia)
print("Impacto:", impacto)
print("Prioridade:", resultado)
print("Nível de prioridade:", nivel)


def fechaConexao():
    conexao = obtemConexao(
        "172.16.12.14",
        "XXXXX",
        "YYYYY",
        "XXXXX"
    )

    conexao.close()
