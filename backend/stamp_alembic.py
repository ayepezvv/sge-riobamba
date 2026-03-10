path = "alembic/env.py"
with open(path, "r") as f:
    content = f.read()

import re
# Fix syntax
new_env = """
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        include_name=include_name,
        compare_type=True,
        compare_server_default=True,
        include_object=lambda obj, name, type_, reflected, compare_to: False if type_ == 'table' and obj.schema == 'administracion' and name in ['users', 'roles', 'permissions', 'role_permission'] else (False if name in ['spatial_ref_sys', 'layer', 'topology', 'pagc_gaz', 'pagc_lex', 'pagc_rules', 'tabblock', 'zcta5', 'zip_lookup', 'countysub_lookup', 'zip_state', 'featnames', 'edges', 'addr', 'county', 'zip_lookup_base', 'county_lookup', 'loader_variables', 'direction_lookup', 'state_lookup', 'place_lookup', 'secondary_unit_lookup', 'zip_lookup_all', 'geocode_settings_default', 'tabblock20', 'zip_state_loc', 'cousub', 'state', 'addrfeat', 'street_type_lookup', 'loader_lookuptables', 'faces', 'place', 'geocode_settings', 'tract', 'bg', 'loader_platform'] else True)
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            include_schemas=True,
            include_name=include_name,
            compare_type=True,
            compare_server_default=True,
            include_object=lambda obj, name, type_, reflected, compare_to: False if type_ == 'table' and obj.schema == 'administracion' and name in ['users', 'roles', 'permissions', 'role_permission'] else (False if name in ['spatial_ref_sys', 'layer', 'topology', 'pagc_gaz', 'pagc_lex', 'pagc_rules', 'tabblock', 'zcta5', 'zip_lookup', 'countysub_lookup', 'zip_state', 'featnames', 'edges', 'addr', 'county', 'zip_lookup_base', 'county_lookup', 'loader_variables', 'direction_lookup', 'state_lookup', 'place_lookup', 'secondary_unit_lookup', 'zip_lookup_all', 'geocode_settings_default', 'tabblock20', 'zip_state_loc', 'cousub', 'state', 'addrfeat', 'street_type_lookup', 'loader_lookuptables', 'faces', 'place', 'geocode_settings', 'tract', 'bg', 'loader_platform'] else True)
        )
        with context.begin_transaction():
            context.run_migrations()
"""

content = re.sub(r'def run_migrations_offline\(\) -> None:.*?context\.run_migrations\(\)', new_env, content, flags=re.DOTALL)

with open(path, "w") as f:
    f.write(content)
