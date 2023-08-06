from typing import List
from box import Box
from injecta.dtype.DType import DType
from injecta.service.Service import Service
from injecta.service.ServiceAlias import ServiceAlias
from injecta.service.argument.PrimitiveArgument import PrimitiveArgument
from injecta.service.argument.ServiceArgument import ServiceArgument
from pyfonybundles.Bundle import Bundle
from daipecore.detector import is_cli
from pysparkbundle.lineage.PathWriterParser import PathWriterParser
from pysparkbundle.read.PathReader import PathReader
from pysparkbundle.write.PathWriter import PathWriter


class PySparkBundle(Bundle):
    def modify_services(self, services: List[Service], aliases: List[ServiceAlias], parameters: Box):
        formats = ["delta", "parquet", "json", "csv"]

        path_readers = [self.__create_path_reader(format_name) for format_name in formats]
        path_writers = [self.__create_path_writer(format_name) for format_name in formats]
        decorator_parsers = [
            self.__create_decorator_parser(format_name, operation) for format_name in formats for operation in ["append", "overwrite"]
        ]

        return services + path_readers + path_writers + decorator_parsers, aliases

    def modify_parameters(self, parameters: Box) -> Box:
        if is_cli():
            parameters.pysparkbundle.dataframe.show_method = "dataframe_show"
        return parameters

    def __create_path_reader(self, format_name: str):
        return Service(
            f"pysparkbundle.{format_name}.reader",
            DType(PathReader.__module__, "PathReader"),
            [PrimitiveArgument(format_name), ServiceArgument("pysparkbundle.logger")],
        )

    def __create_path_writer(self, format_name: str):
        return Service(
            f"pysparkbundle.{format_name}.writer",
            DType(PathWriter.__module__, "PathWriter"),
            [PrimitiveArgument(format_name), ServiceArgument("pysparkbundle.logger")],
        )

    def __create_decorator_parser(self, format_name: str, operation: str):
        return Service(
            f"pysparkbundle.lineage.{format_name}.parser.{operation}",
            DType(PathWriterParser.__module__, "PathWriterParser"),
            [PrimitiveArgument(format_name + "_" + operation), PrimitiveArgument(operation)],
            tags=["lineage.decorator.parser"],
        )
