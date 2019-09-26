
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accountapp.models import About
@login_required
def admin(request):
    return render(request,"admin/admin.html")

@login_required
def about(request):
    if request.method=='POST':
        body=request.POST["about"]
        if(body):
            old_about=About.objects.get()[0]

            old_about.body=body
            old_about.save()
            return redirect("/admin_page")
    else:
        return redirect("/#about")
    

