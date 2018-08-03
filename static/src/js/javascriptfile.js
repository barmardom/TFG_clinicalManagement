//document.write('<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>');
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

  var totalMujeres = "-";
  var totalHombres = "-";
  var totalDonantes = "-";
  var totalNoDonantes = "-";
  var medicamentosMasRecetados = [];
  var pacientesAdultos0; //Menores
  var pacientesAdultos1; //Adultez temprana
  var pacientesAdultos2; //Adultez media
  var pacientesAdultos3; //Adultez tardia
  var control = 0;



  form_widget.WidgetButton.include({
      on_click: function() {
        //##################################################### RECOPILAR DATOS
        if(this.node.attrs.custom === "cargaDatos"){
          console.log(control);
          cargador_pacientes();
          cargador_medicamentos();
          control = 1;
              
        }
        //##################################################### CARGAR DATOS
        if(this.node.attrs.custom === "click"){

           if(control === 1){

             inserta_datosNumericos();

             if(totalMujeres > 0 || totalHombres > 0) {
              drawChart_pacienteTotales(totalMujeres, totalHombres);
             }
             if(totalDonantes > 0 || totalNoDonantes > 0){
              drawChart_pacienteDonantes(totalDonantes, totalNoDonantes);
             }
             if(pacientesAdultos0 > 0 || pacientesAdultos1 > 0 || pacientesAdultos2 > 0 || pacientesAdultos3 > 0){
              drawChart_pacientesPorEdad(pacientesAdultos0, pacientesAdultos1, pacientesAdultos2, pacientesAdultos3);
             }

             if(medicamentosMasRecetados.length >= 5){
              document.getElementById("masRecetado").innerHTML = String(medicamentosMasRecetados[0][0] + " - " + medicamentosMasRecetados[0][3]);
              drawChart_medicamentosTratamiento(medicamentosMasRecetados[0], medicamentosMasRecetados[1], medicamentosMasRecetados[2], medicamentosMasRecetados[3], medicamentosMasRecetados[4]);
              document.getElementById('textoControl_medicamentos').style.display = 'none';
             }else if((medicamentosMasRecetados.length < 5) && (medicamentosMasRecetados.length >= 1)){
              document.getElementById("masRecetado").innerHTML = String(medicamentosMasRecetados[0][0] + " - " + medicamentosMasRecetados[0][3]);
              document.getElementById('textoControl_medicamentos').innerHTML = "No hay elementos suficientes para mostrar el gráfico.";
             }else{
              document.getElementById('textoControl_medicamentos').innerHTML = "No hay elementos suficientes para mostrar datos.";
              document.getElementById('tablaAlmacenaID').style.display = 'none';
             }
             
             oculta_muestra();

           }else{
              document.getElementById('textoControl_pacientes').innerHTML = 'Recopile los dantos antes de mostrarlos por favor';
              document.getElementById('textoControl_medicamentos').innerHTML = 'Recopile los dantos antes de mostrarlos por favor';

           }
        }
        this._super();
      },
  });


function oculta_muestra(){


  document.getElementById('textoControl_pacientes').style.display = 'none';
 
  document.getElementById('ocultar_pacientes').style.display = '';
  document.getElementById('ocultar_medicamentos').style.display = '';

  

}



function inserta_datosNumericos(){

  document.getElementById("total_hombres").innerHTML = String(totalHombres);
  document.getElementById("total_mujeres").innerHTML = String(totalMujeres);
  document.getElementById("total_donantes").innerHTML = String(totalDonantes);
  document.getElementById("total_pacientes").innerHTML = totalHombres + totalMujeres

  

}

function cargador_pacientes(){

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
      }
    });

}

function cargador_medicamentos(){

  Medicamentos.query(['codigo', 'totalDosis', 'nombre'])
    .all().then(function (res) {
      var i;
      var temp;
      medicamentosMasRecetados = []

      for(i in res){
        temp = []
        temp.push(res[i].codigo);
        temp.push(res[i].totalDosis);
        temp.push(res[i].eficaciaMedia);
        temp.push(res[i].nombre);

        medicamentosMasRecetados.push(temp);
      }
    
      medicamentosMasRecetados.sort(Comparator);
      medicamentosMasRecetados.reverse();

    });

}


});



//######################################################################


function desactiva(){
  var boton = document.getElementById("botonclick");
  boton.disabled=true;
}

  function activa(){
  var boton = document.getElementById("botonclick");
  boton.disabled=true;
}


function Comparator(a, b) {
   if (a[1] < b[1]) return -1;
   if (a[1] > b[1]) return 1;
   return 0;
 }


function calcularEdad(fecha) {
    var hoy = new Date();
    var cumpleanos = new Date(fecha);
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
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)'
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
            'rgba(77,125,190, 1)',
            'rgba(148,183,79, 1)'
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
            'rgba(241, 148, 138, 0.5)',
            'rgba(26, 188, 156, 0.5)',
            'rgba(243, 156, 18, 0.5)',
            'rgb(155, 89, 182, 0.5)'
          ],
          borderColor: [
            'rgba(241, 148, 138, 1)',
            'rgba(26, 188, 156, 1)',
            'rgba(243, 156, 18, 1)',
            'rgb(155, 89, 182, 1)'
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
        labels: [primero[0], segunto[0], tercero[0], cuarto[0], quinto[0]],
        datasets: [{
            label: 'Medicamento más recetado',
            data: [primero[1], segunto[1], tercero[1], cuarto[1], quinto[1]],
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