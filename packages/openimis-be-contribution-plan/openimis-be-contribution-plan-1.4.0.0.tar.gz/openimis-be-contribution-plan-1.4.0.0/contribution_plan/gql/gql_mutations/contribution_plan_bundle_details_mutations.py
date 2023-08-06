from core.gql.gql_mutations import DeleteInputType
from core.gql.gql_mutations.base_mutation  import BaseMutation, BaseDeleteMutation, BaseReplaceMutation, \
    BaseHistoryModelCreateMutationMixin, BaseHistoryModelUpdateMutationMixin, \
    BaseHistoryModelDeleteMutationMixin, BaseHistoryModelReplaceMutationMixin
from contribution_plan.gql.gql_mutations import ContributionPlanBundleDetailsInputType, \
    ContributionPlanBundleDetailsUpdateInputType, ContributionPlanBundleDetailsReplaceInputType
from contribution_plan.models import ContributionPlanBundleDetails


class CreateContributionPlanBundleDetailsMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_class = "ContributionPlanBundleDetailsMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlanBundleDetails

    class Input(ContributionPlanBundleDetailsInputType):
        pass


class UpdateContributionPlanBundleDetailsMutation(BaseHistoryModelUpdateMutationMixin, BaseMutation):
    _mutation_class = "ContributionPlanBundleDetailsMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlanBundleDetails

    class Input(ContributionPlanBundleDetailsUpdateInputType):
        pass


class DeleteContributionPlanBundleDetailsMutation(BaseHistoryModelDeleteMutationMixin, BaseDeleteMutation):
    _mutation_class = "ContributionPlanBundleDetailsMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlanBundleDetails

    class Input(DeleteInputType):
        pass


class ReplaceContributionPlanBundleDetailsMutation(BaseHistoryModelReplaceMutationMixin, BaseReplaceMutation):
    _mutation_class = "ContributionPlanBundleDetailsMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlanBundleDetails

    class Input(ContributionPlanBundleDetailsReplaceInputType):
        pass