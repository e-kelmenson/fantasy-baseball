from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Note


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = (request.form.get('note') or "").strip()
        if not note:
            flash('Note is too short.', category='error')
        elif len(note) > 10000:
            flash('Note must be 10,000 characters or fewer.', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify({"error": "Request body must be a JSON object."}), 400

    note_id = payload.get("noteId")
    if (
        not isinstance(note_id, int)
        or isinstance(note_id, bool)
        or note_id < 1
    ):
        return jsonify({"error": "noteId must be a positive integer."}), 400

    note = db.session.get(Note, note_id)

    if note is None:
        return jsonify({"error": "Note not found."}), 404

    if note.user_id != current_user.id:
        return jsonify({"error": "You cannot delete this note."}), 403

    db.session.delete(note)
    db.session.commit()
    return jsonify({"success": True})