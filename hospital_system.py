#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, messagebox
import heapq
from datetime import datetime

class Patient:
    """Patient class to store patient information"""
    def __init__(self, name, severity_level, age, temperature, blood_pressure, arrival_time=None):
        self.name = name
        self.severity_level = severity_level  # 1-5 scale (1=critical, 5=non-urgent)
        self.age = age
        self.temperature = temperature
        self.blood_pressure = blood_pressure
        self.arrival_time = arrival_time or datetime.now()
        
        # Calculate priority score (lower score = higher priority)
        # Severity has highest weight, then vital signs
        self.priority_score = self.calculate_priority()
    
    def calculate_priority(self):
        """Calculate priority score based on multiple factors"""
        # Severity level is primary (1=highest priority, 5=lowest)
        severity_weight = 10
        severity_score = self.severity_level * severity_weight
        
        # Age factor (older patients get higher priority)
        age_factor = 0
        if self.age >= 65:
            age_factor = 3
        elif self.age >= 18:
            age_factor = 5
        else:
            age_factor = 4  # Children get moderate priority
        
        # Temperature factor
        temp_factor = 5
        if self.temperature >= 39:  # High fever
            temp_factor = 2
        elif self.temperature >= 38:  # Fever
            temp_factor = 4
        
        # Blood pressure factor (simplified)
        bp_factor = 5
        systolic = int(self.blood_pressure.split('/')[0]) if '/' in self.blood_pressure else 120
        if systolic >= 180 or systolic <= 90:
            bp_factor = 2
        elif systolic >= 160 or systolic <= 100:
            bp_factor = 4
        
        # Combine all factors (lower score = higher priority)
        total_score = severity_score + age_factor + temp_factor + bp_factor
        return total_score
    
    def __lt__(self, other):
        # For heapq to compare patients based on priority_score
        return self.priority_score < other.priority_score
    
    def __repr__(self):
        return f"{self.name} (Severity: {self.severity_level}, Priority: {self.priority_score})"

class PriorityQueue:
    """Priority queue implementation for patients"""
    def __init__(self):
        self.patients = []
        self.next_patient_id = 1
    
    def add_patient(self, patient):
        """Add a patient to the priority queue"""
        patient.id = self.next_patient_id
        self.next_patient_id += 1
        heapq.heappush(self.patients, patient)
    
    def call_patient(self):
        """Remove and return the patient with highest priority (lowest score)"""
        if self.patients:
            return heapq.heappop(self.patients)
        return None
    
    def peek_next_patient(self):
        """View next patient without removing"""
        if self.patients:
            return self.patients[0]
        return None
    
    def get_queue_size(self):
        """Return number of patients in queue"""
        return len(self.patients)
    
    def is_empty(self):
        """Check if queue is empty"""
        return len(self.patients) == 0
    
    def reset_queue(self):
        """Clear all patients from queue"""
        self.patients = []
        self.next_patient_id = 1
    
    def get_all_patients(self):
        """Return all patients in priority order without removing them"""
        return sorted(self.patients, key=lambda x: x.priority_score)

class HospitalQueueSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Priority Queue System")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f8ff")
        
        # Initialize priority queue
        self.queue = PriorityQueue()
        
        # Add some sample patients for demonstration
        self.add_sample_patients()
        
        # Setup GUI
        self.setup_gui()
    
    def add_sample_patients(self):
        """Add some sample patients for demonstration purposes"""
        sample_patients = [
            Patient("John Smith", 2, 72, 38.5, "145/95"),
            Patient("Mary Johnson", 1, 68, 39.2, "160/110"),
            Patient("Robert Davis", 4, 45, 37.2, "120/80"),
            Patient("Sarah Wilson", 3, 32, 38.0, "135/85"),
            Patient("James Miller", 5, 28, 36.8, "110/70"),
        ]
        
        for patient in sample_patients:
            self.queue.add_patient(patient)
    
    def setup_gui(self):
        """Setup the GUI components"""
        # Header
        header_frame = tk.Frame(self.root, bg="#2e86ab", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame, 
            text="🏥 Hospital Priority Queue System", 
            font=("Arial", 24, "bold"), 
            bg="#2e86ab", 
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Main content area
        main_frame = tk.Frame(self.root, bg="#f0f8ff")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left panel - Controls
        left_frame = tk.Frame(main_frame, bg="#e6f7ff", relief="ridge", bd=2)
        left_frame.pack(side="left", fill="y", padx=(0, 10))
        
        control_label = tk.Label(
            left_frame, 
            text="Queue Controls", 
            font=("Arial", 16, "bold"), 
            bg="#2e86ab", 
            fg="white",
            width=20
        )
        control_label.pack(pady=10, padx=10)
        
        # Control buttons
        buttons_info = [
            ("1. Check Queue Size", self.check_queue_size),
            ("2. Call Next Patient", self.call_next_patient),
            ("3. Add New Patient", self.open_add_patient_window),
            ("4. Check If Queue Is Empty", self.check_queue_empty),
            ("5. Reset Queue", self.reset_queue),
            ("View All Patients", self.view_all_patients),
            ("View Next Patient", self.view_next_patient)
        ]
        
        for text, command in buttons_info:
            button = tk.Button(
                left_frame, 
                text=text, 
                font=("Arial", 12), 
                bg="#4a9cc7", 
                fg="white",
                activebackground="#2e86ab",
                width=20,
                height=2,
                relief="raised",
                command=command
            )
            button.pack(pady=8, padx=10)
        
        # Right panel - Queue display
        right_frame = tk.Frame(main_frame, bg="white", relief="ridge", bd=2)
        right_frame.pack(side="right", fill="both", expand=True)
        
        display_label = tk.Label(
            right_frame, 
            text="Patient Queue", 
            font=("Arial", 16, "bold"), 
            bg="#2e86ab", 
            fg="white"
        )
        display_label.pack(fill="x", pady=10)
        
        # Create treeview for displaying patients
        columns = ("ID", "Name", "Severity", "Priority", "Age", "Temp", "BP", "Arrival Time")
        self.tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=15)
        
        # Define column headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100 if col != "Name" else 120)
        
        self.tree.column("Arrival Time", width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=(0, 10))
        scrollbar.pack(side="right", fill="y", pady=(0, 10))
        
        # Status bar
        self.status_bar = tk.Label(
            self.root, 
            text="Ready. Queue contains 5 sample patients.", 
            font=("Arial", 10), 
            bg="#2e86ab", 
            fg="white",
            anchor="w",
            relief="sunken",
            bd=1
        )
        self.status_bar.pack(side="bottom", fill="x")
        
        # Update the display with current queue
        self.update_queue_display()
    
    def update_queue_display(self):
        """Update the treeview with current queue data"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get all patients in priority order
        patients = self.queue.get_all_patients()
        
        # Insert patients into treeview
        for patient in patients:
            severity_text = self.get_severity_text(patient.severity_level)
            arrival_time = patient.arrival_time.strftime("%H:%M:%S")
            
            self.tree.insert("", "end", values=(
                getattr(patient, 'id', 'N/A'),
                patient.name,
                severity_text,
                patient.priority_score,
                patient.age,
                f"{patient.temperature}°C",
                patient.blood_pressure,
                arrival_time
            ))
        
        # Update status bar
        queue_size = self.queue.get_queue_size()
        self.status_bar.config(text=f"Queue contains {queue_size} patient(s).")
    
    def get_severity_text(self, level):
        """Convert severity level to text"""
        severity_map = {
            1: "Critical",
            2: "Urgent",
            3: "Moderate",
            4: "Low",
            5: "Non-urgent"
        }
        return severity_map.get(level, "Unknown")
    
    def check_queue_size(self):
        """Button 1: Check number of patients in queue"""
        size = self.queue.get_queue_size()
        messagebox.showinfo(
            "Queue Size", 
            f"There are {size} patient(s) in the queue."
        )
    
    def call_next_patient(self):
        """Button 2: Call next patient from queue"""
        if self.queue.is_empty():
            messagebox.showwarning("Queue Empty", "The queue is empty. No patients to call.")
            return
        
        patient = self.queue.call_patient()
        
        # Show patient details
        severity_text = self.get_severity_text(patient.severity_level)
        messagebox.showinfo(
            "Next Patient Called", 
            f"Patient: {patient.name}\n"
            f"Severity: {severity_text}\n"
            f"Priority Score: {patient.priority_score}\n"
            f"Age: {patient.age}\n"
            f"Temperature: {patient.temperature}°C\n"
            f"Blood Pressure: {patient.blood_pressure}\n\n"
            f"Patient has been directed to the treatment area."
        )
        
        # Update display
        self.update_queue_display()
        
        # Check if queue is now empty
        if self.queue.is_empty():
            messagebox.showinfo("Queue Empty", "All patients have been served. Queue is now empty.")
    
    def open_add_patient_window(self):
        """Button 3: Open window to add new patient"""
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Patient")
        add_window.geometry("500x550")
        add_window.configure(bg="#f0f8ff")
        add_window.grab_set()  # Make window modal
        
        # Title
        title_label = tk.Label(
            add_window, 
            text="Add New Patient to Queue", 
            font=("Arial", 16, "bold"), 
            bg="#2e86ab", 
            fg="white",
            width=40
        )
        title_label.pack(pady=10, fill="x")
        
        # Form frame
        form_frame = tk.Frame(add_window, bg="#f0f8ff")
        form_frame.pack(pady=20, padx=30, fill="both")
        
        # Patient name
        tk.Label(form_frame, text="Patient Name:", font=("Arial", 12), bg="#f0f8ff").grid(row=0, column=0, sticky="w", pady=10)
        name_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
        name_entry.grid(row=0, column=1, pady=10, padx=10)
        name_entry.insert(0, "New Patient")
        
        # Severity level
        tk.Label(form_frame, text="Severity Level:", font=("Arial", 12), bg="#f0f8ff").grid(row=1, column=0, sticky="w", pady=10)
        severity_var = tk.IntVar(value=3)
        
        # Severity explanation
        severity_frame = tk.Frame(form_frame, bg="#f0f8ff")
        severity_frame.grid(row=1, column=1, pady=10, padx=10, sticky="w")
        
        severity_scale = tk.Scale(
            severity_frame, 
            from_=1, 
            to=5, 
            orient="horizontal",
            variable=severity_var,
            length=200
        )
        severity_scale.pack()
        
        severity_info = tk.Label(
            severity_frame,
            text="1=Critical, 2=Urgent, 3=Moderate, 4=Low, 5=Non-urgent",
            font=("Arial", 9),
            bg="#f0f8ff",
            fg="#666666"
        )
        severity_info.pack(pady=5)
        
        # Age
        tk.Label(form_frame, text="Age:", font=("Arial", 12), bg="#f0f8ff").grid(row=2, column=0, sticky="w", pady=10)
        age_spinbox = tk.Spinbox(form_frame, from_=1, to=120, font=("Arial", 12), width=10)
        age_spinbox.grid(row=2, column=1, pady=10, padx=10, sticky="w")
        age_spinbox.delete(0, tk.END)
        age_spinbox.insert(0, "30")
        
        # Temperature
        tk.Label(form_frame, text="Temperature (°C):", font=("Arial", 12), bg="#f0f8ff").grid(row=3, column=0, sticky="w", pady=10)
        temp_spinbox = tk.Spinbox(form_frame, from_=35.0, to=42.0, increment=0.1, format="%.1f", font=("Arial", 12), width=10)
        temp_spinbox.grid(row=3, column=1, pady=10, padx=10, sticky="w")
        temp_spinbox.delete(0, tk.END)
        temp_spinbox.insert(0, "37.0")
        
        # Blood Pressure
        tk.Label(form_frame, text="Blood Pressure:", font=("Arial", 12), bg="#f0f8ff").grid(row=4, column=0, sticky="w", pady=10)
        bp_frame = tk.Frame(form_frame, bg="#f0f8ff")
        bp_frame.grid(row=4, column=1, pady=10, padx=10, sticky="w")
        
        systolic_var = tk.StringVar(value="120")
        diastolic_var = tk.StringVar(value="80")
        
        systolic_spinbox = tk.Spinbox(bp_frame, from_=70, to=200, textvariable=systolic_var, font=("Arial", 10), width=5)
        systolic_spinbox.pack(side="left")
        
        tk.Label(bp_frame, text="/", font=("Arial", 12), bg="#f0f8ff").pack(side="left", padx=5)
        
        diastolic_spinbox = tk.Spinbox(bp_frame, from_=40, to=130, textvariable=diastolic_var, font=("Arial", 10), width=5)
        diastolic_spinbox.pack(side="left")
        
        # Buttons frame
        button_frame = tk.Frame(add_window, bg="#f0f8ff")
        button_frame.pack(pady=20)
        
        def submit_patient():
            """Collect data and add patient to queue"""
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Please enter a patient name.")
                return
            
            severity = severity_var.get()
            age = int(age_spinbox.get())
            temperature = float(temp_spinbox.get())
            bp = f"{systolic_var.get()}/{diastolic_var.get()}"
            
            # Create new patient
            patient = Patient(name, severity, age, temperature, bp)
            
            # Add to queue
            self.queue.add_patient(patient)
            
            # Update display
            self.update_queue_display()
            
            # Show confirmation
            messagebox.showinfo("Patient Added", f"Patient {name} added to the queue with priority score {patient.priority_score}.")
            
            # Close window
            add_window.destroy()
        
        # Submit button
        submit_btn = tk.Button(
            button_frame, 
            text="Add Patient to Queue", 
            font=("Arial", 12, "bold"), 
            bg="#4CAF50", 
            fg="white",
            width=20,
            height=2,
            command=submit_patient
        )
        submit_btn.pack(side="left", padx=10)
        
        # Cancel button
        cancel_btn = tk.Button(
            button_frame, 
            text="Cancel", 
            font=("Arial", 12), 
            bg="#f44336", 
            fg="white",
            width=15,
            height=2,
            command=add_window.destroy
        )
        cancel_btn.pack(side="left", padx=10)
    
    def check_queue_empty(self):
        """Button 4: Check if queue is empty (returns boolean)"""
        is_empty = self.queue.is_empty()
        
        if is_empty:
            messagebox.showinfo("Queue Status", "The queue is EMPTY. (Boolean: True)")
        else:
            messagebox.showinfo("Queue Status", f"The queue is NOT EMPTY. It contains {self.queue.get_queue_size()} patient(s). (Boolean: False)")
    
    def reset_queue(self):
        """Button 5: Reset the queue (clear all patients)"""
        if self.queue.is_empty():
            messagebox.showinfo("Queue Empty", "The queue is already empty.")
            return
        
        # Ask for confirmation
        confirm = messagebox.askyesno(
            "Confirm Reset", 
            "Are you sure you want to reset the queue? This will remove all patients."
        )
        
        if confirm:
            self.queue.reset_queue()
            self.update_queue_display()
            messagebox.showinfo("Queue Reset", "The queue has been reset. All patients have been removed.")
    
    def view_all_patients(self):
        """Additional feature: View all patients in queue"""
        if self.queue.is_empty():
            messagebox.showinfo("Queue Empty", "The queue is empty.")
            return
        
        patients = self.queue.get_all_patients()
        
        # Create a formatted message
        message = "Current Queue (in priority order):\n\n"
        for i, patient in enumerate(patients, 1):
            severity_text = self.get_severity_text(patient.severity_level)
            message += f"{i}. {patient.name}\n"
            message += f"   Severity: {severity_text}, Priority Score: {patient.priority_score}\n"
            message += f"   Age: {patient.age}, Temp: {patient.temperature}°C, BP: {patient.blood_pressure}\n\n"
        
        # Show in a scrollable text box
        view_window = tk.Toplevel(self.root)
        view_window.title("All Patients in Queue")
        view_window.geometry("600x500")
        
        text_widget = tk.Text(view_window, wrap="word", font=("Arial", 11))
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        text_widget.insert("1.0", message)
        text_widget.config(state="disabled")
        
        close_btn = tk.Button(
            view_window, 
            text="Close", 
            font=("Arial", 12), 
            command=view_window.destroy
        )
        close_btn.pack(pady=10)
    
    def view_next_patient(self):
        """Additional feature: View next patient without calling"""
        if self.queue.is_empty():
            messagebox.showinfo("Queue Empty", "The queue is empty.")
            return
        
        patient = self.queue.peek_next_patient()
        severity_text = self.get_severity_text(patient.severity_level)
        
        messagebox.showinfo(
            "Next Patient in Queue", 
            f"Next Patient (not called yet):\n\n"
            f"Name: {patient.name}\n"
            f"Severity: {severity_text}\n"
            f"Priority Score: {patient.priority_score}\n"
            f"Age: {patient.age}\n"
            f"Temperature: {patient.temperature}°C\n"
            f"Blood Pressure: {patient.blood_pressure}\n"
            f"Arrival Time: {patient.arrival_time.strftime('%H:%M:%S')}"
        )

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalQueueSystem(root)
    root.mainloop()
