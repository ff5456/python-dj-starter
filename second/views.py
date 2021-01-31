from django.shortcuts import render
from django.http import HttpResponseRedirect
from second.models import Post
from .forms import PostForm
# Create your views here.

def list(request):
    context={
        'items' : Post.objects.all()
    }
    return render(request,'second/list.html', context)

def create(request):
    if request.method =='POST':         ##이해 안되는 부분(models.py 의 POST 함수와 일치 하면 이라는 뜻)
        form = PostForm(request.POST)
        if form.is_valid():
            # print(form) //레코드를 생성하는 코드 필요, 터미널 창에 내가 친 내용이 print 된다
            new_item = form.save()      ##form 에 실제 입력 내용이 저장되므로 후 second/list/에서 내가 친 제목과 내용이 나타나진다
        return HttpResponseRedirect('/second/list/')

    form = PostForm()
    return render(request, 'second/create.html', {'form': form})
# render 에 context 대신 바로 정의

def confirm(request):
    form = PostForm(request.POST)
    if form.is_valid():
        return render(request, 'second/confirm.html',{'form':form})
    return HttpResponseRedirect('/second/create/')
