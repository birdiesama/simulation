import pymel.core as pm ;

selection_list = pm.ls ( sl = True ) ;
info_list = [] ;

division = 10 ;

for selection in selection_list :
    pos = pm.xform ( selection , q = True , ws = True , rp = True ) ;
    info_list.append ( [ selection , pos ] ) ;
 
start_info = info_list[0] ;
end_info = info_list[-1] ;

start_pos = start_info[1] ;
end_pos = end_info[1] ;

total_dis = ( ( start_pos[0] - end_pos[0] )**2 + ( start_pos[1] - end_pos[1] )**2 + ( start_pos[2]-end_pos[2])**2 ) ** 0.5
print total_dis ;

