from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render, redirect

from app.models import Admin
from app.utils.code import check_code
from app.utils.form import LoginForm


def login(request):
    """登陆"""
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user_input_code = form.cleaned_data.pop('code')
            image_code = request.session.get('image_code', '')
            if user_input_code.upper() != image_code.upper():
                form.add_error("code", "验证码错误")
                return render(request, 'login.html', {'form': form})
            admin_obj = Admin.objects.filter(**form.cleaned_data).first()
            # print(admin_obj)
            if not admin_obj:
                form.add_error("password", "用户名或密码错误")  # 主动添加错误信息
                form.add_error("user_name", "用户名或密码错误")  # 主动添加错误信息
                return render(request, 'login.html', {'form': form})
            request.session["info"] = {'id': admin_obj.id, 'name': admin_obj.user_name}  # 将用户信息写入session
            request.session.set_expiry(60 * 60 * 24 * 7)  # session 保存七天
            return redirect('/admin/list')
        return render(request, 'login.html', {'form': form})


def logout(request):
    """注销"""
    request.session.clear()  # 清除session
    return redirect('/login/')


def image_code(request):
    """生成验证码"""

    img, code_string = check_code()
    # 将验证码放入session  方便登陆验证
    request.session['image_code'] = code_string
    # 设置60秒超时
    request.session.set_expiry(60)
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())
