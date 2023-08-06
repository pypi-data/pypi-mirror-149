## LP REVISING VALIDATION

<class 'pandas.core.frame.DataFrame'>
RangeIndex: 330956 entries, 0 to 330955
Data columns (total 64 columns):
 #   Column                            Non-Null Count   Dtype         definition
---  ------                            --------------   -----           -----
 0   appointment_id                    330956 non-null  object          ?*
 1   city                              329825 non-null  object          ?
 2   c24_quote                         330956 non-null  int64           ?
 3   c2b_service                       330319 non-null  float64         ?
 4   lp                                327772 non-null  float64         ?* last lp
 5   make                              330956 non-null  object          ?
 6   model                             330956 non-null  object          ?
 7   year                              330956 non-null  int64           ?
 8   variant                           330956 non-null  object          ?
 9   first_si                          330956 non-null  datetime64[ns]  ?
 10  listing_status                    330956 non-null  object          ? 
 11  finalc24q                         330956 non-null  int64           ? quotation c24 for seller(customer)
 12  total_inventory_days              330956 non-null  int64           ?
 13  days_from_listing                 330956 non-null  int64           ? active listing days ()
 14  inventory_bucket                  0 non-null       object          ?         
 15  price_bucket                      0 non-null       object          ?
 16  gs_bought_c2ctp                   330956 non-null  int64           ?
 17  gs_bought_dstp                    330956 non-null  int64           De
 18  tps_c2c_tp                        0 non-null       object          ?
 19  tps_ds_tp                         0 non-null       object          ?
 20  tps_ftp                           0 non-null       object          ?
 21  fin_c2c_tp                        330956 non-null  int64           ? C2CTP
 22  final_margin                      330956 non-null  float64         ? Designed Margin () 
 23  ops_cost                          0 non-null       object          ?
 24  refurb_cost                       330956 non-null  int64           ?
 25  rto_cost                          330956 non-null  int64           ?
 26  intra_rto                         330956 non-null  int64           ?
 27  liquidation_price                 330956 non-null  float64         ? final_margin * C2CTP
 28  floor_applied                     0 non-null       object          ?
 29  ceiling_applied                   0 non-null       object          ?
 30  current_lp                        0 non-null       object          ?
 31  final_liquidation_price           330956 non-null  int64           ? Tech Price
 32  final_listing_price               0 non-null       object          ? 
 33  timestamp                         330956 non-null  datetime64[ns]  ?
 34  booked_flag                       151549 non-null  float64         ? Null ? True
 35  booked_amount                     151549 non-null  float64         ? booking amount
 36  final_lp                          330956 non-null  int64           ?
 37  floor_lp                          330956 non-null  int64           ?
 38  gross_margin                      0 non-null       object          ?
 39  gross_margin_per                  0 non-null       object          ?
 40  on_road_price                     330956 non-null  int64           ? for new car MMVY (Market price)
 41  price_after_onroad                330956 non-null  int64           ? Market price after deprciation
 42  manual_override_price_individual  10123 non-null   float64         ? manually not from model 
 43  manual_override_price             330956 non-null  float64         ? manually not from model (cohort level) (discontinue)
 44  tcs_addition                      330956 non-null  float64         ? >10L( liquidation_price ?) TCS 1%
 45  refurb_cost_capped                0 non-null       object          ? x
 46  final_liquidation_price_brc       0 non-null       object          ? x
 47  original_price_new                330956 non-null  int64           ?
 48  original_price                    330956 non-null  int64           ? Actual Price
 49  discount                          0 non-null       object          ? Discounted Price
 50  old_discount                      0 non-null       object          ?
 51  base_price                        0 non-null       object          ?
 52  buyer_margin                      0 non-null       object          ?
 53  seller_margin                     0 non-null       object          ?
 54  start_lp                          0 non-null       object          ?
 55  lp_revised                        0 non-null       object          ?
 56  lp_revised_cap                    0 non-null       object          ?
 57  final_model_lp                    0 non-null       object          ?
 58  pconv                             0 non-null       object          ?
 59  pconv_revised                     0 non-null       object          ?
 60  desired_p                         0 non-null       object          ?
 61  tot_views_cumsum                  0 non-null       object          ?
 62  category2                         0 non-null       object          ?
 63  exp_pct                           0 non-null       object          ?
dtypes: datetime64[ns](2), float64(9), int64(18), object(35)
memory usage: 161.6+ MB
