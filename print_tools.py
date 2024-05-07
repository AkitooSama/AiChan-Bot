#Importing rich modules.
from rich.style import Style
from rich.text import Text

def print_box(text: str) -> None:
    """
    Prints the provided text surrounded by a ascii box.

    Args:
    - text (str): The text to be boxed and printed.
    """
    lines = text.split('\n')
    max_length = max(len(line) for line in lines)
    border = '+' + '-' * (max_length + 2) + '+'
    print(border)
    for line in lines:
        print(f"| {line.ljust(max_length)} |")
    print(border)
    
def str_box(text: str) -> str:
    """
    Generates a string with the provided text surrounded by a ascii box.

    Args:
    - text (str): The text to be boxed.

    Returns:
    - str: A string containing the text surrounded by a box.
    """
    lines = text.split('\n')
    max_length = max(len(line) for line in lines)
    border = '+' + '-' * (max_length + 2) + '+\n'
    boxed_text = border

    for line in lines:
        boxed_text += f"| {line.ljust(max_length)} |\n"

    boxed_text += border
    return boxed_text

def print_side_by_side(text1: str, text2: str) -> Text:
    """
    Prints two strings side by side using different colors for each text line.

    Args:
    - text1 (str): The first text to be displayed.
    - text2 (str): The second text to be displayed.

    Returns:
    - Text: A Rich Text object containing both texts displayed side by side with different colors.
    """
    lines1 = text1.split('\n')
    lines2 = text2.split('\n')
    max_length = max(len(line) for line in lines1 + lines2)

    side_by_side_text = Text()
    for line1, line2 in zip(lines1, lines2):
        side_by_side_text.append(line1.ljust(max_length), style="cyan")
        side_by_side_text.append("   ")
        side_by_side_text.append(line2, style="magenta")
        side_by_side_text.append("\n")

    return side_by_side_text

def print_pink_shades(text: str) -> Text:
    """
    Prints the provided text with shades of pink colors.

    Args:
    - text (str): The text to be displayed with shaded colors.

    Returns:
    - Text: A Rich Text object containing the text displayed with shades of pink colors.
    """
    lines = text.split('\n')
    max_length = max(len(line) for line in lines)

    pink_shades = [
        Style(color=f"#FF00{i*10:02X}", bold=True) for i in range(len(lines))
    ]

    pink_text = Text()
    for i, line in enumerate(lines):
        pink_text.append(line.ljust(max_length), style=pink_shades[i])
        pink_text.append("\n")

    return pink_text

def print_red_shades(text: str) -> Text:
    """
    Prints the provided text with shades of red colors.

    Args:
    - text (str): The text to be displayed with shaded colors.

    Returns:
    - Text: A Rich Text object containing the text displayed with shades of red colors.
    """
    lines = text.split('\n')
    max_length = max(len(line) for line in lines)

    red_shades = [
        Style(color=f"#{255-i*10:02X}0000", bold=True) for i in range(len(lines))
    ]

    red_text = Text()
    for i, line in enumerate(lines):
        red_text.append(line.ljust(max_length), style=red_shades[i])
        red_text.append("\n")

    return red_text

if __name__ == "__main__":
    pass