from ovos_workshop import OVOSAbstractApplication
from ovos_plugin_manager.phal import find_phal_plugins, PHALPlugin
from ovos_utils.messagebus import get_mycroft_bus
from ovos_utils import wait_for_exit_signal
from ovos_utils.log import LOG
from ovos_utils.configuration import read_mycroft_config
from ovos_utils.process_utils import ProcessStatus, StatusCallbackMap


def on_ready():
    LOG.info('PHAL is ready.')


def on_stopping():
    LOG.info('PHAL is shutting down...')


def on_error(e='Unknown'):
    LOG.error(f'PHAL failed to launch ({e}).')


class PHAL(OVOSAbstractApplication):
    """
    Args:
        config (dict): PHAL config, usually from mycroft.conf
        bus (MessageBusClient): mycroft messagebus connection
        watchdog: (callable) function to call periodically indicating
                  operational status.
    """

    def __init__(self, config=None, bus=None,
                 on_ready=on_ready, on_error=on_error,
                 on_stopping=on_stopping, watchdog=lambda: None):
        super().__init__(skill_id="ovos.PHAL")

        callbacks = StatusCallbackMap(on_ready=on_ready,
                                      on_error=on_error,
                                      on_stopping=on_stopping)
        self.status = ProcessStatus('PHAL', callback_map=callbacks)
        self._watchdog = watchdog # TODO implement
        if not config:
            try:
                config = read_mycroft_config()["PHAL"]
            except:
                config = {}
        self.config = config
        self.bus = bus or get_mycroft_bus()
        self.drivers = {}
        self.status.bind(self.bus)

    def load_plugins(self):
        for name, plug in find_phal_plugins().items():
            config = self.config.get(name) or {}
            if hasattr(plug, "validator"):
                enabled = plug.validator.validate(config)
            else:
                enabled = config.get("enabled")
            if enabled:
                try:
                    self.drivers[name] = plug(bus=self.bus, config=config)
                    LOG.info(f"PHAL plugin loaded: {name}")
                except Exception:
                    LOG.exception(f"failed to load PHAL plugin: {name}")
                    continue

    def start(self):
        self.status.set_started()
        try:
            self.load_plugins()
            self.status.set_ready()
            wait_for_exit_signal()
        except Exception as e:
            self.status.set_error(e)
        self.status.set_stopping()

