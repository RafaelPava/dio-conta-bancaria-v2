# Desafio DIO - Conta bancária com funções - Rafael Inocente Pavão

contas_existentes = []
conta_logada = None

def criar_usuario(nome, data_nascimento, cpf, endereco):
    while cpf == "" or not cpf.isdigit() or len(cpf) != 11:
        print("CPF inválido. Por favor, tente novamente.")
        cpf = input("CPF (somente números): ")

    for conta in contas_existentes:
        if int(cpf) == conta['usuario']['cpf']:
            print("Já existe um usuário cadastrado com esse CPF.")
            return None
        
    confirmacao = input(f"Deseja continuar?\nNome: {nome}\nData de Nascimento: {data_nascimento}\nCPF: {cpf}\nEndereço: {endereco}\nS - Continuar\nN - Cancelar\n")
    
    if confirmacao.upper() == "N":
        return None
    elif confirmacao.upper() == "S":
        usuario = {
            "nome" : nome,
            "data_nascimento" : data_nascimento,
            "cpf" : int(cpf),
            "endereco" : endereco
        }
        criar_conta_corrente(usuario)
    else:
        print("Opção inválida, por favor tente novamente.")
        criar_usuario(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

def criar_conta_corrente(usuario):
    AGENCIA = "0001"   
    
    if len(contas_existentes) == 0:
        conta = {
            "agencia": AGENCIA,
            "numero_conta": 1,
            "usuario": usuario,
            "saldo": 0.0,
            "extrato": ""
        }
    else:
        conta = {
            "agencia": AGENCIA,
            "numero_conta": contas_existentes[-1]["numero_conta"] + 1,
            "usuario": usuario,
            "saldo": 0.0,
            "extrato": ""
        }
    contas_existentes.append(conta)
    print(f"Conta criada com sucesso! Número da conta: {conta['numero_conta']}, Agência: {conta['agencia']}")

def saque(*, saldo=0.0, valor=0.0, extrato="", limite=500.0, numero_saques=0, limite_saques=3):
    excedeu_saldo = valor > saldo

    excedeu_limite = valor > limite

    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
        return saldo, extrato, numero_saques

    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
        return saldo, extrato, numero_saques

    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
        return saldo, extrato, numero_saques

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque realizado com sucesso!")
        print(f"Saldo atual: R${saldo:.2f}")
        return saldo, extrato, numero_saques
    else:
        print("Operação falhou! O valor informado é inválido.")
        return saldo, extrato, numero_saques


def deposito(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("Depósito realizado com sucesso!")
        print(f"Saldo atual: R${saldo:.2f}")
        return saldo, extrato
    else:
        print("Operação falhou! O valor informado é inválido.")
        return saldo, extrato

def exibir_extrato(saldo, /, *, extrato = "Não foram realizadas movimentações."):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def operacoes(conta_logada):
    menu = """

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair

    => """

    limite = 500.0
    numero_saques = 0
    LIMITE_SAQUES = 3

    while True:

        opcao = input(menu)

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            conta_logada['saldo'], conta_logada['extrato'] = deposito(conta_logada['saldo'], valor, conta_logada['extrato'])

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            conta_logada['saldo'], conta_logada['extrato'], numero_saques = saque(saldo=conta_logada['saldo'], valor=valor, extrato=conta_logada['extrato'], limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)        

        elif opcao == "e":
            exibir_extrato(conta_logada['saldo'], extrato=conta_logada['extrato'])

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

def main():
    global contas_existentes, conta_logada

    while True:
        if conta_logada == None:
            print("********** Bem-vindo ao Banco DIO! **********\n")
            print("1. Criar usuário")
            print("2. Já possui uma conta? Clique aqui!")
            print("3. Sair")
            print("**********************************************\n")

            opcao = input("Selecione uma opção: ")

            if opcao == "1":
                print("Criando usuário...")
                numero_de_contas = len(contas_existentes)
                criar_usuario(nome=input("Nome: "), data_nascimento=input("Data de Nascimento (xx/xx/xxxx): "), cpf=input("CPF (somente números): "), endereco=input("Endereço (logradouro - número - bairro - cidade/sigla do estado): "))
                if len(contas_existentes) == numero_de_contas:
                    print("Usuário não cadastrado, por favor tente novamente.")
                    continue
                else:
                    print(f"Usuário criado com sucesso!")
            
            elif opcao == "2":
                cpf = input("Informe o CPF para login: ")
                if cpf == "" or not cpf.isdigit() or len(cpf) != 11:
                    print("CPF inválido. Por favor, tente novamente.")
                    continue
                for conta in contas_existentes:
                    if int(cpf) == conta['usuario']['cpf']:
                        conta_logada = conta
                        print(f"Login efetuado com sucesso.\nBem-vindo(a), {conta_logada['usuario']['nome']}!")
                        break
                else:
                    print("Usuário não encontrado. Por favor, verifique o CPF e tente novamente.")

            elif opcao == "3":
                print("Obrigado por usar o Banco DIO!")
                conta_logada = None
                break

            else:
                print("Opção inválida, tente novamente.")

        else:
            print(f"********** Bem-vindo {conta_logada['usuario']['nome']}, ao Banco DIO! **********\n")
            print("1. Realizar operações")
            print("2. Desconectar")
            print("**********************************************\n")

            opcao = input("Selecione uma opção: ")

            if opcao == "1":
                operacoes(conta_logada)

            elif opcao == "2":
                print(f"Obrigado por usar o Banco DIO {conta_logada['usuario']['nome']}!")
                conta_logada = None
                continue

            else:
                print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()