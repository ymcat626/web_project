/*
1, 给 add button 绑定事件
2, 在事件处理函数中, 获取 input 的值
3, 用获取的值 组装一个 todo-cell HTML 字符串
4, 插入 todo-list 中
*/

var log = function () {
    console.log.apply(console, arguments);
};

var e = function (sel) {
    return document.querySelector(sel);
};

var todoTemplate = function (todo) {
    var t = `
        <div class="todo-cell">
            <button class="todo-delete">删除</button>
            <span>${todo}</span>
        </div>
    `;
    return t;
};

var insertTodo = function (todo) {
    var todoCell = todoTemplate(todo);
    var todoList = e('.todo-list');
    todoList.insertAdjacentHTML('beforeend', todoCell);
};

var b = e('#id-button-add');

b.addEventListener('click', function () {
    var input = e('#id-input-todo');
    var todo = input.value;
    insertTodo(todo);
});

/*
给 删除 按钮绑定删除的事件
1, 绑定事件
2, 删除整个 todo-cell 元素
*/
var todoList = e('.todo-list');
todoList.addEventListener('click', function (event) {
    var self = event.target;
    if (self.classList.contains('todo-delete')){
        self.parentElement.remove();
    }
});