__all__ = ['ResultStorageService']

from ..api_client import MyLassiApiClient
from ..schemas.result_storage import *


class ResultStorageService(MyLassiApiClient):
    def all_results(self, page: int = 1) -> ResultStorageListData:
        assert page >= 1

        params = {
            'page': page
        }

        response = self.get(f'/api/v2/resultStorage', params)

        return ResultStorageListSchema.load(response)

    def get_result(self, doc_id: str) -> ResultStorageData:
        response = self.get(f'/api/v2/resultStorage/{doc_id}')

        return ResultStorageSchema.load(response)
