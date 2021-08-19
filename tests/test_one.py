import pytest


@pytest.mark.parametrize('x', (0, 3, 10, 50, 101))
@pytest.mark.positive
def test_chek_enter_natural_integer(get_home_page, x):
    get_home_page.chek_elements()
    get_home_page.check_factorial(x=x)


@pytest.mark.parametrize('x', ('ws', '', 0.5))
@pytest.mark.negative
def test_enter_not_integer(get_home_page, x):
    get_home_page.chek_elements()
    get_home_page.check_negative_data(x, 'Please enter an integer')


@pytest.mark.parametrize('x', (-1, -100))
@pytest.mark.negative
def test_enter_negative_number(get_home_page, x):
    get_home_page.chek_elements()
    get_home_page.check_negative_data(x, 'Please enter an natural number')  # TODO no error


@pytest.mark.parametrize('page_key', ('terms', 'privacy', 'qxf2'))
@pytest.mark.positive
def test_check_links(get_home_page, page_key):
    page = get_home_page.go_to(page_key)
    page.chek_elements()
