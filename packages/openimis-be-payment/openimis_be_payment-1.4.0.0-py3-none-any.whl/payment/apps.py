from django.apps import AppConfig

MODULE_NAME = "payment"

DEFAULT_CFG = {
    "gql_query_payments_perms": ["101401"],
    "gql_mutation_create_payments_perms": ["101402"],
    "gql_mutation_update_payments_perms": ["101403"],
    "gql_mutation_delete_payments_perms": ["101404"],
    "default_validations_disabled": False,
}


class PaymentConfig(AppConfig):
    name = MODULE_NAME

    gql_query_payments_perms = []
    gql_mutation_create_payments_perms = []
    gql_mutation_update_payments_perms = []
    gql_mutation_delete_payments_perms = []
    default_validations_disabled = False

    def _configure_permissions(self, cfg):
        PaymentConfig.gql_query_payments_perms = cfg["gql_query_payments_perms"]
        PaymentConfig.gql_mutation_create_premiums_perms = cfg["gql_mutation_create_payments_perms"]
        PaymentConfig.gql_mutation_update_premiums_perms = cfg["gql_mutation_update_payments_perms"]
        PaymentConfig.gql_mutation_delete_premiums_perms = cfg["gql_mutation_delete_payments_perms"]

    def ready(self):
        from core.models import ModuleConfiguration
        cfg = ModuleConfiguration.get_or_default(MODULE_NAME, DEFAULT_CFG)
        self._configure_permissions(cfg)
        PaymentConfig.default_validations_disabled = cfg["default_validations_disabled"]
