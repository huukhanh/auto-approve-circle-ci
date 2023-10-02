import requests
import time

# Personal access token for CircleCI API authentication
personalToken = '4e28df029f5be5ad2ad20511299411593d12a571'

# List of repository slugs (in the format 'owner/repo') to monitor
slugs = ['undodel/test_ci']

# Base URL for the CircleCI API
url = 'https://circleci.com/api/v2/'

# Headers for the HTTP requests
headers = {"Content-Type": "application/json", 'Circle-Token': personalToken}


# Function to send a GET request to the CircleCI API
def sendGetRequst(path, *param):
    reqUrl = url + path
    result = requests.get(reqUrl.format(*param), headers=headers)
    return result


# Function to send a POST request to the CircleCI API
def sendPostRequst(path, *param):
    reqUrl = url + path
    result = requests.post(reqUrl.format(*param), headers=headers)
    return result


# Function to retrieve all pipeline IDs for a given repository slug
def getAllPipeLine(slug):
    path = 'project/github/{}/pipeline'.format(slug)
    reqResult = sendGetRequst(path)
    if reqResult.status_code == 200:
        return [pipeline['id'] for pipeline in reqResult.json()['items']]
    return []


# Function to retrieve workflow information for a specific pipeline
def getWorkflowByPipeline(pipelineId):
    path = 'pipeline/{}/workflow'
    reqResult = sendGetRequst(path, pipelineId)
    if reqResult.status_code == 200:
        return [{'id': pipeline['id'], 'status': pipeline['status']} for pipeline in reqResult.json()['items']]
    return []


# Function to retrieve workflow information for multiple pipelines
def getWorkflowByPipelines(pipelineIds):
    workflows = []
    for pipeline in pipelineIds:
        workflows += getWorkflowByPipeline(pipeline)
    return workflows


# Function to retrieve job information for a specific workflow
def getJobByWorkflow(workflowId):
    path = 'workflow/{}/job'
    reqResult = sendGetRequst(path, workflowId)
    if reqResult.status_code == 200:
        return [{'workflow_id': workflowId, 'approval_request_id': workflow['approval_request_id']} for workflow in reqResult.json()['items'] if workflow['type'] == 'approval']
    return []


# Function to retrieve job information for multiple workflows
def getJobByWorkflows(workflowIds):
    jobs = []
    for workflowId in workflowIds:
        print(workflowId)
        jobs += getJobByWorkflow(workflowId)
    return jobs


# Function to approve jobs that are on hold
def approvalHoldingJob(workflowId, approvalRequestId):
    path = 'workflow/{}/approve/{}'
    reqResult = sendPostRequst(path, workflowId, approvalRequestId)
    if reqResult.status_code == 200:
        print('{} was approved for build'.format(workflowId))


# Function to approve jobs that are on hold for multiple workflows
def approvalHoldingJobs(jobs):
    for job in jobs:
        approvalHoldingJob(job['workflow_id'], job['approval_request_id'])


# Main function to continuously monitor and approve on-hold jobs
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


# Entry point of the script
if __name__ == "__main__":
    main()
