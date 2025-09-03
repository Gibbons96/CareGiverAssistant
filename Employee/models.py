from django.db import models

class EmployeeApplication(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    TITLE_CHOICES = [('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Miss', 'Miss'), ('Ms', 'Ms')]

    # Personal Info
    title = models.CharField(max_length=10, choices=TITLE_CHOICES)
    forenames = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField()
    phone_mobile = models.CharField(max_length=20)
    address = models.TextField()
    eircode = models.CharField(max_length=10)
    pps_number = models.CharField(max_length=20)
    occupation = models.CharField(max_length=100)
    language = models.CharField(max_length=100, null=True)
    eu_passport_or_gnib = models.BooleanField(default=False)

    # Emergency Contact
    emergency_name = models.CharField(max_length=100)
    emergency_relationship = models.CharField(max_length=50)
    emergency_phone = models.CharField(max_length=20)

    # Bank (Optional - for payroll)
    iban = models.CharField(max_length=34, blank=True)
    bic = models.CharField(max_length=11, blank=True)

    # PROFESSIONAL QUALIFICATIONS / CERTIFICATIONS
    student_nurse_id = models.BooleanField(default=False)
    nmbi_cert = models.BooleanField(default=False)
    fetac_level_5 = models.BooleanField(default=False)
    social_care_cert = models.BooleanField(default=False)

    # General Training Certifications
    cpr_cert = models.BooleanField(default=False)
    patient_moving = models.BooleanField(default=False)
    elder_abuse = models.BooleanField(default=False)
    ppe_training = models.BooleanField(default=False)
    infection_control = models.BooleanField(default=False)
    safeguarding_adults = models.BooleanField(default=False)
    hand_hygiene = models.BooleanField(default=False)
    fire_safety = models.BooleanField(default=False)
    children_first = models.BooleanField(default=False)
    gdpr = models.BooleanField(default=False)

    # Occupational Health
    hep_b = models.BooleanField(default=False)
    mmr_immunity = models.BooleanField(default=False)
    varicella_immunity = models.BooleanField(default=False)


    # Timestamp
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.forenames} {self.surname} - {self.email}"
