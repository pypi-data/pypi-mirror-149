# wibor-simulation


<p align="center">
<a href="https://pypi.python.org/pypi/wibor-simulation">
    <img src="https://img.shields.io/pypi/v/wibor-simulation.svg"
        alt = "Release Status">
</a>

<a href="https://github.com/PhillCli/wibor-simulation/actions">
    <img src="https://github.com/PhillCli/wibor-simulation/actions/workflows/main.yml/badge.svg?branch=release" alt="CI Status">
</a>

<a href="https://wibor-simulation.readthedocs.io/en/latest/?badge=latest">
    <img src="https://readthedocs.org/projects/wibor-simulation/badge/?version=latest" alt="Documentation Status">
</a>

<a href="https://pyup.io/repos/github/PhillCli/wibor-simulation/">
<img src="https://pyup.io/repos/github/PhillCli/wibor-simulation/shield.svg" alt="Updates">
</a>

</p>


Simulates the loan installments at different interest rates


* Free software: MIT
* Documentation: <https://wibor-simulation.readthedocs.io>


## Features

* simulations of loan installment based on changing interest rate (WIBOR6M)

    ```shell
    wibor-simulation simulation 100000.00 0.05 60 0.0025,0.0175,0.0270,0.0500,0.069
    ```


## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [zillionare/cookiecutter-pypackage](https://github.com/zillionare/cookiecutter-pypackage) project template.
