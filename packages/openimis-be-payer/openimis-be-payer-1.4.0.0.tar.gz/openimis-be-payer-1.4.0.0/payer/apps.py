from django.apps import AppConfig

MODULE_NAME = "payer"

DEFAULT_CFG = {
    "gql_query_payers_perms": ["121801"],
    "gql_mutation_payer_add_perms": ["121802"],
    "gql_mutation_payer_update_perms": ["122103"],
    "gql_mutation_payer_delete_perms": ["121804"],
}


class PayerConfig(AppConfig):
    name = MODULE_NAME

    gql_query_payers_perms = []
    gql_mutation_payer_add_perms = []
    gql_mutation_payer_update_perms = []
    gql_mutation_payer_delete_perms = []

    def _configure_permissions(self, cfg):
        PayerConfig.gql_query_payers_perms = cfg["gql_query_payers_perms"]
        PayerConfig.gql_mutation_payer_add_perms = cfg["gql_mutation_payer_add_perms"]
        PayerConfig.gql_mutation_payer_update_perms = cfg[
            "gql_mutation_payer_update_perms"
        ]
        PayerConfig.gql_mutation_payer_delete_perms = cfg[
            "gql_mutation_payer_delete_perms"
        ]

    def ready(self):
        from core.models import ModuleConfiguration

        cfg = ModuleConfiguration.get_or_default(MODULE_NAME, DEFAULT_CFG)
        self._configure_permissions(cfg)
