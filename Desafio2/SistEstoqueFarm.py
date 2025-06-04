estoque = {}  # estoque começa vazio
pedido = {}   # pedido comeca vazio
rodando = True  # variável para fazer o programa rodar enquanto o usuário não quiser sair

# função para adicionar um medicamento ao estoque, não atualizá-lo.
def adicionarMedicamento(nome, quantidade):
    if nome in estoque: # Se o medicamento está no estoque, então informa ao usuário para que utilize a função de atualizar o estoque
        print("Este medicamento já existe no estoque, por favor use a opção de atualizar o estoque.")
    else:   #se não, coloca o novo medicamento e a quantidade no estoque.
        estoque[nome] = quantidade

def atualizarEstoque(nome, novaQtd):
    if nome in estoque: # Se o medicamento estiver no estoque, então atualiza-o
        estoque[nome] = novaQtd
    else: # Se não, informa ao usuário que precisa adicionar o medicamento primeiro.
        print("Esse medicamento não existe no estoque, favor usar a opção de adicionar um novo medicamento.")

def listar():
    if not estoque:  # Se estoque vazio então nao tem como listar.
        print("Estoque vazio.")
        return
    for nome, quantidade in estoque.items():    # Se estoque não vazio então listar todos os medicamentos
        print(f"{nome}: {quantidade} restantes") # e a quantidade de cada um deles no estoque.

def deletarMedicamento(nome):
    if nome in estoque: # Se o medicamento estiver no estoque, então deletar o medicamento
        del estoque[nome]
        print(f"Medicamento {nome} removido do estoque.")
    else:       #Se não, informa ao usuário que o medicamento não existe no estoque.
        print("Este medicamento não está no estoque.")

def processarPedido(pedido):
    if pedido["nome"] in estoque:
        if pedido["quantidade"] <= estoque[pedido["nome"]]:
            estoque[pedido["nome"]] -= pedido["quantidade"] # Se o medicamento existe e tem mais do que a quantidade do pedido
            print(f"Pedido processado: {pedido['quantidade']} unidades de {pedido['nome']}")    # então subtrairmos essa quantidade do estoque e informamos ao usuário.
        else:       # Se o medicamento existir mas não possui o suficiente para atender ao pedido.
            print("No estoque não há a quantidade suficiente para atender a este pedido.")
    else:  
        print("Este medicamento não está no estoque.")  # Se o medicamento não existir no estoque

def exibirResumo():
    print("\n=== RESUMO DO ESTOQUE ===")
    if not estoque: # Se não há nada no estoque, então mostra que o estoque está vazio
        print("Estoque vazio.")
        return
    
    # Se há algo no estoque, então 
    totalMedicamentos = len(estoque)   #Guardamos o total de medicamentos diversos no estoque
    totalUnidades = sum(estoque.values()) #Guardamos o total de unidades de todos os medicamentos
    
    print(f"Total de medicamentos diferentes: {totalMedicamentos}")
    print(f"Total de unidades em estoque: {totalUnidades}")
    print("\nDetalhamento:")
    listar()

def avisoCritico():
    print("\n=== AVISOS CRÍTICOS ===")
    avisosEncontrados = False   # Verificação para saber se há algum aviso.
    
    for nome, quantidade in estoque.items(): 
        if quantidade == 0: # Se em algum item do estoque a quantidade for 0 (o estoque não pode estar vazio)
            print(f"{nome}: ESGOTADO")  # aparecerá que o item está esgotado.
            avisosEncontrados = True    # alerta que há um aviso para ser mostrado.
        elif quantidade <= 5:   # Se algum item tiver menos do que 5 em sua quantidade, avisará que está em estado crítico.
            print(f"{nome}: ESTOQUE CRÍTICO ({quantidade} unidades)")
            avisosEncontrados = True
    
    if not avisosEncontrados:   # Se não for detectado nenhum aviso, então mostra que não há nenhum aviso
        print("Nenhum aviso crítico no momento.")

# Menu
while rodando:
    print("\n" + "="*50)
    print("SISTEMA DE CONTROLE DE ESTOQUE DE MEDICAMENTOS")
    print("="*50)
    print("O que você gostaria de fazer?")
    print("1 - Adicionar um novo medicamento")
    print("2 - Atualizar o estoque")
    print("3 - Listar medicamentos")
    print("4 - Deletar um medicamento")
    print("5 - Fazer um pedido")
    print("6 - Exibir resumo do estoque")
    print("7 - Verificar avisos críticos")
    print("0 - Sair")
    
    try:
        opcao = int(input("\nDigite sua opção: "))
        
        if opcao == 1:      # Se a opção for adicionar um novo medicamento
            nome = input("Nome do medicamento: ").strip()
            if not nome:    # Se o usuário não informou o nome
                print("Nome não pode estar vazio.")
                continue
            quantidade = int(input("Quantidade: "))
            if quantidade < 0:  # Se o usuário informou uma quantidade igual a zero ou negativa
                print("Quantidade não pode ser negativa ou igual a zero.")
                continue
            adicionarMedicamento(nome, quantidade)  # Caso esteja tudo válido então adiciona o medicamento
            
        elif opcao == 2:    # Caso seja selecionada a opção de atualizar a quantidade de um item do estoque
            nome = input("Nome do medicamento: ").strip()   #Remove os espaços em branco no inicio e fim da string.
            if not nome:    # Se o usuário não informou o nome
                print("Nome não pode estar vazio.")
                continue
            novaQtd = int(input("Nova quantidade: "))
            if novaQtd < 0: # Se o usuário informou uma quantidade inválida
                print("Quantidade não pode ser negativa.")
                continue
            atualizarEstoque(nome, novaQtd) # Se tudo for válido, o item será atualizado.
            
        elif opcao == 3:    # Se o usuário escolheu mostrar todos os medicamentos
            listar()    # Mostra todos os medicamentos
            
        elif opcao == 4:    # Se o usuário escolheu deletar um medicamento
            nome = input("Nome do medicamento para deletar: ").strip()
            if not nome:
                print("Nome não pode estar vazio.")
                continue
            deletarMedicamento(nome)    # Deleta o medicamento se tudo estiver válido
            
        elif opcao == 5:    # Se o usuário escolheu fazer um pedido
            nome = input("Nome do medicamento: ").strip()
            if not nome:
                print("Nome não pode estar vazio.")
                continue
            quantidade = int(input("Quantidade solicitada: "))
            if quantidade <= 0:
                print("Quantidade deve ser maior que zero.")
                continue
            pedido = {"nome": nome, "quantidade": quantidade}
            processarPedido(pedido) # Se tudo for válido então faz o processamento do pedido.
            
        elif opcao == 6:
            exibirResumo()  # Mostra o resumo do estoque
            
        elif opcao == 7:
            avisoCritico()  # Se o usuário quer checar se algum medicamento está em estado crítico ou não esyá mais no estoque
            
        elif opcao == 0:    # Se o usuário escolheu sair do programa.
            print("Encerrando o sistema.")
            rodando = False
            
        else:   # Se o usuário digitou uma opção inválida.
            print("Opção inválida. Tente novamente.")
            
    except ValueError:      # Caso uma opção inválida seja digitada
        print("Por favor, digite um número válido.")
    except Exception as e:  # Caso aconteça qualquer outro erro inesperado
        print(f"Erro inesperado: {e}")

print("Sistema encerrado.") 