
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
            try:
                
                about=About.objects.all().order_by("-id")[0]
                about.delete()
                about=About()
                about.body=body
                about.save()
                return redirect("/admin_page")

            except:
                about=About()
                about.body=body
                about.save()
                return redirect("/admin_page")
    else:
        return redirect("/#about")
    

