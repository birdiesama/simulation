import pymel.core as pm ;
import os ;
import re ;

def checkVersion ( name , path , incrementVersion = False , incrementSubVersion = False , *args  ) :
    # look for 'vxxx_xxx' e.g. 'v001_001'

    file_list = os.listdir ( path ) ;
    version_list = [] ;

    if not file_list :
        finalVersion = 'v001_001' ;

    else : 
        for file in file_list :
            if name in str ( file ) :
                version = re.findall ( 'v' + '[0-9]{3}' + '_' + '[0-9]{3}' , file ) ;
                if version :
                    version = version[0] ;
                    version_list.append ( version ) ;
    
        if not version_list :
            finalVersion = 'v001_001' ;
        else :
            version_list.sort() ;

            currentVersion = version_list[-1] ;
            version = currentVersion.split('_')[0] ;
            version = version.split('v')[-1] ;
            version = int ( version ) ;

            subVersion = currentVersion.split('_')[-1] ;
            subVersion = int ( subVersion ) ;

            if incrementVersion :
                version     += 1 ;
                subVersion   = 1 ;           

            elif incrementSubVersion :
                subVersion += 1 ;

            version     = str(version) ;
            subVersion  = str(subVersion) ;

            finalVersion = 'v' + version.zfill(3) + '_' + subVersion.zfill(3) ;
        
    return finalVersion ;

def checkIncrement ( name , path , incrementIncrement = False , *args ) :
    # check for '.xxxx.' e.g. '.0001.'

    file_list = os.listdir ( path ) ;
    increment_list = [] ;

    if not file_list :
        finalIncrement = '0001' ;

    else :
        for file in file_list :
            if name in str ( file ) :
                increment = re.findall ( '.' + '[0-9]{4}' + '.' , file ) ;
                if increment :
                    increment = increment[0] ;
                    increment_list.append ( increment ) ;

        if not increment_list :
            finalIncrement = '0001' ;
        else :
            
            increment_list.sort() ;
            currentIncrement = increment_list[-1] ;
            increment = currentIncrement.split('.')
            for split in increment :
                if split == '' :
                    increment.remove ( split ) ;
            increment = increment[0] ;
            increment = int ( increment ) ;

            if incrementIncrement :
                increment += 1 ;

            finalIncrement = str(increment).zfill(4) ;

    return finalIncrement ;

def composeName ( target , *args ) :

    if type(target) == type([]) :
        
        target_list     = target ;
        name_list = [] ;

        for target in target_list :
            name = composeName ( target ) ;
            name_list.append ( name ) ;

        composedName = name_list[0] ;

        if len ( name_list ) > 1 :

            composedName += '_to_' + name_list[-1] ;

    else :
        
        nameSplit_list = target.split ( '_' ) ;

        for split in nameSplit_list :
            if split == '' :
                nameSplit_list.remove ( split ) ;

        composedName = nameSplit_list[0] ;

        if len ( nameSplit_list ) > 1 :
            for split in nameSplit_list [1:] :
                composedName += split[0].upper() + split[1:] ;

    return composedName ;