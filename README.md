# Seberapa IF Kamu? 🎓💻

An interactive Informatics quiz filter where you answer questions by turning your head left or right.

## 🎯 Features
- Head movement detection using MediaPipe (left/right)
- Real-time scoring with visual feedback (BENAR / SALAH)
- Questions overlaid on camera feed
- JSON-based question management

## 📂 Folder Structure
```
Seberapa_IF_Kamu/
├── assets/
│   ├── soal.json
│   ├── sound_correct.mp3 (you provide)
│   ├── sound_wrong.mp3 (you provide)
│   └── haarcascade_frontalface_default.xml
├── main.py
├── quiz_logic.py
├── head_tracker.py
├── test_camera.py
├── test_quiz_logic.py
├── requirements.txt
└── README.md
```

## 🧪 Quick Start
```bash
pip install -r requirements.txt
python main.py
```

## 👁️ Head Movement
- Turn **left** → answer A
- Turn **right** → answer B

## 📄 Soal Format (assets/soal.json)
```json
[
  {
    "question": "Apa itu algoritma?",
    "option_a": "Langkah logis",
    "option_b": "Bahasa Inggris",
    "answer": "A"
  }
]
```

## 🛠️ Test
```bash
python test_camera.py       # test webcam
python test_quiz_logic.py   # test quiz logic
```