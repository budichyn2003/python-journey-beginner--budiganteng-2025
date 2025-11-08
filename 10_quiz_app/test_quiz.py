import pytest
import json
import os
from quiz import Quiz
from datetime import datetime

@pytest.fixture
def quiz_file(tmp_path):
    """Create a temporary quiz file for testing"""
    file_path = tmp_path / "test_quiz.json"
    data = {
        "categories": ["Test"],
        "quizzes": {
            "Test": [
                {
                    "question": "Test Question 1?",
                    "answers": ["A", "B", "C", "D"],
                    "correct_answer": 0,
                    "explanation": "Test explanation"
                },
                {
                    "question": "Test Question 2?",
                    "answers": ["W", "X", "Y", "Z"],
                    "correct_answer": 1
                }
            ]
        }
    }
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    return str(file_path)

@pytest.fixture
def quiz(quiz_file):
    """Create a Quiz instance for testing"""
    return Quiz(quiz_file)

def test_load_quizzes(quiz):
    """Test loading quiz data from file"""
    data = quiz.load_quizzes()
    assert "categories" in data
    assert "quizzes" in data
    assert "Test" in data["categories"]
    assert len(data["quizzes"]["Test"]) == 2

def test_add_category(quiz):
    """Test adding a new category"""
    quiz.add_category("New Category")
    categories = quiz.get_categories()
    assert "New Category" in categories
    assert "quizzes" in quiz.quizzes
    assert "New Category" in quiz.quizzes["quizzes"]
    assert quiz.quizzes["quizzes"]["New Category"] == []

def test_add_question(quiz):
    """Test adding a new question"""
    category = "Test"
    question = "New Question?"
    answers = ["A", "B", "C", "D"]
    correct_answer = 2
    explanation = "Test explanation"
    
    quiz.add_question(category, question, answers, correct_answer, explanation)
    
    questions = quiz.quizzes["quizzes"][category]
    new_question = questions[-1]
    
    assert new_question["question"] == question
    assert new_question["answers"] == answers
    assert new_question["correct_answer"] == correct_answer
    assert new_question["explanation"] == explanation

def test_start_quiz(quiz):
    """Test starting a new quiz"""
    quiz.start_quiz("Test", 1)
    assert quiz.current_quiz is not None
    assert quiz.current_quiz["category"] == "Test"
    assert len(quiz.current_quiz["questions"]) == 1
    assert isinstance(quiz.current_quiz["start_time"], datetime)
    assert quiz.score == 0
    assert quiz.total_questions == 1
    assert quiz.current_question == 0

def test_get_current_question(quiz):
    """Test getting current question"""
    quiz.start_quiz("Test", 1)
    question = quiz.get_current_question()
    
    assert question is not None
    assert "question" in question
    assert "answers" in question
    assert "number" in question
    assert "total" in question
    assert question["number"] == 1
    assert question["total"] == 1

def test_submit_answer(quiz):
    """Test submitting an answer"""
    quiz.start_quiz("Test", 1)
    result = quiz.submit_answer(0)  # Submit correct answer
    
    assert result is not None
    assert "is_correct" in result
    assert "correct_answer" in result
    assert "score" in result
    assert "total" in result
    assert result["score"] == 1
    assert result["total"] == 1

def test_get_final_results(quiz):
    """Test getting final results"""
    quiz.start_quiz("Test", 2)
    quiz.submit_answer(0)  # Correct
    quiz.submit_answer(0)  # Wrong for second question
    
    results = quiz.get_final_results()
    
    assert results is not None
    assert results["category"] == "Test"
    assert results["score"] == 1
    assert results["total_questions"] == 2
    assert results["percentage"] == 50.0
    assert "duration" in results
    assert "answers" in results
    assert len(results["answers"]) == 2

def test_save_and_get_results_history(quiz, tmp_path):
    """Test saving and loading results history"""
    results_file = tmp_path / "test_results.json"
    
    # Create test results
    quiz.start_quiz("Test", 1)
    quiz.submit_answer(0)
    results = quiz.get_final_results()
    
    # Save results
    quiz.save_results(results, str(results_file))
    
    # Load history
    history = quiz.get_results_history(str(results_file))
    
    assert len(history) == 1
    assert history[0]["category"] == "Test"
    assert history[0]["score"] == 1

def test_invalid_category(quiz):
    """Test starting quiz with invalid category"""
    with pytest.raises(ValueError):
        quiz.start_quiz("Invalid Category")

def test_empty_category(quiz):
    """Test starting quiz with empty category"""
    quiz.add_category("Empty")
    with pytest.raises(ValueError):
        quiz.start_quiz("Empty")

def test_quiz_completion(quiz):
    """Test complete quiz flow"""
    quiz.start_quiz("Test", 2)
    
    # Answer first question
    q1 = quiz.get_current_question()
    assert q1["number"] == 1
    result1 = quiz.submit_answer(0)
    assert result1["is_correct"] == True
    
    # Answer second question
    q2 = quiz.get_current_question()
    assert q2["number"] == 2
    result2 = quiz.submit_answer(1)
    assert result2["is_correct"] == True
    
    # Get final results
    results = quiz.get_final_results()
    assert results["score"] == 2
    assert results["percentage"] == 100.0

def test_no_quiz_started(quiz):
    """Test operations when no quiz is started"""
    assert quiz.get_current_question() is None
    assert quiz.submit_answer(0) is None
    assert quiz.get_final_results() is None