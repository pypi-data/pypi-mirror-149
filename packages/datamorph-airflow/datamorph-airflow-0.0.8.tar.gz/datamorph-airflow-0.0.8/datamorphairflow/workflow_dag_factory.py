import ast
import os

from typing import Any, Dict, Optional, List

from airflow import DAG

from datamorphairflow import utils
from datamorphairflow.helper_classes import WorkflowDAG, WorkflowDAGNode
from datamorphairflow.workflow_dag_builder import WorkflowDagBuilder


class WorkflowDagFactory:
    """
    :param config_filepath: the filepath of the DAG factory JSON config file.
        Must be absolute path to file. Cannot be used with `config`.
    :type config_filepath: str
    :param config: DAG factory config dictionary. Cannot be used with `config_filepath`.
    :type config: dict
    """

    def __init__(  self, config_filepath: Optional[str] = None, config: Optional[dict] = None
                   ) -> None:
        assert bool(config_filepath) ^ bool(
            config
        ), "Either `config_filepath` or `config` should be provided"
        if config_filepath:
            WorkflowDagFactory._validate_config_filepath(config_filepath=config_filepath)
            self.config: Dict[str, Any] = WorkflowDagFactory._load_config(
                config_filepath=config_filepath
            )
            self
        if config:
            self.config: Dict[str, Any] = config

    @staticmethod
    def _validate_config_filepath(config_filepath: str) -> None:
        """
        Validates config file path is absolute
        """
        if not os.path.isabs(config_filepath):
            raise Exception("DAG Factory `config_filepath` must be absolute path")

    @staticmethod
    def _load_config(config_filepath: str) -> Dict[str, Any]:
        """
        Loads JSON config file to dictionary. Substitute variables if any.
        :returns: dict from JSON config file
        """
        # pylint: disable=consider-using-with
        try:
            config: Dict[str, Any] = utils.load_json_config_file(config_filepath)

        except Exception as err:
            raise Exception("Invalid Workflow DAG config file") from err

        return config

    def get_default_config(self) -> Dict[str, Any]:
        """
        Returns all the config elements excluding workflow as workflow contains task specific parameters.
        Typical DAG specific config elements include dag_id, description, schedule_interval etc.

        :returns: dict with default configuration to create dag
        """
        config_elems = self.config
        utils.remove_keys(config_elems, ["workflow","variables"])
        return config_elems

    def get_workflow_nodes(self) -> List[WorkflowDAGNode]:
        nodelist = []
        try:
            workflow = self.config["workflow"]
            for node in ast.literal_eval(str(workflow)):
                properties = node.get("properties")
                description = node.get("description")
                name = node.get('name')
                type = node.get('type')
                nodetype = node.get('nodeType')
                # all nodes may not have depends on
                dependson = properties.get("dependsOn","")
                # only for trigger type there will not be any dependsOn as of now
                eachNode = WorkflowDAGNode(name, description, type, nodetype, dependson, utils.remove_key(properties, "dependsOn"))
                nodelist.append(eachNode)

        except Exception as err:
            raise Exception("Invalid Workflow DAG config file") from err

        return nodelist


    def create_dag(self) -> WorkflowDAG:
        """
        Creates DAG using the config file
        :return: DAG
        """
        workflow_node_list = self.get_workflow_nodes()
        default_config = self.get_default_config()
        dag_name = self.config["dag_id"]
        workflow_dag_builder: WorkflowDagBuilder = WorkflowDagBuilder(
            dag_name=dag_name,
            dag_config=default_config,
            default_config={},
            workflow_nodes=workflow_node_list)
        try:
            dag_with_name: WorkflowDAG = workflow_dag_builder.build()
        except Exception as err:
            raise Exception(
                f"Failed to generate dag {dag_name}. verify config is correct"
            ) from err
        return dag_with_name


    @staticmethod
    def register_dag(dag_id: str, dag: DAG, globals: Dict[str, Any]) -> None:
        """Adds `dags` to `globals` so Airflow can discover them.
        :param: dags_id: Name of the DAG to be registered.
        :param: dags: DAG to be registered.
        :param globals: The globals() from the file used to generate DAGs. The dag_id
            must be passed into globals() for Airflow to import
        """
        globals[dag_id]: DAG = dag

    def generate_dags(self, globals: Dict[str, Any]) -> None:
        """
        Generates DAGs from JSON config
        :param globals: The globals() from the file used to generate DAGs. The dag_id
            must be passed into globals() for Airflow to import
        """
        dag: WorkflowDAG = self.create_dag()
        self.register_dag(dag.dagid, dag.dag, globals)


