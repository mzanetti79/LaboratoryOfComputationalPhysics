import argparse

class BaseOptions():
    #Constant values for each version of the Prisoner Dilemma game
    IPD2P = 0
    IPDMP = 1
    RIPDMP_C = 2
    RIPDMP_I = 3
    CIPDMP = 4
	
    def __init__(self):
        self.initialized = False
		
    def initialize(self, parser, case):
        parser.add_argument('--nplay', type=int, default=(8 if case==BaseOptions.IPD2P else 50), help='number of players in the game')
        parser.add_argument('--niter', type=int, default=50, help='number of repetitions for each match')

        if case < BaseOptions.RIPDMP_C:
            # only useful for 2p, mp
            parser.add_argument('--nrep', type=int, default=10, help='number of repetitions of the game')
        elif case > BaseOptions.IPDMP:
            # for ripdmp const, incr, cipdmp
            parser.add_argument('--maxrep', type=int, default=(5 if case>=BaseOptions.RIPDMP_I else 10), help='max number of allowed repetitions')
            if case != BaseOptions.CIPDMP:
                parser.add_argument('--percent', type=float, default=0.3, help='percentage of the population to be considered [if applicable]')
            if case == BaseOptions.RIPDMP_I or case == BaseOptions.CIPDMP:
                parser.add_argument('--altern', type=int, default=1, help='method to be used when changing population [details in the report]')	

        parser.add_argument('--seed', nargs='?', const=100, type=int, help='seed for the PRNG (not issued = clock-based; no number = 100 is used)')
        parser.add_argument('--fixed',   action='store_true', default=False, help='fix Mainly bad/good probabilities to 0.75/0.25')
        parser.add_argument('--saveimg', action='store_true', default=False, help='save output images instead of showing them')
        parser.add_argument('--latex',   action='store_true', default=False, help='output dataframes as latex code')

        self.initialized = True
        return parser
		
    def parse(self, case):
        if not self.initialized:
            parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
            parser = self.initialize(parser, case)
        opt = parser.parse_args()
        
        self.parser = parser
        self.opt = opt
        self.printer()
        return opt
   	
    def printer(self):
        message = ''
        message += '--- Options ---\n'
        for k, v in sorted(vars(self.opt).items()):
            comment = ''
            default = self.parser.get_default(k)
            if v != default:
                comment = '[default: {}]'.format(str(default))
            message += '{:>10}: {:<10}{}\n'.format(str(k), str(v), comment)
        message += '--- End ---'
        print(message)
