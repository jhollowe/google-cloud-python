
transport inheritance structure
_______________________________

`VpcFlowLogsServiceTransport` is the ABC for all transports.
- public child `VpcFlowLogsServiceGrpcTransport` for sync gRPC transport (defined in `grpc.py`).
- public child `VpcFlowLogsServiceGrpcAsyncIOTransport` for async gRPC transport (defined in `grpc_asyncio.py`).
- private child `_BaseVpcFlowLogsServiceRestTransport` for base REST transport with inner classes `_BaseMETHOD` (defined in `rest_base.py`).
- public child `VpcFlowLogsServiceRestTransport` for sync REST transport with inner classes `METHOD` derived from the parent's corresponding `_BaseMETHOD` classes (defined in `rest.py`).
