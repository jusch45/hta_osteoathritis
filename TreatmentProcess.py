import simpy

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

# Create the simulation environment
env = simpy.Environment()

# Create a patient instance
patient = Patient(patient_id=1, age=45, bmi=32, osteoarthritis_severity=3)

# Define treatment (e.g., physiotherapy weekly)
treatment = TreatmentProcess(env, patient, treatment_type="physiotherapy", frequency=7)

# Run the simulation for 1 year (365 days)
env.process(treatment.run())
env.run(until=365)  # Simulate for one year
