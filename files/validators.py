from django.core.exceptions import ValidationError

def validate_extension(value):
    value= str(value)
    if value.endswith(".csv") != True and value.endswith(".xls") != True and value.endswith(".xlsx") != True: 
        raise ValidationError("Only csv, xls, and xlsx are supported")  
    else:
        return value