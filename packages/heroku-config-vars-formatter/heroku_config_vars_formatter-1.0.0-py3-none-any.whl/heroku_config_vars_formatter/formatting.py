def format_text(text):
    try:
        return _format_text(text)
    except Exception as e:
        msg = (
            "The contents of your cache couldn't be formatted."
            " Please make sure you copied the contents of your Heroku config."
        )
        raise ValueError(msg) from e


def _format_text(text):
    text = text.strip("\n")
    if "Config Vars" in text:
        text = text.split("Config Vars\n")[1]
    text = text.split("\nEdit Delete\nKEY")[0]

    components = text.split("\nEdit Delete")
    split_components = [
        [c for c in component.split("\n") if c] for component in components
    ]
    non_empty_split_components = [c for c in split_components if c]

    split_components_clean = [
        [var_name, encode(value)] for (var_name, value) in non_empty_split_components
    ]
    commands = [
        f"export {var_name}={value}" for (var_name, value) in split_components_clean
    ]
    return "\n".join(commands) + "\n"


def encode(text_):
    special_chars = ["&", "!"]
    for char in special_chars:
        text_ = text_.replace(char, f"\\{char}")
    return text_
