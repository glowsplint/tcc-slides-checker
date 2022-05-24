import os
import re
from functools import cached_property
from pathlib import Path
from typing import Iterable, TypedDict

if __name__ == "__main__":
    if Path(os.getcwd()).name == "processing":
        os.chdir("../..")

from backend.processing.checker import Checker
from pptx import Presentation
from pptx.slide import Slide


class Result(TypedDict):
    title: str
    expected: str  # actionable statement
    provided: str  # observed from slides
    result: bool


SlideSubset = dict[int, Slide]


class ContentChecker(Checker):
    """
    Checks the content of the uploaded slides according to the inputs.
    """

    def __init__(
        self, selected_date, req_order_of_service, sermon_discussion_qns, presentations
    ) -> None:
        self.selected_date = selected_date
        self.req_order_of_service = req_order_of_service
        self.sermon_discussion_qns = sermon_discussion_qns
        self.presentations = presentations

    @cached_property
    def pptx(self):
        # TODO: extend to multiple presentations
        return self.presentations[0]

    def run(self) -> list[Result]:
        """
        Runs all the checks within the ContentChecker.

        Returns:
            list[dict[str,str]]: List of dictionaries containing 'title' and 'description' keys
        """
        result = [
            self.check_existence_of_section_headers(
                section_headers=section_headers(self.pptx.slides)
            )
        ]
        return result

    def check_existence_of_section_headers(
        self, section_headers: SlideSubset
    ) -> Result:
        return {
            "title": "Check existence of section headers",
            "expected": "There should be more than 1 section header slide.",
            "provided": f"{len(section_headers)} section header slides found.",
            "result": len(section_headers) > 0,
        }


def get_slide_subset_with_text(all_slides: Iterable[Slide], text: str) -> SlideSubset:
    """
    Returns a subset of all slides which contain the provided text argument on the slide

    Args:
        all_slides (Iterable[Slide]): An iterable containing all slides
        text (str): String to match

    Returns:
        SlideSubset: Subset of slides with slide number (1-indexed) as keys
    """
    subset = dict()
    for i, slide in enumerate(all_slides):
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            if text in shape.text_frame.text:
                subset[i] = slide
    return subset


def section_headers(all_slides: Iterable[Slide]) -> SlideSubset:
    """
    Section header slides are slides that contain the text "Today's order of service".
    This includes the Welcome slide, and all other item slides (i.e. Family Confession,
    Family Prayer etc.)

    Args:
        all_slides (Iterable[Slide]): An iterable containing all slides

    Returns:
        list[Slide]: List of slides matching the subset
    """
    return get_slide_subset_with_text(all_slides, text="order of service")


def get_raw_text_from_slides(slides: SlideSubset) -> list[str]:
    """
    Returns the raw text from any shapes (including text boxes) in the provided slides.

    Args:
        slides (list[Slide]): List of slides

    Returns:
        list[str]: List of strings in these slides
    """
    return [
        shape.text_frame.text for slide in slides.values() for shape in slide.shapes
    ]


def slide_order_of_service(section_headers: SlideSubset) -> list[list[str]]:
    def filter_order_of_service_only(text: list[str]) -> list[str]:
        return [item for item in text if "order of service" in item]

    def split_and_strip(text: str) -> list[str]:
        """
        Splits up raw text on newline characters and strips on both sides of the
        resulting string.

        Args:
            text (str): _description_

        Returns:
            list[str]: _description_
        """
        split_text = re.split("\n+", text)
        return [
            item.strip()
            for item in split_text
            if len(item) and "order of service" not in item
        ]

    section_header_text = get_raw_text_from_slides(section_headers)
    orders_of_service = filter_order_of_service_only(section_header_text)
    return [split_and_strip(item) for item in orders_of_service]


def check_section_headers_have_correct_order(
    req_order_of_service: list[tuple[str, str]],
    slide_order_of_service: list[list[str]],
):
    """
    Test all section headers have the correct order of service by checking that the
    order of service provided in each section header slide matches the provided order
    of service.

    Section headers are the slides that separate each section of the service.
    These slides will usually have the order of service in grey on the right side.

    Args:
        req_order_of_service (tuple[str, str]): Required order of service
        slide_order_of_service (list[tuple[str, str]]): Order of services from slides
    """
    # 1. Identify the section header slides
    # 2. Check that there is a text box on the page that contains the order of service
    # 3. Check that the order of service is correct
    # TODO: Tell me which slide number and how it is incorrect
    # TODO: add slide numbers to the order of service
    result = []
    matched_text = "(Opening Song|Closing Song|Hearing God(\u2018|')s Word Read)"
    for slide_text in slide_order_of_service:
        index = 0
        for entry in slide_text:
            if re.match(matched_text, entry) is not None:
                title, comments = req_order_of_service[index]
                is_commented_items_correct = f"{title} \u2013 {comments}" == entry
                assert is_commented_items_correct
                if is_commented_items_correct:
                    index += 1
                    continue
                # result.append(
                #     {
                #         "title": "Check section headers have correct order",
                #         "expected": "",
                #         "provided": f"{len(section_headers)} section header slides found.",
                #         "result": len(section_headers) > 0,
                #     }
                # )
            elif entry != req_order_of_service[index][0]:
                continue
            index += 1
        assert index == len(
            req_order_of_service
        ), "The order of service in the slides do not contain the entire required order of service!"
        # return {
        #     "title": "Check existence of section headers",
        #     "expected": "There should be more than 1 section header slide.",
        #     "provided": f"{len(section_headers)} section header slides found.",
        #     "result": len(section_headers) > 0,
        # }


def check_family_confession_content_matches_number(
    req_order_of_service: tuple[str, str]
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
    req_order_of_service: tuple[str, str],
):
    """
    Test that family declaration (if present) has the correct contents by checking that
    the words on the slide match the required content (usually a #number) specified in
    the order of service.

    Family Declaration is an optional item in the order of service.
    """
    pass


def check_all_lyric_slides_have_no_title(req_order_of_service: tuple[str, str]):
    """
    Test all lyric slides do not contain a title.

    Lyric slides are slides for the opening and closing song.
    """
    # 1. Identify the lyric slides for the opening and closing song
    # 2. Check that the title is not present (i.e. none of the text boxes contain the song title exclusively)
    pass


section_mapping = {
    "Bible Reading": "Hearing God\u2018s Word Read",
    "Sermon": "Hearing God\u2018s Word Proclaimed",
    "Discuss in groups": "Sermon Discussion",
}


def raw_req_order_of_service_no_declaration() -> str:
    return """Opening Words	1	
Opening Song	4	God Omniscient, God All Knowing
Family Confession	2	#11 Confession of Sin (Slide 17 & 18)
Family Prayer	4	Refer to Prayer Points Tab in this document (Usually updated by Thu)
Family Business	5	Refer to Family Business Tab
Bible Reading 	4	Daniel 2:1-24 & 31-47
Sermon	30	Preacher: Denesh
Closing Song	4	Crown Him with Many Crowns
Closing Words	1	
Discuss in groups	5	
Dismissal		"""


def get_clean_req_order_of_service(
    raw_req_order_of_service_no_declaration: str,
) -> list[tuple[str, int, str]]:
    """
    Returns the cleaned up required order of service.

    Args:
        raw_req_order_of_service_no_declaration (str): Raw required order of service

    Returns:
        list[tuple[str, int, str]]: _description_
    """
    result, intermediate = [], []
    for item in raw_req_order_of_service_no_declaration.split("\n"):
        intermediate.append(item.split("\t"))
    for item in intermediate:
        result.append(tuple([item[0].strip(), item[1].strip(), item[2].strip()]))
    return result


def filter_clean_req_order_of_service(
    clean_req_order_of_service: list[tuple[str, int, str]],
) -> list[tuple[str, str]]:
    """
    Returns the filtered clean required order of service with elements at position:
    1. Item
    2. Things to note

    Returns:
        tuple[str, str]

    Args:
        raw_req_order_of_service_no_declaration (str): Raw

    Returns:
        list[tuple[str, str]]: _description_
    """
    return [
        (section_mapping.get(item[0], item[0]), item[2])
        for item in clean_req_order_of_service
        if not re.match("(Opening Words|Dismissal|Closing Words)", item[0])
    ]


clean_req_order_of_service = filter_clean_req_order_of_service(
    get_clean_req_order_of_service(raw_req_order_of_service_no_declaration())
)

if __name__ == "__main__":

    with open("input/01.05 (9am) service slides.pptx", "rb") as f:
        pptx = Presentation(f)

    cc = ContentChecker(
        selected_date="08 May 2022",
        req_order_of_service="",
        sermon_discussion_qns="",
        presentations=[pptx],
    )

    check_section_headers_have_correct_order(
        clean_req_order_of_service,
        slide_order_of_service(section_headers(pptx.slides)),
    )
