# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response
import sys
from seach_engine import inverted_index2
reload(sys)
sys.setdefaultencoding('utf-8')

# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators import csrf


# 接收POST请求数据
def search_post(request):
    ctx = {}
    if request.POST:
        ctx['rlt'] = inverted_index2.search1(request.POST['q'])
    return render(request, "index.html", ctx)