dataset3=dataset1.merge(dataset2, how='inner', on='id')



dataset3=dataset3[dataset3['join_time']>dataset3['start_time']]
dataset3=dataset3.loc[:,['leave_time','start_time','id','user_email','join_time']]
max_time=dataset3.groupby(['id','user_email'])['leave_time'].max().reset_index(name='max_time')
min_time=dataset3.groupby(['id','user_email'])['join_time'].min().reset_index(name='min_time')
order_m=pd.merge(min_time,max_time, how='outer')
order_m['minutos']=order_m['max_time']-order_m['min_time']
order_m['minutos']=order_m['minutos'].astype('timedelta64[m]').astype(int)
order_m['SNFrom']=1
order_m['SNTo']=organizar_minutos_estudiantes['minutos']
order_m=order_m.loc[:,['id','user_email','SNFrom','SNTo']]
proint(order_m)

new_df = (order_m.set_index(['id','user_email'])[['SNFrom','SNTo']]
      .apply(lambda x: pd.Series(list(range(x.SNFrom, x.SNTo+1))),1)
      .stack()
      .reset_index(level=[0,1])
      .rename(columns={0:'SN'}))
new_df
