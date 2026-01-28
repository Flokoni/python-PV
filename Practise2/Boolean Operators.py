

has_login = True
has_password = True

is_weekend = True
is_holiday = False


can_rest = is_weekend or is_holiday
print(f"Can we rest? {can_rest}") # True

is_engine_running = False

print(f"Are we need to run engine? {not is_engine_running}") 

score = 85

is_top_score = score > 80 and score <= 100
print(f"It is a good mark? {is_top_score}") # True

is_admin = False
has_key = True
is_owner = False

access = (is_admin or has_key) and not is_owner
print(f"access is allowed: {access}") # True
