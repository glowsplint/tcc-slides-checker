import pytest


@pytest.fixture
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
