class psuedologger():

    __doc__ = '''psuedologger allows replacement of logging logger with simpler
                 but more limited use.'''

    # Numerical levels
    CRITICAL_LVL = 50
    ERROR_LVL = 40
    WARNING_LVL = 30
    INFO_LVL = 20
    DEBUG_LVL = 10
    NOTSET_LVL = 0

    __slots__ = ('file_out', 'file_lvl', 'file_ptr', \
                 'cons_out', 'cons_lvl', \
                 'debug', 'info', 'warn', 'warning', 'error', 'critical')

    def __init__(self, **kargs):

        self.file_out, self.file_ptr = None, None
        # File output
        if 'file_out' in kargs:
            self.set_file_out(kargs.get('file_out'))

        self.file_lvl = kargs.get('file_lvl', 20)

        # Console output
        self.cons_out = kargs.get('cons_out', True)
        self.cons_lvl = kargs.get('cons_lvl', 30)

        # Set output fxns
        self.fix_outut_fxns()

    # Editing the levels
    def set_file_out(self, new_out, append=True):
        if not isinstance(new_out, str):
            raise TypeError('Expected str for file output')
        self.file_out = new_out
        self.file_ptr = open(new_out, 'a' if append else 'w')

    def set_cons_out(self, new_out):
        if not isinstance(new_out, bool):
            raise TypeError('Expected boolean for console output')
        self.cons_out = new_out

    def set_file_lvl(self, new_lvl):
        if not isinstance(new_lvl, int):
            raise TypeError('Expected int for new_lvl')
        self.file_lvl = new_lvl
        self.fix_outut_fxns()

    def set_cons_lvl(self, new_lvl):
        if not isinstance(new_lvl, int):
            raise TypeError('Expected int for new_lvl')
        self.cons_lvl = new_lvl
        self.fix_outut_fxns()

    # Sets the
    def fix_outut_fxns(self):
        cons_lvl, file_lvl = self.cons_lvl, self.file_lvl
        # Default do nothing
        self.debug, self.info, self.warning, self.error, self.critical = \
            self.no_out, self.no_out, self.no_out, self.no_out, self.no_out

        # Set levels
        c_critical = cons_lvl <= 50
        c_error = cons_lvl <= 40
        c_warning = cons_lvl <= 30
        c_info = cons_lvl <= 20
        c_debug = cons_lvl <= 10

        if self.cons_out:
            if c_critical:
                self.critical = self.critical_c
            if c_error:
                self.error = self.error_c
            if c_warning:
                self.warning = self.warning_c
            if c_info:
                self.info = self.info_c
            if c_debug:
                self.debug = self.debug_c

        # Set file lvl
        if self.file_out is not None:
            if file_lvl <= 50:
                if c_critical:
                    self.critical = self.critical_cf
                else:
                    self.critical = self.critical_f
            if file_lvl <= 40:
                if c_error:
                    self.error = self.error_cf
                else:
                    self.error = self.error_f
            if file_lvl <= 30:
                if c_warning:
                    self.warning = self.warning_cf
                else:
                    self.warning = self.warning_f
            if file_lvl <= 20:
                if c_info:
                    self.info = self.info_cf
                else:
                    self.info = self.info_f
            if file_lvl <= 10:
                if c_debug:
                    self.debug = self.debug_cf
                else:
                    self.debug = self.debug_f

        # Set alias for warning (warn)
        self.warn = self.warning


    # Output Functions

    # Default not output function (if none applies)
    def no_out(self, s):
        return

    # Debug statements
    def debug_c(self, s): #10
        print(f'   Debug: {s}')
    def debug_f(self, s):
        self.file_ptr.write(f'   Debug: {s}\n')
    def debug_cf(self, s):
        print(f'   Debug: {s}')
        self.file_ptr.write(f'   Debug: {s}\n')

    # Handles infos
    def info_c(self, s):
        print(f'    Info: {s}')
    def info_f(self, s):
        self.file_ptr.write(f'    Info: {s}\n')
    def info_cf(self, s):
        print(f'    Info: {s}')
        self.file_ptr.write(f'    Info: {s}\n')

    # Handles warnings
    def warning_c(self, s):
        print(f' WARNING: {s}')
    def warning_f(self, s):
        self.file_ptr.write(f' WARNING: {s}\n')
    def warning_cf(self, s):
        print(f' WARNING: {s}')
        self.file_ptr.write(f' WARNING: {s}\n')

    # Handles errors
    def error_c(self, s):
        print(f'   ERROR: {s}')
    def error_f(self, s):
        self.file_ptr.write(f'   ERROR: {s}\n')
    def error_cf(self, s):
        print(f'   ERROR: {s}')
        self.file_ptr.write(f'   ERROR: {s}\n')

    # Handles critical errors
    def critical_c(self, s):
        print(f'CRITICAL: {s}')
    def critical_f(self, s):
        self.file_ptr.write(f'CRITICAL: {s}\n')
    def critical_cf(self, s):
        print(f'CRITICAL: {s}')
        self.file_ptr.write(f'CRITICAL: {s}\n')

    def __del__(self):
        if self.file_ptr is not None:
            self.file_ptr.close()
        return

    # Bonus methods

    # If used as bool, will return whether or not it is being used
    def __bool__(self):
        return (self.file_out is not None or self.cons_out)

    # Allows to see if above this level or not
    def __lt__(self, val):
        return (self.file_lvl.__lt__(val) or \
                self.cons_lvl.__lt__(val))
    def __le__(self, val):
        return (self.file_lvl.__le__(val) or \
                self.cons_lvl.__le__(val))
    def __gt__(self, val):
        return (self.file_lvl.__gt__(val) or \
                self.cons_lvl.__gt__(val))
    def __ge__(self, val):
        return (self.file_lvl.__ge__(val) or \
                self.cons_lvl.__ge__(val))
