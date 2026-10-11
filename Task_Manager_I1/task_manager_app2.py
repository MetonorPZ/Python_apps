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
    @classmethod
    def remove_task(cls, title):
        for task in cls.task_list:
            if task.title == title:
                cls.task_list.remove(task)
                break
    @classmethod
    def display_tasks(cls):
        for task in cls.task_list:
            print(f'Title: {task.title}, Description: {task.description}, Due Date: {task.due_date}, Priority: {task.priority}')
        
    @classmethod
    def create_task_from_input(cls):
        title = input("Enter title: ")
        description = input("Enter description: ")
        due_date = input("Enter due date (YYYY-MM-DD): ")
        priority = input("Enter priority (High/Medium/Low): ")
        return cls(title, description, due_date, priority)


def main():
    # Read tasks from parquet file
    try:
        tasks_df = pd.read_parquet('tasks.parquet')

        # Create tasks from DataFrame
        for index, row in tasks_df.iterrows():
            task = Task(row['Title'], row['Description'], row['Due Date'], row['Priority'])
            task.add_task()

        # Display all tasks
        Task.display_tasks()

    except FileNotFoundError:
        print("No existing tasks found. Starting with an empty task list.")

    while True:
        print("1. Add task")
        print("2. Display tasks")
        print("3. Remove task")
        print("4. Quit")
        choice = input("Choose an option: ")

        if choice == "1":
            task = Task.create_task_from_input()
            task.add_task()
        elif choice == "2":
            print("Current tasks:")
            Task.display_tasks()
        elif choice == "3":
            title = input("Enter title of task to remove: ")
            Task.remove_task(title)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

    
    df = pd.DataFrame([(task.title, task.description, task.due_date, task.priority) for task in Task.task_list], columns=['Title', 'Description', 'Due Date', 'Priority'])
    df.to_parquet('tasks.parquet', engine='pyarrow', compression='snappy')

if __name__ == "__main__":
    main()

