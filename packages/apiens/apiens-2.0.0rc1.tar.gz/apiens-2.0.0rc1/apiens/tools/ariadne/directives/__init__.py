from . import inherits
from . import partial


# Directives mapping: for make_executable_schema()
directives_map = {
    inherits.DIRECTIVE_NAME: inherits.InheritsDirective,
    partial.DIRECTIVE_NAME: partial.PartialDirective,
}

directives_sdl = '\n'.join((
    inherits.DIRECTIVE_SDL,
    partial.DIRECTIVE_SDL,
))