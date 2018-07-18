document.write('<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>');

odoo.define('gestion_clinica.models', function (require) {    
  "use strict";

  var form_widget = require('web.form_widgets');
  var core = require('web.core');
  var _t = core._t;
  var QWeb = core.qweb;
  
  form_widget.WidgetButton.include({

      on_click: function() {
           if(this.node.attrs.custom === "click"){


      /*google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {

        var data = google.visualization.arrayToDataTable([
          ['Task', 'Hours per Day'],
          ['Work',     11],
          ['Eat',      2],
          ['Commute',  2],
          ['Watch TV', 2],
          ['Sleep',    7]
        ]);

        var options = {
          title: 'My Daily Activities'
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart'));

        chart.draw(data, options);
      }*/
          alert("It works!!");

            return;

           }
           this._super();
      },


  });
});



/*
odoo.define('gestion_clinica.grafico', function (require) {    
  "use strict";
  var Widget = require('web.Widget');
  var core = require('web.core');
  var Model = require('web.Model');
  var QWeb = core.qweb;
  var _t = core._t;

  // here we are getting the value in an array.
  var widget_name = Widget.extend({
    tagName: 'div',
    id: 'something',
    className: null,
    attributes: {},
    events: {},

    init: function(parent) {
      alert("it works!!");
      //document.getElementById("demo2").innerHTML = "Hello World";
    },
    start: function() {
      alert("it works2!!");
      //document.getElementById("demo2").innerHTML = "Hello World";
    }
  });
  return widget_name;
});

*/



