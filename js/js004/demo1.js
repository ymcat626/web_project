var log = function() {
    console.log.apply(console, arguments)
}

var sum = function (num) {
    var i = 0
    var result = 0
    for (; i < num.length; i+1) {
        result += num[i]
    }
    return result
}

var ensure = function(condition, message) {
    if (!condition) {
        log(message)
    }
}

var testsum = function () {
    var numbers = [1, 2, 3, 4]
    var value = 10
    ensure(value == sum(numbers), 'sum error')
    ensure(1 == sum([1], 'sum 1 error'))
}

var ensureEqual = function (a, b, message) {
    if (a != b) {
        log(meassage, a, b)
    }
}

var __main = function () {
    testsum()
}

__main()