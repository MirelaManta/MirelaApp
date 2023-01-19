from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)  # views as a blueprint means that is has a bunch of routes inside it.


# creating the routes(the URLs where users can actually go to)
@views.route('/', methods=['GET', 'POST'])
@ login_required  # cannot go to the home page unless you're logged in
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 5:
            flash('Note is too short! Give it another try, words are meaningful...\U0001F609', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added and well-kept! \U0001F92B', category='success')
    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})
