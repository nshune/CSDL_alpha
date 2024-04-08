
collect_ignore_glob = ["*__init__.py"]

from pathlib import Path
from pytest import Module

package_loc = Path(__file__).parent

additional_modules = list((package_loc / "csdl_alpha" / "src" / "operations").glob("*.py"))
additional_modules += list((package_loc / "csdl_alpha" / "src" / "operations" / "set_get").glob("*.py"))

def pytest_collect_file(file_path, path, parent):
    if file_path in additional_modules:
        return Module.from_parent(path=file_path, parent=parent)
    else:
        return None