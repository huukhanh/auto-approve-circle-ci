import requests
import time

personalToken = '4e28df029f5be5ad2ad20511299411593d12a571'
slugs = [
    'undodel/test_ci'
]
url = 'https://circleci.com/api/v2/'
headers={"Content-Type":"application/json", 'Circle-Token': personalToken}

def sendGetRequst(path, *param):
    reqUrl = url + path
    result = requests.get(reqUrl.format(*param), headers=headers)
    return result

def sendPostRequst(path, *param):
    reqUrl = url + path
    result = requests.post(reqUrl.format(*param), headers=headers)
    return result

def getAllPipeLine(slug):
    path = 'project/github/{}/pipeline'.format(slug)
    reqResult = sendGetRequst(path)
    if reqResult.status_code == 200:
        return [pipeline['id'] for pipeline in reqResult.json()['items']]
    return []

def getWorkflowByPipeline(pipelineId):
    path = 'pipeline/{}/workflow'
    reqResult = sendGetRequst(path, pipelineId)
    if reqResult.status_code == 200:
        return [{'id': pipeline['id'], 'status': pipeline['status']} for pipeline in reqResult.json()['items']]
    return []

def getWorkflowByPipelines(pipelineIds):
    workflows = []
    for pipeline in pipelineIds:
        workflows += getWorkflowByPipeline(pipeline)
    return workflows

def getJobByWorkflow(workflowId):
    path = 'workflow/{}/job'
    reqResult = sendGetRequst(path, workflowId)
    if reqResult.status_code == 200:
        return [{'workflow_id': workflowId, 'approval_request_id': workflow['approval_request_id']} for workflow in reqResult.json()['items'] if workflow['type'] == 'approval']
    return []

def getJobByWorkflows(workflowIds):
    jobs = []
    for workflowId in workflowIds:
        print(workflowId)
        jobs += getJobByWorkflow(workflowId)
    return jobs

def approvalHoldingJob(workflowId, approvalRequestId):
    path = 'workflow/{}/approve/{}'
    reqResult = sendPostRequst(path, workflowId, approvalRequestId)
    if reqResult.status_code == 200:
        print('{} was approval for build'.format(workflowId))

def approvalHoldingJobs(jobs):
    for job in jobs:
        approvalHoldingJob(job['workflow_id'], job['approval_request_id'])

def main():
    while True:
        for slug in slugs:
            try:
                print(slug)
                pipelines = getAllPipeLine(slug)
                workflows = getWorkflowByPipelines(pipelines)
                onHoldWorkflows = [workflow for workflow in workflows if workflow['status'] == 'on_hold']
                onHoldWorkflows = [workflow['id'] for workflow in onHoldWorkflows]
                jobs = getJobByWorkflows(onHoldWorkflows)
                approvalHoldingJobs(jobs)
            except:
                pass
        time.sleep(5)

main()
