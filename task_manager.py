#=====importing libraries===========
from datetime import date
from datetime import datetime

#===== Functions ===========
### read a text file ###
def read_file(filename):
    try:
        in_file = open(filename,"r")
    except OSError:
        # if opening the file causes an error
        # (see https://www.topbug.net/blog/2020/10/03/catching-filenotfounderror-watch-out/)
        contents = "error"
        return contents

    # if opening of file was successful
    contents = in_file.read()
    in_file.close()
    return contents

# write data to text file (overwrite)
def write_to_file(file_name, my_string):
    f = open(file_name,"w")        
    f.write(my_string)
    f.close()
    return

### append data to a text file ###
def append_to_file(file_name, my_string):
    f = open(file_name,"a") # a = append data written to file at the end          
    # write to file on a new line \n
    f.write("\n" + my_string)
    f.close()
    return

### dictionary of user name and password ###
def user_dictionary():
    # read text file
    contents = read_file("user.txt")

    # create dictionary of usernames and password
    user_dict = {}
    for c_line in contents.split("\n"):
        # each line contains a string in the following format:
        # username followed by a comma, a space and then the password
        user = c_line.split(", ")[0].lower()
        pw   = c_line.split(", ")[1]

        # keys = user names and values = passwords
        user_dict[user] = pw
    return user_dict

### user list ###
def get_user_list():
    # users = keys in user dictionary
    output = user_dictionary().keys()
    return output

### task list ###
def get_task_list():
    # read all tasks
    contents = read_file("tasks.txt")

    # Read all lines from the file
    task_list = []
    for c_line in contents.split("\n"):
        # split line where there is comma and space
        # append each task into the list as a dictionary
        task_list.append(
                        {
                        "owner":       c_line.split(", ")[0].lower(),
                        "title":       c_line.split(", ")[1],
                        "desc":        c_line.split(", ")[2],
                        "due_date":    c_line.split(", ")[3],
                        "start_date":  c_line.split(", ")[4],
                        "is_complete": c_line.split(", ")[5]
                        }
                        )
    return task_list

### write task list to text file ###
def write_tasks_to_file(task_list, file_name = "tasks.txt"):
    # argument tasklist is a list of dictionaries (each dictionary represents a task)
    # function writes this task list to a text file
    temp_list = []

    # form a string by joining task values separated by ", "
    for task in task_list:
        task_format = ", ".join(task.values())
        temp_list.append(task_format)

    # save output to file
    output = "\n".join(temp_list)
    write_to_file(file_name, output)
    return

### mark task complete ### 
def mark_task_complete(task_nr):
    # get task list (note: each task in the list is a dictionary)
    all_tasks = get_task_list()

    # find desired task and mark it complete
    task = all_tasks[task_nr - 1]
    task["is_complete"] = "Yes"

    # write all tasks into tasks.txt file
    write_tasks_to_file(all_tasks, "tasks.txt")
    return

### edit task ### 
def edit_task(task_nr):
    # get task list (note: each task in the list is a dictionary)
    all_tasks = get_task_list()

    # find desired task to edit
    task = all_tasks[task_nr - 1]

    # the person to whom the task is assigned or the due date of the task can be edited.
    edit_option = input(f"""Edit options for task number: {task_nr}
to - task owner edit (user name)
dd - due date edit
----------------------------
Selection:""").lower()
    if task["is_complete"].lower() == "yes":
        print("Error: can only edit tasks that have not been completed yet.")
    elif edit_option == "to":
        # user input
        new_task_owner = input("New task owner: ").lower()

        # If username does not exist, ask for different user
        while True:
            if new_task_owner in user_dictionary():
                # assign new task owner
                task["owner"] = new_task_owner
                break
            else:
                print("Error: user does not exist. Please try different user.")
                new_task_owner = str(input("New task owner: ")).lower()

    elif edit_option == "dd":
        # assign new due date
        task["due_date"] = input("New due date (e.g. 01 Jan 2023): ")
    else:
        print("Error occurred. Start again.")
    
    # stick task back into list of all task
    all_tasks[task_nr - 1] = task

    # update the tasks.txt file
    write_tasks_to_file(all_tasks, "tasks.txt")
    return

### Registering a user ###
def reg_user(file_name = "user.txt"):
    print("Registering a user\n-------------------")
    # Request new username
    new_username = str(input("New Username:  \t")).lower()
    
    # If username already exists, allow adding new username
    while True:
        if new_username in user_dictionary():
            print("Error: user already registered. Please register different user.")
            new_username = str(input("New Username:  \t")).lower()
        else:
            break

    # Request new password and password confirmation.
    new_pw       = str(input("New Password:  \t"))
    new_pw_conf  = str(input("Confirm Password: "))

    # confirm new passwords match
    if new_pw == new_pw_conf:
        # if match, append to file
        formatted_string = f"{new_username}, {new_pw}"
        append_to_file(file_name, formatted_string)

        # print to console
        print(f"\"{new_username}\" was added to \"{file_name}\" file.")
    else:
        print("Error: Passwords do not match.")
    return

### Adding a task ###
def add_task():
    print("Adding a task\n--------------")
    t_owner    = str(input("task owner (user name):\t\t  ")).lower()

    # check if owner is registered as a user
    while True:
        if t_owner in user_dictionary():
            break
        else:
            print("Error: user not registered. Please chose from users below:")
            for u in get_user_list(): print(u)
            t_owner = str(input("Task owner (user name):\t\t  ")).lower()

    t_title    = str(input("Task title:\t\t\t  "))
    t_des      = str(input("Task description:\t\t  "))
    t_date_due = str(input("Task due date (e.g. 31 Jan 2023): "))

    # current date (see https://www.cyberciti.biz/faq/howto-get-current-date-time-in-python/)
    t_date_now = str(date.today().strftime('%d %b %Y'))

    # append to file ('No' at the end to indicate if task is complete or not) 
    formatted_string = f"{t_owner}, {t_title}, {t_des}, {t_date_due}, {t_date_now}, No"
    append_to_file("tasks.txt", formatted_string)

    # message to user console
    print(f"\"{t_owner}\" was assigned with \"{t_title}\" due on \"{t_date_due}\".")
    return

### View all tasks ###
def view_all():
    print("View all tasks\n--------------")

    # get task list
    all_tasks = get_task_list()

    # Read all tasks (note: each task in the list is a dictionary)
    for task in all_tasks:
        print(f"""
Task owner:      {task["owner"]}
Task title:      {task["title"]}
Task desc:       {task["desc"]}
Task due date:   {task["due_date"]}
Task start date: {task["start_date"]}
Task complete?   {task["is_complete"]}
----------------------------""")
    return

### view my tasks ###
def view_mine(user_input):
    print("View my tasks\n--------------")

    # get task list
    all_tasks = get_task_list()

    # Read all lines from the file
    for i, task in enumerate(all_tasks):
        # Check if the username of the person logged in
        # is the same as the username you have read from the file
        if user_input.lower() == task["owner"]:
            
            # display task on the screen (each with a corresponding number)
            print(f"""
Task Nr:         {i + 1}
Task owner:      {task["owner"]}
Task title:      {task["title"]}
Task desc:       {task["desc"]}
Task due date:   {task["due_date"]}
Task start date: {task["start_date"]}
Task complete?   {task["is_complete"]}
----------------------------""")
    
    # allow user to select a specific task or enter -1 to return to menu
    selected_task = int(input("""
Enter task number for further options (or enter -1 to return to menu):
----------------------------
Task number: """))
    if selected_task == -1:
        pass
    else:
        # user can chose to mark the task as complete or edit the task
        task_option = input(f"""Options for task number: {selected_task}
c - mark as complete
e - edit
----------------------------
Selection:""").lower()
        if task_option == "c":
            # call mark task complete function
            mark_task_complete(selected_task)

        elif task_option == "e":
            # call edit task function
            edit_task(selected_task)
        else:
            print("You have made a wrong choice. Start again.")
    return

### Display Statistics ###
def display_statistics():
    print("Display Statistics\n---------------")

    # read task_overview and user_overview
    task_overview = read_file("task_overview.txt")
    user_overview = read_file("user_overview.txt")

    # if file opening delivered error, generate the files
    if task_overview == "error":
        generate_task_overview()
        task_overview = read_file("task_overview.txt")
    if user_overview == "error":
        generate_user_overview()
        user_overview = read_file("user_overview.txt")

    # print to console
    print(task_overview)
    print(user_overview)

    return

def generate_task_overview():
    # computes several statistics and writes them into task_overview.txt file

    # get task list (note: each task in the list is a dictionary)
    all_tasks = get_task_list()

    # number of tasks that have been generated
    nr_tasks = len(all_tasks)

    # number of completed tasks
    nr_task_completed = 0
    for task in all_tasks:
        if task["is_complete"].lower() == "yes":
            nr_task_completed += 1

    # number of uncompleted tasks
    nr_task_uncompleted = 0
    for task in all_tasks:
        if task["is_complete"].lower() == "no":
            nr_task_uncompleted += 1

    # number of tasks that haven’t been completed and are overdue
    nr_task_overdue = 0
    for task in all_tasks:
        # format a string into a date (for it to be compared against an other date)
        # (see https://www.educative.io/answers/how-to-convert-a-string-to-a-date-in-python)
        date_now_obj = datetime.today()
        date_due_obj = datetime.strptime(task["due_date"], "%d %b %Y")
        if task["is_complete"].lower() == "no" and date_now_obj <= date_due_obj:
            nr_task_overdue += 1

        # Percentage of tasks incomplete
        pct_task_incomplete = round(nr_task_uncompleted / nr_tasks, 2)

        # Percentage of tasks overdue
        pct_task_overdue = round(nr_task_overdue / nr_tasks, 2)

    # output an easy to read format
    output = f"""Number of tasks:                     {nr_tasks}
Number of completed tasks:           {nr_task_completed} 
Number of uncompleted tasks:         {nr_task_uncompleted}
Number of task overdue:              {nr_task_overdue}
Percentage of tasks incomplete:      {pct_task_incomplete}
Percentage of tasks overdue:         {pct_task_overdue}"""

    # save output in task_overview.txt
    write_to_file("task_overview.txt", output)
    return

def generate_user_overview():
    # computes several statistics and writes them into user_overview.txt file
    output_list = []

    # number of users registered
    nr_users_registered = len(get_user_list())
    output_list.append(f"Number of users registered:          {nr_users_registered}")

    # get task list (note: each task in the list is a dictionary)
    all_tasks = get_task_list()

    # number of tasks that have been generated and tracked
    nr_tasks = len(all_tasks)
    output_list.append(f"Number of tasks:                     {nr_tasks}")
    output_list.append(f"================================================")

    # For each user: generate specific statistic
    for user in get_user_list():
        
        # number of tasks assigned to that user
        nr_t = 0
        for task in all_tasks:
            if user == task["owner"]:
                nr_t += 1
        
        # percentage of tasks assigned to that user
        pct_t = round(nr_t / nr_tasks, 2)

        # percentage of tasks assigned to that user that have been completed
        nr_t_completed = 0
        for task in all_tasks:
            if user == task["owner"] and task["is_complete"].lower() == "yes":
                nr_t_completed += 1
        pct_t_completed = round(nr_t_completed / nr_tasks, 2)

        # percentage of tasks assigned to that user that must still be completed
        nr_t_uncompleted = 0
        for task in all_tasks:
            if user == task["owner"] and task["is_complete"].lower() == "no":
                nr_t_uncompleted += 1
        pct_t_uncompleted = round(nr_t_uncompleted / nr_tasks, 2)

        # percentage of tasks assigned to that user not yet completed and overdue
        for task in all_tasks:
            nr_t_overdue = 0
            # format a string into a date (for it to be compared against an other date)
            # (see https://www.educative.io/answers/how-to-convert-a-string-to-a-date-in-python)
            date_now_obj = datetime.today()
            date_due_obj = datetime.strptime(task["due_date"], "%d %b %Y")
            if user == task["owner"].lower() and task["is_complete"].lower() == "no" and date_now_obj <= date_due_obj:
                nr_t_overdue += 1
            pct_t_overdue = round(nr_t_overdue / nr_tasks, 2)

        # output an easy to read format
        output_list.append(
f"""User:                                {user}
Tasks assigned:                      {nr_t} 
Tasks assigned         (% of total): {pct_t}
Completed              (% of total): {pct_t_completed}
Incomplete             (% of total): {pct_t_uncompleted}
Incomplete and overdue (% of total): {pct_t_overdue}
------------------------------------------------""")

    # save output in user_overview.txt
    output = "\n".join(output_list)
    write_to_file("user_overview.txt", output)
    return

### Generate Reports ###
def generate_reports():
    print("Generate Reports\n---------------")
    # generates two text files (in easy to read manner)
    generate_task_overview()
    generate_user_overview()
    return


#=====================#
#=== Login Section ===#
#=====================#
### get user login information ###
print("Welcome to the user login")
user_input = str(input("Username:\t")).lower()
pw_input   = str(input("Password:\t"))

### validate name and password ###
is_user_found = False
is_pw_correct = False

# get valid usernames and password
user_dict   = user_dictionary()

while True:
    # keep asking until valid user_input is entered
    while is_user_found == False:
        # check if user_input exists in the user dictionary
        if user_input in user_dict:
            is_user_found = True

        # if user_input is not found
        if is_user_found == False:
            print("wrong user name. try again.")
            user_input = str(input("Username:\t"))
            pw_input = str(input("Password:\t"))

    # once valid user name is entered, check corresponding password
    # and keep asking for new password until the valid one is entered
    while is_pw_correct == False:
        # get corresponding password (from user dictionary) and compare against input
        if user_dict[user_input] == pw_input:
            # entered pw is correct
            is_pw_correct = True
        else: # if no password match occured, ask for new password
            print("wrong password. try again.")
            pw_input = str(input("Password:\t"))

    # break while loop if user found and pw correct
    if is_user_found == True and is_pw_correct == True:
        break

#=====================#
#=== Menue Section ===#
#=====================#
while True:
    # menu for admin and manu all other users
    admin_menu = ""
    menu       = ""

    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    if user_input.lower() == "admin":
        admin_menu = input("""
Please select one of the following Options below:
r  - Registering a user
a  - Adding a task
va - View all tasks
vm - view my task
gr - generate reports
ds - display statistics
e  - Exit
----------------------------
selection: """).lower()

    else:
        menu = input("""
Please select one of the following Options below:
r  - Registering a user
a  - Adding a task
va - View all tasks
vm - View my task
e  - Exit
----------------------------
selection: """).lower()

    if admin_menu == 'r' or menu == 'r':
        # register user function
        reg_user()

    elif admin_menu == 'a' or menu == 'a':
        # add task function
        add_task()

    elif admin_menu == 'va' or menu == 'va':
        # view all tasks function
        view_all()

    elif admin_menu == 'vm' or menu == 'vm':
        # view my tasks function
        view_mine(user_input)

    elif admin_menu == 'e' or menu == 'e':
        # Exit
        print('Goodbye!!!')
        exit()

    elif admin_menu == 'gr':
        # only admin is allowed to generate reports
        generate_reports()

    elif admin_menu == 'ds':
        # only admin is allowed to see statistics
        display_statistics()

    else:
        # on Error
        print("You have made a wrong choice, Please Try again")