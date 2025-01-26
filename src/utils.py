def slugify(value: str) -> str:
    return "".join([x if x.isalnum() else "_" for x in value])


def remove_dash_values(data: list[dict]) -> None:
    for dct in data:
        for key, value in dct.items():
            if value == "-":
                dct[key] = None
    return
