from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Question, Response
from .forms import RegisterUserForm, LoginForm, NewQuestionForm, NewResponseForm, NewReplyForm, UpdateProfileForm, UpdateUserForm
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.template.defaultfilters import slugify
# Create your views here.

def registerPage(request):
    form = RegisterUserForm()

    if request.method == 'POST':
        try:
            form = RegisterUserForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('index')
        except Exception as e:
            print(e)
            raise

    context = {
        'form': form
    }
    return render(request, 'register.html', context)



def loginPage(request):
    form = LoginForm()

    if request.method == 'POST':
        try:
            form = LoginForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('index')
        except Exception as e:
            print(e)
            raise

    context = {'form': form}
    return render(request, 'login.html', context)

@login_required(login_url='register') # if not logged in , reg page will be shown  (useless)
def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='register')
def newQuestionPage(request):
    form = NewQuestionForm()

    if request.method == 'POST':
        try:
            form = NewQuestionForm(request.POST, request.FILES)
            if form.is_valid():
                question = form.save(commit=False)
                question.author = request.user  # saving author from user(so basically form me sb present ho zruri ni)
                question.save()
                form.save_m2m()  # After you’ve manually saved the instance produced by the form, you can invoke save_m2m() to save the many-to-many form data
                id = question.id
                return redirect('/question/'+str(id))
        except Exception as e:
            print(e)
            raise

    context = {'form': form,}
    return render(request, 'new-question.html', context)

def homePage(request):
    questions = Question.objects.all().order_by('-created_at')[:10]
    context = {
        'questions': questions
    }
    return render(request, 'homepage.html', context)

def questionPage(request, id):
    response_form = NewResponseForm()
    reply_form = NewReplyForm()

    if request.method == 'POST':
        try:
            response_form = NewResponseForm(request.POST)
            # this is for : what happens when you add any response
            if response_form.is_valid():
                response = response_form.save(commit=False) # see this
                response.user = request.user
                response.question = Question(id=id)  # question k id k through Question model se question detail pick krre h, jo  response detail k sath dave krna h
                response.save()
                return redirect('/question/'+str(id)+'#'+str(response.id))  #  /qquestion/'+str(id) - take you to the same page,  '#'+str(response.id) - takes you to the particular section of pg : specified by id : basically on that comment
        except Exception as e:
            print(e)
            raise

    # here , with question.html and in model related name, timestamp: 2:09
    question = Question.objects.get(id=id)
    liked = False
    if question.likes.filter(id=request.user.id).exists():  
        liked = True
    else:
        liked = False  

    context = {
        'question': question,
        'response_form': response_form,
        'reply_form': reply_form,
        'liked': liked,
    }
    return render(request, 'question.html', context)


@login_required(login_url='register')
def replyPage(request):
    if request.method == 'POST':
        try:
            form = NewReplyForm(request.POST)
            if form.is_valid():
                question_id = request.POST.get('question')
                parent_id = request.POST.get('parent')
                reply = form.save(commit=False)
                reply.user = request.user
                reply.question = Question(id=question_id)
                reply.parent = Response(id=parent_id)
                reply.save()
                return redirect('/question/'+str(question_id)+'#'+str(reply.id))
        except Exception as e:
            print(e)
            raise

    return redirect('index')


def searchResults(request):
    search_question = request.GET.get('search')
    if search_question:
        questions = Question.objects.filter(Q(title__icontains=search_question) | Q(body__icontains=search_question) | Q(tags__name__icontains=search_question)).distinct()[:10] # distinct islie kuki , jo result return hta h , vo join of ans set of all condition hta h : to same ans 1 se jyada or cond me satisfy kr skte h
    else:
    # If not searched, return default posts
        questions = Question.objects.all().order_by('-created_at')[:10]   
    
    
    context = {
        'questions': questions,
        'phrase' : search_question
    }
    return render(request, 'homepage.html', context)

def LikeView(request, pk):
    question = get_object_or_404(Question, id=request.POST.get('question_id'))  # this will take that button from form
    if question.likes.filter(id=request.user.id).exists():  # removing the like of person : if he's disliking
        question.likes.remove(request.user)
    else:
        question.likes.add(request.user) # saving that person who liked the question
    return HttpResponseRedirect(reverse('question', args=[str(pk)]))

def LikeViewResponse(request):
    response = get_object_or_404(Response, id=request.POST.get('response_id'))  # this will take that button from form
    if response.likes.filter(id=request.user.id).exists():  # removing the like of person : if he's disliking
        response.likes.remove(request.user)
    else:
        response.likes.add(request.user) # saving that person who liked the question
    return HttpResponseRedirect(reverse('question', args=[str(response.question.id)]))    


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('index')

