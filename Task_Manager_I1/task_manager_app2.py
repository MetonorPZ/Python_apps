import pandas as pd

class Task:
    # lista
    task_list = []
    # argumenty
    def __init__(self, title, description, due_date, priority):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
    # add task to the list
    def add_task(self):
        Task.task_list.append(self)

    def display_tasks(self):
        for task in Task.task_list:
            print(f'Title: {task.title}, Description: {task.description}, Due Date: {task.due_date}, Priority: {task.priority}')
        

x = Task('Task 1', 'Description of Task 1', '2023-12-31', 'High')
x.add_task()
y = Task('Task 2', 'Description of Task 2', '2023-12-30', 'Medium')
y.add_task()
z = Task('Task 3', 'Description of Task 3', '2023-12-29', 'Low')
z.add_task()
w = Task('Task 4', 'Description of Task 4', '2023-12-28', 'High')
w.add_task()
v = Task('Task 5', 'Description of Task 5', '2023-12-27', 'Medium')
v.add_task()
u = Task('Task 6', 'Description of Task 6', '2023-12-26', 'Low')
u.add_task()

x.display_tasks()

