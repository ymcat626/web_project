var polygon = function (length, perimeter) {
    var x = length
    var n = perimeter
    var angle = 180 - ((n - 2) * 180 / n)
    var i = 0
    while (i < n) {
        i += 1
        forward(x)
        right(angle)
    }
}
polygon(50, 4)