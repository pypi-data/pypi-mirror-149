import sqlalchemy as sa
import sqlalchemy.orm
import jessiql
from typing import Union, Optional

from .mutate_api import MutateApi
from ..defs import PrimaryKeyDict
from ..base import SAInstanceT
from ..crudparams import CrudParams
from ..query.query_api import QueryApi


class ReturningMutateApi(MutateApi, QueryApi):
    """ CRUD API implementation: mutations, returning objects

    Implements mutations that also make a query after they succeed
    """
    def __init__(self,
                 ssn: sa.orm.Session,
                 params: CrudParams,
                 query_object: Union[jessiql.QueryObject, jessiql.QueryObjectDict] = None):
        #MutateApi.__init__(self, ssn, params)  # not needed because QueryApi does just the same
        QueryApi.__init__(self, ssn, params, query_object)
        # TODO: perhaps, get `QueryApi` as the input parameter?

    def _format_result_dict(self, instance: SAInstanceT) -> PrimaryKeyDict:
        primary_key_dict = super()._format_result_dict(instance)
        self.params.from_primary_key_dict(primary_key_dict)
        res = self.get()
        assert res is not None, 'Object not found'
        return res
