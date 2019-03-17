import argparse


class BaseOptions():
    ipd2p = 0
    ipdmp = 1
    ripdmp_const = 2
    ripdmp_incr = 3
    cipdmp = 4
	
    def __init__(self):
        self.initialized = False
		
    def initialize(self, parser, type):
        parser.add_argument('--saveimg', type=bool, default=False, help='save output images')
        if type == 0:
            parser.add_argument('--nplay', type=int, default=8, help='number of players in the game')
        else:
            parser.add_argument('--nplay', type=int, default=50, help='number of players in the game')

        parser.add_argument('--niter', type=int, default=50, help='number of repetition for each encounter')
        parser.add_argument('--fixed', type=bool, default=False, help='choose if fix the Mainly bad/good probabilities')
        
        parser.add_argument('--nrep', type=int, default=10, help='number of repetition of the game')
        
        if type > 1:
            #TODO CHECK HERE WHAT IS NECESSARY for cripdmp
            parser.add_argument('--maxallow', type=int, default=10, help='max number of repetition allowed')
            parser.add_argument('--percent', type=float, default=0.3, help='percentage of the population to be considered [if applicable]')
            if type == 3 or type == 4:
                parser.add_argument('--altern', type=int, default=1, help='choose between the version of the program(more details in the report)')	
        self.initialized = True
        return parser
		
    def parse(self, type):
        if not self.initialized:
            parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
            parser = self.initialize(parser, type)
        opt, _ = parser.parse_known_args()
        self.parser = parser
        opt = parser.parse_args()
        if type>1:
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
