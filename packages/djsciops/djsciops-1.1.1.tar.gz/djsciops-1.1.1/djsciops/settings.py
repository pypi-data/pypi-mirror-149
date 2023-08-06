import appdirs
import pathlib
import os
import yaml
from . import __version__ as version
from . import utils as djsciops_utils

CONFIG_TEMPLATE = """
version: "{djsciops_version}"
aws:
  account_id: "{djsciops_aws_account_id}"
s3:
  role: "{djsciops_s3_role}"
  bucket: "{djsciops_s3_bucket}"
djauth:
  client_id: "{djsciops_djauth_client_id}"
"""

LOG_LEVEL = os.getenv("DJSCIOPS_LOG_LEVEL", "info")


def get_config(stdin_enabled=True):
    from .log import log

    config_directory = appdirs.user_data_dir(appauthor="datajoint", appname="djsciops")
    try:
        # loading existing config
        config = yaml.safe_load(
            pathlib.Path(config_directory, "config.yaml").read_text()
        )
        log.info(
            "Existing configuration detected. Loading from "
            f"{pathlib.Path(config_directory, 'config.yaml')}..."
        )
        return config
    except FileNotFoundError as e:
        if not stdin_enabled:
            raise e
        log.info(
            "Welcome! We've detected that this is your first time using DataJoint "
            "SciOps CLI tools. We'll need to ask a few questions to initialize properly."
        )
        # generate default config
        config = CONFIG_TEMPLATE.format(
            djsciops_aws_account_id=(
                os.getenv("DJSCIOPS_AWS_ACCOUNT_ID")
                if os.getenv("DJSCIOPS_AWS_ACCOUNT_ID")
                else input("\n   -> AWS Account ID? ")
            ),
            djsciops_s3_role=(
                os.getenv("DJSCIOPS_S3_ROLE")
                if os.getenv("DJSCIOPS_S3_ROLE")
                else input("\n   -> S3 Role? ")
            ),
            djsciops_s3_bucket=(
                os.getenv("DJSCIOPS_S3_BUCKET")
                if os.getenv("DJSCIOPS_S3_BUCKET")
                else input("\n   -> S3 Bucket? ")
            ),
            djsciops_djauth_client_id=(
                os.getenv("DJSCIOPS_DJAUTH_CLIENT_ID")
                if os.getenv("DJSCIOPS_DJAUTH_CLIENT_ID")
                else input("\n   -> DataJoint Account Client ID? ")
            ),
            djsciops_version=version,
            djsciops_log_level=os.getenv("DJSCIOPS_LOG_LEVEL", "info"),
        )
        # write config
        os.makedirs(config_directory, exist_ok=True)
        with open(pathlib.Path(config_directory, "config.yaml"), "w") as f:
            f.write(config)

        log.info(
            "Thank you! We've saved your responses to "
            f"{pathlib.Path(config_directory, 'config.yaml')} so you won't need to "
            "specify this again."
        )
        # return config
        return yaml.safe_load(config)
