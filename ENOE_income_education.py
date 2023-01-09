#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 10:50:47 2022

@author: ja
"""
# Modules
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import statsmodels.formula.api as smf

# Functions

    # ENOE treatment
def ENOE(DB):
    selection = ["eda",       # Age 
                 "ent",       # State
                 "anios_esc", # School years
                 "cs_p13_1",  # School levels
                 "ing_x_hrs", # Income per hour worked
                 "hrsocup"]   # Hrs worked per week    
    DB = DB[selection]
    
    # Correct variable format
    
        # Age
    DB = DB[DB["eda"] != ' ']
    DB = DB.astype({'eda':'int64'})
    
        # Education leves
    DB = DB[DB['cs_p13_1'] != ' ']
    DB = DB.astype({'cs_p13_1':'int64'}) 
    
    # Persons aged 15 or over and excluding codes 98 (Age not specified for those over 12 years of age and over) 99 (Age not specified for children under 0 to 11 years of age)
    DB = DB[(DB["eda"] >= 15) & (DB["eda"] != 98) & (DB["eda"] != 99)]
    
    # People whose income pero hour worked is greater than 0
    DB = DB[DB["ing_x_hrs"] > 0]
    
    # People whose weekly hours worked are greater than zero
    DB = DB[DB["hrsocup"] > 0]
    
    # Persons with specified years of schooling
    DB = DB[DB["anios_esc"] != 99]
    
    # People with specified educational levels
    DB = DB[DB["cs_p13_1"] != 99]
    
    # Levels assignation
    
    # Educational 
    niveles = [DB["cs_p13_1"] == 0,
               DB["cs_p13_1"] == 1,
               DB["cs_p13_1"] == 2,
               DB["cs_p13_1"] == 3,
               DB["cs_p13_1"] == 4,
               DB["cs_p13_1"] == 5,
               DB["cs_p13_1"] == 6,
               DB["cs_p13_1"] == 7,
               DB["cs_p13_1"] == 8,
               DB["cs_p13_1"] == 9,
               DB["cs_p13_1"] == 99]
    
    DB["cs_p13_1"] = np.select(niveles,["Ninguna",
                                        "Preescolar",
                                        "Primaria",
                                        "Secundaria",
                                        "Preparatoria o bachillerato",
                                        "Normal",
                                        "Carrera técnica",
                                        "Profesional",
                                        "Maestría",
                                        "Doctorado",
                                        "No sabe"])
    
    # Educational levels primary, secondary, high school or baccalaureate, professional, master's, doctorate
    DB = DB[DB["cs_p13_1"].isin(["Ninguna",
                                 "Primaria",
                                 "Secundaria",
                                 "Preparatoria o bachillerato",
                                 "Profesional",
                                 "Maestría",
                                 "Doctorado"])]
    
    DB["cs_p13_1"] = pd.Categorical(DB["cs_p13_1"], categories = ["Ninguna",
                                                                  "Primaria",
                                                                  "Secundaria",
                                                                  "Preparatoria o bachillerato",
                                                                  "Profesional",
                                                                  "Maestría",
                                                                  "Doctorado"], ordered = True)
                                                          
    
    # Federal entities of Mexico
    entidades = [DB["ent"] == 1,
                 DB["ent"] == 2,
                 DB["ent"] == 3,
                 DB["ent"] == 4,
                 DB["ent"] == 5,
                 DB["ent"] == 6,
                 DB["ent"] == 7,
                 DB["ent"] == 8,
                 DB["ent"] == 9,
                 DB["ent"] == 10,
                 DB["ent"] == 11,
                 DB["ent"] == 12,
                 DB["ent"] == 13,
                 DB["ent"] == 14,
                 DB["ent"] == 15,
                 DB["ent"] == 16,
                 DB["ent"] == 17,
                 DB["ent"] == 18,
                 DB["ent"] == 19,
                 DB["ent"] == 20,
                 DB["ent"] == 21,
                 DB["ent"] == 22,
                 DB["ent"] == 23,
                 DB["ent"] == 24,
                 DB["ent"] == 25,
                 DB["ent"] == 26,
                 DB["ent"] == 27,
                 DB["ent"] == 28,
                 DB["ent"] == 29,
                 DB["ent"] == 30,
                 DB["ent"] == 31,
                 DB["ent"] == 32]

    DB["ent"] = np.select(entidades,["Aguascalientes",
                                     "Baja California",
                                     "Baja California Sur",
                                     "Campeche",
                                     "Coahuila de Zaragoza",
                                     "Colima",
                                     "Chiapas",
                                     "Chihuahua",
                                     "Ciudad de México",
                                     "Durango",
                                     "Guanajuato",
                                     "Guerrero",
                                     "Hidalgo",
                                     "Jalisco",
                                     "México",
                                     "Michoacán de Ocampo",
                                     "Morelos",
                                     "Nayarit",
                                     "Nuevo León",
                                     "Oaxaca",
                                     "Puebla",
                                     "Querétaro",
                                     "Quintana Roo",
                                     "San Luis Potosí",
                                     "Sinaloa",
                                     "Sonora",
                                     "Tabasco",
                                     "Tamaulipas",
                                     "Tlaxcala",
                                     "Veracruz de Ignacio de la Llave",
                                     "Yucatán",
                                     "Zacatecas"])
    
    DB["ent"] = DB["ent"].astype("category")
        
    # Experience
    DB["exp"] = DB["eda"] - DB["anios_esc"]
    
    return DB

    # Rename some columns in old data frames
def db_rename(DB):
    DB = DB.rename(columns = {'t_loc':'t_loc_tri'})
    return DB

# Database, table corresponding to sociodemographic variables
DB_2022 = pd.read_csv('/media/ja/Andres data/Documentos/Mincer/Data/enoe_n_2022_trim3_csv/ENOEN_SDEMT322.csv', encoding='unicode_escape',low_memory = False)
DB_2021 = pd.read_csv('/media/ja/Andres data/Documentos/Mincer/Data/enoe_n_2021_trim3_csv/ENOEN_SDEMT321.csv', encoding='unicode_escape',low_memory = False)
DB_2020 = pd.read_csv('/media/ja/Andres data/Documentos/Mincer/Data/enoe_n_2020_trim3_csv/ENOEN_SDEMT320.csv', encoding='unicode_escape',low_memory = False)
DB_2019 = pd.read_csv('/media/ja/Andres data/Documentos/Mincer/Data/2019trim3_csv/sdemt319.csv', encoding='unicode_escape',low_memory = False)
DB_2018 = pd.read_csv('/media/ja/Andres data/Documentos/Mincer/Data/2018trim3_csv/SDEMT318.csv', encoding='unicode_escape',low_memory = False)
DB_2017 = pd.read_csv('/media/ja/Andres data/Documentos/Mincer/Data/2017trim3_csv/SDEMT317.csv', encoding='unicode_escape',low_memory = False)
DB_2016 = pd.read_csv('/media/ja/Andres data/Documentos/Mincer/Data/2016trim3_csv/SDEMT316.csv', encoding='unicode_escape',low_memory = False)
DB_2015 = pd.read_csv('/media/ja/Andres data/Documentos/Mincer/Data/2015trim3_csv/SDEMT315.csv', encoding='unicode_escape',low_memory = False)
DB_2014 = pd.read_csv('/media/ja/Andres data/Documentos/Mincer/Data/2014trim3_csv/sdemt314.CSV', encoding='unicode_escape',low_memory = False)
DB_2013 = pd.read_csv('/media/ja/Andres data/Documentos/Mincer/Data/2013trim3_csv/sdemt313.CSV', encoding='unicode_escape',low_memory = False)
DB_2012 = pd.read_csv('/media/ja/Andres data/Documentos/Mincer/Data/2012trim3_csv/sdemt312.CSV', encoding='unicode_escape',low_memory = False)
DB_2011 = pd.read_csv('/media/ja/Andres data/Documentos/Mincer/Data/2011trim3_csv/sdemt311.CSV', encoding='unicode_escape',low_memory = False)
DB_2010 = pd.read_csv('/media/ja/Andres data/Documentos/Mincer/Data/2010trim3_csv/sdemt310.CSV', encoding='unicode_escape',low_memory = False)
DB_2009 = pd.read_csv('/media/ja/Andres data/Documentos/Mincer/Data/2009trim3_csv/sdemt309.CSV', encoding='unicode_escape',low_memory = False)
DB_2008 = pd.read_csv('/media/ja/Andres data/Documentos/Mincer/Data/2008trim3_csv/sdemt308.CSV', encoding='unicode_escape',low_memory = False)
DB_2007 = pd.read_csv('/media/ja/Andres data/Documentos/Mincer/Data/2007trim3_csv/sdemt307.CSV', encoding='unicode_escape',low_memory = False)

# INPC to have the income in real terms
INPC = pd.read_csv('/media/ja/Andres data/Documentos/Mincer/Data/ca55_2018.csv', encoding='unicode_escape')

INPC = INPC.set_index("Fecha")
INPC = [INPC.loc["jul 2007":"Sep 2007"].mean(),
        INPC.loc["jul 2008":"Sep 2008"].mean(),
        INPC.loc["jul 2009":"Sep 2009"].mean(),
        INPC.loc["jul 2010":"Sep 2010"].mean(),
        INPC.loc["jul 2011":"Sep 2011"].mean(),
        INPC.loc["jul 2012":"Sep 2012"].mean(),
        INPC.loc["jul 2013":"Sep 2013"].mean(),
        INPC.loc["jul 2014":"Sep 2014"].mean(),
        INPC.loc["jul 2015":"Sep 2015"].mean(),
        INPC.loc["jul 2016":"Sep 2016"].mean(),
        INPC.loc["jul 2017":"Sep 2017"].mean(),
        INPC.loc["jul 2018":"Sep 2018"].mean(),
        INPC.loc["jul 2019":"Sep 2019"].mean(),
        INPC.loc["jul 2020":"Sep 2020"].mean(),
        INPC.loc["jul 2021":"Sep 2021"].mean(),
        INPC.loc["jul 2022":"Sep 2022"].mean()]

INPC = [i[0] for i in INPC]

# Selection of variables of interest in the dataframes
DB_2022 = ENOE(DB_2022)
DB_2022["inpc"] = INPC[15]

DB_2021 = ENOE(DB_2021)
DB_2021["inpc"] = INPC[14]

DB_2020 = ENOE(DB_2020)
DB_2020["inpc"] = INPC[13]

lista_mayus = list(DB_2019.columns)

lista_minuscula = [i.lower() for i in lista_mayus]

DB_2019.columns = lista_minuscula

del lista_mayus, lista_minuscula

DB_2019 = ENOE(db_rename(DB_2019))
DB_2019["inpc"] = INPC[12]

DB_2018 = ENOE(db_rename(DB_2018))
DB_2018["inpc"] = INPC[11]

DB_2017 = ENOE(db_rename(DB_2017))
DB_2017["inpc"] = INPC[10]

DB_2016 = ENOE(db_rename(DB_2016))
DB_2016["inpc"] = INPC[9]

DB_2015 = ENOE(db_rename(DB_2015))
DB_2015["inpc"] = INPC[8]
    
DB_2014 = DB_2014.dropna(subset = ["eda","sex","cs_p13_1"])
DB_2014 = ENOE(db_rename(DB_2014))
DB_2014["inpc"] = INPC[7]

DB_2013 = DB_2013.dropna(subset = ["eda","sex","cs_p13_1"])
DB_2013 = ENOE(db_rename(DB_2013))
DB_2013["inpc"] = INPC[6]

DB_2012 = DB_2012.dropna(subset = ["eda","sex","cs_p13_1"])
DB_2012 = ENOE(db_rename(DB_2012))
DB_2012["inpc"] = INPC[5]

DB_2011 = DB_2011.dropna(subset = ["eda","sex","cs_p13_1"])
DB_2011 = ENOE(db_rename(DB_2011))
DB_2011["inpc"] = INPC[4]

DB_2010 = DB_2010.dropna(subset = ["eda","sex","cs_p13_1"])
DB_2010 = ENOE(db_rename(DB_2010))
DB_2010["inpc"] = INPC[3]

DB_2009 = DB_2009.dropna(subset = ["eda","sex","cs_p13_1"])
DB_2009 = ENOE(db_rename(DB_2009))
DB_2009["inpc"] = INPC[2]

DB_2008 = DB_2008.dropna(subset = ["eda","sex","cs_p13_1"])
DB_2008 = ENOE(db_rename(DB_2008))
DB_2008["inpc"] = INPC[1]

DB_2007 = DB_2007.dropna(subset = ["eda","sex","cs_p13_1"])
DB_2007 = ENOE(db_rename(DB_2007))
DB_2007["inpc"] = INPC[0]


datos = [DB_2007,
         DB_2008,
         DB_2009,
         DB_2010,
         DB_2011,
         DB_2012,
         DB_2013,
         DB_2014,
         DB_2015,
         DB_2016,
         DB_2017,
         DB_2018,
         DB_2019,
         DB_2020,
         DB_2021,
         DB_2022]

del DB_2007, DB_2008, DB_2009, DB_2010, DB_2011, DB_2012, DB_2013, DB_2014, DB_2015, DB_2016, DB_2017, DB_2018, DB_2019, DB_2020, DB_2021, DB_2022, INPC

# Real income
for i in datos:
    i['ing_x_hrs'] = (i["ing_x_hrs"]/i["inpc"])*100
del i

# Yeays
year = [2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022]
years_str = [str(i) for i in year]


# Mexico map
entidades = gpd.read_file("/media/ja/Andres data/Descargas/Entidades y Municipios/00ent.shp")

# Tell a story
# =============================================================================
# What has been the evolution of people's income per hour worked
# What is the evolution of the education in Mexico
# What is the evolution of the hours worked

    # Average income per hour worked ======================================
ing_x_hrs = [i["ing_x_hrs"].mean() for i in datos]
ing_x_hrs_ent = [pd.DataFrame(i.groupby("ent")["ing_x_hrs"].mean()) for i in datos]
ing_x_hrs_nivel = [pd.DataFrame(i.groupby("cs_p13_1")["ing_x_hrs"].mean()) for i in datos]    

    # Average educational years ==============================================
years_edu = [i["anios_esc"].mean() for i in datos]
years_edu_ent = [pd.DataFrame(i.groupby("ent")["anios_esc"].mean()) for i in datos]

    # Hours worked per week average ====================================
work_hours = [i["hrsocup"].mean() for i in datos]
work_hours_ent = [pd.DataFrame(i.groupby("ent")["hrsocup"].mean()) for i in datos]
work_hours_nivel = [pd.DataFrame(i.groupby("cs_p13_1")["hrsocup"].mean()) for i in datos]


# Evolution of income per hour worked ======================================== 
    # Level  
ing_x_hrs_nivel_ninguna = [i.loc["Ninguna","ing_x_hrs"] for i in ing_x_hrs_nivel]
ing_x_hrs_nivel_primaria = [i.loc["Primaria","ing_x_hrs"] for i in ing_x_hrs_nivel]
ing_x_hrs_nivel_secundaria = [i.loc["Secundaria","ing_x_hrs"] for i in ing_x_hrs_nivel]
ing_x_hrs_nivel_preparatoria = [i.loc["Preparatoria o bachillerato","ing_x_hrs"] for i in ing_x_hrs_nivel]
ing_x_hrs_nivel_profesional = [i.loc["Profesional","ing_x_hrs"] for i in ing_x_hrs_nivel]
ing_x_hrs_nivel_maestría = [i.loc["Maestría","ing_x_hrs"] for i in ing_x_hrs_nivel]
ing_x_hrs_nivel_doctorado = [i.loc["Doctorado","ing_x_hrs"] for i in ing_x_hrs_nivel]
    # States
ing_x_hrs_ent_years = pd.concat([i.loc[:,"ing_x_hrs"] for i in ing_x_hrs_ent], axis = 1)
ing_x_hrs_ent_years.columns = years_str

    # PLots
plt.style.use("bmh")

        # General
plt.plot(year,ing_x_hrs)
plt.xlabel("años")
plt.ylabel("ingresos por hora trabajada")
plt.title("Ingreso real promedio en México (base 2018)")
plt.ylim(0,48)
plt.savefig('/home/ja/Documentos/income_edu_figures/income_per_hour_worked/plots/ing_x_hrs.jpg',dpi = 300, facecolor='w', bbox_inches='tight',pad_inches=0.3, transparent=True)
plt.show()
        # Education level
plt.plot(year,ing_x_hrs_nivel_ninguna, label = 'ninguno')
plt.plot(year,ing_x_hrs_nivel_primaria, label = 'primaria')
plt.plot(year,ing_x_hrs_nivel_secundaria, label = 'secundaria')
plt.plot(year,ing_x_hrs_nivel_preparatoria, label = 'preparatoria o bachillerato')
plt.plot(year,ing_x_hrs_nivel_profesional, label = 'profesional')
plt.plot(year,ing_x_hrs_nivel_maestría, label = 'maestría')
plt.plot(year,ing_x_hrs_nivel_doctorado, label = 'doctorado')
plt.xlabel("año")
plt.ylabel("ingreso por hora")
plt.title("Ingreso real promedio por nivel educativo en México (base 2018)")
plt.legend(loc=(1.05, 0.2))
plt.savefig('/home/ja/Documentos/income_edu_figures/income_per_hour_worked/plots/ing_x_hrs_niveles.jpg',dpi = 300, facecolor='w', bbox_inches='tight',pad_inches=0.3, transparent=True)
plt.show()

        # States of México
#min and max values 
minimo = ing_x_hrs_ent_years.to_numpy().min()
maximo = ing_x_hrs_ent_years.to_numpy().max()

def income_ent(año,name):
    mex = entidades.merge(ing_x_hrs_ent_years[año], left_on = 'NOMGEO', 
                          right_index = True, how = 'left')
    mapa_ingresos = mex.plot(column = año,
                             vmin=minimo, vmax=maximo,
                             legend = True,
                             cmap = 'Greens',
                             legend_kwds = {'orientation': "horizontal"})
    plt.title("Ingresos promedio por hora de trabajo (base 2018): " + año)
    plt.axis('off')
    plt.savefig(name, dpi = 300, bbox_inches='tight')
    return mapa_ingresos

names_incom = ["/home/ja/Documentos/income_edu_figures/income_per_hour_worked/maps/in_01.jpg",
               "/home/ja/Documentos/income_edu_figures/income_per_hour_worked/maps/in_02.jpg",
               "/home/ja/Documentos/income_edu_figures/income_per_hour_worked/maps/in_03.jpg",
               "/home/ja/Documentos/income_edu_figures/income_per_hour_worked/maps/in_04.jpg",
               "/home/ja/Documentos/income_edu_figures/income_per_hour_worked/maps/in_05.jpg",
               "/home/ja/Documentos/income_edu_figures/income_per_hour_worked/maps/in_06.jpg",
               "/home/ja/Documentos/income_edu_figures/income_per_hour_worked/maps/in_07.jpg",
               "/home/ja/Documentos/income_edu_figures/income_per_hour_worked/maps/in_08.jpg",
               "/home/ja/Documentos/income_edu_figures/income_per_hour_worked/maps/in_09.jpg",
               "/home/ja/Documentos/income_edu_figures/income_per_hour_worked/maps/in_10.jpg",
               "/home/ja/Documentos/income_edu_figures/income_per_hour_worked/maps/in_11.jpg",
               "/home/ja/Documentos/income_edu_figures/income_per_hour_worked/maps/in_12.jpg",
               "/home/ja/Documentos/income_edu_figures/income_per_hour_worked/maps/in_13.jpg",
               "/home/ja/Documentos/income_edu_figures/income_per_hour_worked/maps/in_14.jpg",
               "/home/ja/Documentos/income_edu_figures/income_per_hour_worked/maps/in_15.jpg",
               "/home/ja/Documentos/income_edu_figures/income_per_hour_worked/maps/in_16.jpg"]

#Save figs as jgp
for i,j in zip(ing_x_hrs_ent_years.columns,names_incom):
    income_ent(i,j)

###Creating the GIF
def make_gif(frame_folder):
    frames = [Image.open(image) for image in names_incom]
    frame_one = frames[0]
    frame_one.save("/home/ja/Documentos/income_edu_figures/income_per_hour_worked/maps/ingreso_hora_ent.gif", format="GIF", append_images=frames,
               save_all=True, duration=500, loop=0)
    
if __name__ == "__main__":
    make_gif("/home/ja/Documentos/income_edu_figures/income_per_hour_worked/maps/")

# Evolution of education years =================================================
    # States
years_edu_ent_years = pd.concat([i.loc[:,"anios_esc"] for i in years_edu_ent], axis = 1)
years_edu_ent_years.columns = years_str

    # Plots
        # General
plt.bar(year,years_edu)
plt.title("Años de educación promedio")
plt.xlabel("años")
plt.ylabel("años de educación")
plt.ylim(0,12)
plt.savefig('/home/ja/Documentos/income_edu_figures/education/plots/years_edu.jpg',dpi = 300, facecolor='w', bbox_inches='tight',pad_inches=0.3, transparent=True)
plt.show()        

        # States of México
minimo = years_edu_ent_years.to_numpy().min()
maximo = years_edu_ent_years.to_numpy().max()
    
def education_ent(año,name):
    mex = entidades.merge(years_edu_ent_years[año], left_on = 'NOMGEO', right_index = True, how = 'left')
    mapa_educacion = mex.plot(column = año,
                             vmin=minimo, vmax=maximo,
                             legend = True,
                             cmap = 'Blues',
                             legend_kwds = {'orientation': "horizontal"})
    plt.title("Años de educación promedio: " + año)
    plt.axis('off')
    plt.savefig(name, dpi = 300, bbox_inches='tight')
    return mapa_educacion

names_educa = ["/home/ja/Documentos/income_edu_figures/education/maps/ed_1.jpg",
               "/home/ja/Documentos/income_edu_figures/education/maps/ed_2.jpg",
               "/home/ja/Documentos/income_edu_figures/education/maps/ed_3.jpg",
               "/home/ja/Documentos/income_edu_figures/education/maps/ed_4.jpg",
               "/home/ja/Documentos/income_edu_figures/education/maps/ed_5.jpg",
               "/home/ja/Documentos/income_edu_figures/education/maps/ed_6.jpg",
               "/home/ja/Documentos/income_edu_figures/education/maps/ed_7.jpg",
               "/home/ja/Documentos/income_edu_figures/education/maps/ed_8.jpg",
               "/home/ja/Documentos/income_edu_figures/education/maps/ed_9.jpg",
               "/home/ja/Documentos/income_edu_figures/education/maps/ed_10.jpg",
               "/home/ja/Documentos/income_edu_figures/education/maps/ed_11.jpg",
               "/home/ja/Documentos/income_edu_figures/education/maps/ed_12.jpg",
               "/home/ja/Documentos/income_edu_figures/education/maps/ed_13.jpg",
               "/home/ja/Documentos/income_edu_figures/education/maps/ed_14.jpg",
               "/home/ja/Documentos/income_edu_figures/education/maps/ed_15.jpg",
               "/home/ja/Documentos/income_edu_figures/education/maps/ed_16.jpg"]

for i,j in zip(years_edu_ent_years.columns,names_educa):
    education_ent(i,j)

def make_gif(frame_folder):
    frames = [Image.open(image) for image in names_educa]
    frame_one = frames[0]
    frame_one.save("/home/ja/Documentos/income_edu_figures/education/maps/educa_years_ent.gif", format="GIF", append_images=frames,
               save_all=True, duration=500, loop=0)
    
if __name__ == "__main__":
    make_gif("/home/ja/Documentos/income_edu_figures/education/maps/")

# Hours worked ===========================================================
 
    # Education level
work_hours_nivel_ninguna = [i.loc["Ninguna","hrsocup"] for i in work_hours_nivel]
work_hours_nivel_primaria = [i.loc["Primaria","hrsocup"] for i in work_hours_nivel]
work_hours_nivel_secundaria = [i.loc["Secundaria","hrsocup"] for i in work_hours_nivel]
work_hours_nivel_preparatoria = [i.loc["Preparatoria o bachillerato","hrsocup"] for i in work_hours_nivel]
work_hours_nivel_profesional = [i.loc["Profesional","hrsocup"] for i in work_hours_nivel]
work_hours_nivel_maestría = [i.loc["Maestría","hrsocup"] for i in work_hours_nivel]
work_hours_nivel_doctorado = [i.loc["Doctorado","hrsocup"] for i in work_hours_nivel]   
    # States
work_hrs_ent_years = pd.concat([i.loc[:,"hrsocup"] for i in work_hours_ent], axis = 1)
work_hrs_ent_years.columns = years_str
    
    # Plots
        # General
plt.plot(year, work_hours)
plt.title("Horas de trabajo semanal promedio")
plt.xlabel("años")
plt.ylabel("horas de trabajo")
plt.savefig('/home/ja/Documentos/income_edu_figures/hours_worked/plots/work_hrs.jpg',dpi = 300, facecolor='w', bbox_inches='tight',pad_inches=0.3, transparent=True)
plt.show()     
        # Education levels
plt.plot(year, work_hours_nivel_ninguna, label = "ninguno")
plt.plot(year, work_hours_nivel_primaria, label = "primaria")
plt.plot(year, work_hours_nivel_secundaria, label = "secundaria")
plt.plot(year, work_hours_nivel_preparatoria, label = "preparaoria o bachillerato")
plt.plot(year, work_hours_nivel_profesional, label = "profesional")
plt.plot(year, work_hours_nivel_maestría, label = "maestría")
plt.plot(year, work_hours_nivel_doctorado, label = "doctorado")
plt.xlabel("año")
plt.ylabel("horas de trabajo")
plt.title("Horas de trabajo semanal promedio por nivel educativo")
plt.legend(loc=(1.05, 0.2))
plt.savefig('/home/ja/Documentos/income_edu_figures/hours_worked/plots/work_hrs_niveles.jpg',dpi = 300, facecolor='w', bbox_inches='tight',pad_inches=0.3, transparent=True)
plt.show()

        # Map
minimo = work_hrs_ent_years.to_numpy().min()
maximo = work_hrs_ent_years.to_numpy().max()

def hours_worked(año,name):
    mex = entidades.merge(work_hrs_ent_years[año], left_on = 'NOMGEO', right_index = True, how = 'left')
    mapa_horas =  mex.plot(column = año,
                           vmin = minimo, vmax = maximo,
                           legend = True,
                           cmap = 'Oranges',
                           legend_kwds = {'orientation' : 'horizontal'})
    plt.title("Horas de trabajo semanal promedio: " + año)
    plt.axis('off')
    plt.savefig(name, dpi = 300, bbox_inches='tight')
    return mapa_horas

names_hours = ["/home/ja/Documentos/income_edu_figures/hours_worked/maps/mh_1.jpg",
               "/home/ja/Documentos/income_edu_figures/hours_worked/maps/mh_2.jpg",
               "/home/ja/Documentos/income_edu_figures/hours_worked/maps/mh_3.jpg",
               "/home/ja/Documentos/income_edu_figures/hours_worked/maps/mh_4.jpg",
               "/home/ja/Documentos/income_edu_figures/hours_worked/maps/mh_5.jpg",
               "/home/ja/Documentos/income_edu_figures/hours_worked/maps/mh_6.jpg",
               "/home/ja/Documentos/income_edu_figures/hours_worked/maps/mh_7.jpg",
               "/home/ja/Documentos/income_edu_figures/hours_worked/maps/mh_8.jpg",
               "/home/ja/Documentos/income_edu_figures/hours_worked/maps/mh_9.jpg",
               "/home/ja/Documentos/income_edu_figures/hours_worked/maps/mh_10.jpg",
               "/home/ja/Documentos/income_edu_figures/hours_worked/maps/mh_11.jpg",
               "/home/ja/Documentos/income_edu_figures/hours_worked/maps/mh_12.jpg",
               "/home/ja/Documentos/income_edu_figures/hours_worked/maps/mh_13.jpg",
               "/home/ja/Documentos/income_edu_figures/hours_worked/maps/mh_14.jpg",
               "/home/ja/Documentos/income_edu_figures/hours_worked/maps/mh_15.jpg",
               "/home/ja/Documentos/income_edu_figures/hours_worked/maps/mh_16.jpg"]

for i,j in zip(work_hrs_ent_years,names_hours):
    hours_worked(i,j)

def make_gif(frame_folder):
    frames = [Image.open(image) for image in names_hours]
    frame_one = frames[0]
    frame_one.save("/home/ja/Documentos/income_edu_figures/hours_worked/maps/hours_worked_ent.gif", format="GIF", append_images=frames,
               save_all=True, duration=500, loop=0)
    
if __name__ == "__main__":
    make_gif("/home/ja/Documentos/income_edu_figures/hours_worked/maps/")
    
### Mincer income 

models_MINCER_1 = [smf.ols('np.log(ing_x_hrs) ~ anios_esc + exp + np.square(exp)', data = i).fit() for i in datos]

revenue_education_years = [i.params[1]*100 for i in models_MINCER_1]
revenue_experience_years = [i.params[2]*100 for i in models_MINCER_1]

models_MINCER_2 = [smf.ols('np.log(ing_x_hrs) ~ C(cs_p13_1) + exp + np.square(exp)', data = i).fit() for i in datos]

revenue_education_levels = pd.concat([i.params[1:7]*100 for i in models_MINCER_2], axis = 1)
revenue_education_levels.columns = years_str
revenue_education_levels.index = ["Primaria",
                                  "Secundaria",
                                  "Preparatoria",
                                  "Profesional",
                                  "Maestría",
                                  "Doctorado"]

    # Plots
        # Years
plt.plot(year, revenue_education_years, label = "años de educación")
plt.plot(year, revenue_experience_years, label = "años de experiencia")
plt.xlabel("año")
plt.ylabel("rendimiento %")
plt.title("Rendimientos privados de la educación en México: 2007 - 2022")
plt.legend()
plt.savefig("/home/ja/Documentos/income_edu_figures/mincer/plots/mincer.jpg",dpi = 300, facecolor='w', bbox_inches='tight',pad_inches=0.3, transparent=True)
plt.show()
        # Levels education
plt.plot(year,revenue_education_levels.loc["Primaria",:], label = "Primaria")
plt.plot(year,revenue_education_levels.loc["Secundaria",:], label = "Secundaria")
plt.plot(year,revenue_education_levels.loc["Preparatoria",:], label = "Preparatoria o bachillerato")
plt.plot(year,revenue_education_levels.loc["Profesional",:], label = "Profesional")
plt.plot(year,revenue_education_levels.loc["Maestría",:], label = "Maestría")
plt.plot(year,revenue_education_levels.loc["Doctorado",:], label = "Doctorado")
plt.xlabel("año")
plt.ylabel("rendimiento %, ninguna educación")
plt.title("Rendimientos privados de la educación en México (niveles): 2007 - 2022")
plt.legend(loc=(1.05, 0.2))
plt.savefig("/home/ja/Documentos/income_edu_figures/mincer/plots/mincer_niveles.jpg",dpi = 300, facecolor='w', bbox_inches='tight',pad_inches=0.3, transparent=True)
plt.show()

    # Maps
estados_names = ["Aguascalientes",
                 "Baja California",
                 "Baja California Sur",
                 "Campeche",
                 "Coahuila de Zaragoza",
                 "Colima",
                 "Chiapas",
                 "Chihuahua",
                 "Ciudad de México",
                 "Durango",
                 "Guanajuato",
                 "Guerrero",
                 "Hidalgo",
                 "Jalisco",
                 "México",
                 "Michoacán de Ocampo",
                 "Morelos",
                 "Nayarit",
                 "Nuevo León",
                 "Oaxaca",
                 "Puebla",
                 "Querétaro",
                 "Quintana Roo",
                 "San Luis Potosí",
                 "Sinaloa",
                 "Sonora",
                 "Tabasco",
                 "Tamaulipas",
                 "Tlaxcala",
                 "Veracruz de Ignacio de la Llave",
                 "Yucatán",
                 "Zacatecas"]
   
        # Lits of states data frames                       
def bases_estados(ent):
    df = [i[i["ent"] == ent ] for i in datos]
    return df

data_estados = [bases_estados(i) for i in estados_names]

        # Models for each state
def models_estados(num):
    l = [smf.ols('np.log(ing_x_hrs) ~ anios_esc + exp + np.square(exp)', data = i).fit() for i in data_estados[num]]
    return l 

models_estados_MINCER_1 = [models_estados(i) for i in range(0,32)]
    
def models_estados_2(num):
    l = [smf.ols('np.log(ing_x_hrs) ~ C(cs_p13_1) + exp + np.square(exp)', data = i).fit() for i in data_estados[num]]
    return l

models_estados_MINCER_2 = [models_estados_2(i) for i in range(0,32)]

        # Coefficient for each state
def coef_MINCER_1(num_1,num_2):
    c = pd.DataFrame([i[num_1].params[num_2]*100 for i in models_estados_MINCER_1])
    return c

revenue_education_years_estados = pd.concat([coef_MINCER_1(i,1) for i in range(0,16)], axis = 1)
revenue_education_years_estados.columns = years_str
revenue_education_years_estados.index = estados_names

revenue_experience_years_estados = pd.concat([coef_MINCER_1(i,2) for i in range(0,16)], axis = 1)
revenue_experience_years_estados.columns = years_str
revenue_experience_years_estados.index = estados_names


def coef_MINCER_2(num_1,num_2):
    c = pd.DataFrame([i[num_1].params[num_2]*100 for i in models_estados_MINCER_2])
    return  c    

        # Pro coefficients for each state
revenue_levels_years_estados_pro = pd.concat([coef_MINCER_2(i,4) for i in range(0,16)], axis = 1)
revenue_levels_years_estados_pro.columns = years_str
revenue_levels_years_estados_pro.index = estados_names

        # Mas coefficients for each state
revenue_levels_years_estados_mas = pd.concat([coef_MINCER_2(i,5) for i in range(0,16)], axis = 1)
revenue_levels_years_estados_mas.columns = years_str
revenue_levels_years_estados_mas.index = estados_names

        # Doc coefficients for each state
revenue_levels_years_estados_doc = pd.concat([coef_MINCER_2(i,6) for i in range(0,16)], axis = 1)
revenue_levels_years_estados_doc.columns = years_str
revenue_levels_years_estados_doc.index = estados_names

        # Maps gif years education
minimo = revenue_education_years_estados.to_numpy().min()
maximo = revenue_education_years_estados.to_numpy().max()

def coef_year_state(año,name):
    mex = entidades.merge(revenue_education_years_estados[año], left_on = 'NOMGEO', right_index = True, how = 'left')
    mapa =  mex.plot(column = año,
                           vmin = minimo, vmax = maximo,
                           legend = True,
                           cmap = 'YlOrBr',
                           legend_kwds = {'orientation' : 'horizontal',
                                          'label':"% año de educación adicional"})
    plt.title("Rendimientos privados de la educación en México: " + año)
    plt.axis('off')
    plt.savefig(name, dpi = 300, bbox_inches='tight')
    return mapa

nam_est_yea = ["/home/ja/Documentos/income_edu_figures/mincer/maps/años/edu_est_year_1.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/años/edu_est_year_2.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/años/edu_est_year_3.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/años/edu_est_year_4.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/años/edu_est_year_5.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/años/edu_est_year_6.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/años/edu_est_year_7.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/años/edu_est_year_8.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/años/edu_est_year_9.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/años/edu_est_year_10.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/años/edu_est_year_11.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/años/edu_est_year_12.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/años/edu_est_year_13.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/años/edu_est_year_14.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/años/edu_est_year_15.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/años/edu_est_year_16.jpg"]

for i,j in zip(revenue_education_years_estados,nam_est_yea):
    coef_year_state(i,j)

def make_gif(frame_folder):
    frames = [Image.open(image) for image in nam_est_yea]
    frame_one = frames[0]
    frame_one.save("/home/ja/Documentos/income_edu_figures/mincer/maps/años/edu_est_years.gif", format="GIF", append_images=frames,
               save_all=True, duration=500, loop=0)
    
if __name__ == "__main__":
    make_gif("/home/ja/Documentos/income_edu_figures/mincer/maps/años/")

        # Maps gif experience 
minimo = revenue_experience_years_estados.to_numpy().min()
maximo = revenue_experience_years_estados.to_numpy().max()

def coef_year_state(año,name):
    mex = entidades.merge(revenue_experience_years_estados[año], left_on = 'NOMGEO', right_index = True, how = 'left')
    mapa =  mex.plot(column = año,
                           vmin = minimo, vmax = maximo,
                           legend = True,
                           cmap = 'BuPu',
                           legend_kwds = {'orientation' : 'horizontal',
                                          'label':"% año de experiencia adicional"})
    plt.title("Rendimientos privados de la experiencia en México: " + año)
    plt.axis('off')
    plt.savefig(name, dpi = 300, bbox_inches='tight')
    return mapa

nam_est_exp = ["/home/ja/Documentos/income_edu_figures/mincer/maps/experiencia/exp_est_year_1.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/experiencia/exp_est_year_2.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/experiencia/exp_est_year_3.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/experiencia/exp_est_year_4.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/experiencia/exp_est_year_5.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/experiencia/exp_est_year_6.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/experiencia/exp_est_year_7.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/experiencia/exp_est_year_8.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/experiencia/exp_est_year_9.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/experiencia/exp_est_year_10.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/experiencia/exp_est_year_11.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/experiencia/exp_est_year_12.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/experiencia/exp_est_year_13.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/experiencia/exp_est_year_14.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/experiencia/exp_est_year_15.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/experiencia/exp_est_year_16.jpg"]

for i,j in zip(revenue_experience_years_estados,nam_est_exp):
    coef_year_state(i,j)

def make_gif(frame_folder):
    frames = [Image.open(image) for image in nam_est_exp]
    frame_one = frames[0]
    frame_one.save("/home/ja/Documentos/income_edu_figures/mincer/maps/experiencia/exp_est_years.gif", format="GIF", append_images=frames,
               save_all=True, duration=500, loop=0)
    
if __name__ == "__main__":
    make_gif("/home/ja/Documentos/income_edu_figures/mincer/maps/experiencia/")
    
        # Maps gif profesional
minimo = revenue_levels_years_estados_pro.to_numpy().min()
maximo = revenue_levels_years_estados_pro.to_numpy().max()

def coef_year_state(año,name):
    mex = entidades.merge(revenue_levels_years_estados_pro[año], left_on = 'NOMGEO', right_index = True, how = 'left')
    mapa =  mex.plot(column = año,
                           vmin = minimo, vmax = maximo,
                           legend = True,
                           cmap = 'YlGn',
                           legend_kwds = {'orientation' : 'horizontal',
                                          'label':"% nivel profesional respecto a ninguna eucación"})
    plt.title("Rendimientos de la educación profesional en México: " + año)
    plt.axis('off')
    plt.savefig(name, dpi = 300, bbox_inches='tight')
    return mapa

nam_est_pro = ["/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/profesional/pro_est_year_1.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/profesional/pro_est_year_2.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/profesional/pro_est_year_3.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/profesional/pro_est_year_4.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/profesional/pro_est_year_5.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/profesional/pro_est_year_6.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/profesional/pro_est_year_7.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/profesional/pro_est_year_8.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/profesional/pro_est_year_9.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/profesional/pro_est_year_10.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/profesional/pro_est_year_11.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/profesional/pro_est_year_12.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/profesional/pro_est_year_13.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/profesional/pro_est_year_14.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/profesional/pro_est_year_15.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/profesional/pro_est_year_16.jpg"]

for i,j in zip(revenue_levels_years_estados_pro,nam_est_pro):
    coef_year_state(i,j)

def make_gif(frame_folder):
    frames = [Image.open(image) for image in nam_est_pro]
    frame_one = frames[0]
    frame_one.save("/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/profesional/pro_est_years.gif", format="GIF", append_images=frames,
               save_all=True, duration=500, loop=0)
    
if __name__ == "__main__":
    make_gif("/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/profesional/")

        # Maps gif master
minimo = revenue_levels_years_estados_mas.to_numpy().min()
maximo = revenue_levels_years_estados_mas.to_numpy().max()

def coef_year_state(año,name):
    mex = entidades.merge(revenue_levels_years_estados_mas[año], left_on = 'NOMGEO', right_index = True, how = 'left')
    mapa =  mex.plot(column = año,
                           vmin = minimo, vmax = maximo,
                           legend = True,
                           cmap = 'Reds',
                           legend_kwds = {'orientation' : 'horizontal',
                                          'label':"% nivel maestría respecto a ninguna eucación"})
    plt.title("Rendimientos de una maestría en México: " + año)
    plt.axis('off')
    plt.savefig(name, dpi = 300, bbox_inches='tight')
    return mapa

nam_est_mas = ["/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/maestría/mas_est_year_1.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/maestría/mas_est_year_2.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/maestría/mas_est_year_3.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/maestría/mas_est_year_4.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/maestría/mas_est_year_5.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/maestría/mas_est_year_6.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/maestría/mas_est_year_7.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/maestría/mas_est_year_8.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/maestría/mas_est_year_9.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/maestría/mas_est_year_10.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/maestría/mas_est_year_11.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/maestría/mas_est_year_12.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/maestría/mas_est_year_13.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/maestría/mas_est_year_14.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/maestría/mas_est_year_15.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/maestría/mas_est_year_16.jpg"]

for i,j in zip(revenue_levels_years_estados_mas,nam_est_mas):
    coef_year_state(i,j)

def make_gif(frame_folder):
    frames = [Image.open(image) for image in nam_est_mas]
    frame_one = frames[0]
    frame_one.save("/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/maestría/mas_est_years.gif", format="GIF", append_images=frames,
               save_all=True, duration=500, loop=0)
    
if __name__ == "__main__":
    make_gif("/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/maestría/")
    
        # Maps gif doc
minimo = revenue_levels_years_estados_doc.to_numpy().min()
maximo = revenue_levels_years_estados_doc.to_numpy().max()

def coef_year_state(año,name):
    mex = entidades.merge(revenue_levels_years_estados_doc[año], left_on = 'NOMGEO', right_index = True, how = 'left')
    mapa =  mex.plot(column = año,
                           vmin = minimo, vmax = maximo,
                           legend = True,
                           cmap = 'Blues',
                           legend_kwds = {'orientation' : 'horizontal',
                                          'label':"% nivel doctorado respecto a ninguna eucación"})
    plt.title("Rendimientos de un doctorado en México: " + año)
    plt.axis('off')
    plt.savefig(name, dpi = 300, bbox_inches='tight')
    return mapa

nam_est_doc = ["/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/doctorado/doc_est_year_1.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/doctorado/doc_est_year_2.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/doctorado/doc_est_year_3.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/doctorado/doc_est_year_4.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/doctorado/doc_est_year_5.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/doctorado/doc_est_year_6.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/doctorado/doc_est_year_7.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/doctorado/doc_est_year_8.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/doctorado/doc_est_year_9.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/doctorado/doc_est_year_10.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/doctorado/doc_est_year_11.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/doctorado/doc_est_year_12.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/doctorado/doc_est_year_13.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/doctorado/doc_est_year_14.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/doctorado/doc_est_year_15.jpg",
               "/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/doctorado/doc_est_year_16.jpg"]

for i,j in zip(revenue_levels_years_estados_doc,nam_est_doc):
    coef_year_state(i,j)

def make_gif(frame_folder):
    frames = [Image.open(image) for image in nam_est_mas]
    frame_one = frames[0]
    frame_one.save("/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/doctorado/doc_est_years.gif", format="GIF", append_images=frames,
               save_all=True, duration=500, loop=0)
    
if __name__ == "__main__":
    make_gif("/home/ja/Documentos/income_edu_figures/mincer/maps/niveles/doctorado/")
