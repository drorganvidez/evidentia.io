import logging
from flask import render_template, jsonify, request
from flask_login import login_required
from . import student_bp
from .. import db
from ..auth.models import User

logger = logging.getLogger(__name__)


@student_bp.route("/student")
@login_required
def index():
    logger.info('Access student index')

    return render_template("student/index.html")


@student_bp.route('/student/view/<int:id>')
def view(id):
    user = User.query.get_or_404(id)
    return render_template("student/index.html",
                           user=user)


@student_bp.route('/student/edit/<int:id>')
def edit(id):
    user = User.query.get_or_404(id)
    return render_template("student/edit.html", user=user)


@student_bp.route('/student/delete', methods=['POST'])
def delete():
    try:

        user_id = request.form.get('id')

        if not user_id:
            return jsonify({"message": "ID is required"}), 400

        user = User.query.get(user_id)

        if not user:
            return jsonify({"message": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": "User deleted successfully"}), 200

    except Exception as e:
        from .. import app
        app.logger.error(f"Error deleting user: {str(e)}")
        return jsonify({"message": f"Error: {str(e)}"}), 500
