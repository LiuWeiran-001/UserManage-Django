from django.utils.safestring import mark_safe
import math

"""

自定义分页组件


# 1. 根据自己的情况去筛选数据

querset = models.Foo.object.all()

# 2.实例化分页对象
page_obj = Pagination(request, queryset)
context = {
    "queryset":page_object.page_queryset,   #分完页的数据
    "page_string": page_object.html()       #生成页码    
}
return render(request, '****.html', context)


在html页面中
    {% for obj in queryset %}
       {{ onj.xx }}
    {% endfor %}
    
    
    <div style="text-align: center">
        <ul class="pagination">
            {{ page_string }}
        </ul>
    </div>
"""


class Pagination(object):
    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = 10
        self.start = (self.page - 1) * self.page_size
        self.end = self.page * self.page_size

        self.page_queryset = queryset[self.start:self.end]
        total_count = queryset.count()
        # self.total_page_count = math.ceil(total_count/page_size)
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        if self.total_page_count <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page_count + 1
        else:
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - self.plus * 2
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        page_str_list = []
        # 首页
        page_str_list.append('<li><a href="?page={}">首页</a></li>'.format(1))
        # 上一页
        if self.page > 1:
            prev = '<li><a href="?page={}">上一页</a></li>'.format(self.page - 1)
        else:
            prev = '<li><a href="?page={}">上一页</a></li>'.format(1)
        page_str_list.append(prev)
        # 页码
        for i in range(start_page, end_page + 1):
            if i == self.page:
                ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
            else:
                ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
            page_str_list.append(ele)
        # 下一页
        if self.page < self.total_page_count:
            prev = '<li><a href="?page={}">下一页</a></li>'.format(self.page + 1)
        else:
            prev = '<li><a href="?page={}">下一页</a></li>'.format(self.total_page_count)
        page_str_list.append(prev)
        # 尾页
        page_str_list.append('<li><a href="?page={}">尾页</a></li>'.format(self.total_page_count))
        search_string = """
            <li>
                <form style="float: left;margin-left: -1px" method="get">
                    <input type="text" style="position: relative; float: left; display: inline-block;width: 80px;
                border-radius: 0" name="page" class="form-control" placeholder="页码">
                    <button style="border-radius: 0" class="btn btn-primary" type="submit">跳转</button>
                </form>
            </li>
        """
        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))
        return page_string
