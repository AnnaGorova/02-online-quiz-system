from django.db import models
from .question import Question

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=300, verbose_name='Відповідь')
    is_correct = models.BooleanField(default=False, verbose_name='Правильна')
    
    
    def __str__(self):
        return f"{self.text} ({'✓' if self.is_correct else '✗'})"
