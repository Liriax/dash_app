from alternative import Alternative
import dash_html_components as html
from calculator import convert_decimal_time
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
        ("Durchschnittliche Anzahl an eingeführten Produktfamilien pro Jahr","P_x"),
        ("Durchschnittliche Einnahmen pro Produktfamilie","npvRevProProduct"),
        ("zeitgleich nutzbare Produktionslinien mit DAS", "l_Mx"),
        ("Durchschnittliche Durchlaufzeit der Produktfamilie (Min,Sek)","t_DLZ")]

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
    def __init__(self,KW,investition, time_after, time_before,IiA, KäA, RG, name=None):
        n_prodFam = len(time_after)
        self.KW = KW
        support_functions = []
        if IiA == 1:
            support_functions.append("IiA")
        if KäA == 1:
            support_functions.append("KäA")
        if IiA == 1 and KäA == 1:
            support_functions.append("InA")
        support_functions = str(support_functions).strip("[]'").replace("'", "")
        self.support_functions=support_functions
        # self.name=f"Unterstützungslösung {name}" if not isinstance(name, list) else f"Unterstützungslösung {name[0]} und {name[1]}"
        self.number=name
        self.RG=RG
        self.investition = investition
        if isinstance(KW,str):
            self.table =  html.P(KW)
        else:
            # children = [html.Tr(children=[
            #                 html.Th(colSpan=4, style={'text-align': 'left'},
            #                         children=[self.name])])] if name!=None else []
            children = []
            children +=[
                html.Tr(
                        children=[
                            html.Td(children=["Kapitalwert (€): "]),
                            html.Td(children=[round(KW,2)],style={'color':'red' if KW<0 else 'black'}),
                            html.Td(children=["Investitionssumme (€): "]),
                            html.Td(children=[investition])
                        ]
                    ),

                html.Tr(
                    children=[
                        html.Td(children=["Suchzeit vorher (Min,Sek): "]),
                        html.Td(children=[convert_decimal_time(sum(time_before))]),
                        html.Td(children=["Suchzeit nachher (Min,Sek): "]),
                        html.Td(children=[convert_decimal_time(sum(time_after))])
                    ]
                ),
            ]+[
                html.Tr(
                    [
                        html.Td(children=["Produktfamilie "+str(n+1)], style={"text-align":"right"}),
                        html.Td(children=[convert_decimal_time(time_before[n])]),
                        html.Td(children=["Produktfamilie "+str(n+1)], style={"text-align":"right"}),
                        html.Td(children=[convert_decimal_time(time_after[n])])
                    ]
                ) for n in range(0,n_prodFam)
            ]+[
                html.Tr(
                    [
                        html.Td(children=["Unterstützungen: "]),
                        html.Td(children=[support_functions]),
                        html.Td(children=["Reifegrad: "]),
                        html.Td(children=[RG])
                    ]
                )
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
        if IiA == 1 and KäA == 1:
            support_functions.append("InA")
        self.I=investition
        support_functions = str(support_functions).strip("[]'").replace("'", "")
        self.support_functions = support_functions
        self.table = html.Table(style={"width": "100%"},
                                children=[
                                    html.Tr(
                                        children=[
                                            html.Th(colSpan=4, style={'text-align': 'left'},
                                                    children=[name])]
                                    ),

                                    html.Tr(
                                        children=[
                                            html.Td(children=["Kapitalwert (€): "]),
                                            html.Td(children=[money],style={'color':'red' if money<0 else 'black'}),
                                            html.Td(children=["Investitionssumme (€): "]),
                                            html.Td(children=[investition])
                                        ]
                                    ),

                                    html.Tr(
                                        children=[
                                            html.Td(children=["Suchzeit vorher (Min,Sek): "]),
                                            html.Td(children=[convert_decimal_time(time_before)]),
                                            html.Td(children=["Suchzeit nachher (Min,Sek): "]),
                                            html.Td(children=[convert_decimal_time(time)])
                                        ]
                                    ),
                                ]+[
                                    html.Tr(
                                        [
                                            html.Td(children=["Produktfamilie "+str(n+1)], style={"text-align":"right"}),
                                            html.Td(children=[convert_decimal_time(time_before_x[n])]),
                                            html.Td(children=["Produktfamilie "+str(n+1)], style={"text-align":"right"}),
                                            html.Td(children=[convert_decimal_time(time_x[n])])
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
    # convert from time to decimal
    n_prodFam = len(cumtimeProcess)
    cumTimeSameComponent=[convert_decimal_time(x,False) for x in cumTimeSameComponent]
    mean_amount_of_elem_comp=[convert_decimal_time(x,False) for x in mean_amount_of_elem_comp]
    cumTimeSimComponent = [convert_decimal_time(x,False) for x in cumTimeSimComponent]
    cumTimeNewComponent= [convert_decimal_time(x,False) for x in cumTimeNewComponent]
    cumtimeProcess= [convert_decimal_time(x,False) for x in cumtimeProcess]
    cumtimeResource= [convert_decimal_time(x,False) for x in cumtimeResource]
    # calculate
    all_zeros = [0 for x in range(0, n_prodFam)]
    sameComponent = all_zeros if IiA == 1 else cumTimeSameComponent
    if KäA == 1:
        simComponent = [(0.0006*35+15*0.0006)*n*m for n,m in zip(n_KäA,mean_amount_of_elem_comp)]
    else:
        simComponent = cumTimeSimComponent
    newComponent = all_zeros if IiA == 1 and KäA == 1 else cumTimeNewComponent

    Process = all_zeros if matLevel >= 2 else cumtimeProcess
    Resource = all_zeros if matLevel == 3 else cumtimeResource
    try:
        t_supported = [newComponent[x] + simComponent[x] + sameComponent[x] + Process[x] + Resource[x] for x in range(0, n_prodFam)]
    except:
        print("error")
       
    return t_supported

# Kapitalwerte von einzelnen Unterstützungslösungen berechnen
def calculate_npv(I_total,c_main,k_personal,r,T,t_unsupported,t_supported,r_acc,l_Mx, t_DLZ,P_x):         
    C_main = c_main / 100 * I_total # K_IHJ=k_IH*I_0
    k_P=k_personal / 60 # convert to minutes
    t_DLZ=[convert_decimal_time(x,False) for x in t_DLZ]
    x_specific = sum([(k_P*(t_vorher-t_nachher)+e_Var*l_M*(t_vorher-t_nachher)/t_DLZ)*P-k_P*t_nachher*P for t_vorher, t_nachher, e_Var, l_M,t_DLZ,P in zip(t_unsupported,t_supported,r_acc,l_Mx, t_DLZ,P_x)]) 
    npv = - I_total
    for t in range(1, int(T) + 1): 
        npv += (x_specific - C_main)/ ((1 + r) ** t)
    return npv
def calculate_npv_separate(I_same,I_sim,c_main_same,c_main_sim,k_personal,r,T,t_unsupported,t_supported,r_acc,l_Mx, t_DLZ,P_x):         
    C_main_same = c_main_same / 100 * I_same # K_IHJ=k_IH*I_0
    C_main_sim = c_main_sim / 100 * I_sim
    C_main = C_main_sim+C_main_same
    I_total = I_same+I_sim
    k_P=k_personal / 60 # convert to minutes
    t_DLZ=[convert_decimal_time(x,False) for x in t_DLZ]
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

class Situation:
# Kapitalwerte von einzelnen Unterstützungslösungen berechnen
    def __init__(self,parameters):
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
        r = allgemeine_parameter.get("Zinssatz") / 100
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
        c_main_l2=0
        c_main_l3=0
        c_main_same=0
        c_main_sim=0
        #--------Erhöhung auf Reifegrad 2--------
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
                    c_main_l2=c_main
                    i_l2_best=i
                KW_l2_tables.append(small_table(KW_l2,I_total,t_supported,t_unsupported,IiA,KäA,2,name=i))
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
                    c_main_l3=c_main
                KW_l3_tables.append(small_table(KW_l3,I_total,t_supported,t_unsupported,IiA,KäA,3,name=i))
                i+=1
            KW_l3_tables.sort(key=lambda x: x.KW, reverse=True)

        #--------Erhöhung auf Reifegrad 3--------
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
                    c_main_l3=c_main
                KW_l3_tables.append(small_table(KW_l3,I_total,t_supported,t_unsupported,IiA,KäA,3,name=i))
                i+=1
            KW_l3_tables.sort(key=lambda x: x.KW, reverse=True)
            KW_l2_tables.append(html.P(KW_l2))

        #--------Reifegrad 3--------
        else:
            KW_l2 = "bereits umgesetzt"
            KW_l3 = "bereits umgesetzt"
            KW_l2_tables.append(html.P(KW_l2))
            KW_l3_tables.append(html.P(KW_l3))

        I_l2 = I_l2_best
        I_l3= I_l3_best
        self.I_l2=I_l2
        self.I_l3=I_l3
        self.c_main_l2=c_main_l2
        self.c_main_l3=c_main_l3
        
        c_main_same=0
        c_main_sim=0
        #--------Identifizierung identischer Artikel--------
        KW_IiA_tables = []
        if IiA==0:
            i = 1
            KW_IiA_max=-10**6
            for I_identisch, c_main in zip(I_same_list,c_main_list_3):
                I_total=calculate_investment(Alternative(1, KäA, matlevel),Alternative(IiA, KäA, matlevel),I_l2,I_l3,I_identisch,I_sim)
                t_supported = calculate_time(matlevel,cumTimeSameComponent,cumTimeSimComponent,cumTimeNewComponent,1,KäA,cumtimeProcess,cumtimeResource,n_KäA,mean_amount_of_elem_comp)
                KW_IiA=calculate_npv(I_total,c_main,k_personal,r,T,t_unsupported,t_supported,r_acc,l_Mx, t_DLZ,P_x)
                if KW_IiA>KW_IiA_max:
                    KW_IiA_max=KW_IiA
                    c_main_same=c_main
                    I_identisch_best=I_identisch
                KW_IiA_tables.append(small_table(KW_IiA,I_total,t_supported,t_unsupported,1,KäA,matlevel,name=i))
                i+=1
            KW_IiA_tables.sort(key=lambda x: x.KW, reverse=True)

        #--------Klassifizierung ähnlicher Artikel--------
        KW_KäA_tables = []
        if KäA == 0:
            i=1
            KW_KäA_max=-10**6
            for n_KäA, I_sim, c_main in zip(n_KäA_list,I_sim_list, c_main_list):
                n_KäA = [n_KäA for x in range(0, len(cumtimeProcess))]
                I_total=calculate_investment(Alternative(IiA, 1, matlevel),Alternative(IiA, KäA, matlevel),I_l2,I_l3,I_identisch,I_sim)
                t_supported = calculate_time(matlevel,cumTimeSameComponent,cumTimeSimComponent,cumTimeNewComponent,IiA,1,cumtimeProcess,cumtimeResource,n_KäA,mean_amount_of_elem_comp)
                KW_KäA=calculate_npv(I_total,c_main,k_personal,r,T,t_unsupported,t_supported,r_acc,l_Mx, t_DLZ,P_x)
                if KW_KäA>KW_KäA_max:
                    KW_KäA_max=KW_KäA
                    c_main_sim=c_main
                    I_sim_best=I_sim
                    n_KäA_best=n_KäA
                KW_KäA_tables.append(small_table(KW_KäA,I_total,t_supported,t_unsupported,IiA,1,matlevel,name=i))
                i+=1
            KW_KäA_tables.sort(key=lambda x: x.KW, reverse=True)
        
        #------------beide--------------
        if KäA == 0 and IiA == 0:
            I_total=I_identisch_best+I_sim_best
            t_supported = calculate_time(matlevel,cumTimeSameComponent,cumTimeSimComponent,cumTimeNewComponent,1,1,cumtimeProcess,cumtimeResource,n_KäA_best,mean_amount_of_elem_comp)
            KW_KäA_IiA_max = calculate_npv_separate(I_identisch_best,I_sim_best,c_main_same,c_main_sim,k_personal,r,T,t_unsupported,t_supported,r_acc,l_Mx, t_DLZ,P_x )
            KW_KäA_IiA_table=small_table(KW_KäA_IiA_max,I_total,t_supported,t_unsupported,1,1,matlevel)
            all_tables = [KW_IiA_tables[0]]+[KW_KäA_tables[0]]+[KW_KäA_IiA_table]
            all_tables.sort(key=lambda x: x.KW, reverse=True)
        elif KäA == 0:
            all_tables = [KW_KäA_tables[0]] 
        elif IiA == 0:
            all_tables = [KW_IiA_tables[0]] 
        best_solution = all_tables[0] if (KäA == 0 or IiA == 0) else None

        if IiA==0 or KäA==0:
            used_support = best_solution.support_functions

            #------------------------give recommendations-------------------------------------------------------------------
            recommend1=[]
            if best_solution.KW>=0:
                if "KäA" not in used_support and KäA==0:
                    recommend1.append(html.P("KäA nicht umgesetzt"))
                    i = I_sim
                    while i>=0:
                        i-=1
                        I_total=calculate_investment(Alternative(1, 1, matlevel),Alternative(IiA, KäA, matlevel),I_l2,I_l3,I_identisch,i)
                        t_supported = calculate_time(matlevel,cumTimeSameComponent,cumTimeSimComponent,cumTimeNewComponent,1,1,cumtimeProcess,cumtimeResource,n_KäA_list,mean_amount_of_elem_comp)
                        kw = calculate_npv(I_total,c_main_sim,k_personal,r,T,t_unsupported,t_supported,r_acc,l_Mx, t_DLZ,P_x)
                        if kw >= KW_IiA_max:
                            break
                    if i>=0:
                        recommend1.append(html.P(f"Investition von {I_sim} auf {i} ändern"))
                    else:
                        recommend1.append(html.P("Die Reduzierung der Investition auf den Wert 0 reicht nicht aus, um die Unterstützungslösung anzunehmen\. Daher müssen die Eingangsparameter in Kombination reduziert werden\."))
                    
                    c = c_main_sim
                    I_total=calculate_investment(Alternative(1, 1, matlevel),Alternative(IiA, KäA, matlevel),I_l2,I_l3,I_identisch,I_sim)
                    while c>=0:
                        c-=1
                        t_supported = calculate_time(matlevel,cumTimeSameComponent,cumTimeSimComponent,cumTimeNewComponent,1,1,cumtimeProcess,cumtimeResource,n_KäA_list,mean_amount_of_elem_comp)
                        kw = calculate_npv(I_total,c,k_personal,r,T,t_unsupported,t_supported,r_acc,l_Mx, t_DLZ,P_x)
                        if kw >= KW_IiA_max:
                            break
                    if c>=0:
                        recommend1.append(html.P(f"Instandhaltungskostensatz von {c_main_sim} auf {c} ändern"))
                    else:
                        recommend1.append(html.P("Die Reduzierung von Instandhaltungskostensatz auf den Wert 0 reicht nicht aus, um die Unterstützungslösung anzunehmen. Daher müssen die Eingangsparameter in Kombination reduziert werden."))
                    
                    n_KäA = n_KäA_list.copy()
                    while n_KäA[KW_KäA_tables[0].number-1]>=0:
                        n_KäA[KW_KäA_tables[0].number-1]-=1
                        t_supported = calculate_time(matlevel,cumTimeSameComponent,cumTimeSimComponent,cumTimeNewComponent,1,1,cumtimeProcess,cumtimeResource,n_KäA,mean_amount_of_elem_comp)
                        kw = calculate_npv(I_total,c_main_sim,k_personal,r,T,t_unsupported,t_supported,r_acc,l_Mx, t_DLZ,P_x)
                        if kw >= KW_IiA_max:
                            break
                    if n_KäA[KW_KäA_tables[0].number-1]>=0:
                        recommend1.append(html.P(f"Anzahl manueller Eingabe von {n_KäA_list[KW_KäA_tables[0].number-1]} auf {n_KäA[KW_KäA_tables[0].number-1]} ändern"))
                    else:
                        recommend1.append(html.P("Die Reduzierung der Anzahl manueller Eingabe auf den Wert 0 reicht nicht aus, um die Unterstützungslösung anzunehmen. Daher müssen die Eingangsparameter in Kombination reduziert werden."))
                       
                    
                if "IiA" not in used_support and IiA==0:
                    recommend1.append("IiA nicht umgesetzt")
                    i = I_identisch
                    while i>=0:
                        i-=1
                        I_total=calculate_investment(Alternative(1, 1, matlevel),Alternative(IiA, KäA, matlevel),I_l2,I_l3,i,I_sim)
                        t_supported = calculate_time(matlevel,cumTimeSameComponent,cumTimeSimComponent,cumTimeNewComponent,1,1,cumtimeProcess,cumtimeResource,n_KäA_list,mean_amount_of_elem_comp)
                        kw = calculate_npv(I_total,c_main_same,k_personal,r,T,t_unsupported,t_supported,r_acc,l_Mx, t_DLZ,P_x)
                        if kw >= KW_KäA_max:
                            break
                    if i>=0:
                        recommend1.append(html.P(f"Investition von {I_identisch} auf {i} ändern"))
                    else:
                        recommend1.append(html.P("Die Reduzierung der Investition auf den Wert 0 reicht nicht aus, um die Unterstützungslösung anzunehmen\. Daher müssen die Eingangsparameter in Kombination reduziert werden\."))
                    
                    c = c_main_same
                    I_total=calculate_investment(Alternative(1, 1, matlevel),Alternative(IiA, KäA, matlevel),I_l2,I_l3,I_identisch,I_sim)
                    while c>=0:
                        c-=1
                        t_supported = calculate_time(matlevel,cumTimeSameComponent,cumTimeSimComponent,cumTimeNewComponent,1,1,cumtimeProcess,cumtimeResource,n_KäA_list,mean_amount_of_elem_comp)
                        kw = calculate_npv(I_total,c,k_personal,r,T,t_unsupported,t_supported,r_acc,l_Mx, t_DLZ,P_x)
                        if kw >= KW_KäA_max:
                            break
                    if c>=0:
                        recommend1.append(html.P(f"Instandhaltungskostensatz von {c_main_same} auf {c} ändern"))
                    else:
                        recommend1.append(html.P("Die Reduzierung von Instandhaltungskostensatz auf den Wert 0 reicht nicht aus, um die Unterstützungslösung anzunehmen. Daher müssen die Eingangsparameter in Kombination reduziert werden."))
                    

            else:
                recommend1.append("Kapitalwert negativ")
                if KäA==0:
                    i = I_sim
                    while i>=0:
                        i-=1
                        I_total=calculate_investment(Alternative(1, 1, matlevel),Alternative(IiA, KäA, matlevel),I_l2,I_l3,I_identisch,i)
                        t_supported = calculate_time(matlevel,cumTimeSameComponent,cumTimeSimComponent,cumTimeNewComponent,1,1,cumtimeProcess,cumtimeResource,n_KäA_list,mean_amount_of_elem_comp)
                        kw = calculate_npv(I_total,c_main_sim,k_personal,r,T,t_unsupported,t_supported,r_acc,l_Mx, t_DLZ,P_x)
                        if kw >= 0:
                            break
                    if i>=0:
                            recommend1.append(html.P(f"Investition für KäA von {I_sim} auf {i} ändern"))
                    else:
                        recommend1.append(html.P("Die Reduzierung der Investition für KäA auf den Wert 0 reicht nicht aus, um die Unterstützungslösung anzunehmen. Daher müssen die Eingangsparameter in Kombination reduziert werden."))
                    
                    c = c_main_sim
                    I_total=calculate_investment(Alternative(1, 1, matlevel),Alternative(IiA, KäA, matlevel),I_l2,I_l3,I_identisch,I_sim)
                    while c>=0:
                        c-=1
                        t_supported = calculate_time(matlevel,cumTimeSameComponent,cumTimeSimComponent,cumTimeNewComponent,1,1,cumtimeProcess,cumtimeResource,n_KäA_list,mean_amount_of_elem_comp)
                        kw = calculate_npv(I_total,c,k_personal,r,T,t_unsupported,t_supported,r_acc,l_Mx, t_DLZ,P_x)
                        if kw >= 0:
                            break
                    if c>=0:
                            recommend1.append(html.P(f"Instandhaltungskostensatz von KäA von {c_main_sim} auf {c} ändern"))
                    else:
                        recommend1.append(html.P("Die Reduzierung von Instandhaltungskostensatz von KäA auf den Wert 0 reicht nicht aus, um die Unterstützungslösung anzunehmen. Daher müssen die Eingangsparameter in Kombination reduziert werden."))
                    
                    n_KäA = n_KäA_list.copy()
                    while n_KäA[KW_KäA_tables[0].number-1]>=0:
                        n_KäA[KW_KäA_tables[0].number-1]-=1
                        t_supported = calculate_time(matlevel,cumTimeSameComponent,cumTimeSimComponent,cumTimeNewComponent,1,1,cumtimeProcess,cumtimeResource,n_KäA,mean_amount_of_elem_comp)
                        kw = calculate_npv(I_total,c_main_sim,k_personal,r,T,t_unsupported,t_supported,r_acc,l_Mx, t_DLZ,P_x)
                        if kw >= 0:
                            break
                    if n_KäA[KW_KäA_tables[0].number-1]>=0:
                        recommend1.append(html.P(f"Anzahl manueller Eingabe von {n_KäA_list[KW_KäA_tables[0].number-1]} auf {n_KäA[KW_KäA_tables[0].number-1]} ändern"))
                    else:
                        recommend1.append(html.P("Die Reduzierung von Anzahl manueller Eingabe auf den Wert 0 reicht nicht aus, um die Unterstützungslösung anzunehmen. Daher müssen die Eingangsparameter in Kombination reduziert werden."))
                               
                if IiA==0:
                    i = I_identisch
                    while i>=0:
                        i-=1
                        I_total=calculate_investment(Alternative(1, 1, matlevel),Alternative(IiA, KäA, matlevel),I_l2,I_l3,i,I_sim)
                        t_supported = calculate_time(matlevel,cumTimeSameComponent,cumTimeSimComponent,cumTimeNewComponent,1,1,cumtimeProcess,cumtimeResource,n_KäA_list,mean_amount_of_elem_comp)
                        kw = calculate_npv(I_total,c_main_same,k_personal,r,T,t_unsupported,t_supported,r_acc,l_Mx, t_DLZ,P_x)
                        if kw >= 0:
                            break
                    if i>=0:
                            recommend1.append(html.P(f"Investition für IiA von {I_identisch} auf {i} ändern"))
                    else:
                        recommend1.append(html.P("Die Reduzierung der Investition für IiA auf den Wert 0 reicht nicht aus, um die Unterstützungslösung anzunehmen. Daher müssen die Eingangsparameter in Kombination reduziert werden."))
                       
                    c = c_main_same
                    I_total=calculate_investment(Alternative(1, 1, matlevel),Alternative(IiA, KäA, matlevel),I_l2,I_l3,I_identisch,I_sim)
                    while c>=0:
                        c-=1
                        t_supported = calculate_time(matlevel,cumTimeSameComponent,cumTimeSimComponent,cumTimeNewComponent,1,1,cumtimeProcess,cumtimeResource,n_KäA_list,mean_amount_of_elem_comp)
                        kw = calculate_npv(I_total,c,k_personal,r,T,t_unsupported,t_supported,r_acc,l_Mx, t_DLZ,P_x)
                        if kw >= 0:
                            break
                    if c>=0:
                            recommend1.append(html.P(f"Instandhaltungskostensatz von IiA von {c_main_same} auf {c} ändern"))
                    else:
                        recommend1.append(html.P("Die Reduzierung von Instandhaltungskostensatz von IiA auf den Wert 0 reicht nicht aus, um die Unterstützungslösung anzunehmen. Daher müssen die Eingangsparameter in Kombination reduziert werden."))
                                

            self.recommend1=recommend1
        else:
            self.recommend1=None
        #----------------------------------RG ----------------------------------------------
        self.KW_l2_tables=KW_l2_tables
        self.KW_l3_tables=KW_l3_tables
        recommend2=[]

        if matlevel==1:
            self.best_level = sorted([KW_l2_tables[0]]+[KW_l3_tables[0]], key=lambda x: x.KW, reverse=True)[0]
        elif matlevel==2:
            self.best_level = KW_l3_tables[0]
        else:
            self.best_level = None
        
        if  (matlevel==2 and self.best_level.KW<0) or (matlevel==1 and self.best_level.RG==2):
            if matlevel==1:
                recommend2.append(html.P("Reifegrad 3 nicht umgesetzt"))
            i = I_l3
            goal_KW = KW_l2_max if matlevel == 1 else 0
            while i>=0:
                i-=1
                I_total=KW_l2_tables[0].investition+i if matlevel == 1 else i
                t_supported = calculate_time(3,cumTimeSameComponent,cumTimeSimComponent,cumTimeNewComponent,IiA,KäA,cumtimeProcess,cumtimeResource,n_KäA_list,mean_amount_of_elem_comp)
                kw = calculate_npv(I_total,c_main_l3,k_personal,r,T,t_unsupported,t_supported,r_acc,l_Mx, t_DLZ,P_x)
                if kw >= goal_KW:
                    break
            if i>=0:
                    recommend2.append(html.P(f"Investition für Reifegradstufe 3 von {I_l3} auf {i} ändern"))
            else:
                    recommend2.append(html.P("Die Reduzierung der Investition für Reifegradstufe 3 auf den Wert 0 reicht nicht aus, um die Unterstützungslösung anzunehmen. Daher müssen die Eingangsparameter in Kombination reduziert werden."))
                    
            c = c_main_l3
            I_total=KW_l2_tables[0].investition+I_l3 if matlevel == 1 else I_l3
            while c>=0:
                c-=1
                t_supported = calculate_time(3,cumTimeSameComponent,cumTimeSimComponent,cumTimeNewComponent,IiA,KäA,cumtimeProcess,cumtimeResource,n_KäA_list,mean_amount_of_elem_comp)
                kw = calculate_npv(I_total,c,k_personal,r,T,t_unsupported,t_supported,r_acc,l_Mx, t_DLZ,P_x)
                if kw >= goal_KW:
                    break
            if c>=0:
                    recommend2.append(html.P(f"Instandhaltungskostensatz von Reifegradstufe 3 von {c_main_l3} auf {c} ändern"))
            else:
                        recommend2.append(html.P("Die Reduzierung von Instandhaltungskostensatz von Reifegradstufe 3 auf den Wert 0 reicht nicht aus, um die Unterstützungslösung anzunehmen. Daher müssen die Eingangsparameter in Kombination reduziert werden."))
                            
        if  matlevel==1 and self.best_level.KW<0:
            recommend2.append("Kapitalwert negativ")
            i = I_l2
            while i>=0:
                i-=1
                I_total=i
                t_supported = calculate_time(2,cumTimeSameComponent,cumTimeSimComponent,cumTimeNewComponent,IiA,KäA,cumtimeProcess,cumtimeResource,n_KäA_list,mean_amount_of_elem_comp)
                kw = calculate_npv(I_total,c_main_l2,k_personal,r,T,t_unsupported,t_supported,r_acc,l_Mx, t_DLZ,P_x)
                if kw >= 0:
                    break
            if i>=0:
                    recommend2.append(html.P(f"Investition für Reifegradstufe 2 von {I_l2} auf {i} ändern"))
            else:
                        recommend2.append(html.P("Die Reduzierung der Investition für Reifegradstufe 2 auf den Wert 0 reicht nicht aus, um die Unterstützungslösung anzunehmen. Daher müssen die Eingangsparameter in Kombination reduziert werden."))
                        
            c = c_main_l2
            I_total=I_l2
            while c>=0:
                c-=1
                t_supported = calculate_time(2,cumTimeSameComponent,cumTimeSimComponent,cumTimeNewComponent,IiA,KäA,cumtimeProcess,cumtimeResource,n_KäA_list,mean_amount_of_elem_comp)
                kw = calculate_npv(I_total,c,k_personal,r,T,t_unsupported,t_supported,r_acc,l_Mx, t_DLZ,P_x)
                if kw >= 0:
                    break
            if c>=0:
                    recommend2.append(html.P(f"Instandhaltungskostensatz von Reifegradstufe 2 von {c_main_l2} auf {c} ändern"))
            else:
                        recommend2.append(html.P("Die Reduzierung von Instandhaltungskostensatz von Reifegradstufe 2 auf den Wert 0 reicht nicht aus, um die Unterstützungslösung anzunehmen. Daher müssen die Eingangsparameter in Kombination reduziert werden."))
                    
        self.recommend2=recommend2
        self.KW_IiA_tables=KW_IiA_tables
        self.KW_KäA_tables=KW_KäA_tables
        self.c_main_same=c_main_same
        self.c_main_sim=c_main_sim
        self.best_solution = best_solution





    
    


