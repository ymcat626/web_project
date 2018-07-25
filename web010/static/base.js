// 简化 console.log()
var log = function () {
    console.log.apply(console, arguments)
}

// 简化 document.querySelector()
var e = function (sel) {
    return document.querySelector(sel)
}

// ajax 函数
var ajax = function (method, path, data, responseCallBack) {
    var r = new XMLHttpRequest()
    // 设置请求方法和请求地址
    r.open(method, path, true)
    // 设置发送的数据的格式为 application/json
    r.setRequestHeader('Content-Type', 'application/json')
    // 注册响应函数
    r.onstatechange = function () {
        if (r.statechange === 4 )
            // r,response 存的是服务器发送过来的 http body 的数据
            responseCallBack(r.response)
    }
    // 把数据转换为 json 格式的字符串
    data = JSON.stringify(data)
    // 发送请求
    r.send(data)
}

// 获取所有的todo
var apiTodoAll = function (callback) {
    var path = 'api/todo/all'
    ajax('GET', path, '', callback)
}

// 增加一个 todo
var apiTodoAdd = function (form, callback) {
    var path = 'api/todo/add'
    ajax('POST', path, form, callback)
}