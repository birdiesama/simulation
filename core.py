import pymel.core as pm ;
import maya.cmds as mc ;
import os , ast , re ;

pm.cycleCheck ( e = 0 ) ;

currentProj = pm.workspace ( q = True , rootDirectory = True ) ;

######################################################################################################################################################################################################
######################################################################################################################################################################################################
######################################################################################################################################################################################################
''' cache out '''
######################################################################################################################################################################################################
######################################################################################################################################################################################################
######################################################################################################################################################################################################

## cache out ##
#doCreateGeometryCache 6 { "2", "1", "10", "OneFile", "1", "D:/TwoHeroes/film001/q0310/s0060/hanumanCasual/cache/DYN","0","Pants_DYN_v001_001","0", "export", "0", "1", "1","0","1","mcx","1" } ;
#// Result: D:/TwoHeroes/film001/q0310/s0060/hanumanCasual/cache/DYN//Pants_DYN_v001_001.xml // 

def run ( *args ) :

    from sim.sim_simUtilities import core_nucleus ;
    reload ( core_nucleus ) ;            
    nucleusUtil_GUI = core_nucleus.NucleusUtil_GUI() ;

    from sim.sim_simUtilities import core_cycleCheck ;
    reload ( core_cycleCheck ) ;
    cycleCheckUtil_GUI = core_cycleCheck.CycleCheckUtil_GUI() ;

    from sim.sim_simUtilities import core_nObjects ;
    reload ( core_nObjects ) ;
    nObjectsUtil_GUI = core_nObjects.NObjectUtil_GUI() ;

    from sim.sim_simUtilities import core_timeRange ;
    reload ( core_timeRange ) ;
    timeRange_GUI = core_timeRange.TimeRange_GUI() ;

    from sim.sim_simUtilities import core_sim ;
    reload ( core_sim ) ;
    sim_GUI = core_sim.Sim_GUI() ;

    from sim.sim_simUtilities import core_playblast ;
    reload ( core_playblast ) ;
    playblast_GUI = core_playblast.Playblast_GUI() ;

    from sim.sim_simUtilities import core_import ;
    reload ( core_import ) ;
    import_GUI = core_import.Import_GUI() ;

    from sim.sim_simUtilities import core_export ;
    reload ( core_export ) ;
    export_GUI = core_export.Export_GUI() ;

    ################################################################

    width = 300.00 ;

    if pm.window ( 'simUtilities' , exists = True ) :
        pm.deleteUI ( 'simUtilities' ) ;
    else : pass ;

    window = pm.window ( 'simUtilities', title = "Simulation Utilities" , w = width , 
        mnb = True , mxb = False , sizeable = True , rtf = True ) ;

    pm.window ( 'simUtilities', e = True , w = width , h = 10 ) ;
    
    with window :
    
        mainLayout = pm.rowColumnLayout ( w = width , nc = 1 , columnWidth = [ ( 1 , width ) ] ) ;
        with mainLayout :

            # Nucleus GUI            
            nucleusUtil_GUI.insert ( width = width ) ;
            pm.separator ( vis = 0 ) ;

            # Cycle Check GUI
            cycleCheckUtil_GUI.insert ( width = width ) ;
            pm.separator ( vis = 0 ) ;

            # nObjects GUI 
            nObjectsUtil_GUI.insert ( width = width ) ;
            pm.separator ( vis = True , h = 10 ) ;

            # timeRange GUI
            timeRange_GUI.insert ( width = width ) ;
            
            pm.separator ( vis = True , h = 10 ) ;
            
            tab_layout = pm.tabLayout ( ) ;
            with tab_layout :

                sim_layout = pm.rowColumnLayout ( 'Simulation' , w = width  , nc = 1 ) ;
                with sim_layout :
                    pm.separator ( h = 5 , vis = False ) ;
                    
                    # sim GUI
                    sim_GUI.insert ( width = width ) ;
                    pm.separator ( h = 10 ) ;

                    # playblast GUI
                    playblast_layout = pm.rowColumnLayout ( 'Playblast' , w = width , nc = 1 ) ;
                    with playblast_layout : 
                        playblast_GUI.insert ( width = width ) ;                        

                import_layout = pm.rowColumnLayout ( 'Import' , w = width , nc = 1 ) ;
                with import_layout :
                    pm.separator ( h = 5 , vis = False ) ;

                    # import GUI                    
                    import_GUI.insert( width = width ) ;
                            
                with pm.rowColumnLayout ( 'Export' , w = width , nc = 1 , columnWidth = [ ( 1 , width ) ] ) :
                    export_GUI.insert ( width = width ) ;


    timeRange_GUI.connectSimGUI ( sim_GUI ) ;
    timeRange_GUI.connectPlayblastGUI ( playblast_GUI ) ;
    timeRange_GUI.connectExportGUI ( export_GUI ) ;
    timeRange_GUI.initializeTimeRange ( ) ;
    timeRange_GUI.updateSetTimeRangeBtnClr ( ) ;

    sim_GUI.connectPlayblastGUI ( playblast_GUI ) ;

    window.show ( ) ;

def toShelf ( *args ) :

    import os ;

    self_path = os.path.realpath (__file__) ;
    file_name = os.path.basename (__file__) ;
    self_path = self_path.replace ( file_name , '' ) ;
    self_path = self_path.replace ( '\\' , '/' ) ;

    if self_path[-1] != '/' :
        self_path += '/' ;

    # self_path = D:/Dropbox/script/birdScript/projects/twoHeroes/

    image_path = self_path + 'media/simUtil_icon.png'

    commandHeader = '''
import sys ;

mp = "%s" ;
if not mp in sys.path :
    sys.path.insert ( 0 , mp ) ;
''' % self_path.split ('/sim/')[0] ;
# D:/Dropbox/script/birdScript

    cmd = commandHeader ;
    cmd += '''
import sim.simUtilities as sut ;
reload ( sut ) ;
sut.simUtilities ( ) ;
'''
    mel_cmd = '''
global string $gShelfTopLevel;
string $shelves = `tabLayout -q -selectTab $gShelfTopLevel`;
'''
    currentShelf = pm.mel.eval ( mel_cmd );
    pm.shelfButton ( style = 'iconOnly' , image = image_path , command = cmd , parent = currentShelf ) ;