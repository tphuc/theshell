#!/usr/bin/env python3
import curses
import subprocess
""" 
reference:
https://docs.python.org/3/library/curses.html#module-curses
https://steven.codes/blog/cs10/curses-tutorial/
https://stackoverflow.com/questions/21784625/how-to-input-a-word-in-ncurses-screen
"""
def process_KEY_UP(window, input):
    from global_vars import HISTORY_STACK, STACK_CURRENT_INDEX, PROMPT
    try:
        curs_pos = curses.getsyx()

        if input not in [HISTORY_STACK[STACK_CURRENT_INDEX],'\n','']:
            HISTORY_STACK.append(input)
            STACK_CURRENT_INDEX -= 1

        if abs(STACK_CURRENT_INDEX) != len(HISTORY_STACK): # Not meet the start
            window.deleteln()
            window.addstr(curs_pos[0], 0, PROMPT + HISTORY_STACK[STACK_CURRENT_INDEX-1]) #print the previous
            input = HISTORY_STACK[STACK_CURRENT_INDEX-1]
            STACK_CURRENT_INDEX -= 1
        else:
            if input is not HISTORY_STACK[0]: # EndOfStack
                window.deleteln()
                window.addstr(curs_pos[0], 0, PROMPT + HISTORY_STACK[0])
                input = HISTORY_STACK[0]
        return input
    except IndexError:
        pass
def process_KEY_DOWN(window, input):
    from global_vars import STACK_CURRENT_INDEX, HISTORY_STACK, PROMPT
    try:
        curs_pos = curses.getsyx()

        if input not in [HISTORY_STACK[STACK_CURRENT_INDEX],'\n','']:
            HISTORY_STACK.append(input)
            STACK_CURRENT_INDEX += 1

        if STACK_CURRENT_INDEX != -1: # Not meet the end of stack
            window.deleteln()
            window.addstr(curs_pos[0], 0, PROMPT + HISTORY_STACK[STACK_CURRENT_INDEX+1]) #print the previous
            input = HISTORY_STACK[STACK_CURRENT_INDEX+1]
            STACK_CURRENT_INDEX += 1
        else:
            if input is not HISTORY_STACK[-1]: # EndOfStack
                window.deleteln()
                window.addstr(curs_pos[0], 0, PROMPT + HISTORY_STACK[-1])
                input = HISTORY_STACK[-1]
        return input
    except IndexError:
        pass

def my_raw_input(window):
    from global_vars import PROMPT,HISTORY_STACK,STACK_CURRENT_INDEX
    curs_pos = curses.getsyx()
    window.addstr(curs_pos[0], 0, PROMPT)

    char = chr(window.getch())
    input = "" # inittial input

    while char not in ['\n']:

        if char == chr(curses.KEY_UP):
            input = process_KEY_UP(window, input)
            curs_pos = curses.getsyx()
            curses.setsyx(curs_pos[0],len(PROMPT+input))
            curses.doupdate()
            char = ''  # reset the char empty

        if char == chr(curses.KEY_DOWN):
            input = process_KEY_DOWN(window, input)
            curs_pos = curses.getsyx()
            curses.setsyx(curs_pos[0],len(PROMPT+input))
            curses.doupdate()

            char = ''  # reset the char empty

        if char == chr(curses.KEY_LEFT):
            curs_pos = curses.getsyx()
            curses.setsyx(curs_pos[0], curs_pos[1] - 1)
            curses.doupdate()
            char = ''

        if char == chr(curses.KEY_RIGHT):
            curs_pos = curses.getsyx()
            curses.setsyx(curs_pos[0], curs_pos[1] + 1)
            curses.doupdate()
            char = ''

        curs_pos = curses.getsyx()
        window.addstr(curs_pos[0], curs_pos[1], char)
        input += char
        char = chr(window.getch())

    
    if input not in ['\n','']:
        HISTORY_STACK.append(input)
        STACK_CURRENT_INDEX = -1

    window.addstr("\n")
    window.refresh()

    return input

def main():

    window = curses.initscr()
    window.keypad(True)
    curses.noecho()
    while True:
        choice = my_raw_input(window)
        #choice = input("bash& ")
        if choice == 'exit':
            break
        else:
            try:
                """
                #curses.noecho()
                output = subprocess.check_output(choice.split()).decode()
                ls = output.split('\n')
                for l in ls:
                    window.addstr(l)
                    window.addstr('\n')
                pass
                """
                #urses.raw()
                a = subprocess.run(choice.split())
                #curses.noraw()
                with open('history','w') as f:
                    f.write(str(a.stdout))
                
            except Exception:
                pass

    curses.endwin()


if __name__ == "__main__":

    from global_vars import HISTORY_STACK, STACK_CURRENT_INDEX
    main()
    with open('history','w') as f:
        f.write("\n".join(HISTORY_STACK))