""" Command Line for utilmy

"""
HELP1 ="""
utilmy  init

utilmy  help

$utilmy/images/util_image.py image_remove_background 


"""
import fire, argparse, os, sys



#############################################################################################
def log(*s):
    """function log
    """
    print(*s, flush=True)


#############################################################################################
def run_cli():
    """
        utilmy   deeplearning.keras.util_my




    """
    import argparse
    p   = argparse.ArgumentParser()
    add = p.add_argument

    add('task',  metavar='task', type=str, nargs=1, help='colab')

    add('task2', metavar='task2', type=str, nargs=2, help='colab')

    add("--dirin",    type=str, default=None,     help = "repo_url")
    add("--repo_dir",    type=str, default="./",     help = "repo_dir")
    add("--dirout",     type=str, default="docs/",  help = "doc_dir")
    add("--out_file",     type=str, default="",      help = "out_file")
    add("--exclude_dir", type=str, default="",       help = "path1,path2")
    add("--prefix",      type=str, default=None,     help = "https://github.com/user/repo/tree/a")
  
    args = p.parse_args()


    if args.task == 'help':
        print(HELP1)

    if args.task == 'init':
        pass

    if args.task == 'colab':
        from utilmy import util_colab as mm
        mm.help()


    if "utilmy." in args.task or "utilmy/" in args.task :
        from utilmy.utilmy import load_function_uri
        uri = arg.task.replace(".", "/")  ### "utilmy.ppandas::test"
        dirfile  = "utilmy/" + args.task if 'utilmy/' not in args.task else args.task
        fun_name = args.task2

        cmd = f"{utilmy_dir)/{dirfile}  {fun_name}  {args_values}" 







#############################################################################################



###################################################################################################
if __name__ == "__main__":

    fire.Fire()


