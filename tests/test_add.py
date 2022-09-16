import pytest

from app.calculations import BankAccount, InsufficientFunds


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


def test_bank_account(bank_account):
    assert bank_account.balance == 50


def test_withdraw(bank_account):
    bank_account.withdraw(40)
    assert bank_account.balance == 10


def test_deposit(bank_account):
    bank_account.deposit(40)
    assert bank_account.balance == 90


@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000),
    (100, 20, 80)
])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected


# def test_insufficient_funds(bank_account):
#     try:
#         bank_account.withdraw(200)
#     except InsufficientFunds:
#         assert True


def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)