# STARK AI - Render + Gemini (Free)

Host on Render with your free Gemini key.

## Deploy to Render (2 mins)

1. Create GitHub repo, upload:
   - main.py
   - index.html
   - requirements.txt
   - render.yaml

2. Go to dashboard.render.com -> New -> Web Service -> Connect your repo

3. Settings:
   - Build: pip install -r requirements.txt
   - Start: uvicorn main:app --host 0.0.0.0 --port $PORT
   - Plan: Free

4. Environment -> Add:
   GEMINI_API_KEY = your key from aistudio.google.com

5. Deploy -> You get https://stark-ai-gemini.onrender.com

## How it works (lightweight)

- Browser: MediaPipe WASM for hands/face (runs on GPU, no server cost)
- FIST gesture -> sends ONE snapshot to /api/analyze -> Gemini 1.5 Flash describes it
- No heavy YOLO per frame, so free tier doesn't die

## Local test

GEMINI_API_KEY=yourkey uvicorn main:app --reload
Open http://localhost:8000
