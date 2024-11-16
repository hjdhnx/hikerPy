from com.example.hikerview.service.parser import JSEngine
njs=JSEngine.getInstance()
import java
import json
from com.alibaba.fastjson import JSON

MY_RULE=None
def log(obj):
    njs.log(MY_TITLE+":"+str(obj), None)
    #njs.log(str(obj), None)

def parseDom(html, rule):
    return str(njs.parseDom(html, rule))

def parseDomForArray(html, rule):
    return json.loads(njs.parseDomForArray(html, rule))

def parseDomForHtml(html, rule):
    return str(njs.parseDomForHtml(html, rule))

def confirm(options):
    njs.confirm(_dictToJSONObject(options),MY_TICKET)
    
def toast(info):
    njs.toast(str(info), MY_TICKET)
    
def fetch(url, options={}):
    return str(njs.fetch(url, _dictToJSONObject(options), _getRule()))
    
    
    
def _getRule():
    global MY_RULE
    if MY_RULE==None:
        MY_RULE = JSON.parseObject(my_rule);
    return MY_RULE;
    
def _dictToJSONObject(dic):
    return JSON.parseObject(json.dumps(dic))