from django.conf import settings
from rest_framework.generics import ListAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.settings import perform_import
from rest_framework.viewsets import GenericViewSet
from tablib import Dataset

from unicef_rest_export.renderers import ExportBaseRenderer, ExportOpenXMLRenderer
from unicef_rest_export.serializers import ExportSerializer, XLSXExportSerializer

DEFAULT_TEMPLATE = False
EXPORT_RENDERERS = getattr(settings, "EXPORT_RENDERERS", None)
if EXPORT_RENDERERS is None:
    EXPORT_RENDERERS = (
        "unicef_rest_export.renderers.ExportCSVRenderer",
        "unicef_rest_export.renderers.ExportJSONRenderer",
        "unicef_rest_export.renderers.ExportOpenXMLRenderer",
        "unicef_rest_export.renderers.ExportExcelRenderer",
        "unicef_rest_export.renderers.ExportPDFRenderer",
        "unicef_rest_export.renderers.ExportPDFTableRenderer",
        "unicef_rest_export.renderers.ExportDocxRenderer",
        "unicef_rest_export.renderers.ExportDocxTableRenderer",
    )
    if "unicef_rest_export" in settings.INSTALLED_APPS:
        DEFAULT_TEMPLATE = True
        EXPORT_RENDERERS = (
            "unicef_rest_export.renderers.ExportHTMLRenderer",
        ) + EXPORT_RENDERERS

EXPORT_RENDERERS = perform_import(EXPORT_RENDERERS, "EXPORT_RENDERERS")


class ExportMixin:
    export_serializer_class = ExportSerializer

    def with_list_serializer(self, cls, export_serializer_class=None):
        meta = getattr(cls, 'Meta', object)
        if getattr(meta, 'list_serializer_class', None):
            return cls

        class SerializerWithListSerializer(cls):
            class Meta(meta):
                list_serializer_class = export_serializer_class or self.export_serializer_class

        return SerializerWithListSerializer

    def get_serializer_class(self):
        # c.f rest_framework.generics.GenericAPIView
        # (not using super() since this is a mixin class)
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )

        renderer = self.request.accepted_renderer
        if isinstance(renderer, ExportOpenXMLRenderer):
            return self.with_list_serializer(self.serializer_class, XLSXExportSerializer)
        elif isinstance(renderer, ExportBaseRenderer):
            return self.with_list_serializer(self.serializer_class)
        else:
            return self.serializer_class

    def get_data(self, serializer):
        data = serializer.data
        if isinstance(self.request.accepted_renderer, ExportBaseRenderer):
            headers = []
            for field in data.keys():
                try:
                    label = serializer.fields[field].label
                except KeyError:
                    label = field
                headers.append(label)
            dataset = Dataset(*[[v for _, v in data.items()]], headers=headers)
            if hasattr(self, "transform_dataset"):
                data = self.transform_dataset(dataset)
            else:
                data = dataset
        return data

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(self.get_data(serializer))


class ExportViewBase(ExportMixin):
    renderer_classes = EXPORT_RENDERERS
    pagination_class = None
    if DEFAULT_TEMPLATE:
        template_name = 'rest_export.html'


class ExportView(ExportViewBase, ListAPIView):
    """Export-capable model list view"""
    pass


class ExportViewSet(ExportViewBase, ListModelMixin, GenericViewSet):
    """Export-capable model ViewSet (list only)"""
    pass


class ExportModelView(ListAPIView):
    """Label for export would be retrieved from label attribute"""

    @staticmethod
    def set_labels(serializer_fields, model):
        labels = {}
        model_labels = {}
        for f in model._meta.fields:
            model_labels[f.name] = f.verbose_name
        for f in serializer_fields:
            if model_labels.get(f, False):
                labels[f] = model_labels.get(f)
            elif serializer_fields.get(f) and serializer_fields[f].label:
                labels[f] = serializer_fields[f].label
            else:
                labels[f] = f.replace("_", " ").title()
        return labels

    def get_renderer_context(self):
        context = super().get_renderer_context()
        if hasattr(self, "get_serializer_class"):
            serializer_class = self.get_serializer_class()
            serializer = serializer_class()
            serializer_fields = serializer.get_fields()
            model = getattr(serializer.Meta, "model")
            context["labels"] = self.set_labels(
                serializer_fields,
                model
            )
        return context
