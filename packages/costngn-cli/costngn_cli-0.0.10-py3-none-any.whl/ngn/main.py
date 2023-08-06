from zlib import Z_NO_COMPRESSION
import pkg_resources  # part of setuptools
import typer
from ngn.config.config import *
from ngn.aws.data import *
from ngn.do.data import *
from ngn.het.data import *
import pandas as pd
from termcolor import colored
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
from IPython.display import display
#from setup import version

app = typer.Typer(help='* costngn-cli gives you access to cloud services data and costs')


def choose_acc(company):
    print("Reading configuration file") #config.toml
        
    #config_file=os.path.join(Path.home(), 'costngn','config.toml')    
    prof=toml.load(config_file)
    #Choose the first account found for this provider    
    have_acc=False
    for pro_nick in prof:
        #pp.pprint(prof[pro_nick]['provider'])
        if prof[pro_nick]['provider'].lower()==company:
            have_acc=True
            nick=pro_nick #acc=prof[nick] #pp.pprint(acc)                       
            print(company.upper(),'account found with nickname',nick)
            break
    if not have_acc:
        print(company.upper(),'account not found in profile')
        quit()
    return nick



# Graphic, non Terminal Table    
def rep_gtable(nick, rep, company):    
    typer.echo('Graphical table')
    pd.set_option('display.max_columns', None);pd.set_option('display.max_colwidth', None)
    columns=[]
    rows=['Id','Name','Company','Region','Status','Create Day','IPV4 Priv Add','IPV4 Pub Add',
        'Type','CPUs','Memory','Image','VPC','Avail.Zone','Hourly Price','Monthly Price','Cost (estim)']
    df = pd.DataFrame(columns=columns, index=rows)
    for i,inst in enumerate(rep['instances']):        
        df['Instance '+str(i+1)]=[inst['id'],inst['name'],inst['provider'],inst['region'],inst['status'],
        #df[inst['id'],inst['name'],inst['provider'],inst['region'],inst['status'],
            inst['birthday'],inst['ipv4priv'],inst['ipv4pub'],inst['type'],inst['cpus'],inst['memory'],
            inst['image'],inst['vpc_id'],inst['avzone'],inst['ihprice'],inst['imprice'],inst['est_cost']   
            ]

    fig, ax = plt.subplots(figsize=(10,6))
    table = ax.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index ,loc='right')
    fig.patch.set_visible(False)
    #plt.rcParams["figure.autolayout"] = True
    

    ax.axis('off')
    ax.axis('tight')
    #table = ax.table(cellText=df.values, colLabels=df.columns, loc='center')
    fig.tight_layout()
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    #plt.ion()
    #plt.ioff()
    plt.show(block=False) 
    table.auto_set_column_width(col=list(range(len(df.columns)))) 
    # Choose the Slider color

    slider_color = 'Grey'
    
    # Set the axis and slider position in the plot
    axis_position = plt.axes([0.2, 0.1, 0.65, 0.03],
                            facecolor = slider_color)

    #global slider_position
    slider_position = Slider(axis_position, 'Pos', 0.1, 90.0)

    axis_position = plt.axes([0.2, 0.1, 0.65, 0.03],
                            facecolor = slider_color)
    plt.show()
    #display(df)
    #exit=input('press enter to exit')
    # update() function to change the graph when the
# slider is in use
"""
def update(val):
    #pos = slider_position.val
    print('scroll bar moved!')
    #Axis.axis([pos, pos+10, -1, 1])
    #Plot.canvas.draw_idle()

    # update function called using on_changed() function
    slider_position.on_changed(update)
"""





def rep_table(nick, rep, company): 
    #typer.echo('Show Instances Info')
    #pp.pprint(rep)
    #typer.run(conf_show(),config_file)
    print('Found ',len(rep),'instances:') 
    pd.set_option('display.max_rows', None); pd.set_option('display.max_columns', None)
    pd.set_option('display.width', os.get_terminal_size().columns); pd.set_option('display.max_colwidth', None)
    pd.set_option('display.colheader_justify', 'center')
    
    columns=[]
    rows=['Id','Name','Company','Region','Status','Create Day','IPV4 Priv Add','IPV4 Pub Add',
        'Type','CPUs','Memory','Image','VPC','Avail.Zone','Hourly Price','Monthly Price','Cost (estim)']
    
    for i,row in enumerate(rows):
        row=colored(row,'green')
        rows[i]=row
    

    #for i,inst in enumerate(rep['instances']):
    #    columns.append(colored('Inst '+str(i+1),'yellow'))

    df = pd.DataFrame(columns=columns, index=rows)
    #df= pd.DataFrame(index=rows)    

   
    for i,inst in enumerate(rep['instances']):
        
        df['Instance '+str(i+1)]=[inst['id'],inst['name'],inst['provider'],inst['region'],inst['status'],
        #df[inst['id'],inst['name'],inst['provider'],inst['region'],inst['status'],
            inst['birthday'],inst['ipv4priv'],inst['ipv4pub'],inst['type'],inst['cpus'],inst['memory'],
            inst['image'],inst['vpc_id'],inst['avzone'],inst['ihprice'],inst['imprice'],inst['est_cost']   
            ]
    """ 
    for i,inst in enumerate(rep['instances']):
        #pd.set_option('display.colheader_justify', 'right')
        df[colored('Instance '+str(i+1),'yellow')]=[inst['id'],inst['name'],inst['provider'],inst['region'],inst['status'],
        df[inst['id'],inst['name'],inst['provider'],inst['region'],inst['status'],
            inst['birthday'],inst['ipv4priv'],inst['ipv4pub'],inst['type'],inst['cpus'],inst['memory'],
            inst['image'],inst['vpc_id'],inst['avzone'],inst['ihprice'],inst['imprice'],inst['est_cost']   
            ]
    """

    #df = pd.DataFrame(table, columns = columns, index=rows)
    #df = colored(df,'green')
    #result = df.to_string(header = False) #does not work with max width
    #result =df.to_markdown() #does not work with max width    
    print(df)
    #print(df,header=False)
    #df.style #it is not for terminal
    
    print('')
    #df.style.applymap('green')
    #
    #display(df)
    

    ### Generate output json file
    if os.path.exists(result_path): print(f'Folder {result_path} already exists')
    else: 
        print('Making new folder',result_path)
        os.makedirs(result_path)

    report_file=company.upper()+'-'+nick.upper()+ date.today().strftime(" %Y-%m-%d.json") 
    report_file=os.path.join(result_path,report_file)
    rep_json = json.dumps(rep,indent=2)
    with open(report_file, 'w') as outfile:
        outfile.write(rep_json)
    print(f'Saved to {report_file}')


def nick_ok(company,nick):
    print("Reading configuration file") #config.toml
    prof=toml.load(config_file)
    #Check if an account with that nickname exists and match the company    
    if nick in prof:
        print(f"Nickname {nick}",end=' ')
        if prof[nick]['provider']==company:
            print(f'is correct for an account on {company.upper()}')
            return
        else:
            print('does not match an account in',company.upper(),', it points to an account in', prof[nick]['provider'].upper())
            quit()
    else:
        print(f"There isn't any account with nickname {nick} in {config_file}")
        quit()

    
@app.callback(invoke_without_command=True)
def foo():
    version = pkg_resources.require("costngn-cli")[0].version
    typer.echo(f'Welcome to costngn-cli {version} (alpha)')
    #typer.echo(f"{__app_name__} v{__version__}")
    global config_file
    config_file=os.path.join(Path.home(), 'costngn','.config','config.toml')
    global result_path
    result_path=os.path.join(Path.home(), 'costngn','results')
    #typer.echo(f"{lat}, {long}, {method}")

@app.command()
def config():
    """
    Input and store your account access information
    """
    #global config_file
    #config_file=os.path.join(Path.home(), 'costngn','config.toml')
    typer.echo('Enter below your account access information:')
    typer.echo('It will be saved into config file')
    #typer.run(conf_main,config_file)
    conf_main(config_file)

@app.command()
def list_profiles():
    """
    Show your stored account/s access information
    """
    typer.echo('Show config file content:')
    #typer.run(conf_show(),config_file)
    conf_show(config_file)


@app.command()
def aws(nick:str,   
    graph: bool = typer.Option(False,
    '--graph', '-g', help="Show table in a graphic, non-terminal window"),
    ):

    """
    Gets AWS instances data - 'costngn-cli aws --help' for options
    """
    #global config_file
    #config_file=os.path.join(Path.home(), 'costngn','config.toml')
    company='aws'
    #nick=choose_acc(company)
    typer.echo(f'Go to {company.upper()} data:')
    nick_ok(company, nick)
    #typer.run(aws_main)
    cost=False
    rep=aws_main(company,nick,config_file,cost)
    if graph: rep_gtable(nick, rep, company)
    else: rep_table(nick, rep, company)


@app.command()
def do(nick:str, 
    graph: bool = typer.Option(False,     '--graph', '-g',
    help="Show table in a graphic, non-terminal window"),
    ):

    """
    Gets Digital Ocean instances data \n 'costngn-cli do --help' for options
    """
    company='do'
    #nick=choose_acc(company)
    nick_ok(company, nick)
    typer.echo(f'Go to {company.upper()} data:')
    rep= do_main(company, nick,config_file,result_path)
    if graph: rep_gtable(nick, rep, company)
    else: rep_table(nick, rep, company)

@app.command()
def het(nick:str, 
    graph: bool = typer.Option(False,     '--graph', '-g',
    help="Show table in a graphic, non-terminal window"),
    ):

    """
    Gets Hetzner instances data \n 'costngn-cli het --help' for options
    """
    company='het'
    #nick=choose_acc(company)
    nick_ok(company, nick)
    typer.echo(f'Go to {company.upper()} data:')
    rep= het_main(company, nick,config_file,result_path)
    if graph: rep_gtable(nick, rep, company)
    else: rep_table(nick, rep, company)


@app.command()
def remove(nick:str):
    """
    Remove given profile_id account from config file
    """
    #nick_ok(company, nick)
    #typer.echo(f'Go to {company.upper()} data:')
    conf_del(nick,config_file)


@app.command()
def hello(name:str,nick:str): 
    """
    adding you name after 'hello' you'll be greeted
    """
    typer.echo(f"Hello {name} {nick} from costngn-cli !")


if __name__ == "__main__":
    app()
    



