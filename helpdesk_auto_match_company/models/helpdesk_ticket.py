from odoo import api, models, tools, _


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    def _link_partner_to_company_partner(self, partner_id, email):
        """
        Link the provided partner to a parent  partner based on the domain in the email address.
        This method checks the domain of the provided email against a list of blacklisted domains.
        If the domain is not blacklisted, it searches for a company (partner) with a matching
        website or email domain and links the partner to this company.
        Args:
            partner_id (res.partner): The partner to link to a company.
            email (str): The email address to extract the domain from.
        Returns:
            None
        """
        domain = email.split('@')[-1].strip()
        if domain:

            # Retrieve blacklisted domains
            blacklisted_domains = self.env['ir.config_parameter'].sudo().get_param('helpdesk_auto_match_company.helpdesk_blacklisted_domains')
            blacklisted_domains_lst = blacklisted_domains.split(';') if blacklisted_domains else []

            if domain not in blacklisted_domains_lst:

                # Search for the company based on the website
                parent_partner_id = self.env['res.partner'].sudo().search([
                    ('is_company','=',True),('website', 'ilike', f'%{domain}%'),('id','!=',partner_id.id)
                ], limit=1)
                # If not found, search for the company based on the email domain
                if not parent_partner_id:
                    parent_partner_id = self.env['res.partner'].sudo().search([
                        ('is_company','=',True),('email', 'ilike', f'%@{domain}%'),('id','!=',partner_id.id)
                    ], limit=1)

                # Link the partner to the found company
                if parent_partner_id:
                    partner_id.parent_id = parent_partner_id.id

    @api.model
    def message_new(self, msg, custom_values=None):
        """
        Override the default message_new method to link the ticket's partner to a company based on the partner's email domain.
        This method normalizes the partner's email, calls _link_partner_to_company_partner, and links the partner
        to a company if a matching one is found.
        Returns:
            ticket (helpdesk.ticket): The created helpdesk ticket.
        """
        ticket = super().message_new(msg, custom_values=custom_values)
        if ticket:
            ticket_partner_email = ticket.partner_id.email if ticket.partner_id.email else ticket.partner_email
            partner_email_normalized = tools.email_normalize(ticket_partner_email) or ticket.partner_id.email or False
            if partner_email_normalized:
                self._link_partner_to_company_partner(ticket.partner_id, partner_email_normalized)
        return ticket

