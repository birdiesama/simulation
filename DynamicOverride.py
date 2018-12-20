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
 
        def selection ( self ) :
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
        
    def printValue_cmd ( self , *args ) :
        
        ff = self.FloatField ( lengthFlex_min_floatField )
 
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

                    self.hairSystem_tsl = pm.textScrollList ( w = w , h = 100 ,
                        ams = True ) ;

                ### Attribute Input
               
                # Dynamic Override , Collide
                pm.separator ( vis = False , h = 15 ) ;
                
                with pm.rowColumnLayout ( nc = 2 , cw = [ ( 1 , w/2 ) , ( 2 , w/2 ) ] ) :
                    pm.checkBox ( label = 'Dynamic Override' , w = w/2 , value = True ) ;
                    pm.checkBox ( label = 'Collide' , w = w/2 , value = True ) ;
                    
                # Common Attributes
                pm.separator ( vis = False , h = 15 ) ;

                def insertAttr ( list ) :
                

                with pm.rowColumnLayout ( nc = 4 , cw = [ ( 1 , w/6 ) , ( 2 , w/6 ) , ( 3 , w/3 ) , ( 4 , w/3 ) ] ) :

                    pm.text ( label = 'Attr' , w = w/6  ) ;
                    pm.text ( label = '(Default Val)' , w = w/6 ) ;
                    pm.text ( label = 'Min Value' ) ;
                    pm.text ( label = 'Max Value' ) ;
                    
                    compAttr_list = [] ;
                    compAttr_list.append ( [ 'lengthFlex' , 0.1 , [ 0.0 , 0.0 ] ] ) ;
                    compAttr_list.append ( [ 'damp' , 0.1 , [ 0.0 , 0.0 ] ] ) ;
                    compAttr_list.append ( [ 'stiffness' , 0.1 , [ 0.0 , 0.0 ] ] ) ;
                    
                    
                    for compAttr in compAttr_list :
                    
                        attr = compAttr[0] ;
                        niceName = self.composeNiceName ( attr ) ;
                        defaultValue = compAttr[1] ;
                        min = compAttr[2][0] ;
                        max = compAttr[2][1] ;
                        
                        cmd = """                        
pm.text ( label = '{niceName}' , w = w/6 ) ;
self.{attr}_defaultValue_floatField = pm.floatField ( precision = 3 , v = {defaultValue} , enable = False ) ;
self.{attr}_min_floatField = pm.floatField ( precision = 3 , v = {min} ) ;
self.{attr}_max_floatField = pm.floatField ( precision = 3 , v = {max} ) ;
""".format ( attr = attr , niceName = niceName , defaultValue = defaultValue , min = min , max = max ) ;

                        exec ( cmd ) ;

                    '''
                    pm.text ( label = 'Length Flex' , w = w/6 ) ;
                    pm.text ( label = '(0.1)' , w = w/6 ) ;
                    self.lengthFlex_min_floatField = pm.floatField ( precision = 2 ) ;
                    self.lengthFlex_max_floatField = pm.floatField ( precision = 2 ) ;
                    '''
                    
                # set, and reset to dynamic override default values
                with pm.rowColumnLayout ( nc = 2 , cw = [ ( 1 , w/2 ) , ( 2 , w/2 ) ] ) :

                    pm.button ( label = 'Set' , w = w/2 , bgc = ( 1 , 1 , 1 ) ) ;
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
