var log = function () {
    console.log.apply(console, arguments)
}

var e = function (selector) {
    return document.querySelector(selector)
}

var addButton = e('#id-button-add')
addButton.addEventListener('click', function () {
    // 获取 todo 元素
    var todo = e('#id-input-content')
    log('todo', todo)
    todo = todo.value
    insertTodo(todo)

})

var todoTemplate = function (todo) {
    var t = `
        <div>
            <span>${ todo }</span>
            <button>delete</button>
            <button>done</button>
        </div>
    `
    return t
}

var insertTodo = function (todo) {
    var todoList = e('.todo-list')
    t = todoTemplate(todo)
    todoList.insertAdjacentHTML('beforeEnd', t)
}

var deleteButton = e('')


