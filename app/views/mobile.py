from django.shortcuts import render, redirect
from app.models import PreetyNum
from ..utils.pagination import Pagination
from ..utils.form import MobileModelForm


def mobile_list(request):
    data_dict = {}
    search_data = request.GET.get('search', "")
    if search_data:
        data_dict["mobile__contains"] = search_data

    queryset = PreetyNum.objects.filter(**data_dict)
    page_obj = Pagination(request, queryset)
    query_set = page_obj.page_queryset
    page_string = page_obj.html
    #  页码

    return render(request, 'mobilie_list.html', {"queryset": query_set, 'page_string': page_string})


def mobile_add(request):
    if request.method == "GET":
        mobile_form = MobileModelForm()
        return render(request, 'mobile_add.html', locals())
    mobile_form = MobileModelForm(data=request.POST)
    if mobile_form.is_valid():
        # print(1)
        # print(user_form.cleaned_data)
        mobile_form.save()
        return redirect('/mobile/list/')
    return render(request, 'user_add.html', {'user_form': mobile_form})


def mobile_edit(request, nid):
    row_obj = PreetyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        # 根据id获取编辑行的数据
        form = MobileModelForm(instance=row_obj)
        return render(request, 'mobile_edit.html', {"mobile": form})
    form = MobileModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect("/mobile/list")
    return render(request, 'mobile_edit.html', {"mobile": form})


def mobile_delete(request, nid):
    # print(PreetyNum.objects.all())
    PreetyNum.objects.get(id=nid).delete()
    return redirect('/mobile/list/')
