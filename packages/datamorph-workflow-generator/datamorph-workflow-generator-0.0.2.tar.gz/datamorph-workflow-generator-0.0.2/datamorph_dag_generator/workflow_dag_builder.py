from copy import deepcopy
from typing import Dict, Any, List, Callable

from airflow import DAG
from airflow.models import BaseOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.utils.module_loading import import_string

from workflow_dag_generator.helper_classes import WorkflowDAGNode, WorkflowDAG

from workflow_dag_generator import utils


class WorkflowDagBuilder:
    """
    Generates tasks and a DAG from a config.
    :param dag_name: the name of the DAG
    :param dag_config: a dictionary containing configuration for the DAG
    :param default_config: a dictitionary containing defaults for all DAGs
    """

    def __init__(
            self, dag_name: str, dag_config: Dict[str, Any], default_config: Dict[str, Any], workflow_nodes: List[WorkflowDAGNode]
    ) -> None:
        self.dag_name: str = dag_name
        self.dag_config: Dict[str, Any] = deepcopy(dag_config)
        self.default_config: Dict[str, Any] = deepcopy(default_config)
        self.workflow_nodes: List[WorkflowDAGNode] = deepcopy(workflow_nodes)


    def get_dag_params(self) -> Dict[str, Any]:
        """
        Check all the default parameters for DAGs and validate the type.
        TBD
        :return:
        """
        return self.dag_config

    @staticmethod
    def create_task(node: WorkflowDAGNode, dag: DAG) -> BaseOperator:
        """
        create task using the information from node and returns an instance of the Airflow BaseOperator
        :param dag:
        :return: instance of operator object
        """
        operator = node.type
        task_params = node.taskparams
        task_params["task_id"] = node.name
        task_params["dag"]=dag
        try:
            operator_obj: Callable[..., BaseOperator] = import_string(operator)
        except Exception as err:
            raise Exception(f"Failed to import operator: {operator}") from err
        try:
            # check for PythonOperator and get Python Callable from the
            # function name and python file with the function.
            if operator_obj in [PythonOperator, BranchPythonOperator]:
                if (
                        not task_params.get("python_callable_name")
                        and not task_params.get("python_callable_file")
                ):
                    raise Exception(
                        "Failed to create task. PythonOperator and BranchPythonOperator requires \
                        `python_callable_name` and `python_callable_file` parameters"
                    )
                if not task_params.get("python_callable"):
                    task_params[
                        "python_callable"
                    ]: Callable = utils.get_python_callable(
                        task_params["python_callable_name"],
                        task_params["python_callable_file"],
                    )
                    # remove DataMorph specific parameters
                    del task_params["python_callable_name"]
                    del task_params["python_callable_file"]


            # create task  from the base operator object with all the task params
            task: BaseOperator = operator_obj(**task_params)
        except Exception as err:
            raise Exception(f"Failed to create {operator_obj} task") from err
        return task




    def build(self) -> WorkflowDAG:
        """
        Generates a DAG from the dag parameters
        step 1: iterate through all the nodes in list of WorkflowDAGNode
        step 2: create task for each node
        step 3: set upstream based on the depends on criteria
        step 4: return dag with the dag name as WorkflowDAG object
        :return:
        """

        dag_kwargs = self.dag_config
        dag: DAG = DAG(**dag_kwargs)

        # workflow dictionary to maintain node name and Task as Airflow BaseOpertaor
        workflow_dict = {}

        for node in self.workflow_nodes:
            print(node)
            dependsOn = node.dependson
            dependsOnList = []
            name = node.name
            workflow_dict[name] = WorkflowDagBuilder.create_task(node, dag)
            if dependsOn is not None:
                baseOperator = workflow_dict[name]
                for eachDependsOn in dependsOn:
                    dependsOnList.append(workflow_dict[eachDependsOn])
                print(dependsOnList)
                baseOperator.set_upstream(dependsOnList)
        return WorkflowDAG(self.dag_name, dag)



