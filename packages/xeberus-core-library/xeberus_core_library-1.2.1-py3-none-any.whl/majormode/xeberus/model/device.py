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

import uuid

from majormode.perseus.model.geolocation import GeoPoint
from majormode.perseus.utils import cast
from majormode.perseus.utils.date_util import ISO8601DateTime

from majormode.xeberus.constant.device import BatteryStateEventType


class BatteryStateChangeEvent:
    """
    Event that notifies from the change of the state of the internal
    battery of a tracker mobile device, such as:

    - the device is connected to or disconnected from the power source of
      the vehicle this device is mounted on;

    - the level of the device's battery increases or decreases.


    Only devices equipped with an internal battery can post this
    notification.  A device not equipped with an internal battery is
    indeed less secure as it is not able to send any notification when it
    is disconnected from the power source of the vehicle this device is
    mounted on; the device is immediately switched off.
    """
    def __init__(
            self,
            event_type: BatteryStateEventType,
            event_time: ISO8601DateTime,
            battery_level: float,
            location: GeoPoint = None):
        """
        Build a new object `BatteryStateChangeEvent`.


        @param event_type: An item of the enumeration `BatteryStateEventType`
            that indicates the type of event that occurred.

        @param event_time: The time when this event occurred.

        @param battery_level: The level in percentage of the device's internal
            battery when this even occurred.

        @param location: The last known
            location of the device when this event occurred.
        """
        self.battery_level = battery_level
        self.event_time = event_time
        self.event_type = event_type
        self.location = location;

    @staticmethod
    def from_json(payload: any):
        """
        Build an object `BatteryStateChangeEvent` from the specified JSON
        expression.


        @param payload: JSON representation of a battery state change event::

            {
              "battery_level": decimal,
              "event_time": timestamp,
              "event_type": string,
              "location": {
                "accuracy": decimal,
                "altitude": decimal,
                "bearing": decimal,
                "fix_time": timestamp,
                "latitude": decimal,
                "longitude": decimal,
                "provider": string,
                "speed": decimal
              }
            }

            where:

                - `event_time` (required): The time when this event occurred, which
                  could be slightly different from the time when the device sent this
                  alert to the platform, for instance, in case of limited network
                  connectivity, the device decided to cache locally this alert before
                  sending it eventually to the platform.

                - `event_type` (required): Indicate the type of event that occurred:

                  - `battery_charging`: The level of the device's battery has
                    increased significantly;

                  - `battery_discharging`: The level of the device's battery has
                    decreased significantly;

                  - `battery_plugged`: The battery of the device has been plugged to
                    a power source;

                  - `battery_unplugged`: The battery of the device has been unplugged
                    from a power source.

                - `location` (optional): Last known location of the device when this
                  event occurred:

                  - `accuracy` (required): The accuracy in meters of the location.

                  - `altitude` (required): The altitude in meters of the location.

                  - `bearing` (optional): The bearing in degrees of the device.  Bearing
                    is the horizontal direction of travel of the device, and is not
                    related to the device orientation.  It is guaranteed to be in the
                    range `[0.0, 360.0]`.

                  - `fix_time` (required): The time when the device determined the
                    information of this location fix.

                  - `latitude` (required): The latitude-angular distance, expressed in
                    decimal degrees (WGS84 datum), measured from the center of the Earth,
                    of a point north or south of the Equator corresponding to the
                    location.

                  - `longitude` (required): The longitude-angular distance, expressed in
                    decimal degrees (WGS84 datum), measured from the center of the Earth,
                    of a point east or west of the Prime Meridian corresponding to the
                    location.

                  - `provider` (required): The code name of the location provider that
                    reported the location.

                    - `fused`: The location API in Google Play services that combines
                      different signals to provide the location information.

                    - `gps`: indicate that the location has been provided by a Global
                      Positioning System (GPS).

                    - `network`: indicate that the location has been provided by an hybrid
                      positioning system, which uses different positioning technologies,
                      such as Global Positioning System (GPS), Wi-Fi hotspots, cell tower
                      signals.

                    - `passive`: A special location provider for receiving locations without
                      actually initiating a location fix.  This provider can be used to
                      passively receive location updates when other applications or services
                      request them without actually requesting the locations yourself.  This
                      provider will return locations generated by other providers.

                  - `speed` (optional): The speed in meters/second over the ground.


        @return: an instance `BatteryStateChange`.
        """
        return payload and BatteryStateChangeEvent(
            cast.string_to_enum(payload['event_type'], BatteryStateEventType),
            cast.string_to_timestamp(payload['event_time']),
            payload['battery_level'],
            location=GeoPoint.from_json(payload.get('location')))


class LocationUpdate:
    """
    Geographical location report that a tracker mobile device sent to the
    Location-Based Service (LBS) platform.
    """
    def __eq__(self, other):
        """
        Indicate whether this location report object is the same than another
        passed to this function.


        @param other: an instance `LocationUpdate`.


        @return: `True` if the two objects represent the same geographical
            location report (same identification and same fix time); `False`
            otherwise.
        """
        return 0 if self.event_id == other.event_id \
            else self.location.fix_time == other.location.fix_time

    def __init__(
            self,
            device_id,
            location,
            mileage=None,
            network_type=None,
            payload=None,
            event_id=None,
            satellites=None):
        """
        Build a new instance `LocationUpdate`.


        @param device_id: Identification of the tracker mobile device that
            reported this geographical location.

        @param location: An object `GeoPoint` that corresponds to the location
            fix reported by the tracker mobile device.

        @param mileage: Total distance travelled by the tracker mobile device
            since the tracker application has been installed and executed on
            this device.  This mileage is calculated by the device itself
            based on the location changes its internal GPS determined over the
            time.

            This mileage might not correspond to the mileage displayed by the
            odometer of the vehicle this tracker device is mounted on.

        @param network_type: String representation of the network connection
            at the time this location fix has been determined by the tracker
            mobile device.of this location fix:

               MNCMCC:type[:subtype]

          where:

          * `MNCMCC:string` (required): A Mobile Network Code (MNC) used in
            combination with a Mobile Country Code (MCC) (also known as a "MCC/MNC
            tuple") to uniquely identify the telephony operator of the tracker
            mobile device.

          * `type:string` (required): A human-readable name that describes the
            type of the network that the device is connected to, such as `wifi`,
            `mobile`, `unknown`.

          * `subtype:string` (optional): A human-readable name that describes the
            subtype of this network when applicable.  Network of type `wifi` has
            not subtype.  Network of type `mobile` can have a subtype such as
            `egde`, `hsdpa`, etc.

        @param payload: JSON expression of additional information that the
            tracker mobile device provided within this report.

        @param event_id: Identification of this location report.  If not
            provided, this constructor generates one.

        @param satellites: String representation of the information about the
            the satellites that were used to calculate this location fix.


        :raise ValueError: if the argument `device_id` or `location` is `None`.
        """
        if device_id is None:
            raise ValueError("argument `device_id` MUST not be null")

        if location is None:
            raise ValueError("argument `location` MUST not be null")

        self.event_id = event_id or uuid.uuid1()
        self.device_id = device_id
        self.location = location
        self.network_type = network_type
        self.payload = payload
        self.satellites = satellites

    @staticmethod
    def from_json(payload, device_id=None):
        """
        Build a `LocationUpdate` object from the specified JSON object.


        @param payload: JSON representation of a location report:

                {
                  "accuracy": decimal,
                  "altitude": decimal,
                  "bearing": decimal,
                  "device_id": string,
                  "fix_time": timestamp,
                  "latitude": decimal,
                  "longitude": decimal,
                  "mileage": decimal,
                  "network_type": string,
                  "provider": string,
                  "event_id": uuid,
                  "satellites": string,
                  "speed": decimal
                }

            where:

            * `accuracy` (required): accuracy in meters of the geographical location.

            * `altitude` (required): altitude in meters of the geographical location.

            * `bearing` (optional): bearing in degrees.  Bearing is the horizontal
              direction of travel of the tracker mobile device, and is not related
              to the device orientation.  It is guaranteed to be in the range
              `[0.0, 360.0]`.

            * `device_id` (optional): Identification of the tracker mobile device
              that reported this geographical location.

              This attribute is not required if the argument `device_id` is passed
              to this function.  If the argument and the attribute `device_id` are
              both provided, their value MUST be the same.

            * `fix_time` (required): Time when the tracker mobile device determined
              the information of this fix.

            * `latitude` (required): Latitude-angular distance, expressed in decimal
              degrees (WGS84 datum), measured from the center of the Earth, of a
              point north or south of the Equator.

            * `longitude` (required): Longitude-angular distance, expressed in
              decimal degrees (WGS84 datum), measured from the center of the Earth,
              of a point east or west of the Prime Meridian.

            * `network_type` (optional): String representation of the network
              connection at the time this geographical location fix has been
              determined by the tracker mobile device:

                  MNCMCC:type[:subtype]

              where:

              * `MNCMCC:string` (required): A Mobile Network Code (MNC) used in
                combination with a Mobile Country Code (MCC) (also known as a "MCC/MNC
                tuple") to uniquely identify the telephony operator of the tracker
                mobile device.

              * `type:string` (required): A human-readable name that describes the
                type of the network that the device is connected to, such as `wifi`,
                `mobile`, `unknown`.

              * `subtype:string` (optional): A human-readable name that describes the
                subtype of this network when applicable.  Network of type `wifi` has
                not subtype.  Network of type `mobile` can have a subtype such as
                `egde`, `hsdpa`, etc.

            * `payload` (optional): JSON expression of additional information that
              the tracker mobile device provided within this report.

            * `provider` (required): Type of the location provider that reported
              the geographical location such as:

              * `gps`: This provider determines location using satellites.

              * `network`: This provider determines location based on availability of
                cell towers and Wi-Fi access points.  Results are retrieved by means
                of a network lookup.

              * `passive`: A special location provider for receiving locations without
                actually initiating a location fix.  This provider can be used to
                passively receive location updates when other applications or services
                request them without actually requesting the locations yourself.  This
                provider will return locations generated by other providers.

            * `event_id` (required): Identification of this geographical location
              report as given by the tracker mobile device.

            * `satellites` (optional): String representation of the information
              about the satellites that were used to calculate this geographical
              location fix:

                  (azimuth:elevation:PRN:SNR)[, ...]

              where:

              * `azimuth:float`: Azimuth of the satellite in degrees.

              * `elevation:float`: Elevation of the satellite in degrees.

              * `PRN:integer`: Pseudo-Random Number (PRN) for the satellite.

              * `SNR:float`: Signal to Noise Ratio (SNR) for the satellite.

            * `speed` (optional): Speed in meters/second over the ground.

        @param device_id: Identification of the tracker mobile device that
            reported this geographical location.

            This argument is not required if the attribute `device_id` is passed
            to this function.  If the argument and the attribute `device_id` are
            both provided, their value MUST be the same.


        @return: A `LocationUpdate` object.


        :raise ValueError: If the argument and the attribute `device_id` are
            both passed to this function, but their value are not the same, or
            both of them are `None`.
        """
        if payload is None:
            return None

        device_id_ = payload.get('device_id')
        if device_id and device_id_ and device_id != device_id_:
            raise ValueError("Argument and attribute 'device_id' MUST have the same value")

        if not device_id and not device_id_:
            raise ValueError("Argument and attribute 'device_id' MUST not be both null")

        return LocationUpdate(
            device_id or device_id_,
            GeoPoint(
                payload['latitude'],
                payload['longitude'],
                accuracy=payload['accuracy'],  # Required for tracked location
                altitude=payload['altitude'],  # Required for tracked location
                bearing=payload.get('bearing'),
                fix_time=cast.string_to_timestamp(payload['fix_time']),  # Required for tracked location
                provider=payload['provider'],  # Required for tracked location
                speed=payload.get('speed')),
            network_type=payload.get('network_type'),
            payload=payload.get('payload'),
            event_id=cast.string_to_uuid(payload['event_id']),
            satellites=payload.get('satellites'))
