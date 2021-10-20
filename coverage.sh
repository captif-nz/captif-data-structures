#!/bin/bash

pytest -Werror --cov-report xml:./cov.xml --cov captif_data_structures -v tests