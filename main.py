from colorama import init, Fore, Back, Style
from teacher_system import TeacherManagementSystem
from hospital_system import HospitalManagementSystem
import signal
import sys

init()

def handle_interrupt(signum, frame):
    print(f"\n\n{Fore.GREEN}Thanks for using the Management System! Have a great day!{Style.RESET_ALL}")
    sys.exit(0)

def main_menu():
    signal.signal(signal.SIGINT, handle_interrupt)
    
    try:
        while True:
            print(f"\n{Back.BLUE}{Fore.WHITE}=== Management System ===={Style.RESET_ALL}")
            print(f"\n{Fore.CYAN}1. Teacher Management System")
            print(f"2. Hospital Management System")
            print(f"3. Exit{Style.RESET_ALL}")
            
            choice = input(f"\n{Fore.YELLOW}Enter your choice (1-3): {Style.RESET_ALL}")
            
            if choice == '1':
                system = TeacherManagementSystem()
                print(f"\n{Back.BLUE}{Fore.WHITE}Welcome to Teacher Management System{Style.RESET_ALL}")
                while True:
                    print(f"\n{Fore.CYAN}1. Login")
                    print(f"2. Register")
                    print(f"3. Back to Main Menu{Style.RESET_ALL}")
                    
                    auth_choice = input(f"\n{Fore.YELLOW}Enter your choice (1-3): {Style.RESET_ALL}")
                    
                    if auth_choice == '1':
                        if system.login():
                            system.display_teacher_info()
                            system.main_menu()
                    elif auth_choice == '2':
                        system.register()
                    elif auth_choice == '3':
                        break
                    else:
                        print(f"{Fore.RED}Invalid choice! Please try again.{Style.RESET_ALL}")
                        
            elif choice == '2':
                system = HospitalManagementSystem()
                print(f"\n{Back.BLUE}{Fore.WHITE}Welcome to Hospital Management System{Style.RESET_ALL}")
                while True:
                    print(f"\n{Fore.CYAN}1. Login")
                    print(f"2. Register")
                    print(f"3. Back to Main Menu{Style.RESET_ALL}")
                    
                    auth_choice = input(f"\n{Fore.YELLOW}Enter your choice (1-3): {Style.RESET_ALL}")
                    
                    if auth_choice == '1':
                        if system.login():
                            system.display_doctor_info()
                            system.main_menu()
                    elif auth_choice == '2':
                        system.register()
                    elif auth_choice == '3':
                        break
                    else:
                        print(f"{Fore.RED}Invalid choice! Please try again.{Style.RESET_ALL}")
                        
            elif choice == '3':
                print(f"{Fore.GREEN}Thank you for using the Management System! Goodbye!{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Invalid choice! Please try again.{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main_menu()