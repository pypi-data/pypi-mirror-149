from django.apps import AppConfig
from openIMIS.openimisapps import openimis_apps

import logging

logger = logging.getLogger(__file__)

MODULE_NAME = "report"

DEFAULT_CFG = {
    "gql_query_report_perms": ["131200"],
    "gql_mutation_report_add_perms": ["121002"],
    "gql_mutation_report_edit_perms": ["121003"],
    "gql_mutation_report_delete_perms": ["121004"],
}


class ReportConfig(AppConfig):
    name = MODULE_NAME

    gql_query_report_perms: []
    gql_mutation_report_add_perms: []
    gql_mutation_report_edit_perms: []
    gql_mutation_report_delete_perms: []

    # Legacy permissions for reference
    # REPORTS_PRIMARY_OPERATIONAL_INDICATOR_POLICIES = 131201  # 0x00020081
    # REPORTS_PRIMARY_OPERATIONAL_INDICATORS_CLAIMS = 131202  # 0x00020082
    # REPORTS_DERIVED_OPERATIONAL_INDICATORS = 131203  # 0x00020083
    # REPORTS_CONTRIBUTION_COLLECTION = 131204  # 0x00020084
    # REPORTS_PRODUCT_SALES = 131205  # 0x00020085
    # REPORTS_CONTRIBUTION_DISTRIBUTION = 131206  # 0x00020086
    # REPORTS_USER_ACTIVITY = 131207  # 0x00020087
    # REPORTS_ENROLMENT_PERFORMANCE_INDICATORS = 131208  # 0x00020088
    # REPORTS_STATUS_OF_REGISTER = 131209  # 0x00020089
    # REPORTS_INSUREE_WITHOUT_PHOTOS = 131210  # 0x0002008A
    # REPORTS_PAYMENT_CATEGORY_OVERVIEW = 131211  # 0x0002008B
    # REPORTS_MATCHING_FUNDS = 131212  # 0x0002008C
    # REPORTS_CLAIM_OVERVIEW_REPORT = 131213  # 0x0002008D
    # REPORTS_PERCENTAGE_REFERRALS = 131214  # 0x0002008E
    # REPORTS_FAMILIES_INSUREES_OVERVIEW = 131215  # 0x0002008F
    # REPORTS_PENDING_INSUREES = 131216  # 0x00020090
    # REPORTS_RENEWALS = 131217  # 0x00020091
    # REPORTS_CAPITATION_PAYMENT = 131218  # 0x00020092
    # REPORTS_REJECTED_PHOTO = 131219  # 0x00020093
    # REPORTS_CONTRIBUTION_PAYMENT = 131220  # 0x00020094
    # REPORTS_CONTROL_NUMBER_ASSIGNMENT = 131221  # 0x00020095
    # REPORTS_OVERVIEW_OF_COMMISSIONS = 131222  # 0x00020096
    # REPORTS_CLAIM_HISTORY_REPORT = 131223  # 0x00020097

    reports = []

    def _configure_permissions(self, cfg):
        ReportConfig.gql_query_report_perms = cfg["gql_query_report_perms"]
        ReportConfig.gql_mutation_report_add_perms = cfg[
            "gql_mutation_report_add_perms"
        ]
        ReportConfig.gql_mutation_report_edit_perms = cfg[
            "gql_mutation_report_edit_perms"
        ]
        ReportConfig.gql_mutation_report_delete_perms = cfg[
            "gql_mutation_report_delete_perms"
        ]

    @classmethod
    def get_report(cls, report_name):
        for report in cls.reports:
            if report["name"] == report_name:
                return report
        return None

    def ready(self):
        from core.models import ModuleConfiguration

        cfg = ModuleConfiguration.get_or_default(MODULE_NAME, DEFAULT_CFG)
        self._configure_permissions(cfg)

        all_apps = openimis_apps()

        for app in all_apps:
            try:
                appreports = __import__(f"{app}.report")
                if hasattr(appreports.report, "report_definitions") and isinstance(
                    appreports.report.report_definitions, list
                ):
                    self.reports += appreports.report.report_definitions
                    logger.debug(
                        f"{app} {len(appreports.report.report_definitions)} reports loaded"
                    )
            except ModuleNotFoundError as exc:
                # The module doesn't have a schema.py, just skip
                logger.debug(f"{app} has no schema module, skipping")
            except AttributeError as exc:
                logger.debug(f"{app} queries couldn't be loaded")
                raise  # This can be hiding actual compilation errors
            except Exception as exc:
                logger.debug(f"{app} exception", exc)
        logger.debug("done loading reports")
