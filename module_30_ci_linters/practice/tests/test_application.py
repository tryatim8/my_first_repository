from module_30_ci_linters.practice.src.main import sum_two

def test_hello_thing():
    result = sum_two(1, 2)
    assert result == 3
