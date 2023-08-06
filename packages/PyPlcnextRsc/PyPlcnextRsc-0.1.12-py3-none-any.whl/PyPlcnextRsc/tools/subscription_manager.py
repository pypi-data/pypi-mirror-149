import logging
import threading
import time
from enum import auto, IntFlag
from typing import Union, Sequence, Optional

from PyPlcnextRsc.Arp.Plc.Gds.Services import SubscriptionKind, DataAccessError
from PyPlcnextRsc.wrapper import SubscriptionService
from PyPlcnextRsc.wrapper._SubscriptionService import Subscription, SubscriptionBase, RecordingSubscription
from PyPlcnextRsc.wrapper.common import variable_names_generator

__all__ = ['SubscriptionManager']


class STATE(IntFlag):
    Init = auto()
    Creating = auto()
    Created = auto()
    ReadyToSubscribe = auto()
    Running = auto()
    Pausing = auto()
    Paused = auto()
    ReSubscribe = auto()  #
    Terminate = auto()


class MaintainerBase:
    def __init__(self, sub: SubscriptionBase):
        self._log = logging.getLogger(__name__ + '.' + self.__class__.__name__)
        self._subscription = sub
        self.__state = STATE.Init
        self._lock = threading.RLock()
        self._state_lock = threading.RLock()
        self._state_machine_mutex = threading.RLock()
        self._variables = set()
        self._thread: Optional[threading.Thread] = None
        self._thread_cond = threading.Condition()
        self._isRunning = True
        self.period = 1

    def _onResubscribed(self):
        ...

    def _add_variables(self, variables):
        errs = self._subscription.addVariables(variables)
        for var_name, err in zip(variables, errs):
            if err != DataAccessError.NONE:
                self._log.warning(f"Can not add '{var_name}' : {str(err)}")
            else:
                self._log.debug(f"Add '{var_name}' success")

    def _remove_variables(self, variables):
        errs = self._subscription.removeVariables(variables)
        for var_name, err in zip(variables, errs):
            if err != DataAccessError.NONE:
                self._log.warning(f"Can not remove '{var_name}' : {str(err)}")
            else:
                self._log.debug(f"Remove '{var_name}' success")

    def addVariables(self, variableNames: Union[str, Sequence[str]], prefix: str = None):
        with self._lock:
            variables = variable_names_generator(variableNames, prefix)
            state = self._state
            for var in variables:
                self._variables.add(var)

            if state & (STATE.Running | STATE.Pausing | STATE.Paused) != 0:
                with self._state_machine_mutex:
                    self._add_variables(variables)
                    self._state |= state.ReSubscribe

    def removeVariables(self, variableNames: Union[str, Sequence[str]], prefix: str = None):
        with self._lock:
            variables = variable_names_generator(variableNames, prefix)
            state = self._state
            for var in variables:
                self._variables.discard(var)
            if state & (STATE.Running | STATE.Pausing | STATE.Paused) != 0:
                with self._state_machine_mutex:
                    self._remove_variables(variables)
                    self._state |= state.ReSubscribe

    def start(self):
        with self._lock:
            state = self._state
            if STATE.Pausing in state or STATE.Paused in state:
                self._state |= STATE.Running
                self._state &= ~ (STATE.Paused | STATE.Pausing)
            else:
                self._state = STATE.Creating

    def pause(self):
        with self._lock:
            self._state |= STATE.Pausing

    def terminate(self):
        with self._thread_cond:
            self._state |= STATE.Terminate
        self._log.debug("request terminate")
        with self._thread_cond:
            self._thread_cond.notify_all()
        if self._thread:
            self._thread.join()
            self._thread = None
            self._log.debug("loop stopped")

    def __del__(self):
        self.terminate()

    def do_step(self):
        ...

    def loop_start(self):
        self._log.debug("start loop...")
        if self._thread is None:
            self._thread = threading.Thread(target=self._thread_main)
            self._thread.start()
            self._log.debug("loop started")
        else:
            self._log.warning("loop already started")

    def loop_forever(self):
        self._isRunning = True

        while self._isRunning:
            with self._state_machine_mutex:
                state = self._state
                if STATE.Terminate in state:
                    self._log.debug("going to terminate...")
                    try:
                        if self._subscription.getSubscriptionId() > 0:
                            self._subscription.deleteSubscription()
                    except:
                        pass
                    self._isRunning = False
                    break
                elif STATE.Running in state:
                    if STATE.Pausing in state:
                        self._log.debug("going to pausing...")
                        err = self._subscription.unsubscribe()
                        if err in [DataAccessError.CurrentlyUnavailable, DataAccessError.NotExists]:
                            self._state = STATE.Creating
                        elif err == DataAccessError.NONE:
                            self._log.debug("paused")
                            self._state &= ~ STATE.Pausing
                            self._state |= STATE.Paused
                    elif STATE.Paused in state:
                        with self._thread_cond:
                            self._thread_cond.wait(5)
                    elif STATE.ReSubscribe in state:
                        self._log.debug("going to resubscribe...")
                        err = self._subscription.resubscribe()
                        self._state &= ~STATE.ReSubscribe
                        time.sleep(0.5)
                        if err != DataAccessError.NONE:
                            self._log.debug("error while resubscribe, change to Creating state!")
                            self._state &= ~ STATE.Running
                            self._state |= STATE.Creating
                        else:
                            self._onResubscribed()
                    else:
                        self._log.debug("sample once...")
                        self.do_step()
                        with self._thread_cond:
                            self._thread_cond.wait(self.period)
                    continue
                elif STATE.Init in state:
                    self._state &= ~STATE.Init
                    self._state |= STATE.Creating
                elif STATE.Creating in state:
                    self._log.debug("creating subscription...")
                    _id = self._subscription.create()
                    if _id == 0:
                        self._log.debug("creating subscription fail, wait 1s")
                        with self._thread_cond:
                            self._thread_cond.wait(1)
                            continue
                    else:
                        self._log.debug("creating subscription success")
                        self._state &= ~STATE.Creating
                        self._state |= STATE.Created
                elif STATE.Created in state:
                    self._log.debug("adding variables...")
                    self._add_variables(tuple(self._variables))
                    # TODO
                    self._state &= ~STATE.Created
                    self._state |= STATE.ReadyToSubscribe
                elif STATE.ReadyToSubscribe in state:
                    self._log.debug("going to  subscribe...")
                    err = self._subscription.subscribe()
                    if err == DataAccessError.NONE:
                        self._state &= ~ STATE.ReadyToSubscribe
                        self._state |= STATE.Running
                        with self._thread_cond:
                            self._thread_cond.wait(0.5)
                elif STATE.Pausing in state:
                    self._log.debug("going to pausing...")
                    err = self._subscription.unsubscribe()
                    if err in [DataAccessError.CurrentlyUnavailable, DataAccessError.NotExists]:
                        self._state &= ~ STATE.Pausing
                        self._state |= STATE.Creating
                    elif err == DataAccessError.NONE:
                        self._log.debug("paused")
                        self._state &= ~ STATE.Pausing
                        self._state |= STATE.Paused

        self._log.debug("Subscription terminated")

    def _thread_main(self):
        self.loop_forever()

    @property
    def _state(self):
        with self._state_lock:
            return self.__state

    @_state.setter
    def _state(self, new_state):
        with self._state_lock:
            with self._thread_cond:
                self.__state = new_state
                self._thread_cond.notify_all()

    # def _wait_state_change_to(self, state):
    #     with self._thread_cond:
    #         def test():
    #             s = self._state
    #             if s == STATE.Terminate:
    #                 return True
    #             if type(state) == tuple or type(state) == list:
    #                 return s in state
    #             else:
    #                 return s == state
    #
    #         self._thread_cond.wait_for(test)


class SubsMaintainer(MaintainerBase):
    def __init__(self, sub: Subscription, timestamp):
        super().__init__(sub)
        self._subscription = sub
        self._timestamp = timestamp
        self.onReceive = None
        self.onChanged = None
        self._last_buffer = {}

    def _onResubscribed(self):
        self._last_buffer = {}

    def do_step(self):
        if self._timestamp:
            err, ret = self._subscription.readTimeStampedValues()
        else:
            err, ret = self._subscription.readValues()

        if err != DataAccessError.NONE:
            self._state &= ~ STATE.Running
            self._state |= STATE.Creating
        else:
            if self.onReceive:
                self.onReceive(ret)
            if self.onChanged:
                _start = 0
                _debug = self._log.isEnabledFor(logging.DEBUG)
                if _debug:
                    _start = time.time()
                changed = {}
                for var_name, value in ret.items():
                    last = self._last_buffer.get(var_name, None)
                    py_val = value.Value.GetValue()
                    if last != py_val:
                        changed[var_name] = value
                        self._last_buffer[var_name] = py_val
                if _debug:
                    self._log.debug(f"changed compare cost {(time.time() - _start) * 1000} ms")
                if changed:
                    self.onChanged(changed)


class RecordSubsMaintainer(MaintainerBase):
    def __init__(self, sub: RecordingSubscription, count_per_read=0):
        super().__init__(sub)
        self._subscription = sub
        self.onReceive = None
        self.count_per_read = count_per_read

    def do_step(self):
        err, ret = self._subscription.readRecords(self.count_per_read)
        if err != DataAccessError.NONE:
            self._state &= ~ STATE.Running
            self._state |= STATE.Creating
        else:
            if self.onReceive:
                self.onReceive(ret)


class SubscriptionManager:
    def __init__(self, device):
        self.device = device
        self.subscriptionService = SubscriptionService(device)
        self.all_subs = set()

    def createSubscription(self, kind: SubscriptionKind, timestamp: bool = False, sampleRate: int = 100000) -> SubsMaintainer:
        sub = self.subscriptionService.createSubscription(kind, sampleRate)
        maintainer = SubsMaintainer(sub, timestamp)
        self.all_subs.add(maintainer)
        return maintainer

    def createRecordingSubscription(self, recordCount: int = 10, sampleRate: int = 100000, count_per_read: int = 0) -> RecordSubsMaintainer:
        sub = self.subscriptionService.createRecordingSubscription(recordCount, sampleRate)
        maintainer = RecordSubsMaintainer(sub, count_per_read)
        self.all_subs.add(maintainer)
        return maintainer


# if __name__ == "__main__":
#     from PyPlcnextRsc import *
#
#     logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     logging.getLogger(__name__).setLevel(logging.DEBUG)
#     with Device('192.168.1.10', secureInfoSupplier=lambda: ('admin', '1022b922')) as device:
#         manager = SubscriptionManager(device)
#         hp = manager.createSubscription(SubscriptionKind.HighPerformance, timestamp=True)
#         hp.addVariables("Arp.Plc.Eclr/arr999")
#         hp.onChanged = lambda x: print(x)
#
#         hp.loop_forever()

if __name__ == "__main__":
    from PyPlcnextRsc import *

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.getLogger(__name__).setLevel(logging.DEBUG)
    with Device('192.168.1.11', secureInfoSupplier=lambda: ('admin', '1022b922')) as device:
        manager = SubscriptionManager(device)
        # hp = manager.createRecordingSubscription(recordCount=50, sampleRate=20000)
        # hp.addVariables(["Arp.Plc.Eclr/a", "Arp.Plc.Eclr/b", "Arp.Plc.Eclr/c"])
        # hp.period = 0.5
        # hp.onReceive = lambda x: print(x)
        # hp.loop_start()
        # time.sleep(10)
        # hp.terminate()

        sm = manager.createSubscription(SubscriptionKind.HighPerformance)
        sm.addVariables("Arp.Plc.Eclr/a")
        sm.onChanged = lambda xxxxx: print(xxxxx["Arp.Plc.Eclr/a"].Value.GetValue())
        sm.loop_start()
        time.sleep(60)
        sm.terminate()
