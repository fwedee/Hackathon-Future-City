import os
from fastapi import APIRouter, HTTPException
from google import genai

from app import schemas

router = APIRouter()

def get_google_ai_client():
    """Initialize Google AI client with error handling."""
    api_key = os.getenv("UV_GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("UV_GOOGLE_API_KEY not set in environment")
    print("API_KEY", api_key)
    client = genai.Client(api_key=api_key)
    return client

@router.post("/ask", response_model=schemas.AskResponse, tags=["ai"])
async def ask_gpt(request: schemas.AskRequest):
    """
    Ask Google AI a question with page context.
    """
    try:
        client = get_google_ai_client()
        
        system_prompt = """You are a helpful assistant inside a data analytics dashboard.
            Always answer shortly (max 3 sentences) and be precise.
            If the data does not contain the answer, say so explicitly.
            Do not make up answers.
        """
        
        context_text = f"Page data:\n{request.pageContext}\n"
        user_message = f"{context_text}\nUser question: {request.question}"
        
        # Combine system prompt and user message
        full_prompt = f"{system_prompt}\n\n{user_message}"
        
        # Generate response using Google AI
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )
        
        answer = response.text if response and hasattr(response, 'text') else "No response from model."
        
        return schemas.AskResponse(answer=answer)
        
    except Exception as e:
        print(f"Error calling Google AI: {e}")
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")
