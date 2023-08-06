"""Main module."""

from copy import deepcopy
from functools import lru_cache
from typing import List, Union


class Charges:
    rate: float

    def __init__(self, rate):
        self.rate = rate

    def __add__(self, other):

        if isinstance(other, self.__class__):
            return self.rate + other.rate

        else:
            # try-out default other __add__
            return other + self.rate


class Interest(Charges):
    pass


class Provision(Charges):
    pass


class Installments:
    number: int

    def __init__(self, number):
        self.number = number


class Installment:

    base_capital: int
    total_rate: float
    installments_number: int

    def __init__(
        self, base_capital: int, total_rate: float, installments_number: int
    ):
        self.base_capital = base_capital
        self.total_rate = total_rate
        self.installments_number = installments_number

    #        wibor6M  + x + y
    # 2.25 = 0.25% + 1.10% + 0.9%
    # 2.95 = 0.25% + 1.81% + 0.9%
    # 2.06 = 0.25% + 1.81%
    @staticmethod
    @lru_cache(maxsize=None)
    def _compute_installment(capital, interest_rate, no_installments):
        """
        q = 1 + eff_interest_rate/capitalization_factor
        capital * (q ** no_installments)(q - 1)/(q**n - 1)
        """
        q = 1 + interest_rate / 12
        return (
            capital
            * (q**no_installments)
            * (q - 1)
            / (q**no_installments - 1)
        )

    @property
    def sum(self):
        return self._compute_installment(
            self.base_capital, self.total_rate, self.installments_number
        )

    @property
    def interest(self):
        # https://finanse.rankomat.pl/poradniki/jak-obliczyc-odsetki-i-rate-kredytu-hipotecznego/
        # NOTE: assumes the typical month is 31 days a
        return self.base_capital * self.total_rate * (1 / 12.0)

    @property
    def capital(self):
        return self.sum - self.interest


class Credit:

    start_value: float
    _interest: Interest
    _provision: Provision
    _installments: Installments

    def __init__(
        self,
        nominal_value: Union[float, int],
        installments: int,
        interest: float,
        provision: float = None,
        wibor6m: float = None,
    ):
        self.start_value = nominal_value

        self._interest = (
            Interest(interest) if not wibor6m else Interest(interest + wibor6m)
        )
        self._provision = Provision(provision) if provision else Provision(0)
        self._installments = Installments(installments)
        self._constant_installment = Installment(
            self.capital, self._interest.rate, self.installments
        )

    @property
    def interest_value(self):
        return (self._interest + self._provision) * self.start_value

    @property
    def interest(self):
        return self.interest_value

    @property
    def capital(self):
        return self.start_value

    @property
    def total(self):
        return self.capital + self.interest

    @property
    def installments(self):
        return self._installments.number

    @property
    def installment(self):
        return self._constant_installment.sum

    @property
    def installment_interest(self):
        return self._constant_installment.interest

    @property
    def installment_capital(self):
        return self._constant_installment.capital

    @property
    def total_cost(self):
        return self.installments * self.installment

    @property
    def total_interest(self):
        return self.total_cost - self.capital


class Simulation:
    def __init__(
        self,
        capital: float,
        bank_profit: float,
        no_installments: int,
        wibors: List[float],
    ):

        print(
            "WIBOR6M BANK_INTEREST CAPITAL NO TOTAL_COST INSTALLMENT I-INTEREST I-CAPITAL"
        )
        for wibor in wibors:
            credit = Credit(
                nominal_value=capital,
                installments=no_installments,
                interest=bank_profit,
                wibor6m=wibor,
            )
            print(
                f"{100*wibor:<3.2f}% {100*bank_profit:<3.2f}% {credit.capital} {credit.installments} {credit.total_cost:>10.2f} {credit.installment:>10.2f} {credit.installment_interest:>10.2f} {credit.installment_capital:>10.2f}"
            )


class ScheduleProjection:
    def __init__(
        self,
        capital: float,
        bank_profit: float,
        no_installments: int,
        wibor: float,
    ):

        print("# CAPITAL INSTALLMENT I-INTEREST I-CAPITAL")
        current_capital = deepcopy(capital)
        installments_left = deepcopy(no_installments)
        total_rate = deepcopy(bank_profit + wibor)
        total_interest = 0
        total_paid = 0
        for _ in range(no_installments, 0, -1):
            installment = Installment(
                current_capital,
                total_rate,
                installments_left,
            )
            print(
                f"{installments_left} {current_capital:<3.2f} {installment.sum:<3.2f} {installment.interest:<3.2f} {installment.capital:<3.2f}"
            )
            installments_left -= 1
            current_capital -= installment.capital
            total_interest += installment.interest
            total_paid += installment.sum

        print(f"TOTAL PAID    : {total_paid:<3.2f}")
        print(f"TOTAL INTEREST: {total_interest:<3.2f}")
        print(f"% COST        : {100*(total_paid)/(float(capital)):<3.2f}")
