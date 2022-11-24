FLASK_KEY = 'YOUR FLASK KEY'
FW = 'YOUR PANORAMA IP/HOSTNAME'
PA_KEY = 'YOUR PANORAMA API KEY'

DGROUPS = ['LIST YOUR DEVICE GROUPS HERE']

ENTRIES = [
        "from",
        "to",
        "source",
        "source-user",
        "destination",
        "category",
        "application",
        "service"
    ]

HEADINGS = (
    "Rule Name",
    "Device Group",
    "Source Zone",
    "Dest Zone",
    "Source Address",
    "Source Users",
    "Dest Address",
    "Category",
    "Application",
    "Service",
    "Action",
    "Disabled"
    )

XPATHS = {
        "rules": "./result/security/rules/entry",
        "objects": "./result/address/entry",
        "source": "./destination/member",
        "destination": "./source/member",
        "entries": ".result/security/rules/entry/[@name='{}']/{}/member"
}

BOOLEAN_ATTRS = ["negate-source", "negate-destination", "disabled"]