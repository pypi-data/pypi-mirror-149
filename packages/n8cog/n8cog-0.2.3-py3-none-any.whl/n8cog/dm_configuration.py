from enum import Enum
from typing import List

from questionflow import QuestionFlow, Question, Answer, MultipleChoiceQuestion, MultipleAnswerQuestion, Choice, \
    YesNoQuestion, YesNoAnswer, YesNo


class DMConfigurationEntryType(Enum):
    REGULAR = 1
    MULTIPLE_CHOICE = 2
    MULTIPLE_ANSWER = 3
    TRUE_FALSE = 4


class DMConfigurationEntry:
    def __init__(self, name: str, entry_type: DMConfigurationEntryType, choices: List[Choice] = None):
        self.name = name
        self.type = entry_type
        self.choices = choices


class DMConfiguration:
    def __init__(self, entries: List[DMConfigurationEntry], pre_message: str = None, post_message: str = None):
        self.entries = entries
        self.pre_message = pre_message
        self.post_message = post_message

    @property
    def questions(self) -> List[Question]:
        questions = []
        for entry in self.entries:
            if entry.type == DMConfigurationEntryType.REGULAR:
                questions.append(Question(prompt=entry.name))
            elif entry.type == DMConfigurationEntryType.MULTIPLE_CHOICE:
                questions.append(MultipleChoiceQuestion(prompt=entry.name, choices=entry.choices))
            elif entry.type == DMConfigurationEntryType.MULTIPLE_ANSWER:
                questions.append(MultipleAnswerQuestion(prompt=entry.name))
            elif entry.type == DMConfigurationEntryType.TRUE_FALSE:
                questions.append(YesNoQuestion(prompt=entry.name))
        return questions

    def process_answers(self, questions: List[Question]) -> dict:
        configuration = {}
        for question in questions:
            if isinstance(question, MultipleChoiceQuestion):
                configuration[question.prompt] = [choice.internal_value for choice in question.answer]
            elif isinstance(question, MultipleAnswerQuestion):
                configuration[question.prompt] = [answer.value for answer in question.answer]
            elif isinstance(question, YesNoQuestion):
                configuration[question.prompt] = True if question.answer.enum == YesNo.YES else False
            else:
                configuration[question.prompt] = question.answer.value
        return configuration
