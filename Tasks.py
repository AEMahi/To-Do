from collections.abc import Callable
import datetime as dt
import json

class Task:
    description: str
    done: bool
    due_date: dt.datetime | None
    delta: dt.timedelta | None

    def __init__(self, desc: str, due: dt.datetime | None=None, delta: dt.timedelta | None=None) -> None:
        self.description = desc
        self.done = False
        self.due_date = due
        self.delta = delta

    def mark_done(self) -> None:
        self.done = True

    def __str__(self) -> str:
        status_desc: str = f"{'[x]' if self.done else '[ ]'} {self.description}"

        if not self.due_date or not self.delta:
            return status_desc

        # TODO make time of the due date dynamic string not static at creation
        status_desc_due: str = f'{status_desc}: Due {self.due_date.strftime("%B-%d-%Y-%I-%M")}'

        delta: dt.timedelta = abs(self.delta)
        delta_str: str = f'{delta.days} days, {delta.seconds // 3600} hours, and {(delta.seconds % 3600) // 60} minutes.'
        time_status: str = 'late by' if self.delta < dt.timedelta(seconds=0) else 'in'

        return status_desc_due if self.done else f'{status_desc_due}, {time_status} {delta_str}'

# Define the Reminders class to manage the list of tasks
class Reminders:
    tasks: list[Task]

    def __init__(self) -> None:
        self.tasks = []

    def add_task(self) -> None:
        '''Ask the user to enter a task description.
        Create a Task object using that description and add it to self.tasks.
        Print a confirmation message'''
         
        desc = input('What is the task? ')
        while True:
            date_choice: str = input('Do you want a due date? (y/n): ').lower()

            if date_choice not in {'y', 'n'}:
                print('Not a valid response')

            if date_choice == 'n':
                task: Task = Task(desc)
                self.tasks.append(task)
                print(f'Added task "{task}" to Reminder list')
                break

            if date_choice == 'y':
                while True:
                    try:
                        date: str = input('Enter the Date (MM/DD/YYYY): ')
                        month, day, year = map(int, date.split('/'))
                    except ValueError:
                        print('That\'s not a number')
                    else:
                        break
                while True:
                    try:
                        # TODO double check bugs of time like 12:30 PM
                        time_choice = input('Enter the time (Hr:Min AM/PM): ')
                        time_merid: list[str] = time_choice.split(' ')
                        time, meridiem = time_merid[0], time_merid[1]
                        hour, minute = map(int, time.split(':'))

                        if meridiem.lower() == 'pm' and hour != 12:
                            hour += 12
                        if meridiem.lower() == 'am' and hour == 12:
                            hour = 0

                        due_date = dt.datetime(year, month, day, hour, minute, 0)
                        current_datetime = dt.datetime.now()
                        delta = due_date - current_datetime
                        task_due: Task = Task(desc, due_date, delta)
                    except (ValueError, IndexError, TypeError):
                        print('That\'s not a correct time')
                    else:
                        self.tasks.append(task_due)
                        print(f'Added task "{task_due}" to Reminder list')
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
        '''Show tasks, ask user for a task number, and mark that task as done.
        Handle invalid input with try/except and input checks.'''

        if len(self.tasks) > 0:
            self.view_tasks()
            while True:
                try:
                    task_id: int = int(input('\nEnter task number to mark as done: '))
                    self.tasks[task_id - 1].mark_done()
                except IndexError:
                    print('Invalid task number')
                except ValueError:
                    print('That\'s not a number')
                else:
                    print(f'Marked task "{self.tasks[task_id - 1]}" as done' )
                    break
        else:
            print('\nNo tasks')

    def delete_task(self) -> None:
        '''Show tasks, ask user for a task number, and remove that task from the list.
        Handle invalid input safely.'''

        if len(self.tasks) > 0:
            self.view_tasks()

            while True:
                try:
                    task_id: int = int(input('\nWhich task would you like to delete? '))
                    del self.tasks[task_id - 1]
                except (IndexError, ValueError):
                    print('Invalid task number, please re-enter.')
                else:
                    break
        else:
            print('\nNo tasks to delete')

    def save_to_file(self) -> None:
        """
        Save all tasks to a JSON file.

        Each Task object is converted into a dictionary using its __dict__
        attribute, which stores all instance variables and their values.
        The list of dictionaries is then written to the JSON file.
        """
        
        while True:
            filename: str = input('Please enter name for task file: ')
            if filename[-5:] == '.json':
                break
            print('Oops, please ensure file name extension is .json): ')

        # TODO fix bug: datetime is not JSON serializable
        with open(filename, 'w') as f:
            json.dump([task.__dict__ for task in self.tasks], f)


    def load_from_file(self) -> None:
        """
        Load tasks from a JSON file.

        Reads a list of dictionaries from the JSON file, where each dictionary
        contains the attributes of a Task object. Creates new Task objects
        by unpacking each dictionary (**dict) into the Task constructor.

        If the file is not found, initializes self.tasks as an empty list.
        """

        filename: str = input('Please enter valid task file to load from: ')
        try:
            with open(filename) as f:
                self.tasks = [Task(**item) for item in json.load(f)]
        except FileNotFoundError:
            reset: str = input('No Task file found! Would you like to restart from empty tasks? [y/n]: ').lower()
            if reset == 'y':
                self.tasks = []
        else:
            self.view_tasks()

    def run(self) -> None:
        actions: dict[str, Callable[[], None]] = {
            '1': self.add_task,
            '2': self.view_tasks,
            '3': self.mark_task_done,
            '4': self.delete_task,
            '5': self.save_to_file,
            '6': self.load_from_file,
        }

        while True:
            print('\nTo-Do List Menu')
            print('[1] Add Task')
            print('[2] View Tasks')
            print('[3] Mark Task as Done')
            print('[4] Delete Task')
            print('[5] Save Tasks')
            print('[6] Load Tasks')
            print('[q] Quit')

            choice: str = input('Choose an option: ')
            if choice == 'q':
                print('Goodbye!')
                break

            try:
                actions[choice]()
            except KeyError:
                print('Invalid option. Please choose an option from the menu.')

# Main entry point
if __name__ == '__main__':
    app: Reminders = Reminders()
    app.run()
