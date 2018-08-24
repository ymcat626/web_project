var todoTemplate = function (title) {
    var t = `
        <div>
            <span>${ title }</span>
            <button class="todo-delete">delete</button>
        </div>
    `
    return t
}

var insertTodo = function (todo) {
    var title = todo.title
    var todoCell = todoTemplate(todo)
    var todoList = e('.todo-list')
    todoList.insertAdjacentHTML('beforeend', todoCell)
}

var loadTodos = function () {
    // 调用 ajax api 来载入数据
    apiTodoAll(function (r) {
        var todos = JSON.parse(r)
        for (var i = 0; i < todos.length; i++) {
            var todo = todos[i]
            insertTodo(todo)
        }
    })
}

var bindEventTodoAdd = function () {
    var b = e('#id-button-add')
    b.addEventListener('click', function () {
        var input = e('id-input-todo')
        var title = input.value
        var form = {
            title: title,
        }
        apiTodoAdd(form, function (r) {
            var todo = JSON.parse(r)
            insertTodo(todo)
        })
    })
}

var bindEvents = function () {
    bindEventTodoAdd()
}

var __main = function () {
    bindEvents()
    loadTodos()
}

__main()