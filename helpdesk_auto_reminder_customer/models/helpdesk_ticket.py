from odoo import api, fields, models
from odoo.tools import email_split


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    # Add fields # 386
    already_informed = fields.Boolean(
        string="Customer has been informed", tracking=True, copy=False, readonly=True
    )
    last_reminder_sent = fields.Date(
        string="Last Reminder Sent", tracking=True, copy=False, readonly=True
    )

    @api.returns("mail.message", lambda value: value.id)
    def message_post(
        self,
        body="",
        subject=None,
        message_type="notification",
        email_from=None,
        author_id=None,
        parent_id=False,
        subtype_xmlid=None,
        subtype_id=False,
        partner_ids=None,
        channel_ids=None,
        attachments=None,
        attachment_ids=None,
        add_sign=True,
        record_name=False,
        **kwargs
    ):
        """inherit message_post and if reply from customer then set last_stage_update,
        last_reminder_sent, already_informed # 386"""
        message = super(HelpdeskTicket, self).message_post(
            body=body,
            subject=subject,
            message_type=message_type,
            email_from=email_from,
            author_id=author_id,
            parent_id=parent_id,
            subtype_xmlid=subtype_xmlid,
            subtype_id=subtype_id,
            partner_ids=partner_ids,
            channel_ids=channel_ids,
            attachments=attachments,
            attachment_ids=attachment_ids,
            add_sign=add_sign,
            record_name=record_name,
            **kwargs
        )
        email = self.partner_id.child_ids.mapped("email")
        email.append(self.partner_id.email)
        from_email = (
            email_split(message.email_from)[0]
            if email_split(message.email_from)
            else ""
        )
        if from_email in email:
            self.write(
                {
                    "date_last_stage_update": fields.Datetime.now(),
                    "last_reminder_sent": False
                    if self.last_reminder_sent
                    else self.last_reminder_sent,
                    "already_informed": False
                    if self.already_informed
                    else self.already_informed,
                }
            )
        return message
