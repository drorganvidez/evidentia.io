import logging

from flask import render_template
from flask_login import login_required

from . import lecturer_bp
from ..auth.models import User

logger = logging.getLogger(__name__)


@lecturer_bp.route("/lecturer/users/manage")
@login_required
def users_manage():
    logger.info('Access lecturer index')

    users = User.query.all()
    data_collection = [{'Email': user.email} for user in users]
    return render_template('lecturer/users/manage.html', data_collection=data_collection)


@lecturer_bp.route("/lecturer/users/roles")
@login_required
def users_roles():
    logger.info('Access lecturer index')

    return render_template("lecturer/users/roles.html")
