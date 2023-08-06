import uuid

from contribution.models import Payer, Premium


def create_test_payer(payer_type=Payer.PAYER_TYPE_OTHER, custom_props=None):
    payer = Payer.objects.create(
        **{
            "type": payer_type,
            "uuid": uuid.uuid4(),
            "name": "Test Default Payer Name",
            "address": "Test street name 123, CZ9204 City, Country",
            "validity_from": "2019-01-01",
            "audit_user_id": -1,
            **(custom_props if custom_props else {})
        }
    )
    return payer
