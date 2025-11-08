import pytest
from password_generator import PasswordGenerator
from password_validator import PasswordValidator

@pytest.fixture
def generator():
    return PasswordGenerator()

@pytest.fixture
def validator():
    return PasswordValidator()

def test_generate_password_basic():
    generator = PasswordGenerator()
    result = generator.generate_password(length=12)
    password = result['password']
    assert len(password) == 12
    assert any(c.islower() for c in password)
    assert any(c.isupper() for c in password)
    assert any(c.isdigit() for c in password)
    assert any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

def test_generate_password_custom():
    generator = PasswordGenerator()
    result = generator.generate_password(
        length=10,
        use_lower=True,
        use_upper=False,
        use_digits=True,
        use_symbols=False
    )
    password = result['password']
    assert len(password) == 10
    assert any(c.islower() for c in password)
    assert not any(c.isupper() for c in password)
    assert any(c.isdigit() for c in password)
    assert not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

def test_password_strength():
    validator = PasswordValidator()
    
    # Test weak password
    weak = validator.calculate_strength("password123")
    assert weak['strength'] in ["Sangat Lemah", "Lemah"]
    assert weak['score'] < 50
    
    # Test strong password
    strong = validator.calculate_strength("P@ssw0rd!2023Complex")
    assert strong['strength'] in ["Kuat", "Sangat Kuat"]
    assert strong['score'] > 60

def test_password_validation():
    validator = PasswordValidator()
    
    # Test valid password
    assert validator.validate_password("P@ssw0rd!") is True
    
    # Test invalid passwords
    with pytest.raises(ValueError):
        validator.validate_password("short")  # Too short
        
    with pytest.raises(ValueError):
        validator.validate_password("password")  # Missing uppercase
        
    with pytest.raises(ValueError):
        validator.validate_password("Password")  # Missing number
        
    with pytest.raises(ValueError):
        validator.validate_password("Password1")  # Missing symbol

def test_memorable_password():
    generator = PasswordGenerator()
    result = generator.generate_memorable_password(num_words=3)
    password = result['password']
    
    # Password should contain capital letters (from word capitalization)
    assert any(c.isupper() for c in password)
    
    # Should include number and symbol by default
    assert any(c.isdigit() for c in password)
    assert any(c in generator.symbols for c in password)

def test_pin_generation():
    generator = PasswordGenerator()
    
    # Test default length (6)
    pin = generator.generate_pin()
    assert len(pin) == 6
    assert pin.isdigit()
    
    # Test custom length
    pin = generator.generate_pin(length=8)
    assert len(pin) == 8
    assert pin.isdigit()
    
    # Test minimum length requirement
    with pytest.raises(ValueError):
        generator.generate_pin(length=3)

def test_password_history():
    generator = PasswordGenerator()
    
    # Generate a few passwords
    for _ in range(5):
        generator.generate_password()
    
    history = generator.get_history()
    assert len(history) == 5
    
    # Check history structure
    latest = history[-1]
    assert 'password' in latest
    assert 'strength' in latest
    assert 'timestamp' in latest
    
    # Test history limit (should keep only last 10)
    for _ in range(10):
        generator.generate_password()
    
    history = generator.get_history()
    assert len(history) == 10

def test_repeating_patterns():
    validator = PasswordValidator()
    
    # Test password with repeating patterns
    result = validator.calculate_strength("abcabc123")
    assert result['score'] < 60  # Should have lower score due to pattern
    assert any("pola" in feedback.lower() for feedback in result['feedback'])
    
    # Test password without repeating patterns
    result = validator.calculate_strength("P@ssw0rd!2023")
    assert not any("pola" in feedback.lower() for feedback in result['feedback'])

def test_character_distribution():
    validator = PasswordValidator()
    
    # Test password with poor distribution
    result = validator.calculate_strength("AAAbbb111!!!")
    assert result['score'] < 80  # Should have lower score
    
    # Test password with good distribution
    result = validator.calculate_strength("aB1!cD2@eF3#")
    assert result['score'] >= 80  # Should have higher score