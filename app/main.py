from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Brand Compliance API is running"}

@app.post("/upload-brand-kit")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    # Later: Pass contents to extract_pdf.extract_brand_compliance(contents)
    return {"filename": file.filename, "message": "PDF uploaded"}
