create table ene (
	-- id bigint(8) primary key not null auto_increment,
        --
	-- Time period
	ano_trimestre smallint(2),  -- Year of data (corresponds to the middle month), 2010 to 2019
	mes_central tinyint(1),  -- Middle month of the trimester of data, 1 to 12
	ano_encuesta smallint(2),  -- Year of survey (corresponds to the middle month), 2010 to 2019
	mes_encuesta tinyint(1),  -- Middle month of the trimester of survey, 1 to 12
        --
	-- Household identification
	region tinyint(1),  -- Region number on the base of 16 regions including Ñuble (Ref *1)
	region_15 tinyint(1),  -- Region number on the base of 15 regions (Ref *2)
	estrato smallint(2),  -- Geographical stratum codes based on commune + urban/rural location (Ref *3)
	estrato_15 smallint(2),  -- Same as above, but based on 15 regions (Ref *4)
	estrato_unico bigint(8), -- ?? Appears in 2020 data, undocumented values
	tipo tinyint(1),  -- Stratum type: city, urban, rural (Ref *5)
	r_p_c int(4),  -- Unique 'Region - Province - Commune' code assigned by Regional Development Subsecretary
                    -- http://www.subdere.cl/sites/default/files/documentos/articles-73111_recurso_2.pdf (Ref *6)
	r_p_c_15 int(4),  -- Same as above, but based on 15 regions (Ref *7)
	id_identificacion int(4),  -- Unique household id
	id_directorio int(4),  -- Unique ID for block (urban areas) or section (rural areas)
	conglomerado bigint(8), -- Replaces id_directorio from 2020-01
	id_upm bigint(8), -- Unique identifier for primary sampling unit (UPM)
	hogar tinyint(1),  -- Number of household inside the living place
        --
	-- Person identification
	idrph int(4),  -- Unique person ID
	nro_linea bigint(8), -- ???
	edad smallint(2),  -- Age, 999 - unknown
	sexo tinyint(1),  -- Sex: 1 - male, 2 - female (Ref *8)
	parentesco tinyint(1),  -- Relationship to the head of the household (Ref *9)
	curso tinyint(1),  -- Last approved grade of education
	nivel smallint(2),  -- Education level (Ref *10), 999 - no data
	termino_nivel tinyint(1),  -- If the the education level was finished: 1 - yes, 2 - no
	est_conyugal tinyint(1),  -- Marital status (Ref *11)
	proveedor tinyint(1),  -- Is the person an economic provider of the household:
	                                -- 0 - not a provider, 1 - primary provider, other values up to 9 are possible
	nacionalidad smallint(2),  -- Nationality (Ref *12)
        --
	-- Job situation during the last week
	-- a1, a2, a3, a4, a5, a7: 1- yes, 2 - no
	a1 tinyint(1),  -- During the last week, did you work at least 1 hour? Y/N
	a2 tinyint(1),  -- Did you make any business or been self-employed? Y/N
	a3 tinyint(1),  -- Are you receiving any payment for the activity a1 or a2? Y/N
	a4 tinyint(1),  -- Did you work for a business belonging to your family member? Y/N
	a5 tinyint(1),  -- If you didn't work the last week, did you have any formal employment? Y/N
	a6 tinyint(1),  -- What is the reason why you didn't work during the last week? (Ref *13)
	a6_orig tinyint(1),  -- What is the reason why you didn't work during the last week? (Ref *13) (same as a6)
	a6_otro text,  -- Other reasons of not working, with a6='other'...
	a6_otro_covid tinyint(1),  -- Can the reason you didn't work be associated to COVID-19 pandemics, 1 - yes, 0 - no
	        -- a6_otro_covid is available since 2020-03 report
	a7 tinyint(1),  -- During the period you're not working, are you receiving salary or profits?
	a8 tinyint(1),  -- In what period do you expect to get back to work? Is it less than 4 weeks? (Ref *14)
	        -- 1 - less than 4 weeks, 2 - more than 4 weeks, 3 - don't know
        --
	-- Employment characteristics
	b1 tinyint(1),  -- Occupation group according to International Uniform Classification of Occupations (Ref *15)
	b1_88 tinyint(1),  -- ???
	b2 tinyint(1),  -- Did you work as: 1 - self-employed or business owner, 2 - employed, 3 - for a family member's business (Ref *16)
	b3 tinyint(1),  -- For this work you receive: 1 - salary o wage, 2 - money withdrawals, 3 - merchandise withdrawals, 4 - nothing (Ref *17)
	b4 tinyint(1),  -- At this work, do you employ persons for business or activity, excluding not paid family members? Y/N
	b5 tinyint(1),  -- The company, business or institution where your worked, is: 1 - state-owned, 2 - private, 3 - private home (Ref *18)
	b6 tinyint(1),  -- Your work in this private home is: 1 - live-out domestic service, 2 - live-in, 3 - other (Ref *19)
        --
	-- Values: 1, 2, 3, 88 and 99
	b7_1 tinyint(1),  -- = b7b_1 ??
	b7_2 tinyint(1),  -- = b7b_2 ??
	b7_3 tinyint(1),  -- = b7a_1 ??
	b7_4 tinyint(1),  -- = b7a_1 ??
	b7_5 tinyint(1),  -- = b7a_3 ??
	b7_6 tinyint(1),  -- = b7b_3 ??
	b7_7 tinyint(1),  -- = b7b_4 ??
        --
	-- b7X_X is collected since 2017-08
	-- Answers: 1 - yes, 2 - no, 88 - don't know, 99 - no answer
	b7a_1 tinyint(1),  -- Does your employer make contributions for you to a pension fund?
	b7a_2 tinyint(1),  -- Does your employer make contributions for you to the healthcare system?
	b7a_3 tinyint(1),  -- Does your employer make contributions for you to the unemployment fund?
	b7b_1 tinyint(1),  -- At this job, do you have the right to paid yearly vacations?
	b7b_2 tinyint(1),  -- At this job, do you have the right to a paid sick leave?
	b7b_3 tinyint(1),  -- At this job, do you have the right for maternity/paternity leave?
	b7b_4 tinyint(1),  -- At this job, do you have the right for employer-paid nursery?
        --
	b8 tinyint(1),  -- At this job, do you have a formal written contract? Y/N
	b9 tinyint(1),  -- Is the duration of the contract for a limited time? Y/N (1 - fixed term, 2 - indefinite) (Ref *20)
	b10 tinyint(1),  -- If you have a fixed term contract, the term is due to: (Ref *21)
	b11 tinyint(1),  -- Payment conditions: (Ref *22)
	b12 tinyint(1),  -- Your job contract is with: (Ref *23)
	b13 smallint(2),  -- Obsolete, similar to b13_rev4cl_caenes (different codes), available till 2016-11 (Ref *24)
	b13_rev4cl_caenes tinyint(1),  -- Economic activity of the company WHICH PAYS to the person according to CAENES (Ref *25)
	b14 smallint(2),  -- Obsolete, similar to b13_rev4cl_caenes (different codes), available till 2016-11 (Ref *24)
	b14_rev4cl_caenes tinyint(1),  -- Economic activity of the company WHERE THE PERSON WORKS you according to CAENES (Ref *25)
	b15_1 tinyint(1),  -- Number of employees of the company (direct employee), range, country wide: (Ref *26)
	b15_2 smallint(2),  -- If less than 10 employees, exact number; 999 - doesn't know
	b16 tinyint(1),  -- The place where you worked during the last week (Ref *27), number 1 to 9
	b16_orig tinyint(1),  -- The place where you worked during the last week (Ref *27), number 1 to 9 (same values as b16)
	b16_otro text,  -- Other place of work with b16=9
	b16_otro_covid tinyint(1),  -- Can the place of your work be associated to COVID-19 pandemics, 1 - yes, 0 - no
	        -- b16_otro_covid is available since 2020-03 report
	b17_mes smallint(2),  -- Job starting month 1 to 12, 999 - unknown
	b17_ano smallint(2),  -- Job starting year, 9999 - unknown
	b18_region tinyint(1),  -- Job location, region
	b18_varias smallint(2),  -- Job location in more than 1 commune? 1 - yes, 2 - no
	b18_codigo int(4),  -- Job location, commune code (Ref *6)
	b19 tinyint(1),  -- During the last week, did you have any side employment? 1 - yes, 2 - no
        --
	-- Employer registration in SII (Internal revenue and tax service) and accounting
	-- i* added on 2017-08
	-- Answers: 1 - yes, 2 - no, 88 - don't know, 99 - no answer
	i1 tinyint(1),  -- For dependent employees:
	        -- Is the company registered in SII and has respective permissions (inicio de actividades)? (Ref *28)
	i2 tinyint(1),  -- For dependent employees: Does the company employ an accountant o have accounting office? Y/N
	i3 tinyint(1),  -- For dependent employees: Business name: (Ref *29)
	i3_v tinyint(1),  -- Is the business name provided is a verified name: 0 - no, 1- yes
	i4 tinyint(1),  -- For independent employees: is the employer registered in SII? Y/N
	i5 tinyint(1),  -- For independent employees: your employer is: (Ref *30)
	i6 tinyint(1),  -- For independent employees: Your employer's accounting: (Ref *31)
	i7 tinyint(1),  -- Your employees accounting system, allows separation of business and personal expenses? Y/N
        --
	-- Work hours
	c1 tinyint(1),  -- Working day duration: 1 - full time, 2 - part time (do you work full day Y/N) (Ref *37)
	c2_1_1 smallint(2),  -- Main job: daily hours you typically work? Number or 999 - don't know
	c2_1_2 smallint(2),  -- Main job: days per week you typically work? Number or 999 - don't know
	c2_1_3 smallint(2),  -- Main job: weekly hours you typically work? Number or 999 - don't know
	c2_2_1 smallint(2),  -- Second job: daily hours you typically work? Number or 999 - don't know
	c2_2_2 smallint(2),  -- Second job: days per week you typically work? Number or 999 - don't know
	c2_2_3 smallint(2),  -- Second job: weekly hours you typically work? Number or 999 - don't know
	c3_1 smallint(2),  -- Main job: daily hours contracted or agreed? Number or 999 - don't know
	c3_2 smallint(2),  -- Main job: days per week contracted or agreed? Number or 999 - don't know
	c3_3 smallint(2),  -- Main job: weekly hours contracted or agreed? Number or 999 - don't know
	c4 tinyint(1),  -- Are you getting paid extra hours on your main job? 1 - yes, 2 - no
	c5 tinyint(1),  -- During the last week, did you work more hours than usual on your main job (whether paid or not paid)? Y/N
	c6 smallint(2),  -- How many hours more than usual did you work the last week on your main job? Number or 999 - don't know
	c7 tinyint(1),  -- During the last week, did you work less hours than usual on your main job (whether paid or not paid)? Y/N
	c8 smallint(2),  -- How many hours less than usual did you work the last week on your main job? Number or 999 - don't know
	c9 tinyint(1),  -- What is the main reason your worked different number of hours than usual during the last week? (Ref *32)
	c9_orig tinyint(1),  -- What is the main reason your worked different number of hours than usual during the last week? (Ref *32) (same values as c9)
	c9_otro text,  -- Another reason for different hours (with c9=20)
	c9_otro_covid tinyint(1),  -- Can the reason in c9 be associated to COVID-19 pandemics, 1 - yes, 0 - no
	        -- c9_otro_covid is available since 2020-03 report
	c10 tinyint(1),  -- If depended only on you, would you work more hours than usual? Y/N
	c11 tinyint(1),  -- If you've been offered, would you be available to work more hours weekly? (Ref *33)
	c12 tinyint(1),  -- What is the reason you don't work more hours? (Ref *34)
	c13 tinyint(1),  -- Would you work less hours even if getting less money? Y/N
        --
	-- Job search
	-- 1 - yes, 2 - no; e3_XX all not null values treat as yes
	e1 tinyint(1),  -- Have you done anything to find a job during the last 12 months? Y/N
	e2 tinyint(1),  -- During the last 4 weeks, have you tried to find a job or done anything to create your own business? Y/N
	e3_1 tinyint(1),  -- Job search: sent CV to potential employers? Y/N
	e3_2 tinyint(1),  -- Job search: contacted employers directly? Y/N
	e3_3 tinyint(1),  -- Job search: asked friends/family members for a recommendation or job leads? Y/N
	e3_4 tinyint(1),  -- Job search: looked at the vacations published (newspapers, internet, etc.) Y/N
	e3_5 tinyint(1),  -- Job search: registered or checked openings with the municipal employment office? Y/N
	e3_6 tinyint(1),  -- Job search: took steps to start working as self-employed Y/N
	e3_7 tinyint(1),  -- Job search: was looking for customers and orders? Y/N
	e3_8 tinyint(1),  -- Job search: published your own announcements? Y/N
	e3_9 tinyint(1),  -- Job search: took part in a test or job interview? Y/N
	e3_10 tinyint(1),  -- Job search: consulted employment agencies? Y/N
	e3_11 tinyint(1),  -- Job search: updated your CV published? Y/N
	e3_12 tinyint(1),  -- Job search: done nothing? Y/N
	e3_total tinyint(1),  -- Job search: total number of actions to find a job
	e4 tinyint(1),  -- What is the main reason you're looking for another job? (Ref *35)
	e5 tinyint(1),  -- Till the last week, when was the last time you were looking for a job? (Ref *36)
	e5_dia smallint(2),  -- The day of the last job search, 999 - don't know
	e5_sem smallint(2),  -- Week of the month of the last job search (1 to 5, 999 - don't know)
	e5_mes smallint(2),  -- Month of the last job search, 999 - don't know
	e5_ano smallint(2),  -- Year of the last job search, 999 - don't know
	e6_mes smallint(2),  -- From which month you were looking for a job? (1 to 12, 999 - don't know)
	e6_ano smallint(2),  -- From which year you were looking for a job? 999 - don't know
	e7 tinyint(1),  -- What type of employment are you looking for? 1 - full time, 2 - part time, 3 - any (Ref *37)
	e8 tinyint(1),  -- What type of employment are you looking for? (Ref *38)
	e9 tinyint(1),  -- What is the reason you were not looking for a job during the last 4 weeks? (Ref *39)
	e9_orig tinyint(1),  -- What is the reason you were not looking for a job during the last 4 weeks? (Ref *39) (Same values as e9)
	e9_otro text,  -- Another reason for not looking (with e9=22)
	e9_otro_covid tinyint(1),  -- Can the reason in e9 be associated to COVID-19 pandemics, 1 - yes, 0 - no
	        -- e9_otro_covid is available since 2020-03 report
	e10 tinyint(1),  -- During the last 4 weeks, you either took steps to start your own business/self-employment,
	        -- or reached an agreement or signed a contract to start working? Y/N
	e11 tinyint(1),  -- If you found a job during the last week, would you be available to start the next Monday? Y/N
	e12 tinyint(1),  -- Why you won't be available to start the new job the next Monday? (Ref *40)
	e12_orig tinyint(1),  -- Why you won't be available to start the new job the next Monday? (Ref *40) (Same values as e12)
	e12_otro text,  -- Another reason for not looking (with e12=13)
	e12_otro_covid tinyint(1),  -- Can the reason in e12 be associated to COVID-19 pandemics, 1 - yes, 0 - no
	        -- e12_otro_covid is available since 2020-03 report
	e13 tinyint(1),  -- Were you employed or self-employed in the past for at least 1 month (previous employment)? Y/N
	e14_mes smallint(2),  -- Till which month were you working in your last employment or self-employment? (1 to 12 or 999 - don't know)
	e14_ano smallint(2),  -- Till which year were you working in your last employment or self-employment? Year or 999 - don't know
	e15_meses smallint(2),  -- How long (in months) were you employed at this job? Number of months or 999 - don't know
	e15_anos smallint(2),  -- How long (in years) were you employed at this job? Number of years or 999 - don't know
	e15_ano smallint(2),  -- ???
	e16 tinyint(1),  -- Employment group at the last employment (Ref *15)
	e16_88 tinyint(1),  -- ???
	e17 tinyint(1),  -- What was your role at this employment? (Ref *41)
	e18 smallint(2),  -- Obsolete, similar to e18_rev4cl_caenes (different codes), available till 2016-11 (Ref *24)
	e18_rev4cl_caenes tinyint(1),  -- Economic activity of this previous employment according to CAENES (Ref *25)
	e19 tinyint(1),  -- Why did you leave the previous employment? (Ref *42)
	e19_otro text,  -- Other reason not included in e19
    --
	-- Final section and resulting variables
	cae_general tinyint(1),  -- General condition of economic activity (Ref *43)
	cae_especifico tinyint(1),  -- Specific condition of economic activity (Ref *44)
	categoria_ocupacion tinyint(1),  -- Occupation category according to CISE (Ref *41)
	habituales smallint(2),  -- Usually worked hours per week, 999 - no data
	efectivas smallint(2),  -- Actually worked hours during the last week, 999 - no data
	cine smallint(2),  -- Education level according to International Education Level Classification (Ref *45)
	r_p_rev4cl_caenes tinyint(1),  -- Economic activity of the employer, or the company belonging
	        -- to the surveyed person according to CAENES (Ref *25)
	sector tinyint(1),  -- Employed according to sector: 1 - formal employment, 2 - informal employment, 3 - private home employment (Ref *46)
	ocup_form tinyint(1),  -- Formality of employment: 1 - formal, 2 - informal
	activ tinyint(1),  -- Activity condition: 1 - employed, 2 - unemployed, 3 - beyond workforce (Ref *47)
	tramo_edad tinyint(1),  -- Age range steps of 5: 1 - 15 to 19, 2 - 20 to 25, etc, 12 - 70+ years
	fact float(4),  -- Quarterly expansion factor
	fact_cal float(4),  -- Calibrated quarterly expansion factor (new)
	b11_proxy tinyint, -- Are you being paid with a paycheck, fee slip, money receipt? Y/N (replaces b11)
    --
    -- Additional variables starting from 2019-12
    mercado tinyint(1), -- 0/1
    s_formal tinyint(1), -- 0/1
    s_informal tinyint(1), -- 0/1
    s_hogares tinyint(1), -- 0/1
    ocup_proxy tinyint(1), -- 0/1
    o_formal tinyint(1), -- 0/1
    o_informal tinyint(1), -- 0/1
    p_ocupada tinyint(1), -- 0/1
    publico tinyint(1), -- 0/1
    privado tinyint(1) -- 0/1
)
