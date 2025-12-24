"""
Pydantic schemas untuk request/response validation
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Any

class PredictionRequest(BaseModel):
    """Single prediction request"""
    features: Dict[str, float] = Field(
        ...,
        description="Dictionary of feature values",
        example={
            "rating_average": 0.5,
            "pageCount": 0.3,
            "publicationYear": 0.7,
            "book_age": 0.2,
            "has_awards": 1,
            "title_length": 0.4,
            "adapted_to_movie": 1,
            "genre_encoded": 5,
            "language_encoded": 0,
            "age_category_encoded": 2
        }
    )

class PredictionResponse(BaseModel):
    """Prediction response"""
    prediction: int = Field(..., description="Predicted class (0 or 1)")
    prediction_label: str = Field(..., description="Human-readable label")
    confidence: float = Field(..., description="Confidence score")
    probability: Dict[str, float] = Field(..., description="Class probabilities")
    latency_seconds: float = Field(..., description="Prediction latency")
    model_version: str = Field(..., description="Model version")

class BatchPredictionRequest(BaseModel):
    """Batch prediction request"""
    instances: List[Dict[str, float]] = Field(
        ...,
        description="List of feature dictionaries",
        min_items=1
    )
    
    class Config:
        schema_extra = {
            "example": {
                "instances": [
                    {
                        "rating_average": 0.5,
                        "pageCount": 0.3,
                        "publicationYear": 0.7,
                        "book_age": 0.2,
                        "has_awards": 1,
                        "title_length": 0.4,
                        "adapted_to_movie": 1,
                        "genre_encoded": 5,
                        "language_encoded": 0,
                        "age_category_encoded": 2
                    }
                ]
            }
        }