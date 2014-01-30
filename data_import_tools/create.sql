---drop table input CASCADE;
create table input(
	Family 	text,
	Subfamily 	text,
	Genus	text,
	Species	text,	
	DeterminedBy	text,	
	ZoogeoRegion	text,
	ZoogeoCode	text,
	CountryCode	text,
	Country	text,
	Province	text,
	Station	text,
	OrigCountry		text,
	OrigProvince	text,
	OrigStation	text,
	Date	text,
	Day	integer,
	Month	integer,
	Year	integer,
	Legit	text,
	Ex	text,
	Size	text,
	Filename	text,
	View	text,
	Box	text,
	OrigPhotos	text,
	Remarks	text,
	Line	integer,
	primary key(Line)
);
COPY input FROM '/home/aheugheb/db2/OpenUp/RBINS/Photos IRSNB 03-05-2012.csv' NULL AS '' DELIMITER E';' HEADER CSV;

select * from (select filename, count(*) as count, array_accum(line) as lines from input  group by filename) as tmp where count > 1 ;
alter table input add unique (filename);

drop table images;
create table images(
	id integer,
	family	text,
	subdir	text,
	filename	text,
	genus	text,
	subgenus	text,
	species	text,
	subspecies	text,
	extra	text,
	image	text,
	copie	text,
	extension text,
	primary key (id)
);
COPY images FROM '/home/aheugheb/db2/OpenUp/RBINS/walk.csv' NULL AS '' DELIMITER E';' HEADER CSV;

alter table images add unique (filename);
update images set genus=split_part(filename, ' ', 1), species=split_part(filename, ' ', 2), subspecies=split_part(filename, ' ', 3),
	image=split_part(split_part(filename, ' ', 4), '.', 1), extension=split_part(split_part(filename, ' ', 4), '.', 2)
	where id=403;
update images set genus=split_part(filename, ' ', 1), species=split_part(filename, ' ', 2), 
	extra=split_part(split_part(filename, ' ', 3), '.', 1), extension=split_part(split_part(filename, ' ', 3), '.', 2)
	where id=2120;	

update input set filename = (select filename from images where id=403) where line =378
	 
select * from images where filename not in (select filename from input);
select * from input where filename not in (select filename from images);

select i.line, i.genus as tableGenus, p.genus as imageGenus, (split_part(i.genus, ' ', 1) = p.genus) as sameGenus, 
i.species as tableSpecies, p.species as imageSpecies, (split_part(i.species, ' ', 1) = p.species) as sameSpecies  from input i
join images p on p.filename=i.filename 
where split_part(i.genus, ' ', 1) != p.genus or split_part(i.species, ' ', 1) != p.species 
order by line;

create schema meta; 

DROP TABLE IF EXISTS meta.abcdmetadata;
CREATE TABLE meta.abcdmetadata (
	    "MetadataID" INTEGER,
	    "DatasetGUID" TEXT,
	    "TechnicalContactName" TEXT,
	    "TechnicalContactEmail" TEXT,
	    "TechnicalContactPhone" TEXT,
	    "TechnicalContactAddress" TEXT,
	    "ContentContactName" TEXT,
	    "ContentContactEmail" TEXT,
	    "ContentContactPhone" TEXT,
	    "ContentContactAddress" TEXT,
	    "OtherProviderUDDI" TEXT,
	    "DatasetTitle" TEXT,
	    "DatasetDetails" TEXT,
	    "DatasetCoverage" TEXT,
	    "DatasetURI" TEXT,
	    "DatasetIconURI" TEXT,
	    "DatasetVersionMajor" INTEGER,
	    "DatasetVersionMinor" INTEGER,
	    "DatasetCreators" TEXT,
	    "DatasetContributors" TEXT,
	    "DateCreated" TIMESTAMP,
	    "DateModified" TIMESTAMP,
	    "OwnerOrganizationName" TEXT,
	    "OwnerOrganizationAbbrev" TEXT,
	    "OwnerContactPerson" TEXT,
	    "OwnerContactRole" TEXT,
	    "OwnerAddress" TEXT,
	    "OwnerTelephone" TEXT,
	    "OwnerEmail" TEXT,
	    "OwnerURI" TEXT,
	    "OwnerLogoURI" TEXT,
	    "IPRText" TEXT,
	    "IPRDetails" TEXT,
	    "IPRURI" TEXT,
	    "CopyrightText" TEXT,
	    "CopyrightDetails" TEXT,
	    "CopyrightURI" TEXT,
	    "TermsOfUseText" TEXT,
	    "TermsOfUseDetails" TEXT,
	    "TermsOfUseURI" TEXT,
	    "DisclaimersText" TEXT,
	    "DisclaimersDetails" TEXT,
	    "DisclaimersURI" TEXT,
	    "LicenseText" TEXT,
	    "LicensesDetails" TEXT,
	    "LicenseURI" TEXT,
	    "AcknowledgementsText" TEXT,
	    "AcknowledgementsDetails" TEXT,
	    "AcknowledgementsURI" TEXT,
	    "CitationsText" TEXT,
	    "CitationsDetails" TEXT,
	    "CitationsURI" TEXT,
	    "SourceInstitutionID" TEXT,
	    "SourceID" TEXT,
	    "RecordBasis" TEXT,
	    "KindOfUnit" TEXT
	);

INSERT INTO meta.abcdmetadata("MetadataID","DatasetGUID","TechnicalContactName","TechnicalContactEmail","TechnicalContactPhone","TechnicalContactAddress",
		"ContentContactName","ContentContactEmail","ContentContactPhone","ContentContactAddress","OtherProviderUDDI",
		"DatasetTitle","DatasetDetails","DatasetCoverage","DatasetURI","DatasetIconURI","DatasetVersionMajor","DatasetVersionMinor","DatasetCreators","DatasetContributors","DateCreated","DateModified",
		"OwnerOrganizationName","OwnerOrganizationAbbrev","OwnerContactPerson","OwnerContactRole","OwnerAddress","OwnerTelephone","OwnerEmail","OwnerURI","OwnerLogoURI",
		"IPRText","IPRDetails","IPRURI","CopyrightText","CopyrightDetails","CopyrightURI","TermsOfUseText","TermsOfUseDetails","TermsOfUseURI","DisclaimersText","DisclaimersDetails","DisclaimersURI","LicenseText","LicensesDetails","LicenseURI",
		"AcknowledgementsText","AcknowledgementsDetails","AcknowledgementsURI","CitationsText","CitationsDetails","CitationsURI",
		"SourceInstitutionID","SourceID","RecordBasis","KindOfUnit")
VALUES(1,NULL,E'Andre Heughebaert',E'aheugheb@ulb.ac.be',E'+32 2650 5751',E'Belgian Biodiversity Platform, ULB Campus de la Plaine, CP 257, Bld du Triomphe, B1050 Brussels, Belgium',
		E'Patrick Grootaert',E'Patrick.Grootaert@naturalsciences.be',E'+32 2627 4302',E'Royal Belgian Institute of Natural Sciences, Vautierstreet 29, B-1000 Brussels, Belgium',NULL,
		E'RBINS-OpenUp',E'This dataset is the RBINS contribution to OpenUp! project. It provides 4.000+ images of various Coleoptera with associated details.',E'This database covers various families of the Coleoptera order.',E'http://biocase.biodiversity.be',E'',1,0,E'Andre Heughebaert',E'RBINS',E'2012-05-09 00:00:00',E'2012-05-12 00:00:00',
		E'RBINS',E'RBINS',E'Patrick Grootaert',E'Director',E'Royal Belgian Institute of Natural Sciences, Vautierstreet 29, B-1000 Brussels, Belgium',E'+32 2627 4302',E'Patrick.Grootaert@naturalsciences.be',E'http://www.rbins.be',E'http://www.kbinirsnb.be/layout_images/logo',
		E'IPR ...',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,
		E'RBINS',E'RBINS-OpenUp',E'PreservedSpecimen',E'wholeorganisms');

alter table meta.abcdmetadata add column language TEXT default 'EN EN-US';

create schema rbins; 

---drop table rbins.photos cascade;
create table rbins.photos(
	id integer primary key, -- PhotoID
	ScientificName	varchar(255) not null, -- images
	TypifiedName	varchar(255) not null, -- images
	Family			varchar(64) not null, -- images
	SubFamily		varchar(64) not null, -- images
	Genus 			varchar(64) not null, -- images
	Species			varchar(64) not null, -- images
	SubSpecies 		varchar(64), -- images
	ZooGeoRegion	varchar(2), -- Excel G
	CountryCode		varchar(2),	-- Excel H
	Country			varchar(64),-- Excel I
	Province		varchar(64),-- Excel J
	Station			varchar(64),-- Excel K
	Date			varchar(16),-- from Excel P,Q,R
	filename		varchar(255), -- Excel V
	view			varchar(64), -- Excel W
	fileURI			varchar(255), -- 
	origPathname text,	--images
	origFamily text, -- Excel A
	origSubfamily text,	-- Excel B
	origGenus text, -- Excel C
	origSpecies text, -- Excel D
	origDeterminedBy	text, -- Excel E
	origZooGeoRegion text, -- Excel F
	origCountry text, -- Excel L
	origProvince text, -- Excel M
	origStation text, -- Excel N
	origDate text, -- Excel O
	origDay text, -- Excel P
	origMonth text, -- Excel Q
	origYear text, -- Excel R
	origLegit text, -- Excel S
	origEx	text, -- Excel T
	origSize text, -- Excel U
	origPhotos text, -- Excel X
	origBox	text, -- Excel Y
	origRemarks text, -- Excel Z
	origLine integer -- Excel AA
);


insert into rbins.photos 
		select i.id, 
		i.genus || ' ' || i.species || coalesce (' ' || i.subspecies, '') as scientificName,
		i.genus || ' ' || i.species || coalesce (' ' || i.subspecies, '') || coalesce (' ' || i.extra, '')  as typifiedName,
		btrim(split_part(i.family, ',', 1), ' ') as family, 
		btrim(split_part(i.family, ',', 2), ' ') as subfamily, 
		i.genus, i.species, i.subspecies, e.ZoogeoCode, e.CountryCode, e.Country, e.Province, e.Station,
		case 
		when e.day is null and e.month is null then to_char(e.year, 'FM9999')
		when e.day is null then to_char(e.month, 'FM09') || '/' || to_char(e.year, 'FM9999')
		else to_char(e.day, 'FM09') || '/' || to_char(e.month, 'FM09') || '/' || to_char(e.year, 'FM9999') end as date,
		i.filename, e.view, 
		'http://projects.biodiversity.be/openup/rbins/' || i.id::text || '.jpg' as fileURI,
		case
		when i.subdir is NULL then i.family || '/' || i.filename
		else  i.family || '/' || i.subdir ||'/' ||i.filename end as origPathname,
		e.family, e.genus, e.subfamily, e.species, e.determinedby, e.ZoogeoRegion, e.origCountry, e.origProvince, e.origStation, 
		e.date, e.day, e.month, e.year, e.legit, e.ex, e.size, e.origPhotos, e.box, e.remarks, e.line
		from images i left join input e on e.filename=i.filename
		order by id;

create or replace view rbinsmetadata as
	select * from meta.abcdmetadata where "MetadataID"=1;	
	
create or replace view rbinsPhotos as
	select 
		id as UnitID,
		'image/jpeg'::text as Format,
		'http://creativecommons.org/licenses/by-sa/3.0/'::text as LicenseURI,
		fileURI,
		scientificName,
		typifiedName,
		Family,
		SubFamily,
		Genus,
		Species,
		SubSpecies,
		ZooGeoRegion,
		CountryCode,
		Country,
		Province,
		Station,
		Date as eventDate,
		view
		from rbins.photos where origLine is not null;
