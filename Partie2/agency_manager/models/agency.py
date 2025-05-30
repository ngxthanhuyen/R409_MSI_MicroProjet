from odoo import models, fields

class Agency(models.Model):
    _name = 'agency.manager'
    _description = 'Agences UberCircuit (entreprises individuelles)'

    name = fields.Char(string="Nom de l’agence", required=True)
    siret = fields.Char(string="Numéro SIRET", required=True)
    date_creation = fields.Date(string="Date de création", required=True)
    owner_firstname = fields.Char(string="Prénom du propriétaire", required=True)
    owner_lastname = fields.Char(string="Nom du propriétaire", required=True)
    owner_birthdate = fields.Date(string="Date de naissance du propriétaire", required=True)
    owner_birthplace = fields.Char(string="Lieu de naissance du propriétaire", required=True)
    capital = fields.Float(string="Capital de l’agence", required=True)

    accompagnateurs = fields.Many2many('res.partner', string="Accompagnateurs")
    circuits = fields.One2many('agency.manager.circuit', 'agency_id', string="Circuits")
    accompagnateurs_info = fields.One2many(
        'agency.accompagnateur', 'agency_id', string="Détails des accompagnateurs"
    )

    _sql_constraints = [
        ('unique_siret', 'unique(siret)', 'Le numéro SIRET doit être unique !')
    ]

