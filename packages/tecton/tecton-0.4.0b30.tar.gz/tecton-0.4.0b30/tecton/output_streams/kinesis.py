from typing import Dict
from typing import Optional

from tecton.output_streams.base import OutputStream
from tecton_proto.args import data_source_pb2
from tecton_proto.args import feature_view_pb2


class KinesisOutputStream(OutputStream):
    """
    Configuration used for a Kinesis output stream.
    """

    def __init__(
        self, stream_name: str, region: str, options: Optional[Dict[str, str]] = None, include_features: bool = False
    ):
        """
        Instantiates a new KinesisDSConfig.

        :param stream_name: Name of the Kinesis stream.
        :param region: AWS region of the stream, e.g: "us-west-2".
        :param options: (Optional) A map of additional Spark readStream options. Only `roleArn` is supported.
        :param include_features: Return feature values in addition to entity keys. Not supported for window aggregate Feature Views.

        :return: A KinesisOutputStream object
        """
        args = data_source_pb2.KinesisDataSourceArgs()
        args.stream_name = stream_name
        args.region = region
        options_ = options or {}
        for key in sorted(options_.keys()):
            option = data_source_pb2.Option()
            option.key = key
            option.value = options_[key]
            args.options.append(option)

        output_config = feature_view_pb2.OutputStreamConfig()
        output_config.include_features = include_features
        output_config.kinesis.CopyFrom(args)

        self._args = output_config

    def _to_proto(self) -> feature_view_pb2.OutputStreamConfig:
        return self._args
