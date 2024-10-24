from django.urls import path
from .import views

urlpatterns = [
    path("", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("staffmain/", views.staffmain, name="staffmain"),
    path("event/", views.event, name="event"),
    path('staffmain/update/<str:eid>/', views.update_ev, name='update_ev'),
    path('staffmain/update/save_update_ev/<str:eid>/', views.save_update_ev, name='save_update_ev'),
    path('staffmain/delete_ev/<str:eid>/', views.delete_ev, name="delete_ev"),
    path('studmain/', views.studmain, name='studmain'),
    path('events/<str:eid>/', views.details_ev, name='details_ev'),
    path('my_events/', views.my_events, name='my_events'),
    path('logout/', views.logout, name='logout'),
    path('view_participants/', views.view_participants, name='view_participants')
]
