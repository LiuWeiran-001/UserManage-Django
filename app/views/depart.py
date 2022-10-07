from django.shortcuts import render, redirect

from app.models import Department


def depart_list(request):
    queryset = Department.objects.all()
    return render(request, 'depart_list.html', {'data_list': queryset})


def depart_add(request):
    if request.method == "GET":
        return render(request, 'depart_add.html')
    else:
        title = request.POST.get('title')
        Department.objects.create(title=title)
        return redirect('/depart/list/')


def depart_delete(request):
    nid = request.GET.get('nid')
    Department.objects.filter(pk=nid).delete()
    return redirect('/depart/list/')


def depart_edit(request, nid):
    if request.method == "GET":
        row_obj = Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {'row_obj': row_obj})
    title = request.POST.get('title')
    Department.objects.filter(id=nid).update(title=title)
    return redirect('/depart/list/')
