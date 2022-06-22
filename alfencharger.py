"""
Module for communicating with Alfen EV Chargers
"""
import requests

class AlfenCharger():
    """
    Class for communicating with Alfen EV Chargers
    """
    charger_ip = ""
    http_session = None

    def __init__(self, charger_ip, username, password):
        """
        Initialize instance and login to the charger
        Input:
            - IP address for charger (string)
            - username for charger
            - password for charger
        Output: No
        """
        self.charger_ip = charger_ip
        self.http_session = requests.Session()
        # Login to HTTP server at charger
        headers = {'Content-Type': "application/json; charset=utf-8"}
        url = f"http://{self.charger_ip}/api/login"
        # These values seem to be fixed for all chargers??
        login_data = f'{{"username":"{username}", "password":"{password}", "displayname":"Post"}}'
        login_result = self.http_session.post(url, headers=headers, data=login_data)
        # When status_code is not 200 login was not succesfull
        if login_result.status_code != 200:
            raise Exception("Login incorrect!")

    def set_charge_current(self, current):
        """
        Set new limit for charge_current
        Input: 1-24 (integer) Unit: Amperage
        Output: success (boolean)
        """
        # Check input for valid value
        if current in range(1, 25):
            headers = {'Content-Type': "application/json; charset=utf-8"}
            url = f"http://{self.charger_ip}/api/prop"
            # Send new value to charger
            data = '{"OD_sysMaxStationCurrent":{"id":"2062_0","value": '+str(current)+'}}'
            resp = self.http_session.post(url, headers=headers, data=data)
            if resp.status_code == 200:
                return True
            return False
        raise Exception("ERR: Invalid setting (valid is between 1-24)", current)

    def get_charge_status(self):
        """
        Get current status from charger
        Output: tbd
        """
        headers = {'Content-Type': "application/json; charset=utf-8"}
        url = f"http://{self.charger_ip}/api/prop?ids=2062_0,2165_1,2166_1"
        # Send new value to charger
        resp = self.http_session.get(url, headers=headers)

        if resp.status_code != 200:
            raise Exception("Error in communication")

        output = {}

        try:
            json_data = resp.json()
            output['max_current'] = json_data['OD_sysMaxStationCurrent']['value']
            if json_data["DSC_Socket1_status"]["value"] in [0]:
                output['socket_state'] = 'idle'
            else:
                output['socket_state'] = json_data["DSC_Socket_1_status"]["value"]
        finally:
            return output
