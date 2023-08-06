from daipecore.decorator.DecoratedDecorator import DecoratedDecorator
from pysparkbundle.write.PathWriterDecorator import PathWriterDecorator


@DecoratedDecorator  # pylint: disable = invalid-name
class parquet_write_ignore(PathWriterDecorator):
    _mode = "ignore"
    _writer_service = "pysparkbundle.parquet.writer"
