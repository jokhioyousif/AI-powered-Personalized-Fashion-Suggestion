# AI-powered-Personalized-Fashion-Suggestion

An **AI-powered fashion styling system** that generates **photorealistic outfit images** tailored to your body attributes and style preferences.
This project combines **Google Colab (for heavy AI computation), FastAPI (backend server), and Streamlit (frontend UI)** to deliver an end-to-end pipeline for personalized fashion generation.

---

## 🚀 Features

* **Face-Aware Outfit Generation**
  Upload your photo, and the AI keeps your facial identity consistent in the generated look.
* **Custom Attributes**
  Define your **height, weight, age, gender**, and **style preferences** (occasion, clothing items, colors).
* **Stable Diffusion-Based Fashion Generation**
  Generates full-body photorealistic outfits using a diffusion pipeline.
* **Face Swapping for Realism**
  Integrates InsightFace face swapper (`inswapper_128.onnx`) for identity preservation.
* **Distributed Architecture**

  * **Colab Worker**: Handles GPU-heavy AI tasks.
  * **FastAPI Backend**: Acts as a bridge between frontend and Colab.
  * **Streamlit Frontend**: User-facing app to input details and view results.

---

## 🛠️ Tech Stack

* **Google Colab** → Runs AI worker with GPU
* **PyTorch + Diffusers** → Stable Diffusion for outfit generation
* **InsightFace** → Face analysis & swapping
* **FastAPI** → Local backend API
* **Streamlit** → Frontend user interface
* **Ngrok** → Public tunnel from Colab to FastAPI

---

## 📂 Project Structure

```
.
├── colab_ai_worker.py   # Runs in Google Colab (AI models + face swap + diffusion generation)
├── fastapi_backend.py   # Local backend server forwarding requests to Colab
├── frontend.py          # Streamlit web app for users
```

---

## ⚙️ Setup Instructions

### 1. Colab Worker

1. Open `colab_ai_worker.py` in Google Colab.
2. Upload the **face swapper model** `inswapper_128.onnx` into Google Drive.
3. Update your **Ngrok token** in the script.
4. Run the notebook → it will output a **public URL**. Copy it.

---

### 2. FastAPI Backend

1. Install dependencies:

   ```bash
   pip install fastapi uvicorn requests
   ```
2. Update `COLAB_AI_WORKER_URL` in `fastapi_backend.py` with the Ngrok public URL from Colab.
3. Run the backend:

   ```bash
   uvicorn fastapi_backend:app --reload
   ```

---

### 3. Streamlit Frontend

1. Install dependencies:

   ```bash
   pip install streamlit pillow requests
   ```
2. Ensure `FASTAPI_BACKEND_URL` in `frontend.py` matches your FastAPI server (default: `http://127.0.0.1:8000/create-look`).
3. Run the frontend:

   ```bash
   streamlit run frontend.py
   ```

---

## ▶️ Usage Flow

1. Start the **Colab AI Worker** → copy the Ngrok URL.
2. Run the **FastAPI backend** → paste Ngrok URL in config.
3. Launch the **Streamlit app**.
4. Upload your photo → enter details → generate look.
5. View and download your personalized fashion image.

---

## 📸 Example Workflow

1. Upload photo: `face.jpg`
2. Enter attributes: `180 cm, 75 kg, 28 years, male`
3. Choose: `Style: streetwear, Occasion: vacation, Items: top, pants, shoes`
4. AI Output: Full-body image with your face + chosen outfit.

---

## ⚠️ Limitations

* Requires **GPU runtime** in Google Colab.
* Dependent on **Ngrok tunnel stability**.
* Only supports **binary gender prompts** for now (can be extended).
* Prompt length is limited due to Stable Diffusion token constraints.

---

## 🌟 Future Enhancements

* Support **multi-gender & body diversity**.
* Export final outfits to **3D try-on** applications.
* Add **multi-language support**.
* Implement **user profile storage** for repeated styling sessions.

---

## 📜 License

MIT License – Free to use and modify.
