def get_config_from_file(config_file: str) -> dict:
    from sonusai.mixture.get_default_config import get_default_config
    from sonusai.mixture.update_config_from_file import update_config_from_file

    return update_config_from_file(name=config_file, config=get_default_config())
