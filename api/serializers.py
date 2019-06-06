from rest_framework import serializers

from clients.pipedrive_client import PipedriveClient


class CurrencySerializer(serializers.Serializer):
   """Your data serializer, define your fields here."""
   name = serializers.CharField()
   details = serializers.CharField()

   def create(self, validated_data):
      res = PipedriveClient().create_deal(**validated_data)
      return res