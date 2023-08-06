import json
import logging
from typing import Union

import requests
from requests.adapters import HTTPAdapter, Retry

from wf_airtable_api_schema.models import *

from .. import const


logger = logging.getLogger(__name__)


class Api:
    def __init__(
        self,
        audience: str = const.WF_AUTH0_AIRTABLE_API_AUDIENCE,
        auth_domain: str = const.WF_AUTH0_DOMAIN,
        client_id: str = const.WF_AUTH0_CLIENT_ID,
        client_secret: str = const.WF_AUTH0_CLIENT_SECRET,
        api_url: str = const.WF_AIRTABLE_API_URL,
    ):
        self.audience = audience
        self.auth_domain = auth_domain
        self.auth_url = f"https://{self.auth_domain}".rstrip("/")

        self.client_id = client_id
        self.client_secret = client_secret

        self.api_url = api_url.rstrip("/")
        self.session = self._init_request_retry_object()
        self.access_token = self._load_access_token()

    def _init_request_retry_object(self):
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.2,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)
        http.mount("http://", adapter)
        return http

    def _load_access_token(self):
        _response = self.session.post(
            url=f"{self.auth_url}/oauth/token",
            data=json.dumps(
                {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "audience": self.audience,
                    "grant_type": "client_credentials",
                }
            ),
            headers={"content-type": "application/json"},
        )

        data = _response.json()
        return data["access_token"]

    def request(self, method, path, params: dict = None, data: Union[dict, bytes] = None):
        url = f"{self.api_url}/{path}"

        d = data
        if isinstance(data, dict):
            d = json.dumps(data).encode("utf-8")

        try:
            _response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=d,
                headers={"content-type": "application/json", "authorization": f"Bearer {self.access_token}"},
            )
            _response.raise_for_status()
            return _response
        except requests.exceptions.HTTPError as err:
            logger.exception(f"Request HTTPError ({err.response.status_code}): {url}")
            raise err
        except requests.exceptions.ConnectionError as err:
            logger.exception(f"Request ConnectionError: {url}")
            raise err
        except requests.exceptions.Timeout as err:
            logger.exception(f"Request Timeout: {url}")
            raise err
        except requests.exceptions.RequestException as err:
            logger.exception(f"Unexpected RequestException ({err.response.status_code}): {url}")
            raise err

    def _request(self, method, path, params: dict = None, data: dict = None):
        _response = self.request(method=method, path=path, params=params, data=data)
        return _response.json()

    def get(self, path, params: dict = None):
        return self._request("GET", path, params)

    def post(self, path, params: dict = None, data: dict = None):
        return self._request("POST", path, params, data)

    def put(self, path, params: dict = None, data: dict = None):
        return self._request("PUT", path, params, data)

    def list_hubs(self) -> ListAPIHubResponse:
        r = self.get("hubs")
        _response = ListAPIHubResponse.parse_obj(r)
        return _response

    def get_hub(self, hub_id) -> APIHubResponse:
        r = self.get(f"hubs/{hub_id}")
        _response = APIHubResponse.parse_obj(r)
        return _response

    def get_hub_regional_site_entrepreneurs(self, hub_id) -> ListAPIPartnerResponse:
        r = self.get(f"hubs/{hub_id}/regional_site_entrepreneurs")
        _response = ListAPIPartnerResponse.parse_obj(r)
        return _response

    def get_hub_pods(self, hub_id) -> ListAPIPodResponse:
        r = self.get(f"hubs/{hub_id}/pods")
        _response = ListAPIPodResponse.parse_obj(r)
        return _response

    def get_hub_schools(self, hub_id) -> ListAPISchoolResponse:
        r = self.get(f"hubs/{hub_id}/schools")
        _response = ListAPISchoolResponse.parse_obj(r)
        return _response

    def list_pods(self) -> ListAPIPodResponse:
        r = self.get("pods")
        _response = ListAPIPodResponse.parse_obj(r)
        return _response

    def get_pod(self, pod_id) -> APIPodResponse:
        r = self.get(f"pods/{pod_id}")
        _response = APIPodResponse.parse_obj(r)
        return _response

    def list_partners(self, page_size=50, offset="") -> ListAPIPartnerResponse:
        r = self.get("partners", {"page_size": page_size, "offset": offset})
        _response = ListAPIPartnerResponse.parse_obj(r)
        return _response

    def get_partner(self, partner_id) -> APIPartnerResponse:
        r = self.get(f"partners/{partner_id}")
        _response = APIPartnerResponse.parse_obj(r)
        return _response

    def list_schools(self, page_size=50, offset="") -> ListAPISchoolResponse:
        r = self.get("schools", {"page_size": page_size, "offset": offset})
        _response = ListAPISchoolResponse.parse_obj(r)
        return _response

    def find_schools(self, organizational_unit: Optional[str] = None) -> ListAPISchoolResponse:
        r = self.get(f"schools/find", {"organizational_unit": organizational_unit})
        _response = ListAPISchoolResponse.parse_obj(r)
        return _response

    def get_school(self, school_id) -> APISchoolResponse:
        r = self.get(f"schools/{school_id}")
        _response = APISchoolResponse.parse_obj(r)
        return _response

    def list_educators(self, page_size=50, offset="") -> ListAPIEducatorResponse:
        r = self.get("educators", {"page_size": page_size, "offset": offset})
        _response = ListAPIEducatorResponse.parse_obj(r)
        return _response

    def get_educator(self, educator_id) -> APIEducatorResponse:
        r = self.get(f"educators/{educator_id}")
        _response = APIEducatorResponse.parse_obj(r)
        return _response

    def find_educators(self, email: Optional[Union[str, list[str]]] = None) -> ListAPIEducatorResponse:
        params = {}
        if email:
            email_param = email
            if isinstance(email, str):
                email_param = [email]

            params["email"] = email_param

        r = self.get(f"educators/find", params)
        _response = ListAPIEducatorResponse.parse_obj(r)
        return _response

    def get_educator_by_email(self, email) -> Optional[APIEducatorResponse]:
        _educators = self.find_educators(email)
        if len(_educators.data) == 0:
            return None

        return APIEducatorResponse(data=_educators.data[0], links=_educators.links, meta=_educators.meta)

    def create_educator(self, educator_payload: CreateAPIEducatorFields) -> APIEducatorResponse:
        r = self.post("educators", data=educator_payload.dict())
        _response = APIEducatorResponse.parse_obj(r)
        return _response

    def find_educators_schools(
        self, educator_id: Optional[str] = None, school_id: Optional[str] = None
    ) -> ListAPIEducatorSchoolResponse:
        r = self.get(f"educators_schools/find", {"educator_id": educator_id, "school_id": school_id})
        _response = ListAPIEducatorSchoolResponse.parse_obj(r)
        return _response

    def create_educator_school(
        self, educator_school_payload: CreateUpdateAPIEducatorSchoolFields
    ) -> APIEducatorSchoolResponse:
        r = self.post("educators_schools", data=educator_school_payload.dict())
        _response = APIEducatorSchoolResponse.parse_obj(r)
        return _response

    def update_educator_school(
        self, record_id: str, educator_school_payload: CreateUpdateAPIEducatorSchoolFields
    ) -> APIEducatorSchoolResponse:
        r = self.put(f"educators_schools/{record_id}", data=educator_school_payload.dict())
        _response = APIEducatorSchoolResponse.parse_obj(r)
        return _response

    def list_geo_area_contacts(self) -> ListAPIGeoAreaContactResponse:
        r = self.get("geo_mapping/contacts")
        _response = ListAPIGeoAreaContactResponse.parse_obj(r)
        return _response

    def get_geo_area_contact_for_address(self, address) -> APIGeoAreaContactResponse:
        r = self.get("geo_mapping/contacts/for_address", params={"address": address})
        _response = APIGeoAreaContactResponse.parse_obj(r)
        return _response

    def get_geo_area_contact(self, geo_area_contact_id) -> APIGeoAreaContactResponse:
        r = self.get(f"geo_mapping/contacts/{geo_area_contact_id}")
        _response = APIGeoAreaContactResponse.parse_obj(r)
        return _response

    def list_geo_area_target_communities(self) -> ListAPIGeoAreaTargetCommunityResponse:
        r = self.get("geo_mapping/target_communities")
        _response = ListAPIGeoAreaTargetCommunityResponse.parse_obj(r)
        return _response

    def get_geo_area_target_community_for_address(self, address) -> APIGeoAreaTargetCommunityResponse:
        r = self.get("geo_mapping/target_communities/for_address", params={"address": address})
        _response = APIGeoAreaTargetCommunityResponse.parse_obj(r)
        return _response

    def get_geo_area_target_community(self, geo_area_target_community_id) -> APIGeoAreaTargetCommunityResponse:
        r = self.get(f"geo_mapping/target_communities/{geo_area_target_community_id}")
        _response = APIGeoAreaTargetCommunityResponse.parse_obj(r)
        return _response

    def create_survey_response(
        self, survey_payload: CreateApiSSJTypeformStartASchoolFields
    ) -> ApiSSJTypeformStartASchoolResponse:
        r = self.post("ssj_typeforms/start_a_school_response", data=survey_payload.dict())
        _response = ApiSSJTypeformStartASchoolResponse.parse_obj(r)
        return _response
