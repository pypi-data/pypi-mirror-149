def update_config_from_file(name: str, config: dict) -> dict:
    from copy import deepcopy

    from sonusai import SonusAIError
    from sonusai.mixture.load_config import load_config
    from sonusai.mixture.update_truth_settings import update_truth_settings

    new_config = deepcopy(config)

    try:
        given_config = load_config(name)
    except Exception as e:
        raise SonusAIError(f'Error loading config from {name}: {e}')

    # Use default config as base and overwrite with given config keys as found
    for key in new_config:
        if key in given_config:
            if key != 'truth_settings':
                new_config[key] = given_config[key]

    if 'truth_settings' in given_config:
        new_config['truth_settings'] = deepcopy(given_config['truth_settings'])

    if not isinstance(new_config['truth_settings'], list):
        new_config['truth_settings'] = [new_config['truth_settings']]

    default_ts = deepcopy(config['truth_settings'])
    if not isinstance(default_ts, list):
        default_ts = [default_ts]

    update_truth_settings(new_config['truth_settings'], default_ts)

    required_keys = [
        'class_labels',
        'class_weights_threshold',
        'feature',
        'frame_size',
        'noises',
        'noise_augmentations',
        'num_classes',
        'seed',
        'target_augmentations',
        'targets',
        'truth_settings',
        'truth_mode',
        'truth_reduction_function',
    ]
    for key in required_keys:
        if key not in new_config:
            raise SonusAIError(f"Missing required '{key}' in {name}")

    return new_config
