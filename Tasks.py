# ✅ TODO convert comments in each method into a python docstring
# ✅ TODO start commiting to git and make this a new project
# ✅ TODO use enumerate(self.tasks) to loop through tasks instead for view_tasks()
# ✅ TODO change self.input to 'choice' - no need to make this an attribute, just use a basic variable 
# ✅ TODO use f-strings in print statements instead of print(...,...,...)
# ✅ TODO in view_tasks change 2nd if to an else - only 2 options for length are >0 and =0
# ✅ TODO use try/except block to handle invalid user input choice
# TODO create optional "due date" feature for any given task

class Task:
    description: str
    done: bool
    
    def __init__(self, desc: str) -> None:
        self.description = desc
        self.done = False

    def mark_done(self) -> None:
        self.done = True

    def __str__(self) -> str:
        status: str = '[x]' if self.done else '[ ]'
        return f'{status} {self.description}'

# Define the Reminders class to manage the list of tasks
class Reminders:
    tasks: list[Task]

    def __init__(self) -> None:
        self.tasks = []

    def add_task(self) -> None:
        '''Ask the user to enter a task description.
        Create a Task object using that description and add it to self.tasks.
        Print a confirmation message'''
         
        choice = Task(input('What is the task? '))
        self.tasks.append(choice)
        print(f'Added task "{choice}" to Reminder list')


    def view_tasks(self) -> None:
        if len(self.tasks) > 0:
            for index, task in enumerate(self.tasks, start=1):
                print(f'\nTask {index}: {task}')
        else:
            print('\nNo tasks')
        
        '''Print all tasks in self.tasks.
        Use a loop to show each task with its number and status.
        Print a message if there are no tasks.'''

    def mark_task_done(self) -> None:
        if len(self.tasks) > 0:
            self.view_tasks()
            while True:
                try:
                    choice = int(input('\nenter task number to mark as done: '))
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
            choice = int(input('\nWhich task would you like to delete? '))
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
            choice: str = input('Choose an option (15): ').strip()
            if choice == '1':
                self.add_task()
            elif choice == '2':
                self.view_tasks()
            elif choice == '3':
                self.mark_task_done()
            elif choice == '4':
                self.delete_task()
            elif choice == '5':
                print('Goodbye!')
                break
            else:
                print('Invalid option. Please choose a number from 1 to 5.')


# Main entry point
if __name__ == '__main__':
    app: Reminders = Reminders()
    app.run()
