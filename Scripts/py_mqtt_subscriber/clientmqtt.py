#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script:
    mqttclient.py
Description:
    MQTT client component that allows to connect to a server, subscribe
    to topics and publish messages.
    The component creates a non-blocking thread so the user doesn't need
    to care about it.
Developer:
    Jose Miguel Rios Rubio
Creation date:
    04/02/2019
Last modified date:
    18/06/2025
Version:
    2.0.0
'''

###############################################################################
# Standard Libraries
###############################################################################

# JSON Library
import json

# Logging Library
import logging

# OS Library
import os

# Time Library
import time


###############################################################################
# Third-Party Libraries
###############################################################################

# MQTT Library
from paho.mqtt import client as mqtt


###############################################################################
# Logger Setup
###############################################################################

logger = logging.getLogger(__name__)


###############################################################################
# MQTT Client Class
###############################################################################

class ClientMQTT(mqtt.Client):
    '''
    MQTT Client object to get an encapsulated, ease and simple way of
    communication.
    '''

    ####################################################################
    # MQTT Callbacks
    ####################################################################

    def on_connect(self, client, userdata, flags, reasonCode, properties=None):
        if reasonCode == mqtt.MQTT_ERR_SUCCESS:
            logger.debug("MQTT successfully connected.")
            for i in range(len(self.topics_subs)):
                if not self.topics_subs[i]:
                    logger.debug(f"Subscribing to {self.topics_list[i]}")
                    self.subscription(self.topics_list[i])
            self.isconnected = True
        else:
            error_str = mqtt.connack_string(reasonCode)
            logger.error(f"MQTT connection failed: {error_str}")
        logger.debug("")

    def on_disconnect(self, client, userdata, reasonCode, properties=None):
        logger.debug("MQTT disconnected.")
        if reasonCode != mqtt.MQTT_ERR_SUCCESS:
            error_str = mqtt.error_string(reasonCode)
            logger.debug(f"  Disconnect reason: {error_str}")
        logger.debug("")

    def on_message(self, client, userdata, msg):
        logger.debug("MQTT message received.")
        logger.debug(f"  QoS: {msg.qos}")
        logger.debug(f"  Topic: {msg.topic}")
        logger.debug(f"  Payload: {msg.payload}")
        logger.debug("")
        self.received_msg_callback(client, self.topics, userdata, msg)

    def on_publish(self, client, userdata, mid):
        logger.debug("MQTT message published.")
        logger.debug(f"  mid: {mid}")
        logger.debug("")

    def on_subscribe(self, client, userdata, mid, granted_qos,
                     properties=None):
        logger.debug("MQTT topic subscribed.")
        logger.debug(f"  mid: {mid}")
        logger.debug(f"  granted QoS: {granted_qos}")
        logger.debug("")

    def on_unsubscribe(self, client, userdata, mid, properties=None):
        logger.debug("MQTT topic unsubscribed.")
        logger.debug(f"  mid: {mid}")
        logger.debug("")

    def on_log(self, client, userdata, level, buf):
        if self.protocol_log:
            logger.debug(buf)

    ####################################################################
    # Public Methods
    ####################################################################

    def launch(self, config_file=None, topics=None, rxcallback=None,
               protocol_log=False, max_retries=10, retry_interval_s=5):
        '''
        Starts MQTT client connection.
        Parameters:
            - config_file: path to MQTT connection config JSON file
            - topics: list or object with topics
            - rxcallback: function to call on message received
            - protocol_log: enable internal logging
            - max_retries: max connection attempts (default: 10)
            - retry_interval_s: seconds between retries
        '''
        # Load from JSON if provided
        if config_file is not None:
            try:
                with open(config_file, "r") as f:
                    config = json.load(f)
                client_id = config.get("CLIENTID", "mqttclient")
                host = config.get("HOST", "")
                port = config.get("PORT", 0)
                user = config.get("USER", "")
                passw = config.get("PASS", "")
                ca_cert = config.get("CA_CERT_FILE", "")
                cert_file = config.get("CERT_FILE", "")
                key_file = config.get("CERT_KEY_FILE", "")
                keepalive = config.get("KEEPALIVE", 60)
            except Exception as e:
                logger.error(f"Error loading MQTT config file: {str(e)}")
                return False
            # TLS configuration
            use_tls = any([ca_cert, cert_file, key_file])
            if use_tls:
                # Check if cert files exists
                if ca_cert and not os.path.isfile(ca_cert):
                    logger.error(f"CA certificate not found: {ca_cert}")
                    return False
                if cert_file and not os.path.isfile(cert_file):
                    logger.error(f"Client certificate not found: {cert_file}")
                    return False
                if key_file and not os.path.isfile(key_file):
                    logger.error(f"Client key not found: {key_file}")
                    return False
                # Apply TLS config
                try:
                    kwargs = {}
                    if ca_cert:
                        kwargs["ca_certs"] = ca_cert
                    if cert_file and key_file:
                        kwargs["certfile"] = cert_file
                        kwargs["keyfile"] = key_file
                    self.tls_set(**kwargs)
                    logger.debug("TLS configuration applied.")
                except Exception as e:
                    logger.error(f"TLS setup failed: {str(e)}")
                    return False
        # Check for mandatory config
        if not host or (port == 0):
            return False
        # Initialize internal state
        if client_id:
            self._client_id = client_id.encode()
        self.host = host
        self.port = port
        self.keepalive = keepalive
        self.user = user
        self.passw = passw
        self.topics = topics
        self.topics_list = []
        if topics is not None:
            if isinstance(topics, list):
                self.topics_list = topics
            else:
                for _, topic_val in topics.__dict__.items():
                    self.topics_list.append(topic_val)
        self.topics_subs = [False] * len(self.topics_list)
        self.received_msg_callback = rxcallback
        self.protocol_log = protocol_log
        self.isconnected = False
        # Set auth if user/pass provided
        if self.user and self.passw:
            self.username_pw_set(user, passw)
        self.reconnect_delay_set(min_delay=1, max_delay=60)
        logger.debug("MQTT connecting...")
        attempt = 0
        connected = False
        while not connected and (max_retries is None or attempt < max_retries):
            try:
                self.connect(host, port, keepalive)
                connected = True
            except Exception as e:
                attempt += 1
                str_attempts = f"{attempt}/{max_retries}"
                logger.error(f"[{str_attempts}] MQTT fail connect: {str(e)}")
                time.sleep(retry_interval_s)
        if not connected:
            logger.error("Max retries reached. MQTT client failed to connect.")
            return False
        self.loop_start()
        return True

    def is_connected(self):
        return self.isconnected

    def subscription(self, topic, qos=2):
        '''Make all MQTT subscriptions.'''
        result = self.subscribe(topic=topic, qos=qos)
        if result[0] != mqtt.MQTT_ERR_SUCCESS:
            str_error = mqtt.error_string(result.rc)
            logger.error(f"Fail to subscribe to {topic}. {str_error}")
            self.disconnect()
        else:
            self.topics_subs[self.topics_list.index(topic)] = True
            logger.debug(f"MQTT subscribed to {topic}.")

    def send_publish(self, topic="", payload=None, qos=0, retain=False):
        result = self.publish(topic, payload, qos, retain)
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            str_error = mqtt.error_string(result.rc)
            logger.error(f"Failed to publish to {topic}. {str_error}")

    def end(self):
        '''Finalize loop.'''
        self.disconnect()
        self.loop_stop()

    ####################################################################
    # Private Methods
    ####################################################################

    # None

###############################################################################
