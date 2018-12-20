import pymel.core as pm ;
import re ;

class NHairDynOvr ( object ) :
     
    def __init__ ( self , *args , **kwargs ) :
        super ( NHairDynOvr , self ).__init__() ;
         
    def queryElem ( self , target ) :
        # return list ( fol , crv ) 
 
        target = pm.PyNode ( target ) ;
 
        fol_list    = [] ;
 
        for folTfm in target.getShape().listConnections ( type = 'follicle' ) :
            fol_list.append ( folTfm.getShape() ) ;
 
        crv_list    = [] ;
 
        for fol in fol_list :
            attr_list = fol.listConnections ( type = 'nurbsCurve' , plugs = True ) ;
 
            for attr in attr_list :
                if attr.attrName( longName = True ) == 'create' :
                    crv  = attr.nodeName() ;
                    crv  = pm.PyNode ( crv ) ;
                    crv_list.append ( crv ) ;
 
        return zip ( fol_list , crv_list ) ;

class General ( object ) :

    def __init__ ( self ) :
        super ( General , self ).__init__() ;

    def composeNiceName ( self , input ) :

        name_regex = re.compile ( r'^[a-z]*|[A-Z][^A-Z]*' ) ;
        name_mo_list = name_regex.findall ( input ) ; 
        
        niceName = '' ;
        
        for name in name_mo_list :
            niceName += name.title() ;
            if name != name_mo_list[-1] :
                niceName += ' ' ;
        
        return niceName ;
          
class GuiFunc ( object ) :
 
    def __init__ ( self ) :
        super ( GuiFunc , self ).__init__() ;
 
    class TextScrollList ( object ) :
 
        def __init__ ( self , tsl ) :
            self.tsl = tsl ;
 
        def clear ( self ) :
            pm.textScrollList ( self.tsl , e = True , ra = True ) ;
 
        def appendList ( self , list ) :
            for item in list :
                pm.textScrollList ( self.tsl , e = True , append = item ) ;
 
        def getSelected ( self ) :
            return ( pm.textScrollList ( self.tsl , q = True , si = True ) ) ;
    
    class FloatField ( object ) :
    
        def __init__ ( self , ff ) :
            self.ff = ff ;
        
        def getValue ( self ) :
            return ( pm.floatField ( self.ff , q = True , v = True ) ) ;
 
    def guiInitialize_func ( self ) :
 
        self.guiUpdate_hairSystemTsl_func() ;
 
    def guiUpdate_hairSystemTsl_func ( self ) :
 
        tsl = self.TextScrollList ( self.hairSystem_tsl ) ;
 
        hairSystem_list = pm.ls ( type = 'hairSystem' ) ;
 
        tsl.clear() ;
        tsl.appendList ( hairSystem_list ) ;
    
    def hairSystem_refresh_cmd ( self , *args ) :
        
        self.guiUpdate_hairSystemTsl_func ( ) ;
    
    def getFol ( self , hairSystem ) :
       
        hairSystem = pm.PyNode ( hairSystem ) ;
        
        folTfm_list = hairSystem.listConnections ( type = 'follicle' ) ;
        fol_list = [] ;
        
        for folTfm in folTfm_list :
            fol_list.append ( folTfm.getShape() ) ;
        
        return fol_list ;
    
    ### Enable / Disable [ Dynamic Override / Collide ] ###
     
    def enableFollicleAttr_func ( self , hairSystem , attr , value ) :
        
        hairSystem = pm.PyNode ( hairSystem ) ;
        
        fol_list = self.getFol ( hairSystem ) ;
        
        for fol in fol_list :
            
            exec ( "fol.{attr}.set({value}) ;".format ( attr = attr , value = value ) ) ;
            
    def enableDynamicOverride_cmd ( self , *args ) :
        
        tsl = self.TextScrollList ( self.hairSystem_tsl ) ;
        hairSystem_list = tsl.getSelected() ;
        
        for hairSystem in hairSystem_list :
            self.enableFollicleAttr_func ( hairSystem = hairSystem , attr = 'overrideDynamics' , value = 1 ) ;
    
    def disableDynamicOverride_cmd ( self , *args ) :
        
        tsl = self.TextScrollList ( self.hairSystem_tsl ) ;
        hairSystem_list = tsl.getSelected() ;
        
        for hairSystem in hairSystem_list :
            self.enableFollicleAttr_func ( hairSystem = hairSystem , attr = 'overrideDynamics' , value = 0 ) ;
    
    def enableCollide_cmd ( self , *args ) :
        
        tsl = self.TextScrollList ( self.hairSystem_tsl ) ;
        hairSystem_list = tsl.getSelected() ;
        
        for hairSystem in hairSystem_list :
            self.enableFollicleAttr_func ( hairSystem = hairSystem , attr = 'collide' , value = 1 ) ;
    
    def disableCollide_cmd ( self , *args ) :
        
        tsl = self.TextScrollList ( self.hairSystem_tsl ) ;
        hairSystem_list = tsl.getSelected() ;
        
        for hairSystem in hairSystem_list :
            self.enableFollicleAttr_func ( hairSystem = hairSystem , attr = 'collide' , value = 0 ) ;
    
    def getArcLen ( self , hairSystem ) :
        
        hairSystem = pm.PyNode ( hairSystem ) ;
           
    def set_cmd ( self , *args ) :
        
        tsl = self.TextScrollList ( self.hairSystem_tsl ) ;
        
        hairSystem_list = tsl.getSelected() ;
        
        for hairSystem in hairSystem_list :
            
            hairSystem = pm.PyNode ( hairSystem ) ;
            
            print self.getFol ( hairSystem ) ;
            
class Gui ( object ) :
 
    def __init__ ( self ) :
        super ( Gui , self ).__init__() ;
 
        self.ui         = 'nHairDynOvr_ui' ;
        self.width      = 450.00 ;
        self.title      = 'nHair Dyn Override' ;
        self.version    = 1.0 ;
 
    def __str__ ( self ) :
        return self.ui ;
 
    def __repr__ ( self ) :
        return self.ui ;
 
    # requestioning
    def checkUniqueness ( self , ui ) :
        if pm.window ( ui , exists = True ) :
            pm.deleteUI ( ui ) ;
            self.checkUniqueness ( ui ) ;
    
    ### specific gui func ###
    
    def insertAttr ( self , list ) :
        
        w = self.width ;
        
        attr = list[0] ;
        niceName = self.composeNiceName ( attr ) ;
        defaultValue = list[1] ;
        min = list[2][0] ;
        max = list[2][1] ;

        cmd = """                        
pm.text ( label = '{niceName}' , w = w/6 ) ;
self.{attr}_defaultValue_floatField = pm.floatField ( precision = 3 , v = {defaultValue} , enable = False , w = w/6 ) ;
self.{attr}_min_floatField = pm.floatField ( precision = 3 , v = {min} , w = w/3 ) ;
self.{attr}_max_floatField = pm.floatField ( precision = 3 , v = {max} , w = w/3 ) ;
""".format ( attr = attr , niceName = niceName , defaultValue = defaultValue , min = min , max = max ) ;

        exec ( cmd ) ;

    def showGui ( self ) :
 
        w = self.width ;
 
        # check ui duplication
        self.checkUniqueness ( self.ui ) ;
 
        window = pm.window ( self.ui , 
            title       = '{title} v{version}'.format ( title = self.title , version = self.version ) ,
            mnb         = True  , # minimize button
            mxb         = False , # maximize button 
            sizeable    = True  ,
            rtf         = True  , # resizeToFitChildren
            ) ;
 
        # edit the window, so that the window size is refreshed every time it is called
        pm.window ( window , e = True , w = w , h = 10.00 ) ;
        with window :
            
            # main layout
            with pm.rowColumnLayout ( nc = 1 , w = w ) :
            
                # hairSystem text scroll list
                with pm.rowColumnLayout ( nc = 1 , w = w ) :

                    with pm.rowColumnLayout ( nc = 2 , cw = [ ( 1 , w/2 ) , ( 2 , w/2 ) ] ) :
                        pm.text ( label = 'Hair System(s) :' , w = w/2 ) ;
                        self.hairSystem_refresh_btn = pm.button ( label = 'Refresh' ,
                            c = self.hairSystem_refresh_cmd ) ;

                    self.hairSystem_tsl = pm.textScrollList ( w = w , h = 100 , ams = True ) ;
                    
                # Dynamic Override , Collide
                
                lw = w/2 ; # local width
                cw = [ ( 1 , lw ) , ( 2 , lw ) ] ;
                with pm.rowColumnLayout ( nc = 2 , cw = cw ) :
                        
                    pm.button ( label = 'Enable Dynamic Override' , w = lw , c = self.enableDynamicOverride_cmd ) ;
                    pm.button ( label = 'Disable Dynamic Override' , w = lw , c = self.disableDynamicOverride_cmd ) ;
                    
                    pm.button ( label = 'Enable Collide' , w = lw , c = self.enableCollide_cmd ) ;
                    pm.button ( label = 'Disable Collide' , w = lw , c = self.disableCollide_cmd ) ;
                
                ### Attribute Input
               
                # Common Attributes        
                pm.separator ( vis = False , h = 15 ) ;
               
                cw = [ ( 1 , w/4 ) , ( 2 , w/4 ) , ( 3 , w/4 ) , ( 4 , w/4 ) ] ;
                with pm.rowColumnLayout ( nc = 4 , cw = cw ) :

                    pm.text ( label = 'Attr' , w = w/6  ) ;
                    pm.text ( label = '(Default Val)' , w = w/6 ) ;
                    pm.text ( label = 'Shortest Crv Value' ) ;
                    pm.text ( label = 'Longest Crv Value' ) ;
                    
                compAttr_list = [] ;
                # name , default value , [ min , max ]
                compAttr_list.append ( [ 'lengthFlex' , 0.1 , [ 0.0 , 0.0 ] ] ) ;
                compAttr_list.append ( [ 'damp' , 0.1 , [ 0.0 , 0.0 ] ] ) ;
                compAttr_list.append ( [ 'stiffness' , 0.1 , [ 0.0 , 0.0 ] ] ) ;
                
                cw = [ ( 1 , w/4 ) , ( 2 , w/4 ) , ( 3 , w/4 ) , ( 4 , w/4 ) ] ;
                with pm.rowColumnLayout ( nc = 4 , cw = cw ) :
                    
                    for compAttr in compAttr_list :    
                        self.insertAttr ( compAttr ) ;
                
                # change to frame layout here
                pm.separator ( vis = False , h = 15 ) ;
                
                pm.text ( label = 'Stiffness Scale' , align = 'left' ) ;
                pm.separator () ;
                    
                with pm.rowColumnLayout ( nc = 1 , w = w ) :
                    
                    with pm.rowColumnLayout ( nc = 2 , cw = [ ( 1 , w/2 ) , ( 2 , w/2 ) ] ) :
                        pm.text ( label = '' ) ;
                        pm.checkBox ( label = 'Copy Graph from Hair System' , v = True , w = w/2 ) ;
                    
                    compAttr_list = [] ;
                    compAttr_list.append ( [ 'clumpWidth' , 0.1 , [ 0.0 , 0.0 ] ] ) ;
                    
                    with pm.rowColumnLayout ( nc = 4 , cw = [ ( 1 , w/4 ) , ( 2 , w/4 ) , ( 3 , w/4 ) , ( 4 , w/4 ) ] ) :
                    
                        for compAttr in compAttr_list :
                            self.insertAttr ( compAttr ) ;
                    
                # change to frame layout here
                pm.separator ( vis = False , h = 15 ) ;
                
                pm.text ( label = 'Clump Width Scale' , align = 'left' ) ;
                pm.separator () ;
                
                with pm.rowColumnLayout ( nc = 1 , w = w ) :

                    with pm.rowColumnLayout ( nc = 2 , cw = [ ( 1 , w/2 ) , ( 2 , w/2 ) ] ) :
                        pm.text ( label = '' ) ;
                        pm.checkBox ( label = 'Copy Graph from Hair System' , v = True , w = w/2 ) ;
                    
                # change to frame layout here
                
                pm.separator ( vis = False , h = 15 ) ;
                
                pm.text ( label = 'Attraction Scale' , align = 'left' ) ;
                pm.separator () ;
                
                with pm.rowColumnLayout ( nc = 1 , w = w ) :
                    
                    with pm.rowColumnLayout ( nc = 2 , cw = [ ( 1 , w/2 ) , ( 2 , w/2 ) ] ) :
                        pm.text ( label = '' ) ;
                        pm.checkBox ( label = 'Copy Graph from Hair System' , v = True , w = w/2 ) ;
                    
                    compAttr_list = [] ;
                    compAttr_list.append ( [ 'startCurveAttract' , 0.1 , [ 0.0 , 0.0 ] ] ) ;
                    compAttr_list.append ( [ 'attractionDamp' , 0.1 , [ 0.0 , 0.0 ] ] ) ;
                    
                    with pm.rowColumnLayout ( nc = 4 , cw = [ ( 1 , w/4 ) , ( 2 , w/4 ) , ( 3 , w/4 ) , ( 4 , w/4 ) ] ) :
                        
                        for compAttr in compAttr_list :
                            self.insertAttr ( compAttr ) ;
                
                pm.separator ( vis = False , h = 15 ) ;
                
                # set, and reset to dynamic override default values
                with pm.rowColumnLayout ( nc = 2 , cw = [ ( 1 , w/2 ) , ( 2 , w/2 ) ] ) :

                    pm.button ( label = 'Set' , w = w/2 , bgc = ( 1 , 1 , 1 ) , c = self.set_cmd ) ;
                    pm.button ( label = 'Reset to Default Values' , w = w/2 ) ;
 
        window.show () ;
 
        self.guiInitialize_func() ;
 
class Main ( NHairDynOvr , Gui , GuiFunc , General ) :
     
    def __init__ ( self ) :
        super ( Main , self ).__init__() ;
         
    def run ( self , *args ) :
        self.showGui() ;
 
def run ( *args ) :
    main = Main() ;
    main.run() ;
 
run () ;

# make some follicle stiff by selecting curves
