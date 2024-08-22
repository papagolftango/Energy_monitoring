Feature: Gauge Motor Ranges

  Scenario Outline: Test gauge with different motor IDs and ranges
    Given the gauges are initialized
    When the gauge <motor_id> is moved to <move_to>
    Then the gauge <motor_id> should read <expected_value>

    Examples:
      | motor_id  | move_to   | expected_value   |
      | 0         | 100.0     | 100.0            |
      | 0         | -100.0    | -100.0           |
      | 1         | 1.0       | 1.0              |
      | 1         | -0.5      | 0.0              |
      | 2         | 1.0       | 1.0              |
      | 2         | -2.0      | -1.0             |
      | 3         | 17000.0   | 12000.0          |
      | 3         | -0.1      | -0.1             |