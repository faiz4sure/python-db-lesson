from colorama import init, Fore, Back, Style
import bcrypt
from datetime import datetime, timedelta
from models import Session, Doctor, Patient, Appointment, MedicalRecord

init()

class HospitalManagementSystem:
    def __init__(self):
        self.session = Session()
        self.current_doctor = None

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    def verify_password(self, password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed)

    def login(self):
        print(f"\n{Back.BLUE}{Fore.WHITE}=== Doctor Login ==={Style.RESET_ALL}\n")
        email = input(f"{Fore.CYAN}Enter your email: {Style.RESET_ALL}")
        password = input(f"{Fore.CYAN}Enter your password: {Style.RESET_ALL}")

        doctor = self.session.query(Doctor).filter_by(email=email).first()
        if doctor and doctor.password_hash and self.verify_password(password, doctor.password_hash.encode('utf-8')):
            self.current_doctor = doctor
            return True
        else:
            print(f"{Fore.RED}Invalid credentials!{Style.RESET_ALL}")
            return False

    def register(self):
        print(f"\n{Back.BLUE}{Fore.WHITE}=== Doctor Registration ==={Style.RESET_ALL}\n")
        
        name = input(f"{Fore.CYAN}Enter your name: {Style.RESET_ALL}")
        email = input(f"{Fore.CYAN}Enter your email: {Style.RESET_ALL}")
        specialization = input(f"{Fore.CYAN}Enter your specialization: {Style.RESET_ALL}")
        phone = input(f"{Fore.CYAN}Enter your phone number: {Style.RESET_ALL}")
        password = input(f"{Fore.CYAN}Enter your password: {Style.RESET_ALL}")
        
        if self.session.query(Doctor).filter_by(email=email).first():
            print(f"{Fore.RED}Email already registered!{Style.RESET_ALL}")
            return False

        doctor = Doctor(
            name=name,
            email=email,
            specialization=specialization,
            phone=phone,
            password_hash=self.hash_password(password).decode('utf-8')
        )
        
        self.session.add(doctor)
        self.session.commit()
        print(f"{Fore.GREEN}Registration successful!{Style.RESET_ALL}")
        return True

    def display_doctor_info(self):
        if not self.current_doctor:
            return
        
        print(f"\n{Back.GREEN}{Fore.WHITE}{'='*50}{Style.RESET_ALL}")
        print(f"{Back.GREEN}{Fore.WHITE}           DOCTOR INFORMATION           {Style.RESET_ALL}")
        print(f"{Back.GREEN}{Fore.WHITE}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}👨‍⚕️ Name           : {self.current_doctor.name}")
        print(f"🏥 Specialization : {self.current_doctor.specialization}")
        print(f"📧 Email          : {self.current_doctor.email}")
        print(f"📞 Phone          : {self.current_doctor.phone}")
        print(f"{Fore.GREEN}{'='*50}{Style.RESET_ALL}")

    def add_patient(self):
        if not self.current_doctor:
            return
            
        print(f"\n{Fore.CYAN}=== Add New Patient ==={Style.RESET_ALL}")
        patient_id = input(f"{Fore.YELLOW}Enter patient ID: {Style.RESET_ALL}")
        name = input(f"{Fore.YELLOW}Enter patient name: {Style.RESET_ALL}")
        age = input(f"{Fore.YELLOW}Enter patient age: {Style.RESET_ALL}")
        gender = input(f"{Fore.YELLOW}Enter patient gender (M/F): {Style.RESET_ALL}").upper()
        blood_group = input(f"{Fore.YELLOW}Enter blood group: {Style.RESET_ALL}")
        phone = input(f"{Fore.YELLOW}Enter phone number: {Style.RESET_ALL}")
        address = input(f"{Fore.YELLOW}Enter address: {Style.RESET_ALL}")
        
        if self.session.query(Patient).filter_by(patient_id=patient_id).first():
            print(f"{Fore.RED}Patient ID already exists!{Style.RESET_ALL}")
            return

        patient = Patient(
            patient_id=patient_id,
            name=name,
            age=int(age),
            gender=gender,
            blood_group=blood_group,
            phone=phone,
            address=address,
            doctor_id=self.current_doctor.id
        )
        
        self.session.add(patient)
        self.session.commit()
        print(f"{Fore.GREEN}Patient added successfully!{Style.RESET_ALL}")

    def schedule_appointment(self):
        if not self.current_doctor:
            return

        print(f"\n{Fore.CYAN}=== Schedule Appointment ==={Style.RESET_ALL}")
        patient_id = input(f"{Fore.YELLOW}Enter patient ID: {Style.RESET_ALL}")
        
        patient = self.session.query(Patient).filter_by(
            patient_id=patient_id, 
            doctor_id=self.current_doctor.id
        ).first()
        
        if not patient:
            print(f"{Fore.RED}Patient not found!{Style.RESET_ALL}")
            return

        # Show available time slots for next 7 days
        print(f"\n{Fore.CYAN}Available time slots:{Style.RESET_ALL}")
        time_slots = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]
        dates = [(datetime.now() + timedelta(days=i)).date() for i in range(7)]
        
        for i, date in enumerate(dates, 1):
            print(f"\n{Fore.YELLOW}Date {i}: {date}{Style.RESET_ALL}")
            available_slots = []
            for slot in time_slots:
                # Check if slot is available
                existing = self.session.query(Appointment).filter_by(
                    doctor_id=self.current_doctor.id,
                    date=date,
                    time_slot=slot
                ).first()
                if not existing:
                    available_slots.append(slot)
            
            for j, slot in enumerate(available_slots, 1):
                print(f"{j}. {slot}")
            
        date_choice = int(input(f"\n{Fore.YELLOW}Select date (1-7): {Style.RESET_ALL}"))
        slot_choice = input(f"{Fore.YELLOW}Enter preferred time slot (HH:MM): {Style.RESET_ALL}")
        notes = input(f"{Fore.YELLOW}Any notes for the appointment: {Style.RESET_ALL}")

        appointment = Appointment(
            patient_id=patient.id,
            doctor_id=self.current_doctor.id,
            date=dates[date_choice-1],
            time_slot=slot_choice,
            notes=notes
        )
        
        self.session.add(appointment)
        self.session.commit()
        print(f"{Fore.GREEN}Appointment scheduled successfully!{Style.RESET_ALL}")

    def add_medical_record(self):
        if not self.current_doctor:
            return

        print(f"\n{Fore.CYAN}=== Add Medical Record ==={Style.RESET_ALL}")
        patient_id = input(f"{Fore.YELLOW}Enter patient ID: {Style.RESET_ALL}")
        
        patient = self.session.query(Patient).filter_by(
            patient_id=patient_id, 
            doctor_id=self.current_doctor.id
        ).first()
        
        if not patient:
            print(f"{Fore.RED}Patient not found!{Style.RESET_ALL}")
            return

        diagnosis = input(f"{Fore.YELLOW}Enter diagnosis: {Style.RESET_ALL}")
        prescription = input(f"{Fore.YELLOW}Enter prescription: {Style.RESET_ALL}")
        notes = input(f"{Fore.YELLOW}Additional notes: {Style.RESET_ALL}")

        record = MedicalRecord(
            patient_id=patient.id,
            diagnosis=diagnosis,
            prescription=prescription,
            notes=notes
        )
        
        self.session.add(record)
        self.session.commit()
        print(f"{Fore.GREEN}Medical record added successfully!{Style.RESET_ALL}")

    def view_patient_history(self):
        if not self.current_doctor:
            return

        print(f"\n{Fore.CYAN}=== View Patient History ==={Style.RESET_ALL}")
        patient_id = input(f"{Fore.YELLOW}Enter patient ID: {Style.RESET_ALL}")
        
        patient = self.session.query(Patient).filter_by(
            patient_id=patient_id, 
            doctor_id=self.current_doctor.id
        ).first()
        
        if not patient:
            print(f"{Fore.RED}Patient not found!{Style.RESET_ALL}")
            return

        print(f"\n{Back.BLUE}{Fore.WHITE}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Patient Information:")
        print(f"Name: {patient.name}")
        print(f"Age: {patient.age}")
        print(f"Gender: {patient.gender}")
        print(f"Blood Group: {patient.blood_group}")
        print(f"Contact: {patient.phone}")
        
        # Show medical records
        records = self.session.query(MedicalRecord)\
            .filter_by(patient_id=patient.id)\
            .order_by(MedicalRecord.date.desc())\
            .all()
            
        if records:
            print(f"\n{Fore.CYAN}Medical History:{Style.RESET_ALL}")
            for record in records:
                print(f"\nDate: {record.date}")
                print(f"Diagnosis: {record.diagnosis}")
                print(f"Prescription: {record.prescription}")
                if record.notes:
                    print(f"Notes: {record.notes}")
        
        # Show appointments
        appointments = self.session.query(Appointment)\
            .filter_by(patient_id=patient.id)\
            .order_by(Appointment.date.desc())\
            .all()
            
        if appointments:
            print(f"\n{Fore.YELLOW}Appointments:{Style.RESET_ALL}")
            for appt in appointments:
                print(f"\nDate: {appt.date}")
                print(f"Time: {appt.time_slot}")
                print(f"Status: {appt.status}")
                if appt.notes:
                    print(f"Notes: {appt.notes}")

    def view_appointments(self):
        if not self.current_doctor:
            return

        print(f"\n{Fore.CYAN}=== Today's Appointments ==={Style.RESET_ALL}")
        today = datetime.now().date()
        
        appointments = self.session.query(Appointment)\
            .filter_by(doctor_id=self.current_doctor.id, date=today)\
            .order_by(Appointment.time_slot)\
            .all()
            
        if not appointments:
            print(f"{Fore.YELLOW}No appointments scheduled for today.{Style.RESET_ALL}")
            return
            
        for appt in appointments:
            patient = self.session.query(Patient).get(appt.patient_id)
            print(f"\n{Fore.GREEN}Time: {appt.time_slot}")
            print(f"Patient: {patient.name} (ID: {patient.patient_id})")
            print(f"Status: {appt.status}")
            if appt.notes:
                print(f"Notes: {appt.notes}")

    def main_menu(self):
        while True:
            print(f"\n{Back.BLUE}{Fore.WHITE}=== Hospital Management System ==={Style.RESET_ALL}")
            print(f"{Fore.CYAN}1. Add Patient")
            print("2. Schedule Appointment")
            print("3. Add Medical Record")
            print("4. View Patient History")
            print("5. View Today's Appointments")
            print("6. View My Profile")
            print(f"7. Exit{Style.RESET_ALL}")
            
            choice = input(f"\n{Fore.YELLOW}Enter your choice (1-7): {Style.RESET_ALL}")
            
            if choice == '1':
                self.add_patient()
            elif choice == '2':
                self.schedule_appointment()
            elif choice == '3':
                self.add_medical_record()
            elif choice == '4':
                self.view_patient_history()
            elif choice == '5':
                self.view_appointments()
            elif choice == '6':
                self.display_doctor_info()
            elif choice == '7':
                print(f"{Fore.GREEN}Thank you for using Hospital Management System!{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Invalid choice! Please try again.{Style.RESET_ALL}")

if __name__ == "__main__":
    system = HospitalManagementSystem()
    print(f"\n{Back.BLUE}{Fore.WHITE}Welcome to Hospital Management System{Style.RESET_ALL}")
    while True:
        print(f"\n{Fore.CYAN}1. Login")
        print(f"2. Register")
        print(f"3. Exit{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.YELLOW}Enter your choice (1-3): {Style.RESET_ALL}")
        
        if choice == '1':
            if system.login():
                system.display_doctor_info()
                system.main_menu()
        elif choice == '2':
            system.register()
        elif choice == '3':
            print(f"{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Invalid choice! Please try again.{Style.RESET_ALL}")