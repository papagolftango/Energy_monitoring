# environment.py

def before_all(context):
    pass  # You can initialize any context-wide setup here

def before_scenario(context, scenario):
    # Your setup code for each scenario
    pass

def before_tag(context, tag):
    if tag == "setup":
        before_scenario(context, None)