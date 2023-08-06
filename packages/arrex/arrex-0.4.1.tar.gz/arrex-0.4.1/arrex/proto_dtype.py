
names = {
	'u1': (c_ubyte, 'B'),
	'i1': (c_byte, 'b',
	
	'u2': (c_ushort, 'H'),
	'i2': (c_short, 'h'),
	
	'u4': (c_uint, 'I'),
	'i4': (c_int, 'i'),
	
	'u8': (c_ulong, 'Q'),
	'i8': (c_long, 'q'),
	
	'u16': (c_ulonglong, 'x'*16),
	'i16': (c_longlong, 'x'*16),
	
	'usize': (c_size_t, 'N'),
	'isize': (c_ssize_t, 'n'),
	
	'f2': (c_bytes*2, 'e'),
	'f4': (c_float, 'f'),
	'f8': (c_double 'd'),
	'f16': (c_longdouble, 'x'*16),
	}
	
__dict__.update(names)



	
class DType:
	''' abstract base for dtype definitions '''
	cdef size_t size # item size
	cdef void *get  # function to get a python object from the memory
	cdef void *set  # function to set the memory to the content of a python object
	cdef readonly str format  # struct format
	
class ExtensionDType(DType):
	''' copy directly the content of an extension type, giving its internal layout '''
	cdef readonly size_t size
	cdef void *get
	cdef void *set
	cdef readonly str format
	
	cdef readonly type type
	cdef size_t offset
	
	def __init__(self, type type, str format, size_t offset=0):
		self.type = type
		self.format = format
		# TODO
		
		self.get = self._get
		self.set = self._set
		
	def __repr__(self):
		return self.type.__name__
		
class PythonDType(DType):
	''' pack fields of a pure python type using a struct layout 
	
		If given layout do not have fields names, the type's slots are used to match the layout
	'''
	cdef readonly size_t size
	cdef void *get
	cdef void *set
	cdef str format
	
	cdef readonly Layout layout
	cdef readonly type
	
	def __init__(self, type, layout=None):
		if layout is None:
			layout = type.__layout__
		if isinstance(layout, str):
			self.layout = Layout(layout)
		# ensure that fields match __slots__ names
		# TODO
		
		self.size = self.layout.size
		self.format = self.layout.format
		self.get = self._get
		self.set = self._set
	
	cdef _get(self, void *data):
		pass
		
	cdef _set(self, void *data, obj):
		pass
	
	def __repr__(self):
		return self.type.__name__
	
	
class Layout(DType):
	''' dtype giving access to defined sub-items using a key 
	
		it supports any kind of sub-items dtypes, alignments, offsets
	'''
	cdef readonly size_t size
	cdef void *get
	cdef void *set
	cdef readonly str format
	
	cdef readonly object source  # object tha was passed to create the layout, only for display purpose
	cdef dict _fields  # item def indexed by key (int or str)
	
	_format_pattern = re.compile(r'\s*((\d*[uif]*\d+\s*)|x\s*)+')
	_item_pattern = re.compile(r'\s*((\d*)([uif]*\d+)\s*)|x\s*')
	
	def __init__(self, source, size=None):
		self._fields = {}
		
		if isinstance(source, str):
			offset = 0
			
			# check for moderngl like format
			# check for struct like format
			if _format_pattern.match(text[start:]):
				start = 0
				while start < len(text):
					match = _item_pattern.match(text[start:])
					if match.group(0) == 'x':
						offset += 1
					else:
						start = match.end()
						dtype = names[match.group(2)]
						n = match.group(1)
						if n:
							dtype = array(int(n), dtype)
						self._fields[len(self._fields)] = itemdef(offset, dtype)
						offset += dtype.size
			else:
				raise TypeError('invalid structure format')
		
		elif isinstance(source, dict):
			# full custom format
			for key,item in source.items():
				if not isinstance(item, itemdef):
					item = itemdef(*item)
				self._fields[key] = item
			
		else:
			raise TypeError("source must be a format string, a fields list, or a field dictionary with offsett")
			
		# compute format showing fields that do not overlap
		# TODO
		
		self.source = source
		self.size = size or max(item.offset+item.dtype.size  for item in self._fields)
		
		self.get = self._get
		self.set = self._set
	
	@property
	def fields(self):
		return types.MappingProxyType(self._fields)
	
	def __repr__(self):
		return '{}({})'.format(self.__class__.__name__, repr(self.source))
		
class itemdef:
	''' simple struct holding the way to retreive an item '''
	cdef readonly size_t offset
	cdef readonly DType dtype
	
	def __init__(self, size_t offset, DType dtype):
		self.offset = offset
		self.dtype = dtype
		
	def __repr__(self):
		return 'itemdef({}, {})'.format(self.offset, self.dtype)

cdef _layout_get(Layout *layout, void *data):
	pass
	
cdef _layout_set(Layout *layout, void *data, obj):
	pass
		
	
def Union(**dtypes) -> Layout:
	''' simple layout with overlapping items, like in C '''
	pass
	
def Struct(**fields, align=True) -> Layout:
	''' simple layout with packed struct fields, like in C '''
	if len(fields) == 1 and hasattr(fields[0], '__iter__'):
		fields = fields[0]
	
	# ctypes/numpy like format
	layout = {}
	offset = 0
	for item in fields:
		cdef DType dtype
		cdef size_t offset
		if len(item) == 2:		
			key, dtype = item
			offset += dtype.size-(size % dtype.size)
		elif len(item) == 3:	
			key, dtype, padding = item
			offset += padding
		else:
			raise TypeError('item definition must be (key, dtype) or (key, dtype, padding)')
		layout[key] = itemdef(offset, dtype)
		offset += dtype.size
	return Layout(layout, offset)
	
def Array(dtype, n) -> Layout:
	''' simple statically sized array dtype, like in C '''
	pass


class DItem:
	''' class owning the data of an item '''
	cdef ssize_t ob_size
	cdef readonly Layout type
	cdef readonly char ptr[1]

class DRef:
	''' class referencing the data of an item '''
	cdef readonly Layout type
	cdef readonly object owner
	cdef readonly char *ptr
