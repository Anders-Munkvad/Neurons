from fastapi import FastAPI, UploadFile, File

from extract_pdf import extract_brand_compliance

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Brand Compliance API is running"}


# curl -X POST http://127.0.0.1:8000/extract_brand_compliance -F "file=@C:\Users\ander\OneDrive - University of Copenhagen\Desktop\Neurons\Neurons_brand_kit.pdf"
@app.post("/extract_brand_compliance")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()  # this gives you raw bytes
    results = extract_brand_compliance(contents)  # pass only the bytes
    return {"Requirements": results, "message": "Requirements"}