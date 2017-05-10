(function() {
    $.get('http://127.0.0.1:5000/events', function(data) {
        console.log(data);
    })
}())