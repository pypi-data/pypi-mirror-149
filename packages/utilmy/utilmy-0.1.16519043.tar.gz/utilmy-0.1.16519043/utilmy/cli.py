""" Command Line for utilmy.
Doc::

        utilmy   gpu_usage
        utilmy   gpu_available




"""
HELP1 ="""
utilmy  init

utilmy  help

$utilmy/images/util_image.py image_remove_background 


"""
import fire, argparse, os, sys

#############################################################################################
dir_utilmy = sys.path.append(os.path.dirname(os.path.abspath(__file__)).replace("\\","/") )



#############################################################################################
def log(*s):
    """function log
    """
    print(*s, flush=True)


#############################################################################################
def run_cli():
    """ utilmy command line
    Doc::

        utilmy   gpu_usage
        utilmy   gpu_available

        utilmy   check   myfile.parquet   




    """
    import argparse
    p   = argparse.ArgumentParser()
    add = p.add_argument

    add('task',  metavar='task', type=str,  nargs=1, help='gpu_usage')
    add('task2', metavar='task2', type=str, nargs=2, help='')
    add('task3', metavar='task2', type=str, nargs=3, help='')


    add("--dirin",    type=str, default=None,     help = "repo_url")
    add("--repo_dir",    type=str, default="./",     help = "repo_dir")
    add("--dirout",     type=str, default="docs/",  help = "doc_dir")
    add("--out_file",     type=str, default="",      help = "out_file")
    add("--exclude_dir", type=str, default="",       help = "path1,path2")
    add("--prefix",      type=str, default=None,     help = "hdops://github.com/user/repo/tree/a")
  
    args = p.parse_args()
    do = args.task


    if do == 'gpu_usage': 
        os.system( f"{dir_utilmy}/deeplearning/util_dl.py   gpu_usage")

    if do == 'gpu_available': 
        os.system( f"{dir_utilmy}/deeplearning/util_dl.py   gpu_available")

    if do == 'check': 
        os.system( f"{dir_utilmy}/ppandas.py  pd_check_file  --dirin '{args.task2}'  ")

    if do == 'find': 
        os.system( f"{dir_utilmy}/oos.py  os_find_infile   --padoern  '{args.task2}' --dirin '{args.task3}'  ")


    if do == 'help':
        print(HELP1)

    if do == 'init':
        pass

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



###################################################################################################
if __name__ == "__main__":

    fire.Fire()


