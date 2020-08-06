def print_list_like_table(list):
    size = len(list)
    
    sizeOfEveryListMember = []
    for listMember in list:        
        sizeOfEveryListMember.append(len(listMember))   
    internalSize = max(sizeOfEveryListMember)
    
    colLen = [0] * internalSize
    for i in range(internalSize):
        for j in range(size):
            if i < len(list[j]):
                tmp = []
                tmp.append(colLen[i])
                tmp.append(len(list[j][i]))
                colLen[i] = max(tmp)
    for i in range(size):
        for j in range(len(list[i])):
            print(list[i][j].rjust(colLen[j]), end=' ')
        print()

tableData = [
    ['apples', 'oranges', 'cherries', 'banana'],
    ['Alice', 'Bob', 'Carol', 'David'],
    ['', '', 'Test', ''],
    ['', 'Test', '', ''],
    ['dogs', 'cats', 'moose', 'goose']
]
print_list_like_table(tableData)
