import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.auth.models import Role, User, Lecturer, user_roles
from app.profile.models import UserProfile

DATABASE_URI = (
    f"mysql+pymysql://{os.getenv('MYSQL_USER', 'default_user')}"
    f":{os.getenv('MYSQL_PASSWORD', 'default_password')}"
    f"@{os.getenv('MYSQL_HOSTNAME', 'localhost')}:3306/{os.getenv('MYSQL_DATABASE', 'default_db')}"
)

engine = create_engine(DATABASE_URI, echo=True)
Session = sessionmaker(bind=engine)


def add_roles_and_lecturers_and_students():
    session = Session()

    session.query(Lecturer).delete()
    session.query(UserProfile).delete()
    session.query(user_roles).delete()
    session.query(User).delete()
    session.query(Role).delete()
    session.commit()

    for role_name in Role.VALID_ROLES:
        role = Role(name=role_name)
        session.add(role)

    session.commit()

    lecturer_role = session.query(Role).filter_by(name="LECTURER").first()
    student_role = session.query(Role).filter_by(name="STUDENT").first()

    user1 = User(username="profesor1", email="profesor1@profesor1.com", password="profesor1")
    profile1 = UserProfile(name="Profesor", surname="Uno", dni="12345678X", user=user1)
    user1.roles.append(lecturer_role)
    lecturer1 = Lecturer(user=user1)

    user2 = User(username="profesor2", email="profesor2@profesor2.com", password="profesor2")
    profile2 = UserProfile(name="Profesor", surname="Dos", dni="87654321Z", user=user2)
    user2.roles.append(lecturer_role)
    lecturer2 = Lecturer(user=user2)

    session.add(user1)
    session.add(user2)

    alumno1 = User(username="alumno1", email="alumno1@alumno1.com", password="alumno1")
    student_profile1 = UserProfile(name="Alumno", surname="Uno", dni="11112222A", user=alumno1)
    alumno1.roles.append(student_role)

    alumno2 = User(username="alumno2", email="alumno2@alumno2.com", password="alumno2")
    student_profile2 = UserProfile(name="Alumno", surname="Dos", dni="22221111B", user=alumno2)
    alumno2.roles.append(student_role)

    session.add(alumno1)
    session.add(alumno2)

    session.commit()

    session.close()


if __name__ == "__main__":
    add_roles_and_lecturers_and_students()

