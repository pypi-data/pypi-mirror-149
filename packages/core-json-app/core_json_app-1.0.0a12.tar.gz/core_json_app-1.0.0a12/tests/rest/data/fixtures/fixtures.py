""" Fixtures files for Data
"""
from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from core_main_app.components.workspace import api as workspace_api
from core_main_app.components.workspace.models import Workspace
from core_main_app.utils.integration_tests.fixture_interface import FixtureInterface
from tests.test_utils import get_valid_schema


class AccessControlDataFixture(FixtureInterface):
    """Access Control Data fixture"""

    USER_1_NO_WORKSPACE = 0
    USER_2_NO_WORKSPACE = 1
    USER_1_WORKSPACE_1 = 2
    USER_2_WORKSPACE_2 = 3

    template = None
    workspace_1 = None
    workspace_2 = None
    data_collection = None
    data_1 = None
    data_2 = None
    data_3 = None
    data_4 = None
    data_5 = None

    def insert_data(self):
        """Insert a set of Data.

        Returns:

        """
        # Make a connexion with a mock database
        self.generate_template()
        self.generate_workspace()
        self.generate_data_collection()

    def generate_data_collection(self):
        """Generate a Data collection.

        Returns:

        """

        content = {"root": {"element": "value2"}}

        self.data_1 = Data(template=self.template, title="Data 1", user_id="1").save()
        self.data_2 = Data(template=self.template, title="Data 2", user_id="2").save()
        self.data_3 = Data(
            template=self.template,
            title="Data 3",
            user_id="1",
            workspace=self.workspace_1.id,
            dict_content=content,
        ).save()
        self.data_4 = Data(
            template=self.template,
            title="DataDoubleTitle",
            user_id="2",
            workspace=self.workspace_2.id,
        ).save()
        self.data_5 = Data(
            template=self.template,
            title="DataDoubleTitle",
            user_id="1",
            workspace=self.workspace_1.id,
        ).save()
        self.data_collection = [
            self.data_1,
            self.data_2,
            self.data_3,
            self.data_4,
            self.data_5,
        ]

    def generate_template(self):
        """Generate an unique Template.

        Returns:

        """
        template = Template()
        template.content = get_valid_schema()
        template.hash = ""
        template.filename = "filename"
        self.template = template.save()

    def generate_workspace(self):
        """Generate the workspaces.

        Returns:

        """
        self.workspace_1 = Workspace(
            title="Workspace 1", owner="1", read_perm_id="1", write_perm_id="1"
        ).save()
        self.workspace_2 = Workspace(
            title="Workspace 2", owner="2", read_perm_id="2", write_perm_id="2"
        ).save()

    def generate_workspace_with_perm(self):
        """Generate the workspaces and the perm object.

        Returns:

        """
        try:
            self.workspace_1 = workspace_api.create_and_save("Workspace 1")
            self.workspace_2 = workspace_api.create_and_save("Workspace 2")
            self.data_3.workspace = self.workspace_1
            self.data_4.workspace = self.workspace_2
            self.data_5.workspace = self.workspace_1
        except Exception as e:
            print(e.message)
