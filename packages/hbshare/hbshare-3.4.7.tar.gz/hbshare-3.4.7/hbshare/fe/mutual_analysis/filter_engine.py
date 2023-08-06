import datetime
import pandas as pd
import numpy as np
from hbshare.fe.XZ import db_engine
from hbshare.fe.XZ import functionality


util=functionality.Untils()
hbdb=db_engine.HBDB()
localdb=db_engine.PrvFunDB().engine

jjdm_list = util.get_mutual_stock_funds(datetime.datetime.today().strftime('%Y%m%d'))
jjdm_con = util.list_sql_condition(jjdm_list)
sql = "select jjjc,jjdm from st_fund.t_st_gm_jjxx where jjdm in ({0})".format(jjdm_con)
jjdm_name_map = hbdb.db2df(sql, db='funduser')

class Equilibrium:

    @staticmethod
    def ind_equ():

        latest_asofdate=\
            pd.read_sql("select max(asofdate) as asofdate from hbs_industry_property_new ",con=localdb)['asofdate'][0]

        sql="SELECT jjdm,cen_ind_1,asofdate from hbs_industry_property_new where asofdate='{0}' order by cen_ind_1 ".format(latest_asofdate)
        ind_equ=pd.read_sql(sql,con=localdb)

        return ind_equ

    @staticmethod
    def style_equ():

        latest_asofdate = \
        pd.read_sql("select max(asofdate) as asofdate from hbs_style_property ", con=localdb)['asofdate'][0]

        sql="""SELECT jjdm,cen_lv_rank,asofdate 
        from hbs_style_property where asofdate='{0}' order by cen_lv_rank 
        """.format(latest_asofdate)
        style_equ = pd.read_sql(sql, con=localdb)

        return  style_equ

    @staticmethod
    def size_equ():

        latest_asofdate = \
        pd.read_sql("select max(asofdate) as asofdate from hbs_size_property ", con=localdb)['asofdate'][0]

        sql = """SELECT jjdm,cen_lv_rank,asofdate 
        from hbs_size_property where asofdate='{0}' order by cen_lv_rank 
        """.format(latest_asofdate)

        size_equ = pd.read_sql(sql, con=localdb)

        return  size_equ

    @staticmethod
    def pepbroe_equ():

        latest_asofdate = \
            pd.read_sql("select max(asofdate) as asofdate from hbs_holding_property ", con=localdb)[
                'asofdate'][0]

        sql="""
        select jjdm,PE_rank,PB_rank,ROE_rank,股息率_rank,asofdate 
        from hbs_holding_property where asofdate='{0}'
        """.format(latest_asofdate)

        pepbroe_equ=pd.read_sql(sql,con=localdb)
        pepbroe_equ[
            ['PE_rank','PB_rank','ROE_rank','股息率_rank']
        ]=abs(pepbroe_equ[['PE_rank','PB_rank','ROE_rank','股息率_rank']]-0.5)

        pepbroe_equ=pepbroe_equ.sort_values('PE_rank')

        return pepbroe_equ

    @staticmethod
    def nav_equ():

        latest_asofdate = \
            pd.read_sql("select max(asofdate) as asofdate from nav_ret_bias ", con=localdb)[
                'asofdate'][0]

        sql="""
        select jjdm,mean_rank_monthly,std_rank_monthly,mean_rank_weekly,std_rank_weekly,asofdate
        from nav_ret_bias where asofdate='{0}' order by mean_rank_monthly
        """.format(latest_asofdate)

        nav_equ=pd.read_sql(sql,con=localdb)

        return  nav_equ

    def get_equilibrium(self,threshield,show_num=300):

        # method_1
        ind_equ = self.ind_equ()
        style_equ = self.style_equ()
        size_equ = self.size_equ()
        pepbroe_equ = self.pepbroe_equ()
        nav_equ = self.nav_equ()

        #rename columns :
        ind_equ=pd.merge(ind_equ,
                         jjdm_name_map,
                         how='left', on='jjdm').\
            rename(columns={'cen_ind_1':'行业集中度'})

        style_equ=pd.merge(style_equ,
                         jjdm_name_map,
                         how='left', on='jjdm')\
            .rename(columns={'cen_lv_rank': '风格集中度'})

        size_equ=pd.merge(size_equ,
                         jjdm_name_map,
                         how='left', on='jjdm').\
            rename(columns={'cen_lv_rank': '规模集中度'})

        pepbroe_equ=pd.merge(pepbroe_equ,
                         jjdm_name_map,
                         how='left', on='jjdm').rename(columns={'PE_rank': 'pe偏离度',
                                    'PB_rank': 'pb偏离度',
                                    'ROE_rank': 'roe偏离度',
                                    '股息率_rank': '股息率偏离度'})

        nav_equ=pd.merge(nav_equ,
                         jjdm_name_map,
                         how='left', on='jjdm').rename(columns={'mean_rank_monthly': '净值偏离度（月）',
                                'std_rank_monthly': '净值偏离度方差（月）',
                                'mean_rank_weekly': '净值偏离度（周）',
                                'std_rank_weekly': '净值偏离度方差（周）',
                                })

        # method_2
        joint_rank = pd.merge(ind_equ, style_equ, how='inner', on=['jjdm','jjjc'])
        joint_rank = pd.merge(joint_rank, size_equ, how='inner', on=['jjdm','jjjc'])
        joint_rank = pd.merge(joint_rank, pepbroe_equ, how='inner', on=['jjdm','jjjc'])
        joint_rank = pd.merge(joint_rank, nav_equ, how='inner', on=['jjdm','jjjc'])

        col_list = ['行业集中度', '风格集中度',
                    '规模集中度', 'pe偏离度',
                    '净值偏离度（月）']

        joint_rank['平均集中度'] = joint_rank[col_list].mean(axis=1)
        joint_rank = joint_rank.sort_values('平均集中度')

        # method_3
        joint_result = joint_rank[(joint_rank[col_list] <= threshield).prod(axis=1) == 1][['jjdm','jjjc','asofdate'] + col_list]

        joint_rank=joint_rank[['jjdm','jjjc','平均集中度','asofdate']+col_list]


        #format change
        ind_equ['行业集中度'] = ind_equ['行业集中度'].map("{:.2%}".format)
        style_equ['风格集中度'] = style_equ['风格集中度'].map("{:.2%}".format)
        size_equ['规模集中度'] = size_equ['规模集中度'].map("{:.2%}".format)

        for col in ['pe偏离度','pb偏离度','roe偏离度','股息率偏离度']:
            pepbroe_equ[col] = pepbroe_equ[col].map("{:.2%}".format)
        for col in ['净值偏离度（月）', '净值偏离度方差（月）', '净值偏离度（周）', '净值偏离度方差（周）']:
            nav_equ[col] = nav_equ[col].map("{:.2%}".format)
        for col in col_list:
            joint_rank[col]=joint_rank[col].map("{:.2%}".format)
            joint_result[col]=joint_result[col].map("{:.2%}".format)
        joint_rank['平均集中度']=joint_rank['平均集中度'].map("{:.2%}".format)

        return ind_equ[0:show_num],style_equ[0:show_num],\
               size_equ[0:show_num],pepbroe_equ[0:show_num],nav_equ[0:show_num],\
               joint_rank[0:show_num],joint_result[0:show_num]

class Leftside:

    @staticmethod
    def stock_left():

        latest_asofdate=\
            pd.read_sql("select max(asofdate) as asofdate from hbs_stock_trading_property ",
                        con=localdb)['asofdate'][0]

        sql="""
        SELECT jjdm,`左侧概率（出持仓前,半年线）_rank`,`左侧概率（出持仓前,年线）_rank`,asofdate 
        from hbs_stock_trading_property where asofdate='{0}'  """\
            .format(latest_asofdate)
        stock_left=pd.read_sql(sql,con=localdb)

        stock_left['stock_left_rank']=stock_left[['左侧概率（出持仓前,半年线）_rank','左侧概率（出持仓前,年线）_rank']]\
            .max(axis=1)

        stock_left=stock_left.sort_values('stock_left_rank',ascending=False)

        return stock_left

    @staticmethod
    def ind_left():

        latest_asofdate = \
            pd.read_sql("select max(asofdate) as asofdate from hbs_industry_shift_property_new "
                        , con=localdb)['asofdate'][0]
        sql="""
        SELECT jjdm,项目名,Total_rank,asofdate 
        from hbs_industry_shift_property_new where asofdate='{0}' and (项目名='左侧比率' or 项目名='深度左侧比例') 
        """.format(latest_asofdate)
        ind_left=pd.read_sql(sql,con=localdb)

        ind_left=ind_left.groupby('jjdm').max('Total_rank')
        ind_left.reset_index(inplace=True)
        ind_left['asofdate']=latest_asofdate

        ind_left.sort_values('Total_rank',ascending=False,inplace=True)

        ind_left.rename(columns={'Total_rank':'ind_rank'},inplace=True)

        return ind_left

    @staticmethod
    def value_left():

        latest_asofdate = \
            pd.read_sql("select max(asofdate) as asofdate from hbs_shift_property_value "
                        , con=localdb)['asofdate'][0]
        sql="""
        SELECT jjdm,项目名,Total_rank,asofdate 
        from hbs_shift_property_value where asofdate='{0}' and (项目名='左侧比率' or 项目名='深度左侧比例') 
        """.format(latest_asofdate)
        value_left=pd.read_sql(sql,con=localdb)

        value_left=value_left.groupby('jjdm').max('Total_rank')
        value_left.reset_index(inplace=True)
        value_left['asofdate']=latest_asofdate

        value_left.sort_values('Total_rank',ascending=False,inplace=True)
        value_left.rename(columns={'Total_rank': 'value_rank'}, inplace=True)

        return value_left

    @staticmethod
    def size_left():

        latest_asofdate = \
            pd.read_sql("select max(asofdate) as asofdate from hbs_shift_property_size "
                        , con=localdb)['asofdate'][0]
        sql="""
        SELECT jjdm,项目名,Total_rank,asofdate 
        from hbs_shift_property_size where asofdate='{0}' and (项目名='左侧比率' or 项目名='深度左侧比例') 
        """.format(latest_asofdate)
        size_left=pd.read_sql(sql,con=localdb)

        size_left=size_left.groupby('jjdm').max('Total_rank')
        size_left.reset_index(inplace=True)
        size_left['asofdate']=latest_asofdate

        size_left.sort_values('Total_rank',ascending=False,inplace=True)
        size_left.rename(columns={'Total_rank': 'size_rank'}, inplace=True)


        return size_left

    def get_left(self,threshield,show_num=300):

        # method_1
        stock_left = self.stock_left()
        ind_left = self.ind_left()
        value_left = self.value_left()
        size_left = self.size_left()

        #rename columns
        stock_left=stock_left[['jjdm','stock_left_rank','asofdate']]

        stock_left=pd.merge(stock_left,jjdm_name_map,how='left',on='jjdm')\
            .rename(columns={'stock_left_rank':'个股交易左侧率'})
        ind_left = pd.merge(ind_left, jjdm_name_map, how='left', on='jjdm')\
            .rename(columns={'ind_rank':'行业切换左侧率'})
        value_left = pd.merge(value_left, jjdm_name_map, how='left', on='jjdm')\
            .rename(columns={'value_rank':'风格切换左侧率'})
        size_left = pd.merge(size_left, jjdm_name_map, how='left', on='jjdm')\
            .rename(columns={'size_rank':'规模切换左侧率'})


        # method_2
        joint_rank = pd.merge(stock_left, ind_left, how='inner', on=['jjdm','jjjc'])
        joint_rank = pd.merge(joint_rank, value_left, how='inner', on=['jjdm','jjjc'])
        joint_rank = pd.merge(joint_rank, size_left, how='inner', on=['jjdm','jjjc'])
        col_list = ['个股交易左侧率', '行业切换左侧率', '风格切换左侧率', '规模切换左侧率']
        joint_rank['平均左侧率'] = joint_rank[col_list].mean(axis=1)

        # method_3
        joint_restult = joint_rank[(joint_rank[col_list] >= (1 - threshield)).prod(axis=1) == 1][['jjdm','jjjc'] + col_list]

        joint_rank = joint_rank.sort_values('平均左侧率', ascending=False)[['jjdm','jjjc', '平均左侧率', 'asofdate_x']+col_list]


        #re format
        stock_left['个股交易左侧率']=stock_left['个股交易左侧率'].map("{:.2%}".format)
        ind_left['行业切换左侧率'] = ind_left['行业切换左侧率'].map("{:.2%}".format)
        value_left['风格切换左侧率'] = value_left['风格切换左侧率'].map("{:.2%}".format)
        size_left['规模切换左侧率'] = size_left['规模切换左侧率'].map("{:.2%}".format)
        for col in col_list:
            joint_rank[col] = joint_rank[col].map("{:.2%}".format)
            joint_restult[col] = joint_restult[col].map("{:.2%}".format)

        joint_rank['平均左侧率']=joint_rank['平均左侧率'].map("{:.2%}".format)

        return stock_left[0:show_num],ind_left[0:show_num],value_left[0:show_num],size_left[0:show_num],joint_rank[0:show_num],joint_restult[0:show_num]

class Size:
    @staticmethod
    def size_property(fre):
        latest_asofdate = pd.read_sql("select max(asofdate) as asofdate from hbs_size_property".format(fre), con=localdb)['asofdate'][0]
        sql = "select jjdm, shift_lv, cen_lv, shift_lv_rank, cen_lv_rank,大盘, 中盘, 小盘 ,大盘_rank, 中盘_rank, 小盘_rank, asofdate from hbs_size_property where asofdate='{0}'".format( latest_asofdate)
        size_property = pd.read_sql(sql, con=localdb)
        return size_property

    def get_size(self, fre, show_num=200, shift_ratio_threshold=0.5, centralization_threshold=0.5):
        size_property = self.size_property(fre)
        size_property.columns = ['jjdm', '换手率', '集中度', '换手率排名', '集中度排名','大盘(绝对值）', '中盘(绝对值）', '小盘(绝对值）' ,'大盘', '中盘', '小盘', 'asofdate']
        size_property = size_property.merge(jjdm_name_map, on=['jjdm'], how='left')

        size = size_property[(size_property['换手率排名'] < shift_ratio_threshold) & (size_property['集中度排名'] > centralization_threshold)]
        big_size = size[(size['大盘'] > size['中盘']) & (size['大盘'] > size['小盘'])].sort_values('大盘', ascending=False)
        medium_size = size[(size['中盘'] > size['大盘']) & (size['中盘'] > size['小盘'])].sort_values('中盘', ascending=False)
        small_size = size[(size['小盘'] > size['大盘']) & (size['小盘'] > size['中盘'])].sort_values('小盘', ascending=False)

        big_size = big_size[['jjdm', 'jjjc', 'asofdate', '大盘']]
        medium_size = medium_size[['jjdm', 'jjjc', 'asofdate', '中盘']]
        small_size = small_size[['jjdm', 'jjjc', 'asofdate', '小盘']]
        big_size['大盘'] = big_size['大盘'].map("{:.2%}".format)
        medium_size['中盘'] = medium_size['中盘'].map("{:.2%}".format)
        small_size['小盘'] = small_size['小盘'].map("{:.2%}".format)
        return big_size[0: show_num], medium_size[0: show_num], small_size[0: show_num]

class Value:
    @staticmethod
    def value_property(fre):
        latest_asofdate = pd.read_sql("select max(asofdate) as asofdate from hbs_style_property ", con=localdb)['asofdate'][0]
        sql = "select jjdm, shift_lv, cen_lv, shift_lv_rank, cen_lv_rank,成长,价值,成长_rank, 价值_rank, asofdate from hbs_style_property where  asofdate='{0}'".format(latest_asofdate)
        value_property = pd.read_sql(sql, con=localdb)
        return value_property

    @staticmethod
    def holding_property():
        latest_asofdate = pd.read_sql("select max(asofdate) as asofdate from hbs_holding_property", con=localdb)['asofdate'][0]
        sql = "select jjdm, PE_rank, PB_rank, PE_REL_rank, PB_REL_rank, ROE_rank, 股息率_rank, asofdate from hbs_holding_property where asofdate='{0}'".format(latest_asofdate)
        holding_property = pd.read_sql(sql, con=localdb)
        return holding_property

    def get_value(self, fre, show_num=200, shift_ratio_threshold=0.5, centralization_threshold=0.5):
        value_property = self.value_property(fre)
        value_property.columns = ['jjdm', '换手率', '集中度', '换手率排名', '集中度排名','成长（绝对值）', '价值（绝对值）' ,'成长', '价值', 'asofdate']
        value_property = value_property.merge(jjdm_name_map, on=['jjdm'], how='left')

        value = value_property[(value_property['换手率排名'] < shift_ratio_threshold) & (value_property['集中度排名'] > centralization_threshold)]
        growth = value[value['成长'] > value['价值']].sort_values('成长', ascending=False)
        value = value[value['价值'] > value['成长']].sort_values('价值', ascending=False)

        growth = growth[['jjdm', 'jjjc', 'asofdate', '成长']]
        value = value[['jjdm', 'jjjc', 'asofdate', '价值']]
        growth['成长'] = growth['成长'].map("{:.2%}".format)
        value['价值'] = value['价值'].map("{:.2%}".format)

        holding_property = self.holding_property()
        holding_property.columns = ['jjdm', 'PE排名', 'PB排名', 'PE相对行业均值排名', 'PB相对行业均值排名', 'ROE排名', '股息率排名', 'asofdate']
        value_holding_property = value.merge(holding_property.drop('asofdate', axis=1), on=['jjdm'], how='left')
        absolute_pe_value = value_holding_property.sort_values('PE排名')
        absolute_pb_value = value_holding_property.sort_values('PB排名')
        relative_pe_value = value_holding_property.sort_values('PE相对行业均值排名')
        relative_pb_value = value_holding_property.sort_values('PB相对行业均值排名')
        dividend_value = value_holding_property.sort_values('股息率排名', ascending=False)
        reverse_value = value_holding_property.sort_values('ROE排名')
        high_quality_value = value_holding_property.sort_values('ROE排名', ascending=False)

        absolute_pe_value = absolute_pe_value[['jjdm', 'jjjc', 'asofdate', '价值', 'PE排名']]
        absolute_pb_value = absolute_pb_value[['jjdm', 'jjjc', 'asofdate', '价值', 'PB排名']]
        relative_pe_value = relative_pe_value[['jjdm', 'jjjc', 'asofdate', '价值', 'PE相对行业均值排名']]
        relative_pb_value = relative_pb_value[['jjdm', 'jjjc', 'asofdate', '价值', 'PB相对行业均值排名']]
        dividend_value = dividend_value[['jjdm', 'jjjc', 'asofdate', '价值', '股息率排名']]
        reverse_value = reverse_value[['jjdm', 'jjjc', 'asofdate', '价值', 'ROE排名']]
        high_quality_value = high_quality_value[['jjdm', 'jjjc', 'asofdate', '价值', 'ROE排名']]

        absolute_pe_value['PE排名'] = absolute_pe_value['PE排名'].map("{:.2%}".format)
        absolute_pb_value['PB排名'] = absolute_pb_value['PB排名'].map("{:.2%}".format)
        relative_pe_value['PE相对行业均值排名'] = relative_pe_value['PE相对行业均值排名'].map("{:.2%}".format)
        relative_pb_value['PB相对行业均值排名'] = relative_pb_value['PB相对行业均值排名'].map("{:.2%}".format)
        dividend_value['股息率排名'] = dividend_value['股息率排名'].map("{:.2%}".format)
        reverse_value['ROE排名'] = reverse_value['ROE排名'].map("{:.2%}".format)
        high_quality_value['ROE排名'] = high_quality_value['ROE排名'].map("{:.2%}".format)
        return growth[0: show_num], value[0: show_num], absolute_pe_value[0: show_num], absolute_pb_value[0: show_num], \
               relative_pe_value[0: show_num], relative_pb_value[0: show_num], dividend_value[0: show_num], \
               reverse_value[0: show_num], high_quality_value[0: show_num]

if __name__ == '__main__':


    # equclass=Equilibrium()
    # ind_equ, style_equ,size_equ, \
    # pepbroe_equ, nav_equ,joint_rank, \
    # joint_result=equclass.get_equilibrium(threshield=0.3,show_num=200)
    #
    #
    # plot=functionality.Plot(800,800)
    # plot.plotly_table(joint_result,800,'asdf')
    # plot.plotly_table(joint_rank, 800, 'asdf')
    # plot.plotly_table(ind_equ, 800, 'asdf')
    # plot.plotly_table(style_equ, 800, 'asdf')
    # plot.plotly_table(size_equ, 800, 'asdf')
    # plot.plotly_table(pepbroe_equ, 800, 'asdf')
    # plot.plotly_table(nav_equ, 800, 'asdf')
    #
    # leftclass=Leftside()
    #
    # stock_left, ind_left, value_left, \
    # size_left, joint_rank, joint_restult=leftclass.get_left(threshield=0.3,show_num=200)
    #
    #
    # plot=functionality.Plot(800,800)
    # plot.plotly_table(stock_left,800,'asdf')
    # plot.plotly_table(ind_left, 800, 'asdf')
    # plot.plotly_table(value_left, 800, 'asdf')
    # plot.plotly_table(size_left, 800, 'asdf')
    # plot.plotly_table(joint_rank, 800, 'asdf')
    # plot.plotly_table(joint_restult, 800, 'asdf')

    sizeclass = Size()
    big_size, medium_size, small_size = sizeclass.get_size(fre='M', show_num=200, shift_ratio_threshold=0.5, centralization_threshold=0.5)

    plot = functionality.Plot(800, 800)
    plot.plotly_table(big_size, 800, 'asdf')
    plot.plotly_table(medium_size, 800, 'asdf')
    plot.plotly_table(small_size, 800, 'asdf')

    valueclass = Value()
    growth, value, absolute_pe_value, absolute_pb_value, relative_pe_value, relative_pb_value, \
    dividend_value, reverse_value, high_quality_value = valueclass.get_value(fre='M', show_num=200, shift_ratio_threshold=0.5, centralization_threshold=0.5)

    plot = functionality.Plot(800, 800)
    plot.plotly_table(growth, 800, 'asdf')
    plot.plotly_table(value, 800, 'asdf')
    plot.plotly_table(absolute_pe_value, 800, 'asdf')
    plot.plotly_table(absolute_pb_value, 800, 'asdf')
    plot.plotly_table(relative_pe_value, 800, 'asdf')
    plot.plotly_table(relative_pb_value, 800, 'asdf')
    plot.plotly_table(dividend_value, 800, 'asdf')
    plot.plotly_table(reverse_value, 800, 'asdf')
    plot.plotly_table(high_quality_value, 800, 'asdf')

    # print("Done")


