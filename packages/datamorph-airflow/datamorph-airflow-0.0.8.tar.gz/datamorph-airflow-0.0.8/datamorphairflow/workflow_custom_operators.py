from airflow.models import BaseOperator
from airflow.operators.python import BranchPythonOperator
from airflow.providers.databricks.hooks.databricks import DatabricksHook
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from airflow.operators.bash import BashOperator


class DMStartDatabricksClusterOperator(BaseOperator):
    def __init__(
            self, cluster_id:str, databricks_conn_id: str = "kwartile_databricks", **kwargs
    ):

        super().__init__(**kwargs)
        self.databricks_conn_id = databricks_conn_id
        self.cluster_id=cluster_id

    def execute(self, context):
        databricks_hook = DatabricksHook(databricks_conn_id=self.databricks_conn_id)
        responds = databricks_hook._do_api_call(
            ("POST", "api/2.0/clusters/start"), {"cluster_id": self.cluster_id}
        )
        return responds

class DMTerminateDatabricksClusterOperator(BaseOperator):
    def __init__(
            self, cluster_id:str, databricks_conn_id: str = "kwartile_databricks", **kwargs
    ):

        super().__init__(**kwargs)
        self.databricks_conn_id = databricks_conn_id
        self.cluster_id=cluster_id

    def execute(self, context):
        databricks_hook = DatabricksHook(databricks_conn_id=self.databricks_conn_id)
        responds = databricks_hook._do_api_call(
            ("POST", "api/2.0/clusters/terminate"), {"cluster_id": self.cluster_id}
        )
        return responds

class DMDatabricksRunNowJobOperator(DatabricksRunNowOperator):
    def __init__(
            self, *args, **kwargs
    ):

        super().__init__(do_xcom_push=True, *args, **kwargs)
        #self.databricks_conn_id = databricks_conn_id

    def execute(self, context):
        super(self).execute(context)
        databricks_hook = DatabricksHook(databricks_conn_id=self.databricks_conn_id)
        run_id = context["task_instance"].xcom_pull(self.task_id, key="run_id")
        self.log.info(run_id)
        self.log.info(self.run_id)
        result = databricks_hook.get_run_state_result(self.run_id)
        self.log.info("Result:")
        self.log.info(result)
        context['ti'].xcom_push(key='status',value=result)
        return result

class DMRunJavaJarOperator(BashOperator):
    def __init__(
            self,
            jarpath: str,
            classname: str,
            arguments: str,
            systemparams: str = "",
            *args,
            **kwargs
    ):
        cmd = 'java -cp ' + jarpath + ' ' + systemparams + " " + classname + " " + arguments
        super().__init__(bash_command=cmd, *args, **kwargs)
        self.jarpath = jarpath
        self.classname = classname
        self.arguments = arguments
        self.systemparams = systemparams

class DMBranchOnReturnValueOperator(BranchPythonOperator):
    def __init__(
            self,
            branches,
            parenttask,
            *args,
            **kwargs
    ):
        super().__init__(python_callable=branch_onret_val,
                         op_kwargs={'branches': branches, 'parenttask': parenttask},
                         provide_context=True, *args, **kwargs)



# todo multiple dependson ..now only with one
def branch_onret_val(ti,**kwargs):
    print(kwargs["branches"])
    branches = kwargs["branches"]
    dependsOn = kwargs["parenttask"][0]
    returnBranchList = []
    print(dependsOn)
    for node in branches:
        print(node)
        if "variable" in node:
            variable = node["variable"]
        else:
            variable = "return_value"
        print(variable)
        match = node["match"]
        print(match)
        branch = node["branch"]
        print(branch)
        returnValue = ti.xcom_pull(key=variable, task_ids=[dependsOn])[0]
        print(returnValue)
        if returnValue.lower() == match.lower():
            returnBranchList.append(branch)
            print(branch)
    print(returnBranchList)
    return returnBranchList