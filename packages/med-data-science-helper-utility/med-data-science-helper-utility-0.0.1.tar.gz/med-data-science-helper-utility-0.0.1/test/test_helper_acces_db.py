

import med_data_science_helper.helper_acces_db as hadb

print(hadb.get_path_BD())


df = hadb.get_ECE_2P()
df = hadb.get_ECE_4P()
df = hadb.get_ECE_2S()
df = hadb.get_ECE()

df = hadb.get_Censo_Educativo(anio=2019)

df = hadb.get_traslados_por_anio(2019)
df = hadb.get_traslados_a_publico(2019)

df = hadb.get_df_notas(2019)
df = hadb.get_df_servicios()

df = hadb.get_desertores_por_anio(2019)

df = hadb.get_shock_economico(2019)

df = hadb.get_sisfoh()

df = hadb.get_distancia_prim_sec()

df = hadb.get_siagie_por_anio(2019)
