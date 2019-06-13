# -*- coding: utf-8 -*-
from datetime import datetime

from django.conf import settings
from zdesk import Zendesk, get_id_from_url

from clients.pipedrive_client import send


class ZendeskClient:
    HIGH_PRIORITY = ['Funds Withdrawal',
                     'Deposit',
                     'Security',
                     'Authentication',
                     'Application Performance',
                     'API issue',
                     'Trading']

    def __init__(self):
        config = {
            'zdesk_email': settings.ZENDESK_EMAIL,
            'zdesk_password': settings.ZENDESK_TOKEN,
            'zdesk_url': settings.ZENDESK_URL,
            'zdesk_token': True
            }
        self.zendesk_client = Zendesk(**config)

    def create_user(self, email):
        user_id = None
        user = next(iter(self.zendesk_client.users_search(query=email)["users"]), None)

        if user:
            user_id = user["id"]
        else:
            new_user = {
                'user': {
                    'name': email,
                    'email': email
                    }
                }
            user = self.zendesk_client.user_create(data=new_user)

            user_id = get_id_from_url(user)

        return user_id

    def create_issue(self, type, body, email, files=[]):

        # send notification to telegram
        msg1 = 'Request type: {} \n Email: {} \n Message: {} \n Priority: {}'.format(type, body, email, 'high' if type in self.HIGH_PRIORITY else 'normal')

        msg = "Support form from about.exrates.me \n  \n  \n {} \n {}".format(msg1, datetime.now().strftime("%Y-%m-%d %H:%M"))
        send(msg, settings.TELEGRAMBOT_CHAT_SUPPORT)



        user_id = self.create_user(email)

        files_list = []

        for file in files:

            fname = '{}, {}'.format(type, email)

            fdata = file.read()

            import magic
            mime_type = magic.from_buffer(fdata, mime=True)

            upload_result = self.zendesk_client.upload_create(
                    fdata, filename=fname, mime_type=mime_type, complete_response=True)
            files_list.append(upload_result['content']['upload']['token'])

        new_ticket = {
            'ticket': {
                'requester_id': user_id,
                'requester_email': email,
                'subject': type,
                "comment": {
                    "body": "{} \n \n from Exrates support site form".format(body)
                    }
                },
            'uploads': files_list
            }

        new_ticket['ticket']['comment']['uploads'] = files_list

        if type in self.HIGH_PRIORITY:
            new_ticket['ticket']['priority'] = 'high'

        result = self.zendesk_client.ticket_create(data=new_ticket)

        return result
