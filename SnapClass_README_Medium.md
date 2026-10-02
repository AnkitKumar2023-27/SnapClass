# SnapClass

SnapClass is an AI-powered attendance management system that uses face recognition, liveness detection, voice verification, and geofencing to make classroom attendance faster and more secure.

## 🚀 Live Demo

https://snapclass-aith.streamlit.app/

## ✨ Features

- Face recognition-based attendance
- Liveness check to reduce photo-based proxy attendance
- Voice verification
- Student and teacher portals
- Teacher dashboard with bulk classroom attendance
- AI attendance chatbot using RAG
- Attendance analytics and charts
- Email alerts
- GPS-based geofencing
- Secure teacher authentication with bcrypt
- Supabase PostgreSQL database

## 🏗️ How It Works

### Student Flow

```text
Student
   ↓
Liveness Check
   ↓
Face Recognition
   ↓
Student Verification
   ↓
Attendance Marked
   ↓
Student Dashboard
```

### Teacher Flow

```text
Teacher Login
   ↓
Select Subject
   ↓
Upload Classroom Photo
   ↓
AI Face Analysis
   ↓
Review Attendance
   ↓
Save Attendance
```

## 🧠 AI / ML

SnapClass uses dlib to generate 128-dimensional face embeddings and an SVM classifier to identify registered students.

For liveness detection, OpenCV is used with a challenge-response approach such as smile, head movement, or mouth opening.

Voice verification uses Resemblyzer to generate voice embeddings and compare speaker similarity.

The project also includes an AI chatbot based on RAG. Attendance information is retrieved from Supabase and provided as context to Cerebras LLaMA 3.3 70B for generating responses.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core development |
| Streamlit | Main application |
| Flask | Landing page |
| dlib | Face recognition |
| OpenCV | Liveness detection |
| SVM | Face classification |
| Resemblyzer | Voice verification |
| Supabase PostgreSQL | Database |
| Cerebras LLaMA 3.3 70B | AI chatbot |
| bcrypt | Password hashing |
| Plotly | Analytics |
| Haversine Formula | Geofencing |

## 📁 Project Structure

```text
SnapClass/
├── app.py
├── requirements.txt
├── haarcascade.xml
│
├── src/
│   ├── screens/
│   │   ├── home_screen.py
│   │   ├── student_screen.py
│   │   └── teacher_screen.py
│   │
│   ├── components/
│   │   ├── header.py
│   │   ├── footer.py
│   │   ├── subject_card.py
│   │   ├── ai_chatbot.py
│   │   ├── email_alerts.py
│   │   └── database/
│   │       ├── config.py
│   │       └── db.py
│   │
│   ├── pipelines/
│   │   ├── face_pipeline.py
│   │   ├── voice_pipeline.py
│   │   ├── liveness_pipeline.py
│   │   └── geofence_pipeline.py
│   │
│   └── ui/
│       └── base_layout.py
│
└── landing/
    ├── app.py
    └── templates/
        └── index.html
```

streamlit run app.py
```

## 🔐 Security

The project includes multiple security layers:

- Liveness verification
- bcrypt password hashing
- GPS geofencing
- Supabase Row Level Security
- Face embeddings instead of raw face images in the documented storage design

## ⚠️ Current Limitations

- Face recognition can be affected by poor lighting.
- Identical twins may be difficult to distinguish using face recognition alone.
- The current implementation is designed for a relatively small classroom scale.
- The application is dependent on cloud services for its current database workflow.

## 🔮 Future Improvements

- FAISS or pgvector for large-scale face search
- Offline attendance with automatic synchronization
- Better low-light face processing
- Stronger multi-factor authentication
- Improved large-class batch processing

## 🎯 Project Highlights

SnapClass demonstrates practical implementation of:

- Computer Vision
- Face Recognition
- Machine Learning
- Speaker Verification
- Liveness Detection
- RAG and LLM integration
- PostgreSQL
- Authentication
- Geofencing
- Data Visualization

## 🌐 Live Application

[Open SnapClass](https://snapclass-aith.streamlit.app/)
