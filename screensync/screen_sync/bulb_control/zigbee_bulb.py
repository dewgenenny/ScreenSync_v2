import json
import paho.mqtt.publish as publish
from .abstract_bulb_control import AbstractBulbControl
import screensync.screen_sync.rate_limiter


class ZigbeeBulbControl(AbstractBulbControl):

    def __init__(self, mqtt_broker, port, username, password, topic, rate_limiter, placement):
        self.mqtt_broker = mqtt_broker
        self.port = port
        self.username = username
        self.password = password
        self.topic = topic
        self.rate_limiter = rate_limiter
        self.last_color = None
        self.placement = placement
        self.type = "MQTT"
        self.device_id = topic

    def connect(self):
        """Dummy implementation as connection is handled globally for MQTT."""
        pass

    def _publish_message(self, message):
        """Publish a message to the MQTT broker."""
        publish.single(
            self.topic,
            payload=json.dumps(message),
            hostname=self.mqtt_broker,
            port=self.port,
            auth={'username': self.username, 'password': self.password}
        )

    def set_color(self, r, g, b):
        """Sets the color of the bulb."""

        new_color = (r, g, b)
        if new_color == self.last_color:
            return  # No change in color, no need to update

        if self.rate_limiter.is_allowed():
            message = {"color": {"r": r, "g": g, "b": b}}
            self._publish_message(message)
            self.last_color = new_color

    def turn_off(self):
        """Turns off the bulb."""
        message = {"state": "OFF"}
        self._publish_message(message)

    def turn_on(self):
        """Turns on the bulb."""
        message = {"state": "ON"}
        self._publish_message(message)
