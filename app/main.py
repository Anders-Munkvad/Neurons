from fastapi import FastAPI, UploadFile, File
from image_evaluation import GPT_4o_response
from PIL import Image
from io import BytesIO

from extract_pdf import extract_brand_compliance
from compliance_prompt import build_compliance_prompt

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Brand Compliance API is running"}

# API function to extract brand compliance information from the PDF.
# Testing can be done by requesting the following to the API: curl -X POST http://127.0.0.1:8000/extract_brand_compliance -F "file=@C:\Users\ander\OneDrive - University of Copenhagen\Desktop\Neurons\Neurons_brand_kit.pdf"
@app.post("/extract_brand_compliance")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()  # this gives you raw bytes
    results = extract_brand_compliance(contents)  # pass only the bytes
    return {"Requirements": results, "message": "Requirements"}

# Test: curl -X POST http://127.0.0.1:8000/extract_brand_compliance -F "file=@C:\Users\ander\OneDrive - University of Copenhagen\Desktop\Neurons\Neurons_brand_kit.pdf"
@app.post("/build_compliance_prompt")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()  # raw bytes from PDF
    compliance_data = extract_brand_compliance(contents)  # your updated version that handles bytes
    prompt = build_compliance_prompt(compliance_data)     # build string prompt from dict
    return {
        "Prompt": prompt,
        "message": "Brand compliance prompt successfully generated."
    }

#llava_engine = None

#@app.on_event("startup")
#def load_model():
#    global llava_engine
#    llava_engine = LLaVAEngine()


# Test: curl -X POST http://127.0.0.1:8000/evaluate_brand_compliance_wAPI -F "brand_kit=@C:\Users\ander\OneDrive - University of Copenhagen\Desktop\Neurons\Neurons_brand_kit.pdf" -F "image_file=@C:\Users\ander\OneDrive - University of Copenhagen\Desktop\Neurons\neurons_1.png"
@app.post("/evaluate_brand_compliance_wAPI")
async def evaluate_brand_compliance(
    brand_kit: UploadFile = File(...),
    image_file: UploadFile = File(...)
):
    brand_bytes = await brand_kit.read()
    image_bytes = await image_file.read()
    image = Image.open(BytesIO(image_bytes)).convert("RGB")

    brand_data = extract_brand_compliance(brand_bytes)
    prompt = build_compliance_prompt(brand_data)
    # Call openai api
    response = GPT_4o_response(image_bytes, prompt)

    return {
        "prompt_used": prompt,
        "model_output": response
    }

# Test: curl -X POST http://127.0.0.1:8000/evaluate_brand_compliance -F "brand_kit=@C:\Users\ander\OneDrive - University of Copenhagen\Desktop\Neurons\Neurons_brand_kit.pdf" -F "image_file=@C:\Users\ander\OneDrive - University of Copenhagen\Desktop\Neurons\neurons_1.png"
# @app.post("/evaluate_brand_compliance")
# async def evaluate_brand_compliance(
#     brand_kit: UploadFile = File(...),
#     image_file: UploadFile = File(...)
# ):
#     global llava_engine
#     brand_bytes = await brand_kit.read()
#     image_bytes = await image_file.read()
#     image = Image.open(BytesIO(image_bytes)).convert("RGB")

#     brand_data = extract_brand_compliance(brand_bytes)
#     prompt = build_compliance_prompt(brand_data)
#     response = llava_engine.evaluate(prompt, image)

#     return {
#         "prompt_used": prompt,
#         "model_output": response
#     }

# Function to upload an image - we need to create a function first that can evaluate the image
# @app.post("/upload_image")
# async def upload_pdf(file: UploadFile = File(...)):
#     # Step 1: Upload image

#     # Step 2: Process image

#     # Step 3: return

#     # Considerations: Just upload image or do we just create a single pipeline

#     #contents = await file.read()  # this gives you raw bytes
#     #results = extract_brand_compliance(contents)  # pass only the bytes
#     #return {"Requirements": results, "message": "Requirements"}