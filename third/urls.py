from django.urls import path

from . import views

urlpatterns= [
    path('list/',views.list, name='list'),
    path('create/',views.create, name='restaurant-create'),
    path('update/', views.update, name='restaurant-update'),
    #path('detail/',views.detail, name='restaurant-detail'),
    path('restaurant/delete/<int:id>/',views.delete, name='restaurant-delete'),
    #views.delete 에서 id를 매개변수로 받고 그 id를 url 로 나타낼 수 있게된다
    path('restaurant/<int:id>/',views.detail, name="restaurant-detail"),
    path('restaurant/<int:restaurant_id>/review/create/',views.review_create, name="review-create"),
    path('restaurant/<int:restaurant_id>/review/delete/<int:review_id>',views.review_delete, name="review-delete"),
    path('review/list/',views.review_list, name="review-list")
]