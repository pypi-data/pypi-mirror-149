"""
Alvin Package for Airflow

This plugin contains the installation necessary to
integrate Airflow with Alvin platform.
"""

import logging
from airflow.plugins_manager import AirflowPlugin
from alvin_integration.producers.airflow.installer import AlvinAirflowInstaller

log = logging.getLogger(__name__)

alvin_manager = AlvinAirflowInstaller()

alvin_manager.install()


class AlvinAirflowPatch(AirflowPlugin):
    name = "alvin_airflow_plugin"
