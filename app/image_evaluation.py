# Model: https://huggingface.co/llava-hf/llava-1.5-7b-hf

from transformers import AutoProcessor, AutoModelForVision2Seq
from PIL import Image
import torch

class LLaVAEngine:
    def __init__(self, model_id="llava-hf/llava-1.5-7b-hf", revision="a272c74"):
        self.processor = AutoProcessor.from_pretrained(model_id, revision=revision)
        self.model = AutoModelForVision2Seq.from_pretrained(model_id, revision=revision)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def evaluate(self, prompt: str, image: Image.Image, max_new_tokens: int = 512) -> str:
        # 🧠 LLaVA requires <image> token in the prompt itself
        prompt_with_image_token = f"<image>\n[INST] {prompt} [/INST]"

        # 🛠️ Tokenize text + image at the same time
        inputs = self.processor(
            text=prompt_with_image_token,
            images=image,
            return_tensors="pt"
        )

        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        # 🔁 Generate
        output_ids = self.model.generate(**inputs, max_new_tokens=max_new_tokens)

        # 🧼 Decode
        response = self.processor.tokenizer.batch_decode(
            output_ids[:, inputs["input_ids"].shape[-1]:],
            skip_special_tokens=True
        )[0]

        return response



