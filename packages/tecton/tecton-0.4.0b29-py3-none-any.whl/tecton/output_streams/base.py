from abc import ABC
from abc import abstractmethod

from tecton_proto.args import feature_view_pb2


class OutputStream(ABC):
    @abstractmethod
    def _to_proto() -> feature_view_pb2.OutputStreamConfig:
        pass
