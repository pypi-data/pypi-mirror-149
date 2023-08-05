"""

"""

__version__='90.12.4.0.dev1'

import warnings
warnings.filterwarnings("ignore")

import sys
import logging

import pandas as pd
import geopandas

import matplotlib.pyplot as plt
import matplotlib
from matplotlib import cm

import contextily as cx

logger = logging.getLogger('PT3S')  
if __name__ == "__main__":
    logger.debug("{0:s}{1:s}".format('in MODULEFILE: __main__ Context:','.')) 
else:
    logger.debug("{0:s}{1:s}{2:s}{3:s}".format('in MODULEFILE: Not __main__ Context: ','__name__: ',__name__," ."))

class NFDError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class NFD():

    """
    Raises:
        NFDError
    """

    def __init__(self):
        self.name = 'NFD'

    def plotNFD(gdf_FWVB
                ,gdf_ROHR
                ,colors_FWVB = ['green', 'red']
                ,colors_ROHR = ['lightgray', 'dimgray']
                ,norm_min_FWVB = 24
                ,norm_max_FWVB = 38
                ,yTicks = None
                ,yTickLabels = None
                ,norm_min_ROHR = 333
                ,norm_max_ROHR = 666
                ,FWVB_edgecolor = 'White'
                ,FWVB_groesse = 0.1
                ,color_FWVB_under = 'green'
                ,color_FWVB_over = 'red'
                ,color_ROHR_under = 'magenta'
                ,color_ROHR_over = 'lime'
                ,Anzeigen_ROHR = True
                ,ROHR_Ampel = False
                ,ROHR_dicke = 0.0025
                ,column_ROHR_Dicke = 'DI'
                ,color_ROHR = 'grey'
                ,LabelsOnTop = True
                ,FWVB_markerscaling_col = 'W0'
                ,FWVB_cmap_col = 'ZKOR_k'
                ,Map_resolution = 12
                ,FWVB_cbar_label = 'default'
                ,cbar_size = 0.7
                ):

        """
        Die Funktion plottet FWVB und wahlweise Rohre mit Hintergrundkarte.
        Groesse und Farbe der FWVB/Rohre koennen an eigen gewaehlte Spalten angepasst werden.

        Args:

            * gdf_FWVB:               DataFrame der FWVB (muss vor dem Ausfuehren dieser Funktion definiert werden)
            * gdf_ROHR:               DataFrame der ROHRE (muss vor dem Ausfuehren dieser Funktion definiert werden)
            * colors_FWVB:            Bsp.: ['green', 'red'] Colormap der FWVB (niedrige Werte beginnen bei linker Farbe(hier 'green'))
            * colors_ROHR:            Bsp.: ['lightgray', 'dimgray'] Colormap der Rohre (niedrige Werte beginnen bei linker Farbe(hier 'dimgray'))
            * norm_min_FWVB:          Unterer Wert der Farbskala fuer FWVB
            * norm_max_FWVB:          Oberer Wert der Farbskala fuer FWVB
            * yTicks:                 Hier koennen die yTicks der Colorbar angegeben werden
            * yTickLabels:            Hier koennen die yTickLabels der Colorbar angegeben werden
            * norm_min_ROHR:          Unterer Wert der Farbskala fuer Rohre
            * norm_max_ROHR:          Oberer Wert der Farbskala fuer Rohre
            * FWVB_edgecolor:         Randfarbe der FWVB
            * FWVB_groesse:           Faktor, der die Groesse der FWVB zusaetzlich skaliert
            * color_FWVB_under:       Farbe der FWVB mit Werten unterhalb der definierten Farbskala
            * color_FWVB_over:        Farbe der FWVB mit Werten ueberhalb der definierten Farbskala
            * color_ROHR_under:       Farbe der Rohre mit Werten unterhalb der definierten Farbskala
            * color_ROHR_over:        Farbe der Rohre mit Werten ueberhalb der definierten Farbskala
            * Anzeigen_ROHR:          Bestimmt, ob Rohre angezeigt werden (True/False)
            * ROHR_Ampel:             Sollen die Rohre eine Farbampel besitzen (True/False)
            * ROHR_dicke:             Faktor, der die Dicke der Rohre zusaetzlich skaliert
            * column_ROHR_Dicke:      Spalte, welche die Dicke der Rohre definiert
            * color_ROHR:             Farbe der Rohre (falls nicht in Ampeldarstellung)
            * LabelsOnTop:            Sollen die Labels ueber dem geplotteten angezeigt werden (True/False)
            * FWVB_markerscaling_col: Gibt die Spalte der FWVB an, mit der die Marker (markersize, linewidth, alpha) skaliert werden sollen
            * FWVB_cmap_col:          Gibt die Spalte der FWVB an, mit der diese in die Colormap eingeordnet werden
            * Map_resolution:         0-20 Aufloesung der Hintergrundkarte (Je hoeher das Zommlevel, desto hoeher die Aufloesung)
            * FWVB_cbar_label:        Titel der Colorbar fuer die direkten FWVB
            * cbar_size:              Faktor mit dem die groesse der Colorbar skaliert wird
        """

        logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.'))


        fig = plt.gcf()
        ax = plt.gca()

        norm_FWVB_color = plt.Normalize(vmin=norm_min_FWVB, vmax=norm_max_FWVB)

        norm_ROHR = plt.Normalize(vmin=norm_min_ROHR, vmax=norm_max_ROHR)

        cmap_FWVB = matplotlib.colors.LinearSegmentedColormap.from_list('FWVB', colors_FWVB, N = 256) #Erstellen der Colormap fuer die FWVB
        cmap_FWVB.set_under(color_FWVB_under)
        cmap_FWVB.set_over(color_FWVB_over)

        cmap_ROHR = matplotlib.colors.LinearSegmentedColormap.from_list('ROHR', colors_ROHR, N = 256) #Erstellen der Colormap fuer die Rohre
        cmap_ROHR.set_under(color_ROHR_under)
        cmap_ROHR.set_over(color_ROHR_over)

        norm_FWVB_size = plt.Normalize(vmin = gdf_FWVB[FWVB_markerscaling_col].min(), vmax = gdf_FWVB[FWVB_markerscaling_col].max()) #Festlegen wie diese Spalte normiert werden soll

        try:
            gdf_FWVB.plot(ax = ax
                        ,marker = '.'
                        ,markersize = gdf_FWVB[FWVB_markerscaling_col] * FWVB_groesse #Markersize ist abhaengig von der zum Markerscaling ausgewaehlten Spalte und einem Faktor
                        ,c = cmap_FWVB(norm_FWVB_color(gdf_FWVB[FWVB_cmap_col])) #Einfaerben der Marker entsprechend der definierten Colormap und ausgewaehlten Spalte
                        ,edgecolor = FWVB_edgecolor #FWVB Randfarbe des Markers
                        ,linewidth = norm_FWVB_size(gdf_FWVB[FWVB_markerscaling_col]) / 2 #FWVB Randdicke, abhaengig von der zum Markerscaling ausgewaehlten Spalte. Die Randdicke wird im Anschluss nochmal durch 2 geteilt.
                        ,alpha =  0.9 - (norm_FWVB_size(gdf_FWVB[FWVB_markerscaling_col]) / 2) #FWVB Durchsichtigkeit, abhaengig von der zum Markerscaling ausgewaehlten Spalte. Mit dem Teilen durch 2 ist die maximale Durchsichtigkeit bei 0.5 (0 bei Kleinen-0.5 bei Grossen). Um dies umzudrehen zieht man von 1 ab. Hier wird von 0.9 abgezogen. Damit sind kleinsten FWVB immer noch leicht durchsichtig und die Groessten trotzdem noch erkennbar (0.9 bei Kleinen - 0.4 bei Grossen) 
                        ,zorder = 2) #Reihenfolge zu den anderen geploteten Objekten (je hoeher die Zahl, desto hoeher die geplottete Ebene; Hoehe im Sinne von Vorder- und Hintergrund)

            if Anzeigen_ROHR:

                if ROHR_Ampel:
                    gdf_ROHR.plot(ax = ax
                                    ,zorder = 1
                                    ,linewidth = gdf_ROHR[column_ROHR_Dicke] * ROHR_dicke
                                    ,c = cmap_ROHR(norm_ROHR(gdf_ROHR[column_ROHR_Dicke])))

                else:    
                    gdf_ROHR.plot(ax = ax
                                    ,zorder = 1
                                    ,linewidth = gdf_ROHR[column_ROHR_Dicke] * ROHR_dicke
                                    ,color = color_ROHR)

            if LabelsOnTop:
                cx.add_basemap(ax, crs=gdf_FWVB.crs.to_string(), source = cx.providers.CartoDB.PositronNoLabels, zoom = Map_resolution)
                cx.add_basemap(ax, crs=gdf_FWVB.crs.to_string(), source = cx.providers.CartoDB.PositronOnlyLabels, zoom = Map_resolution)
            else:
                cx.add_basemap(ax, crs=gdf_FWVB.crs.to_string(), source = cx.providers.CartoDB.Positron, zoom = Map_resolution)


            cbar=fig.colorbar(cm.ScalarMappable(norm = norm_FWVB_color, cmap = cmap_FWVB)
                        ,ax = ax
                        ,label = FWVB_cbar_label
                        ,shrink = cbar_size
                        ,ticks=yTicks
                        ,pad = 0.01)
            if yTickLabels != None:
                cbar.ax.set_yticklabels(yTickLabels)

            plt.axis('off')

        except NFDError:
            raise            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise NFDError(logStrFinal)                       
        finally:       
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))
            return