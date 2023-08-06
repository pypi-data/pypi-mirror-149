from typing import Dict

import requests as requests


class T1Service:
    def __init__(self, t1_creds: Dict):
        self.__validateCreds(t1_creds)

        self.headers = {"Accept": "application/vnd.mediamath.v1+json",
                        "Authorization": f"Bearer {t1_creds.get('token')}"}
        self.host = t1_creds.get("host")

    def __validateCreds(self, t1_creds: Dict):
        """
        Do simple attribute validation
        :param t1_creds: Dict
        :return:
        """
        if not t1_creds.get("token"):
            raise AttributeError("token attribute was not provided")

        if not t1_creds.get("host"):
            raise AttributeError("host attribute was not provided")

    def getCurrencyRate(self, currency: str) -> float:
        """
        Get currency rate from t1
        :param currency: str
        :return: float
        """

        url = f"{self.host}/currency_rates?full=*&q=currency_code=={currency}&sort_by=-date&page_limit=1"
        conversion_rate = 1
        for _ in range(5):
            try:
                r = requests.get(url, headers=self.headers, timeout=60)
            except requests.ConnectionError:
                continue

            conversion_rate = r.json().get("data", [{}])[0].get("rate", conversion_rate)
            break

        return conversion_rate

    def isValidAdvertiser(self, advertiser_id: int) -> bool:
        """
        Check is advertiser exists
        :param advertiser_id: int
        :return: bool
        """
        url = f"{self.host}/advertisers/{advertiser_id}"
        exists = False
        try:
            r = requests.get(url, headers=self.headers, timeout=60)
            exists = r.status_code == 200
        except requests.ConnectionError:
            ...

        return exists

    def isValidMeritPixel(self, merit_pixel_id: int) -> bool:
        """
        Check is merit pixel exists
        :param merit_pixel_id: int
        :return: bool
        """
        url = f"{self.host}/pixel_bundles/{merit_pixel_id}"
        exists = False
        try:
            r = requests.get(url, headers=self.headers, timeout=60)
            exists = r.status_code == 200
        except requests.ConnectionError:
            ...

        return exists
