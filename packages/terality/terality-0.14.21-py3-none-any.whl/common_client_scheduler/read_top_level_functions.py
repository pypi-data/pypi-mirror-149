# pandas top level functions (e.g defined as pd.SomeFunc) that Terality reimplements
# we also need to specify each path parameter name as we handle it similarly for all read methods
read_top_level_functions_to_path_parameter = {
    "read_csv": "filepath_or_buffer",
    "read_excel": "io",
    "read_feather": "path",
    "read_fwf": "filepath_or_buffer",
    "read_hdf": "path_or_buf",
    "read_html": "io",
    "read_json": "path_or_buf",
    "read_orc": "path",
    "read_parquet": "path",
    "read_sas": "filepath_or_buffer",
    "read_spss": "path",
    "read_stata": "filepath_or_buffer",
    "read_table": "filepath_or_buffer",
    "read_xml": "path_or_buffer",
}
