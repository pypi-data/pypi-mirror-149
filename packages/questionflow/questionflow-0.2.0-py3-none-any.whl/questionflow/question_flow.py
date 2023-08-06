from typing import Union, List, Optional

from questionflow.classes import Question, Answer, MultipleChoiceQuestion, Choice, YesNoQuestion, YesNoAnswer, YesNo


class ProcessedAnswer:
    def __init__(self, valid: bool, error_message: str = None):
        self.valid = valid
        self.error_message = error_message


def _process_regular_answer(question: Question, answer_string: str) -> bool:
    answer = Answer(value=answer_string)
    if not question.add_answer(answer):  # a regular question will never fail to add an answer
        return False
    return True


def _process_yes_or_no_answer(question: YesNoQuestion, answer_string: str) -> bool:
    answer = Answer(value=answer_string)
    if not question.add_answer(answer):  # answer is not valid yes or no
        return False
    return True


def _process_multiple_choice_answer(question: MultipleChoiceQuestion, answer_string: str) -> bool:
    choice_numbers = [int(num) for num in answer_string.split(',')]
    if not question.select_choice_numbers(choice_numbers=choice_numbers):  # one or more choice numbers not valid
        return False
    return True


class QuestionFlow:
    def __init__(self, questions: List[Union[Question, MultipleChoiceQuestion]]):
        starter_question = Question(prompt="INTERNAL: placeholder")
        starter_question.add_answer(Answer(value="INTERNAL: placeholder"))
        self._questions = [starter_question] + questions
        # add an empty element at the beginning to pop
        self._qa_map = {}
        self._current_question_number = 0

    @property
    def _current_question(self) -> Union[Question, MultipleChoiceQuestion, YesNoQuestion, None]:
        if len(self._questions) == 0:
            return None
        return self._questions[0]

    @property
    def _previous_answered_question(self) -> Union[Question, MultipleChoiceQuestion, YesNoQuestion, None]:
        return self._qa_map.get(self._current_question_number, None)

    @property
    def has_more_questions(self) -> bool:
        """
        Check if there are more questions to answer.
        :return: True if there are more questions to answer, False otherwise
        """
        return len(self._questions) > 1  # accounting for the previous message that has not been popped yet

    def ask_again(self) -> Union[str, None]:
        """
        Ask the same question again.
        :return: Question prompt
        """
        question = self._current_question
        if question is None:  # no questions at all
            return None
        return self._current_question.prompt

    def ask_next_question(self) -> Union[str, None]:
        """
        Ask the next question.
        :return: Question prompt
        """
        if len(self._questions) == 0:  # no questions at all
            return None

        if not self._current_question.is_complete:
            raise Exception("Current question is incomplete.")  # current question is not complete

        self._questions.pop(0)  # remove the previous question from the list

        return self.ask_again()

    def answer(self, answer_string: str) -> ProcessedAnswer:
        """
        Answer the current question.
        :param answer_string: Answer string
        :return: True if the answer was valid, False otherwise
        """
        return self._process_answer(answer_string)

    def _process_answer(self, answer_string: str) -> ProcessedAnswer:
        """
        Process the answer to the current question.
        :param answer_string: Answer string
        :return: True if the answer was valid, False otherwise
        """
        question = self._current_question
        if question is None:  # no questions at all (how did we get here?)
            return ProcessedAnswer(valid=False, error_message="No questions in queue")

        if answer_string is None:
            return ProcessedAnswer(valid=False, error_message="No answer provided")

        if isinstance(question, MultipleChoiceQuestion):
            if not _process_multiple_choice_answer(question=question, answer_string=answer_string):
                return ProcessedAnswer(
                    valid=False,
                    error_message=f"One or more of the choices you selected were invalid. Please try again.")
            self._store_answered_question(question=question)
            return ProcessedAnswer(valid=True)
        elif isinstance(question, YesNoQuestion):
            if not _process_yes_or_no_answer(question=question, answer_string=answer_string):
                return ProcessedAnswer(
                    valid=False,
                    error_message=f"Your answer was not a valid yes/no answer. Please try again.")
            self._store_answered_question(question=question)
            return ProcessedAnswer(valid=True)
        elif isinstance(question, Question):
            if not _process_regular_answer(question=question, answer_string=answer_string):
                # a regular question will never fail to add an answer, so this should never happen
                return ProcessedAnswer(
                    valid=False,
                    error_message=f"Your answer was invalid. Please try again.")
            self._store_answered_question(question=question)
            return ProcessedAnswer(valid=True)
        else:
            raise ValueError(f"Question type {type(question)} not supported.")

    def _store_answered_question(self, question: Question) -> None:
        """
        Store the question and answer in the answered questions list.
        :param question: Question
        """
        # question only gets added to the map once it has been answered
        self._current_question_number += 1
        self._qa_map[self._current_question_number] = question

    def ask_confirmation(self) -> Union[str, None]:
        """
        Ask the user to confirm their answers for the current question.
        :return: Confirmation prompt
        """
        question_just_answered = self._previous_answered_question
        if question_just_answered is None:  # question not on map since not answered yet
            return None

        return question_just_answered.confirmation_prompt

    def answer_confirmation(self, answer_string: str) -> ProcessedAnswer:
        """
        Process the answer to the confirmation prompt.
        :param answer_string: Answer string
        :return: True if the answer was valid, False otherwise
        """
        confirmation_question = YesNoQuestion(prompt="INTERNAL: Confirmation question")
        if not _process_yes_or_no_answer(question=confirmation_question, answer_string=answer_string):
            return ProcessedAnswer(
                valid=False,
                error_message=f"Your answer was not a valid yes/no answer. Please try again.")

        confirmation_answer: Optional[YesNoAnswer] = confirmation_question.answer
        if confirmation_answer is None:
            return ProcessedAnswer(
                valid=False,
                error_message=f"Your answer was invalid. Please try again.")

        if confirmation_answer.enum == YesNo.NO:
            # reset the answer, remove the question from the map and put it back on the stack
            previous_question = self._previous_answered_question
            previous_question.reset_answer()
            del self._qa_map[self._current_question_number]
            self._questions.insert(0, previous_question)
            self._current_question_number -= 1

        return ProcessedAnswer(valid=True)

    def get_question_and_answer(self, question_number: int) \
            -> Union[Question, MultipleChoiceQuestion, YesNoQuestion, None]:
        if question_number not in self._qa_map.keys():
            return None
        return self._qa_map[question_number]
