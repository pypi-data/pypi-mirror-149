import base64
from datetime import datetime
import json
import boto3
import logging
import flask
import webbrowser
import multiprocessing
import time
import urllib
import http.client
from . import utils as djsciops_utils


def _oidc_login(
    auth_client_id: str,
    auth_url: str = "https://accounts.datajoint.io/auth/auth",
    lookup_service_allowed_origin: str = "https://ops.datajoint.io",
    lookup_service_domain: str = "ops.datajoint.io",
    lookup_service_route: str = "/social-login/api/user",
    lookup_service_auth_provider: str = "accounts.datajoint.io",
    code_challenge: str = "ubNp9Y0Y_FOENQ_Pz3zppyv2yyt0XtJsaPqUgGW9heA",
    code_challenge_method: str = "S256",
    code_verifier: str = "kFn5ZwL6ggOwU1OzKx0E1oZibIMC1ZbMC1WEUXcCV5mFoi015I9nB9CrgUJRkc3oiQT8uBbrvRvVzahM8OS0xJ51XdYaTdAlFeHsb6OZuBPmLD400ozVPrwCE192rtqI",
    callback_port: int = 28282,
    delay_seconds: int = 300,
):
    """
    Primary OIDC login flow.
    """
    # Prepare user
    djsciops_utils.log(
        "User authentication required to use DataJoint SciOps CLI tools. We'll be launching a web browser to authenticate your DataJoint account.",
        pause_duration=5,
    )
    # allocate variables for access and context
    code = None
    cancelled = True
    # Prepare HTTP server to communicate with browser
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
    app = flask.Flask("browser-interface")

    def shutdown_server():
        """
        Shuts down Flask HTTP server.
        """
        func = flask.request.environ.get("werkzeug.server.shutdown")
        if func is not None:
            # Ensure running with the Werkzeug Server
            func()

    @app.route("/login-cancelled")
    def login_cancelled():
        """
        Accepts requests which will cancel the user login.
        """
        shutdown_server()
        return """
        <!doctype html>
        <html>
          <head>
            <script>
              window.onload = function load() {
              window.open('', '_self', '');
              window.close();
              };
            </script>
          </head>
          <body>
          </body>
        </html>
        """

    @app.route("/login-completed")
    def login_completed():
        """
        Redirect after user has successfully logged in.
        """
        nonlocal code
        nonlocal cancelled
        cancelled = False
        code = flask.request.args.get("code")
        shutdown_server()
        return """
        <!doctype html>
        <html>
          <head>
            <script>
              window.onload = function load() {
              window.open('', '_self', '');
              window.close();
              };
            </script>
          </head>
          <body>DataJoint login completed! Feel free to close this tab if it did not close automatically.</body>
        </html>
        """

    # build url
    query_params = dict(
        scope="openid",
        response_type="code",
        client_id=auth_client_id,
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method,
        redirect_uri=f"http://localhost:{callback_port}/login-completed",
    )
    link = f"{auth_url}?{urllib.parse.urlencode(query_params)}"
    # attempt to launch browser or provide instructions
    browser_available = True
    try:
        webbrowser.get()
    except webbrowser.Error:
        browser_available = False
    if browser_available:
        djsciops_utils.log(
            f"Browser available. Launching...",
            pause_duration=1,
        )
        webbrowser.open(link, new=2)
    else:
        djsciops_utils.log(
            f"Brower unavailable. On a browser client, please navigate to the following link to login: {link}\n",
            pause_duration=1,
        )
    # start response server
    cancel_process = multiprocessing.Process(
        target=_delayed_request,
        kwargs=dict(
            url=f"http://localhost:{callback_port}/login-cancelled",
            delay=delay_seconds,
        ),
    )
    cancel_process.start()
    app.run(host="0.0.0.0", port=callback_port, debug=False)
    cancel_process.terminate()
    # received a response
    if cancelled:
        raise Exception(
            "User login cancelled. User must be logged in to use DataJoint SciOps CLI tools."
        )
    else:
        djsciops_utils.log("User successfully authenticated.")
        # generate user info
        connection = http.client.HTTPSConnection(lookup_service_domain)
        headers = {
            "Content-type": "application/json",
            "Origin": lookup_service_allowed_origin,
        }
        body = json.dumps(
            {
                "auth_provider": lookup_service_auth_provider,
                "redirect_uri": f"http://localhost:{callback_port}/login-completed",
                "code_verifier": code_verifier,
                "client_id": auth_client_id,
                "code": code,
            }
        )
        connection.request("POST", lookup_service_route, body, headers)
        userdata = json.loads(connection.getresponse().read().decode())
        return userdata["access_token"], userdata["username"]


def _delayed_request(*, url: str, delay: str = 0):
    time.sleep(delay)
    return urllib.request.urlopen(url)


class Session:
    def __init__(
        self,
        aws_account_id: str,
        s3_role: str,
        auth_client_id: str,
        bearer_token: str = None,
    ):
        djsciops_utils.log("authentication", message_type="header")
        # OAuth2.0 authorization
        if not bearer_token:
            self.bearer_token, self.user = _oidc_login(auth_client_id=auth_client_id)
        else:
            jwt_data = json.loads(
                base64.b64decode(bearer_token.split(".")[1].encode()).decode()
            )
            time_to_live = (jwt_data["exp"] - datetime.utcnow().timestamp()) / 60 / 60
            djsciops_utils.log(
                f"Reusing provided bearer token with a life of {time_to_live} [HR]",
                pause_duration=1,
            )
            self.bearer_token, self.user = (bearer_token, jwt_data["sub"])
        # AWS temporary credentials
        sts_client = boto3.client(service_name="sts")
        sts_response = sts_client.assume_role_with_web_identity(
            RoleArn=f"arn:aws:iam::{aws_account_id}:role/{s3_role}",
            RoleSessionName=self.user,
            WebIdentityToken=self.bearer_token,
            DurationSeconds=12 * 60 * 60,
        )
        self.aws_access_key_id = sts_response["Credentials"]["AccessKeyId"]
        self.aws_secret_access_key = sts_response["Credentials"]["SecretAccessKey"]
        self.aws_session_token = sts_response["Credentials"]["SessionToken"]
        # AWS resource
        self.s3 = boto3.Session(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            aws_session_token=self.aws_session_token,
        ).resource("s3")
