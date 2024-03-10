from odoo import models, fields


class HelpdeskTeam(models.Model):
    _inherit = 'helpdesk.team'

    email_model_ids = fields.Many2many(
        'ir.model',
        string="Models",
        help="The models filled in here will be tracked to create new tickets from."
        "If we get an incoming reply into Odoo for one of these models and it is coming from the customer it will"
        "automatically create a new helpdesk ticket."
    )
