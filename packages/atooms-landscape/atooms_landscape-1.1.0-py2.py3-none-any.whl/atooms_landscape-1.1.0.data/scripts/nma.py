#!python

"""
CLI to landscape normal modes analysis
"""

if __name__ == '__main__':

    import argh
    import atooms.energy_landscape.api
    argh.dispatch_command(atooms.energy_landscape.api.nma)
    
