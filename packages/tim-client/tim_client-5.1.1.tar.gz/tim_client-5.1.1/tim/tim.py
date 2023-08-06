from datetime import datetime
from typing import List, Union, Callable, Optional
from tim.data_sources.anomaly_detection.anomaly_detection import get_anomaly_detection_job_status, get_anomaly_detection_jobs
from tim.data_sources.anomaly_detection import build_anomaly_detection_model, detect, rebuild_anomaly_detection_model, execute_anomaly_detection, get_anomaly_detection, get_anomaly_detection_logs, get_anomaly_detection_model_results, get_anomaly_detection_table_results, poll_anomaly_detection_status, delete_anomaly_detection
from pandas import DataFrame
from tim.core.credentials import Credentials
from tim.data_sources.forecast.types import CleanForecastResponse, ForecastJobConfiguration, ForecastJobType, ForecastMetadata, ForecastResultsResponse, BuildForecastingModelConfiguration, ForecastingPredictConfiguration, ForecastingRebuildModelConfiguration
from tim.data_sources.anomaly_detection.types import AnomalyDetectionRebuildModelConfiguration, AnomalyDetectionType, AnomalyDetectionJobConfiguration, AnomalyDetectionDetectConfiguration, AnomalyDetection, AnomalyDetectionResultsResponse, BuildAnomalyDetectionModelConfiguration
from tim.data_sources.workspace.types import Workspace
from tim.data_sources.dataset.types import Dataset, DatasetListVersion, DatasetStatusResponse, UpdateDatasetConfiguration, UpdateDatasetResponse
from tim.data_sources.dataset import get_dataset, delete_dataset, get_datasets, get_dataset_versions, get_dataset_logs, upload_dataset, update_dataset, poll_dataset_version_status, UploadDatasetResponse, UploadDatasetResultsResponse, UploadDatasetConfiguration
from tim.data_sources.forecast import build_forecasting_model, rebuild_forecasting_model, predict, execute, get_forecast, get_forecast_accuracies_result, get_forecast_logs, get_forecast_model_results, get_forecast_table_results, poll_forecast_status, get_status, delete_forecast, get_forecasting_jobs
from tim.data_sources.use_case import create_use_case, UseCaseConfiguration
from tim.data_sources.workspace import get_workspaces
from tim.types import ExecuteResponse, Status, Id, StatusResponse
from tim.endpoint import endpoint


class Tim:
  __credentials: Credentials

  def __init__(
      self,
      email: str,
      password: str,
      endpoint: str = endpoint,
      clientName: str = "Python Client",
  ):
    self.__credentials = Credentials(email, password, endpoint, clientName)

  def upload_dataset(
      self,
      dataset: DataFrame,
      configuration: UploadDatasetConfiguration = UploadDatasetConfiguration(),
      wait_to_finish: bool = True,
      handle_status_poll: Optional[Callable[[DatasetStatusResponse], None]] = None
  ) -> Union[UploadDatasetResultsResponse, UploadDatasetResponse]:
    """Upload a dataset to the TIM repository

        Parameters
        ----------
        dataset : DataFrame
        	The dataset containing time-series data
        configuration: Dict
        	Metadata of the dataset, Optional
          Available keys are: timestampFormat, timestampColumn, decimalSeparator, name, description and samplingPeriod
        	The value of samplingPeriod is a Dict containing the keys baseUnit and value
      wait_to_finish : bool, Optional
        Wait for the dataset to be uploaded before returning
        If set to False, the function will return once the dataset upload process has started
      handle_status_poll: Callable, Optional
        A callback function to poll for the status and progress of the dataset upload

        Returns
        -------
        dataset_metadata : Dict | None
        	Dict when successful; None when unsuccessful
        logs : list of Dict
        """
    upload_response = upload_dataset(self.__credentials, dataset, configuration)
    if wait_to_finish is False: return upload_response

    id = upload_response['id']

    status_result = poll_dataset_version_status(
        credentials=self.__credentials,
        id=id,
        version_id=upload_response['version']['id'],
        handle_status_poll=handle_status_poll
    )

    metadata = None
    if Status(status_result['status']).value != Status.FAILED.value:
      metadata = get_dataset(self.__credentials, id)

    logs = get_dataset_logs(self.__credentials, id)

    return UploadDatasetResultsResponse(metadata, logs)

  def update_dataset(
      self,
      dataset_id: str,
      dataset_version: DataFrame,
      configuration: UpdateDatasetConfiguration = UpdateDatasetConfiguration(),
      wait_to_finish: bool = True,
      handle_status_poll: Optional[Callable[[DatasetStatusResponse], None]] = None
  ) -> Union[UploadDatasetResultsResponse, UpdateDatasetResponse]:
    """Update a dataset in the TIM repository by uploading a new version

        Parameters
        ----------
        dataset_id: str
          The ID of the dataset to update
        dataset_version : DataFrame
        	The dataset containing time-series data
        configuration: Dict
        	Metadata of the dataset, Optional
          Available keys are: timestampFormat, timestampColumn, decimalSeparator
      wait_to_finish : bool, Optional
        Wait for the dataset version to be uploaded before returning
        If set to False, the function will return once the dataset version upload process has started
      handle_status_poll: Callable, Optional
        A callback function to poll for the status and progress of the dataset version upload

        Returns
        -------
        dataset_metadata : Dict | None
        	Dict when successful; None when unsuccessful
        logs : list of Dict
        """
    update_response = update_dataset(self.__credentials, dataset_id, dataset_version, configuration)
    if wait_to_finish is False: return update_response

    id = update_response['version']['id']

    status_result = poll_dataset_version_status(
        credentials=self.__credentials, id=dataset_id, version_id=id, handle_status_poll=handle_status_poll
    )

    metadata = None
    if Status(status_result['status']).value != Status.FAILED.value:
      metadata = get_dataset(self.__credentials, dataset_id)

    logs = get_dataset_logs(self.__credentials, dataset_id)

    return UploadDatasetResultsResponse(metadata, logs)

  def build_forecasting_model(
      self, dataset_id: str, job_configuration: Optional[BuildForecastingModelConfiguration] = None
  ) -> str:
    """Create a forecast job in the workspace the dataset is connected to (the default workspace)

    Parameters
    ----------
    dataset_id : str
        The ID of a dataset in the TIM repository
    job_configuration : BuildForecastingModelConfiguration, Optional
        TIM Engine model building and forecasting configuration, by default None
        Available keys are: name, configuration, data

    Returns
    -------
    id : str
    """
    workspace = Id(id=get_dataset(self.__credentials, dataset_id)['workspace']['id'])

    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    use_case_configuration = UseCaseConfiguration(
        name=f'Quick Forecast - {dt_string}', workspace=workspace, dataset=Id(id=dataset_id)
    )

    use_case = create_use_case(credentials=self.__credentials, configuration=use_case_configuration)
    config = ForecastJobConfiguration(
        **job_configuration, useCase=use_case
    ) if job_configuration else ForecastJobConfiguration(useCase=use_case)

    model = build_forecasting_model(credentials=self.__credentials, job_configuration=config)

    return model['id']

  def execute_forecast(
      self,
      forecast_job_id: str,
      wait_to_finish: bool = True,
      handle_status_poll: Optional[Callable[[StatusResponse], None]] = None
  ) -> Union[ForecastResultsResponse, ExecuteResponse]:
    """Execute a forecast job

    Parameters
    ----------
    forecast_job_id : str
        The ID of a forecast job to execute
    wait_to_finish : bool, Optional
        Wait for all results to be calculated before returning
        If set to False, the function will return once the job has started the execution process
    handle_status_poll: Callable, Optional
      A callback function to poll for the status and progress of the forecasting job execution

    Returns
    -------
    metadata : Dict | None
      Dict when successful; None when unsuccessful
    model_result : Dict | None
      Dict when successful; None when unsuccessful
    table_result : DataFrame | None
      DataFrame when successful; None when unsuccessful
    accuracies : Dict | None
      Dict when successful; None when unsuccessful
    logs : list of Dict
    """
    executed_response = execute(self.__credentials, forecast_job_id)
    if wait_to_finish is False: return executed_response

    poll_forecast_status(self.__credentials, forecast_job_id, handle_status_poll)
    return self.get_forecast_results(forecast_job_id)

  def build_forecasting_model_and_execute(
      self,
      dataset_id: str,
      job_configuration: Optional[BuildForecastingModelConfiguration] = None,
      wait_to_finish: bool = True,
      handle_status_poll: Optional[Callable[[StatusResponse], None]] = None
  ) -> Union[ForecastResultsResponse, ExecuteResponse]:
    """Create a forecast job in the workspace the dataset is connected to (default workspace) and execute it

    Parameters
    ----------
    dataset_id : str
      The ID of a dataset in the TIM repository
    job_configuration : BuildForecastingModelConfiguration
      TIM Engine model building and forecasting configuration
      Available keys are : name, configuration, data
    wait_to_finish : bool, Optional
      Wait for all results to be calculated before returning
      If set to False, the function will return once the job has started the execution process
    handle_status_poll: Callable, Optional
      A callback function to poll for the status and progress of the forecasting job execution

    Returns
    -------
    metadata : Dict | None
      Dict when successful; None when unsuccessful
    model_result : Dict | None
      Dict when successful; None when unsuccessful
    table_result : DataFrame | None
      DataFrame when successful; None when unsuccessful
    accuracies : Dict | None
      Dict when successful; None when unsuccessful
    logs : list of Dict
    """
    id = self.build_forecasting_model(dataset_id, job_configuration)
    return self.execute_forecast(id, wait_to_finish, handle_status_poll)

  def create_forecast(
      self, parent_job_id: str, job_configuration: Optional[ForecastingPredictConfiguration] = None
  ) -> str:
    """Create a forecasting job using the same model as the parent forecasting job

    Parameters
    ----------
    parent_job_id : str
      The ID of a parent forecasting job
    job_configuration : ForecastingPredictConfiguration
      TIM Engine forecasting configuration
      Available keys are : name, configuration, data

    Returns
    -------
    id : str
    """
    return predict(
        credentials=self.credentials, parent_job_id=parent_job_id, job_configuration=job_configuration
    )['id']

  def create_forecast_and_execute(
      self,
      parent_job_id: str,
      job_configuration: Optional[ForecastingPredictConfiguration] = None,
      wait_to_finish: bool = True,
      handle_status_poll: Optional[Callable[[StatusResponse], None]] = None
  ) -> Union[ForecastResultsResponse, ExecuteResponse]:
    """Create a forecasting job using the same model as the parent forecasting job and execute it

    Parameters
    ----------
    parent_job_id : str
        The ID of a parent forecasting job
    job_configuration : ForecastingPredictConfiguration
        TIM Engine forecasting configuration
        Available keys are : name, configuration, data
    wait_to_finish : bool, Optional
        Wait for all results to be calculated before returning
        If set to False, the function will return once the job has started the execution process
    handle_status_poll: Callable, Optional
        A callback function to poll for the status and progress of the forecasting job execution

    Returns
    -------
    metadata : Dict | None
        Dict when successful; None when unsuccessful
    model_result : Dict | None
        Dict when successful; None when unsuccessful
    table_result : DataFrame | None
        DataFrame when successful; None when unsuccessful
    accuracies : Dict | None
        Dict when successful; None when unsuccessful
    logs : list of Dict
    """
    id = self.create_forecast(parent_job_id=parent_job_id, job_configuration=job_configuration)
    return self.execute_forecast(id, wait_to_finish, handle_status_poll)

  def rebuild_forecasting_model(
      self, parent_job_id: str, job_configuration: Optional[ForecastingRebuildModelConfiguration] = None
  ) -> str:
    """Create a forecast job to rebuild the model(s) of the parent forecasting job

    Parameters
    ----------
    parent_job_id : str
        The ID of a parent forecasting job
    job_configuration : ForecastingRebuildModelConfiguration, Optional
        TIM Engine model rebuilding and forecasting configuration, by default None
        Available keys are: name, configuration, data

    Returns
    -------
    id : str
    """
    return rebuild_forecasting_model(
        credentials=self.credentials, parent_job_id=parent_job_id, job_configuration=job_configuration
    )['id']

  def rebuild_forecasting_model_and_execute(
      self,
      parent_job_id: str,
      job_configuration: Optional[ForecastingRebuildModelConfiguration] = None,
      wait_to_finish: bool = True,
      handle_status_poll: Optional[Callable[[StatusResponse], None]] = None
  ) -> Union[ForecastResultsResponse, ExecuteResponse]:
    """Create a forecast job to rebuild the model(s) of the parent forecasting job and execute it

    Parameters
    ----------
    parent_job_id : str
        The ID of a parent forecasting job
    job_configuration : ForecastingRebuildModelConfiguration, Optional
        TIM Engine model rebuilding and forecasting configuration, by default None
        Available keys are: name, configuration, data
    wait_to_finish : bool, Optional
      Wait for all results to be calculated before returning
      If set to False, the function will return once the job has started the execution process
    handle_status_poll: Callable, Optional
      A callback function to poll for the status and progress of the forecasting job execution

    Returns
    -------
    metadata : Dict | None
      Dict when successful; None when unsuccessful
    model_result : Dict | None
      Dict when successful; None when unsuccessful
    table_result : DataFrame | None
      DataFrame when successful; None when unsuccessful
    accuracies : Dict | None
      Dict when successful; None when unsuccessful
    logs : list of Dict
    """
    id = self.rebuild_forecasting_model(parent_job_id=parent_job_id, job_configuration=job_configuration)
    return self.execute_forecast(id, wait_to_finish, handle_status_poll)

  def get_forecast_results(self, forecast_job_id: str) -> ForecastResultsResponse:
    """Retrieve the results of a forecast job

    Parameters
    ----------
    forecast_job_id : str
      The ID of a forecast job

    Returns
    -------
    metadata : Dict | None
      Dict when successful; None when unsuccessful
    model_result : Dict | None
      Dict when successful; None when unsuccessful
    table_result : DataFrame | None
      Dict when successful; None when unsuccessful
    accuracies : Dict | None
      Dict when successful; None when unsuccessful
    logs : list of Dict
    """
    metadata = model_result = table_result = accuracies = None
    status = get_status(self.__credentials, forecast_job_id)
    logs = get_forecast_logs(self.__credentials, forecast_job_id)

    if Status(status['status']).value != Status.FAILED.value:
      metadata = get_forecast(self.__credentials, forecast_job_id)
      table_result = get_forecast_table_results(self.__credentials, forecast_job_id)
      accuracies = get_forecast_accuracies_result(self.__credentials, forecast_job_id)
      is_predict_job = ForecastJobType(metadata['type']).value == ForecastJobType.PREDICT.value
      job_id = metadata['parentJob']['id'] if is_predict_job else forecast_job_id
      model_result = get_forecast_model_results(self.__credentials, job_id)

    return ForecastResultsResponse(metadata, model_result, table_result, accuracies, logs)

  def delete_forecast(self, forecast_job_id: str) -> ExecuteResponse:
    """Delete a forecasting job

    Parameters
    ----------
    forecast_job_id : str
        ID of the forecasting job to delete
    Returns
    -------
    message : Dict
        Available keys: message (str) and code (str)
    """
    return delete_forecast(self.__credentials, forecast_job_id)

  def clean_forecast(
      self,
      dataset: DataFrame,
      dataset_configuration: UploadDatasetConfiguration = UploadDatasetConfiguration(),
      job_configuration: Optional[BuildForecastingModelConfiguration] = None,
      handle_dataset_upload_status_poll: Optional[Callable[[DatasetStatusResponse], None]] = None,
      handle_forecast_status_poll: Optional[Callable[[StatusResponse], None]] = None
  ) -> Union[CleanForecastResponse, ExecuteResponse]:
    """Perform a clean forecast: upload the dataset in the default workspace, create a forecast job in this workspace, execute it, return the results and delete the dataset and job from the TIM Repository

    Parameters
    ----------
    dataset : DataFrame
      The dataset containing time-series data
    dataset_configuration: Dict
      Metadata of the dataset, Optional
      Available keys are: timestampFormat, timestampColumn, decimalSeparator, name, description and samplingPeriod
      The value of samplingPeriod is a Dict containing the keys baseUnit and value
    job_configuration : BuildForecastingModelConfiguration
      TIM Engine model building and forecasting configuration
      Available keys are : name, configuration, data
    handle_dataset_upload_status_poll: Callable, Optional
      A callback function to poll for the status and progress of the dataset upload
    handle_forecast_status_poll: Callable, Optional
      A callback function to poll for the status and progress of the forecasting job execution

    Returns
    -------
    metadata : Dict | None
      Dict when successful; None when unsuccessful
    model_result : Dict | None
      Dict when successful; None when unsuccessful
    table_result : DataFrame | None
      DataFrame when successful; None when unsuccessful
    accuracies : Dict | None
      Dict when successful; None when unsuccessful
    forecasting_logs : list of Dict
    dataset_logs : list of Dict
    """
    if job_configuration and "data" in job_configuration and "dataVersion" in job_configuration["data"]:
      raise ValueError("'dataVersion' is not a valid key in in data in job_configuration for this function.")

    upload_response = self.upload_dataset(
        dataset, dataset_configuration, True, handle_dataset_upload_status_poll
    )

    if isinstance(upload_response, UploadDatasetResultsResponse):
      if upload_response.dataset:
        execute_response = self.build_forecasting_model_and_execute(
            upload_response.dataset['id'], job_configuration, True, handle_forecast_status_poll
        )
        self.delete_dataset(upload_response.dataset['id'])

        if isinstance(execute_response, ForecastResultsResponse):
          return CleanForecastResponse(
              metadata=execute_response.metadata,
              model_result=execute_response.model_result,
              table_result=execute_response.table_result,
              accuracies=execute_response.accuracies,
              forecast_logs=execute_response.logs,
              dataset_logs=upload_response.logs
          )
        raise ValueError("Internal error. Please contact support.")

      return CleanForecastResponse(
          metadata=None,
          model_result=None,
          table_result=None,
          accuracies=None,
          forecast_logs=None,
          dataset_logs=upload_response.logs
      )
    raise ValueError("Internal error. Please contact support.")

  def build_anomaly_detection_model(
      self, dataset_id: str, job_configuration: Optional[BuildAnomalyDetectionModelConfiguration] = None
  ) -> str:
    """Create an anomaly detection job in the workspace the dataset is connected to (default workspace)

    Parameters
    ----------
    dataset_id : str
      The ID of a dataset in the TIM repository
    job_configuration : BuildAnomalyDetectionModelConfiguration
      TIM Engine model building and anomaly detection configuration
      Available keys are : name, configuration, data

    Returns
    -------
    id : str
    """
    workspace = Id(id=get_dataset(self.__credentials, dataset_id)['workspace']['id'])

    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    use_case_configuration = UseCaseConfiguration(
        name=f'Quick Anomaly Detection - {dt_string}', workspace=workspace, dataset=Id(id=dataset_id)
    )

    use_case = create_use_case(credentials=self.__credentials, configuration=use_case_configuration)
    config = AnomalyDetectionJobConfiguration(
        **job_configuration, useCase=use_case
    ) if job_configuration else AnomalyDetectionJobConfiguration(useCase=use_case)

    model = build_anomaly_detection_model(credentials=self.__credentials, job_configuration=config)

    return model['id']

  def execute_anomaly_detection(
      self,
      anomaly_detection_job_id: str,
      wait_to_finish: bool = True,
      handle_status_poll: Optional[Callable[[StatusResponse], None]] = None
  ) -> Union[AnomalyDetectionResultsResponse, ExecuteResponse]:
    """Execute an anomaly detection job

    Parameters
    ----------
    anomaly_detection_job_id : str
        The ID of an anomaly detection job to execute
    wait_to_finish : bool, Optional
        Wait for all results to be calculated before returning
        If set to False, the function will return once the job has started the execution process
    handle_status_poll: Callable, Optional
      A callback function to poll for the status and progress of the anomaly detection job execution

    Returns
    -------
    metadata : Dict | None
      Dict when successful; None when unsuccessful
    model_result : Dict | None
      Dict when successful; None when unsuccessful
    table_result : DataFrame | None
      DataFrame when successful; None when unsuccessful
    logs : list of Dict
    """
    executed_response = execute_anomaly_detection(self.__credentials, anomaly_detection_job_id)
    if wait_to_finish is False: return executed_response

    poll_anomaly_detection_status(self.__credentials, anomaly_detection_job_id, handle_status_poll)
    return self.get_anomaly_detection_results(anomaly_detection_job_id)

  def build_anomaly_detection_model_and_execute(
      self,
      dataset_id: str,
      job_configuration: Optional[BuildAnomalyDetectionModelConfiguration] = None,
      wait_to_finish: bool = True,
      handle_status_poll: Optional[Callable[[StatusResponse], None]] = None
  ) -> Union[AnomalyDetectionResultsResponse, ExecuteResponse]:
    """Create an anomaly detection job in the workspace the dataset is connected to (default workspace) and execute it

    Parameters
    ----------
    dataset_id : str
      The ID of a dataset in the TIM repository
    job_configuration : BuildAnomalyDetectionModelConfiguration
      TIM Engine model building and anomaly detection configuration
      Available keys are : name, configuration, data
    wait_to_finish : bool, Optional
      Wait for all results to be calculated before returning
      If set to False, the function will return once the job has started the execution process
    handle_status_poll: Callable, Optional
      A callback function to poll for the status and progress of the anomaly detection job execution

    Returns
    -------
    metadata : Dict | None
      Dict when successful; None when unsuccessful
    model_result : Dict | None
      Dict when successful; None when unsuccessful
    table_result : DataFrame | None
      DataFrame when successful; None when unsuccessful
    logs : list of Dict
    """
    id = self.build_anomaly_detection_model(dataset_id, job_configuration)
    return self.execute_anomaly_detection(id, wait_to_finish, handle_status_poll)

  def create_anomaly_detection(
      self, parent_job_id: str, job_configuration: Optional[AnomalyDetectionDetectConfiguration] = None
  ) -> str:
    """Create an anomaly detection job using the same model as the parent anomaly detection job

    Parameters
    ----------
    parent_job_id : str
      The ID of a parent anomaly detection job
    job_configuration : AnomalyDetectionDetectConfiguration
      TIM Engine anomaly detection configuration
      Available keys are : name, data

    Returns
    -------
    id : str
    """
    return detect(
        credentials=self.credentials, parent_job_id=parent_job_id, job_configuration=job_configuration
    )['id']

  def create_anomaly_detection_and_execute(
      self,
      parent_job_id: str,
      job_configuration: Optional[AnomalyDetectionDetectConfiguration] = None,
      wait_to_finish: bool = True,
      handle_status_poll: Optional[Callable[[StatusResponse], None]] = None
  ) -> Union[AnomalyDetectionResultsResponse, ExecuteResponse]:
    """Create an anomaly detection job using the same model as the parent anomaly detection job and execute it

    Parameters
    ----------
    parent_job_id : str
      The ID of a parent anomaly detection job
    job_configuration : AnomalyDetectionDetectConfiguration
      TIM Engine anomaly detection configuration
      Available keys are : name, data
    wait_to_finish : bool, Optional
      Wait for all results to be calculated before returning
      If set to False, the function will return once the job has started the execution process
    handle_status_poll: Callable, Optional
      A callback function to poll for the status and progress of the anomaly detection job execution

    Returns
    -------
    metadata : Dict | None
      Dict when successful; None when unsuccessful
    model_result : Dict | None
      Dict when successful; None when unsuccessful
    table_result : DataFrame | None
      DataFrame when successful; None when unsuccessful
    logs : list of Dict
    """
    id = self.create_anomaly_detection(parent_job_id=parent_job_id, job_configuration=job_configuration)
    return self.execute_anomaly_detection(id, wait_to_finish, handle_status_poll)

  def rebuild_anomaly_detection_model(
      self, parent_job_id: str, job_configuration: Optional[AnomalyDetectionRebuildModelConfiguration] = None
  ) -> str:
    """Create an anomaly detection job to rebuild the model(s) of the parent anomaly detection job

    Parameters
    ----------
    parent_job_id : str
        The ID of a parent anomaly detection job
    job_configuration : AnomalyDetectionRebuildModelConfiguration, Optional
        TIM Engine model rebuilding and detection configuration, by default None
        Available keys are: name, configuration, data

    Returns
    -------
    id : str
    """
    return rebuild_anomaly_detection_model(
        credentials=self.credentials, parent_job_id=parent_job_id, job_configuration=job_configuration
    )['id']

  def rebuild_anomaly_detection_model_and_execute(
      self,
      parent_job_id: str,
      job_configuration: Optional[AnomalyDetectionRebuildModelConfiguration] = None,
      wait_to_finish: bool = True,
      handle_status_poll: Optional[Callable[[StatusResponse], None]] = None
  ) -> Union[AnomalyDetectionResultsResponse, ExecuteResponse]:
    """Create an anomaly detection job to rebuild the model(s) of the parent anomaly detection job and execute it

    Parameters
    ----------
    parent_job_id : str
        The ID of a parent anomaly detection job
    job_configuration : AnomalyDetectionRebuildModelConfiguration, Optional
        TIM Engine model rebuilding and anomaly detection configuration, by default None
        Available keys are: name, configuration, data
    wait_to_finish : bool, Optional
      Wait for all results to be calculated before returning
      If set to False, the function will return once the job has started the execution process
    handle_status_poll: Callable, Optional
      A callback function to poll for the status and progress of the anomaly detection job execution

    Returns
    -------
    metadata : Dict | None
      Dict when successful; None when unsuccessful
    model_result : Dict | None
      Dict when successful; None when unsuccessful
    table_result : DataFrame | None
      DataFrame when successful; None when unsuccessful
    logs : list of Dict
    """
    id = self.rebuild_anomaly_detection_model(
        parent_job_id=parent_job_id, job_configuration=job_configuration
    )
    return self.execute_anomaly_detection(id, wait_to_finish, handle_status_poll)

  def get_anomaly_detection_results(self, anomaly_detection_job_id: str) -> AnomalyDetectionResultsResponse:
    """Retrieve the results of an anomaly detection job

    Parameters
    ----------
    anomaly_detection_job_id : str
        The ID of an anomaly detection job

    Returns
    -------
    metadata : Dict | None
      Dict when successful; None when unsuccessful
    model_result : Dict | None
      Dict when successful; None when unsuccessful
    table_result : DataFrame | None
      Dict when successful; None when unsuccessful
    logs : list of Dict
    """
    metadata = model_result = table_result = None
    status = get_anomaly_detection_job_status(self.__credentials, anomaly_detection_job_id)
    logs = get_anomaly_detection_logs(self.__credentials, anomaly_detection_job_id)

    if Status(status['status']).value != Status.FAILED.value:
      metadata = get_anomaly_detection(self.__credentials, anomaly_detection_job_id)
      table_result = get_anomaly_detection_table_results(self.__credentials, anomaly_detection_job_id)
      is_detect_job = AnomalyDetectionType(metadata['type']).value == AnomalyDetectionType.DETECT.value
      job_id = metadata['parentJob']['id'] if is_detect_job else anomaly_detection_job_id
      model_result = get_anomaly_detection_model_results(self.__credentials, job_id)

    return AnomalyDetectionResultsResponse(metadata, model_result, table_result, logs)

  def delete_anomaly_detection(self, anomaly_detection_job_id: str) -> ExecuteResponse:
    """Delete an anomaly detection job

    Parameters
    ----------
    anomaly_detection_job_id : str
        ID of the anomaly detection job to delete
    Returns
    -------
    message : Dict
        Available keys: message (str) and code (str)
    """
    return delete_anomaly_detection(self.__credentials, anomaly_detection_job_id)

  def get_workspaces(
      self,
      offset: int = 0,
      limit: int = 10000,
      user_group_id: Optional[str] = None,
      sort: Optional[str] = None
  ) -> List[Workspace]:
    """Get a list of workspaces and their metadata

    Parameters
    ----------
    offset : int, optional
        Number of records to be skipped from beginning of the list, by default 0
    limit : int, optional
        Maximum number of records to be returned, by default 10000
    user_group_id : Optional[str], optional
        User Group ID, by default None
    sort : Optional[str], optional
        Sorting output by the chosen attribute. +/- indicates ascending/descending order, by default -createdAt
        Available values : +createdAt, -createdAt, +updatedAt, -updatedAt, +title, -title

    Returns
    -------
    workspaces : list of Dict
        Available keys for each list item (workspace) : id (str), name (str), description (str), userGroup (Dict) with id (str), isFavorite (bool), createdAt (str), createdBy (str), updatedAt (str), updatedBy (str)
    """
    return get_workspaces(self.__credentials, offset, limit, user_group_id, sort)

  def delete_dataset(self, dataset_id: str) -> ExecuteResponse:
    """Delete a dataset

    Parameters
    ----------
    dataset_id : str
        ID of the dataset to delete
    Returns
    -------
    message : Dict
        Available keys: message (str) and code (str)
    """
    return delete_dataset(self.__credentials, dataset_id)

  def get_datasets(
      self,
      offset: int = 0,
      limit: int = 10000,
      workspace_id: Optional[str] = None,
      sort: Optional[str] = None
  ) -> List[Dataset]:
    """Get a list of datasets and their metadata

    Parameters
    ----------
    offset : int, optional
        Number of records to be skipped from beginning of the list, by default 0
    limit : int, optional
        Maximum number of records to be returned, by default 10000
    workspace_id : Optional[str] = None
        Filter for specific Workspace, by default None
    sort : Optional[str] = None
        Sorting output by the chosen attribute. +/- indicates ascending/descending order.
        Available values : +createdAt, -createdAt

    Returns
    -------
    datasets : list of Dict
        Available keys for each list item (dataset) : id (str), name (str), workspace (Dict), latestVersion (Dict), description (str), isFavorite (bool), estimatedSamplingPeriod (str), createdAt (str), createdBy (str), updatedAt (str), updatedBy (str)
        Available keys for workspace are : id (str), name (str)
        Available keys for latestVersion are : id (str), status, numberOfVariables (int), numberOfObservations (int), firstTimestamp (str), lastTimestamp (str)
        Available values for status are : Registered, Running, Finished, FinishedWithWarning, Failed, Queued
    """
    return get_datasets(self.__credentials, offset, limit, workspace_id, sort)

  def get_dataset_versions(
      self,
      id: str,
      offset: int = 0,
      limit: int = 10000,
  ) -> List[DatasetListVersion]:
    """Get a list of the versions of a dataset and their metadata

    Parameters
    ----------
    id : str
        Dataset ID
    offset : int, optional
        Number of records to be skipped from beggining of the list, by default 0
    limit : int, optional
        Maximum number of records to be returned, by default 10000

    Returns
    -------
    versions : list of Dict
        Available keys for each list item (version) : id (str), createdAt (str), status
        Available values for status are : Registered, Running, Finished, FinishedWithWarning, Failed, Queued
    """
    return get_dataset_versions(self.__credentials, id, offset, limit)

  def get_anomaly_detection_jobs(
      self,
      offset: Optional[int] = None,
      limit: Optional[int] = None,
      sort: str = '-createdAt',
      experiment_id: Optional[str] = None,
      use_case_id: Optional[str] = None,
      type: Optional[str] = None,
      status: Optional[str] = None,
      parent_id: Optional[str] = None,
      from_datetime: Optional[str] = None,
      to_datetime: Optional[str] = None
  ) -> List[AnomalyDetection]:
    """Get a list of all anomaly detection jobs and their metadata

    Parameters
    ----------
    offset : int, optional
        Number of records to be skipped from beginning of the list, by default 0
    limit : int, optional
        Maximum number of records to be returned, by default 100
    sort : str, optional
        Sorting output by the chosen attribute. +/- indicates ascending/descending order, by default '-createdAt'
        Available values : +createdAt, -createdAt, +executedAt, -executedAt, +completedAt, -completedAt, +priority, -priority
    experiment_id : Optional[str], optional
        Filter for a specific Experiment, by default None
    use_case_id : Optional[str], optional
        Filter for a specific Use Case, by default None
    type : Optional[str], optional
        Filter for specific types (comma separated string), by default None
        Available values : build-model, rebuild-model, detect, rca
    status : Optional[str], optional
        Filter for specific job statuses (comma separated string), by default None
        Available values : Registered, Queued, Running, Finished, FinishedWithWarning, Failed
    parent_id : Optional[str], optional
        Filter for a specific parent job, by default None
    from_datetime : Optional[str], optional
        Filter for a minimal date and time of job creation, by default None
    to_datetime : Optional[str], optional
        Filter for a maximal date and time of job creation, by default None

    Returns
    -------
    jobs : list of Dict
        Available keys for each list item (job) are : id (str), name (str), type (str), status (str), parentJob (Dict), useCase (Dict), experiment (Dict), dataset (Dict), createdAt (str), completedAt (str), executedAt (str), workerVersion (float), registrationBody (Dict)
        Available keys for registrationBody are : name (str), useCase (Dict), data (Dict), configuration (Dict)
        Available keys for useCase are : id (str)
        Available keys for experiment are: id (str)
        Available keys for dataset are : version (Dict) containing id (str)
        Available keys for registrationBody are : data (Dict) and configuration (Dict)
        Available keys for errorMeasures are : bin (Dict), samplesAhead (Dict), all (Dict)
    """
    return get_anomaly_detection_jobs(
        self.__credentials, offset, limit, sort, experiment_id, use_case_id, type, status, parent_id,
        from_datetime, to_datetime
    )

  def get_forecasting_jobs(
      self,
      offset: Optional[int] = None,
      limit: Optional[int] = None,
      sort: Optional[str] = None,
      experiment_id: Optional[str] = None,
      use_case_id: Optional[str] = None,
      type: Optional[str] = None,
      status: Optional[str] = None,
      parent_id: Optional[str] = None,
      from_datetime: Optional[str] = None,
      to_datetime: Optional[str] = None
  ) -> List[ForecastMetadata]:
    """Get a list of all forecasting jobs and their metadata

    Parameters
    ----------
    offset : int, optional
        Number of records to be skipped from beggining of the list, by default 0
    limit : int, optional
        Maximum number of records to be returned, by default 10000
    sort : str, optional
        Sorting output by the chosen attribute. +/- indicates ascending/descending order, by default '-createdAt'
        Available values : +createdAt, -createdAt, +executedAt, -executedAt, +completedAt, -completedAt, +priority, -priority
    experiment_id : Optional[str], optional
        Filter for a specific Experiment, by default None
    use_case_id : Optional[str], optional
        Filter for a specific Use Case, by default None
    type : Optional[str], optional
        Filter for specific types (comma separated string), by default None
        Available values : build-model, rebuild-model, predict, rca
    status : Optional[str], optional
        Filter for specific job statuses (comma separated string), by default None
        Available values : Registered, Queued, Running, Finished, FinishedWithWarning, Failed
    parent_id : Optional[str], optional
        Filter for a specific parent job, by default None
    from_datetime : Optional[str], optional
        Filter for a minimal date and time of job creation, by default None
    to_datetime : Optional[str], optional
        Filter for a maximal date and time of job creation, by default None

    Returns
    -------
    jobs : list of Dict
        Available keys for each list item (job) are : id (str), name (str), type (str), status (str), parentJob (Dict), useCase (Dict), experiment (Dict), dataset (Dict), createdAt (str), completedAt (str), executedAt (str), workerVersion (float), jobLoad (str), registrationBody (Dict), errorMeasures (Dict)
        Available keys for useCase are : id (str)
        Available keys for experiment are: id (str)
        Available keys for dataset are : version (Dict) containing id (str)
        Available keys for registrationBody are : data (Dict) and configuration (Dict)
        Available keys for errorMeasures are : bin (Dict), samplesAhead (Dict), all (Dict)
    """
    return get_forecasting_jobs(
        self.__credentials, offset, limit, sort, experiment_id, use_case_id, type, status, parent_id,
        from_datetime, to_datetime
    )

  @property
  def credentials(self):
    return self.__credentials
