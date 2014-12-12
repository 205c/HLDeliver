DELIMITER $$

DROP FUNCTION IF EXISTS getDotSum;

CREATE FUNCTION getDotSum(nV_Id int(11),nC0 DECIMAL(10,2),nC1 DECIMAL(10,2),nC2 DECIMAL(10,2),nC3 DECIMAL(10,2),nC4 DECIMAL(10,2),nC5 DECIMAL(10,2),nC6 DECIMAL(10,2),nC7 DECIMAL(10,2),nC8 DECIMAL(10,2),nC9 DECIMAL(10,2),nC10 DECIMAL(10,2),nC11 DECIMAL(10,2),nC12 DECIMAL(10,2),nC13 DECIMAL(10,2),nC14 DECIMAL(10,2),nC15 DECIMAL(10,2),nC16 DECIMAL(10,2),nC17 DECIMAL(10,2),nC18 DECIMAL(10,2),nC19 DECIMAL(10,2),nC20 DECIMAL(10,2),nC21 DECIMAL(10,2),nC22 DECIMAL(10,2),nC23 DECIMAL(10,2),nC24 DECIMAL(10,2),nC25 DECIMAL(10,2),nC26 DECIMAL(10,2),nC27 DECIMAL(10,2),nC28 DECIMAL(10,2),nC29 DECIMAL(10,2),nC30 DECIMAL(10,2),nC31 DECIMAL(10,2),nC32 DECIMAL(10,2),nC33 DECIMAL(10,2),nC34 DECIMAL(10,2),nC35 DECIMAL(10,2),nC36 DECIMAL(10,2),nC37 DECIMAL(10,2),nC38 DECIMAL(10,2),nC39 DECIMAL(10,2),nC40 DECIMAL(10,2),nC41 DECIMAL(10,2),nC42 DECIMAL(10,2),nC43 DECIMAL(10,2),nC44 DECIMAL(10,2),nC45 DECIMAL(10,2),nC46 DECIMAL(10,2)) RETURNS DECIMAL(10, 2)
BEGIN
DECLARE dotProduct DECIMAL(10,2);
select(
    V0 * nC0+ V1 * nC1+ V2 * nC2+ V3 * nC3+ V4 * nC4+
    V5 * nC5+ V6 * nC6+ V7 * nC7+ V8 * nC8+ V9 * nC9+
    V10 * nC10+ V11 * nC11+ V12 * nC12+ V13 * nC13+ V14 * nC14+
    V15 * nC15+ V16 * nC16+ V17 * nC17+ V18 * nC18+ V19 * nC19+
    V20 * nC20+ V21 * nC21+ V22 * nC22+ V23 * nC23+ V24 * nC24+
    V25 * nC25+ V26 * nC26+ V27 * nC27+ V28 * nC28+ V29 * nC29+
    V30 * nC30+ V31 * nC31+ V32 * nC32+ V33 * nC33+ V34 * nC34+
    V35 * nC35+ V36 * nC36+ V37 * nC37+ V38 * nC38+ V39 * nC39+
    V40 * nC40+ V41 * nC41+ V42 * nC42+ V43 * nC43+ V44 * nC44+
    V45 * nC45+ V46 * nC46) into dotProduct
from V
where V_Id = nV_Id;

return dotProduct;

END $$
DELIMITER ;
