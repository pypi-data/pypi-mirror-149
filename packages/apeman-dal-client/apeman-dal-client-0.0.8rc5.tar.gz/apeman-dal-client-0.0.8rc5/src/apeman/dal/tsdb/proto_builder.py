from apeman.dal.tsdb import tsdb_pb2
from apeman.dal.tsdb.enum import DataAmount
from apeman.dal.tsdb.enum import DataType


class ColumnDefinitionBuilder(object):
    name = None
    data_type = None
    limit = None
    non_null = None

    def __init__(self):
        self.__reset__()

    def __reset__(self):
        self.name = None
        self.data_type = None
        self.limit = None
        self.non_null = None

    def set_name(self, name: str = None):
        self.name = name
        return self

    def set_type(self, data_type: DataType):
        self.data_type = data_type
        return self

    def set_limit(self, limit: int = None):
        self.limit = limit
        return self

    def set_non_null(self, non_null: bool = None):
        self.non_null = non_null
        return self

    def build(self) -> tsdb_pb2.ColumnDefinition:
        data_type = DataTypeBuilder().set_type(self.data_type).build()
        ret = tsdb_pb2.ColumnDefinition(name=self.name, type=data_type, limit=self.limit,
                                        nonNull=self.non_null)
        self.__reset__()
        return ret


class CreateDatafeedRequestBuilder(object):
    name = ''
    tag = []
    field = []
    unique_key = []
    data_amount = None

    def __init__(self):
        self.__reset__()

    def __reset__(self):
        self.name = ''
        self.tag = []
        self.field = []
        self.unique_key = []
        self.data_amount = None

    def set_name(self, name: str = None):
        self.name = name
        return self

    def add_tag(self, tag: tsdb_pb2.ColumnDefinition = None):
        self.tag.append(tag)
        return self

    def add_field(self, field: tsdb_pb2.ColumnDefinition = None):
        self.field.append(field)
        return self

    def add_unique_key(self, unique_key: tsdb_pb2.UniqueKey = None):
        self.unique_key.append(unique_key)
        return self

    def set_data_amount(self, data_amount: DataAmount = None):
        self.data_amount = data_amount
        return self

    def build(self) -> tsdb_pb2.CreateDatafeedRequest:
        data_amount = DataAmountBuilder().set_data_amount(self.data_amount).build()
        ret = tsdb_pb2.CreateDatafeedRequest(name=self.name, tag=self.tag, field=self.field,
                                             uniqueKey=self.unique_key, dataAmount=data_amount)
        self.__reset__()
        return ret


class DataAmountBuilder(object):
    data_amount = DataAmount.UNKNOWN.value

    def __init__(self):
        self.__reset__()

    def __reset__(self):
        self.data_amount = None

    def set_data_amount(self, data_amount: DataAmount = DataAmount.UNKNOWN):
        self.data_amount = data_amount.value
        return self

    def build(self) -> tsdb_pb2.DataAmount:
        ret = tsdb_pb2.DataAmount.Value(self.data_amount)
        self.__reset__()
        return ret


class DataTypeBuilder(object):
    data_type = DataType.UNKNOWN.value

    def __init__(self):
        self.__reset__()

    def __reset__(self):
        self.data_type = None

    def set_type(self, data_type: DataType = DataType.UNKNOWN):
        self.data_type = data_type.value
        return self

    def build(self) -> tsdb_pb2.DataType:
        ret = tsdb_pb2.DataType.Value(self.data_type)
        self.__reset__()
        return ret


class UniqueKeyBuilder(object):
    name = []

    def __init__(self):
        self.__reset__()

    def __reset__(self):
        self.name = []

    def add(self, name: str = None):
        self.name.append(name)
        return self

    def build(self) -> tsdb_pb2.UniqueKey:
        ret = tsdb_pb2.UniqueKey(name=self.name)
        self.__reset__()
        return ret


class ValBuilder(object):
    s = None
    i64 = None
    i32 = None
    d = None
    f = None
    b = None
    ts = None

    def __int__(self):
        self.__reset__()

    def __reset__(self):
        self.s = None
        self.i64 = None
        self.i32 = None
        self.d = None
        self.f = None
        self.b = None
        self.ts = None

    def set_s(self, s: str = None):
        self.__reset__()
        self.s = s
        return self

    def set_i64(self, i64: int = None):
        self.__reset__()
        self.i64 = i64
        return self

    def set_i32(self, i32: int = None):
        self.__reset__()
        self.i32 = i32
        return self

    def set_d(self, d: float = None):
        self.__reset__()
        self.d = d
        return self

    def set_f(self, f: float = None):
        self.__reset__()
        self.f = f
        return self

    def set_b(self, b: bool = None):
        self.__reset__()
        self.b = b
        return self

    def set_ts(self, ts: tsdb_pb2.Timestamp):
        self.__reset__()
        self.ts = ts

    def build(self) -> tsdb_pb2.Val:
        ret = tsdb_pb2.Val(s=self.s, i64=self.i64, i32=self.i32, d=self.d, f=self.f, b=self.b, ts=self.ts)
        self.__reset__()
        return ret


class TimestampBuilder(object):
    epoch_in_millis = None

    def __int__(self):
        self.__reset__()

    def __reset__(self):
        self.val = []

    def set_epoch_in_millis(self, epoch_in_millis: int = None):
        self.epoch_in_millis = epoch_in_millis
        return self

    def build(self) -> tsdb_pb2.Timestamp:
        ret = tsdb_pb2.Timestamp(epochInMillis=self.epoch_in_millis)
        self.__reset__()
        return ret


class TupleBuilder(object):
    val = []

    def __int__(self):
        self.__reset__()

    def __reset__(self):
        self.val = []

    def add_val(self, val: tsdb_pb2.Val):
        self.val.append(val)
        return self

    def build(self):
        ret = tsdb_pb2.Tuple(cell=self.val)
        self.__reset__()
        return ret


class ColumnMetaBuilder(object):
    name = None
    data_type = None

    def __int__(self):
        self.__reset__()

    def __reset__(self):
        self.name = None
        self.data_type = None

    def set_name(self, name: str):
        self.name = name
        return self

    def set_data_type(self, data_type: DataType):
        self.data_type = data_type
        return self

    def build(self):
        data_type_builder = DataTypeBuilder()
        data_type = data_type_builder.set_type(self.data_type).build()
        ret = tsdb_pb2.ColumnMeta(name=self.name, type=data_type)
        self.__reset__()
        return ret


class TabularDataBuilder(object):
    column = []
    tuple = []

    def __int__(self):
        self.__reset__()

    def __reset__(self):
        self.column = []
        self.tuple = []

    def add_column(self, column: tsdb_pb2.ColumnMeta):
        self.column.append(column)
        return self

    def add_tuple(self, t: tsdb_pb2.Tuple = None):
        self.tuple.append(t)
        return self

    def build(self):
        ret = tsdb_pb2.TabularData(column=self.column, tuple=self.tuple)
        self.__reset__()
        return ret


class PutDataRequest(object):
    datafeed = None
    tabular_data = None

    def __int__(self):
        self.__reset__()

    def __reset__(self):
        self.datafeed = None
        self.tabular_data = None

    def set_datafeed(self, datafeed: str):
        self.datafeed = datafeed
        return self

    def set_tabular_data(self, tabular_data: tsdb_pb2.TabularData):
        self.tabular_data = tabular_data
        return self

    def build(self):
        ret = tsdb_pb2.PutDataRequest(datafeed=self.datafeed, data=self.tabular_data)
        self.__reset__()
        return ret


class OutputColumnBuilder(object):
    expr = None
    alias = None

    def __int__(self):
        self.__reset__()

    def __reset__(self):
        self.expr = None
        self.alias = None

    def set_expr(self, expr):
        self.expr = expr
        return self

    def set_alias(self, alias):
        self.alias = alias
        return self

    def build(self):
        ret = tsdb_pb2.OutputColumn(expr=self.expr, alias=self.alias)
        self.__reset__()
        return ret


class GetDataRequestBuilder(object):
    datafeed = None
    column = []
    where = None
    group_by = None
    having = None
    order_by = None
    offset = 0
    limit = 100

    def __int__(self):
        self.__reset__()

    def __reset__(self):
        self.datafeed = None
        self.column = []
        self.where = None
        self.group_by = None
        self.having = None
        self.order_by = None
        self.offset = 0
        self.limit = 100

    def set_datafeed(self, datafeed: str = None):
        self.datafeed = datafeed
        return self

    def add_column(self, column: tsdb_pb2.OutputColumn = None):
        self.column.append(column)
        return self

    def set_where(self, where: str = None):
        self.where = where
        return self

    def set_group_by(self, group_by: str = None):
        self.group_by = group_by
        return self

    def set_having(self, having: str = None):
        self.having = having
        return self

    def set_order_by(self, order_by: str = None):
        self.order_by = order_by
        return self

    def set_offset(self, offset: int = None):
        self.offset = offset
        return self

    def set_limit(self, limit: int = None):
        self.limit = limit
        return self

    def build(self) -> tsdb_pb2.GetDataRequest:
        ret = tsdb_pb2.GetDataRequest(datafeed=self.datafeed, column=self.column, where=self.where,
                                      groupBy=self.group_by, having=self.having, orderBy=self.having,
                                      offset=self.offset, limit=self.limit)
        self.__reset__()
        return ret
