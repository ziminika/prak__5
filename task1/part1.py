class Node:
    def __init__(self, value = 0, next = None):
        self.value = value
        self.next = next
        
class List:
    def __init__(self):
        self.first = None
        
    # Add a new node to the end of the list
    def add_to_end(self, new_value):
        if self.first == None:
            self.first = Node(new_value)
        else:
            curr = self.first
            while curr.next != None:
                curr = curr.next
            curr.next = Node(new_value)

    # Add a new node to the start of the list
    def add_to_start(self, new_value):
        if self.first == None:
            self.first = Node(new_value)
        else:
            curr = self.first
            self.first = Node(new_value, curr)
     
    def __str__(self):
        if self.first != None:
            output = "List: " + str(self.first.value)
            curr = self.first.next 
            while curr != None:
                output += " -> " + str(curr.value) 
                curr = curr.next
            return output
        return "Empty list"

    # Search value by list items
    def find(self, value):
        curr = self.first
        pos = 0
        while curr != None:
            pos += 1
            if curr.value == value:
                return "Item is in position " + str(pos)
            curr = curr.next
        return "Item not listed"

    # Delete the first occurrence of a value in a list
    def remove(self, value):
        curr = self.first
        parrent = self.first
        while curr != None:
            if curr.value == value:
                if curr == self.first:
                    self.first = curr.next
                else:
                    parrent.next = curr.next
                break
            else:
                parrent = curr
                curr = curr.next

# Listing a Number
def num_to_list(number):
    lst = List()
    while number != 0:
        lst.add_to_end(number % 10)
        number /= 10
    return lst
    
# Program operation example
""" L = List()
L.add_to_end(1)
L.add_to_end(2)
L.add_to_end(3)
print(L)
L.add_to_start(5)
print(L)  
print(L.find(2))
L.remove(3)
print(L)
print(num_to_list(2 ** 100)) """