import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%d %b %Y"


class Task:
    def __init__(self, username=None, title=None, description=None, due_date=None, assigned_date=None, completed=None):
        '''
        Inputs:
        username: String
        title: String
        description: String
        due_date: DateTime
        assigned_date: DateTime
        completed: Boolean
        '''
        self.username = username
        self.title = title
        self.description = description
        self.due_date = due_date
        self.assigned_date = assigned_date
        self.completed = completed

    def from_string(self, task_str):
        '''
        Convert from string in tasks.txt to object
        '''
        tasks = task_str.split(", ")
        username = tasks[0]
        title = tasks[1]
        description = tasks[2]
        due_date = datetime.strptime(tasks[4], DATETIME_STRING_FORMAT)
        assigned_date = datetime.strptime(tasks[3], DATETIME_STRING_FORMAT)
        completed = True if tasks[5] == "Yes" else False
        self.__init__(username, title, description,
                      due_date, assigned_date, completed)

    def to_string(self):
        '''
        Convert to string for storage in tasks.txt
        '''
        str_attrs = [
            self.username,
            self.title,
            self.description,
            self.due_date.strftime(DATETIME_STRING_FORMAT),
            self.assigned_date.strftime(DATETIME_STRING_FORMAT),
            "Yes" if self.completed else "No"
        ]
        return ", ".join(str_attrs)

    def display(self):
        '''
        Display object in readable format
        '''
        disp_str = f"Task: \t\t {self.title}\n"
        disp_str += f"Assigned to: \t {self.username}\n"
        disp_str += f"Date Assigned: \t {self.assigned_date.strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {self.due_date.strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {self.description}\n"
        return disp_str


# Read and parse tasks.txt
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = Task()
    curr_t.from_string(t_str)
    task_list.append(curr_t)

# Read and parse user.txt

# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin, password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(', ')
    username_password[username] = password

# Keep trying until a successful login
logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


def validate_string(input_str):
    '''
    Function for ensuring that string is safe to store
    '''
    if ";" in input_str:
        print("Your input cannot contain a ';' character")
        return False
    return True


def check_username_and_password(username, password):
    '''
    Ensures that usernames and passwords can't break the system
    '''
    # ';' character cannot be in the username or password
    if ";" in username or ";" in password:
        print("Username or password cannot contain ';'.")
        return False
    return True


def write_usernames_to_file(username_dict):
    '''
    Function to write username to file

    Input: dictionary of username-password key-value pairs
    '''
    with open("user.txt", "w") as out_file:
        user_data = []
        for k in username_dict:
            user_data.append(f"{k}, {username_dict[k]}")
        out_file.write("\n".join(user_data))

# Added functions:


def reg_user(curr_user):
    # if user is not authorised, do not let them create a new user.
    if curr_user != "admin":
        print("Registering a user requires admin priviledges.\n")
        return
    # if admin, collect username and password of this new user.
    while True:
        new_username = input("New Username: ")
        if new_username not in username_password.keys():
            break
        else:
            print("Username already taken\n")

    new_password = input("New Password: ")

    if not check_username_and_password(new_username, new_password):
        # Username or password is not safe for storage - continue
        return

    # Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    if new_password == confirm_password:
        print("New user added.")
        username_password[new_username] = new_password
        write_usernames_to_file(username_password)
    else:
        print("Passwords do not match.")
        return


def display_statistics():
    num_users = len(username_password.keys())
    num_tasks = len(task_list)

    print("-----------------------------------")
    print(f"Number of users: \t\t {num_users}")
    print(f"Number of tasks: \t\t {num_tasks}")
    print("-----------------------------------")

    # Below is the additional code that is requested in the final part of the task.
    # add functionality to display_statistics() that reads the overview files nad prints them to the screen.
    # if the files dont exist, generate them.
    while True:
        # try to open the file, if it exists leave loop, if not, generate reports and then try again.
        try:
            user_overview = open("user_overview.txt", 'r')
            break
        except FileNotFoundError:
            generate_report()
    while True:
        try:
            task_overview = open("task_overview.txt", 'r')
            break
        except FileNotFoundError:
            generate_report()

    # next, read each line in the file and print it to the screen.
    for line in user_overview:
        print(line)
    user_overview.close()
    # do the same loop to print task_overview
    for line in task_overview:
        print(line)
    task_overview.close()


def add_task():
    # Add a new task
    # Prompt a user for the following:
    #     A username of the person whom the task is assigned to,
    #     A title of a task,
    #     A description of the task and
    #     the due date of the task.

    # collect the username of the person being assigned the task.
    while True:
        task_username = input("name of user being assigned this task: ")

    # check if it is a valid username.
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
        else:
            break

    # Get title of task and ensure safe for storage
    while True:
        task_title = input("Title of task: ")
        if validate_string(task_title):
            break

    # Get description of task and ensure safe for storage
    while True:
        task_description = input("What is the task description: ")
        if validate_string(task_description):
            break

    # Obtain and parse due date
    while True:
        try:
            task_due_date = input("Due date of task (DD MON YYYY): ")
            due_date_time = datetime.strptime(
                task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Obtain and parse current date
    curr_date = date.today()

    # Create a new Task object and append to list of tasks
    new_task = Task(task_username, task_title,
                    task_description, due_date_time, curr_date, False)
    task_list.append(new_task)

    # Write to tasks.txt
    with open("tasks.txt", "w") as task_file:
        task_file.write("\n".join([t.to_string() for t in task_list]))
        print("Task successfully added.")


def view_all():  # View all tasks
    print("-----------------------------------")

    if len(task_list) == 0:
        print("There are no tasks.")
        print("-----------------------------------")

    for t in task_list:
        print(t.display())
        print("-----------------------------------")


def view_mine(task_list):  # View my tasks
    print("-----------------------------------")
    # start at false, and if user is in the database of tasks, then change to true and display that user's tasks.
    has_task = False

    for t in range(0, len(task_list)):
        if task_list[t].username == curr_user:
            has_task = True
            print(f"ID: {t}\n" + task_list[t].display())
            print("-----------------------------------")

    if not has_task:
        print("You have no tasks.")
        print("-----------------------------------")

    # to add the additional functionality.
    while True:
        choice = input(
            "Select one of the options below: \n\ts - Select task\n\te - exit to menu\n\t: ")
        # if choose select task, navigate to the correct function.
        if choice == "s":
            task_id = int(
                input("Which task would you like to select? (-1 to exit)"))
            if task_id > 0 and task_id <= len(task_list):
                print(
                    f"You've selected task {task_id}. What would you like to do?")
                choice = input("Mark as complete (c)\ edit the task (e): ")
                if choice == 'e':
                    choice = input(
                        "Change due date (d)/change asignee(a): ")
                    if choice == 'd':
                        change_due_date(t)
                        break
                    elif choice == 'a':
                        change_asignee(t)
                        break
                elif choice == 'c' and not task_list[t].completed:
                    completed(t)
                elif task_list[t].complete:
                    print("Task is already complete.")
                else:
                    print("Invalid selection")
            elif task_id > len(task_list):
                print("Invalid choice")
                return
        elif choice == 'e':
            break


def change_due_date(index):
    # a function to update the task.txt file with updated due date
    for i in range(0, len(task_data)):
        task_data[i] = task_data[i].split(', ')
        # read and create a variable we can manipulate and assign.
    # replace old due date with new one.
    task_data[index][4] = input(
        "Please enter new date (e.g. 21 Jul 2022) ").strip()
    for i in range(0, len(task_data)):
        task_data[i] = ", ".join(task_data[i])
    # write the file back from ground up. - there is definitely a more elegant way to do this.
    with open("tasks.txt", "w+") as task_file:
        task_file.write("\n".join([t for t in task_data]))
        print("Date successfully changed.")


def change_asignee(index):
    # a function to update the task.txt file with updated employee
    for i in range(0, len(task_data)):
        task_data[i] = task_data[i].split(', ')
        # read and create a variable we can manipulate and assign.
    # replace old user with new one.
    task_data[index][0] = input(
        "Please enter user: ").strip()
    # once we have the user to reassign if it is a valid user, update the tasks file.
    if task_data[index][0] in username_password.keys():
        for i in range(0, len(task_data)):
            task_data[i] = ", ".join(task_data[i])
    else:
        print("User not found.\nReturning to menu.")
        return
    # update file
    with open("tasks.txt", "w+") as task_file:
        task_file.write("\n".join([t for t in task_data]))
        print("User successfully changed.")


def completed(index):
    # a function to update the task.txt file with updated employee
    for i in range(0, len(task_data)):
        task_data[i] = task_data[i].split(', ')
        # read and create a variable we can manipulate and assign.
    # replace old due date with new one.
    if curr_user != "admin" or curr_user != task_data[index][0]:
        print("Only admin or user assigned to task can complete. Returning to menu.")
        return
        # User can only complete a task if it is their task or if the admin is completing it.

    # next, if the task is incomplete, set it to complete and update task_data.
    if task_data[index][5] == "No":
        for i in range(0, len(task_data)):
            task_data[index][5] = "Yes"
            task_data[i] = ", ".join(task_data[i])

    # update the file.
    with open("tasks.txt", "w+") as task_file:
        task_file.write("\n".join([t for t in task_data]))
        print("Task completed.")


# add a function to generate reports.
def generate_report():
    # should generate two text files

    # total number of tasks generated.
    total_tasks = len(task_list)
    # total number of completed tasks/incomplete tasks
    complete_tasks = 0
    incomplete_tasks = 0
    overdue_tasks = 0
    for task in task_list:
        if task.completed == True:
            complete_tasks += 1
        else:
            incomplete_tasks += 1

    # for the overdue tasks, we need to compare the due date of the task with the current date.
    # IF IT DOESNT WORK CHECK THIS.
        if task.due_date < datetime.today():
            overdue_tasks += 1
    task_overview_list = [total_tasks, complete_tasks, incomplete_tasks, overdue_tasks, str(round(
        (complete_tasks * 100 / total_tasks))), str((round(incomplete_tasks * 100 / total_tasks)))]
    # Since the task has specified that the text files show text in an easy to read way, I've interpreted that to mean, in plain english with statements labelling what the data is.
    with open("task_overview.txt", 'w') as file:
        file.write(
            "Task Overview document\n-----------------------------------\n")
        file.write(
            f"Total tasks generated: {task_overview_list[0]}\nNumber of Completed tasks: {task_overview_list[1]}\nNumber of incomplete tasks: {task_overview_list[2]}\nNumber of overdue tasks: {task_overview_list[3]}\n")
        file.write("-----------------------------------\n")
        file.write(
            f"Percentage of complete tasks: {task_overview_list[4]}%\nPercentage of incomplete tasks: {task_overview_list[5]}%")
        print("task_overview.txt has been generated.")

    # for the second file, user_overview, we need to generate a text file with:
    # the total number of users registered
    total_users = len(username_password.keys())

    # total number of of tasks
    # we have this already in our variable total_tasks.

    # for each user:
    # the total number of tasks assigned to that user
    # create a dictionary for each user and the value will be their total number of tasks.
    task_per_user = {}
    username_list = []
    for key in username_password.keys():
        # this is effectively to order the dictionary we're creating.
        username_list.append(key)
        n = 0
        for task in task_list:
            if task.username == key:
                n += 1
        task_per_user[key] = n
    # percentage of the total number of tasks assigned to that user.
    # & percentage of the tasks assigned to that user that have been completed
    # & percentage of the tasks assigned to that user that have not been completed
    # stores the percentage of users tasks as share of total tasks.
    user_task_percent = [0 for _ in range(0, len(username_list))]
    user_complete_percent = [0 for _ in range(0, len(username_list))]
    user_incomplete_percent = [0 for _ in range(0, len(username_list))]
    user_overdue_percent = [0 for _ in range(0, len(username_list))]
    for n in range(0, len(username_list)):
        user_task_percent[n] = (
            task_per_user[username_list[n]] * 100) / total_tasks
        # above we've collected the total tasks for this user, * 100 and divided by the total number of tasks to calculate the percentage share of this user's task.
        # below we've a for loop that looks at all tasks belonging to this user and if it is completed, adding one to the completed section. at the end of this loop we will calculate the percentage.
        for task in task_list:
            if task.username == username_list[n] and task.completed == True:
                user_complete_percent[n] += 1
            if task.username == username_list[n] and task.completed == False:
                # this will do the same as above but count only incomplete tasks.
                user_incomplete_percent[n] += 1
            if task.username == username_list[n] and task.completed == False and task.due_date < datetime.today():
                user_overdue_percent[n] += 1

        # we have calculated each of the important pieces of information, now turn them into percentages and finalise the lists.
        if task_per_user[username_list[n]] != 0:
            # this is to avoid a divide by zero error
            user_complete_percent[n] = round(
                user_complete_percent[n] * 100 / task_per_user[username_list[n]], 2)
            user_incomplete_percent[n] = round(
                user_incomplete_percent[n] * 100 / task_per_user[username_list[n]], 2)
            user_overdue_percent[n] = round(
                user_overdue_percent[n] * 100 / task_per_user[username_list[n]], 2)

    with open("user_overview.txt", "w") as file:
        file.write("User Overview Document\n")
        file.write("-----------------------------------\n")
        for n in range(0, len(username_list)):
            file.write(f"User: {username_list[n]}\n")
            file.write(
                f"Total tasks belonging to this user: {task_per_user[username_list[n]]}\n")
            file.write(f"Percentage of total tasks: {user_task_percent[n]}\n")
            file.write(
                f"Percentage of user's tasks that are complete: {user_complete_percent[n]}%\n")
            file.write(
                f"Percentage of user's tasks that are incomplete: {user_incomplete_percent[n]}%\n")
            file.write(
                f"Percentage of user's tasks that are overdue: {user_overdue_percent[n]}%\n")
            file.write("-----------------------------------\n")
    # percentage of the tasks assigned to that user that have not been completed and are overdue.


########################## Main Program #########################
while True:
    # Get input from user
    print()
    if curr_user == 'admin':
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - view my task
    gr - Generate Reports
    ds - display statistics
    e - Exit
    : ''').lower()
    else:
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my tasks
    gr - Generate Reports
    ds - Display Statistics
    e - Exit
    : ''').lower()

    if menu == 'r':  # Register new user (if admin)
        reg_user(curr_user)
    elif menu == 'a':  # Add a new task
        add_task()
    elif menu == 'va':  # View all tasks
        view_all()
    elif menu == 'vm':  # View my tasks
        view_mine()
    elif menu == "gr":
        generate_report()
    elif menu == 'ds' and curr_user == 'admin':  # If admin, display statistics
        display_statistics()
    elif menu == 'e':  # Exit program
        print('Goodbye!!!')
        exit()
    else:  # Default case
        print("You have made a wrong choice, Please Try again")
