"""Spark related utils
Doc::



"""
import os, sys, yaml
import pyspark

def log(*s):
    print(*s, flush=True)



########################################################################################
def spark_dataframe_check(df:pyspark.sql.DataFrame, tag="check", conf:dict=None, dirout:str= "", nsample:int=10,
                          save=True, verbose=True, returnval=False):
    """ Check dataframe for debugging
    Doc::
        Args:
            conf:  Configuration in dict
            df:
            dirout:
            nsample:
            save:
            verbose:
            returnval:
        Returns:
    """
    if conf is not None :
        confc = conf.get('Check', {})
        dirout = confc.get('path_check', dirout)
        save = confc.get('save', save)
        returnval = confc.get('returnval', returnval)
        verbose = confc.get('verbose', verbose)

    if save or returnval or verbose:
        df1 =   df.limit(nsample).toPandas()

    if save :
        ##### Need HDFS version
        os.makedirs(dirout, exist_ok=True)
        df1.to_csv(dirout + f'/table_{tag}.csv', sep='\t', index=False)

    if verbose :
        log(df1.head(2).T)
        log( df.printSchema() )

    if returnval :
        return df1






###############################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()


