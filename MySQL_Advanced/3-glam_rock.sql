--kjbkjgkgjh
SELECT band_name,
       YEAR(IFNULL(split, CURDATE())) - YEAR(formed) AS lifespan
FROM metal_bands
WHERE style = 'Glam rock'
ORDER BY lifespan DESC;
