from django.shortcuts import render, get_object_or_404, redirect
from third.models import Restaurant, Review
from django.core.paginator import Paginator
from third.forms import RestaurantForm, ReviewForm, UpdateRestaurantForm
from django.http import HttpResponseRedirect
from django.db.models import Count, Avg


# Create your views here.
def list(request):
    restaurants=Restaurant.objects.all().annotate(reviews_count=Count('review'))\
        .annotate(average_point=Avg('review__point'))
    # restaurants 에 데이터 저장,  annotate를 사용하면 models.Restaurant 에 reviews_count=0,1,2, ..(Count('review')) 이렇게 자동 저장된다
    # 이때 review는 models.py 의 Review 이다. Restaurant model을 가져왔지만 Review model에서 ForeignKey 를 통해 연결되었으므로 자동으로 Restaurant model 에서도 Review 가 적용가능해진다. 대문자는 모두 소문자로 인식하는 장고 특성
    #평균을 하는 것은 review가 아닌, review 안의 point 변수이다. 이는 review__point 로 표시한다
    paginator=Paginator(restaurants, 5)

    page= request.GET.get('page')       ##  --third/list?page=1 형태로 표시
    items = paginator.get_page(page)
    context={
        'restaurants' : items           #restaurants 에 items 저장
    }
    return render(request, 'third/list.html', context)          #html 에 보내기

def create(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            new_item = form.save()
        return HttpResponseRedirect('/third/list/')
    form = RestaurantForm()
    return render(request, 'third/create.html',{'form':form})

def update(request):
    if request.method == 'POST' and 'id' in request.POST :
        #item = Restaurant.objects.get(pk=request.POST.get('id'))
        item = get_object_or_404(Restaurant, pk=request.POST.get('id'))
        password = request.POST.get('password','')
        form = UpdateRestaurantForm(request.POST, instance=item)
        if form.is_valid() and password == item.password:
            item = form.save()
        return HttpResponseRedirect('/third/list/')
    elif request.method == 'GET':
        #item=Restaurant.objects.get(pk=request.GET.get('id'))
        item = get_object_or_404(Restaurant, pk=request.GET.get('id'))
        form = RestaurantForm(instance=item)
        return render(request, 'third/update.html', {'form': form})
    return HttpResponseRedirect('/third/list/')

def detail(request, id):
    if 'id' is not None:
        item = get_object_or_404(Restaurant, pk=id)
        reviews = Review.objects.filter(restaurant=item).all()
        return render(request, 'third/detail.html', {'item':item, 'reviews':reviews})
    return HttpResponseRedirect('/third/list/')

def delete(request, id):
    item = get_object_or_404(Restaurant, pk=id)
    if request.method == 'POST' and 'password' in request.POST:
        if item.password == request.POST.get('password') or item.password == None:
            item.delete()
            return redirect('list')
        return redirect('restaurant-detail', id=id)
    return render(request, 'third/delete.html', {'item':item})

    return HttpResponseRedirect('/third/list/')
#주소를 다 써줘야함

def review_create(request, restaurant_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_item=form.save()
            return redirect('restaurant-detail', id=restaurant_id)
            #주소를 VIEW 이름 기반으로 해서 그대로 간다
    item = get_object_or_404(Restaurant, pk=restaurant_id)
    form = ReviewForm(initial={'restaurant':item})
            #ReviewForm 을 생성하면 원래 백지장 처럼 아무것도 모르는 form 이 생성되는데 시작하면서 initial을 만들어
            #어떤 restaurant에 적혀야 할 comment 인지를 제공하는 것이다. 이때 'restaurant'은 forms.ReveiwForm 의 fields명 이다.
    return render(request, 'third/review_create.html',{'form':form, 'item':item})

'''
정리: 처음 실행이 되면, restaurant_id를 전달받는다. 처음은 POST 가 아니므로 밑에 3 줄이 실행되는데, 
이때 받은 restaurant_id 와 models 의 ReviewForm 을 통해 함수 내에서 item, form 을 생성한다.
이를 html 에 item 과 form 이라는 이름으로 전달해준다. (html 에 설명 있음)
그 다음 POST를 받으면 form의 save가 자동으로 된다. 그후 redirect를 통해 restaurant-detail 화면으로 돌아가게 된다
'''

def review_delete(request, restaurant_id, review_id):
    item = get_object_or_404(Review, pk=review_id)
    item.delete()

    return redirect('restaurant-detail',id=restaurant_id)

def review_list(request):
    reviews = Review.objects.all().select_related().order_by('-created_at')
    paginator = Paginator(reviews, 10)

    page = request.GET.get('page')
    items = paginator.get_page(page)

    context={
        'reviews' : items
    }
    return render(request, 'third/review_list.html', context)