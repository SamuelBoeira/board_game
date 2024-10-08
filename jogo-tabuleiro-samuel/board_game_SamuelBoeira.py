#Autor: Samuel Boeira Dantas
#Componenete curricula: 2024.1 EXA854 - MI - ALGORITMOS (TP04)
#Concluído em: 07/07/2024
#Declaro que este código foi elaborado por mim de forma individual e não contém nenhum techo de código 
#de outro colega ou de outro autor, tais como provindos de livros e apostilas, e páginas de documentos
#eletrônicos da internet. Qualquer trecho de código de outra autoria que não a minha está destacado com
#uma citação para o autor e a fonte do código, e estou ciente que esses techaos não serão considerados 
#para fins de avaliação.

import random
import csv
from tabulate import tabulate

Player = True


# função que torna aleatória a entrega de objetivos para cada jogador 
def mission():
    objective = random.randint(1, 4)
    if objective == 1:
        mission = 'Sequência Ascendente'
    elif objective == 2:
        mission = 'Sequência Descendente'
    elif objective == 3:
        mission = 'Sequência Pares'
    elif objective == 4:
        mission = 'Sequência Ímpares'  
    return mission


# função que entrega os objetivos 
def deliver_mission(Player, ob1, ob2):
    if Player:
        print(f'O objetivo do jogador 1 é: {ob1}.')
        proceed = input('Objetivo entregue. Pressione ENTER para seguir. ')
        if proceed == '':
            Player = False
            print("\n" * 130)
    if not Player:
        print(f'O objetivo do jogador 2 é: {ob2}.')
        proceed = input('Objetivo entregue. Pressione ENTER para seguir. ')
        if proceed == '':
            Player = True
            print("\n" * 130)

#pergunta se o jogo será com jogada especial
def special_option():
    choice = input("Deseja jogar com jogada especial(s/n): ")
    if choice == 's' or choice == 'S':
        return True, True
    else:
        return False, False


# função suporte que corta as listas de possíveis vitórias para a quantidade ideal de acordo com o tamanho do tabuleiro
def cut(list, index):
    match index:
        case 3:
            return [i for i in list if i <= 9]
        case 4:
            return [i for i in list if i <= 16]
        case 5:
            return [i for i in list if i <= 25]


# função que identifica todos os números que podem estar contidos naquele tipo de objetivo 
def objective_series(objective, index):
    if objective == 'Sequência Pares':
        pair = [2,4,6,8,10,12,14,16,18,20,22,24]
        objective_list = cut(pair, index)

    elif objective == 'Sequência Ímpares':
        odd = [1,3,5,7,9,11,13,15,17,19,21,23,25]
        objective_list = cut(odd, index)

    elif objective == 'Sequência Ascendente':
        upward = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
        objective_list = cut(upward, index)

    elif objective == 'Sequência Descendente':
        downward = [25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]
        objective_list = cut(downward, index)
        
    return objective_list

# função que cria todas as possíveis vitórias de acordo com o objetivo as devolve
def possible_win(mission, objective, index):
    sequence = []
    for turn in range(len(objective)):
        if turn > len(objective) - index:
                return sequence
        combination = []
        combination2 = []
        for j in range(index):
            combination.append(objective[turn+j])
            combination2.append(objective[turn+j])
        combination2.reverse()
        sequence.append(combination)
        if mission == 'Sequência Pares' or mission == 'Sequência Ímpares':
            sequence.append(combination2)


# função que cria uma tabela de acordo com a dificuldade selecionada
def generate_table(size):
    if size == 3:
        usable_num = list(range(1, 10))
    elif size == 4:
        usable_num = list(range(1, 17))
    elif size == 5:
        usable_num = list(range(1, 26))
    matriz = []
    color_matriz = []
    for l in range(size):
        line = []
        for c in range(size):
            line.append(' ')
        matriz.append(line.copy())
        color_matriz.append(line.copy())
    print(tabulate(color_matriz, headers="firstrow", tablefmt="heavy_grid"))
    return color_matriz, matriz, usable_num


# as funções a seguir checam as linhas, colunas e diagonais de acordo com a última jogada feita, 
# priorizando apenas os possíveis espaços que podem ocasionar em vitória
def CheckLine(ob1, ob2, table, line):
    if table[line] in ob1 and table[line] in ob2:
        return 'draw'
    if table[line] in ob1:
        return 'jogador 1'
    if table[line] in ob2:
        return 'jogador 2'
    

def CheckCol(ob1, ob2, table, col):
    colomn = [row[col] for row in table]
    if colomn in ob1 and colomn in ob2:
        return 'draw'
    if colomn in ob1:
        return 'jogador 1'
    if colomn in ob2:
        return 'jogador 2'

def CheckDiag(ob1, ob2, table):
    main_diag = [table[index][index] for index in range(len(table))] #diagonal principal
    sec_daig = [table[-(index+1)][index] for index in range(len(table))] #diagonal secundária
    if (main_diag in ob1 or sec_daig in ob1) and (main_diag in ob2 or sec_daig in ob2):
        return 'draw'
    if (main_diag in ob1 or sec_daig in ob1):
        return 'jogador 1'
    if (main_diag in ob2 or sec_daig in ob2):
        return 'jogador 2'


# essa função junta todas as outras em uma só, fazendo a verificação da tabela por um todo, assim tornando possível
# o player ganhar pela linha, coluna, diagonal principal ou diagonal secundária
def CheckWin(ob1, ob2, Player, table, line, col):
    winner = None
    win_diag = CheckDiag(ob1, ob2, table)
    if win_diag == 'jogador 1' or win_diag == 'jogador 2':
        winner = win_diag

    win_line = CheckLine(ob1, ob2, table, line)
    if win_line == 'jogador 1' or win_line == 'jogador 2':
        winner = win_line

    win_col = CheckCol(ob1, ob2, table, col)
    if win_col == 'jogador 1' or win_col == 'jogador 2':
        winner = win_col

    if win_col == 'draw' or win_line == 'draw' or win_diag == 'draw':
        winner = 'draw'

    if winner != None:
        return winner
    
# função que serve para caso o jogador escolha remover uma linha
def delete_line(table, index, matrizStr):
    invalidLine = True
    especial = False
    while invalidLine:
        DelRow = int(input(f"Escolha a linha (1-{index}): ")) - 1
        if 0 <= DelRow < index:
            table[DelRow] = ['' for i in table[index - 1]]
            matrizStr[DelRow] = ['' for i in table[index - 1]]
            invalidLine = False
        else:
            print(f"Linha inválida. Escolha entre 1 e {index}.")
    return table, especial, matrizStr

# função que serve para caso o jogador escolha remover uma coluna
def delete_col(table, index, matrizStr):
    invalidCol = True
    especial = False
    while invalidCol:
        DelCol = int(input(f"Escolha uma coluna (1-{index}): ")) - 1
        if 0 <= 1 < index:
            for i in range(len(table)):
                table[i][DelCol] = ''
                matrizStr[i][DelCol] = ''
            invalidCol = False
        else:
            print(f"Coluna inválida. Escolha entre 1 e {index}.")
    return table, especial, matrizStr


# função que contêm os inputs que adicionam números na matriz, fazendo a remoção dos números jogados
# da lista de números usáveis e adicionando na lista de números usados
def play(Player, size, color_matriz, matriz, usable_num, objective1, objective2, special1, special2):
    turn = True
    used_nums = []
    while usable_num and turn:
        while turn:
            if Player:
                print('\033[31mVez do jogador 1\033[0m')
            elif not Player:
                print('\033[34mVez do jogador 2\033[0m')
            num = int(input('Digite o número que deseja jogar(ou 0 para jogada especial e S para salvar): '))
            if Player and num == 0 and special1: # aqui jogada especial para o player 1
                use_special = input("Deseja usar o especial em uma linha ou coluna? ")
                if use_special == 'linha':
                    matriz, special1, color_matriz = delete_line(matriz, size, color_matriz)
                    print(tabulate(color_matriz, headers="firstrow", tablefmt="heavy_grid"))
                elif use_special == 'coluna':
                    matriz, special1, color_matriz = delete_col(matriz, size, color_matriz)
                    print(tabulate(color_matriz, headers="firstrow", tablefmt="heavy_grid"))
            elif not Player and num == 0 and special2: # aqui jogada especial para o player 2
                use_special = input("Deseja usar o especial em uma linha ou coluna? ")
                if use_special == 'linha':
                    matriz, special1, color_matriz = delete_line(matriz, size, color_matriz)
                    print(tabulate(color_matriz, headers="firstrow", tablefmt="heavy_grid"))
                elif use_special == 'coluna':
                    matriz, special1, color_matriz = delete_col(matriz, size, color_matriz)
                    print(tabulate(color_matriz, headers="firstrow", tablefmt="heavy_grid"))
            elif num == 'S' or num == 's': # aqui salva, incompleto
                print("Ainda não é possível salvar o jogo. Atualização está por vir!")
            if num != 0 and num != 'S' and num != 's':
                line = int(input('Digite o número da linha que deseja fazer a jogada: '))
                column = int(input('Digite o número da coluna que deseja fazer a jogada: '))
                if size > line >= 0 and size > line >= 0 and num in usable_num and matriz[line][column] == ' ':
                    if Player:
                        color_matriz[line][column] = f'\033[31m{num}\033[0m' # matriz para diferenciar jogadas e mostrar ao usuário
                        matriz[line][column] = num # matriz para ser usada na verificação de vitória
                        played_num = usable_num.remove(num) # retira o numero usado da lista de números disponíveis e coloca na lista de números usados em seguida
                        used_nums.append(played_num)
                        print(tabulate(color_matriz, headers="firstrow", tablefmt="heavy_grid"))
                        winner = CheckWin(objective1, objective2, Player, matriz, line, column)
                        if winner == 'jogador 1' or winner == 'jogador 2':
                            # verifica se algum jogador ganhou e caso sim pede o nome para entrar no ranking
                            InvalidName = True
                            while InvalidName:
                                print(tabulate(color_matriz, headers="firstrow", tablefmt="heavy_grid"))
                                name = input(f'{winner} venceu! Entre para a galeria dos campeões digitando seu nome: ')
                                if name == '':
                                    print("Digite um nome válido para entrar na galeria!")
                                else:
                                    with open('./ranking.csv', 'a', encoding='utf8', newline='') as arquive:
                                        fields = ['Nomes', 'Fácil', 'Médio', 'Difícil', 'Total']
                                        writer = csv.DictWriter(arquive, fieldnames=fields) 
                                        line = {'Nomes': name, 'Total': 1}
                                        writer.writerow(line)
                                    InvalidName = False
                                    turn = False
                        # checa se ainda tem casas disponíveis, se não, empate e nenhum jogador ganha
                        elif winner == None:
                            print(tabulate(color_matriz, headers="firstrow", tablefmt="heavy_grid"))
                            input('Jogo empatou! Nenhum objetivo foi concluído e acabaram as jogadas disponíveis.')
                            break
                        Player = False
                    elif not Player:
                        color_matriz[line][column] = f'\033[34m{num}\033[0m' #matriz para diferenciar jogadas e mostrar ao usuário
                        matriz[line][column] = num #matriz para ser usada na verificação de vitória
                        used_num = usable_num.remove(num) # retira o numero usado da lista de números disponíveis e coloca na lista de números usados em seguida
                        used_nums.append(used_num)
                        print(tabulate(color_matriz, headers="firstrow", tablefmt="heavy_grid"))
                        winner = CheckWin(objective1, objective2, Player, matriz, line, column)
                        if winner == 'jogador 1' or winner == 'jogador 2':
                            # verifica se algum jogador ganhou e caso sim pede o nome para entrar no ranking
                            InvalidName = True
                            while InvalidName:
                                print(tabulate(color_matriz, headers="firstrow", tablefmt="heavy_grid"))
                                name = input(f'{winner} venceu! Entre para a galeria dos campeões digitando seu nome: ')
                                if name == '':
                                    print("Digite um nome válido para entrar na galeria!")
                                else: # abre o arquivo com o ranking e incrementa o nome do jogador vitorioso
                                    with open('./ranking.csv', 'a', encoding='utf8', newline='') as arquive:
                                        fields = ['Nomes', 'Fácil', 'Médio', 'Difícil', 'Total']
                                        writer = csv.DictWriter(arquive, fieldnames=fields) 
                                        line = {'Nomes': name, 'Total': 1}
                                        writer.writerow(line)
                                    InvalidName = False
                                    turn = False
                        # checa se ainda tem casas disponíveis, se não, empate e nenhum jogador ganha
                        elif winner == None:
                            print(tabulate(color_matriz, headers="firstrow", tablefmt="heavy_grid"))
                            input('Jogo empatou! Nenhum objetivo foi concluído e acabaram as jogadas disponíveis.')
                            break
                        Player = True
                else:
                    print("Jogada inválida! Verifique se a casa já não está preenchida ou se o número já não foi jogado.")


while True:
    menu = int(input('''
Escolha uma opção:
[1] Começar novo jogo
[2] Visualizar ranking
[3] Sair
Opção:'''))
    match menu:
        case 1: #inserir o if para avisar que tem um jogo salvo e se deseja sobrescrever esse jogo
            play_game = int(input(
'''Escolha uma opção:
[1] Novo jogo
[2] Continuar jogo
Opção:'''))
            if play_game == 1:
                difficulty_selection = int(input(
'''Selecione a dificuldade:
[1] Fácil (3x3)
[2] Moderada (4x4)
[3] Difícil (5x5)
Opção: '''))
                match difficulty_selection:
                    case 1:
                        size = 3
                        special1, special2 = special_option()
                        objective1, objective2 = mission(), mission()
                        misson1, misson2 = objective_series(objective1, size), objective_series(objective2, size)
                        deliver_mission(Player, objective1, objective2)
                        win_condition1, win_condition2 = possible_win(objective1, misson1, size), possible_win(objective2, misson2, size)
                        matrizStr, matriz, usable_num = generate_table(size)
                        play(Player, size, matrizStr, matriz, usable_num, win_condition1, win_condition2, special1, special2)
                    case 2:
                        size = 4
                        special1, special2 = special_option()
                        objective1, objective2 = mission(), mission()
                        misson1, misson2 = objective_series(objective1, size), objective_series(objective2, size)
                        deliver_mission(Player, objective1, objective2)
                        win_condition1, win_condition2 = possible_win(objective1, misson1, size), possible_win(objective2, misson2, size)
                        matrizStr, matriz, usable_num = generate_table(size)
                        play(Player, size, matrizStr, matriz, usable_num, win_condition1, win_condition2, special1, special2)
                    case 3:
                        size = 5
                        special1, special2 = special_option()
                        objective1, objective2 = mission(), mission()
                        misson1, misson2 = objective_series(objective1, size), objective_series(objective2, size)
                        deliver_mission(Player, objective1, objective2)
                        win_condition1, win_condition2 = possible_win(objective1, misson1, size), possible_win(objective2, misson2, size)
                        matrizStr, matriz, usable_num = generate_table(size)
                        play(Player, size, matrizStr, matriz, usable_num, win_condition1, win_condition2, special1, special2)
            elif play_game == 2:
                print("Ainda não é possível salvar o jogo. Atualização está por vir!")
        case 2: # abre o arquivo como modo de leitura e printa em forma de tabela com todos os nomes de antigos vencedores
            with open('./ranking.csv', 'r', encoding='utf8', newline='') as arquive:
                reader = csv.DictReader(arquive)
                print(tabulate(reader, headers="keys", tablefmt="heavy_grid"))
        case 3:
            print('Obrigado por jogar!')
            break
        case _:
            print('Opção inválida.')