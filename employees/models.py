from django.db import models
import uuid

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)

    class Meta:
        abstract = True

class PermanentAddress(Address):
    pass

class CommunicationAddress(Address):
    pass

class BankAccount(models.Model):
    account_holder_name = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50)
    ifsc_code = models.CharField(max_length=20)
    branch_name = models.CharField(max_length=255, blank=True, null=True)
    account_type = models.CharField(
        max_length=10,
        choices=[('savings', 'Savings'), ('current', 'Current')],
        default='savings'
    )

class Employee(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]

    # Primary Key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Personal Information
    full_name = models.CharField(max_length=255)
    father_or_spouse_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    personal_mobile = models.CharField(max_length=15)
    personal_email = models.EmailField()
    
    # Addresses (One-to-One relationships)
    permanent_address = models.OneToOneField(PermanentAddress, on_delete=models.CASCADE)
    communication_address = models.OneToOneField(CommunicationAddress, on_delete=models.CASCADE)
    
    # Bank Account Details (One-to-One relationship)
    bank_account = models.OneToOneField(BankAccount, on_delete=models.CASCADE)
    
    # Employee Information
    employee_id = models.CharField(max_length=50, unique=True)
    designation = models.CharField(max_length=100)
    joining_date = models.DateField()
    reporting_manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    official_mobile = models.CharField(max_length=15)
    official_email = models.EmailField()
    
    # Document Upload Fields
    aadhar_card = models.FileField(upload_to='employee_docs/aadhar/', null=True, blank=True)
    pan_card = models.FileField(upload_to='employee_docs/pan/', null=True, blank=True)
    salary_slip = models.FileField(upload_to='employee_docs/salary/', null=True, blank=True)
    passport = models.FileField(upload_to='employee_docs/passport/', null=True, blank=True)
    driving_license = models.FileField(upload_to='employee_docs/driving/', null=True, blank=True)
    bank_statement = models.FileField(upload_to='employee_docs/bank/', null=True, blank=True)
    offer_letter = models.FileField(upload_to='employee_docs/offer/', null=True, blank=True)
    photo = models.ImageField(upload_to='employee_docs/photos/', null=True, blank=True)
    education_certificates = models.FileField(upload_to='employee_docs/education/', null=True, blank=True)
    experience_certificate = models.FileField(upload_to='employee_docs/experience/', null=True, blank=True)
    relieving_letter = models.FileField(upload_to='employee_docs/relieving/', null=True, blank=True)
    appraisal_document = models.FileField(upload_to='employee_docs/appraisal/', null=True, blank=True)
    medical_certificate = models.FileField(upload_to='employee_docs/medical/', null=True, blank=True)
    appointment_letter = models.FileField(upload_to='employee_docs/appointment/', null=True, blank=True)
    employee_agreement = models.FileField(upload_to='employee_docs/agreement/', null=True, blank=True)
    insurance_document = models.FileField(upload_to='employee_docs/insurance/', null=True, blank=True)
    tax_form = models.FileField(upload_to='employee_docs/tax/', null=True, blank=True)
    nominee_form = models.FileField(upload_to='employee_docs/nominee/', null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.employee_id})"
