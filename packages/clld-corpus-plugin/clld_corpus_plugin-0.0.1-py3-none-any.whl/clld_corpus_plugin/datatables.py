from clld.web.datatables.base import DataTable
from clld.web.datatables.base import LinkCol


class Texts(DataTable):
    def col_defs(self):
        return [LinkCol(self, "name")]


def includeme(config):
    config.register_datatable("texts", Texts)
