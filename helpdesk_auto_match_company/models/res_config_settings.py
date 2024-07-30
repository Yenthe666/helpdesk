from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    helpdesk_blacklisted_domains = fields.Char(
        string="Helpdesk blacklisted domains",
        config_parameter="helpdesk_auto_match_company.helpdesk_blacklisted_domains",
    )
