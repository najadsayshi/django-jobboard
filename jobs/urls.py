from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.post_job, name='post_job'),
        path('', views.job_list, name='job_list'),  # list all jobs
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),  # apply to a job
    path('applications/<int:job_id>/', views.job_applications, name='job_applications'),
    path('applications/update/<int:app_id>/<str:status>/', views.update_application_status, name='update_application_status'),
path('my-applications/', views.my_applications, name='my_applications'),

]
