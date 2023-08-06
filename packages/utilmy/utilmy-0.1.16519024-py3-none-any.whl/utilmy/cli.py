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
dir_utilmy = sys.path.append(os.path.dirname(os.path.abspath(__file__)))



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
    add("--prefix",      type=str, default=None,     help = "https://github.com/user/repo/tree/a")
  
    args = p.parse_args()


    if args.task == 'gpu_usage': 
        os.system( f"{dir_utilmy}/deeplearning/util_dl.py   gpu_usage")

    if args.task == 'gpu_available': 
        os.system( f"{dir_utilmy}/deeplearning/util_dl.py   gpu_available")

    if args.task == 'check': 
        os.system( f"{dir_utilmy}/ppandas.py  pd_check_file  --dirin '{args.task2}'  ")

    if args.task == 'find': 
        os.system( f"{dir_utilmy}/oos.py  os_find_infile   --pattern  '{args.task2}' --dirin '{args.task3}'  ")


    if args.task == 'help':
        print(HELP1)

    if args.task == 'init':
        pass

    if args.task == 'colab':
        from utilmy import util_colab as mm
        mm.help()


    if "utilmy." in args.task or "utilmy/" in args.task :
        from utilmy.utilmy import load_function_uri
        uri = args.task.replace(".", "/")  ### "utilmy.ppandas::test"
        dirfile  = "utilmy/" + args.task if 'utilmy/' not in args.task else args.task
        fun_name = args.task2

        cmd = f"{dir_utilmy}/{dirfile}  {fun_name}  "
        os.system(cmd)






#############################################################################################



###################################################################################################
if __name__ == "__main__":

    fire.Fire()


