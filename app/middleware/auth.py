from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin



class AuthMiddleWare(MiddlewareMixin):

    def process_request(self, request):

        # 1. 读取当前访问用户的session信息，如果能读的到，说明已经登陆过，则可以继续向后走
        #   request.path_info  获取当前用户请求的URL
        if request.path_info in ["/login/", "/image/code/"]:
            return
        info_dict = request.session.get("info")
        # print(info_dict)
        if info_dict:
            return

        # 2. 如果没有登陆过，回到登录页面
        return redirect('/login/')
