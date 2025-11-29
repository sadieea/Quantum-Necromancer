from fastapi import APIRouter
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from typing import List

router = APIRouter()

class LDARequest(BaseModel):
    texts: List[str]
    n_topics: int = 5

@router.post("/lda/analyze")
async def analyze_topics(request: LDARequest) -> dict:
    """Extract topics from text data using LDA."""
    try:
        vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        tfidf = vectorizer.fit_transform(request.texts)
        
        lda = LatentDirichletAllocation(n_components=request.n_topics, random_state=42)
        lda.fit(tfidf)
        
        feature_names = vectorizer.get_feature_names_out()
        topics = []
        
        for topic_idx, topic in enumerate(lda.components_):
            top_indices = topic.argsort()[-10:][::-1]
            keywords = [feature_names[i] for i in top_indices]
            topics.append({
                "topic_id": topic_idx,
                "keywords": keywords,
                "weights": topic[top_indices].tolist()
            })
        
        return {
            "success": True,
            "data": {"topics": topics, "n_topics": request.n_topics},
            "error": None
        }
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}
