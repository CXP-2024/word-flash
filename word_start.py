import tqdm
import sys
import os

# 跨平台的单字符输入函数
if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode('utf-8')
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
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines()]
            
        for i in range(0, len(lines), 2):
            word = lines[i] if i < len(lines) else ""
            definition = lines[i+1] if i+1 < len(lines) else ""
            words.append((word, definition))
    except FileNotFoundError:
        print(f"Error: {file_path} not found")
    except Exception as e:
        print(f"Error happened when reading：{str(e)}")
    return words

def main():
    word_list = load_word_list("word_list.txt")
    if not word_list:
        print("no valid word list found")
        return

    italic_purple = "\033[3;35m"  # 3=斜体，35=紫色
    reset_style = "\033[0m" 
    
    with tqdm.tqdm(
    total=len(word_list),
    desc=f"{italic_purple}📖 Reviewing{reset_style}",  
    unit="word",
    bar_format=f"{italic_purple}{{l_bar}}{{bar}}{reset_style} {{n_fmt}}/{{total_fmt}}",  
) as pbar:
        for word, definition in word_list:
            # show word
            tqdm.tqdm.write(f"\n\033[1;3;32mCurrent：{word}\033[0m")
            # tqdm.tqdm.write("L or Enter to go")
            
            key_pressed = False
            while True:
                key = getch().lower()
                if key == 'l' and not key_pressed:
                    tqdm.tqdm.write(f"\033[1;3;36mDefinition：{definition}\033[0m")
                    key_pressed = True
                elif key in ('\r', '\n'):
                    break
                elif key == 'q':
                    return
            pbar.update(1)

if __name__ == "__main__":
    main()
    print("\n👋 You are so great! See you next time!")