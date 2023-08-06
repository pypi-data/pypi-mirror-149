import os
import asyncio

from wslink import server
from wslink import register as exportRpc
from wslink.websocket import ServerProtocol

from trame_server.utils import logger, asynchronous


class CoreServer(ServerProtocol):
    authentication_token = "wslink-secret"
    app = None

    # ---------------------------------------------------------------
    # Static methods
    # ---------------------------------------------------------------

    @staticmethod
    def bind_application(app):
        logger.initialize_logger(app.options)
        CoreServer.app = app

        # Forward options to wslink
        os.environ["WSLINK_MAX_MSG_SIZE"] = str(app.options["ws_max_msg_size"])
        os.environ["WSLINK_HEART_BEAT"] = str(app.options["ws_heart_beat"])

    @staticmethod
    def add_arguments(parser):
        server.add_arguments(parser)

    @staticmethod
    def configure(args):
        CoreServer.authentication_token = args.authKey

    @staticmethod
    def server_start(options, **kwargs):
        return server.start_webserver(options=options, protocol=CoreServer, **kwargs)

    @staticmethod
    def server_stop():
        server.stop_webserver()

    # ---------------------------------------------------------------
    # Server
    # ---------------------------------------------------------------

    def initialize(self):  # Called by wslink
        self.rpcMethods = {}
        self.app = CoreServer.app
        self.app._root_protocol = self

        for configure in self.app._protocols_to_configure:
            configure(self)

        self.updateSecret(CoreServer.authentication_token)

    def set_server(self, _server):
        self.app._server = _server

    def port_callback(self, port_used):
        self.app._running_port = port_used
        if self.app._running_stage < 2:
            self.app._running_stage = 2
            if self.app.controller.on_server_ready.exists():
                self.app.controller.on_server_ready(**self.app.state.to_dict())

    # ---------------------------------------------------------------

    def getRPCMethod(self, name):
        if len(self.rpcMethods) == 0:
            import inspect

            for protocolObject in self.getLinkProtocols():
                test = lambda x: inspect.ismethod(x) or inspect.isfunction(x)
                for k in inspect.getmembers(protocolObject.__class__, test):
                    proc = k[1]
                    if "_wslinkuris" in proc.__dict__:
                        uri_info = proc.__dict__["_wslinkuris"][0]
                        if "uri" in uri_info:
                            uri = uri_info["uri"]
                            self.rpcMethods[uri] = (protocolObject, proc)

        if name in self.rpcMethods:
            return self.rpcMethods[name]

    # ---------------------------------------------------------------
    # Publish
    # ---------------------------------------------------------------

    def push_state_change(self, modified_state):
        logger.state_s2c(modified_state)
        self.publish("trame.state.topic", modified_state)

    # ---------------------------------------------------------------

    def push_actions(self, actions):
        logger.action_s2c(actions)
        self.publish("trame.actions.topic", actions)

    # ---------------------------------------------------------------
    # RPCs
    # ---------------------------------------------------------------

    @exportRpc("trame.lifecycle.update")
    def life_cycle_update(self, name):
        _fn = self.app.controller[f"on_{name}"]
        if _fn.exists():
            _fn()

    # ---------------------------------------------------------------

    @exportRpc("trame.error.client")
    def js_error(self, message):
        print(f" JS Error => {message}")

    # ---------------------------------------------------------------

    @exportRpc("trame.state.get")
    def get_app_state(self):
        initial_state = self.app.get_app_state()
        logger.initial_state(initial_state)
        return initial_state

    # ---------------------------------------------------------------

    @exportRpc("trame.trigger")
    async def trigger(self, name, args, kwargs):
        logger.action_c2s({"name": name, "args": args, "kwargs": kwargs})
        with self.app.state:
            if name in self.app._triggers:
                await asyncio.coroutine(self.app._triggers[name])(*args, **kwargs)
            else:
                print(f"Trigger {name} seems to be missing")

    # ---------------------------------------------------------------

    @exportRpc("trame.state.update")
    def update_state(self, changes):
        logger.state_c2s(changes)

        with self.app.state:
            for change in changes:
                self.app.state[change["key"]] = change.get("value")
