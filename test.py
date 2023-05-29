import context

def hello(a: str, b: str=None, c: str=None):
	print(context.function.name)
	print(context.function.valueargs)
	print(context.function.source)
	print(context.function.locals)
	print(context.globals)
	print(context.filename)
	print(context.lineno)

	print(
		a,
		b,
		c
	)


hello("Hello")

props = context.function.properties(hello)

with open("hello.functionProperties.json", 'w') as f:
	f.write(str(props))

context.program.crash()