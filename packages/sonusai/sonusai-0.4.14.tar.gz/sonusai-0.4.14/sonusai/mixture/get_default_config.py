def get_default_config() -> dict:
    import sonusai
    from sonusai.mixture.load_config import load_config

    try:
        return load_config(sonusai.mixture.DEFAULT_CONFIG)
    except Exception as e:
        raise sonusai.SonusAIError(f'Error loading default config: {e}')
