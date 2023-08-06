from core.gql.gql_mutations import DeleteInputType
from core.gql.gql_mutations.base_mutation import (
    BaseMutation,
    BaseDeleteMutation,
    BaseReplaceMutation,
    BaseHistoryModelCreateMutationMixin,
    BaseHistoryModelUpdateMutationMixin,
    BaseHistoryModelDeleteMutationMixin,
    BaseHistoryModelReplaceMutationMixin,
)
from contribution_plan.gql.gql_mutations import (
    ContributionPlanBundleInputType,
    ContributionPlanBundleUpdateInputType,
    ContributionPlanBundleReplaceInputType
)
from contribution_plan.models import (
    ContributionPlanBundle,
    ContributionPlanBundleDetails
)
from contribution_plan.services import (
    ContributionPlanBundleDetails as ContributionPlanBundleDetailsService
)


class CreateContributionPlanBundleMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_class = "ContributionPlanBundleMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlanBundle

    class Input(ContributionPlanBundleInputType):
        pass


class UpdateContributionPlanBundleMutation(BaseHistoryModelUpdateMutationMixin, BaseMutation):
    _mutation_class = "ContributionPlanBundleMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlanBundle

    class Input(ContributionPlanBundleUpdateInputType):
        pass


class DeleteContributionPlanBundleMutation(BaseHistoryModelDeleteMutationMixin, BaseDeleteMutation):
    _mutation_class = "ContributionPlanBundleMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlanBundle

    class Input(DeleteInputType):
        pass


class ReplaceContributionPlanBundleMutation(BaseHistoryModelReplaceMutationMixin, BaseReplaceMutation):
    _mutation_class = "ContributionPlanBundleMutation"
    _mutation_module = "contribution_plan"
    _model = ContributionPlanBundle

    @classmethod
    def _mutate(cls, user, **data):
        super()._mutate(user, **data)
        # copy attached contribution plan bundles into new version
        list_cpbd = ContributionPlanBundleDetails.objects.filter(
            contribution_plan_bundle__id=data["uuid"],
            is_deleted=False,
        )
        old_cpb = ContributionPlanBundle.objects.get(id=data["uuid"], is_deleted=False)
        new_cpb = ContributionPlanBundle.objects.get(id=old_cpb.replacement_uuid, is_deleted=False)
        if new_cpb:
            for cpbd in list_cpbd:
                cls._attach_contribution_plan_to_new_version_of_bundle(
                    user,
                    cpbd.contribution_plan.id,
                    new_cpb.id,
                    new_cpb.date_valid_from,
                    new_cpb.date_valid_to
                )
                cls._update_old_validity_to(cpbd, new_cpb, user)

    @classmethod
    def _create_payload_cpbd(cls, cp_uuid, cpb_uuid, date_valid_from, date_valid_to):
        return {
            "contribution_plan_id": f"{cp_uuid}",
            "contribution_plan_bundle_id": f"{cpb_uuid}",
            "date_valid_from": date_valid_from,
            "date_valid_to": date_valid_to
        }

    @classmethod
    def _attach_contribution_plan_to_new_version_of_bundle(cls, user, cp_uuid, cpb_uuid, valid_from, valid_to):
        cpbd_service = ContributionPlanBundleDetailsService(user)
        payload_cpbd = cls._create_payload_cpbd(cp_uuid, cpb_uuid, valid_from, valid_to)
        response = cpbd_service.create(payload_cpbd)
        return response

    @classmethod
    def _update_old_validity_to(cls, old_cpbd, new_cpb, user):
        cpbd_service = ContributionPlanBundleDetailsService(user)
        payload_update_cpbd = cls._create_payload_update_cpbd(
            old_cpbd.id,
            new_cpb.date_valid_from,
            old_cpbd.date_valid_to
        )
        response = cpbd_service.update(payload_update_cpbd)
        return response

    @classmethod
    def _create_payload_update_cpbd(cls, cpbd_uuid, new_valid_from, old_valid_to):
        if old_valid_to:
            new_valid_from = new_valid_from if old_valid_to > new_valid_from else old_valid_to
        else:
            new_valid_from = new_valid_from
        return {
            "id": f"{cpbd_uuid}",
            "date_valid_to": new_valid_from,
        }

    class Input(ContributionPlanBundleReplaceInputType):
        pass
