from enum import Enum
from typing import Union

from questionflow.classes import Question
from questionflow.classes.answer import Answer


class YesNo(Enum):
    YES = "y"
    NO = "n"

    @classmethod
    def to_enum(cls, value: str) -> Union["YesNo", None]:
        if value == cls.YES.value:
            return cls.YES
        elif value == cls.NO.value:
            return cls.NO
        else:
            return None


class YesNoAnswer(Answer):
    def __init__(self, value: YesNo):
        super().__init__(value=value.value)

    @property
    def enum(self) -> YesNo:
        return YesNo(self.value)


def is_valid_yes_no_answer(answer: Answer) -> bool:
    """
    Validate the answer.
    :return: True if the answer is valid, False if the answer is invalid.
    """
    if isinstance(answer, YesNoAnswer):
        return True

    value = answer.value
    if value == YesNo.YES.value or value == YesNo.NO.value:
        return True

    return False


class YesNoQuestion(Question):
    def __init__(self, prompt: str):
        super().__init__(prompt=prompt)

    def add_answer(self, answer: Answer) -> bool:
        """
        Add an answer to the question.
        :return: True if the answer was noted, False if the answer is invalid.
        """
        if not is_valid_yes_no_answer(answer):
            return False

        self._answer = answer
        return True

    @property
    def answer(self) -> Union[YesNoAnswer, None]:
        if not self._answer:
            return None
        answer_value = self._answer.value
        answer_enum = YesNo.to_enum(value=answer_value)
        if not answer_enum:  # how did this answer get stored if it's not valid?
            return None
        return YesNoAnswer(value=answer_enum)

    @property
    def prompt(self) -> str:
        return f"{self._prompt} [y/n]"

    @property
    def confirmation_prompt(self) -> Union[str, None]:
        if not self._answer:
            return None
        return f"Is '{self._answer.value}' correct?"
