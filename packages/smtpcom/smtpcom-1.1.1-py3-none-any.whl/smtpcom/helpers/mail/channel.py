class Channel(object):
    """A channel for an email message."""

    def __init__(self, channel):
        """Create a Channel.

        :param channel: The channel for an email
        :type channel: string
        """
        self._channel = None

        self.channel = channel

    @property
    def channel(self):
        """The subject of an email.

        :rtype: string
        """
        return self._channel

    @channel.setter
    def channel(self, value):
        """The channel of an email.

        :param value: The channel of an email.
        :type value: string
        """
        self._channel = value

    def __str__(self):
        """Get a JSON representation of this Mail request.

        :rtype: string
        """
        return str(self.get())

    def get(self):
        """
        Get a JSON-ready representation of this Subject.

        :returns: This channel, ready for use in a request body.
        :rtype: string
        """
        return self.channel
