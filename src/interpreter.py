import commandHandler as ch
from getpass import getpass
import simple_term_menu as stm

# from json import load
from os import system as sys, name as os_name

# import datetime
import commons


def clear_screen():
    return sys("cls" if "nt" in os_name else "clear")


def interpreterCommands(cmd):
    cmd = cmd[1:].lower()

    if cmd == "show settings":
        print("<< SETTINGS >>")
        print(str(commons.settings)[1:-1])

    elif cmd == "help":
        print(commons.HELP_TEXT)

    elif cmd == "quit" or cmd == "exit":
        print("Bye!")
        ch.quit()
        exit()


clear_screen()
command_mode = bool(commons.settings["commandMode"])
ch = ch.CommandHandler()

if command_mode:
    user_credentials = (
        input("username: "),
        input("password: ") if commons.settings["echoOn"] else getpass("password"),
    )

    if ch.login(*user_credentials) == 0:
        clear_screen()
        print("USER not found")
        signup = "y" == input("Do you want to sign up(y/n)")
        if signup:
            ch.signup(*user_credentials)
        exit()

    cmndno = 0
    # command mode loop[for find]
    try:
        while 1:
            # cmndhndlr.get_query()
            query = None
            query = input(f"[{cmndno}]> ")

            if query == "":
                continue

            elif query == "exit":
                ch.quit()
                exit()

            elif query.startswith("*"):
                interpreterCommands(query)

            elif query.startswith("$"):
                sys(query[1:])
                commons.logging.info(f"executed on shell: {query[1:]}")

            elif query:
                ch.query = query.split()
                code = ch.process_query()

                if code == 1:
                    print(ch.output)
                    ch.output = None
                elif code == 0:
                    print(commons.ERROR_MSG)
                elif code == -1:
                    print("wrong syntax")

                cmndno += 1
                ch.query = None

    except Exception:
        commons.traceback(commons.exc_info())
        print(commons.ERROR_MSG)


# command mode menu
elif command_mode is False:
    echo_on = commons.settings["echoOn"]

    options = ["Log in", "Sign up"]
    menu = stm.TerminalMenu([f"[{i}] {options[i]}" for i in range(len(options))])
    option_selected = menu.show()

    if option_selected == 0:
        login_code = ch.login(
            input("username: "),
            (
                input("password: ")
                if commons.settings["echoOn"]
                else getpass("password: ")
            ),
        )

        if login_code == 0:
            print("LOGIN FAILED!")

    elif option_selected == 1:
        signup_code = ch.signup(
            input("username: "),
            (
                getpass("password")
                if commons.settings["echoOn"] is False
                else input(("password: "))
            ),
        )

    # menu loop[for find]
    menu_options = ch.commands + ["exit"]
    while ch.logged_in:
        clear_screen()
        menu = stm.TerminalMenu(
            [f"[{i}] {menu_options[i]}" for i in range(len(menu_options))]
        )
        user_selection = menu.show()
        selected_option = menu_options[user_selection]

        # 0:set
        # 1:get
        # 2:delete
        # 3:update

        # menu for SET
        if selected_option == "exit":
            clear_screen()
            print("Good Bye")
            ch.quit()

        if user_selection == 0:
            pid = input("<<<< Password Identifier >>>>\n> ")
            password = (
                input("<<<< Password >>>>\n> ")
                if echo_on
                else getpass("<<<< Password >>>>\n> ")
            )

            ch.query = (selected_option, pid, password)
            del password
            ch.process_query()
            ch.query = None
            clear_screen()

        # menu for GET
        elif user_selection == 1:
            print("<< GET >>")
            pid = input("<<<< Password Identifier >>>>\n> ")
            ch.query = (selected_option, pid)
            ch.process_query()

            if ch.output:
                # copy/print menu
                options = ["copy", "print"]
                menu = stm.TerminalMenu(
                    [f"[{i}] {str(options[i])}" for i in range(len(options))]
                )
                clear_screen()

                print("<< GET >>")
                selection = menu.show()

                if selection == 1:
                    print(ch.output)

                    if commons.settings["letPasswordStill"]:
                        print("won't vanish until u press enter")
                        input()
                    else:
                        time = commons.settings["vanishTime"]
                        print(f"will vanish in {time}")
                        commons.sleep(time)

                elif selection == 0:
                    try:
                        from clipboard import copy

                        copy(ch.output)
                        print("copied to your clipboard")

                    except Exception as e:
                        commons.logger.error(e)
                        commons.traceback(commons.exc_info())
                        print(commons.ERROR_MSG)
            else:
                print("Nothing")
                input()

            ch.output = None
            clear_screen()

        # menu for DELETE
        elif user_selection == 2:
            print("<< DELETE >>")
            pid = input("<<<< Password Identifier >>>>\n> ")
            ch.query = (selected_option, pid)
            ch.process_query()
            clear_screen()

        # menu for UPDATE
        elif user_selection == 3:
            print("<< UPDATE >>")
            pid = input("<<<< Password Identifier >>>>\n> ")
            newPassword = input("<<<< New PASSWORD >>>>\n")
            ch.query = (selected_option, pid, newPassword)
            ch.process_query()
            clear_screen()
