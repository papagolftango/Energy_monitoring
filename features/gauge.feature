Feature: Gauge Calibration and Movement

  Scenario: Calibrate the gauge
    Given the gauge is initialized
    When the gauge is calibrated
    Then the gauge should be calibrated

  Scenario: Move the gauge to a specific value
    Given the gauge is calibrated
    When the gauge is moved to 50
    Then the gauge should read 50

  Scenario: Move the gauge beyond its maximum limit
    Given the gauge is calibrated
    When the gauge is moved to 7000
    Then the gauge should read its maximum value

  Scenario: Move the gauge below its minimum limit
    Given the gauge is calibrated
    When the gauge is moved to -10
    Then the gauge should read its minimum value