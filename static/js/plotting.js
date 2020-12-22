/*
   Will plot the datetime on x and discharge_time on y.

   Inputs:
      * graph_data <json> => The graph data with x = 'datetime', 
                                                 y = 'discharge_time_{plant_name}'
                                                 err = 'discharge_time_{plant_name}_err'
      * divName <str>     => The name of the div to plot the graph on
      * plant_name <str>  => The name of the plant in the data
*/
function plot_moisture_data(graph_data, divName, plant_name) {
   var x = graph_data['datetime'];
   var y = graph_data['discharge_time_'+plant_name];
   var err = graph_data['discharge_time_'+plant_name+'_err'];
   
   var ylow = []; 
   for (var i=0; i<y.length; i++) {ylow.push(y[i] - err[i]);}
   var yhigh = [];
   for (var i=0; i<y.length; i++) {yhigh.push(y[i] + err[i]);}
   
   dataH = {x: x,
            y: yhigh,
            type: "scatter",
            name: "Ivy Data",
            fill: "tonexty",
            mode: "lines", 
            line: {color: "transparent"},
            fillcolor: "rgba(0, 176, 246, 0.2)",
            showlegend: false
           };
   data =  {x: x,
            y: y,
            type: "scatter",
            name: "Ivy Data",
            mode: "lines",
            fill: "tonexty",
            line: {color: "rgb(0,176,246)"},
            fillcolor: "rgba(0, 176, 246, 0.2)",
            showlegend: false};
   dataL = {x: x, 
            y: ylow,
            type: "Scatter",
            name: "Ivy Data",
            mode: "lines",
            line: {color: "transparent"},
            showlegend: false
           };
   
   var layout = {
                  xaxis: {'title': "Datetime"},
                  yaxis: {'title': "Discharge Time [s]"},
                 };
   
   var config = {responsive: true}

   Plotly.newPlot(divName, [dataL, data, dataH], layout, config);
};
