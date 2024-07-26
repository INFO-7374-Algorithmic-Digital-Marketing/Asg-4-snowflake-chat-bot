SELECT dt.d_year,
       item.i_brand_id AS brand_id,
       item.i_brand AS brand,
       SUM({aggc}) AS sum_agg
FROM date_dim dt,
     store_sales,
     item
WHERE dt.d_date_sk = store_sales.ss_sold_date_sk
  AND store_sales.ss_item_sk = item.i_item_sk
  AND item.i_manufact_id = {manufact}
  AND dt.d_moy = {month}
GROUP BY dt.d_year,
         item.i_brand,
         item.i_brand_id
ORDER BY dt.d_year,
         sum_agg DESC,
         brand_id
LIMIT {limit};
