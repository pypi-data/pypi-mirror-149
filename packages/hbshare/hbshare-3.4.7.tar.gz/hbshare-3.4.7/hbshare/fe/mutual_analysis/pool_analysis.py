import datetime
import pandas as pd
import numpy as np
from hbshare.fe.XZ import db_engine
from hbshare.fe.XZ import functionality
from hbshare.fe.mutual_analysis import  jj_picturing as jjpic
from ortools.linear_solver import  pywraplp



util=functionality.Untils()
hbdb=db_engine.HBDB()
localdb=db_engine.PrvFunDB().engine
plot=functionality.Plot(1000,600)


def get_core_pool():

    sql="select jjdm,jjjc from st_fund.t_st_gm_jjxx where hxbz='1' and cpfl='2' "
    pool=hbdb.db2df(sql,db='funduser')

    return  pool

def get_jj_picture(jjdm_con=None,if_inverse=False):

    if(if_inverse):
        inornot='not in '
    else:
        inornot='in'

    value_df_list = [pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(),
                     pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()]

    industry_df_list = [pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()]


    stock_df_list = [pd.DataFrame(), pd.DataFrame()]


    if(jjdm_con is not None):
        value_p, value_p_hbs, value_sp, value_sp_hbs, size_p, size_p_hbs, size_sp, size_sp_hbs, \
        industry_p, industry_sp, theme_p, theme_sp, industry_detail_df_list, stock_p, stock_tp=\
            jjpic.get_pic_from_localdb("jjdm {1} ({0})".format(jjdm_con,inornot), if_percentage=False)
    else:
        value_p, value_p_hbs, value_sp, value_sp_hbs, size_p, size_p_hbs, size_sp, size_sp_hbs, \
        industry_p, industry_sp, theme_p, theme_sp, industry_detail_df_list, stock_p, stock_tp=\
            jjpic.get_pic_from_localdb("1=1", if_percentage=False)

    value_df_list[0]=value_p
    value_df_list[1] = value_p_hbs
    value_df_list[2] = value_sp
    value_df_list[3] = value_sp_hbs
    value_df_list[4] = size_p
    value_df_list[5] = size_p_hbs
    value_df_list[6] = size_sp
    value_df_list[7] = size_sp_hbs

    industry_df_list[0]=industry_p
    industry_df_list[1] = industry_sp
    industry_df_list[2] = theme_p
    industry_df_list[3] = theme_sp
    for j in range(len(industry_detail_df_list)):
        # industry_detail_df_list[j]['jjdm'] = jjdm
        industry_detail_df_list[j]['industry_level'] = j + 1
        industry_df_list[4] = pd.concat([industry_df_list[4], industry_detail_df_list[j]], axis=0)

    stock_df_list[0]=stock_p
    stock_df_list[1] = stock_tp

    return value_df_list,industry_df_list,stock_df_list

def features_calculation(value_df_list, industry_df_list, stock_df_list):

    industry_style=industry_df_list[0].groupby('一级行业类型').count()['jjdm'].to_frame('num')
    industry_style=industry_style/len(industry_df_list[0])*100
    industry_style_dis = (industry_df_list[4].groupby(['industry_level', '行业名称']).mean() * 100).reset_index()[
        ['industry_level', '行业名称', '占持仓比例(时序均值)', '占持仓比例(时序均值)排名']]
    #take industry with weight more than 5%
    industry_style_dis=industry_style_dis[industry_style_dis['占持仓比例(时序均值)'] >= 5]
    class_list=[]
    for i in range(3):
        class_list.append(industry_style_dis[industry_style_dis['industry_level'] == (i + 1)] \
            .sort_values('占持仓比例(时序均值)', ascending=False).set_index('行业名称').drop('industry_level', axis=1))

    style_type_dis = value_df_list[1].groupby('风格类型').count()['jjdm'].to_frame('风格类型') \
                     / len(value_df_list[1]) * 100
    style_incline_dis=value_df_list[1][value_df_list[1]['风格类型']=='专注'][['风格类型','风格偏好']]
    style_incline_dis=style_incline_dis.groupby('风格偏好').count()/len(style_incline_dis)*100
    style_weight_dis=value_df_list[1][['成长绝对暴露(持仓)',
       '价值绝对暴露(持仓)','成长暴露排名(持仓)', '价值暴露排名(持仓)']].mean(axis=0).to_frame('成长价值权重分布')*100

    style_type_dis2 = value_df_list[5].groupby('规模风格类型').count()['jjdm'].to_frame('规模风格类型') \
                      / len(value_df_list[5]) * 100
    style_incline_dis2=value_df_list[5][value_df_list[5]['规模风格类型']=='专注'][['规模风格类型','规模偏好']]
    style_incline_dis2=style_incline_dis2.groupby('规模偏好').count()/len(style_incline_dis2)*100
    style_weight_dis2=value_df_list[5][['大盘绝对暴露(持仓)',
       '中盘绝对暴露(持仓)', '小盘绝对暴露(持仓)','大盘暴露排名(持仓)',
       '中盘暴露排名(持仓)', '小盘暴露排名(持仓)']].mean(axis=0).to_frame('成长价值权重分布')*100

    stock_style_a=stock_df_list[0].groupby('个股风格A').count()['jjdm'].to_frame('个股风格类型A')\
                  /(len(stock_df_list[0])*100)
    stock_style_b = stock_df_list[0].groupby('个股风格B').count()['jjdm'].to_frame('个股风格类型B')\
                    /len(stock_df_list[0])*100
    stock_left = stock_df_list[1].groupby('左侧标签').count()['jjdm'].to_frame('左侧类型分布')\
                 / len(stock_df_list[1]) * 100
    stock_df_list[1].loc[stock_df_list[1]['新股次新股偏好'] == '', '新股次新股偏好'] = '无'
    stock_new=stock_df_list[1].groupby('新股次新股偏好').count()['jjdm'].to_frame('新股偏好分布')\
              / len(stock_df_list[1]) * 100
    stock_fin2=(stock_df_list[1][['平均持有时间(出持仓前)_rank', '左侧概率(出重仓前,半年线)_rank','新股概率(出持仓前)_rank'
        ,'出重仓前平均收益率_rank',
       '出全仓前平均收益率_rank',]]).mean(axis=0)
    stock_fin=(stock_df_list[0][['PE_rank', 'PB_rank',
       'ROE_rank', '股息率_rank','平均仓位']]).mean(axis=0)
    stock_fin=pd.concat([stock_fin,stock_fin2],axis=0).to_frame('个股持仓特征')
    stock_fin.index = [x.replace('rank', '排名') for x in stock_fin.index]


    return industry_style,class_list,style_type_dis,style_incline_dis,\
           style_weight_dis,style_type_dis2,style_incline_dis2,style_weight_dis2,\
           stock_style_a,stock_style_b,stock_left,stock_new,stock_fin

def pool_industry(industry_style,class_list):

    if(len(industry_style.columns)>1):
        plot.plotly_jjpic_bar(industry_style, '行业风格分布')
    else:
        plot.plotly_pie(industry_style, '行业风格分布')

    for i in range(3):
        # if(len(class_list[i].columns)>2):
        #     plot.plotly_style_bar(class_list[i][['占持仓比例(时序均值)_x',
        #                                                   '占持仓比例(时序均值)_y']].fillna(0), "{}级行业持仓分布".format(i + 1))
        #     plot.plotly_style_bar(class_list[i][['占持仓比例(时序均值)排名_y',
        #                                                   '占持仓比例(时序均值)排名_y']].fillna(0), "{}级行业持仓分布".format(i + 1))
        # else:
        plot.plotly_jjpic_bar(class_list[i].fillna(0),"{}级行业持仓分布".format(i+1))

def pool_style(style_type_dis,style_incline_dis,
               style_weight_dis,style_type_dis2,style_incline_dis2,style_weight_dis2):

    if(len(style_type_dis.columns)>1):
        plot.plotly_jjpic_bar(style_type_dis, '风格类型分布')
        plot.plotly_jjpic_bar(style_incline_dis, '风格专注型分布')
        plot.plotly_jjpic_bar(style_weight_dis.iloc[0:2], '成长价值持仓占比')
        plot.plotly_jjpic_bar(style_weight_dis.iloc[2:], '成长价值持仓占比排名')

        plot.plotly_jjpic_bar(style_type_dis2, '规模风格类型分布')
        plot.plotly_jjpic_bar(style_incline_dis2, '专注型风格分布')
        plot.plotly_jjpic_bar(style_weight_dis2.iloc[0:3], '大中小盘持仓占比')
        plot.plotly_jjpic_bar(style_weight_dis2.iloc[3:], '大中小盘持仓占比排名')
    else:
        plot.plotly_pie(style_type_dis,'风格类型分布')
        plot.plotly_pie(style_incline_dis,'风格专注型分布')
        plot.plotly_pie(style_weight_dis.iloc[0:2],'成长价值持仓占比')
        plot.plotly_pie(style_weight_dis.iloc[2:],'成长价值持仓占比排名')


        plot.plotly_pie(style_type_dis2,'规模风格类型分布')
        plot.plotly_pie(style_incline_dis2,'专注型风格分布')
        plot.plotly_pie(style_weight_dis2.iloc[0:3],'大中小盘持仓占比')
        plot.plotly_pie(style_weight_dis2.iloc[3:],'大中小盘持仓占比排名')

def pool_other(stock_style_a,stock_style_b,stock_left,stock_new,stock_fin):

    if(len(stock_style_a.columns)>1):
        plot.plotly_jjpic_bar(stock_style_a,'个股风格类型分布A')
        plot.plotly_jjpic_bar(stock_style_b,'个股风格类型分布B')
        plot.plotly_jjpic_bar(stock_left ,'左侧类型分布')
        plot.plotly_jjpic_bar(stock_new,'新股偏好分布')
    else:
        plot.plotly_pie(stock_style_a,'个股风格类型分布A')
        plot.plotly_pie(stock_style_b,'个股风格类型分布B')
        plot.plotly_pie(stock_left ,'左侧类型分布')
        plot.plotly_pie(stock_new,'新股偏好分布')
    plot.plotly_jjpic_bar(stock_fin,'个股持仓特征')

def pool_picturing_engine(industry_style, class_list, style_type_dis, style_incline_dis, \
    style_weight_dis, style_type_dis2, style_incline_dis2, style_weight_dis2, \
    stock_style_a, stock_style_b, stock_left, stock_new, stock_fin):

    pool_industry(industry_style,class_list)
    pool_style(style_type_dis,style_incline_dis,
               style_weight_dis,style_type_dis2,style_incline_dis2,style_weight_dis2)
    pool_other(stock_style_a,stock_style_b,stock_left,stock_new,stock_fin)


def get_potient_pool(jjdm_con):

    value_df_list,industry_df_list,stock_df_list=get_jj_picture(jjdm_con,if_inverse=True)

    return value_df_list,industry_df_list,stock_df_list

def optimizer_allocation(value_df_list,industry_df_list, stock_df_list,pool,industry_style, class_list, style_type_dis, style_incline_dis, \
    style_weight_dis, style_type_dis2, style_incline_dis2, style_weight_dis2, \
    stock_style_a, stock_style_b, stock_left, stock_new, stock_fin):

    turnover_num=20
    style_order = ['专注', '博弈', '轮动', '配置']

    jjdm_con=util.list_sql_condition(pool['jjdm'].unique().tolist())
    value_df_list_pot, industry_df_list_pot, stock_df_list_pot=get_potient_pool(jjdm_con)

    potient_jj_list=industry_df_list_pot[0]['jjdm'].tolist()


    sql="select jjdm,zxppm1nyj from st_fund.t_st_gm_nxpblpm where jjdm not in ({0}) and tjnf>={1} ".format(jjdm_con,2022-1)
    sharpr=-1*hbdb.db2df(sql,db='funduser').set_index('jjdm').loc[potient_jj_list]['zxppm1nyj'].astype(float).values

    solver=pywraplp.Solver.CreateSolver('SCIP')
    x=[]
    for i in potient_jj_list:
        x.append(solver.IntVar(0,1,"x_{}".format(i)))


    input_industry_style_cons_ub=np.array([0.3,0.3,0.3,0.3])
    input_industry_style_cons_lb = np.array([0, 0, 0, 0])
    input_industry_style_cons_ub=input_industry_style_cons_ub*(turnover_num+len(pool))\
                                 -industry_style.loc[style_order]['num'].values/100*len(pool)
    input_industry_style_cons_lb=input_industry_style_cons_lb*(turnover_num+len(pool))\
                                 -industry_style.loc[style_order]['num'].values/100*len(pool)


    cons_dict=dict()
    #set constrains bound
    cons_dict['turnover_num']=solver.Constraint(turnover_num, turnover_num)
    for m in range(4):
        cons_dict['industry_style_{}'.format(style_order[m])] = solver.Constraint(input_industry_style_cons_lb[m], input_industry_style_cons_ub[m])
    industry_style_cofe=pd.get_dummies(industry_df_list_pot[0].set_index('jjdm')
                                       .loc[potient_jj_list]['一级行业类型'])[style_order].astype(float).values

    for i in range(len(x)):
        cons_dict['turnover_num'].SetCoefficient(x[i], 1)
        for m in range(4):
            cons_dict['industry_style_{}'.format(style_order[m])].SetCoefficient(x[i], industry_style_cofe[i,m])

    objective = solver.Objective()
    for i in range(len(x)):
        objective.SetCoefficient(x[i], sharpr[i])
    objective.SetMaximization()

    result_status = solver.Solve()
    print(result_status == pywraplp.Solver.OPTIMAL)
    print(solver.Objective().Value())

    adding_list=[]
    for i in range(len(x)):
        if(x[i].solution_value()==1):
            adding_list.append(str(x[i]).split('_')[-1])

    new_jjdm_list=pool['jjdm'].unique().tolist()+adding_list

    return  new_jjdm_list

def pool_picturing():

    pool = get_core_pool()

    #picture the original pool
    jjdm_con = util.list_sql_condition(pool['jjdm'].unique().tolist())
    value_df_list, industry_df_list, stock_df_list = get_jj_picture(jjdm_con)
    industry_style, class_list, style_type_dis, style_incline_dis, \
    style_weight_dis, style_type_dis2, style_incline_dis2, style_weight_dis2, \
    stock_style_a, stock_style_b, stock_left, stock_new, stock_fin\
        =features_calculation(value_df_list, industry_df_list, stock_df_list)

    pool_picturing_engine(industry_style, class_list, style_type_dis, style_incline_dis, \
    style_weight_dis, style_type_dis2, style_incline_dis2, style_weight_dis2, \
    stock_style_a, stock_style_b, stock_left, stock_new, stock_fin)

    # new_jjdm_list=optimizer_allocation(value_df_list, industry_df_list, stock_df_list,pool,industry_style, class_list, style_type_dis, style_incline_dis, \
    # style_weight_dis, style_type_dis2, style_incline_dis2, style_weight_dis2, \
    # stock_style_a, stock_style_b, stock_left, stock_new, stock_fin)

    #pic the new pool
    #new_jjdm_con=util.list_sql_condition(new_jjdm_list)
    new_jjdm_con="'001705','001410','001856','450009','166006'," \
                 "'001975','003095','005241','161606','005827','002708'," \
                 "'005968','005267','519133','002340','000577','163415'," \
                 "'000729','000756','000991','001208','001487','001532'," \
                 "'001718','001877','002258','002871','002943','004350'," \
                 "'004784','005161','005457','005669','005825','006257','007130','519702'"
    value_df_list, industry_df_list, stock_df_list = get_jj_picture(new_jjdm_con)
    industry_style_new, class_list_new, style_type_dis_new, style_incline_dis_new, \
    style_weight_dis_new, style_type_dis2_new, style_incline_dis2_new, style_weight_dis2_new, \
    stock_style_a_new, stock_style_b_new, stock_left_new, stock_new_new, stock_fin_new\
        =features_calculation(value_df_list, industry_df_list, stock_df_list)

    industry_style_new=pd.merge(industry_style,industry_style_new,how='outer',left_index=True,right_index=True)
    industry_style_new.columns=['旧池','新池']

    for i in range(3):
        class_list_new[i]=pd.merge(class_list[i],class_list_new[i],how='outer',
                                   left_index=True,right_index=True)
        class_list_new[i].columns=[x.replace('x','旧') for x in class_list_new[i].columns]
        class_list_new[i].columns = [x.replace('y', '新') for x in class_list_new[i].columns]
        class_list_new[i]=class_list_new[i][class_list_new[i].columns.sort_values()]


    style_type_dis_new=pd.merge(style_type_dis,style_type_dis_new,how='outer',
                                left_index=True,right_index=True).fillna(0)
    style_type_dis_new.columns=['旧池','新池']

    style_incline_dis_new=pd.merge(style_incline_dis,style_incline_dis_new,how='outer',
                                   left_index=True,right_index=True).fillna(0)
    style_incline_dis_new.columns=['旧池','新池']

    style_weight_dis_new=pd.merge(style_weight_dis,style_weight_dis_new,how='outer',
                                  left_index=True,right_index=True).fillna(0)
    style_weight_dis_new.columns=['旧池','新池']

    style_type_dis2_new=pd.merge(style_type_dis2,style_type_dis2_new,how='outer',
                                 left_index=True,right_index=True).fillna(0)
    style_type_dis2_new.columns=['旧池','新池']

    style_incline_dis2_new=pd.merge(style_incline_dis2,style_incline_dis2_new,
                                    how='outer',left_index=True,right_index=True).fillna(0)
    style_incline_dis2_new.columns=['旧池','新池']

    style_weight_dis2_new=pd.merge(style_weight_dis2,style_weight_dis2_new,
                                   how='outer',left_index=True,right_index=True).fillna(0)
    style_weight_dis2_new.columns=['旧池','新池']

    stock_style_a_new=pd.merge(stock_style_a,stock_style_a_new,
                               how='outer',left_index=True,right_index=True).fillna(0)
    stock_style_a_new.columns=['旧池','新池']

    stock_style_b_new=pd.merge(stock_style_b,stock_style_b_new,how='outer'
                               ,left_index=True,right_index=True).fillna(0)
    stock_style_b_new.columns=['旧池','新池']

    stock_left_new=pd.merge(stock_left,stock_left_new,how='outer'
                            ,left_index=True,right_index=True).fillna(0)
    stock_left_new.columns=['旧池','新池']

    stock_new_new=pd.merge(stock_new,stock_new_new,how='outer',
                           left_index=True,right_index=True).fillna(0)
    stock_new_new.columns=['旧池','新池']

    stock_fin_new=pd.merge(stock_fin,stock_fin_new,how='outer',
                           left_index=True,right_index=True).fillna(0)
    stock_fin_new.columns=['旧池','新池']


    pool_picturing_engine(industry_style_new, class_list_new, style_type_dis_new, style_incline_dis_new, \
    style_weight_dis_new, style_type_dis2_new, style_incline_dis2_new, style_weight_dis2_new, \
    stock_style_a_new, stock_style_b_new, stock_left_new, stock_new_new, stock_fin_new)



if __name__ == '__main__':


    # sql="select jjdm,trade_date,weight from st_hedge.r_st_sm_subjective_fund_holding"
    # df1=hbdb.db2df(sql,db='highuser')
    # df1['状态'] = '解析成功'
    # df1.loc[df1['weight'] == 99999, '状态'] = '解析失败'
    # df1.drop('weight',axis=1,inplace=True)
    # df1.drop_duplicates(['jjdm','trade_date'],inplace=True)
    # df2 = pd.read_excel(r"C:\Users\xuhuai.zhe\Downloads\股多-估值表-20220428.xlsx")
    #
    # df1['trade_date'] = df1['trade_date'].astype(str) + ","
    # df3 = df1.groupby('jjdm').sum()['trade_date'].to_frame('估值表日期').reset_index()
    # df3 = pd.merge(df3, df1.drop_duplicates(['jjdm', '状态']), how='left', on='jjdm')
    # df3 = df3[['jjdm', '状态', '估值表日期']]
    # df = pd.merge(df2, df3, how='left', left_on='基金代码', right_on='jjdm')
    # df.to_excel('对比结果.xlsx')

    pool_picturing()