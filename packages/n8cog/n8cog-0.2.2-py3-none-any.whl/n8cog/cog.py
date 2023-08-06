import asyncio
import logging
from typing import Optional, List, Union

from discord import Member
from redbot.core.commands import Cog, Context

from questionflow import QuestionFlow, Question, Answer, MultipleChoiceQuestion, Choice, YesNoQuestion, YesNoAnswer, \
    YesNo

from n8cog.dm_configuration import DMConfiguration


class BaseCog(Cog):
    """
    Base cog for all other cogs to inherit from.
    """
    __author__ = "nwithan8"

    def __init__(self, name: str, bot):
        super().__init__()
        self.bot = bot

        log = logging.getLogger(f"red.cog.{name}")

    async def send_error(self, ctx: Context, error_message: Optional[str] = None):
        await ctx.send(error_message or "Something went wrong!")

    async def _send_and_get_dm_response(self, user: Member, message: str, timeout: int = 60) -> Union[str, None]:
        await user.dm_channel.send(message)
        try:
            response = await self.bot.wait_for(
                'message',
                check=lambda x: x.channel == user.dm_channel and x.author == user,
                timeout=timeout)
            return response.content
        except asyncio.TimeoutError:
            return None

    async def run_dm_questionnaire(self, user: Member,
                                   questions: List[Union[Question, MultipleChoiceQuestion, YesNoQuestion]],
                                   consent_message: str = None,
                                   end_message: str = "Thank you. This questionnaire is complete.") \
            -> Union[List[Union[Question, MultipleChoiceQuestion, YesNoQuestion]], None]:
        """
        Run a questionnaire in a Direct Message with a Member.

        :param user: The member to run the questionnaire for.
        :param questions: The questions to ask.
        :param consent_message: The consent message user should agree to before the questionnaire (optional).
        :param end_message: The message to send when the questionnaire is complete.
        :return: The answered questions or None if the user cancelled the questionnaire.
        """
        dm_channel = None
        try:
            dm_channel = user.dm_channel
        except AttributeError:
            dm_channel = await self.bot.create_dm(user)
        if dm_channel is None:
            dm_channel = await self.bot.create_dm(user)

        if dm_channel is None:
            raise Exception("Could not create DM channel.")

        if consent_message is not None:
            consent_flow = QuestionFlow(
                questions=[YesNoQuestion(prompt=f"{consent_message}\n\nAnswer 'y' to continue.")])
            consent_prompt = consent_flow.ask_next_question()

            consent_response = await self._send_and_get_dm_response(user=user, message=consent_prompt)
            if consent_response is None:
                consent_response = "n"
            consent_flow.answer(answer_string=consent_response)

            consent_question: YesNoQuestion = consent_flow.get_question_and_answer(question_number=1)
            consent_answer: YesNoAnswer = consent_question.answer
            if consent_answer.enum == YesNo.NO:
                await dm_channel.send("You did not agree. This questionnaire has been cancelled.")
                return None

        flow = QuestionFlow(questions=questions)
        while flow.has_more_questions:
            prompt = flow.ask_next_question()
            answer = await self._send_and_get_dm_response(user=user, message=prompt)
            if answer is None:
                await dm_channel.send("You did not answer in time. This questionnaire has been cancelled.")
                return None
            if not flow.answer(answer_string=answer):
                await dm_channel.send("You answered incorrectly. This questionnaire has been cancelled.")
                return None

        if end_message is not None:
            await dm_channel.send(end_message)

        answered_questions = []
        for question_number, _ in enumerate(questions):
            question: Question = flow.get_question_and_answer(question_number=question_number)
            answered_questions.append(question)
        return answered_questions

    async def run_dm_configuration(self, user: Member,
                                   configuration: DMConfiguration) \
            -> Union[dict, None]:
        """
        Run a configuration questionnaire in a Direct Message with a Member.

        :param user: The member to run the questionnaire for.
        :param configuration: The configuration to ask.
        :return: The compiled configuration or None if the user cancelled the questionnaire.
        """
        questions = configuration.questions
        consent_message = configuration.pre_message
        end_message = configuration.post_message
        answered_questions = await self.run_dm_questionnaire(user=user, questions=questions,
                                                             consent_message=consent_message,
                                                             end_message=end_message)
        if answered_questions is None:
            return None

        return configuration.process_answers(questions=answered_questions)
