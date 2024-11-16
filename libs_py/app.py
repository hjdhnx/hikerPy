import json
import builtins


def json_parse(content):
    return json.loads(content)



def json_stringify(data):
    return json.dumps(data, ensure_ascii=False)


def call_function_to_jsonstr(mo, func_name,*args, **kwargs):
    return json_stringify(call_function(mo,func_name,*args, **kwargs))

def call_function(mo, func_name,*args, **kwargs):
    func = getattr(mo,func_name,None)
    if func and callable(func):
        return func(*args, **kwargs)
    else:
        raise ValueError(f"Function {func_name} not found in module")

def call_global_function(func_name,*args, **kwargs):
    return call_function(builtins,func_name,*args, **kwargs)


def run():
    pass


if __name__ == '__main__':
    run()