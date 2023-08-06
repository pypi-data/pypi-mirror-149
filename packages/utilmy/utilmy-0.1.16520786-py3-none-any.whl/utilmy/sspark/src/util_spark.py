"""Spark related utils
Doc::



"""
import os, sys, yaml
import calendar
import datetime
import json
import pytz
import subprocess
import time
import zlib

import pyspark
from pyspark import SparkConf
from pyspark.sql import SparkSession



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




class SparkEnv(object):

    def __init__(self, config=None):
        if config is not None:
            self.set_spark_config(config)

    @property
    def spark(self):
        if not hasattr(self, '_spark'):
            if not hasattr(self, '_spark_config'):
                raise Exception('No spark config specified')

            conf = SparkConf()
            conf.setAll(self._spark_config.get('extra_options').items())
            builder = SparkSession.builder.config(conf=conf)
            if self._spark_config.get('hive_support', False):
                builder = builder.enableHiveSupport()
            self._spark = builder.getOrCreate()
            for file in self._spark_config.get('extra_files', []) or []:
                self._spark.sparkContext.addPyFile(file)
        return self._spark

    def set_spark_config(self, config):
        self._spark_config = config

    def destroy_spark(self):
        if hasattr(self, '_spark'):
            self.spark.stop()
            delattr(self, '_spark')
        else:
            raise Exception('spark session was not initialized')



##################################################################################


from pyspark.sql.functions import col, explode, array, lit

def spark_over_sample_df(df,major_label, minor_label, ratio, label_col_name):
    print("Count of df before over sampling is  "+ str(df.count()))
    major_df = df.filter(col(label_col_name) == major_label)
    minor_df = df.filter(col(label_col_name) == minor_label)
    a = range(ratio)
    # duplicate the minority rows
    oversampled_df = minor_df.withColumn("dummy", explode(array([lit(x) for x in a]))).drop('dummy')
    # combine both oversampled minority rows and previous majority rows
    combined_df = major_df.unionAll(oversampled_df)
    print("Count of combined df after over sampling is  "+ str(combined_df.count()))
    return combined_df


def spark_under_sample_df(df,major_label, minor_label, ratio, label_col_name):
    print("Count of df before under sampling is  "+ str(df.count()))
    major_df = df.filter(col(label_col_name) == major_label)
    minor_df = df.filter(col(label_col_name) == minor_label)
    sampled_majority_df = major_df.sample(False, ratio,seed=33)
    combined_df = sampled_majority_df.unionAll(minor_df)
    print("Count of combined df after under sampling is  " + str(combined_df.count()))
    return combined_df




##################################################################################
from pyspark.mllib.evaluation import MulticlassMetrics
from pyspark.mllib.evaluation import BinaryClassificationMetrics

def spark_metrics_summary(labels_and_predictions_df):
    labels_and_predictions_rdd =labels_and_predictions_df.rdd.map(list)
    metrics = MulticlassMetrics(labels_and_predictions_rdd)
    # Overall statistics
    precision = metrics.precision()
    recall = metrics.recall()
    f1Score = metrics.fMeasure()
    confusion_metric = metrics.confusionMatrix
    print("Summary Stats")
    print("Precision = %s" % precision)
    print("Recall = %s" % recall)
    print("F1 Score = %s" % f1Score)
    print("Confusion Metrics = %s " %confusion_metric)
    # Weighted stats
    print("Weighted recall = %s" % metrics.weightedRecall)
    print("Weighted precision = %s" % metrics.weightedPrecision)
    print("Weighted F(1) Score = %s" % metrics.weightedFMeasure())
    print("Weighted F(0.5) Score = %s" % metrics.weightedFMeasure(beta=0.5))
    print("Weighted false positive rate = %s" % metrics.weightedFalsePositiveRate)


def spark_metrics_roc_summary(labels_and_predictions_df):
    labels_and_predictions_rdd =labels_and_predictions_df.rdd.map(list)
    metrics = BinaryClassificationMetrics(labels_and_predictions_rdd)
    # Area under precision-recall curve
    print("Area under PR = %s" % metrics.areaUnderPR)
    # Area under ROC curve
    print("Area under ROC = %s" % metrics.areaUnderROC)




##################################################################################
from pyspark import SparkConf
from pyspark.sql import SparkSession
import subprocess


def spark_get_session(configs):
    if not isinstance(configs, dict):
        raise Exception('spark configuration is not a dictionary {}'.format(configs))
    conf = SparkConf()
    conf.setAll(configs.items())
    spark = SparkSession.builder.config(conf=conf).enableHiveSupport().getOrCreate()
    return spark


def spark_execute_sqlfile(spark_config,sql_path):
    with open(sql_path) as fr:
        query = fr.read()
        results = spark_get_session(spark_config).sql(query)
        return results


def hdfs_mkdir(op_path):
    cat = subprocess.Popen(["hadoop", "fs", "-mkdir", "-p", op_path], stdout=subprocess.PIPE)

def hdfs_copy_to_hdfs_from_local(op_path, ip_path):
    rm_dir_hdfs(op_path)
    print("put from " + ip_path  + " to " + op_path)
    cat = subprocess.call(["hadoop", "fs", "-copyFromLocal", ip_path , op_path])


def hdfs_rm_dir(ip_path):
    if test_dir_exists_hdfs(ip_path):
        print("removing old file "+ip_path)
        cat = subprocess.call(["hadoop", "fs", "-rm", ip_path ])

def hdfs_dir_isexists(ip_path):
    return {0: True, 1: False}[subprocess.call(["hadoop", "fs", "-test", "-f", ip_path ])]

def hdfs_copy_to_local_from_hdfs(hdfs_path, local_path):
    cat = subprocess.call(["hadoop", "fs", "-copyToLocal", hdfs_path , local_path])







##################################################################################
def pa_read_file(path=  'hdfs://user/test/myfile.parquet/', 
                 cols=None, n_rows=1000, file_start=0, file_end=100000, verbose=1, ) :
    """ Requied HDFS connection
       conda install libhdfs3 pyarrow
       os.environ['ARROW_LIBHDFS_DIR'] = '/opt/cloudera/parcels/CDH/lib64/'
    """
    import pyarrow as pa, gc
    import pyarrow.parquet as pq
    hdfs = pa.hdfs.connect()    
    
    n_rows = 999999999 if n_rows < 0  else n_rows
    
    flist = hdfs.ls( path )  
    flist = [ fi for fi in flist if  'hive' not in fi.split("/")[-1]  ]
    flist = flist[file_start:file_end]  #### Allow batch load by partition
    if verbose : print(flist)
    dfall = None
    for pfile in flist:
        if not "parquet" in pfile and not ".db" in pfile :
            continue
        if verbose > 0 :print( pfile )            
                    
        arr_table = pq.read_table(pfile, columns=cols)
        df        = arr_table.to_pandas()
        del arr_table; gc.collect()
        
        dfall = pd.concat((dfall, df)) if dfall is None else df
        del df
        if len(dfall) > n_rows :
            break

    if dfall is None : return None        
    if verbose > 0 : print( dfall.head(2), dfall.shape )          
    dfall = dfall.iloc[:n_rows, :]            
    return dfall



##################################################################################
class TimeConstants:
    HOURS_PER_DAY = 24
    SECONDS_PER_DAY = 86400
    SECONDS_PER_HOUR = 3600
    UTC_TO_JST_SHIFT = 9 * 3600

def get_month_days(time):
    _, days = calendar.monthrange(time.year, time.month)
    return days

def get_intdate(seconds_adjust=0):
    """
    based on JST
    seconds_adjust = number of seconds in the future
    """
    t = time.time()
    t_struct = time.gmtime(t+9*3600+seconds_adjust)
    return time.strftime('%Y%m%d',t_struct)

def get_time_key(unix_ts):
    return int(unix_ts+9*3600)/86400

def get_unix_ts_from_datetime(dt_with_timezone):
    return time.mktime(dt_with_timezone.astimezone(pytz.utc).timetuple())

def get_unix_day_from_datetime(dt_with_timezone):
    return int(get_unix_ts_from_datetime(dt_with_timezone)) / TimeConstants.SECONDS_PER_DAY

def get_hour_range(dt, offset, output_format):
    hour_range = []
    for hr in xrange(offset):
        hour_range.append((dt + datetime.timedelta(hours=hr)).strftime(output_format))
    return hour_range

def get_time_now_with_timezone(timezone):
    return datetime.datetime.now(timezone)

def get_date_with_delta(time, days_delta):
    return time + datetime.timedelta(days=days_delta)

def get_start_of_month(time):
    return time.replace(day=1)

class ReportDateTime(object):
    def __init__(self, report_date, timezone):
        """
        report_date: datetime.date
        timezone: pytz.tzinfo
        """
        if type(report_date) is not datetime.date:
            raise TypeError('report_date {} must be datetime.date'.format(report_date))
        self._report_date = report_date
        self._timezone = timezone

    @property
    def report_datetime_notz(self):
        return datetime.datetime.combine(self._report_date, datetime.datetime.min.time())

    @property
    def report_datetime_localtz(self):
        return self._timezone.localize(self.report_datetime_notz)

    @property
    def report_datetime_utc(self):
        return self.report_datetime_localtz.astimezone(pytz.utc)

    @property
    def unix_timestamp_range(self):
        start = calendar.timegm(self.report_datetime_utc.utctimetuple())
        end = start + TimeConstants.SECONDS_PER_DAY
        return start, end

    @property
    def time_key_in_jst(self):
        return (self.unix_timestamp_range[0] + TimeConstants.UTC_TO_JST_SHIFT) / TimeConstants.SECONDS_PER_DAY

    @staticmethod
    def get_target_report_date(target_report_date, now, day_shift, datetime_format):
        if target_report_date is None:
            _target_report_date = get_date_with_delta(now, day_shift).date()
        else:
            _target_report_date = datetime.datetime.strptime(target_report_date, datetime_format).date()
        return _target_report_date

    @property
    def this_monday(self):
        return self._report_date - datetime.timedelta(days=self._report_date.weekday())

    @property
    def last_monday(self):
        return self.this_monday - datetime.timedelta(7)

def get_compressed_json(raw_obj):
    return zlib.compress(str.encode(json.dumps(raw_obj)))


def get_json_from_compressed(data):
    return json.loads(bytes.decode(zlib.decompress(data)))


def hdfs_file_exists(filename):
    ''' Return True when indicated file exists on HDFS.
    '''
    proc = subprocess.Popen(['hadoop', 'fs', '-test', '-e', filename])
    proc.communicate()

    if proc.returncode == 0:
        return True
    else:
        return False

def run_subprocess_cmd(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
    proc = subprocess.Popen(args_list, stdout=stdout, stderr=stderr)
    stdout, stderr = proc.communicate()
    return proc.returncode, stdout, stderr



###############################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()


