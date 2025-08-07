# ✅ TODO convert comments in each method into a python docstring
# ✅ TODO start commiting to git and make this a new project
# ✅ TODO use enumerate(self.tasks) to loop through tasks instead for view_tasks()
# ✅ TODO change self.input to 'choice' - no need to make this an attribute, just use a basic variable 
# ✅ TODO use f-strings in print statements instead of print(...,...,...)
# ✅ TODO in view_tasks change 2nd if to an else - only 2 options for length are >0 and =0
# ✅ TODO use try/except block to handle invalid user input choice
# ✅ TODO create optional "due date" feature for any given task

import datetime

class Task:
    description: str
    done: bool
    due_date: datetime.datetime
    delta: datetime.timedelta
    
    def __init__(self, desc: str, due = None, delta = None) -> None:
        self.description = desc
        self.done = False
        self.due_date = due
        self.delta = delta

    def mark_done(self) -> None:
        self.done = True

    def __str__(self) -> str:
        status: str = '[x]' if self.done else '[ ]'
        #print(type(self.due_date))
        if self.due_date is not None:
            if  self.delta > datetime.timedelta(seconds=0):
                if self.done == False:
                    return f'{status} {self.description}: Due {self.due_date.strftime('%B-%d-%Y-%I-%M')}, in {self.delta.days} days, {int(self.delta.seconds // 3600)} hours, and {int((self.delta.seconds % 3600) // 60)} minutes.'
                else:
                    return f'{status} {self.description}: Due {self.due_date.strftime('%B-%d-%Y-%I-%M')}'
            elif datetime.timedelta(seconds=0) == self.delta:
                return f'{status} {self.description}: Due now'
            else:
                if self.done == False:
                    abs_delta = abs(self.delta)
                    return f'{status} {self.description}: Due {self.due_date.strftime('%B-%d-%Y-%I-%M')}, late by {abs_delta.days} days, {int(abs_delta.seconds // 3600)} hours, and {int((abs_delta.seconds % 3600) // 60)} minutes.'
                else:
                    return f'{status} {self.description}: Due {self.due_date.strftime('%B-%d-%Y-%I-%M')}'
        else:
            return f'{status} {self.description}'
        

#if self.due_date is none

# Define the Reminders class to manage the list of tasks
class Reminders:
    tasks: list[Task]

    def __init__(self) -> None:
        self.tasks = []

    def add_task(self) -> None:
        '''Ask the user to enter a task description.
        Create a Task object using that description and add it to self.tasks.
        Print a confirmation message'''
         
        name = input('What is the task? ')
        while True:
            date_choice = input('Do you want a due date? (y/n): ')
            if date_choice.lower() != 'y' and date_choice.lower() != 'n':
                print('Not a valid response')
            elif date_choice.lower() == 'n':
                choice = Task(name)
                self.tasks.append(choice)
                print(f'Added task "{choice}" to Reminder list')
                break
            elif date_choice.lower() == 'y':
                while True:
                    try:
                        date = input('Enter the Date (MM/DD/YYYY): ')
                        date = date.split('/')
                        month = int(date[0])
                        day = int(date[1])
                        year = int(date[2])
                    except ValueError:
                        print('that\'s not a number')
                    else:
                        break
                while True:
                    try:
                        time = input('Enter the time (Hr:Min AM/PM): ')
                        time = time.split(' ')
                        meridiem = time[1]
                        time = time[0]
                        time = time.split(':')
                        hour = int(time[0])
                        minute = int(time[1])
                        if meridiem.lower() == 'pm':
                            hour = hour + 12
                        due_date = datetime.datetime(year, month, day, hour, minute, 0)
                        current_datetime = datetime.datetime.now()
                        delta = due_date - current_datetime
                        choice = Task(name, due_date, delta)
                    except ValueError:
                        print('That\'s not a correct time')
                    except IndexError:
                        print('That\'s not a correct time')
                    except TypeError:
                        print('That\'s not a correct time')
                    else:
                        self.tasks.append(choice)
                        print(f'Added task "{choice}" to Reminder list')
                        break
                    break
                break

    def view_tasks(self) -> None:
        '''Print all tasks in self.tasks.
        Use a loop to show each task with its number and status.
        Print a message if there are no tasks.'''

        if len(self.tasks) > 0:
            for index, task in enumerate(self.tasks, start=1):
                print(f'\nTask {index}: {task}')
        else:
            print('\nNo tasks')
        
        

    def mark_task_done(self) -> None:
        if len(self.tasks) > 0:
            self.view_tasks()
            while True:
                try:
                    choice: int = int(input('\nenter task number to mark as done: '))
                    self.tasks[choice - 1].mark_done()
                except IndexError:
                    print('Invalid task number')
                except ValueError:
                    print('That\'s not a number')
                else:
                    print(f'Marked task "{self.tasks[choice - 1]}" as done' )
                    break
        else:
            print('\nNo tasks')
        
        '''Show tasks, ask user for a task number, and mark that task as done.
        Handle invalid input with try/except and input checks.'''

    def delete_task(self) -> None:
        if len(self.tasks) > 0:
            choice: int = int(input('\nWhich task would you like to delete? '))
            while True:
                try:
                    self.view_tasks()
                    del self.tasks[choice - 1]
                except IndexError:
                    print('invalid task number, please reenter.')
                except ValueError:
                    print('That\'s not a number')
                else:
                    break
        else:
            print('\nNo tasks to delete')
       
        '''Show tasks, ask user for a task number, and remove that task from the list.
        Handle invalid input safely.'''

    def show_menu(self) -> None:
        print('\nTo-Do List Menu')
        print('[1] Add Task')
        print('[2] View Tasks')
        print('[3] Mark Task as Done')
        print('[4] Delete Task')
        print('[5] Quit')

    def run(self) -> None:
        while True:
            self.show_menu()
            choice: int = int(input('Choose an option (1-5): ').strip())
            if choice == 1:
                self.add_task()
            elif choice == 2:
                self.view_tasks()
            elif choice == 3:
                self.mark_task_done()
            elif choice == 4:
                self.delete_task()
            elif choice == 5:
                print('Goodbye!')
                break
            else:
                print('Invalid option. Please choose a number from 1 to 5.')


# Main entry point
if __name__ == '__main__':
    app: Reminders = Reminders()
    app.run()
