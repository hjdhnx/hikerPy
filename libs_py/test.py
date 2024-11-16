from base.hiker import *
def holle():
    return "ok h"

def my_function(a, b, d=5,c=3):
    return a + b + c+d

def main():

    log(99)
    confirm({"title":"ok", "content":'检测到你的规则版本小于服务器版本，是否立即更新？'})
    toast(99)
    #og(fetch("http://hiker.nokia.press/hikerule/notice/get"))