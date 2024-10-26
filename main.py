# config.py
import os
import pandas as pd

GDB_PATH = r"path/to/your.gdb"
CROSSWALK_PATH = r"path/to/your/crosswalk.csv"

# utils.py
import arcpy
import pandas as pd
import os
from area_expressions import AREA_EXPRESSIONS, LENGTH_EXPRESSIONS

def list_all_feature_classes(gdb_path):
    """List all feature classes efficiently"""
    arcpy.env.workspace = gdb_path
    fc_list = []
    
    # Walk through all feature classes, including those in datasets
    for dirpath, _, filenames in arcpy.da.Walk(gdb_path, datatype="FeatureClass"):
        for fc in filenames:
            # Get relative path from GDB root
            relative_path = os.path.relpath(os.path.join(dirpath, fc), gdb_path)
            fc_list.append(relative_path)
    
    return fc_list

def process_feature_class(fc_name, gdb_path, crosswalk_df):
    """Process a single feature class"""
    fc_map = crosswalk_df[crosswalk_df['feature_class'] == fc_name].iloc[0]
    fc_path = os.path.join(gdb_path, fc_name)
    
    value_field = fc_map['value_field']
    uom_value = fc_map['uom_value']
    
    # Check if UOM is in either area or length expressions
    if uom_value in AREA_EXPRESSIONS:
        expression = AREA_EXPRESSIONS[uom_value]
    elif uom_value in LENGTH_EXPRESSIONS:
        expression = LENGTH_EXPRESSIONS[uom_value]
    else:
        raise ValueError(f"Unsupported UOM: {uom_value}")
    
    # Calculate the field
    arcpy.management.CalculateField(
        in_table=fc_path,
        field=value_field,
        expression=expression,
        expression_type='PYTHON3'
    )
    
    # Update UOM field if needed
    if fc_map['uom_field']:
        arcpy.management.CalculateField(
            in_table=fc_path,
            field=fc_map['uom_field'],
            expression=f"'{uom_value}'",
            expression_type='PYTHON3'
        )

    else:
        raise ValueError(f"Unsupported UOM: {uom}")

def main():
    crosswalk = pd.read_csv(CROSSWALK_PATH)
    
    # Get all feature classes
    print("Listing feature classes...")
    all_fcs = list_all_feature_classes(GDB_PATH)
    
    # Process feature classes that exist in crosswalk
    fc_count = len(crosswalk['feature_class_name'].unique())
    for i, fc_name in enumerate(crosswalk['feature_class_name'].unique(), 1):
        if fc_name in all_fcs:
            try:
                print(f"Processing {i}/{fc_count}: {fc_name}")
                process_feature_class(fc_name, GDB_PATH, crosswalk)
            except Exception as e:
                print(f"Error processing {fc_name}: {str(e)}")
        else:
            print(f"Warning: Feature class {fc_name} not found in geodatabase")

if __name__ == "__main__":
    main()
