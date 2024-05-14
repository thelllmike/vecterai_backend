from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import vtracer
from PIL import Image
import io
import os

app = FastAPI()

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")
    
    image_bytes = await file.read()
    try:
        # Convert image from bytes and get SVG string
        svg_string = convert_image_from_bytes(image_bytes, file.filename.split('.')[-1])
        svg_filename = f"{file.filename}.svg"
        with open(svg_filename, "w") as svg_file:
            svg_file.write(svg_string if svg_string else "")
        return FileResponse(path=svg_filename, filename=svg_filename, media_type='image/svg+xml')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def convert_image_from_bytes(input_bytes, img_format):
    """Converts image from raw bytes to SVG string."""
    try:
        return vtracer.convert_raw_image_to_svg(input_bytes, img_format=img_format)
    except Exception as e:
        print(f"Error converting from bytes: {e}")
        return None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
