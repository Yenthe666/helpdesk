# from odoo.addons.test_mail.tests.common import TestMailCommon
from odoo.tests.common import TransactionCase


class TestHelpdeskTicket(TransactionCase):
    def setUp(self):
        super(TestHelpdeskTicket, self).setUp()
        company = self.env["res.company"].create({"name": "Test Company"})
        self.partner = self.env["res.partner"].create(
            {
                "name": "Test Partner",
                "email": "test@customer.com",
                "child_ids": [
                    (0, 0, {"name": "Test Child", "email": "test@child.com"})
                ],
            }
        )
        self.internal_partner = self.env["res.partner"].create(
            {
                "name": "Test Internal Partner",
                "email": "test@internalpartner.com",
            }
        )
        self.helpdesk_team = self.env["helpdesk.team"].create(
            {
                "name": "Test Helpdesk Team",
                "company_id": company.id,
            }
        )
        self.helpdesk_stage = self.env["helpdesk.stage"].create(
            {
                "name": "New",
                "sequence": 1,
                "team_ids": [(6, 0, [self.helpdesk_team.id])],
                "is_auto_change_ticket_stage": False,
            }
        )
        self.helpdesk_stage1 = self.env["helpdesk.stage"].create(
            {
                "name": "Inprogress",
                "sequence": 1,
                "team_ids": [(6, 0, [self.helpdesk_team.id])],
                "is_auto_change_ticket_stage": True,
                "auto_change_stage_id": self.helpdesk_stage.id,
            }
        )
        self.helpdesk_stage2 = self.env["helpdesk.stage"].create(
            {
                "name": "waiting",
                "sequence": 1,
                "team_ids": [(6, 0, [self.helpdesk_team.id])],
                "is_auto_change_ticket_stage": False,
            }
        )
        self.helpdesk_ticket = self.env["helpdesk.ticket"].create(
            {
                "name": "Test Ticket",
                "team_id": self.helpdesk_team.id,
                "partner_id": self.partner.id,
                "stage_id": self.helpdesk_stage1.id,
            }
        )
        self.partner_emp = self.env["res.partner"].create(
            {
                "name": "Test Partner",
                "email": "test@employee.com",
                "child_ids": [
                    (0, 0, {"name": "Test Child", "email": "test@child.com"})
                ],
            }
        )
        self.employee = self.env["hr.employee"].create(
            {"name": "Test Employee", "work_email": "test@employee.com"}
        )
        self.employee1 = self.env["hr.employee"].create(
            {"name": "Test Employee1", "work_email": "test@employeeemail.com"}
        )
        self.helpdesk_ticket_emp = self.env["helpdesk.ticket"].create(
            {
                "name": "Test Ticket Employee",
                "team_id": self.helpdesk_team.id,
                "partner_id": self.partner_emp.id,
                "stage_id": self.helpdesk_stage1.id,
            }
        )

    def test_message_post(self):
        # set stage_id Inprogress for customer
        self.helpdesk_ticket.message_post(
            email_from=self.helpdesk_ticket.partner_id.email
        )
        self.assertEqual(
            self.helpdesk_ticket.stage_id.name,
            "New",
            "Helpdesk ticket stage should not be changed",
        )

        # set stage_id waiting for customer
        self.helpdesk_ticket.stage_id = self.helpdesk_stage2.id
        self.helpdesk_ticket.message_post(email_from=self.internal_partner.email)
        self.assertEqual(
            self.helpdesk_ticket.stage_id.name,
            "waiting",
            "Helpdesk ticket stage is changed",
        )

        # set stage_id Inprogress for employee
        self.helpdesk_ticket_emp.message_post(email_from=self.employee.work_email)
        self.assertEqual(
            self.helpdesk_ticket_emp.stage_id.name,
            "New",
            "Helpdesk ticket stage should not be changed",
        )

        # set stage_id waiting for employee
        self.helpdesk_ticket_emp.stage_id = self.helpdesk_stage2.id
        self.helpdesk_ticket_emp.message_post(email_from=self.employee1.work_email)
        self.assertEqual(
            self.helpdesk_ticket_emp.stage_id.name,
            "waiting",
            "Helpdesk ticket stage is changed",
        )
