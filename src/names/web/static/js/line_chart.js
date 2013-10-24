/**
 * Created by dankerrigan on 10/24/13.
 */


function graph_data(data, name) {
    var males = [];
    var females = [];

    for (year in data) {;
        males.push({x: year, y: data[year].M});
        females.push({x: year, y: data[year].F});
    }

    data = [
        {values:males,
         key: "Male",
         color: "FF0000"},
        {values: females,
        key: "Female",
        color: "0000FF"}
    ];

    nv.addGraph(function() {
    var chart = nv.models.lineChart();

    chart.xAxis
         .axisLabel('Year')
         .tickFormat(d3.format('d'));

    chart.yAxis
         .axisLabel('Count')
         .tickFormat(d3.format('d'));

    d3.select('#data_graph svg')
      .datum(data)
      .transition().duration(500)
      .call(chart);

    nv.utils.windowResize(chart.update);

    return chart;
});

}