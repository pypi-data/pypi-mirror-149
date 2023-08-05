import json

import requests
from bs4 import BeautifulSoup
from colorama import Fore

commands = {}
actions = {}
no_command_exists_msg = "[+] No such command."
default_header = ["", 0]


def log(msg, style=None, header=None):
    global default_header
    if header:
        if isinstance(header, list):
            default_header = header
        else:
            log("[-] Header value should be a list.", style="error")
    if style == 'success':
        print(default_header[0] * default_header[1] + Fore.GREEN + str(msg) + Fore.RESET)
    elif style == 'error':
        print(default_header[0] * default_header[1] + Fore.RED + str(msg) + Fore.RESET)
    else:
        print(default_header[0] * default_header[1] + str(msg))


def config(no_command_found_msg=no_command_exists_msg):
    global no_command_exists_msg
    no_command_exists_msg = no_command_found_msg


def get_dataset(name=None):
    return load_json(name)


def get_arg_count(command):
    try:
        arg_count = get_dataset()[command][0]
        if arg_count is not None:
            return arg_count
    except KeyError:
        return False


def get_usage(command):
    try:
        usage = get_dataset()[command][1]
        if usage is not None:
            return usage
    except KeyError:
        return False


def get_help_info(command):
    try:
        cmdinfo = get_dataset()[command][2]
        if cmdinfo is not None:
            return cmdinfo
    except KeyError:
        return False


def get_command_info(command):
    return get_arg_count(command), get_help_info(command)


def save_json(data, filename=None):
    if filename is None:
        filename = f"../commands.json"
    with open(filename, 'w') as file:
        file.write(json.dumps(data))


def load_json(filename=None):
    if filename is None:
        filename = "../commands.json"
    with open(filename, 'r') as file:
        return json.load(file)


def add_command(command, arguments=None, usage=None, cmdinfo=None, action=None):
    if usage is None:
        usage = ""
    if cmdinfo is None:
        cmdinfo = ""
    commands[command] = [arguments, usage, cmdinfo]
    save_json(commands)
    actions[command] = action


# Returns all commands
def load_commands(name=None):
    return load_json(name)


def cmd_result(command, input_):
    arg_amnt = get_arg_count(command)
    if not input_:
        return False, ""
    if arg_amnt is not False:
        input_ = input_.split()
        cmd = input_[0]
        del input_[0]
        arguments = input_
        if arg_amnt is not None:
            if arg_amnt > len(input_):
                return False, "[-] Missing args."
            elif arg_amnt < len(input_):
                return False, "[-] Too many args passed."
            else:
                try:
                    actions[cmd](arguments)
                except Exception as e:
                    return False, f"[-] Error running action: {e}"
                return True, "OK"
        try:
            actions[cmd]()
        except Exception as e:
            return False, f"[-] Error running action: {e}"
        return True, "OK"
    else:
        return False, no_command_exists_msg


if __name__ == '__main__':
    r = requests.get('https://raw.githubusercontent.com/Izaan17/TermuxCreate/main/README.md')
    text = BeautifulSoup(r.content, 'lxml')
    print(text.text.replace("#", "/"))
    # print("""---USAGE---
    # / Import termuxcreate
    # import TermuxCreate as tc
    #
    #
    # / Action to run
    # def print_input(msg):
    #     print(msg)
    #
    #
    # / You add the commands you want to use
    # tc.add_command(command='testcommand', arguments=1, cmdinfo="[+] prints whatever u type.", action=print_input)
    #     | command /  We set a command name whenever we type it this name will be used to access the function.
    #     | arguments / We input a number of required arguments for a function.
    #     | action / Function to call when success of this command.
    #
    # / We create a function to get input
    # def terminal():
    #     while 1:
    #         input_ = input("shell> ")
    #         command = input_.split()
    #         if command:
    #             cmd_result, msg = tc.cmd_result(command=command[0], input_=input_)  # we use 0 to get the command name
    #             if not cmd_result:
    #                 print(msg)
    #     |  def terminal() / we can create a loop to get input forever to feed the terminal input.
    #     |  command = input_.split() / this is the full command along with arguments passed, we need to supply this to tc.cmd_result()
    #     |  cmd_result, msg = tc.cmd_result(command=command[0], input_=input_)/ tc.cmd_result() returns two values which are either 'True' or 'False' and if the command passed the arg check and the error msg if it did not pass.
    #     |  if command: / We use this in order to prevent no input from passing through.
    #     |  if not cmd_result: print(msg) / this means if the command result turns out to be false print the error message.
    # ----------------IMPORTANT--------------------
    # | WHEN EXECUTING AN ACTION THE ARGUMENTS ARE IN A LIST FORMAT. WE CAN EITHER FORMAT IT TO STRING IN THE FUNCTION OR MAKE TERMUXCREATE DO IT.
    # """)
