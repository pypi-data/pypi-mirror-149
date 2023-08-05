import ast

from marketplace.app import MarketPlaceApp


class HPCApp(MarketPlaceApp):
    def status(self):
        return super().heartbeat()

    def new_job(self, config=None):
        """Create a new job

        Actually it will create a new folder in specific user path on HPC
        Return the folder name for further opreration."""
        resp = super().new_transformation(config)
        resp = ast.literal_eval(resp)

        return resp["resourceId"]

    def upload(self, resource_id, source_path=str):
        """upload file to remote path `resource_id` from source path"""
        with open(source_path, "rb") as fh:
            super().put(
                path="updateDataset",
                params={"resource": f"{resource_id}"},
                files={"file": fh},
            )

    def download(self, resource_id, filename) -> str:
        """download file from `resource_id`
        return str of content"""
        resp = super().get(
            path="getDataset",
            params={"resource": f"{resource_id}"},
            json={"filename": filename},
        )

        return resp.text

    def list_job(self):
        """List the jobs"""
        # TODO filter jobs from respond
        return super().get(path="getTransformationList").json()

    def run_job(self, resource_id):
        """submit job in the path `resource_id`
        It actually execute sbatch submit.sh in remote
        Need job script `submit.sh` uploaded to the folder
        TODO, check the job script ready"""
        resp = super().post(
            path="startTransformation", params={"resource": f"{resource_id}"}
        )

        return resp.text
