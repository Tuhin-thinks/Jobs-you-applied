from colorama import Fore, Back, Style
import string


class Ask:
    filter_inp = set([''] + list(string.punctuation))

    @staticmethod
    def str(prompt):
        inp = input(prompt)
        if inp in Ask.filter_inp:
            Display.str("Input not valid", 'f')
            return Ask.str(prompt)
        else:
            return inp

    def int(self):
        pass

    def float(self):
        pass


class Display:
    @staticmethod
    def str(message, msg_type='success'):
        if msg_type == 'success':
            print(f"{Fore.LIGHTGREEN_EX}{message}{Fore.RESET}")
        else:  # failure
            print(f"{Fore.LIGHTRED_EX}{message}{Fore.RESET}")
