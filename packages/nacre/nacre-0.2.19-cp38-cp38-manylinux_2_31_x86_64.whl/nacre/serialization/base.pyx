cdef class AsyncSerializer:
    async def serialize(self, object obj) -> bytes:
        pass

    async def deserialize(self, bytes obj_bytes) -> object:
        pass

    async def stop(self):
        pass
