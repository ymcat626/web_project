var log = function () {
    console.log.apply(console, arguments)
}

var e = function (selector) {
    return document.querySelector(selector)
}

var addButton = e('#id-button-add')
// 给 addButton 加事件绑定
addButton.addEventListener('click', function () {
    // 获取 todo 元素
    var todo = e('#id-input-content')
    log('todo', todo)
    todo = todo.value
    insertTodo(todo)

})

// 用来生成 todo 的模版方法
var todoTemplate = function (todo) {
    var t = `
        <div class="todo-cell">
            <span contenteditable="true">${ todo }</span>
            <button class="todo-delete">delete</button>
            <button class="todo-done">done</button>
        </div>
    `
    return t
}

// 向节点中插入 todo
var insertTodo = function (todo) {
    var todoList = e('#id-div-container')
    t = todoTemplate(todo)
    todoList.insertAdjacentHTML('beforeend', t)
}

var container = e('#id-div-container')

container.addEventListener('click', function (event) {
    log('event', event)
    var target = event.target
    log('target', target)
    if (target.classList.contains('todo-delete')) {
        log('delete')
        target.parentElement.remove()
    }else if(target.classList.contains('todo-done')) {
        var todoDiv = target.parentElement
        toggleClass(todoDiv, 'done')
    }
})

// 此函数用来切换一个元素的某个 class
var toggleClass = function (element, className) {
    if (element.classList.contains(className)) {
        element.classList.remove(className)
    }else {
        element.classList.add(className)
    }
}


