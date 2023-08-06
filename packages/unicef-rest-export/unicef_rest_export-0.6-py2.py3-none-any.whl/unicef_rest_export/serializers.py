from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
from rest_framework import serializers
from tablib import Dataset


class ExportSerializer(serializers.ListSerializer):
    """Transforms data into a dataset"""
    read_only = True

    def get_header_label(self, field):
        try:
            label = self.child.fields[field].label
        except KeyError:
            label = field
        return label

    def get_headers(self, data):
        headers = []
        for field in data[0].keys():
            headers.append(str(self.get_header_label(field)))
        return headers

    def get_dataset(self, data):
        headers = self.get_headers(data)
        data_list = []
        for d in data:
            data_list.append([v for _, v in d.items()])
        dataset = Dataset(*data_list, headers=headers)
        return dataset

    def transform_dataset(self, dataset):
        view = self.context.get('view', None)
        if view and hasattr(view, 'transform_dataset'):
            return self.context['view'].transform_dataset(dataset)
        return dataset

    @property
    def data(self):
        data = super().data
        if isinstance(data, Dataset) or data:
            dataset = self.get_dataset(data)
            return self.transform_dataset(dataset)
        else:
            return Dataset([])


class XLSXExportSerializer(ExportSerializer):

    def get_dataset(self, data):
        headers = self.get_headers(data)
        data_list = []
        for d in data:
            data_list.append([ILLEGAL_CHARACTERS_RE.sub('', v) if isinstance(v, str) else v for _, v in d.items()])

        dataset = Dataset(*data_list, headers=headers)
        return dataset
