# Helpdesk
Apps related to the Odoo helpdesk app (enterprise)
- [helpdesk_auto_reminder_customer](#helpdesk_auto_reminder_customer): automatically send reminders to customers when tickets are in specific stages and automatically closes tickets if no response
- [helpdesk_ticket_on_reply](#helpdesk_ticket_on_reply): automatically creates new helpdesk tickets in specific teams based on responses on specific models

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



## helpdesk_ticket_on_reply
Adds support to configure for which models the response of a customer should create a new helpdesk ticket.<br/>
This module allows you to configure, per model, if you want to detect incoming messages from the customer (based on which field) and if you want to create a new helpdesk ticket.<br/>
The idea is to handle responses as tickets which each team has its own strenghts and specialities in. Sample configuration of a model:
<img width="1258" alt="image" src="https://github.com/Yenthe666/helpdesk/assets/6352350/a8aa8bd0-0590-4eec-a66b-4439cde4378c">

Based on the above configuration we would detect if a response email comes from the email of the related partner (through the field "partner_id") and if so we will create a new ticket.<br/>
Per helpdesk team you can then configure for which model(s) it should create tickets in the current team:
<img width="1262" alt="image" src="https://github.com/Yenthe666/helpdesk/assets/6352350/04f55736-a521-43f2-987d-6c1b9ab53426">

When the customer then responds on the original message a new ticket will be created with the content of the email as a body and with a link to the source:
<img width="1272" alt="image" src="https://github.com/Yenthe666/helpdesk/assets/6352350/a6d8d69b-64e5-4b29-8049-eae99ff027a2">
