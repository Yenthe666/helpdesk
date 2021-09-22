from datetime import timedelta

from odoo import fields
from odoo.tests.common import TransactionCase


class TestHelpdeskTicket(TransactionCase):
    def setUp(self):
        super(TestHelpdeskTicket, self).setUp()
        company = self.env.ref("base.main_partner")
        self.partner = self.env["res.partner"].create(
            {
                "name": "Test Partner",
                "email": "test@customer.com",
                "child_ids": [
                    (0, 0, {"name": "Test Child", "email": "test@child.com"})
                ],
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
        self.helpdesk_team = self.env["helpdesk.team"].create(
            {
                "name": "Test Helpdesk Team",
                "company_id": company.id,
            }
        )
        self.helpdesk_stage1 = self.env["helpdesk.stage"].create(
            {
                "name": "Inprogress",
                "sequence": 1,
                "team_ids": [(6, 0, [self.helpdesk_team.id])],
            }
        )
        self.helpdesk_stage2 = self.env["helpdesk.stage"].create(
            {
                "name": "waiting",
                "sequence": 1,
                "team_ids": [(6, 0, [self.helpdesk_team.id])],
            }
        )
        self.helpdesk_ticket = self.env["helpdesk.ticket"].create(
            {
                "name": "Test Ticket",
                "team_id": self.helpdesk_team.id,
                "partner_id": self.partner.id,
                "stage_id": self.helpdesk_stage1.id,
                "date_last_stage_update": False,
                "last_reminder_sent": False,
                "already_informed": False,
            }
        )
        self.helpdesk_ticket2 = self.env["helpdesk.ticket"].create(
            {
                "name": "Test Ticket1",
                "team_id": self.helpdesk_team.id,
                "partner_id": self.partner1.id,
                "stage_id": self.helpdesk_stage2.id,
                "date_last_stage_update": False,
                "last_reminder_sent": fields.Date.today() + timedelta(days=7),
                "already_informed": True,
            }
        )

    def test_message_post(self):
        self.helpdesk_ticket.message_post(
            email_from=self.helpdesk_ticket.partner_id.email
        )
        self.assertEqual(
            self.helpdesk_ticket.last_reminder_sent,
            False,
            "Helpdesk ticket Last Reminder Sent is set False",
        )
        self.assertEqual(
            self.helpdesk_ticket.already_informed,
            False,
            "Helpdesk ticket Already Inform to Customer is False",
        )

        self.helpdesk_ticket2.message_post(
            email_from=self.helpdesk_ticket2.partner_id.email
        )
        self.assertEqual(
            self.helpdesk_ticket2.last_reminder_sent,
            False,
            "Helpdesk ticket Last Reminder Sent is set today date",
        )
        self.assertEqual(
            self.helpdesk_ticket2.already_informed,
            False,
            "Helpdesk ticket Already Inform to Customer is False",
        )
