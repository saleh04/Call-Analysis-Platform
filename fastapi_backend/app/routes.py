from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import tempfile
import os
from app.services.STT import whisper_service
from app.services.intent import intent_classifier
from app.services.rules import rule_engine

router = APIRouter()


class AnalysisResponse(BaseModel):
    transcript: str
    intent: str
    confidence: float
    urgency: str
    department: str


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_audio(file: UploadFile = File(...)):
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        # Step 1: STT - Convert audio to text
        transcript = whisper_service.transcribe(tmp_path)

        # Clean up temp file
        os.unlink(tmp_path)

        # Step 2: Intent Classification
        intent_result = intent_classifier.predict(transcript)
        intent = intent_result["intent"]
        confidence = float(intent_result["confidence"])

        # Step 3: Rule Engine
        routing = rule_engine.get_routing(intent)

        return AnalysisResponse(
            transcript=transcript,
            intent=intent,
            confidence=confidence,
            urgency=routing["urgency"],
            department=routing["department"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))