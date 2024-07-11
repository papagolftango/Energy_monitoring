Feature: Startup



  Scenario: Move to a value within range
    Given a GaugeStepper with a range from 0 to 100
    When I move the gauge to 50
    Then the gauge position should be 50
    And the motor should have moved 50 steps

  Scenario: Move to a value above the maximum
    Given a GaugeStepper with a range from 0 to 100
    When I move the gauge to 150
    Then the gauge position should be 100

  Scenario: Move to a value below the minimum
    Given a GaugeStepper with a range from 0 to 100
    When I move the gauge to -10
    Then the gauge position should be 0

  Scenario: Calibrate the gauge
    Given a GaugeStepper with a range from 0 to 100
    When I calibrate the gauge
    Then the motor should return to the start position
    And the gauge should be calibrated
