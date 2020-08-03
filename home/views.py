from django.shortcuts import render

# Create your views here.
def departments(request):  
    return render(request,'departments.html')
def contact(request):  
    return render(request,'contact.html')
def blog(request):  
    return render(request,'blog.html')
def about(request):  
    return render(request,'about.html')