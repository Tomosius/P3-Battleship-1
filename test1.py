# ANSI color codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Text to be displayed in different colors
text = "Hello, Colorful World!"

# Print text in different colors
print(RED + "This is red text" + RESET)
print(GREEN + "This is green text" + RESET)
print(YELLOW + "This is yellow text" + RESET)
print(BLUE + "This is blue text" + RESET)
print(MAGENTA + "This is magenta text" + RESET)
print(CYAN + "This is cyan text" + RESET)

# Print the original text with the default color
print(text)
