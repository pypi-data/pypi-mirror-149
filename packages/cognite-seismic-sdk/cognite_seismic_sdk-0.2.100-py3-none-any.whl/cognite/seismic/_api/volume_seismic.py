# Copyright 2019 Cognite AS

import os
from typing import *

import numpy as np
from cognite.seismic._api.api import API
from cognite.seismic._api.utility import Direction, LineRange, MaybeString, get_identifier, get_search_spec
from cognite.seismic.data_classes.api_types import Geometry, InterpolationMethod, RangeInclusive, Trace, VolumeDef

if not os.getenv("READ_THE_DOCS"):
    from cognite.seismic.protos.types_pb2 import GeoJson
    from cognite.seismic.protos.types_pb2 import Geometry as GeometryProto
    from cognite.seismic.protos.types_pb2 import LineDescriptor
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import LineBasedVolume, OptionalMap
    from cognite.seismic.protos.v1.seismic_service_messages_pb2 import (
        GeometryBasedVolume,
        SearchSeismicsRequest,
        SearchSeismicStoresRequest,
        VolumeRequest,
    )
    from google.protobuf.wrappers_pb2 import Int32Value as i32
    from google.protobuf.wrappers_pb2 import StringValue
else:
    from cognite.seismic._api.shims import LineDescriptor


class ArrayData(NamedTuple):
    """Encapsulates the array returned from :py:meth:`VolumeSeismicAPI.get_array`, along with metadata about coordinates.

    Attributes:
        volume_data: 3D Array containing the requested volume data
        crs: The coordinate system used
        coord_x: 2D array containing the x coordinate of each (inline, xline) pair
        coord_y: 2D array containing the y coordinate of each (inline, xline) pair
        inline_range: The range of inline ids described by the first dimension of the array, or None if the result is empty
        xline_range: The range of xline ids described by the second dimension of the array, or None if the result is empty
        z_range: The range of depth indices described by the third dimension of the array, or None if the result is empty
    """

    volume_data: np.ma.MaskedArray
    crs: str
    coord_x: np.ma.MaskedArray
    coord_y: np.ma.MaskedArray
    inline_range: Optional[RangeInclusive]
    xline_range: Optional[RangeInclusive]
    z_range: Optional[RangeInclusive]

    def __repr__(self) -> str:
        return (
            f"ArrayData(volume_data=<array of shape {self.volume_data.shape}>, "
            f"crs={repr(self.crs)}, "
            f"coord_x=<array of shape {self.coord_x.shape}>, "
            f"coord_y=<array of shape {self.coord_x.shape}>, "
            f"inline_range={repr(self.inline_range)}, "
            f"xline_range={repr(self.xline_range)}, "
            f"z_range={repr(self.z_range)})"
        )


class GetVolumeSize(NamedTuple):
    """Information about the size returned from get_volume.

    Attributes:
        trace_count: The number of traces that will be streamed
        sample_count: The number of samples in each trace, if available
        size_kilobytes: An estimate of the total streaming size in kilobytes (= 1024 bytes),
                        or None if sample_count is None
    """

    trace_count: int
    sample_count: Optional[int]
    size_kilobytes: Optional[int]


class VolumeSeismicAPI(API):
    def __init__(self, query, ingestion):
        super().__init__(query=query, ingestion=ingestion)

    def get_volume(
        self,
        *,
        id: Optional[int] = None,
        external_id: MaybeString = None,
        seismic_store_id: Optional[int] = None,
        inline_range: Optional[LineRange] = None,
        xline_range: Optional[LineRange] = None,
        z_range: Optional[LineRange] = None,
        geometry: Optional[Geometry] = None,
        interpolation_method: Optional[InterpolationMethod] = None,
        include_trace_header: bool = False,
    ) -> Iterable[Trace]:
        """Retrieve traces from a seismic or seismic store

        Provide one of: the seismic id, the seismic external id, the seismic store id.
        The line ranges are specified as tuples of either (start, end) or (start, end, step).
        If a line range is not specified, the maximum ranges will be assumed.

        Args:
            id (int | None): The id of the seismic to query
            external_id (str | None): The external id of the seismic to query
            seismic_store_id (int | None): The id of the seismic store to query
            inline_range ([int, int] | [int, int, int] | None): The inline range
            xline_range ([int, int] | [int, int, int] | None): The xline range
            z_range ([int, int] | [int, int, int]): The range of samples to include
            include_trace-header (bool): Whether to include trace header info in the response.

        Returns:
            Iterable[:py:class:`~cognite.seismic.data_classes.api_types.Trace`], the traces for the specified volume
        """
        req = _build_volume_request(
            id,
            external_id,
            seismic_store_id,
            inline_range,
            xline_range,
            z_range,
            geometry,
            interpolation_method,
            include_trace_header,
        )
        for proto in self.query.GetVolume(req):
            yield Trace.from_proto(proto)

    def get_volume_size(
        self,
        *,
        id: Optional[int] = None,
        external_id: MaybeString = None,
        seismic_store_id: Optional[int] = None,
        inline_range: Optional[LineRange] = None,
        xline_range: Optional[LineRange] = None,
        z_range: Optional[LineRange] = None,
        geometry: Optional[Geometry] = None,
        interpolation_method: Optional[InterpolationMethod] = None,
        include_trace_header: bool = False,
    ) -> GetVolumeSize:
        """Estimate the total size of data streamed by get_volume

        Parameters: See :py:meth:`VolumeSeismicAPI.get_volume`

        Returns:
            A :py:class:`~GetVolumeSize` object describing the size
        """
        req = _build_volume_request(
            id,
            external_id,
            seismic_store_id,
            inline_range,
            xline_range,
            z_range,
            geometry,
            interpolation_method,
            include_trace_header,
        )
        volume_bounds = self.query.GetVolumeBounds(req)

        sample_count = volume_bounds.sample_count
        size_kilobytes = (volume_bounds.trace_size_bytes * volume_bounds.num_traces) // 1024

        return GetVolumeSize(
            trace_count=volume_bounds.num_traces, sample_count=sample_count, size_kilobytes=size_kilobytes
        )

    # Refuse to allocate arrays larger than this
    # FIXME(audunska): Figure out the right limit here, or maybe just use numpy's memory limit
    ARR_LIM = 1e8

    def get_array(
        self,
        *,
        id: Optional[int] = None,
        external_id: MaybeString = None,
        seismic_store_id: Optional[int] = None,
        inline_range: Optional[LineRange] = None,
        xline_range: Optional[LineRange] = None,
        z_range: Optional[LineRange] = None,
        geometry: Optional[Geometry] = None,
        interpolation_method: Optional[InterpolationMethod] = None,
        progress: Optional[bool] = False,
    ) -> ArrayData:
        """Store traces from a seismic or seismic store into a numpy array

        Provide one of: the seismic id, the seismic external id, the seismic store id.
        The line ranges are specified as tuples of either (start, end) or (start, end, step).
        If a line range is not specified, the maximum ranges will be assumed.

        Args:
            id (int | None): The id of the seismic to query
            external_id (str | None): The external id of the seismic to query
            seismic_store_id (int | None): The id of the seismic store to query
            inline_range ([int, int] | [int, int, int] | None): The inline range
            xline_range ([int, int] | [int, int, int] | None): The xline range
            z_range ([int, int] | [int, int, int]): The range of samples to include
            progress: (bool): If set to true, display a progress bar. Default: False

        Returns:
            An :py:class:`~ArrayData` object encapsulating the retrieved array (see below)
        """

        req = _build_volume_request(
            id, external_id, seismic_store_id, inline_range, xline_range, z_range, geometry, interpolation_method
        )
        volume_bounds = self.query.GetVolumeBounds(req)
        z_size = volume_bounds.sample_count

        if not volume_bounds.HasField("bounds"):
            # Not traces to stream, so return early
            volume_data = np.ma.masked_all((0, 0, z_size), dtype="float")
            coord_x = np.ma.masked_all((0, 0), dtype="float")
            coord_y = np.ma.masked_all((0, 0), dtype="float")
            return ArrayData(
                volume_data=volume_data,
                coord_x=coord_x,
                coord_y=coord_y,
                crs=volume_bounds.crs,
                inline_range=None,
                xline_range=None,
                z_range=None,
            )

        bounds = volume_bounds.bounds
        if not bounds.HasField("iline") or not bounds.HasField("xline"):
            raise ValueError("get_array not supported for linear geometries")

        inline_range = RangeInclusive.from_proto(bounds.iline)
        xline_range = RangeInclusive.from_proto(bounds.xline)
        z_range = RangeInclusive.from_proto(bounds.z)

        inline_size = len(inline_range)
        xline_size = len(xline_range)

        crs = volume_bounds.crs

        if inline_size * xline_size * z_size > self.ARR_LIM:
            raise ValueError(
                f"Array of size ({inline_size},{xline_size},{z_size}) has more than {self.ARR_LIM} elements. Consider restricting the array using inline_range etc."
            )

        volume_data = np.ma.masked_all((inline_size, xline_size, z_size), dtype="float")

        coord_x = np.ma.masked_all((inline_size, xline_size), dtype="float")
        coord_y = np.ma.masked_all((inline_size, xline_size), dtype="float")

        # Fetch data
        traces = self.query.GetVolume(req)

        if progress:
            try:
                from tqdm.auto import tqdm
            except ImportError:
                raise Exception("progress=True requires the tqdm package. Install with 'pip install tqdm'.")
            traces = tqdm(traces, total=volume_bounds.num_traces)

        for trace in traces:
            inline_ind = inline_range.index(trace.iline.value)
            xline_ind = xline_range.index(trace.xline.value)
            volume_data[inline_ind, xline_ind, :] = trace.trace
            coord_x[inline_ind, xline_ind] = trace.coordinate.x
            coord_y[inline_ind, xline_ind] = trace.coordinate.y
        return ArrayData(
            volume_data=volume_data,
            crs=crs,
            coord_x=coord_x,
            coord_y=coord_y,
            inline_range=inline_range,
            xline_range=xline_range,
            z_range=z_range,
        )


def into_line_range(linerange: Optional[LineRange]) -> LineDescriptor:
    "Converts a tuple of two or three values into a LineDescriptor"
    if linerange is None:
        return None
    if len(linerange) == 2:
        start, stop = linerange
        return LineDescriptor(min=i32(value=start), max=i32(value=stop))
    if len(linerange) == 3:
        start, stop, step = linerange
        return LineDescriptor(min=i32(value=start), max=i32(value=stop), step=i32(value=step))
    raise Exception("A line range should be None, (int, int), or (int, int, int).")


def _build_volume_request(
    id: Optional[int] = None,
    external_id: MaybeString = None,
    seismic_store_id: Optional[int] = None,
    inline_range: Optional[LineRange] = None,
    xline_range: Optional[LineRange] = None,
    z_range: Optional[LineRange] = None,
    geometry: Optional[Geometry] = None,
    interpolation_method: Optional[InterpolationMethod] = None,
    include_trace_header: Optional[bool] = None,
) -> "VolumeRequest":
    zline = into_line_range(z_range)
    req = VolumeRequest(include_trace_header=include_trace_header)
    if geometry is not None:
        if inline_range is not None or xline_range is not None:
            raise ValueError("Specifying both inline or xline ranges and geometry is not supported")
        interpolation_method = 0 if interpolation_method is None else interpolation_method.value
        req.geometry.MergeFrom(
            GeometryBasedVolume(geometry=geometry.to_proto(), interpolation_method=interpolation_method, z_range=zline)
        )
    else:
        inline = into_line_range(inline_range)
        xline = into_line_range(xline_range)
        req.volume.MergeFrom(LineBasedVolume(iline=inline, xline=xline, z=zline))

    if seismic_store_id:
        req.seismic_store_id = seismic_store_id
    else:
        req.seismic.MergeFrom(get_identifier(id, external_id))
    return req
