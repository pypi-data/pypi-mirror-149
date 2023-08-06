def safe_int(v: str):
    try:
        return int(v)
    except Exception:
        return None
