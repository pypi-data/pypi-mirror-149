"""Console script for wibor_simulation."""

from typing import List

import fire

from wibor_simulation import ScheduleProjection, Simulation


def simulation(
    capital: float,
    bank_profit: float,
    no_installments: int,
    wibors: List[float],
):
    Simulation(capital, bank_profit, no_installments, wibors)


def schedule(
    capital: float,
    bank_profit: float,
    no_installments: int,
    wibor: float,
):
    ScheduleProjection(capital, bank_profit, no_installments, wibor)


def help():
    print("wibor_simulation")


def main():
    fire.Fire({"help": help, "simulation": simulation, "schedule": schedule})


if __name__ == "__main__":
    main()  # pragma: no cover
