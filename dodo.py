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
            'file_dep': [f'{TRANDIR}/reaboo.mo'],
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
    ignore_dir = '.buildozer,.git,.venv,__pycache__,build,dist,' \
        + 'CardStack,Swiper,source'
    yield {
        'actions': ['flake8 --extend-exclude={}'.format(ignore_dir)],
        'name': "pep8"}
    yield {
        'actions': ['pydocstyle --match-dir=\'^(?!.*(\\{})).*$\''.format(
            ignore_dir.replace('.', '\\.').replace(',', '|')
            )],
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
            'actions': ['python main.py'],
            'task_dep': ['mo'],
           }


def task_wheel():
    """Generate whl file."""
    return {
        'actions': ['python -m build -n -w'],
        'file_dep': ['pyproject.toml']
        }


def task_buildozer():
    """Generate apk file."""
    return {
        'actions': ['buildozer android debug']
        }
