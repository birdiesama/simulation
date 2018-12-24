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

class NaturalSort ( object ) :

    def __init__ ( self ) :
        super ( NaturalSort , self ).__init__() ;

    def convertKeyElem ( self , input ) :

        if input.isdigit() :
            return int ( input ) ;
        else :
            return input.lower() ;

    def splitKey ( self , key ) :

        return_list = [] ;

        key = str ( key ) ;

        for elem in re.split ( '([0-9]+)' , key ) :
            return_list.append ( self.convertKeyElem ( elem ) ) ;

        return return_list ;

    def naturalSort ( self , list ) :

        return sorted ( list , key = self.splitKey ) ;

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

        def select ( self , item ) :
            pm.textScrollList ( self.tsl , e = True , si = item ) ;
    
    class FloatField ( object ) :
    
        def __init__ ( self , ff ) :
            self.ff = ff ;
        
        def getValue ( self ) :
            return ( pm.floatField ( self.ff , q = True , v = True ) ) ;
 
    class CheckBox ( object ) :

        def __init__ ( self , cbx ) :
            self.cbx = cbx ;

        def getValue ( self ) :
            return ( pm.checkBox ( self.cbx , q = True , v = True ) ) ;

    def guiInitialize_func ( self ) :
 
        self.guiUpdate_hairSystemTsl_func() ;
 
    def guiUpdate_hairSystemTsl_func ( self ) :
 
        tsl = self.TextScrollList ( self.hairSystem_tsl ) ;
 
        hairSystem_list = pm.ls ( type = 'hairSystem' ) ;
 
        tsl.clear() ;
        tsl.appendList ( hairSystem_list ) ;
        tsl.select ( hairSystem_list[0] ) ;
    
    def hairSystem_refresh_cmd ( self , *args ) :
        
        self.guiUpdate_hairSystemTsl_func ( ) ;
    
    def getFol_func ( self , hairSystem ) :
       
        hairSystem = pm.PyNode ( hairSystem ) ;
        
        folTfm_list = hairSystem.listConnections ( type = 'follicle' ) ;
        fol_list = [] ;
        
        for folTfm in folTfm_list :
            fol_list.append ( folTfm.getShape() ) ;
        
        fol_list = set ( fol_list ) ;
        fol_list = list ( fol_list ) ;

        fol_list = self.naturalSort ( fol_list ) 

        return fol_list ;
    
    ### Enable / Disable [ Dynamic Override / Collide ] ###
     
    def enableFollicleAttr_func ( self , hairSystem , attr , value ) :
        
        hairSystem = pm.PyNode ( hairSystem ) ;
        
        fol_list = self.getFol_func ( hairSystem ) ;
        
        for fol in fol_list :
            
            exec ( "fol.{attr}.set({value}) ;".format ( attr = attr , value = value ) ) ;
            
    def enableDynamicOverride_btn_cmd ( self , *args ) :
        
        tsl = self.TextScrollList ( self.hairSystem_tsl ) ;
        hairSystem_list = tsl.getSelected() ;
        
        for hairSystem in hairSystem_list :
            self.enableFollicleAttr_func ( hairSystem = hairSystem , attr = 'overrideDynamics' , value = 1 ) ;
    
    def disableDynamicOverride_btn_cmd ( self , *args ) :
        
        tsl = self.TextScrollList ( self.hairSystem_tsl ) ;
        hairSystem_list = tsl.getSelected() ;
        
        for hairSystem in hairSystem_list :
            self.enableFollicleAttr_func ( hairSystem = hairSystem , attr = 'overrideDynamics' , value = 0 ) ;
    
    def enableCollide_btn_cmd ( self , *args ) :
        
        tsl = self.TextScrollList ( self.hairSystem_tsl ) ;
        hairSystem_list = tsl.getSelected() ;
        
        for hairSystem in hairSystem_list :
            self.enableFollicleAttr_func ( hairSystem = hairSystem , attr = 'collide' , value = 1 ) ;
    
    def disableCollide_btn_cmd ( self , *args ) :
        
        tsl = self.TextScrollList ( self.hairSystem_tsl ) ;
        hairSystem_list = tsl.getSelected() ;
        
        for hairSystem in hairSystem_list :
            self.enableFollicleAttr_func ( hairSystem = hairSystem , attr = 'collide' , value = 0 ) ;
    
    ### Copy Graph ###

    def graph_getSize_func ( self , node , attribute ) :

        node = pm.PyNode ( node ) ;

        attrSize = pm.getAttr (
            "{node}.{attribute}".format ( node = node , attribute = attribute ) ,
            size = True ) ;

        # get the index list, so that it won't create any unnecessary point
        counter = 0 ;
        index_list = [] ;

        while ( len ( index_list ) != attrSize ) :

            cmd = '''
if node.{attribute}[{counter}].exists() :

    index_list.append ( {counter} ) ;
    '''.format ( attribute = attribute , counter = counter ) ;

            exec ( cmd ) ;

            counter += 1 ;

            # kill the infinity loop
            if counter == 100 :
                break ;

        return index_list ;

    def graph_query_func ( self , node , attribute ) :
        # return attrVal_dict ;
        # attrVal_dict [ index ] = [ floatValue , position , interp ] ; 

        node = pm.PyNode ( node ) ;

        index_list = self.graph_getSize_func ( node = node , attribute = attribute ) ;

        # start the query, 
        attrVal_dict = {} ;

        for index in index_list :

            val_list = [] ;
            attributeSuffix_list = [ '_FloatValue' , '_Position' , '_Interp' ] ;

            for attributeSuffix in attributeSuffix_list :
                val = pm.getAttr (
                    "{node}.{attribute}[{index}].{attribute}{attributeSuffix}".format (
                        node        = node ,
                        attribute   = attribute ,
                        index       = index ,
                        attributeSuffix = attributeSuffix ) ) ;
                val_list.append ( val ) ;

            floatValue , position , interp = val_list ;
            
            attrVal_dict [ index ] = [ floatValue , position , interp ] ; 

        return attrVal_dict ;

    def graph_set_func ( self , node , attribute , attrVal_dict ) :

        node = pm.PyNode ( node ) ;

        # set the value first, regardless of the points
        for index in attrVal_dict.keys() :

            attributeSuffix_list = [ '_FloatValue' , '_Position' , '_Interp' ] ;

            for val , attributeSuffix in zip ( attrVal_dict [ index ] , attributeSuffix_list ) :
                
                pm.setAttr (
                    "{node}.{attribute}[{index}].{attribute}{attributeSuffix}".format (
                        node        = node ,
                        attribute   = attribute ,
                        index       = index ,
                        attributeSuffix = attributeSuffix ) , val ) ;

        # get the index list, if index doesn't exist in the dictionary, remove it
        index_list = self.graph_getSize_func ( node = node , attribute = attribute ) ;

        for index in index_list :

            if index not in attrVal_dict.keys() :
                pm.removeMultiInstance (
                    "{node}.{attribute}[{index}]".format (
                        node        = node ,
                        attribute   = attribute ,
                        index       = index ) ,
                    b = True ) ;

    def graph_copy_func ( self , driver , driven , attribute ) :

        driver = pm.PyNode ( driver ) ;
        driven = pm.PyNode ( driven ) ;

        attrVal_dict = self.graph_query_func ( node = driver , attribute = attribute ) ;
        self.graph_set_func ( node = driven , attribute = attribute , attrVal_dict = attrVal_dict ) ;
    
    ### Set ###

    def getArclen ( self , hairSystem ) :
        # return min/max length
        
        hairSystem = pm.PyNode ( hairSystem ) ;
                        
        arclen_list = [] ;
        
        fol_list = self.getFol_func ( hairSystem ) ;
        
        for fol in fol_list :
            
            crvTfm = fol.listConnections ( type = 'nurbsCurve' ) [0] ;
            
            arclen_list.append ( pm.arclen ( crvTfm.getShape() ) ) ;
                                
        arclen_list.sort() ;
                                
        minlen = arclen_list[0] ;
        maxlen = arclen_list[-1] ;
                                
        return minlen , maxlen ;
    
    def getFolLenDict_func ( self , hairSystem ) :
        
        hairSystem = pm.PyNode ( hairSystem ) ;
        
        arclen_list = [] ;
        folLen_dict = {} ;
        
        fol_list = self.getFol_func ( hairSystem ) ;

        for fol in fol_list :

            crv = fol.listConnections ( type = 'nurbsCurve' ) [0] ;
            crvShape = crv.getShapes() ;

            for shape in crvShape :
                if 'rebuiltCurveShape' in str (shape) :
                    crvShape.remove( shape ) ;

            crvShape = crvShape[0] ;
            
            arclen = pm.arclen ( crvShape ) ;
            
            arclen_list.append ( arclen ) ;
            folLen_dict[str(fol)] = arclen ;
        
        arclen_list.sort() ;
        
        minlen = arclen_list[0] ;
        maxlen = arclen_list[-1] ;
        
        folLen_dict['min'] = minlen ;
        folLen_dict['max'] = maxlen ;
        
        return folLen_dict ;
        
    def set_btn_cmd ( self , *args ) :
        
        tsl = self.TextScrollList ( self.hairSystem_tsl ) ;
        
        hairSystem_list = tsl.getSelected() ;
        
        for hairSystem in hairSystem_list :
            
            hairSystem = pm.PyNode ( hairSystem ) ;
            fol_list = self.getFol_func ( hairSystem ) ;
            fol_dict = self.getFolLenDict_func ( hairSystem ) ;

            # Copy Graphs
            for fol in fol_list :

                fol = pm.PyNode ( fol ) ;

                if pm.checkBox ( self.stiffnessScale_graph_cbx , q = True , v = True ) :
                    self.graph_copy_func (
                        driver = hairSystem ,
                        driven = fol ,
                        attribute = 'stiffnessScale' ) ;

                if pm.checkBox ( self.clumpWidthScale_graph_cbx , q = True , v = True ) :
                    self.graph_copy_func (
                        driver = hairSystem ,
                        driven = fol ,
                        attribute = 'clumpWidthScale' ) ;

                if pm.checkBox ( self.attractionScale_graph_cbx , q = True , v = True ) :
                    self.graph_copy_func (
                        driver = hairSystem ,
                        driven = fol ,
                        attribute = 'attractionScale' ) ;

            # Set Attr
            maxlen = float ( fol_dict ['max'] ) ;
            minlen = float ( fol_dict ['min'] ) ;
            
            lenRange = maxlen - minlen ;

            attr_list = [] ;
            attr_list.extend ( [ 'lengthFlex' , 'damp' , 'stiffness' ] ) ;
            attr_list.append ( 'clumpWidth' ) ;
            attr_list.extend ( [ 'startCurveAttract' , 'attractionDamp' ] ) ;

            for attr in attr_list :

                cmd = """
# {attr}_default_ff   = self.FloatField ( self.{attr}_defaultValue_floatField ) ;
{attr}_min_ff       = self.FloatField ( self.{attr}_min_floatField ) ;
{attr}_max_ff       = self.FloatField ( self.{attr}_max_floatField ) ;

max_val = {attr}_max_ff.getValue() ;
min_val = {attr}_min_ff.getValue() ;

valRange = max_val - min_val ;
valPerPercentage = valRange / 100 ;

for fol in fol_list :
    len = fol_dict [ str(fol) ] ;
    val = min_val + ( ( (len-minlen)/lenRange*100 ) * valPerPercentage ) ;

    fol.{attr}.set ( val ) ;
""".format ( attr = attr ) ;
                
                exec ( cmd ) ;
            
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
                        
                    pm.button ( label = 'Enable Dynamic Override' , w = lw , c = self.enableDynamicOverride_btn_cmd ) ;
                    pm.button ( label = 'Disable Dynamic Override' , w = lw , c = self.disableDynamicOverride_btn_cmd ) ;
                    
                    pm.button ( label = 'Enable Collide' , w = lw , c = self.enableCollide_btn_cmd ) ;
                    pm.button ( label = 'Disable Collide' , w = lw , c = self.disableCollide_btn_cmd ) ;
                
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
                compAttr_list.append ( [ 'lengthFlex' , 0.0 , [ 0.2 , 0.5 ] ] ) ;
                compAttr_list.append ( [ 'damp' , 0.0 , [ 0.2 , 1 ] ] ) ;
                compAttr_list.append ( [ 'stiffness' , 0.15 , [ 0.2 , 0.5 ] ] ) ;
                
                cw = [ ( 1 , w/4 ) , ( 2 , w/4 ) , ( 3 , w/4 ) , ( 4 , w/4 ) ] ;
                with pm.rowColumnLayout ( nc = 4 , cw = cw ) :
                    
                    for compAttr in compAttr_list :    
                        self.insertAttr ( compAttr ) ;
                
                ### Stiffness Scale
                pm.separator ( vis = False , h = 15 ) ;
                with pm.frameLayout (
                    label       = 'Stiffness Scale' ,
                    width       = w ,
                    collapsable = True ,
                    collapse    = False ,
                    bgc         = ( 0.078 , 0.153 , 0.263 ) ,
                    ) :
                    
                    with pm.rowColumnLayout ( nc = 2 , cw = [ ( 1 , w/2 ) , ( 2 , w/2 ) ] ) :
                        pm.text ( label = '' ) ;
                        self.stiffnessScale_graph_cbx = pm.checkBox ( v = True , w = w/2 ,
                            label = 'Copy Graph from Hair System' ) ;
                    
                    compAttr_list = [] ;
                    compAttr_list.append ( [ 'clumpWidth' , 0.3 , [ 0.2 , 0.3 ] ] ) ;
                    
                    with pm.rowColumnLayout ( nc = 4 , cw = [ ( 1 , w/4 ) , ( 2 , w/4 ) , ( 3 , w/4 ) , ( 4 , w/4 ) ] ) :
                    
                        for compAttr in compAttr_list :
                            self.insertAttr ( compAttr ) ;
                    
                ### Clump Width Scale
                pm.separator ( vis = False , h = 15 ) ;
                with pm.frameLayout (
                    label       = 'Clump Width Scale' ,
                    width       = w ,
                    collapsable = True ,
                    collapse    = False ,
                    bgc         = ( 0.078 , 0.153 , 0.263 ) ,
                    ) :

                    with pm.rowColumnLayout ( nc = 2 , cw = [ ( 1 , w/2 ) , ( 2 , w/2 ) ] ) :
                        pm.text ( label = '' ) ;
                        self.clumpWidthScale_graph_cbx = pm.checkBox ( v = True , w = w/2 ,
                            label = 'Copy Graph from Hair System' ) ;

                ### Attraction Scale
                pm.separator ( vis = False , h = 15 ) ;
                with pm.frameLayout (
                    label       = 'Attraction Scale' ,
                    width       = w ,
                    collapsable = True ,
                    collapse    = False ,
                    bgc         = ( 0.078 , 0.153 , 0.263 ) ,
                    ) :
                                    
                    with pm.rowColumnLayout ( nc = 2 , cw = [ ( 1 , w/2 ) , ( 2 , w/2 ) ] ) :
                        pm.text ( label = '' ) ;
                        self.attractionScale_graph_cbx = pm.checkBox ( v = True , w = w/2 ,
                            label = 'Copy Graph from Hair System' ) ;
                    
                    compAttr_list = [] ;
                    compAttr_list.append ( [ 'startCurveAttract' , 0.0 , [ 0.3 , 1.25 ] ] ) ;
                    compAttr_list.append ( [ 'attractionDamp' , 0.0 , [ 0.1 , 0.3 ] ] ) ;
                    
                    with pm.rowColumnLayout ( nc = 4 , cw = [ ( 1 , w/4 ) , ( 2 , w/4 ) , ( 3 , w/4 ) , ( 4 , w/4 ) ] ) :
                        
                        for compAttr in compAttr_list :
                            self.insertAttr ( compAttr ) ;
                
                pm.separator ( vis = False , h = 15 ) ;
                
                # set, and reset to dynamic override default values
                with pm.rowColumnLayout ( nc = 2 , cw = [ ( 1 , w/2 ) , ( 2 , w/2 ) ] ) :

                    pm.button ( label = 'Set' , w = w/2 , bgc = ( 1 , 1 , 1 ) , c = self.set_btn_cmd ) ;
                    pm.button ( label = 'Reset to Default Values (WIP)' , w = w/2 , enable = False ) ;
 
        window.show () ;
 
        self.guiInitialize_func() ;
 
class Main ( NHairDynOvr , Gui , GuiFunc , General , NaturalSort ) :
     
    def __init__ ( self ) :
        super ( Main , self ).__init__() ;
         
    def run ( self , *args ) :
        self.showGui() ;
 
def run ( *args ) :
    main = Main() ;
    main.run() ;
 
run () ;

# make some follicle stiff by selecting curves

'''
usable version

known bugs : 
- If there's only 1 curve in the hair system the script will not work as it will produce the len range of 0
- Need maximum value for lengthFlex , Damp, Stiffness, etc.

Features to add : 
- Make stiff curve (static) from selected
- Reset values to default
'''

