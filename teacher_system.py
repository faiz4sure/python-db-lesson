from colorama import init, Fore, Back, Style
import bcrypt
from datetime import datetime
from models import Session, Teacher, Student, Attendance, Grade

init()

class TeacherManagementSystem:
    def __init__(self):
        self.session = Session()
        self.current_teacher = None

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    def verify_password(self, password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed)

    def login(self):
        print(f"\n{Back.BLUE}{Fore.WHITE}=== Teacher Login ==={Style.RESET_ALL}\n")
        email = input(f"{Fore.CYAN}Enter your email: {Style.RESET_ALL}")
        password = input(f"{Fore.CYAN}Enter your password: {Style.RESET_ALL}")

        teacher = self.session.query(Teacher).filter_by(email=email).first()
        if teacher and teacher.password_hash and self.verify_password(password, teacher.password_hash.encode('utf-8')):
            self.current_teacher = teacher
            return True
        else:
            print(f"{Fore.RED}Invalid credentials!{Style.RESET_ALL}")
            return False

    def register(self):
        print(f"\n{Back.BLUE}{Fore.WHITE}=== Teacher Registration ==={Style.RESET_ALL}\n")
        
        name = input(f"{Fore.CYAN}Enter your name: {Style.RESET_ALL}")
        email = input(f"{Fore.CYAN}Enter your email: {Style.RESET_ALL}")
        department = input(f"{Fore.CYAN}Enter your department: {Style.RESET_ALL}")
        subject = input(f"{Fore.CYAN}Enter your subject: {Style.RESET_ALL}")
        password = input(f"{Fore.CYAN}Enter your password: {Style.RESET_ALL}")
        
        # Check if email already exists
        if self.session.query(Teacher).filter_by(email=email).first():
            print(f"{Fore.RED}Email already registered!{Style.RESET_ALL}")
            return False

        teacher = Teacher(
            name=name,
            email=email,
            department=department,
            subject=subject,
            password_hash=self.hash_password(password).decode('utf-8')
        )
        
        self.session.add(teacher)
        self.session.commit()
        print(f"{Fore.GREEN}Registration successful!{Style.RESET_ALL}")
        return True

    def display_teacher_info(self):
        if not self.current_teacher:
            return
        
        print(f"\n{Back.GREEN}{Fore.WHITE}{'='*50}{Style.RESET_ALL}")
        print(f"{Back.GREEN}{Fore.WHITE}           TEACHER INFORMATION           {Style.RESET_ALL}")
        print(f"{Back.GREEN}{Fore.WHITE}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}📋 Name       : {self.current_teacher.name}")
        print(f"📚 Subject    : {self.current_teacher.subject}")
        print(f"📧 Email      : {self.current_teacher.email}")
        print(f"🏫 Department : {self.current_teacher.department}")
        print(f"{Fore.GREEN}{'='*50}{Style.RESET_ALL}")

    def add_student(self):
        if not self.current_teacher:
            return
            
        print(f"\n{Fore.CYAN}=== Add New Student ==={Style.RESET_ALL}")
        student_id = input(f"{Fore.YELLOW}Enter student ID: {Style.RESET_ALL}")
        name = input(f"{Fore.YELLOW}Enter student name: {Style.RESET_ALL}")
        grade = input(f"{Fore.YELLOW}Enter class/grade: {Style.RESET_ALL}")
        
        # Check if student ID already exists
        if self.session.query(Student).filter_by(student_id=student_id).first():
            print(f"{Fore.RED}Student ID already exists!{Style.RESET_ALL}")
            return

        student = Student(
            student_id=student_id,
            name=name,
            grade=grade,
            teacher_id=self.current_teacher.id
        )
        
        self.session.add(student)
        self.session.commit()
        print(f"{Fore.GREEN}Student added successfully!{Style.RESET_ALL}")

    def mark_attendance(self):
        if not self.current_teacher:
            return

        print(f"\n{Fore.CYAN}=== Mark Attendance ==={Style.RESET_ALL}")
        date_str = datetime.now().strftime("%Y-%m-%d")
        print(f"{Fore.YELLOW}Date: {date_str}{Style.RESET_ALL}")

        students = self.session.query(Student).filter_by(teacher_id=self.current_teacher.id).all()
        if not students:
            print(f"{Fore.RED}No students registered yet!{Style.RESET_ALL}")
            return

        for student in students:
            while True:
                status = input(f"{Fore.YELLOW}Is {student.name} (ID: {student.student_id}) present? (p/a): {Style.RESET_ALL}").lower()
                if status in ['p', 'a']:
                    attendance = Attendance(
                        student_id=student.id,
                        date=datetime.now().date(),
                        status=True if status == 'p' else False
                    )
                    self.session.add(attendance)
                    break
                print(f"{Fore.RED}Invalid input! Please enter 'p' for present or 'a' for absent.{Style.RESET_ALL}")
        
        self.session.commit()
        print(f"{Fore.GREEN}Attendance marked successfully!{Style.RESET_ALL}")

    def add_grades(self):
        if not self.current_teacher:
            return

        print(f"\n{Fore.CYAN}=== Add Grades ==={Style.RESET_ALL}")
        student_id = input(f"{Fore.YELLOW}Enter student ID: {Style.RESET_ALL}")
        
        student = self.session.query(Student).filter_by(
            student_id=student_id, 
            teacher_id=self.current_teacher.id
        ).first()
        
        if not student:
            print(f"{Fore.RED}Student not found!{Style.RESET_ALL}")
            return

        subject = input(f"{Fore.YELLOW}Enter subject: {Style.RESET_ALL}")
        while True:
            try:
                score = float(input(f"{Fore.YELLOW}Enter score (0-100): {Style.RESET_ALL}"))
                if 0 <= score <= 100:
                    break
                print(f"{Fore.RED}Score must be between 0 and 100{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number{Style.RESET_ALL}")

        grade = Grade(
            student_id=student.id,
            subject=subject,
            score=score
        )
        
        self.session.add(grade)
        self.session.commit()
        print(f"{Fore.GREEN}Grade added successfully!{Style.RESET_ALL}")

    def view_student_details(self):
        if not self.current_teacher:
            return

        print(f"\n{Fore.CYAN}=== View Student Details ==={Style.RESET_ALL}")
        student_id = input(f"{Fore.YELLOW}Enter student ID: {Style.RESET_ALL}")
        
        student = self.session.query(Student).filter_by(
            student_id=student_id, 
            teacher_id=self.current_teacher.id
        ).first()
        
        if not student:
            print(f"{Fore.RED}Student not found!{Style.RESET_ALL}")
            return

        print(f"\n{Back.BLUE}{Fore.WHITE}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Student Information:")
        print(f"Name: {student.name}")
        print(f"Grade: {student.grade}")
        print(f"Added Date: {student.added_date}")
        
        # Show grades
        grades = self.session.query(Grade).filter_by(student_id=student.id).all()
        if grades:
            print(f"\n{Fore.CYAN}Grades:{Style.RESET_ALL}")
            for grade in grades:
                print(f"{grade.subject}: {grade.score}")
        
        # Show recent attendance
        print(f"\n{Fore.YELLOW}Recent Attendance:{Style.RESET_ALL}")
        attendance_records = self.session.query(Attendance)\
            .filter_by(student_id=student.id)\
            .order_by(Attendance.date.desc())\
            .limit(10)\
            .all()
            
        for record in attendance_records:
            status = "Present" if record.status else "Absent"
            print(f"{record.date}: {status}")

    def main_menu(self):
        while True:
            print(f"\n{Back.BLUE}{Fore.WHITE}=== Teacher Management System ==={Style.RESET_ALL}")
            print(f"{Fore.CYAN}1. Add Student")
            print("2. Mark Attendance")
            print("3. Add Grades")
            print("4. View Student Details")
            print("5. View My Profile")
            print(f"6. Exit{Style.RESET_ALL}")
            
            choice = input(f"\n{Fore.YELLOW}Enter your choice (1-6): {Style.RESET_ALL}")
            
            if choice == '1':
                self.add_student()
            elif choice == '2':
                self.mark_attendance()
            elif choice == '3':
                self.add_grades()
            elif choice == '4':
                self.view_student_details()
            elif choice == '5':
                self.display_teacher_info()
            elif choice == '6':
                print(f"{Fore.GREEN}Thank you for using Teacher Management System!{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Invalid choice! Please try again.{Style.RESET_ALL}")

if __name__ == "__main__":
    system = TeacherManagementSystem()
    print(f"\n{Back.BLUE}{Fore.WHITE}Welcome to Teacher Management System{Style.RESET_ALL}")
    while True:
        print(f"\n{Fore.CYAN}1. Login")
        print(f"2. Register")
        print(f"3. Exit{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.YELLOW}Enter your choice (1-3): {Style.RESET_ALL}")
        
        if choice == '1':
            if system.login():
                system.display_teacher_info()
                system.main_menu()
        elif choice == '2':
            system.register()
        elif choice == '3':
            print(f"{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Invalid choice! Please try again.{Style.RESET_ALL}")