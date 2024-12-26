import requests


class QuizBrain:

    def __init__(self):
        self.questions = {}

##### PONER qtype="boolean" #####################
    def new_questions(self, amount=10, qtype=None, category=None, difficulty=None):
        api_url = "https://opentdb.com/api.php?"
        parameters = f"amount={amount}"
        if qtype is not None:
            parameters += f"&type={qtype}"
        if category is not None:
            parameters += f"&category={category}"
        if difficulty is not None:
            parameters += f"&difficulty={difficulty}"
        response = requests.get(url=api_url, params=parameters)
        data = response.json()
        self.questions = data
        return self.questions
