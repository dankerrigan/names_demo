// Default Query Years
var DEFAULT_YEARS = 1

// Autocomplete for zip field
$("#name_field").autocomplete({
    source: function (request, response) {
        var uri = "/search/" + request.term;
        $.ajax({
            url:"/search/" + request.term,
            dataType:"json",
            success: function(data) {
                response($.map(data, function(count, name) { return {label: name + " " + count, value: name}}) )
            }
        });
    },
    minLength: 2,
    select: function(event, ui) {
        var name = ui.item.value;
        var range = $("#year_range").val();
        console.log(range);
        var years = range.split(' - ');
        var start_year = years[0];
        var stop_year = years[1];
        var uri = "/usage/" + name + "/years/" + (stop_year - start_year);
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
      min: 1950,
      max: 2012,
      values: [ 2002, 2012 ],
      slide: function( event, ui ) {
        $( "#year_range" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
      }
    });
    $( "#year_range" ).val( $( "#slider_year_range" ).slider( "values", 0 ) +
      " - " + $( "#slider_year_range" ).slider( "values", 1 ) );
  });
