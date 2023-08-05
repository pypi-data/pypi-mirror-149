from colorama import Fore, Back, Style

log_level_colors = {
    "error": Fore.RED,
    "info": Fore.YELLOW,
    "warning": Fore.LIGHTRED_EX,
    "debug": Fore.GREEN
}


class PrettifyPrint:
    __instance = None

    def __init__(self, custom_message=None):
        if PrettifyPrint.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            PrettifyPrint.__instance = self
            if custom_message:
                print(Fore.MAGENTA + custom_message)
            print(Fore.CYAN + '*' * 120)

    def __del__(self):
        print(Fore.CYAN + '*' * 120)

    def pretty_print(self, message, level='debug'):
        """
        This function will be used to display messages with colors depending on level
        Args:
            message(str): message that need to be displayed.
            level(str): message level depeding on which we can display images
        """
        message_color = log_level_colors.get(level.lower(), Fore.LIGHTBLACK_EX)
        print(message_color + message)


pprint = PrettifyPrint("Welcome to AWS Infra Automation...")
