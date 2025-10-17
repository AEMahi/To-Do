import datetime as dt
from collections.abc import Callable
from dataclasses import dataclass, field


@dataclass
class Task:
    description: str
    is_done: bool = False
    due_date: dt.datetime | None = None

    def __str__(self) -> str:
        status_desc: str = f'{"[x]" if self.is_done else "[ ]"} {self.description}'

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

    def __len__(self) -> int:
        """Number of tasks"""
        return len(self.tasks)

    def add_task(self) -> None:
        """Ask the user to enter a task and creates it with all features"""

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
        """Print all tasks in self.tasks"""
        if len(self) == 0:
            print('No Tasks')
            return

        for index, task in enumerate(self.tasks, start=1):
            print(f'\nTask {index}: {task}')

    def mark_done(self) -> None:
        """Show tasks, ask user for a task number, and mark that task as done"""
        if len(self) == 0:
            print('No Tasks')
            return

        while True:
            try:
                task_id: int = int(input('\nEnter task number to mark as done: '))
                task: Task = self.tasks[task_id - 1]
            except (IndexError, ValueError):
                print(f'Invalid task id: Please choose integer from 0 ... {len(self)}')
            else:
                task.is_done = True
                print(f'Marked task "{task}" as done')
                break

    def delete_task(self) -> None:
        """Show tasks, ask user for a task number, and remove that task from the list"""
        if len(self) == 0:
            print('No Tasks')
            return

        while True:
            try:
                task_id: int = int(input('\nWhich task would you like to delete? '))
                del self.tasks[task_id - 1]
            except (IndexError, ValueError):
                print('Invalid task number, please re-enter.')
            else:
                break

    def save_to_file(self) -> None:
        """Save all tasks to a JSON file"""
        pass

    def load_from_file(self) -> None:
        """Load tasks from a JSON file"""
        pass

    def run(self) -> None:
        actions: dict[str, Callable[[], None]] = {
            '1': self.add_task,
            '2': self.view_tasks,
            '3': self.mark_done,
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
