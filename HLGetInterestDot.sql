DELIMITER $$

DROP FUNCTION IF EXISTS HLGetInterestDot;

CREATE FUNCTION HLGetInterestDot(A_Id int(11), B_Id int(11)) RETURNS DECIMAL(10, 2)
BEGIN

DECLARE dotProduct DECIMAL(10,2); 

select  (
        Vec0.I0 * Vec1.I0 + 
        Vec0.I1 * Vec1.I1 +
        Vec0.I2 * Vec1.I2 + 
        Vec0.I3 * Vec1.I3 +
        Vec0.I4 * Vec1.I4 + 
        Vec0.I5 * Vec1.I5 +
        Vec0.I6 * Vec1.I6 + 
        Vec0.I7 * Vec1.I7 +
        Vec0.I8 * Vec1.I8 + 
        Vec0.I9 * Vec1.I9 +
        Vec0.I10 * Vec1.I10 + 
        Vec0.I11 * Vec1.I11 + 
        Vec0.I12 * Vec1.I12 + 
        Vec0.I13 * Vec1.I13 + 
        Vec0.I14 * Vec1.I14 + 
        Vec0.I15 * Vec1.I15 + 
        Vec0.I16 * Vec1.I16 +
        Vec0.I17 * Vec1.I17 +
        Vec0.I18 * Vec1.I18 +
        Vec0.I19 * Vec1.I19 +
        Vec0.I20 * Vec1.I20 +
        Vec0.I21 * Vec1.I21 +
        Vec0.I22 * Vec1.I22 +
        Vec0.I23 * Vec1.I23 +
        Vec0.I24 * Vec1.I24 +
        -- Vec0.I25 * Vec1.I25 + 
        -- Vec0.I26 * Vec1.I26 + 
        -- Vec0.I27 * Vec1.I27 +
        -- Vec0.I28 * Vec1.I28 + 
        -- Vec0.I29 * Vec1.I29 +
        -- Vec0.I30 * Vec1.I30 + 
        -- Vec0.I31 * Vec1.I31 + 
        -- Vec0.I32 * Vec1.I32 + 
        -- Vec0.I33 * Vec1.I33 + 
        -- Vec0.I34 * Vec1.I34 + 
        -- Vec0.I35 * Vec1.I35 + 
        -- Vec0.I36 * Vec1.I36 +
        -- Vec0.I37 * Vec1.I37 +
        -- Vec0.I38 * Vec1.I38 +
        -- Vec0.I39 * Vec1.I39 +
        -- Vec0.I40 * Vec1.I40 +
        -- Vec0.I41 * Vec1.I41 +
        -- Vec0.I42 * Vec1.I42 +
        -- Vec0.I43 * Vec1.I43 +
        -- Vec0.I44 * Vec1.I44
) into dotProduct 
from InterestVector as Vec0, InterestVector as Vec1
where Vec0.MB_Id = A_Id and Vec1.MB_Id = B_Id;

RETURN dotProduct;

END $$
DELIMITER ;
