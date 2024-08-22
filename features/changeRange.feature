Feature: Change Gauge Range
  As a user
  I want to change the max and min values of the gauges on the fly
  So that I can dynamically adjust the gauge ranges

  Background:
    Given the gauges are initialized

  Scenario Outline: Change max and min values of a gauge
    Given the gauge <gauge_id> has a max value of <initial_max> and a min value of <initial_min>
    When I set the max value of gauge <gauge_id> to <new_max>
    And I set the min value of gauge <gauge_id> to <new_min>
    Then the gauge <gauge_id> should have a max value of <new_max>
    And the gauge <gauge_id> should have a min value of <new_min>

    Examples:
      | gauge_id | initial_max | initial_min | new_max | new_min |
      | 0        | 100.0       | -100.0      | 200.0   | -200.0  |
      | 1        | 1.0         | 0.0         | 2.0     | -1.0    |

  Scenario Outline: Move gauge within new range
    Given the gauge <gauge_id> has a max value of <initial_max> and a min value of <initial_min>
    When I set the max value of gauge <gauge_id> to <new_max>
    And I set the min value of gauge <gauge_id> to <new_min>
    And I move the gauge <gauge_id> to <move_value>
    Then the gauge <gauge_id> should read <expected_value>

    Examples:
      | gauge_id | initial_max | initial_min | new_max | new_min | move_value | expected_value |
      | 1        | 1.0         | 0.0         | 2.0     | -1.0    | 1.5        | 1.5            |

  Scenario Outline: Move gauge beyond new range
    Given the gauge <gauge_id> has a max value of <initial_max> and a min value of <initial_min>
    When I set the max value of gauge <gauge_id> to <new_max>
    And I set the min value of gauge <gauge_id> to <new_min>
    And I move the gauge <gauge_id> to <move_value>
    Then the gauge <gauge_id> should read <expected_value>

    Examples:
      | gauge_id | initial_max | initial_min | new_max | new_min | move_value | expected_value |
      | 2        | 1.0         | -1.0        | 3.0     | -3.0    | 4.0        | 3.0            |
      | 2        | 1.0         | -1.0        | 3.0     | -3.0    | -4.0       | -3.0           |