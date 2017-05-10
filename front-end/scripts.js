(function() {
    // Hide venues and entrants div on load
    $('#venues').hide();
    $('#entrants').hide();
    $('#event-details').hide();

    const baseUrl = 'http://127.0.0.1:5000'

    //// FRONT PAGE ///////////////////////////////////////////////////////////////////////////////////////////
    // GET events info for front page ////////////////////////////////////////////////////////////////////////
    $.get(baseUrl + '/events', function(data) {
        data.events.forEach(function (obj) {
            // create new event div, set data-id, css classes, and event name
            var newDiv = document.createElement('div');
            newDiv.setAttribute('data-id', obj.id);
            newDiv.innerHTML = obj.name;
            newDiv.className = 'event';

            // create new span to list event's games, and change font size
            var gamesSpan = document.createElement('span');
            gamesSpan.style.fontSize = '12pt';
            gamesSpan.innerHTML = obj.games;

            // append gamesSpan to newDiv
            $(newDiv).append('<br/>');
            $(newDiv).append(gamesSpan);

            // append to events div in index.html
            $('#events').append(newDiv);
        });
    });

    //// EVENT DETAILS ///////////////////////////////////////////////////////////////////////////////////////////
    // Shows event details on click
    var selectedEventId;

    function loadEventDetail() {
        console.log('load');
        console.log(selectedEventId);

        // Removes details of event if present from a previous click
        $('.details-info div').remove();
        $('.event-entrants table').find("tr:gt(0)").remove();

        url = baseUrl + '/events/' + selectedEventId;

        // get event details and display it
         $.get(url, function(data) {
             console.log(data);

            // Event Info div
            // save event info into variables
            var name = 'Name: ' + data.event[0].name;
            var games = 'Games: ' + data.event[0].games;
            var desc = 'Description: ' + data.event[0].description;
            var textDiv = '<div>' + name + '<br/>' + games + '<br/>' + desc + '</div>';

            // create new div for event info
            $('.details-info').append(textDiv);

            // Event entrants div
            // Iterate through entrants, create rows, and append them to table
            data.entrants.forEach(function(entrant, index) {
                var row = document.createElement('tr');
                var present;
                var paid;

                entrant.present === 0 ? present = 'No' : present = 'Yes';
                entrant.paid === 0 ? paid = 'No' : paid = 'Yes';

                $(row).append('<td>' + (index + 1) + '</td>');
                $(row).append('<td>' + entrant.name + '</td>');
                $(row).append('<td>' + present + '</td>');
                $(row).append('<td>' + paid + '</td>');
                $('.event-entrants table').append(row);
            });
         })
         .done(function() {
            // hide events container, show event details when data has loaded
            $('.events-container').hide();
            $('#event-details').show();
         })
         .fail(function() {
             alert('An error has occurred, please try again');
         });
    }

    $('.events-container').on('click', 'div', function(event) {
        event.preventDefault();
        
        // get data-id for url to get event details and entrants
        var id = event.target.getAttribute('data-id');
        selectedEventId = id;

        loadEventDetail()
    });

    // Back button on event-details, sends user back to list of all events
    $('#back-to-events-btn').on('click', function() {
        $('.events-container').show();
        $('#event-details').hide();
    });

    // Register an entrant to an event. Adds event listener to the 'Add' button and sends a post request
    $('#register-form').on('submit', function(event) {
        event.preventDefault();
        var data = { entrant: {} };
        formData = $('#register-form').serializeArray();
        console.log(formData);
        formData.forEach(function(input) {
            var name = input.name
            var value = input.value
            data.entrant[name] = value;
        });

        // POST new entrant, get new entrant's id and save
        var newEntrantId;
        $.ajax({
            url: baseUrl + '/entrants',
            type: 'POST',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify(data),
            success: function(response) {
                console.log('new entry id: ' + response[0].id);
                newEntrantId = response[0].id;
                registerEntrantToEvent();
            }
        });

        // POST to events_entrants to register
        function registerEntrantToEvent() {
            console.log('new entry id outside: ', newEntrantId);

            $.ajax({
                url: baseUrl + '/events_entrants',
                type: 'POST',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    events_entrants: {
                        "event_id": selectedEventId,
                        "entrant_id": newEntrantId
                    }
                }),
                success: function(data) {
                    console.log('worked');
                    console.log(this);   
                }
            }).done(function() {
                console.log('done');
            });

            // Reloads entrants to show new entry
            loadEventDetail();
        }
    });
}())