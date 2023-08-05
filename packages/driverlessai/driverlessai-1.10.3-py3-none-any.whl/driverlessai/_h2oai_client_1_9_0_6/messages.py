from .patch_utils import *
# -----------------------------------------------------------------------
#             *** WARNING: DO NOT MODIFY THIS FILE ***
#
#         Instead, modify h2oai/service.proto and run "make proto".
# -----------------------------------------------------------------------

from typing import List, Any

from . import validation
from .references import *

class EchoStatus:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, message) -> None:
        self.progress = progress
        self.message = message

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'EchoStatus':
        return EchoStatus(self.progress, self.message)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'EchoStatus':
        return EchoStatus(**d)


class License:
    """
    Represents a license key.

    :param is_valid: Is this license valid?
    :param message: License message.
    :param days_left: Days left before license expires.
    :param plaintext_key: License key.
    :param save_succeeded: Whether the license was applied successfully.
    :param organization: Organization that obtained the license
    :param serial_number: Serial number of the license
    :param license_type: License type ("developer", "trial", "academic", "pilot", "production", "cloud").
    """
    @ignore_unexpected_kwargs
    def __init__(self, is_valid, message, days_left, plaintext_key, save_succeeded, organization, serial_number, license_type) -> None:
        self.is_valid = is_valid
        self.message = message
        self.days_left = days_left
        self.plaintext_key = plaintext_key
        self.save_succeeded = save_succeeded
        self.organization = organization
        self.serial_number = serial_number
        self.license_type = license_type

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'License':
        return License(self.is_valid, self.message, self.days_left, self.plaintext_key, self.save_succeeded, self.organization, self.serial_number, self.license_type)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'License':
        return License(**d)


class AppVersion:
    """
    The application version

    :param arch: Machine's architecture type.
    :param version: The application version (semver).
    :param build: The application build number.
    :param license: The license associated with this instance.
    :param config: List of expert configurable options for experiments
    :param mliConfig: List of configurable options for MLI
    :param enable_storage: Whether GUI should have H2O remote storage capabilities (https://github.com/h2oai/h2oai-storage) for dataset import/export
    :param enable_storage_projects: Whether GUI uses remote projects loaded from H2O Storage
    """
    @ignore_unexpected_kwargs
    def __init__(self, arch, version, build, license, config, mliConfig, enable_storage, enable_storage_projects) -> None:
        self.arch = arch
        self.version = version
        self.build = build
        self.license = license
        self.config = config
        self.mliConfig = mliConfig
        self.enable_storage = enable_storage
        self.enable_storage_projects = enable_storage_projects

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['license'] = self.license.dump()
        d['config'] = [a.dump() for a in self.config]
        d['mliConfig'] = [a.dump() for a in self.mliConfig]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'AppVersion':
        return AppVersion(self.arch, self.version, self.build, self.license, self.config, self.mliConfig, self.enable_storage, self.enable_storage_projects)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'AppVersion':
        d['license'] = License.load(d['license'])
        d['config'] = [ConfigItem.load(a) for a in d['config']]
        d['mliConfig'] = [ConfigItem.load(a) for a in d['mliConfig']]
        return AppVersion(**d)


class ListInterpretationQueryResponse:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, items, offset, limit, total_count) -> None:
        self.items = items
        self.offset = offset
        self.limit = limit
        self.total_count = total_count

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['items'] = [a.dump() for a in self.items]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ListInterpretationQueryResponse':
        return ListInterpretationQueryResponse(self.items, self.offset, self.limit, self.total_count)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ListInterpretationQueryResponse':
        d['items'] = [InterpretSummary.load(a) for a in d['items']]
        return ListInterpretationQueryResponse(**d)


class ListVisualizationQueryResponse:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, items, offset, limit, total_count) -> None:
        self.items = items
        self.offset = offset
        self.limit = limit
        self.total_count = total_count

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['items'] = [a.dump() for a in self.items]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ListVisualizationQueryResponse':
        return ListVisualizationQueryResponse(self.items, self.offset, self.limit, self.total_count)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ListVisualizationQueryResponse':
        d['items'] = [AutoVizSummary.load(a) for a in d['items']]
        return ListVisualizationQueryResponse(**d)


class JobStatus:
    """
    Generic job status object. It is meant to represent status of an async job, either directly for async jobs with
    no response payload or to be embedded in other jobs along with their normal response payload.

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, created) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'JobStatus':
        return JobStatus(self.progress, self.status, self.error, self.message, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'JobStatus':
        return JobStatus(**d)


class OAuth2ClientTokens:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, status, access_token, refresh_token, client_id, error, token_endpoint_url, token_introspection_url) -> None:
        self.status = status
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.client_id = client_id
        self.error = error
        self.token_endpoint_url = token_endpoint_url
        self.token_introspection_url = token_introspection_url

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'OAuth2ClientTokens':
        return OAuth2ClientTokens(self.status, self.access_token, self.refresh_token, self.client_id, self.error, self.token_endpoint_url, self.token_introspection_url)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'OAuth2ClientTokens':
        return OAuth2ClientTokens(**d)


class ExportEntityJob:
    """

    :param id: On success, holds the new ID of the exported entity in h2ai-storage.
    """
    @ignore_unexpected_kwargs
    def __init__(self, status, id) -> None:
        self.status = status
        self.id = id

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['status'] = self.status.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ExportEntityJob':
        return ExportEntityJob(self.status, self.id)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ExportEntityJob':
        d['status'] = JobStatus.load(d['status'])
        return ExportEntityJob(**d)


class ImportEntityJob:
    """

    :param key: On success, holds the key of the new local entity representing the imported one.
    """
    @ignore_unexpected_kwargs
    def __init__(self, status, key) -> None:
        self.status = status
        self.key = key

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['status'] = self.status.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ImportEntityJob':
        return ImportEntityJob(self.status, self.key)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ImportEntityJob':
        d['status'] = JobStatus.load(d['status'])
        return ImportEntityJob(**d)


class Sharing:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, id, entity_id, user_id, group_id, restriction_role_id, type) -> None:
        self.id = id
        self.entity_id = entity_id
        self.user_id = user_id
        self.group_id = group_id
        self.restriction_role_id = restriction_role_id
        self.type = type

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'Sharing':
        return Sharing(self.id, self.entity_id, self.user_id, self.group_id, self.restriction_role_id, self.type)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'Sharing':
        return Sharing(**d)


class Role:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, id, display_name) -> None:
        self.id = id
        self.display_name = display_name

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'Role':
        return Role(self.id, self.display_name)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'Role':
        return Role(**d)


class StorageUser:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, id, username) -> None:
        self.id = id
        self.username = username

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'StorageUser':
        return StorageUser(self.id, self.username)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'StorageUser':
        return StorageUser(**d)


class ExperimentScore:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, score, score_sd, roc, gains, act_vs_pred, residual_plot) -> None:
        self.score = score
        self.score_sd = score_sd
        self.roc = roc
        self.gains = gains
        self.act_vs_pred = act_vs_pred
        self.residual_plot = residual_plot

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['roc'] = self.roc.dump()
        d['gains'] = self.gains.dump()
        d['act_vs_pred'] = self.act_vs_pred.dump()
        d['residual_plot'] = self.residual_plot.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ExperimentScore':
        return ExperimentScore(self.score, self.score_sd, self.roc, self.gains, self.act_vs_pred, self.residual_plot)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ExperimentScore':
        d['roc'] = ROC.load(d['roc'])
        d['gains'] = GainLift.load(d['gains'])
        d['act_vs_pred'] = H2OPlot.load(d['act_vs_pred'])
        d['residual_plot'] = H2OPlot.load(d['residual_plot'])
        return ExperimentScore(**d)


class KdbCreateDatasetArgs:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, dst, query) -> None:
        self.dst = dst
        self.query = query

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'KdbCreateDatasetArgs':
        return KdbCreateDatasetArgs(self.dst, self.query)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'KdbCreateDatasetArgs':
        return KdbCreateDatasetArgs(**d)


class SparkJDBCConfig:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, options, url, classpath, jarpath, database) -> None:
        self.options = options
        self.url = url
        self.classpath = classpath
        self.jarpath = jarpath
        self.database = database

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'SparkJDBCConfig':
        return SparkJDBCConfig(self.options, self.url, self.classpath, self.jarpath, self.database)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'SparkJDBCConfig':
        return SparkJDBCConfig(**d)


class JdbcCreateDatasetArgs:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, dst, query, id_column, jdbc_user, password, url, classpath, jarpath, database) -> None:
        self.dst = dst
        self.query = query
        self.id_column = id_column
        self.jdbc_user = jdbc_user
        self.password = password
        self.url = url
        self.classpath = classpath
        self.jarpath = jarpath
        self.database = database

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'JdbcCreateDatasetArgs':
        return JdbcCreateDatasetArgs(self.dst, self.query, self.id_column, self.jdbc_user, self.password, self.url, self.classpath, self.jarpath, self.database)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'JdbcCreateDatasetArgs':
        return JdbcCreateDatasetArgs(**d)


class HiveCreateDatasetArgs:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, dst, query, hive_conf_path, keytab_path, auth_type, principal_user, database) -> None:
        self.dst = dst
        self.query = query
        self.hive_conf_path = hive_conf_path
        self.keytab_path = keytab_path
        self.auth_type = auth_type
        self.principal_user = principal_user
        self.database = database

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'HiveCreateDatasetArgs':
        return HiveCreateDatasetArgs(self.dst, self.query, self.hive_conf_path, self.keytab_path, self.auth_type, self.principal_user, self.database)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'HiveCreateDatasetArgs':
        return HiveCreateDatasetArgs(**d)


class HiveConfig:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, options, hive_conf_path, keytab_path, auth_type, principal_user, database) -> None:
        self.options = options
        self.hive_conf_path = hive_conf_path
        self.keytab_path = keytab_path
        self.auth_type = auth_type
        self.principal_user = principal_user
        self.database = database

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'HiveConfig':
        return HiveConfig(self.options, self.hive_conf_path, self.keytab_path, self.auth_type, self.principal_user, self.database)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'HiveConfig':
        return HiveConfig(**d)


class GbqCreateDatasetArgs:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, dataset_id, bucket_name, dst, query) -> None:
        self.dataset_id = dataset_id
        self.bucket_name = bucket_name
        self.dst = dst
        self.query = query

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'GbqCreateDatasetArgs':
        return GbqCreateDatasetArgs(self.dataset_id, self.bucket_name, self.dst, self.query)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'GbqCreateDatasetArgs':
        return GbqCreateDatasetArgs(**d)


class SnowCreateDatasetArgs:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, region, database, warehouse, schema, role, dst, query, optional_formatting, sf_user, password) -> None:
        self.region = region
        self.database = database
        self.warehouse = warehouse
        self.schema = schema
        self.role = role
        self.dst = dst
        self.query = query
        self.optional_formatting = optional_formatting
        self.sf_user = sf_user
        self.password = password

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'SnowCreateDatasetArgs':
        return SnowCreateDatasetArgs(self.region, self.database, self.warehouse, self.schema, self.role, self.dst, self.query, self.optional_formatting, self.sf_user, self.password)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'SnowCreateDatasetArgs':
        return SnowCreateDatasetArgs(**d)


class ConnectorProperties:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, type, title_text, input_boxes) -> None:
        self.type = type
        self.title_text = title_text
        self.input_boxes = input_boxes

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['input_boxes'] = [a.dump() for a in self.input_boxes]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ConnectorProperties':
        return ConnectorProperties(self.type, self.title_text, self.input_boxes)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ConnectorProperties':
        d['input_boxes'] = [InputBoxProperties.load(a) for a in d['input_boxes']]
        return ConnectorProperties(**d)


class InputBoxProperties:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, type, required, is_password, label_title, placeholder_text, name) -> None:
        self.type = type
        self.required = required
        self.is_password = is_password
        self.label_title = label_title
        self.placeholder_text = placeholder_text
        self.name = name

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'InputBoxProperties':
        return InputBoxProperties(self.type, self.required, self.is_password, self.label_title, self.placeholder_text, self.name)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'InputBoxProperties':
        return InputBoxProperties(**d)


class H2OVisAggregation:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, aggregated_frame, mapping_frame) -> None:
        self.aggregated_frame = aggregated_frame
        self.mapping_frame = mapping_frame

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'H2OVisAggregation':
        return H2OVisAggregation(self.aggregated_frame, self.mapping_frame)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'H2OVisAggregation':
        return H2OVisAggregation(**d)


class H2OVisStats:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, number_of_columns, number_of_rows, column_names, column_is_categorical) -> None:
        self.number_of_columns = number_of_columns
        self.number_of_rows = number_of_rows
        self.column_names = column_names
        self.column_is_categorical = column_is_categorical

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'H2OVisStats':
        return H2OVisStats(self.number_of_columns, self.number_of_rows, self.column_names, self.column_is_categorical)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'H2OVisStats':
        return H2OVisStats(**d)


class H2OParallelCoordinatesPlot:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, variable_names, profiles, counts, is_categorical, cluster_indices, data_min_max) -> None:
        self.variable_names = variable_names
        self.profiles = profiles
        self.counts = counts
        self.is_categorical = is_categorical
        self.cluster_indices = cluster_indices
        self.data_min_max = data_min_max

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'H2OParallelCoordinatesPlot':
        return H2OParallelCoordinatesPlot(self.variable_names, self.profiles, self.counts, self.is_categorical, self.cluster_indices, self.data_min_max)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'H2OParallelCoordinatesPlot':
        return H2OParallelCoordinatesPlot(**d)


class H2OHeatMap:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, column_names, columns, number_of_columns, number_of_rows, counts) -> None:
        self.column_names = column_names
        self.columns = columns
        self.number_of_columns = number_of_columns
        self.number_of_rows = number_of_rows
        self.counts = counts

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'H2OHeatMap':
        return H2OHeatMap(self.column_names, self.columns, self.number_of_columns, self.number_of_rows, self.counts)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'H2OHeatMap':
        return H2OHeatMap(**d)


class NoGroupVariable:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, upper_hinge, median, lower_hinge, extreme_outliers, outliers, lower_adjacent_value, upper_adjacent_value) -> None:
        self.upper_hinge = upper_hinge
        self.median = median
        self.lower_hinge = lower_hinge
        self.extreme_outliers = extreme_outliers
        self.outliers = outliers
        self.lower_adjacent_value = lower_adjacent_value
        self.upper_adjacent_value = upper_adjacent_value

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'NoGroupVariable':
        return NoGroupVariable(self.upper_hinge, self.median, self.lower_hinge, self.extreme_outliers, self.outliers, self.lower_adjacent_value, self.upper_adjacent_value)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'NoGroupVariable':
        return NoGroupVariable(**d)


class H2OBoxplotEnvelope:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, no_group_variable) -> None:
        self.no_group_variable = no_group_variable

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['no_group_variable'] = self.no_group_variable.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'H2OBoxplotEnvelope':
        return H2OBoxplotEnvelope(self.no_group_variable)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'H2OBoxplotEnvelope':
        d['no_group_variable'] = NoGroupVariable.load(d['no_group_variable'])
        return H2OBoxplotEnvelope(**d)


class H2OBoxplot:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, boxplots, variable_name) -> None:
        self.boxplots = boxplots
        self.variable_name = variable_name

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'H2OBoxplot':
        return H2OBoxplot(self.boxplots, self.variable_name)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'H2OBoxplot':
        return H2OBoxplot(**d)


class Histogram:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, counts, variable_name, number_of_bars, number_of_ticks, scale_max, scale_min) -> None:
        self.counts = counts
        self.variable_name = variable_name
        self.number_of_bars = number_of_bars
        self.number_of_ticks = number_of_ticks
        self.scale_max = scale_max
        self.scale_min = scale_min

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'Histogram':
        return Histogram(self.counts, self.variable_name, self.number_of_bars, self.number_of_ticks, self.scale_max, self.scale_min)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'Histogram':
        return Histogram(**d)


class H2OHistobar:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, variable_name, bins, counts) -> None:
        self.variable_name = variable_name
        self.bins = bins
        self.counts = counts

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'H2OHistobar':
        return H2OHistobar(self.variable_name, self.bins, self.counts)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'H2OHistobar':
        return H2OHistobar(**d)


class H2OTimeSeriesPlot:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, x_variable_name, x_values, y_variable_name, y_values, subtype) -> None:
        self.x_variable_name = x_variable_name
        self.x_values = x_values
        self.y_variable_name = y_variable_name
        self.y_values = y_values
        self.subtype = subtype

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'H2OTimeSeriesPlot':
        return H2OTimeSeriesPlot(self.x_variable_name, self.x_values, self.y_variable_name, self.y_values, self.subtype)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'H2OTimeSeriesPlot':
        return H2OTimeSeriesPlot(**d)


class H2OScale:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, scale_min, scale_max, number_of_ticks) -> None:
        self.scale_min = scale_min
        self.scale_max = scale_max
        self.number_of_ticks = number_of_ticks

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'H2OScale':
        return H2OScale(self.scale_min, self.scale_max, self.number_of_ticks)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'H2OScale':
        return H2OScale(**d)


class H2OOutliers:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, row_indices) -> None:
        self.row_indices = row_indices

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'H2OOutliers':
        return H2OOutliers(self.row_indices)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'H2OOutliers':
        return H2OOutliers(**d)


class H2OPlot:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, x_variable_name, x_values, y_variable_name, y_values, counts) -> None:
        self.x_variable_name = x_variable_name
        self.x_values = x_values
        self.y_variable_name = y_variable_name
        self.y_values = y_values
        self.counts = counts

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'H2OPlot':
        return H2OPlot(self.x_variable_name, self.x_values, self.y_variable_name, self.y_values, self.counts)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'H2OPlot':
        return H2OPlot(**d)


class H2ODotplot:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, stacks, variable_name, x_values, scale_min, scale_max, histogram, outliers) -> None:
        self.stacks = stacks
        self.variable_name = variable_name
        self.x_values = x_values
        self.scale_min = scale_min
        self.scale_max = scale_max
        self.histogram = histogram
        self.outliers = outliers

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['histogram'] = self.histogram.dump()
        d['outliers'] = self.outliers.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'H2ODotplot':
        return H2ODotplot(self.stacks, self.variable_name, self.x_values, self.scale_min, self.scale_max, self.histogram, self.outliers)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'H2ODotplot':
        d['histogram'] = Histogram.load(d['histogram'])
        d['outliers'] = H2OOutliers.load(d['outliers'])
        return H2ODotplot(**d)


class H2ONetwork:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, edges, edge_weights, nodes) -> None:
        self.edges = edges
        self.edge_weights = edge_weights
        self.nodes = nodes

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'H2ONetwork':
        return H2ONetwork(self.edges, self.edge_weights, self.nodes)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'H2ONetwork':
        return H2ONetwork(**d)


class H2OBarchart:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, x_values, y_values, x_variable_name, y_variable_name, group_variable_name) -> None:
        self.x_values = x_values
        self.y_values = y_values
        self.x_variable_name = x_variable_name
        self.y_variable_name = y_variable_name
        self.group_variable_name = group_variable_name

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'H2OBarchart':
        return H2OBarchart(self.x_values, self.y_values, self.x_variable_name, self.y_variable_name, self.group_variable_name)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'H2OBarchart':
        return H2OBarchart(**d)


class H2ORegression:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, x_variable_name, x_values, y_variable_name, y_values, predicted_values) -> None:
        self.x_variable_name = x_variable_name
        self.x_values = x_values
        self.y_variable_name = y_variable_name
        self.y_values = y_values
        self.predicted_values = predicted_values

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'H2ORegression':
        return H2ORegression(self.x_variable_name, self.x_values, self.y_variable_name, self.y_values, self.predicted_values)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'H2ORegression':
        return H2ORegression(**d)


class H2OTimeSeriesPlot:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, subtype, x_variable_name, y_variable_name, x_values, y_values) -> None:
        self.subtype = subtype
        self.x_variable_name = x_variable_name
        self.y_variable_name = y_variable_name
        self.x_values = x_values
        self.y_values = y_values

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'H2OTimeSeriesPlot':
        return H2OTimeSeriesPlot(self.subtype, self.x_variable_name, self.y_variable_name, self.x_values, self.y_values)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'H2OTimeSeriesPlot':
        return H2OTimeSeriesPlot(**d)


class AutoVizScatterplot:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, clumpy, correlated, unusual) -> None:
        self.clumpy = clumpy
        self.correlated = correlated
        self.unusual = unusual

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'AutoVizScatterplot':
        return AutoVizScatterplot(self.clumpy, self.correlated, self.unusual)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'AutoVizScatterplot':
        return AutoVizScatterplot(**d)


class AutoVizHistogram:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, spikes, skewed, unusual, gaps) -> None:
        self.spikes = spikes
        self.skewed = skewed
        self.unusual = unusual
        self.gaps = gaps

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'AutoVizHistogram':
        return AutoVizHistogram(self.spikes, self.skewed, self.unusual, self.gaps)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'AutoVizHistogram':
        return AutoVizHistogram(**d)


class AutoVizBoxplot:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, disparate, heteroscedastic) -> None:
        self.disparate = disparate
        self.heteroscedastic = heteroscedastic

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'AutoVizBoxplot':
        return AutoVizBoxplot(self.disparate, self.heteroscedastic)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'AutoVizBoxplot':
        return AutoVizBoxplot(**d)


class AutoVizBiplot:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, components, loadings, number_of_rows, number_of_columns, component_names, counts) -> None:
        self.components = components
        self.loadings = loadings
        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        self.component_names = component_names
        self.counts = counts

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'AutoVizBiplot':
        return AutoVizBiplot(self.components, self.loadings, self.number_of_rows, self.number_of_columns, self.component_names, self.counts)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'AutoVizBiplot':
        return AutoVizBiplot(**d)


class AutoVizBarcharts:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, unbalanced) -> None:
        self.unbalanced = unbalanced

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'AutoVizBarcharts':
        return AutoVizBarcharts(self.unbalanced)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'AutoVizBarcharts':
        return AutoVizBarcharts(**d)


class AutoVizTransformations:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, transforms, deletions) -> None:
        self.transforms = transforms
        self.deletions = deletions

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'AutoVizTransformations':
        return AutoVizTransformations(self.transforms, self.deletions)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'AutoVizTransformations':
        return AutoVizTransformations(**d)


class H2OAutoViz:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, scatterplots, barcharts, histograms, boxplots, outliers, biplot, transformations, custom_plots) -> None:
        self.scatterplots = scatterplots
        self.barcharts = barcharts
        self.histograms = histograms
        self.boxplots = boxplots
        self.outliers = outliers
        self.biplot = biplot
        self.transformations = transformations
        self.custom_plots = custom_plots

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['scatterplots'] = self.scatterplots.dump()
        d['barcharts'] = self.barcharts.dump()
        d['histograms'] = self.histograms.dump()
        d['boxplots'] = self.boxplots.dump()
        d['biplot'] = self.biplot.dump()
        d['transformations'] = self.transformations.dump()
        d['custom_plots'] = [a.dump() for a in self.custom_plots]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'H2OAutoViz':
        return H2OAutoViz(self.scatterplots, self.barcharts, self.histograms, self.boxplots, self.outliers, self.biplot, self.transformations, self.custom_plots)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'H2OAutoViz':
        d['scatterplots'] = AutoVizScatterplot.load(d['scatterplots'])
        d['barcharts'] = AutoVizBarcharts.load(d['barcharts'])
        d['histograms'] = AutoVizHistogram.load(d['histograms'])
        d['boxplots'] = AutoVizBoxplot.load(d['boxplots'])
        d['biplot'] = AutoVizBiplot.load(d['biplot'])
        d['transformations'] = AutoVizTransformations.load(d['transformations'])
        d['custom_plots'] = [VegaPlotJob.load(a) for a in d['custom_plots']]
        return H2OAutoViz(**d)


class Scorer:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, name, maximize, for_regression, for_binomial, for_multiclass, limit_type, description, is_custom) -> None:
        self.name = name
        self.maximize = maximize
        self.for_regression = for_regression
        self.for_binomial = for_binomial
        self.for_multiclass = for_multiclass
        self.limit_type = limit_type
        self.description = description
        self.is_custom = is_custom

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'Scorer':
        return Scorer(self.name, self.maximize, self.for_regression, self.for_binomial, self.for_multiclass, self.limit_type, self.description, self.is_custom)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'Scorer':
        return Scorer(**d)


class TransformerWrapper:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, name, is_custom) -> None:
        self.name = name
        self.is_custom = is_custom

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'TransformerWrapper':
        return TransformerWrapper(self.name, self.is_custom)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'TransformerWrapper':
        return TransformerWrapper(**d)


class PreTransformerWrapper:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, name, is_custom) -> None:
        self.name = name
        self.is_custom = is_custom

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'PreTransformerWrapper':
        return PreTransformerWrapper(self.name, self.is_custom)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'PreTransformerWrapper':
        return PreTransformerWrapper(**d)


class ModelEstimatorWrapper:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, name, is_custom) -> None:
        self.name = name
        self.is_custom = is_custom

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ModelEstimatorWrapper':
        return ModelEstimatorWrapper(self.name, self.is_custom)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ModelEstimatorWrapper':
        return ModelEstimatorWrapper(**d)


class DataWrapper:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, name, is_custom) -> None:
        self.name = name
        self.is_custom = is_custom

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DataWrapper':
        return DataWrapper(self.name, self.is_custom)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DataWrapper':
        return DataWrapper(**d)


class DatasetNumericColumnStats:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, count, mean, std, min, max, unique, freq, hist_ticks, hist_counts) -> None:
        self.count = count
        self.mean = mean
        self.std = std
        self.min = min
        self.max = max
        self.unique = unique
        self.freq = freq
        self.hist_ticks = hist_ticks
        self.hist_counts = hist_counts

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DatasetNumericColumnStats':
        return DatasetNumericColumnStats(self.count, self.mean, self.std, self.min, self.max, self.unique, self.freq, self.hist_ticks, self.hist_counts)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DatasetNumericColumnStats':
        return DatasetNumericColumnStats(**d)


class DatasetNonNumericColumnStats:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, count, unique, top, freq, hist_ticks, hist_counts) -> None:
        self.count = count
        self.unique = unique
        self.top = top
        self.freq = freq
        self.hist_ticks = hist_ticks
        self.hist_counts = hist_counts

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DatasetNonNumericColumnStats':
        return DatasetNonNumericColumnStats(self.count, self.unique, self.top, self.freq, self.hist_ticks, self.hist_counts)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DatasetNonNumericColumnStats':
        return DatasetNonNumericColumnStats(**d)


class DatasetColumnStats:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, is_numeric, num_classes, numeric, non_numeric) -> None:
        self.is_numeric = is_numeric
        self.num_classes = num_classes
        self.numeric = numeric
        self.non_numeric = non_numeric

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['numeric'] = self.numeric.dump()
        d['non_numeric'] = self.non_numeric.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DatasetColumnStats':
        return DatasetColumnStats(self.is_numeric, self.num_classes, self.numeric, self.non_numeric)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DatasetColumnStats':
        d['numeric'] = DatasetNumericColumnStats.load(d['numeric'])
        d['non_numeric'] = DatasetNonNumericColumnStats.load(d['non_numeric'])
        return DatasetColumnStats(**d)


class DatasetColumn:
    """

    :param data_type: Internal column representation type
    :param logical_types: List of DS types, which this column can be treated as ['num', 'cat', 'date', 'datetime', 'text', 'id', 'image']
    """
    @ignore_unexpected_kwargs
    def __init__(self, name, data_type, logical_types, datetime_format, stats, data, training_params) -> None:
        self.name = name
        self.data_type = data_type
        self.logical_types = logical_types
        self.datetime_format = datetime_format
        self.stats = stats
        self.data = data
        self.training_params = training_params

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['stats'] = self.stats.dump()
        d['training_params'] = self.training_params.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DatasetColumn':
        return DatasetColumn(self.name, self.data_type, self.logical_types, self.datetime_format, self.stats, self.data, self.training_params)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DatasetColumn':
        d['stats'] = DatasetColumnStats.load(d['stats'])
        d['training_params'] = TrainingFeature.load(d['training_params'])
        return DatasetColumn(**d)


class Dataset:
    """

    :param remote: True if the model is only available remotely in Storage.
    """
    @ignore_unexpected_kwargs
    def __init__(self, key, name, file_path, file_size, bin_file_path, data_source, row_count, columns, original_frame, aggregated_frame, mapping_frame, uploaded, remote) -> None:
        self.key = key
        self.name = name
        self.file_path = file_path
        self.file_size = file_size
        self.bin_file_path = bin_file_path
        self.data_source = data_source
        self.row_count = row_count
        self.columns = columns
        self.original_frame = original_frame
        self.aggregated_frame = aggregated_frame
        self.mapping_frame = mapping_frame
        self.uploaded = uploaded
        self.remote = remote

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['columns'] = [a.dump() for a in self.columns]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'Dataset':
        return Dataset(self.key, self.name, self.file_path, self.file_size, self.bin_file_path, self.data_source, self.row_count, self.columns, self.original_frame, self.aggregated_frame, self.mapping_frame, self.uploaded, self.remote)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'Dataset':
        d['columns'] = [DatasetColumn.load(a) for a in d['columns']]
        return Dataset(**d)


class DatasetSummary:
    """

    :param remote: True if the model is only available remotely in Storage.
    """
    @ignore_unexpected_kwargs
    def __init__(self, key, name, file_path, file_size, data_source, row_count, column_count, import_status, import_error, aggregation_status, aggregation_error, aggregated_frame, mapping_frame, uploaded, remote, created, logfile_path) -> None:
        self.key = key
        self.name = name
        self.file_path = file_path
        self.file_size = file_size
        self.data_source = data_source
        self.row_count = row_count
        self.column_count = column_count
        self.import_status = import_status
        self.import_error = import_error
        self.aggregation_status = aggregation_status
        self.aggregation_error = aggregation_error
        self.aggregated_frame = aggregated_frame
        self.mapping_frame = mapping_frame
        self.uploaded = uploaded
        self.remote = remote
        self.created = created
        self.logfile_path = logfile_path

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DatasetSummary':
        return DatasetSummary(self.key, self.name, self.file_path, self.file_size, self.data_source, self.row_count, self.column_count, self.import_status, self.import_error, self.aggregation_status, self.aggregation_error, self.aggregated_frame, self.mapping_frame, self.uploaded, self.remote, self.created, self.logfile_path)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DatasetSummary':
        return DatasetSummary(**d)


class ListDatasetQueryResponse:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, datasets, offset, limit, total_count) -> None:
        self.datasets = datasets
        self.offset = offset
        self.limit = limit
        self.total_count = total_count

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['datasets'] = [a.dump() for a in self.datasets]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ListDatasetQueryResponse':
        return ListDatasetQueryResponse(self.datasets, self.offset, self.limit, self.total_count)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ListDatasetQueryResponse':
        d['datasets'] = [DatasetSummary.load(a) for a in d['datasets']]
        return ListDatasetQueryResponse(**d)


class DatasetJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, aggregation_status, aggregation_error, entity, created, uploaded, logfile_path) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.aggregation_status = aggregation_status
        self.aggregation_error = aggregation_error
        self.entity = entity
        self.created = created
        self.uploaded = uploaded
        self.logfile_path = logfile_path

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DatasetJob':
        return DatasetJob(self.progress, self.status, self.error, self.message, self.aggregation_status, self.aggregation_error, self.entity, self.created, self.uploaded, self.logfile_path)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DatasetJob':
        d['entity'] = Dataset.load(d['entity'])
        return DatasetJob(**d)


class AutoVizSummary:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, key, name, dataset, progress, status, message, training_duration, created) -> None:
        self.key = key
        self.name = name
        self.dataset = dataset
        self.progress = progress
        self.status = status
        self.message = message
        self.training_duration = training_duration
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['dataset'] = self.dataset.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'AutoVizSummary':
        return AutoVizSummary(self.key, self.name, self.dataset, self.progress, self.status, self.message, self.training_duration, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'AutoVizSummary':
        d['dataset'] = DatasetReference.load(d['dataset'])
        return AutoVizSummary(**d)


class AutoVizJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, entity, created, finished, key, name, dataset, deprecated) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created
        self.finished = finished
        self.key = key
        self.name = name
        self.dataset = dataset
        self.deprecated = deprecated

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        d['dataset'] = self.dataset.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'AutoVizJob':
        return AutoVizJob(self.progress, self.status, self.error, self.message, self.entity, self.created, self.finished, self.key, self.name, self.dataset, self.deprecated)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'AutoVizJob':
        d['entity'] = H2OAutoViz.load(d['entity'])
        d['dataset'] = DatasetReference.load(d['dataset'])
        return AutoVizJob(**d)


class VegaPlotJob:
    """

    :param entity: Vega dictionary
    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, entity, created, key, description, dataset) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created
        self.key = key
        self.description = description
        self.dataset = dataset

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['dataset'] = self.dataset.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'VegaPlotJob':
        return VegaPlotJob(self.progress, self.status, self.error, self.message, self.entity, self.created, self.key, self.description, self.dataset)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'VegaPlotJob':
        d['dataset'] = DatasetReference.load(d['dataset'])
        return VegaPlotJob(**d)


class ScatterPlotJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, entity, created) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ScatterPlotJob':
        return ScatterPlotJob(self.progress, self.status, self.error, self.message, self.entity, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ScatterPlotJob':
        d['entity'] = H2OPlot.load(d['entity'])
        return ScatterPlotJob(**d)


class HistogramJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, entity, created) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'HistogramJob':
        return HistogramJob(self.progress, self.status, self.error, self.message, self.entity, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'HistogramJob':
        d['entity'] = Histogram.load(d['entity'])
        return HistogramJob(**d)


class VisStatsJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, entity, created) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'VisStatsJob':
        return VisStatsJob(self.progress, self.status, self.error, self.message, self.entity, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'VisStatsJob':
        d['entity'] = H2OVisStats.load(d['entity'])
        return VisStatsJob(**d)


class BoxplotJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, entity, created) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'BoxplotJob':
        return BoxplotJob(self.progress, self.status, self.error, self.message, self.entity, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'BoxplotJob':
        d['entity'] = H2OBoxplot.load(d['entity'])
        return BoxplotJob(**d)


class DotplotJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, entity, created) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DotplotJob':
        return DotplotJob(self.progress, self.status, self.error, self.message, self.entity, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DotplotJob':
        d['entity'] = H2ODotplot.load(d['entity'])
        return DotplotJob(**d)


class HeatMapJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, entity, created) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'HeatMapJob':
        return HeatMapJob(self.progress, self.status, self.error, self.message, self.entity, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'HeatMapJob':
        d['entity'] = H2OHeatMap.load(d['entity'])
        return HeatMapJob(**d)


class NetworkJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, entity, created) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'NetworkJob':
        return NetworkJob(self.progress, self.status, self.error, self.message, self.entity, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'NetworkJob':
        d['entity'] = H2ONetwork.load(d['entity'])
        return NetworkJob(**d)


class ParallelCoordinatesPlotJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, entity, created) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ParallelCoordinatesPlotJob':
        return ParallelCoordinatesPlotJob(self.progress, self.status, self.error, self.message, self.entity, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ParallelCoordinatesPlotJob':
        d['entity'] = H2OParallelCoordinatesPlot.load(d['entity'])
        return ParallelCoordinatesPlotJob(**d)


class BarchartJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, entity, created) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'BarchartJob':
        return BarchartJob(self.progress, self.status, self.error, self.message, self.entity, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'BarchartJob':
        d['entity'] = H2OBarchart.load(d['entity'])
        return BarchartJob(**d)


class OutliersJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, entity, created) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'OutliersJob':
        return OutliersJob(self.progress, self.status, self.error, self.message, self.entity, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'OutliersJob':
        d['entity'] = H2OOutliers.load(d['entity'])
        return OutliersJob(**d)


class FileSearchResult:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, type, name, extra, path) -> None:
        self.type = type
        self.name = name
        self.extra = extra
        self.path = path

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'FileSearchResult':
        return FileSearchResult(self.type, self.name, self.extra, self.path)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'FileSearchResult':
        return FileSearchResult(**d)


class FileSearchResults:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, dir, entries) -> None:
        self.dir = dir
        self.entries = entries

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entries'] = [a.dump() for a in self.entries]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'FileSearchResults':
        return FileSearchResults(self.dir, self.entries)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'FileSearchResults':
        d['entries'] = [FileSearchResult.load(a) for a in d['entries']]
        return FileSearchResults(**d)


class ModelParameters:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, dataset, resumed_model, target_col, weight_col, fold_col, orig_time_col, time_col, is_classification, cols_to_drop, validset, testset, enable_gpus, seed, accuracy, time, interpretability, score_f_name, time_groups_columns, unavailable_columns_at_prediction_time, time_period_in_seconds, num_prediction_periods, num_gap_periods, is_timeseries, cols_imputation, config_overrides, custom_features, is_image) -> None:
        validation.validate_toml(config_overrides, 'config_overrides')
        self.dataset = dataset
        self.resumed_model = resumed_model
        self.target_col = target_col
        self.weight_col = weight_col
        self.fold_col = fold_col
        self.orig_time_col = orig_time_col
        self.time_col = time_col
        self.is_classification = is_classification
        self.cols_to_drop = cols_to_drop
        self.validset = validset
        self.testset = testset
        self.enable_gpus = enable_gpus
        self.seed = seed
        self.accuracy = accuracy
        self.time = time
        self.interpretability = interpretability
        self.score_f_name = score_f_name
        self.time_groups_columns = time_groups_columns
        self.unavailable_columns_at_prediction_time = unavailable_columns_at_prediction_time
        self.time_period_in_seconds = time_period_in_seconds
        self.num_prediction_periods = num_prediction_periods
        self.num_gap_periods = num_gap_periods
        self.is_timeseries = is_timeseries
        self.cols_imputation = cols_imputation
        self.config_overrides = config_overrides
        self.custom_features = custom_features
        self.is_image = is_image

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['dataset'] = self.dataset.dump()
        d['resumed_model'] = self.resumed_model.dump()
        d['validset'] = self.validset.dump()
        d['testset'] = self.testset.dump()
        d['cols_imputation'] = [a.dump() for a in self.cols_imputation]
        d['custom_features'] = [a.dump() for a in self.custom_features]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ModelParameters':
        return ModelParameters(self.dataset, self.resumed_model, self.target_col, self.weight_col, self.fold_col, self.orig_time_col, self.time_col, self.is_classification, self.cols_to_drop, self.validset, self.testset, self.enable_gpus, self.seed, self.accuracy, self.time, self.interpretability, self.score_f_name, self.time_groups_columns, self.unavailable_columns_at_prediction_time, self.time_period_in_seconds, self.num_prediction_periods, self.num_gap_periods, self.is_timeseries, self.cols_imputation, self.config_overrides, self.custom_features, self.is_image)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ModelParameters':
        d['dataset'] = DatasetReference.load(d['dataset'])
        d['resumed_model'] = ModelReference.load(d['resumed_model'])
        d['validset'] = DatasetReference.load(d['validset'])
        d['testset'] = DatasetReference.load(d['testset'])
        d['cols_imputation'] = [ColumnImputation.load(a) for a in d['cols_imputation']]
        d['custom_features'] = [TrainingFeature.load(a) for a in d['custom_features']]
        return ModelParameters(**d)


class ColumnImputation:
    """

    :param meta: e.g. percentile rank
    :param precomputed: Whether value provided, or computed at validation
    """
    @ignore_unexpected_kwargs
    def __init__(self, col_name, type, value, meta, precomputed) -> None:
        self.col_name = col_name
        self.type = type
        self.value = value
        self.meta = meta
        self.precomputed = precomputed

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ColumnImputation':
        return ColumnImputation(self.col_name, self.type, self.value, self.meta, self.precomputed)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ColumnImputation':
        return ColumnImputation(**d)


class ListDatasetsRequest:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, offset, limit) -> None:
        self.offset = offset
        self.limit = limit

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ListDatasetsRequest':
        return ListDatasetsRequest(self.offset, self.limit)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ListDatasetsRequest':
        return ListDatasetsRequest(**d)


class ListDatasetsResponse:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, datasets) -> None:
        self.datasets = datasets

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['datasets'] = [a.dump() for a in self.datasets]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ListDatasetsResponse':
        return ListDatasetsResponse(self.datasets)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ListDatasetsResponse':
        d['datasets'] = [Dataset.load(a) for a in d['datasets']]
        return ListDatasetsResponse(**d)


class VarImpTable:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, gain, interaction, description) -> None:
        self.gain = gain
        self.interaction = interaction
        self.description = description

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'VarImpTable':
        return VarImpTable(self.gain, self.interaction, self.description)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'VarImpTable':
        return VarImpTable(**d)


class ScoresTable:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, best, iteration, score, model_types) -> None:
        self.best = best
        self.iteration = iteration
        self.score = score
        self.model_types = model_types

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ScoresTable':
        return ScoresTable(self.best, self.iteration, self.score, self.model_types)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ScoresTable':
        return ScoresTable(**d)


class TraceEvent:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, name, ph, ts, ppid, pid, tid, args) -> None:
        self.name = name
        self.ph = ph
        self.ts = ts
        self.ppid = ppid
        self.pid = pid
        self.tid = tid
        self.args = args

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'TraceEvent':
        return TraceEvent(self.name, self.ph, self.ts, self.ppid, self.pid, self.tid, self.args)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'TraceEvent':
        return TraceEvent(**d)


class TraceProgress:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, trace_events) -> None:
        self.trace_events = trace_events

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['trace_events'] = [a.dump() for a in self.trace_events]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'TraceProgress':
        return TraceProgress(self.trace_events)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'TraceProgress':
        d['trace_events'] = [TraceEvent.load(a) for a in d['trace_events']]
        return TraceProgress(**d)


class ModelTraceEvents:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, events, done, status) -> None:
        self.events = events
        self.done = done
        self.status = status

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['events'] = [a.dump() for a in self.events]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ModelTraceEvents':
        return ModelTraceEvents(self.events, self.done, self.status)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ModelTraceEvents':
        d['events'] = [TraceEvent.load(a) for a in d['events']]
        return ModelTraceEvents(**d)


class AutoDLInit:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, score_f_name) -> None:
        self.score_f_name = score_f_name

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'AutoDLInit':
        return AutoDLInit(self.score_f_name)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'AutoDLInit':
        return AutoDLInit(**d)


class AutoDLProgress:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, message, iteration, max_iterations, progress, importances, scores, score, score_mean, score_sd, total_features, roc, gains, act_vs_pred, residual_plot) -> None:
        self.message = message
        self.iteration = iteration
        self.max_iterations = max_iterations
        self.progress = progress
        self.importances = importances
        self.scores = scores
        self.score = score
        self.score_mean = score_mean
        self.score_sd = score_sd
        self.total_features = total_features
        self.roc = roc
        self.gains = gains
        self.act_vs_pred = act_vs_pred
        self.residual_plot = residual_plot

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['importances'] = [a.dump() for a in self.importances]
        d['scores'] = self.scores.dump()
        d['roc'] = self.roc.dump()
        d['gains'] = self.gains.dump()
        d['act_vs_pred'] = self.act_vs_pred.dump()
        d['residual_plot'] = self.residual_plot.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'AutoDLProgress':
        return AutoDLProgress(self.message, self.iteration, self.max_iterations, self.progress, self.importances, self.scores, self.score, self.score_mean, self.score_sd, self.total_features, self.roc, self.gains, self.act_vs_pred, self.residual_plot)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'AutoDLProgress':
        d['importances'] = [VarImpTable.load(a) for a in d['importances']]
        d['scores'] = ScoresTable.load(d['scores'])
        d['roc'] = ROC.load(d['roc'])
        d['gains'] = GainLift.load(d['gains'])
        d['act_vs_pred'] = H2OPlot.load(d['act_vs_pred'])
        d['residual_plot'] = H2OPlot.load(d['residual_plot'])
        return AutoDLProgress(**d)


class GainLift:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, quantiles, gains, lifts, cum_right, cum_wrong) -> None:
        self.quantiles = quantiles
        self.gains = gains
        self.lifts = lifts
        self.cum_right = cum_right
        self.cum_wrong = cum_wrong

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'GainLift':
        return GainLift(self.quantiles, self.gains, self.lifts, self.cum_right, self.cum_wrong)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'GainLift':
        return GainLift(**d)


class ROC:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, labels, auc, aucpr, thresholds, threshold_cms, argmax_cm, default_threshold) -> None:
        self.labels = labels
        self.auc = auc
        self.aucpr = aucpr
        self.thresholds = thresholds
        self.threshold_cms = threshold_cms
        self.argmax_cm = argmax_cm
        self.default_threshold = default_threshold

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['threshold_cms'] = [a.dump() for a in self.threshold_cms]
        d['argmax_cm'] = self.argmax_cm.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ROC':
        return ROC(self.labels, self.auc, self.aucpr, self.thresholds, self.threshold_cms, self.argmax_cm, self.default_threshold)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ROC':
        d['threshold_cms'] = [ConfusionMatrix.load(a) for a in d['threshold_cms']]
        d['argmax_cm'] = ConfusionMatrix.load(d['argmax_cm'])
        return ROC(**d)


class ConfusionMatrix:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, labels, matrix, row_counts, col_counts, miss_counts) -> None:
        self.labels = labels
        self.matrix = matrix
        self.row_counts = row_counts
        self.col_counts = col_counts
        self.miss_counts = miss_counts

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ConfusionMatrix':
        return ConfusionMatrix(self.labels, self.matrix, self.row_counts, self.col_counts, self.miss_counts)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ConfusionMatrix':
        return ConfusionMatrix(**d)


class TrainingColumn:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, name, dtype, typecode, possible_types, is_numeric, is_integer, is_bool, is_real, is_str, min, max, num_uniques, has_na, sample_levels, datetime_format, raw_name) -> None:
        self.name = name
        self.dtype = dtype
        self.typecode = typecode
        self.possible_types = possible_types
        self.is_numeric = is_numeric
        self.is_integer = is_integer
        self.is_bool = is_bool
        self.is_real = is_real
        self.is_str = is_str
        self.min = min
        self.max = max
        self.num_uniques = num_uniques
        self.has_na = has_na
        self.sample_levels = sample_levels
        self.datetime_format = datetime_format
        self.raw_name = raw_name

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'TrainingColumn':
        return TrainingColumn(self.name, self.dtype, self.typecode, self.possible_types, self.is_numeric, self.is_integer, self.is_bool, self.is_real, self.is_str, self.min, self.max, self.num_uniques, self.has_na, self.sample_levels, self.datetime_format, self.raw_name)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'TrainingColumn':
        return TrainingColumn(**d)


class ModelTrainingSchema:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, pre_columns, columns, transformed_columns, target, is_classification, labels, missing_values) -> None:
        self.pre_columns = pre_columns
        self.columns = columns
        self.transformed_columns = transformed_columns
        self.target = target
        self.is_classification = is_classification
        self.labels = labels
        self.missing_values = missing_values

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['pre_columns'] = [a.dump() for a in self.pre_columns]
        d['columns'] = [a.dump() for a in self.columns]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ModelTrainingSchema':
        return ModelTrainingSchema(self.pre_columns, self.columns, self.transformed_columns, self.target, self.is_classification, self.labels, self.missing_values)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ModelTrainingSchema':
        d['pre_columns'] = [TrainingColumn.load(a) for a in d['pre_columns']]
        d['columns'] = [TrainingColumn.load(a) for a in d['columns']]
        return ModelTrainingSchema(**d)


class TrainingFeature:
    """
    Used to pre-populate experiment with force-in features

    :param transformer_name: Name of transformer, which will be applied
    :param column_names: Ordered list! E.g. for SUM Interaction transformer could be ['x1', 'x2']
    :param monotonicity: Monotonic constraint for model (auto, -1, 0, 1) - as in https://xgboost.readthedocs.io/en/latest/tutorials/monotonic.html
    :param forced_on_off: Whether this feature must be in experiment (on), or must not (off). ['on', 'off', 'auto']
    :param sign: per-feature sign
    :param exclusive: If this feature with this column is used, whether any other transformer can use it
    :param allowed_transformations: List of transformers which can be later applied to this feature
    :param allowed_models: List of models, which can use this feature
    :param interaction_depth: Max depth of nested transformation, in which this feature can occur, -1 for infinite
    :param apply_to_all: Apply the selected transformer to all vs any selected columns
    """
    @ignore_unexpected_kwargs
    def __init__(self, transformer_name, column_names, monotonicity, forced_on_off, sign, exclusive, allowed_transformations, allowed_models, interaction_depth, apply_to_all) -> None:
        self.transformer_name = transformer_name
        self.column_names = column_names
        self.monotonicity = monotonicity
        self.forced_on_off = forced_on_off
        self.sign = sign
        self.exclusive = exclusive
        self.allowed_transformations = allowed_transformations
        self.allowed_models = allowed_models
        self.interaction_depth = interaction_depth
        self.apply_to_all = apply_to_all

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'TrainingFeature':
        return TrainingFeature(self.transformer_name, self.column_names, self.monotonicity, self.forced_on_off, self.sign, self.exclusive, self.allowed_transformations, self.allowed_models, self.interaction_depth, self.apply_to_all)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'TrainingFeature':
        return TrainingFeature(**d)


class AutoDLResult:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, log_file_path, pickle_path, summary_path, train_predictions_path, valid_predictions_path, test_predictions_path, unfitted_pipeline_path, fitted_model_path, scoring_pipeline_path, mojo_pipeline_path, test_score, test_score_sd, test_roc, test_gains, test_act_vs_pred, test_residual_plot, labels, ids_col) -> None:
        self.log_file_path = log_file_path
        self.pickle_path = pickle_path
        self.summary_path = summary_path
        self.train_predictions_path = train_predictions_path
        self.valid_predictions_path = valid_predictions_path
        self.test_predictions_path = test_predictions_path
        self.unfitted_pipeline_path = unfitted_pipeline_path
        self.fitted_model_path = fitted_model_path
        self.scoring_pipeline_path = scoring_pipeline_path
        self.mojo_pipeline_path = mojo_pipeline_path
        self.test_score = test_score
        self.test_score_sd = test_score_sd
        self.test_roc = test_roc
        self.test_gains = test_gains
        self.test_act_vs_pred = test_act_vs_pred
        self.test_residual_plot = test_residual_plot
        self.labels = labels
        self.ids_col = ids_col

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['test_roc'] = self.test_roc.dump()
        d['test_gains'] = self.test_gains.dump()
        d['test_act_vs_pred'] = self.test_act_vs_pred.dump()
        d['test_residual_plot'] = self.test_residual_plot.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'AutoDLResult':
        return AutoDLResult(self.log_file_path, self.pickle_path, self.summary_path, self.train_predictions_path, self.valid_predictions_path, self.test_predictions_path, self.unfitted_pipeline_path, self.fitted_model_path, self.scoring_pipeline_path, self.mojo_pipeline_path, self.test_score, self.test_score_sd, self.test_roc, self.test_gains, self.test_act_vs_pred, self.test_residual_plot, self.labels, self.ids_col)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'AutoDLResult':
        d['test_roc'] = ROC.load(d['test_roc'])
        d['test_gains'] = GainLift.load(d['test_gains'])
        d['test_act_vs_pred'] = H2OPlot.load(d['test_act_vs_pred'])
        d['test_residual_plot'] = H2OPlot.load(d['test_residual_plot'])
        return AutoDLResult(**d)


class AutoDLScoresOverview:
    """

    :param path: Path to Markdown document describing scores
    :param checksum: MD5 checksum to check if content was modified
    """
    @ignore_unexpected_kwargs
    def __init__(self, path, checksum) -> None:
        self.path = path
        self.checksum = checksum

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'AutoDLScoresOverview':
        return AutoDLScoresOverview(self.path, self.checksum)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'AutoDLScoresOverview':
        return AutoDLScoresOverview(**d)


class AutoDLNotification:
    """

    :param priority: 0 - low, 1 - medium, 2 - high
    """
    @ignore_unexpected_kwargs
    def __init__(self, key, title, content, priority, created) -> None:
        self.key = key
        self.title = title
        self.content = content
        self.priority = priority
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'AutoDLNotification':
        return AutoDLNotification(self.key, self.title, self.content, self.priority, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'AutoDLNotification':
        return AutoDLNotification(**d)


class MLIProgress:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, msg, done) -> None:
        self.progress = progress
        self.msg = msg
        self.done = done

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'MLIProgress':
        return MLIProgress(self.progress, self.msg, self.done)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'MLIProgress':
        return MLIProgress(**d)


class H2OProgress:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, msg, done) -> None:
        self.progress = progress
        self.msg = msg
        self.done = done

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'H2OProgress':
        return H2OProgress(self.progress, self.msg, self.done)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'H2OProgress':
        return H2OProgress(**d)


class SystemStats:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, kind, cpu, mem, per) -> None:
        self.kind = kind
        self.cpu = cpu
        self.mem = mem
        self.per = per

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['mem'] = self.mem.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'SystemStats':
        return SystemStats(self.kind, self.cpu, self.mem, self.per)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'SystemStats':
        d['mem'] = MemoryStats.load(d['mem'])
        return SystemStats(**d)


class GPUStats:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, gpus, mems, types, usages) -> None:
        self.gpus = gpus
        self.mems = mems
        self.types = types
        self.usages = usages

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'GPUStats':
        return GPUStats(self.gpus, self.mems, self.types, self.usages)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'GPUStats':
        return GPUStats(**d)


class DiskStats:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, total, available, limit) -> None:
        self.total = total
        self.available = available
        self.limit = limit

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DiskStats':
        return DiskStats(self.total, self.available, self.limit)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DiskStats':
        return DiskStats(**d)


class MemoryStats:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, total, available, limit, per) -> None:
        self.total = total
        self.available = available
        self.limit = limit
        self.per = per

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'MemoryStats':
        return MemoryStats(self.total, self.available, self.limit, self.per)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'MemoryStats':
        return MemoryStats(**d)


class ExperimentsStats:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, total, running, finished, failed, my_total, my_running, my_finished, my_failed) -> None:
        self.total = total
        self.running = running
        self.finished = finished
        self.failed = failed
        self.my_total = my_total
        self.my_running = my_running
        self.my_finished = my_finished
        self.my_failed = my_failed

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ExperimentsStats':
        return ExperimentsStats(self.total, self.running, self.finished, self.failed, self.my_total, self.my_running, self.my_finished, self.my_failed)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ExperimentsStats':
        return ExperimentsStats(**d)


class Model:
    """

    :param insights_paths: Paths to insights documents in Markdown format
    :param notifications: List of AutoDLNotification keys
    :param experiment_dir: Path to root of experiment structure
    :param remote: True if the model is only available remotely in Storage.
    """
    @ignore_unexpected_kwargs
    def __init__(self, key, description, parameters, log_file_path, pickle_path, autoreport_path, summary_path, train_predictions_path, valid_predictions_path, test_predictions_path, unfitted_pipeline_path, fitted_model_path, scoring_pipeline_path, mojo_pipeline_path, valid_score, valid_score_sd, valid_roc, valid_gains, valid_act_vs_pred, valid_residual_plot, test_score, test_score_sd, test_roc, test_gains, test_act_vs_pred, test_residual_plot, labels, ids_col, score_f_name, score, iteration_data, insights_paths, scores_overview, trace_events, notifications, training_duration, deprecated, patched_pred_contribs, max_iterations, model_file_size, diagnostic_keys, summary, experiment_dir, remote) -> None:
        self.key = key
        self.description = description
        self.parameters = parameters
        self.log_file_path = log_file_path
        self.pickle_path = pickle_path
        self.autoreport_path = autoreport_path
        self.summary_path = summary_path
        self.train_predictions_path = train_predictions_path
        self.valid_predictions_path = valid_predictions_path
        self.test_predictions_path = test_predictions_path
        self.unfitted_pipeline_path = unfitted_pipeline_path
        self.fitted_model_path = fitted_model_path
        self.scoring_pipeline_path = scoring_pipeline_path
        self.mojo_pipeline_path = mojo_pipeline_path
        self.valid_score = valid_score
        self.valid_score_sd = valid_score_sd
        self.valid_roc = valid_roc
        self.valid_gains = valid_gains
        self.valid_act_vs_pred = valid_act_vs_pred
        self.valid_residual_plot = valid_residual_plot
        self.test_score = test_score
        self.test_score_sd = test_score_sd
        self.test_roc = test_roc
        self.test_gains = test_gains
        self.test_act_vs_pred = test_act_vs_pred
        self.test_residual_plot = test_residual_plot
        self.labels = labels
        self.ids_col = ids_col
        self.score_f_name = score_f_name
        self.score = score
        self.iteration_data = iteration_data
        self.insights_paths = insights_paths
        self.scores_overview = scores_overview
        self.trace_events = trace_events
        self.notifications = notifications
        self.training_duration = training_duration
        self.deprecated = deprecated
        self.patched_pred_contribs = patched_pred_contribs
        self.max_iterations = max_iterations
        self.model_file_size = model_file_size
        self.diagnostic_keys = diagnostic_keys
        self.summary = summary
        self.experiment_dir = experiment_dir
        self.remote = remote

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['parameters'] = self.parameters.dump()
        d['valid_roc'] = self.valid_roc.dump()
        d['valid_gains'] = self.valid_gains.dump()
        d['valid_act_vs_pred'] = self.valid_act_vs_pred.dump()
        d['valid_residual_plot'] = self.valid_residual_plot.dump()
        d['test_roc'] = self.test_roc.dump()
        d['test_gains'] = self.test_gains.dump()
        d['test_act_vs_pred'] = self.test_act_vs_pred.dump()
        d['test_residual_plot'] = self.test_residual_plot.dump()
        d['scores_overview'] = self.scores_overview.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'Model':
        return Model(self.key, self.description, self.parameters, self.log_file_path, self.pickle_path, self.autoreport_path, self.summary_path, self.train_predictions_path, self.valid_predictions_path, self.test_predictions_path, self.unfitted_pipeline_path, self.fitted_model_path, self.scoring_pipeline_path, self.mojo_pipeline_path, self.valid_score, self.valid_score_sd, self.valid_roc, self.valid_gains, self.valid_act_vs_pred, self.valid_residual_plot, self.test_score, self.test_score_sd, self.test_roc, self.test_gains, self.test_act_vs_pred, self.test_residual_plot, self.labels, self.ids_col, self.score_f_name, self.score, self.iteration_data, self.insights_paths, self.scores_overview, self.trace_events, self.notifications, self.training_duration, self.deprecated, self.patched_pred_contribs, self.max_iterations, self.model_file_size, self.diagnostic_keys, self.summary, self.experiment_dir, self.remote)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'Model':
        d['parameters'] = ModelParameters.load(d['parameters'])
        d['valid_roc'] = ROC.load(d['valid_roc'])
        d['valid_gains'] = GainLift.load(d['valid_gains'])
        d['valid_act_vs_pred'] = H2OPlot.load(d['valid_act_vs_pred'])
        d['valid_residual_plot'] = H2OPlot.load(d['valid_residual_plot'])
        d['test_roc'] = ROC.load(d['test_roc'])
        d['test_gains'] = GainLift.load(d['test_gains'])
        d['test_act_vs_pred'] = H2OPlot.load(d['test_act_vs_pred'])
        d['test_residual_plot'] = H2OPlot.load(d['test_residual_plot'])
        d['scores_overview'] = AutoDLScoresOverview.load(d['scores_overview'])
        return Model(**d)


class ModelJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, entity, eta, created, started, worker_info) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.eta = eta
        self.created = created
        self.started = started
        self.worker_info = worker_info

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        d['worker_info'] = self.worker_info.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ModelJob':
        return ModelJob(self.progress, self.status, self.error, self.message, self.entity, self.eta, self.created, self.started, self.worker_info)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ModelJob':
        d['entity'] = Model.load(d['entity'])
        d['worker_info'] = WorkerID.load(d['worker_info'])
        return ModelJob(**d)


class ImportModelJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, aggregation_status, aggregation_error, entity, created) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.aggregation_status = aggregation_status
        self.aggregation_error = aggregation_error
        self.entity = entity
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ImportModelJob':
        return ImportModelJob(self.progress, self.status, self.error, self.message, self.aggregation_status, self.aggregation_error, self.entity, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ImportModelJob':
        d['entity'] = Model.load(d['entity'])
        return ImportModelJob(**d)


class ModelSummary:
    """

    :param remote: True if the model is only available remotely in Storage.
    """
    @ignore_unexpected_kwargs
    def __init__(self, key, description, parameters, log_file_path, pickle_path, summary_path, train_predictions_path, valid_predictions_path, test_predictions_path, progress, status, training_duration, score_f_name, score, test_score, deprecated, model_file_size, diagnostic_keys, remote, created) -> None:
        self.key = key
        self.description = description
        self.parameters = parameters
        self.log_file_path = log_file_path
        self.pickle_path = pickle_path
        self.summary_path = summary_path
        self.train_predictions_path = train_predictions_path
        self.valid_predictions_path = valid_predictions_path
        self.test_predictions_path = test_predictions_path
        self.progress = progress
        self.status = status
        self.training_duration = training_duration
        self.score_f_name = score_f_name
        self.score = score
        self.test_score = test_score
        self.deprecated = deprecated
        self.model_file_size = model_file_size
        self.diagnostic_keys = diagnostic_keys
        self.remote = remote
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['parameters'] = self.parameters.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ModelSummary':
        return ModelSummary(self.key, self.description, self.parameters, self.log_file_path, self.pickle_path, self.summary_path, self.train_predictions_path, self.valid_predictions_path, self.test_predictions_path, self.progress, self.status, self.training_duration, self.score_f_name, self.score, self.test_score, self.deprecated, self.model_file_size, self.diagnostic_keys, self.remote, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ModelSummary':
        d['parameters'] = ModelParameters.load(d['parameters'])
        return ModelSummary(**d)


class ListModelQueryResponse:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, models, offset, limit, total_count) -> None:
        self.models = models
        self.offset = offset
        self.limit = limit
        self.total_count = total_count

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['models'] = [a.dump() for a in self.models]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ListModelQueryResponse':
        return ListModelQueryResponse(self.models, self.offset, self.limit, self.total_count)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ListModelQueryResponse':
        d['models'] = [ModelSummary.load(a) for a in d['models']]
        return ListModelQueryResponse(**d)


class InterpretParameters:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, dai_model, dataset, target_col, prediction_col, use_raw_features, nfolds, klime_cluster_col, weight_col, drop_cols, sample, sample_num_rows, qbin_cols, qbin_count, lime_method, dt_tree_depth, config_overrides, vars_to_pdp, dia_cols, testset, debug_model_errors, debug_model_errors_class) -> None:
        validation.validate_toml(config_overrides, 'config_overrides')
        self.dai_model = dai_model
        self.dataset = dataset
        self.target_col = target_col
        self.prediction_col = prediction_col
        self.use_raw_features = use_raw_features
        self.nfolds = nfolds
        self.klime_cluster_col = klime_cluster_col
        self.weight_col = weight_col
        self.drop_cols = drop_cols
        self.sample = sample
        self.sample_num_rows = sample_num_rows
        self.qbin_cols = qbin_cols
        self.qbin_count = qbin_count
        self.lime_method = lime_method
        self.dt_tree_depth = dt_tree_depth
        self.config_overrides = config_overrides
        self.vars_to_pdp = vars_to_pdp
        self.dia_cols = dia_cols
        self.testset = testset
        self.debug_model_errors = debug_model_errors
        self.debug_model_errors_class = debug_model_errors_class

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['dai_model'] = self.dai_model.dump()
        d['dataset'] = self.dataset.dump()
        d['testset'] = self.testset.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'InterpretParameters':
        return InterpretParameters(self.dai_model, self.dataset, self.target_col, self.prediction_col, self.use_raw_features, self.nfolds, self.klime_cluster_col, self.weight_col, self.drop_cols, self.sample, self.sample_num_rows, self.qbin_cols, self.qbin_count, self.lime_method, self.dt_tree_depth, self.config_overrides, self.vars_to_pdp, self.dia_cols, self.testset, self.debug_model_errors, self.debug_model_errors_class)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'InterpretParameters':
        d['dai_model'] = ModelReference.load(d['dai_model'])
        d['dataset'] = DatasetReference.load(d['dataset'])
        d['testset'] = DatasetReference.load(d['testset'])
        return InterpretParameters(**d)


class InterpretSummary:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, key, description, parameters, progress, status, training_duration, is_timeseries) -> None:
        self.key = key
        self.description = description
        self.parameters = parameters
        self.progress = progress
        self.status = status
        self.training_duration = training_duration
        self.is_timeseries = is_timeseries

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['parameters'] = self.parameters.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'InterpretSummary':
        return InterpretSummary(self.key, self.description, self.parameters, self.progress, self.status, self.training_duration, self.is_timeseries)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'InterpretSummary':
        d['parameters'] = InterpretParameters.load(d['parameters'])
        return InterpretSummary(**d)


class Prediction:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, key, model_key, scoring_dataset_key, predictions_csv_path) -> None:
        self.key = key
        self.model_key = model_key
        self.scoring_dataset_key = scoring_dataset_key
        self.predictions_csv_path = predictions_csv_path

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'Prediction':
        return Prediction(self.key, self.model_key, self.scoring_dataset_key, self.predictions_csv_path)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'Prediction':
        return Prediction(**d)


class PredictionJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, entity, created, scoring_duration) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created
        self.scoring_duration = scoring_duration

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'PredictionJob':
        return PredictionJob(self.progress, self.status, self.error, self.message, self.entity, self.created, self.scoring_duration)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'PredictionJob':
        d['entity'] = Prediction.load(d['entity'])
        return PredictionJob(**d)


class AutoReport:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, key, model_key, report_path) -> None:
        self.key = key
        self.model_key = model_key
        self.report_path = report_path

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'AutoReport':
        return AutoReport(self.key, self.model_key, self.report_path)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'AutoReport':
        return AutoReport(**d)


class AutoReportJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, entity, created) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'AutoReportJob':
        return AutoReportJob(self.progress, self.status, self.error, self.message, self.entity, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'AutoReportJob':
        d['entity'] = AutoReport.load(d['entity'])
        return AutoReportJob(**d)


class Transformation:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, key, model_key, training_dataset_key, validation_dataset_key, test_dataset_key, validation_split_fraction, seed, fold_column, training_output_csv_path, validation_output_csv_path, test_output_csv_path) -> None:
        self.key = key
        self.model_key = model_key
        self.training_dataset_key = training_dataset_key
        self.validation_dataset_key = validation_dataset_key
        self.test_dataset_key = test_dataset_key
        self.validation_split_fraction = validation_split_fraction
        self.seed = seed
        self.fold_column = fold_column
        self.training_output_csv_path = training_output_csv_path
        self.validation_output_csv_path = validation_output_csv_path
        self.test_output_csv_path = test_output_csv_path

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'Transformation':
        return Transformation(self.key, self.model_key, self.training_dataset_key, self.validation_dataset_key, self.test_dataset_key, self.validation_split_fraction, self.seed, self.fold_column, self.training_output_csv_path, self.validation_output_csv_path, self.test_output_csv_path)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'Transformation':
        return Transformation(**d)


class TransformationJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, entity, created) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'TransformationJob':
        return TransformationJob(self.progress, self.status, self.error, self.message, self.entity, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'TransformationJob':
        d['entity'] = Transformation.load(d['entity'])
        return TransformationJob(**d)


class DaiPdIceInterpretationJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, created, finished, mli_key, dai_key) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.created = created
        self.finished = finished
        self.mli_key = mli_key
        self.dai_key = dai_key

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DaiPdIceInterpretationJob':
        return DaiPdIceInterpretationJob(self.progress, self.status, self.error, self.message, self.created, self.finished, self.mli_key, self.dai_key)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DaiPdIceInterpretationJob':
        return DaiPdIceInterpretationJob(**d)


class InterpretTimeSeries:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, key, description, tmp_dir, parameters, training_duration, test_window_start, test_window_end, holdout_window_start, holdout_window_end, log_file_path, group_metric_file_path) -> None:
        self.key = key
        self.description = description
        self.tmp_dir = tmp_dir
        self.parameters = parameters
        self.training_duration = training_duration
        self.test_window_start = test_window_start
        self.test_window_end = test_window_end
        self.holdout_window_start = holdout_window_start
        self.holdout_window_end = holdout_window_end
        self.log_file_path = log_file_path
        self.group_metric_file_path = group_metric_file_path

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['parameters'] = self.parameters.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'InterpretTimeSeries':
        return InterpretTimeSeries(self.key, self.description, self.tmp_dir, self.parameters, self.training_duration, self.test_window_start, self.test_window_end, self.holdout_window_start, self.holdout_window_end, self.log_file_path, self.group_metric_file_path)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'InterpretTimeSeries':
        d['parameters'] = InterpretParameters.load(d['parameters'])
        return InterpretTimeSeries(**d)


class InterpretTimeSeriesJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, entity, created) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'InterpretTimeSeriesJob':
        return InterpretTimeSeriesJob(self.progress, self.status, self.error, self.message, self.entity, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'InterpretTimeSeriesJob':
        d['entity'] = InterpretTimeSeries.load(d['entity'])
        return InterpretTimeSeriesJob(**d)


class Interpretation:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, key, description, tmp_dir, scoring_package_path, binned_list, labels, parameters, training_duration, log_file_path, lime_rc_csv_path, shapley_rc_csv_path, shapley_orig_rc_csv_path, subtask_keys, dai_target_transformation, prediction_label) -> None:
        self.key = key
        self.description = description
        self.tmp_dir = tmp_dir
        self.scoring_package_path = scoring_package_path
        self.binned_list = binned_list
        self.labels = labels
        self.parameters = parameters
        self.training_duration = training_duration
        self.log_file_path = log_file_path
        self.lime_rc_csv_path = lime_rc_csv_path
        self.shapley_rc_csv_path = shapley_rc_csv_path
        self.shapley_orig_rc_csv_path = shapley_orig_rc_csv_path
        self.subtask_keys = subtask_keys
        self.dai_target_transformation = dai_target_transformation
        self.prediction_label = prediction_label

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['parameters'] = self.parameters.dump()
        d['subtask_keys'] = [a.dump() for a in self.subtask_keys]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'Interpretation':
        return Interpretation(self.key, self.description, self.tmp_dir, self.scoring_package_path, self.binned_list, self.labels, self.parameters, self.training_duration, self.log_file_path, self.lime_rc_csv_path, self.shapley_rc_csv_path, self.shapley_orig_rc_csv_path, self.subtask_keys, self.dai_target_transformation, self.prediction_label)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'Interpretation':
        d['parameters'] = InterpretParameters.load(d['parameters'])
        d['subtask_keys'] = [StrArrayEntry.load(a) for a in d['subtask_keys']]
        return Interpretation(**d)


class InterpretationJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, h2oprogress, mliprogress, status, error, message, entity, created) -> None:
        self.progress = progress
        self.h2oprogress = h2oprogress
        self.mliprogress = mliprogress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['h2oprogress'] = self.h2oprogress.dump()
        d['mliprogress'] = self.mliprogress.dump()
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'InterpretationJob':
        return InterpretationJob(self.progress, self.h2oprogress, self.mliprogress, self.status, self.error, self.message, self.entity, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'InterpretationJob':
        d['h2oprogress'] = H2OProgress.load(d['h2oprogress'])
        d['mliprogress'] = MLIProgress.load(d['mliprogress'])
        d['entity'] = Interpretation.load(d['entity'])
        return InterpretationJob(**d)


class ScoringPipeline:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, model_key, file_path) -> None:
        self.model_key = model_key
        self.file_path = file_path

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ScoringPipeline':
        return ScoringPipeline(self.model_key, self.file_path)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ScoringPipeline':
        return ScoringPipeline(**d)


class MojoPipeline:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, model_key, file_path) -> None:
        self.model_key = model_key
        self.file_path = file_path

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'MojoPipeline':
        return MojoPipeline(self.model_key, self.file_path)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'MojoPipeline':
        return MojoPipeline(**d)


class ScoringPipelineJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, entity, created) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ScoringPipelineJob':
        return ScoringPipelineJob(self.progress, self.status, self.error, self.message, self.entity, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ScoringPipelineJob':
        d['entity'] = ScoringPipeline.load(d['entity'])
        return ScoringPipelineJob(**d)


class MojoPipelineJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, entity, created) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'MojoPipelineJob':
        return MojoPipelineJob(self.progress, self.status, self.error, self.message, self.entity, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'MojoPipelineJob':
        d['entity'] = MojoPipeline.load(d['entity'])
        return MojoPipelineJob(**d)


class ExperimentArtifact:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, name, type, size, text, created) -> None:
        self.name = name
        self.type = type
        self.size = size
        self.text = text
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ExperimentArtifact':
        return ExperimentArtifact(self.name, self.type, self.size, self.text, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ExperimentArtifact':
        return ExperimentArtifact(**d)


class ExperimentArtifactSummary:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, artifacts, user_note, location, user) -> None:
        self.artifacts = artifacts
        self.user_note = user_note
        self.location = location
        self.user = user

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['artifacts'] = [a.dump() for a in self.artifacts]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ExperimentArtifactSummary':
        return ExperimentArtifactSummary(self.artifacts, self.user_note, self.location, self.user)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ExperimentArtifactSummary':
        d['artifacts'] = [ExperimentArtifact.load(a) for a in d['artifacts']]
        return ExperimentArtifactSummary(**d)


class ArtifactsExportJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, model_key, created) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.model_key = model_key
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ArtifactsExportJob':
        return ArtifactsExportJob(self.progress, self.status, self.error, self.message, self.model_key, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ArtifactsExportJob':
        return ArtifactsExportJob(**d)


class ExemplarRowsResponse:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, exemplar_id, headers, rows, totalRows) -> None:
        self.exemplar_id = exemplar_id
        self.headers = headers
        self.rows = rows
        self.totalRows = totalRows

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ExemplarRowsResponse':
        return ExemplarRowsResponse(self.exemplar_id, self.headers, self.rows, self.totalRows)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ExemplarRowsResponse':
        return ExemplarRowsResponse(**d)


class ConfigItem:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, name, description, comment, type, val, predefined, tags, min_, max_, category) -> None:
        self.name = name
        self.description = description
        self.comment = comment
        self.type = type
        self.val = val
        self.predefined = predefined
        self.tags = tags
        self.min_ = min_
        self.max_ = max_
        self.category = category

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ConfigItem':
        return ConfigItem(self.name, self.description, self.comment, self.type, self.val, self.predefined, self.tags, self.min_, self.max_, self.category)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ConfigItem':
        return ConfigItem(**d)


class ConfigOption:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, key, value, type, comment, desc, exposed, protected, enum, min, max, tags) -> None:
        self.key = key
        self.value = value
        self.type = type
        self.comment = comment
        self.desc = desc
        self.exposed = exposed
        self.protected = protected
        self.enum = enum
        self.min = min
        self.max = max
        self.tags = tags

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ConfigOption':
        return ConfigOption(self.key, self.value, self.type, self.comment, self.desc, self.exposed, self.protected, self.enum, self.min, self.max, self.tags)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ConfigOption':
        return ConfigOption(**d)


class ExperimentPreviewResponse:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, accuracy, time, interpretability, lines) -> None:
        self.accuracy = accuracy
        self.time = time
        self.interpretability = interpretability
        self.lines = lines

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ExperimentPreviewResponse':
        return ExperimentPreviewResponse(self.accuracy, self.time, self.interpretability, self.lines)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ExperimentPreviewResponse':
        return ExperimentPreviewResponse(**d)


class ExperimentPreviewJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, entity, created) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ExperimentPreviewJob':
        return ExperimentPreviewJob(self.progress, self.status, self.error, self.message, self.entity, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ExperimentPreviewJob':
        d['entity'] = ExperimentPreviewResponse.load(d['entity'])
        return ExperimentPreviewJob(**d)


class UserInfo:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, name) -> None:
        self.name = name

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'UserInfo':
        return UserInfo(self.name)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'UserInfo':
        return UserInfo(**d)


class TimeSeriesSplitSuggestion:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, period_ticks, gap_ticks, train_values, valid_values, alpha_values, train_samples, valid_samples, gapped_samples, total_periods, period_size, period_units, default_unit, threshold, test_gap, test_periods, frequency, frequency_unit) -> None:
        self.period_ticks = period_ticks
        self.gap_ticks = gap_ticks
        self.train_values = train_values
        self.valid_values = valid_values
        self.alpha_values = alpha_values
        self.train_samples = train_samples
        self.valid_samples = valid_samples
        self.gapped_samples = gapped_samples
        self.total_periods = total_periods
        self.period_size = period_size
        self.period_units = period_units
        self.default_unit = default_unit
        self.threshold = threshold
        self.test_gap = test_gap
        self.test_periods = test_periods
        self.frequency = frequency
        self.frequency_unit = frequency_unit

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'TimeSeriesSplitSuggestion':
        return TimeSeriesSplitSuggestion(self.period_ticks, self.gap_ticks, self.train_values, self.valid_values, self.alpha_values, self.train_samples, self.valid_samples, self.gapped_samples, self.total_periods, self.period_size, self.period_units, self.default_unit, self.threshold, self.test_gap, self.test_periods, self.frequency, self.frequency_unit)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'TimeSeriesSplitSuggestion':
        return TimeSeriesSplitSuggestion(**d)


class TimeSeriesSplitSuggestionJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, entity, created) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'TimeSeriesSplitSuggestionJob':
        return TimeSeriesSplitSuggestionJob(self.progress, self.status, self.error, self.message, self.entity, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'TimeSeriesSplitSuggestionJob':
        d['entity'] = TimeSeriesSplitSuggestion.load(d['entity'])
        return TimeSeriesSplitSuggestionJob(**d)


class AwsCredentials:
    """
    API for Mojo scorer deployment.
    Credentials for the AWS account to be used for the deployment.

    :param take_from_config: If true, the keys from the config file are used.
    """
    @ignore_unexpected_kwargs
    def __init__(self, take_from_config, access_key, secret_key) -> None:
        self.take_from_config = take_from_config
        self.access_key = access_key
        self.secret_key = secret_key

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'AwsCredentials':
        return AwsCredentials(self.take_from_config, self.access_key, self.secret_key)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'AwsCredentials':
        return AwsCredentials(**d)


class AwsLambdaParameters:
    """
    Parameters specific for the AWS lambda deployment.

    :param region: AWS region to deploy to.
    :param deployment_name: Unique deployment id. The id is used to name related AWS objects required by the lambda.
    """
    @ignore_unexpected_kwargs
    def __init__(self, region, deployment_name) -> None:
        self.region = region
        self.deployment_name = deployment_name

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'AwsLambdaParameters':
        return AwsLambdaParameters(self.region, self.deployment_name)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'AwsLambdaParameters':
        return AwsLambdaParameters(**d)


class LocalRestScorerParameters:
    """
    Parameters specific for local rest scorer deployed in DAI environment

    :param deployment_name: Unique deployment id
    :param port: Port number on which the rest server will be exposed on, default is 8080
    :param heap_size: Max heap size for jvm in GB, should be an integer, ex. 4
    """
    @ignore_unexpected_kwargs
    def __init__(self, deployment_name, port, heap_size) -> None:
        self.deployment_name = deployment_name
        self.port = port
        self.heap_size = heap_size

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'LocalRestScorerParameters':
        return LocalRestScorerParameters(self.deployment_name, self.port, self.heap_size)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'LocalRestScorerParameters':
        return LocalRestScorerParameters(**d)


class ScorerEndpoint:
    """

    :param base_url: Resulting root URL for the scorer API requests.
    :param api_key: Api key required by the scorer API. For AWS deployments, pass this in the x-api-key HTTP header.
    :param model_key: unique model hash from mojo. For local rest scorer deployments.
    """
    @ignore_unexpected_kwargs
    def __init__(self, base_url, api_key, model_key) -> None:
        self.base_url = base_url
        self.api_key = api_key
        self.model_key = model_key

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ScorerEndpoint':
        return ScorerEndpoint(self.base_url, self.api_key, self.model_key)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ScorerEndpoint':
        return ScorerEndpoint(**d)


class Deployment:
    """
    Represents one of the supported scorer deployment types

    :param key: Unique name of this deployment.
    :param model: Reference to the model this deployment represents.
    :param type: Determines on of the supported deployment types, e.g., AWS_LAMBDA.
    :param status: Status of the deployment, e.g., RUNNING, STOPPED.
    :param parameters: Serialized parameters fro the deployment, e.g., AwsLambdaParameters.
    :param credentials: Serialized credentials for the deployment provider, e.g., AwsCredentials.
    :param endpoint: Connection info for the deployment endpoint.
    :param pid: Process ID for deployments running locally.
    """
    @ignore_unexpected_kwargs
    def __init__(self, key, model, type, status, parameters, credentials, endpoint, pid) -> None:
        self.key = key
        self.model = model
        self.type = type
        self.status = status
        self.parameters = parameters
        self.credentials = credentials
        self.endpoint = endpoint
        self.pid = pid

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['model'] = self.model.dump()
        d['endpoint'] = self.endpoint.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'Deployment':
        return Deployment(self.key, self.model, self.type, self.status, self.parameters, self.credentials, self.endpoint, self.pid)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'Deployment':
        d['model'] = ModelReference.load(d['model'])
        d['endpoint'] = ScorerEndpoint.load(d['endpoint'])
        return Deployment(**d)


class CreateDeploymentJob:
    """

    :param entity: On success, holds the definition of the deployment.
    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, entity, created) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'CreateDeploymentJob':
        return CreateDeploymentJob(self.progress, self.status, self.error, self.message, self.entity, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'CreateDeploymentJob':
        d['entity'] = Deployment.load(d['entity'])
        return CreateDeploymentJob(**d)


class DestroyDeploymentJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, deployment_key, created) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.deployment_key = deployment_key
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DestroyDeploymentJob':
        return DestroyDeploymentJob(self.progress, self.status, self.error, self.message, self.deployment_key, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DestroyDeploymentJob':
        return DestroyDeploymentJob(**d)


class ListDeploymentQueryResponse:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, items, offset, limit, total_count) -> None:
        self.items = items
        self.offset = offset
        self.limit = limit
        self.total_count = total_count

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['items'] = [a.dump() for a in self.items]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ListDeploymentQueryResponse':
        return ListDeploymentQueryResponse(self.items, self.offset, self.limit, self.total_count)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ListDeploymentQueryResponse':
        d['items'] = [Deployment.load(a) for a in d['items']]
        return ListDeploymentQueryResponse(**d)


class ListModelDiagnosticQueryResponse:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, items, offset, limit, total_count) -> None:
        self.items = items
        self.offset = offset
        self.limit = limit
        self.total_count = total_count

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['items'] = [a.dump() for a in self.items]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ListModelDiagnosticQueryResponse':
        return ListModelDiagnosticQueryResponse(self.items, self.offset, self.limit, self.total_count)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ListModelDiagnosticQueryResponse':
        d['items'] = [ModelDiagnosticJob.load(a) for a in d['items']]
        return ListModelDiagnosticQueryResponse(**d)


class ModelDiagnosticJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, entity, created, training_duration) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created
        self.training_duration = training_duration

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ModelDiagnosticJob':
        return ModelDiagnosticJob(self.progress, self.status, self.error, self.message, self.entity, self.created, self.training_duration)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ModelDiagnosticJob':
        d['entity'] = ModelDiagnostic.load(d['entity'])
        return ModelDiagnosticJob(**d)


class ModelScore:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, model_key, score_f_name, score, score_mean, score_sd) -> None:
        self.model_key = model_key
        self.score_f_name = score_f_name
        self.score = score
        self.score_mean = score_mean
        self.score_sd = score_sd

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ModelScore':
        return ModelScore(self.model_key, self.score_f_name, self.score, self.score_mean, self.score_sd)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ModelScore':
        return ModelScore(**d)


class ModelDiagnostic:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, key, name, model, dataset, preds_csv_path, roc, gains, act_vs_pred, residual_plot, residual_loess, residual_hist, scores, scoring_duration) -> None:
        self.key = key
        self.name = name
        self.model = model
        self.dataset = dataset
        self.preds_csv_path = preds_csv_path
        self.roc = roc
        self.gains = gains
        self.act_vs_pred = act_vs_pred
        self.residual_plot = residual_plot
        self.residual_loess = residual_loess
        self.residual_hist = residual_hist
        self.scores = scores
        self.scoring_duration = scoring_duration

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['model'] = self.model.dump()
        d['dataset'] = self.dataset.dump()
        d['roc'] = self.roc.dump()
        d['gains'] = self.gains.dump()
        d['act_vs_pred'] = self.act_vs_pred.dump()
        d['residual_plot'] = self.residual_plot.dump()
        d['residual_loess'] = self.residual_loess.dump()
        d['residual_hist'] = self.residual_hist.dump()
        d['scores'] = [a.dump() for a in self.scores]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ModelDiagnostic':
        return ModelDiagnostic(self.key, self.name, self.model, self.dataset, self.preds_csv_path, self.roc, self.gains, self.act_vs_pred, self.residual_plot, self.residual_loess, self.residual_hist, self.scores, self.scoring_duration)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ModelDiagnostic':
        d['model'] = ModelReference.load(d['model'])
        d['dataset'] = DatasetReference.load(d['dataset'])
        d['roc'] = ROC.load(d['roc'])
        d['gains'] = GainLift.load(d['gains'])
        d['act_vs_pred'] = H2OPlot.load(d['act_vs_pred'])
        d['residual_plot'] = H2OPlot.load(d['residual_plot'])
        d['residual_loess'] = H2ORegression.load(d['residual_loess'])
        d['residual_hist'] = ResidualHistogram.load(d['residual_hist'])
        d['scores'] = [ModelScore.load(a) for a in d['scores']]
        return ModelDiagnostic(**d)


class ResidualHistogram:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, ticks, counts, mean, std) -> None:
        self.ticks = ticks
        self.counts = counts
        self.mean = mean
        self.std = std

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ResidualHistogram':
        return ResidualHistogram(self.ticks, self.counts, self.mean, self.std)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ResidualHistogram':
        return ResidualHistogram(**d)


class Project:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, key, name, description, train_datasets, test_datasets, validation_datasets, experiments, status, created) -> None:
        self.key = key
        self.name = name
        self.description = description
        self.train_datasets = train_datasets
        self.test_datasets = test_datasets
        self.validation_datasets = validation_datasets
        self.experiments = experiments
        self.status = status
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'Project':
        return Project(self.key, self.name, self.description, self.train_datasets, self.test_datasets, self.validation_datasets, self.experiments, self.status, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'Project':
        return Project(**d)


class ListProjectQueryResponse:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, items, offset, limit, total_count) -> None:
        self.items = items
        self.offset = offset
        self.limit = limit
        self.total_count = total_count

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['items'] = [a.dump() for a in self.items]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ListProjectQueryResponse':
        return ListProjectQueryResponse(self.items, self.offset, self.limit, self.total_count)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ListProjectQueryResponse':
        d['items'] = [Project.load(a) for a in d['items']]
        return ListProjectQueryResponse(**d)


class ProjectSummary:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, key, name, description) -> None:
        self.key = key
        self.name = name
        self.description = description

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ProjectSummary':
        return ProjectSummary(self.key, self.name, self.description)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ProjectSummary':
        return ProjectSummary(**d)


class ListStorageProjectQueryResponse:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, projects) -> None:
        self.projects = projects

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['projects'] = [a.dump() for a in self.projects]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ListStorageProjectQueryResponse':
        return ListStorageProjectQueryResponse(self.projects)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ListStorageProjectQueryResponse':
        d['projects'] = [ProjectSummary.load(a) for a in d['projects']]
        return ListStorageProjectQueryResponse(**d)


class ModelSummaryWithDiagnostics:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, summary, diagnostics) -> None:
        self.summary = summary
        self.diagnostics = diagnostics

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['summary'] = self.summary.dump()
        d['diagnostics'] = [a.dump() for a in self.diagnostics]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ModelSummaryWithDiagnostics':
        return ModelSummaryWithDiagnostics(self.summary, self.diagnostics)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ModelSummaryWithDiagnostics':
        d['summary'] = ModelSummary.load(d['summary'])
        d['diagnostics'] = [ModelDiagnostic.load(a) for a in d['diagnostics']]
        return ModelSummaryWithDiagnostics(**d)


class DatasetSplitJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, entity, created) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DatasetSplitJob':
        return DatasetSplitJob(self.progress, self.status, self.error, self.message, self.entity, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DatasetSplitJob':
        return DatasetSplitJob(**d)


class CreateCsvJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, status, url) -> None:
        self.status = status
        self.url = url

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['status'] = self.status.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'CreateCsvJob':
        return CreateCsvJob(self.status, self.url)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'CreateCsvJob':
        d['status'] = JobStatus.load(d['status'])
        return CreateCsvJob(**d)


class CustomRecipeJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, entity, created) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'CustomRecipeJob':
        return CustomRecipeJob(self.progress, self.status, self.error, self.message, self.entity, self.created)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'CustomRecipeJob':
        d['entity'] = CustomRecipe.load(d['entity'])
        return CustomRecipeJob(**d)


class CustomRecipe:
    """

    :param models: Freshly added model estimators
    :param scorers: Freshly added scorers
    :param transformers: Freshly added transformers
    :param data_files: Freshly created dataset files
    :param pretransformers: Freshly added pretransformers
    :param datas: Freshly added data recipes
    """
    @ignore_unexpected_kwargs
    def __init__(self, key, name, fpath, url, data_file, type, models, scorers, transformers, data_files, pretransformers, datas) -> None:
        self.key = key
        self.name = name
        self.fpath = fpath
        self.url = url
        self.data_file = data_file
        self.type = type
        self.models = models
        self.scorers = scorers
        self.transformers = transformers
        self.data_files = data_files
        self.pretransformers = pretransformers
        self.datas = datas

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['models'] = [a.dump() for a in self.models]
        d['scorers'] = [a.dump() for a in self.scorers]
        d['transformers'] = [a.dump() for a in self.transformers]
        d['pretransformers'] = [a.dump() for a in self.pretransformers]
        d['datas'] = [a.dump() for a in self.datas]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'CustomRecipe':
        return CustomRecipe(self.key, self.name, self.fpath, self.url, self.data_file, self.type, self.models, self.scorers, self.transformers, self.data_files, self.pretransformers, self.datas)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'CustomRecipe':
        d['models'] = [ModelEstimatorWrapper.load(a) for a in d['models']]
        d['scorers'] = [Scorer.load(a) for a in d['scorers']]
        d['transformers'] = [TransformerWrapper.load(a) for a in d['transformers']]
        d['pretransformers'] = [PreTransformerWrapper.load(a) for a in d['pretransformers']]
        d['datas'] = [DataWrapper.load(a) for a in d['datas']]
        return CustomRecipe(**d)


class OriginalShapleyJob:
    """
    Original Shapley

    """
    @ignore_unexpected_kwargs
    def __init__(self, mli_key, progress, status, error, message, entity, created, training_duration) -> None:
        self.mli_key = mli_key
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created
        self.training_duration = training_duration

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'OriginalShapleyJob':
        return OriginalShapleyJob(self.mli_key, self.progress, self.status, self.error, self.message, self.entity, self.created, self.training_duration)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'OriginalShapleyJob':
        d['entity'] = OriginalShapley.load(d['entity'])
        return OriginalShapleyJob(**d)


class OriginalShapley:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, key, name, mli_key, shapley_orig_rc_csv_path) -> None:
        self.key = key
        self.name = name
        self.mli_key = mli_key
        self.shapley_orig_rc_csv_path = shapley_orig_rc_csv_path

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'OriginalShapley':
        return OriginalShapley(self.key, self.name, self.mli_key, self.shapley_orig_rc_csv_path)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'OriginalShapley':
        return OriginalShapley(**d)


class OriginalShapleyParameters:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, model_key, mli_key, orig_shap_key, config_overrides, model_path, tmp_dir_path, dataset_path, mli_dir_path, classes, intr_params, orig_shap_entity, mojo_zip_path, wait_for_mojo, labels, actual_col, id_cols) -> None:
        validation.validate_toml(config_overrides, 'config_overrides')
        self.model_key = model_key
        self.mli_key = mli_key
        self.orig_shap_key = orig_shap_key
        self.config_overrides = config_overrides
        self.model_path = model_path
        self.tmp_dir_path = tmp_dir_path
        self.dataset_path = dataset_path
        self.mli_dir_path = mli_dir_path
        self.classes = classes
        self.intr_params = intr_params
        self.orig_shap_entity = orig_shap_entity
        self.mojo_zip_path = mojo_zip_path
        self.wait_for_mojo = wait_for_mojo
        self.labels = labels
        self.actual_col = actual_col
        self.id_cols = id_cols

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['intr_params'] = self.intr_params.dump()
        d['orig_shap_entity'] = self.orig_shap_entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'OriginalShapleyParameters':
        return OriginalShapleyParameters(self.model_key, self.mli_key, self.orig_shap_key, self.config_overrides, self.model_path, self.tmp_dir_path, self.dataset_path, self.mli_dir_path, self.classes, self.intr_params, self.orig_shap_entity, self.mojo_zip_path, self.wait_for_mojo, self.labels, self.actual_col, self.id_cols)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'OriginalShapleyParameters':
        d['intr_params'] = InterpretParameters.load(d['intr_params'])
        d['orig_shap_entity'] = OriginalShapley.load(d['orig_shap_entity'])
        return OriginalShapleyParameters(**d)


class DecisionTreeSurrogateJob:
    """
    Decision Tree Surrogate Model for MLI

    """
    @ignore_unexpected_kwargs
    def __init__(self, mli_key, progress, status, error, message, entity, created, training_duration) -> None:
        self.mli_key = mli_key
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created
        self.training_duration = training_duration

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DecisionTreeSurrogateJob':
        return DecisionTreeSurrogateJob(self.mli_key, self.progress, self.status, self.error, self.message, self.entity, self.created, self.training_duration)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DecisionTreeSurrogateJob':
        d['entity'] = DecisionTreeSurrogate.load(d['entity'])
        return DecisionTreeSurrogateJob(**d)


class DecisionTreeSurrogate:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, key, name, mli_key, dt_rules_zip_path) -> None:
        self.key = key
        self.name = name
        self.mli_key = mli_key
        self.dt_rules_zip_path = dt_rules_zip_path

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DecisionTreeSurrogate':
        return DecisionTreeSurrogate(self.key, self.name, self.mli_key, self.dt_rules_zip_path)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DecisionTreeSurrogate':
        return DecisionTreeSurrogate(**d)


class DecisionTreeSurrogateParameters:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, model_key, mli_key, dt_surrogate_key, config_overrides, model_path, tmp_dir_path, dataset_path, mli_dir_path, classes, intr_params, dt_surrogate_entity, mojo_zip_path, wait_for_mojo, labels, actual_col, predict_col, weights_col, dropped_cols, qbin_cols, qbin_count, debug_model_errors, debug_model_errors_class, unfitted_pipeline_path) -> None:
        validation.validate_toml(config_overrides, 'config_overrides')
        self.model_key = model_key
        self.mli_key = mli_key
        self.dt_surrogate_key = dt_surrogate_key
        self.config_overrides = config_overrides
        self.model_path = model_path
        self.tmp_dir_path = tmp_dir_path
        self.dataset_path = dataset_path
        self.mli_dir_path = mli_dir_path
        self.classes = classes
        self.intr_params = intr_params
        self.dt_surrogate_entity = dt_surrogate_entity
        self.mojo_zip_path = mojo_zip_path
        self.wait_for_mojo = wait_for_mojo
        self.labels = labels
        self.actual_col = actual_col
        self.predict_col = predict_col
        self.weights_col = weights_col
        self.dropped_cols = dropped_cols
        self.qbin_cols = qbin_cols
        self.qbin_count = qbin_count
        self.debug_model_errors = debug_model_errors
        self.debug_model_errors_class = debug_model_errors_class
        self.unfitted_pipeline_path = unfitted_pipeline_path

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['intr_params'] = self.intr_params.dump()
        d['dt_surrogate_entity'] = self.dt_surrogate_entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DecisionTreeSurrogateParameters':
        return DecisionTreeSurrogateParameters(self.model_key, self.mli_key, self.dt_surrogate_key, self.config_overrides, self.model_path, self.tmp_dir_path, self.dataset_path, self.mli_dir_path, self.classes, self.intr_params, self.dt_surrogate_entity, self.mojo_zip_path, self.wait_for_mojo, self.labels, self.actual_col, self.predict_col, self.weights_col, self.dropped_cols, self.qbin_cols, self.qbin_count, self.debug_model_errors, self.debug_model_errors_class, self.unfitted_pipeline_path)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DecisionTreeSurrogateParameters':
        d['intr_params'] = InterpretParameters.load(d['intr_params'])
        d['dt_surrogate_entity'] = DecisionTreeSurrogate.load(d['dt_surrogate_entity'])
        return DecisionTreeSurrogateParameters(**d)


class DisparateImpactAnalysisJob:
    """
    DISPARATE IMPACT ANALYSIS

    """
    @ignore_unexpected_kwargs
    def __init__(self, mli_key, progress, status, error, message, entity, created, training_duration) -> None:
        self.mli_key = mli_key
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created
        self.training_duration = training_duration

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DisparateImpactAnalysisJob':
        return DisparateImpactAnalysisJob(self.mli_key, self.progress, self.status, self.error, self.message, self.entity, self.created, self.training_duration)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DisparateImpactAnalysisJob':
        d['entity'] = DisparateImpactAnalysis.load(d['entity'])
        return DisparateImpactAnalysisJob(**d)


class DisparateImpactAnalysis:
    """

    :param global_conf_matrix: binomial
    """
    @ignore_unexpected_kwargs
    def __init__(self, key, name, mli_key, path, problem_type, summary, feature_summaries, global_conf_matrix) -> None:
        self.key = key
        self.name = name
        self.mli_key = mli_key
        self.path = path
        self.problem_type = problem_type
        self.summary = summary
        self.feature_summaries = feature_summaries
        self.global_conf_matrix = global_conf_matrix

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['summary'] = self.summary.dump()
        d['feature_summaries'] = [a.dump() for a in self.feature_summaries]
        d['global_conf_matrix'] = self.global_conf_matrix.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DisparateImpactAnalysis':
        return DisparateImpactAnalysis(self.key, self.name, self.mli_key, self.path, self.problem_type, self.summary, self.feature_summaries, self.global_conf_matrix)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DisparateImpactAnalysis':
        d['summary'] = DisparateImpactAnalysisSummary.load(d['summary'])
        d['feature_summaries'] = [DisparateImpactAnalysisFeatureSummary.load(a) for a in d['feature_summaries']]
        d['global_conf_matrix'] = DisparateImpactAnalysisNumericTable.load(d['global_conf_matrix'])
        return DisparateImpactAnalysis(**d)


class DisparateImpactAnalysisSummary:
    """

    :param max_metric: binomial
    :param cut_off: binomial
    :param rmse: regression
    :param r2: regression
    """
    @ignore_unexpected_kwargs
    def __init__(self, max_metric, cut_off, rmse, r2) -> None:
        self.max_metric = max_metric
        self.cut_off = cut_off
        self.rmse = rmse
        self.r2 = r2

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DisparateImpactAnalysisSummary':
        return DisparateImpactAnalysisSummary(self.max_metric, self.cut_off, self.rmse, self.r2)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DisparateImpactAnalysisSummary':
        return DisparateImpactAnalysisSummary(**d)


class DisparateImpactAnalysisFeatureSummary:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, feature_name, ref_levels) -> None:
        self.feature_name = feature_name
        self.ref_levels = ref_levels

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['feature_name'] = self.feature_name.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DisparateImpactAnalysisFeatureSummary':
        return DisparateImpactAnalysisFeatureSummary(self.feature_name, self.ref_levels)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DisparateImpactAnalysisFeatureSummary':
        d['feature_name'] = BoolEntry.load(d['feature_name'])
        return DisparateImpactAnalysisFeatureSummary(**d)


class DisparateImpactAnalysisNumericTable:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, name, col_names, row_names, values) -> None:
        self.name = name
        self.col_names = col_names
        self.row_names = row_names
        self.values = values

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DisparateImpactAnalysisNumericTable':
        return DisparateImpactAnalysisNumericTable(self.name, self.col_names, self.row_names, self.values)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DisparateImpactAnalysisNumericTable':
        return DisparateImpactAnalysisNumericTable(**d)


class DiaSummary:
    """
    Disparate Impact Analysis Summary Domain Object

    """
    @ignore_unexpected_kwargs
    def __init__(self, dia_features, mli_key, dia_key, problem_type, global_confusion_matrix) -> None:
        self.dia_features = dia_features
        self.mli_key = mli_key
        self.dia_key = dia_key
        self.problem_type = problem_type
        self.global_confusion_matrix = global_confusion_matrix

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['dia_features'] = [a.dump() for a in self.dia_features]
        d['global_confusion_matrix'] = self.global_confusion_matrix.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DiaSummary':
        return DiaSummary(self.dia_features, self.mli_key, self.dia_key, self.problem_type, self.global_confusion_matrix)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DiaSummary':
        d['dia_features'] = [BoolEntry.load(a) for a in d['dia_features']]
        d['global_confusion_matrix'] = DiaMatrix.load(d['global_confusion_matrix'])
        return DiaSummary(**d)


class DiaAvp:
    """
    Disparate Impact Analysis AvP Domain Object

    """
    @ignore_unexpected_kwargs
    def __init__(self, category_summary, metrics, avp) -> None:
        self.category_summary = category_summary
        self.metrics = metrics
        self.avp = avp

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['category_summary'] = [a.dump() for a in self.category_summary]
        d['metrics'] = [a.dump() for a in self.metrics]
        d['avp'] = [a.dump() for a in self.avp]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DiaAvp':
        return DiaAvp(self.category_summary, self.metrics, self.avp)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DiaAvp':
        d['category_summary'] = [DiaCategorySummary.load(a) for a in d['category_summary']]
        d['metrics'] = [DiaMetric.load(a) for a in d['metrics']]
        d['avp'] = [DiaAvpEntry.load(a) for a in d['avp']]
        return DiaAvp(**d)


class DiaCategorySummary:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, name, count, value) -> None:
        self.name = name
        self.count = count
        self.value = value

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DiaCategorySummary':
        return DiaCategorySummary(self.name, self.count, self.value)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DiaCategorySummary':
        return DiaCategorySummary(**d)


class DiaMetric:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, name, levels) -> None:
        self.name = name
        self.levels = levels

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['levels'] = [a.dump() for a in self.levels]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DiaMetric':
        return DiaMetric(self.name, self.levels)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DiaMetric':
        d['levels'] = [FloatEntry.load(a) for a in d['levels']]
        return DiaMetric(**d)


class DiaAvpEntry:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, actual, predicted, category) -> None:
        self.actual = actual
        self.predicted = predicted
        self.category = category

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DiaAvpEntry':
        return DiaAvpEntry(self.actual, self.predicted, self.category)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DiaAvpEntry':
        return DiaAvpEntry(**d)


class Dia:
    """
    Disparate Impact Analysis Domain Object

    """
    @ignore_unexpected_kwargs
    def __init__(self, summary, confusion_matrices, group_metrics, group_disparity, group_me_smd, group_parity, current_page, max_rows) -> None:
        self.summary = summary
        self.confusion_matrices = confusion_matrices
        self.group_metrics = group_metrics
        self.group_disparity = group_disparity
        self.group_me_smd = group_me_smd
        self.group_parity = group_parity
        self.current_page = current_page
        self.max_rows = max_rows

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['summary'] = self.summary.dump()
        d['confusion_matrices'] = [a.dump() for a in self.confusion_matrices]
        d['group_metrics'] = self.group_metrics.dump()
        d['group_disparity'] = [a.dump() for a in self.group_disparity]
        d['group_me_smd'] = [a.dump() for a in self.group_me_smd]
        d['group_parity'] = [a.dump() for a in self.group_parity]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'Dia':
        return Dia(self.summary, self.confusion_matrices, self.group_metrics, self.group_disparity, self.group_me_smd, self.group_parity, self.current_page, self.max_rows)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'Dia':
        d['summary'] = DiaFeatureSummary.load(d['summary'])
        d['confusion_matrices'] = [DiaNamedMatrix.load(a) for a in d['confusion_matrices']]
        d['group_metrics'] = DiaMatrix.load(d['group_metrics'])
        d['group_disparity'] = [DiaNamedMatrix.load(a) for a in d['group_disparity']]
        d['group_me_smd'] = [DiaNamedMatrix.load(a) for a in d['group_me_smd']]
        d['group_parity'] = [DiaNamedMatrix.load(a) for a in d['group_parity']]
        return Dia(**d)


class DiaNamedMatrix:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, name, matrix) -> None:
        self.name = name
        self.matrix = matrix

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['matrix'] = self.matrix.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DiaNamedMatrix':
        return DiaNamedMatrix(self.name, self.matrix)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DiaNamedMatrix':
        d['matrix'] = DiaMatrix.load(d['matrix'])
        return DiaNamedMatrix(**d)


class DiaFeatureSummary:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, dia_experiment, maximized_metric, cut_off, rmse, r2, ref_levels) -> None:
        self.dia_experiment = dia_experiment
        self.maximized_metric = maximized_metric
        self.cut_off = cut_off
        self.rmse = rmse
        self.r2 = r2
        self.ref_levels = ref_levels

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DiaFeatureSummary':
        return DiaFeatureSummary(self.dia_experiment, self.maximized_metric, self.cut_off, self.rmse, self.r2, self.ref_levels)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DiaFeatureSummary':
        return DiaFeatureSummary(**d)


class DiaMatrix:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, matrix) -> None:
        self.matrix = matrix

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['matrix'] = [a.dump() for a in self.matrix]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DiaMatrix':
        return DiaMatrix(self.matrix)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DiaMatrix':
        d['matrix'] = [DiaTableRow.load(a) for a in d['matrix']]
        return DiaMatrix(**d)


class DiaTableRow:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, values) -> None:
        self.values = values

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['values'] = [a.dump() for a in self.values]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DiaTableRow':
        return DiaTableRow(self.values)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DiaTableRow':
        d['values'] = [DiaTableColumn.load(a) for a in d['values']]
        return DiaTableRow(**d)


class DiaTableColumn:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, col_name, col_value) -> None:
        self.col_name = col_name
        self.col_value = col_value

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DiaTableColumn':
        return DiaTableColumn(self.col_name, self.col_value)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DiaTableColumn':
        return DiaTableColumn(**d)


class FloatEntry:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'FloatEntry':
        return FloatEntry(self.name, self.value)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'FloatEntry':
        return FloatEntry(**d)


class BoolEntry:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'BoolEntry':
        return BoolEntry(self.name, self.value)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'BoolEntry':
        return BoolEntry(**d)


class StrEntry:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'StrEntry':
        return StrEntry(self.name, self.value)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'StrEntry':
        return StrEntry(**d)


class StrArrayEntry:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'StrArrayEntry':
        return StrArrayEntry(self.name, self.value)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'StrArrayEntry':
        return StrArrayEntry(**d)


class MliSubtaskStatus:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, mli_key, subtask_name, status, training_duration) -> None:
        self.mli_key = mli_key
        self.subtask_name = subtask_name
        self.status = status
        self.training_duration = training_duration

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['status'] = self.status.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'MliSubtaskStatus':
        return MliSubtaskStatus(self.mli_key, self.subtask_name, self.status, self.training_duration)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'MliSubtaskStatus':
        d['status'] = JobStatus.load(d['status'])
        return MliSubtaskStatus(**d)


class MliNlpJob:
    """
    MLI NLP

    """
    @ignore_unexpected_kwargs
    def __init__(self, mli_key, progress, status, error, message, entity, created, training_duration) -> None:
        self.mli_key = mli_key
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created
        self.training_duration = training_duration

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'MliNlpJob':
        return MliNlpJob(self.mli_key, self.progress, self.status, self.error, self.message, self.entity, self.created, self.training_duration)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'MliNlpJob':
        d['entity'] = MliNlp.load(d['entity'])
        return MliNlpJob(**d)


class MliNlp:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, mli_nlp_key, mli_nlp_name, mli_key, mli_nlp_path) -> None:
        self.mli_nlp_key = mli_nlp_key
        self.mli_nlp_name = mli_nlp_name
        self.mli_key = mli_key
        self.mli_nlp_path = mli_nlp_path

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'MliNlp':
        return MliNlp(self.mli_nlp_key, self.mli_nlp_name, self.mli_key, self.mli_nlp_path)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'MliNlp':
        return MliNlp(**d)


class DataPreviewJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, created, entity, recipe_path, dataset_key) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.created = created
        self.entity = entity
        self.recipe_path = recipe_path
        self.dataset_key = dataset_key

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DataPreviewJob':
        return DataPreviewJob(self.progress, self.status, self.error, self.message, self.created, self.entity, self.recipe_path, self.dataset_key)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DataPreviewJob':
        d['entity'] = ExemplarRowsResponse.load(d['entity'])
        return DataPreviewJob(**d)


class DisparateImpactAnalysisParameters:
    """
    Used internally for do_dia job parameters

    """
    @ignore_unexpected_kwargs
    def __init__(self, model_key, mli_key, dia_key, config_overrides, model_path, tmp_dir_path, dataset_path, mli_dir_path, classes, intr_params, dia_entity, roc, labels, cut_off, path, actual_col, predict_column) -> None:
        validation.validate_toml(config_overrides, 'config_overrides')
        self.model_key = model_key
        self.mli_key = mli_key
        self.dia_key = dia_key
        self.config_overrides = config_overrides
        self.model_path = model_path
        self.tmp_dir_path = tmp_dir_path
        self.dataset_path = dataset_path
        self.mli_dir_path = mli_dir_path
        self.classes = classes
        self.intr_params = intr_params
        self.dia_entity = dia_entity
        self.roc = roc
        self.labels = labels
        self.cut_off = cut_off
        self.path = path
        self.actual_col = actual_col
        self.predict_column = predict_column

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['intr_params'] = self.intr_params.dump()
        d['dia_entity'] = self.dia_entity.dump()
        d['roc'] = self.roc.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DisparateImpactAnalysisParameters':
        return DisparateImpactAnalysisParameters(self.model_key, self.mli_key, self.dia_key, self.config_overrides, self.model_path, self.tmp_dir_path, self.dataset_path, self.mli_dir_path, self.classes, self.intr_params, self.dia_entity, self.roc, self.labels, self.cut_off, self.path, self.actual_col, self.predict_column)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DisparateImpactAnalysisParameters':
        d['intr_params'] = InterpretParameters.load(d['intr_params'])
        d['dia_entity'] = DisparateImpactAnalysis.load(d['dia_entity'])
        d['roc'] = ROC.load(d['roc'])
        return DisparateImpactAnalysisParameters(**d)


class MliVarImpTable:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, global_imp, local_imp) -> None:
        self.global_imp = global_imp
        self.local_imp = local_imp

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['global_imp'] = self.global_imp.dump()
        d['local_imp'] = self.local_imp.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'MliVarImpTable':
        return MliVarImpTable(self.global_imp, self.local_imp)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'MliVarImpTable':
        d['global_imp'] = VarImpTable.load(d['global_imp'])
        d['local_imp'] = VarImpTable.load(d['local_imp'])
        return MliVarImpTable(**d)


class SensitivityAnalysisJob:
    """
    Sensitivity analysis fork/join job.

    """
    @ignore_unexpected_kwargs
    def __init__(self, mli_key, progress, status, error, message, entity, created, training_duration) -> None:
        self.mli_key = mli_key
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.entity = entity
        self.created = created
        self.training_duration = training_duration

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'SensitivityAnalysisJob':
        return SensitivityAnalysisJob(self.mli_key, self.progress, self.status, self.error, self.message, self.entity, self.created, self.training_duration)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'SensitivityAnalysisJob':
        d['entity'] = SensitivityAnalysis.load(d['entity'])
        return SensitivityAnalysisJob(**d)


class SensitivityAnalysis:
    """
    Sensitivity analysis fork/join entity.

    """
    @ignore_unexpected_kwargs
    def __init__(self, key, name, mli_key, dai_key) -> None:
        self.key = key
        self.name = name
        self.mli_key = mli_key
        self.dai_key = dai_key

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'SensitivityAnalysis':
        return SensitivityAnalysis(self.key, self.name, self.mli_key, self.dai_key)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'SensitivityAnalysis':
        return SensitivityAnalysis(**d)


class SaDatasetSummary:
    """
    Sensitivity analysis dataset summary.

    """
    @ignore_unexpected_kwargs
    def __init__(self, name, size, rows, cols, types, features_meta, experiment_name, experiment_type, sampled_dataset) -> None:
        self.name = name
        self.size = size
        self.rows = rows
        self.cols = cols
        self.types = types
        self.features_meta = features_meta
        self.experiment_name = experiment_name
        self.experiment_type = experiment_type
        self.sampled_dataset = sampled_dataset

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['features_meta'] = [a.dump() for a in self.features_meta]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'SaDatasetSummary':
        return SaDatasetSummary(self.name, self.size, self.rows, self.cols, self.types, self.features_meta, self.experiment_name, self.experiment_type, self.sampled_dataset)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'SaDatasetSummary':
        d['features_meta'] = [SaFeatureMeta.load(a) for a in d['features_meta']]
        return SaDatasetSummary(**d)


class SaWorkingSetSummary:
    """
    Sensitivity analysis working set summary.

    """
    @ignore_unexpected_kwargs
    def __init__(self, name, size, rows, cols, types, experiment_name, experiment_type, sampled_dataset) -> None:
        self.name = name
        self.size = size
        self.rows = rows
        self.cols = cols
        self.types = types
        self.experiment_name = experiment_name
        self.experiment_type = experiment_type
        self.sampled_dataset = sampled_dataset

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'SaWorkingSetSummary':
        return SaWorkingSetSummary(self.name, self.size, self.rows, self.cols, self.types, self.experiment_name, self.experiment_type, self.sampled_dataset)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'SaWorkingSetSummary':
        return SaWorkingSetSummary(**d)


class SaPredsEntry:
    """
    Sensitivity analysis predictions entry. Category gives main chart color.

    """
    @ignore_unexpected_kwargs
    def __init__(self, actual, predicted, category) -> None:
        self.actual = actual
        self.predicted = predicted
        self.category = category

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'SaPredsEntry':
        return SaPredsEntry(self.actual, self.predicted, self.category)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'SaPredsEntry':
        return SaPredsEntry(**d)


class SaWorkingSetPreds:
    """
    Sensitivity analysis predictions.

    """
    @ignore_unexpected_kwargs
    def __init__(self, preds) -> None:
        self.preds = preds

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['preds'] = [a.dump() for a in self.preds]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'SaWorkingSetPreds':
        return SaWorkingSetPreds(self.preds)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'SaWorkingSetPreds':
        d['preds'] = [SaPredsEntry.load(a) for a in d['preds']]
        return SaWorkingSetPreds(**d)


class SaFeatureMeta:
    """
    Sensitivity analysis features metadata.

    """
    @ignore_unexpected_kwargs
    def __init__(self, name, type, min, max, mean, mode, sd, unique, importance) -> None:
        self.name = name
        self.type = type
        self.min = min
        self.max = max
        self.mean = mean
        self.mode = mode
        self.sd = sd
        self.unique = unique
        self.importance = importance

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'SaFeatureMeta':
        return SaFeatureMeta(self.name, self.type, self.min, self.max, self.mean, self.mode, self.sd, self.unique, self.importance)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'SaFeatureMeta':
        return SaFeatureMeta(**d)


class SaWorkingSetCell:
    """
    Sensitivity analysis working set (table) cell.
    TODO value:any type didn't worked (proto serializer failed) > string

    """
    @ignore_unexpected_kwargs
    def __init__(self, feature, value) -> None:
        self.feature = feature
        self.value = value

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'SaWorkingSetCell':
        return SaWorkingSetCell(self.feature, self.value)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'SaWorkingSetCell':
        return SaWorkingSetCell(**d)


class SaWorkingSetRow:
    """
    Sensitivity analysis working set (table) row.

    """
    @ignore_unexpected_kwargs
    def __init__(self, index, category, cells) -> None:
        self.index = index
        self.category = category
        self.cells = cells

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['cells'] = [a.dump() for a in self.cells]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'SaWorkingSetRow':
        return SaWorkingSetRow(self.index, self.category, self.cells)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'SaWorkingSetRow':
        d['cells'] = [SaWorkingSetCell.load(a) for a in d['cells']]
        return SaWorkingSetRow(**d)


class SaWorkingSet:
    """
    Sensitivity analysis working set (table).

    """
    @ignore_unexpected_kwargs
    def __init__(self, frame) -> None:
        self.frame = frame

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['frame'] = [a.dump() for a in self.frame]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'SaWorkingSet':
        return SaWorkingSet(self.frame)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'SaWorkingSet':
        d['frame'] = [SaWorkingSetRow.load(a) for a in d['frame']]
        return SaWorkingSet(**d)


class SaShape:
    """
    Sensitivity analysis working set shape.

    """
    @ignore_unexpected_kwargs
    def __init__(self, rows, cols) -> None:
        self.rows = rows
        self.cols = cols

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'SaShape':
        return SaShape(self.rows, self.cols)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'SaShape':
        return SaShape(**d)


class SaStatistics:
    """
    Sensitivity analysis predictions statistics (last, absolute/relative change)

    """
    @ignore_unexpected_kwargs
    def __init__(self, score, last_score, score_change, mode_prediction) -> None:
        self.score = score
        self.last_score = last_score
        self.score_change = score_change
        self.mode_prediction = mode_prediction

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'SaStatistics':
        return SaStatistics(self.score, self.last_score, self.score_change, self.mode_prediction)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'SaStatistics':
        return SaStatistics(**d)


class SaHistoryItem:
    """
    Sensitivity analysis history item.

    """
    @ignore_unexpected_kwargs
    def __init__(self, idx, in_progress, action, feature, scope, value) -> None:
        self.idx = idx
        self.in_progress = in_progress
        self.action = action
        self.feature = feature
        self.scope = scope
        self.value = value

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'SaHistoryItem':
        return SaHistoryItem(self.idx, self.in_progress, self.action, self.feature, self.scope, self.value)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'SaHistoryItem':
        return SaHistoryItem(**d)


class SaHistory:
    """
    Sensitivity analysis history.

    """
    @ignore_unexpected_kwargs
    def __init__(self, history) -> None:
        self.history = history

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['history'] = [a.dump() for a in self.history]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'SaHistory':
        return SaHistory(self.history)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'SaHistory':
        d['history'] = [SaHistoryItem.load(a) for a in d['history']]
        return SaHistory(**d)


class SaPredsHistoryChartDataPoint:
    """
    Sensitivity analysis history chart point.

    """
    @ignore_unexpected_kwargs
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'SaPredsHistoryChartDataPoint':
        return SaPredsHistoryChartDataPoint(self.x, self.y)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'SaPredsHistoryChartDataPoint':
        return SaPredsHistoryChartDataPoint(**d)


class SaPredsHistoryChartData:
    """
    Sensitivity analysis history chart data (points).

    """
    @ignore_unexpected_kwargs
    def __init__(self, points) -> None:
        self.points = points

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['points'] = [a.dump() for a in self.points]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'SaPredsHistoryChartData':
        return SaPredsHistoryChartData(self.points)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'SaPredsHistoryChartData':
        d['points'] = [SaPredsHistoryChartDataPoint.load(a) for a in d['points']]
        return SaPredsHistoryChartData(**d)


class SaMainChartDataPoint:
    """
    Sensitivity analysis main chart point. Structure field names are frontend
    driven to avoid conversion: x is prediction, y is feature value, cluster is
    category.

    """
    @ignore_unexpected_kwargs
    def __init__(self, x, y, cluster, ws_row) -> None:
        self.x = x
        self.y = y
        self.cluster = cluster
        self.ws_row = ws_row

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'SaMainChartDataPoint':
        return SaMainChartDataPoint(self.x, self.y, self.cluster, self.ws_row)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'SaMainChartDataPoint':
        return SaMainChartDataPoint(**d)


class SaMainChartData:
    """
    Sensitivity analysis main chart data (points).

    """
    @ignore_unexpected_kwargs
    def __init__(self, cut_off, feature, points) -> None:
        self.cut_off = cut_off
        self.feature = feature
        self.points = points

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['points'] = [a.dump() for a in self.points]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'SaMainChartData':
        return SaMainChartData(self.cut_off, self.feature, self.points)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'SaMainChartData':
        d['points'] = [SaMainChartDataPoint.load(a) for a in d['points']]
        return SaMainChartData(**d)


class Sa:
    """
    Sensitivity analysis snapshot structure

    """
    @ignore_unexpected_kwargs
    def __init__(self, hist_entry, dataset_summary, summary_row, main_chart, preds_history_chart, working_set_summary, working_set, stats, history) -> None:
        self.hist_entry = hist_entry
        self.dataset_summary = dataset_summary
        self.summary_row = summary_row
        self.main_chart = main_chart
        self.preds_history_chart = preds_history_chart
        self.working_set_summary = working_set_summary
        self.working_set = working_set
        self.stats = stats
        self.history = history

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['dataset_summary'] = self.dataset_summary.dump()
        d['summary_row'] = self.summary_row.dump()
        d['main_chart'] = self.main_chart.dump()
        d['preds_history_chart'] = self.preds_history_chart.dump()
        d['working_set_summary'] = self.working_set_summary.dump()
        d['working_set'] = self.working_set.dump()
        d['stats'] = self.stats.dump()
        d['history'] = self.history.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'Sa':
        return Sa(self.hist_entry, self.dataset_summary, self.summary_row, self.main_chart, self.preds_history_chart, self.working_set_summary, self.working_set, self.stats, self.history)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'Sa':
        d['dataset_summary'] = SaDatasetSummary.load(d['dataset_summary'])
        d['summary_row'] = SaWorkingSetRow.load(d['summary_row'])
        d['main_chart'] = SaMainChartData.load(d['main_chart'])
        d['preds_history_chart'] = SaPredsHistoryChartData.load(d['preds_history_chart'])
        d['working_set_summary'] = SaWorkingSetSummary.load(d['working_set_summary'])
        d['working_set'] = SaWorkingSet.load(d['working_set'])
        d['stats'] = SaStatistics.load(d['stats'])
        d['history'] = SaHistory.load(d['history'])
        return Sa(**d)


class Task:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, key, kind, owner) -> None:
        self.key = key
        self.kind = kind
        self.owner = owner

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'Task':
        return Task(self.key, self.kind, self.owner)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'Task':
        return Task(**d)


class Worker:
    """

    :param status: running, finished
    :param remote_tasks: only for large tasks
    :param remote_processors: only for large tasks
    """
    @ignore_unexpected_kwargs
    def __init__(self, healthy, ip, name, total_gpus, last_modified, status, remote_tasks, remote_processors) -> None:
        self.healthy = healthy
        self.ip = ip
        self.name = name
        self.total_gpus = total_gpus
        self.last_modified = last_modified
        self.status = status
        self.remote_tasks = remote_tasks
        self.remote_processors = remote_processors

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['remote_tasks'] = [a.dump() for a in self.remote_tasks]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'Worker':
        return Worker(self.healthy, self.ip, self.name, self.total_gpus, self.last_modified, self.status, self.remote_tasks, self.remote_processors)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'Worker':
        d['remote_tasks'] = [Task.load(a) for a in d['remote_tasks']]
        return Worker(**d)


class WorkerID:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, ip, name) -> None:
        self.ip = ip
        self.name = name

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'WorkerID':
        return WorkerID(self.ip, self.name)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'WorkerID':
        return WorkerID(**d)


class HealthResponse:
    """

    :param local_task_queue_size: Active tasks for each task queue
    """
    @ignore_unexpected_kwargs
    def __init__(self, healthy, local_task_queue_size, cpu_task_queue_size, gpu_task_queue_size, workers, worker_mode) -> None:
        self.healthy = healthy
        self.local_task_queue_size = local_task_queue_size
        self.cpu_task_queue_size = cpu_task_queue_size
        self.gpu_task_queue_size = gpu_task_queue_size
        self.workers = workers
        self.worker_mode = worker_mode

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['workers'] = [a.dump() for a in self.workers]
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'HealthResponse':
        return HealthResponse(self.healthy, self.local_task_queue_size, self.cpu_task_queue_size, self.gpu_task_queue_size, self.workers, self.worker_mode)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'HealthResponse':
        d['workers'] = [Worker.load(a) for a in d['workers']]
        return HealthResponse(**d)


class TaskQueueResponse:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, gpu_queue, cpu_queue) -> None:
        self.gpu_queue = gpu_queue
        self.cpu_queue = cpu_queue

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'TaskQueueResponse':
        return TaskQueueResponse(self.gpu_queue, self.cpu_queue)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'TaskQueueResponse':
        return TaskQueueResponse(**d)


class DataPreviewJob:
    """

    """
    @ignore_unexpected_kwargs
    def __init__(self, progress, status, error, message, created, entity, recipe_path, dataset_key) -> None:
        self.progress = progress
        self.status = status
        self.error = error
        self.message = message
        self.created = created
        self.entity = entity
        self.recipe_path = recipe_path
        self.dataset_key = dataset_key

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        d['entity'] = self.entity.dump()
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'DataPreviewJob':
        return DataPreviewJob(self.progress, self.status, self.error, self.message, self.created, self.entity, self.recipe_path, self.dataset_key)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'DataPreviewJob':
        d['entity'] = ExemplarRowsResponse.load(d['entity'])
        return DataPreviewJob(**d)


class EntitySortQuery:
    """

    :param path: Path to nested field in entity, e.g. $.entity.file_size
    :param type: Type of field: 'value', 'array' or 'reference'
    :param reference_type: Kind of entity which is referenced, e.g. Model. Must be defined in `Kind` enum
    """
    @ignore_unexpected_kwargs
    def __init__(self, path, type, reference_type) -> None:
        self.path = path
        self.type = type
        self.reference_type = reference_type

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'EntitySortQuery':
        return EntitySortQuery(self.path, self.type, self.reference_type)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'EntitySortQuery':
        return EntitySortQuery(**d)


class PendingJobsListItem:
    """
    Entity used by frontend to persist content of side panel pending items.
    Pending item is understood as item which may require some kind of action, like click to download, or click to navigate to MLI

    :param key: Pending item key
    :param is_pending: If the job to which this pending item corresponds is still running
    :param title: Display name
    :param description: Longer job description
    :param job_key: Job key for polling function
    :param url: URL to page where pending item is running (e.g. experiment link, or prediction csv link)
    :param remotePollingProcedure: Procedure for polling progress of Async Job
    :param remoteAbortProcedure: Procedure to abort Async Job
    """
    @ignore_unexpected_kwargs
    def __init__(self, key, is_pending, title, description, job_key, url, remotePollingProcedure, remoteAbortProcedure) -> None:
        self.key = key
        self.is_pending = is_pending
        self.title = title
        self.description = description
        self.job_key = job_key
        self.url = url
        self.remotePollingProcedure = remotePollingProcedure
        self.remoteAbortProcedure = remoteAbortProcedure

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'PendingJobsListItem':
        return PendingJobsListItem(self.key, self.is_pending, self.title, self.description, self.job_key, self.url, self.remotePollingProcedure, self.remoteAbortProcedure)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'PendingJobsListItem':
        return PendingJobsListItem(**d)


class ColumnQuery:
    """

    :param value: Value of the column, case insensitive!
    """
    @ignore_unexpected_kwargs
    def __init__(self, column_name, value) -> None:
        self.column_name = column_name
        self.value = value

    @ignore_unexpected_kwargs
    def dump(self) -> dict:
        d = {k: v for k, v in vars(self).items()}
        return d

    @ignore_unexpected_kwargs
    def clone(self) -> 'ColumnQuery':
        return ColumnQuery(self.column_name, self.value)

    @staticmethod
    @ignore_unexpected_kwargs
    def load(d: dict) -> 'ColumnQuery':
        return ColumnQuery(**d)


# PATCHES
from . import messages_patches_1_9

# 1.9.0 - 1.9.0.6
ModelParameters = messages_patches_1_9.ModelParameters

# 1.9.0 - 1.9.2.1
GbqCreateDatasetArgs = messages_patches_1_9.GbqCreateDatasetArgs_up_to_1_9_2_1

# 1.9
SnowCreateDatasetArgs = messages_patches_1_9.SnowCreateDatasetArgs