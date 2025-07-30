instr = {
    'conn': {},
    'flux': {}
}


mb_reg = {
    'Function': {
        'reg': 130,
        'desc': 'Product Address',
        'value': 0,
    },
    'Serial number': {
        'reg': 49,
        'desc': 'Serial number of the product',
        'value': 0,
    },
    'Flow rate 1': {
        'reg': 59,
        'desc': 'Serial number of the product',
        'value': 0,
    },
    'Flow rate 2': {
        'reg': 60,
        'desc': 'Serial number of the product',
        'value': 0,
    },
    'Baud rate': {
        'reg': 131,
        'desc': 'Communication baud rate',
        'value': 0,
    },
    'Set point source': {
        'reg': 187,
        'desc': 'Set the setpoint source',
        'value': 0,
    },
    'Set point Flow Code': {
        'reg': 188,
        'desc': 'Set the flow rate in percentage of the full-scale flow',
        'value': 0,
    },
    'Flow1': {
        'reg': 189,
        'desc': 'Read the current flow rate set by the user',
        'value': 0,
    },
    'Flow2': {
        'reg': 190,
        'desc': 'Read the current flow rate set by the user',
        'value': 0,
    },
    'P gain': {
        'reg': 191,
        'desc': 'PD proportional control of the valve/flow rate',
        'value': 0,
    },
    'D gain': {
        'reg': 192,
        'desc': 'PD differential control of the valve/flow rate',
        'value': 0,
    },
    'Valve preload offset': {
        'reg': 193,
        'desc': 'Default or preloaded valve opening',
        'value': 0,
    },
    'Exhaust mode': {
        'reg': 194,
        'desc': 'Set the exhaust mode',
        'value': 0,
    },
    'Exhaust valve': {
        'reg': 195,
        'desc': 'Percentage of the opened valve (Open loop control)',
        'value': 0,
    },
    'Valve status': {
        'reg': 196,
        'desc': 'Percentage of the opened valve',
        'value': 0,
    },
    # 'Offset calibration': {
    #     'reg': 241,
    #     'desc': 'Offset reset or calibration',
    #     'value': 0,
    # },
    # 'Write protection': {
    #     'reg': 256,
    #     'desc': 'Write protection of selected parameters',
    #     'value': 0,
    # },
    'GCF': {
        'reg': 140,
        'desc': 'Write protection of selected parameters',
        'value': 0,
    },
}


par = {
    'set': 0,
    'read': 0,
}