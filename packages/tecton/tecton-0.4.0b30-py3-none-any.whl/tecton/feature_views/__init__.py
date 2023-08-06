# nopycln: file
from tecton_spark import conf as _conf

if not _conf.get_bool("ALPHA_SNOWFLAKE_COMPUTE_ENABLED"):
    from tecton.feature_views.feature_view import batch_feature_view
    from tecton.feature_views.feature_view import batch_window_aggregate_feature_view
from tecton.feature_views.feature_view import FeatureDefinition
from tecton.feature_views.feature_view import Input
from tecton.feature_views.feature_view import MaterializedFeatureView
from tecton.feature_views.feature_view import on_demand_feature_view
from tecton.feature_views.feature_view import OnDemandFeatureView
from tecton.feature_views.feature_view import stream_feature_view
from tecton.feature_views.feature_view import stream_window_aggregate_feature_view
from tecton.data_sources.request_data_source import RequestDataSource
