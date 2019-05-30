from django.conf import settings
from pipedrive.client import Client


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


        # check if organization exists
        organization = next(iter(self.client.get_organizations(name=company_name)["data"]), None) if self.client.get_organizations(name=company_name)["data"] else None
        org = {"name": company_name, settings.ORG_LINK_TO_PROJECT: link_to_project}

        if not organization:
            organization = self.client.create_organization(**org)["data"]
        else:
            data.update({"data_id": organization["id"]})
            organization = self.client.update_organization(**org)["data"]

        # check if contact exists
        contact =  next(iter(self.client.get_persons_by_name(term=name)["data"]), None) if self.client.get_persons_by_name(term=name)["data"] else None
        data = {"name": name, "email": email, settings.USER_TELEGRAM: telegram, "label": "adviser",
               "org_id": organization["id"]}
        if not contact:
            contact = self.client.create_person(**data)["data"]
        else:
            data.update({"data_id": contact["id"]})
            contact = self.client.update_person(**data)["data"]

        deal = {
            "title": title,
            "org_id": organization["id"],
            "pipeline_id": settings.PIPELINE_CHANNELS[type],
            "person_id": contact["id"]
            }

        self.client.create_deal(**deal)

    def create_adviser(self, data):
        name = data.get("name", "")
        telegram = data.get("telegram", "")
        email = data.get("email")
        linkedin = data.get("linkedin")


        # check if contact exists
        contact = next(iter(self.client.get_persons_by_name(term=name)["data"]), None) if \
        self.client.get_persons_by_name(term=name)["data"] else None
        data = {"name": name, "email": email, settings.USER_TELEGRAM: telegram, "label": "adviser",
                settings.USER_LINKEDIN: linkedin}
        if not contact:
            contact = self.client.create_person(**data)["data"]
        else:
            data.update({"data_id": contact["id"]})
            contact = self.client.update_person(**data)["data"]

        return contact