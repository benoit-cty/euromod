/* LEGAL TEXT */

/* List juridictions */
SELECT * FROM public.jurisdictions;


SELECT * FROM public.instruments
WHERE jurisdiction_id = 3 /* LT */
ORDER BY id ASC LIMIT 10;
/* first id = b0000000-0000-4000-8000-000000000004 */


SELECT * FROM public.legal_units
WHERE instrument_id = 'b0000000-0000-4000-8000-000000000004'
ORDER BY id ASC LIMIT 10;
/* first id = 0278d2eb-1f4f-4c75-8cbc-9cecd85a601f */

SELECT * FROM public.legal_unit_versions
WHERE legal_unit_id = '0278d2eb-1f4f-4c75-8cbc-9cecd85a601f';
/* first id = 34b61e92-0063-4111-b1c4-1c293346d11b */

SELECT * FROM public.unit_texts
WHERE version_id = '34b61e92-0063-4111-b1c4-1c293346d11b';
/* first id =  ff8fec02-e0db-4b5a-8149-1347fe061cc8 */

SELECT * FROM public.unit_texts
WHERE translation_of = 'ff8fec02-e0db-4b5a-8149-1347fe061cc8';