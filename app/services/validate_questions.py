from ..mongo.questions_crud import get_question_group
from ..schemas.questions import (
    FullQuestionGroup,
    AnswerResul,
    QuestionResult,
    QuestionGroupResult,
    ValidateQuestionGroup,
)


class ValidateException(Exception):
    pass


async def validate_questions(
    user_answers: ValidateQuestionGroup,
) -> QuestionGroupResult:
    total_questions = len(user_answers.questions)
    user_score = 0

    valid_answers: FullQuestionGroup = await get_question_group(user_answers.id)

    if total_questions != len(valid_answers.questions):
        raise ValidateException(
            f"Вы ответили не на все вопросы ({total_questions} из {len(valid_answers.questions)})"
        )

    questions_group_status = []

    for i in range(total_questions):
        question_is_valid = True
        answers_status = []

        # Создаем словарь с вариантами ответа и отметкой пользователя.
        user_question_answers = {}
        for user_answer in user_answers.questions[i].answers:
            user_question_answers[user_answer.text] = user_answer.is_valid

        if len(user_question_answers) != len(valid_answers.questions[i].answers):
            raise ValidateException(
                f"Количество ответов ({len(user_question_answers)}) для задания"
                f' "{valid_answers.questions[i].text}" не соответствуют оригиналу'
                f" ({len(valid_answers.questions[i].answers)})"
            )

        # Проверяем действительные варианты ответа и те, что указал пользователь.
        for valid_answer in valid_answers.questions[i].answers:
            user_answer_is_valid = user_question_answers.get(valid_answer.text)
            if user_answer_is_valid is None:
                raise ValidateException(
                    f'У задания "{valid_answers.questions[i].text}" нет варианта ответа "{valid_answer.text}"'
                )

            # Если вариант ответа пользователя верный.
            question_is_valid = (
                question_is_valid and valid_answer.is_valid is user_answer_is_valid
            )

            # Отмечаем статус варианта ответа.
            answers_status.append(
                AnswerResul(
                    text=valid_answer.text,
                    is_valid=user_answer_is_valid,
                    true_valid=valid_answer.is_valid,
                )
            )

        # Если все варианты ответа были отмечены верно.
        if question_is_valid:
            user_score += 1

        # Добавляем статус проверки текущего вопроса.
        questions_group_status.append(
            QuestionResult(
                text=valid_answers.questions[i].text,
                image=valid_answers.questions[i].image,
                answers=answers_status,
                explanation=valid_answers.questions[i].explanation,
            )
        )

    return QuestionGroupResult(
        _id=valid_answers.id,
        name=valid_answers.name,
        tags=valid_answers.tags,
        created_at=valid_answers.created_at,
        updated_at=valid_answers.updated_at,
        timeout_minutes=valid_answers.timeout_minutes,
        completion_time_minutes=valid_answers.completion_time_minutes,
        questions=questions_group_status,
        total_score=total_questions,
        user_score=user_score,
    )
