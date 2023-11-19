from flask import Blueprint, render_template, redirect, url_for
from string import digits
from random import choice

import uuid
import logging

from . import db

from .models import Todo
from .webforms import TodoForm

homepage = Blueprint("homepage", __name__)

@homepage.route('/')
def home():
    form = TodoForm()
    todo_list = Todo.query.where(Todo.complete=='n').order_by(Todo.date_added).all()
    todo_done = Todo.query.where(Todo.complete=='y').order_by(Todo.date_added).all()
    todo_list_count = Todo.query.where(Todo.complete=='n').order_by(Todo.date_added).count()
    todo_done_count = Todo.query.where(Todo.complete=='y').order_by(Todo.date_added).count()
    todo_count = Todo.query.count()
    logging.info(f"Page refresh - todo count {todo_count}")
    return render_template("todo.html", 
                           todo_list=todo_list,
                           todo_done=todo_done,
                           todo_count=todo_count,
                           todo_done_count=todo_done_count,
                           todo_list_count=todo_list_count,
                           form=form)

@homepage.route('/add', methods=['POST'])
def add():
    form = TodoForm()
    code=generate_code()
    logging.debug(f"New code - {code}")
    new_item = Todo(id=uuid.uuid4(),
                    title=form.title.data,
                    code=code)
    db.session.add(new_item)
    db.session.commit()
    logging.info(f"New todo added {new_item.title}")
    return redirect(url_for("homepage.home"))

@homepage.route('/update/<int:id>')
def update(id):
    logging_text = {
        'y' : "Complete",
        'n' : "Not Complete"
    }
    item_to_update = Todo.query.where(Todo.code==id).first()
    item_to_update.complete = 'y' if item_to_update.complete == 'n' else 'n'
    db.session.commit()
    logging.info(f"Todo {item_to_update.title} changed to {logging_text[item_to_update.complete]}")
    return redirect(url_for('homepage.home', 
                            _anchor=str(item_to_update.code)))

@homepage.route('/complete')
def complete():
    todo_list = Todo.query.where(Todo.complete=='n').order_by(Todo.date_added).all()
    for todo in todo_list:
        todo.complete = 'y'
    db.session.commit()
    logging.info(f"Complete all todo items!")
    return redirect(url_for('homepage.home'))

@homepage.route('/notcomplete')
def notcomplete():
    todo_list = Todo.query.where(Todo.complete=='y').order_by(Todo.date_added).all()
    for todo in todo_list:
        todo.complete = 'n'
    db.session.commit()
    logging.info(f"Complete all todo items!")
    return redirect(url_for('homepage.home'))

@homepage.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    item_to_update = Todo.query.where(Todo.code==id).first()
    form=TodoForm()
    old_text = item_to_update.title
    item_to_update.title = form.title.data
    db.session.commit()
    logging.info(f"todo {old_text} changed to {item_to_update.title}")
    return redirect(url_for('homepage.home', 
                            _anchor=str(item_to_update.code)))

@homepage.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    # item_to_delete = Todo.query.get_or_404(id)
    item_to_delete = Todo.query.where(Todo.code==id).first()
    db.session.delete(item_to_delete)
    db.session.commit()
    logging.info(f"todo deleted {item_to_delete.title}")
    return redirect(url_for('homepage.home'))

@homepage.route('/deleteall' , methods=['POST'])
def deleteall():
    items_to_delete = Todo.query.where(Todo.complete=='y').all()
    for item_to_delete in items_to_delete:
        db.session.delete(item_to_delete)
    db.session.commit()
    logging.info("all completed deleted")
    return redirect(url_for('homepage.home'))

def generate_code():
    new_code = 'code'
    while True:
        new_code = ''.join(choice(digits) for i in range(6))
        check_code = Todo.query.where(Todo.code==new_code).first()
        if not check_code:
            break
    return new_code