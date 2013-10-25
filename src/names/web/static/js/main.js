// Default Query Years
var MAX_YEAR = 2012;
var MIN_YEAR = MAX_YEAR-5;

var start_year = 2012;
var stop_year = 2012;

// Autocomplete for zip field
$("#name_field").autocomplete({
    source: function (request, response) {
        var uri = "/search/" + request.term + "/years/" + start_year + "/" + stop_year;
        $.ajax({
            url:uri,
            dataType:"json",
            success: function(data) {
                response($.map(data, function(count, name) { return {label: name + " " + count, value: name}}) )
            }
        });
    },
    minLength: 2,
    select: function(event, ui) {
        var name = ui.item.value;
        var uri = "/usage/" + name + "/years/" + start_year + "/" + stop_year;
        $.ajax({
            url:uri,
            dataType:"json",
            success: function(data) {
                graph_data(data, name);
            }
        });
    },
    open: function() {
        $( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" );
    },
    close: function() {
        $( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
    }
});

$(function() {
    $( "#slider_year_range" ).slider({
      range: true,
      min: MIN_YEAR,
      max: MAX_YEAR,
      values: [ start_year, stop_year ],
      slide: function( event, ui ) {
        $( "#year_range" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
        start_year = ui.values[0];
        stop_year = ui.values[1];
      }
    });
    $( "#year_range" ).val( $( "#slider_year_range" ).slider( "values", 0 ) +
      " - " + $( "#slider_year_range" ).slider( "values", 1 ) );
  });
