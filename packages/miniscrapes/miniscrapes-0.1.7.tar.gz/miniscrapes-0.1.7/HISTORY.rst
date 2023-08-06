=======
History
=======

0.1.7 (2022-05-08)
------------------
* Added air quality index from the AirNow API.

0.1.6 (2022-04-13)
------------------
* Update Covid tracker to use new NYT data source (the old one is no longer
  updated), use DuckDB to identify latest reading, and cache intermediate
  download to avoid multiple requests against NYT's servers.
* Move dependencies from requirements.txt to setup.py.
* Introduce mypy in linting process.

0.1.0 (2021-01-24)
------------------

* First release on PyPI.
