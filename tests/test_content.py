import re
from pathlib import Path

import pytest
from pptx import Presentation
from pptx.slide import Slide


@pytest.fixture
def order_of_service_with_declaration():
    pass


# @pytest.fixture
def order_of_service_without_declaration() -> list[tuple[str, int, str]]:
    """
    Order of service with elements at position:
    1. Item
    2. Minutes
    3. Things to note

    Returns:
        tuple[str, int, str]
    """
    return [
        ("Opening Words", 1, ""),
        ("Opening Song", 4, "God Omniscient, God All Knowing"),
        ("Family Confession", 2, "#11 Confession of Sin (Slide 17 & 18)"),
        (
            "Family Prayer",
            4,
            "Refer to Prayer Points Tab in this document (Usually updated by Thu)",
        ),
        ("Family Business", 5, "Refer to Family Business Tab"),
        ("Bible Reading", 4, "Daniel 2:1-24 & 31-47"),
        ("Sermon", 30, "Preacher: Denesh"),
        ("Closing Song", 4, "Crown Him with Many Crowns"),
        ("Closing Words", 1, ""),
        ("Discuss in groups", 5, ""),
        ("Dismissal", 0, ""),
    ]


# @pytest.fixture
def clean_order_of_service_without_declaration() -> list[tuple[str, str]]:
    """
    Order of service with elements at position:
    1. Item
    2. Things to note

    Returns:
        tuple[str, str]
    """
    return [
        (section_mapping().get(item[0], item[0]), item[2])
        for item in order_of_service_without_declaration()
        if not ("Opening Words" in item[0] or "Dismissal" in item[0])
    ]


# @pytest.fixture
def section_mapping() -> dict[str, str]:
    return {
        "Bible Reading": "Hearing God\u2018s Word Read",
        "Sermon": "Hearing God\u2018s Word Proclaimed",
        "Discuss in groups": "Sermon Discussion",
    }


@pytest.fixture
def sermon_discussion_qns():
    return


# @pytest.fixture
def all_slides() -> list[Slide]:
    return get_all_slides(pptx=pptx())


def pptx() -> Presentation:
    PATH_TO_PRESENTATION = Path("../input/01.05 (9am) service slides.pptx")
    # PATH_TO_PRESENTATION = Path("input/01.05 (9am) service slides.pptx")
    return Presentation(PATH_TO_PRESENTATION)


def get_all_slides(pptx: Presentation) -> list[Slide]:
    return [slide for slide in pptx.slides]


def get_slide_subset_with_text(all_slides: list[Slide], text: str) -> list[Slide]:
    """
    Returns a subset of all slides which contain the provided text argument on the slide

    Args:
        all_slides (list[Slide]): _description_
        text (str): _description_

    Returns:
        list[Slide]: _description_
    """
    section_headers = []
    for slide in all_slides:
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            if text in shape.text_frame.text:
                section_headers.append(slide)
    return section_headers


# @pytest.fixture
def section_headers(all_slides: list[Slide]) -> list[Slide]:
    """
    Section header slides are slides that contain the text "Today's order of service".
    This includes the Welcome slide, and all other item slides (i.e. Family Confession,
    Family Prayer etc.)

    Args:
        all_slides (list[Slide]): A list of all slides

    Returns:
        list[Slide]: List of slides
    """
    return get_slide_subset_with_text(all_slides, text="order of service")


def get_text_from_slides(slides: list[Slide]) -> list[str]:
    return [shape.text_frame.text for slide in slides for shape in slide.shapes]


def test_existence_of_section_headers(section_headers: list[Slide]):
    assert len(section_headers) > 0


def split_and_strip(text: str) -> list[str]:
    split_text = re.split("\n+", text)
    return [
        item.strip()
        for item in split_text
        if len(item) and "order of service" not in item
    ]


def get_order_of_service_in_slide(text: str) -> list[tuple[str, str]]:
    return [item for item in text if "order of service" in item]


def get_reformatted_text(text: str) -> list[tuple[str, str]]:
    return [split_and_strip(item) for item in text]


def get_final():
    section_header_slides = section_headers(all_slides())
    section_header_text = get_text_from_slides(section_header_slides)
    orders_of_service = get_order_of_service_in_slide(section_header_text)
    return [split_and_strip(item) for item in orders_of_service]


def test_section_headers_have_correct_order(
    order_of_service_without_declaration: tuple[str, int, str],
    section_headers: list[Slide],
):
    """
    Test all section headers have the correct order of service by checking that the
    order of service provided in each section header slide matches the provided order
    of service.

    Section headers are the slides that separate each section of the service.
    These slides will usually have the order of service in grey on the right side.
    """
    # 1. Identify the section header slides
    # 2. Check that there is a text box on the page that contains the order of service
    # 3. Check that the order of service is correct
    pass


def test_family_confession_content_matches_number(
    order_of_service_without_declaration: tuple[str, int, str]
):
    """
    Test family confession has the correct contents by checking that the words on the
    slide match the required content (usually a #number) specified in the order of
    service.

    Family Confession is an item in the order of service.
    """
    # 1. Identify the family confession slides
    # 2. Check that there is a text box on the page that contains the family confession
    # 3. Check that it matches the number
    pass


def test_family_declaration_content_matches_number(
    order_of_service_without_declaration: tuple[str, int, str],
):
    """
    Test that family declaration (if present) has the correct contents by checking that
    the words on the slide match the required content (usually a #number) specified in
    the order of service.

    Family Declaration is an optional item in the order of service.
    """
    pass


def test_all_lyric_slides_have_no_title(
    order_of_service_without_declaration: tuple[str, int, str]
):
    """
    Test all lyric slides do not contain a title.
    """
    # 1. Identify the lyric slides
    # 2.
    pass
