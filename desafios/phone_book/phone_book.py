import re

contactos = [{'id':'5', 'name': 'Jose Macucule', 'phone_number': '843991991'},
             {'id':'6', 'name': 'Anatercia Joaquim', 'phone_number': '829194359'},
             {'id':'7', 'name': 'Anacleto Cuna', 'phone_number': '857044444'}]


def add_contact():
    if len(contactos) == 0:
        id = 1
    else:
        id = int(contactos[-1]['id']) + 1

    name = input("Name: \n")
    phone_number = input("Phone Number: \n")
    my_contact = {'id': str(id), 'name': name, 'phone_number': phone_number}
    return contactos.append(my_contact)

def delete_contact(id):
    i = 0
    for contacto in contactos:
        i += 1
        if str(id) in contacto['id']:
            details = view_contact_details(id)
            print(details)
            contactos.pop(i-1)
            return f"Contact: '{details}' deleted."
    return "No data found"
    

def search_contact(my_input, criteria):
    matches_found = []
    for info in contactos:
        if re.search(my_input, info[criteria]) != None:
            matches_found.append(info)
        else:
             pass
    if len(matches_found) >= 1:
        return matches_found
    else:
        return "No Data Found"

def update_contact (id, field, new_data):
    result = "Error updating information"
    for data in contactos:
        if str(id) in data['id']:
            old_data = data[field]
            data.update({field:new_data})
            data[field] = new_data
            result = f"'{old_data}' updated to '{data[field]}'."
        else:
            pass
    return result

def view_contacts(lst:list):
    index = 0
    for x in lst:
        index += 1
        print(f"{index}. {x['name']} ({x['phone_number']})")


def view_contact_details(id):
    for x in contactos:
        if str(id) in x['id']:
           return f"{x['name']} ({x['phone_number']})"
    return "No info found."    


def main():
    while True:
        print("1. Add contact")
        print("2. Delete contact")
        print("3. Search contact")
        print("4. Update contact")

        selected_option = int((input("Digite a operacao: ")))
        if selected_option == 1:
            add_contact()
            print(contactos[-1])
        elif selected_option == 2:
            id_contact = input("Digite o contacto a remover: ")
            print(delete_contact(int(id_contact)))
        elif selected_option == 3:
            print("Find contact via:")
            print("1. Name")
            print("2. Phone number:")
            selected_option = int((input("Digite a operacao: ")))
            if selected_option == 1:
                my_criteria = "name"
            elif selected_option == 2:
                my_criteria = "phone_number"
            my_input = input("Pesquisar por:\n")
            print(search_contact(my_input, my_criteria))
        elif selected_option == 4:
            print("Find contact via:")
            print("1. Name")
            print("2. Phone number:")
            selected_option = int((input("Digite a operacao: ")))
            if selected_option == 1:
                my_criteria = "name"
            elif selected_option == 2:
                my_criteria = "phone_number"
            my_input = input("Pesquisar por:\n")
            if len(search_contact(my_input, my_criteria)) >= 1:
                data = search_contact(my_input, my_criteria)
                view_contacts(data)
                selected_option = int(input("Selecione o contacto a actualizar: "))
                selected = data[selected_option - 1]
                print(view_contact_details(selected['id']))
                print("O que deseja actualizar?\n")
                print("1. Nome")
                print("2. Numero de celular\n")
                selected_option = int(input(""))
                if selected_option == 1:
                    new_value = input("New info: ")
                    update_contact(int(selected['id']), "name", new_value)
                if selected_option == 2:
                    new_value = input("New info: ")
                    update_contact(int(selected['id']), "phone_number", new_value)
                else:
                    print("Something went wrong.")
        else:
            print("Try again")


main()