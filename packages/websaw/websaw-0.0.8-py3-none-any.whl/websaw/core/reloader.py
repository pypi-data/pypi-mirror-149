import re
import sys
import os
import click
import importlib
import traceback
from typing import Dict

from .globs import app as om_app
from .loggers import error_logger, get_error_snapshot
from .utils import module2filename
from .static_registry import static_registry

from .core_events import core_event_bus, CoreEvents


def _clear_modules(pckg_name):
    # all files/submodules
    names = [
        name for name in sys.modules
        if (name + ".").startswith(pckg_name + ".")
    ]
    for name in names:
        del sys.modules[name]


class Reloader:

    modules = {}
    errors = {}
    apps_data: Dict[str, list] = {}
    current_import_app: str
    forget_package = staticmethod(_clear_modules)

    @staticmethod
    def read_password_hash():
        """Read admin password hash from WEBSAW_PASSWORD_FILE if exists one."""
        pwf = os.environ["WEBSAW_PASSWORD_FILE"]
        if os.path.exists(pwf):
            with open(pwf, 'r') as f:
                hash = f.read().strip()
            return hash

    @staticmethod
    def get_apps_folder():
        return os.environ["WEBSAW_APPS_FOLDER"]

    @classmethod
    def package_folder(cls, package_name):
        pdir = os.path.dirname(sys.modules[package_name].__file__)
        return pdir

    @classmethod
    def package_folder_path(cls, package_name, *parts):
        return os.path.join(cls.package_folder(package_name), *parts)

    @classmethod
    def register_app_data(cls, app_data):
        app_lst = cls.apps_data.setdefault(cls.current_import_app, [])
        app_lst.append(app_data)

    @classmethod
    def install_reloader_hook(cls):
        core_event_bus.on(CoreEvents.RELOAD_APPS, cls.reimport_apps)

    @classmethod
    def expand_apps_to_reload(cls, *app_names):
        ret = set()
        for app_name in app_names:
            ret.add(app_name)
            module_name = f"apps.{app_name}"
            app = getattr(sys.modules.get(module_name), 'app', None)
            get_all_clients = getattr(app, 'get_all_clients', None)
            if not get_all_clients:
                continue
            clients = get_all_clients()
            for m_name in (capp._module_name for capp in clients):
                if not re.match(r'apps\.\w+', m_name):
                    continue
                ret.add(m_name.split('.')[1])
        return ret

    @classmethod
    def clear_routes(cls, app_name=''):
        app_name.strip('/')
        root = f'/{app_name}' if app_name else ''
        routes = f'{root}/*'
        om_app.router.remove(routes)
        if root:
            om_app.router.remove(root)
            root_slash = f'{root}/'
            for app_data in cls.apps_data.pop(app_name, []):
                for route in app_data.routes:
                    if route.rule == root or route.rule.startswith(root_slash):
                        # already removed
                        continue
                    om_app.router.remove(route)
                static_registry.unregister(app_data.static_base_url, app_name)

    @classmethod
    def reimport_apps(cls, *apps):
        if not apps:
            return
        apps = cls.expand_apps_to_reload(*apps)
        for app in apps:
            cls.forget_package(f"apps.{app}")
            cls.clear_routes(app)
        for app in apps:
            cls.import_app(app, clear_before_import=False)

    @classmethod
    def import_apps(cls):
        """Import or reimport modules"""
        cls.clear_routes()
        folder = cls.get_apps_folder()
        # if first time reload dummy top module
        if not cls.modules:
            path = os.path.join(folder, "__init__.py")
            loader = importlib.machinery.SourceFileLoader("apps", path)
            loader.load_module()
        # Then load all the apps as submodules
        for app_name in os.listdir(folder):
            cls.import_app(app_name, clear_before_import=False)

    @classmethod
    def import_app(cls, app_name: str, clear_before_import=True):
        folder = cls.get_apps_folder()
        path = os.path.join(folder, app_name)
        init = os.path.join(path, "__init__.py")

        if not (
            not app_name.startswith("__")
            and os.path.isdir(path)
            and os.path.exists(init)
        ):
            return

        if clear_before_import:
            cls.clear_routes(app_name)
        cls.current_import_app = app_name

        module_name = f"apps.{app_name}"
        is_loaded = module_name in sys.modules
        try:
            module = cls.modules.get(app_name)
            if module is None:
                if is_loaded:
                    click.secho(f"[X] already loaded {app_name}       ", fg="green")
                else:
                    click.echo(f"[ ] loading {app_name} ...")
            else:
                if is_loaded:
                    click.secho(f"[X] already reloaded {app_name}       ", fg="green")
                else:
                    click.echo(f"[ ] reloading {app_name} ...")
                    # forget the module
                    del cls.modules[app_name]

            if not is_loaded:
                module = importlib.machinery.SourceFileLoader(
                    module_name, init
                ).load_module()
                if hasattr(module, 'websaw_main'):
                    module.websaw_main()
                click.secho(f"\x1b[A[X] loaded {app_name}       ", fg="green")
            cls.modules[app_name] = module
            cls.errors[app_name] = None
        except Exception as err:
            cls.errors[app_name] = traceback.format_exc()
            error_logger.log(
                app_name, get_error_snapshot()
            )
            click.secho(
                f"\x1b[A[FAILED] loading {app_name} ({err})",
                fg="red",
            )
            # clear all files/submodules if the loading fails
            cls.forget_package(module_name)
            return None

    @staticmethod
    def get_registered_routes():
        routes = []
        for route in om_app.routes.values():
            for method, method_obj in route.methods.items():
                func = method_obj.handler
                rule = route.rule
                routes.append(
                    {
                        "rule": rule,
                        "method": method,
                        "filename": module2filename(func.__module__),
                        "action": func.__name__,
                    }
                )
        return [*sorted(routes, key=lambda item: item["rule"])]
