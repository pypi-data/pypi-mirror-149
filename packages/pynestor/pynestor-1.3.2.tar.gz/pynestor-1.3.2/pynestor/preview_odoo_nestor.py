import base64
import collections.abc
import os
import sys
import time
from datetime import date

import gitlab
from kubernetes import client, config
from minio import Minio

######################################
# Python wrapping nestor
######################################
from .pynestor import (
    NestorDescSet,
    NestorGitDesc,
    NestorOpt,
    ScriptNestorInstance,
    Utils,
)

CURRENT_PATH = os.path.expanduser(os.path.abspath(os.path.curdir))


class EnvironementConfig:
    def __init__(self, base_env_vars=None):
        base_env_vars = dict(base_env_vars or {}, **os.environ)
        self.NESTOR_NAME = base_env_vars.get("NESTOR_NAME") or base_env_vars.get("CI_COMMIT_REF_SLUG")
        self.NESTOR_NAME_PREFIX = base_env_vars.get("NESTOR_NAME_PREFIX")
        self.ALWAYS_DELETE = base_env_vars.get("ALWAYS_DELETE")
        self.CI_COMMIT_REF_NAME = base_env_vars.get("CI_COMMIT_REF_NAME")
        self.CI_PROJECT_DIR = base_env_vars.get("CI_PROJECT_DIR")
        self.CI_PROJECT_PATH = base_env_vars.get("CI_PROJECT_PATH")
        self.GITLAB_TOKEN = base_env_vars.get("GITLAB_TOKEN")
        self.ODOO_VERSION = base_env_vars.get("ODOO_VERSION")
        self.S3_SECRET_PREVIEW = base_env_vars.get("S3_SECRET_PREVIEW")
        self.S3_DUMP_SECRET = base_env_vars.get("S3_DUMP_SECRET")
        self.S3_DUMP_BUCKET = base_env_vars.get("S3_DUMP_BUCKET")
        self.VERBOSE = bool(base_env_vars.get("VERBOSE"))
        self.DATE = base_env_vars.get("DATE")
        self.S3_BUCKET = base_env_vars.get("S3_BUCKET")
        self.PROD_INSTANCE_NAME = base_env_vars.get("PROD_INSTANCE_NAME") or base_env_vars.get("CI_PROJECT_NAME")
        self.DB_NAME = base_env_vars.get("DB_NAME")
        self.ODOO_DEPENDS = base_env_vars.get("ODOO_DEPENDS")
        self.DUMP_PATH = base_env_vars.get("PATH_DUMP")
        self.NESTOR_CFG_FILENAME = os.environ.get("NESTOR_CFG_FILENAME", ".nestor-cfg.yml")
        self.BASE_MODULE_UPDATE = os.environ.get("BASE_MODULE_UPDATE", "all")

    def apply_default(self):

        self.CI_PROJECT_PATH = self.CI_PROJECT_PATH or CURRENT_PATH
        self.S3_SECRET_PREVIEW = self.S3_SECRET_PREVIEW or "s3-ndp-preview"
        self.S3_DUMP_SECRET = self.S3_DUMP_SECRET or "s3-ndp-scaleway"
        self.S3_DUMP_BUCKET = self.S3_DUMP_BUCKET or "ndp-production-backups"
        self.DATE = self.DATE or date.today().isoformat()
        self.S3_BUCKET = "ndp-preview-" + (self.S3_BUCKET or self.NESTOR_NAME)
        self.DB_NAME = self.DB_NAME or self.PROD_INSTANCE_NAME
        self.ODOO_DEPENDS = self.ODOO_DEPENDS or "odoo-addons/common-modules,odoo-addons/community-addons"
        dump_path_fmt = "%(PROD_INSTANCE_NAME)s/journaliere/%(DB_NAME)s_%(DATE)s.dump"
        self.DUMP_PATH = (self.DUMP_PATH or dump_path_fmt) % {
            "PROD_INSTANCE_NAME": self.PROD_INSTANCE_NAME,
            "DB_NAME": self.DB_NAME,
            "DATE": self.DATE,
        }
        self.NESTOR_CFG_FILENAME = self.NESTOR_CFG_FILENAME or ".nestor-cfg.yml"
        self.BASE_MODULE_UPDATE = self.BASE_MODULE_UPDATE or "all"
        self.S3_SECRET_PREVIEW = self.S3_SECRET_PREVIEW or "s3-ndp-preview"
        self.S3_DUMP_SECRET = self.S3_DUMP_SECRET or "s3-ndp-scaleway"
        self.S3_DUMP_BUCKET = self.S3_DUMP_BUCKET or "ndp-production-backups"
        self.DATE = self.DATE or date.today().isoformat()

        if self.NESTOR_NAME_PREFIX:
            self.NESTOR_NAME = f"{self.NESTOR_NAME_PREFIX}-{self.NESTOR_NAME}"

    def __repr__(self):
        res = "NESTOR_NAME = " + str(self.NESTOR_NAME)
        res += "\nCI_PROJECT_DIR = " + str(self.CI_PROJECT_DIR)
        res += "\nCI_COMMIT_REF_NAME = " + str(self.CI_COMMIT_REF_NAME)
        res += "\nCI_PROJECT_PATH = " + str(self.CI_PROJECT_PATH)
        res += "\nGITLAB_TOKEN = " + str((self.GITLAB_TOKEN and "*********"))
        res += "\nODOO_VERSION = " + str(self.ODOO_VERSION)
        res += "\nS3_SECRET_PREVIEW = " + str(self.S3_SECRET_PREVIEW)
        res += "\nS3_DUMP_SECRET = " + str(self.S3_DUMP_SECRET)
        res += "\nS3_DUMP_BUCKET = " + str(self.S3_DUMP_BUCKET)
        res += "\nVERBOSE = " + str(self.VERBOSE)
        res += "\nDATE = " + str(self.DATE)
        res += "\nS3_BUCKET = " + str(self.S3_BUCKET)
        res += "\nPROD_INSTANCE_NAME = " + str(self.PROD_INSTANCE_NAME)
        res += "\nDB_NAME = " + str(self.DB_NAME)
        res += "\nODOO_DEPENDS = " + str(self.ODOO_DEPENDS)
        res += "\nDUMP_PATH = " + str(self.DUMP_PATH)
        res += "\nNESTOR_CFG_FILENAME = " + str(self.NESTOR_CFG_FILENAME)
        res += "\nBASE_MODULE_UPDATE = " + str(self.BASE_MODULE_UPDATE)
        return res


class InteractiveConfig(EnvironementConfig):
    def __init__(self):
        super(InteractiveConfig, self).__init__()
        log("Nom du projet git (Sans le 'odoo-addons/' ex: mettre `aef` pour `odoo-addons/aef`) ?")
        log("Mettre un '/' si c'est un path absolut (ex /odoo/v15/tms/core')")
        self.CI_PROJECT_PATH = input("=> ")
        DEFAULT_PROD_INSTANCE_NAME = self.CI_PROJECT_PATH
        if self.CI_PROJECT_PATH:
            if not self.CI_PROJECT_PATH.startswith("/"):
                self.CI_PROJECT_PATH = "odoo-addons/" + self.CI_PROJECT_PATH
            else:
                self.CI_PROJECT_PATH = self.CI_PROJECT_PATH.removeprefix("/")
        else:
            log("Un projet est obligatoire")
            sys.exit(1)

        log("Version d'Odoo ?")
        self.ODOO_VERSION = input("=> ")

        log(f"Nom de la branche ou du tag || default = {self.ODOO_VERSION}")
        self.CI_COMMIT_REF_NAME = input("=> ") or self.ODOO_VERSION

        log(f"Nom du nestor (Vide pour utliser '{self.CI_COMMIT_REF_NAME}')")
        self.NESTOR_NAME = input("=> ") or self.CI_COMMIT_REF_NAME

        log(f"Nom de l'instance nestor dans le kube de prod || default '{DEFAULT_PROD_INSTANCE_NAME}'")
        self.PROD_INSTANCE_NAME = input("=> ") or DEFAULT_PROD_INSTANCE_NAME

        log(f"Repertoire du projet ou laisser vide pour utiliser '{CURRENT_PATH}'")
        self.CI_PROJECT_DIR = input("=> ") or CURRENT_PATH

        log(f"Prefix à utliser pour le nom sinon '{self.NESTOR_NAME}'")
        self.NESTOR_NAME_PREFIX = input("=> ") or ""

        log(f"Nom de la base de backup ? (Vide pour le nom de la prod '{self.PROD_INSTANCE_NAME}')")
        self.DB_NAME = input("=> ")

        log(f"Date du dump à utiliser (format ISO YYYY-MM-DD) || default = {date.today().isoformat()}")
        self.DATE = input("=> ") or self.DATE

        log(f"Odoo depends || default = odoo-addons/common-modules,odoo-addons/community-addons")
        self.ODOO_DEPENDS = input("=> ") or self.ODOO_DEPENDS

        log(f"Token Gitlab (Vide pour utiliser '{self.GITLAB_TOKEN}')")
        self.GITLAB_TOKEN = input("=> ") or self.GITLAB_TOKEN


def log(*args):
    print(" ".join([str(arg) for arg in args]), flush=True, file=sys.stderr)


class PreviewUtils:
    def __init__(self, gitlab_api, env_config):
        self.gitlab_api = gitlab_api
        self.env_config = env_config

    def _try_find_suitable_branch(self, project, branch_to_try_names):
        for branch_name in branch_to_try_names:
            try:
                depends_branch = project.branches.get(branch_name).name
                log("Project %s: branch '%s' found" % (project.name, branch_name))
                return depends_branch
            except gitlab.GitlabGetError:
                log("Project %s: branch not found with name %s" % (project.name, branch_name))
                continue
        return project.default_branch

    def create_spec_sources(self, idx, project_path, branch_to_test) -> NestorGitDesc:
        project = self.gitlab_api.projects.get(project_path)
        branch_founded = self._try_find_suitable_branch(project, branch_to_test)
        log("\tProject %s: use branch '%s'" % (project.name, branch_founded))
        return NestorGitDesc(idx, project_path, branch_founded)

    def _create_all_spec_sources(self, main_project_path):
        current_gl_project = self.gitlab_api.projects.get(main_project_path)
        default_branch = Utils.quote_if_needed(str(current_gl_project.default_branch))
        nestor_values = NestorDescSet([NestorOpt("sources.branch", default_branch)])
        spec_src = self.create_spec_sources(
            idx=0,
            project_path=main_project_path,
            branch_to_test=[
                self.env_config.CI_COMMIT_REF_NAME,
                current_gl_project.default_branch,
                self.env_config.ODOO_VERSION,
            ],
        )
        nestor_values.add(spec_src)
        idx = 2
        for depend in self.env_config.ODOO_DEPENDS.split(","):
            if depend:
                nestor_values.add(
                    self.create_spec_sources(
                        idx=idx,
                        project_path=depend,
                        branch_to_test=[
                            self.env_config.CI_COMMIT_REF_NAME,
                            current_gl_project.default_branch,
                            self.env_config.ODOO_VERSION,
                        ],
                    )
                )
                idx += 1
        return nestor_values

    def get_spec_values(self, sections: collections.abc.Iterable = ("default",), stage="runtime"):
        cfg_file_name = ".nestor-cfg.yml"
        preview_confs_path = os.path.join(os.path.dirname(__file__), "default-preview-nestor-cfg.yml")
        nestor_cfg_path = os.path.join(self.env_config.CI_PROJECT_DIR, cfg_file_name)

        values = NestorDescSet()
        values.add(NestorOpt("version", self.env_config.ODOO_VERSION))
        values.add(self._get_spec_from_path(preview_confs_path, sections, stage))
        values.add(self._get_spec_from_path(nestor_cfg_path, sections, stage))
        return values

    def _get_spec_from_path(self, nestor_cfg_path, sections, stage):
        values = NestorDescSet()
        log("")
        log("Use cfg file %s" % nestor_cfg_path)
        if os.path.exists(nestor_cfg_path):
            for section in sections:
                values.add(NestorDescSet.parse_nestor_cfg(nestor_cfg_path, section))
                values.add(NestorDescSet.parse_nestor_cfg(nestor_cfg_path, section=section + "-" + stage))
        else:
            log("Cfg file %s not exist" % nestor_cfg_path)
        return values


class ScriptNestor:
    def __init__(self, config: EnvironementConfig):
        self.config = config
        self.inst = ScriptNestorInstance(config.NESTOR_NAME)
        self.gitlab_api = gitlab.Gitlab("https://gitlab.ndp-systemes.fr", config.GITLAB_TOKEN, api_version="4")
        self.preview_utils = PreviewUtils(self.gitlab_api, self.config)

    def delete(self):
        self.inst.delete()
        self.inst.wait(up=False, postgres=True)
        self.inst.wait(up=False)

    def edit_with_values(self, values):
        log("MAJ de l'instance", self.inst.name)
        log(values.to_str(pretty=True))
        log("")
        self.stop()
        self.inst.delete_and_exit_if_failed(self.inst.edit(values))
        time.sleep(10)

    def create_with_values(self, values):
        log("")
        log("Nouvelle instance", self.config.NESTOR_NAME)
        log(values.to_str(pretty=True))
        log("")
        self.inst.create(self.config.ODOO_VERSION, values_set=values)
        self.wait_all_up()

    def wait_all_up(self):
        self.inst.delete_and_exit_if_failed(self.inst.wait(postgres=True, timeout=5 * 60))
        self.inst.delete_and_exit_if_failed(self.inst.wait(timeout=5 * 60))

    def wait_all_down(self):
        self.inst.delete_and_exit_if_failed(self.inst.wait(up=False, postgres=True, timeout=5 * 60))
        self.inst.delete_and_exit_if_failed(self.inst.wait(up=False, timeout=5 * 60))

    def stop(self):
        self.inst.delete_and_exit_if_failed(self.inst.stop())
        self.inst.delete_and_exit_if_failed(self.inst.wait(up=False, postgres=False, timeout=5 * 60))  # Timeout de 5min

    def enable_s3_spec(self, values):
        if values["persistence.s3.secret"]:
            values.add(
                self.inst.filestore.enable_on_s3_spec(
                    s3_secret="s3-ndp-preview", s3_bucket=self.config.S3_BUCKET, values=values
                )
            )
        client = self._get_s3_client()
        if not client.bucket_exists(self.config.S3_BUCKET):
            client.make_bucket(self.config.S3_BUCKET)
        return values

    def log_spec(self, spec_values: NestorDescSet):
        log("")
        log("Spec Nestor", self.inst.name)
        log(spec_values.to_str(pretty=True))
        log("")

    def run_script(self) -> int:
        log("Nothing to do !!!!!!!!!!")
        return 1

    def _get_s3_client(self):
        try:
            config.load_incluster_config()
        except config.config_exception.ConfigException:
            config.load_config()
        v1 = client.CoreV1Api()
        ret = v1.list_namespaced_secret("ndp-test")
        for i in ret.items:
            if (i.metadata.labels or {}).get("type") == "s3":
                if self.config.S3_SECRET_PREVIEW == i.metadata.name:
                    return Minio(
                        endpoint=base64.b64decode(i.data["S3_HOST"]).decode("utf-8"),
                        access_key=base64.b64decode(i.data["S3_ACCESS_KEY"]).decode("utf-8"),
                        secret_key=base64.b64decode(i.data["S3_SECRET_KEY"]).decode("utf-8"),
                        region=base64.b64decode(i.data["S3_REGION"]).decode("utf-8"),
                    )


class PreviewUpScript(ScriptNestor):
    def run_script(self):
        if not self.inst.name:
            log("Instance don't have a name")
            return 1
        if self.config.ALWAYS_DELETE:
            if self.inst.exist():
                self.delete()
                self.wait_all_up()

        if not self.inst.exist():
            log("Create instance")
            values = self.preview_utils.get_spec_values(
                sections=["default", "preview", self.config.CI_COMMIT_REF_NAME], stage="restore"
            )
            values.add(self.preview_utils._create_all_spec_sources(self.config.CI_PROJECT_PATH))
            values.add(self.enable_s3_spec(values))

            self.log_spec(values)

            self.create_with_values(values)
            log("Stop de l'instance pour la restauration")
            self.stop()
            log("Restauration du dump %s" % self.config.DUMP_PATH)
            self.inst.delete_and_exit_if_failed(
                self.inst.db_restore_from_s3(
                    self.config.DUMP_PATH,
                    s3_secret=self.config.S3_DUMP_SECRET,
                    bucket=self.config.S3_DUMP_BUCKET,
                    set_password_to_all=True,
                )
            )
        else:
            log("MAJ de l'instance", self.inst.name)
            self.stop()
        values = self.preview_utils.get_spec_values(
            sections=["default", "preview", self.config.CI_COMMIT_REF_NAME], stage="runtime"
        )
        values = self.enable_s3_spec(values)
        self.log_spec(values)
        self.edit_with_values(values)
        log("Attente du demarrage postgresql")
        self.inst.delete_and_exit_if_failed(self.inst.wait(up=True, postgres=True))
        time.sleep(10)
        log("Update >> -u", self.config.BASE_MODULE_UPDATE)
        self.inst.delete_and_exit_if_failed(self.inst.update(self.config.BASE_MODULE_UPDATE))
        self.inst.delete_and_exit_if_failed(self.inst.wait(up=True, postgres=True))
        self.inst.delete_and_exit_if_failed(self.inst.start())

        self.wait_all_up()

        log("=======================================================")
        log("Url:", self.inst.url)
        log("Mot de passe:", self.inst.password)
        log("=======================================================")

        return 0


class PreviewDownScript(ScriptNestor):
    def run_script(self):
        s3_client = self._get_s3_client()
        self.inst.delete()
        log("Removing S3 bucket", self.config.S3_BUCKET)
        if s3_client.bucket_exists(self.config.S3_BUCKET):
            for obj in s3_client.list_objects(self.config.S3_BUCKET, recursive=True):
                log("delete", self.config.S3_BUCKET, obj.object_name)
                s3_client.remove_object(self.config.S3_BUCKET, obj.object_name)
            s3_client.remove_bucket(self.config.S3_BUCKET)
        log("OK")
        return 0
