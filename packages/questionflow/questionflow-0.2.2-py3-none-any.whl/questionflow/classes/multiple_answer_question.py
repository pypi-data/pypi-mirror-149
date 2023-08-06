from typing import List, Union

from questionflow.classes import Question
from questionflow.classes.answer import Answer


class MultipleAnswerQuestion(Question):
    def __init__(self, prompt: str, min_number_answers: int = 1, max_number_answers: int = None,
                 required_number_answers: int = None):
        super().__init__(prompt=prompt)

        self._required_number_answers = required_number_answers
        self._min_number_answers = required_number_answers or min_number_answers
        self._max_number_answers = required_number_answers or max_number_answers

        self._answers: List[Answer] = []

    def __eq__(self, other: 'MultipleAnswerQuestion') -> bool:
        return self._prompt == other._prompt and self._answers == other._answers

    @property
    def _how_many_answers_can_provide_message(self) -> str:
        if self._required_number_answers:
            return f"{self._required_number_answers} answer{'s' if self._required_number_answers > 1 else ''}"

        if self._min_number_answers == self._max_number_answers:
            return f"{self._min_number_answers} answer{'s' if self._min_number_answers > 1 else ''}"

        if self._max_number_answers is None:
            return f"{self._min_number_answers} or more answers"

        return f"{self._min_number_answers}-{self._max_number_answers} answers"

    @property
    def prompt(self) -> str:
        ask = self._prompt
        ask += f"\nSelect {self._how_many_answers_can_provide_message} (separate with commas)"
        return ask

    @property
    def confirmation_prompt(self) -> Union[str, None]:
        if not self._answers:
            return None
        return f"Is '{', '.join([answer.value for answer in self._answers])}' correct?"

    def add_answer(self, answer: Answer) -> bool:
        """
        Add an answer to the question.
        :return: Always True.
        """
        self._answers.append(answer)
        return True

    def add_answers(self, answers: List[Answer]) -> bool:
        """
        Add multiple answers to the question.
        :return: Always True.
        """
        for answer in answers:
            if not self.add_answer(answer):
                return False
        return True

    def reset_answer(self) -> None:
        self._answers = []

    @property
    def is_complete(self) -> bool:
        """
        :return: True if question has been answered properly, False otherwise.
        """
        if not self._answers:
            return False

        if len(self._answers) < self._min_number_answers:
            return False

        if len(self._answers) > self._max_number_answers:
            return False

        return True

    @property
    def answer(self) -> List[Answer]:
        return self._answers
