from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from agent import main

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your extension's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    query: str

@app.post("/search")
async def process_query(request: Query):
    try:
        print(f"Received query: {request.query}")
        result = await main(request.query)
        if result is None:
            raise HTTPException(status_code=500, detail="No response generated")
        return {"answer": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 