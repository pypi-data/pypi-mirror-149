import http
import requests
import os


class Email:
    def __init__(self, api_url_env_name):
        self.api_url_env_name = api_url_env_name

    def send(self, id_template: str, email_from: str, from_name: str, to, params: dict):
        """
        Send an email based on a template id. If the email is not sent, an exception is raised.
        :param id_template: The template id.
        :param email_from: The origin email.
        :param from_name: The origin name.
        :param to: The single email or a list of emails to be sent.
        :param params: The template parameters (each template has a different params).
        """
        if not isinstance(to, (list, tuple, set)):
            to = [to]
        url = os.environ[self.api_url_env_name]
        body = {"IdTemplate": id_template, "From": email_from, "FromName": from_name, "To": to, "Parameters": params}
        response = requests.post(url, json=body)
        if response.status_code == http.HTTPStatus.NO_CONTENT:
            return
        raise Exception(response.content)