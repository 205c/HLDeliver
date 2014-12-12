DELIMITER $$

DROP PROCEDURE IF EXISTS createNewInterestVector;

CREATE PROCEDURE createNewInterestVector(nMB_Id INT(11)) 
BEGIN

declare nInterest BIGINT(20);
declare nSex INT(2);


declare nV0 DECIMAL(10,2);
declare nV1 DECIMAL(10,2);
declare nV2 DECIMAL(10,2);
declare nV3 DECIMAL(10,2);
declare nV4 DECIMAL(10,2);
declare nV5 DECIMAL(10,2);
declare nV6 DECIMAL(10,2);
declare nV7 DECIMAL(10,2);
declare nV8 DECIMAL(10,2);
declare nV9 DECIMAL(10,2);
declare nV10 DECIMAL(10,2);
declare nV11 DECIMAL(10,2);
declare nV12 DECIMAL(10,2);
declare nV13 DECIMAL(10,2);
declare nV14 DECIMAL(10,2);
declare nV15 DECIMAL(10,2);
declare nV16 DECIMAL(10,2);
declare nV17 DECIMAL(10,2);
declare nV18 DECIMAL(10,2);
declare nV19 DECIMAL(10,2);
declare nV20 DECIMAL(10,2);
declare nV21 DECIMAL(10,2);
declare nV22 DECIMAL(10,2);
declare nV23 DECIMAL(10,2);
declare nV24 DECIMAL(10,2);
declare nC0 DECIMAL(10,2) default 0.0;
declare nC1 DECIMAL(10,2) default 0.0;
declare nC2 DECIMAL(10,2) default 0.0;
declare nC3 DECIMAL(10,2) default 0.0;
declare nC4 DECIMAL(10,2) default 0.0;
declare nC5 DECIMAL(10,2) default 0.0;
declare nC6 DECIMAL(10,2) default 0.0;
declare nC7 DECIMAL(10,2) default 0.0;
declare nC8 DECIMAL(10,2) default 0.0;
declare nC9 DECIMAL(10,2) default 0.0;
declare nC10 DECIMAL(10,2) default 0.0;
declare nC11 DECIMAL(10,2) default 0.0;
declare nC12 DECIMAL(10,2) default 0.0;
declare nC13 DECIMAL(10,2) default 0.0;
declare nC14 DECIMAL(10,2) default 0.0;
declare nC15 DECIMAL(10,2) default 0.0;
declare nC16 DECIMAL(10,2) default 0.0;
declare nC17 DECIMAL(10,2) default 0.0;
declare nC18 DECIMAL(10,2) default 0.0;
declare nC19 DECIMAL(10,2) default 0.0;
declare nC20 DECIMAL(10,2) default 0.0;
declare nC21 DECIMAL(10,2) default 0.0;
declare nC22 DECIMAL(10,2) default 0.0;
declare nC23 DECIMAL(10,2) default 0.0;
declare nC24 DECIMAL(10,2) default 0.0;
declare nC25 DECIMAL(10,2) default 0.0;
declare nC26 DECIMAL(10,2) default 0.0;
declare nC27 DECIMAL(10,2) default 0.0;
declare nC28 DECIMAL(10,2) default 0.0;
declare nC29 DECIMAL(10,2) default 0.0;
declare nC30 DECIMAL(10,2) default 0.0;
declare nC31 DECIMAL(10,2) default 0.0;
declare nC32 DECIMAL(10,2) default 0.0;
declare nC33 DECIMAL(10,2) default 0.0;
declare nC34 DECIMAL(10,2) default 0.0;
declare nC35 DECIMAL(10,2) default 0.0;
declare nC36 DECIMAL(10,2) default 0.0;
declare nC37 DECIMAL(10,2) default 0.0;
declare nC38 DECIMAL(10,2) default 0.0;
declare nC39 DECIMAL(10,2) default 0.0;
declare nC40 DECIMAL(10,2) default 0.0;
declare nC41 DECIMAL(10,2) default 0.0;
declare nC42 DECIMAL(10,2) default 0.0;
declare nC43 DECIMAL(10,2) default 0.0;
declare nC44 DECIMAL(10,2) default 0.0;
declare nC45 DECIMAL(10,2) default 0.0;
declare nC46 DECIMAL(10,2) default 0.0;
declare vecSum DECIMAL(10,2) default 0.0;
declare vecLen DECIMAL(10,2);


select MB_Interests into nInterest from Members where MB_Id = nMB_Id;
select MB_Sex into nSex from Members where MB_Id = nMB_Id;

IF (nInterest & 1) then
SET nC0= 1.0;
END IF;
IF (nInterest & 2) then
SET nC1= 1.0;
END IF;
IF (nInterest & 4) then
SET nC2= 1.0;
END IF;
IF (nInterest & 8) then
SET nC3= 1.0;
END IF;
IF (nInterest & 16) then
SET nC4= 1.0;
END IF;
IF (nInterest & 32) then
SET nC5= 1.0;
END IF;
IF (nInterest & 64) then
SET nC6= 1.0;
END IF;
IF (nInterest & 128) then
SET nC7= 1.0;
END IF;
IF (nInterest & 256) then
SET nC8= 1.0;
END IF;
IF (nInterest & 512) then
SET nC9= 1.0;
END IF;
IF (nInterest & 1024) then
SET nC10= 1.0;
END IF;
IF (nInterest & 2048) then
SET nC11= 1.0;
END IF;
IF (nInterest & 4096) then
SET nC12= 1.0;
END IF;
IF (nInterest & 8192) then
SET nC13= 1.0;
END IF;
IF (nInterest & 16384) then
SET nC14= 1.0;
END IF;
IF (nInterest & 32768) then
SET nC15= 1.0;
END IF;
IF (nInterest & 65536) then
SET nC16= 1.0;
END IF;
IF (nInterest & 131072) then
SET nC17= 1.0;
END IF;
IF (nInterest & 262144) then
SET nC18= 1.0;
END IF;
IF (nInterest & 524288) then
SET nC19= 1.0;
END IF;
IF (nInterest & 1048576) then
SET nC20= 1.0;
END IF;
IF (nInterest & 2097152) then
SET nC21= 1.0;
END IF;
IF (nInterest & 4194304) then
SET nC22= 1.0;
END IF;
IF (nInterest & 8388608) then
SET nC23= 1.0;
END IF;
IF (nInterest & 16777216) then
SET nC24= 1.0;
END IF;
IF (nInterest & 33554432) then
SET nC25= 1.0;
END IF;
IF (nInterest & 67108864) then
SET nC26= 1.0;
END IF;
IF (nInterest & 134217728) then
SET nC27= 1.0;
END IF;
IF (nInterest & 268435456) then
SET nC28= 1.0;
END IF;
IF (nInterest & 536870912) then
SET nC29= 1.0;
END IF;
IF (nInterest & 1073741824) then
SET nC30= 1.0;
END IF;
IF (nInterest & 2147483648) then
SET nC31= 1.0;
END IF;
IF (nInterest & 4294967296) then
SET nC32= 1.0;
END IF;
IF (nInterest & 8589934592) then
SET nC33= 1.0;
END IF;
IF (nInterest & 17179869184) then
SET nC34= 1.0;
END IF;
IF (nInterest & 34359738368) then
SET nC35= 1.0;
END IF;
IF (nInterest & 68719476736) then
SET nC36= 1.0;
END IF;
IF (nInterest & 137438953472) then
SET nC37= 1.0;
END IF;
IF (nInterest & 274877906944) then
SET nC38= 1.0;
END IF;
IF (nInterest & 549755813888) then
SET nC39= 1.0;
END IF;
IF (nInterest & 1099511627776) then
SET nC40= 1.0;
END IF;
IF (nInterest & 2199023255552) then
SET nC41= 1.0;
END IF;
IF (nInterest & 4398046511104) then
SET nC42= 1.0;
END IF;
IF (nInterest & 8796093022208) then
SET nC43= 1.0;
END IF;
IF (nInterest & 17592186044416) then
SET nC44= 1.0;
END IF;
IF (nSex = 1) then
SET nC45= 1.0;
END IF;
IF (nSex = 2) then
SET nC46= 1.0;
END IF;
SET nV0 = getDotSum(0, nC0,nC1,nC2,nC3,nC4,nC5,nC6,nC7,nC8,nC9,nC10,nC11,nC12,nC13,nC14,nC15,nC16,nC17,nC18,nC19,nC20,nC21,nC22,nC23,nC24,nC25,nC26,nC27,nC28,nC29,nC30,nC31,nC32,nC33,nC34,nC35,nC36,nC37,nC38,nC39,nC40,nC41,nC42,nC43,nC44,nC45,nC46);
SET nV1 = getDotSum(1, nC0,nC1,nC2,nC3,nC4,nC5,nC6,nC7,nC8,nC9,nC10,nC11,nC12,nC13,nC14,nC15,nC16,nC17,nC18,nC19,nC20,nC21,nC22,nC23,nC24,nC25,nC26,nC27,nC28,nC29,nC30,nC31,nC32,nC33,nC34,nC35,nC36,nC37,nC38,nC39,nC40,nC41,nC42,nC43,nC44,nC45,nC46);
SET nV2 = getDotSum(2, nC0,nC1,nC2,nC3,nC4,nC5,nC6,nC7,nC8,nC9,nC10,nC11,nC12,nC13,nC14,nC15,nC16,nC17,nC18,nC19,nC20,nC21,nC22,nC23,nC24,nC25,nC26,nC27,nC28,nC29,nC30,nC31,nC32,nC33,nC34,nC35,nC36,nC37,nC38,nC39,nC40,nC41,nC42,nC43,nC44,nC45,nC46);
SET nV3 = getDotSum(3, nC0,nC1,nC2,nC3,nC4,nC5,nC6,nC7,nC8,nC9,nC10,nC11,nC12,nC13,nC14,nC15,nC16,nC17,nC18,nC19,nC20,nC21,nC22,nC23,nC24,nC25,nC26,nC27,nC28,nC29,nC30,nC31,nC32,nC33,nC34,nC35,nC36,nC37,nC38,nC39,nC40,nC41,nC42,nC43,nC44,nC45,nC46);
SET nV4 = getDotSum(4, nC0,nC1,nC2,nC3,nC4,nC5,nC6,nC7,nC8,nC9,nC10,nC11,nC12,nC13,nC14,nC15,nC16,nC17,nC18,nC19,nC20,nC21,nC22,nC23,nC24,nC25,nC26,nC27,nC28,nC29,nC30,nC31,nC32,nC33,nC34,nC35,nC36,nC37,nC38,nC39,nC40,nC41,nC42,nC43,nC44,nC45,nC46);
SET nV5 = getDotSum(5, nC0,nC1,nC2,nC3,nC4,nC5,nC6,nC7,nC8,nC9,nC10,nC11,nC12,nC13,nC14,nC15,nC16,nC17,nC18,nC19,nC20,nC21,nC22,nC23,nC24,nC25,nC26,nC27,nC28,nC29,nC30,nC31,nC32,nC33,nC34,nC35,nC36,nC37,nC38,nC39,nC40,nC41,nC42,nC43,nC44,nC45,nC46);
SET nV6 = getDotSum(6, nC0,nC1,nC2,nC3,nC4,nC5,nC6,nC7,nC8,nC9,nC10,nC11,nC12,nC13,nC14,nC15,nC16,nC17,nC18,nC19,nC20,nC21,nC22,nC23,nC24,nC25,nC26,nC27,nC28,nC29,nC30,nC31,nC32,nC33,nC34,nC35,nC36,nC37,nC38,nC39,nC40,nC41,nC42,nC43,nC44,nC45,nC46);
SET nV7 = getDotSum(7, nC0,nC1,nC2,nC3,nC4,nC5,nC6,nC7,nC8,nC9,nC10,nC11,nC12,nC13,nC14,nC15,nC16,nC17,nC18,nC19,nC20,nC21,nC22,nC23,nC24,nC25,nC26,nC27,nC28,nC29,nC30,nC31,nC32,nC33,nC34,nC35,nC36,nC37,nC38,nC39,nC40,nC41,nC42,nC43,nC44,nC45,nC46);
SET nV8 = getDotSum(8, nC0,nC1,nC2,nC3,nC4,nC5,nC6,nC7,nC8,nC9,nC10,nC11,nC12,nC13,nC14,nC15,nC16,nC17,nC18,nC19,nC20,nC21,nC22,nC23,nC24,nC25,nC26,nC27,nC28,nC29,nC30,nC31,nC32,nC33,nC34,nC35,nC36,nC37,nC38,nC39,nC40,nC41,nC42,nC43,nC44,nC45,nC46);
SET nV9 = getDotSum(9, nC0,nC1,nC2,nC3,nC4,nC5,nC6,nC7,nC8,nC9,nC10,nC11,nC12,nC13,nC14,nC15,nC16,nC17,nC18,nC19,nC20,nC21,nC22,nC23,nC24,nC25,nC26,nC27,nC28,nC29,nC30,nC31,nC32,nC33,nC34,nC35,nC36,nC37,nC38,nC39,nC40,nC41,nC42,nC43,nC44,nC45,nC46);
SET nV10 = getDotSum(10, nC0,nC1,nC2,nC3,nC4,nC5,nC6,nC7,nC8,nC9,nC10,nC11,nC12,nC13,nC14,nC15,nC16,nC17,nC18,nC19,nC20,nC21,nC22,nC23,nC24,nC25,nC26,nC27,nC28,nC29,nC30,nC31,nC32,nC33,nC34,nC35,nC36,nC37,nC38,nC39,nC40,nC41,nC42,nC43,nC44,nC45,nC46);
SET nV11 = getDotSum(11, nC0,nC1,nC2,nC3,nC4,nC5,nC6,nC7,nC8,nC9,nC10,nC11,nC12,nC13,nC14,nC15,nC16,nC17,nC18,nC19,nC20,nC21,nC22,nC23,nC24,nC25,nC26,nC27,nC28,nC29,nC30,nC31,nC32,nC33,nC34,nC35,nC36,nC37,nC38,nC39,nC40,nC41,nC42,nC43,nC44,nC45,nC46);
SET nV12 = getDotSum(12, nC0,nC1,nC2,nC3,nC4,nC5,nC6,nC7,nC8,nC9,nC10,nC11,nC12,nC13,nC14,nC15,nC16,nC17,nC18,nC19,nC20,nC21,nC22,nC23,nC24,nC25,nC26,nC27,nC28,nC29,nC30,nC31,nC32,nC33,nC34,nC35,nC36,nC37,nC38,nC39,nC40,nC41,nC42,nC43,nC44,nC45,nC46);
SET nV13 = getDotSum(13, nC0,nC1,nC2,nC3,nC4,nC5,nC6,nC7,nC8,nC9,nC10,nC11,nC12,nC13,nC14,nC15,nC16,nC17,nC18,nC19,nC20,nC21,nC22,nC23,nC24,nC25,nC26,nC27,nC28,nC29,nC30,nC31,nC32,nC33,nC34,nC35,nC36,nC37,nC38,nC39,nC40,nC41,nC42,nC43,nC44,nC45,nC46);
SET nV14 = getDotSum(14, nC0,nC1,nC2,nC3,nC4,nC5,nC6,nC7,nC8,nC9,nC10,nC11,nC12,nC13,nC14,nC15,nC16,nC17,nC18,nC19,nC20,nC21,nC22,nC23,nC24,nC25,nC26,nC27,nC28,nC29,nC30,nC31,nC32,nC33,nC34,nC35,nC36,nC37,nC38,nC39,nC40,nC41,nC42,nC43,nC44,nC45,nC46);
SET nV15 = getDotSum(15, nC0,nC1,nC2,nC3,nC4,nC5,nC6,nC7,nC8,nC9,nC10,nC11,nC12,nC13,nC14,nC15,nC16,nC17,nC18,nC19,nC20,nC21,nC22,nC23,nC24,nC25,nC26,nC27,nC28,nC29,nC30,nC31,nC32,nC33,nC34,nC35,nC36,nC37,nC38,nC39,nC40,nC41,nC42,nC43,nC44,nC45,nC46);
SET nV16 = getDotSum(16, nC0,nC1,nC2,nC3,nC4,nC5,nC6,nC7,nC8,nC9,nC10,nC11,nC12,nC13,nC14,nC15,nC16,nC17,nC18,nC19,nC20,nC21,nC22,nC23,nC24,nC25,nC26,nC27,nC28,nC29,nC30,nC31,nC32,nC33,nC34,nC35,nC36,nC37,nC38,nC39,nC40,nC41,nC42,nC43,nC44,nC45,nC46);
SET nV17 = getDotSum(17, nC0,nC1,nC2,nC3,nC4,nC5,nC6,nC7,nC8,nC9,nC10,nC11,nC12,nC13,nC14,nC15,nC16,nC17,nC18,nC19,nC20,nC21,nC22,nC23,nC24,nC25,nC26,nC27,nC28,nC29,nC30,nC31,nC32,nC33,nC34,nC35,nC36,nC37,nC38,nC39,nC40,nC41,nC42,nC43,nC44,nC45,nC46);
SET nV18 = getDotSum(18, nC0,nC1,nC2,nC3,nC4,nC5,nC6,nC7,nC8,nC9,nC10,nC11,nC12,nC13,nC14,nC15,nC16,nC17,nC18,nC19,nC20,nC21,nC22,nC23,nC24,nC25,nC26,nC27,nC28,nC29,nC30,nC31,nC32,nC33,nC34,nC35,nC36,nC37,nC38,nC39,nC40,nC41,nC42,nC43,nC44,nC45,nC46);
SET nV19 = getDotSum(19, nC0,nC1,nC2,nC3,nC4,nC5,nC6,nC7,nC8,nC9,nC10,nC11,nC12,nC13,nC14,nC15,nC16,nC17,nC18,nC19,nC20,nC21,nC22,nC23,nC24,nC25,nC26,nC27,nC28,nC29,nC30,nC31,nC32,nC33,nC34,nC35,nC36,nC37,nC38,nC39,nC40,nC41,nC42,nC43,nC44,nC45,nC46);
SET nV20 = getDotSum(20, nC0,nC1,nC2,nC3,nC4,nC5,nC6,nC7,nC8,nC9,nC10,nC11,nC12,nC13,nC14,nC15,nC16,nC17,nC18,nC19,nC20,nC21,nC22,nC23,nC24,nC25,nC26,nC27,nC28,nC29,nC30,nC31,nC32,nC33,nC34,nC35,nC36,nC37,nC38,nC39,nC40,nC41,nC42,nC43,nC44,nC45,nC46);
SET nV21 = getDotSum(21, nC0,nC1,nC2,nC3,nC4,nC5,nC6,nC7,nC8,nC9,nC10,nC11,nC12,nC13,nC14,nC15,nC16,nC17,nC18,nC19,nC20,nC21,nC22,nC23,nC24,nC25,nC26,nC27,nC28,nC29,nC30,nC31,nC32,nC33,nC34,nC35,nC36,nC37,nC38,nC39,nC40,nC41,nC42,nC43,nC44,nC45,nC46);
SET nV22 = getDotSum(22, nC0,nC1,nC2,nC3,nC4,nC5,nC6,nC7,nC8,nC9,nC10,nC11,nC12,nC13,nC14,nC15,nC16,nC17,nC18,nC19,nC20,nC21,nC22,nC23,nC24,nC25,nC26,nC27,nC28,nC29,nC30,nC31,nC32,nC33,nC34,nC35,nC36,nC37,nC38,nC39,nC40,nC41,nC42,nC43,nC44,nC45,nC46);
SET nV23 = getDotSum(23, nC0,nC1,nC2,nC3,nC4,nC5,nC6,nC7,nC8,nC9,nC10,nC11,nC12,nC13,nC14,nC15,nC16,nC17,nC18,nC19,nC20,nC21,nC22,nC23,nC24,nC25,nC26,nC27,nC28,nC29,nC30,nC31,nC32,nC33,nC34,nC35,nC36,nC37,nC38,nC39,nC40,nC41,nC42,nC43,nC44,nC45,nC46);
SET nV24 = getDotSum(24, nC0,nC1,nC2,nC3,nC4,nC5,nC6,nC7,nC8,nC9,nC10,nC11,nC12,nC13,nC14,nC15,nC16,nC17,nC18,nC19,nC20,nC21,nC22,nC23,nC24,nC25,nC26,nC27,nC28,nC29,nC30,nC31,nC32,nC33,nC34,nC35,nC36,nC37,nC38,nC39,nC40,nC41,nC42,nC43,nC44,nC45,nC46);
SET vecSum = nV0*nV0+nV1*nV1+nV2*nV2+nV3*nV3+nV4*nV4+nV5*nV5+nV6*nV6+nV7*nV7+nV8*nV8+nV9*nV9+nV10*nV10+nV11*nV11+nV12*nV12+nV13*nV13+nV14*nV14+nV15*nV15+nV16*nV16+nV17*nV17+nV18*nV18+nV19*nV19+nV20*nV20+nV21*nV21+nV22*nV22+nV23*nV23+nV24*nV24;
SET vecLen = sqrt(vecSum);
Insert into InterestVector values (nMB_Id,nV0/vecLen,nV1/vecLen,nV2/vecLen,nV3/vecLen,nV4/vecLen,nV5/vecLen,nV6/vecLen,nV7/vecLen,nV8/vecLen,nV9/vecLen,nV10/vecLen,nV11/vecLen,nV12/vecLen,nV13/vecLen,nV14/vecLen,nV15/vecLen,nV16/vecLen,nV17/vecLen,nV18/vecLen,nV19/vecLen,nV20/vecLen,nV21/vecLen,nV22/vecLen,nV23/vecLen,nV24/vecLen);

END $$
DELIMITER ;
