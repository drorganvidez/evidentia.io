import logging

from flask import render_template
from flask_login import login_required

from . import lecturer_bp

logger = logging.getLogger(__name__)


@lecturer_bp.route("/lecturer/users/manage")
@login_required
def users_manage():
    logger.info('Access lecturer index')

    return render_template("lecturer/users/manage.html")


@lecturer_bp.route("/lecturer/users/roles")
@login_required
def users_roles():
    logger.info('Access lecturer index')

    return render_template("lecturer/users/manage.html")
