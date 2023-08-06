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


# Indicate the method used to plug the device's battery to the power
# source of the vehicle.
BatteryPlugMode = Enum(
    # The device's battery is directly plugged to the power source of the
    # vehicle.  Even when the vehicle engine is switched off, the device's
    # is still connected to the power source of the vehicle.  This is the
    # common setup when mounting the device in a vehicle with a higher
    # amperage capacity battery (e.g., automobile, bus, truck, boat).
    'direct',

    # The device's battery is plugged to the ignition system of the vehicle.
    # When the vehicle engine is switched off, the device's battery is not
    # connected to the power source of the vehicle.  This is the common
    # setup when mounting the device in a vehicle with low amperage
    # capacity battery (e.g., motorcycle), in order not to drain the battery
    # when the vehicle's engine is switched off.
    'ignition'
)


# Indicate that the state of the battery of a tracker device module has
# changed.
BatteryStateEventType = Enum(
    # Event that indicates the level of the device's battery has increased
    # significantly.
    'battery_charging',

    # Event that indicates the level of the device's battery has decreased
    # significantly.
    'battery_discharging',

    # Event that indicates the battery of the device has been plugged to a
    # power source.
    'battery_plugged',

    # Event that indicates the battery of the device has been unplugged
    # from a power source.
    'battery_unplugged'
)


SecurityLevel = Enum(
    # Indicate that the alarm system of a tracker mobile device is active,
    # which is an alarm that the user manually arms when he leaves the
    # vehicle this device is mounted on.  The user will be urgently alerted
    # of any movement of his vehicle.
    'active',

    # Indicate that the alarm system of a tracker mobile device is disabled.
    'disabled',

    # Indicate that the alarm system of a tracker mobile device is passive,
    # which is an alarm that doesn't need to be manually armed when the user
    # leaves the vehicle this device is mounted on.  Instead, the alarm is
    # automatically activated when the vehicle doesn't move anymore after a
    # few seconds.  The user will be gently notified of any movement of his
    # vehicle.
    'passive'
)


ThreatLevel = Enum(
    'Critical',    # Red
    'Severe',      # Orange
    'Substantial', # Yellow
    'Moderate',    # Green
    'Low'          # Blue
)
