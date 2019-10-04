from part1 import num_to_list, List

# The sum of two numbers represented by a list
def sum(L1, L2):
    res = List()
    curr1 = L1.first
    curr2 = L2.first
    surplus = 0
    while curr1 != None and curr2 != None:
        res.add_to_end((curr1.value + curr2.value + surplus) % 10)
        surplus = (curr1.value + curr2.value + surplus) // 10
        curr1 = curr1.next
        curr2 = curr2.next
    if curr1 == None:
        while curr2 != None:
            res.add_to_end((curr2.value + surplus) % 10)
            surplus = (curr2.value + surplus) // 10
            curr2 = curr2.next
    else:    
        while  curr1 != None:
            res.add_to_end((curr1.value + surplus) % 10)
            surplus = (curr1.value + surplus) // 10
            curr1 = curr1.next
    if surplus != 0:
        res.add_to_end(surplus)
    return res

# Program operation example
print("Enter two numbers")
L1 = num_to_list(int(input()))
L2 = num_to_list(int(input()))
#print(L1)
#print(L2)
print(sum(L1, L2))
