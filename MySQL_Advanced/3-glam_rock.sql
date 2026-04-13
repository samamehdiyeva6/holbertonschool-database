--kjbkjgkgjh
SELECT band_name,
       YEAR(IFNULL(split, CURDATE())) - formed AS lifespan
FROM metal_bands
WHERE LOWER(style) LIKE '%glam rock%'
ORDER BY lifespan DESC;
