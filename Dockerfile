FROM python:3.14

RUN mkdir /app/
WORKDIR /app

COPY src/PvInstallationCalculationService ./src/PvInstallationCalculationService
COPY pyproject.toml ./
COPY README.md ./

RUN pip install ./
ENTRYPOINT ["python3", "src/PvInstallationCalculationService/pv_installation_calculation_service.py"]
