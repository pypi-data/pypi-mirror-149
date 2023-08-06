""" Command Line for utilmy.
Doc::

        utilmy  help
        utilmy  gpu_usage
        utilmy  gpu




"""
HELP1 ="""
Commands:

    utilmy  gpu
    utilmy  gpu_usage
    python $utilmy/images/util_image.py image_remove_background 


"""
import fire, argparse, os, sys
from utilmy.parallel import pd_read_file


#############################################################################################
from utilmy.utilmy import log
from utilmy.utilmy import os_system   

#############################################################################################
try :
   import utilmy 
   dir_utilmy =  utilmy.__path__[0].replace("\\","/")  + "/"
except:   
   dir_utilmy = os.path.dirname(os.path.abspath(__file__)).replace("\\","/") 



#############################################################################################
def run_cli():
    """ utilmy command line
    Doc::

        utilmy   gpu_usage
        utilmy   gpu

        utilmy   show   myfile.parquet




    """
    import argparse 
    p   = argparse.ArgumentParser()
    add = p.add_argument

    add('task',  metavar='task',  type=str,  nargs="?", help='gpu,gpu_usage')
    add('arg2', metavar='arg2', type=str, nargs="?", help='')
    add('arg3', metavar='arg3', type=str, nargs="?", help='')


    add("--dirin",        type=str, default='gpu',     help = "repo_url")
    add("--repo_dir",     type=str, default="./",      help = "repo_dir")
    add("--dirout",       type=str, default="docs/",   help = "doc_dir")
    add("--fileout",      type=str, default="",        help = "out_file")
    add("--dir_exclude",  type=str, default="",        help = "path1,path2")
    add("--verbose",      type=int, default=0,         help = "hdops://github.com/user/repo/tree/a")
  
    args = p.parse_args()
    do = args.task

    if args.verbose > 0 : 
        log(dir_utilmy)

    if do == 'help':
        print(HELP1)

    if do == 'init':
        pass

    #################################################################################################
    if do == 'gpu_usage': 
        ss=  os_system( f"python {dir_utilmy}/deeplearning/util_dl.py   gpu_usage", doprint=True)

    if do == 'gpu': 
        ss = os_system( f"python {dir_utilmy}/deeplearning/util_dl.py   gpu_available",doprint=True)
        # log(ss[0])

    if do == 'show':
        ss = os_system( f"python {dir_utilmy}/cli.py  run_show  --dirin '{args.arg2}'  ",doprint=True)
        log(ss)

    if do == 'find': 
        os_system( f"{dir_utilmy}/oos.py  os_find_infile   --pattern  '{args.arg2}' --dirin '{args.arg3}'  ")


    if do == 'colab':
        from utilmy import util_colab as mm
        mm.help()


    if "utilmy." in do or "utilmy/" in do :
        from utilmy.utilmy import load_function_uri
        uri = do.replace(".", "/")  ### "utilmy.ppandas::test"
        dirfile  = "utilmy/" + do if 'utilmy/' not in do else do
        fun_name = args.task

        cmd = f"{dir_utilmy}/{dirfile}  {fun_name}  "
        os.system(cmd)


#############################################################################################
def run_show(dirin:str):
   if ".py" in dirin :
       os_system( f'cat {dirin}', doprint=True)
   
   if ".parquet" in dirin :
       from utilmy import pd_read_file
       df = pd_read_file(dirin)
       print(df)






#############################################################################################



###################################################################################################
if __name__ == "__main__":
    run_cli()
    # fire.Fire()


