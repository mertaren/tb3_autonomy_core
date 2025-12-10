import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/mertaren/robot_ws/src/tb3_autonomy_core/install/tb3_autonomy'
