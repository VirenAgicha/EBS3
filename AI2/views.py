from flask import Blueprint, redirect, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from werkzeug import datastructures
from .models import Note, TodoItem
from . import db
import json

views = Blueprint('views', __name__)
# Create your views here.


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note Added', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            flash('Note Deleted', category='success')
            db.session.delete(note)
            db.session.commit()
    return jsonify({})


@views.route('/add', methods=['POST'])
def add():
    # get the task name from the form data
    task = request.form.get('task')

    # insert the new task into the database
    new_item = TodoItem(task=task, user_id=current_user.id)
    db.session.add(new_item)
    db.session.commit()
    flash('Task Added', category='success')
    # redirect back to the index page
    return render_template("home.html", user=current_user)


@views.route('/done/<int:item_id>', methods=['POST'])
def done(item_id):
    # update the task as done in the database

    item = TodoItem.query.get(item_id)
    item.done = True
    db.session.commit()
    flash('Task Done', category='success')
    # redirect back to the index page
    return render_template("home.html", user=current_user)


@views.route('/cancel/<int:item_id>', methods=['POST'])
def cancel(item_id):
    # delete the task from the database

    item = TodoItem.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Task Cancelled', category='success')
    # redirect back to the index page
    return render_template("home.html", user=current_user)
