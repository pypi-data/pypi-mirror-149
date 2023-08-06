import io
import json
import logging
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from requests.auth import HTTPDigestAuth
from urllib.error import HTTPError
from urllib3 import Retry


class AhrefsClient:
    """ Client for interacting with ahrefs API.

    Attributes:
        session (requests.Session): Session object for handling the connection to ahrefs.
        logger (logging.Logger): Logger for logging the object's method calls.
    """

    # URLs for ahrefs requests
    _APP_BASE_URL = 'https://app.ahrefs.com'
    _AUTH_BASE_URL = 'https://auth.ahrefs.com'
    _LOGIN_URL = _AUTH_BASE_URL + '/auth/login'
    _UPDATE_SERP_URL = _APP_BASE_URL + '/v4/keUpdate'
    _GET_KEYWORD_LISTS_URL = _APP_BASE_URL + '/v4/keLists'
    _KEYWORD_EXPORT_URL = _APP_BASE_URL + '/v4/keListOverviewExport?mode=csv-utf8'
    _SERP_EXPORT_URL = _APP_BASE_URL + '/v4/keListOverviewSerpsExport?mode=csv-utf8'

    # Column names used in csv exports
    _KEYWORD_COLUMN_NAME = 'Keyword'

    def __init__(self, email: str, password: str):
        """ Sets up a session to ahrefs given the specified credentials.

        Args:
            email: The e-mail used to log in.
            password: The password used with <email> to log in.
        """
        self._email = email
        self._password = password
        self.session = requests.Session()
        self.session.auth = HTTPDigestAuth(self._email, self._password)
        self.session.mount('https://', self._retry_adapter(retries=3, backoff_factor=4))
        self.logger = logging.getLogger(__name__)
        # Log in and attach the cookies from the response to session
        login_response = self._request(method='POST', url=self._LOGIN_URL,
                                       data=self._build_login_body())
        self.session.cookies = login_response.cookies

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.session.__exit__()

    def __del__(self):
        self.session.__exit__()

    @staticmethod
    def _retry_adapter(
            retries=5,
            backoff_factor=1.0,
            status_forcelist=(429, 500, 501, 502, 503, 504)
    ):
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        return HTTPAdapter(max_retries=retry)

    def _request(self, method: str = 'GET', url: str = None, *args, **kwargs):
        """ Wrapper around the session.request method that handles HTTP errors

        Args:
            method: The HTTP/HTTPS request method. I.e. GET or POST.
            url: The URL to perform the request on.

        Returns:
            A requests.Response object with the request response.

        Raises:
            An HTTPError with the response status code and failure reason if the status code
                response is not 200.
        """
        response = self.session.request(method, url, *args, **kwargs)
        if response.status_code != 200:
            raise HTTPError(url, response.status_code, response.reason, None, None)
        return response

    def _build_login_body(self):
        """ Bulds the body of the message for the request to the login page. """
        return json.dumps(
            {
                'remember_me': True,
                'auth': {
                    'password': self._password,
                    'login': self._email
                }
            }
        )

    def _build_keyword_update_body(self, country_abbr: str, keyword_list: List[str]):
        """ Builds the body of the message for the request for updating the keywords. """
        return json.dumps({'country': country_abbr, 'keywords': keyword_list})

    def _build_keyword_export_body(self, country_abbr: str, list_id: int, keyword_no: int,
                                   **kwargs) -> str:
        """ Builds the body of the message for the request for exporting the keywords/SERP data.

        Args:
            country_abbr: The country for which the keyword data should be exported.
            list_id: The id of the list which has the keywords we want to export the data for.
            keyword_no: A limit on the number of keywords we can extract data for with each
                request.

        Returns:
            The string corresponding to the body of the keyword export request body.

        """
        return json.dumps(
            {
                "limit": keyword_no,
                "offset": kwargs.get('offset', 0),
                "filters": self._build_filters(**kwargs),
                "sort": {"order": "Desc", "by": "Volume"},
                "country": country_abbr,
                "searchEngine": kwargs.get('search_engine', 'Google'),
                "listId": list_id
            }
        )

    def _build_filters(self, **kwargs) -> List[Dict[str, Union[List[str], str]]]:
        """ Builds a list of the filters that are used in exporting keyword/SERP data. """
        return [
            {"filter": ["Range", kwargs.get('difficulty', "None")], "id": "Difficulty"},
            {"filter": ["Range", kwargs.get('volume', "None")], "id": "Volume"},
            {"filter": ["Range", kwargs.get('global_volume', "None")], "id": "GlobalVolume"},
            {"filter": ["Range", kwargs.get('traffic_potential', "None")],
             "id": "TrafficPotential"},
            {"filter": ["Terms", kwargs.get('terms', "None")], "id": "Terms"},
            {"filter": ["ParentTopic", kwargs.get('parent_topic', "None")], "id": "ParentTopic"},
            {"filter": ["Range", kwargs.get('word_count', "None")], "id": "WordCount"},
            {"filter": ["SerpFeatures", kwargs.get('serp', "None")], "id": "Serp"},
            {"filter": ["IncludeWords", kwargs.get('include', "None")], "id": "Include"},
            {"filter": ["ExcludeWords", kwargs.get('exclude', "None")], "id": "Exclude"},
            {"filter": ["Range", kwargs.get('cps', "None")], "id": "CPS"},
            {"filter": ["UsdRange", kwargs.get('cpc', "None")], "id": "CPC"}
        ]

    def _build_keyword_export_url(self, include_serps: bool):
        """ Builds the URL used for exporting keyword/SERP data. """
        return self._SERP_EXPORT_URL if include_serps else self._KEYWORD_EXPORT_URL

    def export_keyword_list(
            self,
            country_abbr: str,
            list_id: int,
            keyword_no: int = 1000,
            csv_path: str = 'keyword_export.csv',
            include_serps: bool = False,
            trunc_dict: Dict[str, int] = None
    ) -> List[str]:
        """ Exports a csv with keyword/SERP data.

        Args:
            country_abbr: The abbreviation of the country to export data for. E.g. 'us' or 'se'.
            list_id: The id of the keyword list to extract data from.
            keyword_no: A limit on the number of keywords we can extract data for with each
                request.
            csv_path: The path to the csv where the data should be written to. The file is overwrit-
                ten if it already exists.
            include_serps: Whether to include SERP data in the export. This is the same with the
                include_serps option in the ahrefs browser API.
            trunc_dict: If set to a non None dict object, this dictionary maps a column name (key)
                to the character length (value) the column should be truncated to.

                E.g. trunc_dict = {'URL': 256} will truncate the column URL to 256 characters.

        Returns:
            A list of strings corresponding to the keywords we exported data for.
        """
        # Get list of all keyword data except for serp
        response = self._request(
            method='POST',
            url=self._build_keyword_export_url(include_serps=False),
            data=self._build_keyword_export_body(
                country_abbr=country_abbr, list_id=list_id, keyword_no=keyword_no
            ),
            headers={'Content-type': 'application/json; charset=UTF-8'}
        )

        # Get keyword data in dataframe
        df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))

        # Drop duplicates
        df.drop_duplicates(inplace=True)

        if include_serps:
            # Download serp data in batches
            df = self.get_serp_data(
                country_abbr=country_abbr,
                list_id=list_id,
                keyword_no=len(df)
            )

        if trunc_dict:
            for col in trunc_dict.keys():
                df[col] = df[col].fillna('').apply(lambda x: x[0:trunc_dict[col]])

        # Write out dataframe into csv file
        df.to_csv(csv_path, sep='|', index=False)

        # Return list of distinct keywords
        return df[self._KEYWORD_COLUMN_NAME].tolist()

    def get_serp_data(self, country_abbr: str, list_id: int, keyword_no: int,
                      batch_size: int = 1000):
        """ Extracts serp data in batches.

        Args:
            country_abbr: The abbreviation of the country to export data for. E.g. 'us' or 'se'.
            list_id: The id of the keyword list to extract data from.
            keyword_no: The number of keywords in the list corresponding to <list_id>.
            batch_size: The keywords in each exported batch.

        Returns:
            A dataframe with all the exported serp data.
        """
        serp_export_url = self._build_keyword_export_url(include_serps=True)

        # Iterate over different volume ranges so that each range has <1000 keywords
        df = pd.DataFrame()
        for i in range(0, keyword_no, batch_size):
            # Get indexes of keyword batch for which we will export data
            batch_start = i
            batch_end = min(keyword_no - 1, i + batch_size)

            self.logger.info("Exporting serp for keywords from {} to {}"
                             .format(batch_start, batch_end))

            # Request exported data
            response = self._request(
                method='POST',
                url=serp_export_url,
                data=self._build_keyword_export_body(
                    country_abbr=country_abbr, list_id=list_id, keyword_no=keyword_no,
                    offset=batch_start
                ),
                headers={'Content-type': 'application/json; charset=UTF-8'}
            )

            # Read response data into dataframe
            df = df.append(pd.read_csv(io.StringIO(response.content.decode('utf-8'))))

        # Drop duplicates
        undup_len = len(df)
        df.drop_duplicates(inplace=True)
        self.logger.info(f'{len(df) - undup_len} serp data rows removed by deduplication.')

        return df

    def update_keywords(self, country_abbr: str, keyword_list: List[str]):
        """ Updates the data on the keyword explorer for a given country.

        Args:
            country_abbr: The country for which the keyword data should be updated.
            keyword_list: The keywords that should be updated.
        """
        response = self._request(
            method='POST',
            url=self._UPDATE_SERP_URL,
            data=self._build_keyword_update_body(country_abbr=country_abbr,
                                                 keyword_list=keyword_list),
            headers={'Content-type': 'application/json; charset=UTF-8'}
        )
        self.logger.info(f'Keywords updated for country: {country_abbr}')

    def update_keywords_for_countries(self, country_abbr_list: List[str], keyword_list=List[str]):
        """ Updates the keywords for a number of countries specified in country_abbr_list.

        Args:
            country_abbr: The list of the country abbreviations for which the keyword data
                should be updated.
            keyword_list: The keywords that should be updated.
        """
        for country in country_abbr_list:
            try:
                self.update_keywords(country_abbr=country, keyword_list=keyword_list)
            except HTTPError as e:
                self.logger.exception(e)

    def get_keyword_lists_by_name(self, name_list: List[str]) -> List[Tuple[str, str]]:
        """ Acquires the identifiers/lengths for a list of specified keyword list names.

        Args:
            name_list: The names of the lists for which we extract the ids/lengths.

        Returns:
            A list of identifiers and lengths where the id with the i_th index corresponds
            to the list which has as a name the i_th element of <name_list>.
        """
        to_ke_list_tuple = lambda x: (x['id'], x['length'])
        keyword_lists = self.get_keyword_lists()
        return [to_ke_list_tuple(next(x for x in keyword_lists if x['name'] == name)) for name in
                name_list]

    def get_keyword_lists(self):
        """ Doesn't work as intended, currently causing a 401 or 400 error. Returned valued are hence hardcoded."""
        return [
            {"id": 373534, "name": "US", "length": 1412},
            {"id": 373539, "name": "CH", "length": 186},
            {"id": 375550, "name": "Sweden 2021", "length": 957},
            {"id": 395810, "name": "Brands", "length": 1549},
            {"id": 421932, "name": "Norway 2021", "length": 984},
            {"id": 425668, "name": "Germany 2021", "length": 2024},
            {"id": 431596, "name": "Denmark 2021", "length": 409},
            {"id": 433067, "name": "Finland 2021", "length": 505},
            {"id": 438051, "name": "Snus category", "length": 1292},
            {"id": 438054, "name": "Nicotine pouches category", "length": 117},
            {"id": 438058, "name": "Nicotine free snus and american chew/dip category",
             "length": 30},
            {"id": 438059, "name": "Chewing tobacco and american chew/dip category", "length": 598},
            {"id": 438060, "name": "Nicotine pouches brands", "length": 622},
            {"id": 438061, "name": "Snus brands", "length": 692},
            {"id": 438062, "name": "Nicotine free snus and american chew/dip brands", "length": 58},
            {"id": 438063, "name": "Chewing tobacco and american chew/dip brands", "length": 473},
            {"id": 439050, "name": "Nicotine free snus category", "length": 27},
            {"id": 439052, "name": "Nicotine free snus brands", "length": 58},
            {"id": 439054, "name": "diy snus brands", "length": 59},
            {"id": 442015, "name": "DE TEAMP LIST", "length": 4335},
            {"id": 443813, "name": "EU SCAN FEB 2021", "length": 735},
            {"id": 446106, "name": "snus, nicotine pocuhes mar 2021", "length": 3822},
            {"id": 448793, "name": "chew/dip/loz", "length": 4335},
            {"id": 492156, "name": "pris", "length": 165},
            {"id": 508851, "name": "Store Brands", "length": 190},
            {"id": 540825, "name": "YMYL US", "length": 27},
            {"id": 633150, "name": "DE 202201", "length": 581},
            {"id": 633310, "name": "CH 202201", "length": 220},
            {"id": 633371, "name": "NO 202201", "length": 1115},
            {"id": 633684, "name": "SE 202201", "length": 1433},
            {"id": 633802, "name": "UK 202201", "length": 936},
            {"id": 633807, "name": "US 202201", "length": 3024}
        ]
        """
        return self._request(
            method='POST',
            url=self._GET_KEYWORD_LISTS_URL,
            data={},
            headers={
                'accept': '*/*',
                'cookie': ';'.join([f'{cookie.name}={cookie.value}' for cookie in self.session.cookies]),
                'origin': 'https://app.ahrefs.com',
                'referer': 'https://app.ahrefs.com/keywords-explorer',
                'sec-ch-ua': '',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': 'macOS',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'content-type': 'application/json; charset=UTF-8',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                'accept-encoding': 'gzip, deflate, br',
                'user-agent': ''
            }
        )
        """