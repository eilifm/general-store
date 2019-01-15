CREATE OR REPLACE VIEW public.pge_data
AS SELECT to_date(obvents.val ->> 'start_time'::text, 'YYYY-MM-DD"T"HH24:MI:SS'::text) AS samp_date,
    to_timestamp(obvents.val ->> 'start_time'::text, 'YYYY-MM-DD"T"HH24:MI:SS'::text) AS start_time,
    (obvents.val ->> 'cost'::text)::double precision AS cost,
    (obvents.val ->> 'usage'::text)::double precision AS power_usage,
    to_timestamp(obvents.val ->> 'end_time'::text, 'YYYY-MM-DD"T"HH24:MI:SS'::text) AS end_time
   FROM obvents
  WHERE obvents.o_type::text = 'pge_data'::text;
