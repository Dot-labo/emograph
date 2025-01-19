def remove_null_values(data: dict | list) -> dict | list:
    """
    nullの項目を再帰的に削除
    """
    if isinstance(data, dict):
        return {k: remove_null_values(v) for k, v in data.items() if v is not None}
    elif isinstance(data, list):
        return [remove_null_values(item) for item in data]

    return data
