# Copyright (C) 2019 Majormode.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Majormode or one of its subsidiaries.  You shall not disclose this
# confidential information and shall use it only in accordance with the
# terms of the license agreement or other applicable agreement you
# entered into with Majormode.
#
# MAJORMODE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY
# OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE, OR NON-INFRINGEMENT.  MAJORMODE SHALL NOT BE LIABLE FOR ANY
# LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING
# OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.

from majormode.perseus.model.enum import Enum
from majormode.perseus.model.geolocation import GeoPoint
from majormode.utils import cast





# # Length of time, expressed in seconds, the start playback
# # notification lives before it is deleted.
# NOTIFICATION_LIFESPAN_START_PLAYBACK = 40
#
# # Length of time, expressed in seconds, the device alert state changed
# # notification lives before it is deleted.
# NOTIFICATION_LIFESPAN_DEVICE_ALERT_STATE_CHANGED = 60
#
# # Maximum default number of registered devices allowed per user.  This
# # prevents freight companies from using this service, which is
# # dedicated to end-users only.
# MAXIMUM_REGISTERED_DEVICES_PER_USER = 3








# XeberusNotification = Enum(
#     # Indicate that the alert state of a vehicle has changed as reported
#     # by the a device mounted on this vehicle.
#     'on_alert_state_changed',
#
#     # Indicate that a device has been activated by an administrator of the
#     # Xeberus team.
#     'on_device_activated',
#
#     # Indicate that a device sent a handshake while it was not yet
#     # registered against the platform.  Its activation stays pending until
#     # an administrator of the Xeberus team decides to activate it.
#     'on_device_activation_requested',
#
#     # Indicate that the geographical location of a vehicle has changed.
#     'on_location_changed',
#
#     # Indicate that the user requested one of his device to start the
#     # playback of a sound effect.
#     'on_playback_start_requested',
#     'on_playback_started',
#
#     # Indicate that the user requested one of his device to stop the
#     # playback of a sound effect.
#     'on_playback_stop_requested',
#
#     'on_playback_stopped',
#
#     # Request a Xeberus agent application, running on a device, to
#     # recharge the credit of the Subscriber Identification Module (SIM)
#     # card currently installed on this device. The agent application needs
#     # to send a  Unstructured Supplementary Service Data (USSD) message to
#     # the telephony operator of the SIM card with the magic code of a top
#     # up card.  The amount of money to credit the SIM card of the device
#     # corresponds to the value of a top up card.
#     'on_sim_recharge_requested',
# )
#
#
# class AlertEvent(object):
#     """
#     An event indicates that an alert starts or stops.  An alert starts
#     whenever the device detects a movement based on the values read from
#     a built-in motion sensor, such as a gyroscope or an accelerometer.  An
#     alert stops when no movement is detected after a few seconds.
#
#     Depending on the current alert mode of the device, an alert event is
#     considered either as a serious threat (active mode), either as
#     expected (passive mode).
#
#     While active mode engaged, an alarm has to be immediately raised to
#     the owner of the device.  While passive mode enabled, a simple
#     notification is sent to the owner of the device.
#     """
#
#     AlertEventType = Enum(
#         # Event that indicates an alert starts whenever the device detects a
#         # movement based on the values read from a built-in motion sensor, such
#         # as a gyroscope or an accelerometer.
#         'alert_start',
#
#         # Event that indicates an an alert stops when no movement is detected
#         # after a few seconds.
#
#         'alert_end'
#     )
#
#     def __init__(
#             self,
#             event_id,
#             event_type,
#             event_time,
#             location=None,
#             sensor_values=None):
#         """
#         Build a new instance ``AlertEvent``.
#
#
#         @param event_id: identification of  the event as given by the device.
#             It corresponds to the identification of the alert.
#
#         @param event_type: item of the enumeration ``AlertEventType``
#             that indicates the type of event that occurred.
#
#         @param event_time: time when this event occurred.
#
#         @param location: a ``GeoPoint`` instance corresponding to the last
#             known location of the device when this event occurred.
#
#         @param sensor_values:  acceleration minus Gx on the 3 axes if the
#             motion sensor used on the device is an accelerometer, or the
#             angular speed around the 3 axes in radians/second if the motion
#             sensor used is a gyroscope.  The value of an event is used as
#             debugging information.
#         """
#         self.event_id = event_id
#         self.event_time = event_time
#         self.event_type = event_type
#         self.location = location
#         self.sensor_values = sensor_values
#
#     @staticmethod
#     def from_json(payload):
#         """
#         Build a ``BatteryStateChange`` instance from the specified JSON
#         object.
#
#         @param payload: JSON representation of a location report::
#
#             {
#               "event_id": string,
#               "event_time": timestamp,
#               "event_type": string,
#               "location": {
#                 "accuracy": decimal,
#                 "altitude": decimal,
#                 "bearing": decimal,
#                 "fix_time": timestamp,
#                 "latitude": decimal,
#                 "longitude": decimal,
#                 "provider": string,
#                 "speed": decimal
#               },
#               sensor_values: [ decimal, decimal, decimal ]
#             }
#
#             where:
#
#                 * ``alert_id`` (required): identification of the alert which is unique
#                   whether the alert starts or it stops.
#
#                 * ``event_time`` (required): time when the device raises this alert
#                   event, i.e., when the alert started or when it stopped.  This time
#                   could be slightly different from the time when the device sent this
#                   alert to the platform, for instance, in case of limited network
#                   connectivity, the device decided to cache locally this alert before
#                   sending it eventually to the platform.
#
#                 * ``event_type`` (required): an item of the enumeration
#                   ``AlertEventType``.
#
#                 * ``location`` (optional): last known location of the device:
#
#                   * ``accuracy`` (required): accuracy in meters of the location.
#
#                   * ``altitude`` (required): altitude in meters of the location.
#
#                   * ``bearing`` (optional): bearing in degrees.  Bearing is the horizontal
#                     direction of travel of the device, and is not related to the device
#                     orientation.  It is guaranteed to be in the range ``[0.0, 360.0]``.
#
#                   * ``fix_time`` (required): time when the device determined the
#                     information of this fix.
#
#                   * ``latitude`` (required): latitude-angular distance, expressed in
#                     decimal degrees (WGS84 datum), measured from the center of the Earth,
#                     of a point north or south of the Equator corresponding to the
#                     location.
#
#                   * ``longitude`` (required): longitude-angular distance, expressed in
#                     decimal degrees (WGS84 datum), measured from the center of the Earth,
#                     of a point east or west of the Prime Meridian corresponding to the
#                     location.
#
#                   * ``provider`` (required): code name of the location provider that
#                     reported the location.
#
#                     * ``gps``: indicate that the location has been provided by a Global
#                       Positioning System (GPS).
#
#                     * ``network``: indicate that the location has been provided by an hybrid
#                       positioning system, which uses different positioning technologies,
#                       such as Global Positioning System (GPS), Wi-Fi hotspots, cell tower
#                       signals.
#
#                   * ``speed`` (optional): speed in meters/second over the ground.
#
#                 * ``sensor_values`` (optional): acceleration minus Gx on the 3 axes if
#                   the motion sensor used on the device is an accelerometer, or the
#                   angular speed around the 3 axes in radians/second if the motion
#                   sensor used is a gyroscope.  The value of an event is used as
#                   debugging information.
#
#
#         @return: an instance ``BatteryStateChange``.
#         """
#         return payload and AlertEvent(
#             cast.string_to_uuid(payload['alert_id']),
#             cast.string_to_enum(payload['event_type'], AlertEvent.AlertEventType),
#             cast.string_to_timestamp(payload['event_time']),
#             location=GeoPoint.from_json(payload.get('location')),
#             sensor_values=payload.get('sensor_values'))
#
#

#
# # class ErrorReport(object):
# #     def __init__(self,
# #                  imei,
# #                  class_name,
# #                  message,
# #                  error_time,
# #                  stack_trace):
# #         self.report_id = uuid.uuid1()
# #         self.imei = imei
# #         self.class_name = class_name
# #         self.message = message
# #         self.error_time = error_time
# #         self.stack_trace = stack_trace
# #
# #     @staticmethod
# #     def from_json(payload, imei=None):
# #         return None if payload is None \
# #             else ErrorReport(imei or payload["imei"],
# #                    payload['class_name'],
# #                    payload.get('message', '<<NO MESSAGE>>'),
# #                    cast.string_to_timestamp(payload['error_time']),
# #                    payload['stack_trace'])
#
#
