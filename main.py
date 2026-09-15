from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os
import base64

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini setup - key from Render env var
GEMINI_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/analyze")
async def analyze(request: Request):
    try:
        data = await request.json()
        image_b64 = data.get("image", "")
        prompt = data.get("prompt", "What do you see in this image? Be Stark JARVIS style, concise, tactical.")
        
        if not GEMINI_KEY or not model:
            return JSONResponse({"error": "GEMINI_API_KEY not set on Render", "mock": "MOCK: I see a person in front of camera, desk setup detected. (Add GEMINI_API_KEY in Render env vars for real AI)"})
        
        # Remove data URL prefix if present
        if "," in image_b64:
            image_b64 = image_b64.split(",")[1]
        
        image_bytes = base64.b64decode(image_b64)
        
        response = model.generate_content([
            {"mime_type": "image/jpeg", "data": image_bytes},
            prompt
        ])
        
        return {"text": response.text}
    except Exception as e:
        return JSONResponse({"error": str(e), "text": f"Error: {e}"}, status_code=500)

@app.post("/api/jarvis")
async def jarvis(request: Request):
    try:
        data = await request.json()
        message = data.get("message", "")
        context = data.get("context", "")
        
        if not model:
            return {"text": f"MOCK JARVIS: You said '{message}'. Context: {context[:100]}. (Set GEMINI_API_KEY for real AI)"}
        
        full_prompt = f"You are JARVIS, Tony Stark's AI. Tactical, witty, concise. Context from camera: {context}\nUser: {message}\nJARVIS:"
        response = model.generate_content(full_prompt)
        return {"text": response.text}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
