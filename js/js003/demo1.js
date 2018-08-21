var log = function() {
    console.log.apply(console, arguments)
}

log('impossible'.includes('possible'))
log('very' + 'good')

var name = 'wanger'
var a = `${ name }, hello`
log(a)

