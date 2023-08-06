import os
import pprint

from pynestor import NestorDescSet, NestorInstance

instances = NestorInstance.list()
for inst in instances:
    if not inst.spec["persistence"]["disabled"]:
        inst.filestore.dump_on_s3(s3_secret="s3-ndp-preview", s3_bucket=None)
        inst.stop()
        inst.start_progressive_edit()
        inst.filestore.enable_on_s3(s3_secret="s3-ndp-preview", s3_bucket=None)

        memory_soft = None
        memory_hard = None
        limit_ram_odoo = None
        limit_cpu_odoo = None
        request_cpu_odoo = None
        request_ram_odoo = None
        limit_ram_db = None
        limit_cpu_db = None
        request_cpu_db = None
        request_ram_db = None
        # J'assume que tous les projets son sous odoo-addons et que c'est le premier depot git
        project = inst.spec["sources"]["repositories"]["DEPOT_GIT"]["path"].split("/")[1]
        if project == "fmp":  # fmp à besoin de minimum 1.3Go en soft en 2Go en hard
            memory_soft = 1_300_000_000
            memory_hard = 2_000_000_000

        inst.set_memory_worker(worker=2, memory_soft=memory_soft, memory_hard=memory_hard)
        inst.set_ressource_kube_odoo(
            request_cpu=request_cpu_odoo,
            request_ram=request_ram_odoo,
            limit_cpu=limit_cpu_odoo,
            limit_ram=limit_ram_odoo,
        )
        inst.set_ressource_kube_db(
            request_cpu=request_cpu_db, request_ram=request_ram_db, limit_cpu=limit_cpu_db, limit_ram=limit_ram_db
        )

        inst.commit_progressive_edit()


secret_filestore_preview = os.getenv("S3_SECRET_PREVIEW", "s3-ndp-preview")
inst = NestorInstance("aef-t1946", verbose=True)
pprint.pprint(inst.spec)
version = int(float(inst.spec["version"]))
desc_set = NestorDescSet()
if not inst.spec["persistence"]["disabled"]:
    inst.filestore.enable_on_s3(s3_secret="s3-ndp-preview", s3_bucket=None)
