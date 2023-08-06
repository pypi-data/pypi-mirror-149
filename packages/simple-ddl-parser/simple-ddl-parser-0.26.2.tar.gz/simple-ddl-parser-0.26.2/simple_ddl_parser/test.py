from simple_ddl_parser import DDLParser

ddl="""
create schema my_schema comment='this is comment1';
"""
result = DDLParser(ddl,normalize_names=True).run(output_mode="snowflake")

import pprint
pprint.pprint(result) 
