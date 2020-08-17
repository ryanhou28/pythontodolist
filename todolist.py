# Write your code here
from datetime import datetime, timedelta

from sqlalchemy import create_engine

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

#-------

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()

class task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

#-----

Base.metadata.create_all(engine)

#-----

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

#------

#new_row = task(task='This is a task!',
#         deadline=datetime.strptime('01-24-2020', '%m-%d-%Y').date())
#session.add(new_row)
#session.commit()

#-----

#rows = session.query(task).all()

#-------

#first_row = rows[0] # In case rows list is not empty

#print(first_row.task) # Will print value of the string_field
#print(first_row.id) # Will print the id of the row.
#print(first_row) # Will print the string that was returned by __repr__ method


program_on = True

while program_on:
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")
    user_choice = input()
    if user_choice == "1":
        today = datetime.today()
        rows = session.query(task).filter(task.deadline == today.date()).all()
        print("Today", datetime.today().day, datetime.today().strftime('%b'))
        if not rows:
            print("Nothing to do!")
        else:
            for tasks in rows:
                print(str(tasks.id) + '. ' + tasks.task)
    elif user_choice == "2":
        for days_n in range(0,7):
            this_day = datetime.today().date() + timedelta(days=days_n)
            rows = session.query(task).filter(task.deadline == this_day).all()
            print("")
            print(this_day.strftime('%A'), str(this_day.day), this_day.strftime('%b') + ':')
            if not rows:
                print("Nothing to do!")
            else:
                counter = 0
                for tasks in rows:
                    counter += 1
                    print(str(counter) + '. ' + tasks.task)
    elif user_choice == "3":
        #All tasks
        rows = session.query(task).order_by(task.deadline).all()
        for tasks in rows:
            print(str(tasks.id) + '. ' + tasks.task + '. ' + str(tasks.deadline.day), tasks.deadline.strftime('%b'))
    elif user_choice == "4":
        rows = session.query(task).filter(task.deadline < datetime.today().date()).all()
        print("Missed tasks:")
        if not rows:
            print("Nothing is missed!")
        else:
            counter = 0
            for tasks in rows:
                counter += 1
                print(str(counter) + '. ' + tasks.task)
        print("")
    elif user_choice == "5":
        print("Enter task")
        task_string = input()
        print("Enter deadline")
        deadline_input = input()
        task_deadline = datetime.strptime(deadline_input, '%Y-%m-%d')
        new_task = task(task=task_string, deadline=task_deadline)
        session.add(new_task)
        session.commit()
        print("The task has been added!")
    elif user_choice == "6":
        rows = session.query(task).order_by(task.deadline).all()
        for tasks in rows:
            print(str(tasks.id) + '. ' + tasks.task + '. ' + str(tasks.deadline.day), tasks.deadline.strftime('%b'))
        print("Choose the number of the task you want to delete:")
        delete_number = int(input())
        specific_row = rows[delete_number-1]
        session.delete(specific_row)
        session.commit()
        print("The task has been deleted!")
    elif user_choice == "0":
        print("Bye!")
        program_on = False
    else:
        pass
