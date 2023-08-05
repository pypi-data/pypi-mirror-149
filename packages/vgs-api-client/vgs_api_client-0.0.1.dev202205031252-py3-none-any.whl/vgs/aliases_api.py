import vgs_api_client
from vgs_api_client.exceptions import ApiException
from vgs_api_client import Configuration
from vgs_api_client.api import aliases_api
from vgs_api_client.model.alias_format import AliasFormat
from vgs_api_client.model.create_aliases_request import CreateAliasesRequest
from vgs_api_client.model.create_aliases_request_new import CreateAliasesRequestNew
from vgs_api_client.model.update_alias_request import UpdateAliasRequest
from vgs_api_client.model.update_alias_request_data import UpdateAliasRequestData


class Aliases:
    def __init__(self, config: Configuration):
        if not config:
            raise ValueError
        self._api = aliases_api.AliasesApi(vgs_api_client.ApiClient(config))

    def redact(self, data):
        # TODO: validate data and raise meaningful exception on validation error
        try:
            requests = []
            for item in data:
                requests.append(
                    CreateAliasesRequestNew(
                        format=AliasFormat(item.get("format")),
                        value=item.get("value"),
                        classifiers=item.get("classifiers", []),
                        storage=item.get("storage", "PERSISTENT"),
                    )
                )
            create_aliases_request = CreateAliasesRequest(data=requests)

            api_response = self._api.create_aliases(create_aliases_request=create_aliases_request)
            return api_response["data"]
        except ApiException as e:
            raise e
        except Exception as e:
            raise ApiException(f"Failed to redact data ${data}. Exception: ${e}")

    def reveal(self, aliases):
        # TODO: validate data and raise meaningful exception on validation error
        try:
            query = ",".join(aliases) if isinstance(aliases, list) else aliases
            api_response = self._api.reveal_multiple_aliases(q=query)
            return api_response["data"]
        except ApiException as e:
            raise e
        except Exception as e:
            raise ApiException(f"Failed to reveal aliases ${aliases}. Exception: ${e}")

    def delete(self, alias):
        try:
            self._api.delete_alias(alias=alias)
        except ApiException as e:
            raise e
        except Exception as e:
            raise ApiException(f"Failed to reveal delete ${alias}. Exception: ${e}")

    def update(self, alias, data):
        try:
            self._api.update_alias(
                alias=alias,
                update_alias_request=UpdateAliasRequest(
                    UpdateAliasRequestData(data["classifiers"])
                ),
            )
        except ApiException as e:
            raise e
        except Exception as e:
            raise ApiException(f"Failed to update alias ${alias}. Exception: ${e}")
