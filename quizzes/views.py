from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Quiz, Question, Answer, QuizResult
from .forms import QuizForm, UsernameForm


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
    """Історія проходжень"""
    username = request.GET.get('username', '')
    results = []

    if username:
        results = QuizResult.objects.filter(username__icontains=username)

    return render(request, 'quizzes/history.html', {
        'results': results,
        'search_username': username
    })


def admin_panel(request):
    """Адмінпанель для створення квізів, питань, відповідей"""
    quizzes = Quiz.objects.all()
    questions = Question.objects.all()
    quiz_form = QuizForm()

    # Створення квізу
    if request.method == 'POST' and 'create_quiz' in request.POST:
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save()
            messages.success(request, f'Квіз "{quiz.title}" успішно створено!')
            return redirect('admin_panel')
        else:
            messages.error(request, 'Помилка при створенні квізу')

    # Створення питання
    if request.method == 'POST' and 'create_question' in request.POST:
        quiz_id = request.POST.get('quiz_id')
        question_text = request.POST.get('question_text')

        if quiz_id and question_text:
            quiz = Quiz.objects.get(id=quiz_id)
            Question.objects.create(quiz=quiz, text=question_text)
            messages.success(request, 'Питання додано!')
            return redirect('admin_panel')
        else:
            messages.error(request, 'Заповніть всі поля')

    # Створення відповіді
    if request.method == 'POST' and 'create_answer' in request.POST:
        question_id = request.POST.get('question_id')
        answer_text = request.POST.get('answer_text')
        is_correct = request.POST.get('is_correct') == 'on'

        if question_id and answer_text:
            question = Question.objects.get(id=question_id)
            Answer.objects.create(question=question, text=answer_text, is_correct=is_correct)
            messages.success(request, 'Відповідь додано!')
            return redirect('admin_panel')
        else:
            messages.error(request, 'Заповніть текст відповіді')

    # Видалення квізу
    if request.method == 'POST' and 'delete_quiz' in request.POST:
        quiz_id = request.POST.get('quiz_id')
        if quiz_id:
            Quiz.objects.filter(id=quiz_id).delete()
            messages.success(request, 'Квіз видалено!')
            return redirect('admin_panel')

    # Видалення питання
    if request.method == 'POST' and 'delete_question' in request.POST:
        question_id = request.POST.get('question_id')
        if question_id:
            Question.objects.filter(id=question_id).delete()
            messages.success(request, 'Питання видалено!')
            return redirect('admin_panel')

    return render(request, 'quizzes/admin_panel.html', {
        'quizzes': quizzes,
        'questions': questions,
        'quiz_form': quiz_form,
    })
