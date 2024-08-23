Feature: MQTT Gauge Test for Motor 1

  @use_real_mqtt
  Scenario: Test query command with real MQTT broker for Motor 1
    Given the MQTT broker is running on "192.168.68.86" and port "1883"
    When I publish a "query" command to the gauge "Motor 1" with payload ""
    Then the response should be received on the gauge "Motor 1" with payload '{"name": "Motor 1", "min_val": -100.0, "max_val": 100.0, "calibrated": true, "position": 0.0}'1883