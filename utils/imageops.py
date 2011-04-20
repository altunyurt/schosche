# coding:utf-8
from subprocess import PIPE, Popen
from cStringIO import StringIO
from django.conf import settings
import os

def call_gm_convert(content, size, fname, geometry=None):

    if not geometry:
        command = ["gm", "convert", "-", "-resize", size, "-filter","box","-antialias",
               "-colorspace","RGB", "-quality", "90", "-depth", "8", "+profile", "*", 
               "-interlace", "LINE", "-"] 
    else:
        _size = size.split('x')
        if isinstance(geometry, basestring):
            _geo = geometry
            geometry = {}
            for item in _geo.split(';'):
                key,val = item.split(':')
                geometry.update({key: int(val)})

        command = ["gm", "convert",'-', '-define', 'jpeg:size=%dx%d'% (int(_size[0])*2, int(_size[0])*2),
                    "-crop", "%(w)dx%(h)d+%(l)d+%(t)d" % geometry, "-filter", 'box',
                   "-antialias", "-colorspace","RGB", "-quality", "90", "-depth", "8", "+profile", "*", 
               "-interlace", "LINE", '-thumbnail', '%s>' % size, '-' ]



    p = Popen(command, stdout=PIPE, stderr=PIPE, stdin=PIPE)
    out, err = p.communicate(input=content)

    if err:
        print err
    else:
        file = open(fname, 'wb')
        file.write(out)
        file.close()
    return 

def get_file_size(data):
    command = ["gm", 'identify', "-", '-format', '%w,%h'] 
    #command = ['identify', '-format', '%w,%h', "-"] 

    p = Popen(command, stdout=PIPE, stderr=PIPE, stdin=PIPE)
    out, err = p.communicate(input=data)
    if err:
        print err
    else:
        return [int(item) for item in out.strip().split(',')]

