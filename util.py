from alternative import Alternative
import dash_html_components as html

absolute = [("Identifizierung identischer Artikel", "timeSameComponent"),("Klassifizierung ähnlicher Artikel", "timeSimComponent"), 
("Identifizierung neuer Artikel", "timeNewComponent"), ("Gesamte benötigte Zeit zur Identifizierung und Klassifizierung von Prozessen","timeProcess"),
("Gesamte benötigte Zeit zur Identifizierung und Klassifizierung von Ressourcen", "timeResource")]

relative = [('totalSearchTimeComponents','Identifizierung und Klassifizierung der Artikel'),
                                ( 'shareSameComponent','Prozentualer Anteil bei Identifizierung identischer Artikel'),
                                ('shareSimComponent',  'Prozentualer Anteil bei Klassifizierung ähnlicher Artikel'),
                                ('shareNewComponent', 'Prozentualer Anteil bei Identifizierung neuer Artikel'),
                                ('totalSearchTimeProcesses',  'Identifizierung und Klassifizierung der Prozessen'),
                                ('totalSearchTimeResources',  'Identifizierung und Klasssifizierung der Resourcen')]
                                

cond = [("Durschnittliche Anzahl an unbekannten Artikeln","mean_amount_of_elem_comp"),
        ("Durchschnittliche Durchlaufzeit der Produktfamilie (Min)","t_DLZ"),
        ("Durchschnittliche Anzahl an eingeführten Produktfamilien pro Jahr","P_x"),
        ("Durchschnittliche Einnahmen pro Produktfamilie","npvRevProProduct"),
        ("zeitgleich nutzbare Produktionslinien mit DAS", "l_Mx")]

simProd = [
    ("Investitionssumme","I_x"),("Anzahl manueller Eingaben pro Bauteil (z.B. Produktmerkmale)","n_KäA"),("Instandhaltungskostensatz","c_main")
    ]

headerStyle={
            'backgroundColor': 'white',
            'font-size': '15px'}

style_cell={
        'font-family':'Open Sans',
        'whiteSpace': 'normal',
        'height': 'auto',
        'font-size': '15px'
    }

# Tabelle für das Anzeigen einzelner Kapitalwerte der Unterstützungslösungen
class small_table:
    def __init__(self,KW,investition, time_after, time_before,name=None):
        n_prodFam = len(time_after)
        self.KW = KW
        
        self.name=name
        self.investition = investition
        if isinstance(KW,str):
            self.table =  html.P(KW)
        else:
            children = [html.Tr(children=[
                            html.Th(colSpan=4, style={'text-align': 'left'},
                                    children=[name])])] if name!=None else []
            children +=[
                html.Tr(
                        children=[
                            html.Td(children=["Kapitalwert: "]),
                            html.Td(children=[KW],style={'color':'red' if KW<0 else 'black'}),
                            html.Td(children=["Investitionssumme: "]),
                            html.Td(children=[investition])
                        ]
                    ),

                html.Tr(
                    children=[
                        html.Td(children=["Suchzeit vorher: "]),
                        html.Td(children=[sum(time_before)]),
                        html.Td(children=["Suchzeit nachher: "]),
                        html.Td(children=[sum(time_after)])
                    ]
                ),
            ]+[
                html.Tr(
                    [
                        html.Td(children=["Produktfamilie "+str(n+1)], style={"text-align":"right"}),
                        html.Td(children=[time_before[n]]),
                        html.Td(children=["Produktfamilie "+str(n+1)], style={"text-align":"right"}),
                        html.Td(children=[time_after[n]])
                    ]
                ) for n in range(0,n_prodFam)
            ]
            self.table = html.Table(style={"width":"100%"},children=children)


# Tabelle für das Anzeigen Kapitalwerte der Gesamtlösungen
class html_table:
    def __init__(self, name, money, investition, time, time_before, IiA, KäA, matLevel, n_prodFam, time_x, time_before_x):
        support_functions = []
        if IiA == 1:
            support_functions.append("IiA")
        if KäA == 1:
            support_functions.append("KäA")
        support_functions = str(support_functions).strip("[]'").replace("'", "")
        
        self.table = html.Table(style={"width": "100%"},
                                children=[
                                    html.Tr(
                                        children=[
                                            html.Th(colSpan=4, style={'text-align': 'left'},
                                                    children=[name])]
                                    ),

                                    html.Tr(
                                        children=[
                                            html.Td(children=["Kapitalwert: "]),
                                            html.Td(children=[money],style={'color':'red' if money<0 else 'black'}),
                                            html.Td(children=["Investitionssumme: "]),
                                            html.Td(children=[investition])
                                        ]
                                    ),

                                    html.Tr(
                                        children=[
                                            html.Td(children=["Suchzeit vorher: "]),
                                            html.Td(children=[time_before]),
                                            html.Td(children=["Suchzeit nachher: "]),
                                            html.Td(children=[time])
                                        ]
                                    ),
                                ]+[
                                    html.Tr(
                                        [
                                            html.Td(children=["Produktfamilie "+str(n+1)], style={"text-align":"right"}),
                                            html.Td(children=[time_before_x[n]]),
                                            html.Td(children=["Produktfamilie "+str(n+1)], style={"text-align":"right"}),
                                            html.Td(children=[time_x[n]])
                                        ]
                                    ) for n in range(0,n_prodFam)
                                ]+[
                                    # header support function outputs
                                    html.Tr(
                                        children=[
                                            html.Td(children=["Unterstützungen: "]),
                                            html.Td(support_functions),
                                            html.Td(children=["Reifegradstufe: "]),
                                            html.Td(matLevel)
                                        ]
                                    ),

                                    html.Br()
                                ])

# Zeit von einzelnen Unterstützungslösungen berechnen
def calculate_time(matLevel,cumTimeSameComponent,cumTimeSimComponent,cumTimeNewComponent,IiA,KäA,cumtimeProcess,cumtimeResource,n_KäA,mean_amount_of_elem_comp):
    n_prodFam = len(cumtimeProcess)
    all_zeros = [0 for x in range(0, n_prodFam)]
    sameComponent = all_zeros if IiA == 1 else cumTimeSameComponent
    simComponent = [(0.0006*35+15*0.0006)*n*m if KäA == 1 else t for n,m,t in zip(n_KäA,mean_amount_of_elem_comp,cumTimeSimComponent)]
    newComponent = all_zeros if IiA == 1 and KäA == 1 else cumTimeNewComponent    
    Process = all_zeros if matLevel >= 2 else cumtimeProcess
    Resource = all_zeros if matLevel == 3 else cumtimeResource
    time = [newComponent[x] + simComponent[x] + sameComponent[x] + Process[x] + Resource[x] for x in range(0, n_prodFam)]
    return time

# Kapitalwerte von einzelnen Unterstützungslösungen berechnen
def calculate_npv(I_total,c_main,k_personal,r,T,t_unsupported,t_supported,r_acc,l_Mx, t_DLZ,P_x):         
    C_main = c_main * I_total # K_IHJ=k_IH*I_0
    k_P=k_personal / 60 # convert to minutes
    x_specific = sum([(k_P*(t_vorher-t_nachher)+e_Var*l_M*(t_vorher-t_nachher)/t_DLZ)*P-k_P*t_nachher*P for t_vorher, t_nachher, e_Var, l_M,t_DLZ,P in zip(t_unsupported,t_supported,r_acc,l_Mx, t_DLZ,P_x)]) 
    npv = - I_total
    for t in range(1, int(T) + 1): 
        npv += (x_specific - C_main)/ ((1 + r) ** t)
    return npv

# Investitionssumme von einzelnen Unterstützungslösungen berechnen
def calculate_investment(alternative, ist_situation, I_l2, I_l3, I_same, I_sim):
    # find out if extra investment is to be made:
    invest_IiA = alternative.IiA - ist_situation.IiA
    invest_KäA = alternative.KäA - ist_situation.KäA
    # find out investment needed for the increase of maturity level:
    mat_increase = 0
    if alternative.matLevel > ist_situation.matLevel:
        if alternative.matLevel == 3 and ist_situation.matLevel == 2:
            mat_increase += I_l3
        if alternative.matLevel == 2 and ist_situation.matLevel == 1:
            mat_increase += I_l2
        if alternative.matLevel == 3 and ist_situation.matLevel == 1:
            mat_increase += I_l2 + I_l3
    # calculate amount of investment needed:
    I_total = invest_IiA * I_same + invest_KäA * I_sim + mat_increase
    return I_total


# Kapitalwerte von einzelnen Unterstützungslösungen berechnen
def calculate_separate_npvs(parameters):
    ist_situation = parameters.get('ist_situation')
    investition = parameters.get('investition')
    allgemeine_parameter = parameters.get('allgemeine_parameter')
    product_family_parameter = parameters.get('product_family_parameter')
    product_family_time = parameters.get('product_family_time')
    matlevel = ist_situation.get("matLevel")
    IiA = ist_situation.get("IiA")
    KäA = ist_situation.get("KäA")
    cumtimeProcess = product_family_time.get('cumtimeProcess')
    cumtimeResource = product_family_time.get('cumtimeResource')
    cumTimeSameComponent = product_family_time.get('cumTimeSameComponent')
    cumTimeSimComponent = product_family_time.get('cumTimeSimComponent')
    cumTimeNewComponent = product_family_time.get('cumTimeNewComponent')
    AS = allgemeine_parameter.get("Arbeitsstunden pro Woche")
    K_PGrund = allgemeine_parameter.get("Monatliches Grundgehalt in der Arbeitsvorbereitung")
    r = allgemeine_parameter.get("Zinssatz")
    T=allgemeine_parameter.get("Betrachtungszeitraum")
    I_l2_df = investition.get('I_l2')
    I_l3_df = investition.get('I_l3')
    I_identisch_df = investition.get('I_identisch')
    I_ähnlich_df = investition.get('I_ähnlich')
    k_personal = (K_PGrund * 12 * 7 * (1 + 0.726)) / (365 * AS)

    

    n_KäA_list = list(I_ähnlich_df['n_KäA'])
    I_sim_list  = list(I_ähnlich_df['I_x'])
    c_main_list = list(I_ähnlich_df['c_main'])
    I_same_list = list(I_identisch_df['I_x'])
    c_main_list_3 = list(I_identisch_df['c_main'])
    mean_amount_of_elem_comp = list(product_family_parameter['mean_amount_of_elem_comp'])
    r_acc = list(product_family_parameter['npvRevProProduct'])
    l_Mx = list(product_family_parameter['l_Mx'])
    t_DLZ = list(product_family_parameter['t_DLZ'])
    P_x = list(product_family_parameter['P_x'])

    # für Reifegraderhöhungen 
    I_sim = min(I_sim_list)
    I_identisch = min(I_same_list)
    n_KäA = [n_KäA_list[I_sim_list.index(I_sim)] for x in range(0, len(cumtimeProcess))]
    t_unsupported = calculate_time(matlevel,cumTimeSameComponent,cumTimeSimComponent,cumTimeNewComponent,IiA,KäA,cumtimeProcess,cumtimeResource,n_KäA,mean_amount_of_elem_comp)
    
    KW_l2_tables=[]
    KW_l3_tables=[]
    I_l2_best = 0
    I_l3_best = 0

    #--------Erhöhung auf Reifegrad 1--------
    if matlevel == 1:
        i = 1
        KW_l2_max = -10**6
        for c_main, I_l2 in zip(list(I_l2_df['c_main']), list(I_l2_df['I_l2'])):
            t_supported = calculate_time(2,cumTimeSameComponent,cumTimeSimComponent,cumTimeNewComponent,IiA,KäA,cumtimeProcess,cumtimeResource,n_KäA,mean_amount_of_elem_comp)
            I_total = I_l2
            KW_l2 = calculate_npv(I_total,c_main,k_personal,r,T,t_unsupported,t_supported,r_acc,l_Mx, t_DLZ,P_x)
            if KW_l2 > KW_l2_max:
                KW_l2_max = KW_l2
                I_l2_best = I_total
            KW_l2_tables.append(small_table(KW_l2,I_total,t_supported,t_unsupported,name=f"Investition {i}"))
            i+=1
        KW_l2_tables.sort(key=lambda x: x.KW, reverse=True)
        KW_l3_max = -10**6
        i=1
        for c_main, I_l3 in zip(list(I_l3_df['c_main']), list(I_l3_df['I_l3'])):
            t_supported = calculate_time(3,cumTimeSameComponent,cumTimeSimComponent,cumTimeNewComponent,IiA,KäA,cumtimeProcess,cumtimeResource,n_KäA,mean_amount_of_elem_comp)
            I_total = I_l2_best + I_l3
            KW_l3 = calculate_npv(I_total,c_main,k_personal,r,T,t_unsupported,t_supported,r_acc,l_Mx, t_DLZ,P_x)
            if KW_l3 > KW_l3_max:
                KW_l3_max = KW_l3
                I_l3_best = I_l3
            KW_l3_tables.append(small_table(KW_l3,I_total,t_supported,t_unsupported,name=f"Investition {i}"))
            i+=1
        KW_l3_table = small_table(KW_l3_max,I_l3_best,t_supported,t_unsupported)
        KW_l3_tables.sort(key=lambda x: x.KW, reverse=True)

    #--------Erhöhung auf Reifegrad 2--------
    elif matlevel == 2: 
        KW_l2 = "bereits umgesetzt"
        KW_l3_max = -10**6
        i=1
        for c_main, I_l3 in zip(list(I_l3_df['c_main']), list(I_l3_df['I_l3'])):
            I_total = I_l3
            t_supported = calculate_time(3,cumTimeSameComponent,cumTimeSimComponent,cumTimeNewComponent,IiA,KäA,cumtimeProcess,cumtimeResource,n_KäA,mean_amount_of_elem_comp)
            KW_l3 = calculate_npv(I_total,c_main,k_personal,r,T,t_unsupported,t_supported,r_acc,l_Mx, t_DLZ,P_x)
            if KW_l3 > KW_l3_max:
                KW_l3_max = KW_l3
                I_l3_best = I_l3
            KW_l3_tables.append(small_table(KW_l3,I_total,t_supported,t_unsupported,name=f"Investition {i}"))
            i+=1
        KW_l3_tables.sort(key=lambda x: x.KW, reverse=True)
        KW_l2_tables.append(html.P(KW_l2))

    #--------Erhöhung auf Reifegrad 3--------
    else:
        KW_l2 = "bereits umgesetzt"
        KW_l3 = "bereits umgesetzt"
        KW_l2_tables.append(html.P(KW_l2))
        KW_l3_tables.append(html.P(KW_l3))

    I_l2 = I_l2_best
    I_l3= I_l3_best

    #--------Identifizierung identischer Artikel--------
    KW_IiA_tables = []
    if IiA == 1:
        KW_IiA = "bereits umgesetzt"
        KW_IiA_tables.append(small_table(KW_IiA,I_total,t_supported,t_unsupported).table)
    else:
        i = 1
        for I_identisch, c_main in zip(I_same_list,c_main_list_3):
            I_total=calculate_investment(Alternative(1, KäA, matlevel),Alternative(IiA, KäA, matlevel),I_l2,I_l3,I_identisch,I_sim)
            t_supported = calculate_time(matlevel,cumTimeSameComponent,cumTimeSimComponent,cumTimeNewComponent,1,KäA,cumtimeProcess,cumtimeResource,n_KäA,mean_amount_of_elem_comp)
            KW_IiA=calculate_npv(I_total,c_main,k_personal,r,T,t_unsupported,t_supported,r_acc,l_Mx, t_DLZ,P_x)
            KW_IiA_tables.append(small_table(KW_IiA,I_total,t_supported,t_unsupported,name=f"Methode zur Identifizierung {i}"))
            i+=1
        KW_IiA_tables.sort(key=lambda x: x.KW, reverse=True)

    #--------Klassifizierung ähnlicher Artikel--------
    KW_KäA_tables = []
    if KäA == 1:
        KW_KäA = "bereits umgesetzt"
        KW_KäA_tables.append(small_table(KW_KäA,I_total,t_supported,t_unsupported).table)
    else:
        i=1
        for n_KäA, I_sim, c_main in zip(n_KäA_list,I_sim_list, c_main_list):
            n_KäA = [n_KäA for x in range(0, len(cumtimeProcess))]
            I_total=calculate_investment(Alternative(IiA, 1, matlevel),Alternative(IiA, KäA, matlevel),I_l2,I_l3,I_identisch,I_sim)
            t_supported = calculate_time(matlevel,cumTimeSameComponent,cumTimeSimComponent,cumTimeNewComponent,IiA,1,cumtimeProcess,cumtimeResource,n_KäA,mean_amount_of_elem_comp)
            KW_KäA=calculate_npv(I_total,c_main,k_personal,r,T,t_unsupported,t_supported,r_acc,l_Mx, t_DLZ,P_x)
            KW_KäA_tables.append(small_table(KW_KäA,I_total,t_supported,t_unsupported,name=f"Methode zur Klassifizierung {i}"))
            i+=1
        KW_KäA_tables.sort(key=lambda x: x.KW, reverse=True)
        
    return KW_l2_tables,KW_l3_tables,KW_IiA_tables,KW_KäA_tables




    
    


