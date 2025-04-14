import tqdm
import sys
import os

# 跨平台的单字符输入函数
if os.name == "nt":
    import msvcrt

    def getch():
        return msvcrt.getch().decode("utf-8")

else:
    import tty
    import termios

    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


def load_word_list(file_path):
    words = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            # Decode special notation for umlauted vowels
            def decode_umlaut(text):
                umlaut_map = {
                    # German umlauts
                    '"a': "ä",
                    '"e': "ë",
                    '"i': "ï",
                    '"o': "ö",
                    '"u': "ü",
                    '"A': "Ä",
                    '"E': "Ë",
                    '"I': "Ï",
                    '"O': "Ö",
                    '"U': "Ü",
                    # French accents
                    "\\'e": "é",
                    "`e": "è",
                    "^e": "ê",
                    "^a": "â",
                    "^i": "î",
                    "^o": "ô",
                    "^u": "û",
                    "`a": "à",
                    "`u": "ù",
                    "\\'E": "É",
                    "`E": "È",
                    "^E": "Ê",
                    "^A": "Â",
                    "^I": "Î",
                    "^O": "Ô",
                    "^U": "Û",
                    "`A": "À",
                    "`U": "Ù",
                    "\\,c": "ç",
                    "\\,C": "Ç",
                    "\\oe": "œ",
                }
                for code, char in umlaut_map.items():
                    text = text.replace(code, char)
                return text

            # Apply umlaut decoding to each line
            content = f.read()
            content = decode_umlaut(content)
            lines = [line.strip() for line in content.splitlines()]

        for i in range(0, len(lines), 2):
            word = lines[i] if i < len(lines) else ""
            definition = lines[i + 1] if i + 1 < len(lines) else ""
            words.append((word, definition))
    except FileNotFoundError:
        print(f"Error: {file_path} not found")
    except Exception as e:
        print(f"Error happened when reading: {str(e)}")
    return words


def run():
    word_list = load_word_list("word_list.txt")
    if not word_list:
        print("no valid word list found")
        return
    print("👋\033[1;3;34mYou can choose the reviewing mode now: word/definition (w/d)\033[0m")
    while True:
        mode = getch().lower()
        if mode in ("w", "d"):
            break
        else:
            print("\033[1;3;31mPlease press w or d\033[0m")
            if mode == "c":
                sys.exit(0)

    with tqdm.tqdm(
        total=len(word_list), desc="📖 \033[1;3;33mReviewing\033[0m", unit="word"
    ) as pbar:
        current_index = 0
        while current_index < len(word_list):
            if mode == "w":
                word, definition = word_list[current_index]
            else:
                definition, word = word_list[current_index]

            # Display current word (using ANSI escape codes for color)
            tqdm.tqdm.write(f"\n\033[1;3;32mCurrent: {word}\033[0m")
            # tqdm.tqdm.write("\033[33m[L]View Definition  [Enter]Next  [R]Back  [Q]Quit\033[0m")

            key_pressed = False
            while True:
                key = getch().lower()
                if key == "l" and not key_pressed:
                    # Display definition with color
                    if mode == "w":
                        tqdm.tqdm.write(f"\033[1;3;36mDefinition: {definition}\033[0m")
                    else:
                        tqdm.tqdm.write(f"\033[1;3;36mWord: {definition}\033[0m")
                    key_pressed = True
                elif key in ("\r", "\n"):  # Enter key
                    # Move to next word and update progress
                    current_index += 1
                    pbar.update(1)
                    break
                elif key == "r":  # Back functionality
                    if current_index > 0:
                        # Go back to previous word and reset progress
                        current_index -= 1
                        pbar.update(-1)  # Progress bar goes back
                    else:
                        # Visual feedback
                        tqdm.tqdm.write("\033[1;31mAlready at first word!\033[0m")
                    break  # Exit current word loop
                elif key == "q":
                    tqdm.tqdm.write(f"\033[1;3;31mExiting review session...\033[0m")
                    return
                elif key == "c":
                    tqdm.tqdm.write(f"\033[1;3;31mExiting program...\033[0m")
                    sys.exit(0)
                elif key == "g":  # Go to specific word
                    tqdm.tqdm.write("\033[1;3;33m Enter word number: \033[0m", end="")
                    word_num = input()
                    try:
                        word_num = int(word_num)
                        if word_num < 1 or word_num > len(word_list):
                            tqdm.tqdm.write("\033[1;3;31mInvalid word number\033[0m")
                        else:
                            current_index = word_num - 1
                            pbar.n = current_index
                            pbar.last_print_n = current_index
                            break
                    except ValueError:
                        tqdm.tqdm.write("\033[1;3;31mInvalid input\033[0m")


def main():
    while True:
        print(
            "👋 \033[1;3;34mWelcome to Word Flash! <All rights reserved>\n\033[1;3;35mWhen you're reviewing, some rules you should know: \nEnter: show the next word\nR: show the previous word\nL: show the definition\nG: Go to i-th some word you want\nC: exit the entire program; \nQ: Quitting review session\033[0m"
        )
        run()
        print("\n👋 You finished it! Chouchou, do you want to try again? (y/n)")
        while True:
            key = getch().lower()
            if key == "y":
                break
            elif key == "n":
                print("\n👋 \033[1;3;34mGoodbye! Chouchou~\033[0m")
                sys.exit(0)
            else:
                print("\n👋 \033[1;3;31mPlease press y or n\033[0m")


if __name__ == "__main__":
    main()
