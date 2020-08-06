import copy

def get_rotate_copy(list):
    resList = []
    size = len(list)
    sizeOfEveryListMember = []
    for listMember in list:        
        sizeOfEveryListMember.append(len(listMember))   
    internalSize = max(sizeOfEveryListMember)    
    for i in range(internalSize):
        tmpList = []
        for j in range(size):            
            if i < len(list[j]):                 
                tmpList.append(list[j][i])
        resList.append(tmpList)
    return resList

def print_list(list):
    print('-----------------------------')
    for i in range (len(list)):
        for j in range(len(list[i])):
            print(str(list[i][j]) + ' ', end=' ')
        print()
    print('-----------------------------')


firstList = [['.', '.', '.', '.', '.', '.'],
             ['.', 'O', 'O', '.', '.', '.'],
             ['O', 'O', 'O', 'O', '.', '.'],
             ['0', 'O', 'O', 'O', 'O', '.'],
             ['.', 'O', 'O', 'O', 'O', 'O'],
             ['O', 'O', 'O', 'O', 'O', '.'],
             ['O', 'O', 'O', 'O', '.', '.'],
             ['.', 'O', 'O', '.', '.', '.'],
             ['.', '.', '.', '.', '.', '.']]
secondList = get_rotate_copy(firstList)
print_list(firstList)

print_list(secondList)

