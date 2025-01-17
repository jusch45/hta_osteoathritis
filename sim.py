import random
import simpy
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


class Patient:
    def __init__(self, patient_id, age, bmi, osteoarthritis_severity):
        self.patient_id = patient_id
        self.age = age
        self.bmi = bmi
        self.osteoarthritis_severity = osteoarthritis_severity
        self.pain_level = random.uniform(5, 8)  # Initial pain level
        self.mobility_score = random.uniform(20, 40)  # Initial mobility score (WOMAC scale)
        self.treatment_adherence = 1.0  # Adherence to treatment (initially perfect)
        self.fallback = False
        self.quality_of_life = 50  # SF-36 score

    def apply_treatment(self, treatment_type):
        # Simulate response to physiotherapy or NSAID treatment
        if treatment_type == 'physiotherapy':
            self.pain_level -= random.uniform(0.2, 0.5)  # Pain reduction
            self.mobility_score += random.uniform(1, 2)  # Mobility improvement
        elif treatment_type == 'NSAID':
            self.pain_level -= random.uniform(0.3, 0.6)  # Pain reduction
            self.mobility_score += random.uniform(0.5, 1.5)  # Small improvement in mobility

        # Ensure pain level is non-negative
        self.pain_level = max(0, self.pain_level)

    def simulate_fallback(self):
        # Simulate a fallback scenario where the patient worsens
        if random.random() < 0.1:  # 10% chance of fallback
            self.fallback = True

    def report(self):
        return {
            'patient_id': self.patient_id,
            'pain_level': self.pain_level,
            'mobility_score': self.mobility_score,
            'fallback': self.fallback,
            'quality_of_life': self.quality_of_life
        }


class TreatmentProcess:
    def __init__(self, env, patient, treatment_type, frequency):
        self.env = env
        self.patient = patient
        self.treatment_type = treatment_type
        self.frequency = frequency  # Frequency of treatment (e.g., weekly)

    def run(self):
        while True:
            yield self.env.timeout(self.frequency)  # Time until next treatment session
            self.patient.apply_treatment(self.treatment_type)
            self.patient.simulate_fallback()


def system_dynamics(population, days):
    pain_levels = []
    mobility_scores = []
    for day in range(days):
        total_pain = 0
        total_mobility = 0
        fallback_count = 0
        for patient in population:
            patient.apply_treatment("physiotherapy" if day % 7 == 0 else "NSAID")
            patient.simulate_fallback()
            total_pain += patient.pain_level
            total_mobility += patient.mobility_score
            if patient.fallback:
                fallback_count += 1
        avg_pain = total_pain / len(population)
        avg_mobility = total_mobility / len(population)
        pain_levels.append(avg_pain)
        mobility_scores.append(avg_mobility)

    return pain_levels, mobility_scores


# Simulation setup

def run_simulation():
    # Create the simulation environment
    env = simpy.Environment()

    # Create a population of 100 patients
    population = [Patient(patient_id=i, age=45, bmi=32, osteoarthritis_severity=3) for i in range(100)]

    # Create treatment processes (e.g., weekly physiotherapy sessions)
    treatment_processes = []
    for patient in population:
        treatment_type = "physiotherapy" if patient.patient_id % 2 == 0 else "NSAID"
        treatment_processes.append(TreatmentProcess(env, patient, treatment_type, frequency=7))  # Weekly treatments

    # Run the simulation for 1 year (365 days)
    for process in treatment_processes:
        env.process(process.run())
    env.run(until=365)  # Simulate for one year

    # Run system dynamics simulation for the entire population
    pain_levels, mobility_scores = system_dynamics(population, 365)

    # Return results for further analysis
    return pain_levels, mobility_scores, population


def analyze_results(pain_levels, mobility_scores, population):
    # Plot the results
    plt.plot(pain_levels, label="Average Pain Level")
    plt.plot(mobility_scores, label="Average Mobility Score")
    plt.xlabel("Days")
    plt.ylabel("Score")
    plt.legend()
    plt.title("Treatment Effects Over Time")
    plt.show()

    # Example: Compare pain levels between physiotherapy and NSAID groups
    physiotherapy_group = [patient for patient in population if patient.patient_id % 2 == 0]
    NSAID_group = [patient for patient in population if patient.patient_id % 2 != 0]

    # Collect pain levels for both groups
    pain_physio = [patient.pain_level for patient in physiotherapy_group]
    pain_nsaid = [patient.pain_level for patient in NSAID_group]

    # Perform t-test
    t_stat, p_value = stats.ttest_ind(pain_physio, pain_nsaid)

    print(f"T-statistic: {t_stat}, P-value: {p_value}")


if __name__ == "__main__":
    # Run the simulation and analyze the results
    pain_levels, mobility_scores, population = run_simulation()
    analyze_results(pain_levels, mobility_scores, population)
