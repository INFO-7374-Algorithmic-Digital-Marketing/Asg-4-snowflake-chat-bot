SELECT i_item_id, 
       AVG(ss_quantity) AS agg1,
       AVG(ss_list_price) AS agg2,
       AVG(ss_coupon_amt) AS agg3,
       AVG(ss_sales_price) AS agg4 
FROM store_sales, 
     customer_demographics, 
     date_dim, 
     item, 
     promotion
WHERE ss_sold_date_sk = d_date_sk 
  AND ss_item_sk = i_item_sk 
  AND ss_cdemo_sk = cd_demo_sk 
  AND ss_promo_sk = p_promo_sk 
  AND cd_gender = '{gen}' 
  AND cd_marital_status = '{ms}' 
  AND cd_education_status = '{es}' 
  AND (p_channel_email = 'N' OR p_channel_event = 'N') 
  AND d_year = {year}
GROUP BY i_item_id
ORDER BY i_item_id
LIMIT {limit};
