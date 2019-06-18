# -*- coding: utf-8 -*-
import re
from datetime import datetime

import telegram
from django.conf import settings
from pipedrive.client import Client



def send(msg, chat, token=settings.TELEGRAMBOT_TOKEN):
    """
        Send a mensage to a telegram user specified on chatId
        chat_id must be a number!
    """
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id=chat, text=msg)
    return  bot


class PipedriveClient:


    def __init__(self):
        self.client = Client(api_base_url=settings.PIPEDRIVE_URL)
        self.client.set_token(settings.CLIENT_SECRET)


    def create_deal(self, data):
        name = data.get("name", "")
        type = data.get("request_type", "")
        title = '{} ({})'.format(name, type)
        company_name = data.get("company_name")
        link_to_project = data.get("link_to_project")

        email = data.get("email")
        telegram = data.get("telegram")

        #send notification to telegram
        msg1 = ''
        for k,v in data.items():
            msg1 += '{}: {} \n'.format(k,v)

        msg = "Deal form \n  \n  \n {} \n {}".format(msg1, datetime.now().strftime("%Y-%m-%d %H:%M"))
        send(msg, settings.TELEGRAMBOT_CHAT_DEAL)


        # check if organization exists
        organization = next(iter(self.client.get_organizations(name=company_name)["data"]), None) if self.client.get_organizations(name=company_name)["data"] else None
        org = {"name": company_name, settings.ORG_WEBSITE: link_to_project}

        if not organization:
            organization = self.client.create_organization(**org)["data"]
        else:
            org.update({"data_id": organization["id"]})
            organization = self.client.update_organization(**org)["data"]

        # check if contact exists
        contact =  next(iter(self.client.get_persons_by_name(term=name)["data"]), None) if self.client.get_persons_by_name(term=name)["data"] else None


        usr = {"name": name, "email": email,
               "org_id": organization["id"]}
        phone_pattern = re.compile("^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?$")
        telegram_pattern = re.compile("^[a-zA-Z0-9]+$")
        if phone_pattern.match(telegram):
            usr.update({"phone": telegram})
        elif telegram_pattern.match(telegram):
            usr.update({settings.USER_TELEGRAM: "https://t.me/{}".format(telegram)})


        if not contact:
            contact = self.client.create_person(**usr)["data"]
        else:
            usr.update({"data_id": contact["id"]})
            contact = self.client.update_person(**usr)["data"]

        deal = {
            "title": title,
            "org_id": organization["id"],
            "pipeline_id": settings.PIPEDRIVECHANNEL,
            "person_id": contact["id"]
            }

        return self.client.create_deal(**deal)

    def create_or_update_adviser(self, data, edit_url, update_url):
        name = data.get("name", "")
        telegram = data.get("telegram", "")
        email = data.get("email")
        linkedin = data.get("linkedin")

        # send notification to telegram
        msg1 = ''
        for k, v in data.items():
            msg1 += '{}: {} \n'.format(k, v)

        msg = "Ambassador form \n  \n  \n {} \n {}".format(msg1, datetime.now().strftime("%Y-%m-%d %H:%M"))
        send(msg, settings.TELEGRAMBOT_CHAT_DEAL)


        # check if contact exists
        contact = next(iter(self.client.get_persons_by_name(term=name)["data"]), None) if \
        self.client.get_persons_by_name(term=name)["data"] else None


        data = {"name": name, "email": email, "label": "adviser",
                settings.USER_LINKEDIN: linkedin, settings.USER_LINKS: '{} \n {}'.format(edit_url, update_url)}

        phone_pattern = re.compile("^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?$")
        telegram_pattern = re.compile("^[a-zA-Z0-9]+$")

        if telegram:
            if phone_pattern.match(telegram):
                data.update({"phone": telegram})
            elif telegram_pattern.match(telegram):
                data.update({settings.USER_TELEGRAM: "https://t.me/{}".format(telegram)})

        if not contact:
            contact = self.client.create_person(**data)["data"]
        else:
            data.update({"data_id": contact["id"]})
            contact = self.client.update_person(**data)["data"]

        deal = {
            "title": name,
            "pipeline_id": settings.PIPEDRIVE_NEW_ADVISER,
            "person_id": contact["id"]
            }

        self.client.create_deal(**deal)

        return contact