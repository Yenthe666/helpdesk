# Helpdesk
Apps related to the Odoo helpdesk app (enterprise)
- [helpdesk_auto_reminder_customer](#helpdesk_auto_reminder_customer): automatically send reminders to customers when tickets are in specific stages and automatically closes tickets if no response

## helpdesk_auto_reminder_customer
Adds support to automatically send reminders to customers when a ticket is in some specific stages.
This module allows you to configure, per helpdesk team:
- After how many days you want to send a reminder to the custmoer
- Which reminder (e-mail template) you'd like to send
- Which stages should auto send a reminder
- When to auto-close a ticket
- To which stage the ticket should move when it was automatically closed

This is all configurable per helpdesk team under Helpdesk > Configuration > Helpdesk Teams:
![image](https://user-images.githubusercontent.com/6352350/134292849-272b2330-28c5-4992-adad-522695d36642.png)

<b>Note:</b> This module will not influence tickets that where created before installing this module. <br/>
You can change this by modifying the `ir.config_parameter` named `helpdesk_ticket_reminder_start_date`.<br/>
By default it will only consider tickets that had a stage change from the day you install it onwards.<br/>
e.g: having a ticket created on 01/09/2021 will not send an automatic reminder until this ticket had a stage change.
