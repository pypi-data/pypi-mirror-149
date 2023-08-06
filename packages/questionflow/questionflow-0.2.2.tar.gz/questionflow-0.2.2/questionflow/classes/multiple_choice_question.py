from typing import List, Union

from questionflow.classes import Question
from questionflow.classes.answer import Answer


class Choice:
    def __init__(self, display_value: str, internal_value=None):
        self.display_value = display_value
        self.internal_value = internal_value or display_value

    def __eq__(self, other: 'Choice') -> bool:
        return self.display_value == other.display_value and self.internal_value == other.internal_value


class MultipleChoiceQuestion(Question):
    def __init__(self, prompt: str, choices: List[Choice], min_number_choices: int = 1, max_number_choices: int = 1,
                 required_number_choices: int = None, allow_all_choices: bool = False):
        super().__init__(prompt=prompt)
        self.choices = {}
        for num, choice in enumerate(choices):
            self.choices[num] = choice
        self._required_number_choices = required_number_choices
        self._min_number_choices = required_number_choices or min_number_choices
        self._max_number_choices = required_number_choices or (
            len(choices) if allow_all_choices else max_number_choices)

        self._selected_choices: List[Choice] = []

    def __eq__(self, other: 'MultipleChoiceQuestion') -> bool:
        return self._prompt == other._prompt and self._selected_choices == other._selected_choices

    @property
    def _how_many_choices_can_select_message(self) -> str:
        if self._required_number_choices:
            return f"{self._required_number_choices} choice{'s' if self._required_number_choices > 1 else ''}"

        if self._min_number_choices == self._max_number_choices:
            return f"{self._min_number_choices} choice{'s' if self._min_number_choices > 1 else ''}"

        return f"{self._min_number_choices}-{self._max_number_choices} choices"

    @property
    def prompt(self) -> str:
        ask = self._prompt
        for num, choice in self.choices.items():
            ask += f"\n{num + 1}) {choice.display_value}\n"
        ask += f"\nSelect {self._how_many_choices_can_select_message} (separate with commas)"
        return ask

    @property
    def confirmation_prompt(self) -> Union[str, None]:
        if not self._selected_choices:
            return None
        return f"Is '{', '.join([choice.display_value for choice in self._selected_choices])}' correct?"

    def _validate_choice(self, choice: Choice) -> bool:
        """
        Validate the choice to the question.
        :return: True if the choice is valid, False otherwise.
        """
        selections = self._selected_choices or []

        if len(selections) + 1 > self._max_number_choices:
            # adding this would make it too many choices selected
            return False

        for selection in selections:
            if choice == selection:
                return True
        return False

    def _answer_to_choice(self, answer: Answer) -> Union[Choice, None]:
        """
        Convert an answer to a choice.
        :return: The matching choice, or None if no match.
        """
        for choice in self.choices.values():
            if choice.internal_value == answer.value:  # answer must match internal value, not display value
                return choice
        return None

    def select_choice(self, choice: Choice) -> bool:
        """
        Select a choice.
        :return: True if the choice was noted, False if the choice is invalid.
        """
        if not self._validate_choice(choice):
            return False

        self._selected_choices.append(choice)
        return True

    def select_choices(self, choices: List[Choice]) -> bool:
        """
        Select multiple choices.
        :return: True if all choices were noted, False if any choice is invalid.
        """
        for choice in choices:
            if not self.select_choice(choice):
                return False
        return True

    def select_choice_number(self, choice_number: int) -> bool:
        """
        Select a choice by number.
        :return: True if the choice was noted, False if the choice is invalid.
        """
        choice_number -= 1  # convert to zero-based index
        if choice_number not in self.choices.keys():
            return False

        self._selected_choices.append(self.choices[choice_number])
        return True

    def select_choice_numbers(self, choice_numbers: List[int]) -> bool:
        """
        Select multiple choices by number.
        :return: True if the choices were noted, False if the choices are invalid.
        """
        for choice_number in choice_numbers:
            if not self.select_choice_number(choice_number=choice_number):
                return False
        return True

    def add_answer(self, answer: Answer) -> bool:
        """
        Add an answer to the question.
        :return: True if the answer was noted, False if the answer is invalid.
        """
        choice = self._answer_to_choice(answer=answer)

        if not choice:
            return False

        return self.select_choice(choice)

    def add_answers(self, answers: List[Answer]) -> bool:
        """
        Add multiple answers to the question.
        :return: True if all answers were noted, False if any answer is invalid.
        """
        for answer in answers:
            if not self.add_answer(answer):
                return False
        return True

    def reset_answer(self) -> None:
        self._selected_choices = []

    @property
    def is_complete(self) -> bool:
        """
        :return: True if question has been answered properly, False otherwise.
        """
        if not self._selected_choices:
            return False

        if len(self._selected_choices) < self._min_number_choices:
            return False

        if len(self._selected_choices) > self._max_number_choices:
            return False

        return True

    @property
    def answer(self) -> List[Choice]:
        return self._selected_choices
