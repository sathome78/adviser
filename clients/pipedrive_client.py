# -*- coding: utf-8 -*-
import re
from datetime import datetime

import telegram
from django.conf import settings
from pipedrive.client import Client


import logging
logger = logging.getLogger(__name__)

def send(msg, chat, token=settings.TELEGRAMBOT_TOKEN):
    """
        Send a mensage to a telegram user specified on chatId
        chat_id must be a number!
    """
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id=chat, text=msg)
    return  bot


class PIPEDRIVE_ME(object):
    def __init__(self):
        self.args = getattr(settings, self.__class__.__name__)
        self.client = Client(api_base_url=self.args["PIPEDRIVE_URL"])
        self.client.set_token(self.args["CLIENT_SECRET"])

class PIPEDRIVE(object):
    def __init__(self):
        self.args = getattr(settings, self.__class__.__name__)
        self.client = Client(api_base_url=self.args["PIPEDRIVE_URL"])
        self.client.set_token(self.args["CLIENT_SECRET"])

class PipedriveClient:


    def __init__(self):
        self.client1 = PIPEDRIVE_ME()
        #self.client1.set_token(settings.PIPEDRIVE_ME["CLIENT_SECRET"])

        self.client2 = PIPEDRIVE()
        #self.client2.set_token(settings.PIPEDRIVE["CLIENT_SECRET"])

    def create_deal(self, data, args):
        name = data.get("name", "")
        type = data.get("request_type", "")
        title = '{} ({})'.format(name, type)
        company_name = data.get("company_name")
        link_to_project = data.get("link_to_project")

        email = data.get("email")
        telegram = data.get("telegram", "@")[1:]

        result = self.__make_deal([PIPEDRIVE_ME, PIPEDRIVE], company_name, email, link_to_project, name, telegram, title)

        # send notification to telegram
        msg1 = ''
        for k, v in data.items():
            msg1 += '{}: {} \n'.format(k, v)

        msg = "Deal form \n  \n  \n {} \n {} \n \n Result: {}".format(msg1, datetime.now().strftime("%Y-%m-%d %H:%M"), result)
        send(msg, settings.TELEGRAMBOT_CHAT_DEAL)

        return result


    def __make_deal(self, setting_list, company_name, email, link_to_project, name, telegram, title):
        result = {}
        deals = []
        for set in setting_list:
            provider = set()
            args = provider.args
            # check if organization exists
            organization = next(iter(provider.client.get_organizations(name=company_name)["data"]), None) if \
                provider.client.get_organizations(name=company_name)["data"] else None
            org = {"name": company_name, args["ORG_WEBSITE"]: link_to_project}
            if not organization:
                organization = provider.client.create_organization(**org)["data"]
            else:
                org.update({"data_id": organization["id"]})
                organization = provider.client.update_organization(**org)["data"]

            # check if contact exists
            contact = next(iter(provider.client.get_persons_by_name(term=name)["data"]), None) if \
                provider.client.get_persons_by_name(term=name)["data"] else None
            usr = {"name": name, "email": email,
                   "org_id": organization["id"]}
            phone_pattern = re.compile("^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?$")
            telegram_pattern = re.compile("^[a-zA-Z0-9]+$")
            if phone_pattern.match(telegram):
                usr.update({"phone": telegram})
            elif telegram_pattern.match(telegram):
                usr.update({args["USER_TELEGRAM"]: "https://t.me/{}".format(telegram)})
            if not contact:
                contact = provider.client.create_person(**usr)["data"]
            else:
                usr.update({"data_id": contact["id"]})
                contact = provider.client.update_person(**usr)["data"]
            deal = {
                "title": title,
                "org_id": organization["id"],
                "pipeline_id": args["PIPEDRIVECHANNEL"],
                "person_id": contact["id"]
                }
            deal = provider.client.create_deal(**deal)
            result[provider.client.api_base_url] = "success: ".format(deal.get("success"))
            logger.info('Deal created in {} \n Params {}'.format(provider.client, deal))
            deals.append({"deal_id": deal["data"]["id"], "workspace": provider.__class__.__name__})
        return deals

    def create_or_update_adviser(self, data, edit_url, update_url, args):
        name = data.get("name", "")
        telegram = data.get("telegram", "@")[1:]
        email = data.get("email")
        linkedin = data.get("linkedin")

        result = self.__make_adviser([PIPEDRIVE_ME, PIPEDRIVE], edit_url, email, linkedin, name, telegram, update_url)

        # send notification to telegram
        msg1 = ''
        for k, v in data.items():
            msg1 += '{}: {} \n'.format(k, v)

        msg = "Ambassador form \n  \n  \n {} \n {} \n \n result: {}".format(msg1, datetime.now().strftime("%Y-%m-%d %H:%M"), result)
        send(msg, settings.TELEGRAMBOT_CHAT_DEAL)

        return result

    def __make_adviser(self, setting_list, edit_url, email, linkedin, name, telegram, update_url):
        deals = []
        result = {}
        for set in setting_list:
            provider = set()
            args = provider.args
            # check if contact exists
            contact = next(iter(provider.client.get_persons_by_name(term=name)["data"]), None) if \
                provider.client.get_persons_by_name(term=name)["data"] else None
            data = {"name": name, "email": email, "label": "adviser",
                    args["USER_LINKEDIN"]: linkedin, args["USER_LINKS"]: '{} \n {}'.format(edit_url, update_url)}
            phone_pattern = re.compile("^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?$")
            telegram_pattern = re.compile("^[a-zA-Z0-9]+$")
            if telegram:
                if phone_pattern.match(telegram):
                    data.update({"phone": telegram})
                elif telegram_pattern.match(telegram):
                    data.update({args["USER_TELEGRAM"]: "https://t.me/{}".format(telegram)})
            if not contact:
                contact = provider.client.create_person(**data)["data"]
            else:
                data.update({"data_id": contact["id"]})
                contact = provider.client.update_person(**data)["data"]
            deal = {
                "title": name,
                "pipeline_id": args["PIPEDRIVE_NEW_ADVISER"],
                "person_id": contact["id"]
                }

            deal = provider.client.create_deal(**deal)
            result[provider.client.api_base_url] = "success: ".format(deal.get("success"))
            logger.info('Deal created in {} \n Params {}'.format(provider.client, deal))
            deals.append({"deal_id": deal["data"]["id"], "workspace": provider.__class__.__name__})
        return deals

    def delete_deal(self, deal_id, client):
        deal = client.delete_deal(deal_id)
        # send notification to telegram
        msg1 = ''
        msg = "Deal with id ".format(deal_id,datetime.now().strftime("%Y-%m-%d %H:%M"),
                                                                            )
        send(msg, settings.TELEGRAMBOT_CHAT_DEAL)
        return deal
