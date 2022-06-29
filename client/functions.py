def join_path(url: str, paths: list) -> str:
    """Method returns full url include paths"""

    return f"{url}/{'/'.join(list(filter(None, paths)))}" if any(paths) else url
