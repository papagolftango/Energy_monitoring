Feature: Gauge Motor Ranges

  Scenario Outline: Test gauge with different motor IDs and ranges
    Given the gauge is initialized with motor ID <motor_id> and min value <min_val> and max value <max_val>
    When the gauge is moved to <move_to>
    Then the gauge should read <expected_value>

    Examples:
      | motor_id | min_val | max_val | move_to | expected_value |
      | 0        | -100.0    | 100.0     | 100.0     | 100.0            |
      | 0        | -100.0    | 100.0     | -100.0    | -100             |
      | 1        | 0.0       | 1.0       | 1.0       | 1.0              |
      | 1        | 0.0       | 1.0       | -0.5      | 0.0              |
      | 2        | -1.0      | 1.0       | 1.0       | 1.0              |
      | 2        | -1.0      | 1.0       | -2.0      | -1.0             |
      | 3        | 0.0       | 0.5       | 0.6       | 0.5              |
      | 3        | 0.0       | 0.5       | -0.1      | 0.0              |