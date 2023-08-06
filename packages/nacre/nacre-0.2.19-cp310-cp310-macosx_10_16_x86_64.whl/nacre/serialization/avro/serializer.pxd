from nacre.serialization.base cimport AsyncSerializer


cdef class AvroSerializer(AsyncSerializer):
    cdef object _async_serializer
    cdef object _client

    cpdef dict type_convert(self, object obj, dict obj_dict)
    cpdef dict order_type_convert(self, object obj, dict obj_dict)
    cpdef dict position_type_convert(self, object obj, dict obj_dict)
