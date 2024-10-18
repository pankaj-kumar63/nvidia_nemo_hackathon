from django.db import models

class Question(models.Model):
    _id = models.IntegerField(blank=False, null=False)  # Optional field to store the original question ID
    question = models.TextField(blank=True, null=True)  # Store the question text
    option_1 = models.TextField(blank=True, null=True)  # Store the first option text
    option_2 = models.TextField(blank=True, null=True)  # Store the second option text
    option_3 = models.TextField(blank=True, null=True)  # Store the third option text
    option_4 = models.TextField(blank=True, null=True)  # Store the fourth option text
    correct_option_number = models.TextField(blank=True, null=True)  # Store the correct option number (e.g., 1, 2, 3, or 4)
    correct_answer = models.TextField(blank=True, null=True)  # Store the correct answer text
    solution = models.TextField(blank=True, null=True)  # Detailed solution or explanation for the answer

    def __str__(self):
        return self.question[:50]  # Returns the first 50 characters of the question for easy reference

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    marks = models.FloatField()

    def __str__(self):
        return f"{self.first_name} {self.second_name}"
