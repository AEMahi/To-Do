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
        self.input = Task(input('What is the task? '))
        self.tasks.append(self.input)
        print('Added task "', self.input, '" to Reminder list')
        #Ask the user to enter a task description.
        #Create a Task object using that description and add it to self.tasks.
        #Print a confirmation message

    def view_tasks(self) -> None:
        if len(self.tasks) > 0:
            for counter in range(0, len(self.tasks)):
                print('\nTask ', counter + 1, ': ',self.tasks[counter], )
        if len(self.tasks) == 0:
            print('\nNo tasks')
        
        #Print all tasks in self.tasks.
        #Use a loop to show each task with its number and status.
        #Print a message if there are no tasks.

    def mark_task_done(self) -> None:
        if len(self.tasks) > 0:
            self.view_tasks()
            while True:
                self.input = int(input('\nenter task number to mark as done: '))
                if self.input >= 1 and self.input <= len(self.tasks):
                    self.tasks[self.input - 1].mark_done()
                    print('Marked task "',self.tasks[self.input - 1],'" as done' )
                    break
                else:
                    print('Not a valid task number')
        else:
            print('\nNo tasks')
        
        #Show tasks, ask user for a task number, and mark that task as done.
        #Handle invalid input with try/except and input checks.

    def delete_task(self) -> None:
        if len(self.tasks) > 0:
            self.input = int(input('\nWhich task Would you like to delete? '))
            while True:
                self.view_tasks()
                if self.input >= 1 and self.input <= len(self.tasks):
                    del self.tasks[self.input - 1]
                    break
                else:
                    print('invalid task number, please reenter.')
        else:
            print('\nNo tasks to delete')
       
        #Show tasks, ask user for a task number, and remove that task from the list.
        #Handle invalid input safely.

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