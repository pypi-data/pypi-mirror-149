from django.db import models
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_model import models as edc_models
from edc_model.models import HistoricalRecords
from edc_sites.models import CurrentSiteManager, SiteModelMixin
from edc_utils import get_utcnow
from edc_visit_tracking.managers import CrfModelManager

from .model_mixins import (
    BiosynexSemiQuantitativeCragMixin,
    CsfCultureModelMixin,
    CsfModelMixin,
    LpModelMixin,
    QuantitativeCultureModelMixin,
)


class LpCsf(
    UniqueSubjectIdentifierFieldMixin,
    LpModelMixin,
    CsfModelMixin,
    CsfCultureModelMixin,
    BiosynexSemiQuantitativeCragMixin,
    QuantitativeCultureModelMixin,
    SiteModelMixin,
    edc_models.BaseUuidModel,
):

    report_datetime = models.DateTimeField(default=get_utcnow)

    on_site = CurrentSiteManager()

    objects = CrfModelManager()

    history = HistoricalRecords()

    class Meta(edc_models.BaseUuidModel.Meta):
        verbose_name = "Lumbar Puncture/Cerebrospinal Fluid"
        verbose_name_plural = "Lumbar Puncture/Cerebrospinal Fluid"
