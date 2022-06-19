"""
Tests are written to minimise the number of slides. This means that to test a given scenario,
we change the input to the tests rather than changing the slides.
"""

import pytest
from backend.processing.checker.content import ContentChecker
from backend.processing.result import Status
from pptx import Presentation as PresentationConstructor


def cc_factory(
    order_of_service_without_declaration: str,
    sermon_discussion_qns: str,
    file_path: str,
) -> ContentChecker:
    with open(f"input/{file_path}", "rb") as f:
        pptx = PresentationConstructor(f)

    return ContentChecker(
        selected_date="22 May 2022",
        req_order_of_service=order_of_service_without_declaration,
        sermon_discussion_qns=sermon_discussion_qns,
        file_path=file_path,
        presentation=pptx,
    )


@pytest.fixture
def order_of_service_without_declaration() -> str:
    return """Opening Words	1	
Opening Song	4	Behold Our God
Family Confession	2	#11 Confession of Sin (Slide 17 & 18)
Family Prayer	4	Refer to Prayer Points Tab in this document (Usually updated by Thu)
Family Business	5	Refer to Family Business Tab
Bible Reading 	4	Daniel 5
Sermon	30	Preacher: Denesh
Closing Song	4	Only a Holy God
Closing Words	1	
Discuss in groups	5	
Dismissal		"""


@pytest.fixture
def sermon_discussion_qns() -> str:
    return """1. How have you been confronted with your own arrogance before God today? How have you been challenged to repent?
2. How has our passage been a comfort if we are seeking to live for God in this anti-God world?"""


@pytest.fixture
def sermon_discussion_qns_with_typo() -> str:
    # 1. confrontedd, 2. comforting
    return """1. How have you been confrontedd with your own arrogance before God today? How have you been challenged to repent?
2. How has our passage been comforting if we are seeking to live for God in this anti-God world?"""


@pytest.fixture
def sermon_discussion_qns_with_wrong_qns() -> str:
    return """1. What was your view of God before hearing Daniel 2? How has God changed or expanded your view of him today?
2. How has today's passage helped you to be more confident about God's coming kingdom? What would that confidence look like in practice for you personally?"""


@pytest.fixture
def twenty_second_may() -> str:
    return "22.05 (10.30am) service slides.pptx"


@pytest.fixture
def twenty_second_may_cc(
    order_of_service_without_declaration: str,
    sermon_discussion_qns: str,
    twenty_second_may: str,
) -> ContentChecker:
    return cc_factory(
        order_of_service_without_declaration,
        sermon_discussion_qns,
        file_path=twenty_second_may,
    )


class TestSectionHeaders:
    def test_check_existence_of_section_headers(
        self, twenty_second_may_cc: ContentChecker
    ):
        actual = twenty_second_may_cc.check_existence_of_section_headers()
        expected = {
            "title": "Check existence of section header slides",
            "status": Status.PASS,
            "comments": f"Expected: >=1 section header slides. Provided: 11 section header slide(s) found.",
        }
        assert expected == actual

    def test_check_section_headers_have_correct_order(
        self, twenty_second_may_cc: ContentChecker
    ):
        actual = twenty_second_may_cc.check_section_headers_have_correct_order()
        expected = [
            {
                "title": "Check all required order of service items are present and in the correct order",
                "status": Status.PASS,
                "comments": "All slides containing order of service have the required order of service items and are presented in the correct order.",
            }
        ]
        assert expected == actual


def test_check_family_confession_content_matches_number():
    pass


def test_check_all_lyric_slides_have_no_title():
    pass


def test_check_all_dates_are_as_provided(twenty_second_may_cc: ContentChecker):
    actual = twenty_second_may_cc.check_all_dates_are_as_provided()
    expected = [
        {
            "title": "Check all dates that appear in the slides are the same as the date of Sunday service.",
            "status": Status.PASS,
            "comments": "All slides containing dates display the required date of Sunday service.",
        }
    ]
    assert expected == actual


def test_check_existence_of_lone_sermon_discussion_slide(
    twenty_second_may_cc: ContentChecker,
):
    actual = twenty_second_may_cc.check_existence_of_lone_sermon_discussion_slide()
    expected = {
        "title": "Check existence of sermon discussion slides.",
        "status": Status.PASS,
        "comments": "Expected: 1 sermon discussion slide. Provided: 1 sermon discussion slide(s) found.",
    }
    assert expected == actual


class TestSermonDiscussionQnsAreAsProvided:
    def test_happy_path(
        self,
        twenty_second_may_cc: ContentChecker,
    ):
        actual = twenty_second_may_cc.check_sermon_discussion_qns_are_as_provided()
        expected = [
            {
                "title": "Check sermon discussion questions are as provided.",
                "status": Status.PASS,
                "comments": "All sermon discussion questions are present.",
            }
        ]
        assert expected == actual

    def test_minor_typo(
        self, twenty_second_may_cc: ContentChecker, sermon_discussion_qns_with_typo: str
    ):
        # patching sermon discussion questions
        twenty_second_may_cc.sermon_discussion_qns = sermon_discussion_qns_with_typo
        actual = twenty_second_may_cc.check_sermon_discussion_qns_are_as_provided()
        expected = [
            {
                "title": "Check sermon discussion questions are as provided: Is there a typo?",
                "status": Status.WARNING,
                "comments": "On Slide 43, Expected: 'How have you been confrontedd with your own arrogance before God today? How have you been challenged to repent?'. Provided: 'How have you been confronted with your own arrogance before God today? How have you been challenged to repent?'. Similarity score = 99 of 100",
            },
            {
                "title": "Check sermon discussion questions are as provided: Is there a typo?",
                "status": Status.WARNING,
                "comments": "On Slide 43, Expected: 'How has our passage been comforting if we are seeking to live for God in this anti-God world?'. Provided: 'How has our passage been a comfort if we are seeking to live for God in this anti-God world?'. Similarity score = 97 of 100",
            },
        ]
        assert expected == actual

    def test_wrong_questions(
        self,
        twenty_second_may_cc: ContentChecker,
        sermon_discussion_qns_with_wrong_qns: str,
    ):
        # patching sermon discussion questions
        twenty_second_may_cc.sermon_discussion_qns = (
            sermon_discussion_qns_with_wrong_qns
        )
        actual = twenty_second_may_cc.check_sermon_discussion_qns_are_as_provided()
        expected = [
            {
                "title": "Check sermon discussion questions are as provided.",
                "status": Status.ERROR,
                'comments': "On Slide 43, Expected: 'What was your view of God before hearing Daniel 2? How has God changed or expanded your view of him today?'. Could not find this required question."
            },
            {
                "title": "Check sermon discussion questions are as provided.",
                "status": Status.ERROR,
                'comments': "On Slide 43, Expected: 'How has today's passage helped you to be more confident about God's coming kingdom? What would that confidence look like in practice for you personally?'. Could not find this required question."
            },
        ]
        assert expected == actual
