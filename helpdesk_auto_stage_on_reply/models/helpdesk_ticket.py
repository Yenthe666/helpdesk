from odoo import api, models
from odoo.tools import email_split


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    @api.returns("mail.message", lambda value: value.id)
    def message_post(
        self,
        **kwargs
    ):
        """
            Inherit the message_post. If the ticket stage is configured
            and the sent message is from the customer email and their related
            email is set the stage_is will be automatically changed.
        """
        message = super(HelpdeskTicket, self).message_post(
            **kwargs
        )
        email = self.partner_id.child_ids.mapped("email")
        if self.partner_id.email:
            email.append(self.partner_id.email)
        if self.partner_email:
            email.append(self.partner_email)
        from_email = (
            email_split(message.email_from)[0]
            if email_split(message.email_from)
            else ""
        )
        if self.stage_id.is_auto_change_ticket_stage and from_email in email:
            self.write(
                {
                    "stage_id": self.stage_id.auto_change_stage_id.id,
                }
            )
        return message
