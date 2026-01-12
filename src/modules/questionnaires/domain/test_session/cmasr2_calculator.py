from sqlalchemy import false

from src.modules.questionnaires.domain.test_session.answers_set import AnswerSet
from src.modules.questionnaires.domain.test_session.test_results import TestResults


def calculate_cmasr2_test_results(answer_set: AnswerSet) -> TestResults:
    if answer_set is None:
        return TestResults(0, 0, 0, 0, 0, 0)
    else:
        # CMASR-2 test results calculation
        #     social_anxiety_index: int
        _social_anxiety_index = 0
        _physiological_anxiety_index = 0
        _defensiveness_index = 0
        _worry_index = 0
        _total_anxiety_index = 0
        _inconsistent_answers_index = 0

        _physiological_index_questions = [1, 5, 7, 8, 11, 13, 15, 16, 18, 25, 27, 28, 31, 34, 36, 39, 42, 43, 47]
        _defensiveness_index_questions = [14, 19, 24, 29, 33, 38, 40, 44, 48]
        _social_index_questions = [3, 4, 6, 9, 10, 17, 22, 23, 26, 32, 37, 41, 45, 49]
        _worry_index_questions = [2, 12, 20, 21, 30, 35, 40, 44, 46, 48]

        for answer in answer_set.answer_list:
            # physiological_anxiety_index: int
            if answer.question_id.value in _physiological_index_questions:
                if answer.value:
                    _physiological_anxiety_index += 1

            # defensiveness_index: int
            if answer.question_id.value in _defensiveness_index_questions:
                if answer.value and answer.question_id.value not in [40, 44, 48]:
                    _defensiveness_index += 1

                if (answer.question_id.value in [40, 44, 48]) and (answer.value is False):
                    _defensiveness_index += 1

            # social_anxiety_index: int
            if answer.question_id.value in _social_index_questions:
                if answer.value:
                    _social_anxiety_index += 1

            # worry_index: int
            if answer.question_id.value in _worry_index_questions:
                if answer.value:
                    _worry_index += 1

        #     total_anxiety_index: int
        _total_anxiety_index = _social_anxiety_index + _physiological_anxiety_index + _worry_index

        #     inconsistent_answers_index: int
        if answer_set.answer_list[1].value != answer_set.answer_list[7].value:
            _inconsistent_answers_index += 1

        if answer_set.answer_list[2].value != answer_set.answer_list[34].value:
            _inconsistent_answers_index += 1

        if answer_set.answer_list[3].value != answer_set.answer_list[9].value:
            _inconsistent_answers_index += 1

        if answer_set.answer_list[5].value != answer_set.answer_list[48].value:
            _inconsistent_answers_index += 1

        if answer_set.answer_list[6].value != answer_set.answer_list[38].value:
            _inconsistent_answers_index += 1

        if answer_set.answer_list[18].value != answer_set.answer_list[32].value:
            _inconsistent_answers_index += 1

        if answer_set.answer_list[22].value != answer_set.answer_list[36].value:
            _inconsistent_answers_index += 1

        if answer_set.answer_list[23].value != answer_set.answer_list[28].value:
            _inconsistent_answers_index += 1

        if answer_set.answer_list[37].value == answer_set.answer_list[47].value:
            _inconsistent_answers_index += 1

        return TestResults(
            social_anxiety_index=_social_anxiety_index,
            physiological_anxiety_index=_physiological_anxiety_index,
            defensiveness_index=_defensiveness_index,
            worry_index=_worry_index,
            total_anxiety_index=_total_anxiety_index,
            inconsistent_answers_index=_inconsistent_answers_index)
