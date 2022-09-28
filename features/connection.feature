Feature: Startup

Scenario: Startup
        Given the device is in operation
        When its switched operation
        Then the LED lights

Scenario: CloseDown
        Given the device is in operation
        When its switched off
        Then the LED turns off
