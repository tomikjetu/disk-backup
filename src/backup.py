from colorama import Fore, Style, init
init(autoreset=True)
print(f"{Fore.GREEN}{'='*5} SETTINGS {'='*5}{Style.RESET_ALL}")
import settings
print("\n")
print(f"{Fore.GREEN}{'='*5} PROJECTS STATUS {'='*5}{Style.RESET_ALL}")
import project_status
print("\n")
print(f"{Fore.GREEN}{'='*5} BACKING UP {'='*5}{Style.RESET_ALL}")
import update