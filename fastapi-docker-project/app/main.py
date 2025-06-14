from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from modular import run_visualization_chain
import uvicorn
import os

app = FastAPI(
    title="Visualisation API",
)

class VisualizationRequest(BaseModel):
    question: str

@app.post("/visualise/")
async def create_visualization(request: VisualizationRequest):
    try:
        # Call your existing function from modular.py
        result = run_visualization_chain(request.question)
        
        # Find the generated media file
        media_dir = "app/media/videos/generated_code/480p15/"
        if os.path.exists(media_dir):
            # For Manim visualizations, find the latest MP4 file
            video_files = []
            for root, _, files in os.walk(media_dir):
                for file in files:
                    if file.endswith(".mp4"):
                        video_path = os.path.join(root, file)
                        video_files.append((video_path, os.path.getmtime(video_path)))
            
            if video_files:
                # Get the most recently created video file
                latest_video = sorted(video_files, key=lambda x: x[1], reverse=True)[0][0]
                return FileResponse(
                    path=latest_video, 
                    media_type="video/mp4", 
                    filename=os.path.basename(latest_video)
                )
        
        # Fallback if no video file is found
        return {"status": "success", "message": "Visualization processed but no video file was found"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)