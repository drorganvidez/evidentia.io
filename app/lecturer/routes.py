import logging

from flask import render_template
from flask_login import login_required

from . import lecturer_bp
from .. import db
from ..auth.models import User, Role, user_roles

logger = logging.getLogger(__name__)


@lecturer_bp.route("/lecturer/users/manage")
@login_required
def users_manage():
    logger.info('Access lecturer index')

    lecturer_role = Role.query.filter_by(name="LECTURER").first()
    if not lecturer_role:
        return "Role LECTURER not found", 500

    lecturer_users_ids = [user_role.user_id for user_role in
                          db.session.query(user_roles.c.user_id).filter(user_roles.c.role_id == lecturer_role.id).all()]

    users = User.query.filter(User.id.notin_(lecturer_users_ids)).all()

    data_collection = [{'id': user.id, 'Email': user.email} for user in users]
    return render_template('lecturer/users/manage.html', data_collection=data_collection)


@lecturer_bp.route("/lecturer/users/roles")
@login_required
def users_roles():
    logger.info('Access lecturer index')

    return render_template("lecturer/users/roles.html")
