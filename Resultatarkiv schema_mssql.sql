USE [master]
GO
/****** Object:  Database [DataArkiv]    Script Date: 11.04.2018 07:41:12 ******/
CREATE DATABASE [DataArkiv]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'DataArkiv', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL11.MSSQLSERVER2\MSSQL\DATA\DataArkiv.mdf' , SIZE = 307200KB , MAXSIZE = 307200KB , FILEGROWTH = 1024KB )
 LOG ON 
( NAME = N'DataArkiv_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL11.MSSQLSERVER2\MSSQL\Data\DataArkiv_log.ldf' , SIZE = 200512KB , MAXSIZE = 2048GB , FILEGROWTH = 10%)
GO
ALTER DATABASE [DataArkiv] SET COMPATIBILITY_LEVEL = 110
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [DataArkiv].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [DataArkiv] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [DataArkiv] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [DataArkiv] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [DataArkiv] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [DataArkiv] SET ARITHABORT OFF 
GO
ALTER DATABASE [DataArkiv] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [DataArkiv] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [DataArkiv] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [DataArkiv] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [DataArkiv] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [DataArkiv] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [DataArkiv] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [DataArkiv] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [DataArkiv] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [DataArkiv] SET  DISABLE_BROKER 
GO
ALTER DATABASE [DataArkiv] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [DataArkiv] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [DataArkiv] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [DataArkiv] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [DataArkiv] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [DataArkiv] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [DataArkiv] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [DataArkiv] SET RECOVERY FULL 
GO
ALTER DATABASE [DataArkiv] SET  MULTI_USER 
GO
ALTER DATABASE [DataArkiv] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [DataArkiv] SET DB_CHAINING OFF 
GO
ALTER DATABASE [DataArkiv] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [DataArkiv] SET TARGET_RECOVERY_TIME = 0 SECONDS 
GO
USE [DataArkiv]
GO
/****** Object:  User [NRPA\mortens]    Script Date: 11.04.2018 07:41:12 ******/
CREATE USER [NRPA\mortens] FOR LOGIN [NRPA\mortens] WITH DEFAULT_SCHEMA=[dbo]
GO
/****** Object:  User [NRPA\DataArkiv-R]    Script Date: 11.04.2018 07:41:12 ******/
CREATE USER [NRPA\DataArkiv-R] FOR LOGIN [NRPA\DataArkiv-R]
GO
/****** Object:  User [NRPA\DataArkiv-A]    Script Date: 11.04.2018 07:41:12 ******/
CREATE USER [NRPA\DataArkiv-A] FOR LOGIN [NRPA\DataArkiv-A]
GO
/****** Object:  User [NRPA\Alle Sammen]    Script Date: 11.04.2018 07:41:12 ******/
CREATE USER [NRPA\Alle Sammen] FOR LOGIN [NRPA\Alle Sammen] WITH DEFAULT_SCHEMA=[dbo]
GO
ALTER ROLE [db_owner] ADD MEMBER [NRPA\mortens]
GO
ALTER ROLE [db_datareader] ADD MEMBER [NRPA\mortens]
GO
ALTER ROLE [db_datawriter] ADD MEMBER [NRPA\mortens]
GO
ALTER ROLE [db_datareader] ADD MEMBER [NRPA\DataArkiv-R]
GO
ALTER ROLE [db_owner] ADD MEMBER [NRPA\DataArkiv-A]
GO
ALTER ROLE [db_datareader] ADD MEMBER [NRPA\Alle Sammen]
GO
/****** Object:  UserDefinedFunction [dbo].[ReturnAreaGeom]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

Create FUNCTION [dbo].[ReturnAreaGeom]
(
    @geoid int
 
)
RETURNS geometry
AS
BEGIN
    Declare @geo_area geometry;
    SELECT @geo_area = va.ogr_geometry from GeoAreas As va
    where va.ogr_fid = @geoid

    RETURN  @geo_area

END



GO
/****** Object:  UserDefinedFunction [dbo].[ReturnAreaID]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
Create FUNCTION [dbo].[ReturnAreaID]
(
    @varname varchar(50),
    @vartype varchar(50)
)
RETURNS int
AS
BEGIN
    Declare @varid int;
    SELECT @varid = va.ogr_fid from GeoAreas As va
    where va.areaid = @varname AND va.objtype = @vartype

    RETURN  @varid

END


GO
/****** Object:  UserDefinedFunction [dbo].[ReturnMetadataID]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO


CREATE FUNCTION [dbo].[ReturnMetadataID]
(
    @varname varchar(50)
)
RETURNS int
AS
BEGIN
    Declare @varid int;
    SELECT @varid = va.id from MetadataList As va
    where va.shortname = @varname

    RETURN  @varid

END




GO
/****** Object:  UserDefinedFunction [dbo].[ReturnNuclideID]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE FUNCTION [dbo].[ReturnNuclideID]
(
    @varname varchar(50)
)
RETURNS int
AS
BEGIN
    Declare @varid int;
    SELECT @varid = va.id from NuclideList As va
    where va.shortname = @varname

    RETURN  @varid

END



GO
/****** Object:  UserDefinedFunction [dbo].[ReturnQuantityID]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE FUNCTION [dbo].[ReturnQuantityID]
(
    @varname varchar(50)
)
RETURNS int
AS
BEGIN
    Declare @varid int;
    SELECT @varid = va.id from QuantityList As va
    where va.shortname = @varname

    RETURN  @varid

END



GO
/****** Object:  UserDefinedFunction [dbo].[ReturnSampletypeID]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO


CREATE FUNCTION [dbo].[ReturnSampletypeID]
(
    @varname varchar(50)
)
RETURNS int
AS
BEGIN
    Declare @varid int;
    SELECT @varid = va.id from SampletypeList As va
    where va.shortname = @varname

    RETURN  @varid

END




GO
/****** Object:  UserDefinedFunction [dbo].[ReturnVarID]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE FUNCTION [dbo].[ReturnVarID]
(
    @varname varchar(50)
)
RETURNS int
AS
BEGIN
    Declare @varid int;
    SELECT @varid = va.id from UnitList As va
    where va.shortname = @varname

    RETURN  @varid

END


GO
/****** Object:  UserDefinedFunction [dbo].[SampletypeName]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO


CREATE FUNCTION [dbo].[SampletypeName]
(
    @id int
)
RETURNS nvarchar(MAX)
AS
BEGIN
    Declare @varname nvarchar(MAX)
    SELECT @varname = t.name from SampletypeList As t
    where t.id = @id

    RETURN  @varname

END




GO
/****** Object:  UserDefinedFunction [dbo].[SpeciesName]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO


CREATE FUNCTION [dbo].[SpeciesName]
(
    @id int
)
RETURNS nvarchar(MAX)
AS
BEGIN
    Declare @varname nvarchar(MAX)
    SELECT @varname = t.species_no from SpeciesList As t
    where t.id = @id

    RETURN  @varname

END




GO
/****** Object:  Table [dbo].[BasisPropertiesList]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[BasisPropertiesList](
	[id] [int] IDENTITY(1000,1) NOT NULL,
	[name] [nvarchar](50) NULL,
	[shortname] [nvarchar](50) NULL,
	[datatype] [nvarchar](50) NULL,
	[decription] [text] NULL,
	[format] [nvarchar](50) NULL,
	[attrtype] [nvarchar](50) NULL,
 CONSTRAINT [PK_BasisPropertiesList] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO
/****** Object:  Table [dbo].[GeoAreas]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[GeoAreas](
	[ogr_fid] [int] IDENTITY(1,1) NOT NULL,
	[ogr_geometry] [geometry] NULL,
	[areaid] [nvarchar](12) NULL,
	[name] [nvarchar](100) NULL,
	[objtype] [nvarchar](12) NULL,
	[centroid] [geometry] NULL,
 CONSTRAINT [PK_kommuner] PRIMARY KEY CLUSTERED 
(
	[ogr_fid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO
/****** Object:  Table [dbo].[geometry_columns]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_PADDING ON
GO
CREATE TABLE [dbo].[geometry_columns](
	[f_table_catalog] [varchar](128) NOT NULL,
	[f_table_schema] [varchar](128) NOT NULL,
	[f_table_name] [varchar](256) NOT NULL,
	[f_geometry_column] [varchar](256) NOT NULL,
	[coord_dimension] [int] NOT NULL,
	[srid] [int] NOT NULL,
	[geometry_type] [varchar](30) NOT NULL,
 CONSTRAINT [geometry_columns_pk] PRIMARY KEY CLUSTERED 
(
	[f_table_catalog] ASC,
	[f_table_schema] ASC,
	[f_table_name] ASC,
	[f_geometry_column] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
SET ANSI_PADDING OFF
GO
/****** Object:  Table [dbo].[HabitatList]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[HabitatList](
	[id] [int] NOT NULL,
	[name] [nvarchar](200) NULL,
 CONSTRAINT [PK_HabitatList] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[MetadataList]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_PADDING ON
GO
CREATE TABLE [dbo].[MetadataList](
	[id] [int] IDENTITY(1000,1) NOT NULL,
	[name] [varchar](max) NULL,
	[shortname] [varchar](50) NULL,
	[description] [varchar](max) NULL,
 CONSTRAINT [PK_MetadataList] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO
SET ANSI_PADDING OFF
GO
/****** Object:  Table [dbo].[NuclideList]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_PADDING ON
GO
CREATE TABLE [dbo].[NuclideList](
	[id] [int] IDENTITY(1000,1) NOT NULL,
	[name] [varchar](50) NULL,
	[shortname] [varchar](50) NULL,
	[halflife] [float] NULL,
 CONSTRAINT [PK_NuclideList] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
SET ANSI_PADDING OFF
GO
/****** Object:  Table [dbo].[Projects]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Projects](
	[id] [int] NOT NULL,
	[name] [nvarchar](100) NULL,
	[contact] [nvarchar](50) NULL,
	[description] [text] NULL,
	[dataowner] [nvarchar](50) NULL,
	[restrictions] [text] NULL,
	[viewname] [nvarchar](50) NULL,
 CONSTRAINT [PK__Monitori__3213E83FAC06D7CB] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO
/****** Object:  Table [dbo].[ProjectTopics]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ProjectTopics](
	[projectid] [int] NOT NULL,
	[topicid] [int] NOT NULL,
 CONSTRAINT [PK_ProjectTopics] PRIMARY KEY CLUSTERED 
(
	[projectid] ASC,
	[topicid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
/****** Object:  Table [dbo].[QuantityList]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[QuantityList](
	[id] [int] IDENTITY(1000,1) NOT NULL,
	[name] [nvarchar](50) NOT NULL,
	[shortname] [nvarchar](20) NOT NULL,
	[description] [text] NULL,
 CONSTRAINT [PK__Quantity__3213E83F33C54365] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO
/****** Object:  Table [dbo].[Sample]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Sample](
	[id] [int] IDENTITY(1000,1) NOT NULL,
	[projectid] [int] NOT NULL,
	[reftime] [datetime] NULL,
	[sampletype] [int] NULL,
	[areaid] [int] NULL,
	[comment] [nvarchar](max) NULL,
	[speciesid] [int] NULL,
	[samplestart] [datetime] NULL,
	[samplestop] [datetime] NULL,
	[parentsampleid] [int] NULL,
	[location] [geometry] NULL,
	[sample_date] [datetime] NULL,
 CONSTRAINT [PK__Sample__3213E83F5EBFF1AF] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO
/****** Object:  Table [dbo].[SampleCatList]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[SampleCatList](
	[id] [int] NOT NULL,
	[name] [nvarchar](200) NULL,
	[description] [ntext] NULL,
 CONSTRAINT [PK_SampleCatList] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO
/****** Object:  Table [dbo].[SampleMetadata]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_PADDING ON
GO
CREATE TABLE [dbo].[SampleMetadata](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[sampleid] [int] NOT NULL,
	[varname] [nchar](10) NULL,
	[value] [varchar](max) NULL,
	[metadataid] [int] NULL,
 CONSTRAINT [PK_SampleMetadata] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO
SET ANSI_PADDING OFF
GO
/****** Object:  Table [dbo].[SampletypeList]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_PADDING ON
GO
CREATE TABLE [dbo].[SampletypeList](
	[id] [int] IDENTITY(1000,1) NOT NULL,
	[name] [varchar](max) NULL,
	[shortname] [varchar](50) NOT NULL,
	[description] [text] NULL,
	[samplecatid] [int] NOT NULL,
	[samplesubtype] [text] NULL,
 CONSTRAINT [PK_SampletypeList] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO
SET ANSI_PADDING OFF
GO
/****** Object:  Table [dbo].[SampleValue]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[SampleValue](
	[id] [int] IDENTITY(1000,1) NOT NULL,
	[sampleid] [int] NOT NULL,
	[value] [float] NULL,
	[unitid] [int] NULL,
	[unc_value] [float] NULL,
	[unc_unitid] [int] NULL,
	[mda_value] [float] NULL,
	[mda_unitid] [int] NULL,
	[laboratory] [nvarchar](max) NULL,
	[comment] [text] NULL,
	[quantityid] [int] NULL,
	[nuclideid] [int] NULL,
	[instrument] [nvarchar](50) NULL,
	[uncmeasure] [nvarchar](50) NULL,
	[below_mda] [smallint] NULL,
 CONSTRAINT [PK__SampleVa__3213E83F242D082B] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO
/****** Object:  Table [dbo].[spatial_ref_sys]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_PADDING ON
GO
CREATE TABLE [dbo].[spatial_ref_sys](
	[srid] [int] NOT NULL,
	[auth_name] [varchar](256) NULL,
	[auth_srid] [int] NULL,
	[srtext] [varchar](2048) NULL,
	[proj4text] [varchar](2048) NULL,
PRIMARY KEY CLUSTERED 
(
	[srid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
SET ANSI_PADDING OFF
GO
/****** Object:  Table [dbo].[SpeciesList]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[SpeciesList](
	[id] [int] NOT NULL,
	[species_no] [text] NULL,
	[species_lat] [text] NULL,
	[species_en] [text] NULL,
	[habitatid] [int] NULL,
	[sampletypeid] [int] NULL,
 CONSTRAINT [PK_species] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO
/****** Object:  Table [dbo].[TopicList]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[TopicList](
	[id] [int] NOT NULL,
	[name] [nvarchar](200) NOT NULL,
	[description] [ntext] NULL,
 CONSTRAINT [PK_SubProgram] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO
/****** Object:  Table [dbo].[UnitList]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[UnitList](
	[id] [int] IDENTITY(1000,1) NOT NULL,
	[unit] [nvarchar](20) NOT NULL,
	[baseunit] [int] NULL,
	[name] [nvarchar](50) NOT NULL,
	[shortname] [nvarchar](20) NOT NULL,
	[desciption] [text] NULL,
 CONSTRAINT [PK__ValueUni__3213E83F33C54365] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO
/****** Object:  View [dbo].[metadata]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE VIEW [dbo].[metadata] AS
SELECT s.projectid as projectid, s.id as sampleid, ml.shortname as shortname, sm.value as value, NULL as unit 
FROM SampleMetadata sm, Sample s, MetadataList ml
WHERE sm.sampleid=s.id and ml.id=sm.metadataid

GO
/****** Object:  View [dbo].[nuclidedata]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[nuclidedata] AS
SELECT s.projectid as projectid, s.id as sampleid, nl.shortname+'_'+vu.shortname as shortname, sv.value as value, vu.unit as unit 
FROM SampleValue sv, Sample S, UnitList vu,nuclidelist nl
where sv.sampleid=s.id AND nl.id = sv.nuclideid AND vu.id=sv.unitid
UNION
SELECT s.projectid as projectid, s.id as sampleid, rtrim(nl.shortname+'_'+vu.shortname)+'_unc' as shortname, sv.unc_value as value, vu.unit as unit 
FROM SampleValue sv, Sample S, UnitList vu,nuclidelist nl
where sv.sampleid=s.id AND nl.id = sv.nuclideid AND vu.id=sv.unitid
UNION
SELECT s.projectid as projectid, s.id as sampleid, rtrim(nl.shortname+'_'+vu.shortname)+'_mda' as shortname, sv.mda_value as value, vu.unit as unit 
FROM SampleValue sv, Sample S, UnitList vu,nuclidelist nl
where sv.sampleid=s.id AND nl.id = sv.nuclideid AND vu.id=sv.unitid
GO
/****** Object:  View [dbo].[nuclidedataprop]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[nuclidedataprop] AS
SELECT s.projectid as projectid, s.id as sampleid, rtrim(nl.shortname+'_'+vu.shortname)+'_lab' as shortname, sv.laboratory as value, NULL as unit 
FROM SampleValue sv, Sample S, nuclidelist nl, UnitList vu
where sv.sampleid=s.id AND nl.id = sv.nuclideid AND vu.id=sv.unitid AND sv.laboratory is not null
union
SELECT s.projectid as projectid, s.id as sampleid, rtrim(nl.shortname+'_'+vu.shortname)+'_uncmeasure' as shortname, sv.uncmeasure as value, NULL as unit 
FROM SampleValue sv, Sample S, nuclidelist nl, UnitList vu
where sv.sampleid=s.id AND nl.id = sv.nuclideid AND vu.id=sv.unitid AND sv.uncmeasure is not null
union
SELECT s.projectid as projectid, s.id as sampleid, rtrim(nl.shortname+'_'+vu.shortname)+'_instrument' as shortname, sv.instrument as value, NULL as unit 
FROM SampleValue sv, Sample S, nuclidelist nl, UnitList vu
where sv.sampleid=s.id AND nl.id = sv.nuclideid AND vu.id=sv.unitid AND sv.instrument is not null
GO
/****** Object:  View [dbo].[Matkurven]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[Matkurven] AS SELECT id, geometry::STGeomFromText(location, 4326) as location,latitude,longitude,dbo.ReturnAreaGeom(area) as area,reftime,samplestart,samplestop,parentsampleid,comment,sampletype,sampletypename,speciesid,speciesname,[BRAND],[LOCALITY],[MUNICIPALITY],[SAMPLEPART],[SAMPLESUBTYPE],[CS134_BQ_KG_WET],[CS134_BQ_KG_WET_mda],[CS134_BQ_KG_WET_unc],[CS137_BQ_KG_WET],[CS137_BQ_KG_WET_mda],[CS137_BQ_KG_WET_unc],[CS137_BQ_KG_WET_lab] FROM (
		SELECT s.id,s.location.STAsText() as location,s.location.STY as latitude,s.location.STX as longitude, s.areaid as area,s.reftime,s.samplestart,s.samplestop,s.parentsampleid,s.comment,s.sampletype,dbo.sampletypename(s.sampletype) as sampletypename,s.speciesid,dbo.speciesname(s.speciesid) as speciesname, md.shortname as metaname, md.value as metavalue,nd.shortname as nuclidename, nd.value as nuclidevalue,pr.shortname as propname, pr.value as propvalue
		FROM Sample s
		
		LEFT JOIN metadata md on s.id=md.sampleid
		LEFT JOIN nuclidedata nd on s.id=nd.sampleid
		LEFT JOIN nuclidedataprop pr on s.id=pr.sampleid

		where s.projectid=2
		) x 
		PIVOT (max(nuclidevalue) for nuclidename in ([CS134_BQ_KG_WET],[CS134_BQ_KG_WET_mda],[CS134_BQ_KG_WET_unc],[CS137_BQ_KG_WET],[CS137_BQ_KG_WET_mda],[CS137_BQ_KG_WET_unc])) AS nucl
		
		PIVOT (max(propvalue) for propname in ([CS137_BQ_KG_WET_lab])) AS prop
		PIVOT (max(metavalue) for metaname in ([BRAND],[LOCALITY],[MUNICIPALITY],[SAMPLEPART],[SAMPLESUBTYPE])) AS meta
GO
/****** Object:  View [dbo].[valuedata]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[valuedata] AS
SELECT s.projectid AS projectid, s.id as sampleid, q.shortname+'_'+vu.shortname as shortname, sv.value as value, vu.unit as unit 
FROM QuantityList q, SampleValue sv, UnitList vu, Sample S 
WHERE s.id=sv.sampleid AND vu.id=sv.unitid AND q.id=sv.quantityid AND sv.nuclideid is null
GO
/****** Object:  View [dbo].[RadioaktivitetVillrein]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[RadioaktivitetVillrein] AS SELECT id, geometry::STGeomFromText(location, 4326) as location,latitude,longitude,dbo.ReturnAreaGeom(area) as area,reftime,samplestart,samplestop,parentsampleid,comment,sampletype,sampletypename,speciesid,speciesname,[DRYWETRATIO_RATIO_DRY],[SLAUGHTERWEIGHT_KILOGRAM],[AGGREGATEDVALUE],[COLLECTOR],[LOCALITY],[MUNICIPALITY],[MUNICIPALITYNR],[REGION],[SAMPLEID],[SAMPLEPART],[CS137_BQ_KG_DRY],[CS137_BQ_KG_DRY_mda],[CS137_BQ_KG_DRY_unc],[CS137_BQ_KG_WET],[CS137_BQ_KG_WET_mda],[CS137_BQ_KG_WET_unc],[CS137_BQ_KG_DRY_lab] FROM (
		SELECT s.id,s.location.STAsText() as location,s.location.STY as latitude,s.location.STX as longitude, s.areaid as area,s.reftime,s.samplestart,s.samplestop,s.parentsampleid,s.comment,s.sampletype,dbo.sampletypename(s.sampletype) as sampletypename,s.speciesid,dbo.speciesname(s.speciesid) as speciesname,vd.shortname as varname, vd.value as varvalue, md.shortname as metaname, md.value as metavalue,nd.shortname as nuclidename, nd.value as nuclidevalue,pr.shortname as propname, pr.value as propvalue
		FROM Sample s
		LEFT JOIN valuedata vd ON s.id=vd.sampleid
		LEFT JOIN metadata md on s.id=md.sampleid
		LEFT JOIN nuclidedata nd on s.id=nd.sampleid
		LEFT JOIN nuclidedataprop pr on s.id=pr.sampleid

		where s.projectid=4
		) x 
		PIVOT (max(nuclidevalue) for nuclidename in ([CS137_BQ_KG_DRY],[CS137_BQ_KG_DRY_mda],[CS137_BQ_KG_DRY_unc],[CS137_BQ_KG_WET],[CS137_BQ_KG_WET_mda],[CS137_BQ_KG_WET_unc])) AS nucl
		PIVOT (max(varvalue) for varname in ([DRYWETRATIO_RATIO_DRY],[SLAUGHTERWEIGHT_KILOGRAM])) AS var
		PIVOT (max(propvalue) for propname in ([CS137_BQ_KG_DRY_lab])) AS prop
		PIVOT (max(metavalue) for metaname in ([AGGREGATEDVALUE],[COLLECTOR],[LOCALITY],[MUNICIPALITY],[MUNICIPALITYNR],[REGION],[SAMPLEID],[SAMPLEPART])) AS meta
GO
/****** Object:  View [dbo].[RAMEKyststasjoner]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[RAMEKyststasjoner] AS SELECT id, geometry::STGeomFromText(location, 4326) as location,latitude,longitude,dbo.ReturnAreaGeom(area) as area,reftime,samplestart,samplestop,parentsampleid,comment,sampletype,sampletypename,speciesid,speciesname,[SALINITY_PERMIL],[SAMPLEWEIGHT_GRAM],[COLLECTOR],[COORDINATEORIGIN],[LIMSNR],[LOCALITY],[SAMPLEDEPTH],[SAMPLEID],[SAMPLEPART],[SAMPLESUBTYPE],[SAMPLINGPROCEDURE],[SEA],[STATION],[AM241_BQ_M3],[AM241_BQ_M3_mda],[AM241_BQ_M3_unc],[CS137_BQ_KG_DRY],[CS137_BQ_KG_DRY_mda],[CS137_BQ_KG_DRY_unc],[CS137_BQ_KG_WET],[CS137_BQ_KG_WET_mda],[CS137_BQ_KG_WET_unc],[CS137_BQ_M3],[CS137_BQ_M3_mda],[CS137_BQ_M3_unc],[K40_BQ_KG_DRY],[K40_BQ_KG_DRY_mda],[K40_BQ_KG_DRY_unc],[PU239_240_BQ_KG_DRY],[PU239_240_BQ_KG_DRY_mda],[PU239_240_BQ_KG_DRY_unc],[PU239_240_BQ_M3],[PU239_240_BQ_M3_mda],[PU239_240_BQ_M3_unc],[SR90_BQ_M3],[SR90_BQ_M3_mda],[SR90_BQ_M3_unc],[TC99_BQ_KG_DRY],[TC99_BQ_KG_DRY_mda],[TC99_BQ_KG_DRY_unc],[TC99_BQ_KG_WET],[TC99_BQ_KG_WET_mda],[TC99_BQ_KG_WET_unc],[TC99_BQ_M3],[TC99_BQ_M3_mda],[TC99_BQ_M3_unc],[AM241_BQ_M3_instrument],[AM241_BQ_M3_lab],[CS137_BQ_KG_DRY_instrument],[CS137_BQ_KG_DRY_lab],[CS137_BQ_KG_WET_lab],[CS137_BQ_M3_lab],[K40_BQ_KG_DRY_lab],[PU239_240_BQ_M3_instrument],[PU239_240_BQ_M3_lab],[SR90_BQ_M3_instrument],[SR90_BQ_M3_lab],[TC99_BQ_KG_DRY_lab],[TC99_BQ_KG_WET_lab],[TC99_BQ_M3_instrument],[TC99_BQ_M3_lab] FROM (
		SELECT s.id,s.location.STAsText() as location,s.location.STY as latitude,s.location.STX as longitude, s.areaid as area,s.reftime,s.samplestart,s.samplestop,s.parentsampleid,s.comment,s.sampletype,dbo.sampletypename(s.sampletype) as sampletypename,s.speciesid,dbo.speciesname(s.speciesid) as speciesname,vd.shortname as varname, vd.value as varvalue, md.shortname as metaname, md.value as metavalue,nd.shortname as nuclidename, nd.value as nuclidevalue,pr.shortname as propname, pr.value as propvalue
		FROM Sample s
		LEFT JOIN valuedata vd ON s.id=vd.sampleid
		LEFT JOIN metadata md on s.id=md.sampleid
		LEFT JOIN nuclidedata nd on s.id=nd.sampleid
		LEFT JOIN nuclidedataprop pr on s.id=pr.sampleid

		where s.projectid=5
		) x 
		PIVOT (max(nuclidevalue) for nuclidename in ([AM241_BQ_M3],[AM241_BQ_M3_mda],[AM241_BQ_M3_unc],[CS137_BQ_KG_DRY],[CS137_BQ_KG_DRY_mda],[CS137_BQ_KG_DRY_unc],[CS137_BQ_KG_WET],[CS137_BQ_KG_WET_mda],[CS137_BQ_KG_WET_unc],[CS137_BQ_M3],[CS137_BQ_M3_mda],[CS137_BQ_M3_unc],[K40_BQ_KG_DRY],[K40_BQ_KG_DRY_mda],[K40_BQ_KG_DRY_unc],[PU239_240_BQ_KG_DRY],[PU239_240_BQ_KG_DRY_mda],[PU239_240_BQ_KG_DRY_unc],[PU239_240_BQ_M3],[PU239_240_BQ_M3_mda],[PU239_240_BQ_M3_unc],[SR90_BQ_M3],[SR90_BQ_M3_mda],[SR90_BQ_M3_unc],[TC99_BQ_KG_DRY],[TC99_BQ_KG_DRY_mda],[TC99_BQ_KG_DRY_unc],[TC99_BQ_KG_WET],[TC99_BQ_KG_WET_mda],[TC99_BQ_KG_WET_unc],[TC99_BQ_M3],[TC99_BQ_M3_mda],[TC99_BQ_M3_unc])) AS nucl
		PIVOT (max(varvalue) for varname in ([SALINITY_PERMIL],[SAMPLEWEIGHT_GRAM])) AS var
		PIVOT (max(propvalue) for propname in ([AM241_BQ_M3_instrument],[AM241_BQ_M3_lab],[CS137_BQ_KG_DRY_instrument],[CS137_BQ_KG_DRY_lab],[CS137_BQ_KG_WET_lab],[CS137_BQ_M3_lab],[K40_BQ_KG_DRY_lab],[PU239_240_BQ_M3_instrument],[PU239_240_BQ_M3_lab],[SR90_BQ_M3_instrument],[SR90_BQ_M3_lab],[TC99_BQ_KG_DRY_lab],[TC99_BQ_KG_WET_lab],[TC99_BQ_M3_instrument],[TC99_BQ_M3_lab])) AS prop
		PIVOT (max(metavalue) for metaname in ([COLLECTOR],[COORDINATEORIGIN],[LIMSNR],[LOCALITY],[SAMPLEDEPTH],[SAMPLEID],[SAMPLEPART],[SAMPLESUBTYPE],[SAMPLINGPROCEDURE],[SEA],[STATION])) AS meta
GO
/****** Object:  View [dbo].[RAMETokt]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[RAMETokt] AS SELECT id, geometry::STGeomFromText(location, 4326) as location,latitude,longitude,dbo.ReturnAreaGeom(area) as area,reftime,samplestart,samplestop,parentsampleid,comment,sampletype,sampletypename,speciesid,speciesname,[SALINITY_PERMIL],[SAMPLECOUNT_NUMBER],[TEMPERATURE_CELSIUS],[WATERDEPTH_METER],[COORDINATEORIGIN],[LIMSNR],[LOCALITY],[SAMPLEDEPTH],[SAMPLEID],[SAMPLEPART],[SAMPLESUBTYPE],[SAMPLINGPROCEDURE],[SEA],[STATION],[VESSEL],[AM241_BQ_M3],[AM241_BQ_M3_mda],[AM241_BQ_M3_unc],[CS137_BQ_KG_DRY],[CS137_BQ_KG_DRY_mda],[CS137_BQ_KG_DRY_unc],[CS137_BQ_KG_WET],[CS137_BQ_KG_WET_mda],[CS137_BQ_KG_WET_unc],[CS137_BQ_M3],[CS137_BQ_M3_mda],[CS137_BQ_M3_unc],[H3_BQ_L],[H3_BQ_L_mda],[H3_BQ_L_unc],[PU239_240_BQ_M3],[PU239_240_BQ_M3_mda],[PU239_240_BQ_M3_unc],[RA226_BQ_FILTER],[RA226_BQ_FILTER_mda],[RA226_BQ_FILTER_unc],[RA226_BQ_M3],[RA226_BQ_M3_mda],[RA226_BQ_M3_unc],[RA228_BQ_FILTER],[RA228_BQ_FILTER_mda],[RA228_BQ_FILTER_unc],[RA228_BQ_M3],[RA228_BQ_M3_mda],[RA228_BQ_M3_unc],[SR90_BQ_M3],[SR90_BQ_M3_mda],[SR90_BQ_M3_unc],[CS137_BQ_KG_DRY_instrument],[CS137_BQ_KG_DRY_lab],[CS137_BQ_KG_WET_lab],[CS137_BQ_M3_lab] FROM (
		SELECT s.id,s.location.STAsText() as location,s.location.STY as latitude,s.location.STX as longitude, s.areaid as area,s.reftime,s.samplestart,s.samplestop,s.parentsampleid,s.comment,s.sampletype,dbo.sampletypename(s.sampletype) as sampletypename,s.speciesid,dbo.speciesname(s.speciesid) as speciesname,vd.shortname as varname, vd.value as varvalue, md.shortname as metaname, md.value as metavalue,nd.shortname as nuclidename, nd.value as nuclidevalue,pr.shortname as propname, pr.value as propvalue
		FROM Sample s
		LEFT JOIN valuedata vd ON s.id=vd.sampleid
		LEFT JOIN metadata md on s.id=md.sampleid
		LEFT JOIN nuclidedata nd on s.id=nd.sampleid
		LEFT JOIN nuclidedataprop pr on s.id=pr.sampleid

		where s.projectid=7
		) x 
		PIVOT (max(nuclidevalue) for nuclidename in ([AM241_BQ_M3],[AM241_BQ_M3_mda],[AM241_BQ_M3_unc],[CS137_BQ_KG_DRY],[CS137_BQ_KG_DRY_mda],[CS137_BQ_KG_DRY_unc],[CS137_BQ_KG_WET],[CS137_BQ_KG_WET_mda],[CS137_BQ_KG_WET_unc],[CS137_BQ_M3],[CS137_BQ_M3_mda],[CS137_BQ_M3_unc],[H3_BQ_L],[H3_BQ_L_mda],[H3_BQ_L_unc],[PU239_240_BQ_M3],[PU239_240_BQ_M3_mda],[PU239_240_BQ_M3_unc],[RA226_BQ_FILTER],[RA226_BQ_FILTER_mda],[RA226_BQ_FILTER_unc],[RA226_BQ_M3],[RA226_BQ_M3_mda],[RA226_BQ_M3_unc],[RA228_BQ_FILTER],[RA228_BQ_FILTER_mda],[RA228_BQ_FILTER_unc],[RA228_BQ_M3],[RA228_BQ_M3_mda],[RA228_BQ_M3_unc],[SR90_BQ_M3],[SR90_BQ_M3_mda],[SR90_BQ_M3_unc])) AS nucl
		PIVOT (max(varvalue) for varname in ([SALINITY_PERMIL],[SAMPLECOUNT_NUMBER],[TEMPERATURE_CELSIUS],[WATERDEPTH_METER])) AS var
		PIVOT (max(propvalue) for propname in ([CS137_BQ_KG_DRY_instrument],[CS137_BQ_KG_DRY_lab],[CS137_BQ_KG_WET_lab],[CS137_BQ_M3_lab])) AS prop
		PIVOT (max(metavalue) for metaname in ([COORDINATEORIGIN],[LIMSNR],[LOCALITY],[SAMPLEDEPTH],[SAMPLEID],[SAMPLEPART],[SAMPLESUBTYPE],[SAMPLINGPROCEDURE],[SEA],[STATION],[VESSEL])) AS meta
GO
/****** Object:  View [dbo].[RAMEFjordtokt]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[RAMEFjordtokt] AS SELECT id, geometry::STGeomFromText(location, 4326) as location,latitude,longitude,dbo.ReturnAreaGeom(area) as area,reftime,samplestart,samplestop,parentsampleid,comment,sampletype,sampletypename,speciesid,speciesname,[SALINITY_PERMIL],[TEMPERATURE_CELSIUS],[WATERDEPTH_METER],[COORDINATEORIGIN],[SAMPLEDEPTH],[SAMPLESUBTYPE],[SEA],[STATION],[VESSEL],[CS137_BQ_KG_DRY],[CS137_BQ_KG_DRY_mda],[CS137_BQ_KG_DRY_unc],[CS137_BQ_M3],[CS137_BQ_M3_mda],[CS137_BQ_M3_unc],[CS137_BQ_KG_DRY_instrument],[CS137_BQ_M3_lab] FROM (
		SELECT s.id,s.location.STAsText() as location,s.location.STY as latitude,s.location.STX as longitude, s.areaid as area,s.reftime,s.samplestart,s.samplestop,s.parentsampleid,s.comment,s.sampletype,dbo.sampletypename(s.sampletype) as sampletypename,s.speciesid,dbo.speciesname(s.speciesid) as speciesname,vd.shortname as varname, vd.value as varvalue, md.shortname as metaname, md.value as metavalue,nd.shortname as nuclidename, nd.value as nuclidevalue,pr.shortname as propname, pr.value as propvalue
		FROM Sample s
		LEFT JOIN valuedata vd ON s.id=vd.sampleid
		LEFT JOIN metadata md on s.id=md.sampleid
		LEFT JOIN nuclidedata nd on s.id=nd.sampleid
		LEFT JOIN nuclidedataprop pr on s.id=pr.sampleid

		where s.projectid=8
		) x 
		PIVOT (max(nuclidevalue) for nuclidename in ([CS137_BQ_KG_DRY],[CS137_BQ_KG_DRY_mda],[CS137_BQ_KG_DRY_unc],[CS137_BQ_M3],[CS137_BQ_M3_mda],[CS137_BQ_M3_unc])) AS nucl
		PIVOT (max(varvalue) for varname in ([SALINITY_PERMIL],[TEMPERATURE_CELSIUS],[WATERDEPTH_METER])) AS var
		PIVOT (max(propvalue) for propname in ([CS137_BQ_KG_DRY_instrument],[CS137_BQ_M3_lab])) AS prop
		PIVOT (max(metavalue) for metaname in ([COORDINATEORIGIN],[SAMPLEDEPTH],[SAMPLESUBTYPE],[SEA],[STATION],[VESSEL])) AS meta
GO
/****** Object:  View [dbo].[RAMESkagerak]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[RAMESkagerak] AS SELECT id, geometry::STGeomFromText(location, 4326) as location,latitude,longitude,dbo.ReturnAreaGeom(area) as area,reftime,samplestart,samplestop,parentsampleid,comment,sampletype,sampletypename,speciesid,speciesname,[SALINITY_PERMIL],[TEMPERATURE_CELSIUS],[WATERDEPTH_METER],[COORDINATEORIGIN],[SAMPLEDEPTH],[SAMPLESUBTYPE],[SEA],[STATION],[VESSEL],[CS137_BQ_M3],[CS137_BQ_M3_mda],[CS137_BQ_M3_unc],[CS137_BQ_M3_lab] FROM (
		SELECT s.id,s.location.STAsText() as location,s.location.STY as latitude,s.location.STX as longitude, s.areaid as area,s.reftime,s.samplestart,s.samplestop,s.parentsampleid,s.comment,s.sampletype,dbo.sampletypename(s.sampletype) as sampletypename,s.speciesid,dbo.speciesname(s.speciesid) as speciesname,vd.shortname as varname, vd.value as varvalue, md.shortname as metaname, md.value as metavalue,nd.shortname as nuclidename, nd.value as nuclidevalue,pr.shortname as propname, pr.value as propvalue
		FROM Sample s
		LEFT JOIN valuedata vd ON s.id=vd.sampleid
		LEFT JOIN metadata md on s.id=md.sampleid
		LEFT JOIN nuclidedata nd on s.id=nd.sampleid
		LEFT JOIN nuclidedataprop pr on s.id=pr.sampleid

		where s.projectid=9
		) x 
		PIVOT (max(nuclidevalue) for nuclidename in ([CS137_BQ_M3],[CS137_BQ_M3_mda],[CS137_BQ_M3_unc])) AS nucl
		PIVOT (max(varvalue) for varname in ([SALINITY_PERMIL],[TEMPERATURE_CELSIUS],[WATERDEPTH_METER])) AS var
		PIVOT (max(propvalue) for propname in ([CS137_BQ_M3_lab])) AS prop
		PIVOT (max(metavalue) for metaname in ([COORDINATEORIGIN],[SAMPLEDEPTH],[SAMPLESUBTYPE],[SEA],[STATION],[VESSEL])) AS meta
GO
/****** Object:  View [dbo].[RAMEKomsomolets]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[RAMEKomsomolets] AS SELECT id, geometry::STGeomFromText(location, 4326) as location,latitude,longitude,dbo.ReturnAreaGeom(area) as area,reftime,samplestart,samplestop,parentsampleid,comment,sampletype,sampletypename,speciesid,speciesname,[SALINITY_PERMIL],[TEMPERATURE_CELSIUS],[WATERDEPTH_METER],[COORDINATEORIGIN],[LIMSNR],[SAMPLEDEPTH],[SAMPLEID],[SAMPLESUBTYPE],[SAMPLINGPROCEDURE],[SEA],[STATION],[VESSEL],[AM241_BQ_M3],[AM241_BQ_M3_mda],[AM241_BQ_M3_unc],[CS137_BQ_KG_DRY],[CS137_BQ_KG_DRY_mda],[CS137_BQ_KG_DRY_unc],[CS137_BQ_M3],[CS137_BQ_M3_mda],[CS137_BQ_M3_unc],[PU239_240_BQ_M3],[PU239_240_BQ_M3_mda],[PU239_240_BQ_M3_unc],[RA226_BQ_M3],[RA226_BQ_M3_mda],[RA226_BQ_M3_unc],[SR90_BQ_M3],[SR90_BQ_M3_mda],[SR90_BQ_M3_unc],[TC99_BQ_M3],[TC99_BQ_M3_mda],[TC99_BQ_M3_unc],[CS137_BQ_KG_DRY_lab],[CS137_BQ_M3_lab] FROM (
		SELECT s.id,s.location.STAsText() as location,s.location.STY as latitude,s.location.STX as longitude, s.areaid as area,s.reftime,s.samplestart,s.samplestop,s.parentsampleid,s.comment,s.sampletype,dbo.sampletypename(s.sampletype) as sampletypename,s.speciesid,dbo.speciesname(s.speciesid) as speciesname,vd.shortname as varname, vd.value as varvalue, md.shortname as metaname, md.value as metavalue,nd.shortname as nuclidename, nd.value as nuclidevalue,pr.shortname as propname, pr.value as propvalue
		FROM Sample s
		LEFT JOIN valuedata vd ON s.id=vd.sampleid
		LEFT JOIN metadata md on s.id=md.sampleid
		LEFT JOIN nuclidedata nd on s.id=nd.sampleid
		LEFT JOIN nuclidedataprop pr on s.id=pr.sampleid

		where s.projectid=11
		) x 
		PIVOT (max(nuclidevalue) for nuclidename in ([AM241_BQ_M3],[AM241_BQ_M3_mda],[AM241_BQ_M3_unc],[CS137_BQ_KG_DRY],[CS137_BQ_KG_DRY_mda],[CS137_BQ_KG_DRY_unc],[CS137_BQ_M3],[CS137_BQ_M3_mda],[CS137_BQ_M3_unc],[PU239_240_BQ_M3],[PU239_240_BQ_M3_mda],[PU239_240_BQ_M3_unc],[RA226_BQ_M3],[RA226_BQ_M3_mda],[RA226_BQ_M3_unc],[SR90_BQ_M3],[SR90_BQ_M3_mda],[SR90_BQ_M3_unc],[TC99_BQ_M3],[TC99_BQ_M3_mda],[TC99_BQ_M3_unc])) AS nucl
		PIVOT (max(varvalue) for varname in ([SALINITY_PERMIL],[TEMPERATURE_CELSIUS],[WATERDEPTH_METER])) AS var
		PIVOT (max(propvalue) for propname in ([CS137_BQ_KG_DRY_lab],[CS137_BQ_M3_lab])) AS prop
		PIVOT (max(metavalue) for metaname in ([COORDINATEORIGIN],[LIMSNR],[SAMPLEDEPTH],[SAMPLEID],[SAMPLESUBTYPE],[SAMPLINGPROCEDURE],[SEA],[STATION],[VESSEL])) AS meta
GO
/****** Object:  View [dbo].[RADIAC]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[RADIAC] AS SELECT id, geometry::STGeomFromText(location, 4326) as location,latitude,longitude,dbo.ReturnAreaGeom(area) as area,reftime,samplestart,samplestop,parentsampleid,comment,sampletype,sampletypename,speciesid,speciesname,[DOSE_GY_H],[SNOWDEPTH_METER],[COLLECTOR],[LOCALITY],[PRECIPOCCUR],[SAMPLEID] FROM (
		SELECT s.id,s.location.STAsText() as location,s.location.STY as latitude,s.location.STX as longitude, s.areaid as area,s.reftime,s.samplestart,s.samplestop,s.parentsampleid,s.comment,s.sampletype,dbo.sampletypename(s.sampletype) as sampletypename,s.speciesid,dbo.speciesname(s.speciesid) as speciesname,vd.shortname as varname, vd.value as varvalue, md.shortname as metaname, md.value as metavalue
		FROM Sample s
		LEFT JOIN valuedata vd ON s.id=vd.sampleid
		LEFT JOIN metadata md on s.id=md.sampleid
		
		

		where s.projectid=14
		) x 
		
		PIVOT (max(varvalue) for varname in ([DOSE_GY_H],[SNOWDEPTH_METER])) AS var
		
		PIVOT (max(metavalue) for metaname in ([COLLECTOR],[LOCALITY],[PRECIPOCCUR],[SAMPLEID])) AS meta
GO
/****** Object:  View [dbo].[RadioaktivitetGnagere]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[RadioaktivitetGnagere] AS SELECT id, geometry::STGeomFromText(location, 4326) as location,latitude,longitude,dbo.ReturnAreaGeom(area) as area,reftime,samplestart,samplestop,parentsampleid,comment,sampletype,sampletypename,speciesid,speciesname,[DRYWETRATIO_RATIO_DRY],[COLLECTOR],[LIMSNR],[LOCALITY],[MEASUREDDRYWET],[SAMPLEID],[SAMPLEPART],[CS137_BQ_KG_DRY],[CS137_BQ_KG_DRY_mda],[CS137_BQ_KG_DRY_unc],[CS137_BQ_KG_WET],[CS137_BQ_KG_WET_mda],[CS137_BQ_KG_WET_unc],[CS137_BQ_KG_DRY_instrument],[CS137_BQ_KG_DRY_lab],[CS137_BQ_KG_DRY_uncmeasure],[CS137_BQ_KG_WET_lab],[CS137_BQ_KG_WET_uncmeasure] FROM (
		SELECT s.id,s.location.STAsText() as location,s.location.STY as latitude,s.location.STX as longitude, s.areaid as area,s.reftime,s.samplestart,s.samplestop,s.parentsampleid,s.comment,s.sampletype,dbo.sampletypename(s.sampletype) as sampletypename,s.speciesid,dbo.speciesname(s.speciesid) as speciesname,vd.shortname as varname, vd.value as varvalue, md.shortname as metaname, md.value as metavalue,nd.shortname as nuclidename, nd.value as nuclidevalue,pr.shortname as propname, pr.value as propvalue
		FROM Sample s
		LEFT JOIN valuedata vd ON s.id=vd.sampleid
		LEFT JOIN metadata md on s.id=md.sampleid
		LEFT JOIN nuclidedata nd on s.id=nd.sampleid
		LEFT JOIN nuclidedataprop pr on s.id=pr.sampleid

		where s.projectid=15
		) x 
		PIVOT (max(nuclidevalue) for nuclidename in ([CS137_BQ_KG_DRY],[CS137_BQ_KG_DRY_mda],[CS137_BQ_KG_DRY_unc],[CS137_BQ_KG_WET],[CS137_BQ_KG_WET_mda],[CS137_BQ_KG_WET_unc])) AS nucl
		PIVOT (max(varvalue) for varname in ([DRYWETRATIO_RATIO_DRY])) AS var
		PIVOT (max(propvalue) for propname in ([CS137_BQ_KG_DRY_instrument],[CS137_BQ_KG_DRY_lab],[CS137_BQ_KG_DRY_uncmeasure],[CS137_BQ_KG_WET_lab],[CS137_BQ_KG_WET_uncmeasure])) AS prop
		PIVOT (max(metavalue) for metaname in ([COLLECTOR],[LIMSNR],[LOCALITY],[MEASUREDDRYWET],[SAMPLEID],[SAMPLEPART])) AS meta
GO
/****** Object:  View [dbo].[TjottaProsjektet]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[TjottaProsjektet] AS SELECT id, geometry::STGeomFromText(location, 4326) as location,latitude,longitude,dbo.ReturnAreaGeom(area) as area,reftime,samplestart,samplestop,parentsampleid,comment,sampletype,sampletypename,speciesid,speciesname,[CONDUCTIVITY_USIEMENS_CM],[CR_FRESHWATER_RATIO_DRY],[CR_SEAWATER_RATIO_DRY],[CR_SOIL_RATIO_DRY],[DRYWETRATIO_DIMLESS],[ELEVATION_METER],[LOI_PERCENT],[PH_DIMLESS],[SALINITY_PERMIL],[SAMPLECOUNT_NUMBER],[TEMPERATURE_CELSIUS],[WHOLELENGTH_CM],[WHOLEWEIGHT_GRAM],[AGE],[COLLECTOR],[SAMPLEID],[SAMPLEPART],[SAMPLESUBTYPE],[SEX],[CS_MG_KG_DRY],[CS_MG_KG_DRY_mda],[CS_MG_KG_DRY_unc],[CS_MG_KG_WET],[CS_MG_KG_WET_mda],[CS_MG_KG_WET_unc] FROM (
		SELECT s.id,s.location.STAsText() as location,s.location.STY as latitude,s.location.STX as longitude, s.areaid as area,s.reftime,s.samplestart,s.samplestop,s.parentsampleid,s.comment,s.sampletype,dbo.sampletypename(s.sampletype) as sampletypename,s.speciesid,dbo.speciesname(s.speciesid) as speciesname,vd.shortname as varname, vd.value as varvalue, md.shortname as metaname, md.value as metavalue,nd.shortname as nuclidename, nd.value as nuclidevalue
		FROM Sample s
		LEFT JOIN valuedata vd ON s.id=vd.sampleid
		LEFT JOIN metadata md on s.id=md.sampleid
		LEFT JOIN nuclidedata nd on s.id=nd.sampleid
		

		where s.projectid=16
		) x 
		PIVOT (max(nuclidevalue) for nuclidename in ([CS_MG_KG_DRY],[CS_MG_KG_DRY_mda],[CS_MG_KG_DRY_unc],[CS_MG_KG_WET],[CS_MG_KG_WET_mda],[CS_MG_KG_WET_unc])) AS nucl
		PIVOT (max(varvalue) for varname in ([CONDUCTIVITY_USIEMENS_CM],[CR_FRESHWATER_RATIO_DRY],[CR_SEAWATER_RATIO_DRY],[CR_SOIL_RATIO_DRY],[DRYWETRATIO_DIMLESS],[ELEVATION_METER],[LOI_PERCENT],[PH_DIMLESS],[SALINITY_PERMIL],[SAMPLECOUNT_NUMBER],[TEMPERATURE_CELSIUS],[WHOLELENGTH_CM],[WHOLEWEIGHT_GRAM])) AS var
		
		PIVOT (max(metavalue) for metaname in ([AGE],[COLLECTOR],[SAMPLEID],[SAMPLEPART],[SAMPLESUBTYPE],[SEX])) AS meta
GO
/****** Object:  View [dbo].[RadioaktivitetBaer]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[RadioaktivitetBaer] AS SELECT id, geometry::STGeomFromText(location, 4326) as location,latitude,longitude,dbo.ReturnAreaGeom(area) as area,reftime,samplestart,samplestop,parentsampleid,comment,sampletype,sampletypename,speciesid,speciesname FROM (
		SELECT s.id,s.location.STAsText() as location,s.location.STY as latitude,s.location.STX as longitude, s.areaid as area,s.reftime,s.samplestart,s.samplestop,s.parentsampleid,s.comment,s.sampletype,dbo.sampletypename(s.sampletype) as sampletypename,s.speciesid,dbo.speciesname(s.speciesid) as speciesname
		FROM Sample s
		
		
		
		

		where s.projectid=3
		) x 
		
		
		
		
GO
/****** Object:  View [dbo].[RadioaktivitetHusdyr]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[RadioaktivitetHusdyr] AS SELECT id, geometry::STGeomFromText(location, 4326) as location,latitude,longitude,dbo.ReturnAreaGeom(area) as area,reftime,samplestart,samplestop,parentsampleid,comment,sampletype,sampletypename,speciesid,speciesname FROM (
		SELECT s.id,s.location.STAsText() as location,s.location.STY as latitude,s.location.STX as longitude, s.areaid as area,s.reftime,s.samplestart,s.samplestop,s.parentsampleid,s.comment,s.sampletype,dbo.sampletypename(s.sampletype) as sampletypename,s.speciesid,dbo.speciesname(s.speciesid) as speciesname
		FROM Sample s
		
		
		
		

		where s.projectid=13
		) x 
		
		
		
		
GO
/****** Object:  View [dbo].[RadioaktivitetSau]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[RadioaktivitetSau] AS SELECT id, geometry::STGeomFromText(location, 4326) as location,latitude,longitude,dbo.ReturnAreaGeom(area) as area,reftime,samplestart,samplestop,parentsampleid,comment,sampletype,sampletypename,speciesid,speciesname FROM (
		SELECT s.id,s.location.STAsText() as location,s.location.STY as latitude,s.location.STX as longitude, s.areaid as area,s.reftime,s.samplestart,s.samplestop,s.parentsampleid,s.comment,s.sampletype,dbo.sampletypename(s.sampletype) as sampletypename,s.speciesid,dbo.speciesname(s.speciesid) as speciesname
		FROM Sample s
		
		
		
		

		where s.projectid=1
		) x 
		
		
		
		
GO
/****** Object:  View [dbo].[RAMESnitt]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[RAMESnitt] AS SELECT id, geometry::STGeomFromText(location, 4326) as location,latitude,longitude,dbo.ReturnAreaGeom(area) as area,reftime,samplestart,samplestop,parentsampleid,comment,sampletype,sampletypename,speciesid,speciesname FROM (
		SELECT s.id,s.location.STAsText() as location,s.location.STY as latitude,s.location.STX as longitude, s.areaid as area,s.reftime,s.samplestart,s.samplestop,s.parentsampleid,s.comment,s.sampletype,dbo.sampletypename(s.sampletype) as sampletypename,s.speciesid,dbo.speciesname(s.speciesid) as speciesname
		FROM Sample s
		
		
		
		

		where s.projectid=10
		) x 
		
		
		
		
GO
/****** Object:  View [dbo].[ValidData]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create view [dbo].[ValidData] as 
select shortname, attrtype, datatype, name, cast(decription as nvarchar(max)) as description from BasisPropertiesList
UNION
select shortname, 'METADATA','character',name, cast(description as nvarchar(max)) from MetadataList
UNION
select shortname, 'NUCLIDE','^[a-zA-Z]{1,2}[0-9]{1,3}m{0,1}\\_{0,1}[0-9]{0,3}\\#{0,1}[0-9]{0,9}$',name,NULL from NuclideList
UNION
select shortname, 'QUANTITY','numeric',name,cast(description as nvarchar(max)) from QuantityList
UNION
select cast(id as nvarchar),'CATEGORY','numeric',name,cast(description as nvarchar(max)) from SampleCatList
UNION
select shortname,'SAMPLETYPE','character',name, cast(description as nvarchar(max)) from SampletypeList
UNION
select cast(id as nvarchar), 'SPECIES','numeric',cast(species_no as nvarchar(max)),NULL from SpeciesList
UNION
select shortname, 'UNITS','character',cast(name as nvarchar(max)),cast(desciption as nvarchar(max)) from UnitList
GO
SET ANSI_PADDING ON

GO
/****** Object:  Index [NonClusteredIndex-20180403-093100]    Script Date: 11.04.2018 07:41:12 ******/
CREATE NONCLUSTERED INDEX [NonClusteredIndex-20180403-093100] ON [dbo].[GeoAreas]
(
	[objtype] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
/****** Object:  Index [NonClusteredIndex-20171113-090522]    Script Date: 11.04.2018 07:41:12 ******/
CREATE NONCLUSTERED INDEX [NonClusteredIndex-20171113-090522] ON [dbo].[Sample]
(
	[projectid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
SET ANSI_PADDING ON

GO
/****** Object:  Index [METADATA_id_sampleid]    Script Date: 11.04.2018 07:41:12 ******/
CREATE NONCLUSTERED INDEX [METADATA_id_sampleid] ON [dbo].[SampleMetadata]
(
	[metadataid] ASC
)
INCLUDE ( 	[sampleid],
	[value]) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
SET ANSI_PADDING ON

GO
/****** Object:  Index [Sample_Metadata_key_nonclust]    Script Date: 11.04.2018 07:41:12 ******/
CREATE NONCLUSTERED INDEX [Sample_Metadata_key_nonclust] ON [dbo].[SampleMetadata]
(
	[sampleid] ASC
)
INCLUDE ( 	[value],
	[metadataid]) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
/****** Object:  Index [NonClusteredIndex-20171113-085339]    Script Date: 11.04.2018 07:41:12 ******/
CREATE NONCLUSTERED INDEX [NonClusteredIndex-20171113-085339] ON [dbo].[SampleValue]
(
	[sampleid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
/****** Object:  Index [SAMPLEVALUE_quanity_nuclide_unit]    Script Date: 11.04.2018 07:41:12 ******/
CREATE NONCLUSTERED INDEX [SAMPLEVALUE_quanity_nuclide_unit] ON [dbo].[SampleValue]
(
	[quantityid] ASC,
	[nuclideid] ASC
)
INCLUDE ( 	[sampleid],
	[value],
	[unitid]) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
/****** Object:  Index [SampleValueIndex_id_unit_mda]    Script Date: 11.04.2018 07:41:12 ******/
CREATE NONCLUSTERED INDEX [SampleValueIndex_id_unit_mda] ON [dbo].[SampleValue]
(
	[nuclideid] ASC
)
INCLUDE ( 	[sampleid],
	[unitid],
	[mda_value]) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
/****** Object:  Index [IX_SpeciesList]    Script Date: 11.04.2018 07:41:12 ******/
CREATE NONCLUSTERED INDEX [IX_SpeciesList] ON [dbo].[SpeciesList]
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
ALTER TABLE [dbo].[ProjectTopics]  WITH CHECK ADD  CONSTRAINT [FK_ProjectTopics_Projects] FOREIGN KEY([projectid])
REFERENCES [dbo].[Projects] ([id])
GO
ALTER TABLE [dbo].[ProjectTopics] CHECK CONSTRAINT [FK_ProjectTopics_Projects]
GO
ALTER TABLE [dbo].[ProjectTopics]  WITH CHECK ADD  CONSTRAINT [FK_ProjectTopics_Topics] FOREIGN KEY([topicid])
REFERENCES [dbo].[TopicList] ([id])
GO
ALTER TABLE [dbo].[ProjectTopics] CHECK CONSTRAINT [FK_ProjectTopics_Topics]
GO
ALTER TABLE [dbo].[Sample]  WITH CHECK ADD  CONSTRAINT [FK__Sample__program__3E52440B] FOREIGN KEY([projectid])
REFERENCES [dbo].[Projects] ([id])
GO
ALTER TABLE [dbo].[Sample] CHECK CONSTRAINT [FK__Sample__program__3E52440B]
GO
ALTER TABLE [dbo].[Sample]  WITH CHECK ADD  CONSTRAINT [FK__Sample_areaid] FOREIGN KEY([areaid])
REFERENCES [dbo].[GeoAreas] ([ogr_fid])
GO
ALTER TABLE [dbo].[Sample] CHECK CONSTRAINT [FK__Sample_areaid]
GO
ALTER TABLE [dbo].[Sample]  WITH CHECK ADD  CONSTRAINT [FK_Sample_Sample] FOREIGN KEY([parentsampleid])
REFERENCES [dbo].[Sample] ([id])
GO
ALTER TABLE [dbo].[Sample] CHECK CONSTRAINT [FK_Sample_Sample]
GO
ALTER TABLE [dbo].[Sample]  WITH CHECK ADD  CONSTRAINT [FK_Sample_SampletypeList] FOREIGN KEY([sampletype])
REFERENCES [dbo].[SampletypeList] ([id])
GO
ALTER TABLE [dbo].[Sample] CHECK CONSTRAINT [FK_Sample_SampletypeList]
GO
ALTER TABLE [dbo].[Sample]  WITH CHECK ADD  CONSTRAINT [FK_Sample_SpeciesList] FOREIGN KEY([speciesid])
REFERENCES [dbo].[SpeciesList] ([id])
GO
ALTER TABLE [dbo].[Sample] CHECK CONSTRAINT [FK_Sample_SpeciesList]
GO
ALTER TABLE [dbo].[SampleMetadata]  WITH CHECK ADD  CONSTRAINT [FK__SampleMet__sampl__57DD0BE4] FOREIGN KEY([sampleid])
REFERENCES [dbo].[Sample] ([id])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[SampleMetadata] CHECK CONSTRAINT [FK__SampleMet__sampl__57DD0BE4]
GO
ALTER TABLE [dbo].[SampleMetadata]  WITH CHECK ADD  CONSTRAINT [FK_SampleMetadata_MetadataList] FOREIGN KEY([metadataid])
REFERENCES [dbo].[MetadataList] ([id])
GO
ALTER TABLE [dbo].[SampleMetadata] CHECK CONSTRAINT [FK_SampleMetadata_MetadataList]
GO
ALTER TABLE [dbo].[SampletypeList]  WITH CHECK ADD  CONSTRAINT [FK_SampletypeList_SampleCatList] FOREIGN KEY([samplecatid])
REFERENCES [dbo].[SampleCatList] ([id])
GO
ALTER TABLE [dbo].[SampletypeList] CHECK CONSTRAINT [FK_SampletypeList_SampleCatList]
GO
ALTER TABLE [dbo].[SampleValue]  WITH CHECK ADD  CONSTRAINT [fk_samplevalue_mdaunitid] FOREIGN KEY([mda_unitid])
REFERENCES [dbo].[UnitList] ([id])
GO
ALTER TABLE [dbo].[SampleValue] CHECK CONSTRAINT [fk_samplevalue_mdaunitid]
GO
ALTER TABLE [dbo].[SampleValue]  WITH CHECK ADD  CONSTRAINT [FK_SampleValue_NuclideList] FOREIGN KEY([nuclideid])
REFERENCES [dbo].[NuclideList] ([id])
GO
ALTER TABLE [dbo].[SampleValue] CHECK CONSTRAINT [FK_SampleValue_NuclideList]
GO
ALTER TABLE [dbo].[SampleValue]  WITH CHECK ADD  CONSTRAINT [fk_samplevalue_quantitu] FOREIGN KEY([quantityid])
REFERENCES [dbo].[QuantityList] ([id])
GO
ALTER TABLE [dbo].[SampleValue] CHECK CONSTRAINT [fk_samplevalue_quantitu]
GO
ALTER TABLE [dbo].[SampleValue]  WITH CHECK ADD  CONSTRAINT [fk_samplevalue_sampleid] FOREIGN KEY([sampleid])
REFERENCES [dbo].[Sample] ([id])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[SampleValue] CHECK CONSTRAINT [fk_samplevalue_sampleid]
GO
ALTER TABLE [dbo].[SampleValue]  WITH CHECK ADD  CONSTRAINT [fk_samplevalue_uncunitid] FOREIGN KEY([unc_unitid])
REFERENCES [dbo].[UnitList] ([id])
GO
ALTER TABLE [dbo].[SampleValue] CHECK CONSTRAINT [fk_samplevalue_uncunitid]
GO
ALTER TABLE [dbo].[SampleValue]  WITH CHECK ADD  CONSTRAINT [fk_samplevalue_unitid] FOREIGN KEY([unitid])
REFERENCES [dbo].[UnitList] ([id])
GO
ALTER TABLE [dbo].[SampleValue] CHECK CONSTRAINT [fk_samplevalue_unitid]
GO
ALTER TABLE [dbo].[SpeciesList]  WITH NOCHECK ADD  CONSTRAINT [FK_SpeciesList_HabitatList] FOREIGN KEY([habitatid])
REFERENCES [dbo].[HabitatList] ([id])
GO
ALTER TABLE [dbo].[SpeciesList] CHECK CONSTRAINT [FK_SpeciesList_HabitatList]
GO
ALTER TABLE [dbo].[SpeciesList]  WITH NOCHECK ADD  CONSTRAINT [FK_SpeciesList_SampletypeList] FOREIGN KEY([sampletypeid])
REFERENCES [dbo].[SampletypeList] ([id])
GO
ALTER TABLE [dbo].[SpeciesList] CHECK CONSTRAINT [FK_SpeciesList_SampletypeList]
GO
/****** Object:  StoredProcedure [dbo].[CreateProjectView]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE procedure [dbo].[CreateProjectView](@projectid NVARCHAR(MAX),@ViewName as NVARCHAR(MAX))  
AS   
BEGIN


	DECLARE @val AS NVARCHAR(MAX);
	DECLARE @val_1 AS NVARCHAR(MAX);
	DECLARE @val_2 AS NVARCHAR(MAX);
	DECLARE @val_3 AS NVARCHAR(MAX);
	DECLARE @val_4 AS NVARCHAR(MAX);

	DECLARE @nucl AS NVARCHAR(MAX);
	DECLARE @nucl_1 AS NVARCHAR(MAX);
	DECLARE @nucl_2 AS NVARCHAR(MAX);
	DECLARE @nucl_3 AS NVARCHAR(MAX);
	DECLARE @nucl_4 AS NVARCHAR(MAX);
	

	DECLARE @meta AS NVARCHAR(MAX);
	DECLARE @meta_1 AS NVARCHAR(MAX);
	DECLARE @meta_2 AS NVARCHAR(MAX);
	DECLARE @meta_3 AS NVARCHAR(MAX);
	DECLARE @meta_4 AS NVARCHAR(MAX);

	DECLARE @prop AS NVARCHAR(MAX);
	DECLARE @prop_1 AS NVARCHAR(MAX);
	DECLARE @prop_2 AS NVARCHAR(MAX);
	DECLARE @prop_3 AS NVARCHAR(MAX);
	DECLARE @prop_4 AS NVARCHAR(MAX);


	DECLARE @query AS NVARCHAR(MAX);

	if object_id(@ViewName,'v') is not null
		execute('DROP VIEW '+ @ViewName)

	SET @val = STUFF((SELECT * FROM (
	SELECT distinct ','+QUOTENAME(rtrim(shortname)) as TEST FROM valuedata where projectid=@projectid 
	) AS K
	 FOR XML PATH(''), TYPE
	).value('.', 'NVARCHAR(MAX)'),1,1,'');

	SET @meta = STUFF((SELECT * FROM (
	 SELECT distinct ','+QUOTENAME(rtrim(ml.shortname)) as test FROM SampleMetadata sm, MetadataList ml, Sample S where sm.sampleid=s.id and ml.id = sm.metadataid and s.projectid=@projectid
	) AS meta

	            FOR XML PATH(''), TYPE
	            ).value('.', 'NVARCHAR(MAX)') 
	        ,1,1,'');


	SET @nucl = STUFF((SELECT * FROM (
	SELECT distinct ','+QUOTENAME(rtrim(shortname)) as TEST FROM nuclidedata where projectid=@projectid
	) AS K
	 FOR XML PATH(''), TYPE
	).value('.', 'NVARCHAR(MAX)'),1,1,'');

	SET @prop = STUFF((SELECT * FROM (
	SELECT distinct ','+QUOTENAME(rtrim(shortname)) as TEST FROM nuclidedataprop where projectid=@projectid
	) AS K
	 FOR XML PATH(''), TYPE
	).value('.', 'NVARCHAR(MAX)'),1,1,'');

	if (@val is not null) 
		begin
			set @val_1 = ','+@val
			set @val_2 = 'PIVOT (max(varvalue) for varname in ('+@val+')) AS var'
			set @val_3 = 'LEFT JOIN valuedata vd ON s.id=vd.sampleid'
			set @val_4 = ',vd.shortname as varname, vd.value as varvalue' 	
		end
	ELSE
		begin
			set @val_1 = ''
			set @val_2 = '' 	
			set @val_3 = '' 	
			set @val_4 = '' 	
		end

	if (@nucl is not null) 
		begin
			set @nucl_1 = ','+@nucl
			set @nucl_2 = 'PIVOT (max(nuclidevalue) for nuclidename in ('+@nucl+')) AS nucl' 	
			set @nucl_3 = 'LEFT JOIN nuclidedata nd on s.id=nd.sampleid'
			set @nucl_4 = ',nd.shortname as nuclidename, nd.value as nuclidevalue'
		end
	ELSE
		begin
			set @nucl_1 = ''
			set @nucl_2 = '' 	
			set @nucl_3 = '' 	
			set @nucl_4 = '' 	
		end

	if (@prop is not null) 
		begin
			set @prop_1 = ','+@prop
			set @prop_2 = 'PIVOT (max(propvalue) for propname in ('+@prop+')) AS prop' 	
			set @prop_3 = 'LEFT JOIN nuclidedataprop pr on s.id=pr.sampleid'
			set @prop_4 = ',pr.shortname as propname, pr.value as propvalue'
		end
	ELSE
		begin
			set @prop_1 = ''
			set @prop_2 = '' 	
			set @prop_3 = '' 	
			set @prop_4 = '' 	
		end

	if (@meta is not null) 
		begin
			set @meta_1 = ','+@meta
			set @meta_2 = 'PIVOT (max(metavalue) for metaname in ('+@meta+')) AS meta'	
			set @meta_3 =	'LEFT JOIN metadata md on s.id=md.sampleid'
			set @meta_4 = ', md.shortname as metaname, md.value as metavalue' 

		end
	ELSE
		begin
			set @meta_1 = ''
			set @meta_2 = '' 	
			set @meta_3 = '' 	
			set @meta_4 = '' 	
		end

	set @query = 'CREATE VIEW dbo.'+@ViewName+' AS SELECT id, geometry::STGeomFromText(location, 4326) as location,latitude,longitude,dbo.ReturnAreaGeom(area) as area,reftime,samplestart,samplestop,parentsampleid,comment,sampletype,sampletypename,speciesid,speciesname'+@val_1+@meta_1+@nucl_1+@prop_1+' FROM (
		SELECT s.id,s.location.STAsText() as location,s.location.STY as latitude,s.location.STX as longitude, s.areaid as area,s.reftime,s.samplestart,s.samplestop,s.parentsampleid,s.comment,s.sampletype,dbo.sampletypename(s.sampletype) as sampletypename,s.speciesid,dbo.speciesname(s.speciesid) as speciesname'+@val_4+@meta_4+@nucl_4+@prop_4+'
		FROM Sample s
		'+@val_3+'
		'+@meta_3+'
		'+@nucl_3+'
		'+@prop_3+'

		where s.projectid='+@projectid+'
		) x 
		'+@nucl_2+'
		'+@val_2+'
		'+@prop_2+'
		'+@meta_2+''

	execute(@query);
END

GO
/****** Object:  StoredProcedure [dbo].[UpdateAllProjectViews]    Script Date: 11.04.2018 07:41:12 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create procedure [dbo].[UpdateAllProjectViews] 
AS
BEGIN
	DECLARE @myId int;
	DECLARE @myName nvarchar(60);
	DECLARE myCursor CURSOR FORWARD_ONLY FOR
		SELECT id, ViewName FROM Projects where viewname is not null
	OPEN myCursor;

	FETCH NEXT FROM myCursor INTO @myId, @myName;
	WHILE @@FETCH_STATUS = 0 BEGIN
    EXECUTE dbo.CreateProjectView @myId, @myName;
    FETCH NEXT FROM myCursor INTO @myId, @myName;
	END;
	CLOSE myCursor;
	DEALLOCATE myCursor;
END
GO
SET ARITHABORT ON
SET CONCAT_NULL_YIELDS_NULL ON
SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
SET ANSI_PADDING ON
SET ANSI_WARNINGS ON
SET NUMERIC_ROUNDABORT OFF

GO
/****** Object:  Index [ogr_dbo_kommuner_ogr_geometry_sidx]    Script Date: 11.04.2018 07:41:12 ******/
CREATE SPATIAL INDEX [ogr_dbo_kommuner_ogr_geometry_sidx] ON [dbo].[GeoAreas]
(
	[ogr_geometry]
)USING  GEOMETRY_GRID 
WITH (BOUNDING_BOX =(-99551.2, 6426050, 1121940, 7962740), GRIDS =(LEVEL_1 = MEDIUM,LEVEL_2 = MEDIUM,LEVEL_3 = MEDIUM,LEVEL_4 = MEDIUM), 
CELLS_PER_OBJECT = 16, PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
USE [master]
GO
ALTER DATABASE [DataArkiv] SET  READ_WRITE 
GO
