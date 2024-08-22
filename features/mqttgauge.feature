Feature: MQTT Gauge Interaction
  As a user
  I want to interact with gauges via MQTT
  So that I can query information, calibrate, and move the gauges

  Background:
    Given the MQTT broker is running on "localhost" and port "1883"
    And the gauges are ready

  Scenario: Query gauge information
    Given I subscribe to the topic "gauges/Motor 1/query"
    When I publish a message to the topic "gauges/Motor 1/query"
    Then I should receive a message on the topic "gauges/Motor 1/response"
    And the message should contain the gauge information

  Scenario: Command gauge calibration
    Given I subscribe to the topic "gauges/Motor 1/calibrate"
    When I publish a message to the topic "gauges/Motor 1/calibrate"
    Then I should receive a message on the topic "gauges/Motor 1/response"
    And the message should indicate the gauge is calibrated

  Scenario: Move gauge to a position
    Given I subscribe to the topic "gauges/Motor 1/move"
    When I publish a message "50.0" to the topic "gauges/Motor 1/move"
    Then I should receive a message on the topic "gauges/Motor 1/response"
    And the message should indicate the gauge position is "50.0"