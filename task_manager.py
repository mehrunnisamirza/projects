#=====importing libraries===========
'''This is the section where you will import libraries'''
import datetime
from dateutil.parser import parse

"""""""""""""""""""""""""""""""""""""""""""""Define functions"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def reg_user():
    if username1 == 'admin,':                             # only the admin can register a user
        username = input("Please enter a new username") + ','   # Request input of a new username
        password = input('Please enter a new password')  # Request input of a new username
        password2 = input("Please enter your new password again")  # Request input of password confirmation.

        if password2 == password: #if passwords match then open user.txt and write the new user's password and username
            f1 = open("user.txt", 'a')
            user = username, password
            if user not in dict.items():     #only register users if their usernames aren't already there
               f1.write(f"\n{username} {password}")
               print("user successfully registered")  #print this message if the user is registered

            else:
                print('Username already exists. Please enter a new one')  #if user enters a username that is already in the file
        else:
            print("passwords don't match")   #if passwords don't match then print this message

    else:
        print("You can't register a user")  #if someone other than the admin tries to register a user then print this message

def add_task():
    username = input("Please enter the username of the person the task is assigned to")  # ask for username
    title = input("Please enter the title of the task")  # ask for task title
    description = input('Please give a description of the task')  # ask for description of the task
    today = '21 Jan 2023'  # today's date
    due = input('Please enter the due date of the task')  # ask for due date

    f2 = open("tasks.txt", 'a')  # open task file
    f2.write(f"\n{username}, {title}, {description}, {today}, {due}, No")  # write all the variables to the file in this format

def view_all():
    f2 = open("tasks.txt", 'r')  # if user selects va option then go through each line in tasks.txt and convert to list
    all_dict_tasks2 = {}
    j = 1
    for line in f2:
        if line == '\n':
            continue
        line = line.strip()
        all_dict_tasks2[j] = line  #append all users and number of their tasks to dictionary
        j = j + 1

    for num, task in all_dict_tasks2.items():  #unpack keys and values to print out all tasks
        task = task.split(',')
        username = task[0]
        title = task[1]
        description = task[2]
        today = task[3]
        due = task[4]
        y_n = task[5]
        dash = '---------------------------------------'
        space = '    '
        print(f"{dash}\n{num: >1}.{'Task:': >5}{title: <5}\n{'Assigned To: ': >5}{username: <5}\n{'Date assigned:': >5}{today: <5}\n{'Due date:': >5}{due: <5}\n{'Task complete?:': >5}{y_n}\n{'Task Description:'}{description}\n{dash}")

def view_mine():
    f2 = open("tasks.txt", 'r')
    all_dict_tasks = {}   #stores the logged in user's tasks
    all_dict_tasks2 = {}  #stores all user's tasks
    i = 1
    j = 1
    for line in f2:
        if line =='\n':
            continue
        line = line.strip()
        all_dict_tasks2[j] = line  #########FIXXXX
        j = j + 1
        if username1 in line:
            line = line.strip()
            all_dict_tasks[i] = line
            i = i + 1

    for num, task in all_dict_tasks.items():
        task = task.split(',')
        username = task[0]
        title = task[1]
        description = task[2]
        today = task[3]
        due = task[4]
        y_n = task[5]
        dash = '---------------------------------------'
        space = '    '
        print(f"{dash}\n{num: >1}.{'Task:': >5}{title: <5}\n{'Assigned To: ': >5}{username: <5}\n{'Date assigned:': >5}{today: <5}\n{'Due date:': >5}{today: <5}\n{'Task complete?:': >5}{y_n}\n{'Task Description:'}{description}\n{dash}")

    task_num = int(input('Please enter the number of the task you would like to see or alternatively type -1 to return to main menu'))
    print('you have chosen the following task:')
    for num, task in all_dict_tasks.items():
        if num == task_num:           #prints out the task the user has selected
            task = task.split(', ')
            task[5] = "Yes"
            print(f"{dash}\n{num: >1}.{'Task:': >5}{title: <5}\n{'Assigned To: ': >5}{username: <5}\n{'Date assigned:': >5}{today: <5}\n{'Due date:': >5}{today: <5}\n{'Task complete?:': >5}{y_n}\n{'Task Description:'}{description}\n{dash}")

    if task_num != -1:   #if user enters a number other than -1 athe display the following options
        options = input('''Please select one from the following options:
m - mark the task as complete
e - edit the task
:''').lower()

        if options == 'm':
            store_lines = []               #store lines from tasks.txt in this list
            f2 = open("tasks.txt", 'r+')
            for line in f2:
                line = line.strip()
                if line == all_dict_tasks[task_num]:   #if task is assigned to the user who is logged in and matches task number
                    line = line.split(', ')
                    line[5] = "Yes"                   #then change no to yes
                    line = ', '.join(line)
                    store_lines.append(line)          #append line to list
                else:
                    store_lines.append(line)          #otherwise append the lines as they are without changing anything

            f2 = open("tasks.txt", 'w+')
            for task in store_lines:
                f2.write(f'{task}\n')

        elif options == 'e':               #fix this too
            store_lines_2 = []
            f2 = open("tasks.txt", 'r')
            for task in f2:
                task = task.strip()
                if task == all_dict_tasks[task_num]:
                    task = task.split(', ')
                    if task[5] == "No":
                       do = input('''what would you like to do?
u - edit username
d - edit due date
:''').lower()
                       if do == 'u':
                          task[0] = input("Please enter a new username")
                          task = ', '.join(task)
                          store_lines_2.append(task)
                       elif do == 'd':
                          task[3] = input("Please enter a new due date")
                          task = ', '.join(task)
                          store_lines_2.append(task)
                    else:
                        print("you can't edit this task as it has been completed")
                        task = ', '.join(task)
                        store_lines_2.append(task)
                else:
                    store_lines_2.append(task)

            f2 = open("tasks.txt", 'w+')
            for task in store_lines_2:
                f2.write(f'{task}\n')

    else:
        print('\nreturning to main menu\n')

#====Login Section====
'''Here you will write code that will allow a user to login.
'''
username1 = input("Please enter your username") + ','  #ask user to enter username and password to log in
password1 = input("Please enter you password")

f1 = open("user.txt",'r')     #open user.text file in read more
dict = {}                     #store all usernames and passwords in dictionary
for line in f1:
    log = line.split()        #split each line and store in list
    dict[log[0]] = log[1]     #first index is the key for the dictionary and second index is the value

user = username1, password1

while user not in dict.items():                                   #keep asking user to enter username and password till
      username1 = input("Please enter your username again") + ',' #till they enter a combination that is in the users.txt file
      password1 = input("Please enter you password again")
      user = username1, password1

print("\nyou are now logged in\n")    #print message if the user sucessfully logs in

while True:
    if username1 == 'admin,':   #keep displaying this menu till admin is logged in
        menu = input('''Select one of the following Options below:  
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
gr - generate reports 
ds - display statistics 
e - Exit
: ''').lower()

    if username1 != 'admin,':    #if someone other than the admin is logged in then present the original menu
        # presenting the menu to the user and
        # making sure that the user input is converted to lower case.
        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
e - Exit
: ''').lower()

    if menu == 'r':
        pass
        reg_user()

    elif menu == 'a':
        pass
        add_task()

    elif menu == 'va':
       view_all()

    elif menu == 'vm':
        view_mine()

    elif menu == 'ds':                             #if admin selects ds then open both text files
        f1 = open("user.txt", 'r')
        f2 = open("tasks.txt", 'r')
        count1 = len(f1.readlines())               #use len to find out how many lines there are in user.txt
        count2 = len(f2.readlines())               #use len to find out how many lines there are in tasks.txt
        print("Total number of Users:", count1)
        print("Total number of tasks:", count2)    #print out the counts for both users and tasks

    elif menu == 'gr':
        f2 = open("tasks.txt", 'r')  #open existting file and count lines
        count2 = len(f2.readlines())  #count lines
        i = 0
        j = 0
        t = 0
        z = 0
        f2 = open("tasks.txt", 'r')  # open existting file and count lines
        now = str(datetime.date.today())
        currentDate = datetime.datetime.strptime(now, '%Y-%m-%d').date()  #format current date

        for line in f2:
            if line == '\n':
                continue
            l = line.strip()
            l = line.split(',')
            username = l[0]
            date = l[4]
            dt = parse(date)
            dt_formated = dt.strftime('%Y-%m-%d')
            y_n = l[5]
            if y_n.startswith(" Y"):   #to count the number of completed and uncompleted tasks
                i = i + 1
            if y_n.startswith(" N"):
                j = j + 1
            if str(currentDate) > dt_formated:   #num of tasks that are overdue
                t = t + 1
            if str(currentDate) > dt_formated and y_n.startswith(" N"): #num of tasks that are overdue an incomplete
                z = z + 1

        f2.close()

        file1 = open("task_overview.txt", 'w')

        file1.write(f"The total number of tasks that have been generated and tracked: {count2}\n")
        file1.write(f"The total number of completed tasks: {i}\n")
        file1.write(f"The total number of uncompleted tasks: {j}\n")
        file1.write(f"The total number of tasks that haven’t been completed and that are overdue: {z}\n")
        file1.write(f"The percentage of tasks that are incomplete: {(j/count2) * 100}%\n")  #get percentage by dividing by total num of tasks
        file1.write(f"The percentage of tasks that are overdue: {(t/count2)*100}%\n")

        ##now for user_overview.txt
        f1 = open("user.txt", 'r')  # open existting file and count lines
        f2 = open("tasks.txt", 'r')
        count1 = len(f1.readlines())  #The total number of users registered with task_manager.py.
        count2 = len(f2.readlines())  #The total number of tasks that have been generated and tracked

        f2 = open("tasks.txt", 'r')
        user_store = []              #store all users in a list
        user_store_complete = []     #store user who have completed tasks
        user_store_incomplete = []   #store user who have incomplete tasks
        user_store_overdue_incomplete = []

        #make separate lists to meet all the different following conditions
        for task in f2:
            if task == '\n':
                continue
            user = task.strip()
            user = task.split(',')
            date = user[4]
            dt = parse(date)
            dt_formated = dt.strftime('%Y-%m-%d')
            user_store.append(user[0])
            if user[5] == " Yes\n":
                user_store_complete.append(user[0])
            if user[5] == " Yes":
               user_store_complete.append(user[0])
            if user[5] == " No\n":
                user_store_incomplete.append(user[0])
            if user[5] == " No":
                user_store_incomplete.append(user[0])
            if str(currentDate) > dt_formated and user[5].startswith(" N"):  #num of tasks that are overdue an incomplete
               user_store_overdue_incomplete.append(user[0])

        #store user and number of type of task (complete or incomplete) in different dictionaries
        dict_users = {x: user_store.count(x) for x in user_store}   #dictionary to store users and the number of their tasks
        dict_users_complete = {x: user_store_complete.count(x) for x in user_store_complete}
        dict_users_incomplete = {x: user_store_incomplete.count(x) for x in user_store_incomplete}
        dict_users_overdue_incomplete = {x: user_store_overdue_incomplete.count(x) for x in user_store_overdue_incomplete}

        file2 = open("user_overview.txt", 'w')
        file2.write(f"The total number of users registered: {count1}\n")
        file2.write(f"The total number of tasks that have been generated and tracked: {count2}\n")
        file2.write('\n')
        for user, count in dict_users.items():
            file2.write(f"The total number of tasks assigned to {user}: {count}\n")
            file2.write(f"The percentage of the total number of tasks assigned to {user}: {(count/count2)*100}%\n")
            if user not in dict_users_complete.keys():
                dict_users_complete[user] = 0
            if user not in dict_users_incomplete.keys():
                dict_users_incomplete[user] = 0
            if user not in dict_users_overdue_incomplete.keys():
                dict_users_overdue_incomplete[user] = 0
            file2.write(f"The percentage of the tasks assigned to {user} that have been completed: {(dict_users_complete[user]/count)*100}%\n")
            file2.write(f"The percentage of the tasks assigned to {user} that must still be completed: {(dict_users_incomplete[user]/dict_users[user])*100}%\n")
            file2.write(f"The percentage of the tasks assigned to {user} that have not yet been completed and are overdue: {((dict_users_overdue_incomplete[user]))/(dict_users[user])*100}%\n")
            file2.write('\n')

        print("Opening user_overview.txt:")    #display contents of both files
        print('-------------------------------------------------------------------------------')
        file2 = open("user_overview.txt", 'r')
        for line in file2:
            print(line)
        print('-------------------------------------------------------------------------------')
        print()
        print("Opening task_overview.txt:")
        print('-------------------------------------------------------------------------------')
        file1 = open("task_overview.txt", 'r')
        for line in file1:
            print(line)
        print('-------------------------------------------------------------------------------')

    elif menu == 'e':
        print('Goodbye!!!')
        exit()


    else:
        print("You have made a wrong choice, Please Try again")