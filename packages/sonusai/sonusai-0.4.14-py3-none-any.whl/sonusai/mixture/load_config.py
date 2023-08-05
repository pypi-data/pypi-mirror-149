def load_config(name: str) -> dict:
    import yaml

    with open(file=name, mode='r') as f:
        config = yaml.safe_load(f)

    config_variable_substitution(config)
    return config


def config_variable_substitution(config: dict) -> None:
    """Find custom SonusAI variables in given dictionary and substitute their values in place"""
    import yaml

    import sonusai

    for key, value in config.items():
        if isinstance(value, dict):
            config_variable_substitution(value)
        else:
            if value == '${frame_size}':
                config[key] = sonusai.mixture.DEFAULT_FRAME_SIZE
            elif isinstance(value, list):
                for idx in range(len(value)):
                    if isinstance(value[idx], str):
                        value[idx] = value[idx].replace('${default_noise}', sonusai.mixture.DEFAULT_NOISE)
