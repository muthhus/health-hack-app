from datetime import datetime
from model import Doctor, Room, Patient, Task
from google.appengine.ext import db

import logging


def complete_doctor_tasks(doctor):
    tasks = []
        
    doctor.closed_tasks = []
    doctor.pending_tasks = []
    
    for patient in doctor.patient_set:
        for task in patient.task_set:
            tasks.append(task)

    tasks.sort()

    for task in tasks:
        if task.when_completed:
            doctor.closed_tasks.append(task)
        else:
            doctor.pending_tasks.append(task)
    
    
    
def get_doctor(doctor_name):
    try:
        doctor = Doctor.gql("WHERE name = :name ", name = doctor_name)[0]
        complete_doctor_tasks(doctor)
    except IndexError:
        doctor = None
    return doctor
            
def complete_patient_tasks(patient):
    tasks = []
    
    patient.closed_tasks = []
    patient.pending_tasks = []
    
    for task in patient.task_set:
        tasks.append(task)

    tasks.sort()
    
    for task in tasks:
        if task.when_completed:
            patient.closed_tasks.append(task)
        else:
            patient.pending_tasks.append(task)

    
def get_tasks_for_patient(patient):
    tasks = Task.gql("WHERE patient = :patient ",
            patient = patient)
    return tasks

def get_all_patients():
    patients = Patient.all().fetch(limit=10000)
    for patient in patients:
        complete_patient_tasks(patient)
    return patients
    
def get_patients_for_doctor(doctor):
    patients = Patient.gql("WHERE doctor = :doctor ",
            doctor = doctor).fetch(limit=100000)
    for patient in patients:
        complete_patient_tasks(patient)
    return patients
    
def handover_patients(from_doctor, to_doctor):
    patients = get_patients_for_doctor(from_doctor)
    for patient in patients:
        patient.doctor = to_doctor
        patient.put()
    
def close_task(task, doctor):
    task.when_completed = datetime.now()
    task.completed_by = doctor
    task.put()
    

    
    
    
