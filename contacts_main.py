import random

MAX_LEVEL = 6  # Maximum level for the skip list

#Creates node by taking contact as dictionary
def create_node(contact, level):
    return {'contact': contact, 'forward': [None]*(level+1)}

#Generates random level with probability set as 1/2
def random_level():
    level = 0
    while random.random() < 0.5 and level < MAX_LEVEL:  #not more than the max level set
        level += 1
    return level

#Takes a node and inserts it into the skiplist by modifying the skiplist inplace
def insert(root, contact):
    update = [None] * (MAX_LEVEL + 1)
    current = root
    for i in range(MAX_LEVEL, -1, -1): #vertical
        while current['forward'][i] and current['forward'][i]['contact']['name'].lower() < contact['name'].lower():
            current = current['forward'][i] #horizontal
        update[i] = current

    level = random_level()
    new_node = create_node(contact, level)
    
    for i in range(level + 1):
        new_node['forward'][i] = update[i]['forward'][i]
        update[i]['forward'][i] = new_node

#Searching by name
def search_name(root, name):
    current = root
    for i in range(MAX_LEVEL, -1, -1):  #changing the vertical levels 
        while current['forward'][i] and current['forward'][i]['contact']['name'].lower() <= name.lower():   #checking if the next node is less than or equal to the target
            if current['forward'][i]['contact']['name'].lower() == name.lower():
                 return current['forward'][i]['contact']
            current = current['forward'][i] #changing the value of current - horizontal traversal
    return None

#Searching by phone number
def search_number(root, number):
    current = root
    for i in range(MAX_LEVEL, -1, -1):
        while current['forward'][i] and current['forward'][i]['contact']['phone'] <= number:
            if current['forward'][i]['contact']['phone'] == number:
                 return current['forward'][i]['contact']
            current = current['forward'][i]
    return None

#Searching by email address
def search_email(root, email):
    current = root
    for i in range(MAX_LEVEL, -1, -1):
        while current['forward'][i] and current['forward'][i]['contact']['email'].lower() <= email.lower():
            if current['forward'][i]['contact']['email'].lower() == email.lower():
                 return current['forward'][i]['contact']
            current = current['forward'][i]
    return None

#Deletes a contact and arranges pointers accordingly
def delete(root, name):
    update = [None] * (MAX_LEVEL + 1)
    current = root
    for i in range(MAX_LEVEL, -1, -1):
        while current['forward'][i] and current['forward'][i]['contact']['name'].lower() < name.lower():
            current = current['forward'][i]
        update[i] = current

    current = current['forward'][0]
    if current and current['contact']['name'].lower() == name.lower():
        for i in range(len(current['forward'])):
            update[i]['forward'][i] = current['forward'][i]
            

#Updates contact in skiplist
def update_contact(root, old_contact, new_contact):
    delete(root, old_contact['name'])
    insert(root, new_contact)
    print("Contact updated successfully.")


def update_contact_menu(root):
    name = input("Enter the name of the contact to update: ")
    old_contact = search_name(root, name)
    if old_contact:
        print("Select the field you want to update:")
        print("1. Name")
        print("2. Phone Number")
        print("3. Email Address")
        choice = input("Enter your choice: ")
        if choice == '1':
            new_name = input("Enter the new name: ")
            new_contact = {'name': new_name, 'phone': old_contact['phone'], 'email': old_contact['email']}
            update_contact(root, old_contact, new_contact)
        elif choice == '2':
            new_phone = input("Enter the new phone number: ")
            new_contact = {'name': old_contact['name'], 'phone': new_phone, 'email': old_contact['email']}
            update_contact(root, old_contact, new_contact)
        elif choice == '3':
            new_email = input("Enter the new email address: ")
            new_contact = {'name': old_contact['name'], 'phone': old_contact['phone'], 'email': new_email}
            update_contact(root, old_contact, new_contact)
        else:
            print("Invalid choice.")
    else:
        print("Contact not found.")
    

#Displays all contact saved in skip list
def display(root):
    print()
    print("Displaying the Contact Book:")
    current = root['forward'][0]    #level zero has all contacts
    while current:
        print("Name:", current['contact']['name'], " Phone:", current['contact']['phone'], " Email:", current['contact']['email'])
        current = current['forward'][0] #moving on to the next node

#Returns a dictionary by taking a name, an integer value for phone number and email address
def get_contact_details():
    name = input("Enter name: ")
    phone = int(input("Enter phone number: "))
    email = input("Enter email address: ")
    return {'name': name, 'phone': phone, 'email': email}

if __name__ == "__main__":
    #create header node
    root = create_node({'name': 'John Doe', 'phone': '1234567890', 'email': 'john@example.com'}, MAX_LEVEL)

    while True:
        #Main menu
        print("\n1. Add Contact")
        print("2. Search Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. Display Contacts")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            try:
                contact = get_contact_details() #create dictionary of contact name, number and email address
            except ValueError:
                print('Please only enter numerical value')  #to accept only integer values
                continue
            insert(root, contact)   #insert contact details into skiplist
            print("Contact added successfully.")
        elif choice == '2':
            #menu to select which field to search by
            print("Select the field you want to search by:")
            print("1. Name")
            print("2. Phone Number")
            print("3. Email Address")
            search_option = input("Enter your choice: ")
            #searches according to field selected
            if search_option=='1':
                name = input("Enter the name to search: ")
                contact = search_name(root, name)
            elif search_option=='2':
                number = input("Enter the Phone number to search: ")
                contact = search_number(root, number)
            elif search_option=='3':
                email = input("Enter the Email address to search: ")
                contact = search_email(root, email)
            else:
                print("Invalid choice. Please try again.")
                continue
            if contact:
                print("Contact found - Name:", contact['name'], " Phone:", contact['phone'], " Email:", contact['email'])
            else:
                print("Contact not found.")
        elif choice == '3':
            update_contact_menu(root)
        elif choice == '4':
            name = input("Enter the name of the contact to delete: ")
            contact = search_name(root, name)
            if contact:
                delete(root, name)
                print("Contact deleted successfully.")
            else:
                print("Contact {} not found.".format(name))
        elif choice == '5':
            display(root)
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")
