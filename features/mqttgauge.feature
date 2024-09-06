Feature: MQTT Gauge Test

  @use_real_mqtt
  Scenario: Check connection to the MQTT broker
    Given the MQTT broker is running on "192.168.68.86" and port "1883"
    Then the connection to the MQTT broker should be successful

  @use_real_mqtt
  Scenario: Discover gauges and save the response
    Given the MQTT broker is running on "192.168.68.86" and port "1883"
    When I publish a "discover" command to the topic "gauges/all/discover" with payload ""
    Then the response should be received on the topic "gauges/discover/status" with a list of gauges
    And each gauge should have a "name", "is_calibrated", and "range"
    And I save the response for later use

  @use_real_mqtt
  Scenario: Move each gauge to a value within range
    Given the saved response from the discover command
    When I publish a "move" command to each gauge with payload '{"position": <within_range_position>}'
    Then each gauge should move to the specified position within its range