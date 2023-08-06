#!python

"""
CLI to landscape API
"""

if __name__ == '__main__':

    import argh
    import atooms.landscape.api
    argh.dispatch_command(atooms.landscape.api.pes)
    
