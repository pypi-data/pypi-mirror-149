# fsai-awrp
Library that helps an application report progress to Argo Workflows.


## Installation 
```shell
pip install fsai-awrp
```

## Usage
Set the environment variable and run your application:
`ARGO_PROGRESS_FILE=/tmp/progress.txt`

```shell
from fsai_awrp.fsai_awrp import ArgoWorkflowsReportProgress

awrp = ArgoWorkflowsReportProgress()
awrp.set_total_progress(100)
awrp.set_current_progress(20)
awrp.start_reporting()
```