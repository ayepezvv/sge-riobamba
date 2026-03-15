from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import sys
import os

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))
from app.db.base_class import Base
import app.models

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table" and object.schema == "tiger":
        return False
    if type_ == "table" and object.schema == "topology":
        return False
    if type_ == "table" and name in [
        'spatial_ref_sys', 'layer', 'topology', 'pagc_gaz', 'pagc_lex', 'pagc_rules',
        'tabblock', 'zcta5', 'zip_lookup', 'countysub_lookup', 'zip_state', 'featnames',
        'edges', 'addr', 'county', 'zip_lookup_base', 'county_lookup', 'loader_variables',
        'direction_lookup', 'state_lookup', 'place_lookup', 'secondary_unit_lookup',
        'zip_lookup_all', 'geocode_settings_default', 'tabblock20', 'zip_state_loc',
        'cousub', 'state', 'addrfeat', 'street_type_lookup', 'loader_lookuptables',
        'faces', 'place', 'geocode_settings', 'tract', 'bg', 'loader_platform'
    ]:
        return False
    return True

def include_name(name, type_, parent_names):
    if type_ == "schema":
        return name in [None, "public", "administracion", "catastro", "comercial", "core", "contratacion", "configuracion", "informatica", "bodega"]
    return True


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

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
