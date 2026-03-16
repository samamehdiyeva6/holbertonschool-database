--dsvdfgsdf
SELECT band_name, IFNULL(split, CURDATE()) - formed AS lifespan FROM metal_bands
WHERE style = 'Glam rock'
ORDER BY lifespan DESC;
