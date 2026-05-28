from django.db import models
from .quiz import Quiz

class QuizResult(models.Model):
    username = models.CharField(max_length=100, verbose_name="Ім'я")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(verbose_name='Правильних')
    total = models.IntegerField(verbose_name='Всього')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    
     
    def __str__(self):
        return f"{self.username}: {self.score}/{self.total}"
    
