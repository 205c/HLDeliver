DELIMITER $$

DROP PROCEDURE IF EXISTS HLGetExpRecV5;

Create PROCEDURE HLGetExpRecV5(
nMBId int,
nMemberInts long,
nMemberAge int,
szMemberRelStatus text,
nMemberGender int,
nTOD INT, # 0:morning, 1:afternoon, 2:evening
nMbLat DOUBLE, 
nMbLon DOUBLE, 
nStyleId INT,
nCatId INT,
szSearch TEXT,
nlatMin double,
nlatMax double,
nlonMin double,
nlonMax double,
-- nLikeMax int,
nOffset int,
nLimit int)
BEGIN

declare nDOW int default 0;
declare nLikeMax int default 0;


if nOffset = 0 then
# crunch ExpLastSeen recs.
call HLCrunchExpLastSeenV4(nMBId);

End If;

# get DOW based on tz offset and utc_date
set nDOW = HLGetDOWForMember(nMBId);

set nLikeMax = HLGetMaxLikes();

set @rowNum = nOffset;

select *, @rowNum := @rowNum + 1  as orderPosition
from
(

select
    getDistance(PL_Lat, PL_Lon, nMbLat, nMbLon) AS distance, 
    getExpLikeCount(EX_Id) AS likeCount, 
    EX_MB_Id, 
    EX_SpecificTime, 
    EX_Modified,
    EX_Category, 
    EX_IM_Id,
    EX_Vid_Id,
    EX_Id, 
    EX_Description, 
    HLGetCommentCountByExpId(EX_Id), 
    CA_Name, 
    CA_Parent, 
    PL_Region, 
    PL_Locality, 
    PL_lat, 
    PL_lon, 
    PL_location, 
    PL_Neighborhood, 
    PL_PostCode, 
    PL_Name, 
    PL_A1, 
    PL_A2, 
    PL_City, 
    PL_Country, 
    PL_x, 
    PL_y, 
    PL_Id, 
    PL_DealUrl, 
    PL_DealDescription,
    HLGetExpCountByPlace(EX_Place_PL_Id) AS ExpByPlace,

    # member
    MB_Id,
    MB_Name,
    MB_Surname,
    MB_InterestRaw,
    MB_PrimaryPicture_IM_Id,
    MB_CurrentRank,
    
    # These fields aren't access by the caller. Debugging.
    HLGetTODFactor(nTOD, nDOW, CA_TODDOW) as TODFactor,
    getDistanceFactor(PL_Lat, PL_Lon, nMbLat, nMbLon, RAD_Distance_M / 1000) as df,
    ML_Relavency,
    ML_TimeLastSeenFactor,
    InterestSimilarity,

    now() as orderTimestamp

from
    (
        Select #Distinct
            EX_Id as ML_EX_Id,
                (
                    ((HLGetARGFromCatAndMembers(CA_ARG, HLAgeOfMember(EX_MB_Id), MB_Maritus_Status, MB_Sex, nMemberAge, szMemberRelStatus, nMemberGender) + 3) / 6)

                ) / 2 -- 5
             + 
            HLGetRecencyFactorV4(EX_SpecificTime)
            as ML_Relavency,
            (IV1.I0 * IV1.I0 + IV0.I1 * IV1.I1 + IV0.I2 * IV1.I2 + IV0.I3 * IV1.I3 + IV0.I4 * IV1.I4 + 
            IV0.I5 * IV1.I5 + IV0.I6 * IV1.I6 + IV0.I7 * IV1.I7 + IV0.I8 * IV1.I8 + IV0.I9 * IV1.I9 +
            IV0.I10 * IV1.I10 + IV0.I11 * IV1.I11 + IV0.I12 * IV1.I12 + IV0.I13 * IV1.I13 + IV0.I14 * IV1.I14 + 
            IV0.I15 * IV1.I15 + IV0.I16 * IV1.I16 + IV0.I17 * IV1.I17 + IV0.I18 * IV1.I18 + IV0.I19 * IV1.I19 +
            IV0.I20 * IV1.I20 + IV0.I21 * IV1.I21 + IV0.I22 * IV1.I22 + IV0.I23 * IV1.I23 + IV0.I24 * IV1.I24) as InterestSimilarity,
            HLGetLastSeenFactor(ES_LastSeen) as ML_TimeLastSeenFactor
            
            
    
        from Experience 
            join Members MC ON EX_MB_Id = MB_Id # the member is the creator
            join Places ON EX_Place_PL_Id = PL_Id
            join Category ON EX_Category = CA_ID
            left join ExperienceLastSeen ON EX_Id = ES_EX_Id and  nMbId = ES_MB_Id

        where
            
            EX_ModerationStatus In ('Display', 'Check') and
            EX_MB_Id <> nMbId and # not created by member
            (EX_ExpiryTime > CURRENT_TIMESTAMP OR EX_ExpiryTime IS NULL) and
            false = HLGetIsExperienceLikedByMember(EX_Id, nMBId) and

            # this should be a 100km radius:
            PL_Lat >= nLatMin and PL_Lat <= nLatMax and 
            PL_Lon >= nLonMin and PL_Lon <= nLonMax and 

            # any common interests with creator
            #nMemberInts & MB_Interests and
            nMemberInts & CA_InterestNumber and
           
            # calc similarity of interest vectors and make sure its above some threshold 
            (IV1.I0 * IV1.I0 + IV0.I1 * IV1.I1 + IV0.I2 * IV1.I2 + IV0.I3 * IV1.I3 + IV0.I4 * IV1.I4 + 
            IV0.I5 * IV1.I5 + IV0.I6 * IV1.I6 + IV0.I7 * IV1.I7 + IV0.I8 * IV1.I8 + IV0.I9 * IV1.I9 +
            IV0.I10 * IV1.I10 + IV0.I11 * IV1.I11 + IV0.I12 * IV1.I12 + IV0.I13 * IV1.I13 + IV0.I14 * IV1.I14 + 
            IV0.I15 * IV1.I15 + IV0.I16 * IV1.I16 + IV0.I17 * IV1.I17 + IV0.I18 * IV1.I18 + IV0.I19 * IV1.I19 +
            IV0.I20 * IV1.I20 + IV0.I21 * IV1.I21 + IV0.I22 * IV1.I22 + IV0.I23 * IV1.I23 + IV0.I24 * IV1.I24) > 0.62


    ) AS MLIST

    JOIN Experience ON ML_EX_Id = EX_Id
    JOIN Members MC ON EX_MB_Id = MB_Id # the member is the creator
    JOIN InterestVector as IV0 ON EX_MB_Id = IV0.IV_MB_Id 
    JOIN InterestVector as IV1 ON nMbId = IV1.IV_MB_Id 
    JOIN Places ON EX_Place_PL_Id = PL_Id
    JOIN Category ON EX_Category = CA_ID
    JOIN Radii on RAD_Layer = CA_RadiusLayer # there will be a region id specified as well.

    
order by
((df + ML_TimeLastSeenFactor) * 0.75) + ML_Relavency desc

) as realTimeExps
    
limit
    nOffset, nLimit;

END $$
DELIMITER ;
