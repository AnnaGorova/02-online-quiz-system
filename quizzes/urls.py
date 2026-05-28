from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('result/<int:result_id>/', views.result, name='result'),
    path('history/', views.history, name='history'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
]
