import time
import logging
from functools import wraps

from . import checkpoint
        

class Profiler(object):
    def __init__(self, logname='profiler.log', verbose=2):
        """
        Create profiler object. Arguments give logging options; verbosity 0 for none, 
        1 for INFO, and 2 for DEBUG.
        """
        self.profile_start = time.time()
        self.checkpoints = {}
        self.open_checkpoint_starts = {}
        self.logname = logname
        if verbose != 0:
            if verbose == 1:
                level = logging.INFO
            else:
                level = logging.DEBUG
            logging.basicConfig(level=level,
                                format='%(asctime)s %(name)-15s %(levelname)-8s %(message)s',
                                filename=self.logname,
                                filemode='w', 
                                force=True)
        
    def start(self, name=None):
        if name == None:
            name = 'Misc'
        if name in self.open_checkpoint_starts:
            raise RuntimeError(f'Open checkpoint named {name} already exists')
        
        start = time.time()
        self.open_checkpoint_starts[name] = start
        if name not in self.checkpoints:
            self.checkpoints[name] = checkpoint.Checkpoint(name)
        logger = logging.getLogger(f'{name}.start')
        logger.debug('Profiling block started.')
        
    def stop(self, name=None):
        if name == None:
            name = list(self.open_checkpoint_starts.keys())[-1]
        elif name not in self.open_checkpoint_starts:
            raise KeyError(f'No open checkpoint named {name}')
        
        stop = time.time()
        start = self.open_checkpoint_starts.pop(name)
        self.checkpoints[name].add_times(start, stop)
        logger = logging.getLogger(f'{name}.stop')
        logger.debug('Profiling block stopped.')
        
        self.checkpoints[name].elapsed
        logger.info(f'Elapsed time: {checkpoint.format_reported_times(stop - start)}')
        
    def end(self, name=None):
        self.stop(name=name)
        
    def remove(self, name=None):
        """
        Option to remove checkpoint start instead of completing a profiling
        set, for example on catching an error.
        """
        if name == None:
            name = list(self.open_checkpoint_starts.keys())[-1]
        elif name not in self.open_checkpoint_starts:
            raise KeyError(f'No open checkpoint named {name}')
        
        start = self.open_checkpoint_starts.pop(name)
        logger = logging.getLogger(f'{name}.stop')
        logger.debug('Profiling block stopped.')
        
    def clear_open(self):
        self.open_checkpoint_starts = {}
        
    def time_func(self, f):
        """
        Function wrapper for profiler.
        """
        @wraps(f)
        def wrapper(*args, **kwargs):
            self.start(name=f.__qualname__)
            result = f(*args, **kwargs)
            self.stop(name=f.__qualname__)
            return result
        return wrapper
        
    def report(self, dec=1):
        for name in self.checkpoints:
            ckpt = self.checkpoints[name]
            print(ckpt.report(dec=dec))
            
            
def time_func(f):
    """
    Independent function wrapper. Creates a one-off profiler and reports time.
    """
    sp = Profiler(verbose=0)
    @wraps(f)
    def wrapper(*args, **kwargs):
        sp.start(name=f.__qualname__)
        result = f(*args, **kwargs)
        sp.stop(name=f.__qualname__)
        sp.report()
        return result
    return wrapper