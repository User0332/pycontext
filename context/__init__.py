"""Provides helpful functions and properties for the code context using `inspect`."""
import inspect
import json
import sys
import os
import random
from types import (
	CodeType, 
	FrameType, 
	FunctionType, 
	MemberDescriptorType, 
	GetSetDescriptorType,
)

CODE_OBJ_PROP_TYPES = (
	MemberDescriptorType, GetSetDescriptorType
)

class FunctionProperties:
	def __init__(self, function: FunctionType):
		self._func = function

	@property
	def name(self):
		"""The name of the function"""

		return self._func.__name__

	@property
	def signature(self):
		"""The function's argument signature"""

		return inspect.signature(self._func)

	@property
	def args(self):
		"""Returns a mapping object of the function's parameters"""
		return self.signature.parameters

	@property
	def code(self):
		"""Get the function's code object"""

		return self._func.__code__

	@property
	def source(self):
		"""Get the function's source code"""

		return inspect.getsource(self._func)

	@property
	def props(self):
		"""Get a dictionary of this object's properties"""

		return {
			**{
				prop: str(getattr(self, prop))
				for prop in self.__class__.__dict__
				if (not prop.startswith(('_', "props")))
			},
			"args": {
				argname: {
					"name": arg.name,
					"annotation": repr(arg.annotation),
					"default": repr(arg.default),
					"kind": arg.kind,
					"decl": str(arg)
				}
				for argname, arg in self.args.items()
			},
			"code": {
				**{
					name: list(getattr(self.code, name))
					for name, value in self.code.__class__.__dict__.items()
					if (
						type(value) in CODE_OBJ_PROP_TYPES
						and
						type(getattr(self.code, name)) is tuple
					)
				},
				**{
					name: str(getattr(self.code, name))
					for name, value in self.code.__class__.__dict__.items()
					if (
						type(value) in CODE_OBJ_PROP_TYPES
						and
						type(getattr(self.code, name)) is bytes
					)
				},
				**{
					name: getattr(self.code, name)
					for name, value in self.code.__class__.__dict__.items()
					if (
						type(value) in CODE_OBJ_PROP_TYPES
						and
						type(getattr(self.code, name)) in (int, str)
					)
				}
			}
		}

	def __str__(self):
		return json.dumps(self.props, indent='\t')

class ProgramObject:
	def __init__(self, frame: FrameType):
		self._frame = frame
	
	@property
	def argv(self):
		"""Get the program's command-line arguments (identical to `sys.argv`)"""

		return sys.argv

	@property
	def env(self):
		"""Return a map of the program's enviroment variables (synonymous to os.environ)"""

		return os.environ

	def crash(self, num: int=None):
		"""Ten fun ways to crash the program (or raise an exception)!"""

		if (num is None) or (not (0 <= num <= 10)):
			num = random.randint(0, 10)

		if num == 0:
			try: self.crash(0)
			except RecursionError: return self.crash(0)
		elif num == 1: raise \
			MemoryError()
		elif num == 2: return 1/0
		elif num == 3: a
		elif num == 4: num.abcdefg
		elif num == 5: exec(
			compile("uh oh!", __file__, "exec")
		)
		elif num == 6: raise \
			KeyboardInterrupt()
		elif num == 7: {}*[]
		elif num == 8: [8].remove(9)
		elif num == 9: { num: num }[num-1]
		elif num == 10: [1]*10000000000000000000000000000000000
		else:
			import _abc_efg_hij.klmnopqrs.ok.cool.if_you_actually_created_this_module.what_r_u_doing_with_your_life

class FunctionContext:
	def __init__(self, frame: FrameType):
		self._frame = frame

	@property
	def frameinfo(self) -> inspect.FrameInfo:
		"""Like calling `inspect.getframeinfo()`."""

		return inspect.getframeinfo(self._frame)

	@property
	def name(self) -> str:
		"""Equivalent of `func.__name__`. Only works on structures like functions and classes."""

		return self.frameinfo.function

	@property
	def arginfo(self) -> inspect.ArgInfo:
		"""Get argument information from `inspect.getargvalues()`."""

		return inspect.getargvalues(self._frame)

	@property
	def args(self) -> dict[str]:
		"""Get all arguments passed to the function."""

		arginfo = self.arginfo

		return {
			arg: arginfo.locals[arg]
			for arg in arginfo.args
		}

	@property
	def valueargs(self) -> dict[str]:
		"""Return function.args excluding args that are `None`."""

		return {
			key: value
			for key, value in self.args.items()
			if value is not None
		}

	@property
	def locals(self) -> dict[str]:
		"""Returns a dict of the function's locals"""

		return self._frame.f_locals

	@property
	def code(self) -> CodeType:
		"""Return a code object representing this frame or function's code."""

		return self._frame.f_code

	@property
	def source(self) -> str:
		"""Return the source code of this frame or function."""

		return inspect.getsource(self.code)

	def properties(self, func: FunctionType):
		return FunctionProperties(func)

function: FunctionContext
builtins: dict
globals: dict
prevframe: FrameType
lineno: int
filename: str
program: ProgramObject

class ContextObject:
	def __init__(self, frame: FrameType):
		self._frame = frame
		self._info = inspect.getframeinfo(frame, 3)
		self._function: FunctionContext = None
		self._program: ProgramObject = None

	@property
	def function(self):
		"""Namespace for function-related properties"""
		if self._function: return self._function

		self._function = FunctionContext(self._frame)

		return self._function

	@property
	def builtins(self):
		"""Returns a dict of the current context's builtins"""
		return self._frame.f_builtins
	
	@property
	def globals(self):
		"""Returns a dict of the current context's globals"""
		return self._frame.f_globals

	@property
	def prevctx(self):
		"""Returns the context of the previous frame"""
		return ContextObject(self._frame.f_back)

	@property
	def code(self):
		"""Returns the code object associated with the current context"""
		return self._frame.f_code
	
	@property
	def sourcelns(self):
		"""Returns the previous, current, and next line of the code context as a string. Returns `None` if it could not be retrieved."""
		try: return self._info.code_context[self._info.index]
		except TypeError: return None

	@property
	def lineno(self):
		"""Returns the line number of the context"""
		return self._frame.f_lineno

	@property
	def filename(self):
		"""Returns the filename of the context"""
		return self._info.filename

	@property
	def program(self):
		"""A namespace containing program-related properties (made especially for `crash()`!)"""

		if self._program: return self._program

		self._program = ProgramObject(self._frame)

		return self._program

def frameify():
	return inspect.currentframe().f_back

def __getattr__(name: str):
	return getattr(ContextObject(frameify().f_back), name)