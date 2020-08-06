def display_inventory(inventory):
    print('Inventory:')
    sum = 0
    for key, value in inventory.items():
        print(str(value) + ' ' + key)
        sum += value
    print('Total number of items: ' + str(sum))

def add_to_inventory(inventory, itemList):
    for item in itemList:
        inventory.setdefault(item, 1)
    return inventory

inventory = {}
inventory['first_item'] = 343
inventory['seocnd_item'] = 122
inventory['third_item'] = 111

list = ['value1', 'value2', 'value3']
add_to_inventory(inventory, list)

display_inventory(inventory)
    
    
