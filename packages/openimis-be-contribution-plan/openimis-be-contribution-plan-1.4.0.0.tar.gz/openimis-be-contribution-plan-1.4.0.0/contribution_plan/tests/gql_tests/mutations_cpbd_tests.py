import datetime
import numbers
import base64
from unittest import TestCase, mock
from uuid import UUID

import graphene
from contribution_plan.tests.helpers import *
from contribution_plan import schema as contribution_plan_schema
from graphene import Schema
from graphene.test import Client


class MutationTestContributionPlanBundleDetails(TestCase):

    class BaseTestContext:
        def __init__(self, user):
            self.user = user

    class AnonymousUserContext:
        user = mock.Mock(is_anonymous=True)

    @classmethod
    def setUpClass(cls):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(username='admin', password='S\/pe®Pąßw0rd™')
        cls.user = User.objects.filter(username='admin').first()
        cls.test_contribution_plan_bundle = create_test_contribution_plan_bundle(
            custom_props={'code': 'SuperContributionPlan mutations!'})
        cls.test_contribution_plan = create_test_contribution_plan()
        cls.test_contribution_plan2 = create_test_contribution_plan()
        cls.test_contribution_plan_bundle_details = create_test_contribution_plan_bundle_details()

        cls.schema = Schema(
            query=contribution_plan_schema.Query,
            mutation=contribution_plan_schema.Mutation
        )

        cls.graph_client = Client(cls.schema)

    @classmethod
    def tearDownClass(cls):
        ContributionPlanBundleDetails.objects.filter(id=cls.test_contribution_plan_bundle_details.id).delete()
        ContributionPlan.objects.filter(id__in=[cls.test_contribution_plan.id, cls.test_contribution_plan2.id]).delete()
        ContributionPlanBundle.objects.filter(id=cls.test_contribution_plan_bundle.id).delete()

    def test_contribution_plan_bundle_details_create_without_obligatory_fields(self):
        time_stamp = datetime.datetime.now()
        input_param = {
            "contributionPlanId": f"{self.test_contribution_plan_bundle.id}",
        }
        result_mutation = self.add_mutation("createContributionPlanBundleDetails", input_param)
        self.assertEqual(True, 'errors' in result_mutation)

    def test_contribution_plan_bundle_details_update_1_existing_foreign_key(self):
        id = self.test_contribution_plan_bundle_details.id
        version = self.test_contribution_plan_bundle_details.version
        input_param = {
            "id": f"{id}",
            "contributionPlanId": f"{self.test_contribution_plan2.id}",
        }
        self.add_mutation("updateContributionPlanBundleDetails", input_param)
        result = self.find_by_id_query("contributionPlanBundleDetails", f"{id}")
        self.test_contribution_plan_bundle_details.version = result[0]['node']['version']
        self.assertEqual(version+1, result[0]['node']['version'])

    def test_contribution_plan_bundle_details_update_2_without_changing_fields_foreign_key(self):
        id = self.test_contribution_plan_bundle_details.id
        version = self.test_contribution_plan_bundle_details.version
        input_param = {
            "id": f"{id}",
            "contributionPlanId": f"{self.test_contribution_plan2.id}",
        }
        self.add_mutation("updateContributionPlanBundleDetails", input_param)
        result = self.find_by_id_query("contributionPlanBundleDetails", f"{id}")
        self.test_contribution_plan_bundle_details.version = result[0]['node']['version']
        self.assertEqual(version, result[0]['node']['version'])

    def test_contribution_plan_update_3_without_id_field(self):
        id = self.test_contribution_plan.id
        version = self.test_contribution_plan.version
        input_param = {
            "name": "XYZ test name xxxxx",
        }
        result_mutation = self.add_mutation("updateContributionPlan", input_param)
        self.assertEqual(True, 'errors' in result_mutation)

    def find_by_id_query(self, query_type, id, context=None):
        query = F'''
        {{
            {query_type}(orderBy: ["dateCreated"], id:"{id}") {{
                totalCount
                edges {{
                  node {{
                    id
                    version
                    dateValidFrom
                    dateValidTo
                    replacementUuid
                  }}
                  cursor
                }}
          }}
        }}
        '''

        query_result = self.execute_query(query, context=context)
        records = query_result[query_type]['edges']

        if len(records) > 1:
            raise ValueError(F"Ambiguous id {id} for query {query_type}")

        return records

    def find_by_exact_attributes_query(self, query_type, params, context=None):
        if "dateValidFrom" in params:
            params.pop('dateValidFrom')
        if "dateValidTo" in params:
            params.pop('dateValidTo')
        if "contributionPlanId" in params:
            params.pop('contributionPlanId')
        if "contributionPlanBundleId" in params:
            params.pop('contributionPlanBundleId')

        node_content_str = "\n".join(params.keys())
        query = F'''
        {{
            {query_type}(orderBy: ["dateCreated"], {self.build_params(params)}) {{
                totalCount
                edges {{
                  node {{
                    {'id' if 'id' not in params else '' }
                    version
                    dateValidFrom
                    dateValidTo
                    replacementUuid
                  }}
                  cursor
                }}
          }}
        }}
        '''
        query_result = self.execute_query(query, context=context)
        records = query_result[query_type]
        return records

    def execute_query(self, query, context=None):
        if context is None:
            context = self.BaseTestContext(self.user)

        query_result = self.graph_client.execute(query, context=context)
        query_data = query_result['data']
        return query_data

    def add_mutation(self, mutation_type, input_params, context=None):
        mutation = f'''
        mutation 
        {{
            {mutation_type}(input: {{
               {self.build_params(input_params)}
            }})  

          {{
            internalId
            clientMutationId
          }}
        }}
        '''
        mutation_result = self.execute_mutation(mutation, context=context)
        return mutation_result

    def execute_mutation(self, mutation, context=None):
        if context is None:
            context = self.BaseTestContext(self.user)

        mutation_result = self.graph_client.execute(mutation, context=context)
        return mutation_result

    def build_params(self, params):
        def wrap_arg(v):
            if isinstance(v, str):
                return F'"{v}"'
            if isinstance(v, list):
                return json.dumps(v)
            if isinstance(v, bool):
                return str(v).lower()
            if isinstance(v, datetime.date):
                return graphene.DateTime.serialize(
                    datetime.datetime.fromordinal(v.toordinal()))
            return v

        params_as_args = [f'{k}:{wrap_arg(v)}' for k, v in params.items()]
        return ", ".join(params_as_args)
