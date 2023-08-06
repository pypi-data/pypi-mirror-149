"""
Malacanang API Module for calling endpoints.
"""

import requests
import json


class MalacanangAPI:
    def __init__(self, env="dev"):
        """
        Initializes the Malacanang API.

        Parameters
        ----------
        env : str, optional
            Environment to be called (e.g. live or dev) (default is "dev")

        Attributes
        ----------
        base_url : str
            Base URL of the Malacanang API endpoint

        headers : Object
            Headers to be passed into requests
        """
        self.base_url = f"https://{env}-malacanang.kumuapi.com/v1"
        self.headers = {"Content-Type": "application/json"}

    def get_variant(self, body):
        """
        Retrieves the variant for the specified request body.

        Parameters
        ----------
        body : Python object, required
            Takes in `user_id` and `use_case` attributes (default is None)

            Example ::
                {
                    "user_id": "user_1",
                    "use_case": "use_case_1",
                }

        Returns
        -------
        Python object
        """
        variants_url = self.base_url + "/variants"
        try:
            res = requests.get(
                url=variants_url, data=json.dumps(body), headers=self.headers
            )
            res.raise_for_status()
            return res.json()
        except requests.exceptions.HTTPError as errh:
            raise ("HTTP ERROR:", errh)
        except requests.exceptions.ConnectionError as errc:
            raise ("CONNECTION ERROR:", errc)
        except requests.exceptions.Timeout as errt:
            raise ("TIMEOUT ERROR:", errt)
        except requests.exceptions.RequestException as err:
            raise ("REQEUST ERROR:", err)

    def get_use_case_variants(self, use_case, enabled=True):
        """
        Retrieves the variant for the specified request body.

        Parameters
        ----------
        body : Python object, required
            Takes in `user_id` and `use_case` attributes (default is None)

            Example ::
                {
                    "user_id": "user_1",
                    "use_case": "use_case_1",
                }

        Returns
        -------
        Python object
        """
        use_case_variants_url = (
            self.base_url
            + f"/use-cases/{use_case}/variants{ '?enabled=true' if enabled else '' }"
        )
        try:
            res = requests.get(url=use_case_variants_url, headers=self.headers)
            res.raise_for_status()
            return res.json()
        except requests.exceptions.HTTPError as errh:
            raise ("HTTP ERROR:", errh)
        except requests.exceptions.ConnectionError as errc:
            raise ("CONNECTION ERROR:", errc)
        except requests.exceptions.Timeout as errt:
            raise ("TIMEOUT ERROR:", errt)
        except requests.exceptions.RequestException as err:
            raise ("REQEUST ERROR:", err)
