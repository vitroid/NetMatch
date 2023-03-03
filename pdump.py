import pstats
import sys

sts = pstats.Stats(sys.argv[1])
sts.strip_dirs().sort_stats(-1).print_stats()
