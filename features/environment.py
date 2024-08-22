# environment.py
import sys
from unittest.mock import MagicMock

# Mock pigpio module before any other code runs
sys.modules['pigpio'] = MagicMock()

print("Loading environment.py") 

def before_all(context):
    # Additional context-wide setup can be done here
    print("Running additional context-wide setup")

def before_scenario(context, scenario):
    # Your setup code for each scenario
    print(f"Setting up for scenario: {scenario.name}")
    # Verify pigpio is mocked
    import pigpio
    print(f"pigpio is mocked: {isinstance(pigpio, MagicMock)}")

def before_tag(context, tag):
    if tag == "setup":
        before_scenario(context, None)





