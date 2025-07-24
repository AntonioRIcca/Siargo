from pymodbus.client import ModbusSerialClient  # per pymodbus 3.3.x e Python 3.11


mb_conn = True

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
    'Current flow rate': {
        'reg': 59,
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
    'Set point flow': {
        'reg': 189,
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

client = ModbusSerialClient(
    port="COM6",  # TODO: inserire la COM esatta
    startbit=1,
    databits=8,
    parity="N",
    stopbits=2,
    errorcheck="crc",
    baudrate=38400,
    method="RTU",
    timeout=3,
    # unit=31
)

results = [0, 0, 0, 0, 0, 0, 0, 0]
if client.connect():  # Connessione al dispositivo
    registers = 250
    results = []
    addr = 0
    while addr < registers:
        count = min(100, registers-addr)
        results += client.read_holding_registers(address=addr, count=count, slave=1).registers
        addr += count

else:
    mb_conn = False

# print(mb_conn)
# print(results)
# print(len(results))

for par in mb_reg:
    addr = mb_reg[par]['reg'] - 1
    mb_reg[par]['value'] = results[addr]

    print(par, addr, mb_reg[par]['value'])


if client.connect():  # Connessione al dispositivo
    client.write_register(slave=1, address=187, value=int(0.0*64000))

if client.connect():  # Connessione al dispositivo
    registers = 250
    results = []
    addr = 0
    while addr < registers:
        count = min(100, registers-addr)
        results += client.read_holding_registers(address=addr, count=count, slave=1).registers
        addr += count
else:
    mb_conn = False

for par in mb_reg:
    addr = mb_reg[par]['reg'] - 1
    mb_reg[par]['value'] = results[addr]

    print(par, addr, mb_reg[par]['value'])
