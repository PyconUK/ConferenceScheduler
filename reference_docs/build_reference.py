"""A script to build the rst file for the reference section of the docs."""
import sphinx.ext.autodoc

rst = {
    'scheduler': [],
    'resources': []
}

# Monkey Patch sphinx.ext.autodoc so that it appends to our rst list
def add_line(self, line, source, *lineno):
    """Append one line of generated reST to the output."""
    if 'conference_scheduler.scheduler' in source:
        module = 'scheduler'
    else:
        module = 'resources'
    rst[module].append(line)
    self.directive.result.append(self.indent + line, source, *lineno)


def write_reference():
    for module, content in rst.items():
        file = f'../docs/reference/{module}.txt'
        with open(file, 'w'): pass
        with open(file, 'a') as f:
            for line in rst[module]:
                print(line, file=f)


sphinx.ext.autodoc.Documenter.add_line = add_line
try:
    sphinx.main([
        'sphinx-build', '-E', '-b', 'html', '-d', '_build/doctrees', '.',
        '_build/html'])
except SystemExit:
    write_reference()
