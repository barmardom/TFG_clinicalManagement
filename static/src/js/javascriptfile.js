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

          google.charts.load('current', {'packages':['corechart']});
          google.charts.setOnLoadCallback(drawChart);

        }
        this._super();
      },


  });
});

//google.charts.load('current', {'packages':['corechart']});
 //google.charts.setOnLoadCallback(drawChart);

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
        }
