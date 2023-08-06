#!/usr/bin/env python3

from McUnix.diff import argue, diff

args = argue()
diff(args.lhs.rstrip('/'), args.rhs.rstrip('/'))

