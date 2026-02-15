from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import firebase_admin
from firebase_admin import credentials, db
import google.generativeai as genai

# Load env variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Init FastAPI app
app = FastAPI()

# Init Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://upasthit-hai-default-rtdb.firebaseio.com/"
})

class QueryRequest(BaseModel):
    student_id: str
    query: str


@app.post("/chatbot")
def chatbot(req: QueryRequest):

    # 1. Load complete NEW node (BLE + classes + all students)
    new_data = db.reference("NEW").get()

    if new_data is None:
        return {"reply": "Database is empty."}

    classes = new_data.get("classes", {})
    ble_data = new_data.get("BLE", {})

    # 2. Identify student in class
    student_data = None
    student_class = None

    for class_id, class_info in classes.items():
        if "students" in class_info and req.student_id in class_info["students"]:
            student_data = class_info["students"][req.student_id]
            student_class = class_id
            break

    if student_data is None:
        return {"reply": "❌ Student not found in database."}

    # 3. BLE location detection
    current_class = None
    for ble_id, ble_info in ble_data.items():
        try:
            if req.student_id in ble_info["inRangeDevices"]["students"]:
                current_class = ble_info["class"]
                break
        except:
            pass

    # 4. Build prompt with FULL DATA
    prompt = f"""
    You are an intelligent attendance AI assistant.

    Student ID: {req.student_id}
    Student Class: {student_class}
    Student Attendance:
    {student_data}

    BLE Location:
    {current_class}

    FULL_DATA:
    {new_data}

    User Query:
    {req.query}

    RULES:
    - Give a moderate-length answer (3-6 lines).
    - Expand the explanation ONLY if the question requires more detail.
    - Keep the response clear, simple, and easy to read.
    - No raw JSON, no code, no special characters like '*' or '\n'.
    - Do NOT repeat the user's question in the reply.
    - Focus on useful insights: comparisons, averages, trends, risks, analysis.
    - Never write long paragraphs; keep sentences concise.
    - If needed, provide brief context but stay within the 3-5 line limit."""



    # 5. Call Gemini
    response = model.generate_content(prompt)

    # 6. Clean reply text
    cleaned = (
        response.text
        .replace("\\n", " ")
        .replace("\n", " ")
        .replace("*", "")
        .replace("  ", " ")
    ).strip()

    return {"reply": cleaned}
