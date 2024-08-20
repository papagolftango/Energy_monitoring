Feature: Gauge Multiple Motors Parallel Movement

  Scenario: Test multiple motors moving in parallel
    Given the gauges are initialized with the following parameters
      | motor_id | min_val | max_val |
      | 0        | -100.0  | 100.0   |
      | 1        | 0.0     | 1.0     |
      | 2        | -1.0    | 1.0     |
      | 3        | 0.0     | 0.5     |
    When the gauges are moved to the following positions
      | motor_id | move_to |
      | 0        | 50.0    |
      | 1        | 0.5     |
      | 2        | -0.5    |
      | 3        | 0.25    |
    Then the gauges should read the following values
      | motor_id | expected_value |
      | 0        | 50.0           |
      | 1        | 0.5            |
      | 2        | -0.5           |
      | 3        | 0.25           |