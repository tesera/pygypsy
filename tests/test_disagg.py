from pygypsy.disaggregate import (
    fill_sp_prop,
    sp_prop_total,
    merge_simulated_gypsy_df_with_original_sp_prop_df,
    build_disaggregated_simulated_df
    )


def test_sp_prop_total():
    perc_sp = [
                ('Aw', 50), ('Sw', 30), 
                ('Pb', 20), ('', 0), 
                ('', 0)
               ]
    
    assert sp_prop_total(perc_sp) == {'PER_Aw_data':0.5, 'PER_Pb_data':0.2, 'PER_Sw_data':0.3, 'PER_Fb_data':0, 'PER_Fd_data':0}



