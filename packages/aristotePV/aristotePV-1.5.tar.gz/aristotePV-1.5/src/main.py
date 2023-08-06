import pandas as pd,plotly.express as px
from aristoteDash import aristote

LieuEst = {
    'surface': 165,
    # productionCrete: 34,
    'inclinaison': 17,
    'orientation': -70,
    'rendement': 0.2,
    'latitude': 45.382238,
    'longitude': 5.997526,
};

LieuOuest = {
    'surface': 165,
    # 'productionCrete': 34,
    'inclinaison': 17,
    'orientation': 110,
    'rendement': 0.2,
    'latitude': 45.382238,
    'longitude': 5.997526,
};

facadeOuest = {
    'surface': 65,
    # 'productionCrete': 13,
    'inclinaison': 90,
    'orientation': 110,
    'rendement': 0.2,
    'latitude': 45.382238,
    'longitude': 5.997526,

};
pv_est         = aristote.PV_SLS(**LieuEst)
pv_oest        = aristote.PV_SLS(**LieuOuest)
pv_facade_oest = aristote.PV_SLS(**facadeOuest)

# (longitude,lattitude,surface,orientation,inclinaison,rendement):
pvth=pd.DataFrame(pd.date_range('2022-01-05','2022-01-10',freq='600s',tz='CET'),columns=['timestamp'])
pvth['pv theorique'+'_facade_ouest']=pvth['timestamp'].apply(pv_facade_oest.sls_PV_theorique)
pvth['pv theorique'+'_ouest']=pvth['timestamp'].apply(pv_oest.sls_PV_theorique)
pvth['pv theorique'+'_est']=pvth['timestamp'].apply(pv_est.sls_PV_theorique)
pvth=pvth.set_index('timestamp')
fig=px.scatter(pvth);
fig.update_traces(mode='lines+markers',marker_size=5)
fig.show()
