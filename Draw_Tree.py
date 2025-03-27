height = int(input("Enter height of tree: "))


row = 0
while row < height:
    count = 0
    while count < height - row: 
        print(' ', end='')  
        count += 1
    print('*' * row) 
    row += 1

row = height - 2  
while row >= 0:
    count = 0
    while count < height - row:
        print(' ', end='')  
        count += 1
    print('*' * row)  
    row -= 1
