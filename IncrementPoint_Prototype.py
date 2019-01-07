import pymel.core as pm ;

from operator import itemgetter ;

selection_list = pm.ls ( sl = True ) ;

increment = 10 ;

target_list = [] ;

for target1 , target2 in zip ( selection_list[:-1] , selection_list [1:] ) :
    target1_pos = pm.xform ( target1 , q = True , ws = True , rp = True ) ;
    target2_pos = pm.xform ( target2 , q = True , ws = True , rp = True ) ;
    x = ( target1_pos[0] - target2_pos[0] ) ** 2 ;
    y = ( target1_pos[1] - target2_pos[1] ) ** 2 ;
    z = ( target1_pos[2] - target2_pos[2] ) ** 2 ;
    distance = ( x + y + z ) ** 0.5 ;
    target_list.append ( [ target1 , target2 , distance ] ) ;

sorted_list = sorted ( target_list , key = itemgetter (2) ) ;
minDis = sorted_list[0][2] ;
maxDis = sorted_list[-1][2] ;

pointPos_list = [] ;

for i in range ( 0 , len ( selection_list )  ) :
    
    dis = pm.xform ( selection_list[i] , q = True , ws = True , rp = True ) ;
    pointPos_list.append ( dis ) ;
    
    if not i == ( len ( selection_list ) - 1 ) : 
            
        nextDis = pm.xform ( selection[i+1] , q = True , ws = True , rp = True ) ;
        
        x = nextDis[0] - dis[0]  ;
        y = nextDis[1] - dis[1]  ;
        z = nextDis[2] - dis[2]  ;

        difDis = [ x , y , z ] ;
        
        inc = round ( ( target_list[i][2] / maxDis ) * increment ) ;
        inc = int ( inc ) ;
        print inc ;
        
        for j in range ( 1 , inc + 1 ) :
            incX = dis[0] + ( difDis[0]/inc * j ) ;
            incY = dis[1] + ( difDis[1]/inc * j ) ;
            incZ = dis[2] + ( difDis[2]/inc * j ) ;
            pointPos_list.append ( [ incX , incY ,incZ ] ) ;

for point in pointPos_list :
    print point ;
pm.curve ( d = 1 , p = pointPos_list ) ;
