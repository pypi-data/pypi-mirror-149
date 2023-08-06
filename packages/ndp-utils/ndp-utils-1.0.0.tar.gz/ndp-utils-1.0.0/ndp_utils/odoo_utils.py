import ast

import os

MANIFEST_FILES = [
    '__manifest__.py',
    '__odoo__.py',
    '__openerp__.py',
    '__terp__.py',
]

class OdooModules:

    @staticmethod
    def is_module(path):
        """return False if the path doesn't contain an odoo module, and the full
        path to the module manifest otherwise"""

        if not os.path.isdir(path):
            return False
        files = os.listdir(path)
        filtered = [x for x in files if x in (MANIFEST_FILES + ['__init__.py'])]
        if len(filtered) == 2 and '__init__.py' in filtered:
            return os.path.join(
                path, next(x for x in filtered if x != '__init__.py'))
        else:
            return False

    @staticmethod
    def get_modules(path, depth=1):
        """ Return modules of path repo (used in test_server.py)"""
        return sorted(list(OdooModules.get_modules_info(path, depth).keys()))

    @staticmethod
    def get_modules_info(path, depth=1):
        """ Return a digest of each installable module's manifest in path repo"""
        # Avoid empty basename when path ends with slash
        if not os.path.basename(path):
            path = os.path.dirname(path)

        modules = {}
        if os.path.isdir(path) and depth > 0:
            for module in os.listdir(path):
                manifest_path = OdooModules.is_module(os.path.join(path, module))
                if manifest_path:
                    manifest = ast.literal_eval(open(manifest_path).read())
                    if manifest.get('installable', True):
                        modules[module] = {
                            'application': manifest.get('application'),
                            'depends': manifest.get('depends') or [],
                            'auto_install': manifest.get('auto_install'),
                        }
                else:
                    deeper_modules = OdooModules.get_modules_info(os.path.join(path, module), depth - 1)
                    modules.update(deeper_modules)
        return modules