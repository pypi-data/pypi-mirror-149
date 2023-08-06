"""Hadoop, hive related
Doc:

    python $utilmy/sspark/src/util_hadoop.py  print_env_variable
    utilmy spark print_config



"""
import os,sys


def log(*s):
  print(*s, flush=True)


def print_config(dirout=None):
  """ Print configuration variable for Hadoop, Spark


  """
  names =[
    'SPARK_HOME',
    'HADOOP_HOME'


  ]

  dd= []
  for ni in names:
    dd.append( [ni, os.environ.get(ni, '') ] )

  ### Print configuration files on disk
  ### SPARK_HOME/conf/spark_env.sh
  
   



def hdfs_download(from_dir="", to_dir="",  verbose=False, n_pool=1,   **kw):
  """  Donwload files in parallel using pyarrow
  Doc::

        path_glob: list of HDFS pattern, or sep by ";"
        :return:
  """
  import glob, gc,os
  from multiprocessing.pool import ThreadPool

  def log(*s, **kw):
      print(*s, flush=True, **kw)

  #### File ############################################
  import pyarrow as pa
  hdfs  = pa.hdfs.connect()
  flist = [ t for t in hdfs.ls(from_dir) ]

  def fun_async(x):
      hdfs.download(x[0], x[1])


  ######################################################
  file_list = sorted(list(set(flist)))
  n_file    = len(file_list)
  if verbose: log(file_list)

  #### Pool count
  if   n_pool < 1  :  n_pool = 1
  if   n_file <= 0 :  m_job  = 0
  elif n_file <= 2 :
    m_job  = n_file
    n_pool = 1
  else  :
    m_job  = 1 + n_file // n_pool  if n_file >= 3 else 1
  if verbose : log(n_file,  n_file // n_pool )

  pool   = ThreadPool(processes=n_pool)

  res_list=[]
  for j in range(0, m_job ) :
      if verbose : log("Pool", j, end=",")
      job_list = []
      for i in range(n_pool):
         if n_pool*j + i >= n_file  : break
         filei = file_list[n_pool*j + i]

         xi    = (filei,  to_dir + "/" + filei.split("/")[-1] )

         job_list.append( pool.apply_async(fun_async, (xi, )))
         if verbose : log(j, filei)

      for i in range(n_pool):
        if i >= len(job_list): break
        res_list.append( job_list[ i].get() )


  pool.close()
  pool.join()
  pool = None
  if m_job>0 and verbose : log(n_file, j * n_file//n_pool )
  return res_list

 


###############################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()

