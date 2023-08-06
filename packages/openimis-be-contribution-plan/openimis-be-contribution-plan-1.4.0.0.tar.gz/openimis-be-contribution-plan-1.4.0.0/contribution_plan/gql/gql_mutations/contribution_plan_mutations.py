from core.gql.gql_mutations import DeleteInputType
from core.gql.gql_mutations.base_mutation import BaseMutation, BaseDeleteMutation, BaseReplaceMutation, \
    BaseHistoryModelCreateMutationMixin, BaseHistoryModelUpdateMutationMixin, \
    BaseHistoryModelDeleteMutationMixin, BaseHistoryModelReplaceMutationMixin
from contribution_plan.gql.gql_mutations import ContributionPlanInputType, ContributionPlanUpdateInputType, \
    ContributionPlanReplaceInputType
from contribution_plan.models import ContributionPlan


class CreateContributionPlanMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_class = "ContributionPlanMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlan

    class Input(ContributionPlanInputType):
        pass


class UpdateContributionPlanMutation(BaseHistoryModelUpdateMutationMixin, BaseMutation):
    _mutation_class = "ContributionPlanMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlan

    class Input(ContributionPlanUpdateInputType):
        pass


class DeleteContributionPlanMutation(BaseHistoryModelDeleteMutationMixin, BaseDeleteMutation):
    _mutation_class = "ContributionPlanMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlan

    class Input(DeleteInputType):
        pass


class ReplaceContributionPlanMutation(BaseHistoryModelReplaceMutationMixin, BaseReplaceMutation):
    _mutation_class = "ContributionPlanMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlan

    class Input(ContributionPlanReplaceInputType):
        pass
