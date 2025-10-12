def slugify(value: str) -> str:
    return "".join([x if x.isalnum() else "_" for x in value])