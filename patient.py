import random

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
