#!/usr/bin/env python
"""Tests for `wibor_simulation` package."""
# pylint: disable=redefined-outer-name

from wibor_simulation import Credit, Installment


def test_can_init_credit():
    credit = Credit(5000, 1, 0.025)
    assert credit
    assert isinstance(credit, Credit)


def test_can_calculate_interest_value():
    credit = Credit(5000, 1, 0.025)
    assert credit.interest_value == 125


def test_can_calculate_interest_with_provision_value():
    credit = Credit(5000, 1, 0.015, provision=0.01)
    assert credit.interest_value == 125


def test_can_calculate_total_value():
    credit = Credit(5000, 1, 0.015, provision=0.01)
    assert credit.total == 5125


def test_can_parse_installments():
    credit = Credit(5000, 1, 0.015, provision=0.01)
    assert credit.installments == 1


def test_can_compute_loan_installments():
    credit = Credit(300000, 300, 0.047)
    assert round(credit.installment, 2) == 1701.74


def test_can_compute_loan_total_cost():
    credit = Credit(300000, 300, 0.047)
    assert round(credit.total_cost, 2) == 510520.75
    assert round(credit.total_interest, 2) == 210520.75


def test_can_init_installment():
    installment = Installment(300000, 0.047, 300)
    assert isinstance(installment, Installment)


def test_can_compute_constant_installment():
    installment = Installment(300000, 0.047, 300)
    assert round(installment.sum, 2) == 1701.74


def test_can_compute_constant_installment_interest():
    installment = Installment(300000, 0.047, 300)
    assert round(installment.interest, 2) == 1175.0


def test_can_compute_constant_installment_capital():
    installment = Installment(300000, 0.047, 300)
    assert round(installment.capital, 2) == 526.74
