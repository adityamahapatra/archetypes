from importlib import import_module
from importlib.machinery import SourceFileLoader
import importlib.util
import inspect
import os
from pprint import pprint
import sys

# Temporary arrangement. System path would be configured in production.
INSTALL_PATH = "/home/aditya/Dev/projects"
sys.path.append(INSTALL_PATH)


def loadModule(script):
    """Load the given Python script as a module and return it.

    Args:
        script (str): The full path of the Python module.

    Returns:
        module: The module object created from the Python script.
    """
    moduleName, _ = os.path.splitext(os.path.basename(script))
    loader = SourceFileLoader(moduleName, script)
    spec = importlib.util.spec_from_file_location(moduleName, loader=loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules[moduleName] = module
    spec.loader.exec_module(module)
    return module


def getImportedModules(archetypeModule):
    """Extract the modules imported within the given archtype module.

    Args:
        archetypeModule (module): The archtype that builds the rig.

    Returns:
        list[module]: Contains the imported modules.
    """
    modules = []
    for name, obj in inspect.getmembers(archetypeModule):
        if name == "__builtins__":
            continue
        if not inspect.ismodule(obj):
            if not inspect.isclass(obj) and not inspect.isfunction(obj):
                continue
            module = inspect.getmodule(obj)
            modules.append(module)
            continue
        modules.append(obj)
    return modules


def getLibraryVersion(module):
    """Get the version of the library where the given module lives.

    Args:
        module (module): The module whose library version needs to be detected.

    Returns:
        tuple(str, str) | tuple(None, None): Returns the name of the library and it's version.
    """
    if module.__package__:
        libraryName = module.__package__.split(".")[0]

        # Get version data for internal libraries.
        if libraryName in os.listdir(INSTALL_PATH):
            try:
                versionSourceFile = os.path.join(INSTALL_PATH, libraryName, "__init__.py")
                library = loadModule(versionSourceFile)
                version = library.__version__
            except (ImportError, AttributeError):
                version = None
            return libraryName, version

        # Get version data for third-party libraries.
        try:
            library = import_module(libraryName)
            version = library.__version__
        except (ImportError, AttributeError):
            version = None
        return libraryName, version
    return None, None


if __name__ == "__main__":
    # Temporary script path. Actual script path would be derived from from the released Tessa asset (pythonScript).
    SCRIPT = "/home/aditya/Dev/projects/archetypes/src/charGenericRobot/AvA/LodA/archtype.py"

    versionMap = {}
    archtype = loadModule(SCRIPT)
    componentModules = getImportedModules(archtype)
    for module in componentModules:
        libraryName, libraryVersion = getLibraryVersion(module)
        if libraryName is None:
            continue
        versionMap.update({libraryName: libraryVersion})
    pprint(versionMap)
