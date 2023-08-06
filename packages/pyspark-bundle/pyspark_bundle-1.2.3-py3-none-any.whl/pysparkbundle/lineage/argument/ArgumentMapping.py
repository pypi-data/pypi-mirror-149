from daipecore.lineage.argument.ArgumentMappingInterface import ArgumentMappingInterface
from pysparkbundle.csv.lineage.CsvRead import CsvRead
from pysparkbundle.delta.lineage.DeltaRead import DeltaRead
from pysparkbundle.json.lineage.JsonRead import JsonRead
from pysparkbundle.parquet.lineage.ParquetRead import ParquetRead


class ArgumentMapping(ArgumentMappingInterface):
    def get_mapping(self):
        return {
            "read_csv": CsvRead,
            "read_json": JsonRead,
            "read_parquet": ParquetRead,
            "read_delta": DeltaRead,
        }
