import argparse


class BaseOptions():
    def __init__(self):
        self.initialized = False
		
    def initialize(self, parser, ripdmp=False, incr=False, cripdmp = False):
        parser.add_argument('--saveimg', type=bool, default=False, help='save output images')
        parser.add_argument('--niter', type=int, default=50, help='number of repetition for each encounter')
        parser.add_argument('--nplay', type=int, default=50, help='number of players in the game')
        parser.add_argument('--nrep', type=int, default=10, help='number of repetition of the game')
        if cripdmp or ripdmp:
            #TODO CHECK HERE WHAT IS NECESSARY for cripdmp
            parser.add_argument('--maxallow', type=int, default=10, help='max number of repetition allowed')
            parser.add_argument('--percent', type=float, default=0.3, help='percentage of the population to be considered [if applicable]')
            if incr:
                parser.add_argument('--altern', type=int, default=1, help='choose between the kind of player generator')	
        self.initialized = True
        return parser
		
    def parse(self, ripdmp=False, incr=False, cripdmp=False):
        if not self.initialized:
            parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
            parser = self.initialize(parser, ripdmp, incr, cripdmp)
        opt, _ = parser.parse_known_args()
        self.parser = parser
        opt = parser.parse_args()
        if ripdmp:
            opt.nrep = 0
        self.opt = opt
        self.printer()
        return opt
   	
    def printer(self):
        message = ''
        message += '----------------- Options ---------------\n'
        for k, v in sorted(vars(self.opt).items()):
            comment = ''
            default = self.parser.get_default(k)
            if v != default:
                comment = '\t[default: %s]' % str(default)
            message += '{:>25}: {:<30}{}\n'.format(str(k), str(v), comment)
        message += '----------------- End -------------------'
        print(message)
