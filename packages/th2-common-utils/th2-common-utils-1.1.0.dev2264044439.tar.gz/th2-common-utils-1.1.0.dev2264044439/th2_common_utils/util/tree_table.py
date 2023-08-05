#   Copyright 2022-2022 Exactpro (Exactpro Systems Limited)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import enum
from typing import Dict, Union

from sortedcontainers import SortedDict
from th2_common_utils.event_utils import EventUtils
from th2_common_utils.util.common import SimpleType


class TableEntityType(str, enum.Enum):

    ROW = 'row'
    COLLECTION = 'collection'
    TREE_TABLE = 'treeTable'


class Row:

    def __init__(self) -> None:
        self.type = TableEntityType.ROW
        self.columns: Dict[str, SimpleType] = {}

    def add_column(self, name: str, value: SimpleType) -> None:
        self.columns[name] = value


class Collection:

    def __init__(self) -> None:
        self.type = TableEntityType.COLLECTION
        self.rows = SortedDict()

    def add_row(self, name: SimpleType, row: Row) -> None:
        self.rows[name] = row


class TreeTable:

    def __init__(self) -> None:
        self.type = TableEntityType.TREE_TABLE
        self.rows = SortedDict()

    def __bytes__(self) -> bytes:
        return EventUtils.create_event_body(self)

    def add_row(self, name: str, table_entity: Union[Row, Collection]) -> None:
        self.rows[name] = table_entity
