from odoo import fields, models

class ResPartner(models.Model):

    _inherit = ["res.partner"]
    id_relation = fields.Char(string='Relation ID', index=True)


