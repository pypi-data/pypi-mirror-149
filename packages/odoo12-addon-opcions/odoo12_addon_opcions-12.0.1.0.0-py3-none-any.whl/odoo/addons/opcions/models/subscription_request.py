from odoo import fields, models

class SubscriptionRequest(models.Model):

    _inherit = ["subscription.request"]
    
    ref = fields.Char(string='Internal Reference', index=True)
    id_relation = fields.Char(string='Relation ID', index=True)
    
    def get_partner_vals(self):
        partner_vals = super().get_partner_vals()
        partner_vals['ref'] = self.ref
        partner_vals['id_relation'] = self.id_relation
        return partner_vals

    def _get_partner_domain(self):
        if self.email:
            return [("email", "=", self.email)]
        else:
            return None
