import json

# from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app.models import Task
from app.utils.form import TaskModelForm


def task_list(request):
    """任务列表"""
    queryset = Task.objects.all().order_by('-id')
    form = TaskModelForm()
    context = {
        "form": form,
        "queryset": queryset,
    }
    return render(request, 'task_list.html', context)


@csrf_exempt  # 免除  ajax post 的验证
def task_ajax(request):
    print(request.GET)
    print(request.POST)
    data_dict = {"status": True, "data": [11, 22, 33, 44]}
    # json_string = json.dumps(data_dict)
    return HttpResponse(json.dumps(request.POST))


# 用JSonresponse  简写  # return JsonResponse(json.dumps(data_dict))
@csrf_exempt
def task_add(request):
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))
    data_dict = {"status": False, "errors": form.errors}
    return HttpResponse(json.dumps(data_dict))
