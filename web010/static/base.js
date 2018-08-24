var log = function () {
    console.log.apply(console, arguments)
}

var e = function (query) {
    return document.querySelector(query)
}

var ajax = function (method, path, data, responseCallback) {
    var r = new XMLHttpRequest()
    r.open(method, path, true)
    r.setRequestHeader('Content-Type', 'application/json')
    r.onreadystatechange = function () {
        if (r.readyState === 4) {
            responseCallback(r.response)
        }
    }
    // 把数据转换为 json 格式字符串
    data = JSON.stringify(data)
    r.send(data)
}


// todo api
// 获取所有的 todo
var apiTodoAll = function (callback) {
    var path = '/api/todo/all'
    ajax('GET', path, '', callback)
}

// 增加一个 todo
var apiTodoAdd = function (form, callback) {
    var path = 'api/todo/add'
    ajax('POST', path, form, callback)
}