from odoo import models, fields

class AgencyCircuit(models.Model):
    _name = 'agency.manager.circuit'
    _description = 'Circuits proposés par une agence'

    code = fields.Char(string="Identifiant du circuit", required=True)
    name = fields.Char(string="Nom du circuit", required=True)
    date_debut = fields.Date(string="Date de début", required=True)
    date_fin = fields.Date(string="Date de fin", required=True)
    agency_id = fields.Many2one('agency.manager', string="Agence", required=True)

    _sql_constraints = [
        ('unique_code', 'unique(code)', 'L’identifiant du circuit doit être unique.')
    ]

