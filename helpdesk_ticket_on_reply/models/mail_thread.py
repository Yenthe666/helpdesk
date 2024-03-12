# -*- coding: utf-8 -*-
from odoo import api, models, _
from odoo.tools import email_split


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    def _get_new_helpdesk_ticket_vals(self, message):
        """
        Values for new helpdesk ticket
        """
        res_model_id = self.env['ir.model']._get_id(self._name)
        default_helpdesk_team = self.env['helpdesk.team'].search([('email_model_ids', 'in', [res_model_id])], limit=1)
        helpdesk_ticket_vals = {
            "name": _("Customer reply on %s" % message.record_name),
            "description": message.body,
        }
        if default_helpdesk_team:
            helpdesk_ticket_vals.update({'team_id': default_helpdesk_team.id})
        return helpdesk_ticket_vals

    def _create_new_helpdesk_ticket(self, res_model, message):
        """
        Create new helpdesk ticket
        """
        body = _('This ticket has been generated from %s: <a href=# data-oe-model=%s ' \
                'data-oe-id=%d>%s</a>' % (res_model.name, self._name, message.res_id, message.record_name))
        helpdesk_ticket_vals = self._get_new_helpdesk_ticket_vals(message)
        helpdesk_ticket = self.env['helpdesk.ticket'].create(helpdesk_ticket_vals)
        helpdesk_ticket.message_post(body=body)

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        """
        Create new helpdesk ticket based on model
        """
        message = super(MailThread, self).message_post(**kwargs)
        res_model_id = self.env['ir.model']._get_id(self._name)
        res_model = self.env['ir.model'].sudo().browse(res_model_id)
        original_record = self.env[self._name].sudo().browse(message.res_id)
        # Check for partner_field_name from model and email of author
        partner_field = res_model.partner_field_name or 'partner_id'
        if hasattr(original_record, partner_field):
            email = original_record.partner_id.child_ids.mapped("email")
            if original_record.partner_id.email:
                email.append(original_record.partner_id.email)
            from_email = (
                email_split(message.email_from)[0]
                if email_split(message.email_from)
                else ""
            )
            if res_model.create_helpdesk_ticket_on_message and message.message_type != 'notification' and message.message_type != "comment" and \
                    (from_email in email or (message.author_id and message.author_id.email in email)):
                self.sudo()._create_new_helpdesk_ticket(res_model, message)
        return message
