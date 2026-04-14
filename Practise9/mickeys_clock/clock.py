import datetime

def get_time_angles():
    now = datetime.datetime.now()
    
    raw_min_angle = -(now.minute * 6)
    raw_sec_angle = -(now.second * 6)
    
    
    MIN_OFFSET = -180 
    SEC_OFFSET = 0   
    
    return raw_min_angle + MIN_OFFSET, raw_sec_angle + SEC_OFFSET