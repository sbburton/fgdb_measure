 # Dictionary mapping UOM to their arcpy expressions
AREA_EXPRESSIONS = {
    'squareFoot': '!shape.area@SQUAREFEET!',
    'squareYard': '!shape.area@SQUAREYARDS!',
    'squareMeter': '!shape.area@SQUAREMETERS!',
    'acre': '!shape.area@ACRES!',
    'hectare': '!shape.area@HECTARES!',
    'squareMile': '!shape.area@SQUAREMILES!',
    'squareKilometer': '!shape.area@SQUAREKILOMETERS!'
}

LENGTH_EXPRESSIONS = {
    'linearFoot': '!shape.length@FEET!',
    'linearYard': '!shape.length@YARDS!'
}