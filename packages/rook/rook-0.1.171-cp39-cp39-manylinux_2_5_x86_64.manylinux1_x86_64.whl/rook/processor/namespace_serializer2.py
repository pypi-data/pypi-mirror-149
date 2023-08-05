import datetime
import traceback
import decimal
from six.moves.collections_abc import Iterable

from types import TracebackType

import six

from google.protobuf.internal.type_checkers import Int64ValueChecker
from rook.processor.namespace_serializer_base import NamespaceSerializerBase

from .namespaces.container_namespace import ContainerNamespace
from .namespaces.python_object_namespace import PythonObjectNamespace
from .namespaces.collection_namespace import ListNamespace, LIST_TYPE
from .namespaces.traceback_namespace import TracebackNamespace
from .namespaces.error_namespace import ErrorNamespace
from .namespaces.formatted_namespace import FormattedNamespace

from rook.logger import logger

from rook.protobuf import variant_pb2, variant2_pb2

from ..user_warnings import UserWarnings


class NamespaceSerializer2(NamespaceSerializerBase):
    def __init__(self):
        NamespaceSerializerBase.__init__(self, True)
        self.buffer_cache = {}

    def dump(self, namespace, variant, log_errors=True):
        try:
            if isinstance(namespace, ContainerNamespace):
                self._dump_container_namespace(namespace, variant, log_errors)
            elif isinstance(namespace, PythonObjectNamespace):
                self._dump_object_namespace(namespace, variant, log_errors)
            elif isinstance(namespace, ErrorNamespace):
                self._dump_error_namespace(namespace, variant, log_errors)
            elif isinstance(namespace, FormattedNamespace):
                self._dump_formatted_namespace(namespace, variant, log_errors)
            elif isinstance(namespace, TracebackNamespace):
                self._dump_traceback_namespace(namespace, variant, log_errors)
            else:
                raise NotImplementedError("Does not support serializing this type!", type(namespace))
        except Exception as e:
            message = "Failed to serialize namespace"

            variant.Clear()
            NamespaceSerializer2.dump_variant_type(variant, variant_pb2.Variant.VARIANT_ERROR)

            if log_errors:
                from .error import Error
                logger.exception(message)
                UserWarnings.send_warning(Error(exc=e, message=message))

    def dumps(self, namespace, log_errors=True):
        variant = variant2_pb2.Variant2()
        self.dump(namespace, variant, log_errors)
        return variant

    def _dump_container_namespace(self, namespace, variant, log_errors):
        self.dump_variant_type(variant, variant_pb2.Variant.VARIANT_NAMESPACE)

        for key, value in six.iteritems(namespace.dictionary):
            variant.attribute_names_in_cache.append(self._get_string_index_in_cache(key))
            attribute_value = variant.attribute_values.add()
            self.dump(value, attribute_value, log_errors)

    def _dump_object_namespace(self, namespace, variant, log_errors):
        self._dump_python_object(namespace.obj, variant, 0, namespace.dump_config, log_errors)

    def _dump_formatted_namespace(self, namespace, variant, log_errors):
        NamespaceSerializer2.dump_variant_type(variant, variant_pb2.Variant.VARIANT_FORMATTED_MESSAGE)
        variant.bytes_index_in_cache = self._get_string_index_in_cache(namespace.obj)

    def _dump_python_object(self, obj, variant, current_depth, config, log_errors):
        try:
            self._dump_python_object_unsafe(obj, variant, current_depth, config, log_errors)
        except Exception as e:
            message = "Failed to serialize namespace"

            variant.Clear()
            NamespaceSerializer2.dump_variant_type(variant, variant_pb2.Variant.VARIANT_ERROR)

            if log_errors:
                from .error import Error
                logger.exception(message)
                UserWarnings.send_warning(Error(exc=e, message=message))

    def _dump_python_object_unsafe(self, obj, variant, current_depth, config, log_errors):
        original_type = type(obj).__name__
        variant.original_type_index_in_cache = self._get_string_index_in_cache(original_type)

        if isinstance(obj, NamespaceSerializerBase.PRIMITIVE_TYPES):
            self._dump_primitive(obj, original_type, variant, config.max_string)
        elif isinstance(obj, LIST_TYPE):
            self._dump_list(obj, variant, current_depth, config, log_errors)
        elif isinstance(obj, dict):
            self._dump_dictionary(obj, variant, current_depth, config, log_errors)
        elif isinstance(obj, BaseException):
            self._dump_exception(obj, variant, current_depth, config, log_errors)
        elif isinstance(obj, TracebackType):
            self._dump_traceback(obj, variant, current_depth, config, log_errors)
        elif NamespaceSerializer2.is_numpy_obj(obj):
            self._dump_primitive(obj.item(), original_type, variant, config.max_string)
        elif NamespaceSerializer2.is_torch_obj(obj):
            self._dump_primitive(str(obj), original_type, variant, config.max_string)
        elif NamespaceSerializer2.is_multidict_obj(obj):
            self._dump_primitive(str(obj), original_type, variant, config.max_string)
        elif NamespaceSerializer2.is_protobuf_obj(obj):
            self._dump_protobuf(obj, variant, current_depth, config, log_errors)
        elif hasattr(obj, '__dict__'):
            self._dump_user_class(obj, variant, current_depth, config, log_errors)
        else:
            self._dump_not_supported(obj, variant)

    def _dump_traceback(self, obj, variant, current_depth, config, log_errors):
        # python separates the "forward" stack (callees of the except clause)
        # and the "backward" stack (callers of above)
        # Possibly would be more useful to wrap this in a StackNamespace
        tb = traceback.format_tb(obj)
        tb[1:1] = traceback.format_stack(obj.tb_frame.f_back)
        value = ''.join(tb)

        NamespaceSerializer2.dump_variant_type(variant, variant.VARIANT_STRING)
        variant.original_size = len(value)
        variant.bytes_index_in_cache = self._get_string_index_in_cache(value)

    def _dump_primitive(self, obj, original_type, variant, max_string):
        if obj is None:
            self.dump_variant_type(variant, variant_pb2.Variant.VARIANT_NONE)

        elif isinstance(obj, six.integer_types) and (obj < Int64ValueChecker._MAX) and (obj > Int64ValueChecker._MIN):
            self.dump_variant_type(variant, variant_pb2.Variant.VARIANT_LONG)
            variant.long_value = int(obj)

        elif isinstance(obj, six.integer_types):
            NamespaceSerializer2.dump_variant_type(variant, variant_pb2.Variant.VARIANT_LARGE_INT)
            variant.bytes_index_in_cache = self._get_string_index_in_cache(str(obj))

        elif isinstance(obj, bool):
            self.dump_variant_type(variant, variant_pb2.Variant.VARIANT_LONG)
            variant.long_value = int(obj)

        elif isinstance(obj, float):
            self.dump_variant_type(variant, variant_pb2.Variant.VARIANT_DOUBLE)
            variant.double_value = float(obj)

        elif isinstance(obj, decimal.Decimal):
            serialized_decimal = str(obj)

            self.dump_variant_type(variant, variant_pb2.Variant.VARIANT_STRING)
            variant.original_size = len(serialized_decimal)
            variant.bytes_index_in_cache = self._get_string_index_in_cache(str(serialized_decimal))

        elif isinstance(obj, six.string_types):
            self.dump_variant_type(variant, variant_pb2.Variant.VARIANT_STRING)
            variant.original_size = len(obj)

            if len(obj) > max_string:
                obj = obj[:max_string]

            string = self.normalize_string(obj)
            variant.bytes_index_in_cache = self._get_string_index_in_cache(string)

        elif isinstance(obj, self.BINARY_TYPES) or original_type == 'binary_type':
            self.dump_variant_type(variant, variant_pb2.Variant.VARIANT_BINARY)
            variant.original_size = len(obj)

            if len(obj) > max_string:
                obj = obj[:max_string]

            variant.bytes_index_in_cache = self._get_bytes_index_in_cache(bytes(obj))

        elif isinstance(obj, self.CODE_TYPES):
            self.dump_variant_type(variant, variant_pb2.Variant.VARIANT_CODE_OBJECT)
            code_value = variant.code_values.add()
            code_value.name_index_in_cache = self._get_string_index_in_cache(self.normalize_string(obj.__name__))
            if hasattr(obj, '__code__') and hasattr(obj.__code__, 'co_filename'):
                code_value.filename_index_in_cache = self._get_string_index_in_cache(self.normalize_string(obj.__code__.co_filename))
                code_value.lineno = int(obj.__code__.co_firstlineno)
            if hasattr(obj, '__module__') and obj.__module__:
                code_value.module_index_in_cache = self._get_string_index_in_cache(self.normalize_string(obj.__module__))

        elif isinstance(obj, complex):
            self.dump_variant_type(variant, variant_pb2.Variant.VARIANT_COMPLEX)
            variant.complex_value.real = float(obj.real)
            variant.complex_value.imaginary = float(obj.imag)

        elif isinstance(obj, datetime.datetime):
            self._dump_datetime(obj, variant)

        else:
            raise ValueError("Object is not a supported primitive!", type(obj))

    def _dump_datetime(self, obj, variant):
        if obj.tzinfo:
            obj = obj.replace(tzinfo=None)

        self.dump_variant_type(variant, variant_pb2.Variant.VARIANT_TIME)
        variant.time_value.FromDatetime(obj)

    def _dump_list(self, collection, variant, current_depth, config, log_errors):
        NamespaceSerializer2.dump_variant_type(variant, variant_pb2.Variant.VARIANT_LIST)

        if ListNamespace.is_numpy_obj(collection):
            collection = collection.tolist()
            if not collection:
                collection = []
        variant.original_size = len(collection)

        # Dump only if we are not too deep
        if current_depth < config.max_collection_dump:

            for index, item in enumerate(collection):
                if index >= config.max_width:
                    break

                item_variant = variant.collection_values.add()
                self._dump_python_object(item, item_variant, current_depth+1, config, log_errors)

    def _dump_dictionary(self, collection, variant, current_depth, config, log_errors):
        self.dump_variant_type(variant, variant_pb2.Variant.VARIANT_MAP)
        variant.original_size = len(collection)

        # Dump only if we are not too deep
        if current_depth < config.max_collection_dump:

            i = 0

            for key, value in six.iteritems(collection):
                i += 1
                if i > config.max_width:
                    break

                key_variant = variant.collection_keys.add()
                value_variant = variant.collection_values.add()

                self._dump_python_object(key, key_variant, current_depth+1, config, log_errors)
                self._dump_python_object(value, value_variant, current_depth+1, config, log_errors)

    def _dump_protobuf(self, obj, variant, current_depth, config, log_errors):
        self.dump_variant_type(variant, variant_pb2.Variant.VARIANT_OBJECT)
        if hasattr(obj, 'DESCRIPTOR'):
            for field in obj.ListFields():
                try:
                    variant.attribute_names_in_cache.append(self._get_string_index_in_cache(field[0].name))

                    attribute_value_variant = variant.attribute_values.add()
                    self._dump_python_object(field[1], attribute_value_variant, current_depth - 1, config, log_errors)
                except Exception:  # for now we just ignore errors when dumping protobuf
                    pass

    def _dump_exception(self, exc, variant, current_depth, config, log_errors):
        self.dump_variant_type(variant, variant_pb2.Variant.VARIANT_OBJECT)

        if len(exc.args) > 0:
            variant.attribute_names_in_cache.append(self._get_string_index_in_cache("args"))
            args_variant = variant.attribute_values.add()
            self._dump_python_object(exc.args, args_variant, current_depth + 1, config, log_errors)

    def _dump_user_class(self, obj, variant, current_depth, config, log_errors):
        object_weight = current_depth + 1

        self.dump_variant_type(variant, variant_pb2.Variant.VARIANT_OBJECT)

        for key, value in six.iteritems(obj.__dict__.copy()):
            if key not in self.BUILTIN_ATTRIBUTES_IGNORE:
                if object_weight >= config.max_depth:
                    self.dump_variant_type(variant, variant_pb2.Variant.VARIANT_OBJECT, True)
                    return

                variant.attribute_names_in_cache.append(self._get_string_index_in_cache(key))

                attribute_value_variant = variant.attribute_values.add()
                self._dump_python_object(value, attribute_value_variant, object_weight, config, log_errors)

        if hasattr(obj, '__slots__') and obj.__slots__:
            items = obj.__slots__
            # py4j (used by pyspark to communicate with Java proxy objects) sets __slots__ to Java proxy objects,
            # and supports __dir__ instead.
            if not isinstance(items, Iterable):
                items = dir(items)
            for key in list(items):
                if key not in self.BUILTIN_ATTRIBUTES_IGNORE:
                    if object_weight >= config.max_depth:
                        self.dump_variant_type(variant, variant_pb2.Variant.VARIANT_OBJECT, True)
                        return

                    variant.attribute_names_in_cache.append(self._get_string_index_in_cache(key))

                    attribute_value_variant = variant.attribute_values.add()
                    try:
                        value = getattr(obj, key)
                    except AttributeError:
                        value = None
                    self._dump_python_object(value, attribute_value_variant, object_weight, config, log_errors)

    def _dump_not_supported(self, obj, variant):
        self.dump_variant_type(variant, variant_pb2.Variant.VARIANT_UKNOWN_OBJECT)

    def _dump_error_namespace(self, namespace, variant, log_errors):
        self.dump_variant_type(variant, variant_pb2.Variant.VARIANT_ERROR)
        variant.error_value.message = namespace.message.obj
        self.dump(namespace.parameters, variant.error_value.parameters, log_errors)
        self.dump(namespace.exc, variant.error_value.exc, log_errors)
        self.dump(namespace.traceback, variant.error_value.traceback, log_errors)

    def _dump_traceback_namespace(self, namespace, variant, log_errors):
        self.dump_variant_type(variant, variant_pb2.Variant.VARIANT_TRACEBACK)
        namespace.dump(variant.code_values, self._get_string_index_in_cache)

    @staticmethod
    def dump_variant_type(variant, variant_type, max_depth=False):
        variant.variant_type_max_depth = (variant_type << 1) | int(max_depth)

    def _get_bytes_index_in_cache(self, buffer):
        """
        Gets a buffer, store it in 'buffer_cache' if not stored yet and return its index

        @param buffer: The buffer
        @type buffer: bytes
        """

        if buffer in self.buffer_cache:
            return self.buffer_cache[buffer]

        current_size = len(self.buffer_cache)
        # We estimate each character is one byte in utf-8 and overhead is 5 bytes
        self.estimated_pending_bytes += current_size + 5
        self.buffer_cache[buffer] = current_size
        return current_size

    def get_buffer_cache(self):
        return self.buffer_cache
