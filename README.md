Using the Alfen servicetool I managed to sniff the port 80 traffic to the charger. 

Example:

    ~/Projects/AlfenLaadpaal$ python3 -i alfencharger.py 
    >>> lp = AlfenCharger('10.4.101.119', 'admin', 'see-capture-wireshark')
    >>> lp.get_charge_status()
    {'max_current': 23.0, 'socket_state': 'idle'}
    >>> lp.set_charge_current(24)
    True
    >>> lp.get_charge_status()
    {'max_current': 24.0, 'socket_state': 'idle'}

