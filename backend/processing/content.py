import os
import re
from pathlib import Path

if __name__ == "__main__":
    if Path(os.getcwd()).name == "processing":
        os.chdir("../..")

from backend.processing.checker import Checker
from fastapi import UploadFile
from pptx import Presentation
from pptx.slide import Slide


class ContentChecker(Checker):
    """
    Checks the content of the uploaded slides according to the inputs.
    """
    def __init__(
        self, selected_date, req_order_of_service, sermon_discussion_qns, files
    ) -> None:
        self.selected_date = selected_date
        self.req_order_of_service = req_order_of_service
        self.sermon_discussion_qns = sermon_discussion_qns
        self.files = files

    def run(self):
        pass

    def check_existence_of_section_headers(self, section_headers: list[Slide]):
        assert len(section_headers) > 0


def all_slides() -> list[Slide]:
    return get_all_slides(pptx=pptx())


def pptx(path: os.PathLike) -> Presentation:
    return Presentation(path)


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
    subset = []
    for slide in all_slides:
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            if text in shape.text_frame.text:
                subset.append(slide)
    return subset


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


def split_and_strip(text: str) -> list[str]:
    split_text = re.split("\n+", text)
    return [
        item.strip()
        for item in split_text
        if len(item) and "order of service" not in item
    ]


def order_of_service_in_slide(text: str) -> list[tuple[str, str]]:
    return [item for item in text if "order of service" in item]


def get_reformatted_text(text: str) -> list[tuple[str, str]]:
    return [split_and_strip(item) for item in text]


def clean_order_of_service_in_slides(section_headers: list[Slide]):
    section_header_text = get_text_from_slides(section_headers)
    orders_of_service = order_of_service_in_slide(section_header_text)
    return [split_and_strip(item) for item in orders_of_service]


def check_section_headers_have_correct_order(
    clean_order_of_service_without_declaration: tuple[str, str],
    clean_order_of_service_in_slides: list[tuple[str, str]],
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
    # TODO: Tell me which slide number and how it is incorrect
    # TODO: Add front-end and back-end and migrate from pytest to functions
    for slide in clean_order_of_service_in_slides:
        index = 0
        for entry in slide:
            if (
                re.match(
                    "(Opening Song|Closing Song|Hearing God\u2018s Word Read)", entry
                )
                is not None
            ):
                title, comments = clean_order_of_service_without_declaration[index]
                assert f"{title} \u2013 {comments}" == entry
            elif entry != clean_order_of_service_without_declaration[index][0]:
                continue
            index += 1
        assert index == len(
            clean_order_of_service_without_declaration
        ), "The order of service in the slides do not contain the entire required order of service!"


def check_family_confession_content_matches_number(
    clean_order_of_service_without_declaration: tuple[str, str]
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


def check_family_declaration_content_matches_number(
    clean_order_of_service_without_declaration: tuple[str, str],
):
    """
    Test that family declaration (if present) has the correct contents by checking that
    the words on the slide match the required content (usually a #number) specified in
    the order of service.

    Family Declaration is an optional item in the order of service.
    """
    pass


def check_all_lyric_slides_have_no_title(
    clean_order_of_service_without_declaration: tuple[str, str]
):
    """
    Test all lyric slides do not contain a title.

    Lyric slides are slides for the opening and closing song.
    """
    # 1. Identify the lyric slides for the opening and closing song
    # 2. Check that the title is not present (i.e. none of the text boxes contain the song title exclusively)
    pass


if __name__ == "__main__":
    cc = ContentChecker(
        selected_date="08 May 2022",
        req_order_of_service="",
        sermon_discussion_qns="",
        files=[],
    )
    uf = UploadFile("input/01.05 (9am) service slides.pptx")
