"""ber.py
"""
# Standard library imports

# Third party imports

# Local application imports
from common import hstr as _hstr

def parse(hstr: str, recursive=True):
    """parse: Parses a TLV string into a (nested) list of (T,L,V) tuples and a remainder string
    """
    remainder = _hstr.clean(hstr)
    output = []
    while remainder != '':
        # Ignoring 00 bytes before or after TLV objects
        while remainder[0:2] == '00':
            remainder = remainder[2:]

        T, remainder = _decode_tag(remainder)
        if T == '':
            break

        L, remainder = _decode_length(remainder)
        if L == '':
            break

        V, remainder = _decode_value(L, remainder)
        if V == '':
            break

        # Constructed object
        if recursive and _is_tag_constructed(T):
            V, _ = parse(V)

        output.append((T, L, V))

    return (output, remainder)

def find(tag, object):
    """find: finds a specific tag in a list of objects
    """
    tag = _hstr.clean(tag)
    if isinstance(object, tuple):
        return _find_in_tuple(tag, object)
    elif isinstance(object, list):
        return _find_in_list(tag, object)
    else:
        return ('','','')



#
# Helper functions (assume a clean 'hstr' as input)
#

def _find_in_tuple(tag, object):
    T, L, V = object
    if T == tag:
        return object
    else:
        return find(tag, V)

def _find_in_list(tag, object_list):
    for object in object_list:
        r = find(tag, object)
        if r != ('','',''):
            return r

def _is_tag_constructed(tag: str) -> bool:
    return _hstr.and_(tag[0:2], '20') == '20'

def _decode_tag(data: str) -> tuple[str, str]:
    # Input data must be at least 1 byte (i.e., 2 nibbles)
    if len(data) < 2:
        return ('', data)
    
    # Input data must be byte sequence (i.e., even number of nibbles)
    if len(data) % 2 == 1:
        return ('', data)

    # Determining the length of the tag field.
    if _hstr.and_(data[0:2], '1F') != '1F':
        # The tag field is only one byte.
        return (data[0:2], data[2:])
    else:
        # The tag field has more than one byte.
        index = 2

        # Looking for subsequent bytes (i.e., whether most significant bit of current byte is 1)
        while _hstr.and_(data[index:index+2], '80') == '80':
            index += 2
        
        return (data[0:index+2], data[index+2:])


def _decode_length(data: str) -> tuple[str, str]:
    # Input data must be at least 1 byte (i.e., 2 nibbles)
    if len(data) < 2:
        return ('', data)
    
    # Input data must be byte sequence (i.e., even number of nibbles)
    if len(data) % 2 == 1:
        return ('', data)

    # Determining the length of the length field.
    if _hstr.and_(data[0:2], '80') == '00':
        # The length field is only one byte (definite, short)
        return (data[0:2], data[2:])
    elif data[0:2] in ['80', 'FF']:
        # The length field is only one byte (indefinite or reserved)
        return (data[0:2], data[2:])
    else:
        # The length field has more than one byte (definite, long)
        nr_bytes = int(_hstr.and_(data[0:2], '7F'), 2)
        return (data[0:2+2*nr_bytes], data[2+2*nr_bytes:])


def _decode_value(length: str, data: str) -> tuple[str, str]:
    # Input data must be at least 1 byte (i.e., 2 nibbles)
    if len(data) < 2:
        return ('', data)
    
    # Input data must be byte sequence (i.e., even number of nibbles)
    if len(data) % 2 == 1:
        return ('', data)

    if len(length) == 2:
        if length == '80':
            # Length is of indefinite form i.e., data ends with 2 end-of-contents (0x00) octets
            end_pos = data.find('0000')
            if end_pos == -1:
                # Could not find EOC octets
                return ('', data)
            else:
                return (data[0:end_pos], data[end_pos+4:])
        elif length == 'FF':
            # Length value is 'reserved'
            return ('', data)
        else:
            # Length is definite, short
            nr_bytes = int(length, 16)
            if len(data) < 2 * nr_bytes:
                # The data field is too short
                return ('', data)
            else:
                return (data[0:2*nr_bytes], data[2*nr_bytes:])
    else:
        # Length is definite, long
        nr_bytes = int(length[2:], 16)
        if len(data) < 2 * nr_bytes:
            # The data field is too short
            return ('', data)
        else:
            return (data[0:2*nr_bytes], data[2*nr_bytes:])
