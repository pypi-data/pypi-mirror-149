#working with dorianUtilsModulaire==3_9
import os
from aristoteDash import aristoteDash
import dash, dash_core_components as dcc, dash_html_components as html, dash_bootstrap_components as dbc
from dorianUtils.dccExtendedD import DccExtended
from multiprocessing import Process, Queue, current_process,Pool
from dash.dependencies import Input, Output, State
# ==============================================================================
#                       INSTANCIATIONS
# ==============================================================================
home=os.getenv('HOME')
if 'sylfen' in home:baseFolder = '/home/sylfen/data/'
else:baseFolder = '/home/dorian/data/sylfenData/'

dccE = DccExtended()
# ==============================================================================
#                       START APP
# ==============================================================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],title='aristote')
powerTab   = aristoteDash.PowerTab(app,)
energyTab  = aristoteDash.EnergyTab(app,)
titleHTML  = html.H1()
tabsLayout = dccE.createTabs([powerTab,energyTab])

mdFile = powerTab.cfg.confFolder + 'aristote.md'
logModal = dccE.buildModalLog('Aristote V1.4(beta)',mdFile)

app.layout = html.Div([html.Div(logModal),html.Div(tabsLayout)])

@app.callback(
    Output("log_modal", "is_open"),
    [Input("btn_log", "n_clicks"), Input("close", "n_clicks")],
    [State("log_modal", "is_open")],
)
def showLog(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

app.run_server(port=50000,host='0.0.0.0',debug=False,use_reloader=False)
