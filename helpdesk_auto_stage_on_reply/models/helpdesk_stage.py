from odoo import fields, models


class HelpdeskStage(models.Model):
    _inherit = "helpdesk.stage"

    is_auto_change_ticket_stage = fields.Boolean(
        string="Auto Change Ticket Stage",
        copy=False
    )

    auto_change_stage_id = fields.Many2one(
        "helpdesk.stage",
        string="Auto Change Stage",
        copy=False,
        ondelete="set null",
    )
