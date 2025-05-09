
class Quiz:
    def __init__(self, questions):
        self.questions = questions
        self.index = 0
        self.score = 0

    def has_next_question(self):
        return self.index < len(self.questions)

    def current_question(self):
        if self.has_next_question():
            return self.questions[self.index]
        return None

    def answer_current_question(self, answer):
        correct_answer = self.questions[self.index]['answer']
        if answer == correct_answer:
            self.score += 1

    def next_question(self):
        self.index += 1
