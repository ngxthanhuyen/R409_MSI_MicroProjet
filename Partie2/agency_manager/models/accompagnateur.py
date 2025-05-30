from odoo import models, fields

class AgencyAccompagnateur(models.Model):
    _name = 'agency.accompagnateur'
    _description = "Accompagnateurs avec détails personnalisés"

    agency_id = fields.Many2one('agency.manager', string="Agence", required=True)
    partner_id = fields.Many2one('res.partner', string="Partenaire", required=True)

    skills = fields.Char(string="Compétences")
    availability = fields.Text(string="Disponibilités")
    hourly_rate = fields.Float(string="Tarif horaire (€)")

