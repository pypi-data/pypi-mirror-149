def update_truth_settings(truth_settings: list, default: list = None) -> None:
    from sonusai import SonusAIError

    if default is not None and len(truth_settings) != len(default):
        raise SonusAIError(f'Length of truth_settings does not match given default')

    required_keys = [
        'function',
        'config',
        'index',
    ]
    for n in range(len(truth_settings)):
        for key in required_keys:
            if key not in truth_settings[n]:
                if default is not None and key in default[n]:
                    truth_settings[n][key] = default[n][key]
                else:
                    raise SonusAIError(f"Missing required '{key}' in truth_settings")
