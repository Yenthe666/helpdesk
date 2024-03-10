from odoo import api, fields, models


class IrModel(models.Model):
    _inherit = "ir.model"

    create_helpdesk_ticket_on_message = fields.Boolean(
        string="Create new Helpdesk Ticket?",
        help="Enable to create new Helpdesk Ticket on customer's reply",
        copy=False,
    )

    # we choose a text field on purpose to not have more relations from ir.model to other fields
    partner_field_name = fields.Char(
        string='Partner Field',
        help="Enter the relation field name of res.partner to check for valid email",
        copy=False
    )
