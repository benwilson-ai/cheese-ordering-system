from langchain_openai import OpenAIEmbeddings
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import uuid
import json
from app.core.config import settings, ModelType
from app.schemas.cheese_data import CheeseData
from typing import List

class VectorDBService:
    def __init__(self):
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.dims = 1536
        self.spec = ServerlessSpec(cloud="aws", region="us-east-1")
        self.index = self._initialize_index()
        self.embed_model = OpenAIEmbeddings(
            model=ModelType.embedding,
            openai_api_key=settings.OPENAI_API_KEY
        )

    def _initialize_index(self):
        existing_indexes = self.pc.list_indexes()
        
        if settings.PINECONE_INDEX_NAME not in [item["name"] for item in existing_indexes]:
            self.pc.create_index(
                name=settings.PINECONE_INDEX_NAME,
                dimension=self.dims,
                metric='cosine',
                spec=self.spec
            )
        return self.pc.Index(settings.PINECONE_INDEX_NAME)

    def _generate_vector_text(self, cheese) -> str:
        fields = [
            (cheese['name'], "name"),
            (cheese['brand'], "brand"),
            (cheese['department'], "department")
        ]
        return "\n".join([f"{label}: {value}" for value, label in fields if value])

    def upsert_cheese(self, cheese):
        embedding_id = str(uuid.uuid4())
        # metadata = cheese.model_dump()
        metadata = {}
        metadata['image_url'] = cheese['image_url']
        metadata['name'] = cheese['name']
        metadata['brand'] = cheese['brand']
        metadata['department'] = cheese['department']
        metadata['more_image_url'] = cheese['more_image_url']
        metadata['each_count'] = cheese['itemCounts']['EACH'] 
        metadata['each_dimension'] = cheese['dimensions']['EACH']
        metadata['each_weight'] = cheese['weights']['EACH']
        metadata['each_price'] = cheese['prices'].get('EACH', "")
        if(cheese['itemCounts'].get('CASE', "")!=""):
            metadata['case_count'] = cheese['itemCounts'].get('CASE', "")
        if(cheese['dimensions'].get('CASE', "")!=""):
            metadata['case_dimension'] = cheese['dimensions'].get('CASE', "")
        if(cheese['weights'].get('CASE', "")!=""):
            metadata['case_weight'] = cheese['weights'].get('CASE', "")
        if(cheese['prices'].get('CASE', "")!=""):
            metadata['case_price'] = cheese['prices'].get('CASE', "")
        metadata['relateds'] = cheese['relateds']
        metadata['sku'] = cheese['sku']
        metadata['price_per'] = cheese['price_per']
        metadata['product_url'] = cheese['product_url']
        if(cheese.get('wholesale', "")!=""):
            metadata['wholesale'] = cheese.get('wholesale', "")
        metadata['out_of_stock'] = cheese['out_of_stock']
        metadata['priceOrder'] = cheese['priceOrder']
        metadata['popularityOrder'] = cheese['popularityOrder']
        metadata['weight_unit'] = cheese['weight_unit']
        vector = [{
            'id': embedding_id,
            'values': self.embed_model.embed_documents(self._generate_vector_text(cheese))[0],
            'metadata': metadata,
        }]
        self.index.upsert(vectors=vector)
        return embedding_id

    def query(self, query_text: str, top_k: int = 5, filter: str = None) -> List[CheeseData]:
        vector = self.embed_model.embed_documents([query_text])[0]
        results = self.index.query(
            vector=vector,
            top_k=top_k,
            filter=json.loads(filter),
            include_metadata=True,
            include_values=False,
        )
        return [CheeseData(**match['metadata']) for match in results['matches']]

vector_db = VectorDBService()