Feature: Gauge Calibration and Movement

  Scenario: Calibrate the gauge
    Given the gauge is initialized
    When the gauge is calibrated
    Then the gauge should be calibrated

