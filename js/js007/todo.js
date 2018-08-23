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
    var inputButton = e('#id-input-content')
    log('todo', inputButton)
    var todo = inputButton.value
    insertTodo(todo, false)
    inputButton.value = ''
    saveTodos()
})

// 用来生成 todo 的模版方法
var todoTemplate = function (todo, done) {
    log('todoTemplate', todo)
    var status = ''
    if (done != false) {
        status = 'done'
    }
    var t = `
        <div class="todo-cell ${ status }">
            <span contenteditable="true" class="todo-content">${ todo }</span>
            <button class="todo-delete">delete</button>
            <button class="todo-done">done</button>
        </div>
    `
    return t
}

// 向节点中插入 todo
var insertTodo = function (todo, done) {
    var todoList = e('#id-div-container')
    t = todoTemplate(todo, done)
    todoList.insertAdjacentHTML('beforeend', t)
}

var container = e('#id-div-container')
// 通过 event.target 的 class 来判断点击的元素
container.addEventListener('click', function (event) {
    log('event', event)
    var target = event.target
    log('target', target)
    if (target.classList.contains('todo-delete')) {
        log('delete')
        var todoDiv = target.parentElement
        todoDiv.remove()
        saveTodos()
    }else if(target.classList.contains('todo-done')) {
        var todoDiv = target.parentElement
        toggleClass(todoDiv, 'done')
        saveTodos()
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

// 通过浏览器自带的 localStorage 来保存数据
var save = function (array) {
    var t = JSON.stringify(array)
    localStorage.todos = t
}

var saveTodos = function () {
    // 1 先选出所有的 content 标签
    // 2 取出 todo
    // 3 添加到一个 数组中
    // 4 保存数组
    var todos = []
    var todoContents = document.querySelectorAll('.todo-content')
    for (var i = 0; i < todoContents.length; i++) {
        var c = todoContents[i]
        var done = c.parentElement.classList.contains('done')
        // log('save todos done', done)
        var todo = {
            done: done,
            content: c.innerHTML,
        }
        log('saveTodos todo', todo)
        todos.push(todo)
    }
    log('saveTodos todos', todos)
    save(todos)
}

var loadTodos = function () {
    todos = load()
    for (var i = 0; i < todos.length; i++) {
        todo = todos[i]
        insertTodo(todo.content, todo.done)
    }
}

var load = function () {
    var todos = JSON.parse(localStorage.todos)
    return todos
}

loadTodos()

