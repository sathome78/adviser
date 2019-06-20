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


class PipedriveClient:


    def __init__(self):
        self.client1 = Client(api_base_url=settings.PIPEDRIVE_ME["PIPEDRIVE_URL"])
        self.client1.set_token(settings.PIPEDRIVE_ME["CLIENT_SECRET"])

        self.client2 = Client(api_base_url=settings.PIPEDRIVE["PIPEDRIVE_URL"])
        self.client2.set_token(settings.PIPEDRIVE["CLIENT_SECRET"])

    def create_deal(self, data, args):
        name = data.get("name", "")
        type = data.get("request_type", "")
        title = '{} ({})'.format(name, type)
        company_name = data.get("company_name")
        link_to_project = data.get("link_to_project")

        email = data.get("email")
        telegram = data.get("telegram", "@")[1:]

        args[0]["client"] = self.client1
        args[1]["client"] = self.client2
        result = self.__make_deal(args, company_name, email, link_to_project, name, telegram, title)

        # send notification to telegram
        msg1 = ''
        for k, v in data.items():
            msg1 += '{}: {} \n'.format(k, v)

        msg = "Deal form \n  \n  \n {} \n {} \n \n Result: {}".format(msg1, datetime.now().strftime("%Y-%m-%d %H:%M"), result)
        send(msg, settings.TELEGRAMBOT_CHAT_DEAL)

        return result


    def __make_deal(self, setting_list, company_name, email, link_to_project, name, telegram, title):
        result = {}
        for args in setting_list:

            # check if organization exists
            organization = next(iter(args["client"].get_organizations(name=company_name)["data"]), None) if \
            args["client"].get_organizations(name=company_name)["data"] else None
            org = {"name": company_name, args["ORG_WEBSITE"]: link_to_project}
            if not organization:
                organization = args["client"].create_organization(**org)["data"]
            else:
                org.update({"data_id": organization["id"]})
                organization = args["client"].update_organization(**org)["data"]

            # check if contact exists
            contact = next(iter(args["client"].get_persons_by_name(term=name)["data"]), None) if \
                args["client"].get_persons_by_name(term=name)["data"] else None
            usr = {"name": name, "email": email,
                   "org_id": organization["id"]}
            phone_pattern = re.compile("^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){10,14}(\s*)?$")
            telegram_pattern = re.compile("^[a-zA-Z0-9]+$")
            if phone_pattern.match(telegram):
                usr.update({"phone": telegram})
            elif telegram_pattern.match(telegram):
                usr.update({args["USER_TELEGRAM"]: "https://t.me/{}".format(telegram)})
            if not contact:
                contact = args["client"].create_person(**usr)["data"]
            else:
                usr.update({"data_id": contact["id"]})
                contact = args["client"].update_person(**usr)["data"]
            deal = {
                "title": title,
                "org_id": organization["id"],
                "pipeline_id": args["PIPEDRIVECHANNEL"],
                "person_id": contact["id"]
                }
            deal = args["client"].create_deal(**deal)
            result[args["client"].api_base_url] = "success: ".format(deal.get("success"))
            logger.info('Deal created in {} \n Params {}'.format(args["client"], deal))
        return result

    def create_or_update_adviser(self, data, edit_url, update_url, args):
        name = data.get("name", "")
        telegram = data.get("telegram", "@")[1:]
        email = data.get("email")
        linkedin = data.get("linkedin")

        args[0]["client"] = self.client1
        args[1]["client"] = self.client2

        result = self.__make_adviser(args, edit_url, email, linkedin, name, telegram, update_url)

        # send notification to telegram
        msg1 = ''
        for k, v in data.items():
            msg1 += '{}: {} \n'.format(k, v)

        msg = "Ambassador form \n  \n  \n {} \n {} \n \n result: {}".format(msg1, datetime.now().strftime("%Y-%m-%d %H:%M"), result)
        send(msg, settings.TELEGRAMBOT_CHAT_DEAL)

        return result

    def __make_adviser(self, setting_list, edit_url, email, linkedin, name, telegram, update_url):
        result = {}
        for args in setting_list:
            # check if contact exists
            contact = next(iter(args["client"].get_persons_by_name(term=name)["data"]), None) if \
                args["client"].get_persons_by_name(term=name)["data"] else None
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
                contact = args["client"].create_person(**data)["data"]
            else:
                data.update({"data_id": contact["id"]})
                contact = args["client"].update_person(**data)["data"]
            deal = {
                "title": name,
                "pipeline_id": args["PIPEDRIVE_NEW_ADVISER"],
                "person_id": contact["id"]
                }

            deal = args["client"].create_deal(**deal)
            result[args["client"].api_base_url] = "success: ".format(deal.get("success"))
            logger.info('Deal created in {} \n Params {}'.format(args["client"], deal))

        return result