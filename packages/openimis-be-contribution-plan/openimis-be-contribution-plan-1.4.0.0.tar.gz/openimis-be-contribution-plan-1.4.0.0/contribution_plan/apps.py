from django.apps import AppConfig


MODULE_NAME = "contribution_plan"


DEFAULT_CFG = {
    "gql_query_contributionplanbundle_perms": ["151101"],
    "gql_query_contributionplanbundle_admins_perms": [],
    "gql_query_contributionplan_perms": ["151201"],
    "gql_query_contributionplan_admins_perms": [],
    "gql_query_paymentplan_perms": ["157101"],
    "gql_query_paymentplan_admins_perms": [],

    "gql_mutation_create_contributionplanbundle_perms": ["151102"],
    "gql_mutation_update_contributionplanbundle_perms": ["151103"],
    "gql_mutation_delete_contributionplanbundle_perms": ["151104"],
    "gql_mutation_replace_contributionplanbundle_perms": ["151106"],

    "gql_mutation_create_contributionplan_perms": ["151202"],
    "gql_mutation_update_contributionplan_perms": ["151203"],
    "gql_mutation_delete_contributionplan_perms": ["151204"],
    "gql_mutation_replace_contributionplan_perms": ["151206"],

    "gql_mutation_create_paymentplan_perms": ["157102"],
    "gql_mutation_update_paymentplan_perms": ["157103"],
    "gql_mutation_delete_paymentplan_perms": ["157104"],
    "gql_mutation_replace_paymentplan_perms": ["157106"],
}


class ContributionPlanConfig(AppConfig):
    name = MODULE_NAME

    gql_query_contributionplanbundle_perms = []
    gql_query_contributionplanbundle_admins_perms = []

    gql_query_contributionplan_perms = []
    gql_query_contributionplan_admins_perms = []

    gql_query_paymentplan_perms = []
    gql_query_paymentplan_admins_perms = []

    gql_mutation_create_contributionplanbundle_perms = []
    gql_mutation_update_contributionplanbundle_perms = []
    gql_mutation_delete_contributionplanbundle_perms = []
    gql_mutation_replace_contributionplanbundle_perms = []

    gql_mutation_create_contributionplan_perms = []
    gql_mutation_update_contributionplan_perms = []
    gql_mutation_delete_contributionplan_perms = []
    gql_mutation_replace_contributionplan_perms = []

    gql_mutation_create_paymentplan_perms = []
    gql_mutation_update_paymentplan_perms = []
    gql_mutation_delete_paymentplan_perms = []
    gql_mutation_replace_paymentplan_perms = []

    def _configure_permissions(self, cfg):
        ContributionPlanConfig.gql_query_contributionplanbundle_perms = cfg[
            "gql_query_contributionplanbundle_perms"]
        ContributionPlanConfig.gql_query_contributionplanbundle_admins_perms = cfg[
            "gql_query_contributionplanbundle_admins_perms"
        ]

        ContributionPlanConfig.gql_query_contributionplan_perms = cfg[
            "gql_query_contributionplan_perms"]
        ContributionPlanConfig.gql_query_contributionplan_admins_perms = cfg[
            "gql_query_contributionplan_admins_perms"
        ]

        ContributionPlanConfig.gql_query_paymentplan_perms = cfg[
            "gql_query_paymentplan_perms"]
        ContributionPlanConfig.gql_query_paymentplan_admins_perms = cfg[
            "gql_query_paymentplan_admins_perms"
        ]

        ContributionPlanConfig.gql_mutation_create_contributionplanbundle_perms = cfg[
            "gql_mutation_create_contributionplanbundle_perms"
        ]
        ContributionPlanConfig.gql_mutation_update_contributionplanbundle_perms = cfg[
            "gql_mutation_update_contributionplanbundle_perms"
        ]
        ContributionPlanConfig.gql_mutation_delete_contributionplanbundle_perms = cfg[
            "gql_mutation_delete_contributionplanbundle_perms"
        ]
        ContributionPlanConfig.gql_mutation_replace_contributionplanbundle_perms = cfg[
            "gql_mutation_replace_contributionplanbundle_perms"
        ]

        ContributionPlanConfig.gql_mutation_create_contributionplan_perms = cfg[
            "gql_mutation_create_contributionplan_perms"
        ]
        ContributionPlanConfig.gql_mutation_update_contributionplan_perms = cfg[
            "gql_mutation_update_contributionplan_perms"
        ]
        ContributionPlanConfig.gql_mutation_delete_contributionplan_perms = cfg[
            "gql_mutation_delete_contributionplan_perms"
        ]
        ContributionPlanConfig.gql_mutation_replace_contributionplan_perms = cfg[
            "gql_mutation_replace_contributionplan_perms"
        ]

        ContributionPlanConfig.gql_mutation_create_paymentplan_perms = cfg[
            "gql_mutation_create_paymentplan_perms"
        ]
        ContributionPlanConfig.gql_mutation_update_paymentplan_perms = cfg[
            "gql_mutation_update_paymentplan_perms"
        ]
        ContributionPlanConfig.gql_mutation_delete_paymentplan_perms = cfg[
            "gql_mutation_delete_paymentplan_perms"
        ]
        ContributionPlanConfig.gql_mutation_replace_paymentplan_perms = cfg[
            "gql_mutation_replace_paymentplan_perms"
        ]

    def ready(self):
        from core.models import ModuleConfiguration
        cfg = ModuleConfiguration.get_or_default(MODULE_NAME, DEFAULT_CFG)
        self._configure_permissions(cfg)
