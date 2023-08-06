#### File with proto types for Pix+ services.

In order to push changes to the `proto_pixplus_pb2.py`, be sure that:

- The `proto_pixplus.proto` file contains the changes, which were compiled **successfully**.
- New .py file is compiled and overwritten `proto_pixplus_pb2.py` module with current

Please, import needed types with an `ptype` alias
```shell
import proto_pixplus_pb2 as ptype
```