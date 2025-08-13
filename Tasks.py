from dataclasses import dataclass, field
from collections.abc import Callable
import datetime as dt
import json

@dataclass
class Task:
    description: str
    is_done: bool = False
    due_date: dt.datetime | None = None

    def mark_done(self) -> None:
        self.is_done = True

    def __str__(self) -> str:
        status_desc: str = f"{'[x]' if self.is_done else '[ ]'} {self.description}"

        if not self.due_date:
            return status_desc

        delta: dt.timedelta = self.due_date - dt.datetime.now()

        status_desc_due: str = f'{status_desc}: Due {self.due_date.strftime("%B-%d-%Y-%I-%M")}'
        time_status: str = 'late by' if delta < dt.timedelta(seconds=0) else 'in'
        delta_str: str = f'{abs(delta).days} days, {abs(delta).seconds // 3600} hours, and {(abs(delta).seconds % 3600) // 60} minutes.'

        return status_desc_due if self.is_done else f'{status_desc_due}, {time_status} {delta_str}'

@dataclass
class Reminders:
    tasks: list[Task] = field(default_factory=list)

    def add_task(self) -> None:
        '''Ask the user to enter a task and creates it with all features'''

        task: Task = Task(input('What is the task? '))

        while True:
            date_choice: str = input('Do you want a due date? (y/n): ').lower()

            if date_choice not in {'y', 'n'}:
                print('Not a valid response')
                continue

            if date_choice == 'y':
                while True:
                    date: str = input('Enter the Date (MM/DD/YYYY): ')
                    try:
                        month, day, year = map(int, date.split('/'))
                        break
                    except ValueError:
                        print('Oops, please enter a valid month (1-12) day (1-31) and year (yyyy)')

                while True:
                    time_choice: str = input('Enter the time (Hr:Min AM/PM): ')
                    time_merid: list[str] = time_choice.split(' ')

                    try:
                        hour, minute = map(int, time_merid[0].split(':'))
                        meridiem: str = time_merid[1].lower()
                    except ValueError:
                        print('Oops, please enter a valid hour (1-12) and min (0-59)')
                        continue
                    except IndexError:
                        print('Oops, no meridiem found - please enter "am" or "pm" after time with space between')
                        continue
                    else:
                        if meridiem == 'pm' and hour != 12:
                            hour += 12
                        if meridiem == 'am' and hour == 12:
                            hour = 0

                        task.due_date = dt.datetime(year, month, day, hour, minute, 0)
                        break

            self.tasks.append(task)
            print(f'Added task "{task}" to Reminder list')
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
