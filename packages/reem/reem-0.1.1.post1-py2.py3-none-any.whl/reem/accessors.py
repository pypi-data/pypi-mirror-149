from __future__ import print_function

from threading import Thread, Lock
import rejson
from .utilities import *

_ROOT_VALUE_READ_NAME = "{}ROOT{}".format(ROOT_VALUE_SEQUENCE, ROOT_VALUE_SEQUENCE)
_TYPEMAP = {
    'object':dict,
    'array':list,
    'integer':int,
    'number':float,
    'boolean':bool
}

class MetadataListener:
    def __init__(self, interface):
        self.client = rejson.Client(host=interface.hostname)
        self.pubsub = self.client.pubsub()
        self.pubsub.psubscribe(['__keyspace@0__:*'])
        self.listeners = {}

    def add_listener(self, key_name, reader):
        listen_name = "__keyspace@0__:{}".format(key_name)
        self.listeners.setdefault(listen_name,[]).append(reader)

    def flush(self):
        while True:
            item = self.pubsub.get_message()
            if item is None:
                break
            channel = item['channel'].decode("utf_8")
            try:
                for listener in self.listeners[channel]:
                    listener.pull_metadata = True
            except KeyError:
                pass


class KeyAccessor:
    """Main class for accessing sub-keys of a KeyValueStore."""
    def __init__(self, parent, writer, reader, initial_path=[]):
        self.parent = parent
        self.writer = writer
        self.reader = reader
        self.path = initial_path
        self.path_str = None  #caches path string

    def __str__(self):
        if self.path_str is None:
            self.path_str = key_sequence_to_path_ext(self.path)
        return "reem.KeyAccessor({} {})".format(self.writer.top_key_name,self.path_str)

    def __getitem__(self, key):
        assert check_valid_key_name_ext(key),"{} is not a valid key under path {}".format(key,key_sequence_to_path(self.path) if self.path_str is None else self.path_str)
        return self.__class__(self,self.writer,self.reader,self.path+[key])

    def __setitem__(self, key, value):
        if isinstance(value,KeyAccessor):
            #sometimes this happens on += / *= on subkeys
            if value.parent is self:
                return
            else:
                raise ValueError("Cannot set a KeyAccessor to another KeyAccessor... {}[{}] = {}".format(self.path,key,value.path))
        assert check_valid_key_name_ext(key),"{} is not a valid key under path {}".format(key,key_sequence_to_path(self.path) if self.path_str is None else self.path_str)
        if self.path_str is None:
            self.path_str = key_sequence_to_path_ext(self.path)
        if self.path_str.endswith('.'): #root
            if isinstance(key,int):
                path = '[%d]'%(key)
            else:
                path = self.path_str + key
        else:
            if isinstance(key,int):
                path = self.path_str + '[%d]'%(key,)
            else:
                path = self.path_str + '.' + key
        self.writer.send_to_redis(path, value)

    def __delitem__(self,key):
        assert check_valid_key_name_ext(key),"{} is not a valid key under path {}".format(key,key_sequence_to_path(self.path) if self.path_str is None else self.path_str)
        if self.path_str is None:
            self.path_str = key_sequence_to_path_ext(self.path)
        if self.path_str.endswith('.'): #root
            if isinstance(key,int):
                path = '[%d]'%(key)
            else:
                path = self.path_str + key
        else:
            if isinstance(key,int):
                path = self.path_str + '[%d]'%(key,)
            else:
                path = self.path_str + '.' + key
        self.writer.delete_from_redis(path)

    def read(self):
        """Actually read the value referred to by this accessor."""
        if self.path_str is None:
            self.path_str = key_sequence_to_path_ext(self.path)
        server_value = self.reader.read_from_redis(self.path_str)
        #if it's special, then its value is under _ROOT_VALUE_READ_NAME
        try:
            return server_value[_ROOT_VALUE_READ_NAME]
        except:
            return server_value

    def write(self, value):
        """Writes value to the path referred to by this accessor."""
        if self.path_str is None:
            self.path_str = key_sequence_to_path_ext(self.path)
        self.writer.send_to_redis(self.path_str, value)

    def _do_rejson_call(self,fn,*args):
        assert isinstance(fn,str)
        if self.path_str is None:
            self.path_str = key_sequence_to_path_ext(self.path)
        with self.writer.interface.INTERFACE_LOCK:
            return getattr(self.writer.interface.client,fn)(self.writer.top_key_name,self.path_str,*args)

    def type(self):
        """Returns the type of the object"""
        t = self._do_rejson_call('jsontype')
        return _TYPEMAP[t]

    def __len__(self):
        """Returns the length of an array / number of keys in dict"""
        try:
            return self._do_rejson_call('jsonobjlen')
        except:
            return self._do_rejson_call('jsonarrlen')

    def __iadd__(self,rhs):
        """Adds a value to an integer / float value, or concatenates a list
        to an array.

        Type checking is not performed, so the user should know what they're doing.
        """
        if not hasattr(rhs,'__iter__'):
            #treat as value
            if not isinstance(rhs,(int,float)):
                raise ValueError("+= can only accept int or float arguments")
            self._do_rejson_call('jsonnumincrby',rhs)
        else:
            self._do_rejson_call('jsonarrappend',*rhs)
        return self

    def __isub__(self,rhs):
        """Subtracts a value from an integer / float value

        Type checking is not performed, so the user should know what they're doing.
        """
        self += -rhs
        return self

    def __imul__(self,rhs):
        """Multiplies a value by an integer / float value.

        Type checking is not performed, so the user should know what they're doing.
        """
        #treat as value
        if not isinstance(rhs,(int,float)):
            raise ValueError("*= can only accept int or float arguments")
        self._do_rejson_call('jsonnummultby',rhs)
        return self

    def __idiv__(self,rhs):
        """Divides a value by an integer / float value

        Type checking is not performed, so the user should know what they're doing.
        """
        self *= 1.0/rhs
        return self

    def append(self,rhs):
        """Appends a value to an array

        Type checking is not performed, so the user should know what they're doing.
        """
        self._do_rejson_call('jsonarrappend',rhs)    




class WriteOnlyKeyAccessor(KeyAccessor):
    def __init__(self,*args,**kwargs):
        KeyAccessor.__init__(self,*args,**kwargs)
        del self.read
        del self.__delitem__
        del self.__iadd__
        del self.__isub__
        del self.__imul__
        del self.__idiv__
        del self.append


class ActiveSubscriberKeyAccessor(KeyAccessor):
    def __init__(self,*args,**kwargs):
        KeyAccessor.__init__(self,*args,**kwargs)
        del self.write
        del self.__setitem__
        del self.__delitem__
        del self.__iadd__
        del self.__isub__
        del self.__imul__
        del self.__idiv__
        del self.append

    def read(self):
        return_val = self.reader.local_copy
        dissect_path = self.path[1:]  #skip initial .
        if len(dissect_path) == 0:
            pass
        else:
            for key in dissect_path:
                return_val = return_val[key]
        if type(return_val) == dict:
            return copy_dictionary_without_paths(return_val, [])
        return return_val


class ChannelListener(Thread):
    def __init__(self, interface, channel_name, callback_function, kwargs):
        Thread.__init__(self)
        self.client = rejson.Client(host=interface.hostname)
        self.pubsub = self.client.pubsub()
        self.pubsub.psubscribe([channel_name])
        self.callback_function = callback_function
        self.kwargs = kwargs
        self.first_item_seen = False

    def run(self):
        for item in self.pubsub.listen():
            # First Item is a generic message that we need to get rid of
            if not self.first_item_seen:
                self.first_item_seen = True
                continue
            item = json_recode_str(item)
            channel = item['channel']
            message = item['data']

            self.callback_function(channel=channel, message=message, **self.kwargs)

