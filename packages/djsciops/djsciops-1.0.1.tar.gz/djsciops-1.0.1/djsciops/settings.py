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


def get_config():
    djsciops_utils.log("configuration", message_type="header")
    config_directory = appdirs.user_data_dir(appauthor="datajoint", appname="djsciops")
    try:
        # loading existing config
        config = yaml.safe_load(
            pathlib.Path(config_directory, "config.yaml").read_text()
        )
        djsciops_utils.log(
            f"Existing configuration detected. Loading from {pathlib.Path(config_directory, 'config.yaml')}...",
            pause_duration=1,
        )
        return config
    except FileNotFoundError:
        djsciops_utils.log(
            "Welcome! We've detected that this is your first time using DataJoint SciOps CLI tools. We'll need to ask a few questions to initialize properly.",
            pause_duration=5,
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
        )
        # write config
        os.makedirs(config_directory, exist_ok=True)
        with open(pathlib.Path(config_directory, "config.yaml"), "w") as f:
            f.write(config)

        djsciops_utils.log(
            f"Thank you! We've saved your responses to {pathlib.Path(config_directory, 'config.yaml')} so you won't need to specify this again.",
            pause_duration=5,
        )
        # return config
        return yaml.safe_load(config)
