from django.conf.urls import url, include
from . import views

urlpatterns = [
    url('user_owned', views.user_owned, name='users_owned'),
    url('all_owned', views.all_owned, name='all_owned'),
    url('run_rfid', views.Run_rfid, name='Run_rfid'),
    url('run_rf', views.Run_rf, name='Run_rf'),
    url('run_finger', views.Run_finger, name='Run_finger'),

    url('all_name', views.all_name, name='all_name'),
    url('user_activ', views.user_activ, name='user_activ'),
    url('add_finger', views.add_finger, name='add_finger'),
    url('(?P<user_id>[0-9]{1})', views.change_user, name='change_user'),

    url('', views.index, name='users')

]
