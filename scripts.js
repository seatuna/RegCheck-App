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
    // Shows event details on click //////////////////////////////////////////////////////////////////////////////

    // save id of the event that was clicked on
    var selectedEventId;

    // function to load details of selected event
    var loadEventDetail = function() {
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

            // append data retrieved from get to details-info div
            $('.details-info').append(textDiv);

            // Event entrants div
            // Iterate through entrants, create rows, and append them to table
            // When done, hide events-container div and show the event details div
            data.entrants.forEach(function(entrant, index) {
                var row = document.createElement('tr');
                var present;
                var paid;

                // If present or paid is 0, show 'No', else show 'Yes'
                entrant.present === 0 ? present = 'No' : present = 'Yes';
                entrant.paid === 0 ? paid = 'No' : paid = 'Yes';

                // create remove button
                var removeBtn = document.createElement('button');
                var removeBtnTd = document.createElement('td');
                removeBtnTd.className = 'col-md-1';
                removeBtn.id = 'remove-entrant';
                removeBtn.className = 'btn btn-danger';
                removeBtn.innerHTML = 'Remove';
                removeBtn.setAttribute('data-id', entrant.entrant_id);
                $(removeBtnTd).append(removeBtn);

                // create button for marking present or absent
                var presentBtn = document.createElement('button');
                var presentBtnTd = document.createElement('td');
                presentBtnTd.className = 'col-md-1';
                presentBtn.id = 'toggle-present';
                presentBtn.className = 'btn btn-info';
                presentBtn.innerHTML = 'Present';
                presentBtn.setAttribute('data-id', entrant.id);
                presentBtn.setAttribute('paid', entrant.paid);
                presentBtn.setAttribute('present', entrant.present);
                $(presentBtnTd).append(presentBtn);

                // create button for marking paid or not paid
                var paidBtn = document.createElement('button');
                var paidBtnTd = document.createElement('td');
                paidBtnTd.className = 'col-md-1';
                paidBtn.id = 'toggle-paid';
                paidBtn.className = 'btn btn-info';
                paidBtn.innerHTML = 'Paid';
                paidBtn.setAttribute('data-id', entrant.id);
                paidBtn.setAttribute('paid', entrant.paid);
                paidBtn.setAttribute('present', entrant.present);
                $(paidBtnTd).append(paidBtn);

                // Append cells to rows
                $(row).append('<td>' + (index + 1) + '</td>');
                $(row).append('<td>' + entrant.name + '</td>');
                $(row).append('<td>' + present + '</td>');
                $(row).append('<td>' + paid + '</td>');
                $(row).append(removeBtnTd);
                $(row).append(presentBtnTd);
                $(row).append(paidBtnTd);
                $('.event-entrants table').append(row);
            });
         })
         .done(function() {
            // hide events container, show event details when data has loaded
            $('.events-container').hide();
            $('#event-details').show();
         })
         .fail(function() {
             // Show alert in case of error
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
        load = loadEventDetail();

        // POST to events_entrants to register
        function registerEntrantToEvent(entrantId) {
            $.ajax({
                url: baseUrl + '/events_entrants',
                type: 'POST',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify({
                    events_entrants: {
                        "event_id": selectedEventId,
                        "entrant_id": entrantId
                    }
                }),
                complete: function(data) {
                    // clears selectedEntrantId after, so it won't affect the next registrations
                    if(selectedEntrantId) {
                        selectedEntrantId = null;
                    }
                    // Reloads entrants to show new entry
                    loadEventDetail();
                    console.log('Registered!');
                }
            });
        }

        // Register an existing entrant if selected from the typeahead
        if (selectedEntrantId) {
            registerEntrantToEvent(selectedEntrantId);
        } else {
            // create object to send with POST request
            var data = { entrant: {} };
            formData = $('#register-form').serializeArray();

            // Take values from submitted form and put into data object
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
                    // saves id of new entry, to be used for registering the new user to the event
                    newEntrantId = response[0].id;
                    registerEntrantToEvent(newEntrantId);
                }
            });
        }
    });

    // Typeahead for register form
    // Get all entrants from database when clicking on the Name input box
    var names = []; // Array for the suggested names
    var map = {}; // Maps ids to names for POST request to register entrant to an event
    var selectedEntrantId;

    $('#input-entrant-name').on('focus', function() {
        $.get(baseUrl + '/entrants', function(data) {
            data.entrants.forEach(function(entrant) {
                names.push(entrant.name);
                map[entrant.name] = entrant.id;
            })
        });
    });

    // Matches substring, from typeahead.js documentation
    var substringMatcher = function(strings) {
        return function findMatches(q, callback) {
            var matches, substringRegex;

            // an array that will be populated with substring matches
            matches = [];

            // regex used to determine if a string contains the substring `q`
            substrRegex = new RegExp(q, 'i');

            // iterate through the pool of strings and for any string that
            // contains the substring `q`, add it to the `matches` array
            $.each(strings, function(i, string) {
                if (substrRegex.test(string)) {
                    matches.push(string);
                }
            });

            callback(matches);
        };
    };
    
    // Assigns typeahead data to register form
    $('#register-form .typeahead').typeahead({
        hint: true,
        highlight: true,
        minLength: 1
    },
    {
        name: 'names',
        source: substringMatcher(names)
    });

    // Assigns entrant's id to selectedEntrantId when selected from the suggestions menu
    $('.typeahead').bind('typeahead:select', function(event, suggestion) {
        selectedEntrantId = map[suggestion]; 
    });

    // Event handler for the remove button, removes entrant from event when clicking "Remove"
    $('table').on('click', 'button#remove-entrant', function(event) {
        event.preventDefault();
        
        // get data-id for url to get event details and entrants
        var id = event.target.getAttribute('data-id');
        data = {
            "event_id": selectedEventId,
            "entrant_id": id
        };

        $.ajax({
            url: baseUrl + '/events_entrants?' + $.param(data),
            method: 'DELETE',
            complete: function() {
                console.log('deleted!');
                loadEventDetail();
            }
        });
    });

    // Event handler for updating Present / Not Present status
    $('table').on('click', 'button#toggle-present', function(event) {
        event.preventDefault();

        // get data-id for url to get event details and entrants
        var id = event.target.getAttribute('data-id');
        var present;
        var paid = event.target.getAttribute('paid');

        // Assign present and paid value
        event.target.getAttribute('present') == 0 ? present = 1 : present = 0;

        data = { "events_entrants": {
                "events_entrants_id": id,
                "present": present,
                "paid": paid
            }
        };
        
        $.ajax({
            url: baseUrl + '/events_entrants',
            method: 'PATCH',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify(data),
            complete: function() {
                console.log('patched!');
                loadEventDetail();
            }
        })
    });

    // Event handler for updating Present / Not Present status
    $('table').on('click', 'button#toggle-paid', function(event) {
        event.preventDefault();
        
        // get data-id for url to get event details and entrants
        var id = event.target.getAttribute('data-id');
        var present = event.target.getAttribute('present');
        var paid;

        // Assign present and paid value
        event.target.getAttribute('paid') == 0 ? paid = 1 : paid = 0;

        data = { "events_entrants": {
                "events_entrants_id": id,
                "present": present,
                "paid": paid
            }
        };
        
        $.ajax({
            url: baseUrl + '/events_entrants',
            method: 'PATCH',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify(data),
            complete: function() {
                console.log('patched!');
                loadEventDetail();
            }
        })
    });
}())