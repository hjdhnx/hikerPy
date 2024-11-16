const mpath = "hiker://files/plugins/Chaquopy"

function getMP(name) {
    return mpath + "/" + name;
}

function initPython() {
    initChaquopy(getMP("chaquopy.apk"));
    findJavaClass(getMP("classes.dex"), 'com.chaquo.python.android.AndroidPlatform', getMP('arm64-v8a'));
}
initPython();
let AndroidPlatform = new org.mozilla.javascript.NativeJavaClass(this, findJavaClass("com.chaquo.python.android.AndroidPlatform"));
let Python = new org.mozilla.javascript.NativeJavaClass(this, findJavaClass("com.chaquo.python.Python"));
let PyObject = new org.mozilla.javascript.NativeJavaClass(this, findJavaClass("com.chaquo.python.PyObject"));
let Kwarg = new org.mozilla.javascript.NativeJavaClass(this, findJavaClass("com.chaquo.python.Kwarg"));
if (!Python.isStarted()) {
    let androidPlatform = new AndroidPlatform(getCurrentActivity())
    Python.start(androidPlatform);
}


let py = Python.getInstance();

let machinery = py.getModule("importlib.machinery");
let NativePyApp = machinery.callAttr("SourceFileLoader", "app", getPath(getMP("libs_py/app.py")).slice(7)).callAttr("load_module");
let Builtins = py.getBuiltins();

//构建海阔环境模块
let hiker=machinery.callAttr("SourceFileLoader", "hiker", getPath(getMP("libs_py/hiker.py")).slice(7)).callAttr("load_module");
hiker.put("MY_TITLE", MY_RULE.title);
hiker.put("MY_TICKET", MY_TICKET);
hiker.put("my_rule", JSON.stringify(MY_RULE));
/*
function callFunc(pyObj, funcName, ...args) {
    return pyObj.callAttr(funcName, args || []);
}
*/
function evalCode(...args) {
    return NativePyApp.callAttr("call_global_function", ["eval"].concat(args));
}

function execCode(...args) {
    return NativePyApp.callAttr("call_global_function", ["exec"].concat(args));
}

function toJson(pyObj) {
    return JSON.parse(NativePyApp.callAttr("json_stringify", [pyObj]).toString());
}

const cPath = getPath("hiker://files/_cache/py/").slice(7);

function runPy(path, mname) {
    let name = "";
    let mpath = "";
    if (path.startsWith("http")) {
        name = md5(path);
        requireDownload(path, (mpath = cPath + name + ".py"))
    } else {
        let pa = path.split("/");
        name = pa.pop().split(".")[0];
        mpath = cPath + name + ".py";
        copyFiles(name + ".py", cPath, pa.join("/"));

    }
    return machinery.callAttr("SourceFileLoader", mname||name, mpath).callAttr("load_module");
}
$.exports = {
    PyObject,
    Kwarg,
    //callFunc,
    evalCode,
    execCode,
    runPy,
    toJson,
    Builtins
}