from openerp.tests import common
from datetime import timedelta
import datetime

@common.post_install(True)
class TestTodo(TransactionCase):

    def test_calcula_eficacia(self):
        self.medicamento = self.env['gestion_clinica.medicamento'].search([('codigo' = '614537')], limit=1)
        self.assertEqual(self.medicamento.eficaciaMedia, 10)

    def test_calcula_dosis_puntuadas(self):
        self.medicamento = self.env['gestion_clinica.medicamento'].search([('codigo' = '614537')], limit=1)
        self.assertEqual(self.medicamento.dosisPuntuadas, 2)

    def test_totalDosis(self):
        self.medicamento = self.env['gestion_clinica.medicamento'].search([('codigo' = '614537')], limit=1)
        self.assertEqual(self.medicamento.totalDosis, 2)

    def test_get_fecha_fin(self):
        self.dosis = self.env['gestion_clinica.dosis'].search([('id' = 23)], limit=1)

        fI = datetime.datetime.strptime(self.dosis.fechaInicio, '%Y-%m-%d')
        fF = fI + datetime.timedelta(self.dosis.duraccion)

        self.assertEqual(self.dosis.fechaFin, fF)