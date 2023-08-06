import importlib
import os
import uuid

from appdirs import AppDirs
from primaryschool.settings import app_author, app_name, app_version

_dirs = AppDirs(app_name, app_author)

user_data_dir_path = _dirs.user_data_dir
user_cache_dir_path = _dirs.user_cache_dir
user_log_dir_path = _dirs.user_log_dir
user_config_dir_path = _dirs.user_config_dir

user_screenshot_dir_path = os.path.join(user_data_dir_path, "screenshots")

for d in [
    user_data_dir_path,
    user_cache_dir_path,
    user_log_dir_path,
    user_config_dir_path,
    user_screenshot_dir_path,
]:
    if not os.path.exists(d):
        os.makedirs(d, exist_ok=True)


def get_copy_path(module_str):
    return os.path.join(user_data_dir_path, module_str) + f".{app_version}.pkl"


def get_default_screenshot_path(module_str, player_name):
    _uuid = str(uuid.uuid4())
    return os.path.join(
        user_screenshot_dir_path, f"{module_str}.{player_name}.{_uuid}.png"
    )
