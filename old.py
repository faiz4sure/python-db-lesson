from colorama import init, Fore, Back, Style
import json
from datetime import datetime
import os

init()
class TeacherManagementSystem:
    def __init__(self):
        self.students = {}
        self.attendance = {}
        self.grades = {}
        self.load_data()

    def load_data(self):
        if os.path.exists('teacher_data.json'):
            try:
                with open('teacher_data.json', 'r') as f:
                    data = json.load(f)
                    self.students = data.get('students', {})
                    self.attendance = data.get('attendance', {})
                    self.grades = data.get('grades', {})
            except:
                print(f"{Fore.RED}Error loading data. Starting fresh.{Style.RESET_ALL}")

    def save_data(self):
        data = {
            'students': self.students,
            'attendance': self.attendance,
            'grades': self.grades
        }
        with open('teacher_data.json', 'w') as f:
            json.dump(data, f)

    def get_user_details(self):
        print(f"\n{Back.BLUE}{Fore.WHITE}=== Teacher Information System ==={Style.RESET_ALL}\n")
        
        
        name = input(f"{Fore.CYAN}Enter your name: {Style.RESET_ALL}")
        subject = input(f"{Fore.CYAN}Enter your subject: {Style.RESET_ALL}")
        email = input(f"{Fore.CYAN}Enter your email: {Style.RESET_ALL}")
        department = input(f"{Fore.CYAN}Enter your department: {Style.RESET_ALL}")
        
        
        print(f"\n{Fore.GREEN}=== Please confirm your details ==={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Name: {name}")
        print(f"Subject: {subject}")
        print(f"Email: {email}")
        print(f"Department: {department}{Style.RESET_ALL}")
        
        confirm = input(f"\n{Fore.CYAN}Is this information correct? (yes/no): {Style.RESET_ALL}").lower()
        
        if confirm == 'yes':
            self.display_teacher_info(name, subject, email, department)
            return True
        else:
            print(f"\n{Fore.RED}Let's try again!{Style.RESET_ALL}")
            return self.get_user_details()

    def display_teacher_info(self, name, subject, email, department):
        print(f"\n{Back.GREEN}{Fore.WHITE}{'='*50}{Style.RESET_ALL}")
        print(f"{Back.GREEN}{Fore.WHITE}           TEACHER INFORMATION           {Style.RESET_ALL}")
        print(f"{Back.GREEN}{Fore.WHITE}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}📋 Name       : {name}")
        print(f"📚 Subject    : {subject}")
        print(f"📧 Email      : {email}")
        print(f"🏫 Department : {department}")
        print(f"{Fore.GREEN}{'='*50}{Style.RESET_ALL}")

    def add_student(self):
        print(f"\n{Fore.CYAN}=== Add New Student ==={Style.RESET_ALL}")
        student_id = input(f"{Fore.YELLOW}Enter student ID: {Style.RESET_ALL}")
        name = input(f"{Fore.YELLOW}Enter student name: {Style.RESET_ALL}")
        grade = input(f"{Fore.YELLOW}Enter class/grade: {Style.RESET_ALL}")
        
        self.students[student_id] = {
            'name': name,
            'grade': grade,
            'added_date': datetime.now().strftime("%Y-%m-%d")
        }
        self.save_data()
        print(f"{Fore.GREEN}Student added successfully!{Style.RESET_ALL}")

    def mark_attendance(self):
        if not self.students:
            print(f"{Fore.RED}No students registered yet!{Style.RESET_ALL}")
            return

        print(f"\n{Fore.CYAN}=== Mark Attendance ==={Style.RESET_ALL}")
        date = datetime.now().strftime("%Y-%m-%d")
        print(f"{Fore.YELLOW}Date: {date}{Style.RESET_ALL}")

        if date not in self.attendance:
            self.attendance[date] = {}

        for student_id, info in self.students.items():
            while True:
                status = input(f"{Fore.YELLOW}Is {info['name']} (ID: {student_id}) present? (p/a): {Style.RESET_ALL}").lower()
                if status in ['p', 'a']:
                    self.attendance[date][student_id] = 'Present' if status == 'p' else 'Absent'
                    break
                print(f"{Fore.RED}Invalid input! Please enter 'p' for present or 'a' for absent.{Style.RESET_ALL}")
        
        self.save_data()
        print(f"{Fore.GREEN}Attendance marked successfully!{Style.RESET_ALL}")

    def add_grades(self):
        if not self.students:
            print(f"{Fore.RED}No students registered yet!{Style.RESET_ALL}")
            return

        print(f"\n{Fore.CYAN}=== Add Grades ==={Style.RESET_ALL}")
        student_id = input(f"{Fore.YELLOW}Enter student ID: {Style.RESET_ALL}")
        
        if student_id not in self.students:
            print(f"{Fore.RED}Student not found!{Style.RESET_ALL}")
            return

        subject = input(f"{Fore.YELLOW}Enter subject: {Style.RESET_ALL}")
        score = input(f"{Fore.YELLOW}Enter score (0-100): {Style.RESET_ALL}")
        
        if student_id not in self.grades:
            self.grades[student_id] = {}
        
        self.grades[student_id][subject] = score
        self.save_data()
        print(f"{Fore.GREEN}Grade added successfully!{Style.RESET_ALL}")

    def view_student_details(self):
        if not self.students:
            print(f"{Fore.RED}No students registered yet!{Style.RESET_ALL}")
            return

        print(f"\n{Fore.CYAN}=== View Student Details ==={Style.RESET_ALL}")
        student_id = input(f"{Fore.YELLOW}Enter student ID: {Style.RESET_ALL}")
        
        if student_id not in self.students:
            print(f"{Fore.RED}Student not found!{Style.RESET_ALL}")
            return

        student = self.students[student_id]
        print(f"\n{Back.BLUE}{Fore.WHITE}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Student Information:")
        print(f"Name: {student['name']}")
        print(f"Grade: {student['grade']}")
        print(f"Added Date: {student['added_date']}")
        
        if student_id in self.grades:
            print(f"\n{Fore.CYAN}Grades:{Style.RESET_ALL}")
            for subject, score in self.grades[student_id].items():
                print(f"{subject}: {score}")
        
        print(f"\n{Fore.YELLOW}Recent Attendance:{Style.RESET_ALL}")
        for date, attendance in self.attendance.items():
            if student_id in attendance:
                print(f"{date}: {attendance[student_id]}")

    def main_menu(self):
        while True:
            print(f"\n{Back.BLUE}{Fore.WHITE}=== Teacher Management System ==={Style.RESET_ALL}")
            print(f"{Fore.CYAN}1. Add Student")
            print("2. Mark Attendance")
            print("3. Add Grades")
            print("4. View Student Details")
            print(f"5. Exit{Style.RESET_ALL}")
            
            choice = input(f"\n{Fore.YELLOW}Enter your choice (1-5): {Style.RESET_ALL}")
            
            if choice == '1':
                self.add_student()
            elif choice == '2':
                self.mark_attendance()
            elif choice == '3':
                self.add_grades()
            elif choice == '4':
                self.view_student_details()
            elif choice == '5':
                print(f"{Fore.GREEN}Thank you for using Teacher Management System!{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Invalid choice! Please try again.{Style.RESET_ALL}")

if __name__ == "__main__":
    system = TeacherManagementSystem()
    if system.get_user_details():
        system.main_menu()