//document.write('<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>');
//document.write('<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/chart.js@2.7.2/dist/Chart.bundle.min.js"></script>');
//document.write('<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/chart.js@2.7.2/dist/Chart.min.js"></script>');
//document.write('<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/chart.js@2.7.2/src/chart.min.js"></script>');
document.write('<script type="text/javascript" src="/gestion_clinica/static/src/js/Chart.bundle.min.js"></script>');
document.write('<script type="text/javascript" src="/gestion_clinica/static/src/js/Chart.bundle.js"></script>');
document.write('<script type="text/javascript" src="/gestion_clinica/static/src/js/Chart.min.js"></script>');
document.write('<script type="text/javascript" src="/gestion_clinica/static/src/js/Chart.js"></script>');

odoo.define('gestion_clinica.models', function (require) {    
  "use strict";

  
  var form_widget = require('web.form_widgets');
  var core = require('web.core');
  var _t = core._t;
  var QWeb = core.qweb;
  var Model = require('web.Model');
  //MODELOS
  var Pacientes = new Model('gestion_clinica.paciente');
  var Medicamentos = new Model('gestion_clinica.medicamento');

  //VARIABLES

  var totalMujeres;
  var totalHombres;
  var totalDonantes;
  var totalNoDonantes;
  var listaMedicamentosDosis = [];
  var pacientesAdultos0; //Menores
  var pacientesAdultos1; //Adultez temprana
  var pacientesAdultos2; //Adultez media
  var pacientesAdultos3; //Adultez tardia


  form_widget.WidgetButton.include({
      on_click: function() {
        //##################################################### RECOPILAR DATOS
        if(this.node.attrs.custom === "cargaDatos"){

          Pacientes.query(['nif','genero'])
            .filter([['genero', '=', 'femenino']])
            .all().then(function (res) {
              totalMujeres = res.length;
            });

          Pacientes.query(['nif','genero'])
            .filter([['genero', '=', 'masculino']])
            .all().then(function (res) {
              totalHombres = res.length;
            });
          Pacientes.query(['nif','donante'])
            .filter([['donante', '=', true]])
            .all().then(function (res) {
              totalDonantes = res.length;
            });
          Pacientes.query(['nif','donante'])
            .filter([['donante', '=', false]])
            .all().then(function (res) {
              totalNoDonantes = res.length;
            });
          
          Pacientes.query(['nif','fechaNacimiento'])
            .all().then(function (res) {
              var edad;
              pacientesAdultos0 = 0;
              pacientesAdultos1 = 0;
              pacientesAdultos2 = 0;
              pacientesAdultos3 = 0;
              var i;
              
              for (i in res) {
                edad = calcularEdad(res[i].fechaNacimiento);
                if (edad < 18){
                  pacientesAdultos0 = pacientesAdultos0 + 1;
                }else if(edad > 18 && edad <30){
                  pacientesAdultos1 = pacientesAdultos1 + 1;
                }else if(edad > 30 && edad <65){
                  pacientesAdultos2 = pacientesAdultos2 + 1;
                }else if(edad > 65){
                  pacientesAdultos3 = pacientesAdultos3 + 1;
                }
                console.log(edad);
              }

              console.log(pacientesAdultos0);
              console.log(pacientesAdultos1);
              console.log(pacientesAdultos2);
              console.log(pacientesAdultos3);
            });

            Medicamentos.query(['codigo', 'totalDosis'])
            .all().then(function (res) {
              var i;
              listaMedicamentosDosis = []

              for(i in res){
                listaMedicamentosDosis.push(res[i].totalDosis);
              }
            
              listaMedicamentosDosis.sort(function(a, b) {
                return a - b;
              });
              listaMedicamentosDosis.reverse();
            });
        }
        //##################################################### CARGAR DATOS
        if(this.node.attrs.custom === "click"){


           drawChart_pacienteTotales(totalMujeres, totalHombres);
           drawChart_pacienteDonantes(totalDonantes, totalNoDonantes);
           drawChart_pacientesPorEdad(pacientesAdultos0, pacientesAdultos1, pacientesAdultos2, pacientesAdultos3);
           drawChart_medicamentosTratamiento(listaMedicamentosDosis[0], listaMedicamentosDosis[1], listaMedicamentosDosis[2], listaMedicamentosDosis[3], listaMedicamentosDosis[4]);


        }
        this._super();
      },


  });
});


function calcularEdad(fecha) {
    var hoy = new Date();
    var cumpleanos = new Date(fecha);
    //console.log(fecha);
    //console.log(cumpleanos);
    var edad = hoy.getFullYear() - cumpleanos.getFullYear();
    var m = hoy.getMonth() - cumpleanos.getMonth();

    if (m < 0 || (m === 0 && hoy.getDate() < cumpleanos.getDate())) {
        edad--;
    }

    return edad;
}

function comparar(a, b){ 
  return a - b; 
}

function drawChart_pacienteTotales(totalMujeres, totalHombres) {

  var ctx = document.getElementById("pacienteTotales").getContext('2d');
  var myChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        datasets: [{
          data: [
            totalMujeres,
            totalHombres
          ],
          backgroundColor: [
            'rgba(255, 99, 132, 0.5)',
            'rgba(54, 162, 235, 0.5)'
          ],
          borderColor: [
            'rgba(255, 99, 132, 0.5)',
            'rgba(54, 162, 235, 0.5)'
            ],
          label: 'Dataset 1'
        }],
        labels: [
          'Mujeres',
          'Hombres'
        ]
      },
      options: {
        responsive: true,
        title: {
            display: true,
            text: 'Pacientes por sexo',
            fontSize: 14
        },
        legend: {
          display: true,
          position: 'bottom'
        }
 
        //animation: {
        //  animateRotate: false,
        //  animateScale: true
        //}
      }
  });
}


function drawChart_pacienteDonantes(totalDonantes, totalNoDonantes) {

  var ctx = document.getElementById("pacientesDonantes").getContext('2d');
  var myChart2 = new Chart(ctx, {
      type: 'doughnut',
      data: {
        datasets: [{
          data: [
            totalDonantes,
            totalNoDonantes
          ],
          backgroundColor: [
            'rgba(77,125,190, 0.5)',
            'rgba(148,183,79, 0.5)'
          ],
          borderColor: [
            'rgba(77,125,190, 0.5)',
            'rgba(148,183,79, 0.5)'
            ],
          label: 'Dataset 1'
        }],
        labels: [
          'Donantes',
          'No Donantes'
        ]
      },
      options: {
        responsive: true,
        title: {
            display: true,
            text: 'Pacientes donantes',
            fontSize: 14
        },
        legend: {
          display: true,
          position: 'bottom'
        }
        //animation: {
        //  animateRotate: false,
        //  animateScale: true
        //}
      }
  });
}


function drawChart_pacientesPorEdad(pacientesAdultos0, pacientesAdultos1, pacientesAdultos2, pacientesAdultos3) {

  var ctx = document.getElementById("pacientesPorEdad").getContext('2d');
  var myChart3 = new Chart(ctx, {
      type: 'doughnut',
      data: {
        datasets: [{
          data: [
            pacientesAdultos0,
            pacientesAdultos1,
            pacientesAdultos2,
            pacientesAdultos3
          ],
          backgroundColor: [
            'rgba(77,125,190, 0.5)',
            'rgba(148,183,79, 0.5)',
            'rgba(255, 206, 86, 0.5)',
            'rgb(114, 255, 102, 0.5)'
          ],
          label: 'Dataset 1'
        }],
        labels: [
          'Menos de 18',
          'Entre 18 y 30',
          'Entre 30 y 65',
          'Más de 65'
        ]
      },
      options: {
        responsive: true,
        title: {
            display: true,
            text: 'Rango de edades',
            fontSize: 14
        },
        legend: {
          display: true,
          position: 'bottom'
        }
        //animation: {
        //  animateRotate: false,
        //  animateScale: true
        //}
      }
  });

}


function drawChart_medicamentosTratamiento(primero, segunto, tercero, cuarto, quinto) {

  var ctx = document.getElementById("medicamentosTratamiento");
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
        datasets: [{
            label: 'Medicamentos más recetados',
            data: [primero, segunto, tercero, cuarto, quinto],
            backgroundColor: [
                'rgba(255, 99, 132, 0.5)',
                'rgba(54, 162, 235, 0.5)',
                'rgba(255, 206, 86, 0.5)',
                'rgba(75, 192, 192, 0.5)',
                'rgba(153, 102, 255, 0.5)'
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});
}