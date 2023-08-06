import os
import json
import tornado.web
from typing import Union
from jupyter_server.utils import url_path_join
from jupyter_server.base.handlers import APIHandler
from epi2melabs_wfpage.config import Epi2melabsWFPage
from epi2melabs.workflows.launcher import get_workflow_launcher


class LauncherAPIHandler(APIHandler):

    def __init__(self, application, request, launcher, **kwargs):
        super().__init__(application, request, **kwargs)
        self.launcher = launcher


class Workflows(LauncherAPIHandler):

    @tornado.web.authenticated
    def get(self, name: Union[str, None] = None) -> None:
        """Get workflow(s)"""
        if not name:
            self.finish(json.dumps(
                self.launcher.workflows))
            return

        workflow = self.launcher.get_workflow(name)
        self.finish(json.dumps(workflow))


class Cwd(LauncherAPIHandler):

    @tornado.web.authenticated
    def get(self) -> None:
        """Get current working dir"""
        self.finish(json.dumps({
            'curr_dir': os.getcwd(),
            'base_dir': self.launcher.base_dir}
        ))


class Path(LauncherAPIHandler):

    @tornado.web.authenticated
    def get(self, path) -> None:
        """Get path"""
        self.finish(json.dumps(
            self.launcher.get_path(path)
        ))


class File(LauncherAPIHandler):

    @tornado.web.authenticated
    def get(self, path) -> None:
        """Get file"""
        self.finish(json.dumps(
            self.launcher.get_file(
                path,
                contents=self.get_argument("contents", None, True)
            )))


class Directory(LauncherAPIHandler):

    @tornado.web.authenticated
    def get(self, path) -> None:
        """Get directory"""
        self.finish(json.dumps(
            self.launcher.get_directory(
                path,
                contents=self.get_argument("contents", None, True)
            )))


class Instance(LauncherAPIHandler):

    @tornado.web.authenticated
    def get(self, instance_id: Union[str, None] = None) -> None:
        """Get workflow instance(s)"""
        if instance_id:
            self.finish(json.dumps(
                self.launcher.get_instance(instance_id)
            ))
            return

        payload = self.get_json_body() or {}
        all_instances = self.launcher.instances

        if instance_ids := payload.get('instances'):
            self.finish(json.dumps({
                    k: v for (k, v) in x.items()
                    if k in instance_ids
                } for x in all_instances
            ))
            return

        self.finish(json.dumps(all_instances))

    @tornado.web.authenticated
    def post(self) -> None:
        """Create a new instance"""
        payload = self.get_json_body()

        if not payload:
            self.finish(json.dumps({}))
            return

        name = payload['name']
        wf_name = payload['workflow']
        params = payload['params']

        instanceresp = self.launcher.create_instance(
            name, wf_name, params)

        self.finish(json.dumps(instanceresp))

    @tornado.web.authenticated
    def delete(self, instance_id: Union[str, None] = None) -> None:
        """Create a new instance"""
        if not instance_id:
            self.finish(json.dumps({'deleted': False}))
            return

        payload = self.get_json_body() or {}

        self.launcher.delete_instance(
            instance_id, delete=payload.get('delete', False))
        self.finish(json.dumps({'deleted': True}))


def setup_handlers(web_app):
    host_pattern = ".*$"
    base_url = web_app.settings["base_url"]
    epi2melabs_wfpage = "epi2melabs-wfpage"

    # Create the launcher
    config = Epi2melabsWFPage(
        config=web_app.settings['config_manager'].config)

    launcher = {'launcher': get_workflow_launcher(
        base_dir=config.base_dir, workflows_dir=config.workflows_dir,
        remote=config.remote, ip=config.ip, port=config.port)}

    # Workflow get
    workflow_pattern = url_path_join(
        base_url, epi2melabs_wfpage, r"workflows/([-A-Za-z0-9]+)")
    workflows_pattern = url_path_join(
        base_url, epi2melabs_wfpage, r"workflows/?")

    # Instance crd
    instance_pattern = url_path_join(
        base_url, epi2melabs_wfpage, r"instances/([-A-Za-z0-9]+)")
    instances_pattern = url_path_join(
        base_url, epi2melabs_wfpage, r"instances/?")

    # Filesystem
    cwd_pattern = url_path_join(
        base_url, epi2melabs_wfpage, r"cwd/?")
    path_pattern = url_path_join(
        base_url, epi2melabs_wfpage, r"path/([-A-Za-z0-9_%.]+)")
    file_pattern = url_path_join(
        base_url, epi2melabs_wfpage, r"file/([-A-Za-z0-9_%.]+)")
    directory_pattern = url_path_join(
        base_url, epi2melabs_wfpage, r"directory/([-A-Za-z0-9_%.]+)")

    handlers = [
        (cwd_pattern, Cwd, launcher),
        (path_pattern, Path, launcher),
        (file_pattern, File, launcher),
        (directory_pattern, Directory, launcher),
        (workflow_pattern, Workflows, launcher),
        (workflows_pattern, Workflows, launcher),
        (instance_pattern, Instance, launcher),
        (instances_pattern, Instance, launcher)
    ]

    web_app.add_handlers(host_pattern, handlers)
