import json
import random

class QuestionGame:
    def __init__(self, json_path):
        with open(json_path, 'r') as f:
            self.questions = json.load(f)
        self.score = 0
        self.current_index = 0
        random.shuffle(self.questions)

    def get_next_question(self):
        if self.current_index < len(self.questions):
            q = self.questions[self.current_index]
            self.current_index += 1
            return q
        return None

    def evaluate(self, direction, correct_index):
        if (direction == 'left' and correct_index == 0) or (direction == 'right' and correct_index == 1):
            self.score += 1
            return True
        return False