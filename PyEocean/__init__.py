import os
import requests


class Client(object):
    """ A client for accessing the EOcean API. """

    def __init__(self, username=None, password=None, server=None, port=None,
                 originator=None, report_url=None, max_response=None,
                 response_fmt=None, service_provider=None, environment=None):
        """
        Initializes the E-Ocean client

        :param username:
        :param password:
        :param server:
        :param port:
        :param originator:
        :param report_url:
        :param max_response:
        :param response_fmt:
        :param service_provider:
        :param environment:

        :returns: EOcean Client
        :rtype: eocean.Client
        """

        environment = environment or os.environ

        self.username = username or environment.get('EOCEAN_USERNAME')
        self.password = password or environment.get('EOCEAN_PASSWORD')
        self.server = server or environment.get('EOCEAN_SERVER')
        self.port = port or environment.get('EOCEAN_PORT')
        self.originator = originator or environment.get('EOCEAN_ORIGINATOR')
        self.report_url = report_url or environment.get('EOCEAN_REPORT_URL')
        self.response_fmt = \
            response_fmt or environment.get('EOCEAN_RESPONSE_FMT')
        self.service_provider = \
            service_provider or environment.get('EOCEAN_SERVICE_PROVIDER')
        self.max_response = \
            max_response or environment.get('EOCEAN_max_response')

    def __parse_xml_response(self, response):
        """

        :param response:
        :return: status and message as tupple
        """
        import xml.etree.ElementTree as ET
        response_string = ''
        root = ET.fromstring(response.text)
        for child in root.findall('data')[0][0]:
            if child.tag == 'statuscode' or child.tag == 'statusmessage':
                response_string = response_string + child.tag + ": " + child.text + ","

        return response_string

    def __parse_html_response(self, response):
        raise NotImplementedError

    def __send(self, message, recipient, message_type, action):
        """
        Private method for sending any type of message.

        :param message:
        :param recipient:
        :param message_type:
        :param action:
        :return:
        """
        params = {
            'action': action,
            'username': self.username,
            'password': self.password,
            'originator': self.originator,
            'recipient': recipient,
            'messagetype': message_type,
            'messagedata': message,
            'responseformat': self.response_fmt,
            'reporturl': self.report_url,
            'maxresponse': self.max_response
        }

        if self.service_provider:
            params['serviceprovider'] = self.service_provider

        response = requests.\
            get('http://' + self.server + ':' + self.port + '/api', params=params)

        if self.response_fmt == 'xml':
            return self.__parse_xml_response(response)
        else:
            return self.__parse_html_response(response)

    def send_text(self, message, recipient):
        """
        Public method used for sending text message.

        :param message:
        :param recipient:
        :return: message_id
        """
        return self.__send(message, recipient, message_type='TEXT', action='sendmessage')

    def send_wappush(self, message, recipient):
        """
        ublic method used for sending wap push.

        :param message:
        :param recipient:
        :return: message_id
        """
        return self.__send(message, recipient, message_type='WAPPUSH', action='sendmessage')
