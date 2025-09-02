from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import JobForm
from .models import Job, Application
# Create your views here.

@login_required
def post_job(request):
    if request.user.role != 'employer':
        return redirect('/')  # Only employers can post jobs

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user  # set the employer automatically
            job.save()
            return redirect('/accounts/dashboard/')
    else:
        form = JobForm()
    return render(request, 'jobs/post_job.html', {'form': form})




@login_required
def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})



@login_required
def apply_job(request, job_id):
    if request.user.role != 'student':
        return redirect('/')  # Only students can apply

    job = Job.objects.get(id=job_id)

    if request.method == 'POST':
        resume = request.POST.get('resume')
        Application.objects.create(
            job=job,
            student=request.user,
            resume=resume
        )
        return redirect('/accounts/dashboard/')
    
    return render(request, 'jobs/apply_job.html', {'job': job})



@login_required
def job_applications(request, job_id):
    if request.user.role != 'employer':
        return redirect('/')  # Only employers can see applications

    job = Job.objects.get(id=job_id)

    # make sure the logged-in employer owns this job
    if job.posted_by != request.user:
        return redirect('/accounts/dashboard/')

    applications = job.applications.all()  # get all applications for this job
    return render(request, 'jobs/job_applications.html', {'job': job, 'applications': applications})



@login_required
def update_application_status(request, app_id, status):
    if request.user.role != 'employer':
        return redirect('/')  # Only employers can update

    application = Application.objects.get(id=app_id)
    
    # make sure the logged-in employer owns this job
    if application.job.posted_by != request.user:
        return redirect('/accounts/dashboard/')

    if status in ['reviewed', 'accepted', 'rejected']:
        application.status = status
        application.save()
    
    return redirect(f'/jobs/applications/{application.job.id}/')

@login_required
def my_applications(request):
    if request.user.role != 'student':
        return redirect('/')  # Only students can see their applications

    applications = request.user.applications.all()  # uses related_name from Application model
    return render(request, 'jobs/my_applications.html', {'applications': applications})


@login_required
def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})
