AI Attendance Chatbot (FastAPI + Firebase + Gemini)
📌 Overview

This project is an AI-powered Attendance Chatbot built using:

FastAPI (Backend API)

Firebase Realtime Database

Google Gemini (Generative AI)

BLE-based student location tracking

The chatbot analyzes:

Student attendance data

Class details

BLE live location data

Full database structure

It provides intelligent insights like attendance trends, comparisons, risks, and summaries.

🚀 Features

Fetch student data from Firebase

Detect student class automatically

Detect live location using BLE nodes

Generate AI-based analytical responses

Clean formatted output (no raw JSON, no special characters)

Moderate-length intelligent answers

🛠 Tech Stack

Python

FastAPI

Firebase Admin SDK

Google Generative AI (Gemini 2.0 Flash)

dotenv

📂 Project Structure
chat-bot/
│── main.py
│── requirements.txt
│── .env
│── .gitignore
│── serviceAccountKey.json
│── README.md

⚙️ Setup Instructions
1️⃣ Clone the repository
git clone https://github.com/your-username/chat-bot.git
cd chat-bot

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Create .env file
GEMINI_API_KEY=your_api_key_here

4️⃣ Add Firebase Service Key

Download Firebase service account key and place:

serviceAccountKey.json


in the root directory.

5️⃣ Run the server
uvicorn main:app --reload


Server runs at:

http://127.0.0.1:8000

📡 API Endpoint
POST /chatbot

Request Body:

{
  "student_id": "S101",
  "query": "How is my attendance performance?"
}


Response:

{
  "reply": "Your attendance is above class average. You are consistent but slight improvement in practical sessions will strengthen your overall performance."
}

🧠 How It Works

Fetch complete NEW node from Firebase

Identify student and class

Detect BLE location

Build structured AI prompt

Generate smart attendance insights using Gemini

Clean and return formatted response

🔐 Security Notes

Never push .env file

Never push serviceAccountKey.json

Always use .gitignore

🎯 Use Case

Designed for:

Smart Attendance Systems

IoT + BLE tracking solutions

AI-powered student analytics

Educational institutions

👨‍💻 Author

Piyush Sutar
CSE (AI & ML)
Focused on building production-ready AI systems.