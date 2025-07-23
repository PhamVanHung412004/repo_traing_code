import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

class Qwen3PhysicsTester:
    def __init__(self, base_model_name: str):
        self.base_model_name = base_model_name
        self.model = None
        self.tokenizer = None
        self.device = None

    def setup_device(self, force_cpu: bool = False):
        if force_cpu:
            self.device = "cpu"
            print("🖥️ Force sử dụng CPU")
        else:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"📱 Sử dụng device: {self.device}")
        if self.device == "cuda":
            print(f"   GPU: {torch.cuda.get_device_name(0)}")
            print(f"   VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")

    def load_model_from_fold(self, fold_dir: str, use_quantization: bool = False):
        print(f"\n📂 Loading model từ: {fold_dir}")
        self.tokenizer = AutoTokenizer.from_pretrained(fold_dir, trust_remote_code=True)
        print("   Loading base model...")
        if self.device == "cuda" and use_quantization:
            from transformers import BitsAndBytesConfig
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
            )
            base_model = AutoModelForCausalLM.from_pretrained(
                self.base_model_name,
                quantization_config=bnb_config,
                device_map="auto",
                trust_remote_code=True,
            )
        elif self.device == "cuda":
            base_model = AutoModelForCausalLM.from_pretrained(
                self.base_model_name,
                torch_dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True,
            )
        else:
            base_model = AutoModelForCausalLM.from_pretrained(
                self.base_model_name,
                torch_dtype=torch.float32,
                device_map="cpu",
                trust_remote_code=True,
            )
        print("   Loading LoRA adapter...")
        self.model = PeftModel.from_pretrained(base_model, fold_dir)
        self.model.eval()
        print("✅ Model loaded successfully!")

    def Gen_Asne_Optimized(self, messages, target_tokens=500, enable_thinking=True):
        tokenizer = self.tokenizer
        model = self.model
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=enable_thinking
        )
        model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=target_tokens,
            do_sample=True,
            temperature=0.9,
            top_k=50,
            top_p=0.95,
            eos_token_id=tokenizer.eos_token_id
        )
        output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()
        try:
            index = len(output_ids) - output_ids[::-1].index(151668)
        except ValueError:
            index = 0
        thinking_content = tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
        content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")
        return thinking_content, content

    def generate_response(self, question: str, system_prompt: str = None, max_new_tokens: int = 700, temperature: float = 0.7, top_p: float = 0.9, enable_thinking=True) -> str:
        if self.model is None:
            raise ValueError("Model chưa được load!")
        if system_prompt:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ]
            print("\n[DEBUG] Prompt chat template:")
            print(messages)
            thinking, content = self.Gen_Asne_Optimized(messages, target_tokens=max_new_tokens, enable_thinking=enable_thinking)
            return thinking, content
        else:
            prompt = question
            print("\n[DEBUG] Prompt truyền vào model:")
            print(prompt)
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=max_new_tokens
            )
            if self.device == "cuda":
                inputs = inputs.to("cuda")
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_new_tokens,
                    temperature=temperature,
                    do_sample=True,
                    top_p=top_p,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                )
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            response = generated_text[len(prompt):].strip()
            return response 