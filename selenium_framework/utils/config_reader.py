
import configparser
import os


class ConfigReader:
    _config = None
    _config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "config",
        "config.ini",
    )

    @classmethod
    def _load(cls):
        if cls._config is None:
            cls._config = configparser.ConfigParser()
            if not os.path.exists(cls._config_path):
                raise FileNotFoundError(
                    f"Config file not found at {cls._config_path}"
                )
            cls._config.read(cls._config_path)
        return cls._config

    @classmethod
    def get_base_url(cls):
        return cls._load().get("ENVIRONMENT", "base_url")

    @classmethod
    def get_browser(cls):
        return os.environ.get("BROWSER", cls._load().get("ENVIRONMENT", "browser"))

    @classmethod
    def is_headless(cls):
        env_override = os.environ.get("HEADLESS")
        if env_override is not None:
            return env_override.lower() == "true"
        return cls._load().getboolean("ENVIRONMENT", "headless")

    @classmethod
    def get_implicit_wait(cls):
        return cls._load().getint("ENVIRONMENT", "implicit_wait")

    @classmethod
    def get_explicit_wait(cls):
        return cls._load().getint("ENVIRONMENT", "explicit_wait")

    @classmethod
    def get_page_load_timeout(cls):
        return cls._load().getint("ENVIRONMENT", "page_load_timeout")

    @classmethod
    def get_credential(cls, key):
        return cls._load().get("CREDENTIALS", key)

    @classmethod
    def get_path(cls, key):
        return cls._load().get("PATHS", key)


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
