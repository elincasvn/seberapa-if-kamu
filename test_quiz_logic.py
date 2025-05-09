from quiz_logic import Quiz

dummy_questions = [
    {"question": "2 + 2 = ?", "option_a": "4", "option_b": "5", "answer": "A"},
    {"question": "HTML adalah?", "option_a": "Bahasa Markup", "option_b": "Protokol", "answer": "A"}
]

quiz = Quiz(dummy_questions)

while quiz.has_next_question():
    q = quiz.current_question()
    print(q["question"])
    print("A:", q["option_a"])
    print("B:", q["option_b"])
    quiz.answer_current_question(q["answer"])  # otomatis jawab benar
    quiz.next_question()

print("Skor akhir:", quiz.score)