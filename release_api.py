import os
import gitlab
from datetime import datetime

if __name__ == '__main__':
    # TODO: set by protected enviroment variable 
    access_token = os.environ['RELEASE_TOKEN']

    gitlab_url = os.environ['GITLAB_URL']

    project_id = int(os.environ['CI_PROJECT_ID'])
    
    # TODO: need to automate generate these tags in the CI pipeline. 
    tag_name = os.environ['CI_PIPELINE_ID']
    ref = os.environ['CI_COMMIT_REF_NAME']
    
    # artifactory_links
    artifactory_link = os.environ['ARTIFACTORY_PATH']
    group_name = os.environ['GROUP_NAME']
    project_name = os.environ['CI_PROJECT_NAME']
    directory = f'{datetime.now():%Y%m%d}'
    artifact_name = os.environ['ARTIFACT_NAME']
    package_type = os.environ['PACKAGE_TYPE']
    
    # artifacts_links
    artifacts_links = f'{artifactory_link}/{group_name}/{project_name}/{directory}/{artifact_name}-{tag_name}.{package_type}'
    
    # release note
    release_note = os.environ['RELEASE_NOTE']

    # authenticate with gitlab
    gl = gitlab.Gitlab(gitlab_url, private_token=access_token)
    gl.auth()

    # obtain the project object by id
    project = gl.projects.get(project_id)

    # creating the project tags
    project.tags.create({'tag_name': tag_name, 'ref': ref})

    # creating the project releases
    release = project.releases.create(
        {
            'name': f'Release for Pipeline ID {ref}',
            'tag_name': tag_name,
            'description': release_note,
            'assets': {
                'links': [{'name': artifact_name, 'url': artifacts_links}],
            }
        }
    )