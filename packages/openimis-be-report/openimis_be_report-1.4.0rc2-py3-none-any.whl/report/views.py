import logging

from django.http import Http404, HttpResponse
from django.template import loader
from django.utils.translation import gettext as _
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied

from report.services import generate_report, get_report_definition

from .apps import ReportConfig

logger = logging.getLogger(__file__)


@api_view(["GET"])
def report(request, report_name, report_format="pdf", alternate=None):
    """
    Run a report
    :param request: Predefined by Django
    :param report_name: Report name within the module
    :param report_format: pdf (default) or xlsx
    :param alternate: Future use, allows several templates for a single report: different languages or report variants
    :return: view
    """
    logger.debug(
        "report name %s in %s format",
        report_name,
        report_format,
    )
    report_config = ReportConfig.get_report(report_name)
    if not report_config:
        raise Http404("Poll does not exist")
    report_definition = get_report_definition(
        report_name, report_config["default_report"]
    )
    if (
        report_config.get("permission")
        and not request.user.has_perms(ReportConfig.gql_query_report_perms)
        and not request.user.has_perms(report_config.get("permission"))
    ):
        raise PermissionDenied(_("unauthorized"))

    # parameters tend to get put in lists because they *could* be repeated
    unlisted = {
        k: (v[0] if isinstance(v, list) and len(v) == 0 else v)
        for k, v in request.GET.items()
    }

    data = report_config["python_query"](request.user, **unlisted)

    return generate_report(
        report_name,
        report_definition,
        data,
        report_format,
    )


@xframe_options_exempt
def reportbro_designer(request):
    template = loader.get_template("report/reportbro.html")

    context = {}
    return HttpResponse(template.render(context, request))


def reportbro_previewer(request):
    pass
