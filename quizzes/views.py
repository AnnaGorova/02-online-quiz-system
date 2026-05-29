from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Quiz, Question, Answer, QuizResult
<<<<<<< HEAD
from .forms import UsernameForm
=======
from .forms import  UsernameForm
>>>>>>> main


def index(request):
    """Головна сторінка - список доступних квізів"""
    quizzes = Quiz.objects.all()
    return render(request, 'quizzes/index.html', {'quizzes': quizzes})


def quiz_detail(request, quiz_id):
    """Сторінка деталей квізу та введення імені"""
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        form = UsernameForm(request.POST)
        if form.is_valid():
            request.session['username'] = form.cleaned_data['username']
            request.session['quiz_id'] = quiz_id
            return redirect('take_quiz', quiz_id=quiz_id)
    else:
        form = UsernameForm()

    return render(request, 'quizzes/quiz_detail.html', {
        'quiz': quiz,
        'form': form
    })


def take_quiz(request, quiz_id):
    """Проходження квізу"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    username = request.session.get('username')

    if not username:
        messages.warning(request, 'Будь ласка, введіть ваше ім\'я')
        return redirect('quiz_detail', quiz_id=quiz_id)

    questions = quiz.questions.all()

    if request.method == 'POST':
        score = 0
        for question in questions:
            answer_id = request.POST.get(f'q_{question.id}')
            if answer_id:
                try:
                    answer = Answer.objects.get(id=answer_id)
                    if answer.is_correct:
                        score += 1
                except Answer.DoesNotExist:
                    pass

        result = QuizResult.objects.create(
            username=username,
            quiz=quiz,
            score=score,
            total=questions.count()
        )

        # Очищення сесії
        if 'username' in request.session:
            del request.session['username']
        if 'quiz_id' in request.session:
            del request.session['quiz_id']

        messages.success(request, f'Ви завершили квіз! Результат: {score}/{questions.count()}')
        return redirect('result', result_id=result.id)

    return render(request, 'quizzes/take_quiz.html', {
        'quiz': quiz,
        'questions': questions,
        'username': username
    })


def result(request, result_id):
    """Сторінка з результатом"""
    result = get_object_or_404(QuizResult, id=result_id)
    return render(request, 'quizzes/result.html', {'result': result})


def history(request):
    """Історія проходжень - показує всі результати, з можливістю фільтрації"""
    # Беремо ВСІ результати, сортуємо від нових до старих
    results = QuizResult.objects.all().order_by('-date')
<<<<<<< HEAD

=======
    
>>>>>>> main
    # Фільтр пошуку (опціонально)
    username = request.GET.get('username', '')
    if username:
        results = results.filter(username__icontains=username)
<<<<<<< HEAD

    return render(request, 'quizzes/history.html', {
        'results': results,
        'search_username': username
    })
=======
    
    return render(request, 'quizzes/history.html', {
        'results': results,
        'search_username': username
    })


>>>>>>> main
