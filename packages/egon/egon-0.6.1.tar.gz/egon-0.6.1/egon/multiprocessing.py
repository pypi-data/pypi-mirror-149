from __future__ import annotations

import multiprocessing as mp


class MPool:
    """A pool of processes assigned to a single target function"""

    def __init__(self, num_processes: int, target: callable) -> None:
        """Create a collection of processes assigned to execute a given callable

        Args:
            num_processes: The number of processes to allocate
            target: The function to be executed by the allocated processes
        """

        if num_processes < 0:
            raise ValueError(f'Cannot instantiate negative forked processes (got {num_processes}).')

        # Note that we use the memory address of the processes and not the
        # ``pid`` attribute. ``pid`` is only set after the process is started.
        self._processes = [mp.Process(target=self._call_target) for _ in range(num_processes)]
        self._states = mp.Manager().dict({id(p): False for p in self._processes})
        self._target = target

    def _call_target(self) -> None:  # pragma: nocover, Called from forked process
        """Wrapper for calling the pool's target function"""

        self._target()

        # Mark the current process as being finished
        self._states[id(mp.current_process())] = True

    @property
    def num_processes(self) -> int:
        """The number of processes assigned to the pool"""

        return len(self._processes)

    @property
    def target(self) -> callable:
        """The callable to be executed by the pool"""

        return self._target

    def is_finished(self) -> bool:
        """Return whether all processes have finished executing"""

        # Check that all forked processes are finished
        return all(self._states.values())

    def _raise_if_zero(self, action):
        """Raise an error if pool size is zero"""

        if self.num_processes == 0:
            raise RuntimeError(f'Pool has zero assigned processes. No processes available to {action}')

    def start(self) -> None:
        """Start all processes asynchronously"""

        self._raise_if_zero('start')
        for p in self._processes:
            p.start()

    def join(self) -> None:
        """Wait for any running pool processes to finish running before continuing execution"""

        self._raise_if_zero('join')
        if self.num_processes == 0:
            raise RuntimeError('Pool has zero assigned processes. No processes available to join')

        for p in self._processes:
            p.join()

    def kill(self) -> None:
        """Kill all running processes without trying to exit gracefully"""

        self._raise_if_zero('kill')
        for p in self._processes:
            p.terminate()
