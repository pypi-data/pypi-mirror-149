from enum import Enum
from typing import NamedTuple, Optional, Union, List
from typing_extensions import TypedDict
from tim.types import Logs, Id


class BaseUnit(Enum):
  DAY = 'Day'
  HOUR = 'Hour'
  MINUTE = 'Minute'
  SECOND = 'Second'
  MONTH = 'Month'


class Status(Enum):
  REGISTERED = 'Registered'
  RUNNING = 'Running'
  FINISHED = 'Finished'
  FINISHED_WITH_WARNING = 'FinishedWithWarning'
  FAILED = 'Failed'


class DatasetStatusResponse(TypedDict):
  createdAt: str
  status: Status
  progress: int


class RelativeRange(TypedDict):
  baseUnit: BaseUnit
  value: int


class LatestVersion(TypedDict):
  id: str
  status: Status
  numberOfVariables: int
  numberOfObservations: int
  firstTimestamp: str
  lastTimestamp: str


class DatasetWorkspace(TypedDict):
  id: str
  name: str


class Dataset(TypedDict):
  id: str
  latestVersion: LatestVersion
  createdAt: str
  createdBy: str
  updatedAt: str
  updatedBy: str
  description: str
  isFavorite: bool
  estimatedSamplingPeriod: str
  workspace: DatasetWorkspace
  name: str


class Variables(TypedDict):
  name: str
  minimumValue: float
  maximumValue: float
  firstTimestamp: str
  lastTimestamp: str
  missingObservations: int
  type: str
  averageValue: float


class DatasetListVersion(TypedDict):
  id: str
  createdAt: str
  status: Status


class DatasetVersion(TypedDict):
  id: str
  estimatedSamplingPeriod: str
  size: int
  numberOfObservations: int
  firstTimestamp: str
  lastTimestamp: str
  variables: List[Variables]
  createdAt: str
  status: Status


class CSVSeparator(Enum):
  SEMICOLON = ';'
  TAB = ' '
  COMMA = ','


class DecimalSeparator(Enum):
  COMMA = ','
  DOT = '.'


class UploadDatasetConfiguration(TypedDict, total=False):
  timestampFormat: str
  timestampColumn: Union[str, int]
  decimalSeparator: DecimalSeparator
  csvSeparator: CSVSeparator
  name: str
  description: str
  samplingPeriod: RelativeRange
  workspace: Id


class UploadDatasetVersion(TypedDict):
  id: str


class UploadDatasetResponse(TypedDict):
  id: str
  version: UploadDatasetVersion


class UploadDatasetResultsResponse(NamedTuple):
  dataset: Optional[Dataset]
  logs: List[Logs]


class UpdateDatasetConfiguration(TypedDict, total=False):
  timestampFormat: str
  timestampColumn: Union[str, int]
  decimalSeparator: DecimalSeparator
  csvSeparator: CSVSeparator


class UpdateDatasetResponse(TypedDict):
  version: UploadDatasetVersion


class DatasetListPayload(TypedDict, total=False):
  offset: int
  limit: int
  workspaceId: str
  sort: str
