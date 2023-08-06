"""
Note: This breaks if an environment variable is called `KEY`
"""
import pyperclip

from .formatting import format_text


def main():
    text = pyperclip.paste()
    res = format_text(text)
    pyperclip.copy(res)
