==============
Stream Trigger
==============


Trigger IoT devices on Twitch notifications.


Description
===========

Stream Trigger allows you to set your stream apart from others by giving you the ability to trigger your IoT devices
on events such as Follower, Subscriber, Hosts, and Cheers.

Stream Trigger currently support the Philips Hue Bulbs but could theoretically support any IoT device with an API.


Running Stream Trigger
======================

To get started using this project clone this repository. You will need to have the Streamlabs Chatbot installed and
configured. For more information please see `<https://streamlabs.com/chatbot>` for more information.

For the current implementation of Stream Trigger you will also need two Philips Hue light bulbs. At least one of them
must be color changing. (As this project matures I hope to make this more configurable.)

For ease of deployment, Stream Trigger uses Docker. And to make it even easier to spin up I have included a sample
Docker Compose configuration. The main requirements are that you fill out the Environment Variables. I have included
a list of these variables below with a description.

========================= =============================================================================== =======================
Environment Variable Name Description                                                                     Default
========================= =============================================================================== =======================
MAIN_LIGHT                The main light that will be turned off when the light show begins               1
COLOR_LIGHT               The light that will be used for the light show.                                 2
USERNAME                  Specify a username to pass to Streamlabs                                        stream_trigger_username.
WEBSITE                   Your website. (For use by Streamlabs)
STREAMLABS_API_KEY        API Key for Streamlabs. Please see Streamlabs Docs for more information.
STREAMLABS_HOSTNAME       The IP or hostname of the PC/server running Streamlabs.                         localhost
HUE_BRIDGE_HOSTNAME       The IP or hostname of the Hue Bridge. See Philips Hue Docs to discover this.
HUE_BRIDGE_USERNAME       The username provided by the Hue Bridge. See Philips Hue Docs for retrieval.

Once you have configured your docker-compose.yml file simply run::

    docker-compose up


Note
====

This project has been set up using PyScaffold 2.5.7. For details and usage
information on PyScaffold see http://pyscaffold.readthedocs.org/.
