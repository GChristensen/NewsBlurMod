app = require('express')()
server = require('http').createServer(app)
log    = require './log.js'

original_page = require('./original_page.js').original_page
original_text = require('./original_text.js').original_text
favicons = require('./favicons.js').favicons
unread_counts = require('./unread_counts.js').unread_counts

original_page(app)
original_text(app)
favicons(app)
unread_counts(server)

log.debug "Starting NewsBlur Node Server"
server.listen(8008)
