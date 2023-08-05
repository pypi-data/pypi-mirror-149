__all__ = ['DocumentService']

from ..api_client import MyLassiApiClient
from ..schemas.documents import *


class DocumentService(MyLassiApiClient):
    def create_document(self, data: DocumentOptionData) -> DocumentData:
        request_data = DocumentOptionSchema.dump(data)

        response = self.post('/api/v2/documents', request_data)

        return DocumentSchema.load(response)

    def get_document(self, doc_id: str) -> DocumentData:
        response = self.get(f'/api/v2/documents/{doc_id}')

        return DocumentSchema.load(response)

    def update_document(self, doc_id: str, data: DocumentOptionData) -> DocumentData:
        request_data = DocumentOptionSchema.dump(data)
        response = self.post(f'/api/v2/documents/{doc_id}', request_data)

        return DocumentSchema.load(response)
