from django.shortcuts import render, redirect
from  app.models import UserInfo
from ..utils.form import UserInfoModelForm



def user_list(request):
    query_set = UserInfo.objects.all()
    return render(request, 'user_list.html', {"queryset": query_set})


def user_add(request):
    if request.method == "GET":
        user_form = UserInfoModelForm()
        # context = {
        #     "gender_choices": UserInfo.gender_chioces,
        #     "department_list": Department.objects.all()
        # }
        return render(request, 'user_add.html', {'user_form': user_form})
    user_form = UserInfoModelForm(data=request.POST)
    if user_form.is_valid():
        # print(1)
        # print(user_form.cleaned_data)
        user_form.save()
        return redirect('/user/list/')
    return render(request, 'user_add.html', {'user_form': user_form})


def user_edit(request, nid):
    """编辑用户"""
    row_obj = UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        # 根据id获取编辑行的数据
        form = UserInfoModelForm(instance=row_obj)
        return render(request, 'user_edit.html', {"form": form})
    form = UserInfoModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect("/user/list")
    return render(request, 'user_edit.html', {"form": form})


def user_delete(request, nid):
    UserInfo.objects.get(id=nid).delete()
    return redirect('/user/list/')
