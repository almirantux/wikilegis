import json
import os
import pkgutil

from django.conf import settings
import importlib
from pip import _internal as pip


PLUGINS_CONFIG_FILE = settings.BASE_DIR + '/.plugins'


def create_config_file():
    if not os.path.exists(PLUGINS_CONFIG_FILE):
        os.mknod(PLUGINS_CONFIG_FILE)
        for _, name, _ in pkgutil.iter_modules(['plugins']):
            remove_plugin(name)
        return True
    else:
        return False


def load_current_plugins():
    create_config_file()
    config_file = open(PLUGINS_CONFIG_FILE, 'r')
    plugins_json = config_file.read()
    config_file.close()

    if plugins_json:
        plugins_dict = json.loads(plugins_json)
    else:
        plugins_dict = {}
    return plugins_dict


def write_config_file(plugins_dict):
    config_file = open(PLUGINS_CONFIG_FILE, 'w')
    config_file.seek(0)
    config_file.truncate()
    config_file.write(json.dumps(plugins_dict, indent=2, sort_keys=True))
    config_file.close()


def get_installed_packages():
    installed = pip.get_installed_distributions()
    installed_packages = [package.project_name for package in installed]
    return installed_packages


def add_plugin(plugin_name):
    plugins_dict = load_current_plugins()
    plugins_dict[plugin_name] = True

    plugin_settings = get_settings(plugin_name)
    plugin_deps = getattr(plugin_settings, 'DEPENDENCIES', None)

    exit_code = 0
    if plugin_deps:
        for dependency in plugin_deps:
            if dependency not in get_installed_packages():
                exit_code = pip.main(['install', dependency])

    if exit_code == 0:
        write_config_file(plugins_dict)
        return True
    else:
        return False


def get_settings(plugin_name):
    settings_path = 'plugins.{}.settings'.format(plugin_name)
    return importlib.import_module(settings_path)


def remove_plugin(plugin_name):
    plugins_dict = load_current_plugins()
    plugins_dict[plugin_name] = False

    write_config_file(plugins_dict)
