"""Automating task dependency management and execution."""


from doit.tools import create_folder

TRANDIR = 'po/ru_RU.UTF-8/LC_MESSAGES'  # Container for translations


def task_gitclean():
    """Clean all generated files not tracked by GIT."""
    return {
            'actions': ['git clean -df'],
           }


def task_html():
    """Make HTML documentation."""
    return {
            'actions': ['sphinx-build -M html source build'],
           }


def task_test():
    """Perform tests."""
    yield {
        'actions': ['coverage run -m unittest Database/tests_database.py'],
        'name': "run"}
    yield {
        'actions': ['coverage report'],
        'verbosity': 2,
        'name': "report"}


def task_peps():
    """Check if all .py files are satisfies PEP below."""
    yield {
        'actions': ['flake8 --extend-exclude=.venv,source'],
        'name': "pep8"}
    yield {
        'actions': ['pydocstyle --match-dir=\'^(?!.*(\\.venv|source)).*$\''],
        'name': "pep257"}


def task_pot():
    """Create `.pot` file."""
    return {
            'actions': ['pybabel extract -F babel.cfg . -o reaboo.pot'],
            'file_dep': ['reaboo.kv'],
            'targets': ['reaboo.pot'],
           }


def task_po():
    """Update translations."""
    return {
            'actions': ['pybabel update --ignore-pot-creation-date -D reaboo '
                        + '-i reaboo.pot -l ru_RU.UTF-8 -d po'],
            'file_dep': ['reaboo.pot'],
            'targets': [f'{TRANDIR}/reaboo.po'],
           }


def task_mo():
    """Compile translations."""
    return {
            'actions': [
                (create_folder, [TRANDIR]),
                f'pybabel compile -D reaboo -i {TRANDIR}/reaboo.po '
                + '-l ru_RU.UTF-8 -d po'
                       ],
            'file_dep': [f'{TRANDIR}/reaboo.po'],
            'targets': [f'{TRANDIR}/reaboo.mo'],
           }


def task_reaboo():
    """Run application."""
    return {
            'actions': ['python3 main.py'],
            'task_dep': ['mo'],
           }

def task_wheel():
    """Create wheel file."""
    return {
        'actions': ['python -m build -n -w'],
        'file_dep': ['pyproject.toml']
        }