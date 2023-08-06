import abc
from aoa.api.base_api import BaseApi
from aoa.api.api_iterator import ApiIterator


class IteratorBaseApi(BaseApi):
    __metaclass__ = abc.ABCMeta

    def __init__(self, aoa_client=None, iterator_projection=None, show_archived=True):
        super().__init__(aoa_client=aoa_client)

        self.iterator_projection = iterator_projection

        if show_archived:
            self.iterator_func = self.find_all
        else:
            self.iterator_func = self.find_by_archived

    def __iter__(self):
        return ApiIterator(api_func=self.iterator_func,
                           entities=self.path.split('/')[-2],
                           projection=self.iterator_projection)

    def __len__(self):
        return self.find_all()['page']['totalElements']
