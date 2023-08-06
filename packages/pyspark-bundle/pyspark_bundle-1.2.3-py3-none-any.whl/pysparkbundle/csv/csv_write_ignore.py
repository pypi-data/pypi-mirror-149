from daipecore.decorator.DecoratedDecorator import DecoratedDecorator
from pysparkbundle.write.PathWriterDecorator import PathWriterDecorator


@DecoratedDecorator  # pylint: disable = invalid-name
class csv_write_ignore(PathWriterDecorator):
    _mode = "ignore"
    _writer_service = "pysparkbundle.csv.writer"
