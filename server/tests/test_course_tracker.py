import sys
import os
from unittest.mock import MagicMock, patch
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.course_tracker_model import TrackedSections
from jobs.course_tracker import check_and_update_section, term_code

def test_term_code_logic():
    """test that helper function converts year/semester to term code correctly"""
    assert term_code(2026, "Spring") == "202601"
    assert term_code(2026, "Fall") == "202609"
    # winter logic: year - 1 (2026 winter -> 202512)
    assert term_code(2026, "Winter") == "202512"

@patch('jobs.course_tracker.requests.post')
def test_detects_open_class(mock_post):
    """test that a section updates to available when vt returns the crn"""
    mock_db = MagicMock()
    section = TrackedSections(
        subject_code="CS",
        course_number="1114",
        crn="12345",
        year=2026, 
        semester="Spring",
        is_available=False # currently unavailable
    )

    # simulate html response containing the crn
    mock_response = MagicMock()
    mock_response.text = "<html>Some content... <input name='CRN' value='12345' ...></html>"
    mock_post.return_value = mock_response

    is_open = check_and_update_section(mock_db, section)

    assert is_open
    assert section.is_available
    mock_db.commit.assert_called_once()

@patch('jobs.course_tracker.requests.post')
def test_detects_closed_class(mock_post):
    """test that a section updates to unavailable if vt doesn't return the crn"""
    mock_db = MagicMock()
    section = TrackedSections(
        subject_code="CS",
        course_number="1114",
        crn="12345",
        year=2026,
        semester="Spring",
        is_available=True # currently thinks it is available
    )

    # response does not contain crn, implying it's full
    mock_response = MagicMock()
    mock_response.text = "<html>Some content... Class is full ...</html>" 
    mock_post.return_value = mock_response

    is_open = check_and_update_section(mock_db, section)

    assert not is_open
    assert not section.is_available
    mock_db.commit.assert_called_once()

@patch('jobs.course_tracker.requests.post')
def test_handles_vt_error(mock_post):
    """test that we fail gracefully and don't update db on connection error"""
    mock_db = MagicMock()
    section = TrackedSections(
        year=2026,
        semester="Spring",
        is_available=False
    )

    mock_post.side_effect = Exception("VT Down")

    is_open = check_and_update_section(mock_db, section)

    assert not is_open 
    mock_db.commit.assert_not_called() 