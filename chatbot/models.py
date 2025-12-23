from django.db import models

# Create your models here.
class FAQ(models.Model):
    
    question = models.CharField(max_length=150)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)

    
    def __str__(self):
        return f"{self.question}  --- answer => {self.answer}"
    
    