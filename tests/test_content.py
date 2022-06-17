import pytest
from backend.processing.checker.content import (
    ContentChecker,
    SlideOrderOfService,
    SlideSubset,
)
from backend.processing.result import Status
from pptx import Presentation as PresentationConstructor
from pptx.slide import Slide


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
def filename() -> str:
    return "22.05 (10.30am) service slides.pptx"


@pytest.fixture
def cc(
    order_of_service_without_declaration: str, sermon_discussion_qns: str, filename: str
) -> ContentChecker:
    with open(f"input/{filename}", "rb") as f:
        pptx = PresentationConstructor(f)

    return ContentChecker(
        selected_date="22 May 2022",
        req_order_of_service=order_of_service_without_declaration,
        sermon_discussion_qns=sermon_discussion_qns,
        presentations={filename: pptx},
    )


@pytest.fixture
def slides(cc: ContentChecker, filename: str) -> list[Slide]:
    return [slide for slide in cc.presentations[filename].slides]  # type: ignore


@pytest.fixture
def section_headers(cc: ContentChecker, slides: list[Slide]) -> SlideSubset:
    return cc.section_headers(slides)


@pytest.fixture
def sermon_discussion_slides(cc: ContentChecker, slides: list[Slide]) -> SlideSubset:
    return cc.sermon_discussion_slides(slides)


@pytest.fixture
def slide_order_of_service(cc: ContentChecker, section_headers: SlideSubset):
    return cc.slide_order_of_service(section_headers)


def test_check_existence_of_section_headers(
    cc: ContentChecker, section_headers: SlideSubset
):
    actual = cc.check_existence_of_section_headers(section_headers)
    expected = {
        "title": "Check existence of section header slides",
        "status": Status.PASS,
        "comments": f"Expected: >=1 section header slides. Provided: 11 section header slide(s) found.",
    }
    assert expected == actual


def test_check_section_headers_have_correct_order(
    cc: ContentChecker, slide_order_of_service: SlideOrderOfService
):
    actual = cc.check_section_headers_have_correct_order(slide_order_of_service)
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


def test_check_family_declaration_content_matches_number():
    pass


def test_check_all_lyric_slides_have_no_title():
    pass


def test_check_all_dates_are_as_provided(cc: ContentChecker, slides: list[Slide]):
    actual = cc.check_all_dates_are_as_provided(date=cc.selected_date, slides=slides)
    expected = [
        {
            "title": "Check all dates that appear in the slides are the same as the date of Sunday service.",
            "status": Status.PASS,
            "comments": "All slides containing dates display the required date of Sunday service.",
        }
    ]
    assert expected == actual


def test_check_existence_of_lone_sermon_discussion_slide(
    cc: ContentChecker, sermon_discussion_slides: SlideSubset
):
    actual = cc.check_existence_of_lone_sermon_discussion_slide(
        sermon_discussion_slides
    )
    expected = {
        "title": "Check existence of sermon discussion slides.",
        "status": Status.PASS,
        "comments": "Expected: 1 sermon discussion slide. Provided: 1 sermon discussion slide(s) found.",
    }
    assert expected == actual


def test_check_sermon_discussion_qns_are_as_provided(
    cc: ContentChecker, sermon_discussion_slides: SlideSubset
):
    actual = cc.check_sermon_discussion_qns_are_as_provided(sermon_discussion_slides)
    expected = [
        {
            "title": "Check sermon discussion questions are as provided.",
            "status": Status.PASS,
            "comments": "All sermon discussion questions are present.",
        }
    ]
    assert expected == actual
