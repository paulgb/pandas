from vbench.benchmark import Benchmark
from datetime import datetime

SECTION = 'Indexing and scalar value access'

common_setup = """from pandas_vb_common import *
"""

#----------------------------------------------------------------------
# Series.__getitem__, get_value

setup = common_setup + """
tm.N = 1000
ts = tm.makeTimeSeries()
dt = ts.index[500]
"""
statement = "ts[dt]"

bm_getitem = Benchmark(statement, setup, ncalls=100000,
                       name='series_getitem_scalar')

setup = common_setup + """
index = [tm.rands(10) for _ in xrange(1000)]
s = Series(np.random.rand(1000), index=index)
idx = index[100]
"""
statement = "s.get_value(idx)"
bm_df_getitem3 = Benchmark(statement, setup,
                           name='series_get_value',
                           start_date=datetime(2011, 11, 12))

#----------------------------------------------------------------------
# DataFrame __getitem__

setup = common_setup + """
index = [tm.rands(10) for _ in xrange(1000)]
columns = [tm.rands(10) for _ in xrange(30)]
df = DataFrame(np.random.rand(1000, 30), index=index,
               columns=columns)
idx = index[100]
col = columns[10]
"""
statement = "df[col][idx]"
bm_df_getitem = Benchmark(statement, setup,
                          name='dataframe_getitem_scalar')

setup = common_setup + """
try:
    klass = DataMatrix
except:
    klass = DataFrame

index = [tm.rands(10) for _ in xrange(1000)]
columns = [tm.rands(10) for _ in xrange(30)]
df = klass(np.random.rand(1000, 30), index=index,
               columns=columns)
idx = index[100]
col = columns[10]
"""
statement = "df[col][idx]"
bm_df_getitem2 = Benchmark(statement, setup,
                           name='datamatrix_getitem_scalar')


#----------------------------------------------------------------------
# ix get scalar

setup = common_setup + """
index = [tm.rands(10) for _ in xrange(1000)]
columns = [tm.rands(10) for _ in xrange(30)]
df = DataFrame(np.random.randn(1000, 30), index=index,
               columns=columns)
idx = index[100]
col = columns[10]
"""

indexing_frame_get_value_ix = Benchmark("df.ix[idx,col]", setup,
                                        name='indexing_frame_get_value_ix',
                                        start_date=datetime(2011, 11, 12))

indexing_frame_get_value = Benchmark("df.get_value(idx,col)", setup,
                                     name='indexing_frame_get_value',
                                     start_date=datetime(2011, 11, 12))

#----------------------------------------------------------------------
# Boolean DataFrame row selection

setup = common_setup + """
df  = DataFrame(np.random.randn(10000, 4), columns=['A', 'B', 'C', 'D'])
indexer = df['B'] > 0
obj_indexer = indexer.astype('O')
"""
indexing_dataframe_boolean_rows = \
    Benchmark("df[indexer]", setup, name='indexing_dataframe_boolean_rows')

indexing_dataframe_boolean_rows_object = \
    Benchmark("df[obj_indexer]", setup,
              name='indexing_dataframe_boolean_rows_object')

setup = common_setup + """
df  = DataFrame(np.random.randn(50000, 100))
df2 = DataFrame(np.random.randn(50000, 100))
"""
indexing_dataframe_boolean = \
    Benchmark("df > df2", setup, name='indexing_dataframe_boolean',
              start_date=datetime(2012, 1, 1))

setup = common_setup + """
import pandas.core.expressions as expr
df  = DataFrame(np.random.randn(50000, 100))
df2 = DataFrame(np.random.randn(50000, 100))
expr.set_numexpr_threads(1)
"""

indexing_dataframe_boolean_st = \
    Benchmark("df > df2", setup, name='indexing_dataframe_boolean_st',cleanup="expr.set_numexpr_threads()",
              start_date=datetime(2013, 2, 26))


setup = common_setup + """
import pandas.core.expressions as expr
df  = DataFrame(np.random.randn(50000, 100))
df2 = DataFrame(np.random.randn(50000, 100))
expr.set_use_numexpr(False)
"""

indexing_dataframe_boolean_no_ne = \
    Benchmark("df > df2", setup, name='indexing_dataframe_boolean_no_ne',cleanup="expr.set_use_numexpr(True)",
              start_date=datetime(2013, 2, 26))
#----------------------------------------------------------------------
# MultiIndex sortlevel

setup = common_setup + """
a = np.repeat(np.arange(100), 1000)
b = np.tile(np.arange(1000), 100)
midx = MultiIndex.from_arrays([a, b])
midx = midx.take(np.random.permutation(np.arange(100000)))
"""
sort_level_zero = Benchmark("midx.sortlevel(0)", setup,
                            start_date=datetime(2012, 1, 1))
sort_level_one = Benchmark("midx.sortlevel(1)", setup,
                           start_date=datetime(2012, 1, 1))

#----------------------------------------------------------------------
# Panel subset selection

setup = common_setup + """
p = Panel(np.random.randn(100, 100, 100))
inds = range(0, 100, 10)
"""

indexing_panel_subset = Benchmark('p.ix[inds, inds, inds]', setup,
                                  start_date=datetime(2012, 1, 1))

#----------------------------------------------------------------------
# Iloc

setup = common_setup + """
df = DataFrame({'A' : [0.1] * 3000, 'B' : [1] * 3000})
idx = np.array(range(30)) * 99
df2 = DataFrame({'A' : [0.1] * 1000, 'B' : [1] * 1000})
df2 = concat([df2, 2*df2, 3*df2])
"""

frame_iloc_dups = Benchmark('df2.iloc[idx]', setup,
                            start_date=datetime(2013, 1, 1))

frame_loc_dups = Benchmark('df2.loc[idx]', setup,
                            start_date=datetime(2013, 1, 1))
