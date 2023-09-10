import logging

import pandas as pd
from flask import render_template, request, jsonify
from flask_login import login_required

from . import lecturer_bp
from .. import db
from ..auth.models import User, Role, user_roles
from ..profile.models import UserProfile

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

    data_collection = [{
        'id': user.id,
        'Email': user.email,
        'Apellidos': user.surname(),
        'Nombre': user.name()
    } for user in users]

    return render_template('lecturer/users/manage.html', data_collection=data_collection)


@lecturer_bp.route("/lecturer/users/roles")
@login_required
def users_roles():
    logger.info('Access lecturer index')

    return render_template("lecturer/users/roles.html")


@lecturer_bp.route("/lecturer/users/upload", methods=['POST'])
@login_required
def upload_excel():
    # Verifica si se envió un archivo en la solicitud POST
    if 'file' not in request.files:
        return jsonify({'message': 'No se encontró un archivo Excel en la solicitud'}), 400

    file = request.files['file']

    # Verifica si el archivo tiene una extensión válida (por ejemplo, .xls o .xlsx)
    if file.filename == '' or not file.filename.endswith(('.xls', '.xlsx')):
        return jsonify({'message': 'Formato de archivo no válido'}), 400

    try:
        # Carga el archivo Excel en un DataFrame de pandas
        df = pd.read_excel(file)
    except Exception as e:
        return jsonify({'message': 'Error al leer el archivo Excel'}), 500

    # Itera a través de las filas del DataFrame y crea usuarios
    for index, row in df.iterrows():
        dni = str(row['DNI'])
        nombre = row['NOMBRE']
        apellido = row['APELLIDOS']
        email = row['EMAIL']
        curso = row['CURSO']

        # Evita crear usuarios con datos vacíos o duplicados
        if dni and nombre and apellido and email and curso:
            # Verifica si ya existe un usuario con el mismo correo electrónico
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                continue

            # Crea un nuevo usuario y perfil
            new_user = User(email=email, password="tu_contraseña")  # Cambia "tu_contraseña" por la contraseña deseada
            db.session.add(new_user)
            db.session.flush()

            new_profile = UserProfile(
                user_id=new_user.id,
                name=nombre,
                surname=apellido
            )
            db.session.add(new_profile)

            db.session.commit()

    return jsonify({'message': 'Usuarios creados correctamente'}), 201
