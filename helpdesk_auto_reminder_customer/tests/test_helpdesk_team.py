from datetime import timedelta

from odoo import fields
from odoo.tests.common import TransactionCase


class TestHelpdeskTeam(TransactionCase):
    def setUp(self):
        super(TestHelpdeskTeam, self).setUp()

        self.main_company = self.env.ref("base.main_company")
        reminder_template = self.env.ref(
            "helpdesk_auto_reminder_customer.email_template_send_reminer_customer"
        )
        self.helpdesk_team = self.env["helpdesk.team"]
        self.helpdesk_stage3 = self.env["helpdesk.stage"].create(
            {
                "name": "cancel",
                "sequence": 2,
            }
        )
        self.helpdesk_stage2 = self.env["helpdesk.stage"].create(
            {
                "name": "waiting",
                "sequence": 3,
            }
        )
        self.helpdesk_team1 = self.helpdesk_team.create(
            {
                "name": "helpdesk team 0",
                "company_id": self.main_company.id,
                "send_reminder_after": 10,
                "reminder_template_id": reminder_template.id,
                "check_stage_ids": [(6, 0, [self.helpdesk_stage2.id])],
                "days_before_auto_closure": 2,
                "close_stage_id": self.helpdesk_stage3.id,
            }
        )

        self.partner1 = self.env["res.partner"].create(
            {
                "name": "Test Partner1",
                "email": "test@customer1.com",
                "child_ids": [
                    (0, 0, {"name": "Test Child1", "email": "test@child1.com"})
                ],
            }
        )

        self.helpdesk_ticket2 = self.env["helpdesk.ticket"].create(
            {
                "name": "Test Ticket1",
                "team_id": self.helpdesk_team1.id,
                "partner_id": self.partner1.id,
                "stage_id": self.helpdesk_stage2.id,
                "last_reminder_sent": fields.Date.today() - timedelta(days=2),
                "already_informed": False,
            }
        )

    def test_cron_auto_reminder_to_customer(self):
        self.helpdesk_ticket2.write(
            {"date_last_stage_update": fields.Date.today() - timedelta(days=10)}
        )
        self.helpdesk_team._cron_auto_reminder_to_customer()
        self.assertEqual(
            self.helpdesk_ticket2.last_reminder_sent,
            fields.Date.today(),
            "Helpdesk ticket Last Reminder Sent is set today date",
        )
        self.assertEqual(
            self.helpdesk_ticket2.already_informed,
            True,
            "Helpdesk ticket Already Inform to Customer is True",
        )

    def test_cron_auto_close_stage(self):
        self.helpdesk_ticket2.write({"already_informed": True})
        self.helpdesk_team._cron_auto_close_stage()
        self.assertEqual(
            self.helpdesk_ticket2.stage_id.name,
            "cancel",
            "Helpdesk ticket Stage is set",
        )
