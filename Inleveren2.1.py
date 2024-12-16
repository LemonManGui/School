# Maak een functie die een lijst neemt als argument en een nieuwe gesoorteerde lijst returnt

# Test-lijst
getallen = [100, 12, 8, 55, 3, 3, 107, 9, 34]


def sort(list, method):
    # (1) quicksort
    # if method == "quicksort":
    #     n = len(list)
    #     for i in range(n):
    #          for j in range(0, n - i - 1):
    #             if list[j] > list[j + 1]:
    #                 list[j], list[j + 1] = list[j + 1],list[j]  
                    
    #     return list
        

    if method == "gui":
        n = len(list)
        for i in range(n):
            for j in range(0, n - i - 1):
                if list[j] > list[j + 1]:
                    list[j], list[j + 1] = list[j +1], list[j]
        return list    

       
            
            
              
                
            

print(sort(getallen, "gui"))

