# -*- coding: utf-8 -*- {{{
# vim: set fenc=utf-8 ft=python sw=4 ts=4 sts=4 et:
#
# Copyright 2019, Battelle Memorial Institute.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This material was prepared as an account of work sponsored by an agency of
# the United States Government. Neither the United States Government nor the
# United States Department of Energy, nor Battelle, nor any of their
# employees, nor any jurisdiction or organization that has cooperated in the
# development of these materials, makes any warranty, express or
# implied, or assumes any legal liability or responsibility for the accuracy,
# completeness, or usefulness or any information, apparatus, product,
# software, or process disclosed, or represents that its use would not infringe
# privately owned rights. Reference herein to any specific commercial product,
# process, or service by trade name, trademark, manufacturer, or otherwise
# does not necessarily constitute or imply its endorsement, recommendation, or
# favoring by the United States Government or any agency thereof, or
# Battelle Memorial Institute. The views and opinions of authors expressed
# herein do not necessarily state or reflect those of the
# United States Government or any agency thereof.
#
# PACIFIC NORTHWEST NATIONAL LABORATORY operated by
# BATTELLE for the UNITED STATES DEPARTMENT OF ENERGY
# under Contract DE-AC05-76RL01830
# }}}


import logging
import sys
from pprint import pformat

from volttron.platform.agent import utils
from volttron.platform.messaging.health import STATUS_GOOD
from volttron.platform.vip.agent import Agent, Core, PubSub
from volttron.platform.vip.agent.subsystems.query import Query
from volttron.platform.scheduling import periodic
import importlib

utils.setup_logging()
_log = logging.getLogger(__name__)
__version__ = '3.3'
DEFAULT_MESSAGE = 'Listener Message'
DEFAULT_AGENTID = "netatmo2"
DEFAULT_HEARTBEAT_PERIOD = 5


class ListenerAgent(Agent):
    """Listens to everything and publishes a heartbeat according to the
    heartbeat period specified in the settings module.
    """

    def __init__(self, config_path, **kwargs):
        super().__init__(**kwargs)
        self.config = utils.load_config(config_path)
        self._agent_id = self.config.get('agentid', DEFAULT_AGENTID)
        self._message = self.config.get('message', DEFAULT_MESSAGE)
        self._heartbeat_period = self.config.get('heartbeat_period',
                                                 DEFAULT_HEARTBEAT_PERIOD)

        self._address = self.config.get('address')
        self._url = self.config.get('url')
        self._client_id = self.config.get('client_id')
        self._username = self.config.get('username')
        self._password = self.config.get('password')
        self._client_secret = self.config.get('client_secret')
        self.apiLib = importlib.import_module("Agents.NetatmoAgent.netatmo.netatmo_driver")
        self.netatmo = self.apiLib.API(address=self._address, url=self._url, client_id=self._client_id,
                                       username=self._username, password=self._password,
                                       client_secret=self._client_secret)

        try:
            self._heartbeat_period = int(self._heartbeat_period)
        except:
            _log.warning('Invalid heartbeat period specified setting to default')
            self._heartbeat_period = DEFAULT_HEARTBEAT_PERIOD
        log_level = self.config.get('log-level', 'INFO')
        if log_level == 'ERROR':
            self._logfn = _log.error
        elif log_level == 'WARN':
            self._logfn = _log.warn
        elif log_level == 'DEBUG':
            self._logfn = _log.debug
        else:
            self._logfn = _log.info

    @Core.receiver('onsetup')
    def onsetup(self, sender, **kwargs):
        # Demonstrate accessing a value from the config file
        _log.info(self.config.get('message', DEFAULT_MESSAGE))
        self._agent_id = self.config.get('agentid')

    @Core.receiver('onstart')
    def onstart(self, sender, **kwargs):
        _log.debug("VERSION IS: {}".format(self.core.version()))
        if self._heartbeat_period != 0:
            _log.debug(f"Heartbeat starting for {self.core.identity}, published every {self._heartbeat_period}s")
            self.vip.heartbeat.start_with_period(self._heartbeat_period)
            self.vip.health.set_status(STATUS_GOOD, self._message)
        query = Query(self.core)
        _log.info('query: %r', query.query('serverkey').get())

    @PubSub.subscribe('pubsub', '')
    def on_match(self, peer, sender, bus,  topic, headers, message):
        """Use match_all to receive all messages and print them out."""
        self._logfn(
            "Peer: {0}, Sender: {1}:, Bus: {2}, Topic: {3}, Headers: {4}, "
            "Message: \n{5}".format(peer, sender, bus, topic, headers, pformat(message)))

    def publish_response(self, resp_topic, publish_items):
        headers = {'weatherheader'
        }

        resp_topic = 'os/weather01'

        self.vip.pubsub.publish(peer='pubsub',
                                topic=resp_topic,
                                message='publish_items_weather',
                                headers=headers)

    @Core.schedule(periodic(10))
    def lookup_data(self):
        print("")

        self.netatmo.getDeviceStatus()

        headers = {'weatherheader'
                   }

        resp_topic = 'os/weather01/device1'

        self.vip.pubsub.publish(peer='pubsub',
                                topic=resp_topic,
                                message=self.netatmo.variables)

def main(argv=sys.argv):
    '''Main method called by the eggsecutable.'''
    try:
        utils.vip_main(ListenerAgent, version=__version__)
    except Exception as e:
        _log.exception('unhandled exception')


if __name__ == '__main__':
    # Entry point for script
    sys.exit(main())
