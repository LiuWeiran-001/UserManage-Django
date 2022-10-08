import random
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from app.models import Order
from app.utils.form import OrderModelForm
from app.utils.pagination import Pagination


def order_list(request):
    form = OrderModelForm()
    queryset = Order.objects.all()
    page_obj = Pagination(request, queryset)
    context = {
        "form": form,
        "queryset": page_obj.page_queryset,  # 分页完的数据
        "page_string": page_obj.html()  # 生成页码
    }
    return render(request, "order_list.html", context)


@csrf_exempt
def order_add(request):
    """新建订单（ajax请求）"""
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)

        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        form.instance.admin_id = request.session['info']['id']
        # 保存到数据库中
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, "errors": form.errors})


def order_delete(request):
    """删除订单"""

    uid = request.GET.get("uid")
    exists = Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, "error": "数据不存在"})
    Order.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


def order_detail(request):
    """根据id获取订单详细"""

    """第一种方式 手动构建返回值"""
    # uid = request.GET.get('uid')
    # row_obj = Order.objects.filter(id=uid).first()
    # if not row_obj:
    #     return JsonResponse({"status": False, "error": "数据不存在"})
    # row_dict = {
    #     "title": row_obj.title,
    #     "price": row_obj.price,
    #     "status": row_obj.status,
    # }
    # result = {
    #     "status": True,
    #     "data": row_dict,
    # }
    # return JsonResponse(result)

    """第二种方式 """
    uid = request.GET.get('uid')
    row_dict = Order.objects.filter(id=uid).values('title', 'price', 'status').first()
    if not dict:
        return JsonResponse({"status": False, "error": "数据不存在"})
    result = {
        "status": True,
        "data": row_dict,
    }
    return JsonResponse(result)


@csrf_exempt
def order_edit(request):
    """编辑订单"""
    uid = request.GET.get('uid')
    row_obj = Order.objects.filter(id=uid).first()
    if not row_obj:
        return JsonResponse({"status": False, "tips": "数据不存在"})
    form = OrderModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})
