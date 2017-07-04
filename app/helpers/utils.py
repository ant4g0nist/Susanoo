# @ant4g0nist

class TerminalColors:
    '''Simple terminal colors class'''
    def __init__(self, enabled=True):
        # TODO: discover terminal type from "file" and disable if
        # it can't handle the color codes
        self.enabled = enabled
    
    def reset(self):
        '''Reset all terminal colors and formatting.'''
        if self.enabled:
            return "\x1b[0m"
        return ''
    
    def bold(self, on=True):
        '''Enable or disable bold depending on the "on" parameter.'''
        if self.enabled:
            return "\x1b[1m" if on else "\x1b[22m"
        return ''
    
    def italics(self, on=True):
        '''Enable or disable italics depending on the "on" parameter.'''
        if self.enabled:
            return "\x1b[3m" if on else "\x1b[23m"
        return ''
    
    def underline(self, on=True):
        '''Enable or disable underline depending on the "on" parameter.'''
        if self.enabled:
            return "\x1b[4m" if on else "\x1b[24m"
        return ''
    
    def inverse(self, on=True):
        '''Enable or disable inverse depending on the "on" parameter.'''
        if self.enabled:
            return "\x1b[7m" if on else "\x1b[27m"
        return ''
    
    def strike(self, on=True):
        '''Enable or disable strike through depending on the "on" parameter.'''
        if self.enabled:
            return "\x1b[9m" if on else "\x1b[29m"
        return ''

    def black(self, fg=True):
        '''Set the foreground or background color to black.
            The foreground color will be set if "fg" tests True. The background color will be set if "fg" tests False.'''
        if self.enabled:
            return "\x1b[30m" if fg else "\x1b[40m"
        return ''

    def red(self, fg=True):
        '''Set the foreground or background color to red.
            The foreground color will be set if "fg" tests True. The background color will be set if "fg" tests False.'''
        if self.enabled:
            return "\x1b[31m" if fg else "\x1b[41m"
        return ''
    
    def green(self, fg=True):
        '''Set the foreground or background color to green.
            The foreground color will be set if "fg" tests True. The background color will be set if "fg" tests False.'''
        if self.enabled:
            return "\x1b[32m" if fg else "\x1b[42m"
        return ''
    
    def yellow(self, fg=True):
        '''Set the foreground or background color to yellow.
            The foreground color will be set if "fg" tests True. The background color will be set if "fg" tests False.'''
        if self.enabled:
            return "\x1b[43m" if fg else "\x1b[33m"
        return ''
    
    def blue(self, fg=True):
        '''Set the foreground or background color to blue.
            The foreground color will be set if "fg" tests True. The background color will be set if "fg" tests False.'''
        if self.enabled:
            return "\x1b[34m" if fg else "\x1b[44m"
        return ''
    
    def magenta(self, fg=True):
        '''Set the foreground or background color to magenta.
            The foreground color will be set if "fg" tests True. The background color will be set if "fg" tests False.'''
        if self.enabled:
            return "\x1b[35m" if fg else "\x1b[45m"
        return ''
    
    def cyan(self, fg=True):
        '''Set the foreground or background color to cyan.
            The foreground color will be set if "fg" tests True. The background color will be set if "fg" tests False.'''
        if self.enabled:
            return "\x1b[36m" if fg else "\x1b[46m";
        return ''
    
    def white(self, fg=True):
        '''Set the foreground or background color to white.
            The foreground color will be set if "fg" tests True. The background color will be set if "fg" tests False.'''
        if self.enabled:
            return "\x1b[37m" if fg else "\x1b[47m"
        return ''
    
    def default(self, fg=True):
        '''Set the foreground or background color to the default.
            The foreground color will be set if "fg" tests True. The background color will be set if "fg" tests False.'''
        if self.enabled:
            return "\x1b[39m" if fg else "\x1b[49m"
        return ''
