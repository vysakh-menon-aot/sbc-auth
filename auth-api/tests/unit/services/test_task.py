# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for the Task service.

Test suite to ensure that the Task service routines are working as expected.
"""

from datetime import datetime
from unittest.mock import patch

from auth_api.models import ProductCode as ProductCodeModel
from auth_api.models import Task as TaskModel
from auth_api.services import Affidavit as AffidavitService
from auth_api.services import Org as OrgService
from auth_api.services import Task as TaskService
from auth_api.services.rest_service import RestService
from auth_api.utils.enums import TaskStatus, TaskRelationshipType, OrgStatus, LoginSource, TaskRelationshipStatus, \
    TaskTypePrefix
from tests.utilities.factory_scenarios import TestUserInfo, TestJwtClaims, TestAffidavit, TestOrgInfo, \
    TestPaymentMethodInfo
from tests.utilities.factory_utils import factory_task_service, factory_org_model, factory_user_model, \
    factory_user_model_with_contact, factory_product_model


def test_fetch_tasks(session, auth_mock):  # pylint:disable=unused-argument
    """Assert that tasks can be fetched."""
    user = factory_user_model()
    task = factory_task_service(user.id)
    dictionary = task.as_dict()
    name = dictionary['name']

    fetched_task = TaskService.fetch_tasks(task_status=TaskStatus.OPEN.value,
                                           page=1,
                                           limit=10)

    assert fetched_task['tasks']
    for item in fetched_task['tasks']:
        assert item['name'] == name


def test_create_task_org(session, keycloak_mock):  # pylint:disable=unused-argument
    """Assert that a task can be created."""
    user = factory_user_model()
    test_org = factory_org_model()
    task_type_new_account = TaskTypePrefix.NEW_ACCOUNT_STAFF_REVIEW.value
    test_task_info = {
        'name': test_org.name,
        'relationshipId': test_org.id,
        'relatedTo': user.id,
        'dateSubmitted': datetime.today(),
        'relationshipType': TaskRelationshipType.ORG.value,
        'type': task_type_new_account,
        'status': TaskStatus.OPEN.value,
        'relationship_status': TaskRelationshipStatus.PENDING_STAFF_REVIEW.value
    }
    task = TaskService.create_task(test_task_info)
    assert task
    dictionary = task.as_dict()
    assert dictionary['name'] == test_org.name


def test_create_task_product(session, keycloak_mock):  # pylint:disable=unused-argument
    """Assert that a task can be created."""
    user = factory_user_model()
    test_org = factory_org_model()
    test_product = factory_product_model(org_id=test_org.id)
    product: ProductCodeModel = ProductCodeModel.find_by_code(test_product.product_code)
    test_task_info = {
        'name': test_org.name,
        'relationshipId': test_product.id,
        'relatedTo': user.id,
        'dateSubmitted': datetime.today(),
        'relationshipType': TaskRelationshipType.PRODUCT.value,
        'type': product.description,
        'status': TaskStatus.OPEN.value,
        'accountId': test_org.id,
        'relationship_status': TaskRelationshipStatus.PENDING_STAFF_REVIEW.value
    }
    task = TaskService.create_task(test_task_info)
    assert task
    dictionary = task.as_dict()
    assert dictionary['name'] == test_task_info['name']
    assert dictionary['account_id'] == test_org.id
    assert dictionary['relationship_type'] == TaskRelationshipType.PRODUCT.value


def test_update_task(session, keycloak_mock):  # pylint:disable=unused-argument
    """Assert that a task can be updated."""
    user_with_token = TestUserInfo.user_bceid_tester
    user_with_token['keycloak_guid'] = TestJwtClaims.public_bceid_user['sub']
    user = factory_user_model_with_contact(user_with_token)

    affidavit_info = TestAffidavit.get_test_affidavit_with_contact()
    AffidavitService.create_affidavit(token_info=TestJwtClaims.public_bceid_user, affidavit_info=affidavit_info)

    org = OrgService.create_org(TestOrgInfo.org_with_mailing_address(), user_id=user.id,
                                token_info=TestJwtClaims.public_bceid_user)
    org_dict = org.as_dict()
    assert org_dict['org_status'] == OrgStatus.PENDING_STAFF_REVIEW.value

    token_info = TestJwtClaims.get_test_user(sub=user.keycloak_guid, source=LoginSource.STAFF.value)

    tasks = TaskService.fetch_tasks(task_status=TaskStatus.OPEN.value,
                                    page=1,
                                    limit=10)
    fetched_tasks = tasks['tasks']
    fetched_task = fetched_tasks[0]

    task_info = {
        'relationshipStatus': TaskRelationshipStatus.ACTIVE.value
    }
    task: TaskModel = TaskModel.find_by_task_id(fetched_task['id'])

    task = TaskService.update_task(TaskService(task), task_info=task_info,
                                   token_info=token_info)
    dictionary = task.as_dict()
    assert dictionary['status'] == TaskStatus.COMPLETED.value
    assert dictionary['relationship_status'] == TaskRelationshipStatus.ACTIVE.value


def test_create_task_govm(session,
                          keycloak_mock):  # pylint:disable=unused-argument
    """Assert that a task can be created when updating a GOVM account."""
    user = factory_user_model()
    token_info = TestJwtClaims.get_test_user(sub=user.keycloak_guid, source=LoginSource.STAFF.value,
                                             roles=['create_accounts'])
    user2 = factory_user_model(TestUserInfo.user2)
    public_token_info = TestJwtClaims.get_test_user(sub=user2.keycloak_guid, source=LoginSource.STAFF.value,
                                                    roles=['gov_account_user'])

    org: OrgService = OrgService.create_org(TestOrgInfo.org_govm, user_id=user.id, token_info=token_info)
    assert org
    with patch.object(RestService, 'put') as mock_post:
        payment_details = TestPaymentMethodInfo.get_payment_method_input_with_revenue()
        org_body = {
            'mailingAddress': TestOrgInfo.get_mailing_address(),
            **payment_details

        }
        org = OrgService.update_org(org, org_body, token_info=public_token_info)
        assert org
        dictionary = org.as_dict()
        assert dictionary['name'] == TestOrgInfo.org_govm['name']
        mock_post.assert_called()
        actual_data = mock_post.call_args.kwargs.get('data')
        expected_data = {
            'accountId': dictionary.get('id'),
            'accountName': dictionary.get('name') + '-' + dictionary.get('branch_name'),
            'paymentInfo': {
                'methodOfPayment': 'EJV',
                'billable': False,
                'revenueAccount': payment_details.get('paymentInfo').get('revenueAccount')
            },
            'contactInfo': TestOrgInfo.get_mailing_address()

        }
        assert expected_data == actual_data

        # Assert the task that is created
        fetched_task = TaskService.fetch_tasks(task_status=TaskStatus.OPEN.value,
                                               page=1,
                                               limit=10)

        for item in fetched_task['tasks']:
            assert item['name'] == dictionary['name']
            assert item['type'] == TaskTypePrefix.GOVM_REVIEW.value
            assert item['status'] == TaskStatus.OPEN.value
            assert item['relationship_id'] == dictionary['id']