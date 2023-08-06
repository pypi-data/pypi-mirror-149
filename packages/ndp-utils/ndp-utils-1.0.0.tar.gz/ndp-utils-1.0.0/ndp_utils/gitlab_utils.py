from typing import List, Dict

import gitlab
import sys

import os


class GitlabCIVars:
    """
    Contient toutes les variable exposé lors d'un job Gitlab
    https://docs.gitlab.com/ee/ci/variables/predefined_variables.html
    """
    
    def __init__(self, environ: Dict[str, str]=None):
        self.environ = environ or dict(os.environ)

    @property
    def CHAT_CHANNEL(self):
        # 10.6 	all 	The Source chat channel that triggered the ChatOps command.return
        return self.environ.get("CHAT_CHANNEL", "")

    @property
    def CHAT_INPUT(self):
        # 10.6 	all 	The additional arguments passed with the ChatOps command.
        return self.environ.get("CHAT_INPUT", "")

    @property
    def CHAT_USER_ID(self):
        # 14.4 	all 	The chat service’s user ID of the user who triggered the ChatOps command.
        return self.environ.get("CHAT_USER_ID", "")

    @property
    def CI(self):
        # all 	0.4 	Available for all jobs executed in CI/CD. true when available.
        return self.environ.get("CI", "")

    @property
    def CI_API_V4_URL(self):
        # 11.7 	all 	The GitLab API v4 root URL.
        return self.environ.get("CI_API_V4_URL", "")

    @property
    def CI_BUILDS_DIR(self):
        # all 	11.10 	The top-level directory where builds are executed.
        return self.environ.get("CI_BUILDS_DIR", "")

    @property
    def CI_COMMIT_AUTHOR(self):
        # 13.11 	all 	The author of the commit in Name <email> format.
        return self.environ.get("CI_COMMIT_AUTHOR", "")

    @property
    def CI_COMMIT_BEFORE_SHA(self):
        # 11.2 	all 	The previous latest commit present on a branch. Is always 0000000000000000000000000000000000000000 in merge request pipelines.
        return self.environ.get("CI_COMMIT_BEFORE_SHA", "")

    @property
    def CI_COMMIT_BRANCH(self):
        # 12.6 	0.5 	The commit branch name. Available in branch pipelines, including pipelines for the default branch. Not available in merge request pipelines or tag pipelines.
        return self.environ.get("CI_COMMIT_BRANCH", "")

    @property
    def CI_COMMIT_DESCRIPTION(self):
        # 10.8 	all 	The description of the commit. If the title is shorter than 100 characters, the message without the first line.
        return self.environ.get("CI_COMMIT_DESCRIPTION", "")

    @property
    def CI_COMMIT_MESSAGE(self):
        # 10.8 	all 	The full commit message.
        return self.environ.get("CI_COMMIT_MESSAGE", "")

    @property
    def CI_COMMIT_REF_NAME(self):
        # 9.0 	all 	The branch or tag name for which project is built.
        return self.environ.get("CI_COMMIT_REF_NAME", "")

    @property
    def CI_COMMIT_REF_PROTECTED(self):
        # 11.11 	all 	true if the job is running for a protected reference.
        return self.environ.get("CI_COMMIT_REF_PROTECTED", "")

    @property
    def CI_COMMIT_REF_SLUG(self):
        # 9.0 	all 	CI_COMMIT_REF_NAME in lowercase, shortened to 63 bytes, and with everything except 0-9 and a-z replaced with -. No leading / trailing -. Use in URLs, host names and domain names.
        return self.environ.get("CI_COMMIT_REF_SLUG", "")

    @property
    def CI_COMMIT_SHA(self):
        # 9.0 	all 	The commit revision the project is built for.
        return self.environ.get("CI_COMMIT_SHA", "")

    @property
    def CI_COMMIT_SHORT_SHA(self):
        # 11.7 	all 	The first eight characters of CI_COMMIT_SHA.
        return self.environ.get("CI_COMMIT_SHORT_SHA", "")

    @property
    def CI_COMMIT_TAG(self):
        # 9.0 	0.5 	The commit tag name. Available only in pipelines for tags.
        return self.environ.get("CI_COMMIT_TAG", "")

    @property
    def CI_COMMIT_TIMESTAMP(self):
        # 13.4 	all 	The timestamp of the commit in the ISO 8601 format.
        return self.environ.get("CI_COMMIT_TIMESTAMP", "")

    @property
    def CI_COMMIT_TITLE(self):
        # 10.8 	all 	The title of the commit. The full first line of the message.
        return self.environ.get("CI_COMMIT_TITLE", "")

    @property
    def CI_CONCURRENT_ID(self):
        # all 	11.10 	The unique ID of build execution in a single executor.
        return self.environ.get("CI_CONCURRENT_ID", "")

    @property
    def CI_CONCURRENT_PROJECT_ID(self):
        # all 	11.10 	The unique ID of build execution in a single executor and project.
        return self.environ.get("CI_CONCURRENT_PROJECT_ID", "")

    @property
    def CI_CONFIG_PATH(self):
        # 9.4 	0.5 	The path to the CI/CD configuration file. Defaults to .gitlab-ci.yml. Read-only inside a running pipeline.
        return self.environ.get("CI_CONFIG_PATH", "")

    @property
    def CI_DEBUG_TRACE(self):
        # all 	1.7 	true if debug logging (tracing) is enabled.
        return self.environ.get("CI_DEBUG_TRACE", "")

    @property
    def CI_DEFAULT_BRANCH(self):
        # 12.4 	all 	The name of the project’s default branch.
        return self.environ.get("CI_DEFAULT_BRANCH", "")

    @property
    def CI_DEPENDENCY_PROXY_GROUP_IMAGE_PREFIX(self):
        # 13.7 	all 	The top-level group image prefix for pulling images through the Dependency Proxy.
        return self.environ.get("CI_DEPENDENCY_PROXY_GROUP_IMAGE_PREFIX", "")

    @property
    def CI_DEPENDENCY_PROXY_DIRECT_GROUP_IMAGE_PREFIX(self):
        # 14.3 	all 	The direct group image prefix for pulling images through the Dependency Proxy.
        return self.environ.get("CI_DEPENDENCY_PROXY_DIRECT_GROUP_IMAGE_PREFIX", "")

    @property
    def CI_DEPENDENCY_PROXY_PASSWORD(self):
        # 13.7 	all 	The password to pull images through the Dependency Proxy.
        return self.environ.get("CI_DEPENDENCY_PROXY_PASSWORD", "")

    @property
    def CI_DEPENDENCY_PROXY_SERVER(self):
        # 13.7 	all 	The server for logging in to the Dependency Proxy. This is equivalent to $CI_SERVER_HOST:$CI_SERVER_PORT.
        return self.environ.get("CI_DEPENDENCY_PROXY_SERVER", "")

    @property
    def CI_DEPENDENCY_PROXY_USER(self):
        # 13.7 	all 	The username to pull images through the Dependency Proxy.
        return self.environ.get("CI_DEPENDENCY_PROXY_USER", "")

    @property
    def CI_DEPLOY_FREEZE(self):
        # 13.2 	all 	Only available if the pipeline runs during a deploy freeze window. true when available.
        return self.environ.get("CI_DEPLOY_FREEZE", "")

    @property
    def CI_DEPLOY_PASSWORD(self):
        # 10.8 	all 	The authentication password of the GitLab Deploy Token, if the project has one.
        return self.environ.get("CI_DEPLOY_PASSWORD", "")

    @property
    def CI_DEPLOY_USER(self):
        # 10.8 	all 	The authentication username of the GitLab Deploy Token, if the project has one.
        return self.environ.get("CI_DEPLOY_USER", "")

    @property
    def CI_DISPOSABLE_ENVIRONMENT(self):
        # all 	10.1 	Only available if the job is executed in a disposable environment (something that is created only for this job and disposed of/destroyed after the execution - all executors except shell and ssh). true when available.
        return self.environ.get("CI_DISPOSABLE_ENVIRONMENT", "")

    @property
    def CI_ENVIRONMENT_NAME(self):
        # 8.15 	all 	The name of the environment for this job. Available if environment:name is set.
        return self.environ.get("CI_ENVIRONMENT_NAME", "")

    @property
    def CI_ENVIRONMENT_SLUG(self):
        # 8.15 	all 	The simplified version of the environment name, suitable for inclusion in DNS, URLs, Kubernetes labels, and so on. Available if environment:name is set. The slug is truncated to 24 characters.
        return self.environ.get("CI_ENVIRONMENT_SLUG", "")

    @property
    def CI_ENVIRONMENT_URL(self):
        # 9.3 	all 	The URL of the environment for this job. Available if environment:url is set.
        return self.environ.get("CI_ENVIRONMENT_URL", "")

    @property
    def CI_ENVIRONMENT_ACTION(self):
        # 13.11 	all 	The action annotation specified for this job’s environment. Available if environment:action is set. Can be start, prepare, or stop.
        return self.environ.get("CI_ENVIRONMENT_ACTION", "")

    @property
    def CI_ENVIRONMENT_TIER(self):
        # 14.0 	all 	The deployment tier of the environment for this job.
        return self.environ.get("CI_ENVIRONMENT_TIER", "")

    @property
    def CI_HAS_OPEN_REQUIREMENTS(self):
        # 13.1 	all 	Only available if the pipeline’s project has an open requirement. true when available.
        return self.environ.get("CI_HAS_OPEN_REQUIREMENTS", "")

    @property
    def CI_JOB_ID(self):
        # 9.0 	all 	The internal ID of the job, unique across all jobs in the GitLab instance.
        return self.environ.get("CI_JOB_ID", "")

    @property
    def CI_JOB_IMAGE(self):
        # 12.9 	12.9 	The name of the Docker image running the job.
        return self.environ.get("CI_JOB_IMAGE", "")

    @property
    def CI_JOB_JWT(self):
        # 12.10 	all 	A RS256 JSON web token to authenticate with third party systems that support JWT authentication, for example HashiCorp’s Vault.
        return self.environ.get("CI_JOB_JWT", "")

    @property
    def CI_JOB_JWT_V1(self):
        # 14.6 	all 	The same value as CI_JOB_JWT.
        return self.environ.get("CI_JOB_JWT_V1", "")

    @property
    def CI_JOB_JWT_V2(self):
        # 14.6 	all 	alpha: A newly formatted RS256 JSON web token to increase compatibility. Similar to CI_JOB_JWT, except the issuer (iss) claim is changed from gitlab.com to https://gitlab.com, sub has changed from job_id to a string that contains the project path, and an aud claim is added. Format is subject to change. Be aware, the aud field is a constant value. Trusting JWTs in multiple relying parties can lead to one RP sending a JWT to another one and acting maliciously as a job.
        return self.environ.get("CI_JOB_JWT_V2", "")

    @property
    def CI_JOB_MANUAL(self):
        # 8.12 	all 	true if a job was started manually.
        return self.environ.get("CI_JOB_MANUAL", "")

    @property
    def CI_JOB_NAME(self):
        # 9.0 	0.5 	The name of the job.
        return self.environ.get("CI_JOB_NAME", "")

    @property
    def CI_JOB_STAGE(self):
        # 9.0 	0.5 	The name of the job’s stage.
        return self.environ.get("CI_JOB_STAGE", "")

    @property
    def CI_JOB_STATUS(self):
        # all 	13.5 	The status of the job as each runner stage is executed. Use with after_script. Can be success, failed, or canceled.
        return self.environ.get("CI_JOB_STATUS", "")

    @property
    def CI_JOB_TOKEN(self):
        # 9.0 	1.2 	A token to authenticate with certain API endpoints. The token is valid as long as the job is running.
        return self.environ.get("CI_JOB_TOKEN", "")

    @property
    def CI_JOB_URL(self):
        # 11.1 	0.5 	The job details URL.
        return self.environ.get("CI_JOB_URL", "")

    @property
    def CI_JOB_STARTED_AT(self):
        # 13.10 	all 	The UTC datetime when a job started, in ISO 8601 format.
        return self.environ.get("CI_JOB_STARTED_AT", "")

    @property
    def CI_KUBERNETES_ACTIVE(self):
        # 13.0 	all 	Only available if the pipeline has a Kubernetes cluster available for deployments. true when available.
        return self.environ.get("CI_KUBERNETES_ACTIVE", "")

    @property
    def CI_NODE_INDEX(self):
        # 11.5 	all 	The index of the job in the job set. Only available if the job uses parallel.
        return self.environ.get("CI_NODE_INDEX", "")

    @property
    def CI_NODE_TOTAL(self):
        # 11.5 	all 	The total number of instances of this job running in parallel. Set to 1 if the job does not use parallel.
        return self.environ.get("CI_NODE_TOTAL", "")

    @property
    def CI_OPEN_MERGE_REQUESTS(self):
        # 13.8 	all 	A comma-separated list of up to four merge requests that use the current branch and project as the merge request source. Only available in branch and merge request pipelines if the branch has an associated merge request. For example, gitlab-org/gitlab!333,gitlab-org/gitlab-foss!11.
        return self.environ.get("CI_OPEN_MERGE_REQUESTS", "")

    @property
    def CI_PAGES_DOMAIN(self):
        # 11.8 	all 	The configured domain that hosts GitLab Pages.
        return self.environ.get("CI_PAGES_DOMAIN", "")

    @property
    def CI_PAGES_URL(self):
        # 11.8 	all 	The URL for a GitLab Pages site. Always a subdomain of CI_PAGES_DOMAIN.
        return self.environ.get("CI_PAGES_URL", "")

    @property
    def CI_PIPELINE_ID(self):
        # 8.10 	all 	The instance-level ID of the current pipeline. This ID is unique across all projects on the GitLab instance.
        return self.environ.get("CI_PIPELINE_ID", "")

    @property
    def CI_PIPELINE_IID(self):
        # 11.0 	all 	The project-level IID (internal ID) of the current pipeline. This ID is unique only within the current project.
        return self.environ.get("CI_PIPELINE_IID", "")

    @property
    def CI_PIPELINE_SOURCE(self):
        # 10.0 	all 	How the pipeline was triggered. Can be push, web, schedule, api, external, chat, webide, merge_request_event, external_pull_request_event, parent_pipeline, trigger, or pipeline.
        return self.environ.get("CI_PIPELINE_SOURCE", "")

    @property
    def CI_PIPELINE_TRIGGERED(self):
        # all 	all 	true if the job was triggered.
        return self.environ.get("CI_PIPELINE_TRIGGERED", "")

    @property
    def CI_PIPELINE_URL(self):
        # 11.1 	0.5 	The URL for the pipeline details.
        return self.environ.get("CI_PIPELINE_URL", "")

    @property
    def CI_PIPELINE_CREATED_AT(self):
        # 13.10 	all 	The UTC datetime when the pipeline was created, in ISO 8601 format.
        return self.environ.get("CI_PIPELINE_CREATED_AT", "")

    @property
    def CI_PROJECT_CONFIG_PATH(self):
        # 13.8 to 13.12 	all 	Removed in GitLab 14.0. Use CI_CONFIG_PATH.
        return self.environ.get("CI_PROJECT_CONFIG_PATH", "")

    @property
    def CI_PROJECT_DIR(self):
        # all 	all 	The full path the repository is cloned to, and where the job runs from. If the GitLab Runner builds_dir parameter is set, this variable is set relative to the value of builds_dir. For more information, see the Advanced GitLab Runner configuration.
        return self.environ.get("CI_PROJECT_DIR", "")

    @property
    def CI_PROJECT_ID(self):
        # all 	all 	The ID of the current project. This ID is unique across all projects on the GitLab instance.
        return self.environ.get("CI_PROJECT_ID", "")

    @property
    def CI_PROJECT_NAME(self):
        # 8.10 	0.5 	The name of the directory for the project. For example if the project URL is gitlab.example.com/group-name/project-1, CI_PROJECT_NAME is project-1.
        return self.environ.get("CI_PROJECT_NAME", "")

    @property
    def CI_PROJECT_NAMESPACE(self):
        # 8.10 	0.5 	The project namespace (username or group name) of the job.
        return self.environ.get("CI_PROJECT_NAMESPACE", "")

    @property
    def CI_PROJECT_PATH_SLUG(self):
        # 9.3 	all 	$CI_PROJECT_PATH in lowercase with characters that are not a-z or 0-9 replaced with - and shortened to 63 bytes. Use in URLs and domain names.
        return self.environ.get("CI_PROJECT_PATH_SLUG", "")

    @property
    def CI_PROJECT_PATH(self):
        # 8.10 	0.5 	The project namespace with the project name included.
        return self.environ.get("CI_PROJECT_PATH", "")

    @property
    def CI_PROJECT_REPOSITORY_LANGUAGES(self):
        # 12.3 	all 	A comma-separated, lowercase list of the languages used in the repository. For example ruby,javascript,html,css.
        return self.environ.get("CI_PROJECT_REPOSITORY_LANGUAGES", "")

    @property
    def CI_PROJECT_ROOT_NAMESPACE(self):
        # 13.2 	0.5 	The root project namespace (username or group name) of the job. For example, if CI_PROJECT_NAMESPACE is root-group/child-group/grandchild-group, CI_PROJECT_ROOT_NAMESPACE is root-group.
        return self.environ.get("CI_PROJECT_ROOT_NAMESPACE", "")

    @property
    def CI_PROJECT_TITLE(self):
        # 12.4 	all 	The human-readable project name as displayed in the GitLab web interface.
        return self.environ.get("CI_PROJECT_TITLE", "")

    @property
    def CI_PROJECT_URL(self):
        # 8.10 	0.5 	The HTTP(S) address of the project.
        return self.environ.get("CI_PROJECT_URL", "")

    @property
    def CI_PROJECT_VISIBILITY(self):
        # 10.3 	all 	The project visibility. Can be internal, private, or public.
        return self.environ.get("CI_PROJECT_VISIBILITY", "")

    @property
    def CI_PROJECT_CLASSIFICATION_LABEL(self):
        # 14.2 	all 	The project external authorization classification label.
        return self.environ.get("CI_PROJECT_CLASSIFICATION_LABEL", "")

    @property
    def CI_REGISTRY_IMAGE(self):
        # 8.10 	0.5 	The address of the project’s Container Registry. Only available if the Container Registry is enabled for the project.
        return self.environ.get("CI_REGISTRY_IMAGE", "")

    @property
    def CI_REGISTRY_PASSWORD(self):
        # 9.0 	all 	The password to push containers to the project’s GitLab Container Registry. Only available if the Container Registry is enabled for the project. This password value is the same as the CI_JOB_TOKEN and is valid only as long as the job is running. Use the CI_DEPLOY_PASSWORD for long-lived access to the registry
        return self.environ.get("CI_REGISTRY_PASSWORD", "")

    @property
    def CI_REGISTRY_USER(self):
        # 9.0 	all 	The username to push containers to the project’s GitLab Container Registry. Only available if the Container Registry is enabled for the project.
        return self.environ.get("CI_REGISTRY_USER", "")

    @property
    def CI_REGISTRY(self):
        # 8.10 	0.5 	The address of the GitLab Container Registry. Only available if the Container Registry is enabled for the project. This variable includes a :port value if one is specified in the registry configuration.
        return self.environ.get("CI_REGISTRY", "")

    @property
    def CI_REPOSITORY_URL(self):
        # 9.0 	all 	The URL to clone the Git repository.
        return self.environ.get("CI_REPOSITORY_URL", "")

    @property
    def CI_RUNNER_DESCRIPTION(self):
        # 8.10 	0.5 	The description of the runner.
        return self.environ.get("CI_RUNNER_DESCRIPTION", "")

    @property
    def CI_RUNNER_EXECUTABLE_ARCH(self):
        # all 	10.6 	The OS/architecture of the GitLab Runner executable. Might not be the same as the environment of the executor.
        return self.environ.get("CI_RUNNER_EXECUTABLE_ARCH", "")

    @property
    def CI_RUNNER_ID(self):
        # 8.10 	0.5 	The unique ID of the runner being used.
        return self.environ.get("CI_RUNNER_ID", "")

    @property
    def CI_RUNNER_REVISION(self):
        # all 	10.6 	The revision of the runner running the job.
        return self.environ.get("CI_RUNNER_REVISION", "")

    @property
    def CI_RUNNER_SHORT_TOKEN(self):
        # all 	12.3 	First eight characters of the runner’s token used to authenticate new job requests. Used as the runner’s unique ID.
        return self.environ.get("CI_RUNNER_SHORT_TOKEN", "")

    @property
    def CI_RUNNER_TAGS(self):
        # 8.10 	0.5 	A comma-separated list of the runner tags.
        return self.environ.get("CI_RUNNER_TAGS", "")

    @property
    def CI_RUNNER_VERSION(self):
        # all 	10.6 	The version of the GitLab Runner running the job.
        return self.environ.get("CI_RUNNER_VERSION", "")

    @property
    def CI_SERVER_HOST(self):
        # 12.1 	all 	The host of the GitLab instance URL, without protocol or port. For example gitlab.example.com.
        return self.environ.get("CI_SERVER_HOST", "")

    @property
    def CI_SERVER_NAME(self):
        # all 	all 	The name of CI/CD server that coordinates jobs.
        return self.environ.get("CI_SERVER_NAME", "")

    @property
    def CI_SERVER_PORT(self):
        # 12.8 	all 	The port of the GitLab instance URL, without host or protocol. For example 8080.
        return self.environ.get("CI_SERVER_PORT", "")

    @property
    def CI_SERVER_PROTOCOL(self):
        # 12.8 	all 	The protocol of the GitLab instance URL, without host or port. For example https.
        return self.environ.get("CI_SERVER_PROTOCOL", "")

    @property
    def CI_SERVER_REVISION(self):
        # all 	all 	GitLab revision that schedules jobs.
        return self.environ.get("CI_SERVER_REVISION", "")

    @property
    def CI_SERVER_URL(self):
        # 12.7 	all 	The base URL of the GitLab instance, including protocol and port. For example https://gitlab.example.com:8080.
        return self.environ.get("CI_SERVER_URL", "")

    @property
    def CI_SERVER_VERSION_MAJOR(self):
        # 11.4 	all 	The major version of the GitLab instance. For example, if the GitLab version is 13.6.1, the CI_SERVER_VERSION_MAJOR is 13.
        return self.environ.get("CI_SERVER_VERSION_MAJOR", "")

    @property
    def CI_SERVER_VERSION_MINOR(self):
        # 11.4 	all 	The minor version of the GitLab instance. For example, if the GitLab version is 13.6.1, the CI_SERVER_VERSION_MINOR is 6.
        return self.environ.get("CI_SERVER_VERSION_MINOR", "")

    @property
    def CI_SERVER_VERSION_PATCH(self):
        # 11.4 	all 	The patch version of the GitLab instance. For example, if the GitLab version is 13.6.1, the CI_SERVER_VERSION_PATCH is 1.
        return self.environ.get("CI_SERVER_VERSION_PATCH", "")

    @property
    def CI_SERVER_VERSION(self):
        # all 	all 	The full version of the GitLab instance.
        return self.environ.get("CI_SERVER_VERSION", "")

    @property
    def CI_SERVER(self):
        # all 	all 	Available for all jobs executed in CI/CD. yes when available.
        return self.environ.get("CI_SERVER", "")

    @property
    def CI_SHARED_ENVIRONMENT(self):
        # all 	10.1 	Only available if the job is executed in a shared environment (something that is persisted across CI/CD invocations, like the shell or ssh executor). true when available.
        return self.environ.get("CI_SHARED_ENVIRONMENT", "")

    @property
    def GITLAB_CI(self):
        # all 	all 	Available for all jobs executed in CI/CD. true when available.
        return self.environ.get("GITLAB_CI", "")

    @property
    def GITLAB_FEATURES(self):
        # 10.6 	all 	The comma-separated list of licensed features available for the GitLab instance and license.
        return self.environ.get("GITLAB_FEATURES", "")

    @property
    def GITLAB_USER_EMAIL(self):
        # 8.12 	all 	The email of the user who started the job.
        return self.environ.get("GITLAB_USER_EMAIL", "")

    @property
    def GITLAB_USER_ID(self):
        # 8.12 	all 	The ID of the user who started the job.
        return self.environ.get("GITLAB_USER_ID", "")

    @property
    def GITLAB_USER_LOGIN(self):
        # 10.0 	all 	The username of the user who started the job.
        return self.environ.get("GITLAB_USER_LOGIN", "")

    @property
    def GITLAB_USER_NAME(self):
        # 10.0 	all 	The name of the user who started the job.
        return self.environ.get("GITLAB_USER_NAME", "")

    @property
    def TRIGGER_PAYLOAD(self):
        # 13.9 	all 	The webhook payload. Only available when a pipeline is triggered with a webhook.
        return self.environ.get("TRIGGER_PAYLOAD", "")


GITLAB_CI_VARS = GitlabCIVars()


def log(*args):
    print(" ".join([str(arg) for arg in args]), flush=True, file=sys.stderr)


class BranchManager:

    @staticmethod
    def try_find_suitable_branch(project: "gitlab.v4.objects.projects.Project", branch_to_try_names: List[str]):
        for branch_name in branch_to_try_names:
            if not branch_name:
                continue
            try:
                depends_branch = project.branches.get(branch_name).name
                log("Project %s: branch '%s' found" % (project.name, branch_name))
                return depends_branch
            except gitlab.GitlabGetError:
                log("Project %s: branch not found with name %s" % (project.name, branch_name))
                continue
        return project.default_branch

    @staticmethod
    def convert_ODOO_DEPENDS_to_ADDONS_GIT(gitlab_api: gitlab.Gitlab, odoo_depends: str, env_vars: Dict[str, str], default_branch_to_try_names:List[str]) -> Dict[str, str]:
        env = dict(env_vars)
        for project_name in odoo_depends.split(","):
            project = gitlab_api.projects.get(project_name)
            branch_to_try = list(default_branch_to_try_names)
            if env.get(f"ADDONS_GIT_{project_name.upper()}_BRANCH"):
                branch_to_try.insert(0, env.get(f"ADDONS_GIT_{project_name.upper()}_BRANCH"))
            branch = BranchManager.try_find_suitable_branch(project, branch_to_try_names=branch_to_try)
            env[f"ADDONS_GIT_{project_name.upper()}"] = project_name
            env[f"ADDONS_GIT_{project_name.upper()}_BRANCH"] = branch
        return env

    @staticmethod
    def try_find_branch_for_ADDONS_GIT(gitlab_api: gitlab.Gitlab, env_vars: Dict[str, str], default_branch_to_try_names:List[str]) -> Dict[str, str]:
        env = dict(env_vars)
        for project_name in odoo_depends.split(","):
            project = gitlab_api.projects.get(project_name)
            branch_to_try = list(default_branch_to_try_names)
            if env.get(f"ADDONS_GIT_{project_name.upper()}_BRANCH"):
                branch_to_try.insert(0, env.get(f"ADDONS_GIT_{project_name.upper()}_BRANCH"))
            branch = BranchManager.try_find_suitable_branch(project, branch_to_try_names=branch_to_try)
            env[f"ADDONS_GIT_{project_name.upper()}"] = project_name
            env[f"ADDONS_GIT_{project_name.upper()}_BRANCH"] = branch
        return env

    @staticmethod
    def convert_CI_VARS_to_ADDONS_GIT(vars:GitlabCIVars) -> Dict[str, str]:
        return {
            f"ADDONS_GIT_{vars.CI_PROJECT_PATH.upper()}": vars.CI_PROJECT_PATH,
            f"ADDONS_GIT_{vars.CI_PROJECT_PATH.upper()}_BRANCH": vars.CI_COMMIT_REF_NAME,
            f"ADDONS_GIT_{vars.CI_PROJECT_PATH.upper()}_PROTOCOLE": "https",
            f"ADDONS_GIT_{vars.CI_PROJECT_PATH.upper()}_HTTPS_LOGIN": vars.CI_DEPLOY_USER,
            f"ADDONS_GIT_{vars.CI_PROJECT_PATH.upper()}_HTTPS_PASSWORD": vars.CI_DEPLOY_PASSWORD or vars.CI_JOB_TOKEN,
        }

