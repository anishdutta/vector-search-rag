def cache_key_generator(namespace: str, func_name: str, make_hash_key=None, *args, **kwargs) -> str:
    company = kwargs.get('company')
    topic = kwargs.get('topic')
    return f"{namespace}:{func_name}:{company}:{topic}"