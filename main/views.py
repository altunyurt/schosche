# coding:utf-8 

from utils import render_to_response

def index(request):

    return render_to_response('index.jinja', locals())

