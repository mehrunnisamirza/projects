from tabulate import tabulate
#========The beginning of the class==========
class Shoe:

    #define instance variables and other required class methods
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    #to print objects as strings
    def __str__(self):
        return f"Country:        {self.country}\n" \
               f"Code:           {self.code}\n" \
               f"Product:        {self.product}\n" \
               f"Cost:           {self.cost}\n" \
               f"Quantity:       {self.quantity}\n"

#The list will be used to store a list of objects of shoes
shoe_list = []

#This function will open the file inventory.txt
#and read the data from this file, then create a shoes object with this data
#and append this object into the shoes list. I use try and except to account for error handling
def read_shoes_data():
    try:
        shoe_list.clear()  # clear the list that contains shoe objects every time to avoid double writing
        file = open('inventory.txt', 'r')
        for line in file:
            if line.startswith("Country"):     #skipping the first line
                continue
            line = line.strip().split(',')
            country, code, product, cost, quantity = line
            cost = float(cost)
            quantity = int(quantity)
            shoe_object = Shoe(country, code, product, cost, quantity)
            shoe_list.append(shoe_object)
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {str(e)}")

#This function will allow a user to capture data
#about a shoe and use this data to create a shoe object
#and append this object to the shoe list.
def capture_shoes():
    try:
        shoe_list.clear()
        country = input("Enter the country: ")
        code = input("Enter the code: ")
        product = input("Enter the product: ")
        cost = float(input("Enter the cost: "))
        quantity = int(input("Enter the quantity: "))
        shoe_object = Shoe(country, code, product, cost, quantity)
        read_shoes_data()
        shoe_list.append(shoe_object)
        file = open('inventory.txt', 'a')
        file.write(f"\n{shoe_object.country},{shoe_object.code},{(shoe_object.product)},{shoe_object.cost},"
                   f"{shoe_object.quantity}")

    except ValueError:
        print("Invalid input. Cost must be a number and quantity must be an integer.")


#This function will iterate over the shoes list and print the details of the shoes returned from the __str__function
#I organise the data in a table format by using Python’s tabulate module.
def view_all():
    read_shoes_data()
    header = ['Country', 'Code', 'Product', 'Cost', 'Quantity']
    table = [[shoe.country, shoe.code, shoe.product, shoe.cost, shoe.quantity] for shoe in shoe_list]
    print(tabulate(table, headers=header, tablefmt='grid'))


#This function will find the shoe object with the lowest quantity
#Ask the user if they want to add this quantity of shoes and then update it.
#This quantity is updated on the file for this shoe.
def re_stock():
    read_shoes_data()
    lowest_quantity_shoe = min(shoe.get_quantity() for shoe in shoe_list)
    for shoe in shoe_list:
        if shoe.get_quantity() == lowest_quantity_shoe:
            print(f'Shoe with the lowest quantity that needs to be restocked:\n{shoe}')
    file = open('inventory.txt', 'r')
    store_line = []                     #store all lines from the file in this list
    for line in file:
        if line.startswith("Country"):  # skipping the first line
            continue
        line = line.strip().split(',')
        quantity = line[4]
        if int(quantity) == lowest_quantity_shoe:
           user_choice = input("Do you want to add this quantity of shoes? Y/N: ").lower()
           if user_choice == 'y':
               shoe_list.clear()        #clear list every time to avoid double writing
               new_quantity = int(input("Enter new quantity"))
               for shoe in shoe_list:
                   if shoe.get_quantity() == lowest_quantity_shoe:
                       shoe.quantity = new_quantity
               line[4] = str(new_quantity)
               line = ','.join(line)
               store_line.append(line)

           else:
               line = ','.join(line)
               store_line.append(line)
        else:
            line = ','.join(line)
            store_line.append(line)
    file.close()

    file = open('inventory.txt', 'w+')   #rewrite the entire file with updated lines
    for line in store_line:
        file.write(f'{line}\n')

# This function will search for a shoe from the list using the shoe code
# and return this object so that it will be printed.
def search_shoe():
    read_shoes_data()
    enter_code = input("Enter shoe code")
    for shoe in shoe_list:
        if shoe.code == enter_code:
           print(shoe)


#This function will calculate the total value for each item.
def value_per_item():
    read_shoes_data()
    for shoe in shoe_list:
        print(f"{shoe}Value per item: {shoe.cost * shoe.quantity}\n")


#this function determines the product with the highest quantity and prints this shoe as being for sale
def highest_qty():
    read_shoes_data()
    highest_quantity_shoe = max(shoe.get_quantity() for shoe in shoe_list)
    file = open('inventory.txt', 'r')
    for line in file:
        if line.startswith("Country"):  # skipping the first line
            continue
        line = line.strip().split(',')
        country, code, product, cost, quantity = line
        if str(highest_quantity_shoe) in line[4]:   #if the line contains that shoe then print this out 
            print(f"The shoe {product} (code: {code}) in {country} is on sale!\n")


#==========Main Menu=============
while True:
    menu = input('''Select one of the following Options below:  
va - view all shoes and their details in a table
rs - view shoes that need to be restocked
c - add new shoe item into the inventory
h - view the shoe that has the highest quantity
s - search a shoe in the inventory using its code
v - view the value per item 
e - exit 
: ''').lower()

    if menu == 'va':
        view_all()

    elif menu == 'rs':
        re_stock()

    elif menu == 'c':
        capture_shoes()

    elif menu == 'h':
        highest_qty()

    elif menu == 's':
        search_shoe()

    elif menu == 'v':
        value_per_item()

    elif menu == 'e':
        exit()


