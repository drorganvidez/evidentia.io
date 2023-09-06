import os
import shutil


def create_module_module(module):
    # Directories and file paths
    module_path = os.path.join('app', module)
    templates_path = os.path.join(module_path, 'templates')
    templates_module_path = os.path.join(templates_path, module)
    init_path = os.path.join('app', '__init__.py')

    # Check module name
    if os.path.exists(module_path):
        raise Exception(f"Error: A folder named '{module}' already exists in 'app'!")

    # 1. Create the module's sub-directory and its nested directories
    os.makedirs(templates_module_path, exist_ok=True)

    # 2. Create index.html
    with open(os.path.join(templates_module_path, 'index.html'), 'w') as f:
        f.write('{% extends "base_template.html" %}\n\n')
        f.write('{% block title %}' + module + '{% endblock %}\n\n')
        f.write('{% block content %}\n\n{% endblock %}\n')

    # 3. Create __init__.py
    with open(os.path.join(module_path, '__init__.py'), 'w') as f:
        f.write('from flask import Blueprint\n\n')
        f.write(module + '_bp = Blueprint(\'' + module + '\', __name__, template_folder=\'templates\')\n')
        f.write('\nfrom . import routes\n')

    # 4. Create routes.py
    with open(os.path.join(module_path, 'routes.py'), 'w') as f:
        f.write('import logging\n')
        f.write('from flask import render_template\n')
        f.write('from flask_login import login_required\n')
        f.write('from . import ' + module + '_bp\n\n')
        f.write('logger = logging.getLogger(__name__)\n\n\n')
        f.write('@' + module + '_bp.route("/' + module + '")\n')
        f.write('@login_required\n')
        f.write('def index():\n')
        f.write('    logger.info(\'Access ' + module + ' index\')\n\n')
        f.write('    return render_template("' + module + '/index.html")\n')

    # 5. Create forms.py
    with open(os.path.join(module_path, 'forms.py'), 'w') as f:
        f.write('from flask_wtf import FlaskForm\n')

        # Modifying app/__init__.py
        with open(init_path, 'r') as f:
            lines = f.readlines()

        import_idx = None
        register_idx = None

        # Find the location for blueprint import and registration
        for idx, line in enumerate(lines):
            if "# Import blueprints" in line:
                import_idx = idx
            elif "# Register blueprints" in line:
                register_idx = idx

        # Add lines at the found positions, ensuring proper indentation
        if import_idx is not None:
            while not lines[import_idx + 1].strip() == "":
                import_idx += 1
            lines.insert(import_idx + 1, f"    from .{module} import {module}_bp\n")

        if register_idx is not None:
            while not lines[register_idx + 1].strip() == "":
                register_idx += 1
            lines.insert(register_idx + 1, f"    app.register_blueprint({module}_bp)\n")

        if import_idx is None or register_idx is None:
            cleanup_module_directory(module)
            raise Exception(
                f"Error: Insertion point not found in {init_path}. Please check the file and ensure you have the comments '# Import blueprints' and '# Register blueprints' in app/__init__.py.")
        else:
            with open(init_path, 'w') as f:
                f.writelines(lines)


def cleanup_module_directory(module_name):
    """
    Removes the created module directory.
    """
    module_dir = os.path.join('app', module_name)
    if os.path.exists(module_dir):
        shutil.rmtree(module_dir)


if __name__ == '__main__':
    module = input("Please enter the name of the module: ")
    create_module_module(module)
    print("Module successfully created!")
