from datetime import timedelta

from odoo import api, fields, models


class HelpdeskTeam(models.Model):
    _inherit = "helpdesk.team"

    # add new fields
    send_reminder_after = fields.Integer(string="Send Reminder After", copy=False)
    reminder_template_id = fields.Many2one(
        "mail.template",
        string="Reminder Template",
        default=lambda self: self.env.ref(
            "helpdesk_auto_reminder_customer.email_template_send_reminer_customer",
            raise_if_not_found=False,
        ),
        ondelete="cascade",
        copy=False,
    )
    check_stage_ids = fields.Many2many(
        "helpdesk.stage",
        "heldesk_team_stage_rel",
        "helpdesk_team_id",
        "helpdesk_stage_id",
        string="Stage(s) to check for answer",
    )
    days_before_auto_closure = fields.Integer(
        string="Days before auto-closure", copy=False
    )
    close_stage_id = fields.Many2one(
        "helpdesk.stage", string="Closing Stage", copy=False, ondelete="cascade"
    )

    @api.model
    def _cron_auto_reminder_to_customer(self):
        """If no answer on ticket from customer in given send_reminder_after field
        then we Send reminder after to customer"""
        teams = self.search(
            [
                ("send_reminder_after", "!=", 0),
                ("check_stage_ids", "!=", False),
                ("reminder_template_id", "!=", False),
            ]
        )
        reminder_start_date = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(
                "helpdesk_auto_reminder_customer.helpdesk_ticket_reminder_start_date"
            )
        )
        reminder_start_date = fields.Date.from_string(reminder_start_date)

        for team in teams:
            calculated_date = fields.Date.today() - timedelta(
                days=team.send_reminder_after
            )
            tickets = self.env["helpdesk.ticket"].search(
                [
                    ("date_last_stage_update", "<=", calculated_date),
                    ("date_last_stage_update", ">", reminder_start_date),
                    ("stage_id", "in", team.check_stage_ids.ids),
                    ("already_informed", "=", False),
                    ("team_id", "=", team.id),
                ]
            )
            for ticket in tickets:
                ticket.message_post_with_template(team.reminder_template_id.id)
                ticket.write(
                    {
                        "last_reminder_sent": fields.Date.today(),
                        "already_informed": True,
                    }
                )

    @api.model
    def _cron_auto_close_stage(self):
        """if no answer from customer in reminder mail then
        automatic close ticket and set closing stage given in helpdesk team"""
        teams = self.search(
            [
                ("days_before_auto_closure", "!=", 0),
                ("check_stage_ids", "!=", False),
                ("close_stage_id", "!=", False),
            ]
        )
        for team in teams:
            calculated_date = fields.Date.today() - timedelta(
                days=team.days_before_auto_closure
            )
            tickets = self.env["helpdesk.ticket"].search(
                [
                    ("last_reminder_sent", "<=", calculated_date),
                    ("stage_id", "in", team.check_stage_ids.ids),
                    ("team_id", "=", team.id),
                    ("already_informed", "=", True),
                ]
            )
            for ticket in tickets:
                ticket.write(
                    {"stage_id": team.close_stage_id.id, "already_informed": False}
                )
