#****************************************************************************
#*
#****************************************************************************

import subprocess
import os

def dot(args, in_s=None, out_s=None):
    pkg_dir=os.path.dirname(os.path.abspath(__file__))
    
    dot_bin=os.path.join(pkg_dir, "dot")
    
    if not os.path.isfile(dot_bin):
        raise Exception("Failed to find dot")
    
    cmdline = [dot_bin]
    cmdline.extend(args)

    if in_s is not None:
        with open("tmp.in", "w") as fp:
            fp.write(in_s.read())
        cmdline.append("tmp.in")
        
    if out_s is not None:
        cmdline.extend(['-o', "tmp.out"])            

    print("cmdline: %s" % str(cmdline))    
    p = subprocess.run(cmdline)
    
    if p.returncode != 0:
        raise Exception("Command run failed")
    
    if out_s is not None:
        with open("tmp.out", "r") as fp:
            out_s.write(fp.read())
    
    print("Dot")
    
    
    
    
