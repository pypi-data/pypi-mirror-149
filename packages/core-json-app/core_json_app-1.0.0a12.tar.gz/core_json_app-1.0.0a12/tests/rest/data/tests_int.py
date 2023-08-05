""" Integration Test for Data Rest API
"""

from core_json_app.rest.data import views as data_rest_views
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_main_app.utils.integration_tests.integration_base_transaction_test_case import (
    MongoIntegrationTransactionTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock

from tests.rest.user.fixtures.fixtures import UserFixtures
from tests.rest.data.fixtures.fixtures import AccessControlDataFixture

fixture_data_workspace = AccessControlDataFixture()


class TestJsonDataListbyWorkspace(MongoIntegrationBaseTestCase):
    fixture = fixture_data_workspace

    def setUp(self):
        super(TestJsonDataListbyWorkspace, self).setUp()

    def test_get_filtered_by_correct_workspace_returns_data(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.DataList.as_view(),
            user,
            data={"workspace": self.fixture.workspace_1.id},
        )

        # Assert
        self.assertEqual(len(response.data), 2)

    def test_get_filtered_by_incorrect_workspace_returns_no_data(self):
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            data_rest_views.DataList.as_view(),
            user,
            data={"workspace": "5da8ac0622301d1240f2551b"},
        )

        # Assert
        self.assertEqual(len(response.data), 0)


class TestJsonExecuteLocalQueryViewWorkspaceCase(MongoIntegrationTransactionTestCase):
    fixture = fixture_data_workspace

    def setUp(self):
        super(TestJsonExecuteLocalQueryViewWorkspaceCase, self).setUp()

        self.data = {"all": "true"}

        # create user with superuser access to skip access control
        self.user = create_mock_user("1", is_superuser=True)

        self.user2 = UserFixtures().create_user()

        self.user2.id = self.fixture.data_4.user_id

    def test_post_empty_query_with_no_specific_workspace_returns_all_accessible_data_as_superuser(
        self,
    ):

        # Arrange
        self.data.update(dict(query={}, workspaces={}))

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(), self.user, data=self.data
        )

        # Assert
        self.assertEqual(len(response.data), 5)

    def test_post_empty_query_with_no_specific_workspace_returns_all_accessible_data_as_user(
        self,
    ):

        # Arrange
        self.data.update(dict(query={}))
        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(), self.user2, data=self.data
        )

        # Assert
        self.assertEqual(len(response.data), 2)

        for data in response.data:
            self.assertEqual(data["user_id"], str(self.user2.id))

    def test_post_empty_query_string_filter_by_one_workspace_returns_all_data_of_the_workspace(
        self,
    ):

        # Arrange
        self.data.update(
            dict(
                query={},
                workspaces=[{"id": str(self.fixture.workspace_1.id)}],
            )
        )

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(), self.user, data=self.data
        )

        # Assert
        self.assertEqual(len(response.data), 2)

        for data in response.data:
            self.assertEqual(data["workspace"], str(self.fixture.workspace_1.id))

    def test_post_empty_query_string_filter_by_workspaces_returns_all_data_of_those_workspaces(
        self,
    ):

        # Arrange
        self.data.update(
            dict(
                query={},
                workspaces=[
                    {"id": str(self.fixture.workspace_1.id)},
                    {"id": str(self.fixture.workspace_2.id)},
                ],
            )
        )

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(), self.user, data=self.data
        )

        # Assert
        self.assertEqual(len(response.data), 3)

        list_ids = [str(self.fixture.workspace_1.id), str(self.fixture.workspace_2.id)]
        for data in response.data:
            self.assertIn(data["workspace"], list_ids)

    def test_post_query_filter_by_correct_and_wrong_workspaces_returns_data_from_correct_workspace_only_as_superuser(
        self,
    ):

        # Arrange
        self.data.update(
            dict(
                query={},
                workspaces=[
                    {"id": "507f1f77bcf86cd799439011"},
                    {"id": str(self.fixture.workspace_2.id)},
                ],
            )
        )

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(), self.user, data=self.data
        )

        # Assert
        self.assertEqual(len(response.data), 1)

        for data in response.data:
            self.assertEqual(data["workspace"], str(self.fixture.workspace_2.id))

    def test_post_query_filter_by_correct_and_wrong_workspaces_returns_data_from_correct_workspace_only_as_user(
        self,
    ):

        # Arrange
        self.data.update(
            dict(
                query={},
                workspaces=[
                    {"id": str(self.fixture.workspace_1.id)},
                    {"id": str(self.fixture.workspace_2.id)},
                ],
            )
        )

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(), self.user2, data=self.data
        )

        # Assert
        self.assertEqual(len(response.data), 1)

        list_ids = [str(self.fixture.workspace_2.id)]
        for data in response.data:
            self.assertIn(data["workspace"], list_ids)

    def test_post_query_string_filter_by_workspace_returns_data_3(self):

        # Arrange
        self.data.update(
            dict(
                query={"root.element": "value2"},
                workspaces=[{"id": str(self.fixture.workspace_1.id)}],
            )
        )

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(), self.user, data=self.data
        )

        # Assert
        self.assertEqual(len(response.data), 1)

        for data in response.data:
            self.assertEqual(data["id"], str(self.fixture.data_3.id))
            self.assertEqual(data["workspace"], str(self.fixture.workspace_1.id))

    def test_post_query_string_filter_by_workspace_returns_no_data(self):

        # Arrange
        self.data.update(
            dict(
                query={"root.element": "value2"},
                workspaces=[{"id": str(self.fixture.workspace_2.id)}],
            )
        )

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(), self.user, data=self.data
        )

        # Assert
        self.assertEqual(len(response.data), 0)

    def test_post_query_string_filter_by_private_workspace_returns_all_data_with_no_workspace_as_superuser(
        self,
    ):

        # Arrange
        self.data.update(dict(query={}, workspaces=[{"id": "None"}]))

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(), self.user, data=self.data
        )

        # Assert
        self.assertEqual(len(response.data), 2)
        for data in response.data:
            self.assertEqual(data["workspace"], None)

    def test_post_query_string_filter_by_private_workspace_returns_all_data_with_no_workspace_as_user(
        self,
    ):

        # Arrange
        self.data.update(dict(query={}, workspaces=[{"id": "None"}]))

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(), self.user2, data=self.data
        )

        # Assert
        self.assertEqual(len(response.data), 1)
        for data in response.data:
            self.assertEqual(data["workspace"], None)
            self.assertEqual(data["user_id"], self.user2.id)

    def test_post_query_filter_by_private_and_normal_workspaces_returns_all_data_of_those_workspaces_as_superuser(
        self,
    ):

        # Arrange
        self.data.update(
            dict(
                query={},
                workspaces=[{"id": "None"}, {"id": str(self.fixture.workspace_2.id)}],
            )
        )

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(), self.user, data=self.data
        )

        # Assert
        self.assertEqual(len(response.data), 3)

        list_ids = [None, str(self.fixture.workspace_2.id)]
        for data in response.data:
            self.assertIn(data["workspace"], list_ids)

    def test_post_query_filter_by_private_and_normal_workspaces_returns_all_data_of_those_workspaces_as_user(
        self,
    ):

        # Arrange
        self.data.update(
            dict(
                query={},
                workspaces=[{"id": "None"}, {"id": str(self.fixture.workspace_2.id)}],
            )
        )

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(), self.user2, data=self.data
        )

        # Assert
        self.assertEqual(len(response.data), 2)

        list_ids = [None, str(self.fixture.workspace_2.id)]
        for data in response.data:
            self.assertIn(data["workspace"], list_ids)

    def test_post_filtered_by_wrong_workspace_id_returns_no_data(self):
        # Arrange
        self.data.update(
            dict(query={}, workspaces=[{"id": "507f1f77bcf86cd799439011"}])
        )

        # Act
        response = RequestMock.do_request_post(
            data_rest_views.ExecuteLocalQueryView.as_view(), self.user, data=self.data
        )

        # Assert
        self.assertEqual(len(response.data), 0)
