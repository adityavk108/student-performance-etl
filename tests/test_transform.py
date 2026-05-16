import pytest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'etl'))

from transform import transform_data


def test_grade_assignment():
    """Verify grade is assigned correctly for all grade ranges."""
    data = {
        'student_id': [1, 2, 3, 4, 5, 6],
        'name': ['A', 'B', 'C', 'D', 'E', 'F'],
        'subject': ['Math', 'Math', 'Math', 'Math', 'Math', 'Math'],
        'marks': [95, 89, 75, 74, 50, 49]
    }
    df = pd.DataFrame(data)
    result = transform_data(df)
    
    assert result.loc[result['student_id'] == 1, 'grade'].values[0] == 'A'
    assert result.loc[result['student_id'] == 2, 'grade'].values[0] == 'B'
    assert result.loc[result['student_id'] == 3, 'grade'].values[0] == 'B'
    assert result.loc[result['student_id'] == 4, 'grade'].values[0] == 'C'
    assert result.loc[result['student_id'] == 5, 'grade'].values[0] == 'C'
    assert result.loc[result['student_id'] == 6, 'grade'].values[0] == 'D'


def test_pass_fail_logic():
    """Verify PASS/FAIL is assigned correctly based on 50 threshold."""
    data = {
        'student_id': [1, 2, 3, 4],
        'name': ['A', 'B', 'C', 'D'],
        'subject': ['Math', 'Math', 'Math', 'Math'],
        'marks': [50, 49, 100, 0]
    }
    df = pd.DataFrame(data)
    result = transform_data(df)
    
    assert result.loc[result['student_id'] == 1, 'pass_fail'].values[0] == 'PASS'
    assert result.loc[result['student_id'] == 2, 'pass_fail'].values[0] == 'FAIL'
    assert result.loc[result['student_id'] == 3, 'pass_fail'].values[0] == 'PASS'
    assert result.loc[result['student_id'] == 4, 'pass_fail'].values[0] == 'FAIL'


def test_transform_output_columns():
    """Verify all required columns are present in output."""
    data = {
        'student_id': [1],
        'name': ['Test'],
        'subject': ['Math'],
        'marks': [75]
    }
    df = pd.DataFrame(data)
    result = transform_data(df)
    
    expected_cols = ['student_id', 'name', 'subject', 'marks', 
                     'pass_fail', 'grade', 'processed_at']
    
    for col in expected_cols:
        assert col in result.columns, f"Missing column: {col}"


def test_duplicate_removal():
    """Verify duplicate rows (same student_id + subject) are removed."""
    data = {
        'student_id': [1, 1],
        'name': ['Test', 'Test'],
        'subject': ['Math', 'Math'],
        'marks': [75, 80]
    }
    df = pd.DataFrame(data)
    result = transform_data(df)
    
    assert len(result) == 1


def test_null_handling():
    """Verify rows with null values are removed."""
    data = {
        'student_id': [1, 2],
        'name': ['Test', None],
        'subject': ['Math', 'Math'],
        'marks': [75, 80]
    }
    df = pd.DataFrame(data)
    result = transform_data(df)
    
    assert len(result) == 1