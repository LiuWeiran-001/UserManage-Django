from django.shortcuts import render, redirect

from app.models import Admin
from app.utils.form import AdminModelForm
from app.utils.pagination import Pagination


def admin_list(request):
    qs = Admin.objects.all()
    page_obj = Pagination(request, qs)
    context = {
        "queryset": page_obj.page_queryset,  # 分完页的数据
        "page_string": page_obj.html()  # 生成页码
    }
    return render(request, 'admin_list.html', context)


def admin_add(request):
    if request.method == "GET":
        form = AdminModelForm()
        context = {
            "form": form,
            "title": "新建管理员",
        }
        return render(request, 'change.html', context)
    else:
        form = AdminModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("/admin/list")
        return render(request, 'change.html', {"form": form, "title": "添加管理员"})


def admin_edit(request, nid):
    row_obj = Admin.objects.filter(id=nid).first()
    if request.method == "GET":
        form = AdminModelForm(instance=row_obj)
        context = {
            "form": form,
            "title": "编辑管理员",
        }
        return render(request, 'change.html', context)
    form = AdminModelForm(instance=row_obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {'title': "编辑管路员", 'form': form})


def admin_delete(request, nid):
    Admin.objects.get(id=nid).delete()
    return redirect('/admin/list/')


from app.utils.form import AdminResetModelForm


def admin_reset(request, nid):
    row_obj = Admin.objects.filter(id=nid).first()
    if request.method == "GET":
        form = AdminResetModelForm()
        context = {
            "form": form,
            "title": "重置密码 - {}".format(row_obj.user_name),
        }
        return render(request, 'change.html', context)
    form = AdminResetModelForm(instance=row_obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {'title': "重置密码 - {}".format(row_obj.user_name), 'form': form})
