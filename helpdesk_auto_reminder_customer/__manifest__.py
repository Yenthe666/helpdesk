{
    "name": "Helpdesk Auto Reminder to Customer",
    "version": "14.0.0.0.1",
    "category": "Helpdesk",
    "depends": ["helpdesk"],
    "author": "Mainframe Monkey BV",
    "license": "LGPL-3",
    "website": "https://www.mainframemonkey.com",
    "data": [
        "data/customer_reminder_mail_template.xml",
        "data/ir_cron_customer_reminder.xml",
        "data/config_parameter_data.xml",
        "views/helpdesk_team_view.xml",
    ],
    "maintainers": ["bizzappdev"],
    "installable": True,
    "application": False,
}
