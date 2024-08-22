Feature: Gauge Calibration and Movement

 # Scenario: Calibrate all gauges
 #   Given the gauges are initialized
 #   When all gauges are calibrated
 #   Then all gauges should be calibrated

 # Scenario: Move a specific gauge to a specific value
 #   Given the gauges are initialized
  #  When the gauge 0 is moved to 50.0
  #  Then the gauge 0 should read 50.0

#  Scenario: Move a gauge beyond its maximum limit
 #   Given the gauges are initialized
#    When the gauge 1 is moved to 1.1
#    Then the gauge 1 should read its maximum value

  Scenario: Move a gauge below its minimum limit
    Given the gauges are initialized
    When the gauge 2 is moved to -10.0
    Then the gauge 2 should read its minimum value